# main.py
import time
#from services.book_service import initialize_books_if_empty
from services import member_service,search_service,loan_service
from services.ai_service import AIChatService
from animations.animation_effect import (
    show_intro_animation, 
    show_goodbye_animation, 
    clear_screen,
    connecting_ai_animation,
    typing_effect
)

#가장 아래 부분에 main을 제외한 함수들은 네비게이션 로직입니다. 
#추후 navigation 관련 함수들은 views/ 또는 cotrollers/ 폴더 생성 후 옮겨둘수도 있습니다.

"""로그인 성공 후 진입하는 서브 메뉴"""
def run_logged_in_menu(current_user):
    
    while True:
        clear_screen()
        print(f"====================================")
        print(f"   [환영합니다, {current_user['name']} 님!]")
        print(f"   보유 포인트: {current_user['point']}P ") #TODO 등급: {current_user['tier']} 따로 함수 하나 더 짜서 포인트별 등급 매기기
        print("====================================")
        print("1. 도서 검색 및 대출하기")
        print("2. 도서 반납하기")


   
        print("4. 명예의 전당")  #이름을 아직 못정함 이 부분들어가면 명예의전당(다독왕),도서 추천(베스트셀러)등 넣는게나을수도?
        print("5. PyBook chat bot")
        print("7. 마이페이지")   #마이페이지안에  나의 대출 이력 조회(나의 독서 연대기)등을 넣는게 나을수도..?



        print("8. 회원 정보 수정")
        print("9. 로그아웃")
        print("0. 회원탈퇴")
        print("====================================")
     
        
        sub_choice = input("메뉴를 선택하세요: ")
        # 1. 도서 검색 및 대출하기
        if sub_choice == '1':
            clear_screen()
            print("====================================")
            print("            도서 검색               ")
            print("====================================")
            keyword = input("검색할 도서 제목, 저자, 장르를 입력하세요: ").strip()
            
            results, message = search_service.search_books(keyword)
            print(f"\n{message}")
            time.sleep(1.5)
            
            if not results:
                continue
                
            current_results = results
            ##도서 검색 결과 반환 및 다음 action을 위한 창
            while True:
                clear_screen()
                print("====================================")
                print(f"          검색 결과 (총 {len(current_results)}건)        ")
                print("====================================")
                
                for idx, book in enumerate(current_results, start=1):
                    title = book.get('title', '제목 없음')
                    author = book.get('author', '저자 미상')
                    genre = book.get('genre', '기타')
                    stock = book.get('available_stock', 0)
                    rating = book.get('rating', 0.0)
                    print(f"{idx}. [{genre}] '{title}' - {author} (평점: {rating} | 남은 재고: {stock}개)")
                
                print("====================================")
                print("1. 결과 내 재검색 (2차 검색)")
                print("2. 결과 정렬하기")
                print("3. 도서 대출하기 (번호 선택)")
                print("0. 이전 메뉴로 돌아가기")
                print("====================================")
                
                action_choice = input("원하시는 작업을 선택하세요: ").strip()
                
                if action_choice == '1':
                    scnd_kw = input("결과 내에서 다시 검색할 키워드를 입력하세요: ").strip()
                    current_results, msg = search_service.scnd_search_books(current_results, scnd_kw)
                    print(f"\n{msg}")
                    time.sleep(1.5)
                
                elif action_choice == '2':
                    print("\n[ 정렬 기준 선택 ]")
                    print("1. 제목순 (title)")
                    print("2. 평점순 (rating)")
                    print("3. 저자순 (author)")
                    print("4. 재고순 (available_stock)")


                    sort_idx = input("정렬 기준 번호 입력: ").strip()

                    #sort_map 딕셔너리 형태로 번호와 정렬의 기준들을 저장한 후 serach_service.sort_books에 넘깁니다.
                    sort_map = {'1': 'title', '2': 'rating', '3': 'author', '4': 'available_stock'}
                    sort_by = sort_map.get(sort_idx, 'title')
                    
                    rev_input = input("내림차순으로 정렬하시겠습니까? (y/n): ").strip().lower()
                    is_reverse = (rev_input == 'y')
                    
                    current_results = search_service.sort_books(current_results, sort_by=sort_by, reverse=is_reverse)
                    print("\n 정렬이 완료되었습니다!")
                    time.sleep(1)
                
                # 3. 도서 대출하기 연동 부분
                elif action_choice == '3':
                    try:
                        book_num = int(input("대출할 도서 번호를 입력하세요: ").strip())
                        if 1 <= book_num <= len(current_results):
                            selected_book = current_results[book_num - 1]
                            book_id = selected_book.get("id")
                            
                            # loan_service의 borrow 함수 호출 (로그인한 유저의 user_id와 책 id 전달)
                            success = loan_service.borrow(user_id=current_user['user_id'], book_id=book_id)
                            
                            time.sleep(2)
                        else:
                            print("\n[오류] 목록에 있는 번호를 입력해주세요.")
                            time.sleep(1.5)
                    except ValueError:
                        print("\n[오류] 숫자만 입력 가능합니다.")
                        time.sleep(1.5)
                
                elif action_choice == '0':
                    break
                else:
                    print("\n[오류] 올바른 번호를 입력해주세요.")
                    time.sleep(1)

        # 2. 도서 반납하기 연동 부분
        elif sub_choice == '2':
            clear_screen()
            print("====================================")
            print("            도서 반납하기           ")
            print("====================================")
            
            # 현재 로그인한 유저가 대출 중인 목록 가져오기
            active_loans = loan_service.get_user_active_loans(current_user['user_id'])
            
            if not active_loans:
                print("\n현재 대출 중인 도서가 없습니다.")
                time.sleep(2)
                continue
                
            print("대출 중인 도서 목록:")
            for idx, loan in enumerate(active_loans, start=1):
                print(f"{idx}. 도서명: '{loan['book_title']}' (대출일: {loan['loan_date']} ~ 반납기한: {loan['return_date']})")
            
            print("====================================")
            return_idx = input("반납할 도서의 번호를 입력하세요 (취소는 엔터): ").strip()
            
            if return_idx.isdigit():
                idx_num = int(return_idx)
                if 1 <= idx_num <= len(active_loans):
                    target_loan = active_loans[idx_num - 1]
                    loan_id = target_loan["loan_id"]
                    
                    # 🔑 loan_service의 return_book 함수 호출 (리뷰/평점 입력 및 포인트 정산 진행)
                    loan_service.return_book(loan_id)
                    
                    # 반납 후 포인트가 변동되었을 수 있으므로 최신 정보 반영 (필요시 current_user['point'] 갱신)
                    time.sleep(2)
                else:
                    print("\n[오류] 올바른 번호를 입력해주세요.")
                    time.sleep(1.5)
        elif sub_choice == '5':
            # 1. 챗봇 진입 애니메이션 실행
            connecting_ai_animation()
            
            # 2. 챗봇 서비스 객체 생성 및 채팅 루프 시작
            chat_service = AIChatService()
            chat_service.start_chat()
            
            # 3. 챗봇 종료(exit) 후 빠져나왔을 때 자연스러운 전환
            typing_effect("메인 메뉴로 돌아갑니다...", speed=0.03)
            time.sleep(1)
        elif sub_choice=='8':
            member_service.update(current_user['email'])
            
        elif sub_choice == '9':
            if member_service.logout:
                print("\n 로그아웃합니다.")
                time.sleep(1)
                break   # 이 루프를 탈출하면 main으로 돌아가며 세션(current_user) 소멸
                
        #회원탈퇴
        elif sub_choice == '0':
            if member_service.withdraw(current_user["email"],current_user["pw"]):
                break
            else:
                continue

        


"""관리자 로그인 성공 후 진입하는 전용 메뉴"""
def run_admin_menu():
    
    while True:
        clear_screen()
        print("====================================")
        print("         PyBook Admin Menu        ")
        print("====================================")
        print("1. 전체 회원 목록 조회")
        print("2. 도서 재고 강제 일괄 갱신(CRUD)")
        print("3. 로그아웃 (메인으로 돌아가기)")
        print("====================================")
        
        admin_choice = input("관리자 메뉴를 선택하세요: ")
        
        if admin_choice == '1':
            print("\n전체 회원 조회 기능 연동 예정...\n")
            time.sleep(1.5)
        elif admin_choice == '2':
            print("\n도서 재고 갱신 기능 연동 예정...\n")
            time.sleep(1.5)
        elif admin_choice == '3':
            print("\n 관리자 계정을 로그아웃합니다.")
            time.sleep(1)
            break
        else:
            print("\n잘못된 입력입니다.\n")
            time.sleep(1)

def main():
    # 1. 프로그램 실행 시 최초 1회 도서 100권 자동 적재 체크
    #initialize_books_if_empty()
    
    # 2. 오프닝 애니메이션 실행
    show_intro_animation()
    
    while True:
        print("====================================")
        print("        PyBook Main Menu        ")
        print("====================================")
        print("1. 회원가입")
        print("2. 로그인")
        print("3. 관리자 로그인")
        print("4. 프로그램 종료")
        print("====================================")
        
        choice = input("원하시는 메뉴 번호를 입력하세요: ")


        #pw_check 하나 더 추가해야됨
        #회원가입 (1) 입력시 
        if choice == '1':
            clear_screen()
            print("====================================")
            print("            회원가입 화면           ")
            print("====================================")
            
            
            # 회원가입 서비스 호출
            success = member_service.signup()
            
            #print(f"\n{message}")
            time.sleep(2)
            clear_screen()
            
        #로그인 (2) 입력시 
        elif choice == '2':
            while True:
                clear_screen()
                print("====================================")
                print("            로그인 화면             ")
                print("====================================")
                print("1. 로그인 하기")
                print("2. 비밀번호 찾기")
                print("3. 뒤로 가기 (메인 메뉴)")
                print("====================================")
                
                login_choice = input("원하시는 메뉴 번호를 입력하세요: ").strip()
                
                # 1. 일반 로그인 진행
                if login_choice == '1':
                    clear_screen()
                    print("====================================")
                    print("            일반 로그인             ")
                    print("====================================")
                    email = input("아이디 (이메일): ").strip()
                    pw = input("비밀번호: ").strip()
                    
                    # 서비스 레이어 호출 (성공여부, 회원정보 반환)
                    result = member_service.login(email=email, pw=pw)
                    
                    # 팀원 코드가 (success, user_data) 튜플을 반환하므로 안전하게 언패킹
                    if result:
                        success, user_data = result
                    else:
                        success, user_data = False, None
                        
                    time.sleep(1.5)

                    if success:
                        current_user = user_data  # 세션에 회원 정보 딕셔너리 할당
                        clear_screen()
                        run_logged_in_menu(current_user)  # 로그인 후 전용 메뉴 진입
                        current_user = None  # 로그아웃 후 세션 비우기
                    break  # 로그인이 끝나거나 실패하면 메인으로 복귀를 위해 루프 탈출

                # 2. 비밀번호 찾기 진입
                elif login_choice == '2':
                    clear_screen()
                    # 팀원분이 member_service에 만들어둔 find_pw() 호출
                    member_service.find_pw()
                    
                    print("\n잠시 후 로그인 화면으로 돌아갑니다...")
                    time.sleep(2)

                # 3. 뒤로 가기 (메인 메뉴로 복귀)
                elif login_choice == '3':
                    print("\n메인 메뉴로 돌아갑니다.")
                    time.sleep(1)
                    break  # 현재 로그인 화면 루프를 탈출하여 메인 메뉴로 이동

                else:
                    print("\n[오류] 올바른 메뉴 번호를 입력해주세요.\n")
                    time.sleep(1.5)
        
        # 관리자 로그인 3 입력시 
        if choice == '3':
            clear_screen()
            print("====================================")
            print("           관리자 로그인            ")
            print("====================================")
            pw = input("관리자 비밀번호를 입력하세요: ")
            
            success, message = member_service.admin_login(pw=pw)
            
            print(f"\n{message}")
            time.sleep(1.5)
            clear_screen()
            
            if success:
                run_admin_menu()  # 관리자 전용 메뉴 실행


        #프로그램 종료 (4) 입력 시 
        if choice == '4':
            show_goodbye_animation()
            break
        else:
            #print("\n준비 중인 기능입니다...\n")
            time.sleep(1)
            clear_screen()

if __name__ == "__main__":
    main()