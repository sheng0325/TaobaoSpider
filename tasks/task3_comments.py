# tasks/task3_comments.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq

import excel_utils
from settings import get_driver, auto_login

def task3_comments(selected_accounts):
    num_pages = int(input("【任务3】想要抓取多少页的商品评论？ "))
    keyword = input("【任务3】请输入搜索关键词: ")

    title_list = ["Page", "ItemIndex", "Title", "Comment"]
    wb, ws = excel_utils.create_workbook(title_list)
    current_row = 2

    # 创建新的driver实例及wait
    driver = get_driver()
    wait = WebDriverWait(driver, 15)
    # 如果需要登录，请在此调用 auto_login(driver, 用户名, 密码)

    driver.get("https://www.taobao.com/")
    time.sleep(2)
    input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
    input_box.clear()
    input_box.send_keys(keyword)
    search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-button button")))
    search_btn.click()
    time.sleep(2)

    for page in range(1, num_pages + 1):
        print(f"【任务3】开始抓第 {page} 页评论...")
        time.sleep(3)
        html = driver.page_source
        doc = pq(html)
        items = doc('div.content--CUnfXXxv > div > div').items()

        item_index = 1
        for item in items:
            title = item.find('.title--qJ7Xg_90 span').text()
            item_url = item.find('.doubleCardWrapperAdapt--mEcC7olq').attr('href')
            if not item_url:
                continue
            if item_url.startswith("//"):
                item_url = "https:" + item_url

            print(f"    -> 正在打开商品详情: {title}")
            driver.get(item_url)
            time.sleep(3)

            try:
                comment_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(),"累计评价")]')))
                comment_tab.click()
                time.sleep(2)
            except:
                print("    -> 找不到评论tab，跳过此商品...")
                driver.back()
                time.sleep(2)
                continue

            detail_html = driver.page_source
            d_doc = pq(detail_html)
            comments = d_doc('div.tb-revbd div.tm-rate-fulltxt').items()
            for cm in comments:
                comment_text = cm.text()
                ws.cell(row=current_row, column=1, value=page)           
                ws.cell(row=current_row, column=2, value=item_index)     
                ws.cell(row=current_row, column=3, value=title)          
                ws.cell(row=current_row, column=4, value=comment_text)   
                current_row += 1

            driver.back()
            time.sleep(2)
            item_index += 1

        if page < num_pages:
            click_next_page(driver, wait)

    driver.quit()
    excel_utils.save_workbook(wb, filename_prefix="Task3_Comments")

def click_next_page(driver, wait):
    try:
        time.sleep(2)
        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-content-leftWrap"]/div[2]/div[4]/div/div/button[2]')))
        next_btn.click()
    except:
        print("找不到 下一页 按钮。")