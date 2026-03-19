#!/usr/bin/env python3
"""
Strategy Classifier - Multi-dimensional tagging system

Analyzes strategy files and classifies them across multiple dimensions:
- style: Trading style (Trend, Mean Reversion, Momentum, Breakout, Scalping)
- indicators: Primary technical indicators used
- timeframe: Main trading timeframe
- market: Suitable market condition (Trending, Ranging, Any)
- features: Additional features (custom-stoploss, trailing-stop, hyperopt, etc.)
- complexity: 1-10 score based on features and indicators
- family: Grouping name for strategy variants
- side: Trading side (Long, Short, Both)

"""

import os
import re
import json
import glob
from collections import defaultdict


INDICATOR_PATTERNS = {
    "RSI": [r"ta\.RSI", r"rsi\s*\(", r"RSI\s*\("],
    "EMA": [r"ta\.EMA", r"ema\s*\(", r"EMA\s*\("],
    "SMA": [r"ta\.SMA", r"sma\s*\(", r"SMA\s*\("],
    "MACD": [r"ta\.MACD", r"macd\s*\(", r"MACD\s*\("],
    "BB": [r"bollinger", r"bb_lower", r"bb_upper", r"bb_mid", r"BB_"],
    "CCI": [r"ta\.CCI", r"cci\s*\(", r"CCI\s*\("],
    "ADX": [r"ta\.ADX", r"plus_di", r"minus_di", r"adx\s*\("],
    "Ichimoku": [r"ichimoku", r"tenkan", r"kijun", r"senkou", r"kumo"],
    "Supertrend": [r"supertrend", r"SuperTrend", r"SUPER_TREND"],
    "ATR": [r"ta\.ATR", r"atr\s*\(", r"ATR\s*\("],
    "Stoch": [r"ta\.STOCH", r"stoch\s*\(", r"StochRSI", r"fastk", r"fastd"],
    "MFI": [r"ta\.MFI", r"mfi\s*\(", r"MFI\s*\("],
    "VWAP": [r"vwap", r"VWAP"],
    "OBV": [r"ta\.OBV", r"obv\s*\(", r"OBV\s*\("],
    "Williams": [r"williams", r"willr", r"r_14", r"r_96"],
    "Momentum": [r"ta\.MOM", r"momentum\s*\(", r"MOM\s*\("],
    "ROC": [r"ta\.ROC", r"roc\s*\(", r"ROC\s*\("],
    "RMI": [r"RMI\s*\(", r"rmi\s*\("],
    "PSAR": [r"ta\.SAR", r"psar", r"parabolic"],
    "Trix": [r"trix", r"Trix", r"TRIX"],
    "TEMA": [r"tema", r"TEMA"],
    "Alligator": [r"alligator", r"Alligator"],
    "Awesome": [r"awesome", r"AO\s*\("],
    "Donchian": [r"donchian", r"dc_", r"dc_h", r"dc_l"],
    "Keltner": [r"keltner", r"kc_", r"kc_upper", r"kc_lower"],
    "Fibonacci": [r"fib", r"fibonacci", r"retracement"],
    "Heikin": [r"heikin", r"heiken", r"ha_close", r"ha_open"],
    "EWO": [r"EWO", r"elliot_wave", r"ewo"],
}

TIMEFRAME_PATTERN = r'timeframe\s*=\s*["\'](\w+)["\']'


def extract_indicators(content: str) -> list:
    indicators = []
    content_lower = content.lower()

    for ind_name, patterns in INDICATOR_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                if ind_name not in indicators:
                    indicators.append(ind_name)
                break

    return indicators


def extract_timeframe(content: str) -> str:
    match = re.search(TIMEFRAME_PATTERN, content)
    if match:
        return match.group(1)
    return "unknown"


def detect_trading_styles(content: str, indicators: list) -> list:
    styles = []
    content_lower = content.lower()
    scores = defaultdict(float)

    # Trend Following indicators
    trend_indicators = [
        "EMA",
        "SMA",
        "MACD",
        "Ichimoku",
        "Supertrend",
        "Alligator",
        "ADX",
        "PSAR",
    ]
    trend_count = sum(1 for ind in indicators if ind in trend_indicators)
    if trend_count > 0:
        scores["Trend"] += trend_count * 2

    # Trend detection in code
    if re.search(
        r"(up_trend|dn_trend|uptrend|downtrend|ema_\d+\s*>\s*ema|sma.*cross)",
        content_lower,
    ):
        scores["Trend"] += 3

    # Mean Reversion indicators
    mr_indicators = ["RSI", "BB", "CCI"]
    mr_count = sum(1 for ind in indicators if ind in mr_indicators)
    if mr_count > 0:
        if (
            "bb_lower" in content_lower
            or "bb_upper" in content_lower
            or "bollinger" in content_lower
        ):
            if re.search(r"(oversold|overbought|<\s*\d|>\s*\d)", content_lower):
                scores["Mean Reversion"] += mr_count * 3
        elif "rsi" in content_lower and re.search(
            r"(rsi\s*[<>]\s*\d|oversold|overbought)", content_lower
        ):
            scores["Mean Reversion"] += mr_count * 2.5

    # BB+RSI classic mean reversion
    if "BB" in indicators and "RSI" in indicators:
        scores["Mean Reversion"] += 4

    # Momentum indicators
    momentum_indicators = [
        "Momentum",
        "ROC",
        "Stoch",
        "MFI",
        "Williams",
        "Awesome",
        "RMI",
    ]
    mom_count = sum(1 for ind in indicators if ind in momentum_indicators)
    if mom_count > 0:
        scores["Momentum"] += mom_count * 2.5

    # ADX for momentum/trend strength
    if "ADX" in indicators:
        scores["Momentum"] += 1.5

    # Breakout indicators
    breakout_indicators = ["Donchian", "Keltner", "ATR"]
    breakout_count = sum(1 for ind in indicators if ind in breakout_indicators)
    if breakout_count > 0:
        scores["Breakout"] += breakout_count * 2

    # Breakout patterns in code
    if re.search(
        r"(breakout|break.*high|break.*low|above.*high|below.*low)", content_lower
    ):
        scores["Breakout"] += 3

    # Scalping detection
    if re.search(r"(scalp|quick|fast_\w+)", content_lower):
        scores["Scalping"] += 5

    # Filter and sort
    threshold = 2.0
    styles = [style for style, score in scores.items() if score >= threshold]

    # Limit to top 2 styles if too many
    if len(styles) > 2:
        sorted_styles = sorted(scores.items(), key=lambda x: -x[1])
        styles = [s[0] for s in sorted_styles[:2]]

    # Default to Trend if no clear style
    if not styles:
        styles = ["Trend"]

    return styles


def detect_market_condition(content: str, styles: list, indicators: list) -> str:
    content_lower = content.lower()

    # Check for ranging/sideways indicators
    if "Mean Reversion" in styles:
        return "Ranging"

    # Check for trending indicators
    if "Trend" in styles and "Mean Reversion" not in styles:
        return "Trending"

    # Breakout strategies work in both
    if "Breakout" in styles:
        return "Volatile"

    # Default
    return "Any"


def detect_features(content: str) -> list:
    features = []
    content_lower = content.lower()

    if "use_custom_stoploss" in content_lower or "def custom_stoploss" in content_lower:
        features.append("custom-stoploss")

    if "trailing_stop" in content_lower and "trailing_stop" in content_lower:
        if "trailing_stop = True" in content or "trailing_stop=True" in content:
            features.append("trailing-stop")

    if "def custom_exit" in content_lower:
        features.append("custom-exit")

    if "def confirm_trade_entry" in content_lower:
        features.append("confirm-entry")

    if (
        "DecimalParameter" in content
        or "IntParameter" in content
        or "CategoricalParameter" in content
    ):
        features.append("hyperopt")

    if "informative_pairs" in content_lower:
        features.append("multi-timeframe")

    if "heikin" in content_lower or "heiken" in content_lower:
        features.append("heikin-ashi")

    buy_conditions = len(re.findall(r"(is_\w+\s*=|conditions\.append)", content))
    if buy_conditions > 5:
        features.append("multi-condition")

    if "Freqai" in content or "freqai" in content_lower:
        features.append("freqai")

    return features


def calculate_complexity(indicators: list, features: list) -> int:
    score = 1
    score += len(indicators) * 0.4
    
    feature_weights = {
        "custom-stoploss": 1.5,
        "custom-exit": 1.0,
        "confirm-entry": 1.0,
        "hyperopt": 1.5,
        "multi-timeframe": 2.0,
        "heikin-ashi": 1.0,
        "multi-condition": 1.5,
        "freqai": 4.0
    }
    
    for feat in features:
        score += feature_weights.get(feat, 0.5)
        
    return min(10, round(score))


def detect_side(content: str) -> str:
    content_lower = content.lower()
    has_short = False
    if "can_short" in content_lower and "can_short = True" in content:
        has_short = True
    elif "populate_entry_short" in content or "populate_exit_short" in content:
        has_short = True
    elif "is_short" in content_lower:
        has_short = True
        
    has_long = "populate_entry_long" in content or "populate_buy_trend" in content or "populate_entry_trend" in content
    
    if has_long and has_short:
        return "Both"
    if has_short:
        return "Short"
    return "Long"


def determine_family(strategy_name: str) -> str:
    # Remove common suffixes and versioning
    name = strategy_name
    name = re.sub(r'(_?v?\d+_?\d*)$', '', name, flags=re.IGNORECASE)
    name = re.sub(r'(_?final|_?mod|_?test|_?opt|_?optimized)$', '', name, flags=re.IGNORECASE)
    
    # Common Freqtrade strategy prefixes
    prefixes = ["BB_RPB_TSL", "ClucHAnix", "NostalgiaForInfinity", "SMAOffset", "BBRSI"]
    for p in prefixes:
        if strategy_name.startswith(p):
            return p
            
    # Fallback to first word if underscore exists
    if "_" in name:
        return name.split("_")[0]
        
    return name



def is_special_strategy(strategy_name: str, content: str) -> tuple:
    name_lower = strategy_name.lower()
    content_lower = content.lower()

    special_keywords = [
        "alwaysbuy",
        "alwaybuy",
        "buyonly",
        "buy_only",
        "sample",
        "test",
        "experimental",
        "yolo",
        "fake",
        "demo",
    ]

    for kw in special_keywords:
        if kw in name_lower:
            return True, "test-strategy"

    if re.search(
        r"class\s+\w*Always\w*|class\s+\w*BuyOnly\w*|class\s+\w*YOLO\w*",
        content,
        re.IGNORECASE,
    ):
        return True, "test-strategy"

    if re.search(
        r"class\s+\w+\s*\(\s*(YourStrat|BaseStrategy)\s*\)", content, re.IGNORECASE
    ):
        return True, "utility-strategy"

    if "trailing" in name_lower and "strat" in name_lower:
        return True, "trailing-utility"

    if (
        "def populate_entry_trend" not in content
        and "def populate_buy_trend" not in content
    ):
        return True, "minimal-strategy"

    return False, None


def classify_strategy(filepath: str) -> dict:
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return {
            "style": ["Error"],
            "indicators": [],
            "timeframe": "unknown",
            "market": "Any",
            "features": [],
            "error": str(e),
        }

    strategy_name = os.path.basename(filepath)[:-3]

    is_special, special_type = is_special_strategy(strategy_name, content)
    if is_special:
        return {
            "style": ["Special"],
            "indicators": [],
            "timeframe": extract_timeframe(content),
            "market": "Any",
            "features": [special_type],
        }

    indicators = extract_indicators(content)
    timeframe = extract_timeframe(content)
    styles = detect_trading_styles(content, indicators)
    market = detect_market_condition(content, styles, indicators)
    features = detect_features(content)
    complexity = calculate_complexity(indicators, features)
    side = detect_side(content)
    family = determine_family(strategy_name)

    return {
        "style": styles,
        "indicators": indicators,
        "timeframe": timeframe,
        "market": market,
        "features": features,
        "complexity": complexity,
        "side": side,
        "family": family
    }



def main():
    strategies = {}

    # Explicitly sort the list of files to ensure deterministic input order
    strategy_files = sorted(glob.glob("strategies/**/*.py", recursive=True))

    for filepath in strategy_files:
        basename = os.path.basename(filepath)
        if basename == "__init__.py":
            continue
        strategy_name = basename[:-3]

        result = classify_strategy(filepath)
        strategies[strategy_name] = result

    strategies = dict(sorted(strategies.items()))

    # Enable sort_keys for strict idempotency and consistent git diffs
    with open("strategy_registry.json", "w") as f:
        json.dump(strategies, f, indent=2, sort_keys=True)

    # Print summary
    style_counts = defaultdict(int)
    timeframe_counts = defaultdict(int)
    market_counts = defaultdict(int)

    for name, info in strategies.items():
        for style in info["style"]:
            style_counts[style] += 1
        timeframe_counts[info["timeframe"]] += 1
        market_counts[info["market"]] += 1

    print("\n=== Strategy Classification Summary ===")
    print(f"Total strategies: {len(strategies)}")

    print(f"\nTrading Styles:")
    for style, count in sorted(style_counts.items(), key=lambda x: -x[1]):
        print(f"  {style}: {count}")

    print(f"\nTimeframes:")
    for tf, count in sorted(timeframe_counts.items(), key=lambda x: -x[1]):
        print(f"  {tf}: {count}")

    print(f"\nMarket Conditions:")
    for market, count in sorted(market_counts.items(), key=lambda x: -x[1]):
        print(f"  {market}: {count}")

    print(f"\nRegistry saved to strategy_registry.json")


if __name__ == "__main__":
    main()
