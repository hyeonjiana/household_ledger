from fileCheck import vertify_file

#주 프롬프트 :
SEPERATOR = '--------------------------------------------------------------'

def print_mainPrompt():
    print('=주 프롬프트=\n')
    print('[지출] [수입] [조회]\n[편집] [저장] [로그아웃]\n')
    choice = input("메뉴를 입력하세요: ")
    print(SEPERATOR)
    return choice

def callFunc(c):
    if(c == '지출'):
        print('지출함수')
        #지출 함수
    elif(c == '수입'):
        print('수입함수')
        #수입 함수
    elif(c == '조회'):
        print('조회함수')
        #조회 함수
    elif(c == '편집'):
        print('편집함수')
        #편집 함수
    elif(c == '저장'):
        print('저장함수')
        #저장 함수
        while(vertify_file()) : pass
    elif(c == '로그아웃'):
        print('로그아웃함수')
        return -1
        #로그아웃 함수(메인메뉴로 돌아감)
    

def mainPrompt():
    while(1):
        c = print_mainPrompt()
        check = callFunc(c)
        if check == -1: 
            return -1     


