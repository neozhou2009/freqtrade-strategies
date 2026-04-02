# NotAnotherSMAOffsetStrategyModHO Strategy Analysis

## 1. Strategy Overview

### 1.1 Positioning

NotAnotherSMAOffsetStrategyModHO is a trend-following quantitative strategy based on MA Offset + EWO, designed for crypto markets. "ModHO" = Modified + Hull Optimization, featuring HMA and advanced order management enhancements.

Core philosophy: **"Trend is king, offset is tool"** — trend is the market's dominant force; price deviation from trend provides entry timing.

### 1.2 Features

- Multi-dimensional signal verification (three entry signals)
- Dynamic parameter adjustment
- Complete stop-loss + trailing + tiered ROI
- Slippage protection
- Multi-timeframe analysis (5m + 1h)

---

## 2. Technical Indicators

### 2.1 MA Family

- **EMA**: base_nb_candles_buy default 10, base_nb_candles_sell default 6
- **SMA_9**: Short-term trend
- **HMA_50**: Mid-term trend, low lag
- **EMA_100**: Long-term trend reference

### 2.2 EWO

```
EWO = (EMA(5) - EMA(200)) / Low × 100
```

fast=50, slow=200. Thresholds: ewo_high=3.206, ewo_low=-10.69

### 2.3 RSI Multi-Period

RSI Fast(4), Standard(14), Slow(20)

### 2.4 ADX

ADX(2) + DI for trend strength and direction

---

## 3. Entry Signals

### 3.1 Signal 1: Trend Confirmation (ewo1)

```
RSI_fast < 35 AND Close < EMA_buy × 0.984 AND EWO > 3.206
AND RSI < 63 AND Volume > 0 AND Close < EMA_sell × 1.002
```

### 3.2 Signal 2: Bottom-Fishing (ewo2)

```
RSI_fast < 35 AND Close < EMA_buy × 0.984 AND EWO < -10.69
AND Volume > 0 AND Close < EMA_sell × 1.002
```

---

## 4. Exit Signals

### 4.1 Condition 1: Trend Continuation

```
Close > SMA_9 AND Close > EMA_sell × high_offset_2 (1.0)
AND RSI > 50 AND Volume > 0 AND RSI_fast > RSI_slow
```

### 4.2 Condition 2: Trend Weakening

```
Close < HMA_50 AND Close > EMA_sell × high_offset (1.002)
AND Volume > 0 AND RSI_fast > RSI_slow
```

### 4.3 Exit Confirmation

ADX/DI filtering + HMA/EMA trend consistency + RSI momentum check

---

## 5. Risk Management

### 5.1 Stop-Loss

- Fixed: **-32%**
- Trailing: 0.75% distance, activates at 3% profit

### 5.2 ROI

```python
minimal_roi = {"0": 0.214}  # 21.4%
ignore_roi_if_buy_signal = True
```

### 5.3 Custom Stop-Loss

Dynamic adjustment based on profit level and holding time.

### 5.4 Slippage Protection

max_slippage=-2%, retries=3

---

## 6. Parameters

| Parameter | Default | Range |
|-----------|---------|-------|
| base_nb_candles_buy | 10 | 5-80 |
| low_offset | 0.984 | 0.9-0.99 |
| ewo_high | 3.206 | 2.0-12.0 |
| ewo_low | -10.69 | -20.0--8.0 |
| rsi_buy | 63 | 30-70 |
| base_nb_candles_sell | 6 | 5-80 |
| high_offset | 1.002 | 0.95-1.1 |
| high_offset_2 | 1.0 | 0.99-1.5 |

---

## 7. Pros & Cons

### Advantages
- Unique offset mechanism
- Dual signal design
- Multi-layer risk control
- Intelligent stop-loss
- Parameter optimizable

### Limitations
- Wide stop-loss (-32%)
- Complex buy conditions
- Ranging market underperformance
- Parameter sensitivity

---

## 8. Summary

NotAnotherSMAOffsetStrategyModHO is a carefully designed quantitative strategy. Core idea: use price deviation from trend to find entry opportunities. Best suited for experienced traders who understand indicators and risk management. Success requires understanding principles, proper optimization, and disciplined execution.
