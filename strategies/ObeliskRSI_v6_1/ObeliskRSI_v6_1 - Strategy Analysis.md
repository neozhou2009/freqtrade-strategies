# ObeliskRSI_v6_1 Strategy Analysis

## Table of Contents

1. [Strategy Overview and Design Philosophy](#1-strategy-overview-and-design-philosophy)
2. [Theory Foundation and Market Understanding](#2-theory-foundation-and-market-understanding)
3. [Core Indicator System](#3-core-indicator-system)
4. [Buy/Sell Signal Logic](#4-buysell-signal-logic)
5. [Profit-Taking and Stop-Loss Design](#5-profit-taking-and-stop-loss-design)
6. [Trend Judgment and Parameter Adaptation](#6-trend-judgment-and-parameter-adaptation)
7. [Parameter Details](#7-parameter-details)
8. [Risk Management and Protection](#8-risk-management-and-protection)
9. [Applicable Scenarios and Pair Selection](#9-applicable-scenarios-and-pair-selection)
10. [Strategy Advantages and Limitations](#10-strategy-advantages-and-limitations)
11. [Code Implementation Notes](#11-code-implementation-notes)
12. [Live Application Advice](#12-live-application-advice)

---

## 1. Strategy Overview and Design Philosophy

ObeliskRSI_v6_1 is an RSI-based quantitative trading strategy released by developer Obelisk in March 2021. The core design philosophy: enter when the market shows oversold pullback, buying the dip and waiting for rebounds. Uses RSI as the primary buy/sell trigger with a dual-threshold system (bull/bear market modes) enabling dynamic parameter adjustment.

The strategy employs 5 minutes as its primary timeframe, suitable for medium-to-short-term trading, capturing intraday opportunities in cryptocurrency markets.

### 1.1 Core Innovation

The strategy's key innovation is the **long-period RSI-based trend classification** — resampling 5-minute data to 1-hour, then determining whether the market is in bull or bear mode. Different thresholds apply in each mode:
- Bull market: RSI drops to 35 → buy; rises to 69 → sell
- Bear market: RSI drops to 21 → buy; rises to 55 → sell

### 1.2 Positioning

A **mean-reversion dip-buying strategy** — enters when RSI reaches oversold levels, profits from the subsequent bounce. In trending markets, this works well; in prolonged directional moves, it underperforms.

---

## 2. Theory Foundation and Market Understanding

### 2.1 Overbought/Oversold Theory

Based on the technical analysis principle that market prices don't move indefinitely in one direction — extremes must eventually revert. RSI quantifies this deviation from average strength.

### 2.2 Left-Side Trading

The strategy uses **left-side trading** — entering before trend reversal is confirmed, attempting to buy at or near the bottom. vs. right-side trading (waiting for confirmation). Left-side offers better entry prices but higher risk of being wrong.

The dual-threshold system mitigates left-side risk: looser thresholds in bull markets, tighter in bear markets.

### 2.3 Multi-Period Analysis

5-minute primary for signal triggering, 60-minute (resampled) for trend classification. "Look long-term, act short-term" filters counter-trend trades and improves win rate.

---

## 3. Core Indicator System

### 3.1 Standard RSI

14-period RSI on 5-minute data as primary trigger.

### 3.2 Long-Period Resampled RSI

12× resampling: 5-minute × 12 = 60-minute RSI. Used purely for trend classification:
- When long-period RSI > 60 → **bull market mode**
- Otherwise → **bear market mode**

### 3.3 Bull/Bear State Flag

```python
dataframe['bull'] = dataframe[resample_rsi_key].gt(60).astype('int')
```

---

## 4. Buy/Sell Signal Logic

### 4.1 Buy Signal

**Dual-threshold system**:

| Market State | RSI Buy Threshold | Meaning |
|-------------|-------------------|---------|
| Bull (bull=1) | RSI crosses below 35 | Moderate pullback in uptrend → buy |
| Bear (bull=0) | RSI crosses below 21 | Extreme oversold in downtrend → buy |

```python
((dataframe['bull'] > 0) & qtpylib.crossed_below(dataframe['rsi'], params['bull-buy-rsi-value'])) |
(~(dataframe['bull'] > 0) & qtpylib.crossed_below(dataframe['rsi'], params['bear-buy-rsi-value']))
```

### 4.2 Sell Signal

| Market State | RSI Sell Threshold |
|-------------|-------------------|
| Bull | RSI > 69 |
| Bear | RSI > 55 |

---

## 5. Profit-Taking and Stop-Loss Design

### 5.1 Stepped ROI

```python
minimal_roi = {
    "0": 0.15,    # Immediate: 15%
    "35": 0.04,   # 35 minutes: 4%
    "65": 0.01,   # 65 minutes: 1%
    "115": 0      # 115 minutes: force exit
}
```

### 5.2 Static Stop-Loss: -30%

### 5.3 Custom Dynamic Stop-Loss (Key Innovation)

Uses easeInCubic function to gradually tighten stop-loss over time:

```python
def easeInCubic(t):
    return t * t * t

# Stop ramp: -30% initially → ~0% after custom_stop_ramp_minutes
```

At ramp start: allows -30% fluctuation. As time passes, stop line rises. After 110 minutes (default), stop ≈ 0 — forced exit.

---

## 6. Trend Judgment and Parameter Adaptation

### 6.1 Why Dual Thresholds?

**Bull market**:
- Pullbacks are moderate, won't hit extreme oversold — looser threshold (35) catches more opportunities
- Rising is easier — higher sell threshold (69) lets profits run

**Bear market**:
- Downtrends are violent — need extreme oversold (21) to avoid catching knives
- Rebounds are weak — lower sell threshold (55) takes profits earlier

### 6.2 Threshold Validation

RSI > 60 as bull/bear divider means the long-period RSI shows more ups than downs — a reasonable "relative strength" barometer.

---

## 7. Parameter Details

| Parameter | Default | Description |
|-----------|---------|-------------|
| bull-buy-rsi-value | 35 | Bull market buy RSI |
| bear-buy-rsi-value | 21 | Bear market buy RSI |
| bull-sell-rsi-value | 69 | Bull market sell RSI |
| bear-sell-rsi-value | 55 | Bear market sell RSI |
| stoploss | -0.30 | Static stop-loss |
| custom_stop_ramp_minutes | 110 | Dynamic stop ramp time |

---

## 8. Risk Management and Protection

### 8.1 Consecutive Loss Guard

Recommended configuration:
```json
"protections": [{
    "method": "StoplossGuard",
    "lookback_period": 720,
    "trade_limit": 2,
    "stop_duration": 720,
    "only_per_pair": true
}]
```

After 2 consecutive stop-losses on one pair in 720 candles, pause that pair for 720 candles.

### 8.2 Startup Requirements
`startup_candle_count = 240` — needs 240 historical candles.

---

## 9. Applicable Scenarios and Pair Selection

### 9.1 Recommended Pairs
SXP, MATIC, SUSHI, CHZ — moderate market cap, good volatility, sufficient liquidity.

### 9.2 NOT Recommended
BTC and ETH — too stable, not enough pullback opportunities for this strategy.

### 9.3 Best Scenarios
- Volatile ranging markets: frequent pullback opportunities
- Moderate volatility: sufficient pullback depth AND rebound space

### 9.4 Worst Scenarios
- Prolonged one-directional bull markets: no pullbacks to buy
- Prolonged downtrends: bottom-catching fails repeatedly

---

## 10. Strategy Advantages and Limitations

### Advantages
1. **Trend-adaptive**: Dual thresholds adapt to market conditions
2. **Risk-controlled**: Dynamic stop tightens over time
3. **Dip-buying edge**: Better risk/reward than chasing breakouts
4. **Few parameters**: Simple, easy to tune
5. **Efficient computation**: No complex indicators

### Limitations
1. **Fails in directional markets**: Misses trending moves, gets stopped in sustained trends
2. **Parameter-sensitive**: Thresholds significantly impact results
3. **Left-side risk**: May buy too early, catch falling knives
4. **No trend filter**: No clear trend direction indicator

---

## 11. Code Implementation Notes

### 11.1 Helper Functions
```python
def easeInCubic(t): return t * t * t
def clamp(num, min_value, max_value): return max(min(num, max_value), min_value)
def clamp01(num): return clamp(num, 0, 1)
```

### 11.2 Data Processing Flow
1. Resample to 60 minutes
2. Calculate 14-period RSI on resampled data
3. Merge back, forward-fill
4. Calculate bull/bear flag
5. Calculate standard 14-period RSI on 5-minute data
6. Generate signals

---

## 12. Live Application Advice

### 12.1 Backtesting vs. Live Gap
Author warns: "Backtest looks better than live." Causes:
- Backtest can't simulate slippage
- Assumes instant fill at signal price
- Can't model extreme liquidity crunches

### 12.2 Capital Management
- Per-pair position: 5-10% of total capital
- 5-10 pairs simultaneously
- Reserve emergency funds

### 12.3 Continuous Optimization
Author welcomes community improvements:
- Volatility-adjusted thresholds
- Trend strength filtering
- Volume confirmation
- ATR-based dynamic stops
- Multi-pair correlation consideration

---

## Summary

ObeliskRSI_v6_1 is a cleanly designed RSI dip-buying strategy. Its core highlights are the long-period RSI for trend classification and dynamic parameter switching, plus a carefully designed dynamic stop-loss mechanism.

Best for ranging markets with moderate-volatility pairs. Not suitable for sustained trending markets or ultra-stable coins. Thorough backtesting and paper trading are essential before going live.

---

*Strategy Author: Obelisk (brookmiles)*
*Document Date: 2026-03-27*
