import json
import os
import re
from io import BytesIO

import requests as req
from bs4 import BeautifulSoup
from charset_normalizer import detect
from openpyxl.drawing.image import Image

from src.config.config import ROOT_PATH
from src.util import acer

"""
滚动加载
"""

# 目标 URL
target_url = 'https://www.spiderbuf.cn/static/js/h04/udSL29.js'

# 请求头
headers = {
    "GET": "/static/js/h04/udSL29.js HTTP/1.1",
    "Host": "www.spiderbuf.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

# 发送请求
response = req.get(target_url, headers=headers)
response.encoding = detect(response.content)['encoding']

# 表头

s = re.search(r'\[.*?]', response.text).group(0)
# 替换单引号为双引号
s = re.sub(r"(?<!\\)'", '"', s)
# 转换十六进制数值（如 0x1 → 1）
s = re.sub(r':0x([a-fA-F0-9]+)', lambda m: ':' + str(int(m.group(1), 16)), s)
# 处理 \x20 转义为空格
s = s.replace('\\x20', ' ')

data = [['id', 'ranking', 'passwd', 'time_to_crack_it', 'used_count', 'year']]
# 处理每个对象
for item in json.loads(s):
    # 解码 Unicode 字符
    for key, value in item.items():
        if isinstance(value, str):
            item[key] = value.encode('utf-8').decode('unicode_escape')
        elif isinstance(value, int):
            item[key] = int(str(value), 16) if isinstance(value, str) and value.startswith('0x') else value
    print(item)
    data.append(item.values())


# 持久化存储
file_path = os.path.join(ROOT_PATH, 'store', 'practice.xlsx')
acer.save(data, file_path, 'practice_h04')

print("数据已成功保存到:", file_path)
