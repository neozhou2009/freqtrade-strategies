# ichiV1 Strategy Analysis

> **Strategy Number**: #27 (27th of 465 strategies)  
> **Strategy Type**: Ichimoku Cloud + Multi-Timeframe Trend Following  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

**ichiV1** is a multi-timeframe trend following strategy based on Ichimoku Cloud. Key features include using multiple timeframe EMAs to confirm trend strength (Fan), combined with Ichimoku Cloud to filter trends.

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | Multi-condition combination (Cloud + Multi-timeframe trend + Fan) |
| **Exit Conditions** | 1 condition: Trend crossover |
| **Protection** | Hard stoploss + Trailing stop |
| **Timeframe** | 5 minutes |
| **Dependencies** | TA-Lib, technical, pandas, numpy |
| **Special Features** | Multi-timeframe trend confirmation, Fan |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.059,     # Immediate exit: 5.9% profit
    "10": 0.037,    # After 10 minutes: 3.7% profit
    "41": 0.012,    # After 41 minutes: 1.2% profit
    "114": 0,       # After 114 minutes: exit at breakeven
}

# Stoploss setting
stoploss = -0.275  # -27.5% hard stoploss

# Trailing stop
trailing_stop = True
```

**Design Logic**:
- **Multi-Level ROI**: 4-level decreasing ROI, longer holding time means lower exit threshold
- **Loose Stoploss**: -27.5% hard stoploss, giving ample room for fluctuation
- **Trailing Stop**: Enabled but no specific parameters configured

---

## III. Entry Conditions Explained

### 3.1 Entry Logic

**Trend Above Cloud (8 Levels)**
```python
# Levels 1-8, from 5m to 8h
if buy_trend_above_senkou_level >= 1:
    conditions.append(trend_close_5m > senkou_a)
    conditions.append(trend_close_5m > senkou_b)
if buy_trend_above_senkou_level >= 2:
    conditions.append(trend_close_15m > senkou_a)
    conditions.append(trend_close_15m > senkou_b)
# ... until 8h
```

**Trend Bullish (8 Levels)**
```python
# Levels 1-8, from 5m to 8h
if buy_trend_bullish_level >= 1:
    conditions.append(trend_close_5m > trend_open_5m)
if buy_trend_bullish_level >= 2:
    conditions.append(trend_close_15m > trend_open_15m)
# ... until 8h
```

**Fan Confirmation**
```python
# Fan magnitude gain
conditions.append(fan_magnitude_gain >= buy_min_fan_magnitude_gain)
conditions.append(fan_magnitude > 1)

# Fan magnitude continuously rising
for x in range(buy_fan_magnitude_shift_value):
    conditions.append(fan_magnitude.shift(x+1) < fan_magnitude)
```

---

## IV. Exit Logic Explained

### 4.1 Exit Conditions

```python
# Exit conditions
dataframe.loc[
    (
        qtpylib.crossed_below(dataframe['trend_close_5m'], dataframe[sell_trend_indicator])
    ),
    'sell',
] = 1
```

**Logic Analysis**:
- **Trend Crossover**: 5m trend crosses below sell trend indicator (default 2h)
- **Default Sell Indicator**: trend_close_2h

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|---------|---------|------|------|
| **Candles** | Heikin Ashi | - | Smooth candles |
| **Trend** | EMA | 3/6/12/24/48/72/96 | Multi-timeframe trend |
| **Trend** | Ichimoku Cloud | 20/60/120 | Cloud filtering |
| **Fan** | Fan Magnitude | 1h/8h | Trend strength |

### 5.2 Multi-Timeframe Trend

| Timeframe | EMA Period | Purpose |
|---------|---------|------|
| 5m | - | Base trend |
| 15m | 3 | Short-term trend |
| 30m | 6 | Medium short-term trend |
| 1h | 12 | Medium-term trend |
| 2h | 24 | Medium long-term trend |
| 4h | 48 | Long-term trend |
| 6h | 72 | Longer trend |
| 8h | 96 | Longest trend |

### 5.3 Fan

```python
fan_magnitude = trend_close_1h / trend_close_8h
fan_magnitude_gain = fan_magnitude / fan_magnitude.shift(1)
```

**Purpose**:
- Measure gap between 1h and 8h trends
- fan_magnitude > 1: Uptrend
- fan_magnitude_gain > 1: Trend strengthening

---

## VI. Risk Management Features

### 6.1 Loose Hard Stoploss

```python
stoploss = -0.275  # -27.5%
```

**Description**: Loose stoploss, giving ample room for fluctuation.

### 6.2 Trailing Stop

```python
trailing_stop = True
```

**Purpose**: Enable trailing stop to protect profits.

### 6.3 Multi-Layer Trend Filtering

```python
# 8-level trend confirmation
if buy_trend_above_senkou_level >= 8:
    # From 5m to 8h all above cloud
```

**Purpose**:
- Multi-layer trend confirmation, reduces false signals
- Only trade in strong trends

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Multi-Timeframe**: 8 timeframes confirm trend
2. **Ichimoku Cloud**: Cloud filters trends
3. **Fan**: Measures trend strength
4. **Heikin Ashi**: Smooth candles reduce noise
5. **Hyperopt Optimization**: Supports Hyperopt for key parameters
6. **Loose Stoploss**: -27.5% stoploss, giving ample room

### ⚠️ Limitations

1. **Extremely High Complexity**: Multi-timeframe + Ichimoku Cloud, difficult to debug
2. **No BTC Correlation**: Does not detect Bitcoin market trend
3. **Parameter Sensitive**: Hyperopt results may overfit
4. **High Computation**: Multi EMA + Ichimoku Cloud increases computation
5. **Loose Stoploss**: -27.5% stoploss may cause significant losses in extreme conditions

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| **Uptrend** | Highly recommended | Multi-timeframe + cloud filtering, perfect match |
| **Ranging Market** | Not recommended | Trend strategy has many false signals in ranging |
| **Downtrend** | Pause | Multi-layer trend filtering blocks most trades |
| **High Volatility** | Adjust parameters | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |

---

## IX. Summary

**ichiV1** is a well-designed advanced trend following strategy, its core value lies in:

1. **Multi-Timeframe**: 8 timeframes confirm trend
2. **Ichimoku Cloud**: Cloud filters trends
3. **Fan**: Measures trend strength
4. **Heikin Ashi**: Smooth candles reduce noise
5. **Hyperopt Optimization**: Supports Hyperopt for key parameters
6. **Loose Stoploss**: -27.5% stoploss, giving ample room

For quantitative traders, this is an excellent multi-timeframe learning template. Recommendations:
- Use as an advanced case for learning multi-timeframe strategies
- Understand Ichimoku Cloud usage
- Learn Fan application
- Note that hyperopt parameters may overfit, testthoroughly before live trading

---
