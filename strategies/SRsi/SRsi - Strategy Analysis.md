# SRsi Strategy Deep Dive

> **Strategy ID**: #368 (368th of 465 strategies)  
> **Strategy Type**: Stochastic RSI Overbought/Oversold Oscillation Strategy  
> **Timeframe**: 1 minute (1m)

---

## I. Strategy Overview

SRsi is a minimalist quantitative trading strategy based on Stochastic RSI (Stochastic Relative Strength Index). The strategy identifies buying opportunities in oversold regions and selling opportunities in overbought regions by calculating the stochastic indicator values of RSI, representing a classic implementation of oscillation-type strategies.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 buy signal (StochRSI K-line crossing above oversold zone) |
| **Sell Condition** | 1 sell signal (StochRSI K-line crossing below overbought zone) |
| **Protection Mechanism** | Basic stop loss at -15% |
| **Timeframe** | 1 minute (1m) |
| **Dependencies** | talib, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.012    # Immediate 1.2% profit target
}

# Stop loss setting
stoploss = -0.15   # Fixed stop loss at -15%
```

**Design Rationale**:
- ROI setting is simple and direct, exit at 1.2% profit
- Stop loss is relatively loose (-15%), giving the strategy enough room for price fluctuation
- No trailing stop, using basic stop loss mechanism

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',          # Limit order for buying
    'sell': 'limit',         # Limit order for selling
    'stoploss': 'market',    # Market order for stop loss
    'stoploss_on_exchange': False
}

order_time_in_force = {
    'buy': 'gtc',            # Good Till Cancelled
    'sell': 'gtc',
}
```

**Configuration Interpretation**:
- Use limit orders for buying and selling to avoid slippage
- Stop loss uses market orders to ensure execution
- GTC orders remain valid until filled

---

## III. Buy Condition Detailed

### 3.1 Stochastic RSI Indicator Calculation

The strategy uses the classic Stochastic RSI formula:

```python
# Parameter settings
p = 14    # RSI lookback period
d = 3     # D-line smoothing period
k = 3     # K-line smoothing period

# Indicator calculation
dataframe['rsi'] = ta.RSI(dataframe, timeperiod=30)  # Base RSI uses 30 period

# Stochastic RSI calculation
srsi = (rsi - rsi.rolling(p).min()) / (rsi.rolling(p).max() - rsi.rolling(p).min())
dataframe['k'] = srsi.rolling(k).mean() * 100  # K-line
dataframe['d'] = dataframe['k'].rolling(d).mean()  # D-line
```

**Indicator Description**:
- **RSI Period**: Uses 30 periods (longer than standard 14 periods)
- **Stochastic Period**: 14-period rolling window
- **K-line**: 3-period smoothing
- **D-line**: 3-period moving average of K-line

### 3.2 Buy Signal Logic

```python
# Buy condition
(dataframe['k'] < 15) &              # K-line in oversold zone
(dataframe['k'] >= dataframe['d'])   # K-line crossing above D-line (golden cross)
```

**Logic Interpretation**:
1. **K < 15**: Price is in oversold condition, potentially undervalued
2. **K >= D**: K-line crossing above D-line, indicating upward momentum starting

### 3.3 Buy Signal Classification

| Condition Group | Condition # | Core Logic |
|-----------------|-------------|------------|
| **Oversold Golden Cross** | #1 | K-line in oversold zone (<15) + K-line crossing above D-line |

---

## IV. Sell Logic Detailed

### 4.1 Sell Signal Logic

```python
# Sell condition
(dataframe['k'] > 75) &              # K-line in overbought zone
(dataframe['d'] >= dataframe['k'])   # D-line above K-line (death cross)
```

**Logic Interpretation**:
1. **K > 75**: Price is in overbought condition, potentially overvalued
2. **D >= K**: K-line crossing below D-line, indicating downward momentum starting

### 4.2 Sell Signal Classification

| Condition Group | Condition # | Core Logic |
|-----------------|-------------|------------|
| **Overbought Death Cross** | #1 | K-line in overbought zone (>75) + K-line crossing below D-line |

### 4.3 Stop Loss and ROI Exit

| Exit Type | Trigger Condition | Description |
|-----------|-------------------|-------------|
| **ROI Exit** | Profit >= 1.2% | Exit upon reaching target profit |
| **Stop Loss Exit** | Loss >= 15% | Fixed stop loss protection |
| **Signal Exit** | Sell signal triggered | Technical indicator reversal |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Oscillators** | RSI(30) | Relative strength base indicator |
| **Derivatives** | Stochastic RSI | RSI's stochastic processing |

### 5.2 Stochastic RSI Principle

Stochastic RSI is a secondary processing of the RSI indicator:

```
StochRSI = (RSI - RSI_min) / (RSI_max - RSI_min) × 100
```

**Advantages**:
- Normalizes RSI to 0-100 range
- More sensitively captures overbought/oversold conditions
- Generates more frequent trading signals

**Applicable Scenarios**:
- Oscillating markets
- Range trading
- Short-term trading

---

## VI. Risk Management Features

### 6.1 Simple Risk Control

The SRsi strategy uses the most basic risk control approach:

```python
stoploss = -0.15    # Fixed stop loss
minimal_roi = {"0": 0.012}  # Fixed take profit
```

**Characteristics**:
- No trailing stop
- No dynamic take profit
- No multi-layer protection mechanism
- Relies on indicator signal accuracy

### 6.2 Strategy Simplicity

| Comparison Item | SRsi | Complex Strategies |
|-----------------|------|-------------------|
| Buy Conditions | 1 | Usually 3-10 |
| Sell Conditions | 1 | Usually 2-5 |
| Adjustable Parameters | 3 | Usually 10-30 |
| Lines of Code | ~50 lines | Usually 200-500 lines |

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Minimalist Design**: Clean code, easy to understand and maintain
2. **Few Parameters**: Not prone to overfitting, strong generalization ability
3. **Fast Execution**: Small computation load, suitable for high-frequency scenarios
4. **Clear Logic**: Overbought/oversold + golden/death cross, classic technical analysis

### ⚠️ Limitations

1. **Frequent Signals**: May generate many trading signals on 1-minute timeframe
2. **No Protection Mechanism**: Lacks advanced risk controls like anti-pump and circuit breakers
3. **Poor Trend Performance**: May repeatedly trigger stop losses in one-way trending markets
4. **Wide Stop Loss**: -15% stop loss may be too large for short-term strategies

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| **Sideways Oscillation** | Default parameters | Strategy's best scenario |
| **Small Fluctuations** | Adjust oversold threshold | Can change K<15 to K<20 |
| **One-way Trend** | Not recommended | Easy to repeatedly trigger stop losses |
| **Extreme Volatility** | Not recommended | Too much noise in 1-minute timeframe |

---

## IX. Applicable Market Environment Detailed

SRsi is a typical oscillation-type strategy, best suited for **sideways oscillating markets**, while performing poorly in **one-way trending markets**.

### 9.1 Strategy Core Logic

- **Oversold Buying**: Consider price undervalued when K < 15
- **Overbought Selling**: Consider price overvalued when K > 75
- **Cross Confirmation**: Golden cross to buy, death cross to sell

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 Slow Bull Trend | ⭐⭐☆☆☆ | Frequent overbought leads to premature selling |
| 🔄 Sideways Oscillation | ⭐⭐⭐⭐⭐ | Classic oscillation strategy, excellent performance |
| 📉 One-way Downtrend | ⭐⭐☆☆☆ | Frequent oversold signals, catching falling knives |
| ⚡️ Extreme Volatility | ⭐⭐☆☆☆ | Too much noise in 1-minute timeframe |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| timeframe | 1m | Default value, can try 5m |
| stoploss | -0.10 ~ -0.15 | Adjust based on risk preference |
| minimal_roi | 0.01 ~ 0.02 | Can appropriately lower for short-term |

---

## X. Important Reminder: The Cost of Simplicity

### 10.1 Learning Cost

The strategy is extremely simple, code is less than 50 lines, even beginners can quickly understand. But precisely because it's simple, it lacks advanced risk control mechanisms.

### 10.2 Hardware Requirements

| Trading Pair Count | Minimum Memory | Recommended Memory |
|-------------------|----------------|-------------------|
| 1-20 pairs | 1GB | 2GB |
| 20-50 pairs | 2GB | 4GB |
| 50+ pairs | 4GB | 8GB |

Extremely small computation load, any ordinary VPS can run it.

### 10.3 Difference Between Backtesting and Live Trading

Simple strategies have lower overfitting risk, but still need to note:
- Trading frequency may be very high on 1-minute timeframe
- Fees and slippage may erode profits
- Overbought/oversold thresholds may vary by instrument

### 10.4 Manual Trader Recommendations

This strategy has simple logic, manual traders can consider:
- Using StochRSI indicator as auxiliary reference
- Combining with support/resistance levels
- Paying attention to trading frequency control

---

## XI. Summary

**SRsi** is a minimalist Stochastic RSI oscillation strategy. Its core value lies in:

1. **Clean Code**: Less than 50 lines of code, easy to understand and modify
2. **Classic Logic**: Overbought/oversold + golden/death cross, technical analysis fundamentals
3. **Few Parameters**: Not prone to overfitting, suitable as a learning template

For quantitative trading beginners, this is an excellent learning starting point. However, note that simplicity means lacking risk control protection. Before live trading, it's recommended to add more protection mechanisms.

---