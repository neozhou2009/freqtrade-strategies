import pandas as pd

df = pd.read_csv('strategy_evaluation_full.csv')
# Filter successful ones
success_df = df[df['profit_total_pct'].notna()].copy()

# Sort by profit descending
success_df['sort_val'] = pd.to_numeric(success_df['profit_total_pct'], errors='coerce').fillna(-999999)
success_df = success_df.sort_values(by='sort_val', ascending=False)

strategies = success_df['key'].tolist()

print(f"Found {len(strategies)} successful strategies.")
print("Top 10:", strategies[:10])

with open('successful_strategies_sorted.txt', 'w') as f:
    for s in strategies:
        f.write(s + '\n')
