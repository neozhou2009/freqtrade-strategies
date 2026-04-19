#!/usr/bin/env python3
"""
Pair Performance Analyzer for Freqtrade Strategies

Run backtest for each pair individually and analyze performance to recommend
best pair combinations for hyperopt optimization.

Usage:
    python scripts/analyze_pair_performance.py --strategy BBRSITV --timerange 20260101-20260418
    python scripts/analyze_pair_performance.py --strategy BBRSITV --period last_1_month
"""

import os
import json
import subprocess
import argparse
import re
import sys
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
        # Assume it's already a timerange format like 20260101-20260418
        if re.match(r"\d{8}-\d{8}", period):
            return period
        raise ValueError(f"Unknown period: {period}")
    return f"{start.strftime('%Y%m%d')}-{now.strftime('%Y%m%d')}"


def load_pairs_from_config(config_path: str) -> list:
    """Load pair whitelist from config.json."""
    with open(config_path, "r") as f:
        config = json.load(f)
    return config.get("exchange", {}).get("pair_whitelist", [])


def run_backtest_for_pair(
    strategy: str,
    pair: str,
    timerange: str,
    config_path: str,
    use_docker: bool = True,
) -> dict | None:
    """Run backtest for a single pair and parse results."""

    # Build command
    if use_docker:
        # Docker command
        project_root = Path(__file__).parent.parent
        user_data_dir = project_root / "user_data"

        cmd = [
            "docker", "run", "--rm",
            "-v", f"{user_data_dir}:/freqtrade/user_data",
            "neozhou2009/freqtrade-full:latest",
            "backtesting",
            "--config", "/freqtrade/user_data/config.json",
            "--strategy", strategy,
            "--pairs", pair,
            "--timerange", timerange,
        ]
    else:
        # Native freqtrade command
        cmd = [
            "freqtrade", "backtesting",
            "--config", config_path,
            "--strategy", strategy,
            "--pairs", pair,
            "--timerange", timerange,
        ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,  # 2 minutes per pair
        )
        return parse_backtest_output(result.stdout, pair)
    except subprocess.TimeoutExpired:
        print(f"  [TIMEOUT] {pair}")
        return None
    except Exception as e:
        print(f"  [ERROR] {pair}: {e}")
        return None


def parse_backtest_output(output: str, pair: str) -> dict | None:
    """Parse backtest output to extract performance metrics."""

    result = {
        "pair": pair,
        "trades": 0,
        "profit_mean": 0.0,
        "profit_total": 0.0,
        "profit_total_abs": 0.0,
        "win_rate": 0.0,
        "drawdown": 0.0,
        "avg_duration": "",
    }

    # Look for the strategy summary table
    # Format: | Strategy | Buys | Avg Profit % | Cum Profit % | Tot Profit USDT | ...

    # Find the line with results
    lines = output.split("\n")

    for line in lines:
        # Match strategy result line
        if "|" in line and strategy_name_pattern(line):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 9:
                try:
                    # Parse values from table
                    # Format: | Strategy | Buys | Avg Profit % | Cum Profit % | Tot Profit USDT | Tot Profit % | Avg Duration | Win Draw Loss Win% | Drawdown |
                    result["trades"] = int(parts[2]) if parts[2] else 0
                    result["profit_mean"] = float(parts[3].replace("%", "")) if parts[3] else 0.0
                    result["profit_total"] = float(parts[4].replace("%", "")) if parts[4] else 0.0

                    # Parse win/draw/loss for win rate
                    win_loss_parts = parts[8].split()
                    if len(win_loss_parts) >= 4:
                        wins = int(win_loss_parts[0])
                        losses = int(win_loss_parts[2])
                        total = wins + losses
                        if total > 0:
                            result["win_rate"] = (wins / total) * 100

                    # Parse drawdown
                    dd_part = parts[9] if len(parts) > 9 else ""
                    if dd_part:
                        # Format: "123.45 USDT  12.34%"
                        dd_match = re.search(r"(\d+\.?\d*)\s*%", dd_part)
                        if dd_match:
                            result["drawdown"] = float(dd_match.group(1))

                    result["avg_duration"] = parts[7] if len(parts) > 7 else ""

                    return result if result["trades"] > 0 else None
                except (ValueError, IndexError):
                    continue

    # Alternative parsing: look for JSON output if available
    # Check if there's a results file
    return None


def strategy_name_pattern(line: str) -> bool:
    """Check if line contains strategy results."""
    return bool(re.search(r"\|\s+\w+\s+\|\s+\d+\s+\|", line))


def analyze_all_pairs(
    strategy: str,
    pairs: list,
    timerange: str,
    config_path: str,
    use_docker: bool = True,
    max_workers: int = 1,
) -> list:
    """Run backtest for all pairs and collect results."""

    results = []

    print(f"\n{'='*60}")
    print(f"Analyzing pairs for strategy: {strategy}")
    print(f"Timerange: {timerange}")
    print(f"Total pairs: {len(pairs)}")
    print(f"{'='*60}\n")

    for i, pair in enumerate(pairs):
        print(f"[{i+1}/{len(pairs)}] Testing {pair}...")
        result = run_backtest_for_pair(strategy, pair, timerange, config_path, use_docker)
        if result:
            results.append(result)
            print(f"  Trades: {result['trades']}, ROI: {result['profit_total']:.2f}%, WinRate: {result['win_rate']:.1f}%")
        else:
            print(f"  [NO TRADES]")

    return results


def generate_recommendations(results: list) -> dict:
    """Generate recommendations based on pair performance."""

    if not results:
        return {"error": "No valid results to analyze"}

    # Sort by different metrics
    by_roi = sorted(results, key=lambda x: x["profit_total"], reverse=True)
    by_winrate = sorted(results, key=lambda x: x["win_rate"], reverse=True)
    by_trades = sorted(results, key=lambda x: x["trades"], reverse=True)

    # Calculate average metrics
    avg_roi = sum(r["profit_total"] for r in results) / len(results)
    avg_winrate = sum(r["win_rate"] for r in results) / len(results)
    avg_trades = sum(r["trades"] for r in results) / len(results)

    # Recommend top pairs (ROI > average, WinRate > average)
    recommended = [
        r for r in results
        if r["profit_total"] > avg_roi and r["win_rate"] > avg_winrate
    ]

    # Sort recommended by ROI
    recommended = sorted(recommended, key=lambda x: x["profit_total"], reverse=True)

    return {
        "summary": {
            "total_pairs_tested": len(results),
            "avg_roi": avg_roi,
            "avg_winrate": avg_winrate,
            "avg_trades": avg_trades,
        },
        "top_by_roi": by_roi[:10],
        "top_by_winrate": by_winrate[:10],
        "top_by_trades": by_trades[:10],
        "recommended_pairs": recommended,
        "all_results": results,
    }


def print_report(recommendations: dict, output_file: str = None):
    """Print a formatted report."""

    report_lines = []

    report_lines.append("\n" + "=" * 60)
    report_lines.append("PAIR PERFORMANCE ANALYSIS REPORT")
    report_lines.append("=" * 60)

    summary = recommendations.get("summary", {})
    report_lines.append(f"\n📊 Summary:")
    report_lines.append(f"  - Pairs with trades: {summary.get('total_pairs_tested', 0)}")
    report_lines.append(f"  - Average ROI: {summary.get('avg_roi', 0):.2f}%")
    report_lines.append(f"  - Average WinRate: {summary.get('avg_winrate', 0):.1f}%")
    report_lines.append(f"  - Average Trades: {summary.get('avg_trades', 0):.0f}")

    # Top by ROI
    report_lines.append(f"\n🏆 Top 10 by ROI:")
    report_lines.append(f"{'Pair':<15} {'ROI':>8} {'Trades':>8} {'WinRate':>8} {'MaxDD':>8}")
    report_lines.append("-" * 50)
    for r in recommendations.get("top_by_roi", []):
        report_lines.append(
            f"{r['pair']:<15} {r['profit_total']:>7.2f}% {r['trades']:>8} "
            f"{r['win_rate']:>7.1f}% {r['drawdown']:>7.1f}%"
        )

    # Top by WinRate
    report_lines.append(f"\n🎯 Top 10 by WinRate:")
    report_lines.append(f"{'Pair':<15} {'WinRate':>8} {'ROI':>8} {'Trades':>8}")
    report_lines.append("-" * 40)
    for r in recommendations.get("top_by_winrate", []):
        report_lines.append(
            f"{r['pair']:<15} {r['win_rate']:>7.1f}% {r['profit_total']:>7.2f}% {r['trades']:>8}"
        )

    # Recommended pairs for hyperopt
    recommended = recommendations.get("recommended_pairs", [])
    if recommended:
        report_lines.append(f"\n✅ Recommended for Hyperopt (ROI & WinRate above average):")
        report_lines.append(f"{'Pair':<15} {'ROI':>8} {'WinRate':>8} {'Trades':>8}")
        report_lines.append("-" * 40)
        for r in recommended[:15]:
            report_lines.append(
                f"{r['pair']:<15} {r['profit_total']:>7.2f}% {r['win_rate']:>7.1f}% {r['trades']:>8}"
            )

        # Generate pairs list for copy-paste
        pair_list = [r["pair"] for r in recommended[:10]]
        report_lines.append(f"\n📋 Recommended pairs list (copy-paste for hyperopt):")
        report_lines.append(f"  {','.join(pair_list)}")
    else:
        report_lines.append(f"\n⚠️  No pairs meet recommendation criteria (ROI & WinRate above average)")

    report_lines.append("\n" + "=" * 60)

    report = "\n".join(report_lines)
    print(report)

    if output_file:
        with open(output_file, "w") as f:
            f.write(report)
        print(f"\nReport saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze pair performance for a Freqtrade strategy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all pairs for BBRSITV over 2026 Q1
  %(prog)s --strategy BBRSITV --timerange 20260101-20260418

  # Use period shorthand
  %(prog)s --strategy BBRSITV --period last_1_month

  # Save report to file
  %(prog)s --strategy BBRSITV --period 2026_q1 --output pair_analysis.md
""",
    )
    parser.add_argument("--strategy", required=True, help="Strategy name")
    parser.add_argument(
        "--timerange",
        help="Backtest timerange (e.g., 20260101-20260418)",
    )
    parser.add_argument(
        "--period",
        choices=[
            "2025_year", "2026_q1",
            "last_1_week", "last_1_month", "last_3_months",
            "last_6_months", "last_1_year",
        ],
        help="Period shorthand (alternative to --timerange)",
    )
    parser.add_argument(
        "--config",
        default="user_data/config.json",
        help="Path to config.json",
    )
    parser.add_argument(
        "--pairs",
        help="Comma-separated list of pairs to test (default: from config)",
    )
    parser.add_argument(
        "--output",
        help="Output file for report (markdown format)",
    )
    parser.add_argument(
        "--no-docker",
        action="store_true",
        help="Use native freqtrade instead of Docker",
    )
    parser.add_argument(
        "--json",
        help="Output JSON file for raw results",
    )

    args = parser.parse_args()

    # Determine timerange
    if args.timerange:
        timerange = args.timerange
    elif args.period:
        timerange = get_timerange(args.period)
    else:
        print("Error: Must specify --timerange or --period")
        sys.exit(1)

    # Resolve config path
    project_root = Path(__file__).parent.parent
    config_path = project_root / args.config

    # Load pairs
    if args.pairs:
        pairs = [p.strip() for p in args.pairs.split(",")]
    else:
        pairs = load_pairs_from_config(str(config_path))

    print(f"Loaded {len(pairs)} pairs from config")

    # Run analysis
    results = analyze_all_pairs(
        strategy=args.strategy,
        pairs=pairs,
        timerange=timerange,
        config_path=str(config_path),
        use_docker=not args.no_docker,
    )

    # Generate recommendations
    recommendations = generate_recommendations(results)

    # Print report
    output_file = str(project_root / args.output) if args.output else None
    print_report(recommendations, output_file)

    # Save JSON if requested
    if args.json:
        json_path = project_root / args.json
        with open(json_path, "w") as f:
            json.dump(recommendations, f, indent=2)
        print(f"JSON results saved to: {json_path}")


if __name__ == "__main__":
    main()