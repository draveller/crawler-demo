import os
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from src.config.config import ROOT_PATH
from src.util import seler, acer

"""
使用代理ip
"""

url = 'https://www.spiderbuf.cn/playground/e04'
# 这里的代理ip不好用, 暂时注释了
# proxy = proxy_pool.pop()
# proxy_url = f'{'https' if proxy['https'] else 'http'}://{proxy['proxy']}'
# print('proxy_url', proxy_url)
# args = ['--proxy-server=' + proxy_url]
# driver = seler.init_driver(url, no_headless=True, keep_open=True, args=args)
driver = seler.init_driver(url, no_headless=True, keep_open=True)

# 时停等文档加载
WebDriverWait(driver, 10).until(
    lambda d: d.execute_script('return document.readyState') == 'complete')
print(driver.page_source)

page_buttons = driver.find_elements(By.CSS_SELECTOR, 'ul.pagination > li > a')

data = [['排名', '企业估值（亿元）', '企业信息', 'CEO', '行业']]
for i, page_button in enumerate(page_buttons):
    if i == len(page_buttons) - 1:
        break
    print(f'正在解析第 {i + 1} 页...')
    try:
        driver.execute_script("arguments[0].click();", page_button)

        # page_button.click()
        time.sleep(.5)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        data += ([[td.text for td in tr.select('td')] for tr in soup.select('table.table > tbody > tr')])
    except Exception as e:
        print(f'解析第 {i + 1} 页时失败, 错误 = {e}')

file_path = os.path.join(ROOT_PATH, 'store', 'e04.csv')
acer.save_csv(data, file_path)
