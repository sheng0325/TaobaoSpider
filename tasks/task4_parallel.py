# tasks/task4_parallel.py
import time
import threading
from pyquery import PyQuery as pq

from settings import get_driver
import excel_utils

def worker_task4(acc, barrier, scroll_times, result_list):
    """
    单个账号的工作线程：
    - 登录
    - 等待用户确认
    - 开始抓取数据
    - 收集结果到result_list
    """
    driver = get_driver()
    from settings import auto_login
    auto_login(driver, acc['username'], acc['password'])

    # 打开淘宝首页
    driver.get("https://www.taobao.com/")
    time.sleep(3)
    
    print(f"\n[{acc['username']}] 请在浏览器中完成登录验证（如果需要），完成后在命令行输入任意内容继续...")
    input(f"[{acc['username']}] 按回车继续...")

    # 等待所有账号都确认完成
    barrier.wait()
    
    # 设置页面缩放为75%
    driver.execute_script("document.body.style.zoom='75%'")
    time.sleep(1)

    # 模拟向下滚动多次
    rows = []  # 收集此线程的所有抓取行
    count = 1
    
    for i in range(scroll_times):
        print(f"[{acc['username']}] 第{i+1}次向下滚动...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # 等待加载

    # 页面源码
    html = driver.page_source
    doc = pq(html)

    # 使用新的选择器来抓取商品信息
    items = doc('.tb-pick-content-item').items()
    for item in items:
        # 商品标题
        title = item.find('.info-wrapper-title-text').text()
        
        # 价格（组合单位和数值）
        price_unit = item.find('.price-unit').text()
        price_value = item.find('.price-value').text()
        price = float(price_value) if price_value else 0.0
        
        # 成交量
        deal = item.find('.month-sale').text().replace('人购买', '')
        
        # 商品链接
        t_url = item.find('.item-link').attr('href')
        
        # 商品图片
        img_url = item.find('.product-img').attr('src')
        
        # 标签信息
        tag = item.find('.tag-text').text()
        
        # 确保URL是完整的
        if t_url and t_url.startswith('//'):
            t_url = f"https:{t_url}"
        if img_url and img_url.startswith('//'):
            img_url = f"https:{img_url}"

        # 收集一行数据
        row = [
            acc['username'], count, title, price,
            deal, tag, t_url, img_url
        ]
        rows.append(row)
        count += 1

    driver.quit()
    result_list.append(rows)

def parallel_task4_homepage(selected_accounts, config):
    """
    任务4的并行版本：同时打开多个浏览器抓取数据
    """
    # 从配置中获取参数
    scroll_times = config['task']['homepage']['scroll_times']
    print(f"向下滚动次数: {scroll_times}")
    
    # 初始化同步barrier
    barrier = threading.Barrier(len(selected_accounts))
    
    # 准备收集所有线程的结果
    result_list = []
    
    # 创建并启动工作线程
    threads = []
    for acc in selected_accounts:
        t = threading.Thread(
            target=worker_task4,
            args=(acc, barrier, scroll_times, result_list)
        )
        threads.append(t)
        t.start()
    
    # 等待所有线程完成
    for t in threads:
        t.join()
    
    # 创建Excel并写入所有结果
    title_list = ["Account", "Index", "Title", "Price", "Deal", "Tag", "ItemURL", "ImgURL"]
    wb, ws = excel_utils.create_workbook(title_list)
    
    current_row = 2
    for rows in result_list:
        for row in rows:
            for col, value in enumerate(row, 1):
                ws.cell(row=current_row, column=col, value=value)
            current_row += 1
    
    # 保存Excel
    excel_utils.save_workbook(wb, filename_prefix="Task4_Homepage_Parallel")