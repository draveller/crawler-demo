import chardet
import requests as req
from bs4 import BeautifulSoup

from src.util import acer

"""
爬取使用post请求的页面
"""

# 目标 URL
target_url = 'https://www.spiderbuf.cn/playground/s08'

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

# 发送请求
response = req.post(target_url, headers=headers, data={'level': 8})
response.encoding = chardet.detect(response.content)['encoding']
if response.status_code != 200:
    print('请求失败, 结果:', response)
    exit()

soup = BeautifulSoup(response.text, 'lxml')
header = [cell.text for cell in soup.select('thead > tr > th')]
body = [[cell.text for cell in row.select('td')] for row in soup.select('tbody > tr')]
data = [header] + body

# 创建 Excel 文件并写入图片
file_path = '../../store/practice.xlsx'
sheet_name = 'practice_s8'
acer.save(data, file_path, sheet_name)
