# BigZ03HO Strategy Analysis

> **Strategy Number**: #58  
> **Strategy Type**: BigZ03 HyperOpt Optimized Version  
> **Timeframe**: 5 minutes (5m) + Information Timeframe 1h

---

## I. Strategy Overview

BigZ03HO is the **HyperOpt optimized version** of BigZ03, developed by ilya. This strategy optimizes entry parameters on the basis of standard BigZ03, making it more suitable for actual trading environments. The strategy maintains BigZ03's core design philosophy — low drawdown, quick sell — but improves signal precision and trading efficiency through parameter optimization.

### Core Features

| Feature | Configuration Value |
|---------|-------------------|
| Timeframe | 5 minutes (5m) |
| Information Timeframe | 1 hour (1h) |
| Take-Profit (ROI) | 0-10 min: 2.8%, 10-40 min: 1.8%, 40-180 min: 0.5%, 180+ min: 1.8% |
| Stoploss | -0.99 (use custom stoploss) |
| Trailing Stop | Enabled, positive 1%, trigger offset 2.5% |
| Number of Entry Conditions | 12 independent conditions |
| Recommended Number of Pairs | 2-4 |
| Information Timeframe | 1 hour |

---

## II. Strategy Configuration Analysis

### 2.1 Base Configuration

BigZ03HO's base configuration is exactly the same as BigZ03, difference lies in parameter optimization:

```python
timeframe = "5m"
inf_1h = "1h"

minimal_roi = {
    "0": 0.028,    # Immediate 2.8% profit on entry
    "10": 0.018,   # 1.8% after 10 minutes
    "40": 0.005,   # 0.5% after 40 minutes
    "180": 0.018   # 1.8% after 180 minutes
}

stoploss = -0.99  # Disable default stoploss

# Trailing stop configuration
trailing_stop = True
trailing_only_offset_is_reached = False
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.025

# Exit signal configuration
use_exit_signal = True
exit_profit_only = True
exit_profit_offset = 0.001
```

### 2.2 Optimized Parameters Comparison

BigZ03HO's core difference from BigZ03 lies in entry parameter optimization. Below are main changes:

| Parameter | BigZ03 | BigZ03HO | Change Explanation |
|-----------|--------|----------|-------------------|
| buy_bb20_close_bblowerband_safe_1 | 0.989 | 0.957 | Closer to lower band |
| buy_bb20_close_bblowerband_safe_2 | 0.982 | 0.766 | Deep lower band more aggressive |
| buy_volume_pump_1 | 0.4 | 0.1 | Stricter volume filtering |
| buy_volume_drop_1 | 3.8 | 4.0 | Stricter contraction multiple |
| buy_rsi_1h_1 | 16.5 | 39.8 | Significantly relaxed limit |
| buy_rsi_1 | 28.0 | 28.0 | Unchanged |

### 2.3 Parameter Optimization Interpretation

**Bollinger Band Parameter Aggression**:
- `bb_lowerband_safe_1` lowered from 0.989 to 0.957, means condition 1 now allows entry at price closer to lower Bollinger Band
- `bb_lowerband_safe_2` lowered from 0.982 to 0.766, this is very aggressive change, allows entry after price deeply breaks below lower band

**Volume Filtering Stricter**:
- `volume_pump_1` lowered from 0.4 to 0.1, this is a major change. Originally allowed 48-hour volume expansion 2.5x (1/0.4), now only allows 10x (1/0.1)
- `volume_drop_1` increased from 3.8 to 4.0, requires more significant volume contraction

**RSI Conditions Looser**:
- `rsi_1h_1` increased from 16.5 to 39.8, this is a seemingly contradictory but reasonable change. Original strategy required 1-hour RSI extremely oversold to trigger condition 4, while HO version significantly relaxed this limit

### 2.4 Parameter Optimization Logic Analysis

The logic behind these parameter changes is:

1. **Capture More Entry Opportunities**: Relaxed RSI limits mean more trading signals
2. **Filter Pumpdump**: Stricter volume filtering reduces probability of buying at volatility top
3. **More Aggressive Entry Points**: Entry at positions closer to lower Bollinger Band or even deeply broke below

---

## III. Entry Conditions Details

BigZ03HO retains the same 12 entry condition framework as BigZ03, but each condition's parameters optimized. Below detailed analysis of each condition:

### Condition 0: RSI Oversold + Decline Pattern

This is the most basic entry condition, unchanged:

```python
(
    (dataframe["close"] > dataframe["ema_200"]) &
    (dataframe["rsi"] < 30) &
    (dataframe["close"] * 1.024 < dataframe["open"].shift(3)) &
    (dataframe["rsi_1h"] < 71)
)
```

**Design Intent**: Confirm short-term oversold pullback in uptrend.

### Condition 1: Lower Bollinger Band + Volume Contraction (Optimization Focus)

```python
(
    (dataframe["close"] > dataframe["ema_200"]) &
    (dataframe["close"] > dataframe["ema_200_1h"]) &
    (dataframe["close"] < dataframe["bb_lowerband"] * 0.957) &  # Optimized from 0.989 to 0.957
    (dataframe["rsi_1h"] < 69) &
    (dataframe["open"] > dataframe["close"]) &
    # Stricter volume filtering
    (dataframe["volume"] < (dataframe["volume"].shift() * 4.0))  # Optimized from 3.8 to 4.0
)
```

**Optimization Effect**:
- Lower Bollinger Band threshold means buying at lower position
- Stricter volume filtering means more reliable signals

### Condition 2: Deep Lower Band (Aggressive Optimization)

```python
(
    (dataframe["close"] > dataframe["ema_200"]) &
    (dataframe["close"] < dataframe["bb_lowerband"] * 0.766)  # Significantly optimized from 0.982 to 0.766
)
```

**Aggression Level**: Price can be 23.4% lower than Bollinger Band and still enter. This is unimaginable in original strategy.

### Condition 3: Above 1-hour EMA200 + RSI Oversold

```python
(
    (dataframe["close"] > dataframe["ema_200_1h"]) &
    (dataframe["close"] < dataframe["bb_lowerband"]) &
    (dataframe["rsi"] < 14.2)
)
```

Unchanged, still capturing small cycle oversold points in big cycle uptrend.

### Condition 4: Extremely Low 1-hour RSI (Optimization Focus)

```python
(
    (dataframe["rsi_1h"] < 39.8) &  # Significantly relaxed from 16.5 to 39.8
    (dataframe["close"] < dataframe["bb_lowerband"])
)
```

**Change Interpretation**: Originally required 1-hour RSI below 16.5 (extremely oversold), now relaxed to 39.8. This is a big change, means condition 4 can now trigger in any non-overheated market.

This brings impact:
- **Positive**: Trading signals significantly increase
- **Risk**: May buy at trend top

### Conditions 5-9: MACD and RSI Combination Conditions

These conditions maintain BigZ03 framework, parameters may have slight adjustments, but core logic unchanged.

### Conditions 10-11: (Disabled by Default)

Same as BigZ03, these conditions disabled by default.

### Condition 12: False Breakout Pattern

```python
(
    (dataframe["close"] < dataframe["bb_lowerband"] * 0.993) &
    (dataframe["low"] < dataframe["bb_lowerband"] * 0.985) &
    (dataframe["close"].shift() > dataframe["bb_lowerband"]) &
    (dataframe["rsi_1h"] < 72.8) &
    (dataframe["open"] > dataframe["close"]) &
    (Volume and range conditions...)
)
```

Similarly added stricter volume filtering.

---

## IV. Exit Logic Explained

BigZ03HO's exit logic is exactly the same as BigZ03, did not introduce BigZ0307HO's complex exit protection. This is a **design choice**: maintain optimization on entry side, while maintaining simplicity on exit side.

### 4.1 ROI Ladder Take-Profit

```python
minimal_roi = {
    "0": 0.028,    # 0-10 minutes: 2.8%
    "10": 0.018,   # 10-40 minutes: 1.8%
    "40": 0.005,   # 40-180 minutes: 0.5%
    "180": 0.018   # 180+ minutes: 1.8%
}
```

### 4.2 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.025
```

### 4.3 Custom Stoploss

```python
if holding_time < 50 minutes:
    Don't actively stoploss
else:
    if rsi_1h < 35:
        Continue holding
    elif still falling:
        Stoploss
```

---

## V. Technical Indicator System

### 5.1 5-Minute Cycle Indicators

| Indicator Name | Parameters | Usage |
|---------------|-----------|-------|
| EMA200 | 200 | Long-term trend judgment |
| EMA12/26 | 12,26 | MACD calculation |
| RSI | 14 | Momentum |
| Bollinger Bands | 20,2 | Overbought/oversold |
| Volume Mean | 48 | Volume anomaly detection |
| CMF | 20 | Capital flow judgment |

### 5.2 1-Hour Cycle Indicators

| Indicator Name | Parameters | Usage |
|---------------|-----------|-------|
| EMA50 | 50 | Mid-term trend |
| EMA200 | 200 | Long-term trend confirmation |
| RSI | 14 | 1-hour momentum |
| Bollinger Bands | 20,2 | 1-hour overbought/oversold |

---

## VI. Risk Management Features

### 6.1 50-Minute Observation Period

Strategy doesn't actively stoploss within first 50 minutes, giving market time to rebound.

### 6.2 RSI Exception

If 1-hour RSI still very low (< 35) after 50 minutes, continue holding, avoid stoplossing at lowest point.

### 6.3 Volume Protection

All conditions include volume filtering, exclude zombie coins and pumpdump situations.

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Parameter Optimized**: More suitable for actual market environment
2. **More Precise Signals**: Stricter volume filtering excludes false signals
3. **More Entry Opportunities**: Relaxed RSI thresholds increase signal volume
4. **Maintains Simplicity**: No BigZ0307HO's complex exit logic
5. **Easy to Understand**: Logic clear, easy to debug

### ⚠️ Limitations

1. **Overfitting Risk**: Optimized parameters may only be effective in specific periods
2. **Condition 4 Change Too Big**: RSI from 16.5 → 39.8 may cause signal flooding
3. **Deep Lower Band Too Aggressive**: 0.766 threshold may buy continuously falling coins
4. **Trading Frequency May Increase**: Looser conditions mean more trades

---

## VIII. Applicable Scenarios

### 8.1 Recommended Scenarios

- **Wide range oscillation**
- **Range upward**
- **High liquidity major coins**

### 8.2 Not Recommended Scenarios

- **Sideways range market** (easily repeatedly stopped out)
- **Continuous decline market** (each oversold may continue falling)
- **Low volatility coins** (difficult to trigger take-profit)

---

## IX. Summary

BigZ03HO is a **"parameter upgraded"** version of BigZ03, achieving "same logic, more precise parameters" through HyperOpt optimization.

**Key Points**:
- ✅ Parameter optimized, more suitable for actual markets
- ✅ Stricter volume filtering, exclude false signals
- ✅ More entry opportunities, relaxed RSI limits
- ⚠️ Overfitting risk, optimized parameters may fail in future
- ⚠️ Trading frequency may increase

**Usage Recommendations**:
1. First run BigZ03: Understand original version behavior
2. Comparative testing: Run both versions simultaneously, compare effects
3. Monitor condition 4: RSI relaxed may cause signals to increase, need filtering
4. Record parameter effects: Which optimizations are useful, which may be overfitting

---

*This document is based on BigZ03HO strategy source code, for learning reference only, not investment advice.*
