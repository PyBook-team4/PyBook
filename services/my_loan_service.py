# services/my_loan_service.py
# python -m services.my_loan_service
from datetime import datetime
from models.loan import Loan
from utils.file_handler import load_json, save_json


# 대출 기록 조회
LOANS_FILE = "data/loans.json"
BOOKS_FILE = "data/books.json"


def get_my_loan_history(current_user: dict) -> list[dict]:
    """
    로그인한 사용자와 user_id와 일치하는 대출 기록 찾아 리스트로 반환합니다
    """
    loans = load_json(LOANS_FILE) or []
    books = load_json(BOOKS_FILE) or []

    # 로그인 회원의 user_id 가져오기
    my_id = current_user.get("user_id")

    my_history = []

    for loan in loans:
        if str(loan.get("user_id")) == str(my_id):

            # 책 정보 가져오기
            book_id = loan.get("book_id")
            book_title = loan.get("title")
            book_author = loan.get("author")
          

            for book in books:
                if str(book.get("book_id")) == str(book_id):
                    book_title = book.get("title")
                    book_author = book.get("author")
 
                    break
             # 반납일이 없으면 "대출 중", 상태 표시
            ret_date = loan.get("return_date")
            if ret_date:
                status_str = "✅ 반납완료"
                display_return_date = ret_date
            else:
                status_str = "📖 대출중"
                display_return_date = "대출 중 (미반납)"

            # 내가 볼 기록 리스트에 추가
            my_history.append(
                {
                    "title": book_title,
                    "author": book_author,
                    "loan_date": loan.get("loan_date", "-"),
                    "return_date": display_return_date,
                    "status": status_str,
                }
            )

    return my_history


def print_my_loan_history(current_user: dict) -> None:
    """나의 대출/반납 내역을 콘솔에 출력합니다."""
    history = get_my_loan_history(current_user)
    user_name = current_user.get("name", "회원")

    print("\n" + "=" * 50)
    print(f"         📚 [{user_name}] 님의 도서 대출 / 반납 현황")
    print("=" * 50)

    if not history:
        print("  대출 또는 반납된 내역이 존재하지 않습니다.")
    else:
        for idx, item in enumerate(history, 1):
            print(f" {idx}. [{item['status']}] {item['title']} ({item['author']})")
            print(f"    - 대출일: {item['loan_date']}")
            print(f"    - 반납일: {item['return_date']}")
            print("-" * 50)

    print("=" * 50 + "\n")

   






# def print_my_loan_history(current_user: dict) -> None:
#     """로그인한 사용자(current_user)의 대출/반납 현황을 콘솔 화면에 출력합니다."""
#     history = get_my_loan_history(current_user)
#     user_name = current_user.get("name") if isinstance(current_user, dict) else getattr(current_user, "name", "회원")

#     print("\n" + "=" * 60)
#     print(f"         📚 [{user_name}] 님의 도서 대출 / 반납 현황")
#     print("=" * 60)

#     if not history:
#         print("  대출 또는 반납된 내역이 존재하지 않습니다.")
#     else:
#         for idx, item in enumerate(history, 1):
#             print(f" {idx}. [{item['status']}] {item['title']} ({item['author']})")
#             print(f"    - 대출일: {item['loan_date']}")
#             print(f"    - 반납일: {item['return_date']}")
#             print("-" * 60)

#     print("=" * 60 + "\n")


############

if __name__ == "__main__":
    dummy_user = {
        "current_user": 1,
        "email": "dudu1@naver.com",
        "name": "dudu",
        "point": 100
    }



    # 대출 현황 화면 출력
    print_my_loan_history(dummy_user)