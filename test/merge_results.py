import pandas as pd
import glob

def merge_results():
    # Read all CSV files
    files = [
        'strategy_evaluation.csv',
        'strategy_evaluation_part2.csv',
        'strategy_evaluation_part3.csv'
    ]
    
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f)
            dfs.append(df)
        except Exception as e:
            print(f"Error reading {f}: {e}")
            
    if not dfs:
        print("No data found")
        return

    # Concatenate
    full_df = pd.concat(dfs, ignore_index=True)
    
    # Save full raw data
    full_df.to_csv("strategy_evaluation_full.csv", index=False)
    print(f"Saved full data to strategy_evaluation_full.csv with {len(full_df)} rows")
    
    return full_df

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

def generate_markdown_report(df, output_file):
    # Sort
    df['sort_val'] = pd.to_numeric(df['profit_total_pct'], errors='coerce').fillna(-999999)
    df = df.sort_values(by='sort_val', ascending=False)
    
    # Separate lists
    success_df = df[df['status'].isna() | (df['status'] == '')].copy()
    error_df = df[~(df['status'].isna() | (df['status'] == ''))].copy()
    
    top_performers = success_df.head(20)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Freqtrade 全量策略测试报告\n\n")
        f.write(f"- **总测试策略数:** {len(df)}\n")
        f.write(f"- **成功运行:** {len(success_df)}\n")
        f.write(f"- **失败/无数据:** {len(error_df)}\n")
        f.write("- **测试周期:** 5分钟 (2025-12-20 ~ 2026-01-14)\n\n")
        
        f.write("## 🏆 Top 20 最佳策略\n")
        f.write("| 排名 | 策略名称 | 总收益率 | 胜率 | 交易次数 | 夏普比率 | 最大回撤 |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        
        rank = 1
        for index, row in top_performers.iterrows():
            name = row['key']
            profit = format_percentage(row['profit_total_pct'])
            winrate = format_percentage(float(row['winrate']) * 100) if pd.notna(row['winrate']) else "N/A"
            trades = str(int(row['trades'])) if pd.notna(row['trades']) else "N/A"
            sharpe = format_float(row['sharpe'])
            drawdown = format_percentage(float(row['max_drawdown_account']) * 100) if pd.notna(row['max_drawdown_account']) else "N/A"
            
            f.write(f"| {rank} | **{name}** | {profit} | {winrate} | {trades} | {sharpe} | {drawdown} |\n")
            rank += 1
            
        f.write("\n## 完整列表 (按收益排序)\n")
        f.write("| 策略名称 | 状态 | 总收益率 | 胜率 | 交易次数 | 说明 |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        for index, row in df.iterrows():
            name = row['key']
            status = row['status']
            error = row['error']
            
            if pd.isna(status) or status == '':
                status_icon = "✅"
                profit = format_percentage(row['profit_total_pct'])
                winrate = format_percentage(float(row['winrate']) * 100) if pd.notna(row['winrate']) else "N/A"
                trades = str(int(row['trades'])) if pd.notna(row['trades']) else "N/A"
                desc = "盈利" if float(row['profit_total_pct']) > 0 else "亏损"
            else:
                status_icon = "❌"
                profit = "-"
                winrate = "-"
                trades = "-"
                desc = f"{status}: {str(error)[:30]}..." if pd.notna(error) else status

            f.write(f"| {name} | {status_icon} | {profit} | {winrate} | {trades} | {desc} |\n")

    print(f"Report generated: {output_file}")

if __name__ == "__main__":
    df = merge_results()
    if df is not None:
        generate_markdown_report(df, "full_strategy_report.md")
