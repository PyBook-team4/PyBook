# services/loan_service.py
from datetime import datetime, timedelta
from models.loan import Loan
from utils.file_handler import load_json, save_json

'''
해당 파일 구현 시 members,books,records 부분을 모두 접근해야 하기 때문에 난이도가 높을 수 있습니다.
우선 코드 구현 후 테스트 할 경우 books.json에 더미데이터 한개 생성 후 테스트하면 됩니다.

'''

# 1. 대출 등급 및 등급 별 대출 권한 (이름 변경 가능)
#    ├─ beginner - 대출 가능 권수: 2권 / 대출 기한: 7일  / 달성 필요 점수: 없음(40점 이상)
#    ├─ runner   - 대출 가능 권수: 4권 / 대출 기한: 14일 / 달성 필요 점수: 없음(100점 이상)
#    ├─ leader   - 대출 가능 권수: 6권 / 대출 기한: 21일 / 달성 필요 점수: 없음(200점 이상)
#    └─ master   - 대출 가능 권수: 8권 / 대출 기한: 30일 / 달성 필요 점수: 없음(400점 이상)
# 2. 포인트 기준:
#    ├─ 도서 대출 정상 반납시 포인트 +10
#    ├─ 평점 기록시, +3
#    ├─ 리뷰 작성시 +7
#    └─ 도서 반납 지연시, 지연 1일당 -1 (0 이하로 내려가지 않음)

# 파일 경로 정의
MEMBER_FILE  = "data/members.json"
BOOKS_FILE   = "data/books.json"
LOANS_FILE   = "data/loans.json"
RECORDS_FILE = "data/records.json"

# 대출 등급 정의
LOAN_TIER = {
    "beginner" : {"max_books" : 2, "loan_days" : 7},
    "runner"   : {"max_books" : 4, "loan_days" : 14},
    "leader"   : {"max_books" : 6, "loan_days" : 21},
    "master"   : {"max_books" : 8, "loan_days" : 30},
}



#도서 대출
def borrow(member_id: str | int, book_id: int) -> bool:
    """도서 대출: 재고 확인 후 대출 기록 생성 및 재고 감소"""
    # 1. 도서 존재 여부 및 대출 가능 재고 확인 (books.json 접근)
    # 2. 새로운 loan_id 생성     (loans.json 접근)
    # 3. 새 대출 객체 생성 및 추가  
    # 4. 재고 감소 (available_stock - 1)    (books.json 접근)
    # 5. json 파일 저장 (loans.json 접근)

    # 접근 데이터 한번에 호출
    members_data = load_json(MEMBER_FILE) # 회원 정보 접근
    books_data = load_json(BOOKS_FILE)    # 책 정보 접근
    loans_data = load_json(LOANS_FILE)    # 대출 정보 접근

    target_member = "" # 대출 신청 회원 찾기용도

    # 회원 정보에서 대출 신청한 회원 찾기
    for member in members_data:
        if member.get("member_id") == member_id:
            target_member = member
            break
    if not target_member:
        print(f"일치하는 회원 id가 없습니다.")
        return False

    # 찾은 회원 정보(등급, 대출 권한) 가져오기
    user_tier = target_member.get("tier", "beginner") # 유저 등급 
    tier_info = LOAN_TIER.get(user_tier, LOAN_TIER["beginner"]) # 티어 권한 
    max_books = tier_info["max_books"] # 등급별 최대 대출 권수
    loan_days = tier_info["loan_days"] # 등급별 대출 기한 

    current_loan_count = 0 # 현재 대출 권수

    for loan in loans_data: # 대출 기록에서 target_member가 일치하는지 확인
        is_same_member = loan.get("member_id") == target_member.get("member_id") # is_same_member: 대출 신청 회원과 회원 목록 중 회원 일치 여부
        if is_same_member and loan.get("status") == "대출중": # 회원이 일치하고, 대출중이면 현재 대출권수 1씩 증가
            current_loan_count += 1
            if current_loan_count >= max_books:
                print("대출 한도를 초과했습니다.")
                return False

    target_book = "" # 대출 책 찾기용도

    for book in books_data: # 책 정보 중 대출 책 찾기
        if book.get("id") == book_id:
            target_book = book
            break
        if not target_book or target_book.get("available_stock", 0) <= 0: # 대출 요청 책이 없거나, 대출 권수가 0이하면 대출 거부 안내
            print("해당 도서는 대출이 불가능합니다.")
            return False

    existing_loan_ids = [loan.get("loan_id") for loan in loans_data] # 기존 대출 기록에서 loan_id 가져오기
    if existing_loan_ids: # 기존 대출 기록이 존재하면 새로운 loan_id는 기존 loan_id 최대값 + 1
        new_loan_id = max(existing_loan_ids) + 1 
    else:
        new_loan_id = 1 # 첫 대출일 경우 loan_id는 1로 설정

    # 새로운 대출 기록 생성
    new_loan = Loan(
        loan_id=new_loan_id,
        member_id=target_member.get("member_id"),
        book_id=target_book.get("id"),
        loan_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        return_date=(datetime.now() + timedelta(days=loan_days)).strftime("%Y-%m-%d %H:%M:%S"),
        status="대출중"
    )

    

#도서 반납
def return_book(loan_id: int) -> bool:
    """도서 반납: 대출 상태 변경, 재고 복구 및 포인트 적립"""
    # 1. 대출 상태 및 반납일 업데이트
    # 2. 해당 도서 재고 복구 (available_stock + 1)
    # 3. 반납 보상 포인트 지급 (예: 반납 시 10 포인트 적립)  members.json 접근
    # 4, 리뷰, 평점 남길 시 (예: 10포인트 추가 적립)        records.json 접근
    # 5. 파일 저장
    pass




# models/loan.py
from datetime import datetime, timedelta


# 1. 대출 등급 및 등급 별 대출 권한
#    ├─ beginner - 대출 가능 권수: 2권 / 대출 기한: 7일  / 달성 필요 점수: 없음(40점 이상)
#    ├─ runner   - 대출 가능 권수: 4권 / 대출 기한: 14일 / 달성 필요 점수: 없음(100점 이상)
#    ├─ leader   - 대출 가능 권수: 6권 / 대출 기한: 21일 / 달성 필요 점수: 없음(200점 이상)
#    └─ master   - 대출 가능 권수: 8권 / 대출 기한: 30일 / 달성 필요 점수: 없음(400점 이상)
# 2. 포인트 기준:
#    ├─ 도서 대출 정상 반납시 포인트 +10
#    ├─ 평점 기록시, +3
#    ├─ 리뷰 작성시 +7
#    └─ 도서 반납 지연시, 지연 1일당 -1 (0 이하로 내려가지 않음)



class Loan:
    def __init__(self, 
                loan_id: int,               # 대출 고유 번호?
                member_id: str | int,       # 회원 id
                book_id: int,               # 책 고유 번호?
                loan_date: str = None,      # 대출일
                due_date: str = None,       # 반납 기준일
                return_date: str = None,    # 반납일
                status: str = "대출중"       # 대출 상태
                ):
        self.loan_id = loan_id
        self.member_id = member_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status

    def to_dict(self) -> dict:
        """객체를 JSON 저장을 위한 딕셔너리로 변환"""
        return {
            "loan_id": self.loan_id,
            "member_id": self.member_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date,
            "due_date": self.due_date,
            "return_date": self.return_date,
            "status": self.status

        }

    @classmethod
    def from_dict(cls, data: dict):
        """JSON 딕셔너리를 Loan 객체로 생성"""
        return cls(
            loan_id = data["loan_id"],
            member_id = data["member_id"],
            book_id = data["book_id"],
            loan_date = data["loan_date"],
            due_date = data["due_date"],
            return_date = data["return_date"],
            status = data["status"]
        )