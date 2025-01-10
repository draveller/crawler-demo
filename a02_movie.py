#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime

import chardet
import pandas as pd
import requests as req
from bs4 import BeautifulSoup

"""
爬取50条电影信息, 并存入excel
"""

# 目标URL
base_url = "https://ssr1.scrape.center/page/%d"

# 每页只能固定爬取10条
all_movies = []  # 定义 all_movies 列表，用于存储所有电影信息
for i in range(1, 6):
    url = base_url % i

    # 发送HTTP请求
    session = req.Session()
    response = session.get(url)
    response.encoding = chardet.detect(response.content)['encoding']

    # 检查请求是否成功
    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        exit()

    # 使用bs解析HTML页面, 解析器使用lxml
    soup = BeautifulSoup(response.text, 'lxml')
    # 查找信息列表
    movies = soup.find_all('div', class_='el-card item m-t is-hover-shadow')
    all_movies += movies  # 将当前页的电影信息添加到 all_movies 列表中

# 创建一个空列表，用于存储所有电影信息的字典
movies_data = []

# 遍历所有电影信息
for idx, movie in enumerate(all_movies):
    # 提取电影名称
    movie_name = movie.find('a', class_='name').h2.text
    # 提取电影评分
    movie_rate = movie.find('p', class_='score').text.strip()
    # 提取电影标签
    movie_tags_element = movie.find('div', class_='categories').find_all('button')


    # 定义一个函数，用于将标签元素转换为字符串
    def tag2str(tag) -> str:
        return tag.span.text.strip()


    # 将所有标签拼接成一个字符串，用逗号分隔
    movie_tags = ','.join(map(tag2str, movie_tags_element))

    # 获取当前时间，作为爬取时间
    crawl_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 将电影信息存储为字典，并添加到列表中
    movies_data.append({
        '序号': idx + 1,
        '电影名': movie_name,
        '电影标签': movie_tags,
        '电影评分': movie_rate,
        '爬取时间': crawl_time
    })

# 使用pandas将字典列表转换为DataFrame
df = pd.DataFrame(movies_data)

# 定义存储路径
output_dir = './store'
output_file = os.path.join(output_dir, 'data.xlsx')

# 检查存储路径是否存在，如果不存在则创建
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 将DataFrame导出到Excel文件中的'电影信息'工作簿
# 如果文件已存在，则覆盖写入
with pd.ExcelWriter(output_file, engine='openpyxl', mode='w') as writer:
    df.to_excel(writer, sheet_name='电影信息', index=False)

print(f"数据已成功导出到 {output_file}")
