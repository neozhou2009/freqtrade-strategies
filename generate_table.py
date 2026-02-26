import os

def classify_strategy(name):
    lower_name = name.lower()
    
    # 1. Ichimoku
    if 'ichi' in lower_name or 'obelisk' in lower_name:
        return ("一目均衡表 (Ichimoku)", "趋势延续/震荡突破", "适合单边趋势或从云层突破后的行情", "云图、基准线、转换线", "利用云层厚度及延迟线位置判断市场强弱")
    
    # 2. NFI / Hybrid Complex
    if 'nfi' in lower_name or 'nostalgia' in lower_name or 'nasos' in lower_name or 'bigz' in lower_name or 'combined' in lower_name:
        return ("复合优化 (Hybrid/Complex)", "全天候 (All-Weather)", "适合各种市场环境，通过多重过滤降低回撤", "多维过滤、深度参数优化", "集成趋势、回归、动量等10+种子逻辑的分支判断")
    
    # 3. Mean Reversion / BB / RSI
    if 'bb' in lower_name or 'rsi' in lower_name or 'bollinger' in lower_name or 'band' in lower_name:
        return ("均线回归 (Mean Reversion)", "震荡市场 (Ranging)", "在市场没有明显趋势，价格在区间内波动时表现最佳", "布林带、RSI指标", "利用价格回归均值的统计原理，逢低买入逢高卖出")
    
    # 4. Trend Following / EMA / SMA
    if 'trend' in lower_name or 'ema' in lower_name or 'sma' in lower_name or 'adx' in lower_name or 'cross' in lower_name or 'mac' in lower_name:
        return ("趋势跟踪 (Trend Following)", "强牛市/强熊市 (Trend)", "在有明显方向的单边行情中捕获利润", "均线交叉、ADX强度、SuperTrend", "通过长短周期的价格均线确认方向，金叉买入死叉卖出")
    
    # 5. Scalping / Fast / Quick
    if 'scalp' in lower_name or 'fast' in lower_name or 'quick' in lower_name or 'yolo' in lower_name or 'lambo' in lower_name:
        return ("剥头皮 (Scalping)", "高波动 (High Volatility)", "在极短时间内博取微小点位差，适合波动剧烈的行情", "低ROI、紧止损、TEMA", "利用1m/5m的高频信号进行快速进出，减少持仓时间风险")
    
    # 6. Breakout
    if 'break' in lower_name or 'high' in lower_name or 'swing' in lower_name:
        return ("突破交易 (Breakout)", "突破行情 (Breakout)", "适合在关键阻力位/压力位被冲破后的瞬间入场", "最高/最低价、波动率突破", "监测特定周期内的阻力线，放量站上阻力线时进场")
    
    # 7. ML / Stat / Dynamic
    if 'uzichan' in lower_name or 'normalizer' in lower_name or 'adaptive' in lower_name or 'informative' in lower_name:
        return ("机器学习/统计增强 (ML/Stat)", "复杂多变市场", "适合市场节奏变换较快的情况，动态调整参数", "归一化处理、动态参数", "根据当前波动率或市场状态动态修正买卖阈值和止损位")

    # 8. Volatility / Dip Buying (Clucas/BinH)
    if 'cluc' in lower_name or 'binh' in lower_name or 'mad' in lower_name:
        return ("抄底/波动 (Dip Buying)", "暴跌/插针 (Flash Crash)", "在市场极速探底或出现异常插针时捕捉反弹", "Clucas算法、BinH算法", "通过分析蜡烛图成交量与价格偏离度，在恐慌性抛售点买入")

    # Default
    return ("多指标综合 (General)", "标准环境", "适合一般震荡偏上行市场", "多指标组合", "基于常规技术指标组合生成的买卖信号")

input_file = "/home/neozh/freqtrade-strategies/all_strategies.txt"
output_file = "/home/neozh/freqtrade-strategies/docs/465_strategies_full_table.md"

with open(input_file, 'r') as f:
    strategies = [line.strip() for line in f if line.strip()]

header = """# Freqtrade 465 策略详细分类与应用时机全表

| # | 策略名称 (Strategy Name) | 分类 (Category) | 应用时机 (Market Context) | 核心特征 (Core Features) | 策略核心机制 (Mechanism) |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""

with open(output_file, 'w') as out:
    out.write(header)
    for i, name in enumerate(sorted(strategies), 1):
        cat, context, desc, features, mechanism = classify_strategy(name)
        line = f"| {i} | `{name}` | {cat} | {context} | {features} | {desc}。{mechanism} |\n"
        out.write(line)

print(f"File generated: {output_file}")
