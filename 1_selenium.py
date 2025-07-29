# 구글 검색
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome() # 크롬 드라이버 실행
driver.get("https://www.google.com") # 구글 페이지 열기
search = driver.find_element("name", "q") # 검색창 찾기
search.send_keys("날씨") # 검색어 입력
search.send_keys(Keys.RETURN) # 엔터키 입력


time.sleep(5)   # 페이지 로딩 대기