# tasks/task3.py

import time
import pandas as pd
import threading
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from typing import Dict, List, Any
from .utils import (
    init_webdriver,
    login_taobao,
    scroll_to_bottom,
    save_to_excel
)

# 创建全局锁确保 Excel 写入安全
excel_lock = threading.Lock()

class CommentScraper:
    """商品评论采集器"""
    
    def __init__(self, config: Dict[str, Any], accounts: List[Dict[str, str]]):
        self.config = config
        self.accounts = accounts
        self.task_cfg = config['task3']
        self.global_cfg = config['global']
        
    def run(self) -> None:
        """运行评论采集任务"""
        print("===== 开始执行任务3：商品评论数据采集 =====")
        
        # 使用线程池并行处理账号
        with ThreadPoolExecutor(max_workers=len(self.task_cfg['accounts_index'])) as executor:
            futures = [
                executor.submit(
                    self._process_account,
                    self.accounts[idx],
                    self.task_cfg['output_file'],
                    self.task_cfg.get('max_comments', 300)
                )
                for idx in self.task_cfg['accounts_index']
            ]
            
            # 等待所有任务完成
            for future in futures:
                try:
                    future.result(timeout=300)  # 5分钟超时
                except Exception as e:
                    print(f"任务执行失败: {e}")
                    
        print("===== 任务3执行完毕 =====")

    def _process_account(self, account: Dict[str, str], output_file: str, max_comments: int) -> None:
        """处理单个账号的评论采集"""
        driver = self._init_driver()
        if not driver:
            return
            
        try:
            if not self._login(driver, account):
                return
                
            product_data = self._load_product_data(account['username'])
            if not product_data:
                return
                
            comments = self._collect_comments(driver, product_data, max_comments)
            self._save_comments(account['username'], output_file, comments)
            
        finally:
            driver.quit()

    def _init_driver(self):
        """初始化WebDriver"""
        try:
            return init_webdriver(
                self.global_cfg['driver_path'],
                self.global_cfg['headless']
            )
        except Exception as e:
            print(f"初始化 WebDriver 失败: {e}")
            return None

    def _login(self, driver, account: Dict[str, str]) -> bool:
        """登录淘宝账号"""
        try:
            login_taobao(
                driver,
                account['username'],
                account['password'],
                self.global_cfg['manual_verify_wait']
            )
            return True
        except Exception as e:
            print(f"登录过程中发生异常：{e}")
            driver.save_screenshot(f"login_error_{account['username']}.png")
            return False

    def _load_product_data(self, username: str) -> List[Dict[str, str]]:
        """加载task1的商品数据"""
        try:
            df = pd.read_excel("./outputs/task1_output.xlsx", sheet_name=username)
            return list(zip(
                df['t_url'].dropna().unique(),
                df['title'].dropna().unique()
            ))
        except Exception as e:
            print(f"读取task1数据失败: {e}")
            return []

    def _collect_comments(self, driver, product_data: List[Dict[str, str]], max_comments: int) -> List[Dict[str, str]]:
        """采集商品评论"""
        all_comments = []
        wait = WebDriverWait(driver, 20)
        
        for product_url, product_name in product_data:
            print(f"正在采集商品评论：{product_name}")
            try:
                # 访问商品页面并设置缩放
                cleaned_url = product_url.replace("//", "") if product_url.startswith("//") else product_url
                driver.get(f"https:{cleaned_url}")
                driver.execute_script("document.body.style.zoom='50%'")
                time.sleep(3)

                # 导航到评论页面并设置缩放
                self._navigate_to_comments(driver, wait)
                driver.execute_script("document.body.style.zoom='50%'")
                time.sleep(1)
                
                # 采集评论
                comments = self._scroll_and_collect(driver, product_name, max_comments - len(all_comments))
                all_comments.extend(comments)
                
            except Exception as e:
                print(f"采集商品评论时发生异常：{e}")
                driver.save_screenshot(f"comment_error_{product_name}.png")
                continue  # 继续下一个商品
                
        return all_comments

    def _navigate_to_comments(self, driver, wait) -> None:
        """导航到评论页面"""
        # 尝试天猫的评论标签
        try:
            print("尝试天猫评论页面导航...")
            driver.save_screenshot("before_tmall_click.png")
            
            # 点击商品详情标签
            detail_tab = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="titleTabs"]/div/div[1]/div[1]/span')))
            driver.execute_script("arguments[0].scrollIntoView(true);", detail_tab)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", detail_tab)
            print("成功点击商品详情标签")
            time.sleep(2)
            driver.save_screenshot("after_detail_click.png")

            # 尝试第一种评论标签选择器
            try:
                comment_tab = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="ice-container"]/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div')))
                driver.execute_script("arguments[0].scrollIntoView(true);", comment_tab)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", comment_tab)
                print("成功点击评论标签（选择器1）")
                time.sleep(3)
                driver.save_screenshot("after_comment_click_selector1.png")
            except:
                # 尝试第二种评论标签选择器
                try:
                    comment_tab = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '#ice-container > div > div.main--XyozDD28 > div.pageContentWrap > div > div > div.detailInfoWrap--XXyEmkTY > div > div.tabDetailWrap--UUPrzQbC > div:nth-child(1) > div > div.footer--h5lcc85O > div')))
                    driver.execute_script("arguments[0].scrollIntoView(true);", comment_tab)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", comment_tab)
                    print("成功点击评论标签（选择器2）")
                    time.sleep(3)
                    driver.save_screenshot("after_comment_click_selector2.png")
                except Exception as e:
                    print(f"两种评论标签选择器都失败: {e}")
                    driver.save_screenshot("comment_tab_error.png")
                    raise
            
        except Exception as e:
            print(f"天猫页面导航失败: {e}")
            driver.save_screenshot("tmall_nav_error.png")
            
            # 如果天猫的标签失败，尝试淘宝的标签
            try:
                print("尝试淘宝评论页面导航...")
                driver.save_screenshot("before_taobao_click.png")
                
                # 点击用户评论标签
                comment_tab = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="titleTabs"]/div/div[1]/div[1]/span')))
                driver.execute_script("arguments[0].scrollIntoView(true);", comment_tab)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", comment_tab)
                print("成功点击用户评论标签")
                time.sleep(2)
                driver.save_screenshot("after_comment_tab_click.png")

                # 点击全部评价
                all_comments = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="ice-container"]/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[4]/div')))
                driver.execute_script("arguments[0].scrollIntoView(true);", all_comments)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", all_comments)
                print("成功点击全部评价")
                time.sleep(2)
                driver.save_screenshot("after_all_comments_click.png")
                
            except Exception as e:
                print(f"淘宝页面导航失败: {e}")
                driver.save_screenshot("taobao_nav_error.png")
                raise

    def _scroll_and_collect(self, driver, product_name: str, max_comments: int) -> List[Dict[str, str]]:
        """滚动页面并采集评论"""
        comments = []
        wait = WebDriverWait(driver, 20)
        
        while len(comments) < max_comments:
            try:
                # 定位精确的滚动区域
                try:
                    # 等待页面完全加载
                    time.sleep(2)
                    # 检查页面是否包含评论区域
                    if not driver.execute_script("return document.querySelector('body > div.leftDrawer--4H_p9fnt > div.content--ew3Y4lVg > div > div.comments--vOMSBfi2.beautify-scroll-bar')"):
                        print("未找到评论区域，尝试重新加载页面")
                        driver.refresh()
                        time.sleep(3)
                        driver.execute_script("document.body.style.zoom='50%'")
                        
                    # 等待评论区域加载
                    scroll_div = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'body > div.leftDrawer--4H_p9fnt > div.content--ew3Y4lVg > div > div.comments--vOMSBfi2.beautify-scroll-bar')))
                    
                    # 确保评论区域可见
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", scroll_div)
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"无法定位滚动区域: {e}")
                    driver.save_screenshot(f"scroll_error_{product_name}.png")
                    continue  # 继续下一个商品
                
                # 获取滚动区域信息
                current_scroll = driver.execute_script("return arguments[0].scrollTop", scroll_div)
                total_height = driver.execute_script("return arguments[0].scrollHeight", scroll_div)
                client_height = driver.execute_script("return arguments[0].clientHeight", scroll_div)
                print(f"滚动区域信息：scrollTop={current_scroll}, scrollHeight={total_height}, clientHeight={client_height}")
                
                # 检查是否有评论内容
                if total_height <= client_height:
                    print("评论区域可能未加载完整，尝试重新加载")
                    driver.refresh()
                    time.sleep(3)
                    driver.execute_script("document.body.style.zoom='50%'")
                    continue
                
                # 模拟鼠标滚动
                for attempt in range(3):  # 最多重试3次
                    # 计算每次滚动的距离
                    scroll_distance = client_height * 0.8
                    driver.execute_script(f"arguments[0].scrollBy(0, {scroll_distance})", scroll_div)
                    time.sleep(1.5)  # 等待加载
                    
                    # 检查是否滚动成功
                    new_scroll = driver.execute_script("return arguments[0].scrollTop", scroll_div)
                    print(f"滚动尝试 {attempt + 1}：scrollTop={new_scroll}")
                    
                    if new_scroll > current_scroll:
                        break
                    else:
                        print("滚动失败，正在重试...")
                
                if new_scroll <= current_scroll:
                    print("无法继续滚动，可能已到达底部")
                    break
                    
                # 获取评论元素
                try:
                    # 等待评论加载
                    time.sleep(2)
                    # 检查评论容器是否存在
                    comment_container = driver.execute_script("""
                        return document.querySelector('body > div.leftDrawer--4H_p9fnt > div.content--ew3Y4lVg > div > div.comments--vOMSBfi2.beautify-scroll-bar');
                    """)
                    if not comment_container:
                        print("评论容器未找到")
                        continue
                        
                    # 获取评论元素
                    comment_elements = wait.until(EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, 'div.comments--vOMSBfi2.beautify-scroll-bar > div')))
                    
                    print(f"找到 {len(comment_elements)} 条评论")
                    
                    if not comment_elements:
                        print("未找到任何评论元素，尝试重新加载")
                        driver.refresh()
                        time.sleep(3)
                        driver.execute_script("document.body.style.zoom='50%'")
                        continue
                        
                    # 打印第一条评论的HTML结构用于调试
                    first_comment_html = driver.execute_script("""
                        return arguments[0].outerHTML;
                    """, comment_elements[0])
                    print(f"第一条评论HTML结构：\n{first_comment_html[:500]}...")
                    
                except Exception as e:
                    print(f"获取评论元素失败: {e}")
                    driver.save_screenshot(f"comment_error_{product_name}.png")
                    continue
                
                for comment_element in comment_elements:
                    if len(comments) >= max_comments:
                        break
                        
                    try:
                        # 提取评论内容
                        content = comment_element.find_element(
                            By.CSS_SELECTOR, 'div.content--FpIOzHeP').text
                        meta = comment_element.find_element(
                            By.CSS_SELECTOR, 'div.meta--TDfRej2n').text
                        print(f"找到评论内容: {content[:20]}...")
                        
                        date = meta.split('·')[0].strip()
                        comments.append({
                            "product_name": product_name,
                            "comment": content,
                            "comment_date": date
                        })
                    except Exception as e:
                        print(f"解析评论出错: {e}")
                        continue
                        
            except Exception as e:
                print(f"评论采集过程中发生错误: {e}")
                driver.save_screenshot("comment_collection_error.png")
                break
                
        return comments

    def _save_comments(self, username: str, output_file: str, comments: List[Dict[str, str]]) -> None:
        """保存评论数据"""
        with excel_lock:
            headers = ["product_name", "comment", "comment_date"]
            try:
                sheet_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in username)[:31]
                save_to_excel(output_file, sheet_name, comments, headers)
                print(f"账号 {username} 评论数据已保存到 {output_file}")
            except Exception as e:
                print(f"保存评论数据时发生异常：{e}")
                driver.save_screenshot(f"save_comment_error_{username}.png")

def run_task3(config: Dict[str, Any], accounts: List[Dict[str, str]]) -> None:
    """任务3入口函数"""
    scraper = CommentScraper(config, accounts)
    scraper.run()
