#services/ai_service.py
import sys
import os

# PyBook 최상위 디렉토리를 시스템 경로에 추가 (모듈 import 경로 문제 방지)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from utils.openai_client import OpenAIClient
from animations.animation_effect import typing_effect, loading_spinner


"""
챗봇에 과거 대화내역은 슬라이딩 윈도우 기법으로 저장 : 가장 오래된 대화를 순차적으로 버리고 최근 N개의 대화만 남김

but 오래된 대화가 잘려나가서 과거 문맥을 잊어버리는 것을 방지하려면
Summarization 방식: 잘려나갈 대화를 ai한테 미리 요약시키고 시스템 프롬프트에 덧붙이기
"""
#TODO Summarization방식으로 더 효과적으로 구현
class AIChatService:
    def __init__(self):
        # OpenAI API 호출을 담당하는 클라이언트 인스턴스 생성
        self.ai_client = OpenAIClient()
        
        # 시스템 프롬프트: AI의 역할과 성격, 답변 가이드라인을 설정하는 가장 중요한 메시지입니다.
        # 이 메시지는 대화가 길어지더라도 절대 삭제되지 않고 항상 유지되어야 합니다.
        self.system_prompt = {
            "role": "system", 
            "content": """당신은 PyBook의 친절하고 전문적인 도서관 사서 AI입니다. 
            사용자에게 알맞은 책을 추천하거나, 도서 관련 질문에 친절하게 답변해주세요.
            대화는 터미널(CLI) 환경에서 이루어지므로, 너무 길지 않게 핵심을 담아 명확히 답변해야 합니다."""
        }
        
        # 대화 기록(Context)을 저장할 리스트. 처음에는 시스템 프롬프트 하나만 들어있습니다.
        self.chat_history = [self.system_prompt]

        # [슬라이딩 윈도우 설정]
        # 리스트에 유지할 최대 메시지 개수를 지정합니다.
        # 11개 = 시스템 프롬프트(1개) + 최근 대화 5세트(사용자 질문 5개 + AI 답변 5개)
        # 이 숫자를 넘어가면 가장 오래된 대화부터 리스트에서 삭제됩니다.
        # Queue와 같은 동작 논리(FIFO)
        self.max_history_length = 11 

    def start_chat(self):
        """
        AI 사서와의 채팅 루프를 실행합니다.
        """
        typing_effect("[PyBook AI 사서와 대화하기]", speed=0.03)
        print("책 추천, 도서 정보, 독서 고민 등 무엇이든 물어보세요!")
        print("(채팅을 종료하려면 '종료', 'exit', 'q'를 입력하세요)")
        print("="*50)

        # 사용자가 종료를 선언하기 전까지 계속 대화를 주고받는 무한 루프입니다.
        while True:
            # strip()을 사용해 양옆의 공백이나 줄바꿈 문자를 제거합니다.
            user_input = input("\n 사용자: ").strip()
            
            # 사용자가 실수로 엔터만 친 경우, 아무 작업 없이 다시 입력을 기다립니다.
            if not user_input:
                continue
                
            # 종료 커맨드 입력 시 루프를 탈출하여 챗봇을 종료합니다.
            if user_input.lower() in ['종료', 'exit', 'q', 'quit']:
                print("\n AI 사서: PyBook AI 사서를 이용해 주셔서 감사합니다. 즐거운 독서 되세요!\n")
                
                # 다음번에 챗봇을 다시 켰을 때 이전 대화가 남아있지 않도록 기록을 초기화합니다.
                self.chat_history = [self.system_prompt]
                break
            
            # 1. 사용자 메시지를 대화 기록 리스트 마지막에 추가합니다.
            self.chat_history.append({"role": "user", "content": user_input})
            
            # ---------------------------------------------------------
            # [핵심 로직: 슬라이딩 윈도우 적용]
            # 사용자 메시지를 추가한 후, 리스트의 길이가 제한(11개)을 초과했는지 검사합니다.
            # ---------------------------------------------------------
            if len(self.chat_history) > self.max_history_length:
                # 리스트 슬라이싱(Slicing)을 이용해 오래된 대화를 잘라냅니다.
                # 
                # self.chat_history[0] : 0번 인덱스인 '시스템 프롬프트'는 무조건 가져옵니다. (AI의 자아 유지)
                # self.chat_history[-(self.max_history_length - 1):] : 
                # 리스트의 맨 뒤에서부터 10개(최대길이 11 - 시스템 1)의 메시지만 잘라서 가져옵니다.
                # 결과적으로 '시스템 프롬프트 1개 + 최근 대화 10개'의 새로운 리스트가 만들어져 덮어씌워집니다.
                self.chat_history = [self.chat_history[0]] + self.chat_history[-(self.max_history_length - 1):]
            
            loading_spinner("🤖 AI 사서가 생각 중입니다...", duration=1.5)
            
            # 2. 길이를 조절한 대화 기록을 OpenAI 클라이언트로 전송하여 AI의 응답을 받아옵니다.
            ai_response = self.ai_client.generate_chat_response(self.chat_history)
            
            # 3. 받아온 AI 응답을 화면에 출력합니다.
            print("AI 사서: ", end="")
            sys.stdout.flush()
            typing_effect(ai_response, speed=0.02)
            
            # 4. 방금 출력한 AI의 답변도 기록에 추가해야, 다음 질문 시 AI가 본인이 무슨 말을 했는지 기억할 수 있습니다.
            self.chat_history.append({"role": "assistant", "content": ai_response})
            
            # 주의: AI 답변을 append한 직후에는 최대 길이를 초과할 수 있지만(ex: 12개), 
            # 다음 루프에서 사용자가 질문을 던지고 나서 if문을 통해 다시 11개로 잘려나가므로 문제가 없습니다.

# 단독 실행 테스트용 코드
if __name__ == "__main__":
    try:
        chat_service = AIChatService()
        chat_service.start_chat()
    except Exception as e:
        print(f"\n[오류 발생] 챗봇 서비스 실행 중 문제가 발생했습니다: {e}")