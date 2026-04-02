# BBRSI21 Strategy Analysis

> **Strategy Number**: #2 (2nd of 465 strategies)  
> **Strategy Type**: Bollinger Bands + RSI Mean Reversion  
> **Timeframe**: 5 minutes (5m)

---

## 1. Strategy Overview

**BBRSI21** is a classic mean reversion strategy ported by author Gert Wohlgemuth from the C# project Mynt to the Freqtrade platform. The core logic is straightforward: buy when price falls below the lower Bollinger Band and RSI is oversold, sell when price breaks above the upper Bollinger Band and RSI is extremely overbought.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 1 condition: Price < Lower Bollinger Band + RSI < 21 |
| **Exit Conditions** | 1 condition: Price > Upper Bollinger Band + RSI > 99 |
| **Protection** | No independent protection parameters, relies on trailing stop |
| **Timeframe** | 5 minutes |
| **Dependencies** | TA-Lib, technical (qtpylib) |

---

## 2. Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table (time: minimum profit)
minimal_roi = {
    "0": 0.22766,    # Immediate exit: 22.77% profit
    "31": 0.06155,   # After 31 minutes: 6.16% profit
    "78": 0.03227,   # After 78 minutes: 3.23% profit
    "105": 0         # After 105 minutes: exit at breakeven
}

# Stoploss setting
stoploss = -0.30054  # -30.05% hard stoploss

# Trailing stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.17832    # 17.83% trailing activation point
trailing_stop_positive_offset = 0.24807  # 24.81% offset trigger
```

**Design Logic**:
- **High ROI threshold**: First-level ROI set at 22.77%, indicating the strategy expects to capture larger moves
- **Loose stoploss**: -30% hard stoploss gives trades ample room to fluctuate
- **Aggressive trailing stop**: Requires 24.81% profit before trailing activates, with 17.83% trailing distance, suitable for trending markets

### 2.2 Order Type Configuration

Uses Freqtrade default configuration (not explicitly defined in strategy).

---

## 3. Entry Conditions Explained

### 3.1 Entry Logic

```python
# Entry conditions
dataframe.loc[
    (
        (dataframe["close"] < dataframe["bb_lowerband"])  # Price below lower Bollinger Band
        & (dataframe["rsi"] < 21)                         # RSI below 21 (oversold)
    ),
    "entry",
] = 1
```

**Logic Analysis**:
- **Lower Bollinger Band Break**: Price falling below the lower Bollinger Band indicates price is at a statistically low position
- **RSI Oversold Confirmation**: RSI < 21 is far below the traditional 30 oversold line, confirming extreme oversold conditions
- **Dual Confirmation**: Both conditions must be met to trigger entry, reducing false signals

### 3.2 Indicator Calculation

```python
# RSI calculation
dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

# Bollinger Bands calculation (20 periods, 2 standard deviations)
bollinger = qtpylib.bollinger_bands(
    qtpylib.typical_price(dataframe), window=20, stds=2
)
dataframe["bb_lowerband"] = bollinger["lower"]
dataframe["bb_middleband"] = bollinger["mid"]
dataframe["bb_upperband"] = bollinger["upper"]
```

---

## 4. Exit Logic Explained

### 4.1 Exit Conditions

```python
# Exit conditions
dataframe.loc[
    (
        (dataframe["close"] > dataframe["bb_upperband"])  # Price above upper Bollinger Band
        & (dataframe["rsi"] > 99)                          # RSI above 99 (extreme overbought)
    ),
    "exit",
] = 1
```

**Logic Analysis**:
- **Upper Bollinger Band Break**: Price breaking above the upper Bollinger Band indicates price is at a statistically high position
- **RSI Extreme Overbought**: RSI > 99 approaches the theoretical maximum of 100, confirming extreme overbought conditions
- **Symmetric Design**: Entry and exit conditions form a mirror symmetry, reflecting mean reversion philosophy

### 4.2 ROI Exit Priority

The strategy sets 4 levels of ROI exits, with priority over technical signals:

| Hold Time | Minimum Profit | Trigger Exit |
|-----------|---------------|--------------|
| 0 minutes | 22.77% | Exit immediately when reached |
| 31 minutes | 6.16% | Exit when reached after 31 minutes |
| 78 minutes | 3.23% | Exit when reached after 78 minutes |
| 105 minutes | 0% | Exit at breakeven after 105 minutes |

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Usage |
|-------------------|-------------------|------------|-------|
| **Volatility** | Bollinger Bands | 20 periods, 2 std dev | Price boundary judgment |
| **Momentum** | RSI | 14 periods | Overbought/oversold judgment |

### 5.2 Indicator Characteristics

- **Bollinger Bands**: Calculated using typical price ((high + low + close)/3), smoother than using close price only
- **RSI**: Standard 14 periods, thresholds set at 21/99 instead of conventional 30/70, more strict

---

## 6. Risk Management Features

### 6.1 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_stop_positive = 0.17832
trailing_stop_positive_offset = 0.24807
trailing_only_offset_is_reached = True
```

**Working Mechanism**:
1. Trailing stop activates after profit reaches 24.81%
2. Triggers exit when pulling back 17.83% from the highest point
3. Trailing stop does not activate before profit reaches 24.81%

### 6.2 Hard Stoploss Protection

```python
stoploss = -0.30054  # -30.05%
```

**Note**: Loose stoploss giving trades ample fluctuation room, suitable for high volatility coins.

---

## 7. Strategy Strengths and Limitations

### ✅ Strengths

1. **Simple and Clear Logic**: Only 2 indicators, easy to understand and monitor
2. **Classic Mean Reversion**: Bollinger Bands + RSI combination has long-term market validation
3. **High Signal Quality**: Dual confirmation reduces false signals, RSI < 21 condition is strict
4. **Trailing Stop Protection**: Activates on large profits to lock in gains
5. **Low Computational Load**: Few indicators, low hardware requirements

### ⚠️ Limitations

1. **Low Signal Frequency**: RSI < 21 and RSI > 99 are extreme conditions, few trading opportunities
2. **No Trend Filter**: No EMA/SMA trend judgment, may incur consecutive losses in one-way downtrends
3. **No BTC Correlation Analysis**: Does not detect Bitcoin market trend
4. **Loose Stoploss Risk**: -30% stoploss may cause significant losses in extreme conditions
5. **Exit Conditions Too Strict**: RSI > 99 rarely triggers, mainly relies on ROI exits

---

## 8. Recommended Usage Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Ranging Market** | Default configuration | Mean reversion strategies best suited for ranging conditions |
| **Uptrend** | Lower RSI entry threshold | e.g., RSI < 25, increase trading opportunities |
| **Downtrend** | Pause or reduce position | No trend filter, prone to losses in downtrends |
| **High Volatility** | Keep default | Loose stoploss suitable for high volatility |
| **Low Volatility** | Adjust ROI table | Lower ROI thresholds to adapt to small moves |

---

## 9. Suitable Market Environments Explained

BBRSI21 is a classic mean reversion strategy based on the core assumption that "price fluctuates around the mean".

### 9.1 Strategy Core Logic

- **Mean Reversion Philosophy**: After price falls below the lower Bollinger Band, it will likely revert to the middle band
- **Extreme Oversold Confirmation**: RSI < 21 confirms extremely pessimistic market sentiment, high probability of rebound
- **Symmetric Exit**: Exit when price rises to upper Bollinger Band and RSI is extremely overbought

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|------------|-------------------|-----------------|
| 📈 Slow Bull/Ranging Upward | ★★★☆☆ (Neutral) | Mean reversion performs average in uptrends, may exit too early |
| 🔄 Wide Ranging | ★★★★★ (Best) | Ranging conditions are ideal for mean reversion strategies |
| 📉 One-Way Crash | ★☆☆☆☆ (Poor) | No trend filter, may continuously catch falling knives |
| ⚡️ Extreme Sideways | ★★☆☆☆ (Poor) | Volatility too small, difficult to trigger buy/sell conditions |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Notes |
|--------------|------------------|-------|
| **Number of Pairs** | 20-40 USDT pairs | Low signal frequency, needs many pairs |
| **Max Open Trades** | 5-10 orders | Few signals, can hold more positions simultaneously |
| **Position Mode** | Fixed or full position | Choose based on capital |
| **Timeframe** | 5m | Mandatory, cannot be changed |

---

## 10. Important Reminder: The Cost of Simplicity

### 10.1 Low Learning Curve

Strategy has only about 80 lines of code, clear logic, suitable for beginners to learn and modify.

### 10.2 Low Hardware Requirements

Only calculates RSI and Bollinger Bands, extremely low VPS requirements:

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 20-40 pairs | 512MB | 1GB |
| 40-80 pairs | 1GB | 2GB |

### 10.3 Differences Between Backtest and Live Trading

Simple strategy logic means relatively small differences between backtest and live trading, but still recommend:

1. Run paper trading (Dry-Run) for 2-4 weeks first
2. Observe if signal trigger frequency meets expectations
3. Test with small capital for 1 month before increasing capital

### 10.4 Manual Trading Recommendations

Manual traders can reference this strategy's buy/sell signals, but recommend:
- Add trend filter (e.g., only go long when price is above EMA200)
- Combine with BTC market trend analysis
- Adjust RSI thresholds based on market volatility

---

## 11. Summary

**BBRSI21** is a classic mean reversion strategy template, its core value lies in:

1. **Simple and Elegant**: Complete trading logic with only 2 indicators
2. **Easy to Understand**: Short code, suitable for beginners
3. **Classic Combination**: Bollinger Bands + RSI validated by long-term market use
4. **Low Resource Consumption**: Small computational load, suitable for low-spec VPS

For quantitative traders, this is an excellent learning template and modification foundation. Recommendations:
- Use as an introductory case for learning mean reversion strategies
- Can add trend filters, BTC correlation, and other protection mechanisms on this basis
- Adjust RSI thresholds to adapt to different coin characteristics
- Optimize ROI table to improve capital utilization

---
