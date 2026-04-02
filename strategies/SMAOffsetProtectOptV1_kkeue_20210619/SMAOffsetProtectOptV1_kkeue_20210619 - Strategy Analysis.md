# SMAOffsetProtectOptV1_kkeue_20210619 Strategy Analysis

> **Strategy ID**: #365 (365th of 465 strategies)  
> **Strategy Type**: SMA Offset Protection Optimization + EWO Filter + Trend Following  
> **Timeframe**: 5 minutes (5m) + 1 hour informative layer

---

## 1. Strategy Overview

SMAOffsetProtectOptV1_kkeue_20210619 is a protection optimization strategy based on Simple Moving Average offset (SMA Offset), combined with the Elliott Wave Oscillator (EWO) indicator as a trend filter. This strategy identifies buying opportunities through price offset relative to SMA, while using EWO to distinguish different market states, achieving flexible trading with multiple entry conditions.

This strategy is an optimized version of the SMAOffset series, modified and published by community user kkeue on June 19, 2021. It adds EWO protection mechanisms and more refined parameter tuning on top of the original SMA Offset logic.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signals, can trigger independently (OR logic) |
| **Sell Conditions** | 1 base sell signal + tiered ROI take-profit + trailing stop |
| **Protection Mechanism** | EWO high/low threshold filtering + RSI overbought protection |
| **Timeframe** | 5m (main) + 1h (informative layer) |
| **Dependencies** | talib, numpy, qtpylib, technical.indicators |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.028,    # Immediate: 2.8%
    "10": 0.018,   # After 10 minutes: 1.8%
    "30": 0.010,   # After 30 minutes: 1.0%
    "40": 0.005    # After 40 minutes: 0.5%
}

# Stop loss setting
stoploss = -0.10   # Fixed stop loss -10%

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.001        # Activate after 0.1% profit
trailing_stop_positive_offset = 0.01  # Activation offset 1%
trailing_only_offset_is_reached = True
```

**Design Philosophy**:
- ROI uses a tiered decreasing design, encouraging the strategy to take profits early
- 10% fixed stop loss provides basic protection
- Trailing stop uses a "delayed activation" mechanism, only starting to trail after 1% profit to avoid being stopped out by normal volatility

### 2.2 Order Type Configuration

```python
# Sell signal configuration
use_sell_signal = True
sell_profit_only = True          # Use sell signal only when profitable
sell_profit_offset = 0.01        # Consider signal sell only above 1% profit
ignore_roi_if_buy_signal = False # Don't ignore ROI when there's a buy signal
```

---

## 3. Buy Conditions Detailed Analysis

### 3.1 Core Indicator System

The strategy relies on the following technical indicators for trading decisions:

| Indicator | Parameters | Purpose |
|-----------|------------|---------|
| **SMA Buy** | Default 16 periods (optimizable 5-80) | Calculate buy reference price |
| **SMA Sell** | Default 20 periods (optimizable 5-80) | Calculate sell reference price |
| **EWO** | Fast 50 / Slow 200 | Elliott Wave Oscillator, trend judgment |
| **RSI** | 14 periods | Relative Strength Index, prevent overbought chasing |

### 3.2 Buy Parameter Configuration

```python
# Optimizable buy parameters
base_nb_candles_buy = IntParameter(5, 80, default=16)   # SMA period
low_offset = DecimalParameter(0.9, 0.99, default=0.973) # Price offset coefficient
ewo_high = DecimalParameter(2.0, 12.0, default=5.672)   # EWO high threshold
ewo_low = DecimalParameter(-20.0, -8.0, default=-19.931) # EWO low threshold
rsi_buy = IntParameter(30, 70, default=59)               # RSI threshold

# Fixed EWO parameters
fast_ewo = 50   # EWO fast period
slow_ewo = 200  # EWO slow period
```

### 3.3 Two Buy Conditions Detailed

#### Condition #1: EWO High Value + RSI Protected Buy
```python
# Trigger conditions
- Close price < SMA(16) × 0.973 (price 2.7% below moving average)
- EWO > 5.672 (Elliott Wave Oscillator is positive and relatively high)
- RSI < 59 (relative strength not overbought)
- Volume > 0
```

**Logic Interpretation**:
- Price retraces to about 2.7% below the moving average, a pullback buy
- EWO high positive value indicates being in an upward trend correction
- RSI limit prevents buying when overly chasing highs

#### Condition #2: EWO Low Value Bottom-Fishing Buy
```python
# Trigger conditions
- Close price < SMA(16) × 0.973 (price 2.7% below moving average)
- EWO < -19.931 (Elliott Wave Oscillator is deeply negative)
- Volume > 0
```

**Logic Interpretation**:
- Price is also 2.7% below the moving average
- EWO deep negative value indicates possibly being in an oversold state at the end of a downtrend
- No RSI limit, allows bottom fishing during panic

### 3.4 Buy Condition Classification Summary

| Condition Group | Condition ID | Core Logic | Applicable Scenario |
|----------------|-------------|------------|---------------------|
| Trend Pullback | #1 | EWO high positive + Price offset + RSI protection | Healthy pullback in uptrend |
| Panic Bottom-Fishing | #2 | EWO deep negative + Price offset | Oversold bounce at end of downtrend |

---

## 4. Sell Logic Detailed Analysis

### 4.1 Tiered ROI Take-Profit System

The strategy uses a four-tier ROI mechanism:

```
Holding Time        Target Profit
──────────────────────────
Immediate          2.8%
After 10 minutes   1.8%
After 30 minutes   1.0%
After 40 minutes   0.5%
```

**Design Intent**:
- Early stage (0-10 minutes): Pursue higher returns
- Mid stage (10-40 minutes): Gradually lower expectations
- Long term (40+ minutes): Accept minimal profit exit

### 4.2 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_stop_positive = 0.001         # Start trailing after 0.1% profit
trailing_stop_positive_offset = 0.01   # Activate after 1% profit
trailing_only_offset_is_reached = True  # Only activate after offset is reached
```

**Working Mechanism**:
1. Trailing stop activates when position profit reaches 1%
2. Stop loss line rises as price increases
3. Price retraces 0.1% triggers stop

### 4.3 Sell Signal Conditions

```python
# Sell signal (only effective when profitable)
- Close price > SMA(20) × 1.010 (price 1% above moving average)
- Volume > 0
```

**Parameter Description**:
```python
base_nb_candles_sell = IntParameter(5, 80, default=20)
high_offset = DecimalParameter(0.99, 1.1, default=1.010)
```

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|---------------------|---------|
| Trend | SMA (5-80 periods adjustable) | Price offset reference baseline |
| Oscillator | EWO (50/200 EMA difference) | Trend direction judgment |
| Momentum | RSI (14 periods) | Overbought/oversold judgment |
| Volume | Volume | Liquidity confirmation |

### 5.2 Elliott Wave Oscillator (EWO) Detailed

EWO is the core protection indicator of this strategy, calculated as follows:

```python
def EWO(dataframe, ema_length=5, ema2_length=35):
    ema1 = ta.EMA(dataframe, timeperiod=ema_length)
    ema2 = ta.EMA(dataframe, timeperiod=ema2_length)
    emadif = (ema1 - ema2) / dataframe['close'] * 100
    return emadif
```

In this strategy, 50/200 parameter combination is used:
- **Positive value (> 0)**: Indicates short-term MA above long-term MA, in an uptrend
- **Negative value (< 0)**: Indicates short-term MA below long-term MA, in a downtrend
- **High positive value (> ewo_high)**: Strong uptrend, pullback buying opportunity
- **Deep negative value (< ewo_low)**: Deep downtrend, possible oversold bounce

---

## 6. Risk Management Features

### 6.1 Multi-Layer Stop Loss Protection

| Stop Loss Type | Parameter | Function |
|---------------|-----------|----------|
| Fixed stop loss | -10% | Basic protection against extreme losses |
| Trailing stop | 0.1%/1% | Lock in profits, let profits run |
| ROI take-profit | Tiered decreasing | Control holding time, reduce risk |

### 6.2 EWO Bidirectional Protection Mechanism

The strategy uses EWO for bidirectional entry:

- **ewo_high (positive direction)**: Pullback buy in uptrend, utilize momentum continuation
- **ewo_low (negative direction)**: Bottom fish at oversold bottom, capture rebound opportunity

### 6.3 RSI Anti-Chasing Mechanism

The RSI < 59 limit in condition #1 prevents chasing highs when price has already risen strongly.

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Dual Entry Mechanism**: Can capture both trend pullbacks and oversold rebounds, adapting to multiple market states
2. **Optimizable Parameters**: Five buy parameters can all be optimized through HyperOpt, adapting to different trading pairs
3. **Multi-Layer Risk Control**: Fixed stop loss + trailing stop + tiered ROI, triple protection
4. **Trend Filtering**: EWO indicator effectively distinguishes trend states, avoids counter-trend trading

### ⚠️ Limitations

1. **Parameter Sensitivity**: Default parameters are optimized for specific periods, may not apply to current market
2. **Ranging Market Risk**: May trigger frequent stop losses in sideways oscillation
3. **Unused Informative Layer**: Although 1h informative timeframe is configured, it's not actually used in main logic
4. **HyperOpt Overfitting Risk**: Optimized parameters may be overfitted to historical data

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Uptrend | Default parameters | Many pullback buying opportunities |
| Ranging market | Reduce low_offset, increase RSI threshold | Reduce false signals |
| Downtrend | Lower ewo_low threshold | Reduce bottom-fishing signal frequency |
| High volatility | Increase stop loss amplitude | Avoid being stopped out by normal volatility |

---

## 9. Applicable Market Environment Detailed

SMAOffsetProtectOptV1_kkeue_20210619 belongs to the SMA Offset series and is a relatively mature version of this series. Based on its code architecture and long-term community live trading verification, it is most suitable for **markets with clear trends**, and performs poorly in **severe oscillation or one-sided decline**.

### 9.1 Strategy Core Logic

- **Price Offset Entry**: Enter when price is below moving average by a certain percentage, looking for "cheap" entry points
- **EWO Bidirectional Filtering**: Distinguish between "pullback in uptrend" and "oversold in downtrend"
- **Tiered Take-Profit Exit**: The longer the holding time, the lower the target, control holding cycle

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:------------------|:----------------|
| 📈 Slow bull trend | ⭐⭐⭐⭐⭐ | Many pullback buying opportunities, trailing stop can lock profits |
| 🔄 Sideways oscillation | ⭐⭐☆☆☆ | Frequent touching of offset lines, increasing stop loss count |
| 📉 One-sided decline | ⭐⭐☆☆☆ | Bottom-fishing signals may catch falling knives |
| ⚡️ Severe volatility | ⭐⭐⭐☆☆ | Trailing stop can protect, but entry timing is hard to grasp |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|------------------|-------------|
| Trading pair | Major coin/stablecoin pairs | Good liquidity, relatively clear trend |
| Stop loss | -8% ~ -12% | Adjust according to trading pair volatility |
| Trailing stop offset | 0.8% ~ 1.2% | Balance profit locking with volatility tolerance |

---

## 10. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

Although this strategy has limited code, it involves multiple technical indicators:
- Need to understand the meaning of SMA offset
- Need to master EWO indicator interpretation
- Need to understand trailing stop working mechanism
- Need to be familiar with HyperOpt parameter optimization process

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-5 pairs | 2GB | 4GB |
| 5-20 pairs | 4GB | 8GB |
| 20+ pairs | 8GB | 16GB |

### 10.3 Difference Between Backtesting and Live Trading

- **Backtesting advantage**: Historical data performance may have been parameter optimized
- **Live trading risk**: Factors such as slippage, delay, insufficient liquidity may cause actual performance to be lower than backtesting
- **Recommendation**: Test with paper trading first, then verify with small capital live trading

### 10.4 Suggestions for Manual Traders

If you want to manually use the logic of this strategy:
1. Use 16-period SMA as reference line
2. Pay attention when price is 2.7% below SMA
3. Use EWO (50/200 EMA difference) to judge trend
4. Set 10% stop loss and trailing take-profit

---

## 11. Summary

**SMAOffsetProtectOptV1_kkeue_20210619** is a **trend-following strategy with clear structure and explicit logic**. Its core value lies in:

1. **Dual Entry Mechanism**: Can both pullback buy and bottom fish oversold
2. **Multi-Layer Risk Control System**: Fixed stop loss + trailing stop + tiered ROI
3. **Optimizable Parameters**: Adapt to different market environments
4. **Clean Code**: Easy to understand and further develop

For quantitative traders, this is a strategy framework that can serve as a starting point for extension and optimization. It is recommended to conduct sufficient backtesting and paper trading verification before actual use, and adjust parameters according to the characteristics of specific trading pairs.