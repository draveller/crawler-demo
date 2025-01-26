import os
import re
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from openpyxl.drawing.image import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.config.config import ROOT_PATH
from src.util import acer, ster

"""
破解css伪元素反爬
"""

base_url = 'https://www.spiderbuf.cn'

# 配置浏览器选项
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# 启动浏览器
driver = webdriver.Chrome(options=options)

# 隐藏 webdriver 属性
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# 伪造插件列表
driver.execute_script('''
    Object.defineProperty(navigator, 'plugins', {
        get: () => [{
            description: 'PDF Viewer',
            filename: 'internal-pdf-viewer'
        }]
    })
''')

# 访问目标页面
driver.get('https://www.spiderbuf.cn/playground/n04')

soup = BeautifulSoup(driver.page_source, 'lxml')
kv_map = {
    "abcdef.before": "7",
    "abcdef.after": "5",
    "ghijkl.before": "8",
    "ghijkl.after": "9",
    "mnopqr.before": "9",
    "mnopqr.after": "1",
    "uvwxyz.before": "1",
    "uvwxyz.after": "4",
    "yzabcd.before": "2",
    "yzabcd.after": "6",
    "efghij.before": "3",
    "efghij.after": "2",
    "klmnop.before": "5",
    "klmnop.after": "7",
    "qrstuv.before": "4",
    "qrstuv.after": "3",
    "wxyzab.before": "6",
    "wxyzab.after": "0",
    "cdefgh.before": "0",
    "cdefgh.after": "8",
    "hijklm.after": "6",
    "opqrst.after": "0",
    "uvwxab.after": "3",
    "cdijkl.after": "8",
    "pqrmno.after": "1",
    "stuvwx.after": "4",
    "pkenmc.after": "7",
    "tcwdsk.after": "9",
    "mkrtyu.after": "5",
    "umdrtk.after": "2"
}

data = [["电影名称", "封面图片", "豆瓣电影评分", "导演", "编剧", "主演", "类型",
         "制片国家/地区", "语言", "上映日期", "片长", "又名", "IMDb", '简介']]

rows = []

for i, element in enumerate(soup.select('div.container > div.row > div.col-xs-12.col-lg-12')):
    if not element.text:
        continue

    is_top_part = i == 0 or i % 2 != 0
    if is_top_part:
        title = element.select_one('h2').text
        _cover_url = base_url + element.select_one('div.col-xs-3.col-lg-3 > img')['src']
        cover_img = Image(BytesIO(requests.get(_cover_url).content))
        _fields = element.select_one('div.col-xs-9.col-lg-9')
        _class_names = _fields.select_one('span:nth-child(2)')['class']
        score = (kv_map.get(f'{_class_names[0]}.before') + _fields.select_one('span:nth-child(2)').text
                 + kv_map.get(f'{_class_names[1]}.after'))

        # print(_fields.text,'\n\n\n')

        director = ster.ster.get_middledle(_fields.text, '导演:', '\n编剧')
        writer = ster.get_middle(_fields.text, '编剧:', '\n主演')
        actor = ster.get_middle(_fields.text, '主演:', '\n类型')
        movie_type = ster.get_middle(_fields.text, '类型:', '\n制片国家/地区')
        production_area = ster.get_middle(_fields.text, '制片国家/地区:', '\n语言')
        language = ster.get_middle(_fields.text, '语言:', '\n上映日期')
        release_date = ster.get_middle(_fields.text, '上映日期:', '\n片长')
        running_time = ster.get_middle(_fields.text, '片长:', '\n又名')
        another_name = ster.get_middle(_fields.text, '又名:', '\nIMDb')
        imdb = ster.get_middle(_fields.text, 'IMDb:', '')

        fields_text = element.select_one('div.col-xs-9.col-lg-9').text
        rows.append([title, cover_img, score, director, writer, actor, movie_type, production_area, language,
                     release_date, running_time, another_name, imdb])
    else:
        rows[len(rows) - 1].append(element.text.replace('简介：', ''))

data += rows

# 持久化存储
file_path = os.path.join(ROOT_PATH, 'store', 'practice.xlsx')
acer.save(data, file_path, 'practice_n04')

print("数据已成功保存到:", file_path)
