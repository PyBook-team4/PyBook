import os
from openai import OpenAI
from dotenv import load_dotenv

# 해당 코드는 단위 테스트를 위한 코드로 test폴더에 넣기 전까지 utils/openai_client.py에서 코드돌리는경우 필요한 코드입니다 나중에 삭제할 예정입니다.
# 현재 파일(openai_client.py) 위치를 기준으로 부모 폴더(PyBook)의 .env 경로를 자동 추적
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
env_path = os.path.join(parent_dir, ".env")

load_dotenv(dotenv_path=env_path)

# 추적한 절대 경로로 환경변수 로드
#load_dotenv(dotenv_path=env_path)
#현재 개발 가이드를 위한 임시 코드 나중에 전체 수정 필요
class OpenAIClient:

    def __init__(self):
        # .env 파일에 저장된 OPENAI_API_KEY를 호출
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY가 올바르지 않습니다. env 파일을 확인해주세요.")
        
        # 클라이언트 초기화
        self.client = OpenAI(api_key=api_key)

    #ai 기반 독서 퀴즈 
    def generate_book_quiz(self, book_title):
        # GPT에게 역할을 부여하고 퀴즈 생성을 요청하는 코드
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # 추후 성능보고 다른 모델로 변경예정   //gpt4o 로 사용해도 될듯
                #프롬프트 엔지니어링 부분 추후 system에 content 부분 템플릿 양식으로 응답대신 json이나 다른형식으로 받게 할수도 있음
                messages=[
                    {
                        "role": "system", 
                        "content": """너는 PyBook 독서 퀴즈 출제 위원이야. 
                        반드시 아래의 템플릿 양식을 100% 똑같이 지켜서 응답해.
                        다른 부연 설명이나 인사말은 절대 하지 마.

                        [문제] (여기에 문제를 작성)
                        1. (보기 1)
                        2. (보기 2)
                        3. (보기 3)
                        4. (보기 4)
                        [정답] (1, 2, 3, 4 중 정답 숫자 하나만 작성)
                        [해설] (정답인 이유를 2문장 이내로 작성)"""
                        
                    },
                    
                    {"role": "user", "content": f"책 '{book_title}' 에 대한 퀴즈를 만들어줘."}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"퀴즈 생성 중 API 호출 오류가 발생했습니다: {e}"


#아래 부분 주석처리
"""
#임시 테스트 코드, 추후 테스트 폴더에서 진행
if __name__ == "__main__":
    print("--- OpenAI API 연동 테스트 시작 ---")
    try:
        #  클라이언트 생성 테스트
        ai_client = OpenAIClient()
        print("openAI 클라이언트 초기화 성공")
        
        # API 호출 테스트
        test_book = "이기적 유전자"    #임시 테스트용 추후에 사용자한테 입력받은 도서로 퀴즈 생성해야함
        print(f"\n요청 중: '{test_book}' 퀴즈 생성")
        
        quiz_result = ai_client.generate_book_quiz(test_book)

        if "[정답]" not in quiz_result:
            print("퀴즈 양식이 올바르지 않습니다. API 응답 내용:")
            print(quiz_result)
        else:
            #[정답] 을 기준으로 앞쪽 문제 부분과 뒤 정답+해설 부분으로 분리
            question_part,answer_and_explanation=quiz_result.split("[정답]")
            #[해설] 을 기준으로 앞쪽 정답 부분과 뒤 해설 부분으로 분리
            answer_part,explanation_part=answer_and_explanation.split("[해설]")

            correct_answer=answer_part.strip()
            explanation=explanation_part.strip()

        
        print("\n[테스트 결과 출력]")
        print("-" * 40)
        print(question_part.strip())
        print("-" * 40)

        user_input = input("\n정답을 입력하세요 (1~4): ").strip()
        print("\n[채점 결과]")
        print("-" * 40)
        if user_input == correct_answer:
            print("정답입니다!")
        else:
            print(f"오답입니다. (정답: {correct_answer}번)")
        print(f"\n해설: {explanation}")
        print("-" * 40)


        
    except ValueError as ve:
        print(f"\n[설정 오류] {ve}")
    except Exception as e:
        print(f"\n[테스트 실패] {e}")

        """