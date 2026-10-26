# services/loan_service.py
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
