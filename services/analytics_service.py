# services/analytics_service.py
# 실행법: python -m services.analytics_service

from utils.file_handler import load_json, save_json

MEMBERS_FILE = "data/members.json"
LOANS_FILE = "data/loans.json"
BOOKS_FILE = "data/books.json"
RECORDS_FILE = "data/records.json"


def get_user_timeline(user_id: str | int) -> list[dict]:
    """특정 회원의 독서 이력(대출/반납 + 감상평/평점)을 시간순(최신순)으로 종합 조회"""
    loans_data = load_json(LOANS_FILE) or []
    books_data = load_json(BOOKS_FILE) or []
    records_data = load_json(RECORDS_FILE) or []

    # 빠른 도서 조회를 위한 딕셔너리 생성
    book_dict = {
        (b.get("book_id") if isinstance(b, dict) else getattr(b, "book_id", None)): b 
        for b in books_data
    }
    
    # 회원이 작성한 감상평/평점 매핑
    record_dict = {}
    for r in records_data:
        r_user_id = r.get("user_id") if isinstance(r, dict) else getattr(r, "user_id", None)
        r_book_id = r.get("book_id") if isinstance(r, dict) else getattr(r, "book_id", None)
        if str(r_user_id) == str(user_id):
            record_dict[r_book_id] = r

    # 사용자 대출/반납 기록 추출 및 정보 결합
    timeline = []
    for loan in loans_data:
        l_user_id = loan.get("user_id") if isinstance(loan, dict) else getattr(loan, "user_id", None)
        
        if str(l_user_id) == str(user_id):
            b_id = loan.get("book_id") if isinstance(loan, dict) else getattr(loan, "book_id", None)
            book_info = book_dict.get(b_id, {})
            
            # 책 세부 정보 (genre 키가 없거나 데이터가 비어있어도 안전하게 방어)
            if isinstance(book_info, dict):
                title = book_info.get("title", "제목 없음")
                author = book_info.get("author", "저자 미상")
                genre = book_info.get("genre") if book_info.get("genre") else "일반"
            else:
                title = getattr(book_info, "title", "제목 없음")
                author = getattr(book_info, "author", "저자 미상")
                genre = getattr(book_info, "genre", "일반") or "일반"
            
            # 날짜 설정 (반납일 우선, 없으면 대출일)
            ret_date = loan.get("return_date") if isinstance(loan, dict) else getattr(loan, "return_date", None)
            loan_date = loan.get("loan_date") if isinstance(loan, dict) else getattr(loan, "loan_date", "-")
            event_date = ret_date if ret_date else loan_date
            
            # 감상평/평점 가져오기
            rec = record_dict.get(b_id, {})
            rating = rec.get("rating") if isinstance(rec, dict) else getattr(rec, "rating", None)
            review = rec.get("review") if isinstance(rec, dict) else getattr(rec, "review", "")
            
            timeline.append({
                "book_id": b_id,
                "title": title,
                "author": author,
                "genre": genre,
                "date": event_date,
                "status": "완독 (반납)" if ret_date else "읽는 중 (대출 중)",
                "rating": rating,
                "review": review if review else "작성된 감상평이 없습니다."
            })
            
    # 4. 날짜 기준 최신순 정렬
    timeline.sort(key=lambda x: str(x.get("date", "")), reverse=True)
    return timeline


# user_id를 기반으로 회원 이름 조회
def get_user_name(user_id: int | str) -> str:
    members = load_json(MEMBERS_FILE) or []
    for m in members:
        u_id = m.get("user_id") if isinstance(m, dict) else getattr(m, "user_id", None)
        if str(u_id) == str(user_id):
            return m.get("name") if isinstance(m, dict) else getattr(m, "name", f'회원 {user_id}')
    return f'회원 {user_id}'


# 독서 연대기 출력
def print_user_timeline(user_id: str | int) -> None:
    timeline = get_user_timeline(user_id)
    user_name = get_user_name(user_id)

    print("\n" + "=" * 60)
    print(f"        🌟 [{user_name}] 님의 나만의 독서 연대기 🌟")
    print("=" * 60)

    if not timeline:
        print("  아직 기록된 독서 연대기가 없습니다.")
        print("  도서를 대출하고 감상평을 남겨보세요! 📚")
    else:
        total_count = len(timeline)
        print(f"  총 {total_count}권의 독서 발자취가 기록되어 있습니다.\n")

        for index, item in enumerate(timeline, 1):
            if item["rating"]:
                stars = "★" * int(item["rating"]) + "☆" * (5 - int(item["rating"]))
                rating_str = f"{stars} ({item['rating']}점)"
            else:
                rating_str = "평점 미등록"

            print(f"  [{item['date']}] ───►  [{item['status']}]")
            # item.get('genre', '일반')을 통해 2차 안전장치 마련
            genre_str = item.get('genre', '일반')
            print(f"   📖 도서명 : {item['title']} ({item['author']} / {genre_str})")
            print(f"   ⭐ 평  점 : {rating_str}")
            print(f"   💬 한줄평 : \"{item['review']}\"")

            if index < total_count:
                print("            │")
                print("            ▼")

    print("=" * 60 + "\n")


# 독서 목표 권수, 완독 권수, 목표 달성률(%)
def manage_reading_goal(user_id: int | str) -> None:
    members = load_json(MEMBERS_FILE) or []
    loans = load_json(LOANS_FILE) or []

    # user_id 로 회원 정보 조회
    target_member = None
    for m in members:
        u_id = m.get("user_id") if isinstance(m, dict) else getattr(m, "user_id", None)
        if str(u_id) == str(user_id):
            target_member = m
            break

    if not target_member:
        print(f"[오류] 회원 정보를 찾을 수 없습니다.")
        return

    user_name = target_member.get("name") if isinstance(target_member, dict) else getattr(target_member, "name", f'회원 {user_id}')

    # 반납 완료된 대출 수 카운트
    completed_count = 0
    for loan in loans:
        l_user_id = loan.get("user_id") if isinstance(loan, dict) else getattr(loan, "user_id", None)
        l_status = loan.get("status") if isinstance(loan, dict) else getattr(loan, "status", None)
        l_return = loan.get("return_date") if isinstance(loan, dict) else getattr(loan, "return_date", None)

        if str(l_user_id) == str(user_id) and (l_status == "returned" or l_return is not None):
            completed_count += 1

    # 목표 권수 가져오기
    current_goal = target_member.get("reading_goal", 0) if isinstance(target_member, dict) else getattr(target_member, "reading_goal", 0)

    print("\n" + "=" * 60)
    print(f"        🎯 [{user_name}] 님의 독서 목표 및 달성 현황")
    print("=" * 60)

    # 목표 달성 현황 및 게이지 바 출력
    if current_goal == 0:
        print("  📌 현재 설정된 독서 목표가 없습니다.")
    else:
        rate = round((completed_count / current_goal) * 100, 1)

        # 20칸짜리 콘솔 프로그래스 바 연출 ([██████████░░░░░░░░░░])
        bar_length = 20
        filled_length = int(bar_length * min(rate, 100) // 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)

        print(f" • 목표 권수 : {current_goal} 권")
        print(f" • 읽은 권수 : {completed_count} 권 (완독 기준)")
        print(f" • 달 성 률  : {rate}%")
        print(f" • 진행 현황 : [{bar}] {rate}%")
        print("-" * 60)

        if rate >= 100:
            print(" 🎉 축하합니다! 목표를 달성하셨습니다! 🏆")
        elif rate >= 50:
            print(" 👏 목표 절반을 넘었습니다! 조금만 더 힘내세요!")
        else:
            print(" 📖 차근차근 책을 읽어 목표를 달성해 보세요!")

    print("=" * 60)

    # 목표 설정/수정 대화상자
    choice = input("\n독서 목표를 새로 설정(또는 변경)하시겠습니까? (Y/N): ").strip().upper()
    if choice == "Y":
        while True:
            new_goal_input = input("새로운 목표 권수를 입력하세요 (숫자만 입력): ").strip()
            if not new_goal_input.isdigit():
                print("[오류] 숫자만 입력해 주세요.")
                continue

            new_goal = int(new_goal_input)
            if new_goal <= 0:
                print("[오류] 목표 권수는 1권 이상이어야 합니다.")
                continue

            break

        # 변경사항 반영 및 JSON 파일 저장
        if isinstance(target_member, dict):
            target_member["reading_goal"] = new_goal
        else:
            target_member.reading_goal = new_goal

        save_json(MEMBERS_FILE, members)
        print(f"\n[성공] 목표가 {new_goal}권으로 새롭게 설정되었습니다! 🎯")


# 포인트 구간별 회원 등급
def get_user_tier(point: int) -> str:
    if point >= 1000:
        return "💎 VIP"
    elif point >= 500:
        return "🥇 GOLD"
    elif point >= 200:
        return "🥈 SILVER"
    else:
        return "🥉 BRONZE"


# 로그인한 회원 포인트 및 회원등급 안내 출력
def show_my_point_status(user_id: int | str) -> None:
    members = load_json(MEMBERS_FILE) or []
    target_member = None

    for m in members:
        u_id = m.get("user_id") if isinstance(m, dict) else getattr(m, "user_id", None)
        if str(u_id) == str(user_id):
            target_member = m
            break

    if not target_member:
        print("[오류] 회원 정보를 찾을 수 없습니다.")
        return
    
    name = target_member.get("name") if isinstance(target_member, dict) else getattr(target_member, "name", "회원")
    point = target_member.get("point", 0) if isinstance(target_member, dict) else getattr(target_member, "point", 0)
    tier = get_user_tier(point)

    if point < 200:
        next_msg = f"🥈 SILVER 등급까지 {200 - point}P 남았습니다."
    elif point < 500:
        next_msg = f"🥇 GOLD 등급까지 {500 - point}P 남았습니다."
    elif point < 1000:
        next_msg = f"💎 VIP 등급까지 {1000 - point}P 남았습니다."
    else:
        next_msg = "🎉 최고 등급인 VIP 회원입니다!"

    print("\n" + "=" * 50)
    print(f"       🪙 [{name}] 님의 포인트 및 회원 등급")
    print("=" * 50)
    print(f" • 현재 보유 포인트 : {point} P")
    print(f" • 현재 회원 등급   : {tier}")
    print(f" • 등급 달성 안내   : {next_msg}")
    print("-" * 50)
    print(" 💡 [포인트 적립 안내]")
    print("   - 도서 반납 시: 기본 +10 P")
    print("   - 리뷰/평점 작성 시: 추가 +10 P")
    print("=" * 50 + "\n")


################################################
# 모듈 단독 실행 테스트
################################################
if __name__ == "__main__":
    test_user_id = 1
    
    print_user_timeline(test_user_id)
    manage_reading_goal(test_user_id)
    show_my_point_status(test_user_id)