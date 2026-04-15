#!/usr/bin/env python3
import os
import json
import glob
import argparse
import zipfile
from datetime import datetime

OUTPUT_DIR = "user_data/leaderboard"
HISTORY_FILE = os.path.join(OUTPUT_DIR, "history.json")
OUT_JSON = os.path.join(OUTPUT_DIR, "leaderboard.json")
OUT_MD = os.path.join(OUTPUT_DIR, "LEADERBOARD.md")

def load_registry():
    if os.path.exists("strategy_registry.json"):
        with open("strategy_registry.json", "r") as f:
            return json.load(f)
    print("[!] strategy_registry.json not found, using generic categorizations.")
    return {}

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Error loading history: {e}")
    return {"snapshots": []}

def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

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

def calculate_composite_score(strat: dict) -> float:
    """
    Comprehensive scoring 0–100.
    Weights: CAGR (40%), Sharpe (25%), Max Drawdown (20%), Win Rate (10%), Trades (5%)
    """
    # 1. CAGR (40%): Cap at 150%
    cagr = strat.get("cagr", 0)
    cagr_score = min(cagr, 1.5) / 1.5 * 40
    
    # 2. Sharpe (25%): Cap at 4.0
    sharpe = max(strat.get("sharpe", 0), 0)
    sharpe_score = min(sharpe, 4.0) / 4.0 * 25
    
    # 3. Max Drawdown Penalty (20%): 0 score if > 50% drawdown
    max_dd = strat.get("max_drawdown_pct", 0.5)
    dd_score = max(0, (1 - max_dd / 0.5)) * 20
    
    # 4. Win Rate (10%): Score starts from 50%
    winrate = strat.get("winrate", 0)
    wr_score = max(0, (winrate - 0.5) / 0.5) * 10
    
    # 5. Trades count (5%): Cap at 500 trades for statistical significance
    trades = strat.get("trades", 0)
    trades_score = min(trades / 500, 1.0) * 5
    
    total_score = cagr_score + sharpe_score + dd_score + wr_score + trades_score
    return round(min(total_score, 100), 1)

def main():
    parser = argparse.ArgumentParser(
        description="Generate Leaderboard from Freqtrade Backtests"
    )
    parser.add_argument(
        "--input-dir",
        default="user_data/backtest_results",
        help="Directory containing backtest files",
    )
    parser.add_argument(
        "--period", default="Custom", help="Period identifier"
    )
    parser.add_argument(
        "--vecscore", default=None, help="Path to vecscore_results.json to use directly, bypassing raw backtest inputs"
    )
    args = parser.parse_args()

    registry = load_registry()
    history = load_history()
    results = []

    if args.vecscore:
        if not os.path.exists(args.vecscore):
            print(f"[!] Vecscore file not found: {args.vecscore}")
            return
        print(f"[*] Loading VecScore from {args.vecscore}")
        with open(args.vecscore, "r") as f:
            vdata = json.load(f)
        
        # Read the raw phase1 results to attach extra metrics like winrate if needed
        phase1_path = args.vecscore.replace("vecscore_results.json", "phase1_results.json")
        phase1_map = {}
        if os.path.exists(phase1_path):
            with open(phase1_path, "r") as f:
                p1_data = json.load(f)
                for r in p1_data.get("results", []):
                    phase1_map[r["name"]] = r.get("metrics", {})

        for item in vdata.get("ranked", []):
            strat_name = item["name"]
            reg_info = registry.get(strat_name, {})
            p_inputs = item.get("details", {}).get("P_return", {}).get("inputs", {})
            r_inputs = item.get("details", {}).get("R_risk", {}).get("inputs", {})
            e_inputs = item.get("details", {}).get("E_efficiency", {}).get("inputs", {})
            
            p1_metrics = phase1_map.get(strat_name, {})

            strat_result = {
                "strategy": strat_name,
                "category": reg_info.get("style", ["Uncategorized"])[0],
                "styles": reg_info.get("style", []),
                "family": reg_info.get("family", strat_name),
                "complexity": reg_info.get("complexity", 5),
                "side": reg_info.get("side", "Long"),
                "indicators": reg_info.get("indicators", []),
                "timeframe": item.get("timeframe", reg_info.get("timeframe", "unknown")),
                
                # Use VecScore directly
                "composite_score": item["vecscore"],
                "grade": item.get("grade", "D"),
                "badge": item.get("badge", ""),
                "commercial_eligible": item.get("commercial_eligible", False),
                "is_estimated": item.get("is_estimated", True),
                
                # Map metrics to UI fields
                "cagr": p_inputs.get("roi", 0.0), # UI uses 'cagr' for annualized ROI, here we map 30d ROI directly or handle in UI
                "sharpe": r_inputs.get("sharpe", 0.0),
                "max_drawdown_pct": r_inputs.get("max_drawdown", 0.0),
                "max_drawdown_abs": 0.0,
                "trades": e_inputs.get("trades_30d", 0),
                "winrate": p1_metrics.get("win_rate", 0.0),
                "profit_factor": p_inputs.get("profit_factor", 0.0),
            }
            results.append(strat_result)
    else:
        # Find all backtest result files
        json_files = sorted(glob.glob(os.path.join(args.input_dir, "*.json")))
        zip_files = sorted(glob.glob(os.path.join(args.input_dir, "*.zip")))

        print(f"[*] Found {len(json_files)} JSON files and {len(zip_files)} ZIP files")

        # Process files
        for filepath in json_files:
            if any(x in filepath for x in ["leaderboard.json", "_config.json", ".meta.json"]):
                continue
            try:
                with open(filepath, "r") as f:
                    process_backtest_data(json.load(f), registry, results)
            except Exception as e:
                print(f"[!] Error reading {filepath}: {e}")

        for zip_path in zip_files:
            data = extract_json_from_zip(zip_path)
            if data:
                process_backtest_data(data, registry, results)

        if not results:
            print("[!] No results found.")
            return

        # Calculate Composite Score for each (legacy mode)
        for r in results:
            r["composite_score"] = calculate_composite_score(r)

    # Sort by composite score
    results.sort(key=lambda x: x["composite_score"], reverse=True)

    # Get previous rankings for delta calculation
    last_ranking = history["snapshots"][-1]["rankings"] if history["snapshots"] else {}
    
    # Add rank and rank_delta
    current_rankings = {}
    for idx, r in enumerate(results):
        rank = idx + 1
        r["rank"] = rank
        prev_rank = last_ranking.get(r["strategy"])
        r["rank_delta"] = prev_rank - rank if prev_rank else 0
        current_rankings[r["strategy"]] = rank

    # Save snapshot to history
    history["snapshots"].append({
        "generated_at": datetime.now().isoformat(),
        "period": args.period,
        "rankings": current_rankings
    })
    # Keep only last 10 snapshots
    history["snapshots"] = history["snapshots"][-10:]
    save_history(history)

    # Calculate Summary Stats
    summary = {
        "avg_score": round(sum(r["composite_score"] for r in results) / len(results), 1),
        "avg_cagr": round(sum(r.get("cagr", 0) for r in results) / len(results), 3),
        "avg_sharpe": round(sum(r["sharpe"] for r in results) / len(results), 2),
    }

    # Output filenames based on period
    period_slug = args.period.lower().replace(" ", "_").replace("/", "_")
    # Normalise aliases so DB period values match the leaderboard API enum
    _PERIOD_ALIAS = {"2025_year": "last_1_year"}
    period_slug = _PERIOD_ALIAS.get(period_slug, period_slug)
    out_json = os.path.join(OUTPUT_DIR, f"leaderboard_{period_slug}.json")
    out_md = os.path.join(OUTPUT_DIR, f"LEADERBOARD_{period_slug}.md")

    # Output JSON aggregate
    with open(out_json, "w") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "period": args.period,
            "period_slug": period_slug,
            "strat_count": len(results),
            "summary": summary,
            "leaderboard": results,
        }, f, indent=2, sort_keys=True)
    print(f"[*] Generated JSON leaderboard at {out_json}")

    # Generate Markdown
    categories = {}
    for r in results:
        categories.setdefault(r["category"], []).append(r)

    with open(out_md, "w") as f:
        f.write(f"# Strategy Leaderboard: {args.period}\n\n")
        f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("| Metrics | Average |\n|---|---|\n")
        f.write(f"| Score | {summary['avg_score']} |\n")
        f.write(f"| CAGR | {summary['avg_cagr']*100:.1f}% |\n")
        f.write(f"| Sharpe | {summary['avg_sharpe']} |\n\n")

        for cat in sorted(categories.keys()):
            cat_results = sorted(categories[cat], key=lambda x: x["composite_score"], reverse=True)
            f.write(f"## Category: {cat}\n\n")
            f.write("| Rank | Delta | Strategy | Score | CAGR% | Sharpe | MaxDD% | Win% | Trades |\n")
            f.write("|---|---|---|---|---|---|---|---|---|\n")
            for r in cat_results:
                delta = f"↑{r['rank_delta']}" if r['rank_delta'] > 0 else (f"↓{abs(r['rank_delta'])}" if r['rank_delta'] < 0 else "-")
                cagr = (r.get('cagr') or 0) * 100
                sharpe = r.get('sharpe') or 0
                max_dd = (r.get('max_drawdown_pct') or 0) * 100
                winrate = (r.get('winrate') or 0) * 100
                trades = r.get('trades') or 0
                f.write(f"| {r['rank']} | {delta} | {r['strategy']} | **{r['composite_score']}** | {cagr:.1f}% | {sharpe:.2f} | {max_dd:.1f}% | {winrate:.1f}% | {trades} |\n")
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
            "max_drawdown_pct": strat_info.get("max_drawdown", 0.0),
            "profit_factor": total_metrics.get("profit_factor", 0.0),
            "sharpe": total_metrics.get("sharpe", 0.0),
            "cagr": total_metrics.get("cagr", 0.0),
            "sortino": total_metrics.get("sortino", 0.0),
            "calmar": total_metrics.get("calmar", 0.0),
        }
        results.append(strat_result)

if __name__ == "__main__":
    main()
