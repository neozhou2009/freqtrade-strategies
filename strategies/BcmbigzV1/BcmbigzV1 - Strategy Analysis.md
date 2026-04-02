# BcmbigzV1 Strategy Analysis

> **Strategy Number**: #54  
> **Strategy Type**: Bollinger Band + RSI + MACD Multi-Condition Strategy  
> **Timeframe**: 5 minutes (5m) + Information Timeframe 1h

---

## I. Strategy Overview

BcmbigzV1 is a quantitative trading strategy based on Bollinger Bands, RSI, MACD and other technical indicators, derived from a variant of the BigZ series. The core design philosophy of this strategy is to **buy coins in oversold state during market pullbacks, pursuing quick profit-taking**.

### Core Features

| Feature | Configuration Value |
|---------|-------------------|
| Timeframe | 5 minutes (5m) |
| Information Timeframe | 1 hour (1h) |
| Take-Profit (ROI) | 0-10 min: 3.8%, 10-40 min: 2.8%, 40-180 min: 1.5%, 180+ min: 1.8% |
| Stoploss | -0.99 (disable default stoploss, use custom stoploss) |
| Trailing Stop | Enabled, positive offset 1%, trigger offset 2.5% |
| Number of Entry Conditions | 14 independent conditions |
| Recommended Number of Pairs | 2-4 (suggested) |
| Holding Time | Short-term biased, relatively short average |

---

## II. Strategy Configuration Analysis

### 2.1 Base Configuration

```python
timeframe = "5m"
inf_1h = "1h"
minimal_roi = {
    "0": 0.038,    # Immediate 3.8% profit on entry
    "10": 0.028,   # 2.8% after 10 minutes
    "40": 0.015,   # 1.5% after 40 minutes
    "180": 0.018   # 1.8% after 180 minutes
}
stoploss = -0.99  # Disable default stoploss
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.025
```

### 2.2 Key Parameter Explanation

**volume_pump Parameter**:
- `buy_volume_pump_1`: 0.4 (default) - Controls threshold for 48-period volume mean vs previous period comparison

**volume_drop Parameters**:
- `buy_volume_drop_1`: 3.8 - Current volume must be less than previous candle volume multiplier
- `buy_volume_drop_2`: 3.0
- `buy_volume_drop_3`: 2.7

**RSI Threshold Parameters**:
- 1-hour RSI multiple levels: 16.5, 15.0, 20.0, 35.0, 39.0
- 5-minute RSI: 28.0, 10.0, 14.2

**Bollinger Band Proximity Parameters**:
- `bzv7_buy_bb20_close_bblowerband_safe_1`: 0.989
- `bzv7_buy_bb20_close_bblowerband_safe_2`: 0.982

---

## III. Entry Conditions Details

BcmbigzV1 contains **14 independent entry conditions**, each representing a specific market pattern. Any condition being satisfied triggers an entry signal.

### 3.1 Condition 0: RSI Oversold + Price Decline Pattern

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["rsi"] < 30) &
(dataframe["close"] * 1.024 < dataframe["open"].shift(3)) &
(dataframe["rsi_1h"] < 71)
```

**Logic**: Price stands above 200-day EMA, 5-minute RSI below 30 (oversold), consecutive 3 candles price decline, 1-hour RSI below 71.

### 3.2 Condition 1: Lower Bollinger Band Rebound + Volume Contraction

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["close"] > dataframe["ema_200_1h"]) &
(dataframe["close"] < dataframe["bb_lowerband"] * 0.989) &
(dataframe["rsi_1h"] < 69) &
(dataframe["open"] > dataframe["close"])
```

**Logic**: Price near lower Bollinger Band (0.989x), close is bearish (upper shadow), 1-hour RSI below 69, volume contraction.

### 3.3 Condition 2: Deep Lower Band

```python
(dataframe["close"] > dataframe["ema_200"]) &
(dataframe["close"] < dataframe["bb_lowerband"] * 0.982)
```

**Logic**: More aggressive entry, near lower Bollinger Band (0.982x), lower requirements for RSI and volume.

### 3.4 Condition 3: Above 1-hour EMA200 + RSI Oversold

```python
(dataframe["close"] > dataframe["ema_200_1h"]) &
(dataframe["close"] < dataframe["bb_lowerband"]) &
(dataframe["rsi"] < 14.2)
```

**Logic**: 1-hour trend upward (price > EMA200), 5-minute price touches lower Bollinger Band, RSI deeply oversold (14.2).

### 3.5 Condition 4: Extremely Low 1-hour RSI + Lower Bollinger Band

```python
(dataframe["rsi_1h"] < 16.5) &
(dataframe["close"] < dataframe["bb_lowerband"])
```

**Logic**: 1-hour RSI at extremely low level (16.5), price at lower Bollinger Band.

### 3.6 Conditions 5-6: MACD Golden Cross Pattern

```python
(dataframe["ema_26"] > dataframe["ema_12"]) &
((dataframe["ema_26"] - dataframe["ema_12"]) > (dataframe["open"] * 0.02))
```

**Logic**: MACD in golden cross state (fast line > slow line), and difference is large enough, simultaneously price at lower Bollinger Band.

### 3.7 Conditions 7: MACD + Extremely Low 1-hour RSI

```python
(dataframe["rsi_1h"] < 15.0) &
(dataframe["ema_26"] > dataframe["ema_12"]) &
(Condition 5 golden cross logic)
```

### 3.8 Conditions 8-9: Dual RSI Oversold Combination

```python
(dataframe["rsi_1h"] < threshold) &
(dataframe["rsi"] < threshold)
```

### 3.9 Condition 10: 1-hour Oversold + MACD Reversal

```python
(dataframe["rsi_1h"] < 35.0) &
(dataframe["close_1h"] < dataframe["bb_lowerband_1h"]) &
(dataframe["hist"] > 0) &
(dataframe["hist"].shift(2) < 0)  # MACD from negative to positive
```

### 3.10 Condition 11: Volume Anomaly + CMF Outflow

```python
(dataframe["close"] > dataframe["ema_200_1h"]) &
(dataframe["cmf"] < -0.435) &
(dataframe["rsi"] < 22)
```

**Logic**: 1-hour price upward, capital flow (CMF) significantly outflowing, may be prelude to main force accumulation followed by rally.

### 3.11 Condition 12: False Breakout Pattern

```python
(dataframe["close"] < dataframe["bb_lowerband"] * 0.993) &
(dataframe["low"] < dataframe["bb_lowerband"] * 0.985) &
(dataframe["close"].shift() > dataframe["bb_lowerband"])
```

**Logic**: Price briefly breaks below lower Bollinger Band then quickly recovers, forming false breakout (bull flag pattern).

---

## IV. Exit Logic Explained

### 4.1 ROI Take-Profit Strategy

The strategy uses time-based ROI (Return on Investment) take-profit:

| Holding Time | Take-Profit Ratio |
|-------------|------------------|
| 0-10 minutes | 3.8% |
| 10-40 minutes | 2.8% |
| 40-180 minutes | 1.5% |
| 180+ minutes | 1.8% |

### 4.2 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_stop_positive = 0.01      # 1% trailing
trailing_stop_positive_offset = 0.025  # 2.5% trigger
```

### 4.3 Custom Stoploss (custom_stoploss)

```python
if current_profit > 0:
    return 0.99  # No stoploss trigger when profitable
else:
    # After holding for more than 50 minutes
    if current holding time > 50 minutes:
        # If 1-hour RSI < 40, wait for recovery
        if rsi_1h < 40:
            return 0.99
        # If price above EMA200 and still falling, 1% stoploss
        if current price * 1.025 < entry candle open:
            return 0.01
```

**Core Logic**: The strategy assumes profits should be made within 50 minutes; if losing, it indicates wrong judgment, immediately stoploss.

---

## V. Technical Indicator System

### 5.1 5-Minute Cycle Indicators

| Indicator Name | Calculation Parameters | Usage |
|---------------|----------------------|-------|
| Bollinger Bands | Period 20, Std Dev 2 | Identify overbought/oversold |
| EMA200 | Period 200 | Long-term trend judgment |
| EMA12/26 | Period 12,26 | MACD calculation |
| RSI | Period 14 | Momentum judgment |
| Volume Mean | Period 48 | Volume anomaly detection |
| CMF (Capital Flow) | Period 20 | Capital flow judgment |

### 5.2 1-Hour Cycle Indicators (Information Cycle)

| Indicator Name | Calculation Parameters | Usage |
|---------------|----------------------|-------|
| EMA50 | Period 50 | Mid-term trend |
| EMA200 | Period 200 | Long-term trend confirmation |
| RSI | Period 14 | 1-hour momentum |
| Bollinger Bands | Period 20, Std Dev 2 | 1-hour overbought/oversold |

---

## VI. Risk Management Features

### 6.1 Composite Risk Control System

1. **Time Stoploss**: 50-minute forced stoploss line
2. **Trailing Stop**: Ensures profits aren't swallowed
3. **ROI Ladder**: Take-profit by time periods
4. **Custom Conditional Stoploss**: Dynamically adjust based on RSI and price pattern

### 6.2 Risk Control Parameters

```python
# Volume filtering
buy_volume_pump_1 = 0.4  # Volume cannot be at recent high
buy_volume_drop_1 = 3.8  # Volume needs to contract to below 1/3.8
```

### 6.3 Potential Risks

- 14 entry conditions too loose may lead to overtrading
- Short timeframe (5 minutes) easily generates false signals
- ROI take-profit may miss major trend moves

---

## VII. Strategy Pros & Cons

### 7.1 Advantages

1. **Parallel Multi-Conditions**: 14 independent entry conditions, cover various market patterns
2. **Dual Timeframe**: Combine 5-minute and 1-hour indicators, filter false signals
3. **Quick Stoploss**: 50-minute time stoploss controls maximum drawdown
4. **Trend Confirmation**: Requires price above EMA200, reduces counter-trend trading
5. **Capital Flow**: Introduces CMF indicator to judge capital movement

### 7.2 Limitations

1. **Many Parameters**: 14 conditions × multiple parameters, difficult optimization
2. **Trading Frequency**: Many conditions may lead to too frequent trading
3. **Fixed Parameters**: Some thresholds hardcoded, lacks adaptive capability
4. **Bull Market Bias**: Requires price above EMA200, may perform poorly in range markets

---

## VIII. Applicable Scenarios

### 8.1 Recommended Scenarios

- **Pullback buying in bull market or uptrend**
- **High volatility coins** (such as major coins, altcoins)
- **High liquidity pairs** (avoid liquidity risk)

### 8.2 Not Recommended Scenarios

- **Sideways range market** (easily repeatedly stopped out)
- **Sharp decline market** (high risk of catching falling knives)
- **Low liquidity coins** (large slippage)

### 8.3 Recommended Configuration

```json
{
    "max_open_trades": 3,
    "stake_currency": "USDT",
    "dry_run_wallet": 1000,
    "exit_profit_only": true
}
```

---

## IX. Applicable Market Environments Explained

### 9.1 Ideal Market Environment

1. **Healthy pullback in uptrend**:
   - Daily level in uptrend
   - Price pulls back to key support
   - Volume contraction (selling exhaustion)

2. **Breakout after Bollinger Band contraction**:
   - Bollinger Band upper/lower bands contract
   - Volume shrinks to low level
   - Wait for volume breakout direction

3. **RSI divergence pattern**:
   - Price makes new low, RSI doesn't make new low
   - Bottom divergence may be entry signal

### 9.2 Market Environment Warnings

- ⚠️ **Don't trade rebounds in downtrend**: Strategy requires price above EMA200
- ⚠️ **Don't buy after volume surge decline**: Volume abnormally high may be distribution
- ⚠️ **Don't trade high-level sideways**: Lack of volatility difficult to trigger take-profit

---

## X. Important Reminders: The Cost of Complexity

### 10.1 Overfitting Risk

BcmbigzV1 has 14 independent entry conditions, each containing multiple parameters. This complexity brings:

**Risks**:
- Historical backtests may overfit
- Performance may drop sharply in new market environments
- Difficult to understand real driving factors

**Recommendations**:
- Use default values for live testing
- Avoid frequent parameter adjustment
- Focus on long-term performance rather than short-term P&L

### 10.2 Execution Complexity

- Need to monitor multiple indicators simultaneously
- Multi-timeframe data synchronization
- Certain requirements for hardware and network

### 10.3 Monitoring Focus

1. **Daily trade count**: Too frequent indicates conditions too loose
2. **Average holding time**: Too long indicates unreasonable take-profit settings
3. **Win rate**: Check market environment adaptability if below 40%

---

## XI. Summary

BcmbigzV1 is a **trend pullback strategy with Bollinger Bands as core**, achieving multi-pattern entry through 14 independent conditions,combined with time stoploss and trailing take-profit for risk control.

**Key Points**:
- ✅ Suitable for bull market pullback situations
- ✅ Multi-conditions improve signal coverage
- ✅ Custom stoploss protects capital safety
- ⚠️ Many parameters need cautious optimization
- ⚠️ Trading frequency may be high

**Usage Recommendations**:
1. First use default parameters for simulated testing
2. Observe trading performance for 2-4 weeks
3. Adjust maximum position count based on market environment
4. Recommended to use with trend filtering indicators

---

*This document is based on BcmbigzV1.py code auto-generated*
