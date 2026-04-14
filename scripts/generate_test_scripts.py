#!/usr/bin/env python3
"""
Generate test scripts for batches 26-45
Reads strategy names from ALL_STRATEGIES_FIX_PLAN.md
"""

import re
import os


def extract_strategy_names_from_md():
    """Extract strategy names from ALL_STRATEGIES_FIX_PLAN.md"""

    md_file = "/home/neozh/freqtrade-strategies/ALL_STRATEGIES_FIX_PLAN.md"

    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern to match batch sections
    # Example: "### ✅ 第26批 (10个) - 2026-03-03 10/10 批量完成"
    batch_pattern = (
        r"###\s*[✅⚠️❌]?\s*第(\d+)批\s*\([^)]+\)[^\n]*\n\n\|.*?\n\|.*?\n(\|.*?\n)*"
    )

    # Find all batch sections
    batches = []
    current_batch = None
    current_strategies = []

    lines = content.split("\n")
    for i, line in enumerate(lines):
        # Check for batch header
        batch_match = re.match(r"###\s*[✅⚠️❌]?\s*第(\d+)批", line)
        if batch_match:
            if current_batch is not None and current_strategies:
                batches.append((current_batch, current_strategies))
                current_strategies = []

            batch_num = int(batch_match.group(1))
            # Only care about batches 26-45
            if 26 <= batch_num <= 45:
                current_batch = batch_num
            else:
                current_batch = None
            continue

        # Look for strategy table rows
        if current_batch is not None and line.startswith("|"):
            # Extract strategy name from table row
            # Format: "| 251 | MultiMa | MultiMa/MultiMa.py | ✅ | qtpylib + ... |"
            parts = line.split("|")
            if len(parts) >= 3:
                strategy_name = parts[2].strip()
                if (
                    strategy_name
                    and not strategy_name.isdigit()
                    and "--" not in strategy_name
                ):
                    current_strategies.append(strategy_name)

    # Add last batch
    if current_batch is not None and current_strategies:
        batches.append((current_batch, current_strategies))

    return batches


def generate_test_script(batch_num, strategies):
    """Generate a test script for a batch"""

    script_template = """#!/bin/bash
# Batch {batch_num} strategies test script (#{start_num}-{end_num})
# Created: 2026-03-05

set -e

# Configuration
TEST_DIR="/home/neozh/freqtrade-strategies"
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

# Create results CSV file
echo "Strategy,Status,Trades,Profit%,ProfitUSDT,WinRate%,Duration(s)" > "${{RESULTS_DIR}}/results.csv"

# Function to run backtest for a strategy
run_backtest() {
    local strategy=$1
    local log_file="${{LOG_DIR}}/${{strategy}}.log"
    
    echo "Testing strategy: ${{strategy}}"
    
    # Start timer
    local start_time=$(date +%s)
    
    # Run Docker backtest with full dependencies
    docker run --rm \
        -v "${{TEST_DIR}}/user_data:/freqtrade/user_data" \
        freqtrade-full:latest \
        backtesting --strategy "${{strategy}}" \
        --timerange=20250101-20250301 \
        --config /freqtrade/user_data/config.json \
        --timeframe 5m \
        --max-open-trades 3 \
        --stake-amount 100 \
        --dry-run-wallet 10000 \
        2>&1 | tee "${{log_file}}"
    
    local exit_code=${{PIPESTATUS[0]}}
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    # Parse results from log file
    local trades=0
    local profit_percent=""
    local profit_usdt=""
    local win_rate=""
    local status="FAIL"
    
    if [ ${{exit_code}} -eq 0 ]; then
        # Try to extract backtest results
        if grep -q "Backtest result:" "${{log_file}}"; then
            # Extract trades
            local trade_line=$(grep -A5 "Backtest result:" "${{log_file}}" | grep "Trades" | head -1)
            if [ ! -z "${{trade_line}}" ]; then
                trades=$(echo "${{trade_line}}" | grep -o '[0-9]\+' | head -1)
            fi
            
            # Extract profit percentage
            local profit_line=$(grep -A10 "Backtest result:" "${{log_file}}" | grep "Profit %" | head -1)
            if [ ! -z "${{profit_line}}" ]; then
                profit_percent=$(echo "${{profit_line}}" | grep -o '[0-9.-]\+%' | head -1 | tr -d '%')
            fi
            
            # Extract profit USDT
            local usdt_line=$(grep -A10 "Backtest result:" "${{log_file}}" | grep "Profit USDT" | head -1)
            if [ ! -z "${{usdt_line}}" ]; then
                profit_usdt=$(echo "${{usdt_line}}" | grep -o '[0-9.-]\+' | head -1)
            fi
            
            # Extract win rate
            local win_line=$(grep -A10 "Backtest result:" "${{log_file}}" | grep "Win Rate" | head -1)
            if [ ! -z "${{win_line}}" ]; then
                win_rate=$(echo "${{win_line}}" | grep -o '[0-9.-]\+%' | head -1 | tr -d '%')
            fi
            
            status="PASS"
        fi
    fi
    
    # Check for specific errors
    if grep -q "No data found" "${{log_file}}"; then
        status="FAIL - No data"
    elif grep -q "ImportError" "${{log_file}}"; then
        status="FAIL - Import error"
    elif grep -q "AttributeError" "${{log_file}}"; then
        status="FAIL - Attribute error"
    elif grep -q "SyntaxError" "${{log_file}}"; then
        status="FAIL - Syntax error"
    elif grep -q "NameError" "${{log_file}}"; then
        status="FAIL - Name error"
    elif grep -q "CategoricalParameter" "${{log_file}}"; then
        status="FAIL - CategoricalParameter import error"
    elif grep -q "IntParameter" "${{log_file}}"; then
        status="FAIL - IntParameter import error"
    fi
    
    # Save to CSV
    echo "${{strategy}},${{status}},${{trades}},${{profit_percent}},${{profit_usdt}},${{win_rate}},${{duration}}" >> "${{RESULTS_DIR}}/results.csv"
    
    echo "  Status: ${{status}}"
    echo "  Duration: ${{duration}}s"
    echo ""
}

# Run tests sequentially
for strategy in "${{STRATEGIES[@]}}"; do
    run_backtest "${{strategy}}"
done

echo ""
echo "Batch {batch_num} testing completed!"
echo "Results saved to: ${{RESULTS_DIR}}/results.csv"
echo "Logs saved to: ${{LOG_DIR}}/"
echo ""
echo "Summary of results:"
echo "-------------------"
tail -n +2 "${{RESULTS_DIR}}/results.csv" | while IFS=',' read -r strategy status trades profit_percent profit_usdt win_rate duration; do
    echo "  ${{strategy}}: ${{status}}"
done

# Generate summary statistics
total_strategies=$(tail -n +2 "${{RESULTS_DIR}}/results.csv" | wc -l)
pass_count=$(tail -n +2 "${{RESULTS_DIR}}/results.csv" | grep -c "PASS")
fail_count=$((total_strategies - pass_count))

echo ""
echo "Statistics:"
echo "  Total strategies tested: ${{total_strategies}}"
echo "  Pass: ${{pass_count}}"
echo "  Fail: ${{fail_count}}"
echo "  Pass rate: $((pass_count * 100 / total_strategies))%"

exit 0"""

    # Calculate start and end numbers
    start_num = 250 + (batch_num - 25) * 10
    end_num = start_num + 9

    # Create strategy list with quotes
    strategy_list = "\n".join([f'    "{s}"' for s in strategies])

    script = script_template.format(
        batch_num=batch_num,
        start_num=start_num,
        end_num=end_num,
        strategy_list=strategy_list,
    )

    script_path = (
        f"/home/neozh/freqtrade-strategies/scripts/test_batch{batch_num}_strategies.sh"
    )
    with open(script_path, "w") as f:
        f.write(script)

    # Make executable
    os.chmod(script_path, 0o755)

    print(f"Generated test script for Batch {batch_num}: {script_path}")
    return script_path


def main():
    print("Generating test scripts for batches 26-45...")

    # Extract strategy names
    batches = extract_strategy_names_from_md()

    if not batches:
        print("No batches found in range 26-45")
        return

    print(f"Found {len(batches)} batches in range 26-45")

    # Generate scripts
    generated_scripts = []
    for batch_num, strategies in batches:
        if len(strategies) == 10:  # Should be 10 strategies per batch
            script_path = generate_test_script(batch_num, strategies)
            generated_scripts.append(script_path)
        else:
            print(
                f"Warning: Batch {batch_num} has {len(strategies)} strategies (expected 10)"
            )

    print(f"\nGenerated {len(generated_scripts)} test scripts")
    print("\nTo run all scripts:")
    print("cd /home/neozh/freqtrade-strategies")
    for script in generated_scripts:
        batch_num = re.search(r"batch(\d+)", script).group(1)
        print(f"bash scripts/test_batch{batch_num}_strategies.sh")


if __name__ == "__main__":
    main()
