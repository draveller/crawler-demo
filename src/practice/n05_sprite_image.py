import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.config.config import ROOT_PATH
from src.util import acer, ster

"""
雪碧图
"""

target_url = 'https://www.spiderbuf.cn/playground/n05'

# 配置浏览器选项
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# 启动浏览器
driver = webdriver.Chrome(options=options)

# 隐藏 webdriver 属性
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# 伪造插件列表
driver.execute_script('''
    Object.defineProperty(navigator, 'plugins', {
        get: () => [{
            description: 'PDF Viewer',
            filename: 'internal-pdf-viewer'
        }]
    })
''')

# 访问目标页面
driver.get(target_url)
soup = BeautifulSoup(driver.page_source, 'lxml')

data = [['名称', '排名', '企业估值（亿元）', 'CEO', '行业']]
sprite_map = {
    'abcdef': '0',
    'ghijkl': '1',
    'mnopqr': '2',
    'uvwxyz': '3',
    'yzabcd': '4',
    'efghij': '5',
    'klmnop': '6',
    'qrstuv': '7',
    'wxyzab': '8',
    'cdefgh': '9',
}
for element in soup.select('div.container > div.row > div'):
    name = element.select_one('h2').text
    _element_text = element.text
    rank = ster.get_middle(_element_text, '排名：', '\n')
    valuation = ''.join([sprite_map.get(e['class'][1]) for e in element.select('p > span.sprite')])
    ceo = ster.get_middle(_element_text, 'CEO：', '\n')
    industry = ster.get_middle(_element_text, '行业：', '')
    data.append([name, rank, valuation, ceo, industry])

# 持久化存储
file_path = os.path.join(ROOT_PATH, 'store', 'practice.xlsx')
acer.save(data, file_path, 'practice_n05')

print("数据已成功保存到:", file_path)
