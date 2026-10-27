# services/search_service.py
from utils.file_handler import load_json


def search_books(keyword: str):
    """책 제목, 저자, 장르 중 검색된 값 찾기 및 후기 결합"""
    books = load_json("data/books.json")      # 도서 목록 불러오기
    records = load_json("data/records.json")  # 도서 후기/기록 목록 불러오기
    
    results = []  # 최종 검색된 책들을 담기
    keyword = keyword.strip().lower()
    
    if not keyword:
        return results, "검색어를 입력해주세요."
    
    for book in books:
        title = book.get("title", "").lower()
        author = book.get("author", "").lower()
        genre = book.get("genre", "").lower()

        # 검색어가 포함된 책을 찾았을 때
        if keyword in title or keyword in author or keyword in genre:
            # 이번 책 전용 후기 담기
            this_book_reviews = []
            
            # records 중에서 이 책의 ID와 일치하는 후기 담기
            book_id = book.get("id")
            for rec in records:
                if rec.get("book_id") == book_id:
                    this_book_reviews.append(rec)
            
            # 책 딕셔너리에 후기 목록을 통째로 추가
            book["reviews"] = this_book_reviews
            
            # 후기까지 담긴 책을 최종 결과 리스트에 추가
            results.append(book)

    if not results:
        return results, f"'{keyword}'의 검색 결과(제목, 저자, 장르)가 존재하지 않습니다."

    return results, f"총 {len(results)}건이 검색되었습니다."

def scnd_search_books(frst_results: list, scnd_keyword: str):
    """2차 검색 함수(결과내 재 검색)"""
    scnd_results = []  # 2차 검색을 통과한 책들을 담을 바구니
    clean_keyword = scnd_keyword.strip().lower()

    # 1차 검색 결과 리스트 자체가 비어있다면 필터링 불가
    if not frst_results:
        return scnd_results, "재검색할 1차 도서 목록이 없습니다."

    # 2차 검색어가 비어있다면 원래 1차 검색 결과를 그대로 유지해서 반환
    if not clean_keyword:
        return frst_results, "2차 검색어를 입력하지 않아 이전 목록을 유지합니다."

    # 전체 파일이 아니라 '1차 검색 통과 도서들'만 꺼내서 추가 검사
    for book in frst_results:
        title = book.get("title", "").lower()
        author = book.get("author", "").lower()
        genre = book.get("genre", "").lower()

        # 2차 검색어가 포함되어 있는지 확인
        if (clean_keyword in title) or (clean_keyword in author) or (clean_keyword in genre):
            # 이미 1차 검색 때 reviews가 붙어있으므로 그대로 추가
            scnd_results.append(book)

    # 2차 필터링 결과 확인
    if not scnd_results:
        return scnd_results, f"결과 내에서 '{scnd_keyword}' 검색 결과가 없습니다."

    return scnd_results, f"결과 내 재검색 완료: 총 {len(scnd_results)}건으로 재검색되었습니다."

# book_list: 정렬할 책 리스트 / sort_by: 정렬 기준(title, rating, author, available_stck) / reverse: 내림차순 유무
def sort_books(book_list: list, sort_by: str = "title", reverse: bool = False):
    """정렬 함수"""
    # 정렬할 목록이 비어있으면 그대로 리턴
    if not book_list:
        return []

    # 정렬 기준값을 꺼내주는 일반 함수를 내부에 정의
    # sorted() 에서 하나씩 함수 실행
    
    def get_sort_value(single_book):
        # 만약 평점(rating) 기준으로 정렬할 때 값이 없으면 0.0을 반환 (숫자형 비교)
        if sort_by == "rating":
            return single_book.get("rating", 0.0)
        
        # 재고(available_stock) 기준일 때 값이 없으면 0을 반환 (숫자형 비교)
        if sort_by == "available_stock":
            return single_book.get("available_stock", 0)

        # 그 외 문자열(제목 title, 저자 author, 장르 genre)은 문자열로 반환
        return str(single_book.get(sort_by, ""))

    # 파이썬 내장 sorted() 함수 실행
    # key=get_sort_value 라고 적으면, 파이썬이 책을 비교할 때마다 위 함수를 호출해서 기준값을 확인합니다.
    sorted_list = sorted(book_list, key=get_sort_value, reverse=reverse)

    return sorted_list

