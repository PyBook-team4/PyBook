# utils/visualizer.py
# 독서 기록 시각화 (matplotlib)
import platform
from collections import Counter

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator

# 막대는 한 가지 색으로 통일하고, 글자/축/격자는 옅은 회색 계열로 처리
BAR_COLOR = "#2a6fdb"
TEXT_COLOR = "#333333"
MUTED_COLOR = "#888888"
GRID_COLOR = "#e5e5e5"


def _set_korean_font():
    """운영체제에 맞는 한글 폰트 설정 (matplotlib 기본 폰트는 한글이 □로 깨짐)"""
    candidates = {
        "Darwin": ["AppleGothic", "Apple SD Gothic Neo"],   # Mac
        "Windows": ["Malgun Gothic"],                        # Windows (맑은 고딕)
    }.get(platform.system(), []) + ["NanumGothic", "Noto Sans CJK KR"]

    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False   # 한글 폰트에서 마이너스(-) 기호 깨짐 방지


def _month_range(first: str, last: str) -> list[str]:
    """'2026-08' ~ '2026-10' 사이의 모든 월 목록 (책을 안 읽은 달도 0권으로 표시하기 위해)"""
    year, month = map(int, first.split("-"))
    last_year, last_month = map(int, last.split("-"))

    months = []
    while (year, month) <= (last_year, last_month):
        months.append(f"{year}-{month:02d}")
        month += 1
        if month > 12:
            year, month = year + 1, 1
    return months


def _style_axis(ax, grid_axis: str):
    """축 꾸미기: 위/오른쪽 테두리 제거, 격자는 옅게, 막대보다 뒤에 표시"""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID_COLOR)
    ax.tick_params(colors=MUTED_COLOR)
    ax.grid(axis=grid_axis, color=GRID_COLOR, linewidth=1)
    ax.set_axisbelow(True)


def show_reading_charts(timeline: list[dict], user_name: str) -> bool:
    """
    독서 연대기 그래프 창 띄우기 (창을 닫으면 프로그램으로 돌아옴)
    - 왼쪽: 월별 완독 권수 / 오른쪽: 장르별 완독 권수
    - timeline: my_loan_service.get_reading_timeline() 결과
    - 반환값: 그래프를 띄웠으면 True
    """
    returned_months = [item["returned_at"][:7] for item in timeline if item.get("returned_at")]
    if not returned_months:
        print("\n그래프로 표시할 독서 기록이 없습니다.")
        return False

    _set_korean_font()

    # 1. 월별 완독 권수 (첫 달 ~ 마지막 달까지 빠진 달 없이)
    month_counts = Counter(returned_months)
    months = _month_range(min(month_counts), max(month_counts))
    month_values = [month_counts.get(m, 0) for m in months]
    month_labels = [f"{m[:4]}.{m[5:]}" for m in months]   # "2026.10"

    # 2. 장르별 완독 권수 (많이 읽은 장르가 위로 오도록)
    genre_counts = Counter(item.get("genre") or "기타" for item in timeline).most_common()
    genres = [g for g, _ in reversed(genre_counts)]
    genre_values = [c for _, c in reversed(genre_counts)]

    fig, (ax_month, ax_genre) = plt.subplots(1, 2, figsize=(11, 4.8))
    fig.suptitle(f"{user_name} 님의 독서 연대기 (총 {len(timeline)}권 완독)", fontsize=14, color=TEXT_COLOR)

    # 왼쪽: 월별 세로 막대
    bars = ax_month.bar(month_labels, month_values, color=BAR_COLOR, width=0.6)
    ax_month.bar_label(bars, labels=[str(v) if v else "" for v in month_values], padding=3, color=TEXT_COLOR)
    ax_month.set_title("월별 완독 권수", color=TEXT_COLOR, loc="left")
    ax_month.set_ylim(0, max(month_values) + 1)
    ax_month.yaxis.set_major_locator(MaxNLocator(integer=True))   # 권수는 정수만 표시
    _style_axis(ax_month, grid_axis="y")

    # 오른쪽: 장르별 가로 막대
    bars = ax_genre.barh(genres, genre_values, color=BAR_COLOR, height=0.6)
    ax_genre.bar_label(bars, padding=3, color=TEXT_COLOR)
    ax_genre.set_title("장르별 완독 권수", color=TEXT_COLOR, loc="left")
    ax_genre.set_xlim(0, max(genre_values) + 1)
    ax_genre.xaxis.set_major_locator(MaxNLocator(integer=True))
    _style_axis(ax_genre, grid_axis="x")

    fig.tight_layout()
    try:
        plt.show()   # 창을 닫을 때까지 여기서 기다림
    except Exception as e:
        print(f"\n[오류] 그래프 창을 열 수 없습니다: {e}")
        return False
    finally:
        plt.close(fig)
    return True