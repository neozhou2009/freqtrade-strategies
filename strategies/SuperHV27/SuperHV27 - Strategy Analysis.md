# SuperHV27 Strategy Deep Dive

> **Strategy Number**: #399 (399th of 465 strategies)  
> **Strategy Type**: Multi-indicator trend following + Dynamic ROI + Position management  
> **Timeframe**: 5 minutes (5m)

---

## 1. Strategy Overview

SuperHV27 is a multi-indicator trend following strategy improved from the BinHV27 series, incorporating ADX, RSI, EMA, SMA and other technical indicators, with dynamic ROI mechanisms and position management logic. The core design philosophy is to capture trend reversal points through complex conditional combinations while optimizing exit timing using dynamic ROI and profit protection mechanisms.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | Multiple complex buy signal combinations, supporting both new position opening and position addition modes |
| **Sell Conditions** | Multi-scenario sell signals + profit protection + position coordination logic |
| **Protection Mechanisms** | Dynamic ROI (three decay types) + trade timeout checks + entry price protection |
| **Timeframe** | 5-minute primary timeframe |
| **Dependencies** | talib, qtpylib, arrow, technical (RMI), cachetools |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.10,      # Immediate requirement: 10% profit
    "30": 0.05,     # After 30 minutes: 5%
    "40": 0.025,    # After 40 minutes: 2.5%
    "60": 0.015,    # After 60 minutes: 1.5%
    "720": 0.01,    # After 12 hours: 1%
    "1440": 0       # After 24 hours: allow 0% profit exit
}

# Stop loss setting
stoploss = -0.40   # 40% hard stop loss

# Trailing stop (standard trailing stop not enabled)
trailing_stop = False
```

**Design Rationale**:
- ROI table uses stepped decrease, from 10% gradually down to 0%
- Stop loss value -0.40 is relatively loose, working with dynamic ROI for more refined exit control
- Long-term positions allow zero-profit exit to avoid being locked in losses

### 2.2 Dynamic ROI Mechanism

```python
dynamic_roi = {
    'enabled': True,
    'type': 'connect',      # Connect-type decay
    'decay-rate': 0.015,
    'decay-time': 1440,
    'start': 0.10,          # Starting 10%
    'end': 0,               # Ending 0%
}
```

**Three Decay Types**:
- **linear**: Linear decay `f(t) = start - (rate * t)`
- **exponential**: Exponential decay `f(t) = start * e^(-rate*t)`
- **connect**: Linear interpolation connecting points in the ROI table

### 2.3 Order Type Configuration

```python
use_sell_signal = True
sell_profit_only = True
ignore_roi_if_buy_signal = True
```

**Design Logic**:
- Enable sell signals to increase active exit opportunities
- Only sell when profitable to lock in profits
- Ignore ROI when buy signal still exists to extend holding period

---

## 3. Buy Conditions Detailed Analysis

### 3.1 Buy Parameter Groups

```python
buy_params = {
    'adx1': 49,     # ADX threshold during large drops
    'adx2': 36,     # ADX threshold during sustained uptrend
    'adx3': 32,     # ADX threshold during large non-sustained rise
    'adx4': 24,     # ADX threshold during sustained large rise
    'emarsi1': 43,  # EMA-RSI threshold during large drops
    'emarsi2': 27,  # EMA-RSI threshold during sustained uptrend
    'emarsi3': 26,  # EMA-RSI threshold during large non-sustained rise
    'emarsi4': 50   # EMA-RSI threshold during sustained large rise
}
```

### 3.2 Buy Condition Categories

The strategy supports two buy modes: **New Position Opening** and **Position Addition**.

#### Mode #1: New Position Opening (when no active trades)

**Base Conditions**:
```python
# Common conditions that must be met
dataframe['slowsma'].gt(0) &                      # SMA valid
dataframe['close'].lt(dataframe['highsma']) &     # Price below high SMA
dataframe['close'].lt(dataframe['lowsma']) &      # Price below low SMA
dataframe['minusdi'].gt(dataframe['minusdiema']) & # Negative DI above its EMA
dataframe['rsi'].ge(dataframe['rsi'].shift())     # RSI rising
```

**Branch Conditions (Four Groups)**:

| Condition Group | Core Logic | ADX Threshold | EMA-RSI Threshold |
|----------------|------------|---------------|-------------------|
| **Large Drop Trend** | Not preparing to change trend + Not sustained rise + bigdown | 49 | ≤43 |
| **Sustained Rise Drop** | Not preparing to change trend + Sustained rise + bigdown | 36 | ≤27 |
| **Large Rise Not Sustained** | Not preparing to change trend + Not sustained rise + bigup | 32 | ≤26 |
| **Sustained Large Rise** | Sustained rise + bigup | 24 | ≤50 |

#### Mode #2: Position Addition (when active trades exist)

```python
# Position addition conditions
conditions.append(dataframe['rmi-up-trend'] == 1)                   # RMI uptrend
conditions.append(trade_data['current_profit'] > profit_factor)     # Current profit above threshold
conditions.append(dataframe['rmi-slow'] >= rmi_grow)               # RMI reached growth target
```

**Position Addition Logic**:
- Use RMI (Relative Momentum Index) to judge momentum
- Profit factor dynamically adjusts with RMI value
- Linear growth threshold controls addition timing

---

## 4. Sell Logic Detailed Analysis

### 4.1 Multi-Layer Profit Taking System

The strategy uses a multi-scenario combined sell mechanism:

```
Scenario Type    Core Condition                 Signal Name
─────────────────────────────────────────────────────────
Price Breakout   Price breaks SMA low or high   Price breakout exit
EMA-RSI         EMA-RSI too high or price too high  Momentum overheating exit
Trend Reversal  Trend reversal confirmed + deceleration  Trend reversal exit
DI Reversal     Negative DI below positive DI  Direction reversal exit
```

### 4.2 Sell Parameter Groups

```python
sell_params = {
    'adx2': 36,
    'emarsi1': 43,
    'emarsi2': 27,
    'emarsi3': 26
}
```

### 4.3 Five Sell Scenarios

| Scenario | Trigger Condition | Core Logic |
|----------|------------------|------------|
| **Scenario 1** | Price breaks SMA + bigdown | Price rebounds but trend still down |
| **Scenario 2** | Price breaks high SMA + EMA-RSI high | Price overheating exit |
| **Scenario 3** | Price breakout + strong ADX + high EMA-RSI + bigup | Uptrend momentum overheating |
| **Scenario 4** | Trend reversal confirmed + deceleration + high EMA-RSI | Trend about to reverse |
| **Scenario 5** | Trend reversal + DI reversal + price breakout | Clear direction reversal |

### 4.4 Position Coordination Sell

```python
# Trade coordination logic
if trade_data['other_trades']:
    if trade_data['free_slots'] > 0:
        # Free slots available, allow holding
        hold_pct = (trade_data['free_slots'] / 100) * -1
        conditions.append(trade_data['avg_other_profit'] >= hold_pct)
    else:
        # No free slots, sell biggest losing position
        conditions.append(trade_data['biggest_loser'] == True)
```

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Usage |
|-------------------|---------------------|-------|
| **Trend Indicators** | EMA(60, 120), SMA(120, 240) | Judge overall trend direction |
| **Momentum Indicators** | RSI(5), EMA-RSI(5), RMI(21, 8) | Judge buy/sell momentum |
| **Direction Indicators** | ADX, PLUS_DI, MINUS_DI | Judge trend strength and direction |
| **Trend Judgment** | bigup/bigdown, continueup | Compound trend states |

### 5.2 Trend State Indicators

```python
# Major trend direction
dataframe['bigup'] = fastsma > slowsma & difference > close/300
dataframe['bigdown'] = ~bigup

# Trend change preparation
dataframe['preparechangetrend'] = trend > trend.shift()
dataframe['continueup'] = slowsma consecutive rise

# Trend deceleration
dataframe['delta'] = fastsma - fastsma.shift()
dataframe['slowingdown'] = delta < delta.shift()
```

---

## 6. Risk Management Features

### 6.1 Dynamic ROI Decay

The strategy implements three ROI decay modes, allowing refined control over exit timing:

| Decay Type | Formula | Characteristics |
|------------|---------|-----------------|
| **linear** | `start - (rate * t)` | Uniform decrease |
| **exponential** | `start * e^(-rate*t)` | Rapid decrease then gradual |
| **connect** | Linear interpolation between ROI table points | Flexible stepping |

### 6.2 Trade Timeout Check

```python
def check_buy_timeout(pair, trade, order, **kwargs):
    # Cancel buy when current price is 1% above order price
    if current_price > order['price'] * 1.01:
        return True

def check_sell_timeout(pair, trade, order, **kwargs):
    # Cancel sell when current price is 1% below order price
    if current_price < order['price'] * 0.99:
        return True
```

### 6.3 Entry Price Protection

```python
def confirm_trade_entry(pair, order_type, amount, rate, time_in_force, **kwargs):
    # Reject entry when current price is 1% above expected entry price
    if current_price > rate * 1.01:
        return False
    return True
```

### 6.4 Position Coordination Mechanism

The strategy checks all active trades and coordinates sell decisions:
- **Has free slots**: Continue holding if average profit is above hold threshold
- **No free slots**: Prioritize selling the biggest losing position

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Refined Dynamic ROI**: Three decay modes adapt to different market rhythms
2. **Multi-dimensional Trend Judgment**: Integrates ADX, RSI, SMA, DI and other indicators
3. **Smart Position Coordination**: Cross-position coordinated selling optimizes capital utilization
4. **Position Addition Mechanism**: Add positions when profitable to amplify gains
5. **Complete Entry Protection**: Price protection and timeout checks prevent slippage losses

### ⚠️ Limitations

1. **Complex Parameters**: 8 buy parameters, 4 sell parameters, difficult to optimize
2. **Loose Stop Loss**: 40% stop loss may incur significant single-trade losses
3. **Position Addition Risk**: Adding positions amplifies risk exposure
4. **Many Dependencies**: Requires technical library and cachetools

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Oscillating Rebound** | Default configuration | Capture rebound opportunities at trend reversal points |
| **Slow Bull Trend** | Enable position addition | Use position addition to amplify gains |
| **Sharp Drop** | Tighten stop loss | Prevent triggering wide stop loss |
| **Sideways Consolidation** | Disable strategy | Indicators may become ineffective |

---

## 9. Applicable Market Environment Details

SuperHV27 is a **trend reversal capture strategy**. Based on its code architecture, it is most suitable for **oscillating rebound markets**, while performance may be limited in one-sided trend markets.

### 9.1 Strategy Core Logic

- **Reversal Capture**: Judge trend changes through preparechangetrend and continueup
- **Low Price Entry**: Require price below highsma and lowsma, capturing low position opportunities
- **Momentum Rise Confirmation**: RSI rising, negative DI above EMA as confirmation conditions
- **Multi-branch Combination**: Four branch conditions cover different trend state combinations

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:------------------|:----------------|
| 📈 **Slow Bull Trend** | ⭐⭐⭐☆☆ | Can capture pullback opportunities in trend, position addition effective |
| 🔄 **Oscillating Rebound** | ⭐⭐⭐⭐⭐ | Designed for reversal capture, best performance |
| 📉 **Sharp Drop** | ⭐⭐☆☆☆ | 40% stop loss may incur large losses |
| ⚡ **One-sided Surge** | ⭐⭐☆☆☆ | Price below SMA condition hard to satisfy |
| ⚡ **Sideways Consolidation** | ⭐☆☆☆☆ | Trend indicators ineffective, few signals |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| stoploss | -0.25~-0.30 | Tighten stop loss to prevent large losses |
| dynamic_roi type | 'exponential' | Rapidly lower ROI requirements |
| max_open_trades | 3-5 | Coordinate with position addition mechanism |
| timeframe | 5m | Default configuration, not recommended to modify |

---

## 10. Important Note: The Cost of Complexity

### 10.1 Learning Cost

SuperHV27 involves multiple compound indicators and complex conditional combination logic:
- Meaning and usage of ADX/PLUS_DI/MINUS_DI
- Special calculation of RMI (Relative Momentum Index)
- Differences between three dynamic ROI decay modes
- Working principle of position coordination mechanism

**Recommended reading time**: 2-3 hours for deep understanding

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-30 pairs | 4GB | 8GB |
| 30+ pairs | 8GB | 16GB |

**Computational Burden**:
- Supertrend indicator loop calculation
- RMI indicator calculation
- Multi-condition combination judgment

### 10.3 Differences Between Backtesting and Live Trading

- **Backtesting Environment**: Cannot simulate position coordination (assumes single position)
- **Live Trading Environment**: Position addition and coordination mechanisms take effect
- **Recommendation**: Test with single position first, then enable multi-position

### 10.4 Suggestions for Manual Traders

Manual traders can learn from:
- **Dynamic ROI concept**: Lower profit targets over time
- **Position coordination logic**: When capital is tight, prioritize exiting worst positions
- **Entry price protection**: Reject unfavorable price entries

---

## 11. Summary

**SuperHV27** is a **complex and refined trend reversal capture strategy**. Its core value lies in:

1. **Dynamic ROI Flexibility**: Three decay modes adapt to different market rhythms
2. **Multi-dimensional Confirmation**: Integrates trend, momentum, and direction indicators
3. **Smart Position Management**: Position addition and coordinated selling mechanisms
4. **Complete Entry Protection**: Price protection and timeout checks

For quantitative traders, this is an **advanced strategy suitable for oscillating rebound markets**, requiring careful parameter tuning and understanding of complex conditional combination logic. It is recommended to thoroughly understand the strategy mechanism before enabling the position addition feature.

---

**Final Reminder**: No matter how good the strategy is, the market will humble you without warning. Test with small positions, survival comes first! 🙏