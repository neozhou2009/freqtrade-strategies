# NostalgiaForInfinityV7_SMAv2 — Strategy Analysis

---

## I. Strategy Overview

NostalgiaForInfinityV7_SMAv2 is the V7 SMA variant's second version, developed by the iterativ team for the Freqtrade platform. This strategy uses SMA (Simple Moving Average) as the core trend indicator, combining with multi-layer protection mechanisms to capture trend opportunities while effectively controlling drawdown risk.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 26 independent signals (#1–#26, #25 missing) |
| **Sell Conditions** | 8 base sell + 12-level custom_sell |
| **Protection** | Each condition: 7–10 protection parameter groups |
| **Timeframe** | Main: 5m, Informative: 1h |
| **Startup Candles** | 400 |
| **Recommended Positions** | 4–6 concurrent, 40–80 pair whitelist |

---

## II. Technical Indicator System

### 2.1 Moving Averages

**EMA Series**: 12, 15, 20, 26, 35, 50, 100, 200
**SMA Series**: 5, 30, 200 (SMA200 is the long-term trend benchmark)

### 2.2 Oscillators

**RSI**: 4 (fast), 14 (standard), 20 (slow) — for overbought/oversold and momentum
**MFI**: 14-period — money flow confirmation with RSI
**EWO**: (EMA5 - EMA35) / Close × 100 — Elliott Wave Oscillator
**CMF**: 20-period — Chaikin Money Flow

### 2.3 Bollinger Bands

**BB20**: 20-period, 2 standard deviations — for short-term volatility
**BB40**: 40-period, 2 standard deviations — more stable reference

### 2.4 Special Indicators

**Choppiness Index**: 14-period — trending vs choppy market identification
**ZEMA**: 61-period — zero-lag EMA for faster response

---

## III. Protection Mechanisms

### 3.1 Safe Dips (11 Levels, 10–110)

Prevents buying during significant drawdowns. Each level has 4 thresholds (0/2/12/144 periods).

### 3.2 Safe Pump (12 Levels × 3 Time Windows, 24h/36h/48h)

Prevents buying after rapid price surges. Two-condition check: (1) range change below threshold, OR (2) sufficient pullback from high.

### 3.3 SMA200 Trend Confirmation

SMA200 rising (comparing with N periods ago) — the "anchor" of the entire strategy.

---

## IV. Buy Conditions (26 Total)

| Category | Conditions | Core Logic |
|----------|-----------|------------|
| RSI/MFI Oversold | 1, 2, 8, 20, 21 | RSI/MFI lows with trend protection |
| Bollinger Band | 3, 4, 5, 6, 14, 15, 18, 22, 23 | Price at/touching BB lower band |
| EMA Deviation | 5, 6, 7, 14, 15 | EMA26 > EMA12 with gap |
| EWO | 12, 13, 16, 17, 22, 23 | Elliott Wave Oscillator values |
| SMA Deviation | 9, 10, 11, 12, 13, 16, 17 | Price deviates from SMA |
| Trend Shift | 19, 24 | CMF/EMA trend reversal |
| Extreme Values | 20, 21, 26 | RSI extremes or ZEMA lows |

### Key Conditions

**Condition #1**: SMA200 rising, RSI 30–84, RSI < 36, MFI < 36 — classic trend pullback entry.

**Condition #8**: RSI < 29, volume > 2× previous, bullish candle, long lower wick — volume price reversal.

**Condition #18**: RSI < 26, BB lower band, multiple trend protections — most protected condition.

**Condition #24**: EMA golden cross + CMF positive shift — trend reversal entry.

---

## V. Sell Logic

### 5.1 Custom Sell (12-Level Profit-Taking)

| Profit | RSI | Signal |
|--------|-----|--------|
| > 20% | < 34 | signal_profit_11 |
| 10%–12% | < 42 | signal_profit_10 |
| 5%–6% | < 43 | signal_profit_5 |
| 1%–2% | < 34 | signal_profit_1 |
| 0.1%–1% | < 34 | signal_profit_0 |

### 5.2 Below EMA200 (12-Level)

Independent, more aggressive parameters when price < EMA200.

### 5.3 Pump After (3 Sets × 5 Levels)

For coins that surged 24h/36h/48h.

### 5.4 Trailing Stop (3 Sets)

| Set | Profit Range | RSI | Drawdown |
|-----|-------------|-----|----------|
| Trail 1 | 16%–60% | 20–50 | 3% |
| Trail 2 | 10%–40% | 20–50 | 3% |
| Trail 3 | 6%–20% | — | 5% + SMA200_1h falling |

### 5.5 Recovery Exit

- Max loss > 12%, now profit > 4% → exit
- Max loss > 6%, profit 1%–5%, RSI < 46 → exit

### 5.6 Long Holding Exit

Profit 3%–4%, holding > 900 minutes (15 hours).

---

## VI. Base Sell Signals (8)

```python
# 1: RSI > 79.5 + 6 candles above BB upper
# 2: RSI > 81 + 3 candles above BB upper
# 3: RSI > 82 (pure RSI overbought)
# 4: RSI > 73.4 AND RSI_1h > 79.6 (dual timeframe)
# 6: Below EMA200 but above EMA50, RSI > 79
# 7: RSI_1h > 81.7 AND EMA12 crosses below EMA26
# 8: Close > BB20_1h upper × 1.1
```

---

## VII. Risk Management

### 7.1 Multi-Level Stop Loss

1. **Fixed Stop**: -10% hard stop
2. **Trailing Stop**: 0.5% distance after 3% profit
3. **Dynamic Stop**: EMA200 proximity, long-holding conditions
4. **Recovery Stop**: From deep loss, exit on partial recovery

### 7.2 Risk Control at Entry

- Safe Dips prevents catching falling knives
- Safe Pump prevents chasing after surges
- Trend confirmation ensures trend-following
- Volume check ensures liquidity

---

## VIII. Summary

NostalgiaForInfinityV7_SMAv2 is a mature crypto quantitative strategy with:
- Long-term validation
- Comprehensive protection
- High configurability
- Multi-timeframe verification

**Core philosophy**: Follow the trend, control risk, let profits run, stop losses promptly.

Success requires: understanding logic, reasonable configuration, patient execution, continuous optimization.
