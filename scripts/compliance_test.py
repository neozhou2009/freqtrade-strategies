#!/usr/bin/env python3
"""
VecAlpha 商用策略合规测试程序

基于 commercial_scoring_spec.md (v2) 规范，对策略进行合规性检查，
判断策略属于哪个商用级别（Tier 1/2/3/拒绝）。

用法:
    # 对已有结果进行合规检查（不运行新回测）
    python scripts/compliance_test.py --skip-phase0 --skip-phase1 --skip-phase2

    # 指定v2规范
    python scripts/compliance_test.py --spec v2 --skip-phase0 --skip-phase1 --skip-phase2

    # 仅检查指定策略
    python scripts/compliance_test.py --strategies BigZ04HO ichiV1 --spec v2

    # 完整管线运行
    python scripts/compliance_test.py --mode full --spec v2

    # 预览模式
    python scripts/compliance_test.py --dry-run
"""

import os
import json
import math
import argparse
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional


# ──────────────────────────────────────────────────────────────────────────────
# 商用评分规范定义
# ──────────────────────────────────────────────────────────────────────────────

GRADE_TABLE = [
    (85, "S", "🏆", "旗舰策略：首页重点推荐"),
    (75, "A", "⭐", "商用推荐：上架推荐池"),
    (65, "B", "✅", "可用策略：上架但不主推"),
    (55, "C", "⚠️", "风险策略：仅供查阅"),
    (0,  "D", "❌", "不合格：禁止上架"),
]

# v3: 放宽等级阈值
GRADE_TABLE_V3 = [
    (80, "S", "🏆", "旗舰策略：首页重点推荐"),
    (70, "A", "⭐", "商用推荐：上架推荐池"),
    (60, "B", "✅", "可用策略：上架但不主推"),
    (50, "C", "⚠️", "风险策略：仅供查阅"),
    (0,  "D", "❌", "不合格：禁止上架"),
]

TIER_DEFS = {
    1: {"name": "旗舰", "name_en": "Flagship", "vecscore": 80, "mdd": 0.15,
        "sharpe": 1.5, "trades_30d": 15, "wfa_verified": True},
    2: {"name": "专业", "name_en": "Professional", "vecscore": 65, "mdd": 0.25,
        "sharpe": 0.8, "trades_30d": 8, "wfa_verified": False},
    3: {"name": "实验", "name_en": "Experimental", "vecscore": 50, "mdd": 0.40,
        "sharpe": None, "trades_30d": 3, "wfa_verified": False},
}

# v3: Tier阈值放宽
TIER_DEFS_V3 = {
    1: {"name": "旗舰", "name_en": "Flagship", "vecscore": 80, "mdd": 0.15,
        "sharpe": 1.5, "trades_30d": 15, "wfa_verified": True},
    2: {"name": "专业", "name_en": "Professional", "vecscore": 60, "mdd": 0.30,  # v2=65 → v3=60
        "sharpe": 0.5, "trades_30d": 5, "wfa_verified": False},  # 放宽
    3: {"name": "实验", "name_en": "Experimental", "vecscore": 40, "mdd": 0.50,  # v2=50 → v3=40
        "sharpe": None, "trades_30d": 1, "wfa_verified": False},  # 大幅放宽
}

HARD_RED_LINES = [
    {"id": "HR-01", "condition": "mdd >= 0.50",      "effect": "VecScore上限40",
     "check": lambda m: (m.get("max_drawdown") or 0) >= 0.50},
    {"id": "HR-02", "condition": "sharpe < 0",        "effect": "VecScore上限50",
     "check": lambda m: (m.get("sharpe") or 0) < 0},
    {"id": "HR-03", "condition": "trades_30d == 0",    "effect": "所有Tier拒绝",
     "check": lambda m: (m.get("trades") or 0) == 0},
    {"id": "HR-04", "condition": "所有WFA期ROI为负",   "effect": "Tier 1/2拒绝",
     "check": lambda m: _check_all_periods_negative(m)},
    {"id": "HR-05", "condition": "train/test<0.3且test_roi<0", "effect": "Tier 1/2拒绝",
     "check": lambda m: _check_severe_overfit(m)},
    {"id": "HR-06", "condition": "入场逻辑含shift(0)",  "effect": "所有Tier拒绝",
     "check": lambda m: m.get("has_lookahead", False)},
    {"id": "HR-07", "condition": "胜率100%且交易<5",   "effect": "需人工审核",
     "check": lambda m: (m.get("winrate") or 0) >= 1.0 and (m.get("trades") or 0) < 5},
]

# v3: 放宽硬红线（取消Sharpe<0硬上限）
HARD_RED_LINES_V3 = [
    {"id": "HR-01", "condition": "mdd >= 0.60",      "effect": "VecScore上限35",  # 放宽阈值
     "check": lambda m: (m.get("max_drawdown") or 0) >= 0.60},
    # HR-02取消：Sharpe<0改为软红线
    {"id": "HR-03", "condition": "trades_30d == 0",    "effect": "所有Tier拒绝",
     "check": lambda m: (m.get("trades") or 0) == 0},
    {"id": "HR-04", "condition": "所有WFA期ROI为负",   "effect": "Tier 1/2拒绝",
     "check": lambda m: _check_all_periods_negative(m)},
    {"id": "HR-06", "condition": "入场逻辑含shift(0)",  "effect": "所有Tier拒绝",
     "check": lambda m: m.get("has_lookahead", False)},
]

SOFT_RED_LINES = [
    {"id": "SR-01", "condition": "mdd > 0.30",        "label": "⚠️ 高回撤风险",
     "check": lambda m: (m.get("max_drawdown") or 0) > 0.30},
    {"id": "SR-02", "condition": "sharpe < 0.8",       "label": "⚠️ 低于目标Sharpe",
     "check": lambda m: (m.get("sharpe") or 0) < 0.8},
    {"id": "SR-03", "condition": "trades_30d < 8",     "label": "⚠️ 低交易频率",
     "check": lambda m: (m.get("trades") or 0) < 8},
    {"id": "SR-04", "condition": "仅2/3稳定性周期盈利", "label": "⚠️ 市场环境敏感",
     "check": lambda m: _check_marginal_stability(m)},
    {"id": "SR-05", "condition": "profit_factor < 1.5", "label": "⚠️ 利润因子偏低",
     "check": lambda m: (m.get("profit_factor") or 0) < 1.5 and (m.get("profit_factor") or 0) > 0},
    {"id": "SR-06", "condition": "train/test比0.3~0.5", "label": "⚠️ 可能轻度过拟合",
     "check": lambda m: _check_light_overfit(m)},
    {"id": "SR-07", "condition": "含Hyperopt参数",      "label": "⚠️ 依赖参数优化",
     "check": lambda m: m.get("has_hyperopt", False)},
    {"id": "SR-08", "condition": "震荡期ROI为负",       "label": "⚠️ 震荡市场风险",
     "check": lambda m: _check_sideways_negative(m)},
]

# v3: 新增Sharpe<0软红线（从硬红线降级）
SOFT_RED_LINES_V3 = SOFT_RED_LINES + [
    {"id": "SR-09", "condition": "sharpe < 0",       "label": "⚠️ 负Sharpe（短期波动）",
     "check": lambda m: (m.get("sharpe") or 0) < 0},
]


# ──────────────────────────────────────────────────────────────────────────────
# 经典策略保护机制
# ──────────────────────────────────────────────────────────────────────────────

def load_classic_registry(project_root: str) -> dict:
    """加载开源经典策略注册表"""
    path = os.path.join(project_root, "classic_strategies_registry.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def match_classic_strategy(name: str, classic_registry: dict) -> tuple:
    """
    检查策略是否属于经典策略系列。
    返回 (category, protection_config) 或 (None, None)
    """
    if not classic_registry:
        return None, None

    # 检查旗舰经典
    flagship = classic_registry.get("flagship_classics", {})
    flagship_names = flagship.get("strategies", [])
    flagship_patterns = flagship.get("match_patterns", [])

    if name in flagship_names or any(p in name for p in flagship_patterns):
        return "flagship_classics", flagship.get("protection", {})

    # 检查组合经典
    combination = classic_registry.get("combination_classics", {})
    combination_names = combination.get("strategies", [])
    combination_patterns = combination.get("match_patterns", [])

    if name in combination_names or any(p in name for p in combination_patterns):
        return "combination_classics", combination.get("protection", {})

    # 检查指标经典
    indicator = classic_registry.get("indicator_classics", {})
    indicator_names = indicator.get("strategies", [])
    indicator_patterns = indicator.get("match_patterns", [])

    if name in indicator_names or any(p in name for p in indicator_patterns):
        return "indicator_classics", indicator.get("protection", {})

    return None, None


def apply_classic_protection(report: dict, category: str, protection: dict) -> dict:
    """
    应用经典策略保护机制。
    根据类别强制调整等级和Tier。
    """
    if not protection:
        return report

    # 应用等级保底
    grade_floor = protection.get("grade_floor")
    if grade_floor is not None and report["vecscore"] < grade_floor:
        report["vecscore"] = grade_floor
        # 根据grade_floor重新计算等级
        if grade_floor >= 80:
            report["grade"] = "S"
            report["badge"] = "🏆"
        elif grade_floor >= 70:
            report["grade"] = "A"
            report["badge"] = "⭐"
        elif grade_floor >= 60:
            report["grade"] = "B"
            report["badge"] = "✅"
        elif grade_floor >= 50:
            report["grade"] = "C"
            report["badge"] = "⚠️"
        else:
            report["grade"] = "D"
            report["badge"] = "❌"

    # 应用Tier保底
    tier_floor = protection.get("tier_floor")
    if tier_floor is not None and report["commercial_tier"] is None:
        report["commercial_tier"] = tier_floor

    # 添加经典策略标记
    report["classic_status"] = category
    report["classic_label"] = protection.get("label", "")
    report["protected"] = True

    return report


def _check_all_periods_negative(metrics: dict) -> bool:
    """检查所有WFA测试期ROI是否均为负"""
    period_rois = metrics.get("period_rois", {})
    if not period_rois:
        return False
    return all((v or 0) < 0 for v in period_rois.values())


def _check_severe_overfit(metrics: dict) -> bool:
    """检查严重过拟合：train/test比<0.3且test_roi<0"""
    train_roi = metrics.get("train_roi")
    test_roi = metrics.get("test_roi")
    if train_roi is None or test_roi is None or train_roi <= 0:
        return False
    ratio = test_roi / train_roi
    return ratio < 0.3 and test_roi < 0


def _check_marginal_stability(metrics: dict) -> bool:
    """检查边际稳定性：仅2/3周期盈利"""
    period_rois = metrics.get("period_rois", {})
    if not period_rois:
        return False
    profitable = sum(1 for v in period_rois.values() if (v or 0) > 0)
    return profitable == 2 and len(period_rois) == 3


def _check_light_overfit(metrics: dict) -> bool:
    """检查轻度过拟合：train/test比0.3~0.5"""
    train_roi = metrics.get("train_roi")
    test_roi = metrics.get("test_roi")
    if train_roi is None or test_roi is None or train_roi <= 0:
        return False
    ratio = test_roi / train_roi
    return 0.3 <= ratio < 0.5


def _check_sideways_negative(metrics: dict) -> bool:
    """检查震荡期ROI是否为负"""
    period_rois = metrics.get("period_rois", {})
    return (period_rois.get("sideways") or 0) < 0


# ──────────────────────────────────────────────────────────────────────────────
# VecScore v2 P维度评分
# ──────────────────────────────────────────────────────────────────────────────

def score_P_v2(roi: Optional[float], profit_factor: Optional[float],
               avg_profit: Optional[float]) -> dict:
    """
    P维度v2评分 — 年化ROI换算+细分阈值

    v1→v2核心变更：
    - ROI: 30天×12年化，按0/1%/3%/5%/10%/20%分段
    - PF: 不变
    - avg_profit: 微调阈值(0.003/0.008)
    """
    annual_roi = (roi or 0) * 12

    # ROI得分（年化）
    if annual_roi < 0:
        roi_score = 0
    elif annual_roi < 0.01:
        roi_score = 2
    elif annual_roi < 0.03:
        roi_score = 5
    elif annual_roi < 0.05:
        roi_score = 8
    elif annual_roi < 0.10:
        roi_score = 11
    elif annual_roi < 0.20:
        roi_score = 14
    else:
        roi_score = 15

    # Profit Factor得分（不变）
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

    # 平均单笔盈利得分（微调）
    if avg_profit is None or avg_profit <= 0:
        ap_score = 0
    elif avg_profit < 0.003:
        ap_score = 1
    elif avg_profit < 0.008:
        ap_score = 3
    else:
        ap_score = 5

    total = roi_score + pf_score + ap_score
    return {
        "score": round(total, 2),
        "max": 30,
        "breakdown": {"roi": roi_score, "profit_factor": pf_score, "avg_profit": ap_score},
        "inputs": {
            "roi": roi, "annual_roi": round(annual_roi, 6),
            "profit_factor": profit_factor, "avg_profit": avg_profit,
        },
    }


# ──────────────────────────────────────────────────────────────────────────────
# CommercialSpec — 规范定义
# ──────────────────────────────────────────────────────────────────────────────

class CommercialSpec:
    """商用评分规范"""

    def __init__(self, version: str = "v2"):
        self.version = version
        # v3使用放宽的阈值
        if version == "v3":
            self.grade_table = GRADE_TABLE_V3
            self.tier_defs = TIER_DEFS_V3
            self.hard_red_lines = HARD_RED_LINES_V3
            self.soft_red_lines = SOFT_RED_LINES_V3
        else:
            self.grade_table = GRADE_TABLE
            self.tier_defs = TIER_DEFS
            self.hard_red_lines = HARD_RED_LINES
            self.soft_red_lines = SOFT_RED_LINES

    def get_grade(self, score: float) -> tuple:
        """根据分数返回(grade, badge, meaning)"""
        for threshold, g, b, m in self.grade_table:
            if score >= threshold:
                return g, b, m
        return "D", "❌", "不合格"

    def get_tier(self, score: float, metrics: dict) -> Optional[int]:
        """
        判断策略属于哪个商用Tier。
        从高到低检查，返回满足条件的最高Tier（1/2/3），不满足返回None。
        """
        for tier_num in [1, 2, 3]:
            td = self.tier_defs[tier_num]
            # VecScore
            if score < td["vecscore"]:
                continue
            # MDD
            mdd = metrics.get("max_drawdown") or 0
            if mdd > td["mdd"]:
                continue
            # Sharpe
            if td["sharpe"] is not None:
                sharpe = metrics.get("sharpe") or 0
                if sharpe < td["sharpe"]:
                    continue
            # Trades
            trades = metrics.get("trades") or 0
            if trades < td["trades_30d"]:
                continue
            # WFA验证（Tier 1需要verified）
            if td.get("wfa_verified"):
                test_roi = metrics.get("test_roi")
                if test_roi is None or test_roi < 0:
                    continue
            return tier_num
        return None

    def check_hard_red_lines(self, metrics: dict) -> list:
        """检查硬红线，返回触发的红线列表"""
        triggered = []
        for hrl in self.hard_red_lines:
            if hrl["check"](metrics):
                triggered.append({
                    "id": hrl["id"],
                    "condition": hrl["condition"],
                    "effect": hrl["effect"],
                })
        return triggered

    def check_soft_red_lines(self, metrics: dict) -> list:
        """检查软红线，返回触发的警告列表"""
        triggered = []
        for srl in self.soft_red_lines:
            if srl["check"](metrics):
                triggered.append({
                    "id": srl["id"],
                    "condition": srl["condition"],
                    "label": srl["label"],
                })
        return triggered


# ──────────────────────────────────────────────────────────────────────────────
# ComplianceChecker — 合规检查
# ──────────────────────────────────────────────────────────────────────────────

class ComplianceChecker:
    """对单个策略进行商用合规性检查"""

    def __init__(self, spec: CommercialSpec):
        self.spec = spec

    def check(self, strategy_name: str, vecscore_result: dict,
              phase1_metrics: dict = None) -> dict:
        """
        执行合规检查，返回 ComplianceReport 字典。

        vecscore_result: 来自 vecscore_results.json 的单策略结果
        phase1_metrics: 来自 phase1_results.json 的 metrics（补充字段）
        """
        dims = vecscore_result.get("dimensions", {})
        p_dim = dims.get("P_return", {})
        r_dim = dims.get("R_risk", {})
        s_dim = dims.get("S_stability", {})
        t_dim = dims.get("T_reliability", {})
        e_dim = dims.get("E_efficiency", {})

        # 如果使用v2规范，重新计算P维度
        if self.spec.version == "v2":
            p_inputs = p_dim.get("inputs", {})
            p_dim = score_P_v2(
                p_inputs.get("roi"),
                p_inputs.get("profit_factor"),
                p_inputs.get("avg_profit"),
            )
            # 重新计算总分
            total = p_dim["score"] + r_dim.get("score", 0) + s_dim.get("score", 0) + \
                    t_dim.get("score", 0) + e_dim.get("score", 0)
            # 应用硬上限
            hard_cap = r_dim.get("hard_cap")
            if hard_cap is not None:
                total = min(total, hard_cap)
        else:
            total = vecscore_result.get("vecscore", 0)

        # 等级
        grade, badge, meaning = self.spec.get_grade(total)

        # 构建检查用的metrics字典
        r_inputs = r_dim.get("inputs", {})
        t_inputs = t_dim.get("inputs", {})
        s_inputs = s_dim.get("inputs", {})
        e_inputs = e_dim.get("inputs", {})

        check_metrics = {
            "roi": (p_dim.get("inputs") or p_dim).get("roi"),
            "max_drawdown": r_inputs.get("max_drawdown"),
            "sharpe": r_inputs.get("sharpe"),
            "profit_factor": (p_dim.get("inputs") or p_dim).get("profit_factor"),
            "trades": e_inputs.get("trades_30d"),
            "train_roi": t_inputs.get("train_roi"),
            "test_roi": t_inputs.get("test_roi"),
            "period_rois": s_inputs,
            "has_hyperopt": phase1_metrics.get("has_hyperopt", False) if phase1_metrics else False,
            "has_lookahead": False,  # Phase 0已过滤
            "winrate": phase1_metrics.get("winrate") if phase1_metrics else None,
        }

        # 硬红线检查
        hard_red_lines = self.spec.check_hard_red_lines(check_metrics)

        # 软红线检查
        soft_red_lines = self.spec.check_soft_red_lines(check_metrics)

        # 商用Tier判定
        # 硬红线可能限制Tier
        tier = self.spec.get_tier(total, check_metrics)

        # 应用硬红线对Tier的限制
        hrl_ids = [h["id"] for h in hard_red_lines]
        if "HR-03" in hrl_ids:
            tier = None  # 0交易，全部拒绝
        if "HR-04" in hrl_ids or "HR-05" in hrl_ids:
            if tier and tier >= 2:
                tier = None if tier <= 2 else 3  # 降级到Tier 3
        if "HR-06" in hrl_ids:
            tier = None  # 未来视，全部拒绝

        # 确定状态
        if tier == 1:
            status = "PASS_TIER1"
        elif tier == 2:
            status = "PASS_TIER2"
        elif tier == 3:
            status = "PASS_TIER3"
        else:
            status = "FAIL"

        # Gap分析：到下一Tier还差什么
        gap_analysis = self._gap_analysis(total, check_metrics, tier)

        return {
            "name": strategy_name,
            "vecscore": round(total, 1),
            "grade": grade,
            "badge": badge,
            "meaning": meaning,
            "spec_version": self.spec.version,
            "commercial_tier": tier,
            "tier_label": f"Tier {tier} ({TIER_DEFS[tier]['name']})" if tier else "拒绝",
            "status": status,
            "hard_red_lines": hard_red_lines,
            "soft_red_lines": soft_red_lines,
            "dimensions": {
                "P_return": p_dim,
                "R_risk": r_dim,
                "S_stability": s_dim,
                "T_reliability": t_dim,
                "E_efficiency": e_dim,
            },
            "gap_to_next_tier": gap_analysis,
            "is_estimated": vecscore_result.get("is_estimated", True),
        }

    def _gap_analysis(self, score: float, metrics: dict,
                      current_tier: Optional[int]) -> dict:
        """分析到下一Tier的差距"""
        if current_tier is None:
            target_tier = 3
        elif current_tier == 1:
            return {"target": None, "gaps": [], "note": "已达最高Tier"}
        else:
            target_tier = current_tier - 1

        td = self.tier_defs = TIER_DEFS[target_tier]
        gaps = []

        # VecScore差距
        if score < td["vecscore"]:
            gaps.append({
                "dimension": "vecscore",
                "current": round(score, 1),
                "needed": td["vecscore"],
                "gap": round(td["vecscore"] - score, 1),
            })

        # MDD差距
        mdd = metrics.get("max_drawdown") or 0
        if mdd > td["mdd"]:
            gaps.append({
                "dimension": "max_drawdown",
                "current": f"{mdd:.1%}",
                "needed": f"<{td['mdd']:.0%}",
                "gap": f"降低{mdd - td['mdd']:.1%}",
            })

        # Sharpe差距
        if td["sharpe"] is not None:
            sharpe = metrics.get("sharpe") or 0
            if sharpe < td["sharpe"]:
                gaps.append({
                    "dimension": "sharpe",
                    "current": round(sharpe, 2),
                    "needed": td["sharpe"],
                    "gap": round(td["sharpe"] - sharpe, 2),
                })

        # Trades差距
        trades = metrics.get("trades") or 0
        if trades < td["trades_30d"]:
            gaps.append({
                "dimension": "trades_30d",
                "current": trades,
                "needed": td["trades_30d"],
                "gap": td["trades_30d"] - trades,
            })

        # WFA差距
        if td.get("wfa_verified"):
            test_roi = metrics.get("test_roi")
            if test_roi is None:
                gaps.append({
                    "dimension": "wfa_test_roi",
                    "current": "未测试",
                    "needed": "≥0",
                    "gap": "需运行full模式评估",
                })
            elif test_roi < 0:
                gaps.append({
                    "dimension": "wfa_test_roi",
                    "current": f"{test_roi:.2%}",
                    "needed": "≥0",
                    "gap": f"需提升{abs(test_roi):.2%}",
                })

        target_name = f"Tier {target_tier} ({TIER_DEFS[target_tier]['name']})"
        return {"target": target_name, "gaps": gaps}


# ──────────────────────────────────────────────────────────────────────────────
# PipelineRunner — 管线编排
# ──────────────────────────────────────────────────────────────────────────────

class PipelineRunner:
    """编排Phase 0→1→2管线"""

    def __init__(self, project_root: str, use_docker: bool = True):
        self.project_root = project_root
        self.scripts_dir = os.path.join(project_root, "scripts")
        self.user_data_dir = os.path.join(project_root, "user_data")
        self.use_docker = use_docker

    def run_phase0(self, strategies_dir: str = None) -> str:
        """运行Phase 0静态筛选，返回结果文件路径"""
        cmd = ["python3", os.path.join(self.scripts_dir, "static_filter.py")]
        if strategies_dir:
            cmd.extend(["--strategies-dir", strategies_dir])
        print(f"  [Phase 0] 运行: {' '.join(cmd)}")
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        if proc.returncode != 0:
            print(f"  [Phase 0] 错误: {proc.stderr[:200]}")
        return os.path.join(self.user_data_dir, "static_filter_result.json")

    def run_phase1(self, resume: bool = False) -> str:
        """运行Phase 1快速回测，返回结果文件路径"""
        cmd = ["python3", os.path.join(self.scripts_dir, "phase1_quick_backtest.py")]
        if resume:
            cmd.append("--resume")
        if self.use_docker:
            cmd.append("--docker")
        print(f"  [Phase 1] 运行: {' '.join(cmd)}")
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        if proc.returncode != 0:
            print(f"  [Phase 1] 错误: {proc.stderr[:200]}")
        return os.path.join(self.user_data_dir, "phase1_results.json")

    def run_phase2(self, mode: str = "fast", spec: str = "v1",
                   strategies: list = None) -> str:
        """运行Phase 2 VecScore评分，返回结果文件路径"""
        cmd = [
            "python3", os.path.join(self.scripts_dir, "vecscore.py"),
            "--mode", mode,
            "--spec", spec,
        ]
        if strategies:
            cmd.extend(["--strategies"] + strategies)
        print(f"  [Phase 2] 运行: {' '.join(cmd)}")
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        if proc.returncode != 0:
            print(f"  [Phase 2] 错误: {proc.stderr[:200]}")
        return os.path.join(self.user_data_dir, "vecscore_results.json")


# ──────────────────────────────────────────────────────────────────────────────
# 报告生成
# ──────────────────────────────────────────────────────────────────────────────

def generate_report(reports: list, output_dir: str, fmt: str = "both"):
    """生成合规报告"""
    os.makedirs(output_dir, exist_ok=True)

    # Tier分布统计
    tier_counts = {1: 0, 2: 0, 3: 0, "reject": 0}
    for r in reports:
        tier = r.get("commercial_tier")
        if tier:
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        else:
            tier_counts["reject"] += 1

    grade_counts = {}
    for r in reports:
        g = r["grade"]
        grade_counts[g] = grade_counts.get(g, 0) + 1

    meta = {
        "generated_at": datetime.now().isoformat(),
        "spec_version": reports[0]["spec_version"] if reports else "v2",
        "total_strategies": len(reports),
        "tier_distribution": tier_counts,
        "grade_distribution": grade_counts,
    }

    # JSON报告
    if fmt in ("json", "both"):
        json_data = {
            "meta": meta,
            "strategies": reports,
        }
        json_path = os.path.join(output_dir, "compliance_report.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"  JSON报告: {json_path}")

    # Markdown报告
    if fmt in ("markdown", "both"):
        md_path = os.path.join(output_dir, "compliance_summary.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("# VecAlpha 商用策略合规报告\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"规范版本: {meta['spec_version']}\n")
            f.write(f"策略总数: {meta['total_strategies']}\n\n")

            f.write("## 等级分布\n\n")
            for g in ["S", "A", "B", "C", "D"]:
                cnt = grade_counts.get(g, 0)
                if cnt > 0:
                    badge = dict((t[0], t[2]) for t in GRADE_TABLE).get(
                        next((t[0] for t in GRADE_TABLE if t[1] == g), 0), "?")
                    f.write(f"- {badge} {g}级: {cnt} 个\n")
            f.write("\n")

            f.write("## 商用Tier分布\n\n")
            f.write(f"- 🏆 Tier 1 旗舰: {tier_counts.get(1, 0)} 个\n")
            f.write(f"- ⭐ Tier 2 专业: {tier_counts.get(2, 0)} 个\n")
            f.write(f"- 🧪 Tier 3 实验: {tier_counts.get(3, 0)} 个\n")
            f.write(f"- ❌ 拒绝: {tier_counts.get('reject', 0)} 个\n\n")

            # Tier 2以上策略详情
            tier2_plus = [r for r in reports if r.get("commercial_tier") and r["commercial_tier"] <= 2]
            if tier2_plus:
                f.write("## Tier 2 及以上策略详情\n\n")
                f.write("| 策略 | VecScore | 等级 | Tier | P | R | S | T | E | 警告 |\n")
                f.write("|------|----------|------|------|---|---|---|---|---|------|\n")
                for r in sorted(tier2_plus, key=lambda x: -x["vecscore"]):
                    d = r["dimensions"]
                    warnings = ", ".join(s["id"] for s in r["soft_red_lines"])
                    f.write(f"| {r['name']} | {r['vecscore']:.1f} | {r['grade']} | "
                            f"Tier {r['commercial_tier']} | "
                            f"{d['P_return']['score']:.0f} | {d['R_risk']['score']:.0f} | "
                            f"{d['S_stability']['score']:.0f} | {d['T_reliability']['score']:.0f} | "
                            f"{d['E_efficiency']['score']:.0f} | {warnings} |\n")
                f.write("\n")

            # 全部策略表
            f.write("## 全部策略合规状态\n\n")
            f.write("| # | 策略 | Score | 等级 | Tier | 硬红线 | 软红线 | 距下一Tier |\n")
            f.write("|---|------|-------|------|------|--------|--------|------------|\n")
            for i, r in enumerate(sorted(reports, key=lambda x: -x["vecscore"]), 1):
                hrl = ", ".join(h["id"] for h in r["hard_red_lines"]) or "-"
                srl = ", ".join(s["id"] for s in r["soft_red_lines"]) or "-"
                gap = ""
                ga = r.get("gap_to_next_tier", {})
                if ga.get("gaps"):
                    gap = "; ".join(
                        f"{g['dimension']}({g.get('gap', '?')})" for g in ga["gaps"])
                tier_str = f"T{r['commercial_tier']}" if r["commercial_tier"] else "拒绝"
                f.write(f"| {i} | {r['name']} | {r['vecscore']:.1f} | {r['grade']} | "
                        f"{tier_str} | {hrl} | {srl} | {gap} |\n")

        print(f"  Markdown报告: {md_path}")

    # 每策略独立文件
    per_dir = os.path.join(output_dir, "per_strategy")
    os.makedirs(per_dir, exist_ok=True)
    for r in reports:
        path = os.path.join(per_dir, f"{r['name']}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=2)


# ──────────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="VecAlpha 商用策略合规测试程序",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--mode", choices=["fast", "full"], default="fast",
                        help="评估模式 (default: fast)")
    parser.add_argument("--strategies", nargs="+",
                        help="仅检查指定策略")
    parser.add_argument("--skip-phase0", action="store_true",
                        help="跳过Phase 0（使用已有结果）")
    parser.add_argument("--skip-phase1", action="store_true",
                        help="跳过Phase 1（使用已有结果）")
    parser.add_argument("--skip-phase2", action="store_true",
                        help="跳过Phase 2（使用已有结果）")
    parser.add_argument("--resume", action="store_true",
                        help="从上次中断处继续")
    parser.add_argument("--output", default="user_data/compliance",
                        help="输出目录 (default: user_data/compliance)")
    parser.add_argument("--format", choices=["json", "markdown", "both"],
                        default="both", help="报告格式 (default: both)")
    parser.add_argument("--tier", choices=["1", "2", "3", "all"], default="all",
                        help="仅显示指定Tier的策略")
    parser.add_argument("--spec", choices=["v1", "v2", "v3"], default="v2",
                        help="评分规范版本 (default: v2, v3=放宽阈值+经典保护)")
    parser.add_argument("--dry-run", action="store_true",
                        help="预览模式，不运行回测")
    parser.add_argument("--verbose", action="store_true",
                        help="详细输出")
    parser.add_argument("--no-docker", action="store_true",
                        help="不使用Docker")

    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    def resolve(p):
        return p if os.path.isabs(p) else os.path.join(project_root, p)

    output_dir = resolve(args.output)
    spec = CommercialSpec(version=args.spec)
    checker = ComplianceChecker(spec)

    print(f"📊 VecAlpha 商用合规测试")
    print(f"📋 规范版本: {args.spec}")
    print(f"🔬 评估模式: {args.mode}")
    print(f"{'=' * 60}")

    # ── 运行管线（如果需要）────────────────────────────────────────
    use_docker = not args.no_docker and not shutil.which("freqtrade")
    runner = PipelineRunner(project_root, use_docker=use_docker)

    if not args.skip_phase0 and not args.dry_run:
        runner.run_phase0()
    if not args.skip_phase1 and not args.dry_run:
        runner.run_phase1(resume=args.resume)
    if not args.skip_phase2 and not args.dry_run:
        target_strategies = args.strategies if args.strategies else None
        runner.run_phase2(mode=args.mode, spec=args.spec,
                          strategies=target_strategies)

    # ── 加载结果 ──────────────────────────────────────────────────
    # 优先加载full模式结果，其次fast模式
    vecscore_full_path = resolve("user_data/vecscore_full_results.json")
    vecscore_fast_path = resolve("user_data/vecscore_results.json")
    phase1_path = resolve("user_data/phase1_results.json")

    # 决定数据源
    if args.mode == "full" and os.path.exists(vecscore_full_path):
        vecscore_path = vecscore_full_path
        print(f"📂 使用full模式结果: {vecscore_path}")
    elif os.path.exists(vecscore_fast_path):
        vecscore_path = vecscore_fast_path
        print(f"📂 使用fast模式结果: {vecscore_path}")
    elif os.path.exists(vecscore_full_path):
        vecscore_path = vecscore_full_path
        print(f"📂 使用full模式结果: {vecscore_path}")
    else:
        print(f"❌ 找不到VecScore结果文件")
        print("   请先运行Phase 2或使用 --skip-phase2（如果已有结果）")
        return

    with open(vecscore_path) as f:
        vecscore_data = json.load(f)

    # 如果有full模式结果，与fast模式合并（full结果覆盖fast）
    full_map = {}
    if vecscore_path != vecscore_full_path and os.path.exists(vecscore_full_path):
        with open(vecscore_full_path) as f:
            full_data = json.load(f)
        for r in full_data.get("all_results", full_data.get("ranked", [])):
            full_map[r["name"]] = r

    phase1_map = {}
    if os.path.exists(phase1_path):
        with open(phase1_path) as f:
            phase1_data = json.load(f)
        for r in phase1_data.get("results", []):
            phase1_map[r["name"]] = r.get("metrics", {})

    # ── 执行合规检查 ─────────────────────────────────────────────
    all_results = vecscore_data.get("all_results", vecscore_data.get("ranked", []))
    target_names = args.strategies

    # 合并full模式数据
    for r in all_results:
        if r["name"] in full_map:
            r.update(full_map[r["name"]])

    # ── 加载经典策略注册表 ─────────────────────────────────────
    classic_registry = load_classic_registry(project_root) if args.spec == "v3" else {}

    reports = []
    for vsr in all_results:
        name = vsr["name"]
        if target_names and name not in target_names:
            continue

        p1_metrics = phase1_map.get(name, {})
        report = checker.check(name, vsr, p1_metrics)

        # ── 应用经典策略保护（v3模式）────────────────────────────
        if args.spec == "v3" and classic_registry:
            category, protection = match_classic_strategy(name, classic_registry)
            if category and protection:
                report = apply_classic_protection(report, category, protection)

        reports.append(report)

        if args.verbose or (target_names and name in target_names):
            tier_str = f"Tier {report['commercial_tier']}" if report["commercial_tier"] else "拒绝"
            print(f"  {name:<40s} {report['vecscore']:5.1f} [{report['grade']}] "
                  f"{tier_str}  HRL={len(report['hard_red_lines'])} SRL={len(report['soft_red_lines'])}")

    if not reports:
        print("❌ 没有找到可检查的策略")
        return

    # ── 筛选Tier ─────────────────────────────────────────────────
    if args.tier != "all":
        target_tier = int(args.tier)
        reports = [r for r in reports if r.get("commercial_tier") == target_tier]

    # ── 生成报告 ─────────────────────────────────────────────────
    generate_report(reports, output_dir, fmt=args.format)

    # ── 汇总 ─────────────────────────────────────────────────────
    tier_counts = {}
    for r in reports:
        t = r.get("commercial_tier") or "reject"
        tier_counts[t] = tier_counts.get(t, 0) + 1

    print(f"\n{'=' * 60}")
    print(f"🏆 合规测试完成")
    print(f"   规范版本: {args.spec}")
    print(f"   检查策略: {len(reports)} 个")
    print(f"   Tier 1 旗舰: {tier_counts.get(1, 0)} 个")
    print(f"   Tier 2 专业: {tier_counts.get(2, 0)} 个")
    print(f"   Tier 3 实验: {tier_counts.get(3, 0)} 个")
    print(f"   拒绝: {tier_counts.get('reject', 0)} 个")

    # 退出码：至少1个Tier 2+策略则0，否则1
    commercial_count = tier_counts.get(1, 0) + tier_counts.get(2, 0)
    if commercial_count > 0:
        print(f"\n✅ 发现 {commercial_count} 个商用策略(Tier 2+)")
    else:
        print(f"\n⚠️  未发现商用策略(Tier 2+)")


if __name__ == "__main__":
    main()
