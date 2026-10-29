# services/my_loan_service.py
# 마이페이지: 나의 독서 연대기 / 현재 대출 현황 조회
from datetime import datetime

from utils.file_handler import load_json
from services.loan_service import get_tier_info_by_point

LOANS_FILE = "data/loans.json"
BOOKS_FILE = "data/books.json"
RECORDS_FILE = "data/records.json"


def _find_record(records: list, loan: dict) -> dict | None:
    """대출 기록에 해당하는 평점/리뷰 기록 찾기"""
    # loan_id가 저장된 기록이면 loan_id로 정확히 찾음
    for r in records:
        if r.get("loan_id") == loan.get("loan_id"):
            return r

    # loan_id가 없는 기존 기록은 같은 회원 + 같은 책 + 반납한 날짜에 작성된 기록으로 찾음
    returned_day = (loan.get("return_date") or "")[:10]
    for r in records:
        if (r.get("loan_id") is None
                and r.get("user_id") == loan.get("user_id")
                and r.get("book_id") == loan.get("book_id")
                and r.get("created_at", "")[:10] == returned_day):
            return r
    return None


def get_reading_timeline(user_id: int) -> list[dict]:
    """
    나의 독서 연대기: 반납 완료한 도서를 반납일 순서대로 반환
    - 각 항목: 도서 정보 + 대출일/반납일 + 남긴 평점/리뷰
    """
    loans = load_json(LOANS_FILE)
    books = load_json(BOOKS_FILE)
    records = load_json(RECORDS_FILE)
    book_map = {b.get("id"): b for b in books}

    timeline = []
    for loan in loans:
        if loan.get("user_id") != user_id or loan.get("status") != "반납완료":
            continue

        book = book_map.get(loan.get("book_id"), {})
        record = _find_record(records, loan)
        timeline.append({
            "loan_id": loan.get("loan_id"),
            "title": book.get("title", "알 수 없는 도서"),
            "author": book.get("author", "저자 미상"),
            "genre": book.get("genre", "기타"),
            "loan_date": loan.get("loan_date"),
            "returned_at": loan.get("return_date"),   # 반납완료 기록의 return_date는 실제 반납일
            "rating": record.get("rating") if record else None,
            "review": record.get("review") if record else "",
        })

    # 반납일 기준 오래된 순서로 정렬 (연대기)
    timeline.sort(key=lambda item: item["returned_at"] or "")
    return timeline


def get_current_loan_status(user_id: int, point: int) -> dict:
    """
    도서 대출 현황: 현재 대출 중인 도서 목록과 남은 일수, 등급별 대출 한도 반환
    - remaining_days: 양수면 남은 일수, 0이면 오늘까지, 음수면 연체 일수
    """
    loans = load_json(LOANS_FILE)
    books = load_json(BOOKS_FILE)
    book_map = {b.get("id"): b for b in books}
    today = datetime.now().date()

    current_loans = []
    for loan in loans:
        if loan.get("user_id") != user_id or loan.get("status") != "대출중":
            continue

        # due_date가 없는 기존 데이터는 return_date에 반납기한이 들어있음
        due_str = loan.get("due_date") or loan.get("return_date")
        remaining_days = None
        if due_str:
            try:
                due_day = datetime.strptime(due_str[:10], "%Y-%m-%d").date()
                remaining_days = (due_day - today).days
            except ValueError:
                pass

        book = book_map.get(loan.get("book_id"), {})
        current_loans.append({
            "loan_id": loan.get("loan_id"),
            "title": book.get("title", "알 수 없는 도서"),
            "author": book.get("author", "저자 미상"),
            "loan_date": loan.get("loan_date"),
            "due_date": due_str,
            "remaining_days": remaining_days,
        })

    # 반납기한이 가까운 순서로 정렬
    current_loans.sort(key=lambda item: item["due_date"] or "")

    tier_info = get_tier_info_by_point(point)
    return {
        "loans": current_loans,
        "tier": tier_info["tier"],
        "max_books": tier_info["max_books"],
        "loan_days": tier_info["loan_days"],
    }