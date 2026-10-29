# main.py
import time
from services import member_service
from animations.animation_effect import show_intro_animation, show_goodbye_animation, clear_screen
from views.user_view import run_logged_in_menu
from views.admin_view import run_admin_menu

#TODO 모든 비밀번호에 파이썬 기본 모듈인 getpass의 getpass()를 써서 입력한 비밀번호가 콘솔창에 노출되지 않도록 할까?
def main():
    # 오프닝 애니메이션 실행
    show_intro_animation()
    
    
    while True:
        clear_screen()
        print("====================================")
        print("        PyBook Main Menu        ")
        print("====================================")
        print("1. 회원가입")
        print("2. 로그인")
        print("3. 관리자 로그인")
        print("4. 프로그램 종료")
        print("====================================")
        
        choice = input("원하시는 메뉴 번호를 입력하세요: ").strip()

        # 1. 회원가입
        if choice == '1':
            clear_screen()
            print("====================================")
            print("            회원가입 화면           ")
            print("====================================")
            member_service.signup()
            time.sleep(2)

        # 2. 로그인
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
                
                if login_choice == '1':
                    clear_screen()
                    print("====================================")
                    print("            일반 로그인             ")
                    print("====================================")
                    email = input("아이디 (이메일): ").strip()
                    pw = input("비밀번호: ").strip()
                    
                    success,user_data=member_service.login(email=email,pw=pw)
                    time.sleep(1.5)

                    if success:
                        run_logged_in_menu(user_data)
                    break

                elif login_choice == '2':
                    clear_screen()
                    member_service.find_pw()
                    print("\n잠시 후 로그인 화면으로 돌아갑니다...")
                    time.sleep(2)

                elif login_choice == '3':
                    print("\n메인 메뉴로 돌아갑니다.")
                    time.sleep(1)
                    break
                else:
                    print("\n[오류] 올바른 메뉴 번호를 입력해주세요.\n")
                    time.sleep(1.5)
        
        # 3. 관리자 로그인
        elif choice == '3':
            clear_screen()
            print("====================================")
            print("           관리자 로그인            ")
            print("====================================")
            pw = input("관리자 비밀번호를 입력하세요: ")
            
            success, message = member_service.admin_login(pw=pw)
            print(f"\n{message}")
            time.sleep(1.5)
            
            if success:
                run_admin_menu()

        # 4. 프로그램 종료
        elif choice == '4':
            show_goodbye_animation()
            break
        
        else:
            print("\n[오류] 올바른 메뉴 번호를 입력해주세요.\n")
            time.sleep(1)

if __name__ == "__main__":
    main()
