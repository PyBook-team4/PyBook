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


#TODO 개발자들 엔딩 크래딧