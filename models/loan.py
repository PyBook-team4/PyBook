# models/loan.py
from datetime import datetime

class Loan:
    def __init__(self, loan_id: int, user_id: int, book_id: int, 
                 loan_date: str = None, return_date: str = None, status: str = "대출중"):
        self.loan_id = loan_id
        self.user_id = user_id
        self.book_id = book_id
        self.loan_date = loan_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.return_date = return_date
        self.status = status

    def to_dict(self) -> dict:
        """JSON 저장을 위해 객체 속성을 딕셔너리로 변환"""
        return {
            "loan_id": self.loan_id,
            "user_id": self.user_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date,
            "return_date": self.return_date,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict):
        """JSON 딕셔너리 데이터를 받아 Loan 객체로 생성"""
        return cls(
            loan_id=data.get("loan_id"),
            user_id=data.get("user_id"),
            book_id=data.get("book_id"),
            loan_date=data.get("loan_date"),
            return_date=data.get("return_date"),
            status=data.get("status", "대출중")
        )