# tasks/task1_price.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq

import excel_utils
from settings import get_driver, auto_login

def task1_price_data(selected_accounts):
    """
    任务1：商品价格数据
    - 支持多账号依次登录抓取
    - 最后将所有账号的抓取结果存到同一个Excel(可区分账号)
    """

    # 让用户输入要抓几页
    num_pages = int(input("【任务1】想要抓取多少页商品? "))
    # 让用户输入关键词
    keyword = input("【任务1】请输入搜索关键词: ").strip()

    # 创建一个Excel，列中多加一列记录 "账号"
    title_list = ["Account", "Page", "Num", "Title", "Price", "Deal", "Location", "Shop", "PostFree?", "ItemURL", "ShopURL", "ImgURL"]
    wb, ws = excel_utils.create_workbook(title_list)

    # 准备一个行指针
    current_row = 2

    ##############################
    # 依次处理每个选中的账号
    ##############################
    for acc in selected_accounts:
        # 1) 启动浏览器 & 登录
        driver = get_driver()
        wait = WebDriverWait(driver, 15)
        auto_login(driver, acc['username'], acc['password'])

        # 2) 打开淘宝首页，输入关键词搜索
        driver.get("https://www.taobao.com/")
        time.sleep(2)
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        input_box.clear()
        input_box.send_keys(keyword)
        search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-button button")))
        search_btn.click()
        time.sleep(2)

        # 3) 循环抓取指定页数
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
                price = 0.0
                if price_int and price_float:
                    price = float(f"{price_int}{price_float}")
                deal = item.find('.realSales--XZJiepmt').text()
                location = item.find('.procity--wlcT2xH9 span').text()
                shop = item.find('.shopNameText--DmtlsDKm').text()
                postText_raw = item.find('.subIconWrapper--Vl8zAdQn').text()
                postText = "包邮" if "包邮" in postText_raw else "/"
                t_url = item.find('.doubleCardWrapperAdapt--mEcC7olq').attr('href')
                shop_url = item.find('.TextAndPic--grkZAtsC a').attr('href')
                img_url = item.find('.mainPicAdaptWrapper--V_ayd2hD img').attr('src')

                # 写入Excel
                ws.cell(row=current_row, column=1, value=acc['username']) # Account
                ws.cell(row=current_row, column=2, value=page_i)          # Page
                ws.cell(row=current_row, column=3, value=count)           # Num
                ws.cell(row=current_row, column=4, value=title)           # Title
                ws.cell(row=current_row, column=5, value=price)           # Price
                ws.cell(row=current_row, column=6, value=deal)            # Deal
                ws.cell(row=current_row, column=7, value=location)        # Location
                ws.cell(row=current_row, column=8, value=shop)            # Shop
                ws.cell(row=current_row, column=9, value=postText)        # PostFree
                ws.cell(row=current_row, column=10, value=t_url)          # ItemURL
                ws.cell(row=current_row, column=11, value=shop_url)       # ShopURL
                ws.cell(row=current_row, column=12, value=img_url)        # ImgURL

                current_row += 1
                count += 1

            # 如果不是最后一页，则点击下一页
            if page_i < num_pages:
                click_next_page(driver, wait)

        # 4) 当前账号处理完毕，关闭浏览器(也可留着)
        driver.quit()

    # 最后保存Excel
    excel_utils.save_workbook(wb, filename_prefix="Task1_Price")

def click_next_page(driver, wait):
    """
    点击 '下一页' 按钮
    """
    import time
    time.sleep(2)

    # 输入next button
    next_button_selectors = [
        # 国际版选择器
        '//*[@id="search-content-leftWrap"]/div[2]/div[4]/div/div/button[2]',
        # 国内版选择器
        '//*[@id="search-content-leftWrap"]/div[3]/div[4]/div/div/button[2]',
    ]

    # 依次尝试每个选择器
    for selector in next_button_selectors:
        try:
            next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            next_btn.click()
            return  # 如果成功点击就返回
        except:
            continue  # 如果失败就尝试下一个选择器
    
    print("【警告】找不到 下一页 按钮，可能已经到底了~")