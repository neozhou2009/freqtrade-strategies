import pandas as pd
import os

CSV_FILE = "strategy_evaluation_2025.csv"
OUTPUT_FILE = "strategy_report_2025_full_year.md"

def format_percentage(val):
    if pd.isna(val) or val == '':
        return "N/A"
    try:
        return f"{float(val):.2f}%"
    except:
        return str(val)

def format_float(val):
    if pd.isna(val) or val == '':
        return "N/A"
    try:
        return f"{float(val):.2f}"
    except:
        return str(val)

def generate_report():
    if not os.path.exists(CSV_FILE):
        print(f"File {CSV_FILE} not found.")
        return

    df = pd.read_csv(CSV_FILE)
    
    # Deduplicate by key, keeping the last one (assuming latest run is best)
    # But actually they should be identical if inputs are same.
    df = df.drop_duplicates(subset=['key'])

    # Filter valid results
    if 'status' in df.columns:
        valid_df = df[pd.to_numeric(df['profit_total_pct'], errors='coerce').notna()].copy()
    else:
        valid_df = df.copy()

    # Sort
    valid_df['sort_val'] = pd.to_numeric(valid_df['profit_total_pct'], errors='coerce').fillna(-999999)
    valid_df = valid_df.sort_values(by='sort_val', ascending=False)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 2025全年回测结果报告\n\n")
        f.write("- **测试周期:** 2025-01-01 至 2025-12-31\n")
        f.write("- **数据周期:** 5分钟 (5m)\n")
        f.write(f"- **已完成策略:** {len(valid_df)}\n\n")
        
        f.write("## 🏆 表现最佳策略 (Top 10)\n\n")
        f.write("| 排名 | 策略名称 | 总收益率 | 胜率 | 交易次数 | 夏普比率 | 最大回撤 | 评价 |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        
        rank = 1
        for index, row in valid_df.iterrows():
            name = row['key']
            profit_val = float(row['profit_total_pct'])
            profit = format_percentage(profit_val)
            winrate = format_percentage(float(row['winrate']) * 100) if pd.notna(row['winrate']) else "N/A"
            trades = str(int(row['trades'])) if pd.notna(row['trades']) else "N/A"
            sharpe = format_float(row['sharpe'])
            drawdown = format_percentage(float(row['max_drawdown_account']) * 100) if pd.notna(row['max_drawdown_account']) else "N/A"
            
            note = ""
            if profit_val > 20:
                note = "✅ 优秀"
            elif profit_val > 0:
                note = "🆗 盈利"
            else:
                note = "🔻 亏损"
            
            # Write all rows to the main table, but maybe split top 10 for summary
            if rank <= 10:
                f.write(f"| {rank} | **{name}** | {profit} | {winrate} | {trades} | {sharpe} | {drawdown} | {note} |\n")
            
            rank += 1
            
        f.write("\n## 完整列表 (按收益率排序)\n\n")
        f.write("| 序号 | 策略名称 | 总收益率 | 胜率 | 交易次数 | 夏普比率 | 最大回撤 | 备注 |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        
        rank = 1
        for index, row in valid_df.iterrows():
            name = row['key']
            profit_val = float(row['profit_total_pct'])
            profit = format_percentage(profit_val)
            winrate = format_percentage(float(row['winrate']) * 100) if pd.notna(row['winrate']) else "N/A"
            trades = str(int(row['trades'])) if pd.notna(row['trades']) else "N/A"
            sharpe = format_float(row['sharpe'])
            drawdown = format_percentage(float(row['max_drawdown_account']) * 100) if pd.notna(row['max_drawdown_account']) else "N/A"
            
            note = ""
            if profit_val > 20:
                note = "✅ 优秀"
            elif profit_val < 0:
                note = "🔻 亏损"
                
            f.write(f"| {rank} | {name} | {profit} | {winrate} | {trades} | {sharpe} | {drawdown} | {note} |\n")
            rank += 1

    print(f"Generated {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_report()
