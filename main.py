# main.py

import sys
from tasks.utils import load_config, load_accounts
from tasks.task1 import run_task1
from tasks.task2 import run_task2
from tasks.task3 import run_task3
from tasks.task4 import run_task4

def main():
    # 1. 加载配置和账号信息
    config = load_config("config.yaml")
    accounts = load_accounts("accounts.json")

    while True:
        print("请选择要执行的任务：")
        print("1. 任务1 - 搜索商品价格数据")
        print("2. 任务2 - 动态定价数据")
        print("3. 任务3 - 用户评论数据（暂不实现）")
        print("4. 任务4 - 推荐商品数据")
        print("q. 退出程序")
        choice = input("请输入选择：").strip()

        if choice == '1':
            run_task1(config, accounts)
        elif choice == '2':
            run_task2(config, accounts)
        elif choice == '3':
            run_task3(config, accounts)
        elif choice == '4':
            run_task4(config, accounts)
        elif choice.lower() == 'q':
            print("程序退出。")
            sys.exit(0)
        else:
            print("无效输入，请重新选择。")

if __name__ == "__main__":
    main()
