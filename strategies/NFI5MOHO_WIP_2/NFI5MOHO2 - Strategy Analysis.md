# NFI5MOHO2 Strategy Analysis

> **Strategy ID**: #270 (270th of 465 strategies)  
> **Strategy Type**: Multi-condition Trend Following + Multi-MA Offset + Elliott Wave + Protection Mechanisms  
> **Timeframe**: 5 Minutes (5m) + 1 Hour (1h) Informational Layer

---

## I. Strategy Overview

**NFI5MOHO2** is a hyper-optimized fusion of NostalgiaForInfinityV5 series with MultiOffsetLambo strategy. It inherits the NFI series' multi-condition trend-following characteristics while incorporating multi-MA offset technology and Elliott Wave Oscillator (EWO) as auxiliary judgment, building a highly complex trading system.

Strategy name origin:
- **NFI5** = NostalgiaForInfinityV5 base framework
- **MO** = MultiOffset (multi-MA offset)
- **HO** = Hyper-Optimized (hyper-optimized parameters)
- **2** = Version iteration

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 21 independent buy signals + 5 MA offset signals, independently enableable/disableable |
| **Exit Conditions** | 8 basic sell signals + 5 MA offset sell signals + dynamic take-profit logic |
| **Protection Mechanisms** | 3 Dip protection classes + 9 Pump protection groups (strict/normal/loose three modes) |
| **Timeframe** | 5m primary + 1h informational |
| **Dependencies** | qtpylib, talib, pandas, numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table - set to 1% trigger
minimal_roi = {
    "0": 0.01,
}

# Fixed stop loss 10%
stoploss = -0.10

# Trailing Stop Configuration
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01      # Starts trailing after 1% profit
trailing_stop_positive_offset = 0.03  # Activates trailing at 3% profit
```

**Design Philosophy**:
- ROI set to 1%, but with `ignore_roi_if_buy_signal=True`, ROI is ignored when buy signal exists
- 10% fixed stop loss as final defense, actual trading exits earlier through tiered take-profit
- Trailing stop activates at 3% profit, locking in at least 1% profit

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms (3 Dip + 9 Pump)

| Protection Type | Description | Default Values |
|---------------|-------------|----------------|
| **safe_dips** | Normal decline protection, check 1/2/12/144 candle max decline | 2%/14%/32%/50% |
| **safe_dips_strict** | Strict decline protection, more conservative thresholds | 1.5%/6%/24%/40% |
| **safe_dips_loose** | Loose decline protection, more aggressive thresholds | 2.6%/24%/42%/66% |
| **safe_pump_24/36/48** | Normal Pump protection (24/36/48 hours) | thresholds 0.5~1.3 |
| **safe_pump_24/36/48_strict** | Strict Pump protection | thresholds 0.4~0.68 |
| **safe_pump_24/36/48_loose** | Loose Pump protection | thresholds 0.66~1.3 |

### 3.2 MA Offset System

```python
ma_types = ['sma', 'ema', 'trima', 't3', 'kama']

# Buy offset (price below MA * offset)
low_offset: 0.90~0.99

# Sell offset (price above MA * offset)
high_offset: 0.99~1.10
```

### 3.3 Classification of 26 Entry Conditions

| Condition Group | Condition Numbers | Core Logic |
|----------------|-----------------|------------|
| **Trend Following Type** | #1, #10, #14, #18, #19 | Depends on EMA/SMA trend confirmation |
| **Bollinger Band Breakout Type** | #3, #4, #5, #6, #14, #15, #18 | Uses BB lower band breakout |
| **EWO Signal Type** | #12, #13, #16, #17 | Elliott Wave Oscillator |
| **RSI Oversold Type** | #1, #7, #9, #11, #15, #16, #20, #21 | RSI low point buy |
| **Low Volume Buy Type** | #2, #8, #9, #10, #12, #13, #16, #17, #18, #20, #21 | Volume analysis |
| **MA Offset Type** | MA_offset_5 | SMA/EMA/TRIMA/T3/KAMA offset |

---

## IV. Exit Conditions Details

### 4.1 Multi-Layer Take-Profit System

```
Profit Range           Threshold          Signal Name
────────────────────────────────────────────────────────
> 25%                RSI < 50          signal_profit_4
> 8%                 RSI < 48          signal_profit_3
> 5%                 RSI < 43          signal_profit_2
> 3%                 RSI < 38          signal_profit_1
> 1%                 RSI < 33          signal_profit_0

(Below EMA200)
> 60%                RSI < 62          signal_profit_u_3
> 4%                 RSI < 60          signal_profit_u_2
> 2%                 RSI < 56          signal_profit_u_1
```

### 4.2 Dynamic Trailing Take-Profit

```
15%~46% profit      18% drawdown      signal_profit_t_1
1%~12% profit       14% drawdown      signal_profit_t_2
5%~10% profit       1% drawdown       signal_profit_t_3
(Below EMA200)
5%~10% profit       1% drawdown       signal_profit_u_t_1
```

---

## V. Strategy Pros & Cons

### ✅ Pros

1. **Multi-Dimensional Trend Confirmation**: Uses 5m and 1h simultaneously, confirming trends through EMA/SMA multi-cycle
2. **Flexible Entry Signals**: 21 entry conditions covering various market forms, independently enableable/disableable
3. **Complete Protection Mechanism**: Dip/Pump protection prevents chasing and selling
4. **Dynamic Take-Profit**: Intelligently adjusts exit points based on profit and RSI
5. **MA Offset Technology**: 5 MA types providing additional buy/sell signals

### ⚠️ Cons

1. **Extremely Many Parameters**: 100+ adjustable parameters, high optimization difficulty
2. **High Computational Complexity**: Requires 300 candles warm-up, computationally intensive
3. **Overfitting Risk**: Parameters hyper-optimized, may overfit historical data
4. **Delay Issues**: Multi-timeframe analysis may cause signal delays

---

## VI. Summary

**NFI5MOHO2** is a **super-complex strategy integrating the best of NostalgiaForInfinity series with MultiOffset technology**. Its core value lies in:

1. **Multi-Dimensional Confirmation**: Dual timeframe + multi-indicator + multi-protection mechanism
2. **Highly Customizable**: Each entry condition independently enableable/disableable
3. **Dynamic Take-Profit**: Intelligently adjusts exits based on profit and RSI
4. **MA Offset**: 5 MA types providing additional buy/sell signals

For quantitative traders, this is a strategy requiring deep understanding, cautious configuration, and long-term validation. It is recommended to, after passing backtesting, first test with small funds and then gradually scale up.
