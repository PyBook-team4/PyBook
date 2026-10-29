# views/user_view.py
import time
from services import search_service, loan_service, member_service, analytics_service
from services.ai_service import AIChatService
from animations.animation_effect import clear_screen, connecting_ai_animation, typing_effect

def run_logged_in_menu(current_user):
    """로그인 성공 후 진입하는 서브 메뉴"""
    while True:
        # 반납·회원정보 수정 등으로 바뀐 내용을 반영하기 위해 매번 파일에서 다시 불러옴
        latest_user = member_service.get_member_by_id(current_user["user_id"])
        if latest_user is None:
            print("\n회원 정보를 찾을 수 없어 로그아웃합니다.")
            time.sleep(1.5)
            break
        current_user = latest_user
        clear_screen()
        print(f"====================================")
        print(f"   [환영합니다, {current_user['name']} 님!]")
        print(f"   보유 포인트: {current_user['point']}P ")
        print(f"====================================")
        print("1. 도서 검색 및 대출하기")
        print("2. 도서 반납하기")
        print("3. 도서 추천 (베스트셀러)")
        print("4. 명예의 전당 (다독왕)")
        print("5. PyBook Chat Bot")
        print("\n")
        print("7. 마이페이지 (독서 연대기 등)")
        print("8. 회원 정보 수정")
        print("9. 로그아웃")
        print("0. 회원탈퇴")
        print("====================================")
     
        sub_choice = input("메뉴를 선택하세요: ").strip()

        # 1. 도서 검색 및 대출하기
        if sub_choice == '1':
            _handle_book_search_and_borrow(current_user)

        # 2. 도서 반납하기
        elif sub_choice == '2':
            _handle_book_return(current_user)

        # 3. 도서 추천
        elif sub_choice == '3':
            print("\n도서 추천 기능 연동 예정...\n")
            time.sleep(1.5)

        # 4. 명예의 전당
        elif sub_choice == '4':
            clear_screen()
            analytics_service.show_reading_king()
            input("\n계속하려면 엔터 키를 누르세요...")

        # 5. 챗봇
        elif sub_choice == '5':
            connecting_ai_animation()
            chat_service = AIChatService()
            chat_service.start_chat()
            typing_effect("메인 메뉴로 돌아갑니다...", speed=0.03)
            time.sleep(1)

        # 7. 마이페이지
        elif sub_choice == '7':
            print("\n마이페이지 기능 연동 예정...\n")
            time.sleep(1.5)

        # 8. 회원 정보 수정
        elif sub_choice == '8':
            member_service.update(current_user['email'])

        # 9. 로그아웃
        elif sub_choice == '9':
            print("\n로그아웃합니다.")
            time.sleep(1)
            break

        # 0. 회원탈퇴
        elif sub_choice == '0':
            if member_service.withdraw(current_user["email"]):
                break
        else:
            print("\n[오류] 올바른 번호를 입력해주세요.\n")
            time.sleep(1.5)


def _handle_book_search_and_borrow(current_user):
    """도서 검색 및 대출 서브 로직"""
    clear_screen()
    print("====================================")
    print("            도서 검색               ")
    print("====================================")
    keyword = input("검색할 도서 제목, 저자, 장르를 입력하세요: ").strip()
    
    results, message = search_service.search_books(keyword)
    print(f"\n{message}")
    time.sleep(1.5)
    
    if not results:
        return
        
    current_results = results
    while True:
        clear_screen()
        print("====================================")
        print(f"          검색 결과 (총 {len(current_results)}건)        ")
        print("====================================")
        
        for idx, book in enumerate(current_results, start=1):
            print(f"{idx}. [{book.get('genre', '기타')}] '{book.get('title')}' - {book.get('author')} (평점: {book.get('rating', 0.0)} | 남은 재고: {book.get('available_stock', 0)}개)")
        
        print("====================================")
        print("1. 결과 내 재검색")
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
            print("1. 제목순 | 2. 평점순 | 3. 저자순 | 4. 재고순")
            sort_idx = input("정렬 기준 번호 입력: ").strip()
            sort_map = {'1': 'title', '2': 'rating', '3': 'author', '4': 'available_stock'}
            sort_by = sort_map.get(sort_idx, 'title')
            
            is_reverse = input("내림차순 정렬? (y/n): ").strip().lower() == 'y'
            current_results = search_service.sort_books(current_results, sort_by=sort_by, reverse=is_reverse)
            print("\n정렬 완료!")
            time.sleep(1)
        elif action_choice == '3':
            try:
                book_num = int(input("대출할 도서 번호를 입력하세요: ").strip())
                if 1 <= book_num <= len(current_results):
                    selected_book = current_results[book_num - 1]
                    loan_service.borrow(user_id=current_user['user_id'], book_id=selected_book.get("id"))
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


def _handle_book_return(current_user):
    """도서 반납 서브 로직"""
    clear_screen()
    print("====================================")
    print("            도서 반납하기           ")
    print("====================================")
    
    active_loans = loan_service.get_user_active_loans(current_user['user_id'])
    if not active_loans:
        print("\n현재 대출 중인 도서가 없습니다.")
        time.sleep(2)
        return
        
    print("대출 중인 도서 목록:")
    for idx, loan in enumerate(active_loans, start=1):
        print(f"{idx}. 도서명: '{loan['book_title']}' (대출일: {loan['loan_date']} ~ 반납기한: {loan['due_date']})")
    
    print("====================================")
    return_idx = input("반납할 도서의 번호를 입력하세요 (취소는 엔터): ").strip()
    
    if return_idx.isdigit():
        idx_num = int(return_idx)
        if 1 <= idx_num <= len(active_loans):
            loan_id = active_loans[idx_num - 1]["loan_id"]
            loan_service.return_book(loan_id)
        else:
            print("\n[오류] 올바른 번호를 입력해주세요.")
        time.sleep(2)