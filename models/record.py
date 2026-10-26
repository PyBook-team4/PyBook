# models/record.py
from datetime import datetime

class Record:
    """독서 기록 및 감상평(평점/리뷰) 모델 클래스"""
    def __init__(self, record_id: int, member_id: str | int, book_id: int, 
                 rating: float | int = None, review: str = "", created_at: str = None):
        self.record_id = record_id
        self.member_id = member_id
        self.book_id = book_id
        self.rating = rating
        self.review = review
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        """JSON 저장을 위해 객체를 딕셔너리로 변환"""
        return {
            "record_id": self.record_id,
            "member_id": self.member_id,
            "book_id": self.book_id,
            "rating": self.rating,
            "review": self.review,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        """JSON 딕셔너리 데이터를 받아 Record 객체로 생성"""
        return cls(
            record_id=data.get("record_id"),
            member_id=data.get("member_id"),
            book_id=data.get("book_id"),
            rating=data.get("rating"),
            review=data.get("review", ""),
            created_at=data.get("created_at")
        )