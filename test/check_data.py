import pandas as pd
import glob
import os

data_dir = "user_data/data/binance/futures"
files = glob.glob(os.path.join(data_dir, "*.feather"))

for f in files:
    try:
        df = pd.read_feather(f)
        if 'date' in df.columns:
            start = df['date'].min()
            end = df['date'].max()
            print(f"{os.path.basename(f)}: {start} to {end}")
    except Exception as e:
        print(f"Error reading {f}: {e}")
