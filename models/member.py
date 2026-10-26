# models/member.py
from datetime import datetime

class Member:
    """회원 데이터 저장 클래스"""

    def __init__(self,email,pw,name,phone,interest, pw_question="",pw_answer=""):
        self.email = email
        self. pw= pw
        self.name = name
        self.phone = phone
        self.interest = interest
        self.pw_question = pw_question
        self.pw_answer = pw_answer
   

    def to_dict(self) -> dict:
        """
        Member 객체를 JSON 파일 저장용 딕셔너리(dict)로 변환합니다.
        """
        return {
            "email": self.email,
            "pw" : self.pw,
            "name": self.name,
            "phone": self.phone,
            "interest": self.interest,
            "pw_question": self.pw_question,
            "pw_answer": self.pw_answer
            
     
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
            pw_answer=data.get("pw_answer", "")

        )