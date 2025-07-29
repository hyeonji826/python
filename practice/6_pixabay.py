import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient

def crawl_pixabay_images(keyword='cat', max_page=2, scroll_count=5):
    img_list = []
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(options=options)
    
    base_url = f'https://pixabay.com/ko/images/search/{keyword}/'
    
    for page in range(1, max_page + 1):
        url = base_url if page == 1 else base_url + f'?pagi={page}'
        print(f'페이지 {page} 크롤링...')
        driver.get(url)
        time.sleep(2)
        for _ in range(scroll_count):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(1.2)
        imgs = driver.find_elements(By.XPATH, '//img[contains(@src, "cdn.pixabay.com")]')
        print(f'  => 픽사베이 썸네일 {len(imgs)}개')
        for img in imgs:
            img_url = img.get_attribute('src')
            alt_text = img.get_attribute('alt')
            img_dict = {
                'img_url': img_url,
                'alt_text': alt_text,
                'page': page,
                'keyword': keyword
            }
            img_list.append(img_dict)
    driver.quit()
    return img_list

db_url = 'mongodb+srv://apple:P3YcAAsodfOE6TOB@cluster0.tlpvsg7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(db_url)
database = client['pixabay']         
collection = database['img']         

# MongoDB 저장
pixabay_imgs = crawl_pixabay_images(keyword='cat', max_page=2, scroll_count=4)
print(f'총 {len(pixabay_imgs)}개 크롤링 완료!')

inserted, skipped = 0, 0
for img in pixabay_imgs:
    if not collection.find_one({'img_url': img['img_url']}):
        collection.insert_one(img)
        inserted += 1
    else:
        skipped += 1
print(f'>> MongoDB 저장 완료: {inserted}개 (중복 {skipped}개 제외)')
