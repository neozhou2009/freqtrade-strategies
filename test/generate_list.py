import pandas as pd
import math

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

def generate_markdown_list(csv_file, output_file):
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Sort by profit_total_pct descending, putting errors at the end
    # Create a helper column for sorting
    df['sort_val'] = pd.to_numeric(df['profit_total_pct'], errors='coerce').fillna(-999999)
    df = df.sort_values(by='sort_val', ascending=False)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 100个策略测试结果列表说明\n\n")
        f.write("以下列表按**总收益率**从高到低排序。对于未能运行的策略，列在最后。\n\n")
        
        f.write("| 排名 | 策略名称 | 状态 | 总收益率 | 胜率 | 交易次数 | 夏普比率 | 最大回撤 | 说明 |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")

        rank = 1
        for index, row in df.iterrows():
            name = row['key']
            status = row['status']
            error = row['error']
            
            # Status icon
            if pd.isna(status) or status == '':
                status_icon = "✅ 成功"
                # Check profit to determine if it's good or bad
                profit = float(row['profit_total_pct'])
                if profit > 0:
                    desc = "盈利策略"
                else:
                    desc = "亏损策略"
            else:
                status_icon = "❌ 失败"
                desc = f"运行出错: {str(error)[:20]}..." if pd.notna(error) else "运行出错"

            # Metrics
            profit_str = format_percentage(row['profit_total_pct'])
            winrate_str = format_percentage(float(row['winrate']) * 100) if pd.notna(row['winrate']) else "N/A"
            trades_str = str(int(row['trades'])) if pd.notna(row['trades']) else "N/A"
            sharpe_str = format_float(row['sharpe'])
            drawdown_str = format_percentage(float(row['max_drawdown_account']) * 100) if pd.notna(row['max_drawdown_account']) else "N/A"

            # Highlight logic
            if pd.isna(status) or status == '':
                if float(row['profit_total_pct']) > 3.0:
                    name = f"**{name}** (推荐)"
                elif float(row['profit_total_pct']) < -5.0:
                    name = f"~~{name}~~ (不推荐)"

            f.write(f"| {rank} | {name} | {status_icon} | {profit_str} | {winrate_str} | {trades_str} | {sharpe_str} | {drawdown_str} | {desc} |\n")
            rank += 1

    print(f"Successfully generated {output_file}")

if __name__ == "__main__":
    generate_markdown_list('strategy_evaluation.csv', 'strategy_list_100.md')
