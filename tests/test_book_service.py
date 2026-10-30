# tests/test_book_service.py
# 국립중앙도서관 API 검색 결과를 도서 등록 형식으로 변환하는 기능 테스트
# - 실제 API는 호출하지 않고, BookClient를 가짜(Mock)로 바꿔서 실제 응답과 같은 형식의 데이터를 넣어 테스트
import pytest
from unittest.mock import patch
from services.book_service import search_books_by_keyword

# 실제 API 응답 형식 (2026-10 기준, '파이썬' / '사피엔스' / '토지' 검색 결과에서 필요한 필드만 발췌)
FAKE_RESPONSE = {
    "total": 3,
    "result": [
        {   # 여러 명 공저 + 프로그래밍(KDC 005 → 총류)
            "titleInfo": "<span class=\"searching_txt\">파이썬</span> : 입문에서 실무까지 완벽 정리",
            "authorInfo": "공저: 임정목,정진영,조범석,최철재",
            "pubInfo": "현우사",
            "pubYearInfo": "2018",
            "kdcName1s": "총류",
            "classNo": "005.133",
            "isbn": "9788980815197",
        },
        {   # 지은이 + 옮긴이, ISBN 여러 개
            "titleInfo": "<span class=\"searching_txt\">사피엔스</span> : 그래픽 히스토리. Vol.1-3",
            "authorInfo": "지은이: 유발 하라리 ;옮긴이: 조현욱",
            "pubInfo": "김영사",
            "pubYearInfo": "2020-2024",
            "kdcName1s": "역사",
            "classNo": "909",
            "isbn": "9788934991311 9788934991328",
        },
        {   # ISBN 없는 옛날 책
            "titleInfo": "<span class=\"searching_txt\">토지</span>",
            "authorInfo": "박경리 [저]",
            "pubInfo": "동서문화사",
            "pubYearInfo": "1990",
            "kdcName1s": "문학",
            "classNo": "813.6",
            "isbn": "",
        },
    ],
}


@patch("services.book_service.BookClient")
def test_search_books_by_keyword_success(mock_book_client_class):
    # Given: 가짜 클라이언트가 실제 응답과 같은 형식의 데이터를 반환
    mock_client_instance = mock_book_client_class.return_value
    mock_client_instance.search_book.return_value = FAKE_RESPONSE

    # When
    results = search_books_by_keyword("파이썬")

    # Then: 도서 등록에 필요한 형식으로 변환되었는지 확인
    assert len(results) == 3

    # HTML 태그 제거, 여러 저자는 "첫 번째 + 외", 프로그래밍 책은 기술과학으로 변환
    assert results[0]["title"] == "파이썬 : 입문에서 실무까지 완벽 정리"
    assert results[0]["author"] == "임정목 외"
    assert results[0]["genre"] == "기술과학"
    assert results[0]["isbn"] == "9788980815197"

    # "지은이:" 제거 + 옮긴이 제외, ISBN 여러 개면 첫 번째
    assert results[1]["author"] == "유발 하라리"
    assert results[1]["genre"] == "역사"
    assert results[1]["isbn"] == "9788934991311"

    # "[저]" 제거, ISBN이 없으면 빈 문자열
    assert results[2]["author"] == "박경리"
    assert results[2]["isbn"] == ""

    # API 클라이언트가 올바른 검색어와 개수로 호출되었는지 확인
    mock_client_instance.search_book.assert_called_once_with(keyword="파이썬", page_size=10)


@patch("services.book_service.BookClient")
def test_search_books_by_keyword_api_error(mock_book_client_class):
    # Given: API 통신 오류 시 BookClient는 오류 문장(str)을 반환
    mock_client_instance = mock_book_client_class.return_value
    mock_client_instance.search_book.return_value = "API 통신 오류: 타임아웃"

    # When
    results = search_books_by_keyword("에러 테스트")

    # Then: 오류가 나도 프로그램이 멈추지 않고 빈 리스트 반환
    assert results == []


@patch("services.book_service.BookClient")
def test_search_books_by_keyword_no_result(mock_book_client_class):
    # Given: 검색 결과가 0건
    mock_book_client_class.return_value.search_book.return_value = {"total": 0, "result": []}

    # When / Then
    assert search_books_by_keyword("없는책") == []