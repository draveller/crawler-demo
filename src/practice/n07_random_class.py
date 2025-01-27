import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from src.config.config import ROOT_PATH
from src.util import seler, acer

"""
随机类名
"""

url = 'https://www.spiderbuf.cn/playground/n07'
driver = seler.init_driver(url)

# 等待文档页面加载
WebDriverWait(driver, 10).until(
    lambda d: d.execute_script('return document.readyState') == 'complete')

# 获取总页数
data = [['序号', '分类', '题干']]
content = driver.find_element(By.CSS_SELECTOR, 'body > main > div:nth-child(2)').text

last_valid = False
double_lines = []
for line in content.split('\n'):
    is_index_line = line.split('.')[0].isdigit()
    if is_index_line:
        double_lines.append(line)
        last_valid = True
    if not is_index_line and last_valid:
        double_lines.append(line)
        last_valid = False

[print(line) for line in double_lines]

data += [x.split('. ') + [y] for x, y in zip(double_lines[::2], double_lines[1::2])]

file_path = os.path.join(ROOT_PATH, 'store', 'n07.csv')
acer.save_csv(data, file_path)
