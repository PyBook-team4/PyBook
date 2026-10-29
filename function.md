# PyBook 함수 기능 정리

> 파일별 함수와 기능을 정리한 문서입니다.
> 이름이 `_`로 시작하는 함수는 해당 파일 안에서만 쓰는 내부 함수입니다.
> 실행: `python3 main.py` (Python 3.12 이상)

## 전체 구조

```
main.py                 프로그램 시작, 메인 메뉴 (회원가입 / 로그인 / 관리자 로그인 / 종료)
 ├─ views/              화면과 메뉴 흐름 (입력을 받고 결과를 출력)
 │   ├─ user_view.py    일반 회원 메뉴
 │   └─ admin_view.py   관리자 메뉴
 ├─ services/           기능 로직 (데이터 읽기·쓰기, 검증, 계산)
 ├─ models/             데이터 클래스 (Member, Book, Loan, Record)
 ├─ utils/              공통 도구 (JSON 파일, 외부 API, 그래프)
 └─ animations/         콘솔 화면 효과
```

### 데이터 파일 (`data/`)

| 파일 | 내용 | 모델 |
|---|---|---|
| `members.json` | 회원 정보 | `Member` |
| `books.json` | 도서 정보, 재고 | `Book` |
| `loans.json` | 대출/반납 기록 | `Loan` |
| `records.json` | 평점, 리뷰 | `Record` |

### 포인트와 등급 규칙

| 항목 | 포인트 |
|---|---|
| 정상 반납 | +10 |
| 평점 등록 | +3 |
| 리뷰 작성 (20자 이상) | +3 |
| 리뷰 작성 후 AI 퀴즈 정답 | +4 |
| 반납 지연 | 1일당 -1 (0 미만으로 내려가지 않음) |

| 등급 | 필요 포인트 | 최대 대출 권수 | 대출 기간 |
|---|---|---|---|
| BRONZE | 0 이상 | 2권 | 7일 |
| SILVER | 200 이상 | 4권 | 14일 |
| GOLD | 500 이상 | 6권 | 21일 |
| VIP | 1000 이상 | 8권 | 30일 |

---

## main.py

| 함수 | 기능 |
|---|---|
| `main()` | 시작 애니메이션 후 메인 메뉴를 반복 표시. 회원가입, 로그인(성공 시 `run_logged_in_menu`), 비밀번호 찾기, 관리자 로그인(성공 시 `run_admin_menu`), 종료를 처리 |

---

## views/user_view.py (일반 회원 화면)

메인 메뉴: `1` 도서 검색·대출 / `2` 반납 / `3` 도서 추천(예정) / `4` 명예의 전당 / `5` 챗봇 / `9` 마이페이지 / `0` 로그아웃

| 함수 | 기능 |
|---|---|
| `run_logged_in_menu(current_user)` | 로그인 후 메인 메뉴. 메뉴를 그릴 때마다 회원 정보를 파일에서 다시 읽어 포인트·이름을 최신으로 표시 |
| `_handle_book_search_and_borrow(current_user)` | 도서 검색 → 결과 내 재검색 / 정렬 / 번호를 골라 대출 |
| `_handle_book_return(current_user)` | 대출 중인 도서 목록을 보여주고, 고른 도서를 반납 처리 |
| `_handle_my_page(current_user) -> bool` | 마이페이지 메뉴: 내 정보 / 독서 연대기 / 대출 현황 / 회원정보 수정 / 회원 탈퇴. 탈퇴에 성공하면 `True`를 반환해 로그아웃 처리 |
| `_rating_to_stars(rating) -> str` | 평점을 반올림한 별 5개로 변환 (예: `4` → `★★★★☆`, 없으면 `평점 없음`) |
| `_show_reading_timeline(current_user)` | 반납 완료한 도서를 월별로 묶어 출력하고, timeline 리스트를 반환 |
| `_open_reading_charts(current_user, timeline)` | 독서 연대기 그래프 창 열기. matplotlib이 없으면 설치 안내만 출력 |
| `_show_current_loans(current_user)` | 현재 대출 중인 도서, 반납기한까지 남은 일수(D-day)나 연체 일수, 등급별 대출 한도 출력 |

## views/admin_view.py (관리자 화면)

| 함수 | 기능 |
|---|---|
| `run_admin_menu()` | 관리자 메인 메뉴: 회원 관리 / 도서 관리 / 로그아웃 |
| `_handle_member_management()` | 회원 관리: 전체 목록(정렬) / 검색 / 등록 / 정보 수정 / 강제 삭제 / 휴면 회원 조회 |
| `_handle_book_management()` | 도서 관리: 전체 목록 / 신규 등록 / 정보 수정 / 삭제 / 평점·리뷰 수정 |
| `_display_member_summary(members)` | 회원 ID, 이름, 이메일을 표 형태로 출력 |
| `_select_member_id(action) -> int \| None` | 회원 목록을 보여주고 작업할 회원 ID를 입력받음. 취소(`0`)하거나 잘못 입력하면 `None` |

---

## services/member_service.py (회원)

| 함수 | 기능 |
|---|---|
| `admin_login(pw) -> tuple` | `.env`의 `PASSWORD`와 비교해 관리자 인증. `(성공여부, 메시지)` 반환 |
| `_get_members() -> list` | `members.json`을 읽어 `Member` 객체 리스트로 반환 (admin_member_service에서도 사용) |
| `_save_members(members)` | `Member` 객체 리스트를 `members.json`에 저장 (admin_member_service에서도 사용) |
| `_hash_password(password) -> str` | 비밀번호를 SHA-256으로 해싱 (admin_member_service에서도 사용) |
| `is_valid_email(email) -> bool` | 이메일 형식 검증 (5자 이상, `@`와 도메인 포함) |
| `is_valid_pw(pw) -> bool` | 비밀번호 검증 (5자 이상, 특수문자 1개 이상) |
| `is_valid_phone(phone) -> bool` | 연락처 검증 (010으로 시작하는 숫자 11자리, `-`와 공백은 무시) |
| `is_valid_find_pw() -> dict` | 비밀번호 찾기 질문을 고르고 답변을 입력받아 `{"question", "answer"}` 반환 |
| `signup_interests() -> list` | 관심분야 10개 중 최대 3개를 선택받아 리스트로 반환 (관리자 회원 수정에서도 사용) |
| `signup() -> bool` | 회원가입: 이메일 중복·형식, 비밀번호(2차 확인), 비밀번호 찾기 질문, 이름, 연락처, 관심분야 입력 후 저장 (가입 포인트 100) |
| `login(email, pw) -> tuple` | 로그인. 성공하면 마지막 로그인 시각을 갱신하고 `(True, 회원dict)`, 실패하면 `(False, None)` |
| `get_member_by_id(user_id) -> dict \| None` | user_id로 회원의 최신 정보를 dict로 반환 (화면 갱신용) |
| `logout(email) -> bool` | 항상 `True` 반환 (현재 사용하지 않음. 로그아웃은 view에서 메뉴를 빠져나가는 방식) |
| `withdraw(email) -> bool` | 회원 탈퇴: 비밀번호 재확인 → 대출 중인 도서가 있으면 거부 → 최종 확인 후 삭제 |
| `update(email) -> bool` | 회원정보 수정 메뉴: 비밀번호 / 이름 / 연락처 / 관심분야 / 비밀번호 찾기 질문·답변. `0`을 누르면 저장 |
| `find_pw() -> bool` | 비밀번호 찾기: 이메일 확인 → 질문에 답변 → 새 비밀번호로 재설정 |
| `show_member_info(email) -> dict \| None` | 내 정보 출력 (비밀번호는 `********`, 등급은 포인트로 계산) |

## services/admin_member_service.py (관리자 - 회원)

| 함수 | 기능 |
|---|---|
| `get_all_members() -> list` | 전체 회원 dict 리스트. 포인트로 계산한 `tier`, `max_books`, `loan_days` 포함 |
| `sort_members(member_list, sort_by, reverse) -> list` | `user_id` / `name` / `point` / `created_at` 기준으로 정렬 |
| `search_members(keyword) -> list` | 이름, 이메일, 전화번호에 키워드가 포함된 회원 검색 (빈 키워드면 전체) |
| `admin_register_member(email, name, phone, point, interest) -> tuple` | 관리자 회원 등록. 이메일 형식·중복, 이름, 연락처 11자리 검증. 초기 비밀번호는 휴대폰 뒷 4자리 |
| `admin_update_member(user_id, new_email, reset_pw_to_phone_last4, new_interest, new_point, new_created_at) -> tuple` | 전달된 항목만 수정 (이메일 형식·중복 검사, 비밀번호 초기화, 포인트는 0 미만 방지) |
| `admin_delete_member(user_id) -> tuple` | 회원 강제 삭제. 대출 중인 도서가 있으면 삭제 불가 |
| `get_dormant_members(days=90) -> list` | 휴면 회원 조회: 로그인 기록이 없거나 마지막 로그인이 `days`일 이상 지난 회원 (`dormant_reason` 포함) |

## services/admin_book_service.py (관리자 - 도서)

| 함수 | 기능 |
|---|---|
| `register_book(title, author, publisher, genre, isbn, total_stock, available_stock) -> bool` | 신규 도서 등록. 필수 항목, 제목 중복, 보유량(1~10), 대여 가능 재고(0~보유량) 검증 |
| `book_delete(book_id) -> bool` | 도서 삭제. 대출 중인 도서는 삭제 불가 |
| `book_update(book_id, field_choice, new_value) -> bool` | 도서 정보 1개 항목 수정 (1 제목 / 2 저자 / 3 출판사 / 4 ISBN / 5 장르 / 6 평점 / 7 총 보유량 / 8 대여 가능 재고). 평점은 0~5, 재고는 `대여 가능 + 대출 중 = 총 보유량`이 유지되도록 검증 |
| `get_all_book_records() -> list` | 전체 평점·리뷰 기록에 도서 제목(`book_title`)을 붙여 반환 |
| `admin_update_review(record_id, new_rating, new_review) -> tuple` | 특정 기록의 평점(0~5)과 리뷰 수정. 수정할 항목이 없으면 실패 |

## services/loan_service.py (대출 / 반납)

| 함수 | 기능 |
|---|---|
| `get_tier_info_by_point(point) -> dict` | 포인트로 등급, 최대 대출 권수, 대출 기간 계산. **등급 계산은 이 함수 하나만 사용** (다른 서비스에서 import) |
| `borrow(user_id, book_id) -> bool` | 도서 대출: 등급별 대출 한도 확인 → 재고 확인 → 대출 기록 생성(`due_date` = 오늘 + 대출 기간) → 재고 1 감소 |
| `return_book(loan_id) -> bool` | 도서 반납: 상태를 `반납완료`로 변경, 실제 반납일 기록, 재고 복구, 정상 반납/연체 포인트 처리 → 평점(+3) → 리뷰 20자 이상(+3) → 리뷰를 남겼으면 AI 퀴즈(정답 +4) → 평점이나 리뷰가 있으면 `records.json`에 저장 |
| `_play_book_quiz(book_title) -> bool` | `OpenAIClient.generate_book_quiz()`로 퀴즈를 받아 문제를 보여주고 채점 후 해설 출력. 정답이면 `True`. API 키가 없거나 응답 형식이 맞지 않으면 건너뜀 |
| `get_user_active_loans(user_id) -> list` | 회원의 대출 중인 도서 목록 (반납 화면용, 도서 제목과 반납기한 포함) |

## services/my_loan_service.py (마이페이지)

| 함수 | 기능 |
|---|---|
| `get_reading_timeline(user_id) -> list[dict]` | 독서 연대기: 반납 완료한 도서를 반납일 순으로 반환 (제목, 저자, 장르, 대출일, 반납일, 평점, 리뷰) |
| `get_current_loan_status(user_id, point) -> dict` | 대출 현황: 대출 중인 도서와 남은 일수(`remaining_days`, 음수면 연체), 등급과 대출 한도 반환 |
| `_find_record(records, loan) -> dict \| None` | 대출 기록에 해당하는 평점·리뷰 찾기 (`loan_id`가 있으면 그것으로, 없으면 같은 회원·도서·반납일로) |

## services/search_service.py (도서 검색)

| 함수 | 기능 |
|---|---|
| `search_books(keyword) -> (list, str)` | 제목, 저자, 장르로 도서 검색. 각 도서에 리뷰 목록(`reviews`)을 붙여 `(결과, 메시지)` 반환 |
| `scnd_search_books(frst_results, scnd_keyword) -> (list, str)` | 1차 검색 결과 안에서 다시 검색 |
| `sort_books(book_list, sort_by, reverse) -> list` | `title` / `rating` / `author` / `available_stock` 기준 정렬 |

## services/analytics_service.py (통계)

| 함수 | 기능 |
|---|---|
| `show_reading_king(top_n=3) -> list` | 회원별 반납 완료 권수를 집계해 다독왕 상위 `top_n`명을 출력하고, 전체 순위 리스트 반환 |

## services/ai_service.py (AI 챗봇)

| 클래스 / 메서드 | 기능 |
|---|---|
| `AIChatService` | AI 사서 챗봇. 시스템 프롬프트(역할, 사고 과정, 예시)와 대화 기록을 관리 |
| `__init__()` | `OpenAIClient` 생성, 시스템 프롬프트 설정, 대화 기록 최대 11개(시스템 1 + 최근 대화 10) |
| `start_chat()` | 채팅 반복. `종료` / `exit` / `q` / `quit`로 종료. 기록이 11개를 넘으면 오래된 대화부터 삭제(슬라이딩 윈도우) |

## services/book_service.py (도서 데이터 수집)

| 함수 | 기능 |
|---|---|
| `initialize_books_if_empty()` | `books.json`이 비어 있으면 국립중앙도서관 API로 키워드 5개 × 20권을 수집해 저장 (현재 호출하는 곳 없음) |
| `search_books_by_keyword(keyword) -> list` | 국립중앙도서관 API로 실시간 도서 검색 (현재 테스트 코드에서만 사용) |

### 참고: 빈 파일
- `utils/gemini_client.py`: 비어 있음 (Gemini 퀴즈용 예정)

---

## models/ (데이터 클래스)

모든 모델은 같은 구조입니다.
- `__init__(...)`: 객체 생성 (날짜를 넘기지 않으면 현재 시각)
- `to_dict()`: JSON 저장용 dict로 변환
- `from_dict(data)` (classmethod): JSON dict로 객체 생성 (없는 값은 기본값으로 채움)

| 클래스 | 파일 | 주요 속성 |
|---|---|---|
| `Member` | `models/member.py` | `user_id`, `email`, `pw`(해시), `name`, `phone`, `interest`(리스트), `point`, `pw_question`, `pw_answer`, `created_at`, `last_login` |
| `Book` | `models/book.py` | `id`, `title`, `author`, `publisher`, `genre`, `isbn`, `rating`, `total_stock`, `available_stock`, `reg_date` |
| `Loan` | `models/loan.py` | `loan_id`, `user_id`, `book_id`, `loan_date`, `due_date`(반납 기한), `return_date`(실제 반납일, 반납 전 `None`), `status`(`대출중` / `반납완료`) |
| `Record` | `models/record.py` | `record_id`, `user_id`, `book_id`, `rating`, `review`, `created_at` |

> `Member.from_dict()`는 `point`가 없으면 `0`, `interest`가 없으면 `[]`로 채웁니다.
> 예전 대출 기록은 `due_date` 없이 `return_date`에 기한이 들어 있어서, 관련 함수들은 `due_date`가 없으면 `return_date`를 기한으로 읽습니다.

---

## utils/

### file_handler.py

| 함수 | 기능 |
|---|---|
| `load_json(filename) -> list` | JSON 파일 읽기. 파일이 없거나 비어 있으면 `[]`. 파일이 손상됐으면 데이터 손실을 막기 위해 프로그램 종료 |
| `save_json(filename, data_list)` | 임시 파일(`.tmp`)에 먼저 쓴 뒤 원본과 교체 (저장 중 오류가 나도 원본 보존) |

### openai_client.py

| 클래스 / 메서드 | 기능 |
|---|---|
| `OpenAIClient` | `.env`의 `OPENAI_API_KEY`로 OpenAI 클라이언트 생성 (키가 없으면 `ValueError`) |
| `generate_book_quiz(book_title) -> str` | 도서 4지선다 퀴즈 1개 생성 (`gpt-4o`). `[문제]`, 보기 1~4, `[정답]`, `[해설]` 형식의 문자열. 오류 시 오류 문장 반환 |
| `generate_chat_response(messages) -> str` | 대화 기록을 받아 챗봇 응답 생성 (`gpt-4o-mini`) |

### book_api_client.py

| 클래스 / 메서드 | 기능 |
|---|---|
| `BookClient` | `.env`의 `API_KEY`로 국립중앙도서관 검색 API 클라이언트 생성 |
| `search_book(keyword, page_size=5) -> dict \| str` | 키워드로 도서 검색. 성공하면 JSON dict, 실패하면 오류 문장 |

### visualizer.py (matplotlib 필요)

| 함수 | 기능 |
|---|---|
| `show_reading_charts(timeline, user_name) -> bool` | 독서 연대기 그래프 창 표시: 왼쪽 월별 완독 권수(빈 달은 0), 오른쪽 장르별 완독 권수(많은 순) |
| `_set_korean_font()` | 운영체제에 맞는 한글 폰트 설정 (Mac: AppleGothic, Windows: 맑은 고딕) |
| `_month_range(first, last) -> list[str]` | 시작 월부터 끝 월까지 빠짐없는 월 목록 (`"2026-08"` 형식) |
| `_style_axis(ax, grid_axis)` | 그래프 축 스타일 (테두리 정리, 옅은 격자) |

---

## animations/animation_effect.py

| 함수 | 기능 |
|---|---|
| `clear_screen()` | 운영체제에 맞게 콘솔 화면 지우기 (Windows: `cls`, Mac/Linux: `clear`) |
| `show_intro_animation()` | 프로그램 시작 시 PYBOOK 로고와 환영 문구 애니메이션 |
| `show_goodbye_animation()` | 프로그램 종료 시 GOODBYE 로고와 인사 문구 애니메이션 |
| `typing_effect(text, speed=0.03)` | 글자를 한 자씩 타이핑하듯 출력 |
| `loading_spinner(text, duration=2.0)` | `\| / - \` 회전 스피너를 `duration`초 동안 표시 |
| `connecting_ai_animation()` | 챗봇 메뉴 진입 시 연결 애니메이션 |

> `animation_effect_test1.py`, `animation_effect_test2.py`는 애니메이션 시험용 파일로, 프로그램에서는 사용하지 않습니다.
