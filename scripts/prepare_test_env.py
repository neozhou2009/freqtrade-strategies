#!/usr/bin/env python3
"""
Prepare environment for batch backtesting

This script:
1. Flattens strategies from strategies/ to user_data/strategies/

Usage:
    python scripts/prepare_test_env.py
"""

import os
import shutil
import glob
import re


def fix_class_names(directory):
    """Fix class names that don't match filename."""
    fixes = [
        ("BBRSI.py", "class bbrsi", "class BBRSI"),
        ("SuperTrend.py", "class Supertrend", "class SuperTrend"),
        ("SAR.py", "class Sar", "class SAR"),
        ("mabStra.py", "class MabStra", "class mabStra"),
    ]

    fixed_count = 0
    for filename, old_class, new_class in fixes:
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
            if old_class in content:
                content = content.replace(old_class, new_class)
                with open(filepath, "w") as f:
                    f.write(content)
                fixed_count += 1

    if fixed_count > 0:
        print(f"[✓] Fixed {fixed_count} class name mismatches")


def fix_freqtrade_v3_compatibility(directory):
    replacements = [
        ("np.NaN", "np.nan"),
        ("numpy.NaN", "numpy.nan"),
        ("np.NAN", "np.nan"),
        ("numpy.NAN", "numpy.nan"),
        ("sell_profit_only", "exit_profit_only"),
        ("use_sell_signal", "use_exit_signal"),
        ("sell_signal", "exit_signal"),
        ("ignore_roi_if_buy_signal", "ignore_roi_if_entry_signal"),
        ("from freqtrade.strategy.hyper import", "from freqtrade.strategy import"),
        ("from freqtrade.strategy.hyper import\n", "from freqtrade.strategy import\n"),
        ("sell_profit_offset", "exit_profit_offset"),
        ("def custom_sell(", "def custom_exit("),
        ("self.custom_sell(", "self.custom_exit("),
    ]

    fixed_count = 0
    for filename in os.listdir(directory):
        if not filename.endswith(".py"):
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath, "r") as f:
            content = f.read()

        modified = False
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                modified = True

        # Fix DTypePromotionError when mixing string and np.nan in np.where
        if re.search(r",\s*(?:np|numpy)\.nan\)", content):
            new_content = re.sub(
                r"(\bnp\.where\([^,]+,\s*'down',\s*'up'\)),\s*(?:np|numpy)\.nan\)",
                r"\1, 'NaN')",
                content,
            )
            if new_content != content:
                content = new_content
                modified = True

        # Fix order_time_in_force v2→v3 keys
        if re.search(r"order_time_in_force\s*=", content):
            content = re.sub(
                r"(order_time_in_force\s*=\s*\{[^}]*?)'buy'(\s*:\s*')",
                r"\1'entry'\2",
                content,
            )
            content = re.sub(
                r"(order_time_in_force\s*=\s*\{[^}]*?)'sell'(\s*:\s*')",
                r"\1'exit'\2",
                content,
            )
            content = re.sub(
                r'(order_time_in_force\s*=\s*\{[^}]*)"buy"(\s*:\s*")',
                r'\1"entry"\2',
                content,
            )
            content = re.sub(
                r'(order_time_in_force\s*=\s*\{[^}]*)"sell"(\s*:\s*")',
                r'\1"exit"\2',
                content,
            )
            modified = True

        # Fix order_types v2→v3 keys ('buy'→'entry', 'sell'→'exit')
        if re.search(r"order_types\s*=", content):
            content = re.sub(
                r"(order_types\s*=\s*\{[^}]*?)'buy'(\s*:)",
                r"\1'entry'\2",
                content,
            )
            content = re.sub(
                r"(order_types\s*=\s*\{[^}]*?)'sell'(\s*:)",
                r"\1'exit'\2",
                content,
            )
            content = re.sub(
                r'(order_types\s*=\s*\{[^}]*)"buy"(\s*:)',
                r'\1"entry"\2',
                content,
            )
            content = re.sub(
                r'(order_types\s*=\s*\{[^}]*)"sell"(\s*:)',
                r'\1"exit"\2',
                content,
            )
            modified = True

        if modified:
            with open(filepath, "w") as f:
                f.write(content)
            fixed_count += 1

    if fixed_count > 0:
        print(f"[✓] Fixed Freqtrade v3 compatibility in {fixed_count} files")


def flatten_strategies():
    """Copy all strategy files to user_data/strategies/"""
    src_dir = "strategies"
    dst_dir = "user_data/strategies"

    os.makedirs(dst_dir, exist_ok=True)

    # Clear existing flattened strategy files (only those from strategies/ dir,
    # not community-contributed files that were already in user_data/strategies/)
    count = 0
    # Find all .py files in strategy subdirectories
    src_basenames = set()
    for filepath in glob.glob(os.path.join(src_dir, "**/*.py"), recursive=True):
        basename = os.path.basename(filepath)
        if basename != "__init__.py":
            src_basenames.add(basename)

    # Remove old flattened copies that came from strategies/
    for f in glob.glob(os.path.join(dst_dir, "*.py")):
        if os.path.basename(f) in src_basenames:
            os.remove(f)

    for filepath in glob.glob(os.path.join(src_dir, "**/*.py"), recursive=True):
        basename = os.path.basename(filepath)
        if basename == "__init__.py":
            continue
        dst_path = os.path.join(dst_dir, basename)
        shutil.copy2(filepath, dst_path)
        count += 1

    print(f"[✓] Flattened {count} strategy files to {dst_dir}")
    fix_class_names(dst_dir)
    fix_freqtrade_v3_compatibility(dst_dir)
    return count


def main():
    print("=== Preparing Backtest Environment ===")
    print()

    strategies = flatten_strategies()

    # Pre-create backtest results directory and grant generous permissions
    # This prevents PermissionError when the docker container (ftuser) tries to write
    backtest_dir = "user_data/backtest_results"
    os.makedirs(backtest_dir, exist_ok=True)
    for root, dirs, files in os.walk("user_data"):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o777)
        for f in files:
            os.chmod(os.path.join(root, f), 0o666)
    os.chmod("user_data", 0o777)

    print()
    print("=== Summary ===")
    print(f"Strategies: {strategies}")
    print()
    print("Ready for batch backtesting!")


if __name__ == "__main__":
    main()
