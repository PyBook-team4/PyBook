# animations/animation_effect.py
import os
import sys
import time
import itertools

def clear_screen():
    """운영체제에 맞게 콘솔 화면을 깨끗하게 지웁니다."""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_intro_animation():
    """PYBOOK 시작 애니메이션"""
    clear_screen()
    
    logo = [
        "██████╗ ██╗   ██╗██████╗  ██████╗  ██████╗ ██╗  ██╗",
        "██╔══██╗╚██╗ ██╔╝██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝",
        "██████╔╝ ╚████╔╝ ██████╔╝██║   ██║██║   ██║█████╔╝ ",
        "██╔═══╝   ╚██╔╝  ██╔══██╗██║   ██║██║   ██║██╔═██╗ ",
        "██║        ██║   ██████╔╝╚██████╔╝╚██████╔╝██║  ██╗",
        "╚═╝        ╚═╝   ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝"
    ]
    
    COLOR_CYAN = "\033[96m"
    COLOR_YELLOW = "\033[93m"
    COLOR_RESET = "\033[0m"
    
    print("\n\n")
    for line in logo:
        print(f"{COLOR_CYAN}{line}{COLOR_RESET}")
        time.sleep(0.15)
        
    print("\n")
    
    welcome_msg = "나만의 AI 도서관, PyBook 시스템을 초기화합니다..."
    sys.stdout.write(COLOR_YELLOW)
    for char in welcome_msg:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
        
    sys.stdout.write(COLOR_RESET + "\n")
    time.sleep(1.5)
    clear_screen()

def show_goodbye_animation():
    """프로그램 종료 애니메이션"""
    clear_screen()
    
    goodbye_art = [
        "  ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗",
        " ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝",
        " ██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗  ",
        " ██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝  ",
        " ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗",
        "  ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝"
    ]
    
    COLOR_GREEN = "\033[92m"
    COLOR_RESET = "\033[0m"
    
    print("\n\n")
    for line in goodbye_art:
        print(f"{COLOR_GREEN}{line}{COLOR_RESET}")
        time.sleep(0.1)
        
    print("\n")
    
    closing_msg = "PyBook을 이용해 주셔서 감사합니다. 즐거운 독서 되세요!"
    for char in closing_msg:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
        
    print("\n\n")
    time.sleep(1.5)
    clear_screen()


#ai chatbot관련 애니메이션 함수들 
def typing_effect(text, speed=0.03):
    """
    텍스트를 한 글자씩 타이핑하듯 출력하는 애니메이션 효과입니다.
    speed 값을 조절하여 타이핑 속도를 변경할 수 있습니다.
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print() # 마지막에 줄바꿈 추가

def loading_spinner(text="로딩 중...", duration=2.0):
    """
    터미널용 텍스트 스피너(| / - \\) 애니메이션입니다.
    """
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    end_time = time.time() + duration
    
    while time.time() < end_time:
        sys.stdout.write(f'\r{text} {next(spinner)}')
        sys.stdout.flush()
        time.sleep(0.1)
        
    # 로딩이 끝나면 해당 줄을 지우고 완료 상태로 덮어씁니다.
    sys.stdout.write('\r' + ' ' * (len(text) + 5) + '\r')
    sys.stdout.flush()

def connecting_ai_animation():
    """
    AI 챗봇 메뉴 진입 시 전용 연결 애니메이션입니다.
    """
    clear_screen()
    print("\n" + "="*40)
    typing_effect("PyBook 서버와 통신 중...", speed=0.05)
    loading_spinner("AI 사서 모듈을 불러오는 중", duration=1.5)
    typing_effect("연결 완료! AI 사서를 호출합니다.", speed=0.04)
    print("="*40 + "\n")
    time.sleep(0.5)



#TODO 국립중앙도서 api호출하는 동안 스피너 생성 admin_view에 연결하기
def run_with_spinner(text, func, *args, **kwargs):
    """
    func(*args, **kwargs)를 실행하는 "동안" 스피너를 보여주고, 끝나면 func의 결과를 그대로 반환합니다.
    - loading_spinner()는 정해진 시간(duration)만큼만 돌지만,
      이 함수는 API 호출처럼 끝나는 시간을 모르는 작업이 실제로 끝날 때까지 돌아갑니다.
    - 작업은 별도 스레드에서 실행하고, 메인 스레드는 그동안 스피너를 그립니다.
    - 작업 중 예외가 발생하면 스피너를 지운 뒤 같은 예외를 다시 발생시킵니다.
    """
    import threading

    outcome = {}                                    # 스레드에서 실행한 결과/예외를 담아올 상자

    def worker():
        try:
            outcome["result"] = func(*args, **kwargs)
        except Exception as e:                      # 예외는 여기서 잡아두고 메인 스레드에서 다시 발생
            outcome["error"] = e

    thread = threading.Thread(target=worker, daemon=True)   # daemon: 프로그램 종료 시 같이 종료
    thread.start()

    spinner = itertools.cycle(['|', '/', '-', '\\'])
    start = time.time()
    # 작업이 끝날 때까지 + 너무 빨리 끝나도 최소 0.6초는 보여줘서 깜빡임 방지
    while thread.is_alive() or time.time() - start < 0.6:
        sys.stdout.write(f'\r{text} {next(spinner)}')
        sys.stdout.flush()
        time.sleep(0.1)

    # 스피너 줄 지우기
    sys.stdout.write('\r' + ' ' * (len(text) * 2 + 5) + '\r')
    sys.stdout.flush()

    if "error" in outcome:
        raise outcome["error"]
    return outcome.get("result")

#TODO 개발자들 엔딩 크래딧



# ==========================================
# 단독 실행 테스트: run_with_spinner 동작 확인
#   - 프로젝트 폴더(PyBook)에서 실행:  python3 -m animations.animation_effect
# ==========================================
if __name__ == "__main__":

    # [테스트 1] 3초 걸리는 가짜 작업 → 3초 동안 스피너가 돌고, 끝나면 결과 반환
    def slow_task(seconds):
        time.sleep(seconds)                 # API 응답을 기다리는 상황을 흉내냄
        return f"{seconds}초 걸리는 작업 완료!"

    print("[테스트 1] 3초짜리 작업")
    result = run_with_spinner("⏳ 작업을 처리하고 있습니다...", slow_task, 3)
    print(f"결과: {result}\n")

    # [테스트 2] 작업 중 오류 → 스피너가 지워진 뒤 같은 오류가 그대로 전달되는지 확인
    def failing_task():
        time.sleep(1.5)
        raise ValueError("일부러 발생시킨 오류")

    print("[테스트 2] 작업 중 오류 발생")
    try:
        run_with_spinner("⚠️ 오류가 나는 작업을 실행하고 있습니다...", failing_task)
    except ValueError as e:
        print(f"오류를 정상적으로 전달받음: {e}\n")

    # [테스트 3] 실제 국립중앙도서관 API 검색 (응답이 오는 순간 스피너가 멈춤)
    #   - 프로젝트 폴더에서 "python3 -m animations.animation_effect"로 실행해야 services를 불러올 수 있음
    print("[테스트 3] 국립중앙도서관 API 검색")
    try:
        from services.book_service import search_books_by_keyword
        start = time.time()
        books = run_with_spinner("📚 국립중앙도서관에서 '코스모스'를 검색하고 있습니다...",
                                 search_books_by_keyword, "코스모스", page_size=5)
        print(f"{time.time() - start:.1f}초 만에 {len(books)}권 검색 완료")
        for book in books:
            print(f"  - {book['title']} / {book['author']} / {book['publisher']}")
    except ImportError:
        print("services를 불러올 수 없습니다. 프로젝트 폴더에서 'python3 -m animations.animation_effect'로 실행해주세요.")
    except ValueError as e:
        print(f"API 키 오류: {e}")