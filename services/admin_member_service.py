# services/admin_member_service.py

from datetime import datetime
import hashlib
import re
import string

from models.member import Member
from utils.file_handler import load_json, save_json
from animations.animation_effect import clear_screen

# 데이터 파일 경로 정의
MEMBERS_FILE = "data/members.json"
LOANS_FILE = "data/loans.json"


# [공통/유틸리티 함수]

def _get_members() -> list:
    """JSON 파일에서 회원 데이터를 Member 로 반환"""
    data = load_json(MEMBERS_FILE)
    if isinstance(data, list):
        return [Member.from_dict(item) for item in data]
    return []


def _save_members(members: list) -> None:
    """Member 를 딕셔너리로 JSON 파일에 저장"""
    data = [member.to_dict() for member in members]
    save_json(MEMBERS_FILE, data)


def _hash_password(password: str) -> str:
    """비밀번호를 SHA-256 방식으로 안전하게 암호화(해싱)합니다."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def get_tier_info_by_point(point: int) -> dict:
    """등급 계산 함수"""
    if point is None or not isinstance(point, (int, float)):
        point = 0

    if point >= 1000:
        tier_name = "VIP"
        max_books = 8
        loan_days = 30
    elif point >= 500:
        tier_name = "GOLD"
        max_books = 6
        loan_days = 21
    elif point >= 200:
        tier_name = "SILVER"
        max_books = 4
        loan_days = 14
    else:
        tier_name = "BRONZE"
        max_books = 2
        loan_days = 7

    return {
        "tier": tier_name,
        "max_books": max_books,
        "loan_days": loan_days
    }


# 회원 전체 목록 조회
def get_all_members() -> list:
    """전체 회원 정보 리스트(티어 추가)"""
    members = _get_members()
    member_list = []

    for m in members:
        # 회원의 현재 포인트를 기반으로 실시간 등급 산출
        tier_info = get_tier_info_by_point(m.point)
        
        # 딕셔너리로 변환 후 계산된 티어 정보 주머니 추가
        m_dict = m.to_dict()
        m_dict["tier"] = tier_info["tier"].upper()
        m_dict["max_books"] = tier_info["max_books"]
        m_dict["loan_days"] = tier_info["loan_days"]
        
        member_list.append(m_dict)

    return member_list


# 회원 목록 정렬 
def sort_members(member_list: list, sort_by: str = "user_id", reverse: bool = False) -> list:
    """회원 정렬 함수
    - member_list: 정렬할 회원 딕셔너리 리스트
    - sort_by: 정렬 기준 ('user_id', 'name', 'point', 'created_at')
    - reverse: True면 내림차순, False면 오름차순
    """
    if not member_list:
        return []

    # 정렬 기준값을 추출
    def get_sort_key(member_item):
        if sort_by in ["user_id", "point"]:
            # 숫자형 데이터는 정수로 비교
            return int(member_item.get(sort_by, 0))
        # 문자열 데이터(이름, 날짜 등)는 문자열로 비교
        return str(member_item.get(sort_by, ""))

    return sorted(member_list, key=get_sort_key, reverse=reverse)


# 회원 검색
def search_members(keyword: str) -> list:
    """이름, 이메일, 전화번호 중 검색한 내용 포함 회원 반환"""
    keyword = keyword.strip().lower()
    all_members = get_all_members()

    if not keyword:
        return all_members

    results = []
    for m in all_members:
        name = m.get("name", "").lower()
        email = m.get("email", "").lower()
        phone = m.get("phone", "").replace("-", "")

        # 검색어가 이름, 이메일, 전화번호 중 하나라도 포함되면 추가
        if (keyword in name) or (keyword in email) or (keyword in phone):
            results.append(m)

    return results


# 관리자 회원 등록
def admin_register_member(email: str, name: str, phone: str,point: int = 100, interest: list = None) -> tuple:
    """
    관리자 전용 회원 등록
    - 초기 비밀번호는 회원의 '휴대폰 번호 마지막 4자리'로 자동 설정 후 저장됩니다.
    - 반환값: (성공여부 bool, 안내메시지 str)
    """
    members = _get_members()

    # 1. 이메일 중복 검사
    if any(m.email == email for m in members):
        return False, "이미 사용 중인 이메일 계정입니다."

    # 2. 연락처 유효성 검사 (숫자 11자리 기준)
    clean_phone = phone.replace("-", "").replace(" ", "")
    if len(clean_phone) != 11 or not clean_phone.isdigit():
        return False, "연락처는 11자리 숫자여야 합니다. (예: 01012345678)"

    # 3. 비밀번호 자동 생성: 휴대폰 뒷 4자리 -> 해싱
    default_pw = clean_phone[-4:]
    hashed_pw = _hash_password(default_pw)

    # 4. 신규 user_id 채번 (기존 최대값 + 1)
    new_user_id = max([getattr(m, 'user_id', 0) for m in members], default=0) + 1

    # 5. 새 Member 객체 생성
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_member = Member(
        user_id=new_user_id,
        email=email,
        pw=hashed_pw,
        name=name,
        phone=clean_phone,
        interest=interest or [],
        point=point,
        pw_question="관리자 등록 계정 기본 질문",
        pw_answer="관리자",
        created_at=now_str,
        last_login=None
    )

    # 6. 리스트 추가 및 파일 저장
    members.append(new_member)
    _save_members(members)

    return True, f"회원 등록 성공! (ID: {email} / 초기 비밀번호: {default_pw})"


# 회원 정보 수정
def admin_update_member(user_id: int, new_email: str = None, reset_pw_to_phone_last4: bool = False,
                        new_interest: list = None, new_point: int = None, new_created_at: str = None) -> tuple:
    """
    관리자 전용 회원 정보 수정
    - user_id로 대상 회원을 찾아 전달된 항목만 수정
    - reset_pw_to_phone_last4가 True이면, 비밀번호를 해당 회원의 '휴대폰 뒷 4자리'로 초기화하여 해싱 저장
    """
    members = _get_members()
    target_member = next((m for m in members if m.user_id == user_id), None)

    if not target_member:
        return False, f"회원 고유번호(ID: {user_id})를 찾을 수 없습니다."

    # 1. 이메일 수정 (중복 검사)
    if new_email and new_email != target_member.email:
        if any(m.email == new_email and m.user_id != user_id for m in members):
            return False, "이미 다른 회원이 사용 중인 이메일입니다."
        target_member.email = new_email

    # 2. 비밀번호 초기화 (휴대폰 번호 마지막 4자리로 재설정)
    if reset_pw_to_phone_last4:
        clean_phone = target_member.phone.replace("-", "").replace(" ", "")
        if len(clean_phone) >= 4:
            new_plain_pw = clean_phone[-4:]
            target_member.pw = _hash_password(new_plain_pw)
        else:
            return False, "등록된 연락처가 올바르지 않아 비밀번호를 초기화할 수 없습니다."

    # 3. 관심분야 수정
    if new_interest is not None:
        target_member.interest = new_interest

    # 4. 포인트 수정 (음수 방어)
    if new_point is not None:
        target_member.point = max(0, new_point)

    # 5. 가입일 수정 (형식 검증: YYYY-MM-DD 또는 YYYY-MM-DD HH:MM:SS)
    if new_created_at:
        target_member.created_at = new_created_at

    # 파일 영구 저장
    _save_members(members)
    return True, f"회원(ID: {user_id})의 정보가 성공적으로 수정되었습니다."


# 회원 강제 삭제 (대출 중 삭제 불가 추가)
def admin_delete_member(user_id: int) -> tuple:
    """관리자 전용 회원 강제 삭제 (대출중인 경우 삭제 불가)"""
    members = _get_members()
    loans_data = load_json(LOANS_FILE)

    # 회원 여부 확인
    target_member = next((m for m in members if m.user_id == user_id), None)
    if not target_member:
        return False, f"회원 고유번호(ID: {user_id})를 찾을 수 없습니다."

    # 대출 중인 도서 여부 확인
    active_loans = [
        loan for loan in loans_data 
        if loan.get("user_id") == user_id and loan.get("status") == "대출중"
    ]
    if active_loans:
        return False, f"해당 회원은 현재 {len(active_loans)}권의 도서를 대출 중이므로 삭제할 수 없습니다. (반납 처리 후 삭제 가능)"

    # 대상 회원을 제외하고 재확인 후 저장
    members = [m for m in members if m.user_id != user_id]
    _save_members(members)

    return True, f"회원(ID: {user_id}, 이름: {target_member.name}) 계정이 정상적으로 삭제되었습니다."


# 휴면 회원 조회
def get_dormant_members(days: int = 90) -> list:
    """휴면 회원 조회 (마지막 로그인 이후 90일 이상 또는 회원 가입후 로그인을 하지 않은 계정은 휴면)"""
    all_members = get_all_members()
    dormant_list = []
    now = datetime.now()

    for m in all_members:
        last_login_str = m.get("last_login")

        # 1. 가입 후 한 번도 로그인하지 않은 회원
        if not last_login_str:
            m["dormant_reason"] = "로그인 기록 없음"
            dormant_list.append(m)
            continue

        # 2. 마지막 로그인일로부터 경과 일수 계산
        try:
            last_login_date = datetime.strptime(last_login_str[:10], "%Y-%m-%d")
            diff_days = (now - last_login_date).days
            if diff_days >= days:
                m["dormant_reason"] = f"{diff_days}일 동안 미접속"
                dormant_list.append(m)
        except ValueError:
            continue

    return dormant_list

