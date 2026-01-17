import os
import subprocess
import glob
import json
import pandas as pd
import zipfile
import re
from pathlib import Path

STRATEGY_DIR = "freqtrade-strategies/strategies"
CONFIG_FILE = "config.json"
TIMERANGE = "20251220-20260114"
RESULTS_DIR = "user_data/backtest_results"

strategy_files = glob.glob(os.path.join(STRATEGY_DIR, "*", "*.py"))
strategy_files.sort()

# Settings for continuation
START_INDEX = 250
END_INDEX = len(strategy_files)

print(f"Total strategies found: {len(strategy_files)}")
print(f"Running from index {START_INDEX} to {END_INDEX}")

results = []

for i in range(START_INDEX, END_INDEX):
    strategy_file = strategy_files[i]
    strategy_name = Path(strategy_file).stem
    strategy_path = Path(strategy_file).parent
    
    print(f"[{i+1}/{len(strategy_files)}] Testing {strategy_name}...")
    
    export_filename = f"{RESULTS_DIR}/result_{strategy_name}.json"
    
    # Check if result already exists to skip?
    # For now, let's just run it.
    
    cmd = [
        "freqtrade", "backtesting",
        "--config", CONFIG_FILE,
        "--strategy", strategy_name,
        "--strategy-path", str(strategy_path),
        "--timerange", TIMERANGE,
        "--timeframe", "5m",
        "--export", "trades"
    ]
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        
        if proc.returncode != 0:
             err = proc.stderr[:500] + "..." if len(proc.stderr) > 500 else proc.stderr
             # print(f"Error testing {strategy_name}: {err}")
             results.append({"key": strategy_name, "status": "Error", "error": "Return code non-zero"})
             continue

        target_file = None
        match = re.search(r'dumping json to "([^"]+)"', proc.stderr)
        if not match:
             match = re.search(r'dumping json to "([^"]+)"', proc.stdout)
        
        if match:
             meta_file = match.group(1)
             target_file = meta_file.replace('.meta.json', '.zip')
        
        data = None
        if target_file and os.path.exists(target_file):
            with zipfile.ZipFile(target_file, 'r') as z:
                for fname in z.namelist():
                        if fname.endswith('.json') and 'config' not in fname and 'meta' not in fname:
                            with z.open(fname) as f:
                                data = json.load(f)
                                break
        else:
            # Fallback: check latest file in dir
            candidates = glob.glob(f"{RESULTS_DIR}/*.zip")
            if candidates:
                target_file = max(candidates, key=os.path.getctime)
                # Ensure it's recent?
                with zipfile.ZipFile(target_file, 'r') as z:
                    for fname in z.namelist():
                        if fname.endswith('.json') and 'config' not in fname and 'meta' not in fname:
                            with z.open(fname) as f:
                                data = json.load(f)
                                break
        
        if data and 'strategy_comparison' in data:
            # Verify it's the right strategy
            strat_metrics = data['strategy_comparison'][0]
            if strat_metrics['key'] == strategy_name:
                results.append(strat_metrics)
            else:
                 results.append({"key": strategy_name, "status": "Result mismatch"})
        else:
            results.append({"key": strategy_name, "status": "No metrics found"})

    except Exception as e:
        print(f"Exception testing {strategy_name}: {e}")
        results.append({"key": strategy_name, "status": "Exception", "error": str(e)})

# Save to a separate file to avoid overwriting the first batch if something goes wrong
# We will merge later
if results:
    df_results = pd.DataFrame(results)
    output_file = "strategy_evaluation_part3.csv"
    df_results.to_csv(output_file, index=False)
    print(f"\nEvaluation Part 3 Complete. Saved to {output_file}")
    
    cols = ['key', 'profit_total_pct', 'winrate', 'sharpe', 'max_drawdown_account', 'trades']
    cols = [c for c in cols if c in df_results.columns]
    print(df_results[cols].sort_values(by='profit_total_pct', ascending=False).head(10))
else:
    print("No results for Part 2.")
