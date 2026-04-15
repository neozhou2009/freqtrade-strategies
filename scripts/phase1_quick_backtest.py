#!/usr/bin/env python3
"""
VecAlpha Phase 1: 快速回测初筛

读取 Phase 0 输出的 static_filter_result.json，对通过策略逐一运行
30天快速回测，提取关键指标，输出 phase1_results.json。

初筛通过标准（任一条件不满足则标记 FAIL）：
  ✅ 回测运行成功（无报错）
  ✅ ROI > -10%（容忍近期行情不利，排除结构性亏损）
  ✅ 交易次数 >= MIN_TRADES（至少有交易活动，排除永不入场）
  ✅ 运行时间 < TIMEOUT_SEC（排除因数据问题卡死的策略）

用法:
    # 从项目根目录运行（使用 Docker，推荐）
    python scripts/phase1_quick_backtest.py

    # 指定输入/输出文件
    python scripts/phase1_quick_backtest.py \\
        --filter-result user_data/static_filter_result.json \\
        --output user_data/phase1_results.json

    # 只运行指定策略列表（调试用）
    python scripts/phase1_quick_backtest.py --strategies MACDStrategy_crossed BinHV45

    # 不使用 Docker（需要本地 freqtrade 安装）
    python scripts/phase1_quick_backtest.py --no-docker

    # 并行运行（N 个工作进程）
    python scripts/phase1_quick_backtest.py --workers 4

    # 预演模式（不实际运行回测，只显示将要测试的策略）
    python scripts/phase1_quick_backtest.py --dry-run
"""

import os
import re
import json
import glob
import shutil
import argparse
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# ──────────────────────────────────────────────────────────────────────────────
# 配置
# ──────────────────────────────────────────────────────────────────────────────

# 回测时间范围：最近 30 天
BACKTEST_DAYS = 30

# 最小交易次数（少于此值标记为"从不入场"）
MIN_TRADES = 3

# 单个策略回测超时（秒）
TIMEOUT_SEC = 300  # 5 分钟

# ROI 最低门槛（低于此值为"结构性亏损"）
MIN_ROI = -0.10  # -10%

# 标准测试交易对（流动性最好，数据最完整）
TEST_PAIRS = ["BTC/USDT:USDT", "ETH/USDT:USDT"]

# Docker 镜像
DOCKER_IMAGE = "neozhou2009/freqtrade-full:latest"


# ──────────────────────────────────────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────────────────────────────────────

def get_timerange() -> str:
    """生成最近 BACKTEST_DAYS 天的时间范围字符串"""
    end = datetime.now()
    start = end - timedelta(days=BACKTEST_DAYS)
    return f"{start.strftime('%Y%m%d')}-{end.strftime('%Y%m%d')}"


def get_strategy_timeframe(strategy_name: str, registry: dict, strategies_dir: str) -> str:
    """从 registry 或代码文件中检测策略的 timeframe"""
    if strategy_name in registry:
        tf = registry[strategy_name].get("timeframe", "")
        if tf and tf != "unknown":
            return tf
    # 在策略文件里查找
    pattern = os.path.join(strategies_dir, strategy_name, f"{strategy_name}.py")
    if os.path.exists(pattern):
        content = Path(pattern).read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"timeframe\s*=\s*['\"](\w+)['\"]", content)
        if m:
            return m.group(1)
    return "5m"


def parse_backtest_output(stdout: str) -> dict:
    """
    从 freqtrade backtesting 的 stdout 中提取关键指标。
    freqtrade 在结束时会打印 JSON 摘要块（从 ={===} 包围的行之间）。
    也支持解析纯文本输出中的指标。
    """
    metrics = {
        "roi": None,
        "trades": None,
        "win_rate": None,
        "profit_factor": None,
        "sharpe": None,
        "max_drawdown": None,
        "avg_profit": None,
    }

    # ── 方式1：尝试找 JSON 结果块 ────────────────────────────────
    # freqtrade 会输出一段 JSON：{"strategy": {...}, "strategy_comparison": [...]}
    json_match = re.search(
        r'\{["\s]*"strategy"["\s]*:', stdout, re.DOTALL
    )
    if json_match:
        try:
            # 向前找完整 {} 块
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
                metrics["win_rate"] = sd.get("wins", 0) / max(sd.get("total_trades", 1), 1)
                metrics["profit_factor"] = sd.get("profit_factor", None)
                metrics["sharpe"] = sd.get("sharpe", None)
                metrics["max_drawdown"] = sd.get("max_drawdown", sd.get("max_drawdown_abs", None))
                metrics["avg_profit"] = sd.get("profit_mean", None)
                return metrics
        except Exception:
            pass  # 解析失败，降级到文本解析

    # ── 方式2：正则提取文本输出中的关键行 ──────────────────────────
    # freqtrade 2026.x 新格式：│ Key                          │ Value │
    patterns = {
        # 新格式 (freqtrade 2026.x): │ Total profit %  │ 0.13%  │
        "roi":          r"Total profit\s*%?\s*[│|]\s*([-\d.]+)\s*%",
        "roi_alt":      r"Profit total\s*[│|]\s*([-\d.]+)\s*%",
        # 新格式: │ Total/Daily Avg Trades  │ 101 / 3.48  │
        "trades":       r"Total[/\s]?(?:Daily\s+Avg\s+)?Trades\s*[│|]\s*(\d+)",
        "trades_alt":   r"Backtesting results.*?(\d+)\s+trades",
        # 策略汇总行: │ StrategyName │ 101 │ 0.14 │ 13.456 │ 0.13 │ ... │
        "trades_strat": r"│\s+\w[\w\s]*\s*│\s*(\d+)\s*│\s*[-\d.]+\s*│\s*[-\d.]+\s*│\s*[-\d.]+\s*│",
        "win_rate":     r"Win%\s*[│|]\s*([\d.]+)\s*%",
        "profit_factor":r"Profit factor\s*[│|]\s*([\d.]+)",
        "sharpe":       r"Sharpe\s*[│|]\s*([-\d.]+)",
        "max_drawdown": r"(?:Max.{0,10}Drawdown|Absolute drawdown).*?[│|].*?\(([\d.]+)%\)",
        "max_drawdown_alt": r"Max.{0,10}Drawdown\s*[│|]\s*([\d.]+)\s*%",
    }

    for key, pattern in patterns.items():
        m = re.search(pattern, stdout, re.IGNORECASE)
        if m:
            clean_key = key.replace("_alt", "").replace("_strat", "")
            if metrics.get(clean_key) is None:
                try:
                    val = float(m.group(1))
                    if "%" in pattern and clean_key not in ("max_drawdown", "trades"):
                        val = val / 100
                    metrics[clean_key] = val
                except ValueError:
                    pass

    # trades 是整数
    if metrics["trades"] is not None:
        try:
            metrics["trades"] = int(metrics["trades"])
        except (ValueError, TypeError):
            pass

    return metrics


def run_single_backtest(
    strategy: str,
    timeframe: str,
    timerange: str,
    user_data_dir: str,
    use_docker: bool,
    strategies_dir: str,
) -> dict:
    """
    对单个策略执行 30 天快速回测。
    返回结果字典：
    {
        "name": str,
        "status": "PASS" | "FAIL" | "ERROR" | "TIMEOUT",
        "fail_reason": str | None,
        "duration_sec": float,
        "metrics": {...}
    }
    """
    result = {
        "name": strategy,
        "status": "PASS",
        "fail_reason": None,
        "duration_sec": 0.0,
        "metrics": {},
        "timeframe": timeframe,
    }

    # 构建命令
    if use_docker:
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{user_data_dir}:/freqtrade/user_data",
            DOCKER_IMAGE,
            "backtesting",
            "--userdir", "/freqtrade/user_data",
            "--strategy", strategy,
            "--timerange", timerange,
            "--timeframe", timeframe,
            "--config", "/freqtrade/user_data/config.json",
            "--max-open-trades", "3",
            "--stake-amount", "100",
            "--dry-run-wallet", "10000",
            "--export", "none",   # 不写结果文件，加速
        ]
    else:
        cmd = [
            "freqtrade", "backtesting",
            "--strategy", strategy,
            "--timerange", timerange,
            "--timeframe", timeframe,
            "--config", os.path.join(user_data_dir, "config.json"),
            "--max-open-trades", "3",
            "--stake-amount", "100",
            "--dry-run-wallet", "10000",
            "--export", "none",
        ]

    t_start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SEC,
            env=os.environ.copy(),
        )
        duration = time.time() - t_start
        result["duration_sec"] = round(duration, 1)

        if proc.returncode != 0:
            result["status"] = "ERROR"
            # 提取最后 500 字符的错误信息
            stderr_tail = (proc.stderr or "")[-500:]
            stdout_tail = (proc.stdout or "")[-300:]
            result["fail_reason"] = f"returncode={proc.returncode} | {stderr_tail or stdout_tail}"
            return result

        # 解析输出
        output = proc.stdout + proc.stderr
        metrics = parse_backtest_output(output)
        result["metrics"] = metrics

        # ── 初筛判断 ──
        roi = metrics.get("roi")
        trades = metrics.get("trades")

        if trades is None or trades == 0:
            result["status"] = "FAIL"
            result["fail_reason"] = f"交易次数为 0（策略从不入场，可能缺数据或参数不匹配）"
        elif trades < MIN_TRADES:
            result["status"] = "FAIL"
            result["fail_reason"] = f"交易次数 {trades} < {MIN_TRADES}（统计不显著）"
        elif roi is not None and roi < MIN_ROI:
            result["status"] = "FAIL"
            result["fail_reason"] = f"ROI {roi:.1%} < {MIN_ROI:.0%}（结构性亏损）"

    except subprocess.TimeoutExpired:
        result["status"] = "TIMEOUT"
        result["fail_reason"] = f"超过 {TIMEOUT_SEC}s 超时"
        result["duration_sec"] = TIMEOUT_SEC

    except Exception as e:
        result["status"] = "ERROR"
        result["fail_reason"] = str(e)
        result["duration_sec"] = time.time() - t_start

    return result


# ──────────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="VecAlpha Phase 1: 30天快速回测初筛",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--filter-result",
        default="user_data/static_filter_result.json",
        help="Phase 0 输出文件路径（默认: user_data/static_filter_result.json）",
    )
    parser.add_argument(
        "--output",
        default="user_data/phase1_results.json",
        help="Phase 1 输出文件路径（默认: user_data/phase1_results.json）",
    )
    parser.add_argument(
        "--registry",
        default="strategy_registry.json",
        help="strategy_registry.json 路径（默认: strategy_registry.json）",
    )
    parser.add_argument(
        "--strategies-dir",
        default="strategies",
        help="策略目录（默认: strategies）",
    )
    parser.add_argument(
        "--strategies",
        nargs="+",
        help="覆盖模式：只运行指定的策略名称列表（绕过 filter-result）",
    )
    parser.add_argument(
        "--no-docker",
        action="store_true",
        help="不使用 Docker，使用本地 freqtrade 命令",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="并行工作进程数（默认: 1，单线程顺序执行）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预演模式：只显示将要测试的策略，不实际运行回测",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="断点续跑：跳过已有结果的策略（读取已有 output 文件）",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="限制最多测试 N 个策略（0=不限制，调试用）",
    )

    args = parser.parse_args()

    # ── 路径解析 ──────────────────────────────────────────────
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    def resolve(p):
        return p if os.path.isabs(p) else os.path.join(project_root, p)

    filter_result_path = resolve(args.filter_result)
    output_path        = resolve(args.output)
    registry_path      = resolve(args.registry)
    strategies_dir     = resolve(args.strategies_dir)
    user_data_dir      = os.path.join(project_root, "user_data")

    use_docker = not args.no_docker and not shutil.which("freqtrade")
    if use_docker:
        print("🐳 使用 Docker 模式")
    else:
        print("💻 使用本地 freqtrade 模式")

    # ── 加载 registry ─────────────────────────────────────────
    registry = {}
    if os.path.exists(registry_path):
        with open(registry_path) as f:
            registry = json.load(f)

    # ── 确定目标策略列表 ──────────────────────────────────────
    if args.strategies:
        candidate_names = args.strategies
        print(f"📋 覆盖模式：指定 {len(candidate_names)} 个策略")
    else:
        if not os.path.exists(filter_result_path):
            print(f"❌ 找不到 Phase 0 输出文件: {filter_result_path}")
            print("   请先运行: python scripts/static_filter.py")
            return
        with open(filter_result_path) as f:
            filter_data = json.load(f)
        candidate_names = [s["name"] for s in filter_data["pass"]]
        print(f"📋 从 Phase 0 结果加载 {len(candidate_names)} 个候选策略")

    # ── 断点续跑：跳过已有结果 ────────────────────────────────
    existing_results = {}
    if args.resume and os.path.exists(output_path):
        with open(output_path) as f:
            existing_data = json.load(f)
        for r in existing_data.get("results", []):
            existing_results[r["name"]] = r
        skip_count = len(existing_results)
        candidate_names = [n for n in candidate_names if n not in existing_results]
        print(f"⏭️  断点续跑：跳过已完成的 {skip_count} 个，剩余 {len(candidate_names)} 个")

    # ── 限制数量 ──────────────────────────────────────────────
    if args.limit > 0:
        candidate_names = candidate_names[:args.limit]
        print(f"🔢 限制模式：只运行前 {args.limit} 个策略")

    if not candidate_names:
        print("✅ 没有需要运行的策略。")
        return

    # ── 生成 timerange ────────────────────────────────────────
    timerange = get_timerange()
    print(f"📅 回测时间范围: {timerange}（最近 {BACKTEST_DAYS} 天）")
    print(f"🔬 共 {len(candidate_names)} 个策略待测试\n")

    if args.dry_run:
        print("⚠️  预演模式（--dry-run），不实际运行回测：")
        for i, name in enumerate(candidate_names, 1):
            tf = get_strategy_timeframe(name, registry, strategies_dir)
            print(f"  {i:3d}. {name} (tf={tf})")
        print(f"\n合计: {len(candidate_names)} 个策略")
        return

    # ── 回测执行 ──────────────────────────────────────────────
    all_results = list(existing_results.values())  # 断点续跑的已有结果
    lock = Lock()
    done_count = [0]
    total = len(candidate_names)

    def run_and_collect(strategy_name: str) -> dict:
        tf = get_strategy_timeframe(strategy_name, registry, strategies_dir)
        result = run_single_backtest(
            strategy=strategy_name,
            timeframe=tf,
            timerange=timerange,
            user_data_dir=user_data_dir,
            use_docker=use_docker,
            strategies_dir=strategies_dir,
        )
        with lock:
            done_count[0] += 1
            n = done_count[0]
            status_icon = {"PASS": "✅", "FAIL": "⚠️ ", "ERROR": "❌", "TIMEOUT": "⏱️ "}.get(
                result["status"], "?"
            )
            roi_str = ""
            roi = result["metrics"].get("roi")
            if roi is not None:
                roi_str = f"  ROI={roi:+.1%}"
            trades = result["metrics"].get("trades")
            trades_str = f"  trades={trades}" if trades is not None else ""
            print(
                f"  [{n:3d}/{total}] {status_icon} {strategy_name:<45}"
                f"  {result['duration_sec']:.0f}s{roi_str}{trades_str}"
            )
            if result["status"] not in ("PASS",) and result.get("fail_reason"):
                print(f"          └─ {result['fail_reason'][:120]}")
        return result

    print("═" * 70)
    print("开始回测...")
    print("═" * 70)

    t_total_start = time.time()

    if args.workers > 1:
        print(f"🔀 并行模式: {args.workers} 个工作进程")
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {ex.submit(run_and_collect, n): n for n in candidate_names}
            for future in as_completed(futures):
                all_results.append(future.result())
    else:
        for name in candidate_names:
            all_results.append(run_and_collect(name))

    total_time = time.time() - t_total_start

    # ── 统计 ──────────────────────────────────────────────────
    passed  = [r for r in all_results if r["status"] == "PASS"]
    failed  = [r for r in all_results if r["status"] == "FAIL"]
    errored = [r for r in all_results if r["status"] == "ERROR"]
    timeout = [r for r in all_results if r["status"] == "TIMEOUT"]

    # PASS 策略按 ROI 排序
    passed_sorted = sorted(
        passed,
        key=lambda r: r["metrics"].get("roi") or -999,
        reverse=True,
    )

    print()
    print("═" * 70)
    print("📊 Phase 1 快速回测结果摘要")
    print("═" * 70)
    print(f"  总测试策略  : {len(all_results)}")
    print(f"  ✅ PASS     : {len(passed)}")
    print(f"  ⚠️  FAIL     : {len(failed)}")
    print(f"  ❌ ERROR    : {len(errored)}")
    print(f"  ⏱️  TIMEOUT  : {len(timeout)}")
    print(f"  总耗时      : {total_time/60:.1f} 分钟")
    print()

    if passed_sorted:
        print("── PASS 策略（按 ROI 排序）──")
        for r in passed_sorted:
            roi = r["metrics"].get("roi")
            trades = r["metrics"].get("trades")
            sharpe = r["metrics"].get("sharpe")
            roi_str    = f"ROI={roi:+.1%}"    if roi    is not None else "ROI=?"
            trades_str = f"trades={trades}"   if trades is not None else ""
            sharpe_str = f"sharpe={sharpe:.2f}" if sharpe is not None else ""
            print(f"  ✅ {r['name']:<45} {roi_str:12}  {trades_str:12}  {sharpe_str}")

    # ── 保存结果 ──────────────────────────────────────────────
    output_data = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "timerange": timerange,
            "days": BACKTEST_DAYS,
            "total_tested": len(all_results),
            "pass_count": len(passed),
            "fail_count": len(failed),
            "error_count": len(errored),
            "timeout_count": len(timeout),
            "pass_rate": f"{len(passed)/len(all_results)*100:.1f}%" if all_results else "0%",
            "total_time_sec": round(total_time, 1),
        },
        "pass_list": [r["name"] for r in passed_sorted],
        "results": sorted(all_results, key=lambda r: r["name"]),
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print()
    print(f"💾 Phase 1 结果已保存到: {output_path}")
    print(f"📋 PASS 策略共 {len(passed)} 个，进入 Phase 2（完整 VecScore 评分）")


if __name__ == "__main__":
    main()
