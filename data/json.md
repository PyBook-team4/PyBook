## json schema 

data/member.json (회원정보)
[
  {
    "user_id:101,         
    "email": "test@naver.com",   //id
    "pw": "hashed_password_string",
    "name": "test",
    "phone": "010-1234-5678",
    "interest": "IT/개발, 소설",
    "point": 120,
    "tier": "Silver",
    "last_login_date": "2026-10-19",
    "created_at": "2026-10-01"
  }
]

data/books.json csv (도서 정보)
[
  {
    "id": 1,
    "title": "점프 투 파이썬",
    "author": "박응용",
    "publisher": "이지스퍼블리싱",
    "genre": "IT/개발",
    "isbn": "9788968482025",
    "rating": 4.8,
    "total_stock": 3,
    "available_stock": 2,
    "reg_date": "2026-10-01"
  }
]

data/loans.json (대출 및 반납 이력)
[
  {
    "loan_id": 101,
    "user_id": "test",
    "book_id": 1,
    "loan_date": "2026-10-15",
    "due_date": "2026-10-29",
    "return_date": null,
    "status": "대출중"
  }
]

data/records.json (독서 노트 및 ai 분석 결과)
[
  {
    "record_id": 1001,
    "user_id": 101,
    "book_id": 1,
    "rating": 5,
    "review": "초보자가 파이썬 기초를 다지기에 이만한 책이 없습니다.",
    "sentiment_score": 0.92,        //이 부분은 구현시 우선 건너뛰어도 됩니다. 
    "created_at": "2026-10-18"
  }
]