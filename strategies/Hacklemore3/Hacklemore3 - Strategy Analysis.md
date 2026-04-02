# Hacklemore3 Strategy: In-Depth Analysis

> **Strategy ID**: #194 (194th of 465 strategies)
> **Strategy Type**: Trend Following / Dynamic Take-Profit
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**Hacklemore3** is the third version in the Hacklemore series, a trend-following strategy based on the 5-minute timeframe. Compared to Hacklemore2 (15-minute version), Hacklemore3's core innovation is the **dual-mode exit mechanism**: when profitable, it uses dynamic trailing stop to protect profits; when in loss, it relies on trend and momentum indicators to judge exit timing.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Uptrend + RMI strong + SAR confirmation + Volume filter |
| **Exit Conditions** | Dual-mode: Dynamic trailing stop when profitable / Trend+momentum when in loss |
| **Protections** | Trailing stop + Hard stop-loss + ROI tiered take-profit |
| **Timeframe** | 5 Minutes (short-term) |
| **Dependencies** | TA-Lib, technical (RMI, qtpylib) |

### Differences from Hacklemore2

| Comparison | Hacklemore2 | Hacklemore3 |
|-----------|-------------|-------------|
| Timeframe | 15 Minutes | 5 Minutes |
| Trade Frequency | Medium | Higher |
| Exit Logic | Unified mode | Dual-mode (profit/loss separate) |
| Take-Profit Strategy | ROI tiered mainly | Dynamic trailing mainly |
| Applicable Scenario | Mid-term trend | Short-term swing |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.15,    # Immediate exit: 15% profit
    "5": 0.015    # After 5 minutes: 1.5% profit
}

# Stop-Loss Settings
stoploss = -0.10  # -10% hard stop-loss

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.02       # Activate trailing at 2% profit
trailing_stop_positive_offset = 0.03  # 3% offset
```

**Design Philosophy**:
- **High Target Profit**: Initial target 15%, suitable for capturing strong trends
- **Fast Step-Down**: Target drops to 1.5% after 5 minutes, adapting to short-term rhythm
- **Moderate Hard Stop-Loss**: -10% provides sufficient volatility room
- **Trailing Stop**: Activates at 2% profit, effectively locking in gains

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

The strategy uses a quadruple-confirmation mechanism — all conditions must be met simultaneously:

| Condition # | Condition Name | Logic Description |
|-----------|---------------|-------------------|
| Condition 1 | Uptrend Confirmation | `up_trend == True` (recent high judgment) |
| Condition 2 | RMI Strong | `RMI > 55` and `RMI >= RMI.rolling(3).mean()` |
| Condition 3 | SAR Confirmation | `sar < close` (price above SAR) |
| Condition 4 | Volume Filter | `volume < volume_ma * 30` |

### 3.2 Entry Conditions Explained

#### Condition #1: Uptrend Confirmation
```python
dataframe['up_trend'] == True
```

**Logic**:
- Confirms uptrend by price making a recent high
- Ensures entry only when trend is clear
- Avoids frequent trading in ranging or declining markets

#### Condition #2: RMI Strong
```python
(dataframe['RMI'] > 55) & (dataframe['RMI'] >= dataframe['RMI'].rolling(3).mean())
```

**Logic**:
- RMI (Relative Momentum Index) is a variant of RSI focused on momentum changes
- RMI > 55 indicates momentum is in the strong zone
- RMI above its 3-period moving average confirms momentum is strengthening

#### Condition #3: SAR Confirmation
```python
dataframe['sar'] < dataframe['close']
```

**Logic**:
- Parabolic SAR is below price
- Confirms current uptrend
- Provides additional trend direction verification

#### Condition #4: Volume Filter
```python
dataframe['volume'] < dataframe['volume_ma'] * 30
```

**Logic**:
- Volume should not be abnormally inflated
- Avoids entry during extreme market conditions (e.g., breaking news)
- Normal volume environment favors trend continuation

### 3.3 Comprehensive Entry Signal Assessment

The strategy's entry logic can be summarized as:
> **Trend confirmed + Momentum strong + Multi-verification** — only considers entry when uptrend is clear, RMI momentum is strengthening, SAR confirms trend direction, and volume is normal.

---

## IV. Exit Logic Details

### 4.1 Dual-Mode Exit Mechanism

Hacklemore3's core innovation is **using different exit strategies based on profit/loss state**:

| Mode | Trigger Condition | Core Logic |
|------|-----------------|------------|
| **Loss Mode** | `current_profit < 0` | Trend broken + momentum decayed → Exit |
| **Profit Mode** | `current_profit > 0` | Dynamic trailing stop → Protect profits |

### 4.2 Loss Mode: Trend-Based Exit

```python
# Exit Signal 1: Downtrend confirmed
dataframe['dn_trend'] == True

# Exit Signal 2: RMI momentum weak
dataframe['RMI'] < 50
```

**Logic**:
- When position is in loss, strategy focuses more on whether trend is broken
- `dn_trend == True` indicates trend has reversed
- `RMI < 50` indicates momentum has decayed to the weak zone
- Both conditions must be met simultaneously to trigger exit

**Design Philosophy**:
> In loss, give the trend a "second chance" — only admit defeat when trend clearly reverses and momentum decays, avoiding being stopped out by normal fluctuations.

### 4.3 Profit Mode: Dynamic Trailing Stop

```python
# Dynamic trailing stop logic
if current_profit > 0:
    # Price drops below 80% of the highest price
    price_drop = current_price < max_price * 0.8
    # Consecutive decline
    consecutive_drop = dataframe['close'] < dataframe['close'].shift(1)
    
    if price_drop and consecutive_drop:
        sell_signal = True
```

**Logic**:
- When position is profitable, strategy records the highest price during holding
- If price falls below 80% of the highest price (20% pullback), and consecutive decline occurs, trigger exit
- This mechanism allows profits to run while protecting in a timely manner when trend turns

**Design Philosophy**:
> In profit, "let profits run" — continue holding as long as price hasn't pulled back significantly, using dynamic stop to protect accumulated gains.

### 4.4 ROI Tiered Take-Profit Mechanism

The strategy also retains ROI tiered take-profit:

| Holding Time | Target Profit | Design Intent |
|-------------|--------------|--------------|
| Immediate | 15% | Capture large profits from strong trends |
| After 5 minutes | 1.5% | Quick lock-in, adapting to short-term rhythm |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Momentum Indicator** | RMI (Relative Momentum Index) | Judges momentum strength and direction |
| **Trend Indicator** | EMA | Confirms trend direction |
| **Reversal Indicator** | SAR (Parabolic SAR) | Trend reversal confirmation |
| **Trend Judgment** | Recent High | Confirms uptrend |
| **Volume** | Volume MA | Filters abnormal volume |

### 5.2 RMI Indicator Explained

**RMI (Relative Momentum Index)** is a variant of RSI:
- Traditional RSI calculates price changes; RMI calculates momentum changes
- Compared to RSI, RMI is more sensitive to trend changes
- Overbought zone: RMI > 70
- Oversold zone: RMI < 30
- Strong zone: RMI > 55 (this strategy's buy threshold)
- Weak zone: RMI < 50 (this strategy's sell threshold)

### 5.3 SAR Indicator Explained

**Parabolic SAR**:
- Used to determine trend direction and reversal points
- SAR below price: uptrend
- SAR above price: downtrend
- Used in this strategy for trend confirmation

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
- Avoids "bouncing right back after being stopped out"

### 6.3 Multi-Layer Risk Protection

| Protection Layer | Trigger Condition | Function |
|-----------------|------------------|----------|
| ROI Take-Profit | Profit target reached | Lock in gains |
| Trailing Stop | Pullback after 2% profit | Protect profits |
| Dynamic Stop | 20% price pullback when profitable | Trend reversal exit |
| Trend Stop | Loss + trend reversal | Control losses |
| Hard Stop-Loss | -10% | Last line of defense |

---

## VII. Strategy Pros & Cons

### Strengths

1. **Dual-Mode Exit Mechanism**: Protects profits when profitable, gives trend a "second chance" when losing — clear and reasonable logic
2. **Strong Short-Term Adaptability**: 5-minute timeframe, suitable for short-term trading and quick reactions
3. **Complete Risk Control**: Trailing stop + Hard stop-loss + Dynamic stop + ROI tiered, multi-layer protection
4. **Multi-Indicator Confirmation**: RMI + SAR + Trend judgment, reliable signals

### Weaknesses

1. **High Trading Costs**: 5-minute level trades frequently; fees and slippage significantly impact
2. **Average Performance in Ranging Markets**: Common weakness of trend strategies; may frequently get stopped out in ranging markets
3. **Parameter Sensitivity**: RMI threshold, SAR parameters need adjustment for different trading pairs
4. **Lagging**: Trend confirmation has lag, may miss optimal entry points

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

Hacklemore3 is a typical **short-term trend-following strategy**. Based on its code architecture and dual-mode exit mechanism, it is best suited for **unilateral upward markets**, and performs poorly in ranging or declining markets.

### 9.1 Strategy Core Logic

- **Enter on trend confirmation**: Recent high + RMI strong + SAR confirmation
- **Dual-mode exit**: Loss mode watches trend; profit mode watches pullback
- **Dynamic protection**: Activates dynamic trailing stop when profitable
- **Volume filter**: Avoids extreme market conditions

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| Unilateral Upward | ★★★★★ | Core scenario, dual-mode exit effectively protects profits |
| Ranging Market | ★★★☆☆ | Fewer signals, may be repeatedly stopped out |
| Unilateral Downward | ☆☆☆☆☆ | Will not trigger buy signals, no trades |
| High Volatility | ★★★☆☆ | Trailing stop may trigger prematurely |

### 9.3 Key Configuration Recommendations

| Config Item | Suggested Value | Notes |
|------------|---------------|-------|
| trailing_stop_positive | 0.02-0.03 | Adjust based on volatility |
| RMI Buy Threshold | 50-60 | Higher = stricter |
| RMI Sell Threshold | 45-55 | Lower = more tolerant |
| Stop-Loss | -0.08 ~ -0.12 | Adjust based on trading pair characteristics |

---

## X. Important Notes: The Cost of Complexity

### 10.1 Learning Curve

Hacklemore3 involves multiple technical indicators and dual-mode exit logic:
- RMI (Relative Momentum Index)
- SAR (Parabolic SAR)
- Trend judgment (recent high)
- Dynamic trailing stop mechanism

Understanding each indicator's principles and dual-mode exit trigger conditions is necessary; beginners should first understand each indicator's meaning.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------------|------------|----------------|
| Under 10 pairs | 2GB | 4GB |
| 10-30 pairs | 4GB | 8GB |
| Over 30 pairs | 8GB | 16GB |

### 10.3 Backtesting vs. Live Trading Differences

**Notes**:
- 5-minute level trades frequently; slippage impact is greater in live trading
- Dynamic trailing stop may lag in fast-moving markets
- Fee costs are proportionally higher in short-term strategies
- Recommended to increase fee settings in backtesting

### 10.4 Manual Trading Suggestions

If you want to manually apply this strategy's logic:
1. Observe whether price has made a recent high
2. Confirm RMI is in the strong zone (>55)
3. Check if SAR is below price
4. After entry, record the highest price; consider exiting on 20% pullback
5. When in loss, check whether trend has reversed, rather than holding desperately

---

## XI. Summary

**Hacklemore3** is a strategy focused on short-term trend following. Its core value lies in:

1. **Dual-Mode Exit Mechanism**: Dynamic protection when profitable, trend judgment when losing — clear and reasonable logic
2. **Strong Short-Term Adaptability**: 5-minute timeframe, suitable for capturing short-term trend opportunities
3. **Complete Risk Control**: Trailing stop + Hard stop-loss + Dynamic stop + ROI tiered, multi-layer protection
4. **Multi-Indicator Confirmation**: RMI + SAR + Trend judgment, improves signal reliability

For quantitative traders, Hacklemore3 is the short-term version of the Hacklemore series. Compared to Hacklemore2 (15 minutes), it is more suitable for short-term traders but requires attention to trading cost impact. Its dual-mode exit mechanism is a noteworthy design idea — using different exit strategies based on position state, achieving balance between profit protection and risk control.

---
