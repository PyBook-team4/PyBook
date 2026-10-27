# services/member_service.py
from datetime import datetime
from models.member import Member
from utils.file_handler import load_json, save_json
#콘솔창 구현 한것중에 clear_screen해야되는 부분에 적용 ex) 회원정보 수정부분 
from animations.animation_effect import clear_screen
# python -m services.member_service
import string
import hashlib
import re

MEMBERS_FILE = "data/members.json"
LOAN_FILE="data/loans.json"

def _get_members() -> list:
    # json파일에서 회원 데이터를 Member 객체 리스트로 반환합니다.
    data = load_json(MEMBERS_FILE)
    if isinstance(data, list):
        return [Member.from_dict(item) for item in data]
    return []

def _save_members(members: list[Member]) -> None:
    #Member 객체 리스트를 딕셔너리로 변환하여 JSON파일에 저장합니다.
    data = [member.to_dict() for member in members]
    save_json(MEMBERS_FILE, data)

# 비밀번호 해싱
def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# 회원 아이디(이메일) 검증
def is_valid_email(email: str) -> bool:
    # 문자열 타입 검증
    if not isinstance(email,str):
        return False
    # 길이검증(5자 이상)
    if len(email) < 5:
        return False
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        return False


    return True

# 비밀번호 검증하기
def is_valid_pw(pw: str) -> bool:
    # 길이검증(5자 이상)
    if len(pw) < 5:
        return False
    # 특수문자 포함 여부 검증
    has_special = any(char in string.punctuation for char in pw)
    if not has_special:
        return False

    return True

def is_valid_find_pw() -> dict:
    #회원가입시 비밀번호 찾기용 질문을 선택하고 답을 입력받아 반환하는 함수입니다.
    find_pw_questions = [
        "내가 생각하는 나만의 보물1호는?",
        "졸업한 초등학교의 이름은?",
        "가장 감명 깊게 본 영화의 제목은?",
        "조부모님의 성함은?",
        "생애 첫 아르바이트를 했던 가게의 이름은?",
        "가장 처음으로 키웠던 반려동물의 이름은?",
        "태어나서 처음 살았던 동네의 이름은?"] # 비밀번호 찾기용 질문 목록들

    for number, question in enumerate(find_pw_questions, start=1):
        print(f'{number},{question}')

    while True:
        print("="*50)
        choice = input("비밀번호를 찾을 때 질문을 선택하세요(번호 입력): ").strip()

        #숫자를 입력했는지 확인
        if not choice.isdigit():
            print("숫자만 입력해주세요.")
            continue

        choice_num = int(choice)

        # 선택지 중의 숫자를 입력했는지 확인
        if choice_num < 1 or choice_num > len(find_pw_questions):
            print(f"1 ~ {len(find_pw_questions)} 의 번호를 입력하여 선택해주세요.")
        else:
            selected_question = find_pw_questions[choice_num-1]
            break


    user_answer = input("선택하신 질문의 답을 입력하세요: ").strip()

    return {
        "question" : selected_question,
        "answer" : user_answer
    }


# 연락처 검증하기
def is_valid_phone(phone: str) -> bool:
    # 문자열 타입 검증
    if not isinstance(phone, str):
        return False
    # 하이픈(-)과 공백 제거
    clean_phone = phone.replace("-", "").replace(" ", "")

    # 숫자로만 이루어졌는지 확인
    if not clean_phone.isdigit():
        return False

    # 010으로 시작하는지 확인 (국내 휴대전화 표준)
    if not clean_phone.startswith("010"):
        return False

    # 010 포함 총 11자리인지 확인
    if len(clean_phone) != 11:
        return False

    return True

# 관심 분야 
def signup_interests():
    """
    회원가입시 책 관심분야를 설정하고 반환하는 함수입니다.
    """

    available_categories = [
    "총류", "철학", "종교", 
    "사회과학", "자연과학", "기술과학", "예술", 
    "언어", "문학", "역사"
    ] # 국립중앙도서관 도서관 정보나루의 주제 분류를 참고
    print("="*50)
    user_categories = []
    

    # 선택할 수 있는 관심분야 항목 출력
    for number, category in enumerate(available_categories, start=1):
        print(f"{number}. {category}")

    while len(user_categories) < 3:
        print("="*50)
        choice = input(f"\n관심분야 번호 입력 ({len(user_categories)}/3) (종료는 엔터): ").strip()

        # 사용자가 1~2개만 선택하고 싶을 때, 엔터를 치면 즉시 종료
        if not choice:
            break
        
        # 입력한 값이 숫자인지 먼저 확인
        if not choice.isdigit():
            print("숫자만 입력해주세요.")
            continue

        # 입력받은 번호를 정수형으로 전환
        choice_num = int(choice)
    
        # 입력한 숫자가 1번부터 목록의 마지막 번호 사이에 있는지 확인
        if choice_num < 1 or choice_num > len(available_categories):
            print("목록에 없는 번호입니다.")
            continue
        
        # 사용자가 입력한 번호를 분류명으로 변환
        selected_category = available_categories[choice_num - 1]

        # 이미 관심분야에 추가한 항목인지 중복 검사
        if selected_category in user_categories:
            print("이미 선택한 항목입니다.")
            continue

        # 회원 관심분야에 추가
        user_categories.append(selected_category)
        print(f"-> '{selected_category}' 항목이 추가되었습니다.")

    print(f"\n최종 설정된 관심분야: {user_categories}")

    return user_categories



#💡 회원가입 💡
#회원가입하는 아이디(이메일)가 기존의 있는 아이디인지 검증해야합니다.
#비밀번호 해싱 암호화 부분은 구현어려우시면 일단 비밀번호 그대로 members.json에 넣으셔도 됩니다. 나중에 제가 따로 함수 만들어 드리겠습니다.
#비밀번호는 비밀번호 확인(2차입력) 받으셔야 합니다.

def signup() -> bool:

    members = _get_members()
    new_id = max([getattr(m, 'user_id', 0) for m in members], default=0) + 1

    print("\n---[회원가입]---")

    # 이메일(아이디) 입력 & 검증
    while True:
        email_input = input("아이디 입력(이메일 형식): ").strip()

        # 이메일 양식 검증
        if not is_valid_email(email_input):
            print("[오류] 아이디는 @를 포함한 5글자 이상으로 입력하세요.")
            continue

        # 중복 확인
        is_duplicate = any(m.email == email_input for m in members)
        if is_duplicate:
            print("[오류] 이미 존재하는 아이디입니다. 다시 입력해주세요.")
            continue

        break
    print(f"아이디 입력 완료: {email_input}")

    # 비밀번호 입력 & 검증
    while True:
        pw_input = input("비밀번호 입력: ").strip()

        if not pw_input:
            print("[오류] 비밀번호는 필수 입력 항목입니다.")
            continue

        if not is_valid_pw(pw_input):
            print("[오류] 비밀번호는 5자 이상이며, 특수문자를 최소 1개 이상 포함해야 합니다.")
            continue

        # 비밀번호 2차 확인
        pw_check = input("비밀번호 확인을 위해 한 번 더 입력해주세요: ").strip()
        if pw_input != pw_check:
            print("[오류] 입력하신 비밀번호가 서로 일치하지 않습니다. 다시 입력해주세요.")
            continue

        break

    # 비밀번호 해싱
    hashed_pw = _hash_password(pw_input)

    # 비밀번호 찾기 질문 & 답변
    print("="*50)
    find_pw_info = is_valid_find_pw()

    # 이름 입력
    while True:
        name_input = input("이름 입력: ").strip()
        if not name_input:
            print("[오류] 이름은 필수 입력 항목입니다.")
            continue
        break

    # 연락처 입력 & 검증
    while True:
        phone_input = input("연락처 입력(- 제외 숫자 11자리): ").strip()
        if not is_valid_phone(phone_input):
            print("[오류] 연락처는 숫자 11자리로 입력해야 합니다. (예: 01012345678)")
            continue
        break

    # 관심분야 입력 (선택)
    interest_input = signup_interests()

    
    # Member 객체 생성 및 JSON 파일 저장
    new_member = Member(
        user_id=new_id,
        email=email_input,
        pw=hashed_pw,
        name=name_input,
        phone=phone_input,
        interest=interest_input,
        point=100,
        pw_question=find_pw_info["question"],  # 질문 추가
        pw_answer=find_pw_info["answer"],      # 답변 추가
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        last_login=None # 첫 로그인 전에는 None
    )

    # 리스트에 추가 후 파일 저장
    members.append(new_member)
    _save_members(members)

    print(f'{name_input}님, 회원가입이 완료되었습니다!')
    return True

#💡 로그인 💡
def login(email: str, pw: str) -> dict | None:
    members = _get_members()
    #비밀번호 해싱
    hashed_pw = _hash_password(pw)

    for member in members:
        if member.email == email:
            if member.pw == hashed_pw:
                # 로그인 성공 시 마지막 로그인 일시 업데이트
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                member.last_login = now_str

                _save_members(members)

                print(f'{member.name}님, 환영합니다!')
                print(f'[계정 정보] 가입일: {member.created_at} | 최근 로그인: {member.last_login}')
                return True, member.to_dict()
            else:
                print("비밀번호가 올바르지 않습니다.")
                return None
            
    print("존재하지 않는 이메일 계정입니다.")
    return None



#💡 로그아웃 💡
#로그아웃기능은 아마 함수로 구현할 부분은 없을 가능성이 높습니다.
#main에서 세션관리부분만 초기화시키고 처음 홈화면으로 이동시키면 될거같습니다
def logout(email: str) -> bool:
    # 콘솔 프로그램 특성상 세션 관리는 main.py에서 주로 담당하므로 True 반환
    return True

#💡 회원탈퇴 💡
#구현 시 정말 탈퇴하시겠습니까? 같은 문자 출력후 비밀번호 입력하면 json파일에서 회원정보 삭제하는식으로 탈퇴시키면됩니다.
#회원 탈퇴 후에는 홈화면으로 이동하게됩니다.
def withdraw(email: str, pw: str) -> bool:

    members = _get_members()
    # 이메일과 일치하는 회원 찾기
    target_member = next((m for m in members if m.email == email), None)

    # 이메일 검증
    if not target_member:
        print("[오류] 존재하지 않는 회원 계정입니다.")
        return False

    # 비밀번호 검증
    if target_member.pw != pw:
        print("[오류] 비밀번호가 올바르지 않습니다.")
        return False

    #대출 항목 중 미 반납 항목이 있는지 검사
    #TODO 현재 withdraw(email,pw)을 받고 있어서 member.json에서 id를 다시 찾아와야됨 코드리팩토링 진행 시 wirhdraw(user_id, pw)이런식으로 변경하고 loans.json에 있는 user_id와 바로 비교

    loans_data=load_json(LOAN_FILE)     #전체 대출 기록 파일 불러오기
    target_user_id = target_member.user_id  #방금 찾은 회원의 고유 번호(user_id) 저장
    
     #any() 함수 사용해서 "대출중" 인 책이 하나라도 있는지 검사
    has_active_loan = any(
        # 2. 각 기록들 (loan) 보면서  다음 두 조건을 만족하는 loan이 하나라도 있으면 무조건 True 반환(=has_active_loan은 True가 됨)
        loan.get("user_id") == target_user_id and loan.get("status") == "대출중"
        # 1. loans_data에 있는 대출 기록들을 하나씩(loan) 불러오기
        for loan in loans_data          
    )

    if has_active_loan:
        print("\n[오류] 현재 대출 중인 도서가 있어 탈퇴할 수 없습니다. 도서를 먼저 반납해 주세요.")
        return False

    # 탈퇴 의사 재확인
    confirm = input("정말로 탈퇴하시겠습니까? (Y/N): ").strip().upper()
    
    if confirm == "Y":
        # 해당 이메일 제외한 리스트로 재구성
        members = [m for m in members if m.email != email]
        # JSON 파일에 저장
        _save_members(members)
        print("\n 회원 탈퇴가 정상적으로 처리되었습니다. 이용해 주셔서 감사합니다.")
        return True
    else:
        print("\n회원 탈퇴가 취소되었습니다.")
        return False


#회원 정보 수정은 우선 함수 한개로 구성해놓았는데 
#구현 하실 때 비밀번호 재설정과 phone,interest,name 부분 수정으로 함수 두개로 나눠서 구현하셔도 됩니다.

#💡 회원 정보 수정 💡
def update(email: str = "", **kwargs)->bool:
    #kwargs 형태로 전달받은 회원정보를 업데이트합니다.
    members = _get_members()
    updated_member = None # 수정 대상 회원

    # 수정할 회원 찾기
    if not email:
        email = input("회원 아아디(이메일) 입력: ").strip()

    updated_member = next((m for m in members if m.email == email), None)

    if updated_member is None:
        print("[오류] 해당 회원을 찾을 수 없습니다.")
        return False

    updated = False

    # 수정 메뉴
    while True:
        print("\n--- 수정할 항목 선택 ---")
        print("1. 비밀번호 수정")
        print("2. 이름 수정")
        print("3. 연릭처 수정")
        print("4. 관심분야 수정")
        print("0. 수정 종료")

        choice = input("메뉴 선택: ").strip()

        # pw 수정
        if choice == "1":
            while True:
                new_pw = input("새 비밀번호 입력: ").strip()

                if not new_pw:
                    print("[오류] 비밀번호를 입력해주세요.")
                    continue
                if not is_valid_pw(new_pw):
                    print("[오류] 비밀번호는 5자 이상이며, 특수문자를 최소 1개 이상 포함합니다.")
                    continue

                pw_confirm = input("새 비밀번호 확인: ").strip()

                if new_pw != pw_confirm:
                    print("[오류] 비밀번호가 일치하지 않습니다.")

                updated_member.pw = _hash_password(new_pw)
                updated = True
                print("비밀번호가 수정되었습니다.")
                break

        # 이름 수정
        elif choice == "2":
            new_name = input("새 이름 입력: ").strip()

            if not new_name:
                print("[오류] 이름을 입력해주세요.")
                continue

            updated_member.name = new_name
            updated = True
            print("이름이 수정되었습니다.")

        # 연락처 수정
        elif choice == "3":
            new_phone = input("새 연락처 입력(- 제외 숫자 11자리): ").strip()

            if not is_valid_phone(new_phone):
                print("[오류] 연락처는 숫자 11자리로 입력해주세요.")
                continue

            updated_member.phone = new_phone
            updated = True
            print("연락처가 수정되었습니다.")

        # 관심분야 수정
        elif choice == "4":
            print(f"\n[ 현재 관심분야: {updated_member.interest} ]")
            # 기존에 만드신 카테고리 선택 함수 실행
            new_interests = signup_interests()

            if new_interests:
                updated_member.interest = new_interests
                updated = True
                print("-> 관심분야가 성공적으로 수정되었습니다.")
            else:
                print("[알림] 관심분야가 변경되지 않았습니다.")

        # 0. 수정 종료 및 저장
        elif choice == "0":
            if updated:
                _save_members(members)
                print("\n[성공] 변경된 내용이 파일에 성공적으로 저장되었습니다.")
            else:
                print("\n[알림] 변경된 항목 없이 수정을 종료합니다.")
            break

        else:
            print("[오류] 올바른 메뉴 번호를 선택해주세요.")

    return updated


# 💡비밀번호 찾기💡
# 비밀번호 찾기 (질문/답변 검증 후 비밀번호 재설정)
# 이메일 입력받아 등록된 회원 확인, 비민번호 찾기 질문과 답변 일치하면 새 pw로 변경합니다
def find_pw() -> bool:

    members = _get_members()

    print("\n--- [비밀번호 찾기] ---")
    email_input = input("가입하신 아이디(이메일)를 입력하세요: ").strip()

    # 회원 존재 여부 확인
    target_member = next((m for m in members if m.email == email_input),None)

    if not target_member:
        print("[오류] 등록되지 않은 이메일 계정입니다.")
        return False

    # 등록된 질문 출력
    print(f"\n[비밀번호 찾기 질문]\n {target_member.pw_question}")
    answer_input = input("답변 입력: ").strip()

    # 답변 검증
    if target_member.pw_answer != answer_input:
        print("[오류] 답변이 일치하지 않습니다. 비밀번호를 찾을 수 없습니다.")
        return False

    print("\n본인 확인이 완료되었습니다.")

    # 새 비밀번호 입력 및 검증
    while True:
        new_pw = input("새로운 비밀번호를 입력해주세요: ").strip()

        if not new_pw:
            print("[오류] 비밀번호는 필수 입력 항목입니다.")
            continue
        if not is_valid_pw(new_pw):
            print("[오류] 비밀번호는 5자 이상이며, 특수문자를 최소 1개 이상 포함해야 합니다.")
            continue

        pw_check = input("새 비밀번호 확인: ").strip()
        if new_pw != pw_check:
            print("[오류] 입력하신 비밀번호가 서로 일치하지 않습니다.")
            continue

        break

    target_member.pw = _hash_password(new_pw)

    # 변경사항 파일에 저장
    _save_members(members)
    print("\n비밀번호가 성공적으로 재설정되었습니다! 새로운 비밀번호로 로그인해주세요.")
    return True


    



# ==========================================
#테스트 코드
# ==========================================
if __name__ == "__main__":
    # print("=" * 50)
    # print("회원가입 테스트")
    # print("=" * 50)
   
    # signup()
   
    # ######################
    # print("=" * 50)
    # print("로그인 테스트")
    # print("=" * 50)

    # while True:
    #     print("\n--- [ 로그인 ] ---")
    #     login_email = input("아이디(이메일) 입력: ").strip()
    #     login_pw = input("비밀번호 입력: ").strip()
    # ######################
    #     # 로그인 시도
    #     user_data = login(login_email, login_pw)

    #     if user_data:
    #         print(f"\n[로그인 성공 데이터 반환 확인]: {user_data}")
    #         break
    #     else:
    #         retry = input("\n다시 로그인하시겠습니까? (Y/N): ").strip().upper()
    #         if retry != "Y":
    #             print("로그인 테스트를 종료합니다.")
    #             break


    
    # ######################
    # print("=" * 50)
    # print("회원정보수정 테스트")
    # print("=" * 50)

    # login_email = input("수정할 계정(이메일) 입력: ").strip()
    
    # # update 함수 실행 (메뉴 선택창 출력)
    # update(login_email)

    # ######################
    # print("=" * 50)
    # print("회원탈퇴 테스트")
    # print("=" * 50)
    # withdraw_email = input("탈퇴할 계정(이메일) 입력: ").strip()
    # withdraw_pw = input("비밀번호 입력: ").strip()
    # withdraw(withdraw_email, withdraw_pw)

    print("=" * 50)
    print("비밀번호 찾기 테스트")
    print("=" * 50)

    find_pw()
