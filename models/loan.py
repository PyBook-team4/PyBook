# models/loan.py
from datetime import datetime, timedelta

class Loan:
    def __init__(self, loan_id: int, member_id: str | int, book_id: int, 
                 loan_date: str = None, due_date: str = None, 
                 return_date: str = None, status: str = "대출중"):
        pass

    def to_dict(self) -> dict:
        """객체를 JSON 저장을 위한 딕셔너리로 변환"""
        pass

    @classmethod
    def from_dict(cls, data: dict):
        """JSON 딕셔너리를 Loan 객체로 생성"""
        pass