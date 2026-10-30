# 📚 PyBook

<div align="center">

**Python 콘솔 기반 객체지향 지능형 도서 대출 및 독서 기록 관리 시스템**

4조 미니 프로젝트

<img src="https://img.shields.io/badge/Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white"/> <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white"/> <img src="https://img.shields.io/badge/Matplotlib-11557C?style=flat-square&logoColor=white"/> <img src="https://img.shields.io/badge/JSON-000000?style=flat-square&logo=json&logoColor=white"/>

</div>

---

## 목차
- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [시스템 아키텍처](#시스템-아키텍처)
- [프로젝트 구조](#프로젝트-구조)
- [시작하기](#시작하기)
- [주요 구현 사항](#주요-구현-사항)
- [트러블슈팅](#트러블슈팅)
- [팀원 소개](#-팀원-소개)

---

## 💡 프로젝트 소개

**PyBook**은 콘솔 환경에서 동작하는 통합 도서 대출 및 독서 기록 관리 플랫폼입니다.

별도의 데이터베이스 서버 없이 **JSON 파일 저장소**와 **계층형 객체지향 아키텍처**(View – Service – Model)를 기반으로 동작합니다. 도서 검색·대출·반납과 같은 기본 기능에 더해 **포인트/등급제(게이미피케이션)**, **코사인 유사도 기반 맞춤 도서 추천**, **AI 도서 퀴즈와 사서 챗봇**, **Matplotlib 독서 연대기 시각화**를 제공합니다.

### 개발 배경
- 도서 대출 기록이 단순한 이력으로만 남고, **나의 독서 습관을 돌아볼 수 있는 기능**이 부족함
- 반납 후 감상평을 남기거나 다음 책을 고를 **동기와 가이드**가 없음
- 외부 서버 없이도 동작하는 **가볍고 이식성 높은 콘솔 애플리케이션**을 객체지향 설계로 구현

### 진행 기간
**2026.10.13 ~ 2026.10.30** 

---

## 주요 기능

### 1. 회원 및 인증
- 회원가입 시 이메일 형식·중복, 비밀번호 규칙(5자 이상, 특수문자 포함), 연락처 형식 검증
- 비밀번호는 **SHA-256 해시**로 저장하고, 비밀번호 찾기 질문/답변으로 재설정
- 로그인 후 메뉴마다 회원 정보를 다시 불러와 **포인트·이름을 항상 최신 상태로 표시**
- 대출 중인 도서가 있으면 회원 탈퇴 불가

### 2. 도서 검색 및 대출/반납
- 제목·저자·장르 통합 검색과 **결과 내 재검색**
- 제목순 / 평점순 / 저자순 / 재고순 정렬 (오름차순·내림차순)
- 대출 시 **등급별 대출 한도**와 재고 확인, 반납 기한(`due_date`) 자동 설정
- 반납 시 연체 일수 계산, 재고 복구, 포인트 정산

### 3. 포인트 및 등급 제도

| 활동 | 포인트 |
|------|--------|
| 정상 반납 | **+10** |
| 평점 등록 (1~5점) | **+3** |
| 감상평 작성 (20자 이상) | **+3** |
| 감상평 작성 후 AI 도서 퀴즈 정답 | **+4** |
| 반납 지연 | 1일당 **-1** (0점 미만으로 내려가지 않음) |

| 등급 | 필요 포인트 | 최대 대출 권수 | 대출 기간 |
|------|-------------|----------------|-----------|
| BRONZE | 0 이상 | 2권 | 7일 |
| SILVER | 200 이상 | 4권 | 14일 |
| GOLD | 500 이상 | 6권 | 21일 |
| VIP | 1000 이상 | 8권 | 30일 |

### 4. 맞춤 도서 추천 (코사인 유사도)
- 관심분야, **읽은 책의 평점**, **20자 이상 감상평**으로 회원 취향 벡터를 만들고, 아직 읽지 않은 도서와의 코사인 유사도로 추천
- 추천 도서마다 **추천 이유** 표시 (예: "『사피엔스』를 좋게 평가하셔서 추천해요")
- 쌓인 데이터에 따라 단계별 추천

| 단계 | 조건 | 추천 방식 |
|------|------|-----------|
| popular | 관심분야·독서 기록 없음 | 평점 높은 인기 도서 |
| basic | 감상평 5개 미만 | 관심분야 + 읽은 책(평점 가중치) |
| full | 감상평 5개 이상 | 관심분야 + 읽은 책 + 감상평 내용까지 반영 |

- 추천 목록에서 번호를 고르면 **바로 대출**

### 5. 마이페이지 및 독서 연대기
- **나의 독서 연대기**: 반납 완료한 도서를 월별로 묶어 별점(★★★★☆)과 감상평과 함께 출력
- **독서 그래프**: Matplotlib으로 월별 완독 권수와 장르별 완독 권수를 시각화
- **도서 대출 현황**: 대출 중인 도서의 반납 기한(D-day)과 연체 일수, 등급별 대출 한도 표시
- 내 정보 보기, 회원정보 수정(비밀번호·이름·연락처·관심분야·비밀번호 찾기 질문), 회원 탈퇴
- **명예의 전당**: 전체 회원의 완독 권수를 집계한 다독왕 랭킹

### 6. AI 기능 (OpenAI API)
- **AI 도서 퀴즈**: 반납 후 감상평을 남기면 해당 도서의 4지선다 퀴즈 출제, 정답 시 포인트 지급
- **AI 사서 챗봇**: 사서 페르소나와 가드레일(도서와 무관한 질문은 관련 도서 추천으로 전환)을 적용하고, 슬라이딩 윈도우 방식으로 최근 대화 문맥 유지

### 7. 관리자
- **회원 관리**: 전체 회원 정렬 조회, 검색, 회원 등록(휴대폰 뒷 4자리 임시 비밀번호), 정보 수정(이메일·관심분야·포인트·가입일·비밀번호 초기화), 강제 삭제, **휴면 회원 조회**(90일 이상 미접속)
- **도서 관리**: 도서 등록·수정·삭제, 재고 정합성 검증(대여 가능 + 대출 중 = 총 보유량), 대출 중인 도서 삭제 방지
- **평점·리뷰 관리**: 회원이 남긴 평점과 감상평 조회 및 수정

---

## 기술 스택

### Language
<img src="https://img.shields.io/badge/Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white"/>

### Library
<img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white"/> <img src="https://img.shields.io/badge/Matplotlib-11557C?style=flat-square&logoColor=white"/> <img src="https://img.shields.io/badge/python--dotenv-ECD53F?style=flat-square&logo=dotenv&logoColor=black"/> <img src="https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white"/>

### External API
<img src="https://img.shields.io/badge/OpenAI_API-412991?style=flat-square&logo=openai&logoColor=white"/> <img src="https://img.shields.io/badge/국립중앙도서관_Open_API-005BAC?style=flat-square&logoColor=white"/>

### Data Storage
<img src="https://img.shields.io/badge/JSON_File_Storage-000000?style=flat-square&logo=json&logoColor=white"/>

### Cooperation
<img src="https://img.shields.io/badge/Git-F05032?style=flat-square&logo=Git&logoColor=white"/> <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/> <img src="https://img.shields.io/badge/Slack-4A154B?style=flat-square&logo=slack&logoColor=white"/> <img src="https://img.shields.io/badge/Google_Drive-4285F4?style=flat-square&logo=googledrive&logoColor=white"/> <img src="https://img.shields.io/badge/Notion-000000?style=flat-square&logo=notion&logoColor=white"/> <img src="https://img.shields.io/badge/FigJam-F24E1E?style=flat-square&logo=figma&logoColor=white"/>

---

## 시스템 아키텍처

```
┌──────────────────────────────────────────────────────────┐
│                  main.py (프로그램 시작)                  │
│      회원가입 / 로그인 / 비밀번호 찾기 / 관리자 로그인       │
└────────────────────────────┬─────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────┐
│          views/  (화면 출력 + 입력 + 메뉴 흐름 제어)         │
│        user_view.py (일반 회원)  /  admin_view.py (관리자)  │
└────────────────────────────┬─────────────────────────────┘
                             ▼
┌──────────────────────────────────────────────────────────┐
│          services/  (비즈니스 로직 — 결과 값만 반환)          │
│  회원 / 대출·반납 / 검색 / 추천 / 마이페이지 / 통계 / 관리자  │
└──────────────┬──────────────────────────────┬────────────┘
               ▼                              ▼
┌──────────────────────────────┐  ┌───────────────────────────┐
│   models/  (데이터 클래스)    │  │   utils/  (공통 도구)       │
│ Member / Book / Loan / Record │  │ JSON 저장 / 그래프 / API    │
└──────────────┬───────────────┘  └─────────────┬─────────────┘
               ▼                                ▼
┌──────────────────────────────┐  ┌───────────────────────────┐
│   data/*.json (파일 저장소)   │  │ OpenAI API / 국립중앙도서관  │
└──────────────────────────────┘  └───────────────────────────┘
```

- **View**: 콘솔 환경 특성상 입력·출력과 메뉴 흐름 제어(Controller 역할)를 함께 담당
- **Service**: 입력·출력 없이 값만 반환하도록 분리해 추천·대출 같은 핵심 로직을 화면과 독립적으로 재사용
- **Model**: `to_dict()` / `from_dict()`로 JSON과 객체를 상호 변환

---

## 프로젝트 구조

```
PyBook/
├── main.py                       # 프로그램 시작, 메인 메뉴
├── requirements.txt              # 필요한 라이브러리 목록
├── .env.example                  # 환경 변수 예시 (.env는 git에 올리지 않음)
├── function.md                   # 파일별 함수 기능 정리 문서
│
├── views/                        # 화면 출력 + 입력 + 메뉴 흐름
│   ├── user_view.py              # 일반 회원 메뉴, 마이페이지, 도서 추천 화면
│   └── admin_view.py             # 관리자 회원/도서/리뷰 관리 화면
│
├── services/                     # 비즈니스 로직
│   ├── member_service.py         # 회원가입, 로그인, 정보 수정, 탈퇴, 비밀번호 찾기
│   ├── admin_member_service.py   # 관리자 회원 조회/등록/수정/삭제, 휴면 회원
│   ├── admin_book_service.py     # 관리자 도서 등록/수정/삭제, 리뷰 관리
│   ├── loan_service.py           # 대출/반납, 등급 계산, 포인트, AI 퀴즈
│   ├── my_loan_service.py        # 독서 연대기, 대출 현황
│   ├── recommend_service.py      # TF-IDF + 코사인 유사도 맞춤 도서 추천
│   ├── search_service.py         # 도서 검색, 결과 내 재검색, 정렬
│   ├── analytics_service.py      # 명예의 전당 (다독왕 랭킹)
│   ├── ai_service.py             # AI 사서 챗봇
│   └── book_service.py           # 국립중앙도서관 API 도서 수집
│
├── models/                       # 데이터 클래스
│   ├── member.py                 # Member (회원)
│   ├── book.py                   # Book (도서)
│   ├── loan.py                   # Loan (대출)
│   └── record.py                 # Record (평점, 감상평)
│
├── utils/                        # 공통 도구
│   ├── file_handler.py           # JSON 읽기/쓰기 
│   ├── visualizer.py             # Matplotlib 독서 그래프
│   ├── openai_client.py          # OpenAI API (퀴즈 생성, 챗봇 응답)
│   └── book_api_client.py        # 국립중앙도서관 Open API 클라이언트
│
├── animations/
│   └── animation_effect.py       # 시작/종료 화면, 타이핑 효과, 로딩 스피너
│
└── data/                         # JSON 파일 저장소 (git에 올리지 않음)
    ├── members.json
    ├── books.json
    ├── loans.json
    └── records.json
```

> 파일별 함수 설명은 [function.md](function.md)를 참고하세요.

---

## 시작하기

### 사전 요구사항
- **Python 3.12 이상**
  - 코드에 `int | None`, `list[dict]` 같은 타입 힌트가 사용되어 Python 3.10 미만에서는 실행되지 않습니다.
- OpenAI API 키 (AI 퀴즈, 챗봇 사용 시)
- 국립중앙도서관 Open API 키 (도서 정보 수집 시)

### 1️⃣ 설치

```bash
git clone https://github.com/PyBook-team4/PyBook.git
cd PyBook

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2️⃣ 환경 변수 설정
`.env.example`을 복사해 `.env` 파일을 만들고 값을 채웁니다.

```bash
cp .env.example .env
```

```ini
# 국립중앙도서관 Open API 키
API_KEY=
# 관리자 로그인 비밀번호
PASSWORD=
# OpenAI API 키 (AI 퀴즈, 챗봇)
OPENAI_API_KEY=
# Gemini API 키 (예정)
GEMINI_API_KEY=
```

### 3️⃣ 데이터 준비
`data/*.json` 파일은 git에 올라가지 않습니다. 팀에서 공유한 데이터 파일을 `data/` 폴더에 넣어주세요. 파일이 없으면 빈 상태로 시작합니다.

### 4️⃣ 실행

```bash
python3 main.py
```

> 모든 기능은 **터미널**에서 실행하는 것을 권장합니다. (PyCharm Run 창 등에서는 화면 지우기가 동작하지 않을 수 있습니다.)

---


---

## 주요 구현 사항

### 1. 코사인 유사도 기반 맞춤 도서 추천
- 도서마다 `장르 + 키워드 + 제목 + 저자`를 텍스트로 만들어 **TF-IDF 벡터**로 변환
- 한국어는 조사가 붙어 단어가 달라지므로(`문명의`, `문명을`) **글자 2~3개 단위(char n-gram)**로 잘라 형태소 분석기 없이 비교
- 관심분야 + 읽은 책(평점 가중치) + 감상평으로 **회원 취향 벡터**를 만들고, 평점 2점 이하인 책과 그 감상평은 취향에서 제외

```python
vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 3))
book_matrix = vectorizer.fit_transform([_book_text(b) for b in books])

# 취향 벡터 = 관심분야, 읽은 책, 감상평 벡터의 가중 평균
profile = sum(vector * weight for _, _, vector, weight in sources) / total_weight
scores = cosine_similarity(profile, book_matrix)[0]
```

### 2. 계층 분리 (View – Service – Model)
- Service는 `input()` / `print()` 없이 값만 반환하고, 화면 출력은 View가 담당
- 등급 계산(`get_tier_info_by_point`)처럼 여러 곳에서 쓰는 로직은 **한 곳에만 정의**하고 import해서 사용

### 3. JSON 파일 저장소 안정성
- 저장 시 **임시 파일에 먼저 쓴 뒤 원본과 교체**해, 저장 도중 오류가 나도 원본이 보존됨
- 파일이 손상되었으면 빈 데이터로 덮어쓰지 않고 **프로그램을 중단**해 데이터 손실 방지

```python
def save_json(filename, data_list):
    temp_filename = filename + ".tmp"
    with open(temp_filename, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    os.replace(temp_filename, filename)   # 한 번에 교체
```

### 4. AI 도서 퀴즈와 사서 챗봇
- 퀴즈 응답을 `[문제]` / `[정답]` / `[해설]` 형식으로 받아 파싱 후 채점
- API 키가 없거나 통신 오류가 나도 **반납 처리는 정상 진행**되도록 퀴즈만 건너뜀
- 챗봇은 시스템 프롬프트를 고정하고 최근 대화 10개만 유지(슬라이딩 윈도우)

### 5. 선택 라이브러리의 지연 import
- matplotlib, scikit-learn, openai는 **기능을 실행할 때만 import**
- 라이브러리가 없는 PC에서도 프로그램 전체는 실행되고, 해당 기능에서만 설치 안내 표시

---

## 트러블슈팅

### 1. JSON 파일 손상 시 전체 데이터 유실 위험
**문제**: 파일을 읽지 못하면 빈 리스트를 반환해, 그 상태로 저장하면 기존 회원 데이터 전체가 덮어써짐

**해결**: 손상된 파일은 읽기 단계에서 프로그램을 중단하고, 저장은 임시 파일 교체 방식으로 변경

### 2. 반납 기한과 실제 반납일이 한 필드에 섞임
**문제**: `return_date` 하나에 대출 시에는 반납 기한, 반납 시에는 실제 반납일을 덮어써 연체 이력을 알 수 없음

**해결**: `due_date`(반납 기한)와 `return_date`(실제 반납일)로 분리하고, 기존 데이터는 `due_date`가 없으면 `return_date`를 기한으로 읽도록 호환 처리

### 3. 파일마다 다른 등급 기준
**문제**: 등급 계산 함수가 3개 파일에 복사되어, 한 곳만 SILVER 기준이 100점으로 달라 화면마다 등급이 다르게 표시됨

**해결**: 등급 계산 함수를 `loan_service`에 하나만 두고 나머지 파일은 import해서 사용

### 4. 세션 정보가 갱신되지 않음
**문제**: 로그인 시점의 회원 정보를 계속 사용해, 반납으로 포인트가 바뀌거나 비밀번호를 변경해도 반영되지 않음

**해결**: 메뉴를 그릴 때마다 `user_id`로 최신 회원 정보를 다시 불러오도록 변경

### 5. Matplotlib 한글 깨짐
**문제**: 기본 폰트에 한글이 없어 그래프의 한글이 □로 표시됨

**해결**: 운영체제를 확인해 Mac은 `AppleGothic`, Windows는 `Malgun Gothic`을 자동 설정하고 마이너스 기호 깨짐도 함께 처리

---

## 👥 팀원 소개

| 이름 | 역할 | 담당 업무 |
|------|------|-----------|
| 이다민 | **팀장** | 회원 관리(암호화 인증/세션), 등급 및 포인트 시스템, 관리자 휴면 회원 관리 | 
| 노다연 | 기획 / PM | 총괄 기획, 요구사항 정의서·WBS 작성, Git/GitHub 형상 관리 |
| 김지훈 | 코어 개발 | 도서 대출/반납 트랜잭션, 재고/기한 검증, 외부 Open API 연동 |
| 이혜원 | 검색 / 시각화 | 통합 검색과 정렬, 마이페이지 독서 연대기 및 Matplotlib 시각화 |
| 한수빈 | AI 모듈 | OpenAI API 사서 챗봇(페르소나 가드레일, 슬라이딩 윈도우) 구현 |

---

<div align="center">

**4조 미니 프로젝트**

Made with 📚 by PyBook Team

</div>
