import pandas as pd
import glob
import os
from datetime import datetime

data_dir = 'user_data/data/binance/futures'
files = sorted(glob.glob(os.path.join(data_dir, '*.feather')))

print(f"{'File':<50} | {'Start':<25} | {'End':<25}")
print("-" * 110)

for f in files:
    try:
        # Ignore mark and funding rate files for now as they are auxiliary
        if any(x in f for x in ['mark', 'funding_rate']):
            continue
        df = pd.read_feather(f)
        start = df.date.min()
        end = df.date.max()
        print(f"{os.path.basename(f):<50} | {str(start):<25} | {str(end):<25}")
    except Exception as e:
        print(f"Error reading {f}: {e}")
