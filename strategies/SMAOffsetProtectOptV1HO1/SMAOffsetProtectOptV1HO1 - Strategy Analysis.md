# SMAOffsetProtectOptV1HO1 Strategy Deep Analysis

> **Strategy ID**: #362 (362nd of 465 strategies)  
> **Strategy Type**: EMA Offset + EWO Protection + RSI Filter + Tiered ROI  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

SMAOffsetProtectOptV1HO1 is the **Hyperopt Optimization version 1** of SMAOffsetProtectOptV1. While retaining the original EMA offset logic, it adopts a **tiered ROI exit mechanism** and adjusts key parameters. The "HO1" in the strategy name indicates the first variant after hyperparameter optimization.

Core differences compared to original V1:
- ROI changed from fixed 1% to **tiered decreasing** (11.4% → 6.3% → 3.7% → 0%)
- `ignore_roi_if_buy_signal` changed to **False**, no longer ignoring ROI
- All parameters have been re-optimized

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signals, identical to V1 |
| **Sell Conditions** | 1 base sell signal + **Tiered ROI** + trailing stop |
| **Protection Mechanism** | EWO trend protection + RSI overbought filter |
| **Timeframe** | Main timeframe 5m + informative timeframe 1h |
| **Dependencies** | talib, numpy, pandas, technical, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table (tiered decreasing)
minimal_roi = {
    "0": 0.114,   # Exit immediately when 11.4% profit is reached
    "36": 0.063,  # After 36 minutes, reduce to 6.3%
    "95": 0.037,  # After 95 minutes, reduce to 3.7%
    "157": 0      # After 157 minutes, force exit (0 profit)
}

# Stop loss setting
stoploss = -0.10  # 10% fixed stop loss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.001   # Positive trailing threshold 0.1%
trailing_stop_positive_offset = 0.01  # Offset 1%
trailing_only_offset_is_reached = True  # Only enable trailing after offset is reached
```

**Design Rationale**:
- **Tiered ROI Design**: The longer the holding time, the lower the ROI threshold, forcing the strategy to lower profit expectations when holding too long
- Requires 11.4% profit immediately after opening, which is a **quite aggressive** target
- Drops to 6.3% after 36 minutes, 3.7% after 95 minutes
- After 157 minutes (approximately 2.6 hours), exits even without profit

### 2.2 Order Type Configuration

```python
use_sell_signal = True
sell_profit_only = True
sell_profit_offset = 0.01
ignore_roi_if_buy_signal = False  # Key difference! V1 is True
```

**Key Settings**:
- `ignore_roi_if_buy_signal=False`: **This is the biggest difference from V1**
- V1 ignores ROI when buy signals exist, letting profits run
- HO1 strictly follows ROI rules, exits on time regardless of buy signals

---

## III. Buy Conditions Detailed Analysis

### 3.1 Protection Mechanisms (2 Groups)

Same protection mechanism as V1:

| Protection Type | Parameter Description | Default Value (HO1) |
|----------------|----------------------|---------------------|
| **EWO High Threshold** | Considers uptrend pullback when EWO > ewo_high | 2.139 |
| **EWO Low Threshold** | Considers deep oversold when EWO < ewo_low | -19.767 |
| **RSI Filter** | RSI < rsi_buy prevents chasing highs | 65 |

**Parameter Comparison (V1 vs HO1)**:

| Parameter | V1 Default | HO1 Default | Change |
|-----------|------------|--------------|--------|
| ewo_high | 5.638 | 2.139 | ↓ Decreased 62% |
| ewo_low | -19.993 | -19.767 | Slight change |
| rsi_buy | 61 | 65 | ↑ Relaxed 6.5% |

**Interpretation**:
- HO1's ewo_high is lower (2.139 vs 5.638), meaning **trend pullback buy is easier to trigger**
- HO1's rsi_buy is higher (65 vs 61), **relaxing the buy threshold**

### 3.2 Typical Buy Condition Examples

#### Condition #1: Trend Pullback Buy
```python
# Logic (same as V1)
- price < EMA(base_nb_candles_buy) * low_offset  # Price below offset moving average
- EWO > ewo_high  # Uptrend confirmed
- RSI < rsi_buy  # Not overbought
- volume > 0  # Has volume
```

**HO1 Parameters**:
- `base_nb_candles_buy = 17` (V1 is 16)
- `low_offset = 0.98` (V1 is 0.978)
- `ewo_high = 2.139` (V1 is 5.638)
- `rsi_buy = 65` (V1 is 61)

**Interpretation**: HO1's conditions are relatively looser, easier to trigger buys.

#### Condition #2: Deep Oversold Buy
```python
# Logic (same as V1)
- price < EMA(base_nb_candles_buy) * low_offset
- EWO < ewo_low
- volume > 0
```

**Interpretation**: Oversold bounce condition is essentially the same, ewo_low slightly changed (-19.767 vs -19.993).

### 3.3 Two Buy Conditions Classification

| Condition Group | Condition Number | Core Logic |
|----------------|------------------|------------|
| Trend Pullback | Condition #1 | EWO high threshold + RSI filter, lower threshold than V1 |
| Oversold Bounce | Condition #2 | EWO low threshold, basically same as V1 |

---

## IV. Sell Logic Detailed Analysis

### 4.1 Multi-Level Take-Profit System

The strategy employs a **four-tier decreasing ROI mechanism**:

```
Time (minutes)    Profit Threshold    Description
─────────────────────────────────────────────────
0                 11.4%              Requires high returns immediately after opening
36                6.3%               Lower expectations after 36 minutes holding
95                3.7%               Further lower after 95 minutes
157               0%                 Force exit after 157 minutes
```

**Core Design Philosophy**:
1. **Aggressive Opening**: Expects 11.4% high return immediately
2. **Time Penalty**: The longer the holding, the lower the profit expectation
3. **Forced Exit**: After 157 minutes, exits even without profit, preventing long-term holding

### 4.2 Special Sell Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| MA Deviation Sell | close > EMA(base_nb_candles_sell) * high_offset | Sell signal |
| Time Expired | Holding time reaches ROI stage | ROI forced exit |

**Parameter Comparison (V1 vs HO1)**:

| Parameter | V1 Default | HO1 Default |
|-----------|------------|-------------|
| base_nb_candles_sell | 49 | 17 |
| high_offset | 1.006 | 0.99 |

**Key Differences**:
- HO1's sell EMA period is shorter (17 vs 49)
- HO1's high_offset is 0.99, meaning **sell when price is just 1% below MA**
- This is one of the biggest differences from V1: V1 waits for price to rise 0.6% above MA to sell, HO1 sells when price is still 1% below MA

### 4.3 Base Sell Signal (1)

```python
# Sell signal 1: MA deviation sell
- close > EMA(17-period) * 0.99  # Price just 1% below MA
- volume > 0
```

**Interpretation**: HO1's sell condition is more sensitive, **easier to trigger sell**, contrasting with the aggressive ROI settings.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|--------------------|-------------------|---------|
| Trend Indicator | EMA (Exponential Moving Average) | Dynamic support/resistance |
| Oscillator | EWO (Elliott Wave Oscillator) | Trend strength and overbought/oversold judgment |
| Momentum Indicator | RSI (Relative Strength Index) | Overbought filter |
| Volume | volume | Validity confirmation |

### 5.2 Informative Timeframe Indicators (1h)

Same information layer settings as V1:
- Defines 1h timeframe for all trading pairs
- Supports cross-timeframe analysis

### 5.3 Optimizable Parameters

| Parameter Type | Parameter Name | Range | HO1 Default | V1 Default |
|----------------|---------------|-------|--------------|------------|
| IntParameter | base_nb_candles_buy | 5-80 | 17 | 16 |
| IntParameter | base_nb_candles_sell | 5-80 | 17 | 49 |
| DecimalParameter | low_offset | 0.9-0.99 | 0.98 | 0.978 |
| DecimalParameter | high_offset | 0.99-1.1 | 0.99 | 1.006 |
| DecimalParameter | ewo_high | 2.0-12.0 | 2.139 | 5.638 |
| DecimalParameter | ewo_low | -20.0--8.0 | -19.767 | -19.993 |
| IntParameter | rsi_buy | 30-70 | 65 | 61 |

---

## VI. Risk Management Features

### 6.1 Multi-Level ROI + Three-Layer Stop Loss

The strategy employs a **multi-level ROI exit + multi-layer stop loss** combination:

1. **Tiered ROI**: 11.4% → 6.3% → 3.7% → 0%, more stringent over time
2. **Fixed Stop Loss**: -10% hard stop loss
3. **Trailing Stop**: Enabled after 1% profit with 0.1% trailing
4. **Signal Stop Loss**: Exit when sell signal triggers

### 6.2 Key Difference: No Longer Ignoring ROI

`ignore_roi_if_buy_signal=False` is the core difference between HO1 and V1:

| Setting | V1 | HO1 |
|---------|----|----|
| ignore_roi_if_buy_signal | True | False |
| Behavior | Ignores ROI when buy signal exists | Strictly follows ROI rules |
| Risk Preference | Aggressive (let profits run) | Conservative (exit on time) |

### 6.3 More Sensitive Selling

HO1's sell condition settings:
- `base_nb_candles_sell = 17` (V1 is 49): Uses shorter EMA, faster reaction
- `high_offset = 0.99` (V1 is 1.006): Sells when price is 1% below MA, earlier than V1

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Tiered ROI Reduces Risk**: The longer the holding, the lower the exit threshold, avoiding long-term holding
2. **Parameter Optimized**: All parameters have been hyperparameter optimized, may be better suited for specific markets
3. **Easier Buying**: ewo_high lowered, rsi_buy increased, easier to trigger buys
4. **Forced Exit Mechanism**: After 157 minutes forced exit, prevents indefinite holding

### ⚠️ Limitations

1. **ROI Too Aggressive**: 11.4% initial target is high even in cryptocurrency markets
2. **Selling Too Sensitive**: high_offset=0.99 means selling before price even crosses above MA
3. **Hyperopt Overfit Risk**: Parameters may be overfit to specific historical data
4. **Potentially High Trade Frequency**: Easy buying + sensitive selling = frequent trading

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Strong Trend Market | Adjust high_offset | Sell condition too sensitive, may exit too early |
| Ranging Market | Reduce trade frequency | Current settings may cause frequent trading |
| High Volatility Period | Increase ROI threshold | 11.4% target may be hard to reach |
| Low Volatility Period | Decrease ROI threshold | Easier to reach exit target |

---

## IX. Applicable Market Environment Details

SMAOffsetProtectOptV1HO1 belongs to the **Hyperopt Optimized Strategy Variant**, a version tuned for specific market environments. Based on its code architecture and parameter settings, it is more suitable for **high volatility trending markets**, while performing poorly in **low volatility ranging** conditions.

### 9.1 Strategy Core Logic

- **Aggressive ROI**: Expects 11.4% return immediately after opening, suitable for large volatility markets
- **Relaxed Buying**: ewo_high=2.139 (low threshold) + rsi_buy=65 (wide filter)
- **Sensitive Selling**: high_offset=0.99 (sell when price is below MA)
- **Time Pressure**: 157 minutes forced exit, pursuing quick in-and-out

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| 📈 Strong Trend Market | ⭐⭐⭐⭐☆ | Can catch trends, but may exit too early |
| 🔄 Mild Fluctuation | ⭐⭐☆☆☆ | Easy buying + sensitive selling = frequent stop losses |
| 📉 One-sided Decline | ⭐☆☆☆☆ | ROI target hard to reach, frequent stop losses |
| ⚡ High Volatility Market | ⭐⭐⭐⭐⭐ | Aggressive ROI design fits large volatility |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| high_offset | 1.00-1.01 | Original value too sensitive, recommend increasing |
| minimal_roi | Adjust based on coin | 11.4% may be too high for some coins |
| base_nb_candles_sell | 25-35 | Slightly increase, avoid selling too fast |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

HO1 is the hyperopt version of V1, recommend first understanding V1's core logic:
- EMA offset strategy basic principles
- EWO indicator meaning
- Tiered ROI exit mechanism design philosophy

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|---------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

### 10.3 Difference Between Backtesting and Live Trading

**The Double-Edged Sword of Hyperopt**:
- ✅ Parameters optimized for historical data, backtest performance may be very good
- ❌ Easy to overfit, live trading performance may decline
- ⚠️ 11.4% ROI target is almost impossible to reach in bear markets

### 10.4 Manual Trader Recommendations

If you want to manually apply HO1's logic:
1. Use 17-period EMA (more sensitive)
2. Watch when price is 2% below EMA
3. Consider buying when EWO > 2.139 and RSI < 65
4. Set tiered take-profit: 11.4%/6.3%/3.7%
5. After 157 minutes, if still not profitable, consider exiting

---

## XI. Summary

**SMAOffsetProtectOptV1HO1** is V1's **aggressive optimized version**. Its core value lies in:

1. **Tiered ROI Exit**: Lower threshold over time, avoiding long-term holding
2. **Relaxed Buy Conditions**: Easier to catch entry opportunities
3. **Sensitive Sell Settings**: Quick profit locking, but may exit too early
4. **Hyperopt Optimization**: Tuned for specific market environments

**Core Differences from V1**:
| Dimension | V1 | HO1 |
|-----------|----|----|
| ROI | Fixed 1% | Tiered 11.4%→6.3%→3.7%→0% |
| ignore_roi_if_buy_signal | True (let profits run) | False (strict adherence) |
| Buy Threshold | Higher (ewo_high=5.638) | Lower (ewo_high=2.139) |
| Sell Sensitivity | Lower (MA+0.6%) | Higher (MA-1%) |
| Suitable Market | Mild Trend | High Volatility |

For quantitative traders, HO1 is suitable for **high volatility trending markets** with quick in-and-out strategy, but note that parameters may be overfit to historical data. Conduct sufficient forward testing before live trading.

---