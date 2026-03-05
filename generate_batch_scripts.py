#!/usr/bin/env python3
"""
批量生成 Freqtrade 策略测试脚本 (批次 27-45)
基于 ALL_STRATEGIES_FIX_PLAN.md 文档自动生成
"""

import re
import os
from pathlib import Path


def extract_strategies_from_docs(doc_file: str) -> dict:
    """从文档中提取所有批次策略"""
    with open(doc_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 查找批次表格
    batch_pattern = r"### .*第(\d+)批.*\n\n\|.*\n\|[-:|]+\n((?:\|.*\n)+)"
    batches = re.findall(batch_pattern, content)

    strategies_by_batch = {}

    for batch_num, table_content in batches:
        batch_num = int(batch_num)

        # 提取策略行
        strategy_pattern = r"\| (\d+) \| (\w+) \|"
        strategies = re.findall(strategy_pattern, table_content)

        # 只保留本批次的策略
        batch_strategies = []
        for num, name in strategies:
            num = int(num)
            # 计算批次范围: 每批10个策略
            batch_start = ((batch_num - 1) * 10) + 1
            batch_end = batch_num * 10

            if batch_start <= num <= batch_end:
                batch_strategies.append(name)

        if batch_strategies:
            strategies_by_batch[batch_num] = batch_strategies

    return strategies_by_batch


def generate_batch_script(
    batch_num: int, strategies: list, template_file: str = None
) -> str:
    """生成批次测试脚本"""
    if template_file and os.path.exists(template_file):
        with open(template_file, "r") as f:
            template = f.read()
    else:
        template = """#!/bin/bash
# Batch {batch_num} strategies test script (#{start_num}-{end_num})
# Created: 2026-03-05

set -e

# Configuration
TEST_DIR="/home/neozh/freqtrade-strategies/test"
RESULTS_DIR="${{TEST_DIR}}/test_results_batch{batch_num}"
LOG_DIR="${{RESULTS_DIR}}/logs"
mkdir -p "${{RESULTS_DIR}}" "${{LOG_DIR}}"

# List of strategies in Batch {batch_num}
declare -a STRATEGIES=(
{strategy_list}
)

echo "Starting Batch {batch_num} testing (strategies #{start_num}-{end_num})"
echo "Total strategies: ${{#STRATEGIES[@]}}"
echo "Results will be saved to: ${{RESULTS_DIR}}"
echo ""

# Clear previous results
echo "" > "${{RESULTS_DIR}}/results.csv"
echo "Strategy,Status,Trades,Profit%,ProfitUSDT,WinRate%,Duration(s)" > "${{RESULTS_DIR}}/results.csv"

# Common backtesting configuration
CONFIG_FILE="${{TEST_DIR}}/config.json"
TIMERANGE="20250101-20250301"

# Test each strategy
for STRATEGY in "${{STRATEGIES[@]}}"; do
    echo "Testing strategy: ${{STRATEGY}}"
    
    # Start timer
    START_TIME=$(date +%s)
    
    # Run Docker command with timeout
    DOCKER_CMD="docker run --rm \\
        -v $(pwd)/test:/work/freqtrade_test \\
        -v $(pwd)/strategies:/work/freqtrade_test/user_data/strategies \\
        freqtrade-full:latest \\
        backtesting --config /work/freqtrade_test/config.json \\
        --strategy ${{STRATEGY}} \\
        --timerange ${{TIMERANGE}} \\
        --timeframe 5m \\
        --pairs LTC/USDT:USDT BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT XRP/USDT:USDT ADA/USDT:USDT DOGE/USDT:USDT TRX/USDT:USDT DOT/USDT:USDT"
    
    # Execute with timeout
    timeout 30s bash -c "${{DOCKER_CMD}}" > "${{LOG_DIR}}/${{STRATEGY}}.log" 2>&1 || true
    
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    # Parse results from log
    if grep -q "No data found" "${{LOG_DIR}}/${{STRATEGY}}.log"; then
        STATUS="NO_DATA"
        TRADES=0
        PROFIT_PERCENT=""
        PROFIT_USDT=""
        WIN_RATE=""
    elif grep -q "Backtest completed successfully" "${{LOG_DIR}}/${{STRATEGY}}.log"; then
        STATUS="SUCCESS"
        
        # Extract trades
        TRADES_LINE=$(grep "Total trades" "${{LOG_DIR}}/${{STRATEGY}}.log" | tail -1)
        if [ -n "$TRADES_LINE" ]; then
            TRADES=$(echo "$TRADES_LINE" | grep -oE '[0-9]+' | head -1)
        else
            TRADES=0
        fi
        
        # Extract profit percentage
        PROFIT_LINE=$(grep "Total profit %" "${{LOG_DIR}}/${{STRATEGY}}.log" | tail -1)
        if [ -n "$PROFIT_LINE" ]; then
            PROFIT_PERCENT=$(echo "$PROFIT_LINE" | grep -oE '[+-]?[0-9]+\.?[0-9]*' | head -1)
        else
            PROFIT_PERCENT=""
        fi
        
        # Extract profit USDT
        PROFIT_USDT_LINE=$(grep "Total profit USDT" "${{LOG_DIR}}/${{STRATEGY}}.log" | tail -1)
        if [ -n "$PROFIT_USDT_LINE" ]; then
            PROFIT_USDT=$(echo "$PROFIT_USDT_LINE" | grep -oE '[+-]?[0-9]+\.?[0-9]*' | head -1)
        else
            PROFIT_USDT=""
        fi
        
        # Extract win rate
        WIN_RATE_LINE=$(grep "Win Rate" "${{LOG_DIR}}/${{STRATEGY}}.log" | tail -1)
        if [ -n "$WIN_RATE_LINE" ]; then
            WIN_RATE=$(echo "$WIN_RATE_LINE" | grep -oE '[0-9]+\.?[0-9]*' | head -1)
        else
            WIN_RATE=""
        fi
    elif grep -q "Impossible to load Strategy" "${{LOG_DIR}}/${{STRATEGY}}.log"; then
        STATUS="LOAD_ERROR"
        TRADES=0
        PROFIT_PERCENT=""
        PROFIT_USDT=""
        WIN_RATE=""
    elif grep -q "Strategy caused" "${{LOG_DIR}}/${{STRATEGY}}.log"; then
        STATUS="STRATEGY_ERROR"
        TRADES=0
        PROFIT_PERCENT=""
        PROFIT_USDT=""
        WIN_RATE=""
    else
        STATUS="UNKNOWN_ERROR"
        TRADES=0
        PROFIT_PERCENT=""
        PROFIT_USDT=""
        WIN_RATE=""
    fi
    
    # Save results
    echo "${{STRATEGY}},${{STATUS}},${{TRADES}},${{PROFIT_PERCENT}},${{PROFIT_USDT}},${{WIN_RATE}},${{DURATION}}" >> "${{RESULTS_DIR}}/results.csv"
    
    echo "  Status: ${{STATUS}}, Duration: ${{DURATION}}s"
    
    # Brief pause to prevent overwhelming
    sleep 1
done

echo ""
echo "Batch {batch_num} testing completed!"
echo "Results saved to: ${{RESULTS_DIR}}/results.csv"
echo ""
echo "Summary:"
tail -n +2 "${{RESULTS_DIR}}/results.csv" | awk -F, '{{print $1 ": " $2}}'
"""

    start_num = ((batch_num - 1) * 10) + 1
    end_num = batch_num * 10

    strategy_list = "\n".join([f'    "{s}"' for s in strategies])

    return template.format(
        batch_num=batch_num,
        start_num=start_num,
        end_num=end_num,
        strategy_list=strategy_list,
    )


def main():
    doc_file = "ALL_STRATEGIES_FIX_PLAN.md"
    test_dir = Path("test")

    print("提取策略信息...")
    strategies_by_batch = extract_strategies_from_docs(doc_file)

    print(f"找到 {len(strategies_by_batch)} 个批次")

    # 生成批次 27-45 的测试脚本
    for batch_num in range(27, 46):
        if batch_num in strategies_by_batch:
            strategies = strategies_by_batch[batch_num]
            print(f"生成批次 {batch_num}: {len(strategies)} 个策略")

            script_content = generate_batch_script(batch_num, strategies)

            script_file = test_dir / f"test_batch{batch_num}_strategies.sh"

            with open(script_file, "w", encoding="utf-8") as f:
                f.write(script_content)

            # 设置执行权限
            os.chmod(script_file, 0o755)

            print(f"  保存到: {script_file}")
        else:
            print(f"⚠️  批次 {batch_num} 未找到策略信息")


if __name__ == "__main__":
    main()
