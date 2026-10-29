# views/user_view.py
import time
from services import search_service, loan_service, member_service, analytics_service,my_loan_service
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
        print("3. 도서 추천 (베스트셀러)")  #TODO
        print("4. 명예의 전당 (다독왕)")
        print("5. PyBook Chat Bot")
        print("\n")
    
        print("9. 마이페이지")
        print("0. 로그아웃")
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


        # 9. 마이페이지 (회원 탈퇴 시 True가 반환되므로 로그아웃 처리)
        elif sub_choice == '9':
            if _handle_my_page(current_user):
                break

        # 0. 로그아웃
        elif sub_choice == '0':
            print("\n로그아웃합니다.")
            time.sleep(1)
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
            input("\n계속하려면 엔터 키를 누르세요... ")
        else:
            print("\n[오류] 올바른 번호를 입력해주세요.")
            time.sleep(2)




def _handle_my_page(current_user) -> bool:
    """마이페이지 서브 메뉴 (회원 탈퇴가 완료되면 True 반환)"""
    while True:
        # 회원정보 수정 후 바뀐 내용을 반영하기 위해 다시 불러옴
        current_user = member_service.get_member_by_id(current_user["user_id"]) or current_user
        clear_screen()
        print("====================================")
        print(f"        [{current_user['name']} 님의 마이페이지]        ")
        print("====================================")
        print("1. 내 정보 보기")
        print("2. 나의 독서 연대기")
        print("3. 도서 대출 현황")
        print("4. 회원 정보 수정")
        print("5. 회원 탈퇴")
        print("0. 이전 메뉴로 돌아가기")
        print("====================================")

        choice = input("메뉴를 선택하세요: ").strip()

        if choice == '1':
            clear_screen()
            member_service.show_member_info(current_user["email"])
            input("\n계속하려면 엔터 키를 누르세요...")

        elif choice == '2':
            clear_screen()
            timeline=_show_reading_timeline(current_user)
            if timeline and input("\n그래프로 보시겠습니까? (y/n): ").strip().lower()=='y':
                _open_reading_charts(current_user, timeline)
            else:
                input("\n계속하려면 엔터 키를 누르세요...")

        elif choice == '3':
            clear_screen()
            _show_current_loans(current_user)
            input("\n계속하려면 엔터 키를 누르세요...")

        elif choice == '4':
            clear_screen()
            member_service.update(current_user["email"])

        elif choice == '5':
            clear_screen()
            if member_service.withdraw(current_user["email"]):
                time.sleep(1.5)
                return True

        elif choice == '0':
            return False

        else:
            print("\n[오류] 올바른 번호를 입력해주세요.\n")
            time.sleep(1.5)

def _rating_to_stars(rating) -> str:
    """평점을 반올림한 별 5개로 표시 (예: 4 -> ★★★★☆, 4.5 -> ★★★★★)"""
    if rating is None:
        return "평점 없음"
    filled = max(0, min(5, int(rating + 0.5)))   # 반올림 (4.5 -> 5개), 0~5개 범위로 제한
    return "★" * filled + "☆" * (5 - filled)


def _show_reading_timeline(current_user):
    """나의 독서 연대기 출력 (반납 완료한 도서를 월별로 묶어서 표시)"""
    timeline = my_loan_service.get_reading_timeline(current_user["user_id"])

    print("====================================")
    print("           나의 독서 연대기          ")
    print("====================================")

    if not timeline:
        print("\n아직 다 읽은(반납 완료한) 도서가 없습니다.")
        return  []

    current_month = None
    for item in timeline:
        returned_at = item["returned_at"] or ""
        month = returned_at[:7]   # "2026-10"
        if month != current_month:
            current_month = month
            year, mon = (month.split("-") + ["", ""])[:2]
            print(f"\n[{year}년 {mon}월]")

        rating_str = _rating_to_stars(item["rating"])
        print(f"  • {returned_at[5:10]}  『{item['title']}』 - {item['author']} ({item['genre']}) | {rating_str}")
        if item["review"]:
            print(f"      └ \"{item['review']}\"")

    print("\n------------------------------------")
    print(f"총 {len(timeline)}권을 완독했습니다!")
    return timeline

def _open_reading_charts(current_user, timeline):
    """독서 연대기 그래프 창 열기 (창을 닫으면 마이페이지로 돌아옴)"""
    # matplotlib이 없는 PC에서도 다른 기능은 쓸 수 있도록, 그래프를 열 때만 불러옴
    try:
        from utils.visualizer import show_reading_charts
    except ImportError:
        print("\n[안내] 그래프를 보려면 matplotlib을 설치해주세요")
        input("\n계속하려면 엔터 키를 누르세요...")
        return

    print("\n그래프 창을 닫으면 마이페이지로 돌아갑니다...")
    show_reading_charts(timeline, current_user["name"])



def _show_current_loans(current_user):
    """현재 대출 중인 도서와 반납기한(남은 일수 / 연체 일수) 출력"""
    status = my_loan_service.get_current_loan_status(current_user["user_id"], current_user.get("point", 0))
    loans = status["loans"]

    print("====================================")
    print("            도서 대출 현황            ")
    print("====================================")
    print(f"회원 등급: {status['tier']} | 대출 중: {len(loans)} / {status['max_books']}권 | 대출 기간: {status['loan_days']}일")
    print("------------------------------------")

    if not loans:
        print("\n현재 대출 중인 도서가 없습니다.")
        return

    for idx, loan in enumerate(loans, start=1):
        days = loan["remaining_days"]
        if days is None:
            d_day = "기한 정보 없음"
        elif days > 0:
            d_day = f"D-{days}"
        elif days == 0:
            d_day = "오늘까지 반납"
        else:
            d_day = f"*주의* {-days}일 연체 중"

        print(f"{idx}. 『{loan['title']}』 - {loan['author']}")
        print(f"    대출일: {(loan['loan_date'] or '')[:10]} | 반납기한: {(loan['due_date'] or '')[:10]} ({d_day})")


        #TODO
        """
        1. 관심있는 키워드랑 같은 장르중에서 평점순으로 n개 
        2. 키워드 따와가지고 openai api             #가지고 있지 않은 도서도 추천
        3. 국립중앙도서관 api 키워드 기반으로 띄워주기    #가지고 있지 않은 도서도 추천
        
        """