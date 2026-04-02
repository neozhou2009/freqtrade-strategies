# BigPete Strategy Analysis

> **Strategy Number**: #55  
> **Strategy Type**: BigZ04 Improved Version with Adaptive Trailing Stop  
> **Timeframe**: 5 minutes (5m) + Information Timeframe 1h

---

## I. Strategy Overview

BigPete is an improved quantitative trading strategy based on BigZ04, developed by Perkmeister. This strategy adds a **custom trailing stop system** on top of BigZ04, achieving more flexible risk-reward management. Its core design philosophy is to **pursue larger profits in trend situations while controlling maximum drawdown**.

### Core Features

| Feature | Configuration Value |
|---------|-------------------|
| Timeframe | 5 minutes (5m) |
| Information Timeframe | 1 hour (1h) |
| Take-Profit (ROI) | 0-30 min: 10%, 30-60 min: 5%, 60+ min: 2% |
| Stoploss | -0.99 (disable default stoploss, use custom stoploss) |
| Trailing Stop | Enabled, adaptive trailing stop system |
| Number of Entry Conditions | 13 independent conditions |
| Recommended Number of Pairs | 2-4 (suggested) |
| Features | Dynamic trailing stop + layered take-profit |

---

## II. Strategy Configuration Analysis

### 2.1 Base Configuration

```python
timeframe = "5m"
inf_1h = "1h"
minimal_roi = {
    "0": 0.10,    # Immediate 10% profit on entry
    "30": 0.05,   # 5% after 30 minutes
    "60": 0.02    # 2% after 60 minutes
}
stoploss = -0.99  # Disable default stoploss
trailing_stop = True
trailing_stop_positive = 0.003
trailing_stop_positive_offset = 0.0187
```

### 2.2 Trailing Stop Parameters (Core Feature)

```python
# Hard stoploss threshold
pHSL = -0.08  # Forced stoploss if loss exceeds 8%

# Profit threshold 1 (triggers first-level trailing)
pPF_1 = 0.016  # 1.6% profit triggers
pSL_1 = 0.011  # Corresponding stoploss 1.1%

# Profit threshold 2 (triggers second-level trailing)
pPF_2 = 0.080  # 8% profit triggers
pSL_2 = 0.040  # Corresponding stoploss 4%

# Dynamic stoploss formula
# Profit > 8%: sl_profit = 4% + (current profit - 8%)
# Profit 1.6%-8%: sl_profit = 1.1% + (current profit - 1.6%) × ratio
# Profit < 1.6%: sl_profit = -8% (hard stoploss)
```

### 2.3 Key Parameters

```python
# Volume parameters
buy_volume_pump_1 = 0.1    # Volume ratio compared to 48-period mean
buy_volume_drop_1 = 5.4    # Volume contraction multiple

# RSI parameters
buy_rsi_1h_0 = 81.7        # High RSI (condition 0)
buy_rsi_1h_1 = 14.2        # Low RSI (conditions 1-4)
buy_rsi_0 = 11.2           # 5-minute RSI
buy_rsi_1 = 15.7
buy_rsi_2 = 11.3

# MACD parameters
buy_macd_1 = 0.05
buy_macd_2 = 0.03
```

---

## III. Entry Conditions Details

BigPete contains **13 independent entry conditions**:

### 3.1 Condition 0: High RSI + Price Decline Pattern

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["rsi"] < 11.2) &
((dataframe["close"] * 1.029 < dataframe["open"].shift(3)) | 
 (dataframe["close"] * 1.029 < dataframe["open"].shift(2)) |
 (dataframe["close"] * 1.029 < dataframe["open"].shift(1))) &
(dataframe["rsi_1h"] < 81.7)
```

**Logic**: Price above EMA200 but RSI extremely low (11.2), indicates although long-term bullish but short-term oversold. Significant decline within consecutive 3 days.

### 3.2 Condition 1: Lower Bollinger Band + Bearish Candle

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["close"] > dataframe["ema_200_1h"]) &
(dataframe["close"] < dataframe["bb_lowerband"] * 0.999) &
(dataframe["rsi_1h"] < 67.8) &
(dataframe["open"] > dataframe["close"])
```

**Logic**: Price near lower Bollinger Band, bearish close, 1-hour RSI moderate.

### 3.3 Condition 2: Deep Lower Band

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["close"] < dataframe["bb_lowerband"] * 1.01)
```

**Logic**: Looser lower band condition, just needs to approach Bollinger Band.

### 3.4 Condition 3: Above 1-hour EMA200 + RSI Oversold

```python
(dataframe["close"] > dataframe["ema_200_1h"]) &
(dataframe["close"] < dataframe["bb_lowerband"]) &
(dataframe["rsi"] < 35.6)
```

### 3.5 Condition 4: Extremely Low 1-hour RSI

```python
(dataframe["rsi_1h"] < 16.5) &
(dataframe["close"] < dataframe["bb_lowerband"])
```

### 3.6 Condition 5: MACD Golden Cross + Lower Bollinger Band

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["close"] > dataframe["ema_200_1h"]) &
(dataframe["ema_26"] > dataframe["ema_12"]) &
((dataframe["ema_26"] - dataframe["ema_12"]) > (dataframe["open"] * 0.05)) &
(dataframe["close"] < dataframe["bb_lowerband"])
```

### 3.7 Conditions 6-7: MACD Different Parameter Combinations

Similar to condition 5, but using different RSI and MACD parameter thresholds.

### 3.8 Conditions 8-9: Dual RSI Oversold

```python
(dataframe["rsi_1h"] < threshold) &
(dataframe["rsi"] < threshold)
```

### 3.9 Condition 10: 1-hour Oversold + MACD Reversal

```python
(dataframe["rsi_1h"] < 31.3) &
(dataframe["close_1h"] < dataframe["bb_lowerband_1h"]) &
(dataframe["hist"] > 0) &
(dataframe["hist"].shift(2) < 0) &
(dataframe["rsi"] < 40.5)
```

### 3.10 Condition 11: Volume Narrow Range Oscillation

```python
# Consecutive 10 candles range < 1%
((dataframe["high"] - dataframe["low"]) < dataframe["open"] / 100)
```

### 3.11 Condition 12: False Breakout Pattern

```python
(dataframe["close"] < dataframe["bb_lowerband"] * 0.993) &
(dataframe["low"] < dataframe["bb_lowerband"] * 0.985) &
(dataframe["close"].shift() > dataframe["bb_lowerband"])
```

---

## IV. Exit Logic Explained

### 4.1 Custom Trailing Stoploss (Core)

BigPete's biggest feature is its **adaptive trailing stop system**:

```python
def custom_stoploss(current_profit):
    HSL = -0.08  # Hard stoploss -8%
    PF_1 = 0.016  # 1.6% profit threshold
    SL_1 = 0.011  # 1.1% corresponding stoploss
    PF_2 = 0.080  # 8% profit threshold
    SL_2 = 0.040  # 4% corresponding stoploss
    
    if current_profit > PF_2:
        # Profit > 8%: stoploss line moves up, lock more profits
        sl_profit = SL_2 + (current_profit - PF_2)
    elif current_profit > PF_1:
        # Profit 1.6%-8%: linear interpolation
        sl_profit = SL_1 + ((current_profit - PF_1) * (SL_2 - SL_1) / (PF_2 - PF_1))
    else:
        # Profit < 1.6%: use hard stoploss -8%
        sl_profit = HSL
    
    return stoploss_from_open(sl_profit, current_profit)
```

**Logic Interpretation**:
- Profit < 1.6%: Maximum loss 8% (hard stoploss protection)
- Profit 1.6%-8%: Stoploss line moves up, 1.1% → 4%
- Profit > 8%: Stoploss line follows profit increase, lock most profits

### 4.2 Profit Protection Mechanism Diagram

```
Profit:   -8%   0%    1.6%   4%    8%    12%   16%   20%
          |-----|-----|------|-----|-----|-----|-----|
Stoploss: -8%  -8%   -8%   -1.1% -4%   -8%  -12%  -16%
                 (Hard)    (Dynamic Rise)
```

### 4.3 ROI Time Take-Profit

```python
minimal_roi = {
    "0": 0.10,    # 10% profit on entry!
    "30": 0.05,   # 5% after 30 minutes
    "60": 0.02    # 2% after 60 minutes
}
```

**Note**: Due to using trailing stop, ROI mainly plays role in early stage.

---

## V. Technical Indicator System

### 5.1 5-Minute Cycle Indicators

| Indicator Name | Parameters | Usage |
|---------------|-----------|-------|
| EMA200 | 200 | Long-term trend judgment |
| EMA12/26 | 12,26 | MACD calculation |
| SMA5 | 5 | Short-term trend |
| RSI | 14 | Momentum |
| Bollinger Bands | 20,2 | Overbought/oversold |
| ATR | 14 | Volatility |

### 5.2 1-Hour Cycle Indicators

| Indicator Name | Parameters | Usage |
|---------------|-----------|-------|
| SMA50 | 50 | Mid-term trend |
| SMA200 | 200 | Long-term trend |
| RSI | 14 | 1-hour momentum |
| Bollinger Bands | 20,2 | Overbought/oversold |

---

## VI. Risk Management Features

### 6.1 Adaptive Stoploss System

BigPete's core innovation is **dynamically adjusting stoploss line based on profit**:

1. **Loss Phase** (profit < 1.6%):
   - Hard stoploss -8%
   - Allow certain floating loss room

2. **Initial Profit Phase** (profit 1.6%-8%):
   - Stoploss line moves up to -1.1% to -4%
   - Protect existing profits

3. **Large Profit Phase** (profit > 8%):
   - Stoploss line follows increase
   - Always lock at least 4% profit

### 6.2 Differences from BigZ04

| Feature | BigZ04 | BigPete |
|---------|--------|---------|
| Stoploss Type | Fixed time stoploss | Adaptive trailing stoploss |
| Hard Stoploss | -10% | -8% |
| Trailing Stop | None | Yes |
| Profit Target | Ladder ROI | 10% first target |

---

## VII. Strategy Pros & Cons

### 7.1 Advantages

1. **Flexible Stoploss**: Automatically adjusts based on profit, controllable risk
2. **Trend Following**: Can capture more profits in big trends
3. **Multi-Condition Coverage**: 13 conditions cover various patterns
4. **Dual Verification**: 5-minute + 1-hour timeframe

### 7.2 Limitations

1. **Complex Parameters**: Multiple threshold parameters difficult to optimize
2. **High Target**: 10% first target may cause some trades to fail
3. **Volatility Sensitive**: Trailing stop may be triggered by normal fluctuations

---

## VIII. Applicable Scenarios

### 8.1 Recommended Scenarios

- **Pullbacks in strong trends**
- **High volatility markets**
- **Major cryptocurrency pairs**

### 8.2 Not Recommended Scenarios

- **Low volatility sideways**
- **Violently volatile junk coins**
- **Scenarios requiring quick trading**

---

## IX. Applicable Market Environments Explained

### 9.1 Ideal Environment

1. **Clear trends**: Single-sided rise or decline followed by pullback
2. **Normal volatility**: Daily volatility 5-15%
3. **High liquidity**: Major coins

### 9.2 Warning Environments

- ⚠️ Sideways range (high trading frequency, low win rate)
- ⚠️ Sharp decline situations (hard stoploss will trigger)
- ⚠️ Extreme volatility (trailing stop too narrow)

---

## X. Important Reminders: The Cost of Complexity

### 10.1 Cost of Trailing Stop

Although trailing stop can protect profits, it also has costs:

1. **Normal Pullback Trigger**: Normal fluctuations in trends may trigger stoploss
2. **Parameter Sensitivity**: PF_1, PF_2 and other parameters need fine adjustment
3. **Complexity Increase**: Difficult to understand actual P&L sources

### 10.2 Recommendations

1. **Observe First**: Run with default values for 2 weeks
2. **Record Trades**: Analyze which stoplosses were "correct"
3. **Adjust Cautiously**: Only change one parameter at a time

---

## XI. Summary

BigPete is an **enhanced version of BigZ04**, achieving smarter risk management through adaptive trailing stop system:

- ✅ 13 entry conditions, cover various patterns
- ✅ Trailing stop, protect profits
- ✅ 8% hard stoploss, control maximum loss
- ⚠️ Complex parameters, need time to understand
- ⚠️ 10% first target relatively high

**Suitable for**: Traders with certain experience, pursuing steady profit growth.

---

*This document is based on BigPete.py code auto-generated*
