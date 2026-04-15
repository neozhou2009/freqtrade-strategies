#!/usr/bin/env python3
"""
VecAlpha 策略静态预筛工具 (Phase 0: Static Filter)

基于代码静态分析，对策略库进行零成本预筛，输出三类结果：
  - PASS    : 通过静态检查，可进入下一阶段（快速回测初筛）
  - ELIMINATED : 命中硬性淘汰规则，不再回测
  - WARNING : 通过但有风险标记，下一阶段需额外关注

淘汰规则（硬性，R-01 ~ R-10）：
  R-01  AST 语法错误（无法解析）
  R-02  文件名含危险关键词（lookahead, leak）
  R-03  代码中含 .shift(0) 且在入场逻辑函数内（未来视）
  R-04  注释含 "do not use live" / "do not use this strategy live"
  R-05  有效代码行数 < 60
  R-06  strategy_registry.json 中标注 test-strategy
  R-07  无条件全量入场（AlwaysBuy 类）
  R-08  仅有旧版 populate_buy_trend，无 populate_entry_trend（废弃API）
  R-09  明确标注 excluded 字段（registry 中）
  R-10  家族去重：同 family 超过 2 个，仅保留 complexity 最高的 2 个

警告规则（W-01 ~ W-06，不淘汰，标记）：
  W-01  无 stoploss 类属性定义
  W-02  无 timeframe 类属性定义
  W-03  含 Hyperopt 参数但缺少默认值赋值
  W-04  使用 multi-timeframe（informative_pairs）
  W-05  代码超过 2000 行（高复杂度，回测慢）
  W-06  同时使用旧版和新版 API（兼容性风险）

用法:
    # 从项目根目录运行
    python scripts/static_filter.py

    # 指定策略目录和 registry
    python scripts/static_filter.py --strategies-dir strategies/ --registry strategy_registry.json

    # 输出到指定文件
    python scripts/static_filter.py --output user_data/static_filter_result.json

    # 只显示摘要，不写文件
    python scripts/static_filter.py --summary-only
"""

import os
import ast
import re
import json
import glob
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# ──────────────────────────────────────────────────────────────────────────────
# 配置常量
# ──────────────────────────────────────────────────────────────────────────────

# R-02: 文件名危险关键词（小写匹配）
DANGEROUS_NAME_KEYWORDS = ["lookahead", "leak", "cheat", "future"]

# R-04: 注释中的禁用声明（小写匹配）
DO_NOT_USE_PHRASES = [
    "do not use live",
    "do not use this strategy live",
    "don't use live",
    "not for live",
    "not suitable for live",
]

# R-07: 无条件入场检测的已知策略名单（直接匹配）
UNCONDITIONAL_BUY_NAMES = {"AlwaysBuy", "BuyAllSellAllStrategy", "BuyOnly", "Fakebuy", "YOLO"}

# 家族去重最大保留数量
MAX_PER_FAMILY = 2

# R-10 优先白名单：这些策略在家族去重时强制保留（不参与排序竞争）
# 用于保护经过社区验证的旗舰策略，防止被版本号更高的老旧分支误淘汰
PRIORITY_WHITELIST = {
    "NostalgiaForInfinityNext_ChangeToTower_V6",  # NFI 旗舰最新版
    "CombinedBinHAndClucV7",                       # Bin+Cluc 最成熟融合版
    "BigZ04_TSL3",                                  # BigZ 追踪止损最优版
    "Obelisk_Ichimoku_ZEMA_v1",                    # Ichimoku 趋势首选
    "MACDStrategy_crossed",                         # 2025 全年回测最佳
    "SmoothScalp",                                  # 剥头皮代码质量最高
    "ClucHAwerk",                                   # Cluc+HA 抗噪版
}

# 有效代码行数最小值（R-05）
# 注意：MACDStrategy_crossed(57行)、BinHV45(54行) 属于有意设计的极简策略，不应被淘汰
# 门槛设为 40，只淘汰真正只有少量逻辑的草稿策略
MIN_CODE_LINES = 40


# ──────────────────────────────────────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────────────────────────────────────

def count_code_lines(content: str) -> int:
    """统计有效代码行数（排除空行和纯注释行）"""
    lines = content.splitlines()
    count = 0
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            count += 1
    return count


def can_parse_ast(content: str) -> tuple[bool, str]:
    """尝试 AST 解析，返回 (成功, 错误信息)"""
    try:
        ast.parse(content)
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)


def has_dangerous_name(strategy_name: str) -> tuple[bool, str]:
    """R-02: 检测策略名是否含危险关键词"""
    name_lower = strategy_name.lower()
    for kw in DANGEROUS_NAME_KEYWORDS:
        if kw in name_lower:
            return True, f"策略名含危险关键词: '{kw}'"
    return False, ""


def has_do_not_use_comment(content: str) -> tuple[bool, str]:
    """R-04: 检测是否有明确禁用注释"""
    content_lower = content.lower()
    for phrase in DO_NOT_USE_PHRASES:
        if phrase in content_lower:
            return True, f"注释中发现禁用声明: '{phrase}'"
    return False, ""


def check_shift_zero_in_entry(content: str) -> tuple[bool, str]:
    """R-03: 检测 .shift(0) 是否出现在入场函数内"""
    # 找到入场函数体的大致范围
    entry_func_pattern = re.compile(
        r"def\s+(populate_entry_trend|populate_buy_trend)\s*\(.*?\n(.*?)(?=\ndef\s|\Z)",
        re.DOTALL,
    )
    for match in entry_func_pattern.finditer(content):
        func_body = match.group(2)
        if re.search(r"\.\s*shift\s*\(\s*0\s*\)", func_body):
            return True, "在入场函数内检测到 .shift(0)（疑似未来视）"
    return False, ""


def is_unconditional_buyer(strategy_name: str, content: str) -> tuple[bool, str]:
    """R-07: 检测是否是无条件入场策略"""
    if strategy_name in UNCONDITIONAL_BUY_NAMES:
        return True, f"已知无条件入场策略: {strategy_name}"

    # 检测 buy 条件列: dataframe['enter_long'] = 1 / dataframe['buy'] = 1 (unconditional)
    if re.search(
        r"dataframe\[[\'\"](?:enter_long|buy)[\'\"]\]\s*=\s*1(?!\s*where|\s*\()",
        content,
    ):
        # 进一步确认 populate_entry_trend 函数极短
        lines = count_code_lines(content)
        if lines < 40:
            return True, "无条件设置 enter_long=1，且函数体极简"
    return False, ""


def check_deprecated_api(content: str) -> tuple[str, str]:
    """
    R-08: 检测废弃 API 使用
    返回: ('deprecated_only' | 'both' | 'new_only' | 'none', 描述)
    """
    has_old = bool(re.search(r"def\s+populate_buy_trend\s*\(", content))
    has_new = bool(re.search(r"def\s+populate_entry_trend\s*\(", content))

    if has_old and not has_new:
        return "deprecated_only", "仅使用旧版 API populate_buy_trend，无 populate_entry_trend"
    if has_old and has_new:
        return "both", "同时存在旧版 populate_buy_trend 和新版 populate_entry_trend"
    if has_new:
        return "new_only", ""
    return "none", "未找到入场函数（populate_entry_trend 或 populate_buy_trend）"


def check_warnings(content: str, strategy_name: str) -> list[dict]:
    """检测所有警告规则，返回警告列表"""
    warnings = []

    # W-01: 无 stoploss
    if not re.search(r"stoploss\s*=\s*-[\d.]+", content):
        warnings.append({"code": "W-01", "msg": "未发现 stoploss 类属性定义"})

    # W-02: 无 timeframe
    if not re.search(r"timeframe\s*=\s*['\"][\w]+['\"]", content):
        warnings.append({"code": "W-02", "msg": "未发现 timeframe 类属性定义"})

    # W-03: Hyperopt 参数但可能无默认值
    has_hyperopt_params = bool(
        re.search(r"(DecimalParameter|IntParameter|CategoricalParameter)\s*\(", content)
    )
    if has_hyperopt_params:
        # 检查是否有 .value 取值模式（说明设计为 hyperopt 专用）
        value_count = len(re.findall(r"\.value\b", content))
        param_count = len(
            re.findall(r"(DecimalParameter|IntParameter|CategoricalParameter)\s*\(", content)
        )
        if value_count > param_count * 0.8:  # 大量使用 .value
            warnings.append({
                "code": "W-03",
                "msg": f"含 {param_count} 个 Hyperopt 参数，需执行 hyperopt 后才能有效回测",
            })

    # W-04: 多时间框架
    if re.search(r"def\s+informative_pairs\s*\(|merge_informative_pair\s*\(", content):
        warnings.append({"code": "W-04", "msg": "使用多时间框架（MTF），回测需要额外数据"})

    # W-05: 代码行数超限
    total_lines = len(content.splitlines())
    if total_lines > 2000:
        warnings.append({"code": "W-05", "msg": f"代码总行数 {total_lines}，回测较慢"})

    # W-06: 兼容性（旧新 API 共存，已在 R-08 中检测，这里只做 warning 版本）
    api_status, _ = check_deprecated_api(content)
    if api_status == "both":
        warnings.append({"code": "W-06", "msg": "同时使用旧版和新版入场 API，存在兼容性风险"})

    return warnings


# ──────────────────────────────────────────────────────────────────────────────
# 核心分析函数
# ──────────────────────────────────────────────────────────────────────────────

def analyze_strategy(strategy_name: str, filepath: str, registry_entry: dict) -> dict:
    """
    对单个策略文件执行全部静态检查
    返回 {'result': 'PASS'|'ELIMINATED', 'reasons': [...], 'warnings': [...]}
    """
    result = {
        "name": strategy_name,
        "filepath": filepath,
        "result": "PASS",
        "eliminate_reasons": [],
        "warnings": [],
    }

    # ── 读取文件 ──────────────────────────────────────────────
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        result["result"] = "ELIMINATED"
        result["eliminate_reasons"].append({"rule": "R-01", "msg": f"文件读取失败: {e}"})
        return result

    # R-01: AST 解析
    ok, err = can_parse_ast(content)
    if not ok:
        result["result"] = "ELIMINATED"
        result["eliminate_reasons"].append({"rule": "R-01", "msg": err})
        return result  # 解析失败无法继续

    # R-02: 危险策略名
    hit, msg = has_dangerous_name(strategy_name)
    if hit:
        result["result"] = "ELIMINATED"
        result["eliminate_reasons"].append({"rule": "R-02", "msg": msg})

    # R-04: 禁用注释
    hit, msg = has_do_not_use_comment(content)
    if hit:
        result["result"] = "ELIMINATED"
        result["eliminate_reasons"].append({"rule": "R-04", "msg": msg})

    # R-03: shift(0) 在入场函数
    hit, msg = check_shift_zero_in_entry(content)
    if hit:
        result["result"] = "ELIMINATED"
        result["eliminate_reasons"].append({"rule": "R-03", "msg": msg})

    # R-05: 有效代码行数
    code_lines = count_code_lines(content)
    result["code_lines"] = code_lines
    if code_lines < MIN_CODE_LINES:
        result["result"] = "ELIMINATED"
        result["eliminate_reasons"].append({
            "rule": "R-05",
            "msg": f"有效代码行数 {code_lines} < {MIN_CODE_LINES}，策略过于简单",
        })

    # R-06: registry test-strategy
    registry_features = registry_entry.get("features", [])
    if "test-strategy" in registry_features:
        result["result"] = "ELIMINATED"
        result["eliminate_reasons"].append({"rule": "R-06", "msg": "registry 中标注为 test-strategy"})

    # R-07: 无条件入场
    hit, msg = is_unconditional_buyer(strategy_name, content)
    if hit:
        result["result"] = "ELIMINATED"
        result["eliminate_reasons"].append({"rule": "R-07", "msg": msg})

    # R-08: 废弃 API
    api_status, api_msg = check_deprecated_api(content)
    if api_status == "deprecated_only":
        result["result"] = "ELIMINATED"
        result["eliminate_reasons"].append({"rule": "R-08", "msg": api_msg})
    elif api_status == "none":
        result["result"] = "ELIMINATED"
        result["eliminate_reasons"].append({"rule": "R-08", "msg": api_msg})

    # R-09: registry excluded
    if registry_entry.get("excluded"):
        result["result"] = "ELIMINATED"
        result["eliminate_reasons"].append({
            "rule": "R-09",
            "msg": f"registry 中标注 excluded: {registry_entry['excluded']}",
        })

    # ── 警告检测（仅对通过的策略）──────────────────────────
    result["warnings"] = check_warnings(content, strategy_name)

    # ── 附加元数据 ──────────────────────────────────────────
    result["family"] = registry_entry.get("family", strategy_name)
    result["complexity"] = registry_entry.get("complexity", 0)
    result["timeframe"] = registry_entry.get("timeframe", "unknown")
    result["style"] = registry_entry.get("style", [])

    return result


def _version_score(name: str) -> int:
    """
    从策略名中提取版本分数，用于 R-10 家族去重时的次级排序。
    版本号越高 → 分数越高 → 优先保留。
    例:  V6 → 6,  v37 → 37,  _ChangeToTower_V6 → 6,  无版本 → 0
    """
    nums = re.findall(r"[vV](\d+)", name)
    if nums:
        return max(int(n) for n in nums)
    # 名字末尾的纯数字也算版本
    trailing = re.search(r"(\d+)$", name)
    if trailing:
        return int(trailing.group(1))
    return 0


def apply_family_dedup(pass_list: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    R-10: 家族去重
    同一 family 超过 MAX_PER_FAMILY 个通过策略时，按以下优先级保留：
      1. PRIORITY_WHITELIST 中的策略强制保留（不计入配额竞争）
      2. 剩余按 complexity → version_score → name_length 排序，保留 top N
    返回 (deduped_pass_list, newly_eliminated_list)
    """
    family_groups = defaultdict(list)
    for strat in pass_list:
        family_groups[strat["family"]].append(strat)

    final_pass = []
    newly_eliminated = []

    for family, members in family_groups.items():
        if len(members) <= MAX_PER_FAMILY:
            final_pass.extend(members)
        else:
            # 先分离白名单策略（强制保留）
            whitelisted = [m for m in members if m["name"] in PRIORITY_WHITELIST]
            non_whitelisted = [m for m in members if m["name"] not in PRIORITY_WHITELIST]

            # 剩余空位
            slots_remaining = max(0, MAX_PER_FAMILY - len(whitelisted))

            # 非白名单按三级排序竞争剩余空位
            non_whitelisted_sorted = sorted(
                non_whitelisted,
                key=lambda x: (
                    x.get("complexity", 0),
                    _version_score(x["name"]),
                    len(x["name"]),
                ),
                reverse=True,
            )

            kept = whitelisted + non_whitelisted_sorted[:slots_remaining]
            eliminated = non_whitelisted_sorted[slots_remaining:]

            final_pass.extend(kept)
            kept_names = [k["name"] for k in kept]
            for s in eliminated:
                s["result"] = "ELIMINATED"
                s["eliminate_reasons"].append({
                    "rule": "R-10",
                    "msg": (
                        f"家族去重：{family} 共 {len(members)} 个策略通过，"
                        f"保留 {kept_names}，"
                        f"本策略 complexity={s.get('complexity', 0)} "
                        f"version={_version_score(s['name'])} 排名靠后"
                    ),
                })
            newly_eliminated.extend(eliminated)

    return final_pass, newly_eliminated


# ──────────────────────────────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────────────────────────────

def run_filter(strategies_dir: str, registry_path: str, output_path: str = None,
               summary_only: bool = False) -> dict:
    """执行完整的静态预筛流程"""

    # 加载 registry
    registry = {}
    if os.path.exists(registry_path):
        with open(registry_path, "r") as f:
            registry = json.load(f)
        print(f"✅ 已加载 strategy_registry.json ({len(registry)} 个策略)")
    else:
        print(f"⚠️  未找到 {registry_path}，将跳过 registry 相关检查（R-06, R-09, R-10）")

    # 收集所有策略文件
    pattern = os.path.join(strategies_dir, "**", "*.py")
    all_files = sorted(glob.glob(pattern, recursive=True))
    strategy_files = [
        f for f in all_files if os.path.basename(f) != "__init__.py"
    ]
    print(f"📁 发现 {len(strategy_files)} 个策略文件（来自 {strategies_dir}）\n")

    pass_list = []
    eliminated_list = []
    stats = defaultdict(int)
    rule_hit_counts = defaultdict(int)

    for filepath in strategy_files:
        strategy_name = os.path.basename(filepath)[:-3]
        registry_entry = registry.get(strategy_name, {})

        result = analyze_strategy(strategy_name, filepath, registry_entry)

        if result["result"] == "PASS":
            pass_list.append(result)
            stats["pass"] += 1
            warn_count = len(result.get("warnings", []))
            stats["warnings_total"] += warn_count
            for w in result.get("warnings", []):
                rule_hit_counts[w["code"]] += 1
        else:
            eliminated_list.append(result)
            stats["eliminated"] += 1
            for r in result.get("eliminate_reasons", []):
                rule_hit_counts[r["rule"]] += 1

    # R-10: 家族去重
    pass_after_dedup, dedup_eliminated = apply_family_dedup(pass_list)
    eliminated_list.extend(dedup_eliminated)
    stats["eliminated"] += len(dedup_eliminated)
    stats["pass"] = len(pass_after_dedup)
    if dedup_eliminated:
        rule_hit_counts["R-10"] += len(dedup_eliminated)

    # 统计警告分布
    warning_distribution = defaultdict(int)
    for s in pass_after_dedup:
        for w in s.get("warnings", []):
            warning_distribution[w["code"]] += 1

    # 构建输出结构
    output = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "strategies_dir": strategies_dir,
            "total_scanned": len(strategy_files),
            "pass_count": stats["pass"],
            "eliminated_count": stats["eliminated"],
            "pass_rate": f"{stats['pass'] / len(strategy_files) * 100:.1f}%",
        },
        "rule_hit_counts": dict(sorted(rule_hit_counts.items())),
        "warning_distribution": dict(warning_distribution),
        "pass": [
            {
                "name": s["name"],
                "family": s.get("family"),
                "complexity": s.get("complexity"),
                "timeframe": s.get("timeframe"),
                "style": s.get("style"),
                "code_lines": s.get("code_lines"),
                "warnings": s.get("warnings", []),
            }
            for s in sorted(pass_after_dedup, key=lambda x: x["name"])
        ],
        "eliminated": [
            {
                "name": s["name"],
                "rules": [r["rule"] for r in s.get("eliminate_reasons", [])],
                "reasons": [r["msg"] for r in s.get("eliminate_reasons", [])],
            }
            for s in sorted(eliminated_list, key=lambda x: x["name"])
        ],
    }

    # ── 打印摘要 ──────────────────────────────────────────────
    print("=" * 60)
    print("📊 VecAlpha 静态预筛结果摘要")
    print("=" * 60)
    print(f"  总扫描策略数  : {output['meta']['total_scanned']}")
    print(f"  ✅ PASS       : {output['meta']['pass_count']} ({output['meta']['pass_rate']})")
    print(f"  ❌ ELIMINATED : {output['meta']['eliminated_count']}")
    print()
    print("📋 淘汰规则触发统计:")
    for rule in sorted(k for k in rule_hit_counts if k.startswith("R-")):
        print(f"    {rule} : {rule_hit_counts[rule]} 个策略")
    print()
    print("⚠️  警告规则分布 (PASS 策略中):")
    for rule in sorted(warning_distribution.keys()):
        print(f"    {rule} : {warning_distribution[rule]} 个策略")

    if not summary_only:
        print()
        print("── PASS 策略清单（按名称排序）──")
        for s in output["pass"]:
            warn_str = ""
            if s["warnings"]:
                codes = ", ".join(w["code"] for w in s["warnings"])
                warn_str = f"  ⚠️ [{codes}]"
            print(f"  ✅ {s['name']:<45} tf={s['timeframe']:<5} complexity={s['complexity']}{warn_str}")

        print()
        print("── ELIMINATED 策略清单（按名称排序）──")
        for s in output["eliminated"]:
            rules_str = ", ".join(s["rules"])
            print(f"  ❌ {s['name']:<45} [{rules_str}]")

    print()
    print("=" * 60)

    # 写入文件
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"💾 完整结果已保存到: {output_path}")

    return output


# ──────────────────────────────────────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="VecAlpha Phase 0: 策略静态代码预筛工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--strategies-dir",
        default="strategies",
        help="策略目录路径（默认: strategies）",
    )
    parser.add_argument(
        "--registry",
        default="strategy_registry.json",
        help="strategy_registry.json 文件路径（默认: strategy_registry.json）",
    )
    parser.add_argument(
        "--output",
        default="user_data/static_filter_result.json",
        help="输出 JSON 文件路径（默认: user_data/static_filter_result.json）",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="仅显示摘要统计，不打印每个策略的详情",
    )

    args = parser.parse_args()

    # 自动适配从项目根目录运行
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    strategies_dir = args.strategies_dir
    registry_path = args.registry
    output_path = args.output

    # 如果是相对路径，基于项目根目录解析
    if not os.path.isabs(strategies_dir):
        strategies_dir = os.path.join(project_root, strategies_dir)
    if not os.path.isabs(registry_path):
        registry_path = os.path.join(project_root, registry_path)
    if not os.path.isabs(output_path):
        output_path = os.path.join(project_root, output_path)

    if not os.path.exists(strategies_dir):
        print(f"❌ 错误: 策略目录不存在: {strategies_dir}")
        return

    run_filter(
        strategies_dir=strategies_dir,
        registry_path=registry_path,
        output_path=output_path,
        summary_only=args.summary_only,
    )


if __name__ == "__main__":
    main()
