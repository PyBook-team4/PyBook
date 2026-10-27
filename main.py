# main.py
import time
#from services.book_service import initialize_books_if_empty
from services import member_service
from animations.animation_effect import (
    show_intro_animation, 
    show_goodbye_animation, 
    clear_screen
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
        
        if sub_choice == '1':
            # current_user['email']이나 id를 활용해 대출 서비스 호출
            want_book=input("찾으시는 도서를 입력해주세요...")
            result, message =loan_service.search(want_book)
            #result 찾은 도서 리스트또는 딕셔너리로 반환(책제목,저자,출판사, 대출가능권수 등 )
            # message want_book 검색결과 입니다 또는 찾으시는 검색 결과가 없습니다.
            title=input('대출할 도서를 입력해주세요...')
            succes=loan_service.borrow(current_user["user_id"], title)

            print("\n도서 검색 및 대출 기능 연동 예정...\n")
            time.sleep(1.5)


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
        '''if choice == '2':
            clear_screen()
            print("====================================")
            print("            로그인 화면             ")
            print("====================================")
            print("1.비밀번호 찾기")
            print("2.뒤로 가기")
            
            
            email = input("아이디 (이메일): ")
            pw = input("비밀번호: ")
            
            #서비스 레이어 호출 (성공여부, 메시지, 회원정보 반환)
            success,user_data = member_service.login(email=email, pw=pw)
    

            
            time.sleep(1.5)


            if success:
                current_user = user_data  # 로그인 성공 시 세션에 회원 정보 할당(아마 멤버.dict를 들고 있으면 될거같음)
                clear_screen()
                run_logged_in_menu(current_user)  # 세션을 가지고 로그인 전용 메뉴로 진입 아직 미구현상태라 에러뜸
                current_user = None  # 로그아웃 후 빠져나오면 세션 비우기
        '''
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