import os
import sys
from pathlib import Path

# --- 설정 변수 ---
# 홈 경로 설정
HOME_DIR = Path.home()
# 사용자 정보 파일 이름
USER_INFO_FILE = "user_info.txt"
# 가계부 파일 접미사
LEDGER_FILE_SUFFIX = "_HL.txt"

def verify_files():
    # 1. 사용자 파일(user_info.txt) 존재 확인
    user_file_path = HOME_DIR / USER_INFO_FILE

    if not user_file_path.exists():
        print("!오류: 현재 사용자 파일이 존재하지 않습니다.")
        print("!오류: 프로그램이 자동으로 새로운 파일을 생성 중 입니다.")
        # 새로운 빈 파일 생성
        user_file_path.touch()
        print("프로그램이 재시작됩니다.")
        # 재시작을 위해 False 반환
        return False

    # 사용자 파일이 비어있는지 확인
    if user_file_path.stat().st_size == 0:
        # 파일은 있지만 내용이 없으면 통과 (새로 생성된 상태)
        return True
        
    # 2. 사용자 목록 읽기 및 가계부 파일 존재 확인
    try:
        with open(user_file_path, 'r', encoding='utf-8') as f:
            users = [line.strip() for line in f if line.strip()]
    except Exception as e:
        # 파일을 읽는 도중 인코딩 등 다른 문제가 발생했을 경우
        print(f"!치명적오류: {USER_INFO_FILE} 파일을 읽는 중 오류가 발생했습니다: {e}")
        print("프로그램을 종료시킵니다.")
        sys.exit()

    missing_ledger_files_exist = False
    for user in users:
        ledger_file_name = f"{user}{LEDGER_FILE_SUFFIX}"
        ledger_file_path = HOME_DIR / ledger_file_name
        if not ledger_file_path.exists():
            print("!오류: 가계부 파일이 존재하지 않습니다.")
            if not missing_ledger_files_exist:
                print("!오류: 프로그램이 자동으로 새로운 파일을 생성 중 입니다.")
                missing_ledger_files_exist = True
            # 해당 사용자의 가계부 파일 생성
            ledger_file_path.touch()
    
    if missing_ledger_files_exist:
        print("프로그램이 재시작됩니다.")
        # 재시작을 위해 False 반환
        return False

    # 3. 사용자 파일 문법 검사
    #    (예: 각 줄은 공백 없이 하나의 사용자 이름만 포함해야 함)
    for i, user in enumerate(users, 1):
        # 사용자 이름에 공백이나 쉼표가 포함된 경우 오류로 간주
        if ' ' in user or ',' in user:
            print(f"!치명적오류: 현재 {USER_INFO_FILE} {i}행에서 오류가 발생되었습니다")
            print("프로그램을 종료시킵니다.")
            sys.exit()

    # 4. 가계부 파일 문법 검사
    #    (예: 각 줄은 '날짜,카테고리,금액' 형식으로 쉼표가 2개 있어야 함)
    for user in users:
        ledger_file_name = f"{user}{LEDGER_FILE_SUFFIX}"
        ledger_file_path = HOME_DIR / ledger_file_name
        
        # 파일이 비어있으면 검사 통과
        if ledger_file_path.stat().st_size == 0:
            continue
            
        try:
            with open(ledger_file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if not line: # 빈 줄은 무시
                        continue
                    # 쉼표(,)의 개수가 2개가 아니면 문법 오류로 간주
                    if line.count(',') != 2:
                        print(f"!치명적오류: 현재 {ledger_file_name} {i}행에서 오류가 발생되었습니다.")
                        print("프로그램을 종료시킵니다.")
                        sys.exit()
        except Exception as e:
            print(f"!치명적오류: {ledger_file_name} 파일을 읽는 중 오류가 발생했습니다: {e}")
            print("프로그램을 종료시킵니다.")
            sys.exit()

    # 모든 검사를 통과하면 True 반환
    return True

if __name__ == "__main__":
    # 프로그램 시작 시 파일 무결성 검사를 반복적으로 수행
    while not verify_files():
        # verify_files()가 False를 반환하면 (재시작 필요) 루프를 다시 실행
        # 실제 프로그램에서는 이 부분에 잠시 대기(time.sleep)를 추가할 수도 있습니다.
        print("-" * 30) # 재시작 시 구분을 위한 라인

    # 무결성 검사가 최종 통과되었을 때 실행될 메인 로직
    print("\n[알림] 모든 파일의 무결성 검사를 통과했습니다. 프로그램을 시작합니다.")
    # 여기에 실제 프로그램의 메인 코드를 작성하면 됩니다.
    # 예: main_application()