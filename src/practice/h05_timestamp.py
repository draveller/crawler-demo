import base64
import hashlib
import json
import os
import time

import requests as req
from charset_normalizer import detect

from src.config.config import ROOT_PATH
from src.util import acer

"""
请求时间戳
"""

# 1. 生成秒级时间戳
timestamp = int(time.time())  # 等同于 JS 的 Math.floor(new Date().getTime() / 1000)

# 2. 计算 MD5
md5_hash = hashlib.md5(str(timestamp).encode('utf-8')).hexdigest()  # 注意要转字符串

# 3. 拼接并 Base64 编码
combined = f"{timestamp},{md5_hash}"
base64_str = base64.b64encode(combined.encode('utf-8')).decode('utf-8')

# 4. 构造最终 URL
target_url = f'https://www.spiderbuf.cn/playground/h05/api/{base64_str}'
print('target_url', target_url)

# 请求头
headers = {
    "GET": "/playground/h05/api/MTczNzg1NzYzMSwwNWM5M2M2YmNlOTU2YTNhOTkwOWZmYWM2ZGFkMjlkNg== HTTP/1.1",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "www.spiderbuf.cn",
    "Pragma": "no-cache",
    "Referer": "https://www.spiderbuf.cn/playground/h05",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

# 发送请求
response = req.get(target_url, headers=headers)
response.encoding = detect(response.content)['encoding']

# 表头
data = [['ranking', 'passwd', 'time_to_crack_it', 'used_count', 'year']]

# 处理每个对象
for item in json.loads(response.text):
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
acer.save(data, file_path, 'practice_h05')

print("数据已成功保存到:", file_path)
