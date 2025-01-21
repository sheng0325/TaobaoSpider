# tasks/task2_dynamic.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq

import excel_utils
from settings import get_driver, auto_login

def task2_dynamic_pricing(selected_accounts, config):
    """
    任务2：动态价格监控
    - 支持多账号
    - 从配置文件读取参数
    """
    # 从配置文件获取参数
    total_times = config['task']['search'].get('dynamic_times', 3)  # 默认3次
    keywords = config['task']['keywords']  # 获取关键词列表
    interval = config['task']['search'].get('interval_minutes', 30)  # 默认30分钟间隔
    
    print(f"动态监控配置:")
    print(f"- 监控次数: {total_times}")
    print(f"- 监控关键词: {keywords}")
    print(f"- 间隔时间: {interval}分钟")

    # 创建Excel
    title_list = ["TimeRound", "Keyword", "Title", "Price", "Deal", "Location"]
    wb, ws = excel_utils.create_workbook(title_list)
    current_row = 2

    # 循环抓取指定次数
    for i in range(total_times):
        print(f"\n【任务2】第 {i+1} 次抓取...")
        
        # 对每个关键词进行抓取
        for keyword in keywords:
            print(f"正在抓取关键词: {keyword}")
            
            # 创建新的driver实例及wait
            driver = get_driver()
            wait = WebDriverWait(driver, 15)
            
            # 登录第一个账号
            if selected_accounts:
                acc = selected_accounts[0]
                auto_login(driver, acc['username'], acc['password'])

            # 搜索商品
            driver.get("https://www.taobao.com/")
            time.sleep(2)
            input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
            input_box.clear()
            input_box.send_keys(keyword)
            search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-button button")))
            search_btn.click()
            time.sleep(3)

            # 抓取数据
            html = driver.page_source
            doc = pq(html)
            items = doc('div.content--CUnfXXxv > div > div').items()

            for item in items:
                title = item.find('.title--qJ7Xg_90 span').text()
                price_int = item.find('.priceInt--yqqZMJ5a').text()
                price_float = item.find('.priceFloat--XpixvyQ1').text()
                price = float(f"{price_int}{price_float}") if price_int and price_float else 0.0
                deal = item.find('.realSales--XZJiepmt').text()
                location = item.find('.procity--wlcT2xH9 span').text()

                # 写入Excel
                ws.cell(row=current_row, column=1, value=f"第{i+1}次")
                ws.cell(row=current_row, column=2, value=keyword)
                ws.cell(row=current_row, column=3, value=title)
                ws.cell(row=current_row, column=4, value=price)
                ws.cell(row=current_row, column=5, value=deal)
                ws.cell(row=current_row, column=6, value=location)
                current_row += 1

            driver.quit()

        # 如果不是最后一次，则等待指定时间
        if i < total_times - 1:
            print(f"【任务2】等待{interval}分钟后进行下一次抓取...")
            time.sleep(interval * 60)  # 转换为秒

    # 保存Excel
    excel_utils.save_workbook(wb, filename_prefix="Task2_DynamicPricing")