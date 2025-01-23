from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import openpyxl as op
import time

# 全局变量
count = 1  # 写入Excel商品计数
KEYWORD = input('输入搜索的商品关键词Keyword：')
pageStart = int(input('输入爬取的起始页PageStart：'))
pageEnd = int(input('输入爬取的终止页PageEnd：'))

# 启动ChromeDriver服务及设置
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=options)

driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""}
)
driver.get('https://www.taobao.com')
driver.maximize_window()

wait = WebDriverWait(driver, 10)

# 等待用户扫码登录
print("请在浏览器中完成扫码登录，然后再继续运行脚本。")
time.sleep(10)  # 假设给用户10秒时间扫码登陆

# 初始化全局变量供其他模块使用
__all__ = ['driver', 'wait', 'KEYWORD', 'pageStart', 'pageEnd', 'count']
