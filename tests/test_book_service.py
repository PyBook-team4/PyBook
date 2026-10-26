# tests/test_book_service.py
import pytest
from unittest.mock import patch
from services.book_service import search_books_by_keyword

# @patch를 이용해 외부 API를 호출하는 BookClient를 가짜(Mock)로 교체합니다.
@patch("services.book_service.BookClient")
def test_search_books_by_keyword_success(mock_book_client_class):
    # Given: 가짜 클라이언트가 반환할 가상의 API 응답 데이터 설정
    mock_client_instance = mock_book_client_class.return_value
    mock_client_instance.search_book.return_value = {
        "result": [
            {
                "title": "테스트 파이썬 책",
                "author": "김개발",
                "publisher": "코딩 출판사",
                "isbn": "9788900000000"
            }
        ]
    }

    # When: 서비스 함수의 검색 기능 실행
    results = search_books_by_keyword("파이썬")

    # Then: 결과가 기대한 형태로 잘 파싱되어 돌아왔는지 검증
    assert len(results) == 1
    assert results[0]["title"] == "테스트 파이썬 책"
    assert results[0]["author"] == "김개발"
    assert results[0]["isbn"] == "9788900000000"
    
    # API 클라이언트가 올바른 키워드로 호출되었는지 검증
    mock_client_instance.search_book.assert_called_once_with(keyword="파이썬", page_size=10)


@patch("services.book_service.BookClient")
def test_search_books_by_keyword_api_error(mock_book_client_class):
    # Given: API 통신 오류(문자열 반환) 상황 가정
    mock_client_instance = mock_book_client_class.return_value
    mock_client_instance.search_book.return_value = "API 통신 오류: 타임아웃"

    # When: 검색 함수 실행
    results = search_books_by_keyword("에러 테스트")

    # Then: 오류 발생 시 빈 리스트를 안전하게 반환하는지 검증
    assert results == []