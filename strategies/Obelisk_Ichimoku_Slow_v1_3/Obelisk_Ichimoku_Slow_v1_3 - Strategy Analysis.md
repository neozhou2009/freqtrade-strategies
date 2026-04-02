# Obelisk_Ichimoku_Slow_v1_3 Strategy Analysis

## Table of Contents

1. [Strategy Overview and Design Philosophy](#1-strategy-overview-and-design-philosophy)
2. [Core Technical Indicators](#2-core-technical-indicators)
3. [Ichimoku Cloud System](#3-ichimoku-cloud-system)
4. [SSL Channel Confirmation](#4-ssl-channel-confirmation)
5. [EMA Trend Filter](#5-ema-trend-filter)
6. [Elder Force Index](#6-elder-force-index)
7. [Entry Signal Logic](#7-entry-signal-logic)
8. [Exit Signal Logic](#8-exit-signal-logic)
9. [Risk Management](#9-risk-management)
10. [Backtesting Configuration](#10-backtesting-configuration)
11. [Live Application Guide](#11-live-application-guide)

---

## 1. Strategy Overview and Design Philosophy

### 1.1 Strategy Positioning

Obelisk_Ichimoku_Slow_v1_3 is a **medium-to-long-term trend-following** strategy. The "Slow" in its name explicitly signals: this is not a high-frequency scalping strategy, but a **buy-and-hold-a-rising-trend** system.

From the author's code comments: "The purpose of this strategy is to buy and hold an uptrend for as long as possible."

### 1.2 Version Evolution

v1.3 improves on v1.2:
- **Added EMA entry guard**: EMA50 and EMA200 filter, improving trend validity confirmation
- **Removed cloud-top exit**: v1.2's price-breaking-cloud-top exit was too sensitive, removed to allow holding through pullbacks

Goal: "improve returns without significantly increasing drawdown."

### 1.3 Core Design Philosophy

- **Trend is king**: All logic serves trend following. Filters aggressively remove noise.
- **Multi-dimensional confirmation**: Four independent systems (Ichimoku, SSL, EMA, EFI) cross-verify signals.
- **Patience in holding**: No aggressive profit targets or tight trailing stops. Let winners run.
- **"Cloud as boundary"**: Ichimoku Cloud defines the trading zone.

---

## 2. Core Technical Indicators

### 2.1 Four-Layer Indicator Architecture

| Indicator | Verifies | Weight |
|-----------|----------|--------|
| Ichimoku Cloud | Trend direction & strength | 4 (highest) |
| SSL Channel | Price momentum & position | 3 |
| EMA Dual | Medium-term trend confirmation | 2 |
| Elder Force Index | Capital inflow strength | 1 |

### 2.2 Timeframe

**1-hour** as primary timeframe.
`startup_candle_count = 180` — needs 180 candles (7.5 days) for Ichimoku stability.

⚠️ Author warns: "Ichimoku is a long-period indicator — if you reduce startup candles, results in the first week will be unstable."

---

## 3. Ichimoku Cloud System

### 3.1 Custom Parameters

| Component | Standard | Strategy | Purpose |
|-----------|----------|----------|---------|
| Conversion Line | 9 | 20 | More stable signals |
| Base Line | 26 | 60 | Adapted to hourly |
| Lagging Span | 52 | 120 | More stability |
| Displacement | 26 | 30 | Fine-tuned |

Larger parameters = smoother but slower signals.

### 3.2 Cloud Trend Judgment

```python
dataframe['ichimoku_ok'] = (
    (tenkan_sen > kijun_sen)           # Conversion > Base
    & (close > cloud_top)               # Price above cloud
    & (future_green > 0)                # Future cloud is green
    & (chikou_high > 0)                 # Lagging span confirms
).astype('int') * 4
```

### 3.3 Lagging Span Technical Note

The code has a marked "DANGER ZONE" section — Lagging Span is normally shifted backward. The code carefully shifts it forward to properly align signals. The comment clarifies this is not "future data leakage" — it's using the Ichimoku's inherent forward projection.

---

## 4. SSL Channel Confirmation

### 4.1 SSL ATR Formula

```python
def ssl_atr(dataframe, length=7):
    smaHigh = high.rolling(length).mean() + ATR
    smaLow = low.rolling(length).mean() - ATR
    hlv = np.where(close > smaHigh, 1, np.where(close < smaLow, -1, np.NAN))
    sslDown = np.where(hlv < 0, smaHigh, smaLow)
    sslUp = np.where(hlv < 0, smaLow, smaHigh)
    return sslDown, sslUp
```

### 4.2 SSL in Strategy

```python
ssl_ok = (ssl_up > ssl_down).astype('int') * 3
```

Weight 3 — second most important confirmation. SSL confirms momentum direction.

**Entry timing role**: Strategy requires price below SSL_up — waits for pullback to enter, not chasing.

---

## 5. EMA Trend Filter

### 5.1 Dual EMA Configuration (v1.3 Addition)

```python
ema_ok = ((close > ema50) & (ema50 > ema200)).astype('int') * 2
```

- EMA50 > EMA200 confirms medium-term uptrend
- Close > EMA50 confirms current price strength

### 5.2 Weight Analysis

Weight 2 — between EFI (1) and SSL (3). Confirms but does not independently trigger entries.

---

## 6. Elder Force Index

```python
dataframe['efi_base'] = ((close - close.shift()) * volume)
dataframe['efi'] = ta.EMA(dataframe['efi_base'], 13)
```

EFI > 0 = price rising with volume = real buying. EFI < 0 = price falling with volume = real selling.

Used as necessary condition for entry: EFI > 0.

---

## 7. Entry Signal Logic

### 7.1 Trend State (trending)

```python
dataframe['trend_pulse'] = (
    (ichimoku_ok > 0) & (ssl_ok > 0) & (ema_ok > 0)
).astype('int') * 2

dataframe.loc[trend_pulse > 0, 'trending'] = 3
dataframe.loc[trend_over > 0, 'trending'] = 0
dataframe['trending'].fillna(method='ffill')
```

Once all three confirm, `trending` = 3. Forward-filled to maintain state until trend ends.

### 7.2 Entry Timing (entry_ok)

```python
dataframe['entry_ok'] = (
    (efi_ok > 0)              # Real money flowing in
    & (open < ssl_up)         # During pullback
    & (close < ssl_up)        # Didn't chase
).astype('int') * 1
```

Requires: positive EFI + both open and close below SSL_up (pullback entry, not breakout chasing).

### 7.3 Final Entry Condition

```python
dataframe.loc[
    (trending > 0) & (entry_ok > 0) & (date.dt.minute == 0),
    'buy'
] = 1
```

Also requires `minute == 0` (hour boundary) — prevents duplicate signals within the same hour.

---

## 8. Exit Signal Logic

### 8.1 Only SSL Trend Reversal

```python
dataframe['trend_over'] = (ssl_ok == 0).astype('int') * 1
```

The **only exit trigger** is SSL channel flipping bearish. Nothing else.

### 8.2 Why This Simplicity?

- **Avoids over-sensitivity**: Ichimoku signals are lagging; using them for exits would be too slow
- **Simplifies judgment**: One clear rule vs. multiple competing conditions
- **Allows pullback holding**: v1.3's removal of cloud-top exit specifically prevents exits during normal pullbacks

### 8.3 Sell Signal

```python
dataframe.loc[
    (trending == 0) & (date.dt.minute == 0),
    'sell'
] = 1
```

---

## 9. Risk Management

### 9.1 Stop-Loss: -10%

```python
stoploss = -0.10
```

Author's comment: "Setting a stop-loss for this strategy doesn't make much sense since it will buy back into the trend on the next opportunity unless the trend has ended, in which case it will sell anyway."

Meaning: if the stop-loss triggers but the trend is still up, the exit signal will immediately re-trigger a buy — so the stop-loss is more psychological protection than primary exit mechanism.

### 9.2 Trailing Stop

Parameters exist but author says "not actually used" — kept as backup:

```python
trailing_stop_positive_offset = 0.04  # 4% profit activates
trailing_stop_positive = 0.005       # Lock 0.5% profit
```

### 9.3 ROI Configuration

```python
minimal_roi = {
    "0": 0.10,   # 10%
    "60": 0.072,  # 7.2%
    "120": 0.049, # 4.9%
    "240": 0.02,  # 2%
    "360": 0      # Any profit acceptable after 360 min
}
```

"Profit decay" mechanism — encourages exits if trend hasn't delivered new gains after extended holding.

### 9.4 ⚠️ Important Warning

```
WARNING: Do not use stoploss_on_exchange
```
If the bot fails to place a stop-loss order at the exchange, it may trigger an emergency sell — potentially causing unexpected losses.

---

## 10. Backtesting Configuration

### 10.1 Recommended Pairlist

```json
{
    "method": "VolumePairList", "number_assets": 25,
    "sort_key": "quoteVolume", "refresh_period": 1800
},
{"method": "AgeFilter", "min_days_listed": 10},
{"method": "PrecisionFilter"},
{"method": "PriceFilter", "low_price_ratio": 0.001},
{"method": "RangeStabilityFilter", "lookback_days": 3,
    "min_rate_of_change": 0.1, "refresh_period": 1440}
```

Selects top 25 pairs by volume, excludes new listings (<10 days), filters by price stability.

---

## 11. Live Application Guide

### 11.1 Timing Selection

Author stresses: "start timing is important." Starting at market peaks = buying dying trends.

Best starting points:
- After extended consolidation/recovery
- During overall crypto market upcycle
- NOT during FOMO frenzies

### 11.2 Position Sizing

- Per-trade risk: 1-2% of total capital
- Stop-loss is 10% → per-trade position ≈ 10-20% of capital
- Run multiple pairs for diversification

### 11.3 Monitoring

- Watch `trending` state changes
- Don't manually intervene in exits
- Check for exchange API issues causing emergency sells

---

## Summary

Obelisk_Ichimoku_Slow_v1_3 is a meticulously designed trend-following system. Its core strengths are multi-dimensional indicator confirmation, pullback entry timing, and simplified exit logic. It embodies "buy into rising trends and hold them."

Best suited for: trend-following believers, medium-to-long-term investors, those who can accept moderate drawdowns. Not for: range-bound market traders, short-term scalpers, or those needing precise entry/exit timing.

As the author states: this is a "buy and hold" strategy, not a quick in-and-out system. Only embrace this philosophy to see its intended results.

---

*Strategy Version: Obelisk_Ichimoku_Slow_v1_3*
*Author: Obelisk*
*Document Date: March 27, 2026*
