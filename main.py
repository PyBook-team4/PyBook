# main.py
import time
#from services.book_service import initialize_books_if_empty
from services import member_service,search_service,loan_service
from services.ai_service import AIChatService
from services.admin_member_service import (
    get_all_members,
    sort_members,
    search_members,
    admin_register_member,
    admin_update_member,
    admin_delete_member,
    get_dormant_members
)
from services.admin_book_service import (
    register_book,
    book_update,
    book_delete
)
from animations.animation_effect import (
    show_intro_animation, 
    show_goodbye_animation, 
    clear_screen,
    connecting_ai_animation,
    typing_effect
)
from utils.file_handler import load_json
#가장 아래 부분에 main을 제외한 함수들은 네비게이션 로직입니다. 
#추후 navigation 관련 함수들은 views/ 폴더 생성 후 옮겨둘수도 있습니다.

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
            _handle_member_management()
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
import time
from services.admin_member_service import (
    get_all_members,
    sort_members,
    search_members,
    admin_register_member,
    admin_update_member,
    admin_delete_member,
    get_dormant_members
)
from animations.animation_effect import clear_screen

def run_admin_menu():
    """관리자 로그인 성공 후 진입하는 전용 메뉴"""
    
    while True:
        clear_screen()
        print("====================================")
        print("         PyBook Admin Menu        ")
        print("====================================")
        print("1. 회원 관리")
        print("2. 도서 관리")
        print("3. 로그아웃 (메인으로 돌아가기)")
        print("====================================")
        
        admin_choice = input("관리자 메뉴를 선택하세요: ").strip()
        
        if admin_choice == '1':
            _handle_member_management()
        elif admin_choice == '2':
            _handle_book_management()
            
        elif admin_choice == '3':
            print("\n관리자 계정을 로그아웃합니다.")
            time.sleep(1)
            break
        else:
            print("\n잘못된 입력입니다. 다시 선택해주세요.\n")
            time.sleep(1)

#관리자 회원 관리
def _handle_member_management():
    """회원 관리 상세 서브 메뉴"""
    while True:
        clear_screen()
        print("====================================")
        print("        [회원 관리 및 조회]         ")
        print("====================================")
        print("1. 전체 회원 목록 조회 (정렬)")
        print("2. 회원 검색 (이름/이메일/전화번호)")
        print("3. 관리자 회원 등록")
        print("4. 회원 정보 수정 (비밀번호 초기화 등)")
        print("5. 회원 강제 삭제")
        print("6. 휴면 회원 조회")
        print("7. 이전 메뉴로 돌아가기")
        print("====================================")
        
        sub_choice = input("원하시는 작업을 선택하세요: ").strip()
        
        if sub_choice == '1':
            clear_screen()
            print("--- [전체 회원 목록] ---")
            print("정렬 기준 선택 -> 1: 고유번호(ID), 2: 이름, 3: 포인트, 4: 가입일")
            sort_opt = input("정렬 기준 번호 입력 (기본 1): ").strip()
            
            sort_map = {'1': 'user_id', '2': 'name', '3': 'point', '4': 'created_at'}
            sort_by = sort_map.get(sort_opt, 'user_id')
            
            rev_input = input("내림차순 정렬을 원하시나요? (y/n, 기본 n): ").strip().lower()
            reverse = True if rev_input == 'y' else False
            
            members = get_all_members()
            sorted_members = sort_members(members, sort_by=sort_by, reverse=reverse)
            
            if not sorted_members:
                print("\n등록된 회원이 없습니다.")
            else:
                for m in sorted_members:
                    print(f"ID: {m.get('user_id')} | 이름: {m.get('name')} | 이메일: {m.get('email')} | "
                          f"연락처: {m.get('phone')} | 포인트: {m.get('point')} | 티어: {m.get('tier')} | 가입일: {m.get('created_at')}")
            input("\n계속하려면 엔터 키를 누르세요...")

        elif sub_choice == '2':
            clear_screen()
            print("--- [회원 검색] ---")
            keyword = input("검색할 키워드(이름, 이메일, 전화번호)를 입력하세요: ")
            results = search_members(keyword)
            
            print(f"\n검색 결과: 총 {len(results)}건")
            for m in results:
                print(f"ID: {m.get('user_id')} | 이름: {m.get('name')} | 이메일: {m.get('email')} | 연락처: {m.get('phone')}")
            input("\n계속하려면 엔터 키를 누르세요...")

        elif sub_choice == '3':
            clear_screen()
            print("--- [관리자 신규 회원 등록] ---")
            email = input("이메일 입력: ").strip()
            name = input("이름 입력: ").strip()
            phone = input("연락처 입력 (숫자 11자리): ").strip()
            
            success, msg = admin_register_member(email=email, name=name, phone=phone)
            print(f"\n{msg}")
            time.sleep(2)

        elif sub_choice == '4':
            clear_screen()
            print("--- [회원 정보 수정] ---")
            try:
                user_id = int(input("수정할 회원의 고유번호(ID) 입력: ").strip())
            except ValueError:
                print("\n올바른 숫자를 입력해주세요.")
                time.sleep(1.5)
                continue
                
            new_email = input("새 이메일 입력 (변경하지 않으려면 엔터): ").strip() or None
            reset_pw = input("비밀번호를 휴대폰 뒷 4자리로 초기화하시겠습니까? (y/n): ").strip().lower() == 'y'
            
            success, msg = admin_update_member(
                user_id=user_id,
                new_email=new_email,
                reset_pw_to_phone_last4=reset_pw
            )
            print(f"\n{msg}")
            time.sleep(2)

        elif sub_choice == '5':
            clear_screen()
            print("--- [회원 강제 삭제] ---")
            try:
                user_id = int(input("삭제할 회원의 고유번호(ID) 입력: ").strip())
            except ValueError:
                print("\n올바른 숫자를 입력해주세요.")
                time.sleep(1.5)
                continue
                
            confirm = input(f"정말 회원(ID: {user_id})을 삭제하시겠습니까? (y/n): ").strip().lower()
            if confirm == 'y':
                success, msg = admin_delete_member(user_id)
                print(f"\n{msg}")
            else:
                print("\n삭제가 취소되었습니다.")
            time.sleep(2)

        elif sub_choice == '6':
            clear_screen()
            print("--- [휴면 회원 조회 (90일 이상 미접속)] ---")
            dormants = get_dormant_members(days=90)
            if not dormants:
                print("\n현재 휴면 상태인 회원이 없습니다.")
            else:
                print(f"\n휴면 회원 총 {len(dormants)}명 발견:")
                for m in dormants:
                    print(f"ID: {m.get('user_id')} | 이름: {m.get('name')} | "
                          f"마지막 로그인: {m.get('last_login')} | 사유: {m.get('dormant_reason')}")
            input("\n계속하려면 엔터 키를 누르세요...")

        elif sub_choice == '7':
            break
        else:
            print("\n잘못된 입력입니다.\n")
            time.sleep(1)

#관리자 도서 관리
def _handle_book_management():
    """도서 관리 상세 서브 메뉴"""
    while True:
        clear_screen()
        print("====================================")
        print("        [도서 관리 및 재고 갱신]        ")
        print("====================================")
        print("1. 전체 도서 목록 조회")
        print("2. 신규 도서 등록")
        print("3. 도서 정보 수정")
        print("4. 도서 삭제")
        print("5. 이전 메뉴로 돌아가기")
        print("====================================")

        sub_choice = input("원하시는 작업을 선택하세요: ").strip()
        
        if sub_choice == '1':
            clear_screen()
            print("--- [전체 도서 목록] ---")
            books = load_json("data/books.json")
            if not books:
                print("\n등록된 도서가 없습니다.")
            else:
                for b in books:
                    print(f"ID: {b.get('id')} | 제목: {b.get('title')} | 저자: {b.get('author')} | "
                          f"출판사: {b.get('publisher')} | 장르: {b.get('genre')} | ISBN: {b.get('isbn')} | "
                          f"평점: {b.get('rating')} | 재고: {b.get('available_stock')}/{b.get('total_stock')} | 등록일: {b.get('reg_date')}")
            input("\n계속하려면 엔터 키를 누르세요...")

        elif sub_choice == '2':
            clear_screen()
            print("--- [신규 도서 등록] ---")
            title = input("도서 제목 입력: ").strip()
            author = input("저자 입력: ").strip()
            publisher = input("출판사 입력: ").strip()
            genre = input("장르 입력: ").strip()
            isbn = input("ISBN 입력: ").strip()
            
            try:
                total_stock = int(input("최대 보유량 입력 (1~10): ").strip())
                available_stock = int(input("현재 대여 가능 재고 입력: ").strip())
            except ValueError:
                print("\n숫자만 입력해야 합니다.")
                time.sleep(1.5)
                continue
            
            success = register_book(title, author, publisher, genre, isbn, total_stock, available_stock)
            time.sleep(1.5)

        elif sub_choice == '3':
            clear_screen()
            print("--- [도서 정보 수정] ---")
            try:
                book_id = int(input("수정할 도서의 고유 ID 입력: ").strip())
            except ValueError:
                print("\n올바른 숫자를 입력해주세요.")
                time.sleep(1.5)
                continue
            
            print("\n[수정 항목 선택]")
            print("1: 제목, 2: 저자, 3: 출판사, 4: ISBN, 5: 장르, 6: 평점, 7: 최대 재고량, 8: 대여 가능 재고")
            try:
                field_choice = int(input("수정할 항목 번호 입력 (1-8): ").strip())
            except ValueError:
                print("\n올바른 숫자를 입력해주세요.")
                time.sleep(1.5)
                continue
            
            new_value = input("변경할 값을 입력하세요: ")
            book_update(book_id, field_choice, new_value)
            time.sleep(2)

        elif sub_choice == '4':
            clear_screen()
            print("--- [도서 삭제] ---")
            try:
                book_id = int(input("삭제할 도서의 고유 ID 입력: ").strip())
            except ValueError:
                print("\n올바른 숫자를 입력해주세요.")
                time.sleep(1.5)
                continue
            
            confirm = input(f"정말 도서(ID: {book_id})를 삭제하시겠습니까? (y/n): ").strip().lower()
            if confirm == 'y':
                book_delete(book_id)
            else:
                print("\n삭제가 취소되었습니다.")
            time.sleep(2)
        elif sub_choice == '5':
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