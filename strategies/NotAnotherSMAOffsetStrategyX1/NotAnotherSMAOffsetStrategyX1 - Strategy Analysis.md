# NotAnotherSMAOffsetStrategyX1 Strategy Analysis

## 1. Strategy Overview

### 1.1 Positioning

NotAnotherSMAOffsetStrategyX1 is a quantitative trading strategy based on SMA Offset, specifically designed for crypto markets. It combines EMA, HMA, RSI, and EWO into a complete trend-following + mean reversion system.

The "NotAnother" name signals a departure from conventional MA strategies — it uses offset coefficients rather than simple MA crossover signals.

### 1.2 Core Design

- **Primary timeframe**: 5 minutes
- **Auxiliary timeframe**: 1 hour
- **Buy logic**: EMA offset-based mean reversion with trend confirmation
- **Sell logic**: Dynamic tiered selling based on profit level
- **Stop-loss**: -35%
- **Trailing stop**: 1% distance, activates at 3% profit

### 1.3 Architecture

- Entry: 69 conditions (ewo1, ewolow primarily; ewo2 commented out)
- Exit: Tiered selling system (~12 tiers based on profit level)
- Risk: Multi-layer (hard stop, trailing, custom stop, protections)

---

## 2. Technical Indicator System

### 2.1 MA System

- **EMA**: base_nb_candles_buy=14, base_nb_candles_sell=24
- **SMA_9**: Short-term trend
- **HMA_50**: Mid-term trend, low lag
- **EMA_100**: Long-term trend

### 2.2 EWO

```
EWO = (EMA_fast - EMA_slow) / Close × 100
```

fast=50, slow=200. Thresholds: ewo_high=2.327, ewo_low=-19.988

### 2.3 RSI

- RSI(4): Fast entry confirmation
- RSI(14): Standard overbought/oversold
- RSI(20): Slow exit confirmation

---

## 3. Entry Signals

### 3.1 ewo1 (Primary)

```
RSI_fast < 35 AND Close < EMA_buy × 0.975 AND EWO > 2.327
AND RSI < 69 AND Volume > 0 AND Close < EMA_sell × 0.991
```

### 3.2 ewolow (Reversal)

```
RSI_fast < 35 AND Close < EMA_buy × 0.975 AND EWO < -19.988
AND Volume > 0 AND Close < EMA_sell × 0.991
```

---

## 4. Exit Signals

### 4.1 Price > HMA 50

```
Close > SMA_9 AND Close > EMA_sell × 0.997 AND RSI > 50
AND Volume > 0 AND RSI_fast > RSI_slow
```

### 4.2 Price < HMA 50

```
Close < HMA_50 AND Close > EMA_sell × 0.991 AND Volume > 0
AND RSI_fast > RSI_slow
```

### 4.3 Exit Confirmation

```python
if (HMA_50 × 1.149 > EMA_100) and (Close < EMA_100 × 0.951):
    return False  # Reject exit if trend still intact
```

---

## 5. Risk Management

### 5.1 Hard Stop-Loss

```python
stoploss = -0.35  # -35%
```

### 5.2 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.005  # 0.5%
trailing_stop_positive_offset = 0.03  # 3% activation
```

### 5.3 Custom Stop-Loss (Segmented)

Based on profit zones:
- Profit < 2.2%: Hard stop
- Profit 2.2%-8%: Linear interpolation
- Profit > 8%: Stop tightens with profit

### 5.4 ROI

```python
minimal_roi = {
    "0": 0.215,   # 21.5%
    "40": 0.032,  # 3.2%
    "87": 0.016,   # 1.6%
    "201": 0       # Break-even
}
```

### 5.5 Protections

- LowProfitPairs: Pause if pair loses >5% in 60 candles
- CooldownPeriod: 2-candle cooldown between trades

---

## 6. Parameters

| Parameter | Default | Range |
|-----------|---------|-------|
| base_nb_candles_buy | 14 | 5-80 |
| low_offset | 0.975 | 0.9-0.99 |
| ewo_high | 2.327 | 2.0-12.0 |
| ewo_low | -19.988 | -20.0--8.0 |
| rsi_buy | 69 | 30-70 |
| base_nb_candles_sell | 24 | 5-80 |
| high_offset | 0.991 | 0.95-1.1 |
| high_offset_2 | 0.997 | 0.99-1.5 |

---

## 7. Pros & Cons

### Advantages
- 69 entry conditions for adaptability
- Dynamic tiered selling system
- Multi-timeframe verification
- BTC correlation monitoring
- Comprehensive risk controls

### Limitations
- High parameter complexity
- Wide -35% stop-loss
- Ranging market vulnerability
- Requires significant optimization effort

---

## 8. Summary

NotAnotherSMAOffsetStrategyX1 is a sophisticated strategy with multi-dimensional entry signals and a dynamic tiered selling mechanism. Best suited for experienced quantitative traders who can dedicate time to parameter optimization and monitoring. The strategy rewards disciplined risk management and thorough backtesting.
