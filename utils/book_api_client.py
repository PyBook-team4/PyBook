# utils/book_api_client.py
import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv
from typing import Union    
# .env 파일에서 환경변수 로드
load_dotenv(dotenv_path=".env")

class BookClient:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API 키를 불러오지 못했습니다. .env 파일을 확인해주세요.")
        
        self.url = "https://www.nl.go.kr/NL/search/openApi/search.do"

    def search_book(self, keyword: str, page_size: int = 5) -> dict|str: 
       #  API 요청 파라미터 구성 // 나중에 요청사항에 맞게 파라미터 받는형식으로 변경해야함
        params = {
            "key": self.api_key,
            "kwd": keyword,
            "category": "도서",
            "apiType": "json",
            "srchTarget": "total",
            "pageSize": page_size,
            "pageNum": 1
        }
        
        # 쿼리 스트링 조합
        query_string = urllib.parse.urlencode(params)
        full_url = f"{self.url}?{query_string}"
        
        try:
            # 불필요한 헤더와 SSL 예외 처리 제거 후 단순 호출
            with urllib.request.urlopen(full_url, timeout=15) as response:
                response_data = response.read().decode('utf-8')
                return json.loads(response_data)
                
        except Exception as e:
            return f"API 통신 오류: {e}"



#mac 환경에서 api 호출이 안 되는 경우가 생겨 임시 코드로 우선 주석처리해놨습니다.
'''
import os
import json
import urllib.request
import urllib.parse
import ssl
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv(dotenv_path=".env")

class BookClient:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API 키를 불러오지 못했습니다. .env 파일을 확인해주세요.")
        
        self.url = "https://www.nl.go.kr/NL/search/openApi/search.do"

    def search_book(self, keyword:str, page_size:int=5)->dict|str:
        # 1. API 요청 파라미터 구성 // 나중에 요청사항에 맞게 파라미터 받는형식으로 변경해야함
        params = {
            "key": self.api_key,
            "kwd": keyword,
            "category": "도서",
            "apiType": "json",
            "srchTarget": "total",
            "pageSize": page_size,
            "pageNum": 1
        }
        
        # 딕셔너리를 URL 쿼리 문자열(예: key=...&kwd=...)로 안전하게 변환
        query_string = urllib.parse.urlencode(params)
        full_url = f"{self.url}?{query_string}"
        
        # 2. 완벽한 일반 브라우저 위장 (User-Agent 및 Accept 헤더 추가)
        # 현재 코드 작업중 request error 부분 해결하기 위한 임시조치
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01"
        }
        
        # 3. 맥(macOS) 환경의 SSL 인증서 에러를 무시하는 설정
        # 현재 코드 작업중 request error 부분 해결하기 위한 임시조치
        context = ssl._create_unverified_context()
        
        try:
            # 4. 통신 요청 객체 생성 및 호출
            req = urllib.request.Request(full_url, headers=headers)
            with urllib.request.urlopen(req, context=context, timeout=15) as response:
                
                # 받아온 바이트 데이터를 문자열(utf-8)로 디코딩
                response_data = response.read().decode('utf-8')
                
                # JSON 문자열을 파이썬 딕셔너리로 변환하여 반환
                return json.loads(response_data)
                
        except Exception as e:
            return f"API 통신 오류: {e}"
'''

"""주석 처리
# ==========================================
# 단독 실행 테스트 블록
# ==========================================
if __name__ == "__main__":
    print("--- 국립중앙도서관 API 연동 테스트 시작 (urllib 순정 모듈) ---")
    try:
        client = BookClient()
        print(f"API 키 로드 성공: {client.api_key[:4]}********")
        
        test_keyword = "토지"
        print(f"'{test_keyword}' 도서 검색 중...")
        
        result = client.search_book(test_keyword, page_size=1)
        
        print("\n[응답 데이터 확인]")
        print("-" * 50)
        if isinstance(result, dict):
            #깔끔하게 출력
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(result)
        print("-" * 50)
        
    except Exception as e:
        print(f"실행 중 에러가 발생했습니다: {e}")

        """
