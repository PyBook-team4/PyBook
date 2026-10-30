# services/recommend_service.py

# 도서 추천 서비스 (콘텐츠 기반 추천 + 코사인 유사도)
# [핵심 아이디어]
#   1. 모든 도서를 "텍스트(장르 + 키워드 + 제목 + 저자)"로 만든 뒤 숫자 벡터로 바꾼다. (TF-IDF)
#   2. 회원의 취향도 같은 방식으로 벡터로 만든다.
#        - 관심분야 (예: "문학 종교")
#        - 읽은 책들의 벡터 (평점이 높을수록 크게 반영)
#        - 직접 쓴 20자 이상 리뷰 (무엇이 좋았는지가 드러남)
#   3. "회원 취향 벡터"와 "아직 안 읽은 책 벡터" 사이의 코사인 유사도를 계산해
#      값이 큰(=방향이 비슷한) 책부터 추천한다.
#
# [코사인 유사도란?]
#   두 벡터가 가리키는 "방향"이 얼마나 비슷한지를 0 ~ 1 사이 값으로 나타낸 것.
#   1에 가까울수록 비슷하고, 0이면 공통점이 없다는 뜻.
#   (TF-IDF 값은 음수가 없어서 결과도 0 ~ 1 사이)
#
# [단계별 추천] 데이터가 적을수록 추천이 부정확하므로, 쌓인 정보에 따라 방식을 나눈다
#   - 관심분야도, 읽은 책도 없음   → "popular" : 평점 높은 인기 도서
#   - 리뷰 5개 미만               → "basic"   : 관심분야 + 읽은 책(평점)만 반영
#   - 리뷰 5개 이상               → "full"    : 관심분야 + 읽은 책 + 리뷰까지 모두 반영
#
# [이 파일은 화면 출력(print)이나 입력(input)을 하지 않고 결과만 반환한다]
#   → 출력은 views/user_view.py 의 _handle_recommend() 가 담당
# ============================================================

from utils.file_handler import load_json

# 데이터 파일 경로
BOOKS_FILE = "data/books.json"
LOANS_FILE = "data/loans.json"
RECORDS_FILE = "data/records.json"
MEMBERS_FILE = "data/members.json"

# 리뷰를 취향에 반영하는 기준 (반납 시 리뷰 포인트 기준과 동일하게 20자)
REVIEW_MIN_LENGTH = 20
# 이 점수 이상을 준 책만 "좋아한 책"으로 보고 취향에 반영 (2점 이하는 싫어한 책이므로 제외)
LIKED_MIN_RATING = 3
# 평점을 남기지 않은 책은 보통(3점)으로 간주
DEFAULT_RATING = 3
# 리뷰 한 개가 취향에 미치는 비중 (읽은 책 1권이 최대 1.0이므로 그보다 조금 작게)
REVIEW_WEIGHT = 0.7
# 관심분야가 취향에 미치는 비중
INTEREST_WEIGHT = 1.0
# 리뷰까지 반영하는 "full" 추천을 시작하는 리뷰 개수 (이보다 적으면 리뷰는 반영하지 않음)
REVIEW_GOAL = 5


def _book_text(book: dict) -> str:
    
    genre = book.get("genre", "")
    keywords = book.get("keywords", "")
    title = book.get("title", "")
    author = book.get("author", "")
    return f"{genre} {genre} {keywords} {title} {author}"

#회원가입 시 관심분야(interest)를 설정하지 않고 아직 읽은 책이 하나도 없는 경우 
#
def _popular_books(books: list, exclude_ids: set, top_n: int) -> list[dict]:

    candidates = [b for b in books if b.get("id") not in exclude_ids]
    candidates.sort(key=lambda b: b.get("rating") or 0, reverse=True)
    return [
        {"book": b, "score": None, "reason": "평점이 높은 인기 도서예요"}
        for b in candidates[:top_n]
    ]


def _is_usable_review(record: dict) -> bool:

    review = (record.get("review") or "").strip()
    rating = record.get("rating")
    if len(review) < REVIEW_MIN_LENGTH:
        return False
    if rating is not None and rating < LIKED_MIN_RATING:
        return False
    return True


def recommend_for_user(user_id: int, top_n: int = 5) -> dict:

    
    from scipy.sparse import vstack                                   
    from sklearn.feature_extraction.text import TfidfVectorizer      
    from sklearn.metrics.pairwise import cosine_similarity            

    # ------------------------------------------------------------
    # 0. 데이터 불러오기
    # ------------------------------------------------------------
    books = load_json(BOOKS_FILE)
    loans = load_json(LOANS_FILE)
    records = load_json(RECORDS_FILE)
    members = load_json(MEMBERS_FILE)

    if not books:
        return {"items": [], "mode": "popular", "review_count": 0, "review_goal": REVIEW_GOAL}

    member = next((m for m in members if m.get("user_id") == user_id), None)
    interests = []
    if member and isinstance(member.get("interest"), list):
        interests = member["interest"]            # 예: ["문학", "종교"]

    # 내가 반납 완료한 책(=읽은 책)과 지금 대출 중인 책의 id
    my_loans = [loan for loan in loans if loan.get("user_id") == user_id]
    read_ids = {loan.get("book_id") for loan in my_loans if loan.get("status") == "반납완료"}
    borrowing_ids = {loan.get("book_id") for loan in my_loans if loan.get("status") == "대출중"}

    # 읽은 책과 대출 중인 책은 추천하지 않음
    exclude_ids = read_ids | borrowing_ids

    # 내가 남긴 평점/리뷰 기록
    my_records = [r for r in records if r.get("user_id") == user_id]

    # 추천에 쓸 수 있는 리뷰만 골라냄 → 개수로 추천 단계(basic / full)를 정함
    usable_reviews = [r for r in my_records if _is_usable_review(r)]
    review_count = len(usable_reviews)
    mode = "full" if review_count >= REVIEW_GOAL else "basic"


     # 1. 도서 텍스트 → TF-IDF 벡터
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 3))
    book_matrix = vectorizer.fit_transform([_book_text(b) for b in books])
    # book_matrix: (도서 수 × 글자조각 수) 크기의 행렬. i번째 행 = i번째 도서의 벡터

    # 도서 id → book_matrix 의 행 번호
    id_to_row = {b.get("id"): i for i, b in enumerate(books)}

    # 2. 회원 취향 벡터 만들기

    sources = []

    # 2-1. 관심분야 (예: ["문학", "종교"]) → 각각 하나의 재료
    for interest in interests:
        sources.append(("interest", interest, vectorizer.transform([interest]), INTEREST_WEIGHT))

    # 2-2. 읽은 책 → 평점이 높을수록 크게 반영
    for book_id in read_ids:
        row = id_to_row.get(book_id)
        if row is None:                     # 삭제된 도서는 건너뜀
            continue

        # 같은 책을 여러 번 읽었을 수 있으므로 그 책에 남긴 평점들의 평균을 사용
        ratings = [r.get("rating") for r in my_records
                   if r.get("book_id") == book_id and r.get("rating") is not None]
        rating = sum(ratings) / len(ratings) if ratings else DEFAULT_RATING

        if rating < LIKED_MIN_RATING:       # 싫어한 책(2점 이하)은 취향에 넣지 않음
            continue

        title = books[row].get("title", "")
        # 가중치: 5점 → 1.0, 4점 → 0.8, 3점 → 0.6
        sources.append(("book", title, book_matrix[row], rating / 5))

    # 2-3. 20자 이상 리뷰 → 무엇이 좋았는지가 드러나는 문장
  
    if mode == "full":
        for r in usable_reviews:
            review = r.get("review").strip()
            sources.append(("review", review, vectorizer.transform([review]), REVIEW_WEIGHT))

    # 취향 정보가 하나도 없으면(신규 회원 등) 평점 높은 순으로 대체
    if not sources:
        return {
            "items": _popular_books(books, exclude_ids, top_n),
            "mode": "popular",
            "review_count": review_count,
            "review_goal": REVIEW_GOAL,
        }

    # 가중 평균: (벡터1×가중치1 + 벡터2×가중치2 + ...) / (가중치 합)
    total_weight = sum(weight for _, _, _, weight in sources)
    profile = sum(vector * weight for _, _, vector, weight in sources) / total_weight

    # ------------------------------------------------------------
    # 3. 취향 벡터 ↔ 모든 도서의 코사인 유사도
    # ------------------------------------------------------------
    # cosine_similarity(1×N, 도서수×N) → 1×도서수 결과. [0]으로 첫 행만 꺼냄
    scores = cosine_similarity(profile, book_matrix)[0]

    # 추천 후보: 읽은 책/대출 중인 책을 제외한 나머지 (행 번호 목록)
    candidate_rows = [i for i, b in enumerate(books) if b.get("id") not in exclude_ids]
    if not candidate_rows:
        return {"items": [], "mode": mode, "review_count": review_count, "review_goal": REVIEW_GOAL}

    # 유사도가 높은 순으로 정렬, 유사도가 같으면 도서 평점이 높은 순
    candidate_rows.sort(key=lambda i: (scores[i], books[i].get("rating") or 0), reverse=True)
    top_rows = candidate_rows[:top_n]

    # ------------------------------------------------------------
    # 4. 추천 이유 만들기
    # ------------------------------------------------------------
    # 추천된 책마다 "어떤 재료(관심분야/읽은 책/리뷰)와 가장 비슷한지"를 찾아 이유로 보여줌
    source_matrix = vstack([vector for _, _, vector, _ in sources])          # 재료 벡터들을 행렬 하나로
    reason_scores = cosine_similarity(book_matrix[top_rows], source_matrix)  # (추천 책 수 × 재료 수)

    results = []
    for k, row in enumerate(top_rows):
        best = reason_scores[k].argmax()            # 이 책과 가장 비슷한 재료의 번호
        kind, label, _, _ = sources[best]

        if kind == "interest":
            reason = f"관심분야 '{label}'와(과) 관련된 책이에요"
        elif kind == "book":
            reason = f"『{label}』을(를) 좋게 평가하셔서 추천해요"
        else:   # review
            short = label if len(label) <= 20 else label[:20] + "..."
            reason = f"남기신 리뷰 \"{short}\"와(과) 비슷한 주제예요"

        results.append({
            "book": books[row],
            "score": round(float(scores[row]), 3),   # numpy 숫자 → 일반 float
            "reason": reason,
        })

    return {"items": results, "mode": mode, "review_count": review_count, "review_goal": REVIEW_GOAL}