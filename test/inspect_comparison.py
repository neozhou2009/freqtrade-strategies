import zipfile
import json
import glob
import os

list_of_files = glob.glob('user_data/backtest_results/*.zip')
latest_file = max(list_of_files, key=os.path.getctime)

with zipfile.ZipFile(latest_file, 'r') as z:
    for filename in z.namelist():
        if filename.endswith('.json') and 'config' not in filename:
            with z.open(filename) as f:
                data = json.load(f)
                if 'strategy_comparison' in data:
                    print(json.dumps(data['strategy_comparison'], indent=2))
