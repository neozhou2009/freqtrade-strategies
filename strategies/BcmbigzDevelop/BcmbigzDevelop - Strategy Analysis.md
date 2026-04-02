# BcmbigzDevelop Strategy Analysis

> **Strategy Number**: #53  
> **Strategy Type**: Multi-Condition Composite Trend Following Strategy  
> **Timeframe**: 5 minutes (5m) + Information Timeframe 1h

---

## I. Strategy Overview

BcmbigzDevelop is an extremely complex composite quantitative trading strategy that integrates multiple sub-strategy systems, including BigZ07 (bzv7), CombinedBinHClucAndMADV6 (v6), and CombinedBinHClucV8 (v8). The strategy's design philosophy is to build a "multi-layer protection net" through multi-dimensional technical indicator combinations to capture various market entry opportunities.

The core feature of this strategy lies in its highly modular design: each sub-strategy has an independent condition numbering system, conditions can be independently enabled or disabled, and traders can flexibly configure the strategy's "offensiveness" based on their risk preferences and market judgment.

As a multi-timeframe strategy, BcmbigzDevelop simultaneously analyzes the 5-minute main trading timeframe and the 1-hour information timeframe, filtering false signals through higher-dimensional timeframe data to improve signal quality.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 22 independent entry conditions (bzv7: 14 + v6: 4 + v8: 5) |
| **Exit Conditions** | 3 basic exit signals + multi-layer dynamic take-profit logic |
| **Protection** | Multiple independent protection parameter groups (RSI, volume, EMA filtering, etc.) |
| **Timeframe** | 5 minutes + 1 hour (information timeframe) |
| **Dependencies** | talib, technical, numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# Multi-level ROI exit table
minimal_roi = {
    "0": 0.20,
    "38": 0.074,
    "78": 0.025,
    "194": 0
}

# Stoploss setting - actually disabled, uses custom stoploss
stoploss = -0.99
```

**Design Logic**:

This ROI table is relatively concise with only 4 gradients:

1. **Early (0-38 minutes)**: Aggressive 20% take-profit target
2. **Short-term (38-78 minutes)**: Moderate 7.4% take-profit
3. **Mid-term (78-194 minutes)**: Conservative 2.5% take-profit
4. **Long-term (194+ minutes)**: 0% (cost exit)

The stoploss is set to -0.99, meaning the default stoploss is disabled, relying entirely on the custom stoploss function for risk management.

### 2.2 Trailing Stop Configuration

```python
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.05
```

- Trailing stop is enabled
- Only starts trailing after profit exceeds 5%
- Trailing range is 1%

### 2.3 Custom Stoploss Configuration

```python
use_custom_stoploss = True
```

The strategy uses the `custom_stoploss()` function to implement dynamic risk management.

---

## III. Entry Conditions Details

### 3.1 Condition System Overview

| Condition Group | Number of Conditions | Core Logic |
|----------------|---------------------|------------|
| bzv7 (BigZ07) | 14 | RSI filtering + Volume filtering + Bollinger Band break |
| v6 (MADV6) | 4 | EMA long arrangement + Bollinger Band break |
| v8 (V8) | 4 | SSL Channel + EMA crossover + Multi-timeframe confirmation |
| **Total** | **22** | Comprehensive multi-strategy advantages |

### 3.2 bzv7 Condition Group Details

**Condition bzv7_0**: RSI Oversold + Strong Confirmation

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["rsi"] < 30) &
(dataframe["close"] * 1.024 < dataframe["open"].shift(3)) &
(dataframe["rsi_1h"] < 71) &
(Volume filtering conditions)
```

**Conditions bzv7_1-2**: Bollinger Band Safe Zone + Volume Filtering

- Requires close price near lower Bollinger Band (0.982-0.989x)
- Requires volume in specific pattern (recent volume increases then decreases)

**Conditions bzv7_3-4**: 1h RSI Filtering + Bollinger Band Break

**Conditions bzv7_5-7**: MACD Crossover + Bollinger Bands

**Conditions bzv7_8-9**: Dual RSI Filtering (5m + 1h)

**Conditions bzv7_10-11**: Special Pattern Recognition (rarely used)

**Condition bzv7_12**: Comprehensive Filtering

**Condition bzv7_13**: CMF Capital Flow Filtering

### 3.3 v6 Condition Group Details

The v6 strategy comes from CombinedBinHClucAndMADV6, mainly focusing on:

1. **EMA Long Arrangement**: ema_50 > ema_200 and price stands above EMA
2. **Bollinger Band Break**: Price below lower Bollinger Band
3. **Volume Contraction**: Recent volume significantly decreased

### 3.4 v8 Condition Group Details

The v8 strategy comes from CombinedBinHClucV8, introducing some new concepts:

1. **SSL Channel**: SSL upper > SSL lower indicates long state
2. **Drawdown Range Filtering**: Limits maximum drawdown before entry
3. **Multi-Timeframe Confirmation**: Simultaneously checks 5m and 1h EMA trends

---

## IV. Exit Logic Explained

### 4.1 Multi-Layer Take-Profit System

The strategy implements graded take-profit through the `custom_exit()` function:

```
Profit Range     RSI Condition    Signal Name
────────────────────────────────────────────────────
14-30%          RSI < 58         roi_target_4
8-14%           RSI < 56         roi_target_3
4-8%            RSI < 50         roi_target_2
1-4%            RSI < 50         roi_target_1
0-1%            SMA200 Death Cross  roi_target_5
```

### 4.2 Trailing Take-Profit System

```python
# Trailing Take-Profit 1
(current_profit > 0.10) & (current_profit < 0.40) & 
(Drawdown from high > 3% + profit)

# Trailing Take-Profit 2  
(current_profit > 0.02) & (current_profit < 0.10) &
(Drawdown from high > 1.5% + profit)
```

### 4.3 Basic Exit Signals

| Scenario | Trigger Condition | Signal Name |
|---------|------------------|-------------|
| Bollinger Band Middle Break | close > bb_middleband * 1.01 | bzv7_sell_0 |
| Bollinger Upper Consecutive Break | 3 consecutive candles break upper band | v8_sell_0 |
| RSI Overbought | RSI > 80 | v8_sell_1 |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Usage |
|-------------------|-------------------|-------|
| Trend Indicators | EMA (12, 26, 50, 100, 200) | Identify trend direction |
| Momentum Indicators | RSI (14) | Overbought/oversold judgment |
| Trend Indicators | MACD | Momentum transition identification |
| Volatility Indicators | Bollinger Bands (20, 2), (40, 2) | Price relative position |
| Volume Indicators | CMF, MFI | Capital flow |
| Channel Indicators | SSL Channels | Trend channel |

### 5.2 Information Timeframe Indicators (1h)

The strategy uses 1-hour as information timeframe:

- ema_50_1h, ema_100_1h, ema_200_1h
- rsi_1h
- bb_lowerband_1h, bb_middleband_1h, bb_upperband_1h
- sma_200_1h, sma_200_dec_1h
- ssl_up_1h, ssl_down_1h

---

## VI. Risk Management Features

### 6.1 Custom Stoploss Logic

```python
# When profitable: disable stoploss, let profits run
if current_profit > 0:
    return 0.99

# When losing: dynamically adjust based on holding time and market state
if current position > 240 minutes:
    if rsi_1h < 35:
        return 0.99  # Hold, wait for reversal
    if price above EMA200:
        return 0.1  # Weak rebound, small cut
    if price continues falling:
        return 0.01  # Admit defeat
```

### 6.2 Condition Quantity Limitation

```python
buy_minimum_conditions = IntParameter(1, 2, default=1)
```

Requires at least 1 entry condition to be met before triggering entry, avoiding false signals when a single condition is triggered.

### 6.3 Volume Protection

All conditions include volume filtering:
- Volume > 0 (exclude zombie coins)
- Volume pattern filtering (recent volume increase/decrease)

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Multi-Condition System**: 22 conditions provide rich signal sources
2. **Modular Design**: Conditions can be independently configured, high flexibility
3. **Multi-Timeframe**: 1h information filtering improves signal quality
4. **Dynamic Take-Profit**: Multi-level take-profit + trailing take-profit
5. **Custom Stoploss**: Flexible stoploss logic

### ⚠️ Limitations

1. **Overly Complex**: 22 conditions difficult to understand and maintain
2. **Overfitting Risk**: Large number of parameters may have overfitting
3. **High Computation**: Multi-timeframe + multi-indicator calculation
4. **High Hardware Requirements**: High memory and CPU requirements

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Explanation |
|-------------------|--------------------------|-------------|
| Volatile Market | Enable more bzv7 conditions | More conditions = more opportunities |
| Trending Market | Enable v8 conditions | SSL Channel + EMA confirmation |
| Range-bound Market | Reduce condition count | Avoid frequent trading |

---

## IX. Applicable Market Environments Explained

### 9.1 Strategy Core Logic

- **Multi-Strategy Fusion**: Integrates bzv7, v6, v8 three sub-strategies
- **Multi-Dimensional Filtering**: RSI, volume, EMA, Bollinger Band multiple confirmation
- **Dynamic Risk Management**: Adjust stoploss based on market state

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Uptrend | ⭐⭐⭐⭐ | v8 conditions can capture trend pullbacks |
| 🔄 Range Consolidation | ⭐⭐⭐⭐⭐ | Multi-conditions provide rich signals |
| 📉 Downtrend | ⭐⭐⭐ | Counter-trend buying needs strict filtering |
| ⚡️ High Volatility | ⭐⭐⭐⭐ | Volatility provides more opportunities |

---

## X. Important Reminders: The Cost of Complexity

### 10.1 Learning Cost

- Understanding single conditions: 1-2 hours
- Understanding inter-condition relationships: 1-2 days
- Understanding overall logic: 1 week+
- Full mastery: 1 month+

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|---------------|-------------------|
| 10-20 pairs | 2GB | 4GB |
| 50 pairs | 4GB | 8GB |

### 10.3 Recommended Process

1. Backtest with default parameters
2. Observe which conditions contribute most
3. Adjust condition switches based on market
4. Small capital live verification

---

## XI. Summary

BcmbigzDevelop is an **"all-around"** complex strategy that integrates multiple validated sub-strategies, improving signal quality through multi-dimensional technical indicator combinations.

Its core value lies in:

1. **Flexibility**: 22 conditions can be independently configured
2. **Adaptability**: Different markets can enable different condition groups
3. **Comprehensiveness**: Covers various market environments
4. **Professionalism**: Multi-timeframe + dynamic take-profit + custom stoploss

For experienced quantitative traders, this strategy provides great customization space. However, for beginners, it is recommended to start with simpler strategies and try such complex strategies only after accumulating sufficient experience.

---

*This document is based on the BcmbigzDevelop strategy source code, for learning reference only, not investment advice.*
