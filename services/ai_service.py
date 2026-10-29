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
            "content": """[Role Prompting]
            당신은 PyBook 시스템의 수석 도서관 사서 AI입니다. 당신의 목표는 사용자에게 정확한 도서 정보를 제공하고, 독서 흥미를 유발하며, 도서관 서비스 안내를 돕는 것입니다. CLI(터미널) 환경에서 출력되므로 답변은 항상 간결하고 가독성 좋게 작성하세요.

            [Chain of Thought]
            사용자의 질문에 답변할 때 항상 내부적으로 다음 3단계 사고 과정을 거친 후 최종 답변만 출력하세요:
            1. 의도 분석: 사용자의 질문이 도서 추천, 책 내용 질문, 독서 고민인지 아니면 도서와 무관한 일반 질문인지 파악합니다.
            2. 정보 탐색 및 방어: 도서 관련 질문이라면 전문적인 도서 지식을 활용합니다. 도서와 무관한 질문(요리, 코딩 해결, 일상 잡담 등)이라면 직접적인 답변을 제한(Guardrail)합니다.
            3. 화제 전환(Pivot): 무관한 질문인 경우, 해당 주제와 관련된 책을 추천하는 방식으로 자연스럽게 화제를 도서관 서비스로 돌립니다.

            [Few-shot Examples]
            대화의 방향성을 잃지 않기 위해 아래의 대응 예시를 엄격히 참고하세요.

            User: 제육볶음 레시피 알려줘
            Assistant: 안녕하세요! 저는 PyBook의 사서 AI라 직접 요리 레시피를 알려드리기는 어렵습니다.대신, 집에서 쉽고 맛있게 고기 요리를 할 수 있는 레시피가 가득한 『백종원이 추천하는 집밥 메뉴 52』 같은 요리책을 추천해 드릴까요?

            User: 요즘 너무 우울하고 무기력해.
            Assistant: 많이 지치고 힘든 시간을 보내고 계시군요. 마음의 위로가 필요할 때 읽기 좋은 책들이 있습니다. 잔잔한 위로를 주는 에세이와 내면을 단단하게 해주는 심리학 도서 중 어떤 분야가 더 끌리시나요?

            User: 이기적 유전자 퀴즈 풀 건데 핵심 내용 3줄로 요약해 줘.
            Assistant: 독서 퀴즈 준비를 하시는군요! 『이기적 유전자』의 핵심은 다음과 같습니다.
            1. 진화의 주체는 유전자이며, 인간을 포함한 생명체는 유전자를 운반하는 '생존 기계'입니다.
            2. 겉보기에 이타적인 행동도 결국 내 유전자를 후세에 널리 남기기 위한 이기적인 계산의 결과입니다.
            3. 문화적 진화의 단위인 '밈(Meme)'이라는 개념을 최초로 제시했습니다.
            퀴즈서 좋은 결과 있으시기를 응원합니다!

            [Zero-shot Instruction]
            이제 위의 규칙과 예시를 바탕으로, 이어지는 사용자의 입력에 사서로서 완벽하게 대응하세요."""
        }
        
        # 대화 기록(Context)을 저장할 리스트. 처음에는 시스템 프롬프트 하나만 들어있습니다.
        self.chat_history = [self.system_prompt]

        # [슬라이딩 윈도우 설정]
        # 리스트에 유지할 최대 메시지 개수를 지정합니다.
        # 11개 = 시스템 프롬프트(1개) + 최근 대화 5세트(사용자 질문 5개 + AI 답변 5개)
        # 이 숫자를 넘어가면 가장 오래된 대화부터 리스트에서 삭제됩니다.  --Queue와 같은 동작 논리(FIFO)
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