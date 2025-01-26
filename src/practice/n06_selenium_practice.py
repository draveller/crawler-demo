from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

"""
selenium练习
"""

target_url = 'https://www.spiderbuf.cn/playground/n06'

# 配置浏览器选项
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_experimental_option("detach", True)  # 保持浏览器窗口打开

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
driver.get(target_url)
# 时停等文档加载
WebDriverWait(driver, 10).until(
    lambda d: d.execute_script('return document.readyState') == 'complete')

# 获取目标控件
username_element = driver.find_element(By.CSS_SELECTOR, 'input#username')
# 删除单个字符可以键入backspace来实现
username_element.send_keys(Keys.BACKSPACE)
# 删除全部字符使用clear
username_element.clear()
# 输入其他字符
username_element.send_keys('这是我输入的用户名')
# --------------------------------
password_element = driver.find_element(By.CSS_SELECTOR, 'input#password')
password_element.clear()
password_element.send_keys('这是我输入的密码')
# --------------------------------
email_element = driver.find_element(By.CSS_SELECTOR, 'input#email')
email_element.clear()
email_element.send_keys('这是我输入的邮箱@123.com')
# --------------------------------
website_element = driver.find_element(By.CSS_SELECTOR, 'input#website')
website_element.clear()
website_element.send_keys('www.这是我输入的网站.com')
# --------------------------------
date_element = driver.find_element(By.CSS_SELECTOR, 'input#date')
driver.execute_script("arguments[0].value = '2000-01-12';", date_element)
# --------------------------------
time_element = driver.find_element(By.CSS_SELECTOR, 'input#time')
driver.execute_script("arguments[0].value = '12:13:14';", time_element)
# --------------------------------
number_element = driver.find_element(By.CSS_SELECTOR, 'input#number')
number_element.clear()
number_element.send_keys('888666')
# --------------------------------
range_element = driver.find_element(By.CSS_SELECTOR, 'input#range')
# 可以输入方向键来调整滑块
range_element.send_keys(Keys.ARROW_RIGHT)
range_element.send_keys(Keys.ARROW_RIGHT)
# --------------------------------
color_element = driver.find_element(By.CSS_SELECTOR, 'input#color')
color_element.click()
actions = ActionChains(driver)
(actions
 .send_keys(Keys.TAB)
 .send_keys(Keys.TAB)
 .send_keys(Keys.TAB)
 .send_keys('22')
 .send_keys(Keys.TAB)
 .send_keys('83')
 .send_keys(Keys.TAB)
 .send_keys('182')
 .send_keys(Keys.ENTER)
 .perform())
# --------------------------------
search_element = driver.find_element(By.CSS_SELECTOR, 'input#search')
search_element.send_keys('这是我输入的搜索内容')
# --------------------------------
ta_element = driver.find_element(By.CSS_SELECTOR, 'textarea#textarea')
ta_element.clear()
ta_element.send_keys(
    '''
    <静夜思> -唐 李白
    窗前明月光,
    疑是地上霜.
    举头望明月,
    低头思故乡.
    ''')

# --------------------------------
py_checkbox = driver.find_element(By.CSS_SELECTOR, 'input#python')
h_checkbox = driver.find_element(By.CSS_SELECTOR, 'input#html')
css_checkbox = driver.find_element(By.CSS_SELECTOR, 'input#css')
js_checkbox = driver.find_element(By.CSS_SELECTOR, 'input#javascript')
go_checkbox = driver.find_element(By.CSS_SELECTOR, 'input#golang')
driver.execute_script(
    'for (let i = 0; i < arguments.length; i++) { arguments[i].checked = false; }',
    h_checkbox, css_checkbox, js_checkbox, go_checkbox
)

# --------------------------------
select_element = driver.find_element(By.CSS_SELECTOR, 'select#country')
# 使用 JavaScript 增加一个选项
driver.execute_script(
    """
    const option = document.createElement('option');
    option.value = arguments[1];
    option.text = arguments[2];
    arguments[0].appendChild(option);
    """,
    select_element, 'Trump', '川宝'
)

select = Select(select_element)
select.select_by_value('Trump')
# --------------------------------
active_a = driver.find_element(By.CSS_SELECTOR, 'a.item.active')
driver.execute_script(
'''
arguments[0].className = 'item';
''',
active_a)

items = driver.find_element(By.CSS_SELECTOR, 'ul.items')
driver.execute_script(
    '''
const li = document.createElement('li');
li.innerHTML = '<a class="item active" href="javascript:void(0);" title="作者：奥观海" onclick="switchItem(event)">川宝历险记</a>'
arguments[0].appendChild(li);
''', items)
