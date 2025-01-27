import os
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

from src.config.config import ROOT_PATH
from src.util import seler, acer

url = 'https://www.spiderbuf.cn/playground/e04'
driver = seler.init_driver(url, no_headless=True, keep_open=True)

# 等待初始页面加载
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table'))
)

# 获取总页数
page_buttons = driver.find_elements(By.CSS_SELECTOR, 'ul.pagination > li > a')
total_pages = len(page_buttons) - 1

data = [['排名', '企业估值（亿元）', '企业信息', 'CEO', '行业']]

for page_num in range(1, total_pages + 1):
    print(f'正在解析第 {page_num} 页...')
    try:
        # 点击分页按钮
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//a[@class="item" and text()="{page_num}"]'))
        )
        driver.execute_script("arguments[0].click();", button)

        # 等待数据刷新
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table tbody tr'))
        )

        # 解析数据
        soup = BeautifulSoup(driver.page_source, 'lxml')
        rows = [[td.text.strip() for td in tr.select('td')] for tr in soup.select('table.table > tbody > tr')]
        data += rows

    except StaleElementReferenceException:
        print(f"第 {page_num} 页元素失效，重试中...")
        # 重新获取按钮
        button = driver.find_element(By.XPATH, f'//a[@class="item" and text()="{page_num}"]')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)
        continue
    except Exception as e:
        print(f'解析第 {page_num} 页时失败: {e}')

file_path = os.path.join(ROOT_PATH, 'store', 'e04.csv')
acer.save_csv(data, file_path)

driver.quit()