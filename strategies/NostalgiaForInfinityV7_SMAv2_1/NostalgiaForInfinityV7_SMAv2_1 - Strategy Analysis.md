# NostalgiaForInfinityV7_SMAv2_1 — Strategy Analysis

> **Strategy ID**: #308 (out of 465 strategies)  
> **Strategy Type**: Multi-Condition Trend Following + Multi-Layer Protection + Dynamic Profit-Taking  
> **Timeframe**: 5 minutes (5m) + 1 hour (1h)

---

## I. Strategy Overview

NostalgiaForInfinityV7_SMAv2_1 is the SMA variant version of NostalgiaForInfinityV7. A multi-dimensional technical indicator combination quantitative trading strategy developed by the iterativ team for the Freqtrade platform.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 26 independent signals |
| **Sell Conditions** | 8 base + 12-level custom_sell + 36 dynamic exit scenarios |
| **Protection** | 26 groups (EMA trend, SMA direction, Safe Dips, Safe Pump) |
| **Timeframe** | Main: 5m, Informative: 1h |
| **Dependencies** | qtpylib, talib, technical (zema), numpy, pandas |

---

## II. Buy Conditions (26 Total)

| Category | Conditions | Core Logic |
|----------|-----------|------------|
| RSI/MFI Oversold | 1, 2, 8, 20, 21 | RSI/MFI low points with trend protection |
| Bollinger Band | 3, 4, 5, 6, 14, 15, 18, 22, 23 | Price at BB lower band |
| EMA Deviation | 5, 6, 7, 14, 15 | EMA26 > EMA12 with sufficient gap |
| EWO | 12, 13, 16, 17, 22, 23 | Elliott Wave Oscillator signals |
| SMA Deviation | 9, 10, 11, 12, 13, 16, 17 | Price deviates from SMA |
| Trend Shift | 19, 24 | CMF/EMA trend reversal |
| Extreme Values | 20, 21, 26 | RSI extremes or ZEMA lows |

---

## III. Protection Mechanisms

Each of the 26 conditions has independent protection parameters:

| Protection | Description |
|------------|-------------|
| ema_fast | Fast EMA > EMA200 |
| ema_slow (1h) | 1h EMA > EMA200_1h |
| close_above_ema_fast | Close > fast EMA |
| sma200_rising | SMA200 rising (multiple period options) |
| safe_dips | 11 levels (10–110) |
| safe_pump | 12 levels × 3 time windows (24h/36h/48h) |

---

## IV. Sell Logic

### 4.1 Custom Sell (12-Level)

| Profit Range | RSI Threshold | Signal Prefix |
|-------------|--------------|--------------|
| > 20% | < 34 | signal_profit_11 |
| 10%–12% | < 42 | signal_profit_10 |
| 5%–6% | < 43 | signal_profit_5 |
| 1%–2% | < 35 | signal_profit_1 |

### 4.2 Below EMA200 (12-Level)

More aggressive when price < EMA200.

### 4.3 Pump After (3 × 5 Levels)

Dedicated parameters for coins that surged 24h/36h/48h.

### 4.4 Trailing Stops

3 sets with profit range, RSI range, and drawdown thresholds.

### 4.5 Special Scenarios

- SMA Downtrend Exit
- EMA100 Below Exit
- Recovery Exit (from max loss)
- Long Holding Exit (> 900 min)

### 4.6 ATR Dynamic Stop Loss

4 levels of ATR-based stop loss thresholds.

---

## V. Strategy Pros & Cons

### ✅ Advantages
- Highly modular (26 conditions independently switchable)
- Multi-layer protection per condition
- Flexible profit-taking (12-level + trailing + scenarios)
- Dual timeframe verification (5m signal + 1h trend)
- Rich indicator system (10+ indicators)

### ⚠️ Limitations
- 400+ parameters — high optimization difficulty
- High computation (400 candles startup)
- Overfitting risk
- Configuration complexity
- Backtest/live gap

---

## VI. Summary

**NostalgiaForInfinityV7_SMAv2_1** is a "would rather miss than do wrong" conservative strategy. Comprehensive for experienced quants; may overwhelm beginners. Start with small capital testing before scaling up.
