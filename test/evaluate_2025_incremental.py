import os
import subprocess
import glob
import json
import pandas as pd
import zipfile
import re
from pathlib import Path
import time

STRATEGY_DIR = "freqtrade-strategies/strategies"
CONFIG_FILE = "config.json"
TIMERANGE = "20250101-20251231"
RESULTS_DIR = "user_data/backtest_results/2025_full_year"
OUTPUT_CSV = "strategy_evaluation_2025.csv"

# Ensure results dir exists
os.makedirs(RESULTS_DIR, exist_ok=True)

# Read sorted strategies
with open('successful_strategies_sorted.txt', 'r') as f:
    target_strategies = [line.strip() for line in f if line.strip()]

# Load existing results to skip
if os.path.exists(OUTPUT_CSV):
    existing_df = pd.read_csv(OUTPUT_CSV)
    existing_keys = existing_df['key'].tolist()
else:
    existing_keys = []

# Find files for these strategies
strategy_map = {}
all_files = glob.glob(os.path.join(STRATEGY_DIR, "*", "*.py"))
for f in all_files:
    name = Path(f).stem
    strategy_map[name] = f

print(f"Loaded {len(target_strategies)} strategies to test.")
print(f"Skipping {len(existing_keys)} already done.")

for i, strategy_name in enumerate(target_strategies):
    if strategy_name in existing_keys:
        continue

    if strategy_name not in strategy_map:
        print(f"Warning: Strategy file for {strategy_name} not found.")
        continue
        
    strategy_file = strategy_map[strategy_name]
    strategy_path = Path(strategy_file).parent
    
    print(f"[{i+1}/{len(target_strategies)}] Testing {strategy_name}...")
    
    export_filename = f"{RESULTS_DIR}/result_{strategy_name}.json"
    
    cmd = [
        "freqtrade", "backtesting",
        "--config", CONFIG_FILE,
        "--strategy", strategy_name,
        "--strategy-path", str(strategy_path),
        "--timerange", TIMERANGE,
        "--timeframe", "5m",
        "--export", "trades"
    ]
    
    current_result = {}
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        
        if proc.returncode != 0:
             err = proc.stderr[:500] + "..." if len(proc.stderr) > 500 else proc.stderr
             print(f"Error testing {strategy_name}")
             current_result = {"key": strategy_name, "status": "Error", "error": "Return code non-zero"}
        else:
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
            
            if data and 'strategy_comparison' in data:
                strat_metrics = data['strategy_comparison'][0]
                if strat_metrics['key'] == strategy_name:
                    current_result = strat_metrics
                else:
                     current_result = {"key": strategy_name, "status": "Result mismatch"}
            else:
                current_result = {"key": strategy_name, "status": "No metrics found"}

    except Exception as e:
        print(f"Exception testing {strategy_name}: {e}")
        current_result = {"key": strategy_name, "status": "Exception", "error": str(e)}

    # Save immediately
    if os.path.exists(OUTPUT_CSV):
        df_new = pd.DataFrame([current_result])
        df_new.to_csv(OUTPUT_CSV, mode='a', header=False, index=False)
    else:
        df_new = pd.DataFrame([current_result])
        df_new.to_csv(OUTPUT_CSV, index=False)

print("\nEvaluation Complete.")
