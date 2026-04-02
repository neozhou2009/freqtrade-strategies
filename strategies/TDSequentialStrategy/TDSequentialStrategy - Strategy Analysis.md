# TDSequentialStrategy In-Depth Analysis

> **Strategy ID**: #405 (405th of 465 strategies)  
> **Strategy Type**: TD Sequential Reversal Signal Strategy  
> **Timeframe**: 1 Hour (1h)

---

## 1. Strategy Overview

TDSequentialStrategy is a classic reversal strategy based on Tom DeMark's TD Sequential indicator. By identifying consecutive price sequence patterns, it captures reversal opportunities after trend exhaustion, making it one of the most famous reversal signal systems in technical analysis.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 core buy signal (TD Sequential buy sequence completion) |
| **Sell Condition** | 1 basic sell signal (TD Sequential sell sequence completion or price breakout) |
| **Protection Mechanism** | Fixed stop-loss + trailing stop dual protection |
| **Timeframe** | 1 Hour (1h) |
| **Dependencies** | talib, scipy.signal, qtpylib |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {'0': 5}  # 500% target profit (actually relies on signal exit)

# Stop-loss Setting
stoploss = -0.05  # 5% fixed stop-loss

# Trailing Stop
trailing_stop = True
```

**Design Philosophy**:
- ROI set at 500%, strategy actually relies on signal exit rather than ROI
- 5% fixed stop-loss provides basic risk control
- Trailing stop enabled to lock in partial profits after gains

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'limit',
    'stoploss_on_exchange': False
}
```

---

## 3. Buy Condition Details

### 3.1 TD Sequential Buy Signal

The core buy logic is based on TD Sequential's classic sequence identification:

```python
# Buy Condition
dataframe.loc[
    ((dataframe['exceed_low']) & (dataframe['seq_buy'] > 8)),
    'buy'
] = 1
```

**Sequence Counting Logic**:
- Count consecutive times when closing price is lower than the closing price 4 candles ago
- When sequence count reaches 9, a buy signal forms
- Must satisfy "perfection" condition: low of 8th or 9th candle is lower than low of 6th or 7th candle

### 3.2 Buy Condition Breakdown

#### Condition #1: TD Sequential Buy Sequence
```python
# Sequence Count
dataframe['seq_buy'] = dataframe['close'] < dataframe['close'].shift(4)
dataframe['seq_buy'] = dataframe['seq_buy'] * (dataframe['seq_buy'].groupby(
    (dataframe['seq_buy'] != dataframe['seq_buy'].shift()).cumsum()).cumcount() + 1)

# Perfection Condition Verification
if seq_b == 8:
    dataframe.loc[index, 'exceed_low'] = (row['low'] < dataframe.loc[index - 2, 'low']) | \
                        (row['low'] < dataframe.loc[index - 1, 'low'])
if seq_b == 9:
    dataframe.loc[index, 'exceed_low'] = row['exceed_low'] | dataframe.loc[index-1, 'exceed_low']
```

**Core Logic**:
1. Current closing price lower than closing price 4 candles ago → count +1
2. When consecutive count reaches 8 or above, check perfection condition
3. Low of 8th or 9th candle must be lower than low of 6th or 7th candle
4. Both conditions satisfied together triggers buy signal

---

## 4. Sell Logic Details

### 4.1 TD Sequential Sell Signal

Sell logic is symmetrical to buy logic, identifying completion of upward sequences:

```python
# Sell Condition
dataframe.loc[
    ((dataframe['exceed_high']) | (dataframe['seq_sell'] > 8)),
    'sell'
] = 1
```

**Sell Triggers**:
1. Sell sequence exceeds 8 (seq_sell > 8)
2. Or perfect sell condition satisfied (exceed_high)

### 4.2 Sequence Counting Logic

```python
# Sell Sequence Count
dataframe['seq_sell'] = dataframe['close'] > dataframe['close'].shift(4)
dataframe['seq_sell'] = dataframe['seq_sell'] * (dataframe['seq_sell'].groupby(
    (dataframe['seq_sell'] != dataframe['seq_sell'].shift()).cumsum()).cumcount() + 1)

# Perfection Condition Verification
if seq_s == 8:
    dataframe.loc[index, 'exceed_high'] = (row['high'] > dataframe.loc[index - 2, 'high']) | \
                        (row['high'] > dataframe.loc[index - 1, 'high'])
if seq_s == 9:
    dataframe.loc[index, 'exceed_high'] = row['exceed_high'] | dataframe.loc[index-1, 'exceed_high']
```

**Sell Conditions**:
- Consecutive closing prices higher than closing prices 4 candles ago reaching 9 times
- Or high of 8th/9th candle higher than high of 6th/7th candle

### 4.3 Configuration Options

```python
use_sell_signal = True
sell_profit_only = True  # Only sell when profitable
ignore_roi_if_buy_signal = False
```

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|--------------------|-------------------|---------|
| Price Comparison | Close vs Close 4 candles ago | Sequence counting basis |
| Price Extremes | High, Low | Perfection condition verification |
| Auxiliary Variables | exceed_low, exceed_high | Signal confirmation |

### 5.2 TD Sequential Theoretical Foundation

TD Sequential is a technical analysis system developed by Tom DeMark, with core concepts:

1. **Price Exhaustion**: After multiple consecutive candles moving in same direction, trend tends to exhaust
2. **Sequence Counting**: When 9 consecutive candles satisfy specific conditions, potential reversal point forms
3. **Perfection Condition**: Verify signal quality through price extremes, reducing false signals

---

## 6. Risk Management Features

### 6.1 Fixed Stop-Loss

```python
stoploss = -0.05  # 5% stop-loss
```

**Design Purpose**: Limit maximum loss per trade

### 6.2 Trailing Stop

```python
trailing_stop = True
```

**Advantages**:
- Lock in partial profits when profitable
- Allow continued profit during trend extension
- Auto-exit on trend reversal

### 6.3 Profit-Only Sell Restriction

```python
sell_profit_only = True
```

**Protection Mechanism**: Only respond to sell signals when in profit, avoiding premature exit at loss

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Classic and Reliable**: TD Sequential is a technical analysis system validated over decades
2. **Clear Logic**: Based on price action, doesn't rely on complex indicators
3. **Reversal Capture**: Specifically designed to catch trend reversal points
4. **Perfection Condition**: Improves signal quality through extreme value verification

### ⚠️ Limitations

1. **Trending Markets**: May generate too many false signals in strong trend markets
2. **Sequence Interruption**: Any single condition failure resets the count
3. **Lag**: Requires waiting for 9 candles to complete, has some lag
4. **Single Timeframe**: Only uses 1-hour timeframe, lacks multi-timeframe confirmation

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| Ranging Market | Default configuration | Best for catching reversal points within ranges |
| Sideways Consolidation | Default configuration | Suitable for identifying consolidation boundaries |
| Strong Trend | Use with caution | May result in frequent stop-losses, recommend trend filter |
| High Volatility | Increase stop-loss | May widen stop-loss to 7-10% |

---

## 9. Applicable Market Environment Details

TDSequentialStrategy is a **reversal capture strategy**. Based on TD Sequential theory, it performs best in **ranging markets** and may underperform in **strong trend markets**.

### 9.1 Strategy Core Logic

- **Sequence Identification**: Identify trend exhaustion through consecutive price comparisons
- **Perfection Verification**: Confirm signal quality through price extremes
- **Reversal Trading**: Enter opposite direction when trend exhausts

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| 🔄 Ranging Market | ⭐⭐⭐⭐⭐ | High quality reversal signals within range, accurately captures highs and lows |
| 📊 Sideways Consolidation | ⭐⭐⭐⭐☆ | Reliable signals at consolidation boundaries, watch for false breakouts |
| 📈 Strong Uptrend | ⭐⭐☆☆☆ | Frequent sell signals may cause premature exit |
| 📉 Strong Downtrend | ⭐⭐☆☆☆ | Frequent buy signals may result in failed bottom-fishing |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Notes |
|---------------|------------------|-------|
| Timeframe | 1h (default) | Suitable for intraday reversal trading |
| Stop-loss | -5% | Moderate, adjustable based on volatility |
| Trailing Stop | Enabled | Lock profits, follow trend |

---

## 10. Important Note: Cost of Complexity

### 10.1 Learning Curve

TD Sequential theory is relatively simple, but requires understanding:
- Sequence counting calculation method
- Perfection condition verification logic
- Signal interpretation in different market environments

### 10.2 Hardware Requirements

| Trading Pairs | Minimum Memory | Recommended Memory |
|--------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |

### 10.3 Backtesting vs Live Trading Differences

- **Backtesting Advantage**: Reversal points clearly visible in historical data
- **Live Trading Challenge**: Real-time sequence counting may be unexpectedly interrupted
- **Recommendation**: Conduct sufficient forward testing before live trading

### 10.4 Manual Trader Suggestions

TD Sequential can be used for manual trading assistance:
- Set up sequence counting on charts
- Watch for extreme value conditions at 8th and 9th candles
- Confirm reversal signals with other indicators

---

## 11. Summary

**TDSequentialStrategy** is a classic reversal capture strategy. Its core value lies in:

1. **Solid Theoretical Foundation**: TD Sequential is a classic system in technical analysis
2. **Simple and Clear Logic**: Based on price action, easy to understand and verify
3. **Controllable Signal Quality**: Perfection condition filtering improves signal reliability

For quantitative traders, this is a reversal strategy suitable for ranging markets. Recommended for use in sideways or oscillating environments, avoiding over-trading in strong trend markets.