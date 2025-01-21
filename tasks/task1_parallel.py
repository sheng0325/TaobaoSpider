# tasks/task1_price_parallel.py
import time, threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq

import excel_utils
from settings import get_driver, auto_login

def worker_task1(acc, barrier, num_pages, keyword, result_list):
    """
    单个账号的工作线程：
    - 登录
    - 等待同步信号
    - 开始抓取指定页数的数据
    - 收集结果到result_list
    """
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    auto_login(driver, acc['username'], acc['password'])

    # 打开淘宝首页，输入关键词搜索
    driver.get("https://www.taobao.com/")
    time.sleep(2)
    input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
    input_box.clear()
    input_box.send_keys(keyword)
    search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-button button")))
    search_btn.click()
    time.sleep(2)

    # 等待用户确认所有账号已登录后再开始抓取
    barrier.wait()

    rows = []  # 收集此线程的所有抓取行
    count = 1
    for page_i in range(1, num_pages + 1):
        print(f"[{acc['username']}] 正在抓取第 {page_i} 页...")
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
            shop = item.find('.shopNameText--DmtlsDKm').text()
            postText_raw = item.find('.subIconWrapper--Vl8zAdQn').text()
            postText = "包邮" if "包邮" in postText_raw else "/"
            t_url = item.find('.doubleCardWrapperAdapt--mEcC7olq').attr('href')
            shop_url = item.find('.TextAndPic--grkZAtsC a').attr('href')
            img_url = item.find('.mainPicAdaptWrapper--V_ayd2hD img').attr('src')

            # 收集一行数据，包含账号信息
            row = [
                acc['username'], page_i, count, title, price,
                deal, location, shop, postText, t_url, shop_url, img_url
            ]
            rows.append(row)

            count += 1

        # 如果不是最后一页，则点击“下一页”
        if page_i < num_pages:
            click_next_page(driver, wait)

    driver.quit()
    result_list.append(rows)

def click_next_page(driver, wait):
    try:
        time.sleep(2)
        next_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="search-content-leftWrap"]/div[2]/div[4]/div/div/button[2]')))
        next_btn.click()
    except:
        print("【警告】找不到 下一页 按钮，可能已经到底了~")

def parallel_task1_price(selected_accounts):
    # 获取用户输入
    num_pages = int(input("【任务1】想要抓取多少页商品? "))
    keyword = input("【任务1】请输入搜索关键词: ").strip()

    # 初始化屏障：线程数 + 1（主线程）
    barrier = threading.Barrier(len(selected_accounts) + 1)
    threads = []
    results = []  # 用于收集各线程的结果，列表共享但append线程安全

    # 启动每个账号的线程
    for acc in selected_accounts:
        t = threading.Thread(
            target=worker_task1,
            args=(acc, barrier, num_pages, keyword, results)
        )
        t.start()
        threads.append(t)

    print("请确认所有账号都已成功登录并准备就绪，然后按回车继续启动抓取任务...")
    input()  # 用户确认
    barrier.wait()  # 主线程等待，放行所有子线程同时开始抓取

    # 等待所有线程结束
    for t in threads:
        t.join()

    # 将所有结果整合到一个Excel中
    title_list = ["Account", "Page", "Num", "Title", "Price", "Deal", "Location", "Shop", "PostFree?", "ItemURL", "ShopURL", "ImgURL"]
    wb, ws = excel_utils.create_workbook(title_list)
    current_row = 2
    # 遍历results中每个线程的结果列表
    for thread_rows in results:
        for row in thread_rows:
            for col, value in enumerate(row, start=1):
                ws.cell(row=current_row, column=col, value=value)
            current_row += 1

    excel_utils.save_workbook(wb, filename_prefix="Task1_Price_Parallel")