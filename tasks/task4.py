# tasks/task4.py

import time
import threading
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from .utils import (
    init_webdriver,
    login_taobao,
    scroll_to_bottom,
    save_to_excel
)

# 创建全局锁确保 Excel 写入安全
excel_lock = threading.Lock()

def parse_item_info_task4(item):
    """解析单个推荐商品信息"""
    item = pq(item)  # 将 item 转换为 PyQuery 对象

    # 定位商品标题
    title = item.find('.info-wrapper-title-text').text()

    # 定位价格
    price = item.find('.price-value').text()
    price_unit = item.find('.price-unit').text()
    price = f"{price_unit}{price}"

    # 定位销量
    sales = item.find('.month-sale').text()

    # 定位商品链接
    link = item.find('.item-link').attr('href')
    if link and not link.startswith('http'):
        link = f"https:{link}"

    # 定位商品图片
    img_url = item.find('.product-img').attr('src')
    if img_url and not img_url.startswith('http'):
        img_url = f"https:{img_url}"

    # 定位促销信息并转换为字符串
    promotions = [t.text() for t in item.find('.tag-text').items()]
    promotions_str = ", ".join(promotions) if promotions else ""

    return {
        "title": title,
        "price": price,
        "sales": sales,
        "link": link,
        "img_url": img_url,
        "promotions": promotions_str
    }

def run_task4(config, accounts):
    print("===== 开始执行任务4：推荐商品数据 =====")

    task_cfg = config['task4']
    accounts_index = task_cfg['accounts_index']
    scroll_times = task_cfg['scroll_times']
    output_file = task_cfg['output_file']

    global_cfg = config['global']
    driver_path = global_cfg['driver_path']
    headless = global_cfg['headless']
    manual_verify_wait = global_cfg['manual_verify_wait']

    # 使用线程池并行处理账号
    with ThreadPoolExecutor(max_workers=len(accounts_index)) as executor:
        futures = []
        for idx in accounts_index:
            try:
                account = accounts[idx]
            except IndexError:
                print(f"账号索引 {idx} 超出范围，请检查 accounts.json 中的账号数量。")
                continue
            except Exception as e:
                print(f"读取账号信息时发生异常：{e}")
                continue

            # 提交任务到线程池
            future = executor.submit(
                _process_single_account,
                account,
                driver_path,
                headless,
                manual_verify_wait,
                scroll_times,
                output_file
            )
            futures.append(future)

        # 等待所有任务完成
        for future in futures:
            future.result()

    print("===== 任务4执行完毕 =====")

def _process_single_account(account, driver_path, headless, manual_verify_wait, scroll_times, output_file):
    """处理单个账号的任务"""
    try:
        driver = init_webdriver(driver_path, headless)
    except Exception as e:
        print(f"初始化 WebDriver 失败: {e}")
        return

    wait = WebDriverWait(driver, 20)
    username = account['username']
    password = account['password']
    acc_type = account['type']

    print(f"=== 正在使用账号: {username} ===")
    # 登录
    try:
        login_taobao(driver, username, password, manual_verify_wait)
    except Exception as e:
        print(f"登录过程中发生异常：{e}")
        driver.save_screenshot(f"login_error_{username}.png")
        driver.quit()
        return

    # 确认登录状态
    try:
        user_avatar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.J_UserMemberAvatar.member-avatar.member-avatar-order')))            
        print(f"账号 {username} 登录成功。")
    except TimeoutException:
        print(f"账号 {username} 登录后未找到用户头像，可能登录未成功。")
        driver.save_screenshot(f"login_failed_{username}.png")
        driver.quit()
        return

    print("正在执行：访问淘宝首页")
    driver.get("https://www.taobao.com/")
    time.sleep(3)

    # 缩小页面到50%
    driver.execute_script("document.body.style.zoom='50%'")
    time.sleep(2)  # 等待页面缩放完成

    print(f" -> 向下滚动页面 {scroll_times} 次，以触发懒加载...")
    scroll_to_bottom(driver, times=scroll_times, sleep_interval=2)

    all_recommend_data = []
    try:
        # 使用pyquery解析页面
        page_source = driver.page_source
        doc = pq(page_source)
        
        # 解析推荐商品
        items = doc('#ice-container > div.tbpc-layout > div.layer > div > div > div > div.tb-pick-feeds-container > div > div').items()
        for item in items:
            try:
                info = parse_item_info_task4(item)
                all_recommend_data.append(info)
            except Exception as e:
                print(f"解析推荐商品出错: {e}")
                driver.save_screenshot(f"parse_error_{username}.png")
    except Exception as e:
        print(f"解析推荐商品模块出错: {e}")
        driver.save_screenshot(f"parse_error_{username}.png")

    # 使用锁确保线程安全的 Excel 写入
    with excel_lock:
        headers = [
            "title", "price", "sales", "link", 
            "img_url", "promotions"
        ]
        try:
            # 清理无效字符并截断工作表名称
            sheet_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in username)[:31]
            save_to_excel(output_file, sheet_name, all_recommend_data, headers)
            print(f"账号 {username} 数据已保存到 {output_file}")
        except Exception as e:
            print(f"保存 Excel 时发生异常：{e}")
            driver.save_screenshot(f"save_excel_error_{username}.png")

    driver.quit()
