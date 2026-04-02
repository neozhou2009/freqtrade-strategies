# ObeliskIM_v1_1 Strategy Analysis

## Table of Contents

1. [Strategy Overview](#1-strategy-overview)
2. [Design Philosophy and Theory](#2-design-philosophy-and-theory)
3. [Technical Indicator System](#3-technical-indicator-system)
4. [Ichimoku Cloud Deep Dive](#4-ichimoku-cloud-deep-dive)
5. [Entry Signal Logic](#5-entry-signal-logic)
6. [Exit Signal Logic](#6-exit-signal-logic)
7. [Risk Management](#7-risk-management)
8. [Parameter Configuration](#8-parameter-configuration)
9. [Strategy Optimization](#9-strategy-optimization)
10. [Backtesting and Practice](#10-backtesting-and-practice)
11. [Summary](#11-summary)

---

## 1. Strategy Overview

### 1.1 Background

ObeliskIM_v1_1 is a trend-following strategy based on the Ichimoku Kinko Hyo, created by trader Obelisk in March 2021. According to the author, the strategy emerged from watching a YouTube video about the Ichimoku Cloud, then waking up at 3 AM unable to sleep and writing the first version. This "inspiration-driven" development approach is not uncommon in quantitative trading.

### 1.2 Positioning

Medium-to-short-term trend trading on the 5-minute timeframe, capturing intraday trend opportunities. Uses Ichimoku's multi-signal confirmation mechanism combined with fast EMA trend filtering — entering at early trend stages, exiting at reversals.

### 1.3 Core Features

- **Multi-dimensional confirmation**: Ichimoku + EMA, multiple confirmations before entry
- **Early trend entry**: TK Cross signals trend initiation
- **Strict risk control**: 4% stop-loss, phased ROI
- **Anti-chasing design**: Spike detection prevents buying at price peaks

---

## 2. Design Philosophy and Theory

### 2.1 Ichimoku Core Concept

Ichimoku (Ichimoku Kinko Hyo) was invented by Goshu Hosoda in the 1930s — a system designed to let traders assess market trend, momentum, and support/resistance with one chart look. Its unique feature: incorporating time dimensions via displacement, with the "cloud" predicting future support/resistance zones.

### 2.2 Trend-Following Philosophy

"Trend is your friend" — strategy enters at early trend stages rather than attempting to predict bottoms or tops. Benefits:
- Follows established trends, avoids counter-trend risks
- Signal reliability from confirmed trend initiation
- Simple, consistent execution rules

### 2.3 Multi-Confirmation Design

Each entry requires multiple conditions simultaneously — "better to miss an opportunity than to make a mistake". Every entry backed by: Ichimoku trend confirmation + TK Cross trigger + EMA momentum + price spike check.

---

## 3. Technical Indicator System

### 3.1 EMA Triple System

Extremely short periods for 5-minute framework:
- EMA3: 3-period EMA — captures short-term momentum
- EMA5: 5-period EMA — confirms short-term direction
- EMA10: 10-period EMA — filters noise

```python
ema35_ok = (EMA3 > EMA5) AND (EMA5 > EMA10)
```
Bullish when EMA3 > EMA5 > EMA10 (ascending arrangement).

### 3.2 Spike Detection
```python
spike = close > (close.shift(3) * (1 - stoploss * 0.9))
```
Prevents buying when price surged >3.6% in 3 candles — anti-chasing protection.

### 3.3 Recent High
```python
recent_high = high.rolling(12).max()
```
Entry requires price breaking above the 1-hour (12 × 5min) recent high.

---

## 4. Ichimoku Cloud Deep Dive

### 4.1 Custom Parameters

| Component | Standard | Strategy | Rationale |
|-----------|----------|----------|-----------|
| Conversion Line | 9 | 20 | Reduced noise, more stable |
| Base Line | 26 | 60 | Adapted for 5-minute |
| Lagging Span | 52 | 120 | More stability |
| Displacement | 26 | 30 | Fine-tuned cloud position |

### 4.2 Strong Green Cloud
```python
cloud_green_strong = (cloud_green) AND (tenkan_sen > kijun_sen) AND (kijun_sen > senkou_a)
```
Three-way bull confirmation: cloud green + Conversion above Base + Base above cloud.

### 4.3 TK Cross Signal
```python
tk_cross_up = crossed_above(tenkan_sen, kijun_sen)
tk_cross_up.fillna(method='ffill', limit=2)
```
TK Cross signal extends forward 2 candles — allows flexibility to enter shortly after cross.

---

## 5. Entry Signal Logic

Six conditions all required:

1. **cloud_green_strong > 0**: Full bull trend confirmation
2. **tk_cross_up > 0**: Trend initiation trigger
3. **ema35_ok > 0**: Short-term momentum confirmed
4. **close > close.shift()**: Current candle bullish
5. **close > recent_high.shift()**: Broke 1-hour high
6. **spike < 1**: Not chasing a spike

Combined logic: Big trend confirmed → Trend starting → Momentum confirmed → Price rising → Breaking out → Not chasing = BUY.

---

## 6. Exit Signal Logic

Two OR conditions — either triggers exit:

1. **TK Cross Down**: Conversion Line crosses below Base Line
2. **Price Below Base Line**: Close falls below Kijun-sen

Simple and direct — "trend reverses = exit." With 4% stop-loss as floor protection.

---

## 7. Risk Management

### 7.1 Stop-Loss: -4%
Tight stop appropriate for 5-minute framework, prevents large single-trade losses.

### 7.2 Phased ROI
```python
minimal_roi = {
    "0": 0.10,   # 10% immediate target
    "30": 0.05,  # 5% after 30 min
    "60": 0.02   # 2% after 60 min
}
```
Early strong trend = hit 10%; moderate trend = 5%; late exit = 2%.

### 7.3 Time = Risk
Longer hold → lower target. Acknowledges time uncertainty.

---

## 8. Parameter Configuration

**Timeframe**: 5 minutes (fixed)
**Ichimoku**: 20-60-120-30 (custom, non-standard)
**EMA**: 3/5/10
**Stop-loss**: -4%
**ROI**: 10% → 5% → 2%

---

## 9. Strategy Optimization

### 9.1 Author's Suggested Improvements

**Reduce false signals in ranging markets**: Add ADX filter, ATR volatility filter, use cloud thickness.

**Faster entry in strong trends**: Add price retracement to Base Line as secondary entry, or lower conditions when price above cloud and breaking highs.

### 9.2 Additional Suggestions

- Add RSI filter (code defines it but doesn't use)
- Add volume confirmation
- Multi-timeframe: confirm with 1h trend before 5-minute entries
- Dynamic stop-loss using cloud or ATR

---

## 10. Backtesting and Practice

**Best pairs**: High-liquidity mainstream coins (BTC, ETH)
**Recommended data**: At least 6 months, multiple market conditions
**Required startup candles**: 288 (1 day @ 5m)
**Fee consideration**: Set 0.1%+ for accurate results

---

## 11. Summary

ObeliskIM_v1_1 is a well-designed trend-following strategy with solid theory, strict signal filtering, and comprehensive risk control. Its key strength is the multi-confirmation entry mechanism — entering at early trend stages while avoiding false breakouts.

Limitations include ranging market vulnerability, entry lag, unused RSI, long-only design, and single timeframe. These can be addressed through planned improvements.

Best suited for: trend-following believers, those who can accept ranging-period losses, and patient traders with strong discipline.

---

*Document Date: March 27, 2026*
*Strategy Version: ObeliskIM v1.1*
