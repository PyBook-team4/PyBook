# services/book_service.py
import random
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



'''
def search_books_by_keyword(keyword: str) -> list:
    """국립중앙도서관 API를 활용한 실시간 키워드 도서 검색"""
    client = BookClient()
    response = client.search_book(keyword=keyword, page_size=10)
    
    if isinstance(response, str):
        print(response)
        return []
        
    items = response.get("result", [])
    results = []
    for item in items:
        results.append({
            "title": item.get("title"),
            "author": item.get("author"),
            "publisher": item.get("publisher"),
            "isbn": item.get("isbn")
        })
    return results


    
'''