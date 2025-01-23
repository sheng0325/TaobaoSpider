# tasks/task4.py

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .utils import (
    init_webdriver,
    login_taobao,
    scroll_to_bottom,
    save_to_excel
)

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

    driver = init_webdriver(driver_path, headless)

    for idx in accounts_index:
        account = accounts[idx]
        username = account['username']
        password = account['password']
        acc_type = account['type']

        print(f"=== 正在使用账号索引: {idx}, type: {acc_type}, username: {username} ===")
        login_taobao(driver, username, password, manual_verify_wait)

        print("正在执行：访问淘宝首页")
        driver.get("https://www.taobao.com/")
        time.sleep(3)

        print(f" -> 向下滚动页面 {scroll_times} 次，以触发懒加载...")
        scroll_to_bottom(driver, times=scroll_times, sleep_interval=2)

        # 示例：抓取首页推荐信息，需要自行研究选择器
        all_recommend_data = []
        try:
            # 这里的 .some-recommend-class 仅示例，需要根据真实页面做适配
            recommended_items = driver.find_elements(By.CSS_SELECTOR, '.some-recommend-class')
            for item in recommended_items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, '.recommend-title').text
                    price = item.find_element(By.CSS_SELECTOR, '.recommend-price').text
                    link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    all_recommend_data.append({
                        "title": title,
                        "price": price,
                        "link": link
                    })
                except Exception as e:
                    print("解析推荐商品出错：", e)
        except NoSuchElementException:
            print("没有找到首页推荐商品模块，请检查选择器")

        # 写Excel
        headers = ["title", "price", "link"]
        save_to_excel(output_file, acc_type, all_recommend_data, headers)

    driver.quit()
    print("===== 任务4执行完毕 =====")
