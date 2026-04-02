# Strategy002 In-Depth Analysis

> **Strategy ID**: #393 (393rd of 465 strategies)
> **Strategy Type**: Multi-Indicator Oversold Bounce + Candlestick Pattern Confirmation
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

Strategy002 is a classic quantitative strategy based on oversold bounce trading. It seeks price bottoms through oversold signals from RSI, Stochastic, and Bollinger Bands, combined with hammer candlestick pattern confirmation for reversal timing. The strategy design is clean and straightforward, making it suitable as an entry-level quantitative strategy for learning.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 comprehensive buy signal, four indicators must all be satisfied |
| **Sell Conditions** | 1 basic sell signal, based on SAR and Fisher RSI |
| **Protection Mechanism** | Dual protection with fixed stop-loss + trailing stop |
| **Timeframe** | 5m single timeframe |
| **Dependencies** | talib, qtpylib, numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "60": 0.01,   # After 60 minutes, 1% profit is enough to sell
    "30": 0.03,   # After 30 minutes, 3% profit is enough to sell
    "20": 0.04,   # After 20 minutes, 4% profit is enough to sell
    "0":  0.05    # Immediately, 5% profit target
}

# Stop-loss setting
stoploss = -0.10  # 10% fixed stop-loss
```

**Design Rationale**:
- Tiered take-profit design: The longer the position is held, the lower the profit threshold, avoiding profit drawdown
- 5% as initial target, only 1% needed to exit after 60 minutes
- 10% stop-loss provides ample room for price fluctuation

### 2.2 Trailing Stop Configuration

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
```

**Trailing Stop Logic**:
- Activates trailing stop when profit reaches 2%
- Trailing distance is 1%
- A 1% profit drawdown triggers a sell

### 2.3 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

**Configuration Notes**:
- Buy and sell orders use limit orders for better prices
- Stop-loss uses market orders to ensure execution

---

## III. Buy Conditions Detailed

### 3.1 Single Buy Signal

The strategy employs strict four-condition stacking, all conditions must be satisfied simultaneously:

```python
(dataframe['rsi'] < 30) &                    # Condition 1: RSI oversold
(dataframe['slowk'] < 20) &                  # Condition 2: Stochastic oversold
(dataframe['bb_lowerband'] > dataframe['close']) &  # Condition 3: Price below Bollinger lower band
(dataframe['CDLHAMMER'] == 100)              # Condition 4: Hammer pattern confirmation
```

### 3.2 Condition Logic Analysis

| Condition # | Indicator | Threshold | Market Meaning |
|-------------|-----------|-----------|----------------|
| #1 | RSI | < 30 | Entered oversold zone, price may be oversold |
| #2 | Stochastic Slow K | < 20 | Momentum indicator confirms oversold state |
| #3 | Close < Bollinger Lower Band | Price below lower band | Price deviation from mean is excessive |
| #4 | Hammer Pattern | == 100 | Candlestick pattern confirms reversal signal |

### 3.3 Buy Logic Summary

The strategy buys when:
1. RSI indicator shows market is oversold (<30)
2. Stochastic indicator's Slow K line also confirms oversold (<20)
3. Price has broken below the Bollinger Band lower band, showing abnormal deviation
4. Candlestick shows hammer pattern, indicating possible reversal

**Typical Scenario**: Bottom reversal opportunity after sharp price decline

---

## IV. Sell Logic Detailed

### 4.1 Sell Signal

```python
(dataframe['sar'] > dataframe['close']) &   # Condition 1: SAR reversal
(dataframe['fisher_rsi'] > 0.3)              # Condition 2: Fisher RSI confirms strength
```

**Logic Analysis**:

| Condition | Indicator | Threshold | Meaning |
|-----------|-----------|-----------|---------|
| #1 | Parabolic SAR | > Close price | Price broke below SAR support level, trend may reverse |
| #2 | Fisher RSI | > 0.3 | Momentum has exited oversold zone |

### 4.2 Tiered ROI Take-Profit

```
Holding Time    Minimum Profit Target
─────────────────────────────────────
0-20 minutes    5%
20-30 minutes   4%
30-60 minutes   3%
60+ minutes     1%
```

**Design Philosophy**: As holding time extends, lower profit expectations to prioritize locking in gains.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|--------------------|-------------------|---------|
| Momentum Indicator | RSI (14) | Identify oversold/overbought |
| Momentum Indicator | Stochastic (Slow K) | Confirm oversold state |
| Volatility Indicator | Bollinger Bands (20, 2) | Judge price deviation |
| Trend Indicator | Parabolic SAR | Determine trend reversal |
| Momentum Indicator | Fisher RSI | RSI variant, enhanced signal |
| Pattern Indicator | Hammer Candlestick | Confirm reversal pattern |

### 5.2 Indicator Calculation Details

**Fisher RSI Transformation**:
```python
rsi = 0.1 * (dataframe['rsi'] - 50)
dataframe['fisher_rsi'] = (numpy.exp(2 * rsi) - 1) / (numpy.exp(2 * rsi) + 1)
```
- Maps RSI from [0, 100] to [-1, 1]
- Enhances sensitivity to extreme values

---

## VI. Risk Management Features

### 6.1 Dual Stop-Loss Mechanism

| Stop-Loss Type | Trigger Condition | Description |
|----------------|-------------------|-------------|
| Fixed Stop-Loss | Loss reaches 10% | Hard protection line |
| Trailing Stop | Profit drawdown 1% (after profit > 2%) | Locks in floating profit |

### 6.2 Tiered Take-Profit Protection

- Layered profit targets: Gradually decreasing from 5% to 1%
- Time-weighted: The longer held, the lower the tolerance
- Works with trailing stop to form multi-layer exit mechanism

### 6.3 Order Type Configuration

| Scenario | Order Type | Advantage |
|----------|------------|-----------|
| Regular buy/sell | Limit order | Reduce slippage |
| Emergency stop-loss | Market order | Ensure execution |

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Clear Logic**: Four buy conditions are clear and easy to understand and debug
2. **Oversold Capture**: Multi-indicator resonance confirms oversold bottom, reducing false signals
3. **Pattern Confirmation**: Hammer candlestick adds reversal credibility
4. **Comprehensive Risk Control**: Fixed stop-loss + trailing stop + tiered take-profit

### ⚠️ Limitations

1. **Limited Buy Opportunities**: Low probability of all four conditions being satisfied simultaneously
2. **Dependent on Reversal Markets**: May trigger repeated stop-losses in continuous downtrends
3. **Single Timeframe**: 5-minute frame has more noise, may cause misjudgments
4. **Lack of Filtering Mechanism**: No volume confirmation or overall market trend filter

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|--------------------|--------------------------|-------|
| Oscillating downtrend | Default configuration | Many oversold bounce opportunities |
| Continuous crash | Use cautiously | Consecutive oversold may fail |
| Continuous uptrend | Not recommended | Few buy opportunities |
| Sideways oscillation | Default configuration | Can capture short-term fluctuations |

---

## IX. Applicable Market Environment Details

Strategy002 is a classic **oversold bounce strategy**. Based on its code architecture, it is best suited for **markets showing reversal after oscillating decline**, and performs poorly during continuous one-way decline.

### 9.1 Strategy Core Logic

- **Oversold Confirmation**: RSI + Stochastic dual verification
- **Price Deviation**: Bollinger lower band breakthrough confirms abnormality
- **Pattern Confirmation**: Hammer confirms bottom formation
- **Trend Reversal**: SAR used for sell signal

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|-------------|-------------------|----------|
| 📈 Reversal after oscillating decline | ⭐⭐⭐⭐⭐ | Exactly the target scenario the strategy was designed for |
| 🔄 Sideways oscillation | ⭐⭐⭐⭐☆ | More oversold bounce opportunities |
| 📉 Continuous one-way decline | ⭐⭐☆☆☆ | Oversold can continue to be oversold |
| ⚡️ One-way uptrend | ⭐☆☆☆☆ | Almost no buy signals |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| timeframe | 5m | Default setting |
| stoploss | -0.10 | Can adjust based on risk preference |
| trailing_stop_positive_offset | 0.02 | Trailing activates at 2% profit |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

- Strategy code is concise, suitable for beginners to understand
- Indicator calculations are standard, can reference extensive technical analysis materials
- Candlestick pattern recognition requires some basic knowledge

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 | 2GB | 4GB |
| 10-50 | 4GB | 8GB |

### 10.3 Backtesting vs Live Trading Differences

- Candlestick patterns in backtesting may have look-ahead bias
- Limit orders in live trading may not execute timely
- Oversold conditions may trigger consecutively in extreme markets

### 10.4 Manual Trader Recommendations

Strategy logic can be executed manually:
1. Monitor assets with RSI < 30
2. Wait for Stochastic Slow K < 20
3. Check if price has broken below Bollinger lower band
4. Wait for hammer pattern to appear before entering

---

## XI. Summary

**Strategy002** is a concise and effective oversold bounce strategy. Its core value lies in:

1. **Transparent Logic**: Four buy conditions are clear and easy to understand and debug
2. **Multi-Indicator Resonance**: RSI + Stochastic + Bollinger Bands + Hammer quadruple confirmation
3. **Controllable Risk**: Dual stop-loss + tiered take-profit, protecting capital safety

For quantitative trading beginners, this is an excellent learning case; for advanced users, more filter conditions and optimized parameters can be added on this foundation.

---