import os
import re
import glob

def sanitize_md_cell(value):
    text = str(value)
    text = text.replace("\n", " ")
    text = text.replace("|", "\\|")
    return text

def detect_indicators(content):
    patterns = [
        ("RSI", [r"\bta\.RSI\b", r"\bqtpylib\.rsi\b", r"\brsi\b"]),
        ("MACD", [r"\bta\.MACD\b", r"\bMACD\b"]),
        ("EMA", [r"\bta\.EMA\b", r"\bEMA\b"]),
        ("SMA", [r"\bta\.SMA\b", r"\bSMA\b"]),
        ("BBANDS", [r"\bta\.BBANDS\b", r"\bbollinger\b", r"\bbbands\b"]),
        ("ADX", [r"\bta\.ADX\b", r"\bADX\b"]),
        ("ATR", [r"\bta\.ATR\b", r"\bATR\b"]),
        ("MFI", [r"\bta\.MFI\b", r"\bMFI\b"]),
        ("STOCH", [r"\bta\.STOCH\b", r"\bStoch\b", r"\bstoch\b"]),
        ("ICHIMOKU", [r"\bIchimoku\b", r"\bichimoku\b"]),
        ("VWAP", [r"\bVWAP\b", r"\bvwap\b"]),
        ("ROC", [r"\bta\.ROC\b", r"\bROCR\b", r"\broc\b"]),
        ("CCI", [r"\bta\.CCI\b", r"\bCCI\b"]),
    ]
    lowered = content.lower()
    found = []
    for name, pats in patterns:
        matched = False
        for pat in pats:
            if re.search(pat, content, flags=re.IGNORECASE):
                matched = True
                break
        if matched:
            found.append(name)
    if "sklearn" in content or "tensorflow" in lowered or "torch" in lowered:
        found.append("ML")
    if "pywt" in content:
        found.append("WAVELET")
    return found

def detect_qtpylib_import(content):
    if re.search(r"from\s+technical\s+import\s+qtpylib", content):
        return "technical.qtpylib"
    if re.search(r"freqtrade\.vendor\.qtpylib", content):
        return "freqtrade.vendor.qtpylib"
    if re.search(r"\bqtpylib\b", content):
        return "qtpylib"
    return ""

def detect_interface_version(content):
    m = re.search(r"INTERFACE_VERSION\s*=\s*(\d+)", content)
    return int(m.group(1)) if m else None

def detect_method_style(content):
    has_buy = bool(re.search(r"^\s*def\s+populate_buy_trend\s*\(", content, flags=re.MULTILINE))
    has_sell = bool(re.search(r"^\s*def\s+populate_sell_trend\s*\(", content, flags=re.MULTILINE))
    has_entry = bool(re.search(r"^\s*def\s+populate_entry_trend\s*\(", content, flags=re.MULTILINE))
    has_exit = bool(re.search(r"^\s*def\s+populate_exit_trend\s*\(", content, flags=re.MULTILINE))
    return {
        "HasBuy": has_buy,
        "HasSell": has_sell,
        "HasEntry": has_entry,
        "HasExit": has_exit,
    }

def detect_style_markers(content):
    markers = []
    head = "\n".join(content.splitlines()[:40])
    if "flake8: noqa" in head or "noqa" in head:
        markers.append("noqa")
    if "isort: skip_file" in head:
        markers.append("isort-skip")
    if "pragma pylint" in head or "pylint: disable" in head:
        markers.append("pylint-disable")
    return markers

def compute_readability(loc, dataframe_assignments, style_markers, has_docstring, has_typing):
    score = 0
    if loc <= 120:
        score += 2
    elif loc <= 260:
        score += 1
    if dataframe_assignments <= 40:
        score += 1
    if has_docstring:
        score += 1
    if has_typing:
        score += 1
    if style_markers:
        score -= 1
    if score >= 4:
        return "高"
    if score >= 2:
        return "中"
    return "低"

def classify_style(loc, style_markers, has_ml, uses_informative, has_custom_stoploss):
    if has_ml:
        return "实验性/研究型"
    if uses_informative:
        return "工程化/多周期"
    if style_markers and loc > 250:
        return "模板化/堆叠型"
    if has_custom_stoploss:
        return "风控导向"
    return "常规"

def build_review_text(s):
    libs = []
    if s.get("UsesTalib"):
        libs.append("TA-Lib(ta)")
    if s.get("UsesPandasTA"):
        libs.append("pandas_ta")
    if s.get("QtpylibImport"):
        libs.append(s["QtpylibImport"])
    if not libs:
        libs.append("未明确识别指标库")

    indicator_text = "、".join(s.get("IndicatorList", [])[:8]) if s.get("IndicatorList") else "未识别/较少"
    if s.get("IndicatorCount", 0) > 8:
        indicator_text += "…"

    iface = s.get("InterfaceVersion")
    iface_text = f"V{iface}" if iface is not None else "未知"

    method_style = "entry/exit" if (s.get("HasEntry") or s.get("HasExit")) else "buy/sell"
    readability = s.get("Readability", "中")
    style_tag = s.get("StyleTag", "常规")

    issues = []
    if s.get("InterfaceMismatch"):
        issues.append("接口版本与方法命名可能不匹配（升级/运行风险）")
    if s.get("QtpylibImport") == "freqtrade.vendor.qtpylib":
        issues.append("依赖 vendor qtpylib 路径（未来版本兼容风险）")
    if s.get("UsesInformative"):
        issues.append("使用多周期合并（需关注对齐与前视偏差）")
    if s.get("Stoploss") < -0.2 and s.get("Stoploss") != -0.99:
        issues.append("止损较大（回撤风险偏高）")
    if s.get("Stoploss") == -0.99 and not s.get("CustomExit") == "✅":
        issues.append("疑似虚假止损但未发现自定义止损逻辑")
    if s.get("StyleMarkers"):
        issues.append("存在 lint/格式化禁用标记（可能隐藏无用代码）")

    issue_text = "；".join(issues) if issues else "未发现明显结构性风险"

    summary = (
        f"概览：接口{iface_text}，方法风格 {method_style}，主要指标 {indicator_text}，指标库 {', '.join(libs)}。"
        f" 可读性：{readability}；风格：{style_tag}。风险点：{issue_text}。"
    )
    return summary

def build_suggestions(s):
    suggestions = []
    if s.get("InterfaceMismatch"):
        suggestions.append("建议统一接口版本与方法命名（V2: buy/sell；V3: entry/exit）")
    if not s.get("HasProtections"):
        suggestions.append("建议补充保护机制(Protections)，如 cooldown/stoploss guard")
    if not s.get("HasTrailingStop"):
        suggestions.append("建议评估开启移动止损，用于锁定利润")
    if s.get("Stoploss") < -0.1 and s.get("Stoploss") != -0.99:
        suggestions.append("止损偏大，建议收紧或配合动态止损/保护机制")
    if not s.get("UseExitSignal"):
        suggestions.append("建议启用主动离场信号或补充退出条件")
    if s.get("LOC", 0) < 60:
        suggestions.append("逻辑较简单，建议增加趋势过滤/成交量过滤以减少噪声")
    if s.get("IndicatorCount", 0) < 2:
        suggestions.append("指标较少，建议增加二次确认（趋势+动量或波动率）")
    if s.get("UsesTalib") and s.get("UsesPandasTA"):
        suggestions.append("同时混用 ta 与 pandas_ta，建议统一以减少重复计算与列名冲突")
    if s.get("QtpylibImport") == "freqtrade.vendor.qtpylib":
        suggestions.append("建议替换 vendor qtpylib 路径为官方/推荐导入方式以提升兼容性")
    if s.get("UsesInformative"):
        suggestions.append("多周期策略建议校验 timeframe 对齐、列名前缀与 startup_candle_count")
    if s.get("StyleMarkers"):
        suggestions.append("建议移除不必要的 noqa/isort/pylint disable，并删除无用 import/死代码")
    if not suggestions:
        suggestions.append("暂无明显改进建议，可先做参数清理与回测验证")
    return suggestions[:6]

def write_code_review_md(strategies, successful_set, output_path, current_dir):
    interface_counts = {}
    lib_counts = {"TA-Lib": 0, "pandas_ta": 0, "qtpylib": 0}
    indicator_counts = {}
    style_counts = {}
    readability_counts = {}
    risk_counts = {"接口不匹配": 0, "vendor qtpylib": 0, "多周期": 0, "lint禁用": 0}

    for s in strategies:
        iface = s.get("InterfaceVersion")
        interface_counts[iface] = interface_counts.get(iface, 0) + 1
        if s.get("UsesTalib"):
            lib_counts["TA-Lib"] += 1
        if s.get("UsesPandasTA"):
            lib_counts["pandas_ta"] += 1
        if s.get("QtpylibImport"):
            lib_counts["qtpylib"] += 1
        for ind in s.get("IndicatorList", []):
            indicator_counts[ind] = indicator_counts.get(ind, 0) + 1
        style_tag = s.get("StyleTag", "常规")
        style_counts[style_tag] = style_counts.get(style_tag, 0) + 1
        readability = s.get("Readability", "中")
        readability_counts[readability] = readability_counts.get(readability, 0) + 1
        if s.get("InterfaceMismatch"):
            risk_counts["接口不匹配"] += 1
        if s.get("QtpylibImport") == "freqtrade.vendor.qtpylib":
            risk_counts["vendor qtpylib"] += 1
        if s.get("UsesInformative"):
            risk_counts["多周期"] += 1
        if s.get("StyleMarkers"):
            risk_counts["lint禁用"] += 1

    def rel_link(path, display_name):
        try:
            rel_path = os.path.relpath(path, start=current_dir).replace("\\", "/")
            return f"[{display_name}]({rel_path})"
        except ValueError:
            return f"[{display_name}](file://{path})"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 策略源码评审报告 (Code Review Report)\n\n")
        f.write("评审模型：静态规则评审 v2（基于源码特征提取与启发式规则生成）。\n\n")
        f.write(f"**总计分析策略数量:** {len(strategies)}\n\n")
        f.write("## 总览\n\n")
        f.write(f"- **重点关注策略(已通过回测):** {len(successful_set)}\n")
        f.write(f"- **接口版本分布:** {sanitize_md_cell(interface_counts)}\n")
        f.write(f"- **指标库使用分布:** {sanitize_md_cell(lib_counts)}\n")
        top_inds = sorted(indicator_counts.items(), key=lambda x: x[1], reverse=True)[:12]
        f.write(f"- **常见指标 Top12:** {sanitize_md_cell(top_inds)}\n")
        f.write(f"- **可读性分布(高/中/低):** {sanitize_md_cell(readability_counts)}\n")
        f.write(f"- **风格分布:** {sanitize_md_cell(style_counts)}\n")
        f.write(f"- **主要风险计数:** {sanitize_md_cell(risk_counts)}\n\n")

        f.write("## 重点策略评审\n\n")
        for s in strategies:
            if not s.get("IsSuccessful"):
                continue
            title = s["File"]
            f.write(f"### {sanitize_md_cell(title)}\n\n")
            f.write(f"- 文件：{rel_link(s['Path'], s['File'])}\n")
            f.write(f"- 周期：{sanitize_md_cell(s['Timeframe'])}；止损：{sanitize_md_cell(s['Stoploss'])}；评分：{sanitize_md_cell(s['Score'])}\n")
            f.write(f"- 评审结论：{sanitize_md_cell(s.get('ReviewText', ''))}\n")
            f.write("- 建议：\n")
            for item in s.get("SuggestionList", []):
                f.write(f"  - {sanitize_md_cell(item)}\n")
            f.write("\n")

        f.write("## 其它策略摘要\n\n")
        f.write("| 序号 | 策略名称 | 周期 | 止损 | 评分 | 可读性 | 风格 | 一句话评审 |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        idx = 0
        for s in strategies:
            if s.get("IsSuccessful"):
                continue
            idx += 1
            filename = s["File"]
            display_name = filename[:17] + "..." if len(filename) > 20 else filename
            name_link = rel_link(s["Path"], display_name)
            one_liner = s.get("ReviewText", "")
            if len(one_liner) > 70:
                one_liner = one_liner[:67] + "..."
            f.write(
                f"| {idx} | {sanitize_md_cell(name_link)} | {sanitize_md_cell(s['Timeframe'])} | {sanitize_md_cell(s['Stoploss'])} | "
                f"{sanitize_md_cell(s['Score'])} | {sanitize_md_cell(s.get('Readability'))} | {sanitize_md_cell(s.get('StyleTag'))} | "
                f"{sanitize_md_cell(one_liner)} |\n"
            )

def choose_non_overwrite_path(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    i = 2
    while True:
        candidate = f"{base}_v{i}{ext}"
        if not os.path.exists(candidate):
            return candidate
        i += 1

def infer_design_idea(timeframe, indicator_list, uses_informative, has_trailing_stop, has_custom_stoploss, has_protections):
    inds = set(indicator_list or [])

    archetypes = []
    if "ICHIMOKU" in inds:
        archetypes.append("一目均衡的趋势识别")
    if "BBANDS" in inds and "RSI" in inds:
        archetypes.append("布林带+RSI 的均值回归/超买超卖")
    elif "BBANDS" in inds:
        archetypes.append("通道类策略（布林带/Keltner 等）")
    if ("MACD" in inds) or (("EMA" in inds or "SMA" in inds) and ("ADX" in inds or "ROC" in inds)):
        archetypes.append("动量/均线趋势跟随")
    if "ADX" in inds:
        archetypes.append("趋势强度过滤")
    if "VWAP" in inds:
        archetypes.append("围绕 VWAP 的回归/基准定价")
    if "ROC" in inds and "BBANDS" not in inds:
        archetypes.append("动量突破")
    if "ML" in inds:
        archetypes.append("机器学习/特征工程驱动")

    if not archetypes:
        if has_trailing_stop:
            archetypes.append("趋势持有 + 移动止损跟踪")
        else:
            archetypes.append("基于阈值条件的规则策略")

    add_ons = []
    if uses_informative:
        add_ons.append("多周期确认")
    if has_custom_stoploss:
        add_ons.append("动态风控（自定义止损）")
    if has_protections:
        add_ons.append("保护机制防极端行情")

    archetype_text = "；".join(archetypes[:2])
    if add_ons:
        archetype_text += "；" + "；".join(add_ons[:2])

    short = archetype_text
    if len(short) > 80:
        short = short[:77] + "..."

    indicator_text = "、".join(indicator_list[:6]) if indicator_list else "较少"
    if indicator_list and len(indicator_list) > 6:
        indicator_text += "…"

    long_parts = []
    long_parts.append(f"核心思路：以 {indicator_text} 作为主要信号与过滤条件，整体偏向 {archetypes[0]}。")
    if uses_informative:
        long_parts.append("结构特点：包含多周期信息合并，用高周期趋势/波动过滤低周期噪声，强调信号一致性。")
    if has_trailing_stop:
        long_parts.append("持仓管理：使用移动止损倾向于让利润奔跑并控制回撤。")
    if has_custom_stoploss:
        long_parts.append("风控设计：通过自定义止损实现更精细的风险分层与行情自适应。")
    if has_protections:
        long_parts.append("鲁棒性：具备保护机制，用于减少连续亏损或异常波动下的过度交易。")

    long_text = " ".join(long_parts)
    return short, long_text

def write_design_report_md(strategies, successful_set, output_path, current_dir):
    def rel_link(path, display_name):
        try:
            rel_path = os.path.relpath(path, start=current_dir).replace("\\", "/")
            return f"[{display_name}]({rel_path})"
        except ValueError:
            return f"[{display_name}](file://{path})"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 策略设计思想与评审报告\n\n")
        f.write("说明：本报告为静态源码分析推断（不执行策略），以“代码评审”口吻给出设计思想与建议。\n\n")
        f.write(f"**总计分析策略数量:** {len(strategies)}\n")
        f.write(f"**重点关注策略(已通过回测):** {len(successful_set)}\n\n")

        f.write("## 总表（含设计思想列）\n\n")
        f.write("| 序号 | 策略名称 | 周期 | 评分 | 可读性 | 风格 | 设计思想(摘要) | 评审概要 | 改进建议 |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for i, s in enumerate(strategies, 1):
            filename = s["File"]
            display_name = filename[:17] + "..." if len(filename) > 20 else filename
            name_link = rel_link(s["Path"], display_name)
            f.write(
                f"| {i} | {sanitize_md_cell(name_link)} | {sanitize_md_cell(s['Timeframe'])} | {sanitize_md_cell(s['Score'])} | "
                f"{sanitize_md_cell(s.get('Readability'))} | {sanitize_md_cell(s.get('StyleTag'))} | "
                f"{sanitize_md_cell(s.get('DesignIdeaShort', ''))} | {sanitize_md_cell(s.get('ReviewSummary', ''))} | {sanitize_md_cell(s.get('Suggestions', ''))} |\n"
            )

        f.write("\n## 重点策略：设计思想详述\n\n")
        for s in strategies:
            if not s.get("IsSuccessful"):
                continue
            f.write(f"### {sanitize_md_cell(s['File'])}\n\n")
            f.write(f"- 文件：{rel_link(s['Path'], s['File'])}\n")
            f.write(f"- 周期：{sanitize_md_cell(s['Timeframe'])}；止损：{sanitize_md_cell(s['Stoploss'])}；评分：{sanitize_md_cell(s['Score'])}\n")
            f.write(f"- 设计思想：{sanitize_md_cell(s.get('DesignIdeaLong', s.get('DesignIdeaShort', '')))}\n")
            f.write(f"- 评审意见：{sanitize_md_cell(s.get('ReviewText', ''))}\n")
            f.write("- 改进建议：\n")
            for item in s.get("SuggestionList", []):
                f.write(f"  - {sanitize_md_cell(item)}\n")
            f.write("\n")

def analyze_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Extract Class Name
    class_match = re.search(r'class\s+(\w+)\s*\((?:IStrategy|IExtendedStrategy)\):', content)
    if not class_match:
        return None
    
    strategy_name = class_match.group(1)
    
    # Extract Stoploss
    stoploss_match = re.search(r'stoploss\s*=\s*(-?[\d\.]+)', content)
    stoploss = float(stoploss_match.group(1)) if stoploss_match else -0.05 # Default assumption
    
    # Extract Timeframe
    timeframe_match = re.search(r'timeframe\s*=\s*[\'"]([^\'"]+)[\'"]', content)
    timeframe = timeframe_match.group(1) if timeframe_match else "Unknown"
    
    # Check Features
    has_protections = "protections" in content and "@property" in content
    has_custom_stoploss = "def custom_stoploss" in content
    has_trailing_stop = bool(re.search(r"trailing_stop\s*=\s*True", content))
    
    # Exit Signal
    # Check for use_exit_signal = True or use_sell_signal = True
    use_exit_signal = True
    if re.search(r'use_exit_signal\s*=\s*False', content) or re.search(r'use_sell_signal\s*=\s*False', content):
        use_exit_signal = False
        
    indicator_list = detect_indicators(content)
    indicators = ", ".join(indicator_list[:4]) + ("..." if len(indicator_list) > 4 else "")
    indicator_count = len(indicator_list)
    uses_talib = bool(re.search(r"talib\.abstract\s+as\s+ta", content))
    uses_pandas_ta = bool(re.search(r"\bpandas_ta\s+as\s+", content))
    qtpylib_import = detect_qtpylib_import(content)
    interface_version = detect_interface_version(content)
    method_flags = detect_method_style(content)
    style_markers = detect_style_markers(content)
    uses_informative = ("def informative_pairs" in content) or ("merge_informative_pair" in content) or ("@informative" in content)
    dataframe_assignments = len(re.findall(r"dataframe\[['\"]", content))
    has_typing = ("from typing" in content) or bool(re.search(r"def\s+\w+\(.*\)\s*->\s*\w+", content))
    has_docstring = bool(re.search(r'^\s*("""|\'\'\')', content, flags=re.MULTILINE))
    readability = compute_readability(len(content.splitlines()), dataframe_assignments, style_markers, has_docstring, has_typing)
    style_tag = classify_style(len(content.splitlines()), style_markers, "ML" in indicator_list, uses_informative, has_custom_stoploss)
    iface_mismatch = False
    if interface_version == 2 and (method_flags["HasEntry"] or method_flags["HasExit"]):
        iface_mismatch = True
    if interface_version == 3 and (method_flags["HasBuy"] or method_flags["HasSell"]):
        iface_mismatch = True
    
    # Lines of Code
    loc = len(content.splitlines())
    
    # Scoring
    score = 5.0
    if has_protections: score += 1.5
    if has_custom_stoploss: score += 1.5
    if has_trailing_stop: score += 0.5
    if not use_exit_signal: score -= 2.0
    if "ML" in indicator_list: score += 1.0 # Bonus for tech, but risk involved
    if stoploss < -0.2 and stoploss != -0.99: score -= 1.0 # Very loose stoploss (ignoring dummy -0.99)
    if loc < 50: score -= 2.0 # Too simple?
    
    # Cap score
    score = min(10.0, max(0.0, score))

    design_short, design_long = infer_design_idea(
        timeframe,
        indicator_list,
        uses_informative,
        has_trailing_stop,
        has_custom_stoploss,
        has_protections,
    )
    
    return {
        "Name": strategy_name,
        "File": os.path.basename(filepath),
        "Timeframe": timeframe,
        "Stoploss": stoploss,
        "HasProtections": has_protections,
        "Protections": "✅" if has_protections else "❌",
        "HasTrailingStop": has_trailing_stop,
        "HasCustomStoploss": has_custom_stoploss,
        "CustomExit": "✅" if has_custom_stoploss else "❌",
        "UseExitSignal": use_exit_signal,
        "ExitSignal": "✅" if use_exit_signal else "⚠️ No",
        "Indicators": indicators,
        "IndicatorList": indicator_list,
        "IndicatorCount": indicator_count,
        "UsesTalib": uses_talib,
        "UsesPandasTA": uses_pandas_ta,
        "QtpylibImport": qtpylib_import,
        "InterfaceVersion": interface_version,
        "InterfaceMismatch": iface_mismatch,
        "UsesInformative": uses_informative,
        "StyleMarkers": style_markers,
        "Readability": readability,
        "StyleTag": style_tag,
        "HasBuy": method_flags["HasBuy"],
        "HasSell": method_flags["HasSell"],
        "HasEntry": method_flags["HasEntry"],
        "HasExit": method_flags["HasExit"],
        "LOC": loc,
        "Score": round(score, 1),
        "DesignIdeaShort": design_short,
        "DesignIdeaLong": design_long,
        "Path": filepath
    }

def main():
    base_dirs = [
        "/root/test_strategy/freqtrade-test/freqtrade-strategies/strategies",
        "/root/test_strategy/freqtrade-test/user_data/strategies"
    ]
    
    all_strategies = []
    
    # Load successful strategies
    successful_set = set()
    try:
        with open("successful_strategies.txt", "r", encoding="utf-8") as f:
            successful_set = {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        print("successful_strategies.txt not found.")

    for base_dir in base_dirs:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    filepath = os.path.join(root, file)
                    result = analyze_file(filepath)
                    if result:
                        summary_parts = []
                        is_successful = result["Name"] in successful_set
                        
                        if is_successful:
                            summary_parts.append("✅ **重点(已通过回测)**")
                        
                        if result["Score"] >= 8.0:
                            summary_parts.append("评分优秀")
                        elif result["Score"] >= 6.0:
                            summary_parts.append("评分良好")
                        else:
                            summary_parts.append("评分一般")
                            
                        if result["Stoploss"] < -0.1 and result["Stoploss"] != -0.99:
                            summary_parts.append("高风险")
                        elif result["Stoploss"] > -0.05:
                            summary_parts.append("低风险")
                            
                        if result["LOC"] > 300:
                            summary_parts.append("逻辑复杂")
                        elif result["LOC"] < 100:
                            summary_parts.append("逻辑简单")

                        if result.get("InterfaceMismatch"):
                            summary_parts.append("接口不匹配")
                        if result.get("UsesInformative"):
                            summary_parts.append("多周期")
                        if result.get("StyleMarkers"):
                            summary_parts.append("lint禁用")

                        result["ReviewSummary"] = "；".join(summary_parts)
                        result["IsSuccessful"] = is_successful
                        result["ReviewText"] = build_review_text(result)
                        result["SuggestionList"] = build_suggestions(result)
                        result["Suggestions"] = "；".join(result["SuggestionList"])
                        all_strategies.append(result)
                        
    # Sort by Successful first, then by Score Descending
    all_strategies.sort(key=lambda x: (not x["IsSuccessful"], -x["Score"]))

    current_dir = os.getcwd()

    analysis_path = "all_strategies_analysis.md"
    if not os.path.exists(analysis_path):
        with open(analysis_path, "w", encoding="utf-8") as f:
            f.write("# 全策略分析报告 (All Strategies Analysis Report)\n\n")
            f.write(f"**总计分析策略数量:** {len(all_strategies)}\n")
            f.write(f"**重点关注策略:** {len(successful_set)}\n\n")
            f.write("| 序号 | 策略名称 | 周期 | 止损 | 保护机制 | 动态止损 | 主动离场 | 代码行数 | 评分 | 评审概要 | 改进建议 |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
            for i, s in enumerate(all_strategies, 1):
                filename = s["File"]
                display_name = filename[:17] + "..." if len(filename) > 20 else filename
                try:
                    rel_path = os.path.relpath(s["Path"], start=current_dir).replace("\\", "/")
                    name_link = f"[{display_name}]({rel_path})"
                except ValueError:
                    name_link = f"[{display_name}](file://{s['Path']})"
                f.write(
                    f"| {i} | {sanitize_md_cell(name_link)} | {sanitize_md_cell(s['Timeframe'])} | {sanitize_md_cell(s['Stoploss'])} | "
                    f"{sanitize_md_cell(s['Protections'])} | {sanitize_md_cell(s['CustomExit'])} | {sanitize_md_cell(s['ExitSignal'])} | "
                    f"{sanitize_md_cell(s['LOC'])} | {sanitize_md_cell(s['Score'])} | {sanitize_md_cell(s['ReviewSummary'])} | {sanitize_md_cell(s['Suggestions'])} |\n"
                )

    code_review_path = "all_strategies_code_review.md"
    if not os.path.exists(code_review_path):
        write_code_review_md(all_strategies, successful_set, code_review_path, current_dir)

    design_report_path = choose_non_overwrite_path("all_strategies_design_ideas_review.md")
    write_design_report_md(all_strategies, successful_set, design_report_path, current_dir)
    print(f"Design ideas report saved to {design_report_path}")

if __name__ == "__main__":
    main()
