# ema Strategy Analysis

> **Strategy Number**: #18 (18th of 465 strategies)  
> **Strategy Type**: EMA Difference Cross Trend Following  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

**ema** is a minimalist EMA difference cross strategy that generates trend signals through a weighted combination of two EMA difference groups, then applies SMA smoothing as a signal line, forming a "indicator of indicator" dual cross system. The strategy code is only 60 lines, making it a classic introductory template for learning EMA cross strategies.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 1 condition: EMA difference golden cross |
| **Exit Conditions** | 1 condition: EMA difference death cross |
| **Protection** | Trailing stoploss + Hard stoploss |
| **Timeframe** | 5 minutes |
| **Dependencies** | TA-Lib, qtpylib |
| **Special Features** | Dual EMA difference + SMA signal line |

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

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01          # 1% trailing activation
trailing_stop_positive_offset = 0.02   # 2% offset trigger
```

**Design Logic**:
- **Tiered ROI**: 10% → 5% → 2%, longer holding time means lower exit threshold, reflects trend-following thinking
- **Medium hard stoploss**: -10% hard stoploss, gives some room for fluctuation
- **Trailing stop**: Activates 1% trailing after 2% profit, lets profits run

### 2.2 Order Type Configuration

```python
order_types = {
    'entry': 'limit',
    'exit': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

**Design Logic**:
- Entry and exit use limit orders to reduce slippage
- Stoploss uses market orders to ensure execution

---

## III. Entry Conditions Details

### 3.1 EMA Difference Calculation

The strategy's core innovation is the weighted combination of two EMA difference groups:

```python
# EMA calculation (note: parameter names differ from actual periods)
ema6 = ta.EMA(dataframe, 9)    # Actual period 9
ema24 = ta.EMA(dataframe, 18)  # Actual period 18
ema11 = ta.EMA(dataframe, 32)  # Actual period 32
ema25 = ta.EMA(dataframe, 64)  # Actual period 64

# EMA difference weighted combination
ema = (ema6 - ema24) * 0.6 + (ema11 - ema25) * 0.5
```

**Difference Combination Analysis**:
- **Short-term difference**: EMA(9) - EMA(18), weight 0.6, captures short-term trend changes
- **Medium-term difference**: EMA(32) - EMA(64), weight 0.5, confirms medium-term trend direction
- **Weighted combination**: Higher weight on short-term, more sensitive to quick changes

### 3.2 Signal Line Construction

```python
# Smoothed signal line of EMA difference
ema2 = ta.SMA(ema, 29)
```

**Signal Line Design**:
- Applies 29-period SMA smoothing to EMA difference
- Forms "indicator of indicator" dual structure

### 3.3 Entry Logic

```python
# Golden cross entry
qtpylib.crossed_above(ema, ema2)
```

**Logic Analysis**:
- **EMA difference crosses above signal line**: Confirms trend turning upward
- **Dual confirmation**: Both short and medium-term differences contribute to signal
- **SMA smoothing**: Reduces false signals from noise

---

## IV. Exit Logic Explained

### 4.1 Exit Conditions

```python
# Death cross exit
qtpylib.crossed_below(ema, ema2)
```

**Logic Analysis**:
- **EMA difference crosses below signal line**: Confirms trend turning downward
- **Simple and effective**: Single condition for clean exits
- **Symmetric logic**: Same structure as entry but reversed

### 4.2 ROI Exit

```python
minimal_roi = {
    "0": 0.10,    # 10%
    "30": 0.05,   # 5%
    "60": 0.02,   # 2%
}
```

**Purpose**:
- Captures large moves with 10% first-level ROI
- Time-decreasing ROI encourages timely exits
- Suitable for trend-following strategy

### 4.3 Trailing Stoploss

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
```

**Working mechanism**:
1. Trailing activates after profit reaches 2%
2. Triggers exit when pulling back 1% from highest point
3. Lets profits run while protecting gains

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|-------------------|-------------------|------------|---------|
| **Trend** | EMA | 9, 18, 32, 64 periods | Multi-period trend measurement |
| **Signal** | SMA | 29 periods | Signal line for cross detection |

### 5.2 EMA Period Structure

| Variable Name | Actual Period | Purpose |
|--------------|---------------|---------|
| ema6 | 9 | Short-term EMA (fast) |
| ema24 | 18 | Short-term EMA (slow) |
| ema11 | 32 | Medium-term EMA (fast) |
| ema25 | 64 | Medium-term EMA (slow) |

**Note**: Variable names don't match actual periods — this is a known quirk.

---

## VI. Risk Management Features

### 6.1 Medium Hard Stoploss

```python
stoploss = -0.10  # -10%
```

**Purpose**: Medium stoploss to limit losses while giving trend room to develop.

### 6.2 Tiered ROI Exit

```python
minimal_roi = {
    "0": 0.10,    # 10%
    "30": 0.05,   # 5%
    "60": 0.02,   # 2%
}
```

**Purpose**:
- High first-level ROI (10%) expects large moves
- Time-decreasing ROI encourages timely exits
- Suitable for trend-following strategy

### 6.3 Trailing Stoploss

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
```

**Purpose**: Locks profits on large moves while protecting gains.

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Simplicity**: Only EMA and SMA, easy to understand
2. **Dual confirmation**: Short and medium-term differences confirm each other
3. **Signal smoothing**: SMA reduces false signals from noise
4. **Trend-following**: Captures large trends with high ROI
5. **Trailing stop**: Lets profits run while protecting gains

### ⚠️ Limitations

1. **No trend filter**: No higher timeframe trend confirmation
2. **No BTC correlation**: Doesn't detect Bitcoin market trend
3. **Parameter naming confusion**: Variable names don't match actual periods
4. **Lag**: EMA/SMA combination has inherent lag
5. **Ranging losses**: May lose in sideways markets

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Note |
|-------------------|--------------------------|------|
| **Strong uptrend** | Default configuration | EMA cross captures trends well |
| **Ranging market** | Pause or light position | May have many false signals |
| **Downtrend** | Pause | Strategy only goes long |
| **High volatility** | Adjust stoploss | May need wider stoploss |
| **Low volatility** | Adjust ROI | May need lower ROI thresholds |

---

## IX. Applicable Market Environments Explained

ema is a trend-following strategy based on the core philosophy of "EMA difference cross + signal line".

### 9.1 Strategy Core Logic

- **Dual EMA difference**: Short and medium-term differences weighted together
- **SMA signal line**: Smoothed signal for cross detection
- **Simple entry/exit**: Golden cross buys, death cross sells

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Strong uptrend | ★★★★☆ | EMA cross captures trends well |
| 🔄 Wide ranging | ★★☆☆☆ | May have many false signals in ranging |
| 📉 Single-sided crash | ★☆☆☆☆ | Strategy only goes long, will lose |
| ⚡️ Extreme sideways | ★★☆☆☆ | Lag may cause late entries/exits |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Note |
|--------------|------------------|------|
| **Number of pairs** | 15-30 | Moderate signal frequency |
| **Max positions** | 3-5 | Control risk |
| **Position mode** | Fixed position | Recommended fixed position |
| **Timeframe** | 5m | Mandatory requirement |

---

## X. Important Note: EMA Cross Fundamentals

### 10.1 Low Learning Curve

Strategy code is about 60 lines, very simple to understand.

### 10.2 Low Hardware Requirements

Only EMA and SMA, minimal computation:

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 15-30 pairs | 512MB | 1GB |
| 30-60 pairs | 1GB | 2GB |

### 10.3 EMA Cross Characteristics

EMA cross strategies have known characteristics:
- **Lag**: Moving averages have inherent lag
- **Trend-following**: Works well in trends, poorly in ranging
- **Simple logic**: Easy to understand and modify

### 10.4 Manual Trader Recommendations

Manual traders can reference this strategy's approach:
- Use multiple EMA differences for confirmation
- Apply smoothing to reduce noise
- Set trailing stop to protect profits
- Exit on death cross or ROI target

---

## XI. Summary

**ema** is a minimalist trend-following strategy. Its core value lies in:

1. **Simplicity**: Only EMA and SMA, easy to understand
2. **Dual confirmation**: Short and medium-term differences confirm each other
3. **Signal smoothing**: SMA reduces false signals from noise
4. **Trend-following**: Captures large trends with high ROI
5. **Trailing stop**: Lets profits run while protecting gains

For quantitative traders, this is an excellent introductory EMA cross strategy template. Recommendations:
- Use as a case study for learning EMA cross strategies
- Understand dual EMA difference structure
- Can add trend filter and BTC correlation for protection
- Note parameter naming quirk, verify actual periods

---
