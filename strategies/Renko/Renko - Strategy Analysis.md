# Renko Strategy In-Depth Analysis

> **Strategy Number**: #349 (349th of 465 strategies)  
> **Strategy Type**: Renko Brick Chart Trend Following Strategy  
> **Timeframe**: 15 minutes (15m)

---

## 1. Strategy Overview

Renko is a trend-following strategy based on Renko charts. Renko charts are a special charting method that focuses solely on price changes while ignoring time factors, using "bricks" arranged in sequence to identify trend direction. The core idea is to enter positions during trend reversals or continuations and profit by following the trend.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 buy signals (upward trend reversal, trend continuation) |
| **Sell Conditions** | 1 sell signal (downward trend reversal) |
| **Protection Mechanisms** | Tiered take-profit + 10% stop-loss + trend reversal exit |
| **Timeframe** | 15 minutes (15m) |
| **Dependencies** | talib, pandas, numpy, qtpylib |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,   # Immediate hold: 10% take-profit
    "30": 0.05,  # After 30 minutes: 5% take-profit
    "60": 0.02   # After 60 minutes: 2% take-profit
}

# Stop-loss setting
stoploss = -0.10  # 10% stop-loss
```

**Design Rationale**:
- Tiered take-profit mechanism: longer holding time results in lower profit thresholds
- Initially provides larger profit margin (10%), gradually reducing expectations over time
- Encourages quick profit-taking, avoiding prolonged positions

### 2.2 Order Type Configuration

```python
use_sell_signal = True        # Enable sell signals
sell_profit_only = True       # Use sell signals only when profitable
sell_profit_offset = 0.1      # Sell signal profit offset
ignore_roi_if_buy_signal = True  # Ignore ROI when buy signal is present
```

**Design Philosophy**:
- Only respond to sell signals when profitable, protecting profits
- Continue holding when buy signals are present, preventing premature ROI exits

---

## 3. Buy Conditions Explained

### 3.1 Renko Brick Chart Principle

The core of Renko charts is the "brick" concept:

```
Upward Trend:
┌─────┐
│Green│  Price increases by more than 1 brick size
├─────┤
│Green│
└─────┘

Downward Trend:
┌─────┐
│ Red │  Price decreases by more than 1 brick size
├─────┤
│ Red │
└─────┘
```

**Brick Size**: Dynamically calculated using the mean of ATR (Average True Range)

```python
dataframe['ATR'] = ta.ATR(dataframe, timeperiod=5)
brick_size = np.mean(dataframe['ATR'])
```

### 3.2 Trend Reversal Rules

Renko chart trend reversals require **2 bricks of opposite movement**:

```python
# Upward trend reverses to downward trend
if trend and bricks <= -2:
    trend = not trend  # Reverse
    bricks += 1
    # ...generate red brick

# Downward trend reverses to upward trend
if not trend and bricks >= 2:
    trend = not trend  # Reverse
    bricks -= 1
    # ...generate green brick
```

**Explanation**:
- During an uptrend, a decline of 2 bricks is required to confirm reversal
- During a downtrend, an increase of 2 bricks is required to confirm reversal
- This design filters out false breakouts

### 3.3 Buy Conditions Detail

The strategy has 2 buy signals:

#### Condition #1: Upward Trend Reversal

```python
if row['previous-trend'] == False and row['trend'] == True:
    dataframe.loc[..., 'buy'] = 1
```

**Logic**:
- Previous brick trend was downward (False)
- Current brick trend is upward (True)
- Trend reversal triggers buy signal

#### Condition #2: Trend Continuation

```python
if row['previous-trend'] == True and row['trend'] == True:
    dataframe.loc[..., 'buy'] = 1
```

**Logic**:
- Previous brick trend was upward (True)
- Current brick trend remains upward (True)
- Trend continuation triggers buy signal (add position or continue holding)

### 3.4 Buy Condition Classification

| Condition Group | Condition Number | Core Logic |
|-----------------|------------------|------------|
| Trend Reversal | #1 | Reversal from downtrend to uptrend, buy signal |
| Trend Continuation | #2 | Uptrend continues, continue buying/add position signal |

---

## 4. Sell Logic Explained

### 4.1 Tiered Take-Profit System

The strategy employs a tiered take-profit mechanism:

```
Holding Time    Take-Profit Threshold    Description
─────────────────────────────────────────────────────────
0 minutes       10%                      Initial expectation is higher
30 minutes      5%                       As time passes, lower expectations
60 minutes      2%                       Extended holding, secure profits
```

**Design Philosophy**:
- Initially provides larger profit margin
- Longer holding time increases tendency to take profits
- Avoids risks associated with prolonged positions

### 4.2 Trend Reversal Sell

```python
# When trend reverses from upward to downward, mark for sell
else:
    dataframe.loc[..., 'sell'] = 1
```

**Logic**:
- Triggers sell when current trend is downward (False)
- This is a "trend-following" exit method

### 4.3 Protection Mechanisms

```python
sell_profit_only = True       # Use sell signals only when profitable
sell_profit_offset = 0.1      # Profit offset protection
```

**Design**:
- Only respond to sell signals when profitable
- Additional 0.1 profit offset as protection

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Volatility | ATR(5) | Dynamically calculate brick size |
| Trend | Renko Brick Trend | Determine trend direction and reversal |

### 5.2 Renko Brick Chart Explained

Renko charts are a unique charting method:

**Characteristics**:
1. **Ignore Time**: New bricks are generated only when price changes exceed brick size
2. **Filter Noise**: Small price fluctuations do not generate bricks
3. **Clear Trend**: Continuous green bricks indicate uptrend, continuous red bricks indicate downtrend

**Brick Size Calculation**:
```python
dataframe['ATR'] = ta.ATR(dataframe, timeperiod=5)
brick_size = np.mean(dataframe['ATR'])
```

ATR (Average True Range) measures market volatility, and its mean as brick size can adapt to the volatility characteristics of different trading pairs.

---

## 6. Risk Management Features

### 6.1 Trend Reversal Protection

Renko chart reversal rules require 2 bricks of opposite movement:

```
Upward Trend: Requires 2-brick decline to confirm reversal
Downward Trend: Requires 2-brick increase to confirm reversal
```

**Advantages**:
- Filters false breakouts
- Stronger signal required to confirm trend reversal
- Reduces risk of being shaken out

### 6.2 Tiered Take-Profit Mechanism

| Holding Time | Take-Profit Threshold | Risk Control |
|-------------|----------------------|--------------|
| 0-30 minutes | 10% | Give trend room to develop |
| 30-60 minutes | 5% | Time cost consideration |
| 60+ minutes | 2% | Quick profit-taking |

### 6.3 Profit Protection

```python
sell_profit_only = True
```

Only respond to sell signals when profitable, avoiding passive exits during losses.

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Noise Filtering**: Renko charts ignore time factors, focusing on price changes
2. **Clear Trend**: Brick colors intuitively display trend direction
3. **Strict Reversal Confirmation**: Requires 2-brick opposite movement to confirm reversal
4. **Adaptive Brick Size**: ATR dynamic calculation adapts to different trading pairs

### ⚠️ Limitations

1. **Ignores Time Factor**: May lag in fast-moving markets
2. **Brick Size Depends on ATR**: Low volatility markets produce small bricks, excessive signals
3. **Complex Calculation**: Requires building complete Renko chart in `populate_indicators`
4. **Data Transformation**: Outputs Renko dataframe rather than original dataframe

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Clear Trend | Default Configuration | Renko charts can clearly capture trends |
| Low Volatility Range | Increase Brick Size | Reduce false signals |
| High Volatility Market | Decrease Brick Size | More sensitive trend capture |

---

## 9. Suitable Market Environment Explained

Renko is a **trend-following strategy**. Based on its code architecture and Renko chart characteristics, it is most suitable for **clear trend markets** and performs poorly in **ranging/sideways markets**.

### 9.1 Strategy Core Logic

- **Renko Chart Characteristics**: Focus only on price changes, ignore time factors
- **Trend Following**: Enter on trend reversal, add positions on trend continuation
- **Reversal Confirmation**: Requires 2-brick opposite movement to confirm reversal

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Clear Trend | ⭐⭐⭐⭐⭐ | Renko charts can clearly capture trend direction |
| 🔄 Ranging/Sideways | ⭐⭐☆☆☆ | Frequent brick color changes, many false signals |
| 📉 Downtrend | ⭐⭐⭐⭐☆ | Can identify downtrend and exit |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | Brick size adjusts dynamically, may lag |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|------------------|-------------|
| ATR Period | 5 | Default value, adjustable based on market |
| Timeframe | 15m | Default value, suitable for most markets |
| Tiered Take-Profit | Default | Adjust based on risk preference |

---

## 10. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

Renko charts are a relatively special charting method requiring understanding of:
- Renko brick generation rules
- Trend reversal confirmation mechanism
- Relationship between brick size and ATR

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum RAM | Recommended RAM |
|------------------------|-------------|-----------------|
| Below 10 | 2 GB | 4 GB |
| 10-50 | 4 GB | 8 GB |
| Above 50 | 8 GB | 16 GB |

### 10.3 Backtesting vs Live Trading Differences

**Data Transformation Issues**:
- `populate_indicators` returns Renko dataframe
- Not original time series data
- Be aware of data structure during backtesting

**Live Trading Challenges**:
- Renko chart real-time calculation requires continuous updates
- Brick size changes with ATR

### 10.4 Manual Trader Recommendations

Renko charts are suitable for manual traders:
- Intuitive trend direction (brick colors)
- Clear entry/exit signals (trend reversal)
- Can be used in combination with traditional candlestick charts

---

## 11. Summary

**Renko** is a **trend-following strategy based on Renko brick charts**. Its core value lies in:

1. **Noise Filtering**: Renko charts ignore time factors, focusing on price changes
2. **Clear Trend**: Brick colors intuitively display trend direction
3. **Strict Reversal Confirmation**: 2-brick opposite movement confirms reversal, reducing false signals

For quantitative traders, Renko provides a unique perspective for observing market trends, but the complexity of data transformation requires special attention. The strategy's design philosophy of "entering on trend reversal, adding positions on trend continuation" is worth learning from.

---
