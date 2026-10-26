# services/member_service.py
from datetime import datetime
from models.member import Member
from utils.file_handler import load_json, save_json
import hashlib


#비밀번호 해싱함수
#SHA-256 알고리즘을 이용해 평문 비밀번호를 단방향 암호화된 64자리 문자열로 변환합니다.
'''
회원가입 함수에서는 hashed_pw=_hashed_password(pw)이런형식으로 암호화 후
Member 객체 생성 시 해싱된 비밀번호를 전달하면 됩니다. 
로그인,회원탈퇴 함수에서도 hashed_pw=_hashed_password(pw) 똑같이 해싱후 json 파일에 있는 암호화된 비밀번호와 일치하는 지 검증하면됩니다.
'''
def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

#회원가입
#회원가입하는 아이디(이메일)가 기존의 있는 아이디인아니야지 검증해야합니다.
#비밀번호 해싱 암호화 부분은 구현어려우시면 일단 비밀번호 그대로 members.json에 넣으셔도 됩니다. 나중에 제가 따로 함수 만들어 드리겠습니다.
#비밀번호는 비밀번호 확인(2차입력) 받으셔야 합니다.
def signup(email: str, pw: str, pw_check:str,name: str, phone: str = "", interest: str = "") -> bool:
    
    pass

#이걸로 수정해야됨..
#def signup(email: str, pw: str,pw_check:str, name: str, phone: str = "", interest: str = "") -> bool:
    
    


#로그인
def login(email: str, pw: str) -> dict | None:
    pass

#로그아웃
#로그아웃기능은 아마 함수로 구현할 부분은 없을 가능성이 높습니다.
#main에서 세션관리부분만 초기화시키고 처음 홈화면으로 이동시키면 될거같습니다
def logout(email: str) -> bool:
    # 콘솔 프로그램 특성상 세션 관리는 main.py에서 주로 담당하므로 True 반환
    return True

#회원탈퇴
#구현 시 정말 탈퇴하시겠습니까? 같은 문자 출력후 비밀번호 입력하면 json파일에서 회원정보 삭제하는식으로 탈퇴시키면됩니다.
#회원 탈퇴 후에는 홈화면으로 이동하게됩니다.
#pw: str 변수 필요한지 의논
def withdraw(email: str, pw: str = "") -> bool:
    """
    회원 탈퇴를 진행하는 함수
    - email: 현재 로그인한 회원의 이메일 (str)
    - pw: 비밀번호 (str, 기본값 "")
    - 반환값: 탈퇴 성공 시 True, 실패/취소 시 False (bool)
    """
    print("\n=== [ 회원 탈퇴 ] ===")

    # JSON 파일에서 "회원 목록" 불러오기.
    members = load_json('data/members.json')
    # JSON 파일에서 "대여 목록" 불러오기.
    loans = load_json('data/loans.json')

    # 전체 회원 리스트에서 하나씩 꺼내며 내 계정 찾기.
    for member in members:

        # 이메일이 일치하는 내 회원 딕셔너리.
        if member.get("email") == email:

            # # 미반납 도서가 있으면 탈퇴하지 못하는 "예외 처리" 추가.

            # 전체 대여 리스트에서 하나씩 꺼내며 내 대여 정보 찾기.
            for loan in loans:

                # 이메일이 일치하는 내 대여 정보를 찾고 대출 상태 확인.
                if loan.get("member_id") == email and loan.get("status") == "대출중":
                    
                    # 회원 탈퇴 불가 안내 후, False를 반환해서 함수 종료.
                    print("❌ 현재 대출 중인 도서가 있어 탈퇴할 수 없습니다. 도서를 먼저 반납해 주세요.")
                    return False
                
            # 비밀번호를 입력 받아 본인 확인.
            pw_input = input("본인 확인을 위해 비밀번호를 입력해 주세요: ").strip()

            # 입력받은 비밀번호가 회원 딕셔너리에 저장된 비밀번호와 다르면 False를 반환해서 함수 종료.
            if pw_input != member.get("pw"):
                print("❌ 비밀번호가 일치하지 않습니다. 탈퇴가 취소되었습니다.")
                return False

            # 비밀번호가 일치할 경우, 최종 탈퇴 의사 확인. (대소문자 구분 없이 소문자로 변환)
            confirm = input("정말로 탈퇴하시겠습니까? 탈퇴 후 정보는 복구할 수 없습니다. (y/n): ").strip().lower()

            # 'y' 이외의 문구를 입력받으면 False를 반환해서 함수 종료.
            if confirm != "y":
                print("회원 탈퇴가 취소되었습니다.")
                return False

            # 회원 삭제 및 JSON 파일 저장.
            members.remove(member)
            save_json('data/members.json', members)
            
            # 탈퇴 완료 안내 후, True를 반환해서 함수 종료.
            print("✅ 회원 탈퇴가 완료되었습니다. 그동안 이용해 주셔서 감사합니다.")
            return True


    # 관리자용 이메일을 입력해 회원을 탈퇴 시키는 함수
    # current_member = None
    # for member in members:
    #    if member.get("email") == email:
    #        current_member = member
    #        break

    # 만약 이메일에 해당하는 회원이 없다면 종료
    #if current_member is None:
    #    print("❌ 가입된 이메일이 아닙니다.")
    #    return False


    return False


#회원 정보 수정은 우선 함수 한개로 구성해놓았는데 
#구현 하실 때 비밀번호 재설정과 phone,interest,name 부분 수정으로 함수 두개로 나눠서 구현하셔도 됩니다.
def update(email: str, **kwargs) -> bool:
    pass


# 요구사항 정의서 3번, 마이페이지 - 기본 회원 정보 열람 함수 추가
def show_member_info(email: str) -> dict | None:
    """
    현재 로그인한 회원의 상세 정보를 출력하고 회원 딕셔너리를 반환하는 함수
    - email: 현재 로그인한 회원의 이메일 (str)
    - 반환값: 회원 정보 딕셔너리 (찾지 못한 경우 None)
    """
    print("\n=== [ 내 정보 확인 ] ===")

    # JSON 파일에서 전체 회원 리스트 불러오기.
    members = load_json('data/members.json')

    # 전체 회원 리스트에서 하나씩 꺼내며 내 계정 찾기.
    for member in members:
        
        # 이메일이 일치하는 내 회원 딕셔너리
        if member.get("email") == email:
            
            # 비밀번호는 보안을 위해 글자 수만큼 '*'로 가려서 출력하도록 "예외 처리" 추가.
            pw_length = len(member.get("pw", ""))
            masked_pw = "*" * pw_length

            # 회원 정보 화면 출력. (값이 비어있을 경우 '미입력'으로 표시)
            print(f"• 이메일(ID) : {member.get('email')}")
            print(f"• 비밀번호   : {masked_pw}")
            print(f"• 이름       : {member.get('name', '미입력')}")
            print(f"• 전화번호   : {member.get('phone') or '미입력'}")
            print(f"• 관심분야   : {member.get('interest') or '미입력'}")
            
            # 추가 정보 조건부 출력. (json.md의 tier, point, created_at, last_login_date 반영)
            if "tier" in member:
                print(f"• 회원등급     : {member.get('tier')}")

            if "point" in member:
                print(f"• 포인트       : {member.get('point'):,}P")

            if "created_at" in member:
                print(f"• 가입일       : {member.get('created_at')}")

            if "last_login_date" in member:
                print(f"• 최근 로그인  : {member.get('last_login_date')}")
                
            print("==========================")
            return member

    # 일단 예외의 경우를 위해 적어놨지만, 필요한지 의문
    print("❌ 회원 정보를 찾을 수 없습니다.")
    return None

# --- 테스트용 코드 (확인 후 지우거나 주석 처리) ---
if __name__ == "__main__":
    # 1. 마이페이지 내 정보 확인 테스트
    show_member_info("test@naver.com")
    
    # 2. 회원 탈퇴 테스트
    withdraw("test@naver.com")