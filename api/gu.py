from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import concurrent.futures
import psycopg2
from config import config

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
        items = tag.text.split(' ')[-1]
        categories_itemid[category].append(items)
print(categories_itemid)




def scraper(items_cate_id):
    pre_path = 'https://www.gu-global.com/tw/zh_TW/search.html?description='
    driver = webdriver.Chrome(executable_path=Chrome_driver_path, chrome_options=chrome_options)
    path = pre_path + items_cate_id[1]
    print(items_cate_id[1])
    driver.get(path)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, features='html.parser')

    category = items_cate_id[0]
    itemId = items_cate_id[1]
    itemuId = ''
    title = ''
    color = []
    print('now at' , path)
    for tag1 in soup.find_all('div',['class','h-product h-product-gu']):
        for tag2 in tag1.find_all('a',['class','product-herf']):
            path = GU_index_path + str(tag2['href'])
            driver.get(path)
            itemuId = path.split('=')[-1]
            print('now at page', path)
            time.sleep(3)

            # 開始商品類別爬蟲
            soup = BeautifulSoup(driver.page_source, features='html.parser')

            # 找 title
            for tag in soup.find_all('div',['class','gu-product-detail-list-title']):
                title = str(tag.text)

            # 找顏色
            for tag1 in soup.find_all('ul',['class','h-clearfix sku-select-colors']):
                for tag2 in tag1.find_all('li'):
                    for tag3 in tag2.find_all('img'):
                        if 'chip' in str(tag3):
                            # EXAMPLE = "https://www.gu-global.com/tw/hmall/test/u0000000004875/chip/22/GCL08.jpg"
                            # 從代碼去map顏色名稱即可
                            color_id = str(tag3['src']).split('/')[-1].replace('GCL','').replace('.jpg','')
                            color.append(color_id)

            # 找價格
            for tag1 in soup.find_all('div',['class','detail-list-price-main']):
                for tag2 in tag1.find_all('span',['class','h-currency bold']):
                    price =  str(tag2.text).replace('NT$', '').replace(',','')
    print(items, 'thread_end at')
    print(title,category , itemId, itemuId, price)
    print(color_id)
    sqls = []
    insert_into_item_sql = "INSERT INTO ITEM(itemid, itemuid, title, category, colorcode) VALUES ('{}','{}','{}','{}',{})".\
        format(itemId, itemuId, title, category, color_id)
    insert_into_price_sql = "INSERT INTO PRICE(itemid, price) VALUES ('{}','{}')".\
        format(itemId, price)
    sqls.append(insert_into_price_sql)
    sqls.append(insert_into_item_sql)
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for sql in sqls:
            cur.execute(sql)
            conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

items_cate_id = []
for category in categories_itemid:
    for items in categories_itemid[category]:
        items_cate_id.append([category, items])

print(items_cate_id)
start_time = time.time()  # 開始時間
print('START')
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(scraper, items_cate_id)
end_time = time.time()
print(f"{end_time - start_time} 秒爬取 {len(categories_itemid)} 類")


