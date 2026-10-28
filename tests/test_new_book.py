from services.book_service import register_book, book_delete, book_update

# 도서 등록 코드 테스트
# 1. 최대 보유량이 음수인 경우
register_book("책A", "작가", "출판사", "소설", "111", -1, 0)

# 2. 현재 재고가 음수인 경우
register_book("책B", "작가", "출판사", "소설", "222", 3, -1)

# 3. 현재 재고가 최대 보유량보다 큰 경우
register_book("책C", "작가", "출판사", "소설", "333", 3, 6)


# 4. 정상적으로 등록되는 경우 # 이미 같은 제목의 도서가 있다면 등록되지 않음
result = register_book(
    "파이썬 입문",
    "홍길동",
    "테스트 출판사",
    "IT",
    "444",
    3,
    3
)

# 도서 삭제 코드 테스트 # json안에 있는 도서 목록이 실제로 지워지니 조심할 것 
# result = book_delete(2) #실제 json에 존재하는 id인지 확인 후 실행
# print("삭제 성공" if result else "삭제 실패")

# # 도서 수정 코드 테스트
# # json 파일에 올바른 정보가 있어야 실행 가능
# def test_update_title():
#     print("\n[테스트 1] 제목 수정")
#     result = book_update(1, 1, "파이썬 심화")
#     print("결과:", result, "| 기대값: True")


# def test_update_rating_success():
#     print("\n[테스트 2] 평점 수정 성공")
#     result = book_update(1, 6, "4.8")
#     print("결과:", result, "| 기대값: True")


# def test_update_rating_fail():
#     print("\n[테스트 3] 평점 범위 초과")
#     result = book_update(1, 6, "5.5")
#     print("결과:", result, "| 기대값: False")


# def test_update_total_stock_fail():
#     print("\n[테스트 4] 대여 가능 재고보다 적은 전체 재고")
#     result = book_update(1, 7, "1")
#     print("결과:", result, "| 기대값: False")


# def test_update_available_stock_fail():
#     print("\n[테스트 5] 전체 재고보다 많은 대여 가능 재고")
#     result = book_update(1, 8, "4")
#     print("결과:", result, "| 기대값: False")


# def test_empty_value():
#     print("\n[테스트 6] 공백 입력")
#     result = book_update(1, 1, "   ")
#     print("결과:", result, "| 기대값: False")


# def test_invalid_field():
#     print("\n[테스트 7] 잘못된 항목 번호")
#     result = book_update(1, 99, "새 제목")
#     print("결과:", result, "| 기대값: False")


# def test_book_not_found():
#     print("\n[테스트 8] 존재하지 않는 도서 ID")
#     result = book_update(999, 1, "새 제목")
#     print("결과:", result, "| 기대값: False")


# if __name__ == "__main__":
#     test_update_title()
#     test_update_rating_success()
#     test_update_rating_fail()
#     test_update_total_stock_fail()
#     test_update_available_stock_fail()
#     test_empty_value()
#     test_invalid_field()
#     test_book_not_found()