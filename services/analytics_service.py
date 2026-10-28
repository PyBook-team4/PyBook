from models.book import Book
from utils.book_api_client import BookClient
from utils.file_handler import load_json, save_json


def show_reading_king(top_n: int = 5) -> list:
    """
    회원들의 독서 횟수를 집계하여 상위 다독왕 순위를 출력하고 반환하는 함수
    - top_n: 출력할 상위 인원수 (기본값 5명)
    - 반환값: 정렬된 랭킹 리스트 (list)
    """
    print("\n=== 🏆 [ 이달의 다독왕 랭킹 ] 🏆 ===")

    # 회원 목록과 대출 목록 불러오기.
    members = load_json('data/members.json')
    loans = load_json('data/loans.json')

    # 회원들의 독서 횟수를 담을 리스트.
    ranking_list = []

    # 전체 회원을 한 명씩 돌면서 읽은 책 권수 세기
    for member in members:

        # 회원이 독서한 책 개수를 세는 변수
        read_count = 0
        
        for loan in loans:
            # 대출 기록에서 user_id가 일치하고, 반납이 완료된 경우에 1권씩 추가
            if loan.get("user_id") in member.get("user_id") and loan.get("status") != "대출중":
                read_count += 1

        # 랭킹 리스트에 해당 회원의 정보와 읽은 권수를 딕셔너리로 추가
        ranking_list.append({
            "name": member.get("name", "이름없음"),
            "email": member.get("email"),
            "tier": member.get("tier", "일반"),
            "count": read_count
        })

    # 읽은 권수('count')를 기준으로 내림차순 정렬.
    sorted_ranking = sorted(ranking_list, key=lambda x: x["count"], reverse=True)

    # 상위 top_n명 화면에 출력.

    # 없는 경우의 "예외 처리"
    if not sorted_ranking:
        print("등록된 회원 정보가 없습니다.")
        return []

    medals = ["🥇 1위", "🥈 2위", "🥉 3위"]

    # [:top_n] 슬라이싱으로 상위 5명까지만 잘라서 반복
    for i, user in enumerate(sorted_ranking[:top_n]):
        # 1~3위는 메달 표시, 4위부터는 '4위', '5위'로 표시
        rank_str = medals[i] if i < 3 else f"   {i + 1}위"
        print(f"{rank_str} | {user['name']}님 ({user['tier']}) - 총 {user['count']}권 완독")

    print("====================================")
    return sorted_ranking