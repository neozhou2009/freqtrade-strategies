# Hacklemore2 Strategy: In-Depth Analysis

> **Strategy ID**: #193 (193rd of 465 strategies)
> **Strategy Type**: Trend Following / RMI Momentum Confirmation
> **Timeframe**: 15 Minutes (15m)

---

## I. Strategy Overview

**Hacklemore2** is a trend-following strategy based on RMI (Relative Momentum Index), SAR (Parabolic SAR), and trend breakout. The core idea is: during a clear uptrend, buy when RMI strengthens and price makes a recent high, using multi-indicator confirmation to improve signal reliability.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Uptrend + RMI strong + SAR confirmation + Three consecutive green candles + Volume filter |
| **Exit Conditions** | Downtrend + RMI weak + Order book dynamic take-profit |
| **Protections** | Trailing stop + Hard stop-loss + ROI tiered take-profit |
| **Timeframe** | 15 Minutes |
| **Dependencies** | TA-Lib, technical (RMI, qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.14509,    # Immediate exit: 14.51% profit
    "10": 0.07666,   # After 10 minutes: 7.67% profit
    "23": 0.03780,   # After 23 minutes: 3.78% profit
    "36": 0.01987,   # After 36 minutes: 1.99% profit
    "60": 0.01280,   # After 60 minutes: 1.28% profit
    "145": 0.00467,  # After 145 minutes: 0.47% profit
    "285": 0         # After 285 minutes: break-even exit
}

# Stop-Loss Settings
stoploss = -0.10     # -10% hard stop-loss

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.02       # Activate trailing at 2% profit
trailing_stop_positive_offset = 0.03  # 3% offset
```

**Design Philosophy**:
- **Tiered Take-Profit**: Decreasing from 14.51% to break-even, gradually locking in profits
- **Moderate Hard Stop-Loss**: -10% is reasonable for trend strategies, providing reasonable volatility room
- **Trailing Stop**: Activates at 2% profit, effectively protecting gains

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

---

## III. Entry Conditions Details

### 3.1 Core Entry Logic

The strategy uses a quintuple-confirmation mechanism — all conditions must be met simultaneously:

| Condition # | Condition Name | Logic Description |
|-----------|---------------|-------------------|
| Condition 1 | Uptrend Confirmation | `up_trend == True` (60-day high) |
| Condition 2 | RMI Strong | `RMI > 55` and `RMI >= RMI.rolling(3).mean()` |
| Condition 3 | Three Consecutive Green Candles | `close > close.shift() > close.shift(2)` |
| Condition 4 | SAR Confirmation | `sar < close` (price above SAR) |
| Condition 5 | Volume Filter | `volume < volume_ma * 30` |

### 3.2 Entry Conditions Explained

#### Condition #1: Uptrend Confirmation
```python
dataframe['up_trend'] == True
# Based on 60-day high judgment
```

**Logic**:
- Confirms uptrend by price making a 60-day high
- Ensures entry only when trend is clear
- Avoids frequent trading in ranging or declining markets

#### Condition #2: RMI Strong
```python
(dataframe['RMI'] > 55) & (dataframe['RMI'] >= dataframe['RMI'].rolling(3).mean())
```

**Logic**:
- RMI (Relative Momentum Index) is a variant of RSI focused more on momentum changes
- RMI > 55 indicates momentum is in the strong zone
- RMI above its 3-period moving average confirms momentum is strengthening

#### Condition #3: Three Consecutive Green Candles
```python
dataframe['close'] > dataframe['close'].shift(1) > dataframe['close'].shift(2)
```

**Logic**:
- Three consecutive green candles show sustained buying pressure
- Short-term momentum is upward, increasing entry success rate
- Simple and effective trend continuation signal

#### Condition #4: SAR Confirmation
```python
dataframe['sar'] < dataframe['close']
```

**Logic**:
- Parabolic SAR (SAR) is below price
- Confirms current uptrend
- Provides additional trend direction verification

#### Condition #5: Volume Filter
```python
dataframe['volume'] < dataframe['volume_ma'] * 30
```

**Logic**:
- Volume should not be abnormally inflated
- Avoids entry during extreme moves (e.g., breaking news)
- Normal volume environment is more favorable for trend continuation

### 3.3 Comprehensive Entry Signal Assessment

The strategy's entry logic can be summarized as:
> **No trend, no entry** — only considers entry when price makes a 60-day high, RMI momentum strengthens, SAR confirms uptrend, and three consecutive green candles appear.

---

## IV. Exit Logic Details

### 4.1 Exit Conditions

The strategy uses multiple exit signals — any single condition triggers exit:

| Signal Name | Trigger Condition | Technical Meaning |
|-------------|------------------|-------------------|
| Buy Signal Disappears | `buy == 0` | Entry condition no longer met |
| Downtrend | `dn_trend == True` | Trend reversal |
| RMI Weak | `RMI < 30` | Momentum severely decayed |
| Profit Protection | `profit > -3%` | Exit on small loss |

### 4.2 Exit Signal Details

```python
# Exit Signal 1: Buy signal disappears
dataframe['buy'] == 0

# Exit Signal 2: Downtrend confirmed
dataframe['dn_trend'] == True

# Exit Signal 3: RMI weak
dataframe['RMI'] < 30

# Exit Signal 4: Profit protection
current_profit > -0.03  # Exit when loss is less than 3%
```

### 4.3 ROI Tiered Take-Profit Mechanism

The strategy employs a phased take-profit approach:

| Holding Time | Target Profit | Design Intent |
|-------------|--------------|--------------|
| Immediate | 14.51% | Capture large profits from strong trends |
| After 10 minutes | 7.67% | Gradually lower expectations |
| After 23 minutes | 3.78% | Conservative lock-in |
| After 36 minutes | 1.99% | Small profit exit |
| After 60 minutes | 1.28% | Near break-even |
| After 145 minutes | 0.47% | Basically break-even |
| After 285 minutes | Break-even | Time stop |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Momentum Indicator** | RMI (Relative Momentum Index) | Judges momentum strength and direction |
| **Trend Indicator** | EMA | Confirms trend direction |
| **Reversal Indicator** | SAR (Parabolic SAR) | Trend reversal confirmation |
| **Trend Judgment** | 60-Day High | Confirms uptrend |
| **Volume** | Volume MA | Filters abnormal volume |

### 5.2 RMI Indicator Explained

**RMI (Relative Momentum Index)** is a variant of RSI:
- Traditional RSI calculates price changes; RMI calculates momentum changes
- Compared to RSI, RMI is more sensitive to trend changes
- Parameter settings: typically use default period
- Overbought zone: RMI > 70
- Oversold zone: RMI < 30
- Strong zone: RMI > 55 (used in this strategy)

### 5.3 SAR Indicator Explained

**Parabolic SAR (Stop and Reverse)**:
- Used to determine trend direction and reversal points
- SAR below price: uptrend
- SAR above price: downtrend
- This strategy uses SAR for trend confirmation

---

## VI. Risk Management Highlights

### 6.1 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_stop_positive = 0.02
trailing_stop_positive_offset = 0.03
```

**Design Philosophy**:
- Activates trailing stop when profit reaches 2%
- Trail offset of 3% gives some pullback room
- Effectively protects accumulated profits without being stopped out too early

### 6.2 Hard Stop-Loss Protection

```python
stoploss = -0.10  # -10%
```

**Design Philosophy**:
- Moderate stop-loss suitable for trend strategies
- Provides sufficient volatility room
- Avoids the awkward situation of "bouncing right back after being stopped out"

### 6.3 ROI Tiered Take-Profit

| Protection Layer | Function |
|----------------|---------|
| ROI Tiered | Gradually lowers targets based on holding time |
| Trailing Stop | Protects accumulated profits |
| Hard Stop-Loss | Last line of defense |

---

## VII. Strategy Pros & Cons

### Strengths

1. **Multi-Indicator Confirmation**: RMI + SAR + Three green candles + Volume filter, reliable signals
2. **Strong Trend-Following Capability**: Enters only when trend is clear, high win rate
3. **Complete Risk Control**: Trailing stop + Hard stop-loss + ROI tiered, multi-layer protection
4. **Clear Logic**: Entry and exit conditions are clear, easy to understand and adjust

### Weaknesses

1. **Average Performance in Ranging Markets**: Common weakness of trend strategies; fewer signals or frequent stop-losses in ranging markets
2. **Limited Entry Opportunities**: Multi-condition confirmation results in fewer entry opportunities
3. **Parameter Dependence**: RMI, SAR parameters need adjustment for different trading pairs
4. **Lagging**: 60-day high confirmation has lag, may miss optimal entry points

---

## VIII. Applicable Scenarios

| Market Environment | Recommendation | Notes |
|-------------------|---------------|-------|
| Unilateral Upward | Strongly Recommended | Core scenario, trend-following effective |
| Downtrend | Not Recommended | Will not trigger buy signals |
| Ranging Market | Use with Caution | May frequently get stopped out |
| High Volatility | Adjust Parameters | May widen stop-loss or adjust RMI threshold |

---

## IX. Applicable Market Environment Analysis

Hacklemore2 is a typical **trend-following strategy**. Based on its code architecture and logic, it is best suited for **unilateral upward markets**, and performs poorly in ranging or declining markets.

### 9.1 Strategy Core Logic

- **No trend, no entry**: Confirms trend through 60-day high
- **Momentum Confirmation**: Enters only when RMI strengthens, avoiding false breakouts
- **SAR Trend Confirmation**: Dual confirmation of trend direction
- **Volume Filter**: Avoids extreme market conditions

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| Unilateral Upward | ★★★★★ | Core scenario, multi-indicator confirmation improves win rate |
| Ranging Market | ★★★☆☆ | Fewer signals, may be repeatedly stopped out |
| Unilateral Downward | ☆☆☆☆☆ | Will not trigger buy signals, no trades |
| High Volatility | ★★★☆☆ | Trailing stop may trigger prematurely |

### 9.3 Key Configuration Recommendations

| Config Item | Suggested Value | Notes |
|------------|---------------|-------|
| trailing_stop_positive | 0.02-0.03 | Adjust based on volatility |
| RMI Threshold | 50-60 | Higher = stricter |
| Stop-Loss | -0.08 ~ -0.12 | Adjust based on trading pair characteristics |

---

## X. Important Notes: The Cost of Complexity

### 10.1 Learning Curve

Hacklemore2 involves multiple technical indicators:
- RMI (Relative Momentum Index)
- SAR (Parabolic SAR)
- Trend judgment (60-day high)
- Volume analysis

Understanding each indicator's principles and interactions is necessary; beginners should first understand each indicator's meaning.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------------|------------|----------------|
| Under 10 pairs | 2GB | 4GB |
| 10-30 pairs | 4GB | 8GB |
| Over 30 pairs | 8GB | 16GB |

### 10.3 Backtesting vs. Live Trading Differences

**Notes**:
- 60-day high in backtesting may have slippage in live trading
- RMI momentum judgment may lag in fast-moving markets
- Volume filtering may miss sudden positive news events

### 10.4 Manual Trading Suggestions

If you want to manually apply this strategy's logic:
1. Observe whether price has made a recent high
2. Confirm RMI is in the strong zone (>55)
3. Check if SAR is below price
4. Wait for three consecutive green candles to confirm momentum
5. Strictly enforce stop-loss, protect profits

---

## XI. Summary

**Hacklemore2** is a strategy focused on trend following. Its core value lies in:

1. **Multi-Indicator Confirmation Mechanism**: RMI + SAR + Three green candles + Volume filter, improves signal reliability
2. **Strong Trend-Following Capability**: Enters only when trend is clear, avoids frequent stop-losses in ranging markets
3. **Complete Risk Control**: Trailing stop + Hard stop-loss + ROI tiered, multi-layer protection mechanism

For quantitative traders, Hacklemore2 is a classic trend-following template, suitable for capturing trend opportunities in unilateral upward markets. Note that its entry conditions are strict and may miss some moves; flexibly adjust parameters based on market environment.

---
