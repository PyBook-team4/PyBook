# models/book.py
from datetime import datetime

class Book:
    def __init__(self, id: int, title: str, author: str, publisher: str, 
                 genre: str, isbn: str, rating: float = 5.0, 
                 total_stock: int = 2, available_stock: int = 2, reg_date: str = None):
        self.id = id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.genre = genre
        self.isbn = isbn
        self.rating = rating
        self.total_stock = total_stock
        self.available_stock = available_stock
        self.reg_date = reg_date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        """객체를 JSON 저장을 위한 딕셔너리로 변환"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "genre": self.genre,
            "isbn": self.isbn,
            "rating": self.rating,
            "total_stock": self.total_stock,
            "available_stock": self.available_stock,
            "reg_date": self.reg_date
        }

    @classmethod
    def from_dict(cls, data: dict):
        """JSON 딕셔너리를 Book 객체로 생성"""
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            author=data.get("author", "미상"),
            publisher=data.get("publisher", "미상"),
            genre=data.get("genre", "일반"),
            isbn=data.get("isbn", ""),
            rating=data.get("rating", 5.0),
            total_stock=data.get("total_stock", 2),
            available_stock=data.get("available_stock", 2),
            reg_date=data.get("reg_date")
        )