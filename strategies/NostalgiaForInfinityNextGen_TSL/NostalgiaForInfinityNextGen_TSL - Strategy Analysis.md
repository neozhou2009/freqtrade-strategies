# NostalgiaForInfinityNextGen_TSL Strategy Analysis

> **Strategy ID**: #288 (288th of 465 strategies)  
> **Strategy Type**: NFI Series - Multi-Condition Trend Following + Trailing Stop Enhanced Version  
> **Timeframe**: 15 Minutes (15m) + 1 Hour (1h)

---

## I. Strategy Overview

**NostalgiaForInfinityNextGen_TSL** (abbreviated NFI NextGen TSL) is the "Trailing Stop Enhanced Version" of NostalgiaForInfinityNextGen. Building on NextGen's core multi-condition architecture, the TSL version comprehensively enhances the trailing stop mechanism, aiming to better protect profits and reduce drawdowns.

"TSL" stands for **Trailing Stop Loss** (追踪止损), which is this strategy's core differentiating feature. Compared to the original NextGen, the TSL version is more aggressive in profit protection, suited for traders pursuing steady profitability and drawdown control.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 16 independent buy signals, each condition can be independently enabled/disabled |
| **Exit Conditions** | 6 base sell signals + enhanced trailing stop logic |
| **Protection Mechanisms** | 16 sets of buy protection parameters + enhanced trailing stop parameters |
| **Timeframe** | 15-minute primary timeframe + 1-hour informational timeframe |
| **Dependencies** | pandas, numpy, TA-Lib, technical, qtpylib, pandas_ta |
| **Core Difference** | Trailing stop parameter optimization, stronger profit protection |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table (time: minimum profit rate)
minimal_roi = {
    "0": 0.10,    # Immediate exit: 10% profit
    "30": 0.05,   # After 30 minutes: 5% profit
    "60": 0.02,   # After 60 minutes: 2% profit
}

# Stop-Loss Settings
stoploss = -0.10  # -10% hard stop-loss

# Trailing Stop (TSL version core parameter - Enhanced)
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.015   # 1.5% trailing activation point (original 1%)
trailing_stop_positive_offset = 0.025  # 2.5% offset trigger (original 3%)
trailing_stop_negative = -0.02   # -2% negative trailing threshold (new)
```

**Design Philosophy**:
- Uses a **time-decaying ROI** strategy
- **Enhanced Trailing Stop**: TSL version raises trailing activation from 1% to 1.5%, lowers offset trigger from 3% to 2.5%
- Adds **trailing_stop_negative** parameter, more sensitive negative trailing
- Trailing stop activates earlier, locks in profits faster
- Hard stop-loss at -10% controls maximum loss per trade

### 2.2 TSL Parameter Comparison vs. NextGen Original

| Parameter | NextGen Original | TSL Enhanced | Change Description |
|-----------|-----------------|-------------|-------------------|
| trailing_stop_positive | 0.01 (1%) | 0.015 (1.5%) | Trailing activation raised |
| trailing_stop_positive_offset | 0.03 (3%) | 0.025 (2.5%) | Offset trigger lowered |
| trailing_stop_negative | None | -0.02 (-2%) | Negative trailing added |

**Change Interpretation**:
- **Trailing Activation Raised**: From 1% to 1.5%, meaning trailing starts when profit reaches 1.5%
- **Offset Trigger Lowered**: From 3% to 2.5%, enters trailing state earlier
- **Negative Trailing Added**: Allows triggering trailing stop when profit drawdown reaches 2%

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms (16 Sets)

Each entry condition has an independent protection parameter set:

| Protection Type | Parameter Description | Options |
|-----------------|----------------------|---------|
| **Fast EMA** | Whether fast EMA is enabled and its length | 26/50/100/200 |
| **Slow EMA** | Whether slow EMA is enabled and its length | 26/50/100/200 |
| **Close Price Protection** | Whether close price is above EMA | 12/20/26/50/100/200 |
| **SMA200 Rising** | Whether SMA200 is in an uptrend | 20/30/36/44/50 period verification |
| **SMA200 1h Rising** | 1h period SMA200 trend confirmation | 20/30/36/44/50 |
| **Safe Dip** | Dip magnitude threshold protection | 10/50/80/100/130 etc. |
| **Safe Pump** | Pump magnitude threshold protection | 10/20/30/50/70/100/120 etc. |
| **Safe Pump Period** | Detection period | 24h/36h/48h |
| **BTC Trend** | Whether BTC 1h is not in a downtrend | True/False |

### 3.2 16 Entry Conditions Classification

| Condition Group | Condition Numbers | Core Logic |
|-----------------|-------------------|------------|
| **Strict Protection Group** | 1-3 | Multi-protection + trend confirmation |
| **Trend Following Group** | 4-6 | EMA trend + momentum confirmation |
| **Relaxed Entry Group** | 7-9 | Fewer protection conditions |
| **1h Confirmation Group** | 10-12 | High-period trend verification |
| **Aggressive Entry Group** | 13-14 | Fast signal response |
| **BTC Correlation Group** | 15-16 | BTC trend filtering |

---

## IV. Exit Logic Details

### 4.1 Multi-Layer Take-Profit System

```
Profit Range          Threshold        Exit Strategy
───────────────────────────────────────────────────────
> 10%              Immediate        ROI initial exit
5%-10%             30 minutes       ROI secondary exit
2%-5%              60 minutes       ROI tertiary exit
< 2%               Hold             Wait for signal or stop-loss
```

### 4.2 Trailing Stop Mechanism (TSL Version Core)

TSL version's trailing stop mechanism is the core differentiating feature:

```
Trailing activation condition: profit >= 1.5%
Trailing trigger condition: profit >= 2.5% after which trailing begins
Trailing stop trigger: profit drawdown triggers trailing
Negative trailing threshold: profit drawdown >= 2%
```

**Trailing Stop Flow**:
1. When profit reaches 2.5%, trailing stop activates
2. Price continues rising, stop-loss line follows upward
3. Price pulls back, stop-loss line remains stationary
4. Profit drawdown reaches threshold, trigger stop-loss sell

**TSL Version Advantages**:
- Trailing activates earlier (1.5% vs 1%)
- Enters trailing state earlier (2.5% vs 3%)
- Negative trailing protection (-2% threshold)
- More aggressive profit protection

### 4.3 Special Exit Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| **BB Upper Band Breakout** | Continuous upper band breakout | Overbought exit |
| **RSI Extreme** | RSI overbought threshold | Momentum exit |
| **Below EMA** | Price breaks below EMA200 | Trend exit |
| **Trailing Stop** | Profit drawdown triggers | Protection exit (TSL enhanced) |

---

## V. Risk Management Features

### 5.1 Enhanced Trailing Stop (TSL Core Feature)

TSL version's core advantage is trailing stop enhancement:

| Feature | Description | Advantage |
|---------|-------------|-----------|
| **Earlier Activation** | 1.5% profit activates trailing | Protects profit earlier |
| **Earlier Trailing** | 2.5% offset triggers | Enters trailing state faster |
| **Negative Protection** | -2% drawdown threshold | Prevents large profit drawdowns |
| **Dynamic Adjustment** | Stop-loss line follows upward | Locks in floating profit |

### 5.2 Multi-Level Dip Protection (Safe Dips)

Dip threshold protection from levels 10 to 130:

```
Level    Protection Strength    Applicable Scenario
─────────────────────────────────────────────────────
10       Relaxed                Strong trending market
50       Medium                General market
80       Relatively Strict      Volatile market
100      Strict                High-risk environment
130      Extremely Strict       Extreme market
```

### 5.3 BTC Trend Filtering

Some entry conditions require BTC 1h not in a downtrend:
- Conditions 15-16 have this protection enabled by default

---

## VI. Strategy Pros & Cons

### Advantages

1. **Enhanced Trailing Stop**: More aggressive profit protection, better drawdown control
2. **Refined Conditions**: 16 entry conditions covering main market environments
3. **Period Adaptation**: 15-minute timeframe suitable for medium-short-term trend following
4. **Complete Protection**: 16 sets of protection parameters, refined risk management
5. **Multi-Period Verification**: 15m execution + 1h trend confirmation
6. **Flexible Configuration**: Each condition can be independently enabled/disabled
7. **TSL Parameter Optimization**: Compared to original, locks in profits faster

### Limitations

1. **Lower Signal Frequency**: Signal frequency relatively lower on 15-minute timeframe
2. **Trailing Stop Sensitivity**: May exit prematurely, missing larger gains
3. **Depends on Historical Data**: Requires sufficient 1h and 15m historical data
4. **Ranging Market Risk**: Trailing stop may trigger frequently in ranging markets

---

## VII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| **Trending Upward** | Enable all conditions | Trailing stop maximizes profit |
| **Ranging Market** | Enable protection groups 1-6 | Strict protection filters false signals |
| **High Volatility** | Enable BTC filtering conditions | Prevent systemic risk |
| **Low Volatility** | Relax protection thresholds | Increase trading opportunities |

**TSL Version Especially Suitable For**:
- Traders pursuing steady profitability
- Conservative style focused on profit protection
- Investors wanting to reduce drawdowns

---

## VIII. Applicable Market Environment Details

NostalgiaForInfinityNextGen_TSL is the trailing stop enhanced version of the NFI series. It is best suited for **medium-long-term trends with clear direction**, especially in scenarios with higher profit protection needs.

### 8.1 Strategy Core Logic

- **Enhanced Trailing Stop**: TSL parameters optimized, locks in profit earlier
- **Refined Entry Conditions**: 16 different entry conditions, optimized for 15-minute timeframe
- **Strict Risk Filtering**: Real-time detection of "24h/36h/48h rises" prevents chasing
- **Multi-Period Confirmation**: 15m execution + 1h trend confirmation, double insurance
- **BTC Trend Correlation**: Via "BTC 1h trend detection" reduces systemic risk

### 8.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:---|:---|:---|
| Slow Bull/Ranging Upward | StarsStarsStarsStarsStars | Trailing stop maximizes profit, excellent drawdown control |
| Wide Ranging | StarsStarsStarsStars | Protection filters false breakouts, TSL reduces drawdowns |
| One-Sided Selloff | StarsStarsStars | BTC trend filtering + hard stop-loss double protection |
| Extreme Sideways | StarsStars | Few signal triggers, trailing stop may trigger frequently |

---

## IX. Summary

**NostalgiaForInfinityNextGen_TSL** is the trailing stop enhanced version of the NFI series. Its core value lies in:

1. **Enhanced Trailing Stop**: Activates trailing earlier, locks in profit faster
2. **Refined Conditions**: 16 entry conditions covering main market environments
3. **Complete Protection**: 16 sets of protection parameters, refined risk management
4. **Drawdown Control**: TSL parameter optimization, reduces profit drawdowns

For quantitative traders, this is a strategy focused on profit protection. Recommendations:
- Understand trailing stop working principles and parameter impacts
- Adjust TSL parameters based on target trading pair characteristics
- Follow 1h timeframe trend confirmation signals
- Enjoy smaller drawdowns and more stable profitability
