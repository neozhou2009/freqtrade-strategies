# Schism Strategy Deep Analysis

> **Strategy Number**: #375 (375th of 465 strategies)  
> **Strategy Type**: Multi-condition trend following + Dynamic take-profit/stop-loss + Real-time position awareness  
> **Timeframe**: 5 minutes (5m) + 1-hour information layer (1h)

---

## 1. Strategy Overview

Schism is a medium-to-short-term trading strategy combining momentum indicators with trend judgment. Its core features include "sticky buy signals" and "dynamic stop-loss mechanisms." The strategy uses RMI (Relative Momentum Index) dual timeframe analysis, combined with Momentum Pinball and ADR (Average Daily Range) positioning, to implement a trading logic of "bottom fishing but not blind bottom fishing."

This strategy was developed by @werkkrew and @JimmyNixx and is the foundational version of the Schism series, which later evolved into advanced versions like Schism2 and Schism2MM.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signal groups (new position buy + position continuation signals), supports `ignore_roi_if_buy_signal` |
| **Sell Conditions** | Dynamic stop-loss + Tiered ROI take-profit, combined with other trade status decisions |
| **Protection Mechanisms** | Order timeout protection, entry confirmation, price slippage protection |
| **Timeframe** | Main timeframe 5m + Information timeframe 1h |
| **Dependencies** | numpy, talib, qtpylib, arrow, pandas, technical.indicators.RMI, cachetools.TTLCache |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.10,     # Immediately requires 10% profit
    "15": 0.05,    # After 15 minutes requires 5%
    "30": 0.025,   # After 30 minutes requires 2.5%
    "60": 0.01,    # After 1 hour requires 1%
    "120": 0.005,  # After 2 hours requires 0.5%
    "1440": 0      # After 24 hours accepts any profit
}

# Stop-loss setting
stoploss = -0.40  # 40% hard stop-loss

# Signal configuration
use_sell_signal = True
sell_profit_only = True
ignore_roi_if_buy_signal = True  # Key: Ignore ROI when buy signal is active
```

**Design Philosophy**:
- ROI thresholds decrease over time, from 10% down to 0%, adapting to medium-term holdings
- Stop-loss is relatively wide (-40%), providing ample room for volatility
- `ignore_roi_if_buy_signal = True` is the core, allowing position continuation signals to override ROI

### 2.2 Order Type Configuration

The strategy does not explicitly define `order_types`, using Freqtrade default configuration.

### 2.3 Buy Parameters

```python
buy_params = {
    'rmi-slow': 20,      # Slow RMI lower limit
    'rmi-fast': 20,      # Fast RMI upper limit
    'mp': 50,            # Momentum Pinball upper limit
    'inf-rsi': 30,       # Information layer RSI lower limit
    'inf-pct-adr': 0.8   # ADR percentile threshold
}
```

---

## 3. Buy Conditions Detailed

### 3.1 Technical Indicator System

The strategy uses a multi-dimensional indicator combination:

| Indicator Category | Specific Indicator | Parameters | Purpose |
|-------------------|---------------------|------------|---------|
| **Momentum** | RMI-slow | length=21, mom=5 | Trend direction judgment |
| **Momentum** | RMI-fast | length=8, mom=4 | Fast signal capture |
| **Momentum** | ROC | timeperiod=6 | Rate of change measurement |
| **Composite** | Momentum Pinball | RSI(ROC, 6) | Overbought/oversold positioning |
| **Trend** | RMI-up-trend | rolling(3) >= 2 | Uptrend confirmation |
| **Trend** | RMI-dn-trend | rolling(3) >= 2 | Downtrend confirmation |
| **Info Layer** | RSI_1h | timeperiod=14 | Higher-dimension trend judgment |
| **Info Layer** | 1d_high/3d_low | rolling(24/72) | Price range positioning |
| **Info Layer** | ADR | 1d_high - 3d_low | Volatility range calculation |

### 3.2 Buy Condition Classification

The strategy uses different buy logic based on whether there's an active trade:

#### Condition Group #1: New Position Buy Signal (No Active Trade)

```python
# Core logic
conditions = [
    RSI_1h >= 30,                                    # 1-hour RSI not below 30
    close <= 3d_low_1h + 0.8 * ADR_1h,              # Price within 80% volatility range above 3-day low
    rmi-dn-trend == 1,                               # RMI downtrend confirmation
    rmi-slow >= 20,                                  # Slow RMI not below 20
    rmi-fast <= 20,                                  # Fast RMI not above 20
    mp <= 50,                                        # Momentum Pinball not exceeding 50
    volume > 0                                       # Has volume
]
```

**Logic Interpretation**:
- Information layer RSI >= 30: Ensures not in extreme oversold state
- Price positioning: Bottom fish but not at the lowest point, leaving 80% volatility space
- RMI configuration: Slow RMI >= 20 (not extremely weak), Fast RMI <= 20 (short-term momentum low)
- Trend confirmation: Looking for reversal opportunities during RMI downtrend
- Momentum Pinball: Waiting for momentum to stabilize

#### Condition Group #2: Position Continuation Buy Signal (Active Trade Exists)

```python
# Core logic - for ignore_roi_if_buy_signal mechanism
conditions = [
    rmi-up-trend == 1,                               # RMI uptrend
    current_profit > peak_profit * profit_factor,    # Dynamic profit factor
    rmi-slow >= rmi_grow                             # RMI dynamic growth threshold
]

# profit_factor calculation
profit_factor = 1 - (rmi-slow / 400)  # rmi 30 -> 0.925, rmi 80 -> 0.80

# rmi_grow calculation (linear growth)
rmi_grow = linear_growth(30, 70, 180, 720, open_minutes)
# Grows from 30 to 70
# Start time: after 180 minutes
# End time: after 720 minutes
```

**Logic Interpretation**:
- Trend continuation: RMI uptrend confirmation, preventing premature selling
- Dynamic profit factor: As RMI rises, profit requirements decrease (encouraging trend holding)
- Linear growth threshold: As holding time increases, RMI threshold gradually increases, forcing trend confirmation

### 3.3 Buy Conditions Summary

| Condition Group | Applicable Scenario | Core Logic |
|-----------------|---------------------|------------|
| New position buy | No active trade | Information layer positioning + RMI contrarian bottom fishing + Momentum confirmation |
| Position continuation | Active trade exists | Trend confirmation + Dynamic profit factor + RMI growth threshold |

---

## 4. Sell Logic Detailed

### 4.1 Tiered Take-Profit System (ROI)

The strategy uses a time-decay ROI mechanism:

```
Holding Time      Profit Threshold    Description
─────────────────────────────────────────────────
0 minutes         10%                 Very short-term high profit target
15 minutes        5%                  Quick take-profit
30 minutes        2.5%                Medium-term target
60 minutes        1%                  Lowered expectations
120 minutes       0.5%                Accept small profit
1440 minutes      0%                  Accept any profit
```

### 4.2 Dynamic Stop-Loss Sell

The strategy's sell signal is mainly used for "dynamic stop-loss" rather than active take-profit:

```python
# Dynamic stop-loss conditions
if active_trade:
    loss_cutoff = linear_growth(-0.03, 0, 0, 300, open_minutes)
    # Grows from -3% to 0%
    # Start time: immediately
    # End time: after 300 minutes
    
    conditions = [
        current_profit < loss_cutoff,              # Profit below dynamic threshold
        current_profit > stoploss,                 # But hasn't hit hard stop-loss
        rmi-dn-trend == 1,                         # RMI downtrend
        volume > 0                                 # Has volume
    ]
    
    # Profit status branching
    if peak_profit > 0:
        conditions += [rmi-slow crossed_below 50]  # Was profitable: RMI crosses below 50
    else:
        conditions += [rmi-slow crossed_below 10]  # Never profitable: RMI crosses below 10
```

**Logic Interpretation**:
- Dynamic threshold: Longer holding time means higher stop-loss threshold (from -3% to 0%)
- Trend confirmation: Only triggers during downtrend, avoiding false sells in choppy markets
- Profit status branching: Previously profitable trades use looser sell conditions (RMI 50), never profitable trades use stricter conditions (RMI 10)

### 4.3 Other Trade Status Awareness

The strategy implements a global position awareness mechanism:

```python
if other_trades:
    if free_slots > 0:
        # When there are free slots, reference other trades' average profit
        max_market_down = -0.04
        hold_pct = (1 / free_slots) * max_market_down
        conditions += [avg_other_profit >= hold_pct]
        # More free slots means more willing to hold
        # 1 slot -> avg_other_profit >= -0.04
        # 4 slots -> avg_other_profit >= -0.01
    else:
        # When no free slots, only allow biggest losing trade to sell
        conditions += [biggest_loser == True]
```

**Design Philosophy**:
- When there are free slots, decide whether to sell based on overall market state
- When fully invested, prioritize stopping out the biggest losing trade to release capital

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|---------------------|---------|
| **Relative Momentum Index** | RMI-slow (21, 5) | Main trend judgment |
| **Relative Momentum Index** | RMI-fast (8, 4) | Fast signal |
| **Rate of Change** | ROC (6) | Momentum measurement |
| **Momentum Pinball** | MP = RSI(ROC, 6) | Overbought/oversold positioning |
| **Trend Direction** | RMI-up/dn | Single period direction |
| **Trend Strength** | RMI-up-trend/dn-trend | Three-period confirmation |

### 5.2 Information Timeframe Indicators (1h)

The strategy uses the 1-hour timeframe as an information layer for higher-dimension trend judgment:

- **RSI_1h**: 14-period RSI, ensures not entering extreme oversold state
- **1d_high**: 24-hour (1 day) high
- **3d_low**: 72-hour (3 day) low
- **ADR**: Average Daily Range (1d_high - 3d_low)

**Price Positioning Logic**:
```
Buy price upper limit = 3d_low + inf_pct_adr * ADR
                       = 3d_low + 0.8 * ADR
```

---

## 6. Risk Management Features

### 6.1 Hard Stop-Loss Combined with Dynamic Stop-Loss

The strategy uses a dual stop-loss mechanism:

| Stop-Loss Type | Threshold | Trigger Condition |
|----------------|-----------|-------------------|
| Hard stop-loss | -40% | Fixed trigger |
| Dynamic stop-loss | -3% → 0% | Holding time + Trend confirmation |

**Dynamic Stop-Loss Advantages**:
- Early period (holding 0-300 minutes): Stop-loss threshold gradually increases from -3%
- Late period (holding >300 minutes): Stop-loss threshold is 0%, protecting realized profit
- Only triggers during downtrend, avoiding false sells in choppy markets

### 6.2 Order Timeout Protection

```python
def check_buy_timeout(self, pair, trade, order, **kwargs):
    # Buy order timeout: Cancel if price slippage > 1%
    if current_price > order_price * 1.01:
        return True  # Cancel order
    return False

def check_sell_timeout(self, pair, trade, order, **kwargs):
    # Sell order timeout: Cancel if price slippage > 1%
    if current_price < order_price * 0.99:
        return True  # Cancel order
    return False
```

### 6.3 Entry Confirmation Mechanism

```python
def confirm_trade_entry(self, pair, order_type, amount, rate, time_in_force, **kwargs):
    # Pre-entry confirmation: Reject if price slippage > 1%
    if current_price > rate * 1.01:
        return False  # Reject entry
    return True
```

**Slippage Protection Logic**:
- Uses real-time order book to get current price
- Cancel/reject when order price differs from current price by > 1%
- Prevents unfavorable fills during extreme market conditions

### 6.4 Price Cache Mechanism

```python
custom_current_price_cache: TTLCache = TTLCache(maxsize=100, ttl=300)  # 5-minute TTL
```

**Cache Strategy**:
- Maximum cache of 100 trading pairs
- TTL 300 seconds (5 minutes)
- Reduces unnecessary API calls

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Dynamic Profit Factor**: `ignore_roi_if_buy_signal` mechanism combined with dynamic profit factor maximizes holding returns during trending markets

2. **Global Position Awareness**: Strategy is aware of other trade statuses, enabling cross-trade coordinated decisions and avoiding misoperations when fully invested

3. **Multi-Layer Protection Mechanism**: Hard stop-loss + Dynamic stop-loss + Order timeout + Entry confirmation, four-layer protection network

4. **Information Layer Enhancement**: 1-hour timeframe provides higher-dimension trend judgment, reducing noise interference

5. **Linear Growth Threshold**: Dynamically adjusted RMI threshold adapts to different holding durations

### ⚠️ Limitations

1. **Live Trading Only**: `ignore_roi_if_buy_signal` and position continuation signals are not compatible with backtesting and hyperparameter optimization

2. **Wide Stop-Loss**: 40% hard stop-loss may be too wide for conservative traders

3. **Real-Time Data Dependency**: Requires database access to query other trade statuses, demanding high system stability

4. **Computational Complexity**: Multiple indicators, multiple timeframes, multiple trade awareness, significant computational overhead

5. **Parameter Sensitivity**: Buy parameters are optimized, may have overfitting risk

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| **Slow bull market** | Default configuration | Trend continuation signals work effectively |
| **Choppy market** | Raise stop-loss threshold | Reduce false breakout-induced stop-losses |
| **Sharp decline** | Lower RSI threshold | Bottom fish earlier, but increased risk |
| **High volatility coins** | Expand ADR percentage | Adapt to larger volatility ranges |

**Recommended Trading Pairs**:
- Liquid major coins (BTC, ETH, large-cap altcoins)
- Avoid extremely volatile small coins (stop-loss may not trigger in time)

---

## 9. Applicable Market Environment Details

The Schism series is a **"bottom-fishing trend following strategy"**. Based on its code architecture and long-term live trading verification from the community, it is best suited for **rebound markets after oscillating declines**, while performing poorly during **one-sided crashes**.

### 9.1 Strategy Core Logic

- **Bottom fish but not at the lowest point**: Price positioned at 80% volatility range above 3-day low, leaving safety margin
- **Momentum confirmation**: Looking for reversal opportunities during RMI downtrend, avoiding chasing highs
- **Trend continuation**: During holding period, maximize trend returns through buy signal continuation mechanism
- **Global coordination**: Aware of other trade statuses, enabling cross-trade capital management

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:------------------|:----------------|
| 📈 **Slow bull market** | ⭐⭐⭐⭐⭐ | Trend continuation mechanism fully发挥作用，持仓收益最大化 |
| 🔄 **Choppy market** | ⭐⭐⭐☆☆ | Bottom fishing signals may trigger multiple times, watch out for fees |
| 📉 **One-sided crash** | ⭐⭐☆☆☆ | Bottom fishing signals may trigger too early, wide stop-loss poses risk |
| ⚡️ **Rapid rise/fall** | ⭐☆☆☆☆ | Order timeout protection may fail, high slippage risk |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|------------------|-------------|
| `max_open_trades` | 3-5 | Coordinate with global position awareness, avoid over-diversification |
| `stake_amount` | Equal allocation | Coordinate with `free_slots` logic |
| `timeframe` | 5m | Native configuration, not recommended to modify |
| `inf_timeframe` | 1h | Information layer configuration, not recommended to modify |

---

## 10. Important Warning: The Cost of Complexity

### 10.1 Learning Curve

Schism strategy code is approximately 200 lines, including:
- Multi-timeframe indicator calculations
- Real-time database queries
- Dynamic threshold calculations
- Global position awareness

It is recommended to run in **dry_run mode** for at least 1 week before live trading to familiarize yourself with strategy behavior.

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 2 GB | 4 GB |
| 10-30 pairs | 4 GB | 8 GB |
| 30+ pairs | 8 GB | 16 GB |

**Note**: The strategy requires database access to query other trade statuses, with significant memory overhead in multi-pair scenarios.

### 10.3 Differences Between Backtesting and Live Trading

**Key Differences**:
- `ignore_roi_if_buy_signal` and position continuation signals **only work in live trading/dry run**
- Cannot access `Trade.get_trades()` data during backtesting
- Backtesting results may differ significantly from live trading performance

**Recommended Workflow**:
1. First use backtesting to verify buy signal quality
2. Then use dry_run to verify dynamic logic
3. Finally small position live trading verification

### 10.4 Manual Trader Recommendations

Schism's core concepts can be borrowed:
- **Momentum-confirmed bottom fishing**: Look for reversals during RMI downtrend, not blind bottom fishing
- **Dynamic stop-loss**: Longer holding time means tighter stop-loss threshold
- **Global perspective**: Consider the overall state of all positions, avoid full-investment risks

---

## 11. Summary

**Schism** is a **"bottom-fishing trend following strategy"** that implements a trading logic of "bottom fishing but not at the lowest point" through RMI momentum indicator multi-dimensional analysis combined with 1-hour information layer trend judgment. Its core value lies in:

1. **Dynamic Position Continuation**: `ignore_roi_if_buy_signal` mechanism maximizes returns during trending markets
2. **Global Position Awareness**: Cross-trade coordinated decisions, avoiding capital management failures
3. **Multi-Layer Protection Network**: Hard stop-loss + Dynamic stop-loss + Order timeout + Entry confirmation
4. **Information Layer Enhancement**: 1-hour timeframe provides higher-dimension trend judgment

For quantitative traders, Schism is a **live-trading-oriented strategy**, suitable for experienced traders. Not recommended for beginners to use directly. It is recommended to start with Schism2 (evolved version) or default parameters and gradually optimize.