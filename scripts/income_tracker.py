#!/usr/bin/env python3
\"\"\"AI收益追踪器 - 记录各平台收益数据\"\"\"

import json
import os
from datetime import datetime
from typing import Dict, List

DATA_FILE = "data/income_data.json"

def init_data_file():
    \"\"\"初始化数据文件\"\"\"
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({"records": []}, f, ensure_ascii=False, indent=2)

def add_income(platform: str, amount: float, currency: str = "CNY", note: str = ""):
    \"\"\"添加一条收益记录\"\"\"
    init_data_file()
    
    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "platform": platform,
        "amount": amount,
        "currency": currency,
        "note": note
    }
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data["records"].append(record)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f\"✅ 已添加记录：{platform} +{amount}{currency}\")
    return record

def show_summary():
    \"\"\"显示收益汇总\"\"\"
    if not os.path.exists(DATA_FILE):
        print(\"❌ 暂无收益数据\")
        return
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not data["records"]:
        print(\"❌ 暂无收益数据\")
        return
    
    # 按平台汇总
    summary: Dict[str, float] = {}
    total = 0.0
    
    print(\"\\n\" + \"=\"*50)
    print(\"📊 收益汇总\")
    print(\"=\"*50)
    
    for record in data["records"]:
        platform = record["platform"]
        amount = record["amount"]
        if platform not in summary:
            summary[platform] = 0.0
        summary[platform] += amount
        total += amount
    
    for platform, amount in summary.items():
        print(f\"{platform:15s}: ¥{amount:.2f}\")
    
    print(\"=\"*50)
    print(f\"{'总计':15s}: ¥{total:.2f}\")
    print(f\"记录数：{len(data['records'])}\")
    print(\"=\"*50 + \"\\n\")

def export_to_csv(output_file: str = "income_report.csv"):
    \"\"\"导出为CSV文件\"\"\"
    if not os.path.exists(DATA_FILE):
        print(\"❌ 暂无数据\")
        return
    
    import csv
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["date", "platform", "amount", "currency", "note"])
        writer.writeheader()
        writer.writerows(data["records"])
    
    print(f\"✅ 已导出到：{output_file}\")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='AI收益追踪器')
    parser.add_argument('--add', action='store_true', help='添加收益记录')
    parser.add_argument('--platform', type=str, help='平台名称')
    parser.add_argument('--amount', type=float, help='收益金额')
    parser.add_argument('--currency', type=str, default='CNY', help='货币类型')
    parser.add_argument('--note', type=str, default='', help='备注')
    parser.add_argument('--summary', action='store_true', help='显示汇总')
    parser.add_argument('--export', type=str, help='导出CSV文件路径')
    
    args = parser.parse_args()
    
    if args.add and args.platform and args.amount:
        add_income(args.platform, args.amount, args.currency, args.note)
    elif args.summary:
        show_summary()
    elif args.export:
        export_to_csv(args.export)
    else:
        show_summary()
        print(\"\\n使用示例：\")
        print(\"  python income_tracker.py --add --platform zhihu --amount 50 --note '盐选分成'\")
        print(\"  python income_tracker.py --summary\")
        print(\"  python income_tracker.py --export report.csv\")