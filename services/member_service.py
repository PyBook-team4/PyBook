# services/member_service.py
from datetime import datetime
from models.member import Member
from utils.file_handler import load_json, save_json


import string

MEMBERS_FILE = "data/members.json"

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

# 회원 아이디(이메일) 검증
def is_valid_email(email: str) -> bool:
    # 문자열 타입 검증
    if not isinstance(email,str):
        return False
    # 길이검증(5자 이상)
    if len(email) < 5:
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



#회원가입
#회원가입하는 아이디(이메일)가 기존의 있는 아이디인지 검증해야합니다.
#비밀번호 해싱 암호화 부분은 구현어려우시면 일단 비밀번호 그대로 members.json에 넣으셔도 됩니다. 나중에 제가 따로 함수 만들어 드리겠습니다.
#비밀번호는 비밀번호 확인(2차입력) 받으셔야 합니다.
# signup 함수 선언부 매개변수에 기본값 = "" 추가
def signup(email: str = "", pw: str = "", name: str = "", phone: str = "", interest: str = "") -> bool:
     
    members = _get_members()

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
        email=email_input,
        pw=pw_input,
        name=name_input,
        phone=phone_input,
        interest=interest_input,
        pw_question=find_pw_info["question"],  # 질문 추가
        pw_answer=find_pw_info["answer"]       # 답변 추가
    )

    # 리스트에 추가 후 파일 저장
    members.append(new_member)
    _save_members(members)

    print(f'{name_input}님, 회원가입이 완료되었습니다!')
    return True

#로그인
def login(email: str, pw: str) -> dict | None:
    members = _get_members()

    for member in members:
        if member.email == email:
            if member.pw == pw:
                print(f'{member.name}님, 환영합니다!')
                return member.to_dict()
            else:
                print("비밀번호가 올바르지 않습니다.")
                return None
            
    print("존재하지 않는 이메일 계정입니다.")
    return None





#로그아웃
#로그아웃기능은 아마 함수로 구현할 부분은 없을 가능성이 높습니다.
#main에서 세션관리부분만 초기화시키고 처음 홈화면으로 이동시키면 될거같습니다
def logout(email: str) -> bool:
    # 콘솔 프로그램 특성상 세션 관리는 main.py에서 주로 담당하므로 True 반환
    return True

#회원탈퇴
#구현 시 정말 탈퇴하시겠습니까? 같은 문자 출력후 비밀번호 입력하면 json파일에서 회원정보 삭제하는식으로 탈퇴시키면됩니다.
#회원 탈퇴 후에는 홈화면으로 이동하게됩니다.
def withdraw(email: str, pw: str) -> bool:
    pass


#회원 정보 수정은 우선 함수 한개로 구성해놓았는데 
#구현 하실 때 비밀번호 재설정과 phone,interest,name 부분 수정으로 함수 두개로 나눠서 구현하셔도 됩니다.

# 회원 정보 수정
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

                updated_member.pw = new_pw
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





    



# ==========================================
#테스트 코드
# ==========================================
if __name__ == "__main__":
    print("=" * 50)
    print("회원가입 테스트")
    print("=" * 50)
   
    signup()
   
    ######################
    print("=" * 50)
    print("로그인 테스트")
    print("=" * 50)

    while True:
        print("\n--- [ 로그인 ] ---")
        login_email = input("아이디(이메일) 입력: ").strip()
        login_pw = input("비밀번호 입력: ").strip()
    ######################
        # 로그인 시도
        user_data = login(login_email, login_pw)

        if user_data:
            print(f"\n[로그인 성공 데이터 반환 확인]: {user_data}")
            break
        else:
            retry = input("\n다시 로그인하시겠습니까? (Y/N): ").strip().upper()
            if retry != "Y":
                print("로그인 테스트를 종료합니다.")
                break


    
    ######################
    print("=" * 50)
    print("회원정보수정 테스트")
    print("=" * 50)

    login_email = input("수정할 계정(이메일) 입력: ").strip()
    
    # update 함수 실행 (메뉴 선택창 출력)
    update(login_email)