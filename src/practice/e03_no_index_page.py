import chardet
import requests as req
from bs4 import BeautifulSoup

from src.util import acer

"""
无页码爬取
"""

# 目标 URL

base_url = 'https://www.spiderbuf.cn'
target_url = 'https://www.spiderbuf.cn/playground/e03'

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

soup = BeautifulSoup(response.text, 'lxml')
page_marks = [a['href'] for a in soup.select('ul.pagination li a')[-5:]]

# 获取所有页码的数据
data = []
for idx, page_mark in enumerate(page_marks):
    print('baseurl=%s, page_mark=%s' % (base_url, page_mark))
    response = req.get(base_url + page_mark, headers=headers)
    response.encoding = chardet.detect(response.content)['encoding']
    if response.status_code != 200:
        print('请求失败, 结果:', response)
        exit()

    soup = BeautifulSoup(response.text, 'lxml')
    if idx == 0:
        header = [cell.text for cell in soup.select('thead > tr > th')]
        data += [header]
    body = [[cell.text for cell in row.select('td')] for row in soup.select('tbody > tr')]
    data += body

# 创建 Excel 文件并写入图片
file_path = '../../store/practice.xlsx'
sheet_name = 'practice_e3'
acer.save(data, file_path, sheet_name)
