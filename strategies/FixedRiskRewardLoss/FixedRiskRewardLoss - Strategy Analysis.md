# FixedRiskRewardLoss Strategy Analysis

> **Strategy Number**: #6 (6th of 465 strategies)  
> **Strategy Type**: Fixed Risk/Reward Ratio Dynamic Stoploss Strategy  
> **Timeframe**: 5 minutes (5m)

---

## 1. Strategy Overview

**FixedRiskRewardLoss** is an example strategy demonstrating how to implement fixed risk/reward ratio dynamic stoploss management through the `custom_stoploss()` function. The core idea is: calculate initial stoploss based on ATR, then set take-profit target at 3.5 times the initial risk, and adjust stoploss to breakeven after reaching certain profit level.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | None (example strategy, always enters) |
| **Exit Conditions** | No technical exits, relies on dynamic stoploss |
| **Protection** | Fixed risk/reward ratio + breakeven stoploss |
| **Timeframe** | 5 minutes |
| **Dependencies** | TA-Lib |
| **Special Features** | Risk/reward ratio management, breakeven stoploss |

---

## 2. Configuration Analysis

### 2.1 Base Risk Parameters

```python
# Hard stoploss
stoploss = -0.10  # -10%

# Custom stoploss configuration
use_custom_stoploss = True
custom_info = {
    "risk_reward_ratio": 3.5,      # Risk/reward ratio 3.5:1
    "set_to_break_even_at_profit": 1,  # Breakeven at 1x risk profit
}
```

**Design Logic**:
- **Risk/Reward Ratio 3.5:1**: For every $1 risk, expects $3.5 return
- **Breakeven Mechanism**: After reaching 1x risk profit, adjust stoploss to breakeven
- **Example Nature**: Focus on demonstrating money management techniques

### 2.2 Order Type Configuration

Uses Freqtrade default configuration.

---

## 3. Entry Conditions Explained

### 3.1 Entry Logic

```python
# Entry conditions
dataframe.loc[:, "buy"] = 1  # Always buy
```

**Logic Analysis**:
- **Example Strategy**: Entry logic is not the focus, simplified to always buy
- **Focus on Stoploss**: Core of strategy is demonstrating dynamic stoploss management
- **Practical Application**: Replace with real entry signals for live trading

---

## 4. Exit Logic Explained

### 4.1 Custom Stoploss Function

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs) -> float:
    # Get initial stoploss at entry
    initial_sl_abs = open_df["stoploss_rate"]
    initial_sl = initial_sl_abs / current_rate - 1
    
    # Calculate initial risk
    risk_distance = trade.open_rate - initial_sl_abs
    
    # Calculate take-profit target (risk × 3.5)
    reward_distance = risk_distance * 3.5
    take_profit_price_abs = trade.open_rate + reward_distance
    takeprofit_sl = take_profit_price_abs / current_rate - 1
    
    # Calculate breakeven level
    break_even_profit_distance = risk_distance * 1
    break_even_sl = (trade.open_rate * (1 + fee) / current_rate) - 1
    
    # Priority: take-profit > breakeven > initial stoploss
    result = initial_sl
    if current_profit >= break_even_profit_pct:
        result = break_even_sl
    if current_profit >= take_profit_pct:
        result = takeprofit_sl
    
    return result
```

**Working Mechanism**:
1. Calculate initial stoploss based on ATR at entry
2. Set take-profit at 3.5x the initial risk distance
3. Move stoploss to breakeven after reaching 1x risk profit
4. Dynamically adjust stoploss based on current profit level

---

## 5. Risk Management Features

### 5.1 Fixed Risk/Reward Ratio

**Core Principle**:
- Risk: Distance from entry to initial stoploss
- Reward: Distance from entry to take-profit (3.5x risk)
- Ensures positive expectancy over multiple trades

### 5.2 Breakeven Stoploss

**Mechanism**:
- After profit reaches 1x risk amount, move stoploss to breakeven
- Protects capital after trade moves in favor
- Eliminates risk on winning trades

### 5.3 Hard Stoploss Backup

```python
stoploss = -0.10  # -10%
```

**Purpose**: Final backup if custom stoploss fails.

---

## 6. Strategy Strengths and Limitations

### ✅ Strengths

1. **Educational Value**: Excellent example of custom stoploss implementation
2. **Risk Management**: Fixed risk/reward ensures positive expectancy
3. **Breakeven Protection**: Eliminates risk on winning trades
4. **Flexible Framework**: Can be adapted with real entry signals
5. **ATR-Based**: Initial stoploss adapts to market volatility

### ⚠️ Limitations

1. **No Entry Logic**: Must add real entry signals for production use
2. **No Technical Exits**: Relies entirely on stoploss management
3. **Example Only**: Not intended for direct production use
4. **Requires Customization**: Needs adaptation for specific strategies

---

## 7. Implementation Guide

### 7.1 Adding Entry Signals

Replace the always-buy logic with real signals:
```python
# Example: Add RSI oversold entry
dataframe.loc[
    (dataframe["rsi"] < 30),
    "buy",
] = 1
```

### 7.2 Adjusting Risk/Reward

Modify based on strategy characteristics:
- Conservative: 2:1 or 3:1 ratio
- Aggressive: 4:1 or 5:1 ratio

### 7.3 Breakeven Level

Adjust `set_to_break_even_at_profit`:
- Lower value (0.5): Move to breakeven sooner
- Higher value (2): Allow more room before breakeven

---

## 8. Summary

**FixedRiskRewardLoss** is an educational strategy demonstrating advanced stoploss management. Its core value lies in:

1. **Custom Stoploss Example**: Shows how to implement `custom_stoploss()`
2. **Risk/Reward Framework**: Fixed ratio ensures positive expectancy
3. **Breakeven Mechanism**: Protects profits on winning trades
4. **Adaptable Design**: Can be customized with real entry signals

For quantitative traders, this is an excellent learning template for:
- Understanding custom stoploss implementation
- Learning risk/reward ratio management
- Implementing breakeven stoploss logic
- Building robust risk management systems

**Recommendations**:
- Study the custom_stoploss() implementation carefully
- Add real entry signals for production use
- Adjust risk/reward ratio based on strategy characteristics
- Test thoroughly before live deployment

---
