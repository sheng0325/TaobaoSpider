# tasks/task2.py

import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .utils import (
    init_webdriver,
    login_taobao,
    scroll_to_bottom,
    parse_item_info,
    save_to_excel
)

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

    driver = init_webdriver(driver_path, headless)

    for idx in accounts_index:
        account = accounts[idx]
        username = account['username']
        password = account['password']
        acc_type = account['type']

        print(f"=== 正在使用账号索引: {idx}, type: {acc_type}, username: {username} ===")
        login_taobao(driver, username, password, manual_verify_wait)

        all_round_data = []

        for round_idx in range(1, crawl_rounds + 1):
            print(f" -> 第 {round_idx} 轮爬取开始")
            round_data = []

            for product in products:
                print(f"    搜索商品：{product}")
                driver.get("https://s.taobao.com/")
                time.sleep(2)

                search_input = driver.find_element(By.ID, "q")
                search_input.clear()
                search_input.send_keys(product)
                search_input.send_keys(Keys.ENTER)
                time.sleep(3)

                # 爬指定页数
                for page in range(1, pages_per_round + 1):
                    print(f"      第 {page} 页")
                    scroll_to_bottom(driver, times=3, sleep_interval=1)
                    time.sleep(2)

                    items = driver.find_elements(By.CSS_SELECTOR, '.item--JmQgoMU7')
                    print(f"      发现商品数：{len(items)}")
                    for it in items:
                        try:
                            info = parse_item_info(it)
                            info['round'] = round_idx
                            info['page'] = page
                            info['search_keyword'] = product
                            round_data.append(info)
                        except Exception as e:
                            print(f"      解析商品出错: {e}")

                    # 需要翻页可以在这里加，如果 pages_per_round>1，就点下一页
                    # 本示例默认 pages_per_round=1，就不翻页了

            all_round_data.extend(round_data)

            # 如果不是最后一轮，则等待 interval_seconds
            if round_idx < crawl_rounds:
                print(f" -> 第 {round_idx} 轮结束，等待 {interval_seconds} 秒...")
                time.sleep(interval_seconds)

        # 写Excel
        headers = [
            "round", "page", "search_keyword", "title", "price",
            "deal", "location", "shop", "postText", "t_url", "shop_url", "img_url"
        ]
        save_to_excel(output_file, acc_type, all_round_data, headers)

    driver.quit()
    print("===== 任务2执行完毕 =====")
