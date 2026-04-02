# Ichimoku_v31 Strategy Analysis

> **Strategy Number**: #30 (30th of 465 strategies)  
> **Strategy Type**: Ichimoku Cloud + Heikin Ashi + Multi-Timeframe  
> **Timeframe**: 1 hour (1h)

---

## I. Strategy Overview

**Ichimoku_v31** is a multi-timeframe trend following strategy based on Ichimoku Cloud and Heikin Ashi candles. The strategy uses 4-hour informative timeframe Ichimoku cloud to confirm trends, combined with Heikin Ashi candles to smooth price noise.

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | 1 condition: Heikin Ashi + Cloud breakout |
| **Exit Conditions** | 1 condition: Price breaks below cloud |
| **Protection** | Hard stoploss + Trailing stop |
| **Timeframe** | 1 hour |
| **Dependencies** | TA-Lib, technical |
| **Special Features** | 4h informative timeframe, Heikin Ashi candles |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.10,    # Immediate exit: 10% profit
    "30": 0.05,   # After 30 minutes: 5% profit
    "60": 0.02,   # After 60 minutes: 2% profit
}

# Stoploss setting
stoploss = -0.10  # -10% hard stoploss
```

**Design Logic**:
- **Multi-Level ROI**: 3-level decreasing ROI, longer holding time means lower exit threshold
- **Standard Stoploss**: -10% hard stoploss

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "market",
    "exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": False,
}
```

**Description**: Uses market orders to ensure quick execution.

---

## III. Entry Conditions Explained

### 3.1 Entry Logic

```python
# Entry conditions
dataframe.loc[
    (
        (
            (dataframe["ha_close_4h"].crossed_above(dataframe["senkou_a_4h"])) &
            (dataframe["ha_close_4h"].shift() < dataframe["senkou_a_4h"])
        ) |
        (
            (dataframe["ha_close_4h"].crossed_above(dataframe["senkou_b_4h"])) &
            (dataframe["ha_close_4h"].shift() < dataframe["senkou_b_4h"])
        )
    ) &
    (dataframe["cloud_green_4h"] == True),
    "enter_long",
] = 1
```

**Logic Analysis**:
- **Heikin Ashi Close Crosses Above Cloud**: 4h Heikin Ashi close crosses above senkou_a or senkou_b
- **Previous Candle Below Cloud**: Previous candle close below cloud
- **Cloud Green**: 4h cloud is green (uptrend)

### 3.2 Indicator Calculation

```python
# Heikin Ashi candles (4h)
heikinashi = qtpylib.heikinashi(dataframe_inf)
dataframe_inf["ha_open"] = heikinashi["open"]
dataframe_inf["ha_close"] = heikinashi["close"]
dataframe_inf["ha_high"] = heikinashi["high"]
dataframe_inf["ha_low"] = heikinashi["low"]

# Ichimoku Cloud (based on Heikin Ashi)
ichimoku = ftt.ichimoku(heikinashi, conversion_line_period=20, base_line_periods=60, laggin_span=120, displacement=30)
dataframe_inf["senkou_a"] = ichimoku["senkou_span_a"]
dataframe_inf["senkou_b"] = ichimoku["senkou_span_b"]
dataframe_inf["cloud_green"] = ichimoku["cloud_green"]
dataframe_inf["cloud_red"] = ichimoku["cloud_red"]
```

---

## IV. Exit Logic Explained

### 4.1 Exit Conditions

```python
# Exit conditions
dataframe.loc[
    (
        (dataframe["ha_close_4h"] < dataframe["senkou_a_4h"]) |
        (dataframe["ha_close_4h"] < dataframe["senkou_b_4h"])
    ),
    "exit_long",
] = 1
```

**Logic Analysis**:
- **Price Breaks Below Cloud**: 4h Heikin Ashi close breaks below senkou_a or senkou_b
- **Trend Weakening Confirmation**: Price breaking below cloud confirms trend weakening

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|---------|---------|------|------|
| **Candles** | Heikin Ashi | - | Smooth candles |
| **Trend** | Ichimoku Cloud | 20/60/120 | Cloud filtering (4h) |

### 5.2 Informative Timeframe (4h)

The strategy uses 4-hour informative timeframe:

| Indicator | Purpose |
|------|------|
| ha_close_4h | 4h Heikin Ashi close |
| senkou_a_4h | 4h cloud upper rail A |
| senkou_b_4h | 4h cloud upper rail B |
| cloud_green_4h | 4h cloud green (uptrend) |
| cloud_red_4h | 4h cloud red (downtrend) |

### 5.3 Heikin Ashi Candles

```python
ha_close = (open + high + low + close) / 4
ha_open = (prev_ha_open + prev_ha_close) / 2
ha_high = max(high, ha_open, ha_close)
ha_low = min(low, ha_open, ha_close)
```

**Purpose**:
- Smooth price noise
- Easier to identify trends
- Reduce false signals

---

## VI. Risk Management Features

### 6.1 Standard Hard Stoploss

```python
stoploss = -0.10  # -10%
```

**Description**: Standard stoploss, controlling single trade loss within 10%.

### 6.2 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
```

**Working Mechanism**:
1. Trailing stop activates after 2% profit
2. Exit triggers when 1% pullback from highest point

### 6.3 Cloud Filtering

```python
cloud_green_4h == True
```

**Purpose**:
- Only buy when 4h cloud is green
- Auto filters downtrends

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Ichimoku Cloud**: Cloud filters trends, classic and effective
2. **Heikin Ashi**: Smooth candles reduce noise
3. **Multi-Timeframe**: 4h informative timeframe confirms trend
4. **Market Orders**: Ensures quick execution
5. **Low Computation**: Few indicators, low hardware requirements
6. **Trailing Stop**: Locks profits, protects gains

### ⚠️ Limitations

1. **No BTC Correlation**: Does not detect Bitcoin market trend
2. **1h Timeframe**: Lower signal frequency
3. **Fixed Parameters**: Ichimoku Cloud parameters fixed
4. **Market Order Slippage**: Market orders may have slippage
5. **Cloud Lag**: Cloud calculation has lag

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| **Uptrend** | Highly recommended | Cloud filtering + multi-timeframe, perfect match |
| **Ranging Market** | Not recommended | Trend strategy has many false signals in ranging |
| **Downtrend** | Auto pause | Cloud filtering blocks most trades |
| **High Volatility** | Adjust parameters | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |

---

## IX. Applicable Market Environments

Ichimoku_v31 is a trend following strategy based on the core philosophy of "Heikin Ashi + Ichimoku Cloud + Multi-Timeframe".

### 9.1 Strategy Core Logic

- **Heikin Ashi**: Smooth candles reduce noise
- **Cloud Filtering**: Only trade when 4h cloud is green
- **Multi-Timeframe**: 4h informative timeframe confirms trend

### 9.2 Performance in Different Markets

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ★★★★★ | Cloud filtering + multi-timeframe, perfect match |
| 🔄 Wide Ranging | ★★☆☆☆ | Trend strategy has many false signals in ranging |
| 📉 Single-sided Crash | ★★★☆☆ | Cloud filtering blocks most trades, auto lies flat |
| ⚡️ Extreme Sideways | ★★☆☆☆ | Too little volatility, signals decrease |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|--------|--------|------|
| **Number of Pairs** | 20-40 | Moderate signal frequency |
| **Max Open Trades** | 3-6 | Control risk |
| **Position Mode** | Fixed position | Recommended fixed position |
| **Timeframe** | 1h | Mandatory requirement |

---

## X. Important Notes: Ichimoku Cloud Usage

### 10.1 Moderate Learning Cost

Strategy code is about 80 lines, requires understanding Ichimoku Cloud, Heikin Ashi concepts.

### 10.2 Low Hardware Requirements

Only calculates Ichimoku Cloud and Heikin Ashi, low VPS requirements:

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------|---------|---------|
| 20-40 pairs | 512MB | 1GB |
| 40-80 pairs | 1GB | 2GB |

### 10.3 Cloud Filtering Advantages

- **Trend Confirmation**: 4h cloud more reliable than 1h
- **Reduces False Signals**: Only trades when cloud is green
- **Auto Lies Flat**: Auto stops trading when cloud is red

### 10.4 Manual Trading Recommendations

Manual traders can reference this strategy's Ichimoku Cloud approach:
- Use Heikin Ashi to smooth price
- Observe both 1h and 4h cloud simultaneously
- Set standard stoploss (e.g., -10%)

---

## XI. Summary

**Ichimoku_v31** is a well-designed Ichimoku Cloud trend following strategy, its core value lies in:

1. **Ichimoku Cloud**: Cloud filters trends, classic and effective
2. **Heikin Ashi**: Smooth candles reduce noise
3. **Multi-Timeframe**: 4h informative timeframe confirms trend
4. **Market Orders**: Ensures quick execution
5. **Low Computation**: Few indicators, low hardware requirements
6. **Trailing Stop**: Locks profits, protects gains

For quantitative traders, this is an excellent Ichimoku Cloud learning template. Recommendations:
- Use as an advanced case for learning Ichimoku Cloud strategies
- Understand Heikin Ashi usage
- Learn multi-timeframe application
- Note cloud lag, testthoroughly before live trading

---
