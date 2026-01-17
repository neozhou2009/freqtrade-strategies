import os
import glob
import re

STRATEGY_DIR = "freqtrade-strategies/strategies"

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Replace method definitions
    content = re.sub(r'def populate_buy_trend', r'def populate_entry_trend', content)
    content = re.sub(r'def populate_sell_trend', r'def populate_exit_trend', content)
    
    # Replace column assignments and access
    # We use regex to match 'buy' or "buy" inside brackets or loc
    
    # specific case for dataframe['buy'] or dataframe["buy"]
    content = re.sub(r"dataframe\['buy'\]", r"dataframe['enter_long']", content)
    content = re.sub(r'dataframe\["buy"\]', r'dataframe["enter_long"]', content)
    
    # dataframe.loc[..., 'buy']
    content = re.sub(r",\s*'buy'\]", r", 'enter_long']", content)
    content = re.sub(r',\s*"buy"\]', r', "enter_long"]', content)
    
    # Same for sell -> exit_long
    content = re.sub(r"dataframe\['sell'\]", r"dataframe['exit_long']", content)
    content = re.sub(r'dataframe\["sell"\]', r'dataframe["exit_long"]', content)
    
    content = re.sub(r",\s*'sell'\]", r", 'exit_long']", content)
    content = re.sub(r',\s*"sell"\]', r', "exit_long"]', content)
    
    if content != original_content:
        print(f"Fixing {filepath}")
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

files = glob.glob(os.path.join(STRATEGY_DIR, "*", "*.py"))
count = 0
for f in files:
    if fix_file(f):
        count += 1

print(f"Fixed {count} files.")
