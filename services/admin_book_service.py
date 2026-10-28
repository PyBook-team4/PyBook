#services/admin_book_service.py
from datetime import datetime
from models.book import Book
from utils.file_handler import load_json, save_json
# 관리자 메뉴
# 새로운 도서 등록
def register_book(title: str, author: str, publisher:str, genre: str, isbn: str,total_stock: int, available_stock:int) -> bool:
    """ 새로운 도서 등록 """
    # 도서 목록 불러오기
    books = load_json("data/books.json")

    # 1. 도서 목록 중복 검사 # 제목으로 비교한 뒤 이미 존재한다면 False 반환
    for search_book in books:
            if search_book["title"] == title.strip():
                print("이미 등록된 도서입니다.")
                return False

    # 2. 도서 id 생성 
    book_ids = [book["id"] for book in books] # 도서 목록에서 id만 추출
    
    if book_ids:  # id가 있다면 최대값에 +1 / 없다면 1을 도서 id로 지정
        new_book_id = max(book_ids) + 1
    else:
        new_book_id = 1

    # 3. total_stock 검증 # 0 ~ 10의 범위만 가능 
    if total_stock < 1 or total_stock > 10:
        print("도서 최대 보유량은 0 ~ 10의 범위 내로 입력해주세요.")
        return False

    # 4. available_stock 검증 # 0보다 작거나 total_Stock보다 클 수 없음
    if available_stock < 0 or available_stock > total_stock:
        print("현재 도서 재고는 음수이거나 최대 보유량을 넘을 수 없습니다.")
        return False

    # 5. 새로운 도서 등록일 생성
    book_datetime = datetime.now()
    book_date = book_datetime.strftime("%Y-%m-%d")

    # 6. 새로운 객체 생성 및 추가
    new_book = Book(
        id=new_book_id,
        title=title,
        author=author,
        publisher=publisher,
        genre=genre,
        isbn=isbn,
        rating=3.0,     #기본 평점은 3.0
        total_stock=total_stock,
        available_stock=available_stock,
        reg_date=book_date
    )

    books.append(new_book.to_dict())
    
    # 7. json 파일 저장 하고 성공 메세지 출력
    save_json("data/books.json", books) 
    print(f"'{title}' 도서가 성공적으로 등록되었습니다.")
    return True

# 도서 삭제
def book_delete(book_id: int) -> bool:
    """ 도서 삭제 """
    # 도서 목록 불러오기
    books = load_json("data/books.json")
    
    # 1. 입력받은 도서id로 일치하는 도서 찾기
    for book in books:
        # 일치하는 도서가 있는 경우
        if book["id"] == book_id:
            print("일치하는 도서를 찾았습니다.")
            # 성공 메세지를 위한 값 저장 
            deleted_id = book["id"]
            deleted_title = book["title"]

            # 전체 도서목록에서 찾은 도서 삭제
            books.remove(book)
            # 수정된 목록을 JSON 파일에 저장
            save_json("data/books.json",books)
            # 성공 메세지와 True 반환 
            print(f"id: {deleted_id} | '{deleted_title}' 도서가 삭제되었습니다.")
            return True

    # 일치하는 도서가 없는 경우 메세지 출력후 False 반환
    print("일치하는 도서가 없습니다.")
    return False


# 도서 정보 수정
# id는 고유 등록 번호 / reg_date는 최초 등록일이라 수정에서 제외 
# book_id: 수정할 책의 id 
# field_choice: 수정할 정보 유형 선택 
# new_value: 수정할 내용 (새로 집어 넣을 값)
def book_update(book_id: int, field_choice: int, new_value) -> bool:
    """ 도서 정보 수정 """
    # 도서 목록 불러오기
    books = load_json("data/books.json")

    # 수정할 정보 유형 번호 목록 
    field_map = {
        1: "title",
        2: "author",
        3: "publisher",
        4: "isbn",
        5: "genre",
        6: "rating",
        7: "total_stock",
        8: "available_stock"
    }

    target_book = None # 수정할 도서의 정보 저장 변수 (dict)

    # field_choice 검증
    # field_choice가 1-8값이 아닐 경우(field_map에 없는 숫자인 경우)
    if field_choice not in field_map:
        print("잘못된 수정 항목입니다.")
        return False

    # 수정할 내용이 빈 열 인지 확인 
    if not new_value.strip():
        # 빈 열이라면 False
        print("수정할 값은 비워둘 수 없습니다.")
        return False 

    new_value = new_value.strip()

    for book in books:
        # 일치하는 도서가 있는 경우
        if  book["id"] == book_id:
            target_book = book
            break
            
    # 일치하는 도서가 없는 경우        
    if target_book is None:    
        print("일치하는 도서가 없습니다.")
        return False

    

    # 사용자가 6: 평점을 선택했을 경우 new_value를 float로 변환
    if field_choice == 6:
        try:
            new_value = float(new_value)
        except ValueError:
            print("평점은 숫자여야 합니다.")
            return False
    elif field_choice in (7, 8):
        try:
            new_value = int(new_value)
        except ValueError:
            print("재고 수량은 정수여야 합니다.")
            return False

    if field_choice == 6 and not 0.0 <= new_value <= 5.0:
        print("평점은 음수이거나 5.0을 초과할 수 없습니다.")
        return False

    if field_choice == 6:
        try:
            new_value = float(new_value)
        except ValueError:
            print("평점은 숫자여야 합니다.")
            return False
    elif field_choice in (7, 8):
        try:
            new_value = int(new_value)
        except ValueError:
            print("재고 수량은 정수여야 합니다.")
            return False
        
    # 도서 정보에서 수정할 부분을 field에 저장
    field = field_map[field_choice]
    # 수정할 도서에 정보 일부분을 새로운 값으로 수정
    target_book[field] = new_value

    save_json("data/books.json", books) 
    print(f"id: {book_id} 도서의 {field}가 수정되었습니다.")
    return True
