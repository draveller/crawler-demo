import requests as req
from bs4 import BeautifulSoup
from charset_normalizer import detect

from src.util import acer

"""
应对css固定样式偏移反爬
"""

# 目标 URL

target_url = 'https://www.spiderbuf.cn/playground/h01'

# 请求头
headers = {
    "GET": "/playground/n01 HTTP/1.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "www.spiderbuf.cn",
    "Pragma": "no-cache",
    "Referer": "https://www.spiderbuf.cn/list/2",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

# 发送请求
response = req.get(target_url, headers=headers)
response.encoding = detect(response.content)['encoding']
if response.status_code != 200:
    print('请求失败, 结果:', response)
    exit()

soup = BeautifulSoup(response.text, 'lxml')


def parse_row(idx_element):
    i, element = idx_element
    s = element.text
    if i == 0 and len(s) >= 2:
        return s[:0] + s[1] + s[0 + 1:1] + s[0] + s[1 + 1:]
    elif i == 2 and len(s) >= 11:
        prefix = s[:9]
        remain = s[9:]
        return prefix + remain[:0] + remain[1] + remain[0 + 1:1] + remain[0] + remain[1 + 1:]
    else:
        return s


data = [[c for c in map(parse_row, enumerate(row.select('h2,p')))] for row in soup.select('div.row > div')]

# 创建 Excel 文件并写入图片
file_path = '../../store/practice_h01.csv'
acer.save_csv(data, file_path)
