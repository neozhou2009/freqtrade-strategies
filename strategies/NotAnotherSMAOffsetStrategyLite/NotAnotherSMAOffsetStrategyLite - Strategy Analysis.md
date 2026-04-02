# NotAnotherSMAOffsetStrategyLite Strategy Analysis

## Chapter 1: Strategy Overview

### 1.1 Background

NotAnotherSMAOffsetStrategyLite is a lightweight quantitative trading strategy based on SMA Offset technology. The "Lite" designation indicates a simplified version — keeping core trading logic while optimizing parameter complexity and computational requirements.

### 1.2 Core Philosophy

The strategy applies the offset mechanism concept: instead of waiting for price to cross the MA, it sets a discount threshold and buys when price falls below MA by a set percentage. Combined with EWO for trend confirmation, it seeks "trend pullback" opportunities.

### 1.3 Applicable Scenarios

- 5-minute cryptocurrency trading
- Moderate volatility markets
- Trend markets with clear pullbacks
- Liquid trading pairs

---

## Chapter 2: Technical Indicators

### 2.1 EMA System

- Buy EMA: `base_nb_candles_buy` default 14, range 5-80
- Sell EMA: `base_nb_candles_sell` default 24, range 5-80
- Offset buy: `low_offset` default 0.975 (buy when price < EMA's 97.5%)
- Offset sell: `high_offset` default 0.991 (sell when price > EMA's 99.1%)

### 2.2 EWO

```
EWO = (EMA_fast - EMA_slow) / Close × 100
```

Parameters: fast=50, slow=200. EWO > 0 confirms uptrend for buy conditions.

### 2.3 RSI System

- RSI(14): Standard
- RSI(4): Fast for entry
- RSI(20): Slow for confirmation

---

## Chapter 3: Entry Logic

### 3.1 Entry Conditions

Three conditions must ALL be met:

1. **Price below offset**: `close < EMA × low_offset (0.975)`
2. **EWO positive**: `ewo > 0` (uptrend confirmation)
3. **Volume positive**: `volume > 0`

### 3.2 Logic

Captures "trend pullback" opportunities. Uptrend exists (EWO > 0) but price temporarily below EMA → buy at discount.

---

## Chapter 4: Exit Logic

### 4.1 Exit Condition

```
close > EMA × high_offset (0.991) AND volume > 0
```

Simpler than entry — price returns to near baseline = take profit.

### 4.2 Profit Protection

- `sell_profit_only = True`: Only sell when profitable
- `sell_profit_offset = 0.01`: Minimum 1% profit before sell signals work

---

## Chapter 5: Risk Management

### 5.1 Fixed Stop-Loss

```python
stoploss = -0.1  # 10%
```

### 5.2 Dynamic Stop-Loss

```python
if current_profit < -0.05 and holding_time > 720 minutes:
    return -0.01  # Tighten to -1%
```

After 12 hours at >5% loss, tighten stop to -1%.

### 5.3 ROI

```python
minimal_roi = {'0': 0.025}  # 2.5% minimum
```

---

## Chapter 6: Time Frame

```python
timeframe = '5m'
startup_candle_count = 200
```

---

## Chapter 7: Pros & Cons

### 7.1 Advantages

- Clear, simple logic
- Trend confirmation via EWO
- Offset-based dynamic entry
- Complete risk control
- Highly optimizable

### 7.2 Limitations

- Long only, no shorting
- Parameter sensitivity
- Slippage impact
- Overfitting risk
- Ranging market underperformance

---

## Chapter 8: Summary

NotAnotherSMAOffsetStrategyLite is a well-designed lightweight strategy. Core philosophy: "buy cheap during uptrends, sell when recovered." Three-entry/one-exit logic with stop-loss protection. Suitable for users seeking simplicity with effectiveness. Success requires understanding principles, proper parameter tuning, and strict risk control.
