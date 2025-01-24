import json

import chardet
import requests as req

from src.util import acer

"""
爬取使用ajax动态获取数据的页面
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
file_path = '../../store/practice.xlsx'
sheet_name = 'practice_s7'
acer.save(data, file_path, sheet_name)
