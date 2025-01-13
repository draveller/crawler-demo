import json
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
target_url = 'https://www.spiderbuf.cn/playground/iplist'

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

# 解析JSON数组:
items = json.loads(response.text)
header = items[0].keys()
body = [item.values() for item in items]
data = [header] + body

# 创建 Excel 文件并写入图片
file_path = '../store/practice.xlsx'
sheet_name = 'practice_s7'
acer.save(data, file_path, sheet_name)
