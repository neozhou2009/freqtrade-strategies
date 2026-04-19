#!/usr/bin/env python3
"""
Pair Selector Tool for Freqtrade Strategies

Runs a complete backtest and analyzes pair-by-pair performance to recommend
the best trading pair combinations for hyperopt optimization.

Usage:
    python scripts/pair_selector.py --strategy BBRSITV --period 2026_q1
    python scripts/pair_selector.py --strategy NostalgiaForInfinity --timerange 20250101-20251231 --output reports/
"""

import os
import json
import subprocess
import argparse
import tempfile
import zipfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path


def get_timerange(period: str) -> str:
    """Convert period string to timerange format."""
    now = datetime.now()
    if period == "2025_year":
        return "20250101-20251231"
    elif period == "2026_q1":
        return "20260101-20260418"
    elif period == "last_1_week":
        start = now - timedelta(days=7)
    elif period == "last_1_month":
        start = now - timedelta(days=30)
    elif period == "last_3_months":
        start = now - timedelta(days=90)
    elif period == "last_6_months":
        start = now - timedelta(days=180)
    elif period == "last_1_year":
        start = now - timedelta(days=365)
    else:
        # Assume it's already a timerange format
        return period
    return f"{start.strftime('%Y%m%d')}-{now.strftime('%Y%m%d')}"


def run_backtest(strategy: str, timerange: str, config_path: str, use_docker: bool = True) -> Path:
    """Run backtest and return path to result file."""

    project_root = Path(__file__).parent.parent
    user_data_dir = project_root / "user_data"
    results_dir = user_data_dir / "backtest_results"

    if use_docker:
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{user_data_dir}:/freqtrade/user_data",
            "neozhou2009/freqtrade-full:latest",
            "backtesting",
            "--config", "/freqtrade/user_data/config.json",
            "--strategy", strategy,
            "--timerange", timerange,
            "--export", "trades",
        ]
    else:
        cmd = [
            "freqtrade", "backtesting",
            "--config", config_path,
            "--strategy", strategy,
            "--timerange", timerange,
            "--export", "trades",
        ]

    print(f"\n{'='*60}")
    print(f"Running backtest for strategy: {strategy}")
    print(f"Timerange: {timerange}")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    # Find the latest result zip file
    zip_files = sorted(results_dir.glob("backtest-result-*.zip"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not zip_files:
        raise RuntimeError("No backtest result file found")

    return zip_files[0]


def extract_pair_performance(zip_path: Path) -> dict:
    """Extract pair performance from backtest result zip."""

    # Extract to temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(tmpdir)

        # Find the JSON file
        json_files = list(Path(tmpdir).glob("*.json"))
        if not json_files:
            raise RuntimeError("No JSON file in backtest result")

        # Find the result JSON (not config or meta)
        result_json = None
        for f in json_files:
            if "_config" not in f.name and "_meta" not in f.name:
                result_json = f
                break

        if not result_json:
            raise RuntimeError("Could not find result JSON file")

        with open(result_json, 'r') as f:
            data = json.load(f)

    return analyze_results(data)


def analyze_results(data: dict) -> dict:
    """Analyze backtest results and extract pair performance."""

    strategies = data.get('strategy', {})
    if not strategies:
        return {"error": "No strategy results found"}

    all_strategy_results = {}

    for strategy_name, results in strategies.items():
        pairs_with_trades = []

        for pair_data in results.get('results_per_pair', []):
            # Handle nested key structure
            key_info = pair_data.get('key', {})
            pair = key_info.get('key', 'N/A') if isinstance(key_info, dict) else str(pair_data.get('key', 'N/A'))
            trades = key_info.get('trades', pair_data.get('trades', 0)) if isinstance(key_info, dict) else pair_data.get('trades', 0)
            profit_total_pct = key_info.get('profit_total_pct', pair_data.get('profit_total_pct', 0)) if isinstance(key_info, dict) else pair_data.get('profit_total_pct', 0)
            profit_total_abs = key_info.get('profit_total_abs', pair_data.get('profit_total_abs', 0)) if isinstance(key_info, dict) else pair_data.get('profit_total_abs', 0)
            wins = key_info.get('wins', pair_data.get('wins', 0)) if isinstance(key_info, dict) else pair_data.get('wins', 0)
            losses = key_info.get('losses', pair_data.get('losses', 0)) if isinstance(key_info, dict) else pair_data.get('losses', 0)
            winrate = key_info.get('winrate', pair_data.get('winrate', 0)) if isinstance(key_info, dict) else pair_data.get('winrate', 0)
            sharpe = key_info.get('sharpe', pair_data.get('sharpe', 0)) if isinstance(key_info, dict) else pair_data.get('sharpe', 0)
            drawdown = key_info.get('max_drawdown_account', pair_data.get('max_drawdown_account', 0)) if isinstance(key_info, dict) else pair_data.get('max_drawdown_account', 0)
            duration_avg = key_info.get('duration_avg', pair_data.get('duration_avg', 'N/A')) if isinstance(key_info, dict) else pair_data.get('duration_avg', 'N/A')

            # Skip TOTAL row
            if pair == 'TOTAL' or trades == 0:
                continue

            win_rate_pct = winrate * 100 if winrate else (wins / trades) * 100 if trades > 0 else 0
            pairs_with_trades.append({
                'pair': pair,
                'trades': trades,
                'roi': profit_total_pct,
                'win_rate': win_rate_pct,
                'profit_abs': profit_total_abs,
                'wins': wins,
                'losses': losses,
                'drawdown': drawdown * 100,
                'sharpe': sharpe,
                'duration_avg': duration_avg,
            })

        # Sort by ROI
        pairs_with_trades.sort(key=lambda x: x['roi'], reverse=True)

        # Calculate averages
        if pairs_with_trades:
            avg_roi = sum(p['roi'] for p in pairs_with_trades) / len(pairs_with_trades)
            avg_winrate = sum(p['win_rate'] for p in pairs_with_trades) / len(pairs_with_trades)
            avg_trades = sum(p['trades'] for p in pairs_with_trades) / len(pairs_with_trades)
        else:
            avg_roi = avg_winrate = avg_trades = 0

        # Recommend pairs (ROI > avg, WinRate > avg)
        recommended = [p for p in pairs_with_trades if p['roi'] > avg_roi and p['win_rate'] > avg_winrate]
        recommended.sort(key=lambda x: (x['roi'], x['trades']), reverse=True)

        # Filter out pairs with too few trades for reliable recommendation
        reliable_recommended = [p for p in recommended if p['trades'] >= 3]

        all_strategy_results[strategy_name] = {
            'summary': {
                'total_pairs_with_trades': len(pairs_with_trades),
                'avg_roi': avg_roi,
                'avg_winrate': avg_winrate,
                'avg_trades': avg_trades,
            },
            'all_pairs': pairs_with_trades,
            'recommended': recommended,
            'reliable_recommended': reliable_recommended,
        }

    return all_strategy_results


def generate_report(results: dict, strategy: str, timerange: str, output_path: Path = None) -> str:
    """Generate markdown report."""

    if strategy not in results:
        return f"Error: Strategy {strategy} not found in results"

    sr = results[strategy]
    summary = sr['summary']
    all_pairs = sr['all_pairs']
    recommended = sr['recommended']
    reliable = sr['reliable_recommended']

    report_lines = []

    report_lines.append(f"# Pair Selection Report: {strategy}")
    report_lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_lines.append(f"**Timerange:** {timerange}")
    report_lines.append(f"\n---")
    report_lines.append(f"\n## Summary")
    report_lines.append(f"\n| Metric | Value |")
    report_lines.append(f"|--------|-------|")
    report_lines.append(f"| Pairs with trades | {summary['total_pairs_with_trades']} |")
    report_lines.append(f"| Average ROI | {summary['avg_roi']:.2f}% |")
    report_lines.append(f"| Average WinRate | {summary['avg_winrate']:.1f}% |")
    report_lines.append(f"| Average Trades | {summary['avg_trades']:.1f} |")

    # Top performers
    report_lines.append(f"\n## All Pairs Performance (sorted by ROI)")
    report_lines.append(f"\n| Pair | Trades | ROI | WinRate | Profit | Drawdown | Sharpe |")
    report_lines.append(f"|------|--------|-----|---------|--------|----------|--------|")
    for p in all_pairs:
        report_lines.append(f"| {p['pair']} | {p['trades']} | {p['roi']:.2f}% | {p['win_rate']:.1f}% | {p['profit_abs']:.2f}U | {p['drawdown']:.1f}% | {p['sharpe']:.2f} |")

    # Recommended pairs
    if recommended:
        report_lines.append(f"\n## Recommended Pairs for Hyperopt")
        report_lines.append(f"\n*Selection criteria: ROI > avg ({summary['avg_roi']:.2f}%), WinRate > avg ({summary['avg_winrate']:.1f}%)*")
        report_lines.append(f"\n| Pair | Trades | ROI | WinRate |")
        report_lines.append(f"|------|--------|-----|---------|")
        for p in recommended:
            report_lines.append(f"| {p['pair']} | {p['trades']} | {p['roi']:.2f}% | {p['win_rate']:.1f}% |")

        # Copy-paste list
        pair_list = [p['pair'] for p in recommended[:10]]
        report_lines.append(f"\n### Recommended Pair List (copy-paste)")
        report_lines.append(f"\n```")
        report_lines.append(f"{','.join(pair_list)}")
        report_lines.append(f"```")

    # Reliable recommended (trades >= 3)
    if reliable:
        report_lines.append(f"\n## Reliable Recommendations (trades >= 3)")
        report_lines.append(f"\n*These pairs have sufficient trades for meaningful statistics*")
        report_lines.append(f"\n| Pair | Trades | ROI | WinRate |")
        report_lines.append(f"|------|--------|-----|---------|")
        for p in reliable:
            report_lines.append(f"| {p['pair']} | {p['trades']} | {p['roi']:.2f}% | {p['win_rate']:.1f}% |")

        reliable_list = [p['pair'] for p in reliable[:10]]
        report_lines.append(f"\n### Reliable Pair List")
        report_lines.append(f"\n```")
        report_lines.append(f"{','.join(reliable_list)}")
        report_lines.append(f"```")
    else:
        report_lines.append(f"\n**⚠️ No pairs with >= 3 trades meet recommendation criteria**")
        report_lines.append(f"\nConsider using top performers by ROI instead.")

    report = '\n'.join(report_lines)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"\nReport saved to: {output_path}")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Select best trading pairs for a Freqtrade strategy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--strategy", required=True, help="Strategy name")
    parser.add_argument("--timerange", help="Backtest timerange (e.g., 20260101-20260418)")
    parser.add_argument("--period", choices=[
        "2025_year", "2026_q1",
        "last_1_week", "last_1_month", "last_3_months",
        "last_6_months", "last_1_year",
    ], help="Period shorthand")
    parser.add_argument("--config", default="user_data/config.json", help="Config path")
    parser.add_argument("--output", help="Output report path (markdown)")
    parser.add_argument("--json", help="Output JSON results path")
    parser.add_argument("--no-docker", action="store_true", help="Use native freqtrade")

    args = parser.parse_args()

    # Determine timerange
    timerange = args.timerange if args.timerange else get_timerange(args.period)

    project_root = Path(__file__).parent.parent
    config_path = project_root / args.config

    # Run backtest
    try:
        zip_path = run_backtest(args.strategy, timerange, str(config_path), not args.no_docker)
        print(f"Backtest completed: {zip_path}")
    except Exception as e:
        print(f"Error running backtest: {e}")
        return

    # Extract performance
    try:
        results = extract_pair_performance(zip_path)
    except Exception as e:
        print(f"Error extracting results: {e}")
        return

    # Generate report
    output_path = project_root / args.output if args.output else project_root / "user_data" / f"pair_selection_{args.strategy}.md"
    report = generate_report(results, args.strategy, timerange, output_path)
    print(report)

    # Save JSON if requested
    if args.json:
        json_path = project_root / args.json
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nJSON saved to: {json_path}")


if __name__ == "__main__":
    main()