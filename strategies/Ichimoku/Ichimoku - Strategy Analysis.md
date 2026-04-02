# Ichimoku Strategy Analysis

> **Strategy Number**: #8 (8th of 465 strategies)  
> **Strategy Type**: Ichimoku Cloud Trend Following  
> **Timeframe**: 5 minutes (5m)

---

## 1. Strategy Overview

**Ichimoku** is a trend following strategy based on the classic Japanese technical analysis tool "Ichimoku Cloud" (Ichimoku Kinko Hyo). The core logic uses Tenkan-sen (Conversion Line) and Kijun-sen (Base Line) golden/death cross signals, combined with cloud (Kumo) judgment for trend direction.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 1 condition: TK golden cross + Cloud confirmation |
| **Exit Conditions** | No technical exits, relies on trailing stop |
| **Protection** | Trailing stop |
| **Timeframe** | 5 minutes |
| **Dependencies** | technical (ichimoku function) |
| **Special Features** | Complete Ichimoku implementation |

---

## 2. Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {"0": 1}  # 100% profit exit (almost never triggers)

# Stoploss setting
stoploss = -0.1  # -10% hard stoploss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01      # 1% trailing activation
trailing_stop_positive_offset = 0.02  # 2% offset trigger
trailing_only_offset_is_reached = True  # Only activates after offset reached
```

**Design Logic**:
- **High ROI threshold**: 100% ROI almost never triggers, mainly relies on trailing stop for exit
- **Trailing stop**: 2% profit triggers 1% trailing, suitable for trending conditions
- **Example nature**: Strategy focus is on demonstrating Ichimoku application

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "limit",       # Limit order entry
    "exit": "limit",        # Limit order exit
    "stoploss": "market",   # Market stoploss order
    "stoploss_on_exchange": False,
}
```

---

## 3. Entry Conditions Explained

### 3.1 Entry Logic

```python
# Entry conditions
dataframe.loc[
    (
        (dataframe["tenkan"].shift(1) < dataframe["kijun"].shift(1))  # Previous candle: Tenkan < Kijun
        & (dataframe["tenkan"] > dataframe["kijun"])                   # Current candle: Tenkan > Kijun
        & (dataframe["cloud_red"] == True)                             # Above cloud
    ),
    "buy",
] = 1
```

**Logic Analysis**:
- **TK Golden Cross**: Tenkan-sen crosses above Kijun-sen from below
- **Cloud Confirmation**: Price above cloud (Kumo), confirms uptrend
- **Trend Following**: Only goes long in uptrend

### 3.2 Ichimoku Indicators

```python
# Ichimoku calculation
ichi = ichimoku(dataframe)
dataframe["tenkan"] = ichi["tenkan_sen"]      # Conversion line (9 periods)
dataframe["kijun"] = ichi["kijun_sen"]        # Base line (26 periods)
dataframe["senkou_a"] = ichi["senkou_span_a"] # Leading Span A
dataframe["senkou_b"] = ichi["senkou_span_b"] # Leading Span B
dataframe["cloud_green"] = ichi["cloud_green"] # Cloud green (bullish)
dataframe["cloud_red"] = ichi["cloud_red"]     # Cloud red (bearish)
```

**Ichimoku Components**:
- **Tenkan-sen (Conversion Line)**: 9-period high/low midpoint
- **Kijun-sen (Base Line)**: 26-period high/low midpoint
- **Senkou Span A (Leading Span A)**: Midpoint of Tenkan and Kijun, shifted 26 periods forward
- **Senkou Span B (Leading Span B)**: 52-period high/low midpoint, shifted 26 periods forward
- **Kumo (Cloud)**: Area between Leading Span A and B

---

## 4. Exit Logic Explained

### 4.1 No Technical Exit Signals

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[(), "sell"] = 1  # Always allow selling
    return dataframe
```

**Note**: Strategy does not set specific technical exit signals, relies on trailing stop and ROI for exit.

### 4.2 Trailing Stop Exit

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
trailing_only_offset_is_reached = True
```

**Working Mechanism**:
1. Trailing stop activates after profit reaches 2%
2. Triggers exit when pulling back 1% from highest point
3. Trailing stop does not activate before profit reaches 2%

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Usage |
|-------------------|-------------------|------------|-------|
| **Trend** | Ichimoku Cloud | 9/26/52 | Complete trend judgment system |
| **Cloud** | Kumo | Leading Span A/B | Support/resistance area |

### 5.2 Ichimoku Characteristics

- **Multi-component System**: Conversion line, base line, cloud, lagging span (not used in this strategy)
- **Trend Judgment**: Cloud color judges long-term trend
- **Signal Generation**: TK cross generates buy/sell signals
- **Support/Resistance**: Cloud acts as dynamic support/resistance area

---

## 6. Risk Management Features

### 6.1 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
trailing_only_offset_is_reached = True
```

**Working Mechanism**:
1. Trailing stop activates after profit reaches 2%
2. Triggers exit when pulling back 1% from highest point
3. Suitable for trending conditions, can lock in most profits

### 6.2 Cloud Trend Filter

```python
dataframe["cloud_red"] == True  # Price above cloud
```

**Function**:
- Ensures only going long in uptrend
- Cloud acts as dynamic support area
- Avoids counter-trend trading in downtrends

---

## 7. Strategy Strengths and Limitations

### ✅ Strengths

1. **Classic Indicator**: Ichimoku Cloud is a classic Japanese technical analysis tool
2. **Complete System**: Includes conversion line, base line, cloud complete components
3. **Trend Filter**: Cloud confirmation ensures trend-following trading
4. **Trailing Stop**: Suitable for trending conditions, can lock in profits
5. **Concise Code**: About 60 lines, easy to understand

### ⚠️ Limitations

1. **Missing Exit Signals**: No technical exit signals, relies entirely on stoploss
2. **No BTC Correlation**: Does not detect Bitcoin market trend
3. **Fixed Parameters**: Ichimoku parameters fixed at 9/26/52
4. **Lagging Span Not Used**: Does not use Chikou Span for confirmation
5. **Example Nature**: Strategy is relatively simple, suitable for learning not production

---

## 8. Recommended Usage Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Ranging Market** | Not Recommended | Trend strategies perform poorly in ranging markets |
| **Uptrend** | Highly Recommended | Ideal environment for trend following strategies |
| **Downtrend** | Pause | Cloud filter will block most trades |
| **High Volatility** | Keep default | Trailing stop suitable for high volatility |
| **Low Volatility** | Adjust parameters | May need to lower trailing threshold |

---

## 9. Suitable Market Environments Explained

Ichimoku is a classic trend following strategy based on the core philosophy of "following the trend".

### 9.1 Strategy Core Logic

- **TK Golden Cross**: Conversion line crosses above base line, short-term trend turning strong
- **Cloud Confirmation**: Price above cloud, long-term trend upward
- **Trailing Stop**: Locks in trend profits

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|------------|-------------------|-----------------|
| 📈 Slow Bull/Ranging Upward | ★★★★★ (Best) | Ideal environment for trend following strategies |
| 🔄 Wide Ranging | ★★☆☆☆ (Poor) | Trend strategies get whipsawed in ranging markets |
| 📉 One-Way Crash | ★★★☆☆ (Neutral) | Cloud filter blocks most trades, automatically stays flat |
| ⚡️ Extreme Sideways | ★★☆☆☆ (Poor) | Volatility too small, signals reduce |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Notes |
|--------------|------------------|-------|
| **Number of Pairs** | 20-40 | Moderate signal frequency |
| **Max Open Trades** | 3-6 orders | Control risk |
| **Position Mode** | Fixed position | Recommend fixed position |
| **Timeframe** | 5m | Mandatory |

---

## 10. Important Reminder: Ichimoku Learning Curve

### 10.1 Moderate Learning Cost

Ichimoku Cloud is a complex system, requires understanding multiple components:
- Conversion line, base line, leading spans, cloud
- TK cross signals
- Cloud support/resistance function

### 10.2 Low Hardware Requirements

Only calculates Ichimoku indicators, low VPS requirements:

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 20-40 pairs | 512MB | 1GB |
| 40-80 pairs | 1GB | 2GB |

### 10.3 Backtest vs Live Trading Differences

Ichimoku is a lagging indicator, backtest and live trading differences are small.

### 10.4 Manual Trading Recommendations

Manual traders can reference this strategy's Ichimoku usage:
- Observe TK cross signals
- Confirm cloud trend direction
- Use trailing stop to protect profits

---

## 11. Summary

**Ichimoku** is a classic Ichimoku Cloud trend following strategy, its core value lies in:

1. **Classic Indicator**: Ichimoku Cloud validated by long-term market use
2. **Complete System**: Includes conversion line, base line, cloud complete components
3. **Trend Filter**: Cloud confirmation ensures trend-following trading
4. **Concise Code**: About 60 lines, easy to understand and learn
5. **Trailing Stop**: Suitable for trending conditions, can lock in profits

For quantitative traders, this is an excellent Ichimoku learning template. Recommendations:
- Use as an introductory case for learning Ichimoku Cloud
- Understand TK cross and cloud confirmation usage
- Can add Chikou Span confirmation, BTC correlation, and other mechanisms on this basis
- Consider adding technical exit signals (such as TK death cross)

---
