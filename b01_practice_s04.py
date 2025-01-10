import time

import chardet
import requests as req
from bs4 import BeautifulSoup

from util import acer

base_url = 'https://www.spiderbuf.cn/playground/s04'

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "www.spiderbuf.cn",
    "Pragma": "no-cache",
    "Referer": "https://www.spiderbuf.cn/list/3",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

data = []
head_texts = []
for page_no in range(1, 6):

    target_url = base_url + '?pageno=' + str(page_no)
    response = req.get(target_url, headers=headers)
    response.encoding = chardet.detect(response.content)['encoding']
    if response.status_code != 200:
        print('请求失败, 结果:', response)
        exit()

    soup = BeautifulSoup(response.text, 'lxml')
    head = soup.select_one('thead').select_one('tr')
    body = soup.select_one('tbody').select('tr')

    # 列表推导式:
    head_texts = ['页码'] + [e.text for e in head.select('th')]
    body_texts_rows = [[page_no] + [e.text for e in row.select('td')] for row in body]

    # 组合成二维数组:
    data += body_texts_rows
    # 休眠1秒钟
    time.sleep(1)

# 存入excel
data_include_head = [head_texts] + data
acer.fast_save(data_include_head, './store/practice.xlsx', 'practice_s4')
