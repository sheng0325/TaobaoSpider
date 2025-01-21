# tasks/task2_dynamic.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq

import excel_utils
from settings import get_driver, auto_login  # 修改导入

def task2_dynamic_pricing(selected_accounts):
    total_times = int(input("【任务2】需要抓取多少次？(每次间隔30分钟) "))
    keyword = input("【任务2】请输入搜索关键词: ")

    title_list = ["TimeRound", "Title", "Price", "Deal", "Location"]
    wb, ws = excel_utils.create_workbook(title_list)
    current_row = 2

    for i in range(total_times):
        print(f"【任务2】第 {i+1} 次抓取...")

        # 创建新的driver实例及wait
        driver = get_driver()
        wait = WebDriverWait(driver, 15)
        # 如果需要登录，请在此调用 auto_login(driver, 用户名, 密码)
        # 此处假设无需登录或已处理登录逻辑

        driver.get("https://www.taobao.com/")
        time.sleep(2)
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        input_box.clear()
        input_box.send_keys(keyword)
        search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-button button")))
        search_btn.click()
        time.sleep(3)

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

            ws.cell(row=current_row, column=1, value=f"第{i+1}次")
            ws.cell(row=current_row, column=2, value=title)
            ws.cell(row=current_row, column=3, value=price)
            ws.cell(row=current_row, column=4, value=deal)
            ws.cell(row=current_row, column=5, value=location)
            current_row += 1

        driver.quit()

        if i < total_times - 1:
            print("【任务2】等待30分钟后进行下一次抓取...")
            time.sleep(1800)  # 等待30分钟

    excel_utils.save_workbook(wb, filename_prefix="Task2_DynamicPricing")