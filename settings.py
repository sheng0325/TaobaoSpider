# settings.py
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_accounts(file_path='accounts.json'):
    """
    从本地JSON文件中加载所有账号
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def choose_accounts(accounts):
    """
    一次可选择多个账号，使用逗号分隔输入
    """
    print("可选择的账号如下：")
    for i, acc in enumerate(accounts, start=1):
        print(f"{i}. {acc['username']} ({acc['type']})")

    choice = input("请输入要使用的账号序号(可用逗号分隔，如 1,2): ").strip()
    if not choice:
        print("未选择任何账号，即将退出...")
        return []

    selected_indices = []
    for c in choice.split(','):
        c = c.strip()
        if c.isdigit():
            idx = int(c)
            if 1 <= idx <= len(accounts):
                selected_indices.append(idx-1)
    # 返回选中的账号列表
    return [accounts[i] for i in selected_indices]

def get_driver():
    """
    返回一个新的Chrome driver实例，附带反爬配置
    """
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=options)
    # 隐藏webdriver特征
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""}
    )
    return driver

def auto_login(driver, username, password):
    """
    自动登录淘宝
    """
    wait = WebDriverWait(driver, 15)
    driver.get("https://login.taobao.com/")
    # 等待用户名和密码输入框
    user_input = wait.until(EC.presence_of_element_located((By.ID, "fm-login-id")))
    pwd_input = wait.until(EC.presence_of_element_located((By.ID, "fm-login-password")))

    user_input.clear()
    user_input.send_keys(username)
    pwd_input.clear()
    pwd_input.send_keys(password)

    # 点击登录按钮
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".fm-btn button")))
    login_btn.click()

    # 给一些时间处理可能的验证码/滑块
    time.sleep(10)

    # 判断是否成功登录(简易判断)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#J_SiteNavMytaobao")))
        print(f"[{username}] 登录成功!")
    except:
        print(f"[{username}] 登录可能需要验证码或滑块，请手动处理或检查账号密码~")