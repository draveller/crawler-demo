from io import BytesIO

import chardet
import requests as req
from bs4 import BeautifulSoup
from openpyxl.drawing.image import Image

from util import acer

"""
带iframe的页面源码分析及数据爬取
"""

# 目标 URL
target_url = 'https://www.spiderbuf.cn/playground/s06'

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# 发送请求
response = req.get(target_url, headers=headers)
response.encoding = chardet.detect(response.content)['encoding']
if response.status_code != 200:
    print('请求失败, 结果:', response)
    exit()

base_location = 'https://www.spiderbuf.cn'
soup = BeautifulSoup(response.text, 'lxml')
iframe_src = soup.select_one('iframe')['src']
real_url = base_location + iframe_src

real_res = req.get(real_url, headers=headers)
response.encoding = chardet.detect(response.content)['encoding']
if response.status_code != 200:
    print('请求失败, 结果:', response)
    exit()

soup = BeautifulSoup(real_res.text, 'lxml')

head_row = [e.text for e in soup.select_one('body > table > thead > tr').select('th')]
body_rows = [[t.text for t in e.select('td')] for e in soup.select('body > table > tbody > tr')]

# 创建 Excel 文件并写入图片
file_path = '../store/practice.xlsx'
sheet_name = 'practice_s6'

data = [head_row] + body_rows
acer.save(data, file_path, sheet_name)
