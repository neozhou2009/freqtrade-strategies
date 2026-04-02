# Strategy003 In-Depth Analysis

> **Strategy ID**: #394 (394th of 465 strategies)
> **Strategy Type**: Multi-Indicator Oversold Bounce + Trend Filter + Momentum Confirmation
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

Strategy003 is a relatively complex oversold bounce strategy that adds more filtering conditions on top of Strategy002. It uses a multi-layered combination of RSI, Fisher RSI, MFI, Stochastic Fast, EMA moving average groups, and SMA moving averages, screening for high-quality reversal opportunities through strict conditions.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 comprehensive buy signal, containing 8 sub-conditions |
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
- Same tiered take-profit design as Strategy002
- 5% initial target, decreasing to 1% after 60 minutes
- 10% stop-loss provides sufficient room for price fluctuation

### 2.2 Trailing Stop Configuration

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
```

**Trailing Stop Logic**:
- Trailing stop activates when profit reaches 2%
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

---

## III. Buy Conditions Detailed

### 3.1 Comprehensive Buy Signal

The strategy employs extremely strict multi-condition combinations, all conditions must be satisfied simultaneously:

```python
(dataframe['rsi'] < 28) &                                          # Condition 1: RSI oversold
(dataframe['rsi'] > 0) &                                            # Condition 2: RSI validity check
(dataframe['close'] < dataframe['sma']) &                          # Condition 3: Price below SMA
(dataframe['fisher_rsi'] < -0.94) &                                 # Condition 4: Fisher RSI extreme oversold
(dataframe['mfi'] < 16.0) &                                        # Condition 5: MFI money flow oversold
(                                                                   # Condition 6: Trend filter (choose one)
    (dataframe['ema50'] > dataframe['ema100']) |                   # 6a: Mid-term trend upward
    (qtpylib.crossed_above(dataframe['ema5'], dataframe['ema10'])) # 6b: Short-term golden cross
) &
(dataframe['fastd'] > dataframe['fastk']) &                        # Condition 7: Stochastic momentum upward
(dataframe['fastd'] > 0)                                            # Condition 8: Momentum validity check
```

### 3.2 Condition Logic Analysis

| Condition # | Indicator | Threshold | Market Meaning |
|-------------|-----------|-----------|----------------|
| #1 | RSI | < 28 | Entered deep oversold zone |
| #2 | RSI | > 0 | Validity check (exclude abnormal data) |
| #3 | Close vs SMA(40) | Price < SMA | Price below mid-term moving average |
| #4 | Fisher RSI | < -0.94 | Extreme oversold (near -1 limit) |
| #5 | MFI | < 16.0 | Money flow depleted, selling pressure overdone |
| #6a | EMA50 vs EMA100 | EMA50 > EMA100 | Mid-term trend upward (one of two options) |
| #6b | EMA5 vs EMA10 | Golden cross | Short-term bounce signal (one of two options) |
| #7 | FastD vs FastK | FastD > FastK | Momentum turning upward |
| #8 | FastD | > 0 | Validity check |

### 3.3 Buy Logic Summary

The strategy buys only when ALL the following conditions are met:
1. **Deep Oversold**: RSI < 28 (stricter than the typical 30)
2. **Extreme Momentum**: Fisher RSI < -0.94 (near extreme value)
3. **Money Depletion**: MFI < 16.0 (selling pressure over-released)
4. **Price at Low Level**: Below SMA40 mid-term moving average
5. **Trend Confirmation**: Either mid-term trend upward (EMA50>EMA100), or short-term golden cross
6. **Momentum Reversal**: Stochastic Fast's D line above K line and greater than 0

**Typical Scenario**: Deep oversold after price crash, with signs of market bounce

---

## IV. Sell Logic Detailed

### 4.1 Sell Signal

```python
(dataframe['sar'] > dataframe['close']) &   # Condition 1: SAR reversal
(dataframe['fisher_rsi'] > 0.3)              # Condition 2: Fisher RSI exited oversold
```

**Logic Analysis**:

| Condition | Indicator | Threshold | Meaning |
|-----------|-----------|-----------|---------|
| #1 | Parabolic SAR | > Close price | Price broke below SAR support level |
| #2 | Fisher RSI | > 0.3 | Momentum has exited extreme oversold |

### 4.2 Tiered ROI Take-Profit

```
Holding Time    Minimum Profit Target
─────────────────────────────────────
0-20 minutes    5%
20-30 minutes   4%
30-60 minutes   3%
60+ minutes     1%
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|--------------------|-------------------|---------|
| Momentum Indicator | RSI (14) | Identify oversold/overbought |
| Momentum Indicator | Fisher RSI | RSI variant, enhanced extreme value sensitivity |
| Money Flow Indicator | MFI | Money flow intensity |
| Momentum Indicator | Stochastic Fast | Fast momentum indicator |
| Trend Indicator | EMA (5/10/50/100) | Multi-period trend determination |
| Trend Indicator | SMA (40) | Mid-term trend reference |
| Trend Indicator | Parabolic SAR | Trend reversal signal |
| Volatility Indicator | Bollinger Bands | Used in calculations but not as condition |

### 5.2 Indicator Calculation Details

**Fisher RSI Transformation**:
```python
rsi = 0.1 * (dataframe['rsi'] - 50)
dataframe['fisher_rsi'] = (numpy.exp(2 * rsi) - 1) / (numpy.exp(2 * rsi) + 1)
```
- Maps RSI from [0, 100] to [-1, 1]
- < -0.94 indicates extreme oversold

**EMA Moving Average Group**:
```python
dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)   # Short-term
dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10) # Short-term
dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50) # Mid-term
dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100) # Long-term
```

---

## VI. Risk Management Features

### 6.1 Dual Stop-Loss Mechanism

| Stop-Loss Type | Trigger Condition | Description |
|----------------|-------------------|-------------|
| Fixed Stop-Loss | Loss reaches 10% | Hard protection line |
| Trailing Stop | Profit drawdown 1% (after profit > 2%) | Locks in floating profit |

### 6.2 Tiered Take-Profit Protection

- Layered profit targets: Gradually decreasing from 5% to 1%
- Time-weighted: The longer held, the lower the requirement

### 6.3 Multiple Filtering Mechanism

Compared to Strategy002, Strategy003 adds:
- **MFI Money Flow Indicator**: Ensures selling pressure is over-released
- **EMA Moving Average Group**: Filters trend direction
- **Stricter RSI Threshold**: 28 vs 30

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Multiple Confirmations**: 8 sub-conditions ensure signal quality
2. **Trend Filter**: EMA moving average group avoids counter-trend bottom-fishing
3. **Money Flow Confirmation**: MFI indicator ensures selling pressure release
4. **Extreme Value Capture**: Fisher RSI < -0.94 captures true bottoms

### ⚠️ Limitations

1. **Few Signals**: Extremely low probability of all 8 conditions being met
2. **Overfitting Risk**: Too many conditions may lead to good historical performance but poor live trading
3. **Increased Complexity**: Higher maintenance and debugging difficulty
4. **Single Timeframe**: 5-minute frame noise issues persist

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|--------------------|--------------------------|-------|
| Reversal after deep correction | Default configuration | Exactly what the strategy was designed for |
| Oscillating downtrend | Default configuration | More oversold opportunities |
| Continuous crash | Use cautiously | Extreme oversold may continue |
| One-way uptrend | Not recommended | Few buy opportunities |

---

## IX. Applicable Market Environment Details

Strategy003 is a **high-threshold oversold bounce strategy**. Compared to Strategy002, it sets stricter entry conditions, aiming to capture high-quality reversal opportunities.

### 9.1 Strategy Core Logic

- **Deep Oversold Confirmation**: RSI < 28 + Fisher RSI < -0.94 + MFI < 16
- **Trend Direction Filter**: EMA50 > EMA100 or EMA5 crossing above EMA10
- **Momentum Reversal Confirmation**: FastD > FastK and FastD > 0
- **Price Low Position Confirmation**: Close price < SMA40

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|-------------|-------------------|----------|
| 📈 Reversal after deep correction | ⭐⭐⭐⭐⭐ | Exactly the strategy's target scenario |
| 🔄 Oscillating downtrend | ⭐⭐⭐⭐☆ | Can capture high-quality bounces |
| 📉 Continuous crash | ⭐⭐☆☆☆ | Conditions too strict, may miss |
| ⚡️ One-way uptrend | ⭐☆☆☆☆ | Almost no buy signals |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| timeframe | 5m | Default setting |
| stoploss | -0.10 | Can be appropriately relaxed |
| RSI threshold | 28 | Can adjust based on market |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

- Strategy involves multiple indicator combinations, requires some technical analysis foundation
- EMA moving average group usage requires understanding trend filtering principles
- Fisher RSI transformation requires some mathematical understanding

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 | 2GB | 4GB |
| 10-50 | 4GB | 8GB |

### 10.3 Backtesting vs Live Trading Differences

- Multi-condition combinations may produce "perfect match" bias in backtesting
- More conditions in live trading means higher probability of false signals
- EMA golden cross signals have lag

### 10.4 Manual Trader Recommendations

Strategy logic can be executed manually, but requires:
1. Simultaneously monitoring multiple indicators
2. Proficient use of moving average systems to determine trends
3. Understanding the meaning of MFI money flow indicator

---

## XI. Summary

**Strategy003** is an advanced version of Strategy002, screening for high-quality reversal opportunities through stricter conditions. Its core value lies in:

1. **High Signal Quality**: 8 sub-conditions ensure entry timing
2. **Trend Filtering**: EMA moving average group avoids counter-trend trading
3. **Money Flow Confirmation**: MFI ensures selling pressure release

For traders pursuing signal quality, this is a strategy worth studying; but note that too many conditions may lead to sparse signals, missing some opportunities.

---