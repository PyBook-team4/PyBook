# views/admin_view.py

import time
from services.admin_member_service import (
    get_all_members, sort_members, search_members,
    admin_register_member, admin_update_member, admin_delete_member, get_dormant_members
)
from services.admin_book_service import register_book, book_update, book_delete
from utils.file_handler import load_json
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
            sort_opt = input("정렬 기준 선택 -> 1: ID, 2: 이름, 3: 포인트, 4: 가입일 (기본 1): ").strip()
            sort_map = {'1': 'user_id', '2': 'name', '3': 'point', '4': 'created_at'}
            sort_by = sort_map.get(sort_opt, 'user_id')
            
            reverse = input("내림차순 정렬? (y/n, 기본 n): ").strip().lower() == 'y'
            members = get_all_members()
            sorted_members = sort_members(members, sort_by=sort_by, reverse=reverse)
            
            if not sorted_members:
                print("\n등록된 회원이 없습니다.")
            else:
                for m in sorted_members:
                    print(f"ID: {m.get('user_id')} | 이름: {m.get('name')} | 이메일: {m.get('email')} | 포인트: {m.get('point')}P | 티어: {m.get('tier')}")
            input("\n계속하려면 엔터 키를 누르세요...")

        elif sub_choice == '2':
            clear_screen()
            keyword = input("검색할 키워드 입력: ")
            results = search_members(keyword)
            print(f"\n검색 결과: 총 {len(results)}건")
            for m in results:
                print(f"ID: {m.get('user_id')} | 이름: {m.get('name')} | 이메일: {m.get('email')}")
            input("\n계속하려면 엔터 키를 누르세요...")

        elif sub_choice == '3':
            clear_screen()
            email = input("이메일 입력: ").strip()
            name = input("이름 입력: ").strip()
            phone = input("연락처 입력 (11자리): ").strip()
            _, msg = admin_register_member(email=email, name=name, phone=phone)
            print(f"\n{msg}")
            time.sleep(2)

        elif sub_choice == '4':
            clear_screen()
            try:
                user_id = int(input("수정할 회원의 고유 ID 입력: ").strip())
            except ValueError:
                print("\n숫자만 입력 가능합니다.")
                time.sleep(1.5)
                continue
            new_email = input("새 이메일 (변경 없으면 엔터): ").strip() or None
            reset_pw = input("비밀번호를 휴대폰 뒷 4자리로 초기화? (y/n): ").strip().lower() == 'y'
            _, msg = admin_update_member(user_id=user_id, new_email=new_email, reset_pw_to_phone_last4=reset_pw)
            print(f"\n{msg}")
            time.sleep(2)

        elif sub_choice == '5':
            clear_screen()
            try:
                user_id = int(input("삭제할 회원의 고유 ID 입력: ").strip())
            except ValueError:
                print("\n숫자만 입력 가능합니다.")
                time.sleep(1.5)
                continue
            if input(f"정말 회원(ID: {user_id})을 삭제하시겠습니까? (y/n): ").strip().lower() == 'y':
                _, msg = admin_delete_member(user_id)
                print(f"\n{msg}")
            time.sleep(2)

        elif sub_choice == '6':
            clear_screen()
            dormants = get_dormant_members(days=90)
            print(f"\n휴면 회원 총 {len(dormants)}명:")
            for m in dormants:
                print(f"ID: {m.get('user_id')} | 이름: {m.get('name')} | 사유: {m.get('dormant_reason')}")
            input("\n계속하려면 엔터 키를 누르세요...")

        elif sub_choice == '7':
            break

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
            books = load_json("data/books.json")
            for b in books:
                print(f"ID: {b.get('id')} | 제목: {b.get('title')} | 저자: {b.get('author')} | 재고: {b.get('available_stock')}/{b.get('total_stock')}")
            input("\n계속하려면 엔터 키를 누르세요...")

        elif sub_choice == '2':
            clear_screen()
            title = input("도서 제목: ").strip()
            author = input("저자: ").strip()
            publisher = input("출판사: ").strip()
            genre = input("장르: ").strip()
            isbn = input("ISBN: ").strip()
            try:
                tot = int(input("총 보유량 (1~10): ").strip())
                avail = int(input("대여 가능 재고: ").strip())
                register_book(title, author, publisher, genre, isbn, tot, avail)
            except ValueError:
                print("\n숫자를 올바르게 입력해주세요.")
            time.sleep(1.5)

        elif sub_choice == '3':
            clear_screen()
            try:
                book_id = int(input("수정할 도서 ID: ").strip())
                field = int(input("항목 선택 (1:제목, 2:저자, 3:출판사, 4:ISBN, 5:장르, 6:평점, 7:총재고, 8:대여가능재고): ").strip())
                val = input("변경할 값 입력: ")
                book_update(book_id, field, val)
            except ValueError:
                print("\n올바른 숫자를 입력해주세요.")
            time.sleep(2)

        elif sub_choice == '4':
            clear_screen()
            try:
                book_id = int(input("삭제할 도서 ID: ").strip())
                if input(f"정말 도서(ID: {book_id})를 삭제하시겠습니까? (y/n): ").strip().lower() == 'y':
                    book_delete(book_id)
            except ValueError:
                print("\n올바른 숫자를 입력해주세요.")
            time.sleep(2)

        elif sub_choice == '5':
            break
            
