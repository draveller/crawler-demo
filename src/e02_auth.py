import chardet
import requests as req
from bs4 import BeautifulSoup

from util import acer

"""
爬取需要认证的页面
"""

# 目标 URL
login_url = 'https://www.spiderbuf.cn/playground/e02/list'

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
cookies = {
    "admin": "f310daee2fefa78c9c50d16d578d7360",
    "Path": "/",
    "Domain": "spiderbuf.cn",
    "Max-Age": "300"
}

# 发送请求
response = req.get(login_url, headers=headers, cookies=cookies)
response.encoding = chardet.detect(response.content)['encoding']
if response.status_code != 200:
    print('请求失败, 结果:', response)
    exit()

soup = BeautifulSoup(response.text, 'lxml')
header = [cell.text for cell in soup.select('thead > tr > th')]
body = [[cell.text for cell in row.select('td')] for row in soup.select('tbody > tr')]
data = [header] + body

# 创建 Excel 文件并写入图片
file_path = '../store/practice.xlsx'
sheet_name = 'practice_e2'
acer.save(data, file_path, sheet_name)
