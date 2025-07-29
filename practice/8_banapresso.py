import time
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

banapresso_url = 'https://www.banapresso.com/home'
google_api_key = 'AIzaSyBsYZTPY7U17V1J6k1Wu0iYC36F2vh5hMQ'

def get_banapresso_stores():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(banapresso_url)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    # 메뉴 클릭 (매장찾기 메뉴로 이동)
    menu_button = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#wrap > header > div > ul > li:nth-child(3) > a')))
    menu_button.click()
    time.sleep(3)

    # 매장 리스트 영역 로딩 확인
    store_list = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.store_shop_list')))
    
    # 스크롤 30번 반복하여 모든 매장 로딩
    for i in range(30):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", store_list)
        time.sleep(2) 
    
    print("스크롤 완료, 데이터 추출 시작")

    name_list = []
    addr_list = []
    lat_list = []
    lng_list = []

    # BeautifulSoup으로 전체 HTML 파싱
    req = driver.page_source
    soup = BeautifulSoup(req, "html.parser")
    stores = soup.find('div', 'StoreMapStyles__SearchResult-sc-nclvjx-5 eECfsK store_shop_list').find_all('span', 'store_name_map')

    for store in stores:
        store_name = store.find('i').text
        store_addr = store.find('span').text
        name_list.append(store_name)
        addr_list.append(store_addr)
    print("매장명 및 주소 추출 완료")
    driver.quit()

    # 위도/경도 변환 (Geocoding API)
    for addr in addr_list:
        try:
            google_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={addr}&key={google_api_key}"
            resp_data = requests.get(google_url).json()
            if resp_data['status'] == 'OK' and resp_data['results']:
                lat = resp_data['results'][0]['geometry']['location']['lat']
                lng = resp_data['results'][0]['geometry']['location']['lng']
                lat_list.append(lat)
                lng_list.append(lng)
            else:
                lat_list.append(None)
                lng_list.append(None)
        except Exception as e:
            print(f"좌표 변환 오류: {e}")
            lat_list.append(None)
            lng_list.append(None)
        time.sleep(0.5)
    print("위도/경도 변환 완료")

    # 데이터프레임 및 CSV 저장
    df = pd.DataFrame({
        '매장명': name_list,
        '주소': addr_list,
        '위도': lat_list,
        '경도': lng_list
    })
    print("데이터프레임 생성 완료")

    df.to_csv("banapresso_stores.csv", index=False, encoding="utf-8-sig")
    print("CSV 저장 완료!")

if __name__ == "__main__":
    get_banapresso_stores()
