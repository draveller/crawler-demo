from io import BytesIO

import chardet
import requests as req
from bs4 import BeautifulSoup
from openpyxl.drawing.image import Image

from util import acer

# 目标 URL
target_url = 'https://www.spiderbuf.cn/playground/s05'

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

# 解析 HTML
base_url = 'https://www.spiderbuf.cn'
soup = BeautifulSoup(response.text, 'lxml')
img_urls = [base_url + img['src'] for img in soup.select('img')]

# 下载图片并存储到列表
data = [['序号', '图片']]
for i, img_url in enumerate(img_urls):
    response = req.get(img_url, headers=headers)
    if response.status_code != 200:
        print('请求图片失败, 结果:', response)
        continue
    img_data = Image(BytesIO(response.content))
    data.append([i + 1, img_data])

# 创建 Excel 文件并写入图片
file_path = '../store/practice.xlsx'
sheet_name = 'practice_s5'

acer.save(data, file_path, sheet_name)
