#!/usr/bin/env python3
"""
Extract pair-by-pair analysis from backtest result JSON.
"""

import json
import sys
from pathlib import Path


def analyze_backtest_result(json_path: str):
    """Analyze backtest result and print pair-by-pair performance."""

    with open(json_path, 'r') as f:
        data = json.load(f)

    # Find strategy
    strategies = data.get('strategy', {})
    if not strategies:
        print("No strategy results found")
        return

    for strategy_name, results in strategies.items():
        print(f"\n{'='*80}")
        print(f"Pair Analysis for Strategy: {strategy_name}")
        print(f"{'='*80}\n")

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

            if trades > 0 and pair != 'TOTAL':
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
                })

        if not pairs_with_trades:
            print("No trades recorded for any pair")
            continue

        # Sort by ROI
        pairs_with_trades.sort(key=lambda x: x['roi'], reverse=True)

        # Calculate averages
        avg_roi = sum(p['roi'] for p in pairs_with_trades) / len(pairs_with_trades)
        avg_winrate = sum(p['win_rate'] for p in pairs_with_trades) / len(pairs_with_trades)
        avg_trades = sum(p['trades'] for p in pairs_with_trades) / len(pairs_with_trades)

        print(f"Summary:")
        print(f"  - Pairs with trades: {len(pairs_with_trades)}")
        print(f"  - Average ROI: {avg_roi:.2f}%")
        print(f"  - Average WinRate: {avg_winrate:.1f}%")
        print(f"  - Average Trades: {avg_trades:.1f}")
        print()

        # Print table
        print(f"{'Pair':<15} {'Trades':>8} {'ROI':>10} {'WinRate':>10} {'Profit':>12} {'Drawdown':>10}")
        print('-'*65)
        for p in pairs_with_trades:
            print(f"{p['pair']:<15} {p['trades']:>8} {p['roi']:>9.2f}% {p['win_rate']:>9.1f}% {p['profit_abs']:>11.2f}U {p['drawdown']:>9.1f}%")

        # Recommend pairs (ROI > avg, WinRate > avg)
        recommended = [p for p in pairs_with_trades if p['roi'] > avg_roi and p['win_rate'] > avg_winrate]
        recommended.sort(key=lambda x: x['roi'], reverse=True)

        print()
        print(f"Recommended pairs for hyperopt (ROI & WinRate above average):")
        print(f"{'Pair':<15} {'ROI':>10} {'WinRate':>10} {'Trades':>8}")
        print('-'*45)
        for p in recommended[:15]:
            print(f"{p['pair']:<15} {p['roi']:>9.2f}% {p['win_rate']:>9.1f}% {p['trades']:>8}")

        # Generate copy-paste list
        if recommended:
            pair_list = [p['pair'] for p in recommended[:10]]
            print()
            print(f"Recommended pairs list (copy-paste for config):")
            print(f"  {','.join(pair_list)}")

        return pairs_with_trades, recommended


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pair_analysis.py <backtest-result.json>")
        sys.exit(1)

    json_path = sys.argv[1]
    analyze_backtest_result(json_path)