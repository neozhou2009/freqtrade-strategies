# NFI46FrogZ Strategy Analysis

> **Strategy ID**: #263 (263rd of 465 strategies)  
> **Strategy Type**: Multi-condition Trend Following + Dynamic Take-Profit System  
> **Timeframe**: 5 Minutes (5m) + 1 Hour (1h) Informational Layer

---

## I. Strategy Overview

NFI46FrogZ is a multi-condition quantitative strategy evolved from NostalgiaForInfinityV4. It fuses the essence of trend-following, mean reversion, and momentum strategies, capturing trading opportunities across different market environments through 17 independent entry conditions and a multi-layer dynamic take-profit system.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 17 independent buy signals, each independently enableable/disableable |
| **Exit Conditions** | 8 basic sell signals + multi-layer dynamic take-profit logic |
| **Protection Mechanisms** | Dip Protection (3 levels) + Pump Protection (3 time windows × 3 levels) |
| **Timeframe** | 5m (primary) + 1h (informational) |
| **Dependencies** | freqtrade, numpy, talib, finta, pandas, cachetools, skopt |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.028,         # Immediate profit: 2.8%
    "10": 0.018,        # After 10 minutes: 1.8%
    "40": 0.005,        # After 40 minutes: 0.5%
    "180": 0.018,       # After 3 hours: 1.8%
}

# Stop Loss
stoploss = -0.10        # 10% stop loss

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.025
```

**Design Philosophy**:
- ROI table features a "second chance" design: after 180 minutes, if the price rises again, it gives another 1.8% profit opportunity, preventing premature exits
- Stop loss at -10% gives sufficient volatility tolerance
- Trailing stop activates at 2.5% profit, protecting 1% profit

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'market',
    'sell': 'market',
    'trailing_stop_loss': 'market',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms (Dip + Pump Dual Protection)

Each entry condition is equipped with independent protection parameter groups:

#### Dip Protection (Pullback Protection)

| Protection Type | Parameter Count | Function |
|---------------|-----------------|----------|
| Normal Dips | 4 thresholds | Standard pullback protection |
| Strict Dips | 4 thresholds | Strict pullback protection |
| Loose Dips | 4 thresholds | Loose pullback protection |

#### Pump Protection (Surge Protection)

| Time Window | Levels | Parameters |
|------------|--------|-------------|
| 12 hours | Normal/Strict/Loose | pump_threshold + pump_pull_threshold |
| 24 hours | Normal/Strict/Loose | pump_threshold + pump_pull_threshold |
| 36 hours | Normal/Strict/Loose | pump_threshold + pump_pull_threshold |
| 48 hours | Normal/Strict/Loose | pump_threshold + pump_pull_threshold |

### 3.2 Typical Entry Condition Examples

#### Condition #1: Trend Pullback Entry
```python
# Logic
- EMA50_1h > EMA200_1h (1h trend up)
- SMA200 uptrend
- safe_dips (pullback protection passed)
- safe_pump_48_1h (48h surge protection passed)
- 36h minimum gain > 2.2%
- RSI_1h in 30-80 range
- RSI < 36 (oversold)
- MFI < 26 (low money flow)
```

#### Condition #3: Bollinger Band Lower Band Rebound
```python
# Logic
- Close > EMA200_1h × 0.988 (close to but not breaking long MA)
- EMA100 > EMA200 (medium-term trend up)
- safe_pump_36_1h (surge protection)
- BB lower band rebound signal:
  - close < lower.shift() (breaks below lower band)
  - bbdelta > close × 5.7% (volatility sufficient)
  - closedelta > close × 2.3% (significant price action)
```

#### Condition #8: Alligator Breakout
```python
# Logic
- close > smma_lips > smma_teeth > smma_jaw (alligator mouth opens upward)
- MAs in bullish alignment and continuously rising
- RSI < 46
- SMA200_1h uptrend
```

### 3.3 Classification of 17 Entry Conditions

| Condition Group | Condition Numbers | Core Logic |
|----------------|------------------|------------|
| Trend Pullback | #1, #10, #11 | Trend up + pullback entry |
| Bollinger Band Rebound | #2, #3, #4, #5, #6, #14 | BB lower band rebound |
| EMA Deviation | #5, #6, #7, #14, #15 | EMA12/26 deviation |
| Alligator Breakout | #8 | Alligator bullish alignment |
| Mean Reversion | #9, #12, #13, #16, #17 | EWO + oversold |

---

## IV. Exit Conditions Details

### 4.1 Multi-Layer Take-Profit System

The strategy employs a tiered take-profit mechanism (12 profit levels):

```
Profit Range           RSI Threshold    Signal Name
──────────────────────────────────────────────────────
> 20%                  < 34            signal_profit_11
12% ~ 20%              < 42            signal_profit_10
10% ~ 12%              < 50            signal_profit_9
9% ~ 10%               < 54            signal_profit_8
8% ~ 9%                < 54            signal_profit_7
7% ~ 8%                < 49            signal_profit_6
6% ~ 7%                < 44            signal_profit_5
5% ~ 6%                < 43            signal_profit_4
4% ~ 5%                < 42            signal_profit_3
3% ~ 4%                < 38            signal_profit_2
2% ~ 3%                < 34            signal_profit_1
1% ~ 2%                < 33            signal_profit_0
```

**Design Philosophy**: Higher profit yields lower RSI thresholds, locking in profits while avoiding premature exits.

### 4.2 Special Exit Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| Below EMA200 Exit | close < EMA200 + profit tier | signal_profit_u_* |
| Pumped Pairs Exit | Post 48h/36h/24h surge | signal_profit_p_* |
| SMA Decline Exit | SMA200 downtrend | signal_profit_d_* |
| Trailing Exit | Profit drawdown detection | signal_profit_t_* |
| Custom Stop-Loss | Pumped pairs special stop-loss | signal_stoploss_p_* |

### 4.3 Basic Sell Signals (8)

```python
# Sell Signal 1: RSI + BB Upper Band Continuous Breakout
- RSI > 79.5
- close > bb_upperband (5 consecutive candles)

# Sell Signal 2: RSI + BB Upper Band (3 candles)
- RSI > 81
- close > bb_upperband (3 consecutive candles)

# Sell Signal 3: Pure RSI Overbought
- RSI > 82

# Sell Signal 4: Dual RSI Overbought
- RSI > 73.4
- RSI_1h > 79.6

# Sell Signal 6: Below EMA Rebound
- close < EMA200 and close > EMA50
- RSI > 79

# Sell Signal 7: EMA Death Cross
- RSI_1h > 81.7
- EMA12 crosses below EMA26

# Sell Signal 8: BB Relative Position
- close > bb_upperband_1h × 1.1
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | EMA(12,15,20,26,35,50,100,200), SMA(5,30,200) | Trend identification, support/resistance |
| Momentum Indicators | RSI(14), Stoch Fast, StochRSI | Overbought/oversold identification |
| Volatility Indicators | BB(20,40), ATR(14) | Volatility, breakout signals |
| Volume Indicators | MFI, VFI, Volume Mean | Money flow analysis |
| Special Indicators | EWO, Alligator, SAR, CMF, DMI, ADX | Auxiliary judgment |

### 5.2 Informational Timeframe Indicators (1h)

- EMA series (12,15,20,26,35,50,100,200)
- SMA200 and directional judgment
- RSI
- Bollinger Bands
- Chaikin Money Flow
- Pump/Dip protection signals

---

## VI. Risk Management Highlights

### 6.1 Multi-Layer Stop-Loss Mechanism

| Stop-Loss Type | Trigger Condition | Description |
|---------------|-------------------|-------------|
| Fixed Stop-Loss | -10% | Final defense line |
| Trailing Stop | Profit > 2.5% | Protects 1% profit |
| Custom Stop-Loss | Trade duration > 50 min + specific conditions | Dynamic adjustment |
| Pump Stop-Loss | Special stop-loss post-surges | Prevents profit reversal |

### 6.2 Dip Protection (Pullback Protection)

Three-level protection mechanism detecting maximum decline from 1 candle to 144 candles (12 hours):

| Level | Single Candle | 2 Candles | 12 Candles | 144 Candles |
|-------|--------------|-----------|------------|-------------|
| Normal | 2% | 14% | 32% | 50% |
| Strict | 1.5% | 6% | 24% | 40% |
| Loose | 2.6% | 24% | 42% | 80% |

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Multi-Dimensional Entry Signals**: 17 conditions covering trend pullback, mean reversion, breakout and more
2. **Refined Risk Management**: Tiered take-profit, multi-layer stop-loss, Dip/Pump dual protection
3. **Timeframe Synergy**: 5m execution + 1h trend judgment, improving signal quality
4. **Highly Configurable**: All parameters optimizable, adapting to different market environments

### ⚠️ Cons

1. **High Parameter Complexity**: 100+ optimizable parameters, risk of overfitting
2. **High Resource Requirements**: 400 startup candles + multi-timeframe, high memory demands
3. **Live vs. Backtest Discrepancy**: Complex logic may perform differently in live trading
4. **Steep Learning Curve**: Understanding and tuning requires significant time

---

## VIII. Summary

**NFI46FrogZ** is a **fully-featured multi-condition quantitative strategy**. Its core value lies in:

1. **Rich Signals**: 17 entry conditions covering diverse market scenarios
2. **Refined Risk Control**: Tiered take-profit, multi-layer stop-loss, Dip/Pump dual protection
3. **Mature Framework**: Based on NostalgiaForInfinity series, long-term community validation

This strategy is suitable for intermediate to advanced users. Beginners should first use default parameters for backtesting and dry-run trading, and consider parameter optimization only after becoming familiar.
