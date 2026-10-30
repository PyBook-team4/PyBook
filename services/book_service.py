# services/book_service.py
import random
import re
from datetime import datetime
from models.book import Book
from utils.book_api_client import BookClient
from utils.file_handler import load_json, save_json

BOOKS_FILE = "data/books.json"

def initialize_books_if_empty():
    """books.json이 비어있을 경우, 최초 1회 실행하여 약 100권의 도서 데이터를 수집하고 저장"""
    books_data = load_json(BOOKS_FILE)
    if len(books_data) > 0:
        return  # 이미 데이터가 존재하면 패스

    client = BookClient()
    # 골고루 100권을 채우기 위한 다양한 인기 검색 키워드 리스트 (각 20권씩 총 100권)
    keywords = ["파이썬", "인공지능", "소설", "역사", "경제"]
    collected_books = []
    book_id_counter = 1

    for kw in keywords:
        response = client.search_book(keyword=kw, page_size=20)
        
        # API 통신 에러 혹은 응답 형태 검증
        if isinstance(response, str) or not isinstance(response, dict):
            continue
            
        # 국립중앙도서관 API 응답 구조에 맞게 결과 추출 (result 리스트 또는 유사 구조)
        items = response.get("result", [])
        for item in items:
            title = item.get("title", "제목 없음")
            author = item.get("author", "저자 미상")
            publisher = item.get("publisher", "출판사 미상")
            isbn = item.get("isbn", str(book_id_counter))
            
            # 재고 무작위 부여 (0~3)
            total_stock = random.randint(0, 3)
            # 대출 가능 재고는 총 재고를 넘지 않도록 설정 (단, 0이면 0)
            available_stock = total_stock

            book_obj = Book(
                id=book_id_counter,
                title=title,
                author=author,
                publisher=publisher,
                genre=kw,  # 키워드를 장르로 활용
                isbn=isbn,
                rating=round(random.uniform(3.5, 5.0), 1), # 임의의 평점 (3.5 ~ 5.0)
                total_stock=total_stock,
                available_stock=available_stock
            )
            
            collected_books.append(book_obj.to_dict())
            book_id_counter += 1

    # 파일에 저장
    if collected_books:
        save_json(BOOKS_FILE, collected_books)
        print(f"✨ 도서 초기화 완료: 총 {len(collected_books)}권의 도서가 성공적으로 적재되었습니다!")

# ------------------------------------------------------------
# 국립중앙도서관 API 응답 → 우리 도서 등록 형식으로 변환
# (응답 필드 설명: 국립중앙도서관 소장자료 OPEN API 가이드 2.3 출력 결과 필드)
# ------------------------------------------------------------

# 저자 정보 앞뒤에 붙는 역할 표시 (예: "지은이: 박경리", "김용준 저", "안진섭 지음")
AUTHOR_ROLE_WORDS = ["지은이", "저자", "공저", "글", "원작", "저", "지음", "편저", "엮음", "[저]"]


def _strip_html(text: str) -> str:
    """검색어 강조용 HTML 태그 제거: '<span class="searching_txt">파이썬</span>' → '파이썬'"""
    return re.sub(r"<[^>]+>", "", text or "").strip()


def _clean_author(author_info: str) -> str:
    """
    저자 정보에서 대표 저자 한 명만 추출
    - "Y. Daniel Liang 지음 ;길준민,정재화 옮김" → "Y. Daniel Liang"
    - "오연재,김용민,정승언 공저"                → "오연재 외"
    - "지은이: 우재남"                          → "우재남"
    """
    text = _strip_html(author_info)
    first_part = text.split(";")[0]                 # ';' 뒤는 옮긴이, 그림 등 → 첫 부분만 사용
    first_part = first_part.split(":")[-1]          # "지은이: 우재남" → " 우재남"

    words = [w for w in first_part.split() if w not in AUTHOR_ROLE_WORDS]
    name = " ".join(words).strip()

    if "," in name:                                 # 여러 명이면 첫 번째 사람 + " 외"
        name = name.split(",")[0].strip() + " 외"
    return name or "저자 미상"


def _to_genre(kdc_name: str, class_no: str) -> str:
    """
    KDC(한국십진분류) 대분류 → 우리 도서 장르
    - KDC에서는 컴퓨터·프로그래밍(004, 005)이 '총류'에 속하지만,
      우리 데이터와 회원 관심분야는 '기술과학'으로 분류하므로 맞춰서 변환
    """
    if (class_no or "").startswith(("004", "005")):
        return "기술과학"
    return kdc_name or "기타"


def search_books_by_keyword(keyword: str, page_size: int = 10) -> list:
    """
    국립중앙도서관 API로 도서를 검색해, 도서 등록에 필요한 정보만 골라서 반환
    - 반환값: [{"title", "author", "publisher", "pub_year", "genre", "isbn"}, ...]
    - API 통신 오류 시 오류 메시지를 출력하고 빈 리스트 반환
    """
    client = BookClient()
    response = client.search_book(keyword=keyword, page_size=page_size)

    if isinstance(response, str):       # BookClient는 통신 오류 시 오류 문장(str)을 반환
        print(response)
        return []

    results = []
    for item in response.get("result", []):
        results.append({
            "title": _strip_html(item.get("titleInfo")),
            "author": _clean_author(item.get("authorInfo")),
            "publisher": (item.get("pubInfo") or "").strip(),
            "pub_year": item.get("pubYearInfo", ""),
            "genre": _to_genre(item.get("kdcName1s"), item.get("classNo")),
            "isbn": (item.get("isbn") or "").split(" ")[0],    # ISBN이 여러 개면 첫 번째
        })
    return results