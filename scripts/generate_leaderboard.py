#!/usr/bin/env python3
import os
import json
import glob
import argparse
import zipfile
import tempfile


def load_registry():
    if os.path.exists("strategy_registry.json"):
        with open("strategy_registry.json", "r") as f:
            return json.load(f)
    print("[!] strategy_registry.json not found, using generic categorizations.")
    return {}


def extract_json_from_zip(zip_path):
    """Extract and read JSON data from a Freqtrade backtest zip file."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                if name.endswith(".json") and not name.endswith("_config.json"):
                    with zf.open(name) as f:
                        return json.load(f)
    except Exception as e:
        print(f"[!] Error reading zip {zip_path}: {e}")
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate Leaderboard from Freqtrade Backtests"
    )
    parser.add_argument(
        "--input-dir",
        default="test/user_data/backtest_results",
        help="Directory containing backtest files (default: test/user_data/backtest_results)",
    )
    parser.add_argument(
        "--period", default="Custom", help="Period identifier for the markdown title"
    )
    args = parser.parse_args()

    registry = load_registry()
    results = []

    # Find all backtest result files (both .json and .zip) and sort them for idempotency
    json_files = sorted(glob.glob(os.path.join(args.input_dir, "*.json")))
    zip_files = sorted(glob.glob(os.path.join(args.input_dir, "*.zip")))

    print(
        f"[*] Found {len(json_files)} JSON files and {len(zip_files)} ZIP files in {args.input_dir}"
    )

    # Process JSON files
    for filepath in json_files:
        if "leaderboard.json" in filepath or filepath.endswith("_config.json"):
            continue
        if ".meta.json" in filepath:
            continue
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
            process_backtest_data(data, registry, results)
        except Exception as e:
            print(f"[!] Error reading {filepath}: {e}")

    # Process ZIP files (Freqtrade's default format)
    for zip_path in zip_files:
        data = extract_json_from_zip(zip_path)
        if data:
            process_backtest_data(data, registry, results)

    if not results:
        print("[!] No results found to generate leaderboard.")
        return

    # Sort results globally by absolute profit for leaderboard JSON
    results.sort(key=lambda x: x["profit_total_abs"], reverse=True)

    # Output JSON aggregate
    out_json = "leaderboard.json"
    with open(out_json, "w") as f:
        json.dump(
            {
                "period": args.period,
                "strat_count": len(results),
                "leaderboard": results,
            },
            f,
            indent=2,
            sort_keys=True,
        )
    print(f"[*] Generated JSON leaderboard at {out_json}")

    # Generate Markdown grouped by category
    categories = {}
    for r in results:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)

    out_md = "LEADERBOARD.md"
    with open(out_md, "w") as f:
        f.write(f"# Strategy Leaderboard: {args.period}\n\n")
        f.write(f"Total strategies: {len(results)}\n\n")
        f.write("This leaderboard ranks strategies based on backtest performance.\n\n")

        for cat in sorted(categories.keys()):
            cat_results = categories[cat]
            cat_results.sort(key=lambda x: x["profit_total_abs"], reverse=True)
            f.write(f"## Category: {cat}\n\n")
            f.write(
                "| Rank | Strategy | Family | Side | Comp. | TF | Profit | Win% | Sharpe |\n"
            )
            f.write(
                "|------|----------|--------|------|-------|----|--------|------|--------|\n"
            )

            for idx, r in enumerate(cat_results):
                strat_name = r["strategy"]
                family = r.get("family", "-")
                side = r.get("side", "Long")
                complexity = f"{r.get('complexity', 5)}/10"
                tf = r.get("timeframe", "-")
                profit = f"{r['profit_total_abs']:.2f}"
                winrate = f"{r['winrate'] * 100:.1f}%"
                sharpe = f"{r['sharpe']:.2f}"

                f.write(
                    f"| {idx+1} | {strat_name} | {family} | {side} | {complexity} | {tf} | {profit} | {winrate} | {sharpe} |\n"
                )

            f.write("\n")

    print(f"[*] Generated Markdown leaderboard at {out_md}")


def process_backtest_data(data, registry, results):
    """Process backtest data and append to results."""
    strategies_data = data.get("strategy", {})
    for strat_name, strat_info in strategies_data.items():
        if strat_name == "StrategyTest":
            continue

        metrics = strat_info.get("results_per_pair", [])
        total_metrics = next((m for m in metrics if m.get("key") == "TOTAL"), {})
        
        reg_info = registry.get(strat_name, {})

        strat_result = {
            "strategy": strat_name,
            "category": reg_info.get("style", ["Uncategorized"])[0],
            "styles": reg_info.get("style", []),
            "family": reg_info.get("family", strat_name),
            "complexity": reg_info.get("complexity", 5),
            "side": reg_info.get("side", "Long"),
            "indicators": reg_info.get("indicators", []),
            "timeframe": reg_info.get("timeframe", "unknown"),
            "profit_total_abs": total_metrics.get("profit_total_abs", 0.0),
            "profit_total_pct": total_metrics.get("profit_total_pct", 0.0),
            "winrate": total_metrics.get("winrate", 0.0),
            "trades": total_metrics.get("trades", 0),
            "max_drawdown_abs": strat_info.get("max_drawdown_abs", 0.0),
            "profit_factor": total_metrics.get("profit_factor", 0.0),
            "sharpe": total_metrics.get("sharpe", 0.0),
        }
        results.append(strat_result)


if __name__ == "__main__":
    main()
