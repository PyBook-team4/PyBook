# models/member.py
from datetime import datetime

class Member:
    def __init__(self, user_id: int, email: str, pw: str, name: str, 
                 phone: str = "", interest: str = "", point: int = 0, 
                 tier: str = "Bronze", last_login_date: str = None, created_at: str = None):
        pass

    def to_dict(self) -> dict:
        """객체를 JSON 저장을 위한 딕셔너리로 변환"""
        pass

    @classmethod
    def from_dict(cls, data: dict):
        """JSON 딕셔너리를 Member 객체로 생성"""
        pass