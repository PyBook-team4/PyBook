# PyBook 데이터 구조 (JSON 스키마)

> PyBook은 별도 데이터베이스 없이 `data/` 폴더의 JSON 파일 4개를 저장소로 사용합니다.
> 각 파일은 **객체(dict)들의 리스트**이며, `models/`의 클래스와 1:1로 대응합니다. (`to_dict()` / `from_dict()`로 변환)
> `data/*.json`은 `.gitignore`에 포함되어 git에 올라가지 않으므로, 팀원 간에는 파일을 따로 공유합니다.

## 목차
- [파일 관계](#파일-관계)
- [members.json (회원)](#membersjson-회원)
- [books.json (도서)](#booksjson-도서)
- [loans.json (대출/반납)](#loansjson-대출반납)
- [records.json (평점/감상평)](#recordsjson-평점감상평)
- [데이터를 직접 수정할 때 주의할 점](#데이터를-직접-수정할-때-주의할-점)

---

## 파일 관계

```
members.json                 books.json
 user_id ◄──────┐   ┌──────► id
                │   │
            loans.json  (대출 1건 = 1개)
             loan_id, user_id, book_id, status ...
                │   │
            records.json (반납할 때 평점이나 감상평을 남기면 1개)
             record_id, user_id, book_id, rating, review ...
```

- `loans.user_id` → `members.user_id`, `loans.book_id` → `books.id`
- `records.user_id` → `members.user_id`, `records.book_id` → `books.id`
- 각 ID는 **기존 최대값 + 1**로 자동 생성합니다.

---

## members.json (회원)

모델: `models/member.py` → `Member`

```json
[
  {
    "user_id": 1,
    "email": "test1@naver.com",
    "pw": "SHA-256 해시 문자열 (64자)",
    "name": "test1",
    "phone": "01012345678",
    "interest": ["철학", "종교"],
    "point": 100,
    "pw_question": "내가 생각하는 나만의 보물1호는?",
    "pw_answer": "비밀번호 찾기 답변",
    "created_at": "2026-10-27 14:13:31",
    "last_login": "2026-10-27 14:39:07"
  }
]
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `user_id` | int | 회원 고유 번호 |
| `email` | str | 로그인 아이디 (중복 불가) |
| `pw` | str | 비밀번호 **SHA-256 해시** (원래 비밀번호는 저장하지 않음) |
| `name` | str | 이름 |
| `phone` | str | 연락처 (010으로 시작하는 11자리, 회원가입 시 하이픈 포함 입력 가능) |
| `interest` | list[str] | 관심분야 최대 3개. 철학 / 종교 / 사회과학 / 자연과학 / 기술과학 / 예술 / 언어 / 문학 / 역사 |
| `point` | int | 누적 포인트 (가입 시 100). **등급은 저장하지 않고** 포인트로 그때그때 계산 |
| `pw_question` | str | 비밀번호 찾기 질문 |
| `pw_answer` | str | 비밀번호 찾기 답변 |
| `created_at` | str | 가입일시 `YYYY-MM-DD HH:MM:SS` |
| `last_login` | str \| null | 마지막 로그인 일시. 가입 후 로그인 전이면 `null` (휴면 회원 판정에 사용) |

> 관리자가 등록한 회원은 초기 비밀번호가 휴대폰 번호 뒷 4자리입니다.

---

## books.json (도서)

모델: `models/book.py` → `Book`

```json
[
  {
    "id": 102,
    "title": "사피엔스",
    "author": "유발 하라리",
    "publisher": "김영사",
    "genre": "역사",
    "isbn": "DUMMY-102",
    "rating": 4.7,
    "total_stock": 2,
    "available_stock": 2,
    "reg_date": "2026-06-01",
    "keywords": "인류사 진화 문명 농업혁명 인지혁명 세계사"
  }
]
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `id` | int | 도서 고유 번호 |
| `title` | str | 제목 (중복 등록 불가) |
| `author` | str | 저자 |
| `publisher` | str | 출판사 |
| `genre` | str | 장르. 회원 관심분야와 같은 9개 분류 사용 (KDC 대분류 기준, 프로그래밍 도서는 `기술과학`) |
| `isbn` | str | ISBN (더미 데이터는 `DUMMY-번호`) |
| `rating` | float | 도서 평점 0.0 ~ 5.0 (관리자 등록 시 기본 3.0) |
| `total_stock` | int | 총 보유량 1 ~ 10 |
| `available_stock` | int | 대여 가능 재고. 항상 `available_stock + 대출 중 권수 = total_stock` |
| `reg_date` | str | 등록일 `YYYY-MM-DD` |
| `keywords` | str | **맞춤 도서 추천용 키워드** (띄어쓰기로 구분, 비어 있어도 됨) |

> 추천 정확도는 `genre`와 `keywords`의 영향을 가장 크게 받습니다. 도서를 추가할 때 주제가 드러나는 키워드를 3~8개 넣는 것을 권장합니다.

---

## loans.json (대출/반납)

모델: `models/loan.py` → `Loan`

```json
[
  {
    "loan_id": 101,
    "user_id": 4,
    "book_id": 101,
    "loan_date": "2026-06-02 10:00:00",
    "due_date": "2026-06-09 10:00:00",
    "return_date": "2026-06-08 18:20:00",
    "status": "반납완료"
  },
  {
    "loan_id": 112,
    "user_id": 4,
    "book_id": 2,
    "loan_date": "2026-10-29 15:00:00",
    "due_date": "2026-11-05 15:00:00",
    "return_date": null,
    "status": "대출중"
  }
]
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `loan_id` | int | 대출 고유 번호 |
| `user_id` | int | 대출한 회원 (`members.user_id`) |
| `book_id` | int | 대출한 도서 (`books.id`) |
| `loan_date` | str | 대출일시 `YYYY-MM-DD HH:MM:SS` |
| `due_date` | str | **반납 기한** = 대출일 + 등급별 대출 기간 (BRONZE 7일 ~ VIP 30일) |
| `return_date` | str \| null | **실제 반납일시**. 반납 전에는 `null` |
| `status` | str | `"대출중"` 또는 `"반납완료"` |

> ⚠️ **예전 데이터 호환:** `due_date`가 생기기 전의 기록은 `due_date`가 없고, `대출중`인 기록의 `return_date`에 반납 기한이 들어 있습니다. 코드에서는 `due_date`가 없으면 `return_date`를 기한으로 읽도록 처리되어 있습니다.

---

## records.json (평점/감상평)

모델: `models/record.py` → `Record`

```json
[
  {
    "record_id": 2003,
    "user_id": 4,
    "book_id": 102,
    "rating": 5,
    "review": "인류 문명이 농업혁명과 인지혁명을 거쳐 발전해 온 과정이 정말 흥미로웠다",
    "created_at": "2026-08-07"
  }
]
```

| 필드 | 타입 | 설명 |
|---|---|---|
| `record_id` | int | 기록 고유 번호 (첫 기록은 1001부터) |
| `user_id` | int | 작성한 회원 |
| `book_id` | int | 대상 도서 |
| `rating` | int \| float \| null | 평점 1 ~ 5. 평점 없이 감상평만 남기면 `null` (관리자는 0.0 ~ 5.0 소수로 수정 가능) |
| `review` | str | 감상평. 포인트를 받으려면 20자 이상 (빈 문자열 가능) |
| `created_at` | str | 작성일 `YYYY-MM-DD` (= 반납한 날) |

> - 반납할 때 **평점이나 감상평 중 하나라도** 남기면 기록이 생성됩니다.
> - 기록에 `loan_id`가 없어서, 독서 연대기는 **같은 회원 + 같은 도서 + 반납한 날짜**로 어느 대출의 감상평인지 연결합니다.
> - 맞춤 도서 추천은 20자 이상이고 평점이 3점 이상(또는 평점 없음)인 감상평만 사용합니다.

---

## 데이터를 직접 수정할 때 주의할 점

1. **수정 전에 백업**하세요. 쉼표 하나만 틀려도 JSON이 깨지고, 프로그램은 데이터 손실을 막기 위해 **시작 시 종료**됩니다.
   ```bash
   cp data/books.json data/books.json.bak
   ```
2. 저장 후 아래 명령으로 문법을 확인하세요. 오류가 없으면 아무것도 출력되지 않습니다.
   ```bash
   python3 -m json.tool data/books.json > /dev/null
   ```
3. 재고를 고칠 때는 `available_stock + 대출중 권수 = total_stock`이 맞는지 확인하세요.
4. 회원·도서를 지울 때는 그 ID를 쓰는 `loans`/`records` 기록이 남지 않는지 확인하세요. (프로그램에서는 대출 중인 회원·도서 삭제를 막고 있습니다)
5. `pw`에는 원래 비밀번호가 아니라 **SHA-256 해시**를 넣어야 로그인됩니다. 테스트 계정은 회원가입이나 관리자 회원 등록으로 만드는 것이 안전합니다.
