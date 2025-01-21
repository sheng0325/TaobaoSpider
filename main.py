# main.py
from settings import get_driver, auto_login, load_accounts, choose_accounts
import crawler

if __name__ == '__main__':
    # 1. 加载账号
    all_accounts = load_accounts('accounts.json')
    # 2. 选择多个账号
    selected_accounts = choose_accounts(all_accounts)
    if not selected_accounts:
        print("未选择账号，程序结束。")
        exit()

    # 3. 选择任务并执行
    crawler.main(selected_accounts)