import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def human_type(element, text, min_delay=0.1, max_delay=0.3):
    for ch in text:
        element.send_keys(ch)
        time.sleep(random.uniform(min_delay, max_delay))

INSTAGRAM_ID   = 'shguswl826@naver.com'
INSTAGRAM_PW   = '123123123!!'
HASHTAG        = '바다'
COMMENT_TEXT   = '바다 예쁘다'

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-notifications")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/114.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(options=options)
wait   = WebDriverWait(driver, 15)

# 1) 로그인
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(3)
id_input = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
pw_input = driver.find_element(By.NAME, 'password')
human_type(id_input, INSTAGRAM_ID)
time.sleep(0.5)
human_type(pw_input, INSTAGRAM_PW)
pw_input.send_keys(Keys.RETURN)
time.sleep(5)

# 2) 팝업 자동 닫기
for txt in ("나중에 하기", "Not Now", "나중에"):
    try:
        btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//button[text()='{txt}']")))
        btn.click()
        time.sleep(2)
    except:
        pass

# 3) 해시태그 페이지 열기
driver.get(f"https://www.instagram.com/explore/tags/{HASHTAG}/")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
time.sleep(4)

# 4) 게시물 목록에서 랜덤 선택
posts = wait.until(EC.presence_of_all_elements_located((
    By.CSS_SELECTOR, "article a[href*='/p/']"
)))
post = random.choice(posts)
driver.execute_script("arguments[0].scrollIntoView();", post)
time.sleep(1)
post.click()
wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
time.sleep(3)

# 5) 좋아요 클릭
like_btn = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    "//svg[@aria-label='좋아요']/ancestor::button"
)))
ActionChains(driver).move_to_element(like_btn).click().perform()
time.sleep(2)

# 6) 댓글 작성
comment_box = wait.until(EC.presence_of_element_located((
    By.XPATH, "//textarea[@aria-label='댓글 달기...']"
)))
driver.execute_script("arguments[0].scrollIntoView({block:'center'});", comment_box)
ActionChains(driver).move_to_element(comment_box).click().perform()
time.sleep(1)
human_type(comment_box, COMMENT_TEXT, 0.1, 0.2)
comment_box.send_keys(Keys.RETURN)
time.sleep(3)

driver.quit()
