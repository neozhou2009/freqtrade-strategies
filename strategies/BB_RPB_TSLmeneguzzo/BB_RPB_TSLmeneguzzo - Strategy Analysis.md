# BB_RPB_TSLmeneguzzo Strategy Analysis

> **Strategy Number**: #42
> **Strategy Type**: Multi-Condition Trend Following + Protection Mechanisms + Multiple Take-Profit Strategies
> **Timeframe**: 5 minutes (5m) + 1-hour information layer

---

## I. Strategy Overview

BB_RPB_TSLmeneguzzo is an enhanced version of the BB_RPB_TSL series, significantly expanded by user meneguzzo based on the original. This strategy inherits the original's Bollinger Band pullback concept and BTC protection mechanisms, while adding more entry conditions and more complex take-profit logic.

The core design philosophy is to capture buying opportunities in different market environments through multi-condition combinations, and maximize profits in market volatility using multi-layer take-profit strategies.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 12+ independent entry signals |
| **Exit Conditions** | Multiple dynamic take-profits + fixed stoploss + BTC protection |
| **Protection** | BTC 5-minute/1-day dump protection + slippage protection |
| **Timeframe** | Main timeframe 5m + information timeframe 1h |
| **Dependencies** | technical, talib, pandas_ta, numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.205,      # Exit at 20.5% profit immediately after entry
    "81": 0.038,     # Exit at 3.8% after 81 candles
    "292": 0.005,    # Exit at 0.5% after 292 candles
}

# Stoploss setting
stoploss = -0.10   # Base stoploss -10%

# Trailing stop
use_custom_stoploss = True
```

**Design Logic**:
- ROI table shows strategy pursues high initial take-profit point (20.5%)
- Take-profit targets gradually decrease as holding time extends
- Base stoploss -10%, but has multiple custom take-profit/stoploss mechanisms

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "limit",
    "exit": "limit",
    "stoploss": "market",
    "stoploss_on_exchange": False,
}
```

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms

| Protection Type | Parameter Description | Default Value |
|-----------------|----------------------|---------------|
| BTC Protection | 5-minute and 1-day BTC trend monitoring | buy_btc_safe: -200 ~ -300 |
| Slippage Protection | Maximum allowed slippage | max_slip: 0.983 |
| 1h Trend Check | ROC and BB width check | buy_roc_1h, buy_bb_width_1h |

### 3.2 Entry Conditions Details

#### Condition #1: BB_Dip (Bollinger Band Dip)
```python
is_dip = (
    rmi < 49
    & cci <= -116
    & srsi_fk < 32
)
is_break = (
    bb_delta > 0.025
    & bb_width > 0.095
    & close_delta > close * 0.0179
    & close < bb_lowerband3 * 0.999
)
is_BB_checked = is_dip & is_break
```

#### Condition #2: Local Uptrend
```python
is_local_uptrend = (
    ema_26 > ema_12
    & (ema_26 - ema_12) > open * 0.026
    & close < bb_lowerband2 * 0.999
    & close_delta > close * 0.0179
)
```

#### Condition #3: EWO (Elliot Wave Oscillator)
```python
is_ewo = (
    rsi_fast < 44
    & close < ema_8 * 0.935
    & EWO > -5.001
    & close < ema_8 * 0.968
    & rsi < 23
)
```

#### Condition #4: EWO2 (Enhanced EWO)
```python
is_ewo_2 = (
    ema_200_1h > ema_200_1h.shift(12)  # 1-hour trend upward
    & rsi_fast < 45
    & close < ema_8 * 0.970
    & EWO > 4.179
    & rsi < 35
)
```

#### Condition #5: R_Deadfish (Reverse Deadfish)
```python
is_r_deadfish = (
    ema_100 < ema_200 * 1.014
    & bb_width > 0.299
    & close < bb_middleband2 * 1.014
    & volume_mean_12 > volume_mean_24 * 1.59
    & cti < -0.115
    & r_14 < -44.34
)
```

#### Condition #6: Squeeze Momentum (SqzMom)
```python
is_sqzmom = (
    is_sqzOff  # BB and KC separated
    & linreg_val_20 trend upward
    & close < ema_13 * 0.981
    & EWO < -3.966
    & r_14 < -45.068
)
```

#### Condition #7: NFI 13
```python
is_nfi_13 = (
    ema_50_1h > ema_100_1h
    & close < sma_30 * 0.99
    & cti < -0.92
    & EWO < -5.585
    & crsi_1h > 10.0
)
```

#### Condition #8: NFI 32
```python
is_nfi_32 = (
    rsi_slow < rsi_slow.shift(1)
    & rsi_fast < 46
    & rsi > 25.0
    & close < sma_15 * 0.93
    & cti < -0.9
)
```

#### Condition #9: NFI 33
```python
is_nfi_33 = (
    close < ema_13 * 0.978
    & EWO > 8
    & cti < -0.88
    & rsi < 32
    & r_14 < -98.0
)
```

#### Condition #10: NFI 7_33
```python
is_nfi7_33 = (
    moderi_96  # Modified Elder Ray confirmation
    & cti < -0.88
    & close < ema_13 * 0.988
    & EWO > 6.4
    & rsi < 32.0
)
```

#### Condition #11: NFI 7_37
```python
is_nfi7_37 = (
    pm > pmax_thresh  # PMAX trend
    & close < sma_75 * 0.98
    & EWO > 9.8
    & cti < -0.7
    & safe_dump_50_1h
)
```

---

## IV. Exit Conditions Details

### 4.1 Custom Trailing Stoploss

```python
def custom_stoploss(self, current_profit, ...):
    if current_profit > 0.2:
        return 0.05   # Profit >20%, stoploss 5%
    elif current_profit > 0.1:
        return 0.03   # Profit >10%, stoploss 3%
    elif current_profit > 0.06:
        return 0.02   # Profit >6%, stoploss 2%
    elif current_profit > 0.03:
        return 0.015  # Profit >3%, stoploss 1.5%
```

### 4.2 Dynamic Take-Profit Logic (custom_exit)

Strategy uses `custom_exit` method to implement multi-layer take-profit:

| Profit Zone | Condition | Exit Signal |
|-------------|-----------|-------------|
| 0-1.2% | max_profit > current + 4.5% & rsi < 46 | Take-profit trail 1 |
| 0-1.2% | max_profit > current + 2.5% & rsi < 32 | Take-profit trail 2 |
| 1.2-2% | max_profit > current + 1% & rsi < 39 | Take-profit trail 3 |
| 1.2-2% | max_profit > current + 3.5% & rsi < 45 & cmf < 0 | Take-profit trail 4 |
| >2% | momdiv_sell_1h | Momentum divergence sell |
| >2% | Multiple CTI conditions met | Multi-confirmation sell |

### 4.3 Special Exit Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|------------------|-------------|
| BTC Protection | btc_diff < -365 | sell_btc_safe |
| Deadfish Mode | profit < -0.063 & bb_width < 0.043 | sell_deadfish |
| CTI_R Mode | cti > 0.844 & r > -19.99 | sell_cti_r |
| Stoploss Exit | Break below EMA200 & CMF negative | stoploss_u_e |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Usage |
|-------------------|--------------------|-------|
| Trend Indicators | EMA 4/8/12/13/16/20/26/50/100/200 | Judge multi-timeframe trend |
| Momentum Indicators | RSI (4/14/20), EWO, CRSI | Detect overbought/oversold |
| Volatility Indicators | Bollinger Bands (20, 1-4), KC (28) | Identify squeeze breakouts |
| Special Indicators | PMAX, MOMDIV, T3, SROC | Advanced trend identification |

### 5.2 1h Information Layer Indicators

- Ichimoku Cloud
- CTI (20/40 period)
- Williams %R (96/480)
- ROC, CMO
- MOMDIV (Momentum Divergence)
- Heikin Ashi ROCR
- T3 Moving Average

---

## VI. Risk Management Features

### 6.1 Slippage Protection Mechanism

```python
def confirm_trade_entry(self, ..., rate, ...):
    # Check if slippage is within acceptable range
    slippage = ((rate / dataframe["close"]) - 1) * 100
    if slippage < max_slip:
        return True
    return False
```

### 6.2 Multi-Layer Take-Profit Strategies

- Ladder trailing stoploss
- RSI condition take-profit
- Momentum Divergence take-profit
- Time decay take-profit

### 6.3 BTC Correlation Protection

Continues BB_RPB_TSL's BTC protection mechanism, with additional trend checks at 1h level.

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Rich conditions**: 12+ entry conditions adapt to various market environments
2. **Diverse take-profits**: Multiple take-profit strategies automatically match different profit levels
3. **Complete risk control**: Slippage protection + BTC protection + dynamic stoploss
4. **Multi-timeframe**: 5m main trading + 1h trend confirmation

### ⚠️ Cons

1. **Extremely complex**: Numerous parameters, difficult to tune
2. **High computation**: High hardware requirements
3. **Too many signals**: May lead to overtrading
4. **Overfitting risk**: More conditions = higher overfitting risk

---

## VIII. Parameter Optimization

| Parameter Category | Optimization Priority | Notes |
|-------------------|----------------------|-------|
| BTC Protection | High | Critical for risk control |
| Entry Thresholds | High | Affects signal frequency |
| Take-Profit Levels | Medium | Profit protection mechanism |
| Indicator Periods | Low | Default values generally work |

---

## IX. Live Trading Notes

### 9.1 Learning Curve

This strategy involves numerous technical indicators and multi-timeframe analysis. Beginners need to spend considerable time understanding the logic of each entry condition. Recommended to test on demo account first, observing trigger frequency and performance of each entry condition.

### 9.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------------|-------------|-----------------|
| 10-20 | 4GB | 8GB |
| 20-50 | 8GB | 16GB |

### 9.3 Suggested Testing Process

1. First observe signal distribution on demo account
2. Small capital live test for execution rate
3. Gradually optimize parameters
4.放大 position after confirming stability

---

## X. Summary

BB_RPB_TSLmeneguzzo is an **extremely complex** but **powerful** multi-condition trend strategy. Its core value lies in:

1. **Comprehensive coverage**: 12+ entry conditions cover almost all common patterns
2. **Smart take-profit**: Multi-layer take-profit strategies automatically adapt to different profit levels
3. **Complete risk control**: Slippage protection + BTC protection + dynamic stoploss
4. **Community validation**: Improved from mature strategies with some community foundation

For quantitative traders, this strategy suits **experienced investors**. Recommended to invest sufficient time understanding each condition's logic before live trading.

---

*This document is based on strategy code*
