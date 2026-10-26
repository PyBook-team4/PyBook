# animations/animation_effect.py
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