import os
import sys
import time

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
    
    # GOODBYE 아스키 아트
    goodbye_art = [
        "  ██████╗  ██████╗  ██████╗ ██████╗ ██████╗ ██╗   ██╗███████╗",
        " ██╔════╝ ██╔═══██╗██╔═══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝",
        " ██║  ███╗██║   ██║██║   ██║██║  ██║██████╔╝ ╚████╔╝ █████╗  ",
        " ██║   ██║██║   ██║██║   ██║██║  ██║██╔══██╗  ╚██╔╝  ██╔══╝  ",
        " ╚██████╔╝╚██████╔╝╚██████╔╝██████╔╝██████╔╝   ██║   ███████╗",
        "  ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝"
    ]
    
    COLOR_GREEN = "\033[92m"
    COLOR_RESET = "\033[0m"
    
    print("\n\n")
    for line in goodbye_art:
        print(f"{COLOR_GREEN}{line}{COLOR_RESET}")
        time.sleep(0.1) # 시작할 때보다 살짝 빠르게 슉슉 나타납니다
        
    print("\n")
    
    closing_msg = "PyBook을 이용해 주셔서 감사합니다. 즐거운 독서 되세요!"
    for char in closing_msg:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
        
    print("\n\n")
    time.sleep(1.5) # 마지막 인사를 읽을 수 있게 잠시 멈춤
    clear_screen()  # 마지막으로 터미널을 깔끔하게 지우고 프로그램 완전 종료

# ==========================================
# 메인 프로그램 시작 지점
# ==========================================
def main():
    show_intro_animation()
    
    while True:
        print("====================================")
        print("        PyBook Main Menu        ")
        print("====================================")
        print("1. 회원가입")
        print("2. 로그인")
        print("3. 관리자 로그인")
        print("4. 프로그램 종료")
        print("====================================")
        
        choice = input("원하시는 메뉴 번호를 입력하세요: ")
        
        if choice == '4':
            # 💡 기존 단순 print문을 지우고 종료 애니메이션 함수 호출
            show_goodbye_animation()
            break
        else:
            print("\n준비 중인 기능입니다...\n")
            time.sleep(1)
            clear_screen() # 다른 메뉴를 눌렀다 돌아올 때도 화면을 깔끔하게 유지

if __name__ == "__main__":
    main()