import time
import sys
import itertools

def show_spinner(message, duration=3):
    """API 응답을 기다릴 때 쓰기 좋은 회전 애니메이션"""
    # 콘솔에서 부드럽게 돌아가는 특수문자 조합
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']) 
    
    end_time = time.time() + duration
    while time.time() < end_time:
        # \r을 사용해 맨 앞으로 이동한 뒤 덮어쓰기
        sys.stdout.write(f"\r{next(spinner)} {message}...")
        sys.stdout.flush() # 화면에 즉시 글자를 쏘아주는 역할
        time.sleep(0.1)    # 0.1초 대기 (애니메이션 속도)
        
    # 로딩이 끝나면 성공 메시지로 덮어쓰기 (남은 잔상을 지우기 위해 끝에 공백 추가)
    sys.stdout.write(f"\r✅ {message} 완료!                    \n")

def show_progress_bar(message, total_steps=30):
    """파일 저장이나 다량의 데이터를 처리할 때 쓰기 좋은 진행률 바"""
    for i in range(total_steps + 1):
        percent = int(i / total_steps * 100)
        
        # █ (채워짐)과 ░ (비어있음) 기호를 조합하여 바 모양 생성
        filled = '█' * i
        empty = '░' * (total_steps - i)
        
        sys.stdout.write(f"\r{message} |{filled}{empty}| {percent}%")
        sys.stdout.flush()
        time.sleep(0.05)
        
    print("\n✅ 동기화 완료!")

# ==========================================
# 🧪 단독 실행 테스트 블록
# ==========================================
if __name__ == "__main__":
    print("--- PyBook 동적 로딩 UI 테스트 ---\n")
    
    # 1. API 호출처럼 시간이 얼마나 걸릴지 모를 때 (스피너)
    show_spinner("OpenAI에서 데미안 퀴즈를 생성하는 중", duration=3)
    
    print("-" * 50)
    
    # 2. 파일 저장/읽기처럼 진행도를 보여주고 싶을 때 (프로그레스 바)
    show_progress_bar("국립중앙도서관 데이터베이스 동기화 중", total_steps=40)