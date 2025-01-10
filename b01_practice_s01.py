import chardet
import pandas as pd
import requests as req
from bs4 import BeautifulSoup

target_url = 'https://www.spiderbuf.cn/playground/s01'

response = req.get(target_url)
response.encoding = chardet.detect(response.content)['encoding']

soup = BeautifulSoup(response.text, 'lxml')
head = soup.select_one('thead').select_one('tr')
body = soup.select_one('tbody').select('tr')

# 列表推导式:
head_texts = [e.text for e in head.select('th')]
body_texts_rows = [[e.text for e in row.select('td')] for row in body]

# 组合成dict:
data = [dict(zip(head_texts, row)) for row in body_texts_rows]

for element in data:
    print('element', element)

# 存入 ./store/practice.xlsx 的名为 'practice_s1' 的sheet页
pd.DataFrame(data).to_excel('./store/practice.xlsx', sheet_name='practice_s1', index=False)
