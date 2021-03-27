import time
import pyperclip as pyperclip
from datetime import datetime
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#time.sleep(600)
id_file_nm = 'gs_ids.ini'
id_list = []
url_naver_serch = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%B2%9C%ED%95%98%EC%A0%9C%EC%9D%BC+%EA%B1%B0%EC%83%81&oquery=%EA%B1%B0%EC%83%81&tqi=hvV4Elp0YidssmhszRwssssstAC-231111'
url_login = 'http://www.gersang.co.kr/pub/logi/login/login.gs?returnUrl=www%2Egersang%2Eco%2Ekr%2Fpub%2Fmemb%2Fsecu%2Fquie%2Egs%3F'
url_check = 'http://www.gersang.co.kr/event/' + str(datetime.now().year) + '/' + str(datetime.now().year) + str(
    datetime.now().month).zfill(2) + '01_attendance/main.gs'
enc_key = b'NaFu0Jx5tASx9YWr5NHfe9ts-KLhN7HoCF48Uo63Zrw='
global driver

# 아이디 목록 파일 불러오기
file = open(id_file_nm, 'r')
line = file.readline()
while line != '':
    temp = line.split('/')
    tmp_dic = {}
    tmp_dic.setdefault('id', temp[0])
    # 복호화
    decrypt = Fernet(enc_key).decrypt(temp[1].encode())
    tmp_dic.setdefault('pw', decrypt.decode())
    id_list.append(tmp_dic)
    line = file.readline()
file.close()


# print(id_list)


# 거상 로그인
def login(login_id, login_pw):
    # 거상 로그인 열기
    driver.get(url_login)

    # id, pw 입력할 곳을 찾습니다.
    # tag_id = driver.find_element_by_name('GSuserID')
    tag_id = driver.find_element_by_xpath(
        '/html/body/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr/td[3]/input')
    tag_pw = driver.find_element_by_xpath(
        '/html/body/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td/table/tbody/tr/td[3]/input')
    tag_id.clear()
    time.sleep(1)

    # id 입력
    tag_id.click()
    #pyperclip.copy(login_id)
    #tag_id.send_keys(Keys.CONTROL, 'v')
    tag_id.send_keys(login_id)
    time.sleep(1)

    # pw 입력
    tag_pw.click()
    #pyperclip.copy(login_pw)
    #tag_pw.send_keys(Keys.CONTROL, 'v')
    tag_pw.send_keys(login_pw)
    time.sleep(1)

    # 로그인 버튼을 클릭합니다
    driver.find_element_by_xpath(
        '/html/body/table/tbody/tr/td[2]/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[3]/input').click()

    # 슬립을 꼭 넣어줘야 한다.
    # 그렇지 않으면 로그인 끝나기도 전에 다음 명령어가 실행되어 제대로 작동하지 않는다.
    time.sleep(3)

    # 거상 출석체크 페이지 이동
    driver.get(url_check)
    time.sleep(3)
    # 네이버 검색 팝업 클리
    driver.find_element_by_xpath('//*[@id="popup"]/div[1]/a/img').click()
    time.sleep(1)
    # 시간에 따른 출석 체크 버튼 클릭
    #    시간 대     class_name
    # 00:05~05:55 = btn_11
    # 06:05~11:55 = btn_12
    # 12:05~17:55 = btn_13
    # 18:05~23:55 = btn_14
    HM_time = datetime.now().time().strftime("%H%M")
    if '0005' < HM_time < '0555':
        driver.find_element_by_class_name('btn_11').click()
    elif '0605' < HM_time < '1155':
        driver.find_element_by_class_name('btn_12').click()
    elif '1205' < HM_time < '1755':
        driver.find_element_by_class_name('btn_13').click()
    elif '1805' < HM_time < '2355':
        driver.find_element_by_class_name('btn_14').click()
    else:
        print('미정의 시간 630초 후 재실행')
        return True

    time.sleep(2)
    # alet 창 제거
    alert = driver.switch_to.alert
    if alert.text == '이미 아이템을 수령하셨습니다.':
        return True

    alert.accept()
    time.sleep(2)
    # 로그아웃 버튼 클릭
    driver.find_element_by_xpath(
        '//*[@id="navi"]/table/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr/td[3]/a/img').click()
    time.sleep(2)
    return False


#####################################################################
while True:
    #time.sleep(630)
    tt = int(datetime.now().time().strftime("%M"))
    print(tt)
    if 55 <= tt:
        time.sleep(66-tt)
    elif tt <= 5:
        time.sleep(6-tt)

    coptions = webdriver.ChromeOptions()
    coptions.add_argument('headless')
    coptions.add_argument('window-size=1920x1080')
    coptions.add_argument("disable-gpu")
    coptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36")
    coptions.add_argument("lang=ko_KR")
    driver = webdriver.Chrome('chromedriver', options=coptions)

    # 네이버 '거상' 검색 한 주소
    driver.get(url_naver_serch)
    time.sleep(3)
    # 거상 링크 클릭
    driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div[2]/div[1]/div/div[2]/dl/div[5]/dd/a').click()
    time.sleep(3)
    ###################
    for Tid in id_list:
        if login(Tid.get("id"), Tid.get("pw")):
            print('이미 아이템을 수령하셨습니다.' + '[' + str(datetime.now()) + ']')
            break
        print(str(datetime.now()) + ":" + Tid.get("id"))
    driver.quit()
    time.sleep(7200)
