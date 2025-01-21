# excel_utils.py
import openpyxl as op
import time
import os

def create_workbook(title_list):
    wb = op.Workbook()
    ws = wb.active
    # 写入表头
    for col, title in enumerate(title_list, start=1):
        ws.cell(row=1, column=col, value=title)
    return wb, ws

def save_workbook(wb, filename_prefix="Task"):
    timestamp = time.strftime('%Y%m%d-%H%M', time.localtime())
    filename = f"{filename_prefix}_{timestamp}.xlsx"
    # Ensure the excel directory exists
    os.makedirs("excel", exist_ok=True)
    # Save to the excel directory
    filepath = os.path.join("excel", filename)
    wb.save(filepath)
    print(f"Excel 已保存: {filepath}")