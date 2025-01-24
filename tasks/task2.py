# tasks/task2.py

import time
import threading
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from .utils import (
    init_webdriver,
    login_taobao,
    scroll_to_bottom,
    parse_item_info,
    save_to_excel
)

# 创建全局锁确保 Excel 写入安全
excel_lock = threading.Lock()

def run_task2(config, accounts):
    print("===== 开始执行任务2：动态定价数据 =====")

    task_cfg = config['task2']
    accounts_index = task_cfg['accounts_index']
    products = task_cfg['products']
    pages_per_round = task_cfg['pages_per_round']
    crawl_rounds = task_cfg['crawl_rounds']
    interval_seconds = task_cfg['interval_seconds']
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
                products,
                pages_per_round,
                crawl_rounds,
                interval_seconds,
                output_file
            )
            futures.append(future)

        # 等待所有任务完成
        for future in futures:
            future.result()

    print("===== 任务2执行完毕 =====")

def _process_single_account(account, driver_path, headless, manual_verify_wait, products, pages_per_round, crawl_rounds, interval_seconds, output_file):
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

    all_round_data = []
    for round_idx in range(1, crawl_rounds + 1):
        print(f" -> 第 {round_idx} 轮爬取开始")
        round_data = []

        for product in products:
            print(f"账号 {username} 正在执行：搜索商品 - {product}")
            driver.get("https://s.taobao.com/")
            try:
                search_input = wait.until(EC.visibility_of_element_located((By.ID, "q")))
                search_input.clear()
                search_input.send_keys(product)
                search_input.send_keys(Keys.ENTER)
                driver.save_screenshot(f"search_results_{username}_{product}_round_{round_idx}.png")
            except TimeoutException:
                print(f"账号 {username} 搜索输入框未找到或不可见。")
                driver.save_screenshot(f"search_error_{username}_{product}_round_{round_idx}.png")
                continue
            except Exception as e:
                print(f"账号 {username} 搜索过程中发生异常：{e}")
                driver.save_screenshot(f"search_error_{username}_{product}_round_{round_idx}.png")
                continue

            try:
                # 等待搜索结果加载
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.item')))
            except TimeoutException:
                print("搜索结果未加载或没有找到商品。")
                driver.save_screenshot(f"no_results_product_{product}_round_{round_idx}.png")
                continue

            # 爬指定页数
            for page in range(1, pages_per_round + 1):
                print(f"  -> 第 {page} / {pages_per_round} 页")
                try:
                    driver.execute_script("document.body.style.zoom='25%'")
                    time.sleep(3)
                    # 滚动页面，确保懒加载触发
                    scroll_to_bottom(driver, times=3, sleep_interval=2)
                    time.sleep(2)  # 等待内容加载

                    page_source = driver.page_source
                    doc = pq(page_source)  # 定义 doc 对象

                    # 使用显式等待确保商品元素加载
                    items = doc('div.content--CUnfXXxv > div > div').items()  # 使用正确的选择器

                    for it in items:
                        try:
                            info = parse_item_info(it)
                            info['round'] = round_idx
                            info['page'] = page
                            info['search_keyword'] = product
                            info['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")  # 添加时间戳
                            
                            # 检查价格变化
                            if round_idx > 1:
                                # 查找该商品之前的价格
                                prev_price = next((item['price'] for item in all_round_data 
                                                 if item['t_url'] == info['t_url'] 
                                                 and item['round'] == round_idx - 1), None)
                                if prev_price:
                                    info['price_change'] = float(info['price']) - float(prev_price)
                                    if info['price_change'] != 0:
                                        print(f"     价格变化检测：{info['title']} 价格变化 {info['price_change']:.2f} 元")
                            else:
                                info['price_change'] = 0
                            
                            round_data.append(info)
                        except Exception as e:
                            print(f"     解析商品出错: {e}")
                            driver.save_screenshot(f"parse_error_{username}_page_{page}_round_{round_idx}.png")

                    # 点击下一页
                    if page < pages_per_round:
                        try:
                            # 尝试国内版下一页按钮
                            next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-content-leftWrap"]/div[3]/div[5]/div/div/button[2]/span')))
                        except TimeoutException:
                            try:
                                # 如果国内版按钮未找到，尝试国际版下一页按钮
                                next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-content-leftWrap"]/div[2]/div[4]/div/div/button[2]/span')))
                            except TimeoutException:
                                print("     未找到下一页按钮，提前结束翻页。")
                                break

                        try:
                            next_btn.click()
                            time.sleep(3)  # 等待下一页加载
                        except ElementNotInteractableException:
                            print("     下一页按钮不可交互，可能已到最后一页。")
                            break
                        except Exception as e:
                            print(f"     点击下一页时发生异常：{e}")
                            driver.save_screenshot(f"next_page_error_page_{page}_product_{product}_round_{round_idx}.png")
                            break
                except Exception as e:
                    print(f"  -> 翻页过程中发生异常：{e}")
                    driver.save_screenshot(f"pagination_error_page_{page}_product_{product}_round_{round_idx}.png")
                    break

            all_round_data.extend(round_data)

            # 如果不是最后一轮，则等待 interval_seconds
            if round_idx < crawl_rounds:
                print(f" -> 第 {round_idx} 轮结束，等待 {interval_seconds} 秒...")
                time.sleep(interval_seconds)

    # 使用锁确保线程安全的 Excel 写入
    with excel_lock:
        headers = [
            "round", "page", "search_keyword", "title", "price", "price_change",
            "deal", "location", "shop", "postText", "t_url", "shop_url", "img_url", "timestamp"
        ]
        try:
            # 清理无效字符并截断工作表名称
            sheet_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in username)[:31]
            save_to_excel(output_file, sheet_name, all_round_data, headers)
            print(f"账号 {username} 数据已保存到 {output_file}")
        except Exception as e:
            print(f"保存 Excel 时发生异常：{e}")
            driver.save_screenshot(f"save_excel_error_{username}.png")

    driver.quit()
