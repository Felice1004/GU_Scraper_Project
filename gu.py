from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import json
import sys
import requests
import selenium
from bs4 import BeautifulSoup
import json
import time
import threading
import concurrent.futures



 # 設定selenium
Chrome_driver_path = 'chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    'User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"')
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(
    executable_path=Chrome_driver_path, chrome_options=chrome_options)
# driver.maximize_window()  # 最大化視窗

categories = {'coat':'大衣・風衣',
                'jacket':'外套・夾克・外搭背心',
                'parka':'連帽外套',
                'cardigan':'開襟外套'}
pre_path = 'https://www.gu-global.com/tw/zh_TW/women_'
suf_path = '.html'
GU_index_path = 'https://www.gu-global.com'

categories_itemid = {}
for category in categories:
    path = pre_path + category + suf_path
    driver.get(path)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, features='html.parser')
    for tag in soup.find_all('div',['class','font-p-gu']):
        if category not in categories_itemid:
            categories_itemid[category] = []
        item_id = tag.text.split(' ')[-1]
        categories_itemid[category].append(item_id)

# print(categories_itemid)

def scraper(item_id):
    pre_path = 'https://www.gu-global.com/tw/zh_TW/search.html?description='
    driver = webdriver.Chrome(executable_path=Chrome_driver_path, chrome_options=chrome_options)
    driver.get(pre_path + item_id)
    print('now at page',pre_path + item_id)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, features='html.parser')
    for tag1 in soup.find_all('div',['class','h-product h-product-gu']):
        for tag2 in tag1.find_all('a',['class','product-herf']):
            path = GU_index_path + str(tag2['href'])
            driver.get(path)
            print('now at page', path)
            time.sleep(3)

            # 開始商品類別爬蟲
            title = ''
            img = {}
            color = {}
            test_result = ''
            soup = BeautifulSoup(driver.page_source, features='html.parser')

            # 找 title
            for tag in soup.find_all('div',['class','gu-product-detail-list-title']):
                # print(tag.text)
                test_result = test_result + str(tag.text) + ' '

            # 找img
            for tag in soup.find_all('img',['class','sku-img']):
                break
                # print(tag['src'])

            # 找顏色
            for tag1 in soup.find_all('ul',['class','h-clearfix sku-select-colors']):
                for tag2 in tag1.find_all('li'):
                    for tag3 in tag2.find_all('img'):
                        if 'chip' in str(tag3):
                            # 從代碼去map顏色名稱即可
                            # print(tag3) 
                            break

            # 找價格
            for tag1 in soup.find_all('div',['class','detail-list-price-main']):
                for tag2 in tag1.find_all('span',['class','h-currency bold']):
                    # print(tag2.text)
                    test_result = test_result + str(tag2.text)
    print(test_result)
    print('thread_end at', item_id)

item_ids = []
for category in categories_itemid:
    for item_id in categories_itemid[category]:
            item_ids.append(item_id)

start_time = time.time()  # 開始時間
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(scraper, item_ids)
end_time = time.time()
print(f"{end_time - start_time} 秒爬取 {len(categories_itemid)} 類")


# todo -  item ids 是純id 這樣無法記錄類別 除非另外爬
