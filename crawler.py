# crawler.py
from settings import get_driver  # 添加这行
from tasks.task1_price import task1_price_data
from tasks.task1_parallel import parallel_task1_price
from tasks.task2_dynamic import task2_dynamic_pricing
from tasks.task3_comments import task3_comments
from tasks.task4_homepage import task4_homepage

def main(selected_accounts):
    """
    多任务菜单
    selected_accounts: 已经选好的账号列表
    """
    print("======== 请选择要执行的任务 ========")
    print("1. 商品价格数据 (普通翻页)")
    print("1p. 商品价格数据 (并行多账号)")  # 新增并行选项
    print("2. 动态定价数据 (间隔30分钟)")
    print("3. 用户评论数据 (商品详情页)")
    print("4. 首页爬虫 (向下滚动加载)")
    choice = input("请输入任务编号: ")


    if choice == '1p':
        parallel_task1_price(selected_accounts)
    elif choice == '1':
        task1_price_data(selected_accounts)
    elif choice == '2':
        print("【任务2】示例省略，参考之前示例自行实现")
        task2_dynamic_pricing(selected_accounts)
    elif choice == '3':
        print("【任务3】示例省略，参考之前示例自行实现")
        task3_comments(selected_accounts)
    elif choice == '4':
        print("【任务4】示例省略，参考之前示例自行实现")
        task4_homepage(selected_accounts)
    else:
        print("无效选项，请重试~")