# models/member.py
from datetime import datetime

class Member:
    """회원 데이터 저장 클래스"""

    def __init__(self, email: str, pw: str, name: str, phone: str = "", interest: list = None, 
                 pw_question: str = "", pw_answer: str = "", 
                 created_at: str = None, last_login: str = None):
        self.email = email
        self. pw= pw
        self.name = name
        self.phone = phone
        self.interest = interest
        self.pw_question = pw_question
        self.pw_answer = pw_answer
        # 최초 가입일(기본값: 현재 날짜/시간 string)
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 마지막 로그인 일시(가입 초기에는 None 또는 created_at과 동일하게 설정 가능)
        self.last_login = last_login

    def to_dict(self) -> dict:
        """
        Member 객체를 JSON 파일 저장용 딕셔너리(dict)로 변환합니다.
        """
        return {
            "email"      : self.email,
            "pw"         : self.pw,
            "name"       : self.name,
            "phone"      : self.phone,
            "interest"   : self.interest,
            "pw_question": self.pw_question,
            "pw_answer"  : self.pw_answer,
            "created_at" : self.created_at,
            "last_login" : self.last_login
            
     
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Member":
        """
        JSON 파일에서 읽어온 딕셔너리(dict) 데이터를 기반으로 Member 객체를 복원합니다.
        """
        return cls(
            email=data.get("email", ""),
            pw=data.get("pw", ""),
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            interest=data.get("interest", ""),
            pw_question=data.get("pw_question", ""),
            pw_answer=data.get("pw_answer", ""),
            created_at=data.get("created_at"),
            last_login=data.get("last_login")

        )