# views/admin_view.py

import time
from datetime import datetime
from services.admin_member_service import (
    get_all_members, sort_members, search_members,
    admin_register_member, admin_update_member, admin_delete_member, get_dormant_members
)
from services.admin_book_service import (
    register_book, book_update, book_delete,get_all_book_records,admin_update_review
)
from services.member_service import signup_interests
from utils.file_handler import load_json
from animations.animation_effect import clear_screen


def _display_member_summary(members: list):
    """회원 수정/삭제 전에 회원 기본 정보(ID, 이름, 이메일) 목록 출력"""
    print("=" * 55)
    print(f"{'ID':<6} | {'이름':<10} | 이메일")
    print("=" * 55)
    for m in members:
        print(f"{m.get('user_id', ''):<6} | {m.get('name', ''):<10} | {m.get('email', '')}")
    print("-" * 55)


def _select_member_id(action: str) -> int | None:
    """회원 목록을 보여주고 작업할 회원 ID를 입력받음 (취소하거나 잘못 입력하면 None)"""
    members = get_all_members()
    if not members:
        print("\n등록된 회원이 없습니다.")
        time.sleep(1.5)
        return None

    print("\n[현재 등록된 회원 목록]")
    _display_member_summary(members)

    user_id_in = input(f"\n{action}할 회원의 고유 ID 입력 (취소: 0): ").strip()
    if not user_id_in.isdigit():
        print("\n[오류] 숫자만 입력 가능합니다.")
        time.sleep(1.5)
        return None
    user_id = int(user_id_in)
    if user_id == 0:
        return None
    return user_id


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
        print("3. 회원 등록")
        print("4. 회원 정보 수정")
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
            print("--- [회원 정보 수정] ---")
            user_id = _select_member_id("수정")
            if user_id is None:
                continue

            print("\n[수정 항목 입력] (변경을 원하지 않는 항목은 엔터 키를 누르세요)")
            new_email = input("1. 새 이메일: ").strip() or None
            reset_pw = input("2. 비밀번호를 휴대폰 뒷 4자리로 초기화하시겠습니까? (y/n): ").strip().lower() == 'y'

            # 관심분야는 회원가입과 같은 분류 목록에서 선택 (자유 입력 시 분류가 섞이는 것 방지)
            new_interest = None
            if input("3. 관심분야를 수정하시겠습니까? (y/n): ").strip().lower() == 'y':
                new_interest = signup_interests() or None

            # 포인트: 0 이상의 정수만 허용
            new_point_in = input("4. 새 포인트 (0 이상의 정수): ").strip()
            new_point = None
            if new_point_in:
                if not new_point_in.isdigit():
                    print("\n[오류] 포인트는 0 이상의 정수로 입력해주세요. 수정을 취소합니다.")
                    time.sleep(2)
                    continue
                new_point = int(new_point_in)

            # 가입일: YYYY-MM-DD 형식만 허용 (저장은 기존 데이터와 같은 YYYY-MM-DD HH:MM:SS 형식)
            new_created_at_in = input("5. 새 가입일 (예: 2026-10-01): ").strip()
            new_created_at = None
            if new_created_at_in:
                try:
                    new_created_at = datetime.strptime(new_created_at_in, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    print("\n[오류] 가입일은 YYYY-MM-DD 형식으로 입력해주세요. 수정을 취소합니다.")
                    time.sleep(2)
                    continue

            if not any([new_email, reset_pw, new_interest, new_point is not None, new_created_at]):
                print("\n변경할 항목이 없어 수정을 취소합니다.")
                time.sleep(1.5)
                continue

            _, msg = admin_update_member(
                user_id=user_id,
                new_email=new_email,
                reset_pw_to_phone_last4=reset_pw,
                new_interest=new_interest,
                new_point=new_point,
                new_created_at=new_created_at
            )
            print(f"\n{msg}")
            time.sleep(2)

        elif sub_choice == '5':
            clear_screen()
            print("--- [회원 삭제] ---")
            user_id = _select_member_id("삭제")
            if user_id is None:
                continue

            if input(f"\n정말 회원(ID: {user_id})을 삭제하시겠습니까? (y/n): ").strip().lower() == 'y':
                _, msg = admin_delete_member(user_id)
                print(f"\n{msg}")
            else:
                print("\n삭제 작업이 취소되었습니다.")
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
        else:
            print("\n잘못된 입력입니다. 번호를 다시 선택해주세요.\n")
            time.sleep(1)

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
        print("5. 도서 평점 및 리뷰(감상평) 수정")
        print("6. 이전 메뉴로 돌아가기")
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
            clear_screen()
            print("--- [도서 평점 및 리뷰 관리] ---")
            records = get_all_book_records()
            if not records:
                print("\n등록된 독서 기록 및 리뷰가 없습니다.")
                time.sleep(1.5)
                continue

            print("\n[현재 등록된 독서 기록 목록]")
            print("-" * 75)
            print(f"{'기록ID':<6} | {'회원ID':<6} | {'평점':<4} | {'도서명':<15} | 리뷰 내용")
            print("-" * 75)
            for r in records:
                # 평점이나 리뷰 중 하나만 남긴 기록은 값이 None일 수 있으므로 문자열로 바꿔서 출력
                rating_str = "-" if r.get("rating") is None else str(r.get("rating"))
                title_str = str(r.get("book_title") or "")[:13]
                review_str = str(r.get("review") or "-")[:30]
                print(f"{str(r.get('record_id')):<6} | {str(r.get('user_id')):<6} | {rating_str:<4} | {title_str:<15} | {review_str}")
            print("-" * 75)

            rec_id_in = input("\n수정할 기록 ID 입력 (취소: 0): ").strip()
            if not rec_id_in.isdigit():
                print("\n[오류] 숫자만 입력 가능합니다.")
                time.sleep(1.5)
                continue
            rec_id = int(rec_id_in)
            if rec_id == 0:
                continue

            print("\n[수정 항목 입력] (변경을 원하지 않는 항목은 엔터 키를 누르세요)")
            new_rating_in = input("1. 새 평점 (0.0 ~ 5.0): ").strip()
            new_rating = None
            if new_rating_in:
                try:
                    new_rating = float(new_rating_in)
                except ValueError:
                    print("\n[오류] 평점은 숫자로 입력해주세요. 수정을 취소합니다.")
                    time.sleep(2)
                    continue

            new_review = input("2. 새 리뷰 내용: ").strip() or None

            _, msg = admin_update_review(record_id=rec_id, new_rating=new_rating, new_review=new_review)
            print(f"\n{msg}")
            time.sleep(2)

        elif sub_choice == '6':
            break
        else:
            print("\n잘못된 입력입니다. 올바른 숫자를 입력해주세요.\n")
            time.sleep(1)
