"""
使用chardet自动检测编码
使用requests发送HTTP请求
使用BeautifulSoup解析HTML页面
"""

import chardet
import requests as req
from bs4 import BeautifulSoup

from src.util import acer

target_url = 'https://www.spiderbuf.cn/playground/s01'

response = req.get(target_url)
response.encoding = chardet.detect(response.content)['encoding']

soup = BeautifulSoup(response.text, 'lxml')
head = soup.select_one('thead').select_one('tr')
body = soup.select_one('tbody').select('tr')

# 列表推导式:
head_texts = [e.text for e in head.select('th')]
body_texts_rows = [[e.text for e in row.select('td')] for row in body]

# 存入 ./store/practice.xlsx 的名为 'practice_s1' 的sheet页
data_2d = [head_texts] + body_texts_rows
acer.save(data_2d, '../../store/practice.xlsx', 'practice_s1')
