[ 0. 메인 메뉴 ] (MAIN)
 ├── 1. 회원 관리 ───────────────────────────────► [ 1. 회원 관리 메뉴 ] (MEMBER)
 │                                                    ├── 1-1. 로그인 (LOGIN)
 │                                                    ├── 1-2. 회원 정보 및 상태 조회 (MEMBER_INFO)
 │                                                    │     ├── 1-2-1. 대출 기록 확인 (LOAN_HISTORY)
 │                                                    │     └── 1-2-2. 평점 및 감상평 조회 (REVIEW_HISTORY)
 │                                                    ├── 1-3. 회원 가입 (SIGNUP)
 │                                                    ├── 1-4. 회원 정보 수정 및 탈퇴 (MEMBER_EDIT)
 │                                                    ├── 1-5. 로그인 정보 찾기 (FIND_ACC)
 │                                                    └── 1-6. 로그아웃
 │
 ├── 2. 도서 및 대출 관리 ───────────────────────► [ 2. 도서 및 대출 메뉴 ] (BOOK_LENDING)
 │                                                    ├── 2-1. 도서 검색 및 정렬 (BOOK_SEARCH)
 │                                                    │     └── 2-1-1. 검색 결과 및 정렬/재검색 (BOOK_SEARCH_RESULT)
 │                                                    ├── 2-2. 도서 대출 (등급별 권수/기한 제한 체크) (BOOK_LOAN)
 │                                                    ├── 2-3. 도서 반납 및 감상평/평점 기록 (포인트 적립) (BOOK_RETURN)
 │                                                    ├── 2-4. 베스트셀러 및 오늘의 추천 도서 (BOOK_BEST)
 │                                                    └── 2-5. 다독왕 명예의 전당 조회 (BOOK_KING)
 │
 ├── 3. 독서 기록, 통계 및 AI 서비스 ────────────► [ 3. 통계 및 AI 서비스 메뉴 ] (ANALYTICS_AI)
 │                                                    ├── 3-1. 나만의 독서 연대기 조회 (TIMELINE)
 │                                                    ├── 3-2. 독서 목표치 설정 및 달성률 (GOAL)
 │                                                    ├── 3-3. 장르별 독서 비율 시각화 [matplotlib] (CHART)
 │                                                    ├── 3-4. AI 도서 추천 (감성분석 & 코사인 유사도) (AI_REC)
 │                                                    ├── 3-5. AI 독서 퀴즈 (책 내용 기반 퀴즈 풀기) (AI_QUIZ)
 │                                                    ├── 3-6. AI 챗봇 (도서 내용 및 Q&A 대화) (AI_CHAT)
 │                                                    └── 3-7. 독서 기록 관리 (리뷰 수정/삭제) (BOOK_RECORD)
 │
 └── admin. 관리자 메뉴 진입 (ADMIN) ────────────► [ admin. 관리자 메뉴 ] (ADMIN)
                                                      ├── admin-1. 회원 관리 (휴면 회원 찾기 포함) (ADMIN_MEMBER)
                                                      │     ├── admin-1-1. 전체 회원 목록 조회 및 정렬 (ADMIN_MEMBER_LIST)
                                                      │     └── admin-1-2. 회원 추가 및 강제 삭제 (ADMIN_MEMBER_CRUD)
                                                      └── admin-2. 도서 관리 (ADMIN_BOOK)
                                                            └── admin-2-1. 도서 목록 조회 및 CRUD (ADMIN_BOOK_LIST)

※ [전역 명령어 (어디서든 즉시 작동)]
   - h : 메인 메뉴(MAIN)로 이동
   - b : 이전 메뉴(Parent Menu)로 이동
   - e : 프로그램 종료 및 데이터(JSON) 자동 저장