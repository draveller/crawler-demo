import os
from io import BytesIO

import requests as req
from bs4 import BeautifulSoup
from charset_normalizer import detect
from openpyxl.drawing.image import Image

from src.config.config import ROOT_PATH
from src.util import acer

"""
访问频率限制
"""

# 目标 URL
base_url = 'https://www.spiderbuf.cn'
target_url = 'https://www.spiderbuf.cn/playground/h02'

# 请求头
headers = {
    "GET": "/playground/n02 HTTP/1.1",
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

# 表头
data = [["电影名称", "封面图片链接", "豆瓣电影评分", "导演", "编剧", "主演", "类型",
         "制片国家/地区", "语言", "上映日期", "片长", "又名", "IMDb", '详情']]

soup = BeautifulSoup(response.text, 'lxml')

rows = []


def analysis_fields(info):
    # 按换行符分割字符串
    lines = info.strip().split('\n')
    # 提取属性值
    values = []
    for line in lines:
        # 去掉属性名称部分，保留属性值
        value = line.split(':', 1)[-1].strip()
        values.append(value)
    return values


for i, element in enumerate(soup.select('body > div:nth-child(2) > div.row > div.col-xs-12.col-lg-12')):
    is_top_part = i % 2 == 0
    if is_top_part:
        cover_url = base_url + element.select_one('div.col-xs-3.col-lg-3 > img')['src']
        fields_text = element.select_one('div.col-xs-9.col-lg-9').text
        rows.append([
                        element.select_one('h2').text,
                        Image(BytesIO(req.get(cover_url).content))
                    ] + analysis_fields(fields_text))
    else:
        rows[len(rows) - 1].append(element.text.replace('简介：', ''))

data += rows

# 持久化存储
file_path = os.path.join(ROOT_PATH, 'store', 'practice.xlsx')
acer.save(data, file_path, 'practice_h01')

print("数据已成功保存到:", file_path)
