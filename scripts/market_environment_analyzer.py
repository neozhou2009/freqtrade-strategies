#!/usr/bin/env python3
"""
Market Environment Analyzer

Analyzes current market state using multiple authoritative methods:
1. ADX + DI (Wilder 1978) - Trend strength and direction
2. EMA200 - Classic long-term trend
3. Multi-EMA alignment - Classic trend confirmation
4. Relative Price Position - Price relative to recent range
5. BTC Informative - Market-wide sentiment

Usage:
    python scripts/market_environment_analyzer.py
"""

import pandas as pd
import talib.abstract as ta
import json
from pathlib import Path
from datetime import datetime


def load_btc_data(timeframe: str = "1h") -> pd.DataFrame:
    """Load BTC/USDT data from feather file."""
    data_path = Path(__file__).parent.parent / "user_data" / "data" / "binance" / f"BTC_USDT-{timeframe}.feather"
    df = pd.read_feather(data_path)
    return df


def analyze_adx_di(df: pd.DataFrame, period: int = 14) -> dict:
    """Method 3: ADX + DI Analysis (Wilder 1978 - Most authoritative)."""
    adx = ta.ADX(df, timeperiod=period)
    plus_di = ta.PLUS_DI(df, timeperiod=period)
    minus_di = ta.MINUS_DI(df, timeperiod=period)

    latest_adx = adx.iloc[-1]
    latest_plus_di = plus_di.iloc[-1]
    latest_minus_di = minus_di.iloc[-1]

    # Interpretation
    trend_strength = ""
    if latest_adx > 50:
        trend_strength = "极强趋势"
    elif latest_adx > 25:
        trend_strength = "有趋势"
    elif latest_adx > 20:
        trend_strength = "趋势萌芽"
    else:
        trend_strength = "无趋势/震荡"

    direction = "多头" if latest_plus_di > latest_minus_di else "空头"

    # Market state
    if latest_adx > 25 and latest_plus_di > latest_minus_di:
        market_state = "牛市（有趋势+多头方向）"
    elif latest_adx > 25 and latest_minus_di > latest_plus_di:
        market_state = "熊市（有趋势+空头方向）"
    else:
        market_state = "震荡市（无明确趋势）"

    return {
        "adx": latest_adx,
        "plus_di": latest_plus_di,
        "minus_di": latest_minus_di,
        "trend_strength": trend_strength,
        "direction": direction,
        "market_state": market_state,
    }


def analyze_ema200(df: pd.DataFrame) -> dict:
    """Method 5: EMA200 Trend (Classic method)."""
    ema200 = ta.EMA(df, timeperiod=200)
    ema50 = ta.EMA(df, timeperiod=50)
    ema20 = ta.EMA(df, timeperiod=20)

    latest_close = df['close'].iloc[-1]
    latest_ema200 = ema200.iloc[-1]
    latest_ema50 = ema50.iloc[-1]
    latest_ema20 = ema20.iloc[-1]

    # Price vs EMA200
    price_above_ema200 = latest_close > latest_ema200
    distance_from_ema200 = (latest_close - latest_ema200) / latest_ema200 * 100

    # Multi-EMA alignment
    perfect_bull = (latest_ema20 > latest_ema50) and (latest_ema50 > latest_ema200)
    perfect_bear = (latest_ema20 < latest_ema50) and (latest_ema50 < latest_ema200)

    if perfect_bull:
        alignment = "完美牛市排列 (EMA20 > EMA50 > EMA200)"
    elif perfect_bear:
        alignment = "完美熊市排列 (EMA20 < EMA50 < EMA200)"
    elif latest_ema20 > latest_ema50:
        alignment = "短期多头 (EMA20 > EMA50)"
    else:
        alignment = "短期空头 (EMA20 < EMA50)"

    return {
        "close": latest_close,
        "ema200": latest_ema200,
        "ema50": latest_ema50,
        "ema20": latest_ema20,
        "price_above_ema200": price_above_ema200,
        "distance_from_ema200_pct": distance_from_ema200,
        "ema_alignment": alignment,
        "market_state": "牛市" if price_above_ema200 else "熊市",
    }


def analyze_relative_price(df: pd.DataFrame, window: int = 60) -> dict:
    """Method 2: Relative Price Position."""
    close_max = df['close'].rolling(window=window).max().iloc[-1]
    close_min = df['close'].rolling(window=window).min().iloc[-1]
    latest_close = df['close'].iloc[-1]

    relative_price = (latest_close - close_min) / (close_max - close_min) if close_max != close_min else 0.5
    dropped_pct = 1 - (latest_close / close_max)
    pumped_pct = (latest_close - close_min) / latest_close

    # Interpretation
    if relative_price > 0.7:
        position = "高位区域（接近近期高点）"
    elif relative_price > 0.5:
        position = "中高位区域"
    elif relative_price > 0.3:
        position = "中低位区域"
    else:
        position = "低位区域（接近近期低点）"

    return {
        "close": latest_close,
        "close_max": close_max,
        "close_min": close_min,
        "relative_price": relative_price,
        "dropped_pct": dropped_pct,
        "pumped_pct": pumped_pct,
        "position": position,
    }


def analyze_price_trend(df: pd.DataFrame, lookback: int = 30) -> dict:
    """Analyze recent price trend."""
    closes = df['close'].iloc[-lookback:]
    start_price = closes.iloc[0]
    end_price = closes.iloc[-1]

    change_pct = (end_price - start_price) / start_price * 100

    if change_pct > 10:
        trend = "强势上涨"
    elif change_pct > 5:
        trend = "温和上涨"
    elif change_pct > 0:
        trend = "小幅上涨"
    elif change_pct > -5:
        trend = "小幅下跌"
    elif change_pct > -10:
        trend = "温和下跌"
    else:
        trend = "强势下跌"

    return {
        "lookback_days": lookback,
        "change_pct": change_pct,
        "trend": trend,
    }


def find_cycle_start(df: pd.DataFrame) -> dict:
    """
    Find current market cycle start point using multiple methods.

    Methods:
    1. EMA200 breakthrough point
    2. 20% drop/rise threshold (Wall Street standard)
    3. Cycle high/low point

    Returns cycle_type, cycle_start_date, days_in_cycle, method_used
    """
    import numpy as np

    # Calculate indicators
    df = df.copy()
    df['ema200'] = ta.EMA(df, timeperiod=200)
    df['above_ema200'] = df['close'] > df['ema200']

    # Method A: Find EMA200 breakthrough point
    # Find where price crossed EMA200
    breakthrough_mask = (df['above_ema200'] != df['above_ema200'].shift(1))
    breakthrough_points = df[breakthrough_mask]

    if len(breakthrough_points) > 0:
        # Get the most recent breakthrough
        latest_breakthrough = breakthrough_points.iloc[-1]
        breakthrough_date = latest_breakthrough['date']
        breakthrough_type = "突破EMA200向上" if latest_breakthrough['above_ema200'] else "跌破EMA200向下"
        breakthrough_price = latest_breakthrough['close']
        days_since_breakthrough = (df['date'].iloc[-1] - breakthrough_date).days
    else:
        breakthrough_date = None
        breakthrough_type = "无突破点"
        days_since_breakthrough = 0

    # Method B: 20% threshold (Wall Street standard)
    # Find cycle high and low in the last 365 days
    window_365 = min(365, len(df))
    recent_high = df['close'].iloc[-window_365:].max()
    recent_low = df['close'].iloc[-window_365:].min()
    current_price = df['close'].iloc[-1]

    # Find when high/low occurred
    high_idx = df['close'].iloc[-window_365:].argmax()
    low_idx = df['close'].iloc[-window_365:].argmin()

    high_date = df['date'].iloc[-window_365 + high_idx]
    low_date = df['date'].iloc[-window_365 + low_idx]

    # Determine if bull or bear cycle based on 20% rule
    from_high_drop_pct = (1 - current_price / recent_high) * 100
    from_low_rise_pct = ((current_price / recent_low) - 1) * 100

    # Wall Street definition: 20% drop from high = bear market, 20% rise from low = bull market
    if from_high_drop_pct >= 20:
        cycle_type_20pct = "熊市"
        cycle_start_20pct = high_date
        cycle_threshold = f"从高点${recent_high:,.0f}下跌{from_high_drop_pct:.1f}% (>=20%)"
    elif from_low_rise_pct >= 20:
        cycle_type_20pct = "牛市"
        cycle_start_20pct = low_date
        cycle_threshold = f"从低点${recent_low:,.0f}上涨{from_low_rise_pct:.1f}% (>=20%)"
    else:
        # Not meeting 20% threshold, use most recent significant point
        if from_low_rise_pct > from_high_drop_pct:
            cycle_type_20pct = "偏多震荡"
            cycle_start_20pct = low_date
            cycle_threshold = f"从低点涨{from_low_rise_pct:.1f}% (<20%，未达牛市标准)"
        else:
            cycle_type_20pct = "偏空震荡"
            cycle_start_20pct = high_date
            cycle_threshold = f"从高点跌{from_high_drop_pct:.1f}% (<20%，未达熊市标准)"

    days_in_cycle_20pct = (df['date'].iloc[-1] - cycle_start_20pct).days

    # Method C: Cycle high/low point
    if high_date > low_date:
        # High occurred after low -> we're in potential bear cycle from high
        cycle_type_highlow = "潜在熊市周期"
        cycle_start_highlow = high_date
    else:
        # Low occurred after high -> we're in bull cycle from low
        cycle_type_highlow = "牛市周期"
        cycle_start_highlow = low_date

    days_in_cycle_highlow = (df['date'].iloc[-1] - cycle_start_highlow).days

    return {
        # EMA200 breakthrough
        "breakthrough_date": breakthrough_date,
        "breakthrough_type": breakthrough_type,
        "breakthrough_price": breakthrough_price if breakthrough_date else None,
        "days_since_breakthrough": days_since_breakthrough,

        # 20% threshold
        "cycle_type_20pct": cycle_type_20pct,
        "cycle_start_20pct": cycle_start_20pct,
        "cycle_threshold": cycle_threshold,
        "days_in_cycle_20pct": days_in_cycle_20pct,
        "recent_high": recent_high,
        "recent_low": recent_low,
        "from_high_drop_pct": from_high_drop_pct,
        "from_low_rise_pct": from_low_rise_pct,

        # Cycle high/low
        "cycle_type_highlow": cycle_type_highlow,
        "cycle_start_highlow": cycle_start_highlow,
        "days_in_cycle_highlow": days_in_cycle_highlow,
        "high_date": high_date,
        "low_date": low_date,
    }


def get_market_summary(adx_1h: dict, adx_4h: dict, adx_1d: dict, ema_result: dict, relative_result: dict, trend_result: dict) -> str:
    """Generate overall market summary with proper weight."""

    # Weighted scoring (higher weight for more authoritative methods)
    bullish_score = 0
    bearish_score = 0

    # ADX 4H - Most reliable for current trend (weight 2)
    if adx_4h['adx'] > 25:
        if adx_4h['plus_di'] > adx_4h['minus_di']:
            bullish_score += 2
        else:
            bearish_score += 2

    # ADX 1D - Long-term trend (weight 1)
    if adx_1d['adx'] > 25:
        if adx_1d['plus_di'] > adx_1d['minus_di']:
            bullish_score += 1
        else:
            bearish_score += 1
    else:
        # No trend = neutral, but check direction
        if adx_1d['plus_di'] > adx_1d['minus_di']:
            bullish_score += 0.5
        else:
            bearish_score += 0.5

    # EMA200 position (weight 2) - Classic method
    if ema_result['price_above_ema200']:
        bullish_score += 2
    else:
        bearish_score += 2

    # EMA alignment (weight 1)
    if '完美牛市' in ema_result['ema_alignment']:
        bullish_score += 1
    elif '完美熊市' in ema_result['ema_alignment']:
        bearish_score += 1

    # Relative price position
    if relative_result['relative_price'] > 0.7:
        bullish_score += 1  # At highs = bullish momentum
    elif relative_result['relative_price'] < 0.3:
        bearish_score += 1  # At lows = bearish

    # Generate summary
    total = bullish_score + bearish_score
    bullish_pct = bullish_score / total * 100 if total > 0 else 50

    lines = []
    lines.append(f"多头得分: {bullish_score:.1f}")
    lines.append(f"空头得分: {bearish_score:.1f}")
    lines.append(f"多头占比: {bullish_pct:.1f}%")

    if bullish_score >= 4:
        overall = "🟢 **强势牛市** - 市场明确上涨趋势，适合做多策略"
    elif bullish_score >= 2.5:
        overall = "🟡 **偏多震荡/上涨** - 市场有上涨倾向，可考虑做多"
    elif bearish_score >= 4:
        overall = "🔴 **强势熊市** - 市场明确下跌趋势，谨慎抄底策略"
    elif bearish_score >= 2.5:
        overall = "🟠 **偏空震荡** - 市场有下跌倾向，需谨慎"
    else:
        overall = "⚪ **纯震荡** - 无明确方向，等待趋势形成"

    return overall + "\n" + "\n".join(lines), bullish_score, bearish_score


def load_strategy_registry() -> dict:
    """Load strategy registry from JSON file."""
    registry_path = Path(__file__).parent.parent / "strategy_registry.json"
    with open(registry_path, 'r') as f:
        return json.load(f)


def recommend_strategies(registry: dict, market_state: dict) -> dict:
    """
    Recommend strategies based on current market environment.

    Args:
        registry: Strategy registry dict
        market_state: Dict containing:
            - bullish_score, bearish_score
            - adx_4h_has_trend, adx_4h_direction
            - adx_1d_has_trend, adx_1d_direction
            - price_above_ema200
            - relative_price
            - cycle_type

    Returns:
        Dict with categorized strategy recommendations
    """
    # Determine market environment
    bullish_score = market_state['bullish_score']
    bearish_score = market_state['bearish_score']
    relative_price = market_state['relative_price']
    adx_4h_has_trend = market_state['adx_4h_has_trend']
    adx_4h_direction = market_state['adx_4h_direction']

    # Categorize strategies
    high_priority = []      # Can use immediately
    medium_priority = []    # Can use with caution
    cautious = []           # Wait for pullback
    not_recommended = []    # Avoid

    # Known/popular strategies for prioritization
    known_good = [
        'Nostalgia', 'BinHV45', 'BinHV27', 'NASOSRv6', 'BBRSITV',
        'ActionZone', 'AdxSmas', 'AlligatorStrat', 'AwesomeMacd',
        'BBMod1', 'BBRSI', 'BB_RPB_TSL', 'NFI46Frog', 'NFI4Frog'
    ]

    for name, info in registry.items():
        market = info.get('market', 'Unknown')
        style = info.get('style', [])
        timeframe = info.get('timeframe', '')
        side = info.get('side', 'Long')
        family = info.get('family', '')

        is_known = any(k in name for k in known_good) or family in known_good

        entry = {
            'name': name,
            'market': market,
            'style': style,
            'timeframe': timeframe,
            'side': side,
            'is_known': is_known
        }

        # Skip short-only strategies if market is bullish
        if side == 'Short' and bullish_score >= bearish_score:
            not_recommended.append(entry)
            continue

        # Strategy matching logic
        if bullish_score >= 4:  # Strong bull market
            if market == 'Trending':
                high_priority.append(entry)
            elif market == 'Any':
                medium_priority.append(entry)
            elif market == 'Ranging':
                if relative_price > 0.7:
                    cautious.append(entry)  # Wait for pullback
                else:
                    medium_priority.append(entry)

        elif bullish_score >= 2.5:  # Bullish bias
            if market == 'Trending' and adx_4h_has_trend and adx_4h_direction == 'bull':
                high_priority.append(entry)
            elif market == 'Trending':
                medium_priority.append(entry)
            elif market == 'Any':
                medium_priority.append(entry)
            elif market == 'Ranging':
                if relative_price > 0.7:
                    cautious.append(entry)
                else:
                    medium_priority.append(entry)

        elif bearish_score >= 4:  # Strong bear market
            if market == 'Ranging':
                if relative_price < 0.3:
                    medium_priority.append(entry)  # Near lows
                else:
                    cautious.append(entry)
            elif market == 'Any':
                cautious.append(entry)
            elif market == 'Trending':
                not_recommended.append(entry)

        elif bearish_score >= 2.5:  # Bearish bias
            if market == 'Ranging' and relative_price < 0.5:
                cautious.append(entry)
            elif market == 'Any':
                cautious.append(entry)
            elif market == 'Trending':
                not_recommended.append(entry)

        else:  # Pure ranging/choppy
            if market == 'Ranging':
                high_priority.append(entry)
            elif market == 'Any':
                high_priority.append(entry)
            elif market == 'Trending':
                if not adx_4h_has_trend:
                    cautious.append(entry)
                elif adx_4h_direction == 'bull':
                    medium_priority.append(entry)
                else:
                    not_recommended.append(entry)

    # Sort: known strategies first
    for lst in [high_priority, medium_priority, cautious]:
        lst.sort(key=lambda x: (not x['is_known'], x['name']))

    return {
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'cautious': cautious,
        'not_recommended': not_recommended
    }


def print_strategy_recommendations(recommendations: dict, max_display: int = 15):
    """Print strategy recommendations."""

    print("【策略推荐】")
    print("="*60)

    # High priority
    high = recommendations['high_priority']
    print(f"\n✅ 高优先级 - 可立即使用 ({len(high)}个)")
    print("-"*50)
    known_high = [s for s in high if s['is_known']]
    other_high = [s for s in high if not s['is_known']]

    if known_high:
        print("知名策略:")
        for s in known_high[:max_display]:
            styles = ', '.join(s['style']) if s['style'] else 'N/A'
            print(f"  ★ {s['name']} ({s['timeframe']}, {styles}, {s['market']})")

    if other_high and len(known_high) < max_display:
        remaining = max_display - len(known_high)
        print("其他策略:")
        for s in other_high[:remaining]:
            styles = ', '.join(s['style']) if s['style'] else 'N/A'
            print(f"  - {s['name']} ({s['timeframe']}, {styles})")

    if len(high) > max_display:
        print(f"  ... 还有 {len(high) - max_display} 个策略")

    # Medium priority
    medium = recommendations['medium_priority']
    print(f"\n⚠️ 中优先级 - 可用 ({len(medium)}个)")
    print("-"*50)
    known_medium = [s for s in medium if s['is_known']]
    for s in known_medium[:10]:
        styles = ', '.join(s['style']) if s['style'] else 'N/A'
        print(f"  {s['name']} ({s['timeframe']}, {styles}, {s['market']})")
    if len(medium) > 10:
        print(f"  ... 还有 {len(medium) - 10} 个策略")

    # Cautious
    cautious = recommendations['cautious']
    print(f"\n⚠️ 谨慎使用 - 等回调后入场 ({len(cautious)}个)")
    print("-"*50)
    known_cautious = [s for s in cautious if s['is_known']]
    for s in known_cautious[:10]:
        styles = ', '.join(s['style']) if s['style'] else 'N/A'
        print(f"  {s['name']} ({s['timeframe']}, {styles}) - 等回调")
    if len(cautious) > 10:
        print(f"  ... 还有 {len(cautious) - 10} 个策略")

    # Not recommended
    not_rec = recommendations['not_recommended']
    if not_rec:
        print(f"\n❌ 不推荐 ({len(not_rec)}个)")
        print("-"*50)
        print(f"  主要为空头策略或与当前趋势相反的策略")

    # Summary stats
    print(f"\n【统计汇总】")
    print("-"*50)
    total = len(high) + len(medium) + len(cautious) + len(not_rec)
    print(f"总策略数: {total}")
    print(f"可立即使用: {len(high)} ({len(high)/total*100:.1f}%)")
    print(f"需等回调: {len(cautious)} ({len(cautious)/total*100:.1f}%)")

    # Usage tips based on market state
    print(f"\n【使用建议】")
    print("-"*50)
    if len(high) > 0:
        print("1. 高优先级策略可立即入场")
    if len(cautious) > 0:
        print("2. 谨慎策略建议等待价格回调(relative_price < 0.5)")
    print("3. 止损建议: 3-5% (日线趋势不明)")
    print("4. 仓位建议: ≤20% (恢复期波动大)")


def main():
    print("\n" + "="*60)
    print("市场环境分析报告")
    print("="*60)
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"分析标的: BTC/USDT (加密市场风向标)")
    print("="*60 + "\n")

    # Load data
    df_1h = load_btc_data("1h")
    df_4h = load_btc_data("4h")
    df_1d = load_btc_data("1d")

    latest_date = df_1h['date'].iloc[-1]
    print(f"数据截止: {latest_date}")
    print()

    # Method 1: ADX + DI (Most authoritative)
    print("【方法1: ADX + DI 趋势判断】")
    print("来源: Welles Wilder (1978) ⭐⭐⭐⭐⭐ 最高权威")
    print("-"*50)
    adx_1h = analyze_adx_di(df_1h)
    adx_4h = analyze_adx_di(df_4h)
    adx_1d = analyze_adx_di(df_1d)

    print(f"1小时: ADX={adx_1h['adx']:.1f}, +DI={adx_1h['plus_di']:.1f}, -DI={adx_1h['minus_di']:.1f}")
    print(f"       趋势强度: {adx_1h['trend_strength']}, 方向: {adx_1h['direction']}")
    print(f"       判断: {adx_1h['market_state']}")
    print()
    print(f"4小时: ADX={adx_4h['adx']:.1f}, +DI={adx_4h['plus_di']:.1f}, -DI={adx_4h['minus_di']:.1f}")
    print(f"       判断: {adx_4h['market_state']}")
    print()
    print(f"日线:  ADX={adx_1d['adx']:.1f}, +DI={adx_1d['plus_di']:.1f}, -DI={adx_1d['minus_di']:.1f}")
    print(f"       判断: {adx_1d['market_state']}")
    print()

    # Method 2: EMA200
    print("【方法2: EMA200 趋势线】")
    print("来源: 经典技术分析理论 ⭐⭐⭐⭐⭐ 最高权威")
    print("-"*50)
    ema_1h = analyze_ema200(df_1h)
    ema_4h = analyze_ema200(df_4h)
    ema_1d = analyze_ema200(df_1d)

    print(f"当前价格: ${ema_1h['close']:,.2f}")
    print(f"EMA200:  ${ema_1h['ema200']:,.2f} (距离: {ema_1h['distance_from_ema200_pct']:.2f}%)")
    print(f"价格位置: {'在EMA200上方' if ema_1h['price_above_ema200'] else '在EMA200下方'}")
    print(f"均线排列: {ema_1h['ema_alignment']}")
    print(f"判断: {ema_1h['market_state']}")
    print()

    # Method 3: Relative Price
    print("【方法3: Relative Price 相对位置】")
    print("来源: NASOSRv6等社区策略 ⭐⭐ 实践验证")
    print("-"*50)
    relative_1h = analyze_relative_price(df_1h, window=60)  # 60小时 ~ 2.5天
    relative_4h = analyze_relative_price(df_4h, window=60)  # 60个4h ~ 10天
    relative_1d = analyze_relative_price(df_1d, window=30)  # 30天

    print(f"近期高点: ${relative_1d['close_max']:,.2f}")
    print(f"近期低点: ${relative_1d['close_min']:,.2f}")
    print(f"相对位置: {relative_1d['relative_price']:.2f} ({relative_1d['position']})")
    print(f"从高点下跌: {relative_1d['dropped_pct']*100:.1f}%")
    print()

    # Method 4: Recent Trend
    print("【方法4: 近期价格趋势】")
    print("-"*50)
    trend_1d = analyze_price_trend(df_1d, lookback=30)
    trend_7d = analyze_price_trend(df_1d, lookback=7)

    print(f"近30天涨跌: {trend_1d['change_pct']:.1f}% ({trend_1d['trend']})")
    print(f"近7天涨跌:  {trend_7d['change_pct']:.1f}% ({trend_7d['trend']})")
    print()

    # Method 5: Cycle Start Point Analysis
    print("【方法5: 周期起始点分析】")
    print("来源: 多种权威方法综合判断")
    print("-"*50)
    cycle_info = find_cycle_start(df_1d)

    # EMA200 breakthrough
    print(f"EMA200突破点:")
    if cycle_info['breakthrough_date']:
        print(f"  日期: {cycle_info['breakthrough_date']}")
        print(f"  类型: {cycle_info['breakthrough_type']}")
        print(f"  价格: ${cycle_info['breakthrough_price']:,.2f}")
        print(f"  已持续: {cycle_info['days_since_breakthrough']}天")
    else:
        print(f"  {cycle_info['breakthrough_type']}")
    print()

    # 20% threshold (Wall Street standard)
    print(f"华尔街20%法则:")
    print(f"  周期类型: {cycle_info['cycle_type_20pct']}")
    print(f"  起始日期: {cycle_info['cycle_start_20pct']}")
    print(f"  周期天数: {cycle_info['days_in_cycle_20pct']}天")
    print(f"  判断依据: {cycle_info['cycle_threshold']}")
    print()

    # Cycle high/low
    print(f"周期高低点划分:")
    print(f"  周期类型: {cycle_info['cycle_type_highlow']}")
    print(f"  起始日期: {cycle_info['cycle_start_highlow']}")
    print(f"  周期天数: {cycle_info['days_in_cycle_highlow']}天")
    print(f"  近期高点: ${cycle_info['recent_high']:,.2f} ({cycle_info['high_date']})")
    print(f"  近期低点: ${cycle_info['recent_low']:,.2f} ({cycle_info['low_date']})")
    print()

    # Overall Summary
    print("="*60)
    print("【综合判断】")
    print("="*60)
    summary, bullish_score, bearish_score = get_market_summary(adx_1h, adx_4h, adx_1d, ema_1d, relative_1d, trend_1d)
    print(summary)
    print()

    # Strategy recommendations from registry
    print("="*60)
    print("【策略推荐】")
    print("="*60)

    # Build market state for strategy matching
    market_state = {
        'bullish_score': bullish_score,
        'bearish_score': bearish_score,
        'adx_4h_has_trend': adx_4h['adx'] > 25,
        'adx_4h_direction': 'bull' if adx_4h['plus_di'] > adx_4h['minus_di'] else 'bear',
        'adx_1d_has_trend': adx_1d['adx'] > 25,
        'adx_1d_direction': 'bull' if adx_1d['plus_di'] > adx_1d['minus_di'] else 'bear',
        'price_above_ema200': ema_1d['price_above_ema200'],
        'relative_price': relative_1d['relative_price'],
        'cycle_type': cycle_info['cycle_type_20pct']
    }

    # Load strategy registry
    registry = load_strategy_registry()

    # Get recommendations
    recommendations = recommend_strategies(registry, market_state)

    # Print recommendations
    print_strategy_recommendations(recommendations)

    print()
    print("="*60)


if __name__ == "__main__":
    main()