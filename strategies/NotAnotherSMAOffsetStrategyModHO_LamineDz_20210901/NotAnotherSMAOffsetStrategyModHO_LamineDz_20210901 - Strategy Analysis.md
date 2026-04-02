# NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901 Strategy Analysis

## 1. Strategy Overview

### 1.1 Background

NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901 (NASO strategy) is a quantitative trading strategy based on SMA Offset principles, developed by LamineDz team in September 2021. The core idea: use MA offset characteristics combined with EWO and RSI to find oversold entry opportunities and exit at trend reversals or profit targets.

The "NotAnother" name reflects independent thinking — a departure from conventional SMA strategies.

### 1.2 Core Philosophy

**"Be greedy when others are fearful, be fearful when others are greedy."** The offset mechanism solves problems of frequent stop-outs in ranging markets and entry lag in trending markets that plague traditional MA strategies.

### 1.3 Architecture

- Framework: Freqtrade
- Timeframe: 5 minutes
- Suitable for: Crypto markets, moderate volatility, liquid pairs

---

## 2. Core Indicators

### 2.1 MA System

- **Buy EMA**: base_nb_candles_buy=10, low_offset=0.984 (buy at 1.6% below EMA)
- **Sell EMA**: base_nb_candles_sell=6, high_offset=1.002, high_offset_2=1.0
- **HMA_50**: Mid-term trend, low lag
- **EMA_100**: Long-term trend
- **SMA_9**: Short-term trend

### 2.2 EWO

```
EWO = (EMA_5 - EMA_200) / Low × 100
```

Thresholds: ewo_high=3.206, ewo_low=-10.69

### 2.3 RSI

- Fast: RSI(4)
- Standard: RSI(14), buy threshold 63
- Slow: RSI(20)

### 2.4 ADX

ADX(2) + DI for trend strength

---

## 3. Entry Signals

### 3.1 Channel 1: EWO High (Trend Pullback)

```
RSI_fast < 35 AND Close < EMA_buy × 0.984 AND EWO > 3.206
AND RSI < 63 AND Volume > 0 AND Close < EMA_sell × 1.002
```

### 3.2 Channel 2: EWO Low (Deep Oversold)

```
RSI_fast < 35 AND Close < EMA_buy × 0.984 AND EWO < -10.69
AND Volume > 0 AND Close < EMA_sell × 1.002
```

---

## 4. Exit Signals

### 4.1 Trend Continuation Exit

```
Close > SMA_9 AND Close > EMA_sell × 1.0 AND RSI > 50
AND Volume > 0 AND RSI_fast > RSI_slow
```

### 4.2 Trend Reversal Exit

```
Close < HMA_50 AND Close > EMA_sell × 1.002
AND Volume > 0 AND RSI_fast > RSI_slow
```

### 4.3 Exit Confirmation

ADX/DI filtering + HMA/EMA trend check + RSI momentum filter

---

## 5. Risk Management

### 5.1 Stop-Loss

- Fixed: **-10%** (tighter than many variants)
- Trailing: 0.75% distance, activates at 3% profit

### 5.2 ROI

```python
minimal_roi = {"0": 0.214}  # 21.4%
ignore_roi_if_buy_signal = True
```

### 5.3 Slippage Protection

max_slippage=-2%, retries=3

### 5.4 Profit-Only Selling

sell_profit_only=True, sell_profit_offset=0.01

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
- Dual-entry design for different states
- Multi-layer risk control
- Parameter optimizable

### Limitations
- Trend-dependent
- Parameter sensitivity
- Slippage risk
- False breakout risk

---

## 8. Summary

NASO strategy represents innovation in MA-based strategies. Five-layer protection (stop-loss, trailing, dynamic, slippage, exit confirmation) makes it suitable for experienced quantitative traders. Success requires thorough backtesting, parameter optimization, and disciplined execution.
