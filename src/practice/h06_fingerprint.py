import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.config.config import ROOT_PATH
from src.util import acer

"""
浏览器指纹
"""

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
driver.get('https://www.spiderbuf.cn/playground/h06')
# 等待页面加载完成
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#dataContent > thead > tr > td'))
)

elements = driver.find_elements(By.CSS_SELECTOR, '#dataContent > thead > tr')

data = []
for element in elements:
    print(element.text)
    row = []
    for cell in element.find_elements(By.CSS_SELECTOR, 'th, td'):
        row.append(cell.text)
    data.append(row)

# 持久化存储
file_path = os.path.join(ROOT_PATH, 'store', 'practice.xlsx')
acer.save(data, file_path, 'practice_h06')

print("数据已成功保存到:", file_path)
