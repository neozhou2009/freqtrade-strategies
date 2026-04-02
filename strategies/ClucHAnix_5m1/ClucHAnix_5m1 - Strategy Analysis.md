# ClucHAnix_5m1 Strategy Analysis

> **Strategy ID**: #96 (465 strategies, 96th)  
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Mean Reversion + Dynamic Stop-Loss  
> **Timeframe**: 5 Minutes (5m) + 1-Hour Informational Layer

---

## I. Strategy Overview

ClucHAnix_5m1 is a quantitative trading strategy based on Heikin Ashi (HA) candlestick charts and Bollinger Band mean reversion principles. This strategy is a parameter-optimized variant of ClucHAnix_5m, achieving a more aggressive trading style by adjusting entry condition parameters and simplifying the ROI table design. The "_5m1" designation indicates it is the first optimized version of the 5-minute timeframe.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 2 independent entry signal paths, both require 1-hour ROCR filtering |
| **Exit Conditions** | 1 base exit signal + multi-layer dynamic profit-taking logic |
| **Protection Mechanisms** | Custom dynamic trailing stop |
| **Timeframe** | Primary 5m + Informational 1h |
| **Dependencies** | technical, talib, numpy, pandas, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,      # Immediate exit at 10% profit
    "30": 0.05,     # Profit drops to 5% after 30 minutes
    "60": 0.02,     # Profit drops to 2% after 60 minutes
}

# Stop Loss
stoploss = -0.99  # Uses custom stop-loss, fully relies on custom_stoploss

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.001
trailing_stop_positive_offset = 0.012
trailing_only_offset_is_reached = False
```

**Design Philosophy**:
- **ROI Table Design**: Uses a simpler three-tier design — initially expects 10% profit, drops to 5% after 30 minutes, and 2% after 60 minutes. Simpler than ClucHAnix_5m's multi-tier design, embodying a "fast in, fast out" philosophy.
- **Stop Loss Design**: Primary stop loss set to -99%, effectively disabling fixed stop-loss and fully relying on custom_stoploss.

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "market",
    "exit": "market",
    "emergency_exit": "market",
    "force_entry": "market",
    "force_exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": False,
    "stoploss_on_exchange_interval": 60,
    "stoploss_on_exchange_limit_ratio": 0.99,
}
```

---

## III. Entry Conditions Details

### 3.1 Entry Parameter Configuration

The strategy has 5 core entry parameters, optimized via hyperopt:

| Parameter | Default | Optimization Range | Description |
|-----------|---------|-------------------|-------------|
| rocr_1h | 0.79492 | 0.5-1.0 | 1-hour ROC threshold, filters counter-trend trades |
| bbdelta_close | 0.01889 | 0.0005-0.02 | Bollinger Band width to close price ratio |
| closedelta_close | 0.00916 | 0.0005-0.02 | Close price change to close price ratio |
| bbdelta_tail | 0.72235 | 0.7-1.0 | Lower wick to Bollinger Band width ratio |
| close_bblower | 0.0127 | 0.0005-0.02 | Close price to lower Bollinger Band ratio |

### 3.2 Entry Condition Details

#### Condition #1: Bollinger Band Mean Reversion + ROCR Filtering
```python
# Logic conditions
- rocr_1h > 0.79492 (1-hour ROC must be in strong uptrend)
- bbdelta > ha_close * 0.01889 (Bollinger Band width sufficient)
- closedelta > ha_close * 0.00916 (Close price change significant)
- tail < bbdelta * 0.72235 (Lower wick must be relatively short)
- ha_close < lower.shift() (HA close must break below lower band)
- ha_close <= ha_close.shift() (Must show downtrend)
```

**Design Intent**: Through Bollinger compression, HA lower band breakout, and ROC uptrend confirmation, capture mean reversion opportunities. Compared to ClucHAnix_5m, the ROCR threshold is higher (0.79 vs 0.54), meaning stricter trend filtering.

#### Condition #2: EMA Deviation + Lower Band Support
```python
# Logic conditions
- rocr_1h > 0.79492 (1-hour ROC filter)
- ha_close < ema_slow (HA close below 50-period EMA)
- ha_close < 0.0127 * bb_lowerband (Close hugs lower band)
```

**Design Intent**: Rebound opportunities when price deviates excessively from EMA, with lower band support confirmation.

### 3.3 Entry Condition Classification

| Condition Group | Condition # | Core Logic | vs ClucHAnix_5m Comparison |
|----------------|-------------|------------|---------------------------|
| Bollinger Band Mean Reversion | #1 | Bollinger compression + HA lower band + ROC confirmation | Higher ROCR (0.79 vs 0.54) |
| EMA Deviation Repair | #2 | Rebound when price deviates from EMA | Parameters slightly adjusted |

---

## IV. Exit Logic Details

### 4.1 Multi-Layer Take-Profit System

```
Profit Range        Threshold     Description
────────────────────────────────────────────────
0% - 2%             0.02         Base take-profit
2% - 5%             0.05         Medium-term take-profit
5% - 10%            0.10         Initial take-profit
> 10%               -            Trailing stop takes over
```

**Design Logic**: 5-minute-level trading requires quick reactions, using an aggressive take-profit gradient. Compared to ClucHAnix_5m's six-tier design, the three-tier design is simpler and reduces overfitting risk.

### 4.2 Exit Parameter Configuration

| Parameter | Default | Optimization Range | Description |
|-----------|---------|-------------------|-------------|
| sell_fisher | 0.39075 | 0.1-0.5 | Fisher indicator reversal threshold |
| sell_bbmiddle_close | 0.99754 | 0.97-1.1 | Close price to Bollinger middle band ratio |

### 4.3 Base Exit Signal

```python
# Exit signal: Fisher indicator reversal + Bollinger Band confirmation
- fisher > 0.39075 (Fisher indicator exceeds threshold)
- ha_high declining for 3 consecutive candles (Must show downtrend)
- ha_close declining
- ema_fast > ha_close (Short-term MA above price)
- ha_close * 0.99754 > bb_middleband (Close near Bollinger middle band)
- volume > 0 (Ensure volume presence)
```

### 4.4 Custom Trailing Stop

| Profit Range | Stop-Loss Profit | Calculation |
|-------------|-----------------|-------------|
| > 6.4% | Dynamic | SL_2 + (profit - 6.4%) |
| 1.1% - 6.4% | Linear interpolation | Dynamic by profit range |
| < 1.1% | -10% | Hard stop |

```python
# Parameter configuration
pHSL = -0.10   # Hard stop profit
pPF_1 = 0.011  # First take-profit point
pPF_2 = 0.064  # Second take-profit point
pSL_1 = 0.011  # First stop-loss profit
pSL_2 = 0.062  # Second stop-loss profit
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|--------------------|---------|
| Trend Indicators | EMA (3, 50), HA Candlestick | Price trend direction and price smoothing |
| Bollinger Bands | BB (40, 2) | Price volatility ranges and mean reversion |
| Momentum Indicators | ROCR (28), RSI, Fisher | Market momentum and overbought/oversold |
| Volume Indicators | Volume Mean (30) | Volume confirmation of price signals |

### 5.2 Informational Timeframe Indicators (1h)

- **ROC**: 168-period (1-week) rate of change, filters counter-trend trades
- **Heikin Ashi**: Uses 1-hour HA candles for ROCR calculation, eliminates noise

### 5.3 Custom Indicators

| Indicator | Formula | Purpose |
|-----------|---------|---------|
| bbdelta | mid - lower | Bollinger Band width |
| closedelta | abs(ha_close - ha_close.shift()) | Price change magnitude |
| tail | abs(ha_close - ha_low) | Lower wick length |
| fisher | (exp(2*rsi) - 1) / (exp(2*rsi) + 1) | Fisher-transformed RSI |

---

## VI. Risk Management Highlights

### 6.1 Dynamic Trailing Stop

```python
# Stop-loss logic
if current_profit > PF_2 (6.4%):
    sl_profit = SL_2 + (current_profit - PF_2)
elif current_profit > PF_1 (1.1%):
    sl_profit = SL_1 + ((current_profit - PF_1) * (SL_2 - SL_1) / (PF_2 - PF_1))
else:
    sl_profit = HSL (-10%)
```

**Design Philosophy**:
- **Low profit range (<1.1%)**: Uses -10% hard stop, protects principal
- **Medium profit range (1.1%-6.4%)**: Linearly interpolated stop based on profit level
- **High profit range (>6.4%)**: Stop follows profit upward, locking in most gains

### 6.2 Trend Filtering Protection

Through the 1-hour ROCR indicator filter, avoids entering at counter-trend points:
- **rocr_1h > 0.79**: Confirms 1-hour uptrend
- Filters out counter-trend trades, only enters in trend direction

### 6.3 Volume Verification

- **volume > 0**: Ensures trading in volume-backed environments, avoids false signals

---

## VII. Strategy Pros & Cons

### Pros

1. **Strict trend filtering**: ROCR threshold raised to 0.79, effectively filters counter-trend trades
2. **Simplified ROI design**: Three-tier design reduces overfitting risk, easier to understand and maintain
3. **Dynamic profit-taking design**: Dynamically adjusts stop-loss based on profit level
4. **Mean reversion approach**: Bollinger Band strategy performs well in ranging markets
5. **5-minute high-frequency advantage**: Shorter cycles mean faster capital turnover

### Cons

1. **High ROCR threshold**: 0.79 ROCR is high, may miss some trading opportunities
2. **Computation intensive**: Requires multi-period indicator calculations
3. **Depends on 1-hour informational layer**: All entries require 1-hour ROC confirmation
4. **Transaction cost sensitive**: 5-minute level requires low-fee environment
5. **Unsuitable for low-volatility markets**: May underperform during consolidation

---

## VIII. Applicable Scenarios

| Market Environment | Recommendation | Description |
|--------------------|----------------|-------------|
| Slow bull trend | Enable | Bollinger Band mean reversion performs well on trend pullbacks |
| Ranging markets | Applicable | Mean reversion strategy has advantages in ranging markets |
| Pump and dump | Enable | Has dynamic stop-loss protection |
| Flat consolidation | Use with caution | High ROCR threshold may filter out opportunities |
| High-frequency trading | Applicable | 5-minute level suits high turnover |

---

## IX. Comparison with ClucHAnix_5m

### 9.1 Parameter Differences

| Parameter | ClucHAnix_5m | ClucHAnix_5m1 | Change |
|-----------|-------------|---------------|--------|
| rocr_1h | 0.5411 | 0.79492 | Increased 47%, stricter filtering |
| bbdelta_close | 0.01846 | 0.01889 | Slightly increased |
| closedelta_close | 0.01009 | 0.00916 | Slightly decreased |
| bbdelta_tail | 0.98973 | 0.72235 | Decreased 27%, allows longer wicks |
| close_bblower | 0.00785 | 0.0127 | Increased 62%, closer to lower band |

### 9.2 ROI Table Differences

| Time Point | ClucHAnix_5m | ClucHAnix_5m1 |
|------------|-------------|---------------|
| 0 | 10.3% | 10% |
| 3 | 5% | - |
| 5 | 3.3% | - |
| 30 | - | 5% |
| 61 | 2.7% | - |
| 60 | - | 2% |
| 125 | 1.1% | - |
| 292 | 0.5% | - |

### 9.3 Core Differences Summary

1. **Stricter trend filtering**: ROCR threshold raised from 0.54 to 0.79
2. **Simpler ROI table**: Reduced from 6 tiers to 3 tiers
3. **More aggressive entry conditions**: Relaxed lower wick requirement (0.99 vs 0.72)

---

## X. Key Configuration Recommendations

### 10.1 Parameter Optimization Suggestions

| Configuration | Recommended Value | Description |
|---------------|-------------------|-------------|
| rocr_1h | 0.75-0.85 | Adjust based on market volatility |
| bbdelta_close | 0.015-0.025 | Bollinger Band width ratio |
| trailing_stop | True | Recommend enabling |

### 10.2 Transaction Cost Considerations

- 5-minute trading is high-frequency; pay special attention to fee rates
- Recommend low-fee exchanges or maker orders
- Include fees in all backtesting calculations

### 10.3 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 10-20 pairs | 2GB | 4GB |
| 20-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

---

## XI. Summary

ClucHAnix_5m1 is a meticulously designed 5-minute trend-following strategy that uses Heikin Ashi candlesticks to smooth price fluctuations and captures trading opportunities through Bollinger Band mean reversion principles. Compared to ClucHAnix_5m, this version raises the trend filtering threshold (ROCR 0.79 vs 0.54) and simplifies the ROI table design (three tiers vs six tiers), reflecting stricter stock selection logic and a simpler risk management style.

Its core value lies in:

1. **Strict trend filtering**: High ROCR threshold ensures trading only in strong uptrends
2. **Intelligent risk management**: Dynamic trailing stop protects profits
3. **Mean reversion strategy**: Bollinger Band principles capture price reversion opportunities
4. **High-frequency capability**: 5-minute level brings higher trading frequency

For quantitative traders, this strategy suits investors with technical backgrounds trading in trending markets. Pay attention to the ROCR threshold potentially missing opportunities, transaction cost control, and backtesting vs. live trading differences. Test with small capital for at least 1-2 months before gradually increasing positions.
