# tasks/task4_homepage.py
import time
from pyquery import PyQuery as pq

from settings import get_driver
import excel_utils

def task4_homepage(selected_accounts):
    """
    任务4：在淘宝首页抓取商品信息(或"猜你喜欢"一类)
    - 没有翻页，通过向下滚动加载更多
    - 这里简单演示向下滚动N次，抓取页面中的一些商品DOM
    """
    # 问向下滚动次数
    scroll_times = int(input("【任务4】需要向下滚动加载几次？ "))

    # 创建Excel
    title_list = ["Account", "Index", "Title", "Price", "Deal", "Tag", "ItemURL", "ImgURL"]
    wb, ws = excel_utils.create_workbook(title_list)
    current_row = 2
    count = 1

    for acc in selected_accounts:
        # 初始化浏览器并登录
        driver = get_driver()
        from settings import auto_login
        auto_login(driver, acc['username'], acc['password'])

        # 打开淘宝首页
        driver.get("https://www.taobao.com/")
        time.sleep(3)
        
        # 设置页面缩放为75%
        driver.execute_script("document.body.style.zoom='75%'")
        time.sleep(1)

        # 模拟向下滚动多次
        for i in range(scroll_times):
            print(f"[{acc['username']}] 第{i+1}次向下滚动...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # 等待加载

        # 页面源码
        html = driver.page_source
        doc = pq(html)

        # 使用新的选择器来抓取商品信息
        items = doc('.tb-pick-content-item').items()
        for item in items:
            # 商品标题
            title = item.find('.info-wrapper-title-text').text()
            
            # 价格（组合单位和数值）
            price_unit = item.find('.price-unit').text()
            price_value = item.find('.price-value').text()
            price = float(price_value) if price_value else 0.0
            
            # 成交量
            deal = item.find('.month-sale').text().replace('人购买', '')
            
            # 商品链接
            t_url = item.find('.item-link').attr('href')
            
            # 商品图片
            img_url = item.find('.product-img').attr('src')
            
            # 标签信息
            tag = item.find('.tag-text').text()
            
            # 确保URL是完整的
            if t_url and t_url.startswith('//'):
                t_url = f"https:{t_url}"
            if img_url and img_url.startswith('//'):
                img_url = f"https:{img_url}"

            # 写入Excel
            ws.cell(row=current_row, column=1, value=acc['username'])  # Account
            ws.cell(row=current_row, column=2, value=count)           # Index
            ws.cell(row=current_row, column=3, value=title)          # Title
            ws.cell(row=current_row, column=4, value=price)          # Price
            ws.cell(row=current_row, column=5, value=deal)           # Deal
            ws.cell(row=current_row, column=6, value=tag)            # Tag
            ws.cell(row=current_row, column=7, value=t_url)          # ItemURL
            ws.cell(row=current_row, column=8, value=img_url)        # ImgURL

            current_row += 1
            count += 1

        # 关闭当前账号的浏览器
        driver.quit()

    # 最后保存Excel
    excel_utils.save_workbook(wb, filename_prefix="Task4_Homepage")