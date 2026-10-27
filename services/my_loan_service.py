# services/loan_service.py
# python -m services.loan_service
from datetime import datetime
from models.loan import Loan
from utils.file_handler import load_json, save_json

'''
해당 파일 구현 시 members,books,records 부분을 모두 접근해야 하기 때문에 난이도가 높을 수 있습니다.
우선 코드 구현 후 테스트 할 경우 books.json에 더미데이터 한개 생성 후 테스트하면 됩니다.

'''


#도서 대출

def borrow(member_id: str | int, book_id: int) -> bool:
    """도서 대출: 재고 확인 후 대출 기록 생성 및 재고 감소"""
    # 1. 도서 존재 여부 및 대출 가능 재고 확인 (books.json 접근)
    # 2.새로운 loan_id 생성     (loans.json 접근)
    # 3. 새 대출 객체 생성 및 추가  
    # 4. 재고 감소 (available_stock - 1)    (books.json 접근)
    # 5. json 파일 저장 (loans.json 접근)
    pass

#도서 반납

def return_book(loan_id: int) -> bool:
    """도서 반납: 대출 상태 변경, 재고 복구 및 포인트 적립"""
    # 1. 대출 상태 및 반납일 업데이트
    # 2. 해당 도서 재고 복구 (available_stock + 1)
    # 3. 반납 보상 포인트 지급 (예: 반납 시 10 포인트 적립)  members.json 접근
    # 4, 리뷰, 평점 남길 시 (예: 10포인트 추가 적립)        records.json 접근
    # 5. 파일 저장
    pass

# 대출 기록 조회
LOANS_FILE = "data/loans.json"
BOOKS_FILE = "data/books.json"


def get_my_loan_history(current_user: dict) -> list[dict]:
    """로그인한 사용자(current_user)의 대출/반납 전체 내역을 조회하여 리스트로 반환합니다."""
    loans = load_json(LOANS_FILE) or []
    books = load_json(BOOKS_FILE) or []

    # user_id와 email 추출 (방어 코드)
    user_id = current_user.get("user_id") if isinstance(current_user, dict) else getattr(current_user, "user_id", None)
    user_email = current_user.get("email") if isinstance(current_user, dict) else getattr(current_user, "email", None)

    # 빠른 책 정보 조회를 위해 dict로 변환 (book_id 기준)
    book_dict = {
        (b.get("book_id") if isinstance(b, dict) else getattr(b, "book_id", None)): b 
        for b in books
    }

    my_history = []
    for loan in loans:
        # loans.json의 user_id 또는 member_id 추출
        l_user_id = loan.get("user_id") if isinstance(loan, dict) else getattr(loan, "user_id", None)
        l_member_id = loan.get("member_id") if isinstance(loan, dict) else getattr(loan, "member_id", None)

        # 로그인한 회원의 user_id 또는 email과 일치하는 기록만 필터링 (숫자/문자열 호환 비교)
        if (user_id and (str(l_user_id) == str(user_id) or str(l_member_id) == str(user_id))) or \
           (user_email and (l_user_id == user_email or l_member_id == user_email)):

            b_id = loan.get("book_id") if isinstance(loan, dict) else getattr(loan, "book_id", None)
            book_info = book_dict.get(b_id, {})

            # 책 상세정보 추출
            book_title = book_info.get("title") if isinstance(book_info, dict) else getattr(book_info, "title", "알 수 없는 도서")
            author = book_info.get("author") if isinstance(book_info, dict) else getattr(book_info, "author", "저자 미상")

            status = loan.get("status") if isinstance(loan, dict) else getattr(loan, "status", "borrowed")
            loan_date = loan.get("loan_date") if isinstance(loan, dict) else getattr(loan, "loan_date", "-")
            return_date = loan.get("return_date") if isinstance(loan, dict) else getattr(loan, "return_date", None)

            my_history.append({
                "loan_id": loan.get("loan_id") if isinstance(loan, dict) else getattr(loan, "loan_id", None),
                "title": book_title,
                "author": author,
                "loan_date": loan_date,
                "return_date": return_date if return_date else "대출 중 (미반납)",
                "status": "✅ 반납완료" if status == "returned" or return_date else "📖 대출중"
            })

    return my_history


def print_my_loan_history(current_user: dict) -> None:
    """로그인한 사용자(current_user)의 대출/반납 현황을 콘솔 화면에 출력합니다."""
    history = get_my_loan_history(current_user)
    user_name = current_user.get("name") if isinstance(current_user, dict) else getattr(current_user, "name", "회원")

    print("\n" + "=" * 60)
    print(f"         📚 [{user_name}] 님의 도서 대출 / 반납 현황")
    print("=" * 60)

    if not history:
        print("  대출 또는 반납된 내역이 존재하지 않습니다.")
    else:
        for idx, item in enumerate(history, 1):
            print(f" {idx}. [{item['status']}] {item['title']} ({item['author']})")
            print(f"    - 대출일: {item['loan_date']}")
            print(f"    - 반납일: {item['return_date']}")
            print("-" * 60)

    print("=" * 60 + "\n")


############

if __name__ == "__main__":
    dummy_user = {
        "user_id": 1,
        "email": "dudu1@naver.com",
        "name": "dudu",
        "point": 100
    }

    # 대출 현황 화면 출력
    print_my_loan_history(dummy_user)