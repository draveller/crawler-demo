#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用selenium自动化
前提: 下载chrome浏览器驱动, 并配置环境变量
https://googlechromelabs.github.io/chrome-for-testing/
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# 初始化浏览器
driver = webdriver.Chrome()

# 打开百度
driver.get("https://www.baidu.com")

# 找到搜索框并输入关键词
# 使用css选择器获取搜索框
input_element = driver.find_element(By.CSS_SELECTOR, '#kw')
# send_keys方法用于模拟在元素中输入
input_element.send_keys("萌宠照片")

# 找到搜索按钮并点击
button = driver.find_element(By.CSS_SELECTOR, '#su')
button.click()

# 休眠3秒后关闭浏览器
time.sleep(3)
driver.quit()
