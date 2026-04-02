# quantumfirst Strategy Deep Analysis

> **Strategy Number**: #464 (464th out of 465 strategies)  
> **Strategy Type**: Volume Breakout + Reversal Confirmation  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

quantumfirst is a short-term strategy combining volume breakout with momentum reversal. Its core logic is to seek opportunities with abnormal volume expansion when price is below the moving average, using indicators like Fisher RSI to confirm oversold reversal signals. The strategy design is concise but effective, suitable for moderately volatile markets.

### Core Characteristics

| Feature | Description |
|------|------|
| **Buy Conditions** | 6 conditions combination, all must be satisfied (AND logic) |
| **Sell Conditions** | 2 groups of OR signals, either triggers sell |
| **Protection Mechanisms** | Tiered ROI take-profit + trailing stop |
| **Timeframe** | 5-minute level |
| **Dependencies** | talib, qtpylib, numpy, pandas |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.05,     # 5% profit immediately after entry
    "20": 0.04,    # Drops to 4% after 20 minutes
    "40": 0.03,    # Drops to 3% after 40 minutes
    "80": 0.02,    # Drops to 2% after 80 minutes
    "1440": 0.01   # Drops to 1% after 1440 minutes (24 hours)
}

# Stop Loss Setting
stoploss = -0.10  # 10% fixed stop loss
```

**Design Rationale**:
- ROI uses progressive decay, gradually decreasing from 5% to 1%
- Moderate stop loss (-10%), balancing risk control with volatility tolerance
- Still maintains 1% take-profit target after 24 hours

### 2.2 Trailing Stop Configuration

```python
trailing_stop = True
trailing_stop_positive = 0.01        # Trailing activates after 1% profit
trailing_stop_positive_offset = 0.02  # Trailing offset 2%
```

**Design Rationale**:
- Trailing stop activates after profit exceeds 1%
- Trailing offset 2%, allowing price fluctuation space
- Relatively conservative trailing settings, suitable for moderate volatility

### 2.3 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

---

## III. Buy Conditions Detailed Analysis

### 3.1 Buy Signal (Single Condition Group, 6 Indicators)

Strategy uses **full indicator confirmation mode**, all conditions must be satisfied simultaneously:

```python
dataframe.loc[
    (
        (dataframe['close'] > 0.00000200) &                    # Condition 1: Price filter
        (dataframe['volume'] > dataframe['volume'].rolling(200).mean() * 4) &  # Condition 2: Volume explosion
        (dataframe['close'] < dataframe['sma']) &              # Condition 3: Price below MA
        (dataframe['fastd'] > dataframe['fastk']) &            # Condition 4: Stochastic golden cross
        (dataframe['rsi'] > 0) &                               # Condition 5: RSI > 0 (almost always satisfied)
        (dataframe['fastd'] > 0) &                             # Condition 6: FastD > 0 (almost always satisfied)
        (dataframe['fisher_rsi_norma'] < 38.900000000000006)    # Condition 7: Fisher RSI normalized < 38.9
    ),
    'buy'] = 1
```

### 3.2 Condition Interpretation

| Condition # | Indicator | Threshold | Market Meaning |
|---------|------|------|---------|
| #1 | Close Price | > 0.00000200 | Filter low-price coins, avoid liquidity issues |
| #2 | Volume | > 200-period average × 4 | Abnormal volume explosion (4x average) |
| #3 | Close Price | < SMA(40) | Price below moving average, at relatively low position |
| #4 | FastD | > FastK | Stochastic fast line crosses above slow line (golden cross) |
| #5 | RSI | > 0 | RSI is positive (almost always satisfied) |
| #6 | FastD | > 0 | Stochastic is positive (almost always satisfied) |
| #7 | Fisher RSI Normalized | < 38.9 | Fisher RSI in oversold territory |

**Buy Logic Summary**:
- This is a **volume-confirmed reversal strategy**
- Core is "price below MA + volume explosion + momentum reversal"
- Volume 4x average is the key signal, indicating large capital entry
- Fisher RSI normalized < 38.9 confirms oversold state
- Stochastic golden cross as entry timing confirmation

---

## IV. Sell Logic Detailed Analysis

### 4.1 Sell Signal (2 Groups of OR Conditions)

Strategy uses **dual exit mechanism**, either group satisfying triggers sell:

```python
# Signal Group 1: RSI Reversal Confirmation
(
    (qtpylib.crossed_above(dataframe['rsi'], 50)) &   # RSI crosses above 50
    (dataframe['macd'] < 0) &                          # MACD < 0 (bearish trend)
    (dataframe['minus_di'] > 0)                       # Negative momentum indicator > 0
)

# Signal Group 2: SAR + Fisher RSI Combination
(
    (dataframe['sar'] > dataframe['close']) &         # SAR above close price (bearish signal)
    (dataframe['fisher_rsi'] > 0.3)                   # Fisher RSI > 0.3 (overbought territory)
)
```

### 4.2 Sell Conditions Detailed Analysis

| Signal Group | Condition | Market Meaning |
|--------|------|---------|
| **Group 1** | RSI crosses above 50 | RSI enters neutral zone from oversold, rebound in place |
| | MACD < 0 | Still in bearish trend, caution advised |
| | Minus DI > 0 | Negative momentum exists, trend may reverse |
| **Group 2** | SAR > Close Price | Parabolic indicator sends bearish signal |
| | Fisher RSI > 0.3 | Fisher RSI enters overbought territory |

**Sell Logic Summary**:
- Signal Group 1: RSI rebounds to neutral zone, but overall trend still bearish, take profit timely
- Signal Group 2: SAR sends bearish signal + Fisher RSI overbought, dual confirmation to exit
- Two groups are OR relationship, either triggers sell

### 4.3 ROI Tiered Take-Profit

| Time (minutes) | Target Return | Description |
|------------|---------|------|
| 0 | 5% | Immediate take-profit threshold after entry |
| 20 | 4% | Lower requirement after 20 minutes |
| 40 | 3% | Further reduced after 40 minutes |
| 80 | 2% | Continue reducing after 80 minutes |
| 1440 (24h) | 1% | Minimum guaranteed return after one day |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Usage |
|---------|---------|------|
| Trend Indicator | SMA(40) | Price relative position judgment |
| Momentum Indicator | RSI | Overbought/oversold judgment |
| Transform Indicator | Fisher RSI | Non-linear transformation of RSI, amplifies extreme values |
| Stochastic Indicator | FastK, FastD | Short-term momentum and entry timing |
| Volume | Volume | Abnormal volume detection |
| Trend Reversal | SAR | Trend reversal signal |
| Trend Strength | MACD, MINUS_DI | Trend direction and strength judgment |

### 5.2 Key Indicator Calculations

```python
# MACD
macd = ta.MACD(dataframe)
dataframe['macd'] = macd['macd']
dataframe['macdsignal'] = macd['macdsignal']

# Negative momentum indicator
dataframe['minus_di'] = ta.MINUS_DI(dataframe)

# RSI
dataframe['rsi'] = ta.RSI(dataframe)

# Fisher RSI (non-linear transformation, amplifies extreme values)
rsi = 0.1 * (dataframe['rsi'] - 50)
dataframe['fisher_rsi'] = (numpy.exp(2 * rsi) - 1) / (numpy.exp(2 * rsi) + 1)
# Fisher RSI normalized version (0-100 range)
dataframe['fisher_rsi_norma'] = 50 * (dataframe['fisher_rsi'] + 1)

# Stochastic fast version
stoch_fast = ta.STOCHF(dataframe)
dataframe['fastd'] = stoch_fast['fastd']
dataframe['fastk'] = stoch_fast['fastk']

# SAR
dataframe['sar'] = ta.SAR(dataframe)

# SMA
dataframe['sma'] = ta.SMA(dataframe, timeperiod=40)
```

### 5.3 Fisher RSI Interpretation

Fisher RSI is a special indicator transformation:
- **Original RSI**: Range 0-100
- **After Fisher transformation**: Range -1 to +1
- **Normalized version**: Range 0-100

Fisher transformation's purpose is to **amplify extreme values**, making overbought/oversold signals more obvious:
- Fisher RSI < -0.94 (normalized < 3): Extremely oversold
- Fisher RSI > 0.3 (normalized > 65): Overbought territory

---

## VI. Risk Management Features

### 6.1 Volume Explosion Confirmation

Strategy requires volume to be 4x the 200-period average:
```python
dataframe['volume'] > dataframe['volume'].rolling(200).mean() * 4
```
This ensures consideration of entry only when **large capital enters**, avoiding false breakouts.

### 6.2 Low Price Entry

Requires price below 40-period SMA:
```python
dataframe['close'] < dataframe['sma']
```
Ensures entry at **relatively low position**, not chasing highs.

### 6.3 Trailing Stop Protection

- Activates after 1% profit
- Offset 2%, giving price sufficient fluctuation space
- Locks profits while not easily shaken out

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Volume confirmation**: 4x volume ensures large capital entry
2. **Fisher RSI enhancement**: Amplifies extreme signals, improves accuracy
3. **Dual exit mechanism**: Two groups of OR signals, timely profit-taking
4. **Clear logic**: Volume-price combination, reversal confirmation, clear steps

### ⚠️ Limitations

1. **Low-price coin filter**: 0.00000200 price filter may exclude some opportunities
2. **Strict volume requirement**: 4x average may miss some moderate volume expansion opportunities
3. **Conservative trailing stop**: 1% activation, 2% offset may stop out in volatility
4. **No protection mechanism**: No stop loss protection parameters, relies only on fixed stop loss

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| Volatile rise | Keep original parameters | Volume explosion more obvious |
| Oscillating market | Can appropriately reduce volume multiplier | Increase trading opportunities |
| One-sided rise | Not recommended | Price difficult to be below SMA |
| Low liquidity | Not recommended | Volume signals may be distorted |

---

## IX. Applicable Market Environment Detailed Analysis

quantumfirst is a **volume-driven reversal capture strategy**. Based on its code architecture, it is most suitable for **moderately volatile markets with clear capital inflows/outflows**, and performs poorly in one-sided trend markets.

### 9.1 Strategy Core Logic

- **Volume explosion**: Wait for 4x average volume abnormal trading, identify large capital entry
- **Low position reversal**: Price below MA + momentum reversal signal, confirm bottom
- **Fisher RSI confirmation**: Use non-linear transformation to amplify oversold signals

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Oscillating rebound | ⭐⭐⭐⭐⭐ | Volume explosion + reversal, strategy design scenario |
| 🔄 High volatility oscillation | ⭐⭐⭐⭐☆ | Many volume expansion opportunities, good signal quality |
| 📉 One-sided bear market | ⭐⭐☆☆☆ | Price continuously below MA, but volume may be insufficient |
| ⚡️ Stable market | ⭐☆☆☆☆ | Volume not active, signals extremely rare |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|--------|--------|------|
| Timeframe | 5m (native) | Can try 15m, but needs re-optimization |
| Volume multiplier | 3-4x | Can adjust based on variety |
| SMA period | 40 (native) | Can adjust based on variety volatility |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

Strategy involves multiple indicators, requires understanding:
- Mathematical principle of Fisher RSI transformation
- Usage of stochastic indicators FastK/FastD
- SAR trend reversal signals
- Combination of MACD with directional indicators

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|-----------|---------|---------|
| 1-10 pairs | 4GB | 8GB |
| 11-30 pairs | 8GB | 16GB |
| 30+ pairs | 16GB | 32GB |

### 10.3 Differences Between Backtest and Live Trading

- Volume signals may lag in live trading
- Low-price coin filter may become invalid due to coin price changes
- Fisher RSI normalized parameters precise to multiple decimal places, may be overfitting

### 10.4 Manual Trader Recommendations

- Focus on volume anomalies as entry signals
- Fisher RSI < 38.9 can be used as oversold reference
- Stochastic golden cross as entry timing confirmation

---

## XI. Summary

**quantumfirst** is a **volume-confirmed reversal capture strategy**. Its core value lies in:

1. **Volume-driven**: 4x average volume ensures large capital entry
2. **Fisher RSI enhancement**: Amplifies oversold signals, improves accuracy
3. **Dual exit mechanism**: Flexible profit-taking, avoids greed

For quantitative traders, this is a **steady-type** strategy, suitable for capturing rebound trends with capital support.

---
