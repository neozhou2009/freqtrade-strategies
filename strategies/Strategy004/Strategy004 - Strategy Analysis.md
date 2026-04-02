# Strategy004 In-Depth Analysis

> **Strategy ID**: #395 (395th of 465 strategies)  
> **Strategy Type**: Multi-Indicator Oversold Reversal + Trend Strength Filter  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

Strategy004 is a Stochastic oscillator oversold reversal strategy with ADX trend strength confirmation. It captures oversold reversal opportunities through dual timeframe Stochastic indicators while requiring ADX indicator to confirm trend strength, entering during trend continuation.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 comprehensive buy signal with multiple condition combinations |
| **Sell Conditions** | 1 basic sell signal + tiered ROI take-profit |
| **Protection Mechanism** | Trailing stop + Fixed stop loss -10% |
| **Timeframe** | 5-minute primary timeframe |
| **Dependencies** | talib (TA-Lib technical analysis library) |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "60": 0.01,  # Take profit 1% after 60 minutes
    "30": 0.03,  # Take profit 3% after 30 minutes
    "20": 0.04,  # Take profit 4% after 20 minutes
    "0":  0.05   # Take profit 5% immediately
}

# Stop loss setting
stoploss = -0.10  # Fixed 10% stop loss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01      # Activate trailing after 1% profit
trailing_stop_positive_offset = 0.02  # Trailing drawdown tolerance 2%
```

**Design Philosophy**:
- Tiered ROI design: longer holding time means lower take-profit target, encouraging quick profit exits
- 5% immediate take-profit target is aggressive, suitable for short-term operations
- 10% fixed stop loss provides larger price fluctuation tolerance
- Trailing stop protects realized profits

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',           # Limit buy
    'sell': 'limit',          # Limit sell
    'stoploss': 'market',     # Market stop loss execution
    'stoploss_on_exchange': False
}
```

---

## III. Buy Conditions Detailed Analysis

### 3.1 Buy Signal Core Logic

The strategy employs a single but complex buy signal with the following condition combinations:

```python
# Complete buy signal logic
(
    # Condition 1: Trend strength confirmation (either one)
    (dataframe['adx'] > 50) | (dataframe['slowadx'] > 26)
) &
# Condition 2: CCI oversold
(dataframe['cci'] < -100) &
# Condition 3: Fast Stochastic oversold
(dataframe['fastk-previous'] < 20) & (dataframe['fastd-previous'] < 20) &
# Condition 4: Slow Stochastic oversold
(dataframe['slowfastk-previous'] < 30) & (dataframe['slowfastd-previous'] < 30) &
# Condition 5: Stochastic golden cross
(dataframe['fastk-previous'] < dataframe['fastd-previous']) &
(dataframe['fastk'] > dataframe['fastd']) &
# Condition 6: Volume filter
(dataframe['mean-volume'] > 0.75) &
# Condition 7: Price filter
(dataframe['close'] > 0.00000100)
```

### 3.2 Condition Classification Analysis

| Condition Group | Condition Content | Logic Explanation |
|----------------|-------------------|-------------------|
| **Trend Strength** | ADX > 50 or Slow ADX > 26 | Confirms market has trend, avoids false signals in ranging markets |
| **Oversold Confirmation** | CCI < -100 | Commodity Channel Index confirms oversold condition |
| **Fast Stochastic Oversold** | Fast K/D previous value < 20 | Fast period (5 candles) Stochastic deeply oversold |
| **Slow Stochastic Oversold** | Slow K/D previous value < 30 | Slow period (50 candles) Stochastic confirms oversold |
| **Golden Cross Signal** | Fast K crosses above Fast D | Stochastic generates buy golden cross |
| **Volume Filter** | Average volume > 0.75 | Ensures sufficient market liquidity |
| **Price Filter** | Close price > 0.00000100 | Filters extremely low-priced coins, avoids liquidity traps |

### 3.3 Dual Stochastic Indicator System

The strategy uses two periods of Stochastic indicators:

| Period | Parameters | Purpose |
|--------|------------|---------|
| **Fast Stochastic** | 5-period candles | Captures short-term oversold reversal signals |
| **Slow Stochastic** | 50-period candles | Confirms medium-term oversold condition |

**Design Philosophy**: Fast period provides entry timing, slow period confirms trend background, dual verification improves signal reliability.

---

## IV. Sell Logic Detailed Analysis

### 4.1 Sell Signal Logic

```python
# Complete sell signal logic
(
    # Condition 1: Trend weakening
    (dataframe['slowadx'] < 25) &
    # Condition 2: Fast Stochastic overbought (either one)
    ((dataframe['fastk'] > 70) | (dataframe['fastd'] > 70)) &
    # Condition 3: Stochastic death cross
    (dataframe['fastk-previous'] < dataframe['fastd-previous']) &
    # Condition 4: Price position confirmation
    (dataframe['close'] > dataframe['ema5'])
)
```

### 4.2 Sell Condition Analysis

| Condition | Logic Explanation |
|-----------|-------------------|
| **Slow ADX < 25** | Trend strength weakening, market may enter consolidation |
| **Fast K/D > 70** | Stochastic enters overbought territory |
| **Fast K crosses below Fast D** | Stochastic death cross, confirms uptrend momentum exhaustion |
| **Close > EMA5** | Ensures selling while price is still above moving average, locking in profits |

### 4.3 Tiered ROI Take-Profit

```
Holding Time    Take-Profit Target
────────────────────────────────────
60+ minutes     1%
30-60 minutes   3%
20-30 minutes   4%
0-20 minutes    5%
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Trend Strength** | ADX (14-period), Slow ADX (35-period) | Confirm market trend strength |
| **Overbought/Oversold** | CCI (Commodity Channel Index) | Identify oversold conditions |
| **Stochastic** | Fast Stochastic (5-period), Slow Stochastic (50-period) | Capture reversal signals |
| **Trend Following** | EMA5 (5-period Exponential Moving Average) | Short-term trend reference |
| **Volume** | Average volume | Liquidity filter |

### 5.2 Indicator Calculation Details

```python
# ADX indicator
dataframe['adx'] = ta.ADX(dataframe)          # Default 14-period
dataframe['slowadx'] = ta.ADX(dataframe, 35)   # 35-period slow ADX

# CCI indicator
dataframe['cci'] = ta.CCI(dataframe)           # Commodity Channel Index

# Fast Stochastic (5-period)
stoch = ta.STOCHF(dataframe, 5)
dataframe['fastd'] = stoch['fastd']
dataframe['fastk'] = stoch['fastk']

# Slow Stochastic (50-period)
slowstoch = ta.STOCHF(dataframe, 50)
dataframe['slowfastd'] = slowstoch['fastd']
dataframe['slowfastk'] = slowstoch['fastk']

# EMA
dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
```

---

## VI. Risk Management Features

### 6.1 Multi-Layer Filter Mechanism

The strategy employs multi-level condition filtering:

1. **Trend Filter**: ADX indicator ensures trading only in trending markets
2. **Oversold Confirmation**: CCI and dual Stochastic confirm oversold conditions
3. **Volume Filter**: Ensures sufficient liquidity
4. **Price Filter**: Avoids liquidity risks of extremely low-priced coins

### 6.2 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_stop_positive = 0.01      # Activate trailing after 1% profit
trailing_stop_positive_offset = 0.02  # Trailing drawdown tolerance 2%
```

**Mechanism Explanation**:
- When profit reaches 2%, trailing stop activates
- Trailing stop distance is 1% drawdown from current price
- Protects realized profits while allowing price fluctuation room

### 6.3 Fixed Stop Loss

- 10% fixed stop loss provides larger error tolerance
- Suitable for highly volatile cryptocurrency markets

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Trend Confirmation Mechanism**: ADX indicator ensures entry only in trending markets, reducing false signals in ranging markets
2. **Dual Verification System**: Fast and slow Stochastic dual verification improves signal reliability
3. **Flexible Trend Strength Judgment**: ADX > 50 or Slow ADX > 26 adapts to different market rhythms
4. **Volume Filter**: Avoids slippage risk in low-liquidity coins
5. **Trailing Stop Protection**: Dynamically protects profits while considering trend continuation

### ⚠️ Limitations

1. **Single Buy Signal**: All conditions must be met simultaneously, may miss some opportunities
2. **Fixed Parameters**: No Hyperopt optimization support, difficult to adapt to market changes
3. **Oversold Reversal Dependency**: May frequently enter and get trapped in continuous downtrend markets
4. **ADX Lag**: Trend strength indicator has lag, may miss early trend stages
5. **Hardcoded Price Filter**: May not apply to all trading pairs

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Trend Continuation** | Default parameters | Strategy's core designed scenario |
| **Ranging Market** | Not recommended | ADX filter reduces signals, but may still generate false signals |
| **Sharp Drop Rebound** | Use cautiously | Good oversold reversal capture, but watch stop loss |
| **Slow Bull Market** | Can try | Stochastic overbought sell signal may exit too early |

---

## IX. Applicable Market Environment Details

Strategy004 is a typical **oversold reversal strategy**. Based on its code architecture and logic design, it is best suited for **pullback trends during trend continuation**, while performance may be poor in **continuous one-sided decline** or **sideways consolidation**.

### 9.1 Strategy Core Logic

- **Trend Confirmation Priority**: ADX indicator ensures entry only when trend is clear
- **Oversold Reversal Capture**: Multiple oversold indicators confirm, seeking rebound starting points
- **Fast Response**: 5-minute timeframe suitable for short-term operations

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| 📈 Uptrend Pullback | ⭐⭐⭐⭐⭐ | ADX confirms trend, Stochastic captures pullback entry points |
| 🔄 Wide Range Consolidation | ⭐⭐☆☆☆ | ADX filters some signals, but oversold reversal may be misled by false breakouts |
| 📉 Continuous Decline | ⭐⭐☆☆☆ | Frequent oversold signals, but high reversal failure rate |
| ⚡ High Volatility Sharp Moves | ⭐⭐⭐☆☆ | Stochastic responds quickly, but may be stopped out by oscillation |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|------------------|-------|
| **Stop Loss** | -10% or wider | Leave room for oversold reversal |
| **Trailing Stop** | Keep enabled | Protect rebound profits |
| **Trading Pair Selection** | Major coins | Volume filter may be too loose for altcoins |
| **Timeframe** | 5 minutes | Can try 15 minutes to reduce noise |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

The strategy has many conditions requiring understanding of:
- ADX trend strength indicator principles and thresholds
- Stochastic indicator (K/D) calculation and golden cross/death cross
- CCI oversold region meaning
- Dual Stochastic system verification logic

### 10.2 Hardware Requirements

| Trading Pairs | Minimum Memory | Recommended Memory |
|--------------|----------------|---------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-30 pairs | 4GB | 8GB |
| 30+ pairs | 8GB | 16GB |

### 10.3 Backtest vs Live Trading Differences

- Strategy uses previous value judgment (`fastk-previous`, `fastd-previous`), need to watch candle update timing in live trading
- Volume filter uses global average, may behave abnormally during market open/close periods
- Limit orders may have difficulty filling in fast markets

### 10.4 Manual Trading Recommendations

If manually executing this strategy:
1. Watch if ADX breaks above 26 or 50
2. Wait for Stochastic (5-period) K/D both below 20
3. Confirm CCI below -100
4. Observe K line crossing above D line for entry
5. Set 5% take-profit target and 10% stop loss

---

## XI. Summary

**Strategy004** is a rigorously designed oversold reversal strategy. Its core value lies in:

1. **Trend Confirmation Mechanism**: ADX indicator ensures no trading in trendless markets
2. **Multi-Verification System**: Dual Stochastic + CCI forms multiple layers of filtering
3. **Complete Risk Control**: Tiered ROI + trailing stop + fixed stop loss triple protection

For quantitative traders, this is a short-term strategy suitable for trend continuation pullback scenarios, but attention should be paid to its limitations in continuous decline and ranging markets.