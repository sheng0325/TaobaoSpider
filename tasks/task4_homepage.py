# tasks/task4_homepage.py
import time
from pyquery import PyQuery as pq

from settings import get_driver
import excel_utils

def task4_homepage(selected_accounts):
    """
    任务4：在淘宝首页抓取商品信息(或“猜你喜欢”一类)
    - 没有翻页，通过向下滚动加载更多
    - 这里简单演示向下滚动N次，抓取页面中的一些商品DOM
    """
    # 问向下滚动次数
    scroll_times = int(input("【任务4】需要向下滚动加载几次？ "))

    # 创建Excel
    title_list = ["Index", "Title", "Price", "URL"]
    wb, ws = excel_utils.create_workbook(title_list)
    current_row = 2
    count = 1

    # 打开淘宝首页
    driver.get("https://www.taobao.com/")
    time.sleep(3)

    # 模拟向下滚动多次
    for i in range(scroll_times):
        print(f"【任务4】第{i+1}次向下滚动...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # 等待加载

    # 页面源码
    html = driver.page_source
    doc = pq(html)

    # 假设你想抓取“猜你喜欢”这个模块的商品(需自己观察页面结构)
    # 这里仅示例
    items = doc("div.may-like").find(".maylike-content").items()
    for it in items:
        title = it.find(".maylike-desc").text()
        price = it.find(".maylike-price").text()
        url = it.find(".maylike-goods-pic a").attr("href")
        if url and url.startswith("//"):
            url = "https:" + url

        ws.cell(row=current_row, column=1, value=count)
        ws.cell(row=current_row, column=2, value=title)
        ws.cell(row=current_row, column=3, value=price)
        ws.cell(row=current_row, column=4, value=url)

        current_row += 1
        count += 1

    excel_utils.save_workbook(wb, filename_prefix="Task4_Homepage")