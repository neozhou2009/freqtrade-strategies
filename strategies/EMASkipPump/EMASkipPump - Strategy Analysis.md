# EMASkipPump Strategy: In-Depth Analysis

> **Strategy Number**: #157 (157th of 465 strategies)  
> **Strategy Type**: MA Alignment + Volatility Filter + Pump Protection  
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**EMASkipPump** is a strategy specifically designed to "skip pumps." The core idea is: when the market shows abnormal trading volume (possibly a "pump"), the strategy "skips" and doesn't buy, waiting for the market to return to normal before trading.

### Key Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 main condition + volatility filtering |
| **Sell Conditions** | 1 main condition |
| **Protection** | Trading volume anomaly detection (20x 30-period moving average) |
| **Timeframe** | 5 Minutes |

---

## II. Strategy Configuration

```python
# EMA Periods
EMA_SHORT_TERM = 5
EMA_MEDIUM_TERM = 12
EMA_LONG_TERM = 21

# Take-Profit
minimal_roi = {"0": 0.1}  # 10%

# Stoploss
stoploss = -0.05  # -5% (relatively strict)
```

---

## III. Entry Conditions Details

```python
# Buy Condition
dataframe.loc[
    (dataframe['volume'] < volume_rolling_mean * 20) &   # Normal volume
    (dataframe['close'] < ema_5) &                        # Price < short-term EMA
    (dataframe['close'] < ema_12) &                       # Price < medium-term EMA
    (dataframe['close'] == dataframe['min']) &            # Close is period low
    (dataframe['close'] <= bb_lowerband),                 # Touched Bollinger lower band
    'buy'
] = 1
```

**Logic Analysis**:
1. **Volume filter**: `volume < rolling_mean * 20` excludes abnormal volume (pump protection)
2. **MA alignment**: Price below all EMAs, bearish alignment
3. **Extremum confirmation**: Close is the period low
4. **Bollinger confirmation**: Price touches or is below the lower band

---

## IV. Exit Conditions Details

```python
# Sell Condition
dataframe.loc[
    (dataframe['close'] > ema_5) &
    (dataframe['close'] > ema_12) &
    (dataframe['close'] >= dataframe['max']) &
    (dataframe['close'] >= bb_upperband),
    'sell'
] = 1
```

**Logic Analysis**:
- Price above all EMAs, bullish alignment
- Close is the period high
- Touched or broke through Bollinger upper band

---

## V. Technical Indicators

| Indicator | Period | Purpose |
|----------|--------|---------|
| EMA5 | 5 | Short-term trend |
| EMA12 | 12 | Medium-term trend |
| EMA21 | 21 | Long-term trend |
| Bollinger Bands | 20, 2 | Volatility boundaries |
| MIN/MAX | 12 | Extremum confirmation |

---

## VI. Risk Management

### 6.1 Volume Protection

```python
volume < volume_rolling_mean.shift(1) * 20
```

**Function**: Detects and skips abnormal trading volume, avoiding buying "pump coins."

### 6.2 Stoploss Settings

```python
stoploss = -0.05  # -5%
```

Relatively strict stoploss, suitable for short-term trading.

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Pump protection**: Specifically designed to avoid buying coins with abnormal volatility
2. **MA alignment**: Bullish/bearish alignment confirms trend direction
3. **Extremum trading**: Buy at period low, sell at period high
4. **Clear logic**: Code is concise and easy to understand

### ⚠️ Cons

1. **Counter-trend trading**: Buying when MA is bearish — may catch a falling knife
2. **False breakouts**: Bollinger lower band may be touched frequently
3. **Fixed volume threshold**: 20x may not suit all markets

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Config | Notes |
|-------------------|-------------------|-------|
| Trending up | Use sell condition | Sell when bullish alignment |
| Dip bounce | Use buy condition | Buy at support in bearish alignment |
| Oscillating market | Reduce trading pairs | Suitable for selling high/buying low |
| Abnormal volatility | Skip | Pump protection auto-skips |

---

## IX. Applicable Market Environments in Detail

### 9.1 Core Strategy Logic

- Pump protection: Detect abnormal volume, skip "pump coins"
- Extremum trading: Buy at period low, sell at period high
- MA alignment: Confirm trend direction

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---:|:---|
| Trending up | ★★★★☆ | Sell in bullish alignment |
| Dip bounce | ★★★★☆ | Buy at support in bearish alignment |
| Oscillating market | ★★★★★ | Perfect for selling high/buying low |
| Abnormal volatility | ★★★★★ | Auto-skips pumps |

---

## X. Important Notes

### 10.1 Counter-Trend Trading Risk

Buying when MA is bearish — may catch a falling knife!

### 10.2 Hardware Requirements

The strategy has extremely low computational load, no hardware demands.

---

## XI. Summary

**EMASkipPump** is a strategy focused on "avoiding pump" scenarios. Its core value lies in using volume filtering to prevent buying coins with abnormal volatility. The strategy has concise logic and is suitable for running in normal market environments.
