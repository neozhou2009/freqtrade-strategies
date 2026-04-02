# BB_RPB_TSL Strategy Deep Dive

> **Strategy ID**: #438 (438th of 465 strategies)  
> **Strategy Type**: Multi-Condition Bollinger Band Strategy + Real Pull Back + Custom Trailing Stop Loss  
> **Time Frame**: 5 minutes (5m) + 1 hour informative layer (1h)

---

## I. Strategy Overview

BB_RPB_TSL is a highly complex multi-condition strategy, integrating Bollinger Band theory, Real Pull Back concept, and custom trailing stop loss mechanism. Developed by jilv220, it draws inspiration from multiple community strategies' best practices, including Bollinger Band strategies, TheRealPullbackV2, and BigZ04_TSL's trailing stop loss mechanism. The strategy has over 600 lines of code, containing 19 independent buy conditions, dozens of custom sell signals, and rich Hyperopt parameter space.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 19 independent buy signals (including multiple combination conditions) |
| **Sell Conditions** | Custom sell function (dozens of exit scenarios) |
| **Protection Mechanism** | Tiered dynamic stop loss + multi-layer profit tracking |
| **Time Frame** | 5-minute main frame + 1 hour informative frame |
| **Dependencies** | talib, qtpylib, pandas_ta, technical |
| **Hyperopt Parameters** | Over 60 optimizable parameters |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.205,    # 0 minutes: 20.5%
    "81": 0.038,   # After 81 minutes: 3.8%
    "292": 0.005,  # After 292 minutes: 0.5%
}

# Stop loss setting (overridden by custom stop loss)
stoploss = -0.10  # 10% hard stop loss

# Custom stop loss enabled
use_custom_stoploss = True

# Time frame
timeframe = '5m'
inf_1h = '1h'
```

**Design Rationale**:
- Three-tier ROI setting: Initial target 20.5%, drops to 3.8% after 81 minutes holding, further to 0.5% after 292 minutes
- Encourages quick profit taking, lowers target for longer holds
- Custom stop loss overrides hard stop loss for more refined profit protection

### 2.2 Hyperopt Parameter Structure

The strategy contains numerous Hyperopt parameters, divided into multiple optimization spaces:

| Parameter Space | Main Parameters | Optimization Status |
|-----------------|-----------------|---------------------|
| **Buy Parameters** | bb_width, cci, rmi, rsi, ewo, etc. | Most disabled |
| **Sell Parameters** | cmf, ema, deadfish parameters | Most disabled |
| **Slippage Control** | max_slip | Optimizable |
| **BTC Safety** | buy_btc_safe | Optimizable |

In current configuration, most parameters have `optimize=False`, only a few parameters have optimization enabled.

---

## III. Buy Conditions Detailed Explanation

### 3.1 Classification of 19 Buy Conditions

The strategy's buy conditions are extremely rich, categorized as follows:

#### Category 1: Bollinger Band Basic Conditions

**Condition #1: is_BB_checked (Combination Condition)**
```python
is_BB_checked = is_dip & is_break

is_dip = (
    (rmi_length < buy_rmi.value) &
    (cci_length <= buy_cci.value) &
    (srsi_fk < buy_srsi_fk.value)
)

is_break = (
    (bb_delta > buy_bb_delta.value) &
    (bb_width > buy_bb_width.value) &
    (closedelta > close * buy_closedelta.value / 1000) &
    (close < bb_lowerband3 * buy_bb_factor.value)
)
```
**Logic**: RMI oversold + CCI low position + Stochastic RSI low position + BB breakout confirmation

---

#### Category 2: Trend Following Conditions

**Condition #2: is_local_uptrend**
```python
is_local_uptrend = (
    (ema_26 > ema_12) &
    (ema_26 - ema_12 > open * buy_ema_diff.value) &
    (ema_26.shift() - ema_12.shift() > open / 100) &
    (close < bb_lowerband2 * buy_bb_factor.value) &
    (closedelta > close * buy_closedelta.value / 1000)
)
```
**Logic**: EMA trend confirmation + BB lower band deviation + price change confirmation

**Condition #3: is_local_dip**
```python
is_local_dip = (
    (ema_26 > ema_12) &
    (ema_26 - ema_12 > open * buy_ema_diff_local_dip.value) &
    (ema_26.shift() - ema_12.shift() > open / 100) &
    (close < ema_20 * buy_ema_high_local_dip.value) &
    (rsi < buy_rsi_local_dip.value) &
    (crsi > buy_crsi_local_dip.value) &
    (closedelta > close * buy_closedelta_local_dip.value / 1000)
)
```
**Logic**: Trend confirmation + RSI oversold + CRSI protection

---

#### Category 3: EWO (Elliot Wave Oscillator) Conditions

**Condition #4: is_ewo**
```python
is_ewo = (
    (rsi_fast < buy_rsi_fast.value) &
    (close < ema_8 * buy_ema_low.value) &
    (EWO > buy_ewo.value) &
    (close < ema_16 * buy_ema_high.value) &
    (rsi < buy_rsi.value)
)
```
**Logic**: Fast RSI low position + EWO positive value + price deviation from EMA

**Condition #5: is_ewo_2**
```python
is_ewo_2 = (
    (ema_200_1h > ema_200_1h.shift(12)) &
    (ema_200_1h.shift(12) > ema_200_1h.shift(24)) &
    (rsi_fast < buy_rsi_fast_ewo_2.value) &
    (close < ema_8 * buy_ema_low_2.value) &
    (EWO > buy_ewo_high_2.value) &
    (close < ema_16 * buy_ema_high_2.value) &
    (rsi < buy_rsi_ewo_2.value)
)
```
**Logic**: 1-hour EMA200 uptrend + EWO high position + RSI oversold

---

#### Category 4: Reverse Deadfish Conditions

**Condition #6: is_r_deadfish**
```python
is_r_deadfish = (
    (ema_100 < ema_200 * buy_r_deadfish_ema.value) &
    (bb_width > buy_r_deadfish_bb_width.value) &
    (close < bb_middleband2 * buy_r_deadfish_bb_factor.value) &
    (volume_mean_12 > volume_mean_24 * buy_r_deadfish_volume_factor.value) &
    (cti < buy_r_deadfish_cti.value) &
    (r_14 < buy_r_deadfish_r14.value)
)
```
**Logic**: EMA trend deviation + BB width + CTI/R oversold + volume anomaly

---

#### Category 5: ClucHA Conditions

**Condition #7: is_clucHA**
```python
is_clucHA = (
    (rocr_1h > buy_clucha_rocr_1h.value) &
    (bb_lowerband2_40.shift() > 0) &
    (bb_delta_cluc > ha_close * buy_clucha_bbdelta_close.value) &
    (ha_closedelta > ha_close * buy_clucha_closedelta_close.value) &
    (tail < bb_delta_cluc * buy_clucha_bbdelta_tail.value) &
    (ha_close < bb_lowerband2_40.shift()) &
    (ha_close < ha_close.shift())
)
```
**Logic**: ROCR confirmation + Heikin Ashi BB deviation + tail confirmation

---

#### Category 6: Cofi Conditions

**Condition #8: is_cofi**
```python
is_cofi = (
    (open < ema_8 * buy_ema_cofi.value) &
    (qtpylib.crossed_above(fastk, fastd)) &
    (fastk < buy_fastk.value) &
    (fastd < buy_fastd.value) &
    (adx > buy_adx.value) &
    (EWO > buy_ewo_high.value) &
    (cti < buy_cofi_cti.value) &
    (r_14 < buy_cofi_r14.value)
)
```
**Logic**: Price deviation from EMA + Stochastic crossover + ADX trend + EWO + CTI/R protection

---

#### Category 7: Gumbo Conditions

**Condition #9: is_gumbo**
```python
is_gumbo = (
    (EWO < buy_gumbo_ewo_low.value) &
    (bb_middleband2_1h >= T3_1h) &
    (T3 <= ema_8 * buy_gumbo_ema.value) &
    (cti < buy_gumbo_cti.value) &
    (r_14 < buy_gumbo_r14.value)
)
```
**Logic**: EWO low position + T3 deviation + CTI/R protection

---

#### Category 8: Squeeze Momentum Conditions

**Condition #10: is_sqzmom**
```python
is_sqzmom = (
    (is_sqzOff) &
    (linreg_val_20.shift(2) > linreg_val_20.shift(1)) &
    (linreg_val_20.shift(1) < linreg_val_20) &
    (linreg_val_20 < 0) &
    (close < ema_13 * buy_sqzmom_ema.value) &
    (EWO < buy_sqzmom_ewo.value) &
    (r_14 < buy_sqzmom_r14.value)
)
```
**Logic**: BB squeeze release + linear regression reversal + EWO + CTI/R protection

---

#### Category 9: NFI Series (9 Conditions)

The strategy includes multiple conditions from the NFI (Next Generation) series:

| Condition ID | Condition Name | Core Feature |
|--------------|----------------|--------------|
| #11 | is_nfi_13 | 1-hour EMA trend + CTI deep oversold |
| #12 | is_nfi_32 | RSI slow decline + CTI oversold |
| #13 | is_nfi_33 | EWO high position + CTI/R deep oversold |
| #14 | is_nfi_38 | PMAX confirmation + CTI/R oversold |
| #15 | is_nfix_5 | 1-hour EMA200 trend + EWO high position |
| #16 | is_nfix_39 | ClucHA modified version + EMA trend confirmation |
| #17 | is_nfix_49 | Delayed condition + CTI/R protection |
| #18 | is_nfi7_33 | moderi trend + CTI oversold |
| #19 | is_nfi7_37 | PMAX + EWO + safe dump protection |

---

### 3.2 Common Check Conditions

All buy conditions must pass the following common checks:

```python
is_additional_check = (
    (roc_1h < buy_roc_1h.value) &
    (bb_width_1h < buy_bb_width_1h.value)
)
```

**Logic**: 1-hour ROC cannot be too high (avoid chasing highs), 1-hour BB width cannot be too large (avoid extreme volatility).

---

## IV. Sell Logic Detailed Explanation

### 4.1 Custom Sell Function (custom_sell)

The core sell logic is implemented in the `custom_sell` function, containing dozens of exit scenarios:

#### Profit Tracking Exit (profit_t series)

```python
# Profit range 0-1.2%
if 0.012 > current_profit >= 0.0:
    if (max_profit > current_profit + 0.045) and (rsi < 46.0):
        return "sell_profit_t_0_1"
    elif (max_profit > current_profit + 0.025) and (rsi < 32.0):
        return "sell_profit_t_0_2"
    ...

# Profit range 1.2-2%
elif 0.02 > current_profit >= 0.012:
    if (max_profit > current_profit + 0.01) and (rsi < 39.0):
        return "sell_profit_t_1_1"
    ...
```

**Logic**: When profit retraces, determine exit timing based on max profit vs current profit gap + RSI.

---

#### MOMDIV Exit Signal

```python
if current_profit > 0.02:
    if (momdiv_sell_1h == True):
        return "signal_profit_q_momdiv_1h"
    if (momdiv_sell == True):
        return "signal_profit_q_momdiv"
    if (momdiv_coh == True):
        return "signal_profit_q_momdiv_coh"
```

**Logic**: Exit when momentum divergence signal triggers.

---

#### Quick Exit Signals

```python
if (0.06 > current_profit > 0.02) and (rsi > 80.0):
    return "signal_profit_q_1"

if (0.06 > current_profit > 0.02) and (cti > 0.95):
    return "signal_profit_q_2"
```

**Logic**: Quick exit when RSI overbought or CTI high position.

---

#### PMAX Exit Signals

```python
if (0.06 > current_profit > 0.02) and (pm <= pmax_thresh) and (close > sma_21 * 1.1):
    return "signal_profit_q_pmax_bull"
if (0.06 > current_profit > 0.02) and (pm > pmax_thresh) and (close > sma_21 * 1.016):
    return "signal_profit_q_pmax_bear"
```

**Logic**: Profit Maximizer indicator triggers exit.

---

#### Deadfish Stop Loss Signal

```python
if (current_profit < sell_deadfish_profit.value) &
   (close < ema_200) &
   (bb_width < sell_deadfish_bb_width.value) &
   (close > bb_middleband2 * sell_deadfish_bb_factor.value) &
   (volume_mean_12 < volume_mean_24 * sell_deadfish_volume_factor.value):
    return "sell_stoploss_deadfish"
```

**Logic**: Profit loss + price below EMA200 + narrow BB width + low volume = deadfish stop loss.

---

### 4.2 Dynamic Stop Loss System

```python
def custom_stoploss(...):
    sl_new = 1
    
    if (current_profit > 0.2):
        sl_new = 0.05
    elif (current_profit > 0.1):
        sl_new = 0.03
    elif (current_profit > 0.06):
        sl_new = 0.02
    elif (current_profit > 0.03):
        sl_new = 0.015
    
    return sl_new
```

**Stop Loss Tier Table**:

| Profit Range | Stop Loss Lock | Protection Effect |
|---------------|----------------|-------------------|
| >20% | 5% | Retains at least 15% profit |
| >10% | 3% | Retains at least 7% profit |
| >6% | 2% | Retains at least 4% profit |
| >3% | 1.5% | Retains at least 1.5% profit |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Trend** | EMA(4,8,12,13,16,20,26,50,100,200) | Multi-layer trend judgment |
| **Momentum** | RSI, RSI_fast, RSI_slow, CRSI | Overbought/oversold determination |
| **Volatility** | BB(20,2), BB(20,3), BB(40,2) | Price deviation determination |
| **Oscillator** | CCI, RMI, StochRSI | Deep oversold determination |
| **Special** | CTI, EWO, Williams %R | Multi-dimensional oversold confirmation |
| **Volume** | CMF, Volume Mean | Volume confirmation |
| **Trend** | PMAX, MOMDIV, T3 | Profit maximization/momentum divergence |
| **Volatility** | KC (Keltner Channel), Linreg | Squeeze determination |
| **Price Pattern** | Heikin Ashi | Smoothed price pattern |

### 5.2 Informative Time Frame Indicators (1 Hour)

The strategy uses 1 hour as informative layer, providing higher-dimensional trend judgment:

- **EMA(8,50,100,200)**: 1-hour trend judgment
- **CTI, CTI_40**: 1-hour momentum confirmation
- **Williams %R(96,480)**: Long-term overbought/oversold
- **BB Width**: 1-hour volatility judgment
- **RSI, CMF**: 1-hour momentum/money flow
- **ROCR**: 1-hour rate of change
- **Safe dump protection**: Crash protection mechanism

---

## VI. Risk Management Features

### 6.1 Multiple Buy Protections

Each buy condition has independent protection parameters:

| Protection Type | Parameter Example | Description |
|-----------------|-------------------|-------------|
| **CTI Protection** | cti < -0.5 | Deep oversold confirmation |
| **R Indicator Protection** | r_14 < -60 | Williams %R confirmation |
| **Volume Protection** | volume_mean_12 > volume_mean_24 * factor | Volume anomaly confirmation |
| **1-Hour Trend Protection** | ema_200_1h > ema_200_1h.shift(12) | Major trend protection |

### 6.2 Slippage Control

```python
def confirm_trade_entry(...):
    slippage = ((rate / close) - 1) * 100
    if slippage < max_slip:
        return True
    else:
        return False
```

**Logic**: Check slippage at entry, reject entry if exceeds threshold.

### 6.3 Tiered Stop Loss Protection

Dynamic stop loss system ensures profit locking, prevents large drawdowns.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Rich Conditions**: 19 buy conditions cover multiple market scenarios
2. **Multiple Protections**: CTI/R indicator protection, volume protection, 1-hour trend protection
3. **Dynamic Exit**: Dozens of exit scenarios, refined profit tracking
4. **Informative Layer Support**: 1-hour frame provides major trend judgment
5. **Hyperopt Friendly**: Large number of optimizable parameters, suitable for parameter tuning

### ⚠️ Limitations

1. **Extremely High Complexity**: 600+ lines of code, difficult to debug
2. **Too Many Parameters**: 60+ parameters, easy to overfit
3. **High Computational Load**: Large number of indicator calculations, high CPU consumption
4. **Difficult Maintenance**: Many conditions, complex logic, hard to track issues
5. **Backtesting Fitting Risk**: Parameter optimization may lead to "curve fitting"

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Oscillating Market** | Enable all conditions | Multiple conditions cover various bounce scenarios |
| **Trending Market** | Only enable trend-type conditions | nfix_5, ewo_2 and other trend following conditions |
| **Crash Market** | Enable safe_dump protection | Avoid catching falling knives |
| **Low Volatility Market** | Enable squeeze-type conditions | sqzmom captures volatility release |

---

## IX. Applicable Market Environment Detailed Analysis

BB_RPB_TSL is a **multi-condition fusion strategy**. Based on its code architecture and community live trading experience, it performs best in **multi-scenario switching markets**, while requiring configuration adjustments in **single extreme markets**.

### 9.1 Core Strategy Logic

- **Condition Matrix**: 19 conditions cover oscillation, trend, squeeze, pullback and other scenarios
- **Informative Layer Support**: 1-hour frame provides major trend judgment
- **Profit Tracking**: Dozens of exit scenarios for refined profit management
- **Protection Mechanisms**: CTI/R indicator protection, volume protection, slippage protection

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 Slow Bull Uptrend | ⭐⭐⭐⭐☆ | Trend-type conditions capture pullback opportunities, profit tracking effective |
| 🔄 Oscillating Volatile | ⭐⭐⭐⭐⭐ | Multiple conditions cover various bounce scenarios, performs best |
| 📉 One-sided Downtrend | ⭐⭐☆☆☆ | Need to enable safe_dump protection, otherwise high risk |
| ⚡️ Rapid Surge | ⭐⭐⭐☆☆ | Squeeze-type conditions can capture volatility release |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| minimal_roi | {"0": 0.10} | Lower target, faster turnover |
| max_slip | 0.5 | Control slippage, avoid chasing highs |
| buy_btc_safe | Enable | BTC crash protection |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

BB_RPB_TSL has extremely high learning cost:
- 600+ lines of code, need to understand line by line
- 19 buy conditions, interwoven logic
- Dozens of sell scenarios, difficult to track
- Suitable for advanced developers for in-depth research

### 10.2 Hardware Requirements

| Pair Count | Minimum Memory | Recommended Memory |
|-----------|----------------|-------------------|
| 1-10 pairs | 4GB | 8GB |
| 10-50 pairs | 8GB | 16GB |
| 50+ pairs | 16GB | 32GB |

**Warning**: Large number of indicator calculations, high CPU consumption, low-spec VPS may timeout.

### 10.3 Backtesting vs Live Trading Differences

Complex strategy backtesting and live trading differences may be large:
- Many parameters, easy to "fit" historical optimal solution
- Indicator calculations may have delays in live trading
- Slippage and liquidity impact greater

### 10.4 Manual Trader Recommendations

Manual traders not recommended to use directly:
- Conditions too complex, difficult to track manually
- Profit tracking requires real-time monitoring of multiple indicators
- Recommended to simplify to a few core conditions for manual operation

---

## XI. Summary

**BB_RPB_TSL** is a highly complex multi-condition fusion strategy. Its core value lies in:

1. **Rich Conditions**: 19 buy conditions cover multiple market scenarios
2. **Refined Protection**: CTI/R indicator protection, volume protection, slippage protection
3. **Profit Tracking**: Dozens of exit scenarios for refined profit management
4. **Informative Layer Support**: 1-hour frame provides major trend judgment

For advanced quantitative developers, BB_RPB_TSL is a valuable case study for multi-condition strategies. But note:
- Parameter optimization may lead to overfitting
- High computational load, high hardware requirements
- Difficult maintenance, high debugging cost

Recommended to test in oscillating markets first, verify effectiveness of core conditions, then gradually expand configuration.

---

*Strategy ID: #438*
*Document Version: v1.0*