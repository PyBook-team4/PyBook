#services/analytics_service.py
from utils.file_handler import load_json, save_json
from datetime import datetime

def get_tier_info_by_point(point: int) -> dict:
    """포인트 기반 등급 계산 헬퍼 함수"""
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
    elif point >= 100:
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


def show_reading_king(top_n: int = 3) -> list:
    """
    회원들의 독서 횟수를 집계하여 상위 다독왕 순위를 출력하고 반환하는 함수
    - top_n: 출력할 상위 인원수 (기본값 3명)
    - 반환값: 정렬된 랭킹 리스트 (list)
    """
    print("\n=== 🏆 [ 이달의 다독왕 랭킹 ] 🏆 ===")

    # 회원 목록과 대출 목록 불러오기
    members = load_json('data/members.json')
    loans = load_json('data/loans.json')

    if not members:
        print("등록된 회원 정보가 없습니다.")
        print("====================================")
        return []

    ranking_list = []

    # 전체 회원을 한 명씩 돌면서 읽은 책 권수 세기
    for member in members:
        member_id = member.get("user_id")
        read_count = 0
        
        for loan in loans:
            # 대출 기록에서 user_id가 일치하고, 반납이 완료된 경우에 1권씩 추가 (== 비교 사용)
            if loan.get("user_id") == member_id and loan.get("status") != "대출중":
                read_count += 1

        # 회원의 현재 포인트 기반 등급 산출
        point = member.get("point", 0)
        tier_info = get_tier_info_by_point(point)

        ranking_list.append({
            "name": member.get("name", "이름없음"),
            "email": member.get("email"),
            "tier": tier_info["tier"],
            "count": read_count
        })

    # 읽은 권수('count')를 기준으로 내림차순 정렬
    sorted_ranking = sorted(ranking_list, key=lambda x: x["count"], reverse=True)

    medals = ["🥇 1위", "🥈 2위", "🥉 3위"]

    # 상위 top_n명 화면에 출력
    for i, user in enumerate(sorted_ranking[:top_n]):
        rank_str = medals[i] if i < 3 else f"   {i + 1}위"
        print(f"{rank_str} | {user['name']}님 ({user['tier']}) - 총 {user['count']}권 완독")

    print("====================================")
    return sorted_ranking