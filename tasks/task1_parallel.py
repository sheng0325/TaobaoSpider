# tasks/task1_parallel.py
import time
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq

import excel_utils
from settings import get_driver, auto_login

def worker_task1(acc, barrier, num_pages, keywords, result_list):
    """
    工作线程函数
    """
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    
    # 登录并等待用户验证
    if not auto_login(driver, acc['username'], acc['password']):
        print(f"[{acc['username']}] 登录失败，退出任务!")
        driver.quit()
        return

    # 等待所有账号都准备就绪
    barrier.wait()
    
    rows = []  # 收集数据
    
    # 处理每个关键词
    for keyword in keywords:
        print(f"\n[{acc['username']}] 开始搜索关键词: {keyword}")
        count = 1
        
        # 打开淘宝首页，输入关键词搜索
        driver.get("https://www.taobao.com/")
        time.sleep(2)
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        input_box.clear()
        input_box.send_keys(keyword)
        search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-button button")))
        search_btn.click()
        time.sleep(2)

        # 抓取指定页数
        for page_i in range(1, num_pages + 1):
            print(f"[{acc['username']}] [{keyword}] 正在抓取第 {page_i} 页...")
            
            time.sleep(3)
            html = driver.page_source
            doc = pq(html)
            items = doc('div.content--CUnfXXxv > div > div').items()

            for item in items:
                # ... (原有的数据提取代码) ...
                row = [
                    acc['username'], keyword, page_i, count, 
                    title, price, deal, location, shop, 
                    postText, t_url, shop_url, img_url
                ]
                rows.append(row)
                count += 1

            if page_i < num_pages:
                click_next_page(driver, wait)

    driver.quit()
    result_list.append(rows)

def parallel_task1_price(selected_accounts, config):
    """
    并行版本的任务1
    """
    # 从配置中获取参数
    keywords = config['task']['keywords']
    num_pages = config['task']['search']['pages_per_keyword']
    
    print(f"关键词列表: {keywords}")
    print(f"每个关键词抓取页数: {num_pages}")
    
    # 初始化同步barrier
    barrier = threading.Barrier(len(selected_accounts))
    threads = []
    results = []

    # 创建工作线程
    for acc in selected_accounts:
        t = threading.Thread(
            target=worker_task1,
            args=(acc, barrier, num_pages, keywords, results)
        )
        t.start()
        threads.append(t)

    # 等待所有线程完成
    for t in threads:
        t.join()

    # 合并结果到Excel
    title_list = ["Account", "Keyword", "Page", "Num", "Title", "Price", 
                 "Deal", "Location", "Shop", "PostFree?", "ItemURL", 
                 "ShopURL", "ImgURL"]
    
    wb, ws = excel_utils.create_workbook(title_list)
    current_row = 2
    
    for thread_rows in results:
        for row in thread_rows:
            for col, value in enumerate(row, start=1):
                ws.cell(row=current_row, column=col, value=value)
            current_row += 1

    excel_utils.save_workbook(wb, filename_prefix="Task1_Price_Parallel")