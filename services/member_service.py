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
def signup(email: str, pw: str, name: str, phone: str = "", interest: str = "") -> bool:
    
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
def withdraw(email: str, pw: str) -> bool:
    pass


#회원 정보 수정은 우선 함수 한개로 구성해놓았는데 
#구현 하실 때 비밀번호 재설정과 phone,interest,name 부분 수정으로 함수 두개로 나눠서 구현하셔도 됩니다.
def update(email: str, **kwargs) -> bool:
    pass
