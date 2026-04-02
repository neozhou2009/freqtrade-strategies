# Stavix2 Strategy In-Depth Analysis

> **Strategy Number**: #388 (388th of 465 strategies)
> **Strategy Type**: Ichimoku Cloud Trend-Following Strategy
> **Timeframe**: 1 minute (1m)

---

## I. Strategy Overview

Stavix2 is a trend-following strategy based on Ichimoku Kinko Hyo, using **non-standard period parameters** for trend identification. Unlike traditional Ichimoku which uses 9/26/52 periods, this strategy uses 200/350/150/75 parameters, pursuing longer-period trend confirmation to reduce noise interference.

### Core Features

| Feature | Description |
|------|------|
| **Buy Condition** | 1 composite buy signal (3 conditions must be met simultaneously) |
| **Sell Condition** | 1 composite sell signal (3 conditions must be met simultaneously) |
| **Protection Mechanism** | No independent protection parameter group, relies on stop-loss |
| **Timeframe** | 1 minute (1m) |
| **Dependencies** | technical.indicators (ichimoku), qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.15  # 15% take-profit
}

# Stop-loss setting
stoploss = -0.10  # 10% stop-loss
```

**Design Rationale**:
- **15% Take-Profit Target**: Larger profit target,配合 long-period trend following
- **10% Stop-Loss**: Gives sufficient room for trend market fluctuations
- **Risk-Reward Ratio 1.5:1**: Relatively reasonable risk-reward ratio

### 2.2 Order Type Configuration

The strategy does not explicitly configure `order_types`, using default settings:

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

---

## III. Buy Condition Details

### 3.1 Ichimoku Cloud Parameter Configuration

The strategy uses non-standard Ichimoku parameters:

| Parameter Name | Standard Value | This Strategy | Description |
|---------|--------|---------|------|
| Tenkan-sen (Conversion Line) Period | 9 | 200 | Short-term trend line |
| Kijun-sen (Base Line) Period | 26 | 350 | Medium-term trend line |
| Chikou Span (Lagging Span) Period | 26 | 150 | Confirmation line |
| Displacement | 26 | 75 | Cloud forward shift period |

**Parameter Design Philosophy**:
- Uses longer-period parameters to reduce short-term noise
- 200/350 periods provide stronger trend confirmation
- Suitable for capturing medium-to-long-term trend markets

### 3.2 Buy Condition Analysis

The strategy uses **triple AND condition** to trigger buy:

```python
(
    (dataframe['close'] > dataframe['senkou_span_a']) &    # Condition 1
    (dataframe['close'] > dataframe['senkou_span_b']) &     # Condition 2
    (qtpylib.crossed_above(dataframe['kijun_sen'], dataframe['tenkan_sen']))  # Condition 3
)
```

#### Condition #1: Price Above Cloud (Senkou Span A)
```python
dataframe['close'] > dataframe['senkou_span_a']
```
- Close price above cloud upper boundary
- Confirms bullish trend environment

#### Condition #2: Price Above Cloud (Senkou Span B)
```python
dataframe['close'] > dataframe['senkou_span_b']
```
- Close price above cloud lower boundary
- Combined with condition #1, confirms price completely above cloud

#### Condition #3: Base Line Crosses Above Conversion Line
```python
qtpylib.crossed_above(dataframe['kijun_sen'], dataframe['tenkan_sen'])
```
- Base line (Kijun-sen, 350 period) crosses above conversion line (Tenkan-sen, 200 period)
- Note: This is a **reverse crossover signal**
- In traditional Ichimoku, conversion line crossing above base line is buy signal
- This strategy uses reverse logic, possibly specific optimization result

### 3.3 Buy Condition Classification Summary

| Condition Category | Condition No. | Core Logic |
|---------|---------|---------|
| Trend Confirmation | #1, #2 | Price above cloud (bullish market) |
| Entry Timing | #3 | Base line crosses above conversion line (reverse crossover signal) |

---

## IV. Sell Logic Details

### 4.1 Sell Condition Analysis

The strategy uses **triple AND condition** to trigger sell:

```python
(
    (dataframe['close'] < dataframe['senkou_span_a']) &    # Condition 1
    (dataframe['close'] < dataframe['senkou_span_b']) &    # Condition 2
    (qtpylib.crossed_above(dataframe['tenkan_sen'], dataframe['kijun_sen']))  # Condition 3
)
```

#### Condition #1: Price Below Cloud (Senkou Span A)
```python
dataframe['close'] < dataframe['senkou_span_a']
```
- Close price below cloud upper boundary
- Confirms bearish trend environment

#### Condition #2: Price Below Cloud (Senkou Span B)
```python
dataframe['close'] < dataframe['senkou_span_b']
```
- Close price below cloud lower boundary
- Combined with condition #1, confirms price completely below cloud

#### Condition #3: Conversion Line Crosses Above Base Line
```python
qtpylib.crossed_above(dataframe['tenkan_sen'], dataframe['kijun_sen'])
```
- Conversion line (200 period) crosses above base line (350 period)
- Traditional Ichimoku buy signal
- Used as sell signal in this strategy

### 4.2 Sell Signal Summary

| Sell Signal | Trigger Condition | Signal Name |
|---------|---------|---------|
| #1 | Price < Cloud A & Price < Cloud B & Conversion line crosses above base line | Below-cloud trend reversal |

### 4.3 Strategy Logic Analysis

This strategy's buy/sell signals have **reverse correspondence** with traditional Ichimoku:

| Traditional Ichimoku | This Strategy |
|--------------|--------|
| Price above cloud = Bullish | Buy condition |
| Conversion line crosses above base line = Buy | Sell condition |
| Price below cloud = Bearish | Sell condition |
| Base line crosses above conversion line = Sell | Buy condition |

This reverse logic may be based on the following considerations:
1. Trend reversal signals under long-period parameters
2. Optimization results for specific market environments
3. Capturing reversal opportunities at trend ends

---

## V. Technical Indicator System

### 5.1 Core Indicator: Ichimoku Cloud

Ichimoku Kinko Hyo is the strategy's only indicator system:

| Indicator Line | Period Parameter | Meaning | Usage |
|--------|---------|------|------|
| Tenkan-sen (Conversion Line) | 200 | Short-term trend line | Entry signal |
| Kijun-sen (Base Line) | 350 | Medium-term trend line | Entry signal |
| Senkou Span A (Leading Span A) | - | Cloud upper boundary | Trend confirmation |
| Senkou Span B (Leading Span B) | - | Cloud lower boundary | Trend confirmation |
| Chikou Span (Lagging Span) | 150 | Confirmation line | Calculated but not used |

### 5.2 Ichimoku Cloud Interpretation

**Cloud Structure**:
- Senkou Span A = (Conversion line + Base line) / 2, shifted forward 75 periods
- Senkou Span B = (Highest high + Lowest low of past 150 periods) / 2, shifted forward 75 periods
- Cloud area = Region between Senkou Span A and Senkou Span B

**Trend Determination**:
- Price above cloud → Bullish market
- Price below cloud → Bearish market
- Price inside cloud → Ranging/unclear trend

---

## VI. Risk Management Features

### 6.1 Trend-Following Risk Control

| Feature | Description |
|------|------|
| **Cloud Filter** | Must be completely above/below cloud to trade |
| **Period Extension** | 200/350 period parameters reduce noise signals |
| **Trend Confirmation** | Dual cloud condition confirms trend direction |

### 6.2 Risk Parameters

| Parameter | Value | Analysis |
|------|------|------|
| Take-Profit | 15% | Larger target,配合 trend following |
| Stop-Loss | 10% | Gives trend market room for fluctuation |
| Risk-Reward Ratio | 1.5:1 | Reasonable range |

### 6.3 Signal Sparsity

Due to using long-period parameters:
- Signal frequency is low
- Requires longer holding time
- Suitable for patient traders

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Concise Logic**: Single Ichimoku system, no redundant indicators
2. **Long-Period Filter**: 200/350 period parameters reduce noise signals
3. **Strong Trend Confirmation**: Triple AND condition ensures trend direction
4. **Minimal Code**: About 30 lines of core code, easy to understand and maintain
5. **Reasonable Risk-Reward Ratio**: 15% take-profit vs 10% stop-loss

### ⚠️ Limitations

1. **Non-Standard Parameters**: 200/350/150/75 periods are not traditional Ichimoku parameters
2. **Signal Reversal Logic**: Buy/sell signals are opposite to traditional Ichimoku, needs attention
3. **Sparse Signals**: Long-period parameters lead to low signal frequency
4. **1-Minute Timeframe Contradiction**: Long-period parameters + 1-minute timeframe may have parameter mismatch
5. **Lacks Additional Confirmation**: No volume, momentum or other auxiliary indicators

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| Clear Trend Market | ✅ Recommended | Cloud filter effectively identifies trend |
| Ranging Market | ⚠️ Cautious | Sparse signals, possibly long periods without trades |
| High Volatility Assets | ✅ Recommended | Long-period parameters can filter noise |
| Low Volatility Assets | ❌ Not Recommended | Cloud signals too sparse |

---

## IX. Applicable Market Environment Details

Stavix2 is a **long-period trend-following strategy**. Based on code analysis and Ichimoku theory, it is best suited for **clear trend markets**, while performing poorly in **ranging and trendless markets**.

### 9.1 Strategy Core Logic

- **Trend Identification**: Determines bullish/bearish through price position relative to cloud
- **Entry Timing**: Waits for conversion line/base line crossover signal
- **Long-Period Confirmation**: 200/350 period parameters provide stronger trend confirmation

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | Above-cloud buy signals effective |
| 🔄 Sideways Ranging | ⭐⭐☆☆☆ | Sparse signals, increased false signals |
| 📉 Clear Downtrend | ⭐⭐⭐☆☆ | Below-cloud sell signals, but flat position |
| ⚡️ High Volatility No Trend | ⭐☆☆☆☆ | Frequent cloud crossings lead to false signals |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|--------|--------|------|
| Timeframe | Consider 5m/15m | 1-minute + long-period parameters may mismatch |
| Trading Pair Selection | Strong trending varieties | Ranging varieties have few signals |
| Patience Level | High | Possibly long periods without signals |

---

## X. Important Note: Period Parameter Considerations

### 10.1 Parameter Selection Analysis

This strategy uses non-standard Ichimoku parameters:

| Parameter | Standard Value | This Strategy | Difference Analysis |
|------|--------|--------|---------|
| Conversion Line | 9 | 200 | About 22x standard value |
| Base Line | 26 | 350 | About 13x standard value |
| Lagging Span | 26 | 150 | About 6x standard value |
| Displacement | 26 | 75 | About 3x standard value |

**Potential Issues**:
- 1-minute timeframe × 200 periods = 200 minutes ≈ 3.3 hours
- 1-minute timeframe × 350 periods = 350 minutes ≈ 5.8 hours
- This means the strategy uses 3-6 hour level trend confirmation on a 1-minute chart

### 10.2 Hardware Requirements

Strategy calculation is low, hardware requirements are minimal:

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|-----------|---------|---------|
| Any number | 2GB | 4GB |

### 10.3 Backtest vs. Live Trading Differences

- **Signal Frequency**: Long-period parameters lead to sparse signals
- **Timeframe Recommendation**: Consider using on 5-minute or 15-minute timeframe
- **Trend Dependency**: May have long periods without trading when trend is unclear

### 10.4 Manual Trader Recommendations

- Ichimoku cloud is easy to visualize
- Can intuitively observe signals on charts
- Suitable for semi-automated or manual trading

---

## XI. Conclusion

**Stavix2** is an **ultra-minimalist Ichimoku trend-following strategy**, with core value in:

1. **Concise Code**: About 30 lines of core code, easy to understand and modify
2. **Strict Trend Filter**: Triple AND condition ensures trend direction
3. **Long-Period Confirmation**: Non-standard parameters reduce noise signals

For quantitative traders, this is a **lightweight strategy template worth studying**, but also has potential parameter mismatch issues (1-minute timeframe + long-period parameters). Recommended to test on higher timeframes (5m/15m), or adjust period parameters to match target timeframe.

---