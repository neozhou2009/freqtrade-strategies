#!/usr/bin/env python3
"""
NFI 系列现货多周期回测评分脚本
--------------------------------------------
支持57个NFI系列策略的批量回测，分批执行，生成完整评分报告

使用方法:
  python scripts/nfi_spot_backtest.py --batch 1          # 执行Batch 1
  python scripts/nfi_spot_backtest.py --batch all        # 执行全部批次
  python scripts/nfi_spot_backtest.py --strategies X,Xw  # 测试指定策略
"""

import os
import json
import subprocess
import re
import argparse
from datetime import datetime
from pathlib import Path

# 完整策略列表 (57个NFI相关)
ALL_STRATEGIES = [
    # Batch 1: TOP 10 推荐
    "NostalgiaForInfinityX",
    "NostalgiaForInfinityXw",
    "NostalgiaForInfinityX2",
    "NostalgiaForInfinityV7",
    "NostalgiaForInfinityV6HO",
    "Combined_NFIv7_SMA_bAdBoY_20211204",
    "Combined_NFIv7_SMA_Rallipanos_20210707",
    "NostalgiaForInfinityV7_SMAv2",
    "NFI7MOHO",
    "NFI5MOHO",

    # Batch 2: 主版本 V1-V7 (14个)
    "NostalgiaForInfinityV1",
    "NostalgiaForInfinityV2",
    "NostalgiaForInfinityV3",
    "NostalgiaForInfinityV4",
    "NostalgiaForInfinityV4HO",
    "NostalgiaForInfinityV5",
    "NostalgiaForInfinityV5MultiOffsetAndHO",
    "NostalgiaForInfinityV5MultiOffsetAndHO2",
    "NostalgiaForInfinityV6",
    "NostalgiaForInfinityV7_7_2",
    "NostalgiaForInfinityV7_SMA",
    "NostalgiaForInfinityV7_SMAv2_1",

    # Batch 3: X系列 + Next系列 (13个)
    "NFIX_BB_RPB",
    "NFIX_BB_RPB_c7c477d_20211030",
    "NostalgiaForInfinityNext",
    "NostalgiaForInfinityNextGen",
    "NostalgiaForInfinityNextGen_TSL",
    "NostalgiaForInfinityNextV7155",
    "NostalgiaForInfinityNext_ChangeToTower_V5_2",
    "NostalgiaForInfinityNext_ChangeToTower_V5_3",
    "NostalgiaForInfinityNext_ChangeToTower_V6",
    "NostalgiaForInfinityNext_maximizer",

    # Batch 4: NFI缩写变体 (19个)
    "NFI46",
    "NFI46Frog",
    "NFI46FrogZ",
    "NFI46Offset",
    "NFI46OffsetHOA1",
    "NFI46Z",
    "NFI47V2",
    "NFI4Frog",
    "NFI5MOHO2",
    "NFI5MOHO_WIP",
    "NFI5MOHO_WIP_1",
    "NFI5MOHO_WIP_2",
    "NFI731_BUSD",
    "NFINextMOHO",
    "NFINextMOHO2",
    "NFINextMultiOffsetAndHO",
    "NFINextMultiOffsetAndHO2",

    # Batch 5: 组合版本 + 衍生 (7个)
    "Nostalgia",
    "Combined_NFIv6_SMA",
    "Combined_NFIv7_SMA",
    "BigZ07Next",
    "BigZ07Next2",
    "CryptoFrogNFI",
    "CryptoFrogNFIHO1A",
]

# 批次定义
BATCHES = {
    1: ALL_STRATEGIES[0:10],      # TOP 10 (10个)
    2: ALL_STRATEGIES[10:22],     # V1-V7 (12个)
    3: ALL_STRATEGIES[22:32],     # X + Next (10个)
    4: ALL_STRATEGIES[32:51],     # NFI变体 (19个)
    5: ALL_STRATEGIES[51:58],     # 组合+衍生 (7个)
}

# 总策略数验证
TOTAL_STRATEGIES = len(ALL_STRATEGIES)  # 58个

# 时间范围（从2026-04-16往前推）
PERIODS = {
    "3m": "20260116-20260416",
    "6m": "20251016-20260416",
    "12m": "20250416-20260416",
}

# NextGen系列需要15m时间框架
NEXTGEN_STRATEGIES = [
    "NostalgiaForInfinityNextGen",
    "NostalgiaForInfinityNextGen_TSL",
]

DOCKER_IMAGE = "neozhou2009/freqtrade-full:latest"
USER_DATA_DIR = "user_data"
DEFAULT_TIMEFRAME = "5m"

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
        "win_rate": None,
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
                if metrics["trades"] and metrics["trades"] > 0:
                    metrics["win_rate"] = (metrics["wins"] or 0) / metrics["trades"]
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


def run_backtest(strategy: str, timerange: str, timeout: int = 300) -> dict:
    """运行单个策略的回测"""
    # NextGen系列使用15m时间框架
    timeframe = "15m" if strategy in NEXTGEN_STRATEGIES else DEFAULT_TIMEFRAME

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}/{USER_DATA_DIR}:/freqtrade/user_data",
        DOCKER_IMAGE,
        "backtesting",
        "--userdir", "/freqtrade/user_data",
        "--strategy", strategy,
        "--timerange", timerange,
        "--timeframe", timeframe,
        "--config", "/freqtrade/user_data/config.json",
        "--max-open-trades", "6",
        "--stake-amount", "unlimited",
        "--dry-run-wallet", "10000",
        "--export", "none",
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = proc.stdout + proc.stderr

        if proc.returncode != 0:
            return {"status": "error", "returncode": proc.returncode, "output": output[-500:]}

        metrics = parse_backtest_output(output)
        return {"status": "success", "metrics": metrics, "timeframe": timeframe}

    except subprocess.TimeoutExpired:
        return {"status": "timeout", "timeout": timeout}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def calculate_vecscore_fast(metrics: dict) -> dict:
    """快速估算VecScore (fast模式)"""
    if not metrics or metrics.get("roi") is None:
        return {"vecscore": 0, "grade": "D", "P": 0, "R": 0, "S": 2, "T": 6, "E": 5}

    roi = metrics.get("roi", 0)
    pf = metrics.get("profit_factor", 0) or 1
    sharpe = metrics.get("sharpe", 0) or 0
    mdd = abs(metrics.get("max_drawdown", 0) or 0)
    trades = metrics.get("trades", 0) or 0

    # P维度 (收益) - 满分30
    annual_roi = roi * 12  # 简化年化
    if annual_roi < 0:
        p_score = max(0, int(annual_roi * -10))  # 负收益扣分
    elif annual_roi < 0.01:
        p_score = 2
    elif annual_roi < 0.05:
        p_score = 8
    elif annual_roi < 0.10:
        p_score = 11
    else:
        p_score = min(20, 11 + int(annual_roi * 10))

    if pf > 1.5:
        p_score += min(10, int((pf - 1) * 5))

    # R维度 (风控) - 满分25
    r_score = 15
    if mdd < 0.05:
        r_score += 10
    elif mdd < 0.15:
        r_score += 5
    elif mdd > 0.25:
        r_score -= 5

    if sharpe > 0:
        r_score += min(10, int(sharpe * 2))
    elif sharpe < 0:
        r_score -= 5

    # 硬红线检查
    hard_cap = None
    if mdd > 0.4:
        hard_cap = 40
    elif sharpe < 0:
        hard_cap = 50

    # S维度 (稳定) - fast模式估算上限10
    if roi > 0:
        s_score = min(10, 5 + int(abs(roi) * 20))
    else:
        s_score = 2

    # T维度 (可靠) - fast模式估算
    t_score = 6

    # E维度 (效率) - 满分10
    if trades >= 30:
        e_score = 8
    elif trades >= 20:
        e_score = 6
    elif trades >= 10:
        e_score = 5
    elif trades >= 5:
        e_score = 4
    else:
        e_score = 3

    total = p_score + r_score + s_score + t_score + e_score

    if hard_cap:
        total = min(total, hard_cap)

    total = max(0, min(100, total))

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


def run_batch(batch_num: int, strategies: list, periods: dict) -> dict:
    """运行一个批次的回测"""
    batch_results = {
        "batch": batch_num,
        "strategies": strategies,
        "periods": {},
        "started": datetime.now().isoformat(),
    }

    print(f"\n{'='*70}")
    print(f"Batch {batch_num}: {len(strategies)} 个策略")
    print(f"{'='*70}")

    for period_name, timerange in periods.items():
        print(f"\n📅 周期: {period_name} ({timerange})")
        print("-" * 50)

        period_results = []

        for strategy in strategies:
            print(f"  → {strategy}...")
            result = run_backtest(strategy, timerange)

            if result["status"] == "success":
                metrics = result["metrics"]
                score = calculate_vecscore_fast(metrics)
                period_results.append({
                    "strategy": strategy,
                    "timeframe": result.get("timeframe", DEFAULT_TIMEFRAME),
                    "metrics": metrics,
                    "vecscore": score,
                })
                badge = {"S": "🏆", "A": "⭐", "B": "✅", "C": "⚠️", "D": "❌"}[score["grade"]]
                roi_str = f"{metrics.get('roi', 0):+.2%}" if metrics.get('roi') else "N/A"
                print(f"     VecScore: {score['vecscore']} [{score['grade']}] {badge}  "
                      f"ROI={roi_str}  Trades={metrics.get('trades', 0)}")
            else:
                status_icon = {"timeout": "⏱️", "error": "❌"}.get(result["status"], "❌")
                print(f"     {status_icon} {result['status']}: {str(result.get('output', result.get('message', 'unknown')))[:60]}")
                period_results.append({
                    "strategy": strategy,
                    "status": result["status"],
                    "error": result.get("output", result.get("message", "unknown")),
                })

        batch_results["periods"][period_name] = period_results

    batch_results["completed"] = datetime.now().isoformat()
    return batch_results


def generate_markdown_report(all_results: dict) -> str:
    """生成Markdown评分报告"""
    lines = [
        "# NFI 系列现货多周期回测评分报告",
        "",
        f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 数据源: Binance 现货",
        f"> 策略总数: {len(ALL_STRATEGIES)}",
        "",
        "---",
        "",
        "## 一、评分汇总表",
        "",
        "| 策略名 | VecScore(3m) | VecScore(6m) | VecScore(12m) | 平均分 | 等级 |",
        "|--------|--------------|--------------|---------------|--------|------|",
    ]

    # 收集每个策略的分数
    strategy_scores = {}
    for batch_num, batch_data in all_results.items():
        for period_name, period_results in batch_data.get("periods", {}).items():
            for r in period_results:
                strategy = r.get("strategy")
                if strategy and r.get("vecscore"):
                    if strategy not in strategy_scores:
                        strategy_scores[strategy] = {}
                    strategy_scores[strategy][period_name] = r["vecscore"]["vecscore"]

    # 计算平均分并排序
    sorted_strategies = []
    for strategy, scores in strategy_scores.items():
        avg = sum(scores.values()) / len(scores) if scores else 0
        sorted_strategies.append((strategy, scores, avg))
    sorted_strategies.sort(key=lambda x: x[2], reverse=True)

    for strategy, scores, avg in sorted_strategies:
        grade = "S" if avg >= 80 else "A" if avg >= 70 else "B" if avg >= 60 else "C" if avg >= 50 else "D"
        badge = {"S": "🏆", "A": "⭐", "B": "✅", "C": "⚠️", "D": "❌"}[grade]
        lines.append(f"| {strategy} | {scores.get('3m', '-') or '-'} | {scores.get('6m', '-') or '-'} | {scores.get('12m', '-') or '-'} | {avg:.1f} | {grade} {badge} |")

    # 等级分布统计
    lines.extend([
        "",
        "---",
        "",
        "## 二、等级分布",
        "",
    ])

    grade_counts = {"S": 0, "A": 0, "B": 0, "C": 0, "D": 0}
    for _, _, avg in sorted_strategies:
        grade = "S" if avg >= 80 else "A" if avg >= 70 else "B" if avg >= 60 else "C" if avg >= 50 else "D"
        grade_counts[grade] += 1

    lines.append("| 等级 | 数量 | 占比 |")
    lines.append("|------|------|------|")
    total = sum(grade_counts.values())
    for grade, count in grade_counts.items():
        pct = f"{count/total*100:.1f}%" if total > 0 else "0%"
        badge = {"S": "🏆", "A": "⭐", "B": "✅", "C": "⚠️", "D": "❌"}[grade]
        lines.append(f"| {grade} {badge} | {count} | {pct} |")

    # TOP 10推荐
    lines.extend([
        "",
        "---",
        "",
        "## 三、TOP 10 推荐策略",
        "",
        "| 排名 | 策略 | 平均VecScore | 推荐理由 |",
        "|------|------|---------------|----------|",
    ])

    for i, (strategy, scores, avg) in enumerate(sorted_strategies[:10], 1):
        reason = "VecScore最高" if i == 1 else "稳定表现" if avg >= 55 else "需进一步验证"
        medal = {"1": "🥇", "2": "🥈", "3": "🥉"}.get(str(i), "")
        lines.append(f"| {medal}{i} | {strategy} | {avg:.1f} | {reason} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="NFI 系列现货多周期回测")
    parser.add_argument("--batch", type=str, default="1",
                        help="批次号 (1-5) 或 'all' 执行全部")
    parser.add_argument("--strategies", type=str, default=None,
                        help="指定策略列表 (逗号分隔)")
    parser.add_argument("--periods", type=str, default="3m,6m,12m",
                        help="时间周期 (逗号分隔)")
    parser.add_argument("--timeout", type=int, default=300,
                        help="单个策略超时时间(秒)")
    parser.add_argument("--output", type=str, default="user_data/nfi_spot_results.json",
                        help="结果输出文件")

    args = parser.parse_args()

    # 解析时间周期
    selected_periods = {}
    for p in args.periods.split(","):
        if p in PERIODS:
            selected_periods[p] = PERIODS[p]

    # 解析策略列表
    if args.strategies:
        strategies_to_test = [s.strip() for s in args.strategies.split(",")]
    elif args.batch == "all":
        strategies_to_test = ALL_STRATEGIES
    else:
        batch_num = int(args.batch)
        if batch_num not in BATCHES:
            print(f"错误: 无效批次号 {batch_num}，可选 1-5 或 'all'")
            return
        strategies_to_test = BATCHES[batch_num]

    print("=" * 70)
    print("NFI 系列现货多周期回测")
    print("=" * 70)
    print(f"策略数量: {len(strategies_to_test)}")
    print(f"时间周期: {list(selected_periods.keys())}")
    print(f"超时时间: {args.timeout}秒")
    print("=" * 70)

    # 执行回测
    all_results = {}

    if args.batch == "all":
        # 分批执行全部策略
        for batch_num in range(1, 6):
            batch_strategies = BATCHES[batch_num]
            batch_results = run_batch(batch_num, batch_strategies, selected_periods)
            all_results[batch_num] = batch_results

            # 每批完成后保存中间结果
            intermediate_file = f"user_data/nfi_spot_batch{batch_num}_results.json"
            with open(intermediate_file, "w", encoding="utf-8") as f:
                json.dump(batch_results, f, ensure_ascii=False, indent=2)
            print(f"\n💾 Batch {batch_num} 结果已保存: {intermediate_file}")
    else:
        # 执行单个批次
        if args.strategies:
            batch_num = 0  # 自定义策略
        else:
            batch_num = int(args.batch)
        batch_results = run_batch(batch_num, strategies_to_test, selected_periods)
        all_results[batch_num] = batch_results

    # 保存完整结果
    final_results = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "strategies": strategies_to_test,
            "periods": selected_periods,
            "mode": "spot",
            "exchange": "binance",
            "timeout": args.timeout,
        },
        "batches": all_results,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    print(f"\n💾 完整结果已保存: {args.output}")

    # 生成Markdown报告
    report_content = generate_markdown_report(all_results)
    report_file = args.output.replace(".json", "_report.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"\n📄 Markdown报告已保存: {report_file}")

    # 打印汇总
    print("\n" + "=" * 70)
    print("📋 回测完成汇总")
    print("=" * 70)


if __name__ == "__main__":
    main()