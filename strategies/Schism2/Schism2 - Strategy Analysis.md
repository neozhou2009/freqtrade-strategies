# Schism2 Strategy Analysis

> **Strategy Number**: #24 (24th of 465 strategies)  
> **Strategy Type**: RMI + Multi-Timeframe Trend Following  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

**Schism2** is an advanced trend following strategy developed by @werkkrew and @JimmyNixx, an evolved version of the Schism framework. Key features include dynamic buy/sell signals, multi-timeframe confirmation, and dynamic exit logic based on trade state. The strategy supports additional confirmation logic for BTC/ETH staking.

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | Multi-condition combination (RMI + ADR + Multi-timeframe) |
| **Exit Conditions** | Dynamic stoploss + ROI exit |
| **Protection** | Custom trade data management + Price caching |
| **Timeframe** | 5 minutes |
| **Dependencies** | TA-Lib, technical, numpy, cachetools |
| **Special Features** | Dynamic trade data, multi-timeframe, BTC/ETH staking support |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.05,      # Immediate exit: 5% profit
    "10": 0.025,    # After 10 minutes: 2.5% profit
    "20": 0.015,    # After 20 minutes: 1.5% profit
    "30": 0.01,     # After 30 minutes: 1% profit
    "720": 0.005,   # After 720 minutes: 0.5% profit
    "1440": 0,      # After 1440 minutes: exit at breakeven
}

# Stoploss setting
stoploss = -0.30  # -30% hard stoploss
```

**Design Logic**:
- **Multi-Level ROI**: 6-level decreasing ROI, longer holding time means lower exit threshold
- **Loose Stoploss**: -30% hard stoploss, giving ample room for fluctuation
- **Long Holding Protection**: Exit at breakeven after 1440 minutes (24 hours)

---

## III. Entry Conditions Explained

### 3.1 Entry Logic (No Position)

```python
# Main entry conditions
(
    (close <= 3d_low + (inf_pct_adr * adr)) &  # Price <= 3-day low + ADR percentage
    (rsi_1h >= inf_rsi) &                       # 1h RSI >= threshold
    (rmi_dn_trend == 1) &                       # RMI downtrend
    (rmi_slow >= rmi_slow_param) &              # RMI slow >= threshold
    (rmi_fast <= rmi_fast_param) &              # RMI fast <= threshold
    (mp <= mp_param) &                          # Momentum Pinball <= threshold
    (volume > 0)                                 # Volume > 0
)
```

**Logic Analysis**:
- **ADR Pullback**: Price pulls back to 3-day low + ADR percentage
- **1h RSI Confirmation**: 1-hour RSI above threshold
- **RMI Trend**: RMI downtrend confirmation
- **Momentum Pinball**: Momentum indicator confirms oversold

### 3.2 Entry Logic (With Position)

```python
# Continuous entry conditions (ignore ROI)
(
    (rmi_up_trend == 1) &                              # RMI uptrend
    (current_profit > peak_profit * profit_factor) &   # Current profit > peak profit × factor
    (rmi_slow >= rmi_grow) &                           # RMI slow >= growth value
    (volume > 0)                                        # Volume > 0
)
```

**Purpose**:
- Continuous buying in trend
- Use `ignore_roi_if_entry_signal = True` to block premature exit

---

## IV. Exit Logic Explained

### 4.1 Dynamic Stoploss Logic

```python
# If in loss state
if current_profit < loss_cutoff:  # loss_cutoff grows from -0.03 to 0
    if rmi_dn_trend == 1:  # RMI downtrend
        # If peak profit was positive but never reached ROI
        if peak_profit > 0:
            crossed_below(rmi_slow, 50)  # RMI slow crosses below 50
        else:
            crossed_below(rmi_slow, 10)  # RMI slow crosses below 10
```

**Purpose**:
- Dynamic stoploss threshold (grows from -3% to 0%)
- Adjust exit conditions based on peak profit

### 4.2 Multi-Trade State Management

```python
# If other open trades exist
if other_trades:
    if free_slots > 0:
        # Adjust exit threshold based on free slots
        max_market_down = -0.04
        hold_pct = (1 / free_slots) * max_market_down
        avg_other_profit >= hold_pct
    else:
        # If no free slots, allow largest losing trade to exit
        biggest_loser == True
```

**Purpose**:
- Adjust exit strategy based on free slots
- Prioritize releasing largest losing positions

---

## V. Risk Management Features

### 5.1 Dynamic Stoploss Threshold

```python
# Grows from -0.03 to 0, completes in 300 minutes
loss_cutoff = linear_growth(-0.03, 0, 0, 300, open_minutes)
```

**Purpose**:
- Stoploss threshold grows over time
- More loose early, stricter later

### 5.2 Multi-Trade State Management

```python
# Adjust exit threshold based on free slots
hold_pct = (1 / free_slots) * max_market_down
```

**Purpose**:
- More willing to sell when free slots are few
- Prioritize releasing largest losing positions

---

## VI. Strategy Pros & Cons

### ✅ Advantages

1. **Dynamic Buy/Sell Logic**: Dynamically adjusts based on trade state
2. **Multi-Timeframe Confirmation**: 1h informative timeframe confirms trend
3. **Multi-Trade State Management**: Adjusts exit strategy based on free slots
4. **BTC/ETH Staking Support**: Additional staking currency confirmation
5. **Price Caching**: Reduces API calls, improves efficiency
6. **Hyperopt Optimization**: Supports Hyperopt for key parameters

### ⚠️ Limitations

1. **Extremely High Complexity**: Dynamic logic + multi-timeframe, difficult to debug
2. **Live Trading Only**: Dynamic trade data not available in backtest
3. **No BTC Market Correlation**: Does not detect Bitcoin market trend (unless staking is BTC)
4. **High Computation**: Multi-indicator + dynamic data increases computation
5. **Parameter Sensitive**: Hyperopt results may overfit

---

## VII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| **Ranging Market** | Default configuration | Multi-timeframe suitable for ranging markets |
| **Uptrend** | Default configuration | Dynamic buy/sell + multi-timeframe performs well |
| **Downtrend** | Pause or light position | Dynamic stoploss will manage losses |
| **High Volatility** | Adjust parameters | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |

---

## VIII. Summary

**Schism2** is a well-designed advanced trend following strategy, its core value lies in:

1. **Dynamic Buy/Sell Logic**: Dynamically adjusts based on trade state
2. **Multi-Timeframe Confirmation**: 1h informative timeframe confirms trend
3. **Multi-Trade State Management**: Adjusts exit strategy based on free slots
4. **BTC/ETH Staking Support**: Additional staking currency confirmation
5. **Price Caching**: Reduces API calls, improves efficiency
6. **Hyperopt Optimization**: Supports Hyperopt for key parameters

For quantitative traders, this is an excellent advanced strategy learning template. Recommendations:
- Use as an advanced case for learning dynamic trade state
- Understand multi-timeframe usage
- Learn multi-trade state management
- Note live trading only, backtest cannot test dynamic logic

---
