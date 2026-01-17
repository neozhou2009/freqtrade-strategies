import pandas as pd

df = pd.read_csv('strategy_evaluation_full.csv')
# Filter successful ones (where status is empty or NaN, based on previous logic)
# Actually in the CSV generation, if status was not "No metrics found" or "Error", we put metrics.
# Let's check the columns. If 'profit_total_pct' is not null, it ran.

success_df = df[df['profit_total_pct'].notna()]
strategies = success_df['key'].tolist()

print(f"Found {len(strategies)} successful strategies.")
print(strategies[:10])

with open('successful_strategies.txt', 'w') as f:
    for s in strategies:
        f.write(s + '\n')
