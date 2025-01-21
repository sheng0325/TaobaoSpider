# main.py
from settings import get_driver, auto_login, load_accounts, load_config
import crawler

if __name__ == '__main__':
    # 1. 加载配置
    config = load_config('config.yaml')
    print(f"当前任务: {config['task']['id']}")
    
    # 2. 加载账号
    all_accounts = load_accounts('accounts.json')
    selected_indices = [i-1 for i in config['task']['accounts']]
    selected_accounts = [all_accounts[i] for i in selected_indices]
    
    print("已选择的账号：")
    for acc in selected_accounts:
        print(f"- {acc['username']} ({acc['type']})")

    # 3. 执行任务
    crawler.main(selected_accounts, config)