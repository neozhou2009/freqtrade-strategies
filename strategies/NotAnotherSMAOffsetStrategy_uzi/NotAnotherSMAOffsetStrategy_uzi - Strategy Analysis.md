# NotAnotherSMAOffsetStrategy_uzi Strategy Analysis

## 1. Strategy Overview

### 1.1 Background

NotAnotherSMAOffsetStrategy_uzi is a quantitative trading strategy based on SMA Offset principles, developed by Rallipanos for the Freqtrade framework. The strategy's core innovation is the "offset" concept — rather than waiting for price to cross the MA, it buys when price falls below MA by a certain percentage.

### 1.2 Core Positioning

- **Trading style**: Mean reversion + trend confirmation
- **Timeframe**: 5 minutes
- **Buy logic**: Two independent conditions (ewo1, ewolow)
- **Sell logic**: Two conditions (trend continuation, momentum exhaustion)
- **Stop-loss**: -7%
- **Trailing stop**: 0.5% distance, activates at 3% profit

---

## 2. Technical Indicators

### 2.1 MA System

- **EMA**: base_nb_candles_buy=14, base_nb_candles_sell=24
- **HMA_50**: Mid-term trend, low lag
- **SMA_9**: Short-term trend

### 2.2 EWO

```
EWO = (EMA_fast - EMA_slow) / Close × 100
```

fast=50, slow=200. Thresholds: ewo_high=2.327, ewo_low=-20.988

### 2.3 RSI

- RSI(4): Fast entry
- RSI(14): Standard
- RSI(20): Slow exit confirmation

---

## 3. Entry Signals

### 3.1 ewo1 (Trend Pullback)

```
RSI_fast < 35 AND Close < EMA × 0.975 AND EWO > 2.327
AND RSI < 69 AND Volume > 0
```

### 3.2 ewolow (Extreme Oversold)

```
RSI_fast < 35 AND Close < EMA × 0.975 AND EWO < -20.988
AND Volume > 0
```

---

## 4. Exit Signals

### 4.1 Trend Continuation

```
Close > SMA_9 AND Close > EMA × 0.997 AND RSI > 50
AND RSI_fast > RSI_slow AND Volume > 0
```

### 4.2 Momentum Exhaustion

```
SMA_9 rising fast AND Close < HMA_50 AND Close > EMA × 0.991
AND RSI_fast > RSI_slow AND Volume > 0
```

### 4.3 Exit Confirmation

```python
if (HMA_50 × 1.149 > EMA_100) and (Close < EMA_100 × 0.951):
    return False  # Reject exit
```

---

## 5. Risk Management

### 5.1 Stop-Loss

```python
stoploss = -0.07  # -7%
```

### 5.2 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.005
trailing_stop_positive_offset = 0.03
```

### 5.3 ROI

```python
minimal_roi = {
    "0": 0.215,   # 21.5%
    "40": 0.032,  # 3.2%
    "87": 0.016,  # 1.6%
    "201": 0
}
```

### 5.4 Sell Profit Only

```python
sell_profit_only = True
sell_profit_offset = 0.005  # Min 0.5% profit
```

---

## 6. Parameters

| Parameter | Default | Range |
|-----------|---------|-------|
| base_nb_candles_buy | 14 | 5-80 |
| low_offset | 0.975 | 0.9-0.99 |
| ewo_high | 2.327 | 2.0-12.0 |
| ewo_low | -20.988 | -20.0--8.0 |
| rsi_buy | 69 | 30-70 |
| base_nb_candles_sell | 24 | 5-80 |
| high_offset | 0.991 | 0.95-1.1 |
| high_offset_2 | 0.997 | 0.99-1.5 |

---

## 7. Pros & Cons

### Advantages
- Clear entry logic: buy cheap, sell expensive
- Dual buy signals adapt to different markets
- Multi-layer risk control (stop-loss, trailing, ROI)
- Sell only when profitable
- Strong stop-loss discipline

### Limitations
- -7% stop-loss still significant
- Long only, no shorting
- Parameter optimization needed
- Ranging market vulnerability

---

## 8. Summary

NotAnotherSMAOffsetStrategy_uzi is a well-designed strategy combining mean reversion with trend confirmation. Its tight -7% stop-loss and smart trailing mechanism make it suitable for traders seeking disciplined risk management. Best for medium-term trend-following in crypto markets.
