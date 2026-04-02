# Obelisk_Ichimoku_ZEMA_v1 Strategy Analysis

## Table of Contents

1. [Strategy Overview](#1-strategy-overview)
2. [Theoretical Foundations](#2-theoretical-foundations)
3. [Indicator System](#3-indicator-system)
4. [Signal Generation Logic](#4-signal-generation-logic)
5. [Risk Management Mechanisms](#5-risk-management-mechanisms)
6. [Parameter Configuration](#6-parameter-configuration)
7. [Timeframe Design](#7-timeframe-design)
8. [Data Projection and Displacement](#8-data-projection-and-displacement)
9. [Trend Judgment System](#9-trend-judgment-system)
10. [Backtesting and Optimization](#10-backtesting-and-optimization)
11. [Strategy Assessment](#11-strategy-assessment)

---

## 1. Strategy Overview

### 1.1 Strategy Positioning

Obelisk_Ichimoku_ZEMA_v1 is an experimental (EXPERIMENTAL-tagged) crypto trading strategy by Obelisk. Its core design combines the classic Ichimoku Cloud with Zero Lag EMA (ZEMA) to build a trend-following system that captures mid-to-long-term trends and precisely times entries.

### 1.2 Core Features

- **Multi-dimensional trend confirmation**: Ichimoku Cloud (5 components) + SSL ATR → layered trend verification
- **Dynamic entry optimization**: ZEMA's zero-lag property enables early trend capture
- **Smart exit mechanism**: `confirm_trade_exit` overrides ROI exits during uptrends
- **High optimizability**: Four hyperparameters tunable via Freqtrade

### 1.3 Applicable Scenarios

Best for: clearly trending markets, high-liquidity mainstream pairs, medium-to-long-term positions.

⚠️ **Warning**: Marked "EXPERIMENTAL" — not fully validated in live trading.

---

## 2. Theoretical Foundations

### 2.1 Ichimoku Cloud Theory

Five components: Conversion Line (20), Base Line (60), Leading Span A, Leading Span B, Lagging Span (120). Displacement 30.

Custom parameters (vs. standard 9-26-52): More conservative, more stable signals.

### 2.2 Zero Lag EMA Theory

ZEMA removes inherent EMA lag through error compensation. Buy ZEMA (72 default) slower than sell ZEMA (51 default) — entering requires more confirmation; exiting is more responsive.

### 2.3 SSL ATR Theory

ATR-based channel: upper = low.avg + ATR, lower = high.avg - ATR. Auto-adapts to volatility — wider in volatile markets, narrower in calm.

---

## 3. Indicator System

### 3.1 Ichimoku Parameters (Custom)

| Component | Period | Displacement |
|-----------|--------|--------------|
| Conversion | 20 | 0 |
| Base | 60 | 0 |
| Lagging Span | 120 | 30 |

### 3.2 SSL ATR (Default Period 10)

```python
def ssl_atr(dataframe, length=7):
    smaHigh = high.rolling(length).mean() + ATR
    smaLow = low.rolling(length).mean() - ATR
    # price above/below channels determine hlv state
    # sslUp and sslDown swap based on hlv
```

### 3.3 ZEMA

Two ZEMA lines:
- `zema_buy`: multiplied by `low_offset` → entry trigger threshold
- `zema_sell`: multiplied by `high_offset` → exit trigger threshold

---

## 4. Signal Generation Logic

### 4.1 Buy Signal Conditions

Three simultaneous requirements:

**Condition 1: `ichimoku_valid > 0`**: All Ichimoku data computed (120+ candles).

**Condition 2: `bear_trending == 0`**: NOT in bearish state. Bearish defined as:
- Conversion < Base AND
- Close < Cloud Bottom AND
- Future cloud red AND
- Lagging Span below cloud bottom

**Condition 3: `close < zema_buy × low_offset`**: Price must be below ZEMA × offset (default ~1.004 → requires slightly lower price).

### 4.2 Sell Signal

```python
close > zema_sell × high_offset  # default: × 0.964
```

When price exceeds sell ZEMA threshold → sell.

### 4.3 Smart Exit Confirmation

```python
def confirm_trade_exit(...):
    if sell_reason == 'roi':
        if current_candle['trending'] > 0:
            return False  # Reject ROI exit, stay in uptrend
    return True
```

When the reason is ROI, check if still in an uptrend (`trending > 0`). If yes, refuse to exit — continue holding to capture more gains. Classic "let profits run."

---

## 5. Risk Management Mechanisms

### 5.1 ROI Configuration

| Minutes | ROI |
|---------|-----|
| 0 | 7.8% |
| 40 | 6.2% |
| 99 | 3.9% |
| 218 | 0% |

Time-decaying profit expectations — if not rising fast, gradually lower targets.

### 5.2 Stop-Loss: -29.4%

Very wide stop. Aligns with "only exit when trend ends" philosophy — give positions room to breathe.

### 5.3 Startup Requirements

`startup_candle_count = 500`: Needs 500 historical candles before producing valid signals.

---

## 6. Parameter Configuration

### 6.1 Optimizable Parameters

| Parameter | Default | Range | Space |
|-----------|---------|-------|-------|
| low_offset | 1.004 | 0.80-1.20 | buy |
| zema_len_buy | 72 | 30-90 | buy |
| high_offset | 0.964 | 0.80-1.20 | sell |
| zema_len_sell | 51 | 30-90 | sell |

⚠️ Note: The defaults appear swapped relative to parameter names (low_offset=1.004 vs. high_offset=0.964), suggesting the offset logic may be inverted from naming convention.

---

## 7. Timeframe Design

### 7.1 Dual Timeframe

- **Main**: 5m — actual trade execution
- **Informative**: 1h — trend judgment

### 7.2 Assertion

```python
assert timeframe == '5m'  # Strategy locked to 5-minute chart
```

Strategy enforces 5m timeframe only.

---

## 8. Data Projection and Displacement

### 8.1 "Future" Cloud

`future_green` and `future_red` use the current-computed Leading Spans (which are inherently forward-projected) — not actual future data. The naming clarifies this is the "present-computed future cloud."

### 8.2 Lagging Span Handling

Lagging Span is normally plotted 30 periods behind. The strategy shifts it forward by displacement to align with current prices: `chikou_high = chikou_span.shift(displacement)`.

---

## 9. Trend Judgment System

### 9.1 Multi-Layer Trend Signals

Multiple independent trend channels:
- Bull: `trend_pulse → trending → trend_over`
- Bear: `bear_trend_pulse → bear_trending → bear_trend_over`

### 9.2 Trend State Forward Fill

```python
dataframe['trending'].fillna(method='ffill', inplace=True)
```

Once set to 3, stays 3 until `trend_over` resets to 0. State persists across candles.

### 9.3 Multi/Bear Symmetry

Bull and bear systems operate independently — when bull ends, bear can begin.

---

## 10. Backtesting and Optimization

### 10.1 Startup Data Requirement

Need ≥500 5m candles (~41.6 hours). Insufficient data = unreliable first-week signals.

### 10.2 Hyperopt Recommendations

```bash
freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --epochs 500 --spaces buy sell
```

### 10.3 Parameter Guidance by Market

| Condition | low_offset | high_offset | zema_len_buy | zema_len_sell |
|-----------|------------|-------------|---------------|----------------|
| High volatility | 0.95-0.98 | 1.02-1.05 | 40-60 | 40-60 |
| Low volatility | 0.98-1.02 | 1.00-1.03 | 60-80 | 50-70 |
| Clear trend | 1.00-1.05 | 0.98-1.02 | 70-90 | 40-60 |

---

## 11. Strategy Assessment

### 11.1 Strengths
- Solid theoretical foundation (Ichimoku is decades-tested)
- Multi-indicator synergy (Ichimoku + SSL + ZEMA)
- Strong trend capture ability
- Smart exit mechanism (overrides ROI in uptrends)
- Highly optimizable

### 11.2 Risks
- ⚠️ **EXPERIMENTAL**: Unvalidated in live trading
- Stop-loss very wide (-29.4%)
- Lagging Span/Leading Span "future" concept may confuse beginners
- Requires extensive startup data (500 candles)
- Must run on 5m timeframe only

### 11.3 Best For
- Trend-following believers
- Technical analysis researchers
- Quant developers seeking strategy templates
- Higher risk tolerance traders

### 11.4 Not For
- Beginners seeking plug-and-play
- Low risk tolerance
- Those wanting multi-timeframe flexibility

---

*Document Version: v1.0*
*Strategy: Obelisk_Ichimoku_ZEMA_v1*
*Last Updated: 2024*
