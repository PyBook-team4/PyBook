# utils/file_handler.py
import json
import os

def load_json(filename):
    """JSON 파일을 읽어 리스트 데이터로 반환"""
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"파일을 불러오는 중 오류 발생 ({filename}): {e}")
    return []

def save_json(filename, data_list):
    """데이터 리스트를 JSON 파일에 저장"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"파일을 저장하는 중 오류 발생 ({filename}): {e}")