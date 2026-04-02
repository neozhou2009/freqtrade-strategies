# NFI47V2 Strategy Analysis

> **Strategy ID**: #267 (267th of 465 strategies)  
> **Strategy Type**: Multi-condition Trend Following + Multi-layer Protection Mechanisms  
> **Timeframe**: 5 Minutes (5m) + 1 Hour (1h) Informational Layer

---

## I. Strategy Overview

NFI47V2 (NostalgiaForInfinityV2) is a highly complex multi-condition trend-following strategy belonging to the V2 version of the NostalgiaForInfinity series. The strategy integrates 17 independent entry conditions and 8 basic sell signals, paired with three-layer DIP protection mechanisms and three-layer PUMP protection mechanisms, constructing an all-around trading system.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 17 independent buy signals, independently enableable/disableable |
| **Exit Conditions** | 8 basic sell signals + 12-layer dynamic take-profit logic |
| **Protection Mechanisms** | 12 DIP protection parameter groups + 9 PUMP protection parameter groups |
| **Timeframe** | 5m (primary) + 1h (informational) |
| **Dependencies** | talib, qtpylib, technical (zema), pandas, numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,    # Immediate: 10%
    "30": 0.05,   # After 30 minutes: 5%
    "60": 0.02    # After 60 minutes: 2%
}

# Stop Loss
stoploss = -0.10  # Fixed stop loss 10%

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = False
trailing_stop_positive = 0.01        # Activates after 1% profit
trailing_stop_positive_offset = 0.025 # Triggers on 2.5% drawdown from high
```

**Design Philosophy**:
- ROI uses declining design, encouraging quick profit-taking, relaxing requirements over time
- 10% fixed stop loss as final defense line
- Trailing stop allows capturing more profit during trends

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms (Three-Layer Defense)

#### DIP Protection (Deep Drop Protection)

| Level | Parameter Range | Description |
|------|----------------|--------------|
| **Normal** | 4 thresholds (threshold_1-4) | Standard deep drop protection |
| **Strict** | 4 thresholds (threshold_5-8) | Strict deep drop protection |
| **Loose** | 4 thresholds (threshold_9-12) | Loose deep drop protection |

**Core Logic**: Checks whether the current price's decline from the highest price across different time windows (instant, 2, 12, 144 candles) exceeds the threshold.

#### PUMP Protection (Surge Protection)

| Time Window | Levels | Parameter Groups |
|------------|--------|------------------|
| **24 hours** | Normal/Strict/Loose | threshold_1, 4, 7 |
| **36 hours** | Normal/Strict/Loose | threshold_2, 5, 8 |
| **48 hours** | Normal/Strict/Loose | threshold_3, 6, 9 |

**Core Logic**: Detects whether there are abnormal surges recently, avoiding buying at highs.

### 3.2 Classification of 17 Entry Conditions

| Condition Group | Condition Numbers | Core Logic |
|----------------|------------------|------------|
| **Trend Pullback** | #1, #11 | RSI/MFI oversold pullback in uptrend |
| **Bollinger Band Lower Band** | #2, #3, #4, #5, #6, #14 | Price touching near BB lower band |
| **EMA Deviation** | #5, #6, #7, #14, #15 | EMA12/26 negative deviation + oversold |
| **Alligator Breakout** | #8 | Alligator bullish alignment confirmation |
| **SMA Oversold** | #9, #10, #12, #13, #16, #17 | SMA relative position + EWO indicator |

---

## IV. Exit Conditions Details

### 4.1 Multi-Layer Take-Profit System

12-level dynamic take-profit mechanism:

```
Profit Range               RSI Threshold    Signal Name
─────────────────────────────────────────────────────────────
> 21.6%                    < 33.15          signal_profit_11
10%-21.6%                  < 45.16          signal_profit_10
8.7%-11%                   < 58.66          signal_profit_9
...
0%-1.6%                    < 45.61          signal_profit_0
```

### 4.2 Special Exit Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| **Below EMA200 Exit** | close < EMA200 + profit/RSI conditions | signal_profit_u_* |
| **PUMP Exit** | Post-surge detection exit conditions | signal_profit_p_* |
| **SMA Decline Exit** | Profit-taking in SMA200 downtrend | signal_profit_d_* |
| **Trailing Exit** | Drawdown from high by certain percentage | signal_profit_t_* |
| **Recovery Exit** | Recovery from deep loss | signal_profit_r_* |
| **Long Hold Exit** | Small profit exit after holding > 900 minutes | signal_profit_l_* |

### 4.3 Basic Sell Signals (8)

```python
# Sell Signal 1: RSI Overbought + BB Upper Band Continuous
- RSI > 79.5
- 6 consecutive candles close above BB upper band

# Sell Signal 3: Pure RSI Extreme Overbought
- RSI > 82

# Sell Signal 4: Dual Timeframe RSI Overbought
- RSI_5m > 73.4
- RSI_1h > 79.6

# Sell Signal 7: 1h RSI Overbought + EMA Death Cross
- RSI_1h > 81.7
- EMA12 crosses below EMA26
```

---

## V. Risk Management Highlights

### 5.1 Multi-Layer DIP Protection

```python
# Normal Level - Standard Protection
safe_dips_normal = (
    (current decline < 1.7%) &
    (2 candles max decline < 5.8%) &
    (12 candles max decline < 32%) &
    (144 candles max decline < 27.8%)
)
```

### 5.2 Multi-Timeframe PUMP Protection

Detects price fluctuations within 24/36/48 hours — if fluctuation exceeds threshold or price has already fallen significantly from high, marked as "unsafe."

---

## VI. Strategy Pros & Cons

### ✅ Pros

1. **Multi-Condition Risk Diversification**: 17 entry conditions covering diverse market scenarios, reducing single signal failure risk
2. **Three-Layer Protection**: DIP and PUMP protection mechanisms effectively avoid chasing highs and catching falling knives
3. **Dynamic Take-Profit System**: 12-level take-profit dynamically adjusts based on profit and RSI, adapting to different market rhythms
4. **Multi-Timeframe Confirmation**: 1h timeframe provides higher-dimensional trend confirmation

### ⚠️ Cons

1. **Many Parameters**: 100+ adjustable parameters, high optimization difficulty, significant overfitting risk
2. **Complex Calculations**: Requires computing many indicators, higher hardware requirements
3. **Long Startup Time**: Requires 400 candles of warm-up data (~33 hours of 5m data)
4. **Live vs. Backtest Discrepancy**: Complex logic may perform differently in live trading

---

## VII. Summary

**NFI47V2** is a highly complex multi-condition trend-following strategy. Its core value lies in:

1. **Comprehensive Market Coverage**: 17 entry conditions covering diverse entry scenarios
2. **Multi-Layer Protection Mechanism**: DIP and PUMP protection effectively filters high-risk entries
3. **Dynamic Take-Profit System**: 12-level take-profit flexibly adjusts based on market conditions

For quantitative traders, NFI47V2 is a strategy template worthy of deep research, but note:
- Do not over-optimize parameters
- Conduct sufficient out-of-sample validation
- Test in simulated trading before live trading
