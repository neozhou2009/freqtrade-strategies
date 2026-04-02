# JmStrategy Analysis

> **Strategy Number**: #184 (184th of 465 strategies)  
> **Strategy Type**: Trend Following / Market Maker Strategy  
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**JmStrategy** is a multi-indicator trend-following strategy combining KAMA (Kaufman Adaptive Moving Average), CCI, RSI, and MACD. It uses combined signals from multiple indicators to filter false signals and improve trade quality.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Condition** | KAMA golden cross/slope + CCI + RSI multi-condition combo |
| **Exit Condition** | KAMA death cross/slope reversal + CCI/RSI conditions |
| **Protection** | Trailing stop + dynamic take-profit |
| **Timeframe** | 5 Minutes |
| **Dependencies** | TA-Lib, technical, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.11599,
    "18": 0.03112,
    "34": 0.01895,
    "131": 0
}

# Stop-Loss Setting
stoploss = -0.32982  # -32.98%

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.28596
trailing_stop_positive_offset = 0.29771
trailing_only_offset_is_reached = True
```

---

## III. Entry Conditions Details

### 3.1 KAMA Crossover/Slope

```python
# KAMA Crossover Trigger
Condition: KAMA short-term > KAMA long-term

# OR KAMA Slope Trigger
Condition: KAMA long-term slope > 1
```

### 3.2 CCI Condition

```python
# Optional: CCI > threshold (default 198)
```

### 3.3 RSI Condition

```python
# Optional: RSI > threshold (default 72)
```

---

## IV. Exit Conditions Details

### 4.1 Exit Condition Combinations

```python
# KAMA Death Cross
Condition: KAMA short-term < KAMA long-term

# OR KAMA Slope Reversal
Condition: KAMA long-term slope < 1

# Optional: RSI below threshold
# Optional: CCI below threshold
```

---

## V. Technical Indicator System

| Indicator | Purpose |
|-----------|---------|
| KAMA | Adaptive Moving Average, trend confirmation |
| CCI | Commodity Channel Index, momentum judgment |
| RSI | Relative Strength Index, overbought/oversold |
| MACD | Trend direction confirmation |

---

## VI. Risk Management

### 6.1 Take-Profit Strategy

The strategy uses multi-level ROI exits:
- 0 minutes: 11.599%
- 18 minutes: 3.112%
- 34 minutes: 1.895%
- After 131 minutes: No requirement

### 6.2 Trailing Stop

- Activation point: 29.571% profit
- Stop level: 28.596% profit pullback
- Activated only after activation point is reached

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Multi-Indicator Confirmation**: Multiple indicators simultaneously verify, improving signal quality
2. **Adaptive**: KAMA automatically adapts to market volatility
3. **Trailing Stop**: Let profits run

### ⚠️ Cons

1. **Complex**: Many conditions, difficult to optimize
2. **Lagging**: Multi-indicator combinations increase lag
3. **Many Parameters**: Requires extensive tuning

---

## VIII. Applicable Scenarios

| Market Environment | Performance |
|-------------------|-------------|
| Trending Up | ⭐⭐⭐⭐⭐ |
| Trending Down | ⭐⭐⭐⭐⭐ |
| Ranging | ⭐⭐ |

---

## IX. Parameter Optimization

| Parameter | Description |
|-----------|-------------|
| KAMA Period | Short/long-term periods |
| CCI Threshold | Buy/sell thresholds |
| RSI Period | Relative strength period |

---

## X. Live Trading Notes

This strategy's parameters have been optimized (based on 60 days of data). It is recommended to use default parameters directly or fine-tune based on specific trading pairs.

---

## XI. Summary

**JmStrategy** is a complex multi-indicator trend strategy combining KAMA, CCI, and RSI. The strategy is optimized, with default parameters performing well, but adjustment is needed for different market environments. Suitable for experienced traders.

---
