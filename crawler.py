# crawler.py
from tasks.task1_price import task1_price_data
from tasks.task1_parallel import parallel_task1_price
from tasks.task2_dynamic import task2_dynamic_pricing
from tasks.task3_comments import task3_comments
from tasks.task4_homepage import task4_homepage
from tasks.task4_parallel import parallel_task4_homepage

def main(selected_accounts, config):
    """
    多任务菜单
    selected_accounts: 已经选好的账号列表
    config: 配置信息
    """
    task_id = config['task']['id']
    
    print(f"\n执行任务 {task_id}")
    
    if task_id == '1p':
        parallel_task1_price(selected_accounts, config)
    elif task_id == '1':
        task1_price_data(selected_accounts, config)
    elif task_id == '2':
        task2_dynamic_pricing(selected_accounts, config)
    elif task_id == '3':
        task3_comments(selected_accounts, config)
    elif task_id == '4':
        task4_homepage(selected_accounts, config)
    elif task_id == '4p':
        parallel_task4_homepage(selected_accounts, config)
    else:
        print("无效任务ID，请检查配置文件~")