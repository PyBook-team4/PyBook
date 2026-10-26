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
    members_data = load_json("data/members.json") # 회원 정보 접근
    books_data   = load_json("data/books.json")   # 책 정보 접근
    loans_data   = load_json("data/loans.json")   # 대출 정보 접근

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
        loan_id     = new_loan_id,
        member_id   = target_member.get("member_id"),
        book_id     = target_book.get("id"),
        loan_date   = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        return_date = (datetime.now() + timedelta(days=loan_days)).strftime("%Y-%m-%d %H:%M:%S"),
        status      = "대출중"
    )

    
#도서 반납
def return_book(loan_id: int) -> bool:
    """도서 반납: 대출 상태 변경, 재고 복구 및 포인트 적립"""
    # 1. 대출 상태 및 반납일 업데이트
    # 2. 해당 도서 재고 복구 (available_stock + 1)
    # 3. 반납 보상 포인트 지급 (예: 반납 시 10 포인트 적립)  members.json 접근
    # 4, 리뷰, 평점 남길 시 (예: 10포인트 추가 적립)        records.json 접근
    # 5. 파일 저장
    
    # 접근 데이터 한번에 호출
    members_data = load_json("data/members.json") # 회원 정보 접근
    books_data   = load_json("data/books.json")   # 책 정보 접근
    loans_data   = load_json("data/loans.json")   # 대출 정보 접근
    records_data = load_json("data/records.json") # 리뷰, 평점 기록 접근    

    for check_loan in loans_data: # 대출 기록에서 대출 정보 확인
        if check_loan.get("loan_id") == loan_id:
            check_loan["status"] = "반납완료" # 대출 상태 변경
            check_loan["return_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 반납일 업데이트

            # 해당 도서 재고 복구
            for book in books_data:                             # 책 정보에서 대출한 책 찾기
                if book.get("id") == check_loan.get("book_id"): # 대출한 책과 일치하는 책 찾기
                    book["available_stock"] += 1                # 재고 복구(+1)
                    break

            # 반납 보상 포인트 지급 (예: 반납 시 10 포인트 적립)
            target_member = None
            for member in members_data:
                if member.get("member_id") == check_loan.get("member_id"):
                    target_member = member
                    member["point"] += 10
                    break

            # 평점 작성 및 포인트 지급
            rating = None
            rating_input = input("도서 평점을 남기시겠습니까? (1~5점) ").strip()
            if rating_input.isdigit() and 1 <= int(rating_input) <= 5:
                rating = int(rating_input)
                if target_member:
                    target_member["point"] += 3
                print(f"평점 {rating}점이 등록되었습니다. (+3 포인트)")

            # 리뷰 작성 및 포인트 지급
            review = ""
            review_input = input("도서 감상평(리뷰)을 남기시겠습니까? ").strip()
            if review_input:
                review = review_input
                if target_member:
                    target_member["point"] += 7
                print("리뷰 작성이 완료되었습니다. (+7 포인트)")

            # 평점이나, 리뷰 중 하나라도 작성했다면, records.json에 기록
            if review is not None or review:
                # 새로운 record_id 채번 (기존 최대값 + 1, 없으면 1001)
                existing_record_ids = [r.get("record_id", 0) for r in records_data]
                new_record_id = max(existing_record_ids) + 1 if existing_record_ids else 1001

                new_record = {
                    "record_id": new_record_id,
                    "member_id": check_loan.get("member_id"),
                    "book_id": check_loan.get("book_id"),
                    "rating": rating,
                    "review": review,
                    "created_at": datetime.now().strftime("%Y-%m-%d")
                }
                records_data.append(new_record)

            # 파일 저장
            save_json("data/members.json", members_data)
            save_json("data/books.json", books_data)
            save_json("data/loans.json", loans_data)
            save_json("data/records.json", records_data)

            return True


