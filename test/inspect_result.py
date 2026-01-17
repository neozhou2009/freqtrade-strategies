import zipfile
import json
import glob
import os

# Find the latest zip file
list_of_files = glob.glob('user_data/backtest_results/*.zip')
latest_file = max(list_of_files, key=os.path.getctime)
print(f"Inspecting {latest_file}")

with zipfile.ZipFile(latest_file, 'r') as z:
    for filename in z.namelist():
        print(f"Found file: {filename}")
        if filename.endswith('.json'):
            with z.open(filename) as f:
                data = json.load(f)
                print("Keys:", data.keys())
                if 'strategy' in data:
                    print("Strategies:", data['strategy'].keys())
                    first_strat = list(data['strategy'].keys())[0]
                    print(f"Metrics for {first_strat}:")
                    print(json.dumps(data['strategy'][first_strat], indent=2)[:500]) # Print first 500 chars
