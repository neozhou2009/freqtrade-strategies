#!/usr/bin/env python3
"""
Prepare test environment for batch backtesting

This script:
1. Flattens strategies from strategies/ to test/user_data/strategies/
2. Copies data from user_data/data/ to test/user_data/data/

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


def fix_numpy_compatibility(directory):
    """Fix NumPy 2.0 compatibility issues in strategy files."""
    replacements = [
        ("np.NaN", "np.nan"),
        ("numpy.NaN", "numpy.nan"),
        ("np.NAN", "np.nan"),
        ("numpy.NAN", "numpy.nan"),
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

        if modified:
            with open(filepath, "w") as f:
                f.write(content)
            fixed_count += 1

    if fixed_count > 0:
        print(f"[✓] Fixed NumPy 2.0 compatibility in {fixed_count} files")


def flatten_strategies():
    """Copy all strategy files to test/user_data/strategies/"""
    src_dir = "strategies"
    dst_dir = "test/user_data/strategies"

    os.makedirs(dst_dir, exist_ok=True)

    # Clear existing files
    for f in glob.glob(os.path.join(dst_dir, "*.py")):
        os.remove(f)

    count = 0
    # Find all .py files in strategy subdirectories
    for filepath in glob.glob(os.path.join(src_dir, "**/*.py"), recursive=True):
        basename = os.path.basename(filepath)
        if basename == "__init__.py":
            continue
        dst_path = os.path.join(dst_dir, basename)
        shutil.copy2(filepath, dst_path)
        count += 1

    print(f"[✓] Flattened {count} strategy files to {dst_dir}")
    fix_class_names(dst_dir)
    fix_numpy_compatibility(dst_dir)
    return count


def copy_data():
    """Copy data from user_data/data/ to test/user_data/data/"""
    src_dir = "user_data/data/okx"
    dst_dir = "test/user_data/data/okx"

    if not os.path.exists(src_dir):
        print(f"[!] Source data directory not found: {src_dir}")
        return 0

    os.makedirs(os.path.dirname(dst_dir), exist_ok=True)

    # Remove existing data
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)

    shutil.copytree(src_dir, dst_dir)

    file_count = sum(
        1
        for _ in glob.glob(os.path.join(dst_dir, "**/*"), recursive=True)
        if os.path.isfile(_)
    )
    print(f"[✓] Copied {file_count} data files to {dst_dir}")
    return file_count


def main():
    print("=== Preparing Test Environment ===")
    print()

    strategies = flatten_strategies()
    data = copy_data()

    print()

    # Ensure backtest configuration stays synced with user_data/config.json
    # (Fixes the issue where an outdated test/config.json causes failures like Binance US restrictions)
    shutil.copy2("user_data/config.json", "test/config.json")

    # Pre-create backtest results directory and grant generous permissions
    # This prevents PermissionError when the docker container (ftuser) tries to write
    # to the directory created by the github actions runner
    backtest_dir = "test/user_data/backtest_results"
    os.makedirs(backtest_dir, exist_ok=True)
    for root, dirs, files in os.walk("test/user_data"):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o777)
        for f in files:
            os.chmod(os.path.join(root, f), 0o666)
    os.chmod("test/user_data", 0o777)

    print("=== Summary ===")
    print(f"Strategies: {strategies}")
    print(f"Data files: {data}")
    print()
    print("Ready for batch backtesting!")


if __name__ == "__main__":
    main()
