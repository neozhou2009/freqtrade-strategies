#!/usr/bin/env python3
"""
同步脚本：从 freqtrade-strategies 数据源生成 Obsidian Vault
"""

import os
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
VAULT_ROOT = Path("/mnt/d/mytools/Obsidian/vault/vault")

# ──────────────────────────────────────────────────────────────────────────────
# 模板定义
# ──────────────────────────────────────────────────────────────────────────────

STRATEGY_CARD_TEMPLATE = '''---
tags: [strategy, {family_tag}, grade-{grade}, tf-{timeframe}]
family: {family}
grade: {grade}
vecscore: {vecscore}
timeframe: {timeframe}
indicators: [{indicators_str}]
style: [{styles_str}]
commercial: {commercial}
source: strategies/{name}/{name}.py
---

# {name}

## 📊 VecScore 评分
| 维度 | 得分 | 满分 |
|------|------|------|
| P (收益) | {p_score} | 30 |
| R (风控) | {r_score} | 25 |
| S (稳定) | {s_score} | 20 |
| T (可靠) | {t_score} | 15 |
| E (效率) | {e_score} | 10 |
| **总分** | **{vecscore}** | 100 |

**等级**: {grade_icon} {grade} ({grade_meaning})
**商用资格**: {commercial_status}

## 🎯 核心特征
- **家族**: [[{family}-Overview]]
- **风格**: {styles_str}
- **市场环境**: {market}
- **交易方向**: {side}
- **复杂度**: {complexity}/10
- **时间框架**: {timeframe}

## 📈 {test_days}天回测表现
| 指标 | 数值 |
|------|------|
| ROI | {roi:.2%} |
| 年化收益 | {annualized_roi:.2%} |
| Sharpe | {sharpe:.2f} |
| MaxDD | {max_dd:.2%} |
| Win率 | {winrate:.2%} |
| 交易数 | {trades} |

## 🔗 关联策略
### 同家族
{family_links}

### 同风格
{style_links}

## 📝 设计思想
{design_thought}

## ⚠️ 风险提示
{risk_notes}

## 📋 使用建议
- **适用场景**: {market} 市场
- **参数调优**: {hyperopt_hint}
- **止损设置**: {stoploss}

---
*数据更新: {updated_at}*
'''

INDICATOR_TEMPLATE = '''---
tags: [indicator]
---

# {name}

## 📊 基本信息简介
{description}

## 📈 策略应用场景
以下策略使用了此指标：

{strategies_using}

## 🔗 组合搭配建议
常与以下指标组合：
{combinations}

## 📚 参考资料链接
- Freqtrade Wiki: {freqtrade_url}
- TradingView: {tradingview_url}

---
'''

FAMILY_OVERVIEW_TEMPLATE = '''---
tags: [family, strategy-family]
---

# {family_name} 家族

## 🏠 家族特征
- **核心思想**: {core_idea}
- **代表策略数**: {member_count}
- **主要风格**: {main_styles}
- **典型时间框架**: {timeframes}

## 📊 家族成员
| 策略 | 等级 | VecScore | 时间框架 |
|------|------|----------|----------|
{member_table}

## 🔗 进化路线图
```
{evolution_chain}
```

## 📝 设计思想
{design_notes}

---
'''

# ──────────────────────────────────────────────────────────────────────────────
# 加载数据源
# ──────────────────────────────────────────────────────────────────────────────

def load_json(path):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}

def load_all_data():
    registry = load_json(PROJECT_ROOT / "strategy_registry.json")

    vecscore_files = [
        ("default", PROJECT_ROOT / "user_data/vecscore_results.json"),
        ("90d", PROJECT_ROOT / "user_data/vecscore_results_90d.json"),
        ("6m", PROJECT_ROOT / "user_data/vecscore_results_6m.json"),
        ("1y", PROJECT_ROOT / "user_data/vecscore_results_1y.json"),
    ]

    vecscore_data = {}
    for label, path in vecscore_files:
        data = load_json(path)
        if data:
            vecscore_data[label] = data

    phase1_files = [
        ("default", PROJECT_ROOT / "user_data/phase1_results.json"),
        ("90d", PROJECT_ROOT / "user_data/phase1_results_90d.json"),
    ]

    phase1_data = {}
    for label, path in phase1_files:
        data = load_json(path)
        if data:
            phase1_data[label] = data

    return registry, vecscore_data, phase1_data

# ──────────────────────────────────────────────────────────────────────────────
# 策略卡片生成
# ──────────────────────────────────────────────────────────────────────────────

GRADE_ICONS = {"S": "🏆", "A": "⭐", "B": "✅", "C": "⚠️", "D": "❌"}
GRADE_MEANINGS = {
    "S": "旗舰策略：首页重点推荐",
    "A": "商用推荐：上架推荐池",
    "B": "可用：上架但不主推",
    "C": "风险：仅供查阅",
    "D": "不合格：禁止上架"
}

def get_vecscore_metrics(name, vecscore_data, phase1_data):
    """提取策略的VecScore和回测指标"""
    result = {
        "vecscore": 0, "grade": "D", "grade_icon": "❌", "grade_meaning": "不合格",
        "p_score": 0, "r_score": 0, "s_score": 0, "t_score": 0, "e_score": 0,
        "roi": 0, "annualized_roi": 0, "sharpe": 0, "max_dd": 0.5, "winrate": 0, "trades": 0,
        "commercial": False, "is_estimated": True, "test_days": 30
    }

    # 从vecscore结果提取
    for label, data in vecscore_data.items():
        for item in data.get("ranked", []) + data.get("all_results", []):
            if item.get("name") == name:
                result["vecscore"] = item.get("vecscore", 0)
                result["grade"] = item.get("grade", "D")
                result["grade_icon"] = GRADE_ICONS.get(result["grade"], "❌")
                result["grade_meaning"] = GRADE_MEANINGS.get(result["grade"], "不合格")
                result["commercial"] = item.get("commercial_eligible", False)
                result["is_estimated"] = item.get("is_estimated", True)

                dims = item.get("dimensions", {})
                if dims:
                    result["p_score"] = dims.get("P_return", {}).get("score", 0)
                    result["r_score"] = dims.get("R_risk", {}).get("score", 0)
                    result["s_score"] = dims.get("S_stability", {}).get("score", 0)
                    result["t_score"] = dims.get("T_reliability", {}).get("score", 0)
                    result["e_score"] = dims.get("E_efficiency", {}).get("score", 0)
                else:
                    result["p_score"] = item.get("P", 0)
                    result["r_score"] = item.get("R", 0)
                    result["s_score"] = item.get("S", 0)
                    result["t_score"] = item.get("T", 0)
                    result["e_score"] = item.get("E", 0)
                break

    # 从phase1提取回测指标
    for label, data in phase1_data.items():
        for item in data.get("results", []):
            if item.get("name") == name:
                metrics = item.get("metrics", {})
                result["roi"] = metrics.get("roi", 0) or 0
                result["sharpe"] = metrics.get("sharpe", 0) or 0
                result["max_dd"] = metrics.get("max_drawdown", 0.5) or 0.5
                result["winrate"] = metrics.get("win_rate", 0) or 0
                result["trades"] = metrics.get("trades", 0) or 0
                
                meta_days = data.get("meta", {}).get("days", 30)
                result["test_days"] = meta_days
                if meta_days > 0:
                    result["annualized_roi"] = (result["roi"] / meta_days) * 365
                break

    return result

def generate_strategy_card(name, reg_info, vecscore_data, phase1_data, family_groups, style_groups):
    """生成单个策略卡片"""
    metrics = get_vecscore_metrics(name, vecscore_data, phase1_data)

    family = reg_info.get("family", name)
    family_tag = family.lower().replace(" ", "-")

    indicators = reg_info.get("indicators", [])
    indicators_str = ", ".join([f"[[{i}]]" for i in indicators]) if indicators else "未标注"

    styles = reg_info.get("style", [])
    styles_str = ", ".join(styles) if styles else "未标注"

    timeframe = reg_info.get("timeframe", "5m")

    # 关联策略
    family_members = family_groups.get(family, [])
    family_links = "\n".join([f"- [[{m}]]" for m in family_members if m != name]) or "- (独立策略)"

    same_style = []
    for s in styles:
        same_style.extend(style_groups.get(s, []))
    same_style = [m for m in same_style if m != name][:5]
    style_links = "\n".join([f"- [[{m}]]" for m in same_style]) or "- (无同风格策略)"

    content = STRATEGY_CARD_TEMPLATE.format(
        name=name,
        family=family,
        family_tag=family_tag,
        grade=metrics["grade"],
        grade_icon=metrics["grade_icon"],
        grade_meaning=metrics["grade_meaning"],
        vecscore=metrics["vecscore"],
        p_score=metrics["p_score"],
        r_score=metrics["r_score"],
        s_score=metrics["s_score"],
        t_score=metrics["t_score"],
        e_score=metrics["e_score"],
        timeframe=timeframe,
        indicators_str=indicators_str,
        styles_str=styles_str,
        commercial=str(metrics["commercial"]).lower(),
        commercial_status="✅ 符合商用资格" if metrics["commercial"] else "❌ 不符合商用资格",
        market=reg_info.get("market", "Unknown"),
        side=reg_info.get("side", "Long"),
        complexity=reg_info.get("complexity", 5),
        test_days=metrics["test_days"],
        roi=metrics["roi"],
        annualized_roi=metrics["annualized_roi"],
        sharpe=metrics["sharpe"],
        max_dd=metrics["max_dd"],
        winrate=metrics["winrate"],
        trades=metrics["trades"],
        family_links=family_links,
        style_links=style_links,
        design_thought=reg_info.get("design_thought", "待补充"),
        risk_notes="待从评审报告提取",
        hyperopt_hint="含Hyperopt参数" if "hyperopt" in reg_info.get("features", []) else "固定参数",
        stoploss=reg_info.get("stoploss", "-0.1"),
        updated_at=datetime.now().strftime("%Y-%m-%d")
    )

    return content, family

def write_strategy_cards(registry, vecscore_data, phase1_data):
    """生成所有策略卡片"""
    family_groups = defaultdict(list)
    style_groups = defaultdict(list)

    for name, info in registry.items():
        family = info.get("family", name)
        family_groups[family].append(name)
        for s in info.get("style", []):
            style_groups[s].append(name)

    written = 0
    for name, reg_info in registry.items():
        content, family = generate_strategy_card(
            name, reg_info, vecscore_data, phase1_data, family_groups, style_groups
        )

        # 写入对应家族目录
        family_dir = VAULT_ROOT / "01_Strategies" / f"Family-{family}"
        family_dir.mkdir(parents=True, exist_ok=True)

        card_path = family_dir / f"{name}.md"
        card_path.write_text(content)
        written += 1

    print(f"[✓] Generated {written} strategy cards")

    # 生成家族概览页
    generate_family_overviews(family_groups, registry, vecscore_data)

    return family_groups, style_groups

def generate_family_overviews(family_groups, registry, vecscore_data):
    """生成家族概览页"""
    for family, members in family_groups.items():
        if len(members) <= 1:
            continue

        # 统计信息
        member_data = []
        for m in members:
            info = registry.get(m, {})
            metrics = get_vecscore_metrics(m, vecscore_data, {})
            member_data.append({
                "name": m,
                "grade": metrics["grade"],
                "vecscore": metrics["vecscore"],
                "timeframe": info.get("timeframe", "5m")
            })

        member_table = "\n".join([
            f"| [[{d['name']}]] | {d['grade']} | {d['vecscore']} | {d['timeframe']} |"
            for d in sorted(member_data, key=lambda x: -x["vecscore"])
        ])

        evolution_chain = " → ".join([d["name"] for d in member_data])

        styles = set()
        timeframes = set()
        for m in members:
            info = registry.get(m, {})
            styles.update(info.get("style", []))
            timeframes.add(info.get("timeframe", "5m"))

        content = FAMILY_OVERVIEW_TEMPLATE.format(
            family_name=family,
            core_idea="待补充",
            member_count=len(members),
            main_styles=", ".join(styles) or "未标注",
            timeframes=", ".join(timeframes),
            member_table=member_table,
            evolution_chain=evolution_chain,
            design_notes="待从策略源码提取"
        )

        overview_path = VAULT_ROOT / "01_Strategies" / f"Family-{family}" / f"{family}-Overview.md"
        overview_path.write_text(content)

    print(f"[✓] Generated {len(family_groups)} family overview pages")

# ──────────────────────────────────────────────────────────────────────────────
# MOC索引页生成
# ──────────────────────────────────────────────────────────────────────────────

def generate_moc_pages(registry, vecscore_data, family_groups, style_groups):
    """生成MOC索引页"""

    # 1. 策略总览MOC
    generate_moc_strategies(registry, vecscore_data, family_groups, style_groups)

    # 2. 指标MOC
    generate_moc_indicators(registry)

    # 3. 入口页
    generate_start_here(registry, vecscore_data)

def generate_moc_strategies(registry, vecscore_data, family_groups, style_groups):
    """策略总览MOC"""

    # 按等级分组
    by_grade = defaultdict(list)
    for name, info in registry.items():
        metrics = get_vecscore_metrics(name, vecscore_data, {})
        by_grade[metrics["grade"]].append((name, metrics["vecscore"], info.get("timeframe", "5m")))

    content = '''# 策略知识地图

> 本页是策略导航入口，按不同维度组织策略卡片

## 🏆 按等级浏览

'''

    for grade in ["S", "A", "B", "C", "D"]:
        icon = GRADE_ICONS[grade]
        meaning = GRADE_MEANINGS[grade]
        members = sorted(by_grade[grade], key=lambda x: -x[1])

        if members:
            content += f"### {icon} {grade}级 ({meaning})\n"
            for name, score, tf in members[:20]:
                content += f"- [[{name}]] ⭐ VecScore: {score} | {tf}\n"
            if len(members) > 20:
                content += f"- ... 还有 {len(members) - 20} 个策略\n"
            content += "\n"

    # 按家族分组
    content += "## 🏠 按家族浏览\n\n"

    for family, members in sorted(family_groups.items()):
        if len(members) > 1:
            content += f"### {family} 家族\n"
            content += f"> [[{family}-Overview]]\n"
            for m in sorted(members)[:10]:
                content += f"- [[{m}]]\n"
            content += "\n"

    # 按风格分组
    content += "## 🎯 按风格浏览\n\n"

    for style, members in sorted(style_groups.items()):
        if len(members) >= 3:
            content += f"### {style}\n"
            for m in sorted(members)[:15]:
                content += f"- [[{m}]]\n"
            content += "\n"

    # 时间框架表
    by_tf = defaultdict(list)
    for name, info in registry.items():
        tf = info.get("timeframe", "unknown")
        by_tf[tf].append(name)

    content += "## ⏱ 按时间框架浏览\n\n"
    content += "| Timeframe | 策略数 | 代表策略 |\n|-----------|--------|----------|\n"
    for tf in ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "unknown"]:
        members = by_tf.get(tf, [])
        if members:
            examples = ", ".join([f"[[{m}]]" for m in members[:3]])
            content += f"| {tf} | {len(members)} | {examples} |\n"

    content += "\n---\n> 💡 点击策略名查看完整卡片\n"

    moc_path = VAULT_ROOT / "00_Index" / "MOC-Strategies.md"
    moc_path.write_text(content)
    print("[✓] Generated MOC-Strategies.md")

def generate_moc_indicators(registry):
    """指标MOC"""
    indicator_counts = defaultdict(list)

    for name, info in registry.items():
        for ind in info.get("indicators", []):
            indicator_counts[ind].append(name)

    content = '''# 指标知识地图

> 本页列出所有策略使用的指标及其应用场景

## 📊 指标使用统计

| 指标 | 策略数 | 代表策略 |
|------|--------|----------|
'''

    for ind, strategies in sorted(indicator_counts.items(), key=lambda x: -len(x[1])):
        examples = ", ".join([f"[[{s}]]" for s in strategies[:3]])
        content += f"| [[{ind}]] | {len(strategies)} | {examples} |\n"

    content += "\n## 📈 指标详情页\n\n"
    for ind in sorted(indicator_counts.keys()):
        content += f"- [[{ind}]] ({len(indicator_counts[ind])} 策略使用)\n"

    moc_path = VAULT_ROOT / "00_Index" / "MOC-Indicators.md"
    moc_path.write_text(content)
    print("[✓] Generated MOC-Indicators.md")

def generate_start_here(registry, vecscore_data):
    """入口页"""

    total = len(registry)
    graded = defaultdict(int)
    commercial = 0

    for name in registry:
        metrics = get_vecscore_metrics(name, vecscore_data, {})
        graded[metrics["grade"]] += 1
        if metrics["commercial"]:
            commercial += 1

    content = f'''# Freqtrade Strategies 知识库

> 本Vault包含 {total} 个Freqtrade策略的完整分析数据

## 📊 快速概览

| 指标 | 数量 |
|------|------|
| 总策略数 | {total} |
| 🏆 S级 | {graded["S"]} |
| ⭐ A级 | {graded["A"]} |
| ✅ B级 | {graded["B"]} |
| ⚠️ C级 | {graded["C"]} |
| ❌ D级 | {graded["D"]} |
| 💼 商用资格 | {commercial} |

## 🚀 快速入口

- [[MOC-Strategies]] - 策略总览地图
- [[MOC-Indicators]] - 指标知识地图
- [[VecScore-Overview]] - 五维评分体系

## 📁 目录结构

```
00_Index/      ← 入口导航（从这里开始）
01_Strategies/ ← 策略卡片（按家族分簇）
02_Indicators/ ← 指标知识页
04_Evaluation/ ← VecScore评分体系
06_Leaderboard/ ← 排行榜快照
```

## 🔍 推荐阅读流程

1. 先看 [[MOC-Strategies]] 了解策略分类
2. 选择感兴趣的家族，如 [[Nostalgia-Overview]]
3. 深入具体策略卡片，如 [[NostalgiaForInfinityV7]]
4. 查看关联指标，如 [[RSI]]、[[EMA]]

---
*数据更新: {datetime.now().strftime("%Y-%m-%d")}*
'''

    start_path = VAULT_ROOT / "00_Index" / "Start-Here.md"
    start_path.write_text(content)
    print("[✓] Generated Start-Here.md")

# ──────────────────────────────────────────────────────────────────────────────
# 指标页生成
# ──────────────────────────────────────────────────────────────────────────────

def generate_indicator_pages(registry):
    """生成指标知识页"""

    indicator_strategies = defaultdict(list)
    indicator_combos = defaultdict(set)

    for name, info in registry.items():
        inds = info.get("indicators", [])
        for ind in inds:
            indicator_strategies[ind].append(name)

        # 记录组合
        if len(inds) >= 2:
            for i in range(len(inds)):
                for j in range(i+1, len(inds)):
                    combo = f"{inds[i]} + {inds[j]}"
                    indicator_combos[inds[i]].add(inds[j])
                    indicator_combos[inds[j]].add(inds[i])

    for ind, strategies in indicator_strategies.items():
        strategies_using = "\n".join([f"- [[{s}]]" for s in sorted(strategies)[:20]])
        if len(strategies) > 20:
            strategies_using += f"\n- ... 还有 {len(strategies) - 20} 个策略"

        combos = indicator_combos.get(ind, set())
        combinations = "\n".join([f"- [[{c}]]" for c in sorted(combos)[:10]]) or "- (无常见组合)"

        content = INDICATOR_TEMPLATE.format(
            name=ind,
            description=f"{ind} 是常用的技术分析指标",
            strategies_using=strategies_using,
            combinations=combinations,
            freqtrade_url=f"https://www.freqtrade.io/en/stable/strategy-custom-indicators/",
            tradingview_url=f"https://www.tradingview.com/scripts/{ind.lower()}/"
        )

        ind_path = VAULT_ROOT / "02_Indicators" / f"{ind}.md"
        ind_path.write_text(content)

    print(f"[✓] Generated {len(indicator_strategies)} indicator pages")

# ──────────────────────────────────────────────────────────────────────────────
# VecScore体系页
# ──────────────────────────────────────────────────────────────────────────────

def generate_vecscore_pages():
    """生成VecScore评估体系页"""

    overview = '''# VecScore 五维评分体系

> VecScore 是策略综合评分系统，满分100分

## 📊 五维度权重

| 维度 | 名称 | 权重 | 满分 | 评估内容 |
|------|------|------|------|----------|
| P | 收益能力 | 30% | 30 | ROI、Profit Factor、平均盈利 |
| R | 风控能力 | 25% | 25 | 最大回撤、Sharpe Ratio |
| S | 稳定性 | 20% | 20 | 多时段盈利、收益波动 |
| T | 可靠性 | 15% | 15 | Train/Test过拟合检测 |
| E | 效率 | 10% | 10 | 交易频率、持仓时长 |

## 🏆 等级划分

| 等级 | 阈值 | 图标 | 含义 |
|------|------|------|------|
| S | ≥80 | 🏆 | 旗舰策略：首页重点推荐 |
| A | ≥70 | ⭐ | 商用推荐：上架推荐池 |
| B | ≥60 | ✅ | 可用：上架但不主推 |
| C | ≥50 | ⚠️ | 风险：仅供查阅 |
| D | <50 | ❌ | 不合格：禁止上架 |

## ⚠️ 红线规则

- MDD > 40% → 总分上限 40
- Sharpe < 0 → 总分上限 50

## 💼 商用资格判定

需要同时满足：
- VecScore ≥ 75
- Max Drawdown < 30%
- Sharpe ≥ 0.8
- 30天交易数 ≥ 8

---
'''

    overview_path = VAULT_ROOT / "04_Evaluation" / "VecScore-Overview.md"
    overview_path.write_text(overview)
    print("[✓] Generated VecScore-Overview.md")

# ──────────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("="*50)
    print("Freqtrade Strategies → Obsidian Vault")
    print("="*50)

    # 1. 加载数据
    print("\n[1] Loading data sources...")
    registry, vecscore_data, phase1_data = load_all_data()
    print(f"    Registry: {len(registry)} strategies")
    print(f"    VecScore: {len(vecscore_data)} result files")
    print(f"    Phase1: {len(phase1_data)} result files")

    # 2. 生成策略卡片
    print("\n[2] Generating strategy cards...")
    family_groups, style_groups = write_strategy_cards(registry, vecscore_data, phase1_data)

    # 3. 生成MOC索引
    print("\n[3] Generating MOC pages...")
    generate_moc_pages(registry, vecscore_data, family_groups, style_groups)

    # 4. 生成指标页
    print("\n[4] Generating indicator pages...")
    generate_indicator_pages(registry)

    # 5. 生成VecScore页
    print("\n[5] Generating VecScore pages...")
    generate_vecscore_pages()

    # 6. 统计
    print("\n"+"="*50)
    print("Vault generation complete!")
    print("="*50)

    md_count = sum(1 for p in VAULT_ROOT.rglob("*.md"))
    print(f"Total markdown files: {md_count}")
    print(f"Vault location: {VAULT_ROOT}")

if __name__ == "__main__":
    main()