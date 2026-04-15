#!/usr/bin/env python3
"""
Fix INTERFACE_VERSION 3 column name mismatches in strategy files.

In freqtrade INTERFACE_VERSION 3, the column names changed:
  - 'buy'     -> 'enter_long'
  - 'sell'    -> 'exit_long'
  - 'entry'   -> 'enter_long'
  - 'exit'    -> 'exit_long'
  - 'buy_tag' -> 'enter_tag'
  - 'sell_tag'-> 'exit_tag'

Many strategies declare INTERFACE_VERSION = 3 but still use the old v1/v2
column names, causing freqtrade to silently ignore signals (0 trades).

This script performs safe, targeted replacements:
  - Only modifies files with INTERFACE_VERSION = 3
  - Only replaces column-name contexts (dataframe["buy"], ['sell'], etc.)
  - Preserves HyperOpt spaces (space="buy"), variable names, comments, etc.

Usage:
    # Preview changes (dry-run)
    python scripts/fix_v3_column_names.py --dry-run

    # Apply fixes
    python scripts/fix_v3_column_names.py

    # Apply with git auto-commit
    python scripts/fix_v3_column_names.py --commit
"""

import os
import re
import argparse
from pathlib import Path


# ──────────────────────────────────────────────────────────────────────────────
# Column name mapping
# ──────────────────────────────────────────────────────────────────────────────

# Map: old_name -> new_name
COLUMN_MAP = {
    "buy": "enter_long",
    "sell": "exit_long",
    "entry": "enter_long",
    "exit": "exit_long",
    "buy_tag": "enter_tag",
    "sell_tag": "exit_tag",
}


def is_v3_strategy(content: str) -> bool:
    """Check if the strategy file declares INTERFACE_VERSION = 3."""
    return bool(re.search(r"INTERFACE_VERSION\s*=\s*3", content))


def fix_column_names(content: str) -> tuple[str, list[str]]:
    """
    Fix old column names to v3 equivalents in a strategy file.

    Returns (new_content, list_of_changes).
    """
    changes = []
    lines = content.split("\n")
    new_lines = []

    for lineno, line in enumerate(lines, 1):
        original = line
        new_line = line

        # Skip comment-only lines
        stripped = line.lstrip()
        if stripped.startswith("#"):
            new_lines.append(line)
            continue

        # Only process lines that contain dataframe column operations
        # Patterns we want to match (column name contexts):
        #   dataframe["buy"] = 1
        #   dataframe['sell'] = 0
        #   dataframe.loc[..., "entry"] = 1
        #   ["buy", "buy_tag"]
        #   dataframe["buy_tag"] = "signal"
        #   dataframe.loc[:, "buy"] = ...
        #   ,'buy'] = 1
        #   ,"entry"] = 1
        #
        # Patterns we do NOT want to match:
        #   space="buy"        (HyperOpt space)
        #   buy_params          (variable names)
        #   def populate_buy    (method names)
        #   # buy signal        (comments)
        #   "buy_signal_1"     (string values, not column names)

        for old_name, new_name in COLUMN_MAP.items():
            # Pattern 1: ["old_name"] or ['old_name'] as column access
            # This matches: dataframe["buy"], df['sell'], ["buy", "buy_tag"]
            # Uses negative lookbehind for space= and other false positives

            # Match "old_name" or 'old_name' when used as column name
            # Context: preceded by [ or , or .loc etc., followed by ] or ,
            # We use a careful regex that matches the column name in indexing context

            # Double-quoted: "buy" -> "enter_long"
            # Must be in indexing context: after [ or , with optional whitespace
            pattern_dq = r'(?<=[\[,\s])"' + re.escape(old_name) + r'"(?=[\]\,\s])'
            # Also match at start of line after whitespace in multi-line expressions
            # e.g.          'buy'] = 1
            pattern_dq2 = r'(\s)"' + re.escape(old_name) + r'"(\])'

            # Single-quoted: 'buy' -> 'enter_long'
            pattern_sq = r"(?<=[\[,\s])'" + re.escape(old_name) + r"'(?=[\]\,\s])"
            pattern_sq2 = r"(\s)'" + re.escape(old_name) + r"'(\])"

            # Apply double-quote patterns
            new_line = re.sub(pattern_dq, f'"{new_name}"', new_line)
            new_line = re.sub(pattern_dq2, f'\\"{new_name}"\\2', new_line)

            # Apply single-quote patterns
            new_line = re.sub(pattern_sq, f"'{new_name}'", new_line)
            new_line = re.sub(pattern_sq2, f"\\1'{new_name}'\\2", new_line)

        # Safety: undo any replacements in HyperOpt space declarations
        # space="buy" and space="sell" must NOT be changed
        new_line = re.sub(r'space="enter_long"', 'space="buy"', new_line)
        new_line = re.sub(r"space='enter_long'", "space='buy'", new_line)
        new_line = re.sub(r'space="exit_long"', 'space="sell"', new_line)
        new_line = re.sub(r"space='exit_long'", "space='sell'", new_line)

        # Safety: undo replacements in order_types dict
        # "entry": "limit" should stay as is (it's a key, not a column)
        # But "exit": "limit" is also a key... we need to be careful
        # Actually, order_types keys are "entry"/"exit" which are valid v3 names
        # The mapping from "entry" -> "enter_long" would break order_types
        # Let's protect order_types and order_time_in_force contexts

        # Undo if line contains order_types or order_time_in_force patterns
        if "order_types" in original or "order_time_in_force" in original:
            # Restore entry/exit keys in these dicts
            new_line = re.sub(r'"enter_long":\s*"limit"', '"entry": "limit"', new_line)
            new_line = re.sub(r"'enter_long':\s*'limit'", "'entry': 'limit'", new_line)
            new_line = re.sub(r'"exit_long":\s*"limit"', '"exit": "limit"', new_line)
            new_line = re.sub(r"'exit_long':\s*'limit'", "'exit': 'limit'", new_line)
            new_line = re.sub(r'"enter_long":\s*"market"', '"entry": "market"', new_line)
            new_line = re.sub(r"'enter_long':\s*'market'", "'entry': 'market'", new_line)
            new_line = re.sub(r'"exit_long":\s*"market"', '"exit": "market"', new_line)
            new_line = re.sub(r"'exit_long':\s*'market'", "'exit': 'market'", new_line)
            new_line = re.sub(r'"enter_long":\s*"GTC"', '"entry": "GTC"', new_line)
            new_line = re.sub(r"'enter_long':\s*'GTC'", "'entry': 'GTC'", new_line)
            new_line = re.sub(r'"exit_long":\s*"GTC"', '"exit": "GTC"', new_line)
            new_line = re.sub(r"'exit_long':\s*'GTC'", "'exit': 'GTC'", new_line)
            new_line = re.sub(r'"stoploss_on_exchange"', '"stoploss_on_exchange"', new_line)

        # Undo if line contains stoploss_on_exchange
        if "stoploss_on_exchange" in original:
            # These are config keys, not column names
            pass

        if new_line != original:
            # Determine what changed
            for old_name, new_name in COLUMN_MAP.items():
                if old_name in original and new_name in new_line and old_name not in new_line.replace(new_name, ""):
                    # Simple check: did this specific replacement happen?
                    pass
            changes.append(f"L{lineno}: {original.strip()} -> {new_line.strip()}")

        new_lines.append(new_line)

    return "\n".join(new_lines), changes


def process_strategies(strategies_dir: str, dry_run: bool = False) -> dict:
    """Process all strategy files and fix column names."""
    stats = {
        "total_files": 0,
        "v3_files": 0,
        "fixed_files": 0,
        "total_changes": 0,
        "details": [],
    }

    strategies_path = Path(strategies_dir)
    if not strategies_path.exists():
        print(f"❌ Strategies directory not found: {strategies_dir}")
        return stats

    for py_file in sorted(strategies_path.rglob("*.py")):
        stats["total_files"] += 1
        content = py_file.read_text(encoding="utf-8", errors="ignore")

        if not is_v3_strategy(content):
            continue

        stats["v3_files"] += 1
        new_content, changes = fix_column_names(content)

        if changes:
            stats["fixed_files"] += 1
            stats["total_changes"] += len(changes)
            stats["details"].append({
                "file": str(py_file.relative_to(strategies_path.parent)),
                "changes": len(changes),
                "sample_changes": changes[:5],
            })

            if not dry_run:
                py_file.write_text(new_content, encoding="utf-8")

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Fix INTERFACE_VERSION 3 column name mismatches in strategy files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--strategies-dir",
        default="strategies",
        help="Path to strategies directory (default: strategies)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing files",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Auto git-commit changes after applying",
    )

    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent
    strategies_dir = project_root / args.strategies_dir

    print(f"📂 Strategies directory: {strategies_dir}")
    print(f"🔧 Mode: {'DRY-RUN (preview)' if args.dry_run else 'APPLY'}")
    print()

    stats = process_strategies(str(strategies_dir), dry_run=args.dry_run)

    print(f"📊 Results:")
    print(f"   Total .py files scanned: {stats['total_files']}")
    print(f"   INTERFACE_VERSION = 3:   {stats['v3_files']}")
    print(f"   Files with changes:      {stats['fixed_files']}")
    print(f"   Total changes:           {stats['total_changes']}")

    if stats["details"]:
        print(f"\n📋 Changed files (top 20):")
        for d in stats["details"][:20]:
            print(f"   {d['file']}: {d['changes']} changes")
            for c in d["sample_changes"][:3]:
                print(f"      {c[:120]}")

        if len(stats["details"]) > 20:
            print(f"   ... and {len(stats['details']) - 20} more files")

    if args.dry_run:
        print(f"\n⚠️  DRY-RUN: No files were modified.")
        print(f"   Run without --dry-run to apply changes.")
    else:
        print(f"\n✅ Changes applied.")

        if args.commit:
            os.system(
                f'cd "{project_root}" && git add -A strategies/ && '
                f'git commit -m "fix: rename v1/v2 column names to v3 '
                f'(buy->enter_long, sell->exit_long, entry->enter_long, exit->exit_long)"'
            )
            print("   Git commit created.")


if __name__ == "__main__":
    main()
