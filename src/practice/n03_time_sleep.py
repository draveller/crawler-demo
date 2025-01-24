import time

import requests as req
from bs4 import BeautifulSoup
from charset_normalizer import detect

from src.util import acer

"""
访问频率限制
"""

# 目标 URL
base_url = 'https://www.spiderbuf.cn/playground/n03/%s'

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
data = [['排名', '密码', '破解耗时', '使用数']]
for i in range(1, 21):
    target_url = base_url % i

    response = req.get(target_url, headers=headers)
    response.encoding = detect(response.content)['encoding']
    if response.status_code != 200:
        print('请求失败, 结果:', response)
        exit()

    soup = BeautifulSoup(response.text, 'lxml')
    data += [[cell.text for cell in row.select('td')] for row in soup.select('table.table > tbody > tr')]

    # 延时1s:
    time.sleep(1)


# 创建 Excel 文件并写入图片
file_path = '../../store/practice_n03.csv'
acer.save_csv(data, file_path)
