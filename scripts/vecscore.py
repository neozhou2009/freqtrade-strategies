#!/usr/bin/env python3
"""
VecAlpha Phase 2: VecScore 五维综合评分

读取 Phase 1 的回测结果，计算每个策略的 VecScore（0-100分）。

VecScore = P(收益,30%) + R(风控,25%) + S(稳定,20%) + T(可靠,15%) + E(效率,10%)

工作模式:
  --mode fast    : 仅用 Phase 1 的 30 天结果估算评分（快速，适合初排序）
  --mode full    : 额外跑多时间段稳定性回测后再评分（精确，耗时较长）

用法:
    # 快速估算（基于 Phase 1 结果）
    python scripts/vecscore.py --mode fast

    # 完整评分（额外运行三时段稳定性测试）
    python scripts/vecscore.py --mode full

    # 指定输入/输出
    python scripts/vecscore.py \\
        --phase1 user_data/phase1_results.json \\
        --output user_data/vecscore_results.json \\
        --mode fast

    # 只评分指定策略
    python scripts/vecscore.py --strategies MACDStrategy_crossed BinHV45 --mode fast
"""

import os
import re
import json
import math
import time
import shutil
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ──────────────────────────────────────────────────────────────────────────────
# 评分权重配置
# ──────────────────────────────────────────────────────────────────────────────

WEIGHTS = {
    "P": 0.30,  # 收益能力
    "R": 0.25,  # 风控能力
    "S": 0.20,  # 稳定性
    "T": 0.15,  # 可靠性（过拟合检测）
    "E": 0.10,  # 交易效率
}

DOCKER_IMAGE = "neozhou2009/freqtrade-full:latest"
TIMEOUT_SEC  = 400

# ── 三时间段配置（稳定性测试）────────────────────────────────────────────────
# 用于 --mode full；代表：较强上涨 / 震荡 / 下跌 三种市场环境
STABILITY_PERIODS = {
    "bull":    "20241001-20241231",  # 2024 Q4: 牛市
    "sideways":"20240601-20240831",  # 2024 Q2-Q3: 震荡
    "bear":    "20240101-20240331",  # 2024 Q1: 整体下修
}

# ── Train/Test 分割（可靠性测试，基于全年数据）────────────────────────────────
TRAIN_PERIOD = "20250101-20250831"  # 70%
TEST_PERIOD  = "20250901-20251231"  # 30%


# ──────────────────────────────────────────────────────────────────────────────
# 维度一：收益能力 P（满分 30）
# ──────────────────────────────────────────────────────────────────────────────

def score_P(roi: Optional[float], profit_factor: Optional[float], avg_profit: Optional[float]) -> dict:
    """
    收益能力评分（满分 30）
    - ROI 子项（15分）
    - Profit Factor 子项（10分）
    - 平均单笔盈利（5分）
    """
    # ROI 得分
    if roi is None:
        roi_score = 0
    elif roi < 0:
        roi_score = 0
    elif roi < 0.05:
        roi_score = 3
    elif roi < 0.15:
        roi_score = 8
    elif roi < 0.30:
        roi_score = 12
    elif roi < 0.60:
        roi_score = 14
    else:
        roi_score = 15

    # Profit Factor 得分
    if profit_factor is None or profit_factor <= 1.0:
        pf_score = 0
    elif profit_factor < 1.2:
        pf_score = 3
    elif profit_factor < 1.5:
        pf_score = 6
    elif profit_factor < 2.0:
        pf_score = 8
    else:
        pf_score = 10

    # 平均单笔盈利得分
    if avg_profit is None or avg_profit <= 0:
        ap_score = 0
    elif avg_profit < 0.005:
        ap_score = 1
    elif avg_profit < 0.01:
        ap_score = 3
    else:
        ap_score = 5

    total = roi_score + pf_score + ap_score
    return {
        "score": round(total, 2),
        "max": 30,
        "breakdown": {"roi": roi_score, "profit_factor": pf_score, "avg_profit": ap_score},
        "inputs": {"roi": roi, "profit_factor": profit_factor, "avg_profit": avg_profit},
    }


# ──────────────────────────────────────────────────────────────────────────────
# 维度二：风控能力 R（满分 25）
# ──────────────────────────────────────────────────────────────────────────────

def score_R(max_drawdown: Optional[float], sharpe: Optional[float]) -> dict:
    """
    风控能力评分（满分 25）
    - 最大回撤（15分）
    - Sharpe Ratio（10分）

    红线：
    - MDD > 40% → 强制总评分上限 40
    - Sharpe < 0 → 强制总评分上限 50
    """
    hard_cap = None  # 触发红线时的总分上限

    # MDD 评分（注意 max_drawdown 是百分比还是小数？需要归一化）
    mdd = max_drawdown
    if mdd is not None and mdd > 1:
        mdd = mdd / 100.0  # 如果是百分比形式（如 25 表示 25%），转为小数

    if mdd is None:
        mdd_score = 7  # 未知，给中性分
    elif mdd > 0.50:
        mdd_score = 0
        hard_cap = 40
    elif mdd > 0.40:
        mdd_score = 3
        hard_cap = 40
    elif mdd > 0.30:
        mdd_score = 7
    elif mdd > 0.20:
        mdd_score = 10
    elif mdd > 0.10:
        mdd_score = 13
    else:
        mdd_score = 15

    # Sharpe 评分
    if sharpe is None:
        sharpe_score = 3  # 未知，给中性分
    elif sharpe < 0:
        sharpe_score = 0
        if hard_cap is None:
            hard_cap = 50
    elif sharpe < 0.5:
        sharpe_score = 2
    elif sharpe < 1.0:
        sharpe_score = 5
    elif sharpe < 1.5:
        sharpe_score = 7
    elif sharpe < 2.0:
        sharpe_score = 9
    else:
        sharpe_score = 10

    total = mdd_score + sharpe_score
    return {
        "score": round(total, 2),
        "max": 25,
        "breakdown": {"max_drawdown": mdd_score, "sharpe": sharpe_score},
        "inputs": {"max_drawdown": mdd, "sharpe": sharpe},
        "hard_cap": hard_cap,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 维度三：稳定性 S（满分 20）
# ──────────────────────────────────────────────────────────────────────────────

def score_S_simple(roi_30d: Optional[float]) -> dict:
    """
    快速模式下的稳定性估分（满分 20）。
    由于只有单一时间段数据，使用保守估分：
    - 盈利 → 给最高 12 分（满分 20 需要多时段验证）
    - 微盈/亏损 → 按比例给分
    此函数在 --mode fast 下使用。
    """
    if roi_30d is None:
        return {"score": 8, "max": 20, "note": "fast-mode: 单时段估算，满分上限 12", "estimated": True}

    if roi_30d > 0.10:
        s = 12
    elif roi_30d > 0.02:
        s = 9
    elif roi_30d > 0:
        s = 6
    else:
        s = 2

    return {
        "score": s,
        "max": 20,
        "note": f"fast-mode: 30天ROI={roi_30d:+.1%}，满分需多时段回测",
        "estimated": True,
    }


def score_S_full(period_rois: dict) -> dict:
    """
    完整模式下的稳定性评分（满分 20）。
    period_rois = {"bull": float, "sideways": float, "bear": float}
    - 多周期盈利数（每个盈利时段 +3.33，共 3 段满分 10）
    - 收益波动性（变异系数倒数，满分 10）
    """
    rois = [v for v in period_rois.values() if v is not None]

    if not rois:
        return {"score": 5, "max": 20, "note": "无有效周期数据", "estimated": True}

    profit_periods = sum(1 for r in rois if r > 0)
    period_score = (profit_periods / 3) * 10

    if len(rois) >= 2:
        mean_roi = sum(rois) / len(rois)
        if mean_roi != 0:
            cv = math.sqrt(sum((r - mean_roi) ** 2 for r in rois) / len(rois)) / abs(mean_roi)
            volatility_score = max(0, 10 * (1 - min(cv, 1)))
        else:
            volatility_score = 5
    else:
        volatility_score = 5

    total = round(period_score + volatility_score, 2)
    return {
        "score": total,
        "max": 20,
        "breakdown": {
            "profitable_periods": profit_periods,
            "period_score": round(period_score, 2),
            "volatility_score": round(volatility_score, 2),
        },
        "inputs": period_rois,
        "estimated": False,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 维度四：可靠性（过拟合检测）T（满分 15）
# ──────────────────────────────────────────────────────────────────────────────

def score_T_simple(has_hyperopt: bool) -> dict:
    """
    快速模式下的可靠性估分（满分 15）。
    - 无 Hyperopt 参数 → 参数稳定性强，给 8 分（中性）
    - 有 Hyperopt 参数 → 需要 train/test 才能验证，暂给 6 分
    """
    if has_hyperopt:
        return {
            "score": 6,
            "max": 15,
            "note": "fast-mode: 含Hyperopt参数，需Train/Test分析才能完整评估",
            "estimated": True,
        }
    return {
        "score": 8,
        "max": 15,
        "note": "fast-mode: 无Hyperopt参数，参数固定，过拟合风险较低",
        "estimated": True,
    }


def score_T_full(train_roi: Optional[float], test_roi: Optional[float]) -> dict:
    """
    完整模式下的过拟合检测（满分 15）。
    Train/Test 分离评分：
    - Test >= Train * 0.7 → 评分 10（无明显过拟合）
    - Test >= Train * 0.5 → 评分 6（轻度过拟合）
    - Test >= 0           → 评分 3（中度，但仍盈利）
    - Test < 0            → 评分 0（严重过拟合）

    参数稳定性（固定 5 分，fast-mode 下跳过扰动测试）
    """
    if train_roi is None or test_roi is None:
        return {"score": 7, "max": 15, "note": "无 Train/Test 数据，使用中性分", "estimated": True}

    if train_roi <= 0:
        overfitting_score = 0 if test_roi <= 0 else 3
    elif test_roi >= train_roi * 0.7:
        overfitting_score = 10
    elif test_roi >= train_roi * 0.5:
        overfitting_score = 6
    elif test_roi >= 0:
        overfitting_score = 3
    else:
        overfitting_score = 0

    param_score = 3  # full 模式固定 3 分（需参数扰动测试才能给满 5 分）
    total = overfitting_score + param_score

    return {
        "score": round(total, 2),
        "max": 15,
        "breakdown": {"overfitting": overfitting_score, "param_sensitivity": param_score},
        "inputs": {"train_roi": train_roi, "test_roi": test_roi},
        "estimated": False,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 维度五：交易效率 E（满分 10）
# ──────────────────────────────────────────────────────────────────────────────

def score_E(trades_30d: Optional[int], timeframe: str) -> dict:
    """
    交易效率评分（满分 10）。
    - 交易次数子项（5分）：30天数据需换算到全年参考
    - 持仓时长子项（3分）：根据 timeframe 推断
    - 资金利用率（2分）：使用中性估算
    """
    # 30天交易次数换算全年估算
    annual_trades = (trades_30d or 0) * 12

    if annual_trades < 30:
        trades_score = 0
    elif annual_trades < 100:
        trades_score = 2
    elif annual_trades < 300:
        trades_score = 4
    else:
        trades_score = 5

    # 持仓时长估分（基于 timeframe 推断）
    tf_holding_score = {
        "1m":  1,  # 极短，手续费风险高
        "3m":  2,
        "5m":  3,  # 主流，最优评分
        "15m": 3,
        "30m": 3,
        "1h":  2,
        "4h":  1,
        "1d":  1,
    }.get(timeframe, 2)

    # 资金利用率：无精确数据时给中性分
    capital_score = 1

    total = trades_score + tf_holding_score + capital_score
    return {
        "score": round(total, 2),
        "max": 10,
        "breakdown": {
            "trades": trades_score,
            "holding_time": tf_holding_score,
            "capital_util": capital_score,
        },
        "inputs": {
            "trades_30d": trades_30d,
            "annual_trades_est": annual_trades,
            "timeframe": timeframe,
        },
    }


# ──────────────────────────────────────────────────────────────────────────────
# 综合评分计算
# ──────────────────────────────────────────────────────────────────────────────

GRADE_TABLE = [
    (85, "S", "🏆", "旗舰策略：首页重点推荐"),
    (75, "A", "⭐", "商用推荐：上架推荐池"),
    (65, "B", "✅", "可用：上架但不主推"),
    (55, "C", "⚠️",  "风险：仅供查阅"),
    (0,  "D", "❌", "不合格：禁止上架"),
]


def compute_vecscore(p_dim, r_dim, s_dim, t_dim, e_dim) -> dict:
    """整合五维得分，计算最终 VecScore"""
    raw = (
        p_dim["score"] * WEIGHTS["P"] / (p_dim["max"] * WEIGHTS["P"]) * 30 +
        r_dim["score"] * WEIGHTS["R"] / (r_dim["max"] * WEIGHTS["R"]) * 25 +
        s_dim["score"] * WEIGHTS["S"] / (s_dim["max"] * WEIGHTS["S"]) * 20 +
        t_dim["score"] * WEIGHTS["T"] / (t_dim["max"] * WEIGHTS["T"]) * 15 +
        e_dim["score"] * WEIGHTS["E"] / (e_dim["max"] * WEIGHTS["E"]) * 10
    )
    # 等价公式：直接用各维度实际得分求和
    raw = p_dim["score"] + r_dim["score"] + s_dim["score"] + t_dim["score"] + e_dim["score"]
    total = round(raw, 1)

    # 应用风控红线硬上限
    hard_cap = r_dim.get("hard_cap")
    if hard_cap is not None:
        total = min(total, hard_cap)
        cap_applied = True
    else:
        cap_applied = False

    # 确定等级
    grade, badge, meaning = "D", "❌", "不合格"
    for threshold, g, b, m in GRADE_TABLE:
        if total >= threshold:
            grade, badge, meaning = g, b, m
            break

    # 商用资格检查
    commercial_eligible = (
        total >= 75
        and (r_dim["inputs"].get("max_drawdown") or 1) < 0.30
        and (r_dim["inputs"].get("sharpe") or 0) >= 0.8
        and (e_dim["inputs"].get("trades_30d") or 0) >= 8  # 30天至少 8 次 ≈ 全年 ~100次
        and not cap_applied
    )

    is_estimated = any(
        dim.get("estimated", False) for dim in [p_dim, r_dim, s_dim, t_dim, e_dim]
    )

    return {
        "vecscore": total,
        "grade": grade,
        "badge": badge,
        "meaning": meaning,
        "commercial_eligible": commercial_eligible,
        "hard_cap_applied": cap_applied,
        "is_estimated": is_estimated,
    }


# ──────────────────────────────────────────────────────────────────────────────
# 辅助：运行额外回测（稳定性 / Train-Test）
# ──────────────────────────────────────────────────────────────────────────────

def run_backtest_for_period(
    strategy: str, timeframe: str, timerange: str,
    user_data_dir: str, use_docker: bool
) -> Optional[dict]:
    """运行单个时间段的回测，返回解析后的 metrics（失败返回 None）"""
    if use_docker:
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{user_data_dir}:/freqtrade/user_data",
            DOCKER_IMAGE, "backtesting",
            "--userdir", "/freqtrade/user_data",
            "--strategy", strategy,
            "--timerange", timerange,
            "--timeframe", timeframe,
            "--config", "/freqtrade/user_data/config.json",
            "--max-open-trades", "3",
            "--stake-amount", "100",
            "--dry-run-wallet", "10000",
            "--export", "none",
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
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True,
            timeout=TIMEOUT_SEC, env=os.environ.copy()
        )
        if proc.returncode != 0:
            return None
        # 复用 phase1 的解析逻辑
        from phase1_quick_backtest import parse_backtest_output
        return parse_backtest_output(proc.stdout + proc.stderr)
    except Exception:
        return None


# ──────────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────────

def score_strategy(
    name: str,
    phase1_metrics: dict,
    timeframe: str,
    has_hyperopt: bool,
    mode: str,
    user_data_dir: str,
    use_docker: bool,
) -> dict:
    """对单个策略计算 VecScore"""

    roi            = phase1_metrics.get("roi")
    profit_factor  = phase1_metrics.get("profit_factor")
    avg_profit     = phase1_metrics.get("avg_profit")
    sharpe         = phase1_metrics.get("sharpe")
    max_drawdown   = phase1_metrics.get("max_drawdown")
    trades         = phase1_metrics.get("trades")

    # ── P 维度 ──
    p_dim = score_P(roi, profit_factor, avg_profit)

    # ── R 维度 ──
    r_dim = score_R(max_drawdown, sharpe)

    # ── S 维度 ──
    if mode == "full":
        period_rois = {}
        for period_name, timerange in STABILITY_PERIODS.items():
            print(f"    [S] 运行稳定性测试: {period_name} ({timerange})")
            m = run_backtest_for_period(name, timeframe, timerange, user_data_dir, use_docker)
            period_rois[period_name] = m.get("roi") if m else None
        s_dim = score_S_full(period_rois)
    else:
        s_dim = score_S_simple(roi)

    # ── T 维度 ──
    if mode == "full":
        print(f"    [T] 运行 Train/Test 分析")
        train_m = run_backtest_for_period(name, timeframe, TRAIN_PERIOD, user_data_dir, use_docker)
        test_m  = run_backtest_for_period(name, timeframe, TEST_PERIOD, user_data_dir, use_docker)
        train_roi = train_m.get("roi") if train_m else None
        test_roi  = test_m.get("roi")  if test_m  else None
        t_dim = score_T_full(train_roi, test_roi)
    else:
        t_dim = score_T_simple(has_hyperopt)

    # ── E 维度 ──
    e_dim = score_E(trades, timeframe)

    # ── 综合 ──
    vecscore_result = compute_vecscore(p_dim, r_dim, s_dim, t_dim, e_dim)

    return {
        "name": name,
        "timeframe": timeframe,
        "mode": mode,
        "dimensions": {
            "P_return":    p_dim,
            "R_risk":      r_dim,
            "S_stability": s_dim,
            "T_reliability": t_dim,
            "E_efficiency":  e_dim,
        },
        **vecscore_result,
    }


def main():
    parser = argparse.ArgumentParser(
        description="VecAlpha Phase 2: VecScore 五维综合评分",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--phase1",
        default="user_data/phase1_results.json",
        help="Phase 1 结果文件路径",
    )
    parser.add_argument(
        "--output",
        default="user_data/vecscore_results.json",
        help="VecScore 输出文件路径",
    )
    parser.add_argument(
        "--registry",
        default="strategy_registry.json",
        help="strategy_registry.json 路径",
    )
    parser.add_argument(
        "--mode",
        choices=["fast", "full"],
        default="fast",
        help="fast: 基于 Phase1 数据估算；full: 额外运行稳定性+Train/Test回测",
    )
    parser.add_argument(
        "--strategies",
        nargs="+",
        help="只评分指定策略（需要同时存在于 phase1 结果中）",
    )
    parser.add_argument(
        "--no-docker",
        action="store_true",
        help="不使用 Docker（仅 --mode full 有效）",
    )
    parser.add_argument(
        "--min-grade",
        choices=["S", "A", "B", "C", "D"],
        default="D",
        help="输出结果中只保留该等级及以上的策略",
    )

    args = parser.parse_args()

    script_dir   = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    def resolve(p):
        return p if os.path.isabs(p) else os.path.join(project_root, p)

    phase1_path  = resolve(args.phase1)
    output_path  = resolve(args.output)
    registry_path = resolve(args.registry)
    user_data_dir = os.path.join(project_root, "user_data")
    use_docker   = not args.no_docker and not shutil.which("freqtrade")

    # ── 加载 registry ──────────────────────────────────────────
    registry = {}
    if os.path.exists(registry_path):
        with open(registry_path) as f:
            registry = json.load(f)

    # ── 加载 Phase 1 结果 ──────────────────────────────────────
    if not os.path.exists(phase1_path):
        print(f"❌ 找不到 Phase 1 结果: {phase1_path}")
        print("   请先运行: python scripts/phase1_quick_backtest.py")
        return

    with open(phase1_path) as f:
        phase1_data = json.load(f)

    # 构建 name → metrics 映射
    phase1_map = {r["name"]: r for r in phase1_data.get("results", [])}
    pass_names = phase1_data.get("pass_list", [])

    if args.strategies:
        target_names = [n for n in args.strategies if n in phase1_map]
        missing = [n for n in args.strategies if n not in phase1_map]
        if missing:
            print(f"⚠️  以下策略不在 Phase 1 结果中（跳过）: {missing}")
    else:
        target_names = pass_names

    if not target_names:
        print("❌ 没有可评分的策略（Phase 1 PASS 列表为空）")
        return

    print(f"📊 VecScore 评分模式: {'🔬 完整模式' if args.mode == 'full' else '⚡ 快速模式'}")
    print(f"📋 目标策略: {len(target_names)} 个")
    if use_docker:
        print("🐳 使用 Docker 运行额外回测\n")
    print("═" * 70)

    all_scored = []
    t_start = time.time()

    for i, name in enumerate(target_names, 1):
        r = phase1_map.get(name, {})
        metrics = r.get("metrics", {})
        timeframe = r.get("timeframe", registry.get(name, {}).get("timeframe", "5m"))
        has_hyperopt = "hyperopt" in registry.get(name, {}).get("features", [])

        print(f"[{i:3d}/{len(target_names)}] 评分: {name}")

        scored = score_strategy(
            name=name,
            phase1_metrics=metrics,
            timeframe=timeframe,
            has_hyperopt=has_hyperopt,
            mode=args.mode,
            user_data_dir=user_data_dir,
            use_docker=use_docker,
        )
        all_scored.append(scored)

        vs = scored["vecscore"]
        badge = scored["badge"]
        grade = scored["grade"]
        est_mark = "*" if scored["is_estimated"] else ""
        print(
            f"          → VecScore: {vs:.1f}{est_mark}  [{grade}] {badge}  "
            f"P={scored['dimensions']['P_return']['score']:.0f} "
            f"R={scored['dimensions']['R_risk']['score']:.0f} "
            f"S={scored['dimensions']['S_stability']['score']:.0f} "
            f"T={scored['dimensions']['T_reliability']['score']:.0f} "
            f"E={scored['dimensions']['E_efficiency']['score']:.0f}"
        )

    total_time = time.time() - t_start

    # ── 过滤等级 ──────────────────────────────────────────────
    grade_order = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 1}
    min_grade_val = grade_order[args.min_grade]
    filtered = [s for s in all_scored if grade_order.get(s["grade"], 0) >= min_grade_val]

    # ── 排序：VecScore 降序 ──────────────────────────────────
    ranked = sorted(filtered, key=lambda x: x["vecscore"], reverse=True)

    # ── 打印汇总 ─────────────────────────────────────────────
    print()
    print("═" * 70)
    print("🏆 VecScore 排名")
    print("═" * 70)
    for i, s in enumerate(ranked, 1):
        est_mark = "~" if s["is_estimated"] else " "
        commercial = " 💼" if s.get("commercial_eligible") else ""
        print(
            f"  {i:2d}. {s['badge']} [{s['grade']}] {s['vecscore']:.1f}{est_mark}  "
            f"{s['name']}{commercial}"
        )

    grade_counts = {}
    for s in all_scored:
        grade_counts[s["grade"]] = grade_counts.get(s["grade"], 0) + 1

    print()
    print("📊 等级分布:")
    for g, b, _ in [("S","🏆",""), ("A","⭐",""), ("B","✅",""), ("C","⚠️",""), ("D","❌","")]:
        cnt = grade_counts.get(g, 0)
        if cnt > 0:
            print(f"    {b} {g}级: {cnt} 个")

    commercial_list = [s for s in all_scored if s.get("commercial_eligible")]
    print(f"\n💼 符合商用资格: {len(commercial_list)} 个策略")
    if commercial_list:
        for s in sorted(commercial_list, key=lambda x: -x["vecscore"]):
            print(f"    ✅ {s['name']}  VecScore={s['vecscore']:.1f}")

    print(f"\n⏱️  总耗时: {total_time:.1f}s")
    if args.mode == "fast":
        print("   注意: 快速模式下 S/T 维度为估算值（标*），建议重要策略用 --mode full 精确验证")

    # ── 保存结果 ──────────────────────────────────────────────
    output_data = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "mode": args.mode,
            "total_scored": len(all_scored),
            "grade_distribution": grade_counts,
            "commercial_eligible_count": len(commercial_list),
        },
        "ranked": [
            {
                "rank": i + 1,
                "name": s["name"],
                "vecscore": s["vecscore"],
                "grade": s["grade"],
                "badge": s["badge"],
                "commercial_eligible": s.get("commercial_eligible", False),
                "is_estimated": s.get("is_estimated", True),
                "timeframe": s.get("timeframe"),
                "P": s["dimensions"]["P_return"]["score"],
                "R": s["dimensions"]["R_risk"]["score"],
                "S": s["dimensions"]["S_stability"]["score"],
                "T": s["dimensions"]["T_reliability"]["score"],
                "E": s["dimensions"]["E_efficiency"]["score"],
                "details": s["dimensions"],
            }
            for i, s in enumerate(ranked)
        ],
        "all_results": all_scored,
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"\n💾 VecScore 结果已保存到: {output_path}")
    print(f"📋 下一步：将 ranked 列表集成到前端 leaderboard.json")


if __name__ == "__main__":
    main()
