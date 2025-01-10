#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用 Selenium 爬取 Bilibili 视频标题
前提: 下载 Chrome 浏览器驱动, 并配置环境变量
https://googlechromelabs.github.io/chrome-for-testing/
"""
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options


def init_browser():
    """初始化 Chrome 浏览器，配置无头模式"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 启用无头模式
    chrome_options.add_argument("--disable-gpu")  # 禁用 GPU 加速
    chrome_options.add_argument("--no-sandbox")  # 禁用沙盒模式
    return webdriver.Chrome(options=chrome_options)


def search_bilibili(browser, keyword):
    """在 Bilibili 首页搜索指定关键词"""
    browser.get("https://www.bilibili.com/")
    wait = WebDriverWait(browser, 10)

    # 定位搜索输入框并输入关键词
    input_element = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, ".nav-search-input")))
    input_element.send_keys(keyword)

    # 定位搜索按钮并点击
    submit_button = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="nav-searchform"]/div[2]')))
    submit_button.click()

    # 切换到新打开的窗口（搜索结果页）
    print('跳转到新窗口')
    all_handles = browser.window_handles
    browser.switch_to.window(all_handles[1])


def get_total_pages(browser):
    """获取搜索结果的总页数"""
    wait = WebDriverWait(browser, 10)
    total_page_element = wait.until(ec.element_to_be_clickable(
        (By.CSS_SELECTOR,
         '#i_cecream > div > div:nth-child(2) > div.search-content--gray.search-content > div > div > div > div.flex_center.mt_x50.mb_x50 > div > div > button:nth-child(10)')
    ))
    return int(total_page_element.text)


def extract_video_titles(browser):
    """从当前页面提取视频标题"""
    soup = BeautifulSoup(browser.page_source, 'lxml')
    videos = soup.select_one("div.video-list.row").find_all("div", recursive=False)
    titles = []
    for video in videos:
        h3 = video.select_one('div > div.bili-video-card__wrap > div > div > a > h3')
        if h3:
            titles.append(h3.get('title'))
    return titles


def scrape_all_videos(browser, total_pages):
    """爬取所有页面的视频标题"""
    all_titles = []
    for current_page in range(1, total_pages + 1):
        print(f'正在爬取第 {current_page} 页...')
        titles = extract_video_titles(browser)
        all_titles += titles

        if current_page < total_pages:
            # 点击下一页按钮
            next_page_button = WebDriverWait(browser, 10).until(
                ec.element_to_be_clickable((By.XPATH, '//button[contains(text(), "下一页")]'))
            )
            next_page_button.click()
            time.sleep(2)  # 等待页面加载

    return all_titles


def main():
    """主函数"""
    browser = init_browser()
    try:
        search_bilibili(browser, "蔡徐坤 篮球")  # 搜索关键词
        total_pages = get_total_pages(browser)  # 获取总页数
        print('总页数:', total_pages)

        all_titles = scrape_all_videos(browser, total_pages)  # 爬取所有视频标题
        for i, title in enumerate(all_titles):
            print(i, title)  # 打印视频标题
    finally:
        browser.quit()  # 关闭浏览器


if __name__ == "__main__":
    main()
