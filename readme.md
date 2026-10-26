PyBook/
├── .env                          # 환경 변수 설정 (openai api 키,국립중앙박물관 api키, 관리자 암호키 등 )
├── .gitignore                    # 제외 설정   ( .env, data/*.json, __pycache__, venv/ 등)
├── requirements.txt              # 필수 라이브러리 목록(requests, python-dotenv, matplotlib, scikit-learn 등)
├── main.py                       # 애플리케이션 진입점
│
├── animations/                   # 콘솔 UI 애니메이션 및 시각 효과 모듈
│   ├── __init__.py
│   └── effect.py                 # 타이핑 효과, 로딩 바, 오프닝 연출 등
│
├── data/                         # JSON 기반 영구 저장소 (데이터 베이스 역할)
│   ├── members.json              # 회원 정보 (ID, PW, 이름, 포인트, 등급, 마지막 로그인일 등)
│   ├── books.json                # 도서 서지 정보 (ID, 제목, 저자, 장르, 평점, 재고 상태 등)
│   ├── loans.json                # 대출/반납 이력 (대출 ID, 회원 ID, 도서 ID, 대출일, 반납예정일, 상태)
│   └── records.json              # 독서 기록 및 감상평 (별점, 감성 분석 결과, 리뷰 텍스트 등)
│
├── models/                       # 도메인 데이터 객체 모델 (OOP 클래스 정의)
│   ├── __init__.py
│   ├── member.py                 # Member 클래스 (회원 속성 및 등급/포인트 메서드)
│   ├── book.py                   # Book 클래스 (도서 서지 정보 객체)
│   ├── loan.py                   # Loan 클래스 (대출 거래 내역 객체)
│   └── record.py                 # Record 클래스 (독서 노트 및 평점 객체)
│
├── services/                     # 비즈니스 로직 및 핵심 기능 모듈 (CRUD & 서비스)
│   ├── __init__.py
│   ├── member_service.py         # 회원가입, 로그인, 정보수정, 탈퇴, 관리자 휴면 회원 조회
│   ├── book_service.py           # 수동 도서 등록, 국립중앙도서관 API 연동, 베스트셀러/오늘의 추천 관리
│   ├── loan_service.py           # 도서 대출/반납, 등급별 대출 제한/기한 체크, 포인트 적립, 다독왕 선정
│   ├── search_service.py         # 관심분야 1차/2차 키워드 필터링, 정렬(이름/저자/연도/평점)
│   ├── ai_service.py             # AI 퀴즈 생성, AI 챗봇 인터페이스, 코사인 유사도 기반 AI 도서 추천
│   └── analytics_service.py      # 나만의 독서 연대기 집계, 목표치 설정 및 달성률 계산
│
└── utils/                        # 공통 유틸리티 및 외부 연동 도구
    ├── __init__.py
    ├── file_handler.py           # JSON 파일 읽기/쓰기 및 영속성 관리 공통 유틸리티
    ├── book_api_client.py             # Google Books API 호출 클라이언트
    ├── openai_client.py          # OpenAI API (GPT) 전용 통신 클라이언트 
    ├── gemini_client.py          # Gemini API 전용 클라이언트
    └── visualizer.py             # Matplotlib 기반 장르별 독서 비율 파이/바 차트 시각화 유틸리티
