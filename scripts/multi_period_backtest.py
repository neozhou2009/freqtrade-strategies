#!/usr/bin/env python3
"""
多周期回测评分脚本
运行指定策略在3个月、6个月、12个月时间段的回测，并计算VecScore
"""

import os
import json
import subprocess
import re
from datetime import datetime
from pathlib import Path

# 配置
STRATEGIES = [
    "NostalgiaForInfinityXw",
    "NostalgiaForInfinityV7",
    "NostalgiaForInfinityV6HO",
    "NFI7MOHO",
    "NostalgiaForInfinityX2",
]

# 时间范围（从2026-04-16往前推）
PERIODS = {
    "3m": "20260116-20260416",   # 最近3个月
    "6m": "20251016-20260416",   # 最近6个月
    "12m": "20250416-20260416",  # 最近12个月
}

DOCKER_IMAGE = "neozhou2009/freqtrade-full:latest"
USER_DATA_DIR = "user_data"

def parse_backtest_output(stdout: str) -> dict:
    """从回测输出中提取关键指标"""
    metrics = {
        "roi": None,
        "trades": None,
        "profit_factor": None,
        "sharpe": None,
        "max_drawdown": None,
        "avg_profit": None,
        "wins": None,
        "losses": None,
    }

    # 尝试解析JSON结果块
    json_match = re.search(r'\{["\s]*"strategy"["\s]*:', stdout, re.DOTALL)
    if json_match:
        try:
            start_idx = json_match.start()
            brace_count = 0
            end_idx = start_idx
            for i, ch in enumerate(stdout[start_idx:], start=start_idx):
                if ch == '{':
                    brace_count += 1
                elif ch == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            data = json.loads(stdout[start_idx:end_idx])
            strat_data = list(data.get("strategy", {}).values())
            if strat_data:
                sd = strat_data[0]
                metrics["roi"] = sd.get("profit_total", sd.get("profit_total_abs", None))
                metrics["trades"] = sd.get("total_trades", None)
                metrics["wins"] = sd.get("wins", None)
                metrics["losses"] = sd.get("losses", None)
                metrics["profit_factor"] = sd.get("profit_factor", None)
                metrics["sharpe"] = sd.get("sharpe", None)
                metrics["max_drawdown"] = sd.get("max_drawdown", sd.get("max_drawdown_abs", None))
                metrics["avg_profit"] = sd.get("profit_mean", None)
                return metrics
        except Exception:
            pass

    # 正则提取
    patterns = {
        "roi": r"Total profit\s*%?\s*[│|]\s*([-\d.]+)\s*%",
        "trades": r"Total[/\s]?(?:Daily\s+Avg\s+)?Trades\s*[│|]\s*(\d+)",
        "profit_factor": r"Profit factor\s*[│|]\s*([\d.]+)",
        "sharpe": r"Sharpe\s*[│|]\s*([-\d.]+)",
        "max_drawdown": r"Max.{0,10}Drawdown.*?\(([\d.]+)%\)",
    }

    for key, pattern in patterns.items():
        m = re.search(pattern, stdout, re.IGNORECASE)
        if m:
            try:
                val = float(m.group(1))
                if "%" in pattern and key != "max_drawdown":
                    val = val / 100
                metrics[key] = val
            except ValueError:
                pass

    if metrics["trades"] is not None:
        metrics["trades"] = int(metrics["trades"])

    return metrics

def run_backtest(strategy: str, timerange: str) -> dict:
    """运行单个策略的回测"""
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}/{USER_DATA_DIR}:/freqtrade/user_data",
        DOCKER_IMAGE,
        "backtesting",
        "--userdir", "/freqtrade/user_data",
        "--strategy", strategy,
        "--timerange", timerange,
        "--timeframe", "5m",
        "--config", "/freqtrade/user_data/config.json",
        "--max-open-trades", "3",
        "--stake-amount", "100",
        "--dry-run-wallet", "10000",
        "--export", "none",
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        output = proc.stdout + proc.stderr

        if proc.returncode != 0:
            return {"status": "error", "returncode": proc.returncode, "output": output[-500:]}

        metrics = parse_backtest_output(output)
        return {"status": "success", "metrics": metrics}

    except subprocess.TimeoutExpired:
        return {"status": "timeout"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def calculate_vecscore_fast(metrics: dict) -> dict:
    """快速估算VecScore (fast模式)"""
    if not metrics or metrics.get("roi") is None:
        return {"vecscore": 0, "grade": "D", "P": 0, "R": 0, "S": 2, "T": 6, "E": 5}

    roi = metrics.get("roi", 0)
    pf = metrics.get("profit_factor", 0)
    sharpe = metrics.get("sharpe", 0)
    mdd = metrics.get("max_drawdown", 0) or 0
    trades = metrics.get("trades", 0)

    # P维度 (收益) - 满分30
    annual_roi = roi * (12 if roi > 0 else 12)  # 简化年化
    if annual_roi < 0:
        p_score = 0
    elif annual_roi < 0.01:
        p_score = 2
    elif annual_roi < 0.05:
        p_score = 8
    elif annual_roi < 0.10:
        p_score = 11
    else:
        p_score = 15

    if pf and pf > 1.5:
        p_score += min(10, int((pf - 1) * 5))

    # R维度 (风控) - 满分25
    r_score = 15  # MDD基础分
    if mdd < 0.05:
        r_score += 10
    elif mdd < 0.15:
        r_score += 5

    if sharpe > 0:
        r_score += min(10, int(sharpe * 2))

    # 硬红线检查
    hard_cap = None
    if mdd > 0.4:
        hard_cap = 40
    elif sharpe < 0:
        hard_cap = 50

    # S维度 (稳定) - fast模式估算
    s_score = min(10, 5 + int(abs(roi) * 20)) if roi > 0 else 2

    # T维度 (可靠) - fast模式估算
    t_score = 6  # 默认含Hyperopt参数

    # E维度 (效率) - 满分10
    if trades >= 20:
        e_score = 5
    elif trades >= 10:
        e_score = 4
    elif trades >= 5:
        e_score = 3
    else:
        e_score = 2
    e_score += 3  # 持仓时间基础分

    total = p_score + r_score + s_score + t_score + e_score

    if hard_cap:
        total = min(total, hard_cap)

    # 等级判定
    if total >= 80:
        grade = "S"
    elif total >= 70:
        grade = "A"
    elif total >= 60:
        grade = "B"
    elif total >= 50:
        grade = "C"
    else:
        grade = "D"

    return {
        "vecscore": total,
        "grade": grade,
        "P": p_score,
        "R": r_score,
        "S": s_score,
        "T": t_score,
        "E": e_score,
        "hard_cap": hard_cap,
        "inputs": {"roi": roi, "pf": pf, "sharpe": sharpe, "mdd": mdd, "trades": trades}
    }

def main():
    results = {}

    print("=" * 70)
    print("多周期回测评分")
    print("=" * 70)
    print(f"策略: {len(STRATEGIES)} 个")
    print(f"周期: {list(PERIODS.keys())}")
    print("=" * 70)

    for period_name, timerange in PERIODS.items():
        print(f"\n📊 周期: {period_name} ({timerange})")
        print("-" * 50)

        period_results = []

        for strategy in STRATEGIES:
            print(f"  → {strategy}...")
            result = run_backtest(strategy, timerange)

            if result["status"] == "success":
                metrics = result["metrics"]
                score = calculate_vecscore_fast(metrics)
                period_results.append({
                    "strategy": strategy,
                    "metrics": metrics,
                    "vecscore": score,
                })
                badge = {"S": "🏆", "A": "⭐", "B": "✅", "C": "⚠️", "D": "❌"}[score["grade"]]
                print(f"     VecScore: {score['vecscore']} [{score['grade']}] {badge}  "
                      f"ROI={metrics.get('roi', 0):+.2%}  Trades={metrics.get('trades', 0)}")
            else:
                print(f"     ❌ {result['status']}: {result.get('output', '')[:80]}")
                period_results.append({
                    "strategy": strategy,
                    "status": result["status"],
                    "error": result.get("output", result.get("message", "unknown")),
                })

        results[period_name] = period_results

    # 保存结果
    output_file = "user_data/multi_period_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "meta": {
                "generated_at": datetime.now().isoformat(),
                "strategies": STRATEGIES,
                "periods": PERIODS,
                "mode": "spot",
                "exchange": "binance",
            },
            "results": results,
        }, f, ensure_ascii=False, indent=2)

    print(f"\n💾 结果已保存到: {output_file}")

    # 打印汇总
    print("\n" + "=" * 70)
    print("📋 多周期评分汇总")
    print("=" * 70)

    for strategy in STRATEGIES:
        scores = []
        for period_name in PERIODS.keys():
            period_data = results[period_name]
            for r in period_data:
                if r.get("strategy") == strategy and r.get("vecscore"):
                    scores.append(r["vecscore"]["vecscore"])

        if scores:
            avg_score = sum(scores) / len(scores)
            print(f"  {strategy:<40} 平均VecScore: {avg_score:.1f}")

if __name__ == "__main__":
    main()