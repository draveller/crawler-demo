#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import chardet
import requests as req
from bs4 import BeautifulSoup

from util import acer

"""
爬取当当网好评榜前100本书籍信息
"""

# chardet库用于自动检测编码
# requests库用于发送HTTP请求
# bs4库用于解析HTML页面

# 目标URL
base_url = "http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-recent30-0-0-1-%d"

# 每页只能固定爬取20本书, 循环5次:
all_books = []
for i in range(1, 6):
    url = base_url % i

    # 发送HTTP请求
    response = req.get(url)
    response.encoding = chardet.detect(response.content)['encoding']

    # 检查请求是否成功
    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        exit()

    # 使用bs解析HTML页面, 解析器使用lxml
    soup = BeautifulSoup(response.text, 'lxml')

    # 查找图书信息
    books = soup.find('ul', class_='bang_list clearfix bang_list_mode').find_all('li')
    all_books += books


data = [['序号','书名','作者','价格','评分']]
# 提取并打印图书数据
for idx, book in enumerate(all_books):
    # 书名
    title = book.find('div', class_='name').find('a')['title'].strip()
    # 作者
    _ = book.find('div', class_='publisher_info').find('a')
    author = '' if _ is None else _.text.strip()
    # 价格
    price = book.find('span', class_='price_n').text.strip()
    # 评分
    _ = book.find('div', class_='star').find('span', class_='level').find('span')['style']
    rating = _.replace('width:', '').replace('%', '').replace(';', '').strip()  # 提取评分百分比

    data.append([idx + 1, title, author, price, rating])


# 保存数据到csv文件
acer.save_csv(data, '../store/dangdang_books.csv')