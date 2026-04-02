# SuperTrend Strategy Deep Dive

> **Strategy Number**: #400 (400th of 465 strategies)  
> **Strategy Type**: Triple Supertrend indicator trend following  
> **Timeframe**: 1 hour (1h)

---

## 1. Strategy Overview

SuperTrend is a multi-layer trend following strategy based on the Supertrend indicator. The strategy uses three sets of Supertrend indicators (buy group) and three sets of Supertrend indicators (sell group). Entry occurs when all three buy indicators simultaneously show "up" signal, and exit occurs when all three sell indicators simultaneously show "down" signal. This multiple confirmation mechanism ensures trade reliability.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 3 buy Supertrend indicators simultaneously show "up" |
| **Sell Conditions** | 3 sell Supertrend indicators simultaneously show "down" |
| **Protection Mechanisms** | Trailing stop + Stepped ROI |
| **Timeframe** | 1 hour (1h) |
| **Dependencies** | talib, numpy |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.087,      # Immediate requirement: 8.7% profit
    "372": 0.058,    # After ~6 hours: 5.8%
    "861": 0.029,    # After ~14 hours: 2.9%
    "2221": 0        # After ~37 hours: allow 0% profit exit
}

# Stop loss setting
stoploss = -0.265   # 26.5% hard stop loss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.05
trailing_stop_positive_offset = 0.144
trailing_only_offset_is_reached = False
```

**Design Rationale**:
- ROI table uses stepped decrease, from 8.7% down to 0%
- Stop loss value -0.265 is moderate, working with trailing stop to protect profits
- Trailing stop activates after 5% profit, with offset value of 14.4%
- Does not require reaching offset value before enabling trailing stop

### 2.2 Hyperparameter Configuration

```python
# Buy hyperparameters
buy_params = {
    "buy_m1": 4, "buy_m2": 7, "buy_m3": 1,    # Supertrend multipliers
    "buy_p1": 8, "buy_p2": 9, "buy_p3": 8,    # Supertrend periods
}

# Sell hyperparameters
sell_params = {
    "sell_m1": 1, "sell_m2": 3, "sell_m3": 6,  # Supertrend multipliers
    "sell_p1": 16, "sell_p2": 18, "sell_p3": 18, # Supertrend periods
}
```

### 2.3 Hyperparameter Range Definition

```python
# Buy multiplier range: 1-7
buy_m1 = IntParameter(1, 7, default=4)
buy_m2 = IntParameter(1, 7, default=4)
buy_m3 = IntParameter(1, 7, default=4)

# Buy period range: 7-21
buy_p1 = IntParameter(7, 21, default=14)
buy_p2 = IntParameter(7, 21, default=14)
buy_p3 = IntParameter(7, 21, default=14)

# Sell multiplier range: 1-7
sell_m1 = IntParameter(1, 7, default=4)
sell_m2 = IntParameter(1, 7, default=4)
sell_m3 = IntParameter(1, 7, default=4)

# Sell period range: 7-21
sell_p1 = IntParameter(7, 21, default=14)
sell_p2 = IntParameter(7, 21, default=14)
sell_p3 = IntParameter(7, 21, default=14)
```

---

## 3. Buy Conditions Detailed Analysis

### 3.1 Supertrend Indicator Principle

The Supertrend indicator calculates dynamic support/resistance lines based on ATR (Average True Range):

```
Basic Formula:
Upper Band = (High + Low) / 2 + Multiplier × ATR
Lower Band = (High + Low) / 2 - Multiplier × ATR

Trend Judgment:
Price below upper band → "down" (downtrend)
Price above lower band → "up" (uptrend)
```

### 3.2 Triple Buy Confirmation Mechanism

The strategy uses three sets of Supertrend indicators with different parameters for buy judgment:

```python
def populate_entry_trend(self, dataframe, metadata):
    dataframe.loc[
        (
            (dataframe[f'supertrend_1_buy_{m1}_{p1}'] == 'up') &
            (dataframe[f'supertrend_2_buy_{m2}_{p2}'] == 'up') &
            (dataframe[f'supertrend_3_buy_{m3}_{p3}'] == 'up') &
            (dataframe['volume'] > 0)
        ),
        'buy'] = 1
```

**Three Indicator Groups Comparison**:

| Indicator Group | Multiplier (m) | Period (p) | Sensitivity |
|-----------------|----------------|------------|-------------|
| **Supertrend_1_buy** | 4 | 8 | Medium |
| **Supertrend_2_buy** | 7 | 9 | Slower (larger multiplier) |
| **Supertrend_3_buy** | 1 | 8 | Fast (smaller multiplier) |

**Design Logic**:
- Three indicators cover different sensitivity levels
- Fast indicator captures early signals
- Medium indicator confirms trend
- Slow indicator filters false breakouts
- All three must confirm before entry, improving reliability

### 3.3 Indicator Pre-calculation Mechanism

```python
def populate_indicators(self, dataframe, metadata):
    # Pre-calculate all possible Supertrend combinations
    for multiplier in self.buy_m1.range:
        for period in self.buy_p1.range:
            dataframe[f'supertrend_1_buy_{multiplier}_{period}'] = ...
```

**Optimization Features**:
- Pre-calculate all parameter combinations
- Use cached results at runtime
- Facilitates quick switching during hyperparameter optimization

---

## 4. Sell Logic Detailed Analysis

### 4.1 Triple Sell Confirmation Mechanism

```python
def populate_exit_trend(self, dataframe, metadata):
    dataframe.loc[
        (
            (dataframe[f'supertrend_1_sell_{m1}_{p1}'] == 'down') &
            (dataframe[f'supertrend_2_sell_{m2}_{p2}'] == 'down') &
            (dataframe[f'supertrend_3_sell_{m3}_{p3}'] == 'down') &
            (dataframe['volume'] > 0)
        ),
        'sell'] = 1
```

**Three Sell Indicator Groups Comparison**:

| Indicator Group | Multiplier (m) | Period (p) | Sensitivity |
|-----------------|----------------|------------|-------------|
| **Supertrend_1_sell** | 1 | 16 | Fast (small multiplier) |
| **Supertrend_2_sell** | 3 | 18 | Medium |
| **Supertrend_3_sell** | 6 | 18 | Slow (large multiplier) |

### 4.2 Trailing Stop Protection

```python
trailing_stop = True
trailing_stop_positive = 0.05          # Activate after 5% profit
trailing_stop_positive_offset = 0.144  # Offset value 14.4%
trailing_only_offset_is_reached = False # Don't require reaching offset
```

**Trailing Stop Logic**:
- Activates after profit reaches 5%
- Stop loss line follows price increases
- Triggers sell when price drops, protecting profits

---

## 5. Technical Indicator System

### 5.1 Supertrend Indicator Implementation

```python
def supertrend(self, dataframe, multiplier, period):
    # Calculate basic upper/lower bands
    df['TR'] = ta.TRANGE(df)              # True Range
    df['ATR'] = ta.SMA(df['TR'], period)  # ATR average
    
    # Calculate basic upper/lower bands
    df['basic_ub'] = (high + low) / 2 + multiplier * ATR
    df['basic_lb'] = (high + low) / 2 - multiplier * ATR
    
    # Calculate final upper/lower bands (considering previous period state)
    df['final_ub'] = ...
    df['final_lb'] = ...
    
    # Set Supertrend value
    df[st] = ...
    
    # Mark trend direction
    df[stx] = 'up' if close > st else 'down'
```

### 5.2 Core Calculation Logic

Supertrend's final band calculation considers the previous period's state:

```python
# Final upper band
if basic_ub < final_ub[i-1] or close[i-1] > final_ub[i-1]:
    final_ub = basic_ub
else:
    final_ub = final_ub[i-1]  # Keep unchanged

# Final lower band
if basic_lb > final_lb[i-1] or close[i-1] < final_lb[i-1]:
    final_lb = basic_lb
else:
    final_lb = final_lb[i-1]  # Keep unchanged
```

---

## 6. Risk Management Features

### 6.1 Triple Confirmation Filter

| Risk Type | Protection Measure |
|-----------|-------------------|
| **False Breakout** | Three indicators must confirm simultaneously, filtering single-indicator misjudgments |
| **Trend Reversal** | Three sell indicators confirm reversal signal |
| **Profit Giveback** | Trailing stop locks in profits |

### 6.2 Stepped ROI

```
Time Interval       Profit Requirement
───────────────────────────────────────
0 minutes           8.7%
6 hours             5.8%
14 hours            2.9%
37 hours            0%
```

**Design Logic**:
- High profit requirement for short-term, locking in quick profit opportunities
- Lower requirements for long-term, avoiding forced holding for too long

### 6.3 Trailing Stop Parameter Analysis

| Parameter | Value | Description |
|-----------|-------|-------------|
| trailing_stop_positive | 0.05 | Activate trailing after 5% profit |
| trailing_stop_positive_offset | 0.144 | Offset when price rises 14.4% from entry |
| trailing_only_offset_is_reached | False | Don't require reaching offset to start trailing |

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Triple Confirmation Reliability**: Three indicators confirm simultaneously, reducing false signals
2. **Buy/Sell Separation Design**: Buy and sell use different parameter groups, flexible adjustment
3. **Hyperparameter Optimizable**: 12 hyperparameter ranges, easy for Hyperopt optimization
4. **Trailing Stop Protection**: Automatically trails after profit, locking in gains
5. **Calculation Pre-caching**: All combinations pre-calculated, efficient runtime

### ⚠️ Limitations

1. **Strict Entry Conditions**: Triple confirmation may miss early opportunities
2. **Non-official Indicator Implementation**: Supertrend implementation not verified against original paper
3. **Moderate Stop Loss**: 26.5% stop loss may incur significant losses in sharp drops
4. **ATR Stability Dependency**: ATR calculation requires sufficient historical data (startup_candle_count=18)

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Trending Market** | Default configuration | Triple confirmation filters false breakouts |
| **Oscillating Market** | Lower multipliers | Increase sensitivity |
| **Sharp Drop** | Tighten stop loss | Prevent large losses |
| **Low Volatility Market** | Raise multipliers | Expand volatility range threshold |

---

## 9. Applicable Market Environment Details

SuperTrend is a **multi-layer trend following strategy**. Based on its triple Supertrend indicator design, it is most suitable for **stable trend markets**, while signals may be sparse in oscillating markets.

### 9.1 Strategy Core Logic

- **Triple Confirmation Mechanism**: Three Supertrend indicators with different parameters confirm simultaneously
- **Buy/Sell Separation**: Buy and sell groups use different parameters, adapting to different exit strategies
- **Dynamic Support/Resistance**: Dynamic bands based on ATR follow price fluctuations

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:------------------|:----------------|
| 📈 **Stable Trend** | ⭐⭐⭐⭐⭐ | Triple confirmation reliably captures trend |
| 🔄 **Oscillating Market** | ⭐⭐⭐☆☆ | Few signals but high reliability |
| 📉 **Sharp Drop** | ⭐⭐☆☆☆ | 26.5% stop loss may incur large losses |
| ⚡ **Low Volatility** | ⭐☆☆☆☆ | ATR too small, indicator insensitive |
| ⚡ **High Volatility** | ⭐⭐⭐⭐☆ | Large ATR, bands follow more flexibly |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| stoploss | -0.15~-0.20 | Tighten stop loss to prevent large losses |
| trailing_stop_positive | 0.03 | Increase trailing sensitivity |
| buy multipliers | 2-4 | Medium sensitivity |
| sell multipliers | 1-3 | Fast exit response |

---

## 10. Important Note: The Cost of Complexity

### 10.1 Learning Cost

SuperTrend involves understanding the Supertrend indicator:
- ATR (Average True Range) calculation and meaning
- Supertrend upper/lower band calculation logic
- Final band state continuation mechanism
- Triple confirmation design philosophy

**Recommended reading time**: 1-2 hours for deep understanding

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-30 pairs | 4GB | 8GB |
| 30+ pairs | 8GB | 16GB |

**Computational Burden**:
- Pre-calculate all hyperparameter combinations (~7×21×3×2 = 882 combinations)
- Each combination requires iterating historical data to calculate bands

### 10.3 Differences Between Backtesting and Live Trading

- **Backtesting Environment**: Uses pre-calculation cache, fast execution
- **Live Trading Environment**: Requires real-time Supertrend indicator calculation
- **Recommendation**: Ensure startup_candle_count is set correctly (18)

### 10.4 Suggestions for Manual Traders

Manual traders can learn from:
- **Triple confirmation concept**: Multiple indicators must confirm simultaneously before entry
- **Buy/sell separation design**: Use different parameters for entry and exit
- **Trailing stop usage**: Enable trailing protection after profit

---

## 11. Summary

**SuperTrend** is a **clearly designed multi-layer trend following strategy**. Its core value lies in:

1. **Triple Confirmation Reliability**: Three indicators confirm simultaneously reducing false signals
2. **Buy/Sell Separation Flexibility**: Entry and exit parameters independently optimized
3. **Adjustable Hyperparameters**: 12 parameter ranges easy to optimize
4. **Trailing Stop Protection**: Locks in profits after gaining

For quantitative traders, this is an **intermediate strategy suitable for stable trend markets**, with clear logic and adjustable parameters. It is recommended to find parameter combinations suitable for your trading pairs through Hyperopt optimization.

---

**Final Reminder**: No matter how good the strategy is, the market will humble you without warning. Test with small positions, survival comes first! 🙏