# Bandtastic Strategy Analysis

> **Strategy Number**: #49
> **Strategy Type**: Multi-Level Bollinger Bands + Configurable Indicator Filters
> **Timeframe**: 15 minutes (15m)

---

## I. Strategy Overview

Bandtastic is a **highly configurable** Bollinger Band trading strategy — achieves extremely strong adaptability through Hyperopt parameter optimization. Strategy's core design philosophy is to fully utilize multiple Bollinger Band levels (1-4 standard deviations) to capture different levels of price extreme positions — and optionally filter signals through technical indicators (RSI — MFI — EMA).

Different from simple Bollinger Band breakout strategies — Bandtastic provides **multi-layer protection mechanisms**: not only can choose price level to trigger signals — but also can add RSI — MFI or EMA as secondary confirmation conditions. This design greatly reduces probability of false signals — improves signal quality.

Strategy uses 15-minute timeframe — balances signal frequency and noise control — suitable for quantitative traders with certain experience.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Price touches BB lower band (1-4x optional) + optional RSI/MFI/EMA filter |
| **Exit Conditions** | Price touches BB upper band (1-4x optional) + optional RSI/MFI/EMA filter |
| **Protection** | Fixed stoploss -34.5% — trailing stop enabled |
| **Timeframe** | 15m |
| **Dependencies** | technical, talib |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
minimal_roi = {
    "0": 0.162,    # Immediate take-profit 16.2%
    "69": 0.097,   # 9.7% after 69 candles
    "229": 0.061,  # 6.1% after 229 candles
    "566": 0       # Zero after 566 candles
}

stoploss = -0.345   # Stoploss -34.5%!

# Trailing stoploss configuration
trailing_stop = True
trailing_stop_positive = 0.01      # Positive trailing distance 1%
trailing_stop_positive_offset = 0.058  # Trigger offset 5.8%
```

**Configuration Logic Analysis**:

- **minimal_roi Design**: Strategy adopts aggressive high take-profit design — initial take-profit as high as 16.2%. This target quite bold — indicates strategy pursues complete profits in large trend markets. As time extends — take-profit target gradually decreases: drops to 9.7% after 69 candles (about 1.7 days) — to 6.1% after 229 candles (about 5.7 days) — completely relies on trailing stoploss after 566 candles (about 14 days).

- **stoploss -34.5%**: This is a very high stoploss amplitude — reflects strategy designer's tolerance for large volatility. Combined with 16.2% initial take-profit — profit/loss ratio about 0.47:1 — means strategy needs to win in over 68% of trades to break even. This high stoploss design based on following assumption: after buying at extreme Bollinger Band positions (especially 3-4 standard deviations) — price has high probability of significant rebound.

- **trailing_stop Enabled**: Trailing stoploss activates after profit exceeds 5.8% — stoploss line moves up to lock 1% profit. This provides additional protection mechanism.

---

## III. Entry Conditions Details

### 3.1 Configurable Bollinger Band Level Triggers

Strategy provides four levels of Bollinger Band lower bands as buy trigger points:

| Level | Parameter | Meaning |
|-------|-----------|---------|
| bb_lower1 | Price < 1 standard deviation lower band | Price touches normal volatility lower band |
| bb_lower2 | Price < 2 standard deviations lower band | Price touches extended volatility lower band |
| bb_lower3 | Price < 3 standard deviations lower band | Price touches extreme lower band |
| bb_lower4 | Price < 4 standard deviations lower band | Price touches rare extreme |

**Level Selection Logic**:
- Higher level = fewer signals — but higher signal reliability
- 1-2 standard deviations suitable for normal markets — 3-4 suitable for high volatility markets
- Usually recommend starting testing from 2 standard deviations

### 3.2 Optional Indicator Guards

Strategy provides three optional technical indicator filters:

**RSI Filter**:
```python
rsi < buy_rsi  # Default value usually between 20-35
```
RSI filter ensures finding buy opportunities in oversold region — avoids buying too early in downtrend.

**MFI Filter**:
```python
mfi < buy_mfi  # Default value usually between 20-35
```
MFI (Money Flow Index) filter ensures buying when capital outflow slowing — increases signal quality.

**EMA Trend Filter**:
```python
ema_fast > ema_slow  # Requires short-term EMA > long-term EMA when buying
```
EMA filter ensures buying in uptrend — avoids counter-trend trading.

---

## IV. Exit Conditions Details

### 4.1 Exit Logic

Strategy exits via:
- Price touching BB upper band (configurable level)
- ROI table for take-profit
- Trailing stoploss for profit protection
- Fixed stoploss for loss control

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator | Parameters | Usage |
|-----------|------------|-------|
| Bollinger Bands | Multiple (1-4 stds) | Identify extreme positions |
| RSI | 14 (optional) | Oversold/overbought filter |
| MFI | 14 (optional) | Money flow filter |
| EMA | Multiple (optional) | Trend filter |

---

## VI. Risk Management Features

### 6.1 Risk-Return Characteristics

| Dimension | Assessment |
|-----------|------------|
| Maximum Theoretical Loss | -34.5% (fixed stoploss) |
| Maximum Theoretical Profit | Unlimited (trailing stoploss) |
| Expected Profit/Loss Ratio | About 0.5:1 |
| Signal Frequency | Configurable (depends on BB level) |

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Highly configurable**: Many parameters to optimize
2. **Multi-level BB**: Can capture different extremes
3. **Optional filters**: Can add RSI/MFI/EMA confirmation
4. **Adaptable**: Can tune for different markets
5. **Hyperopt ready**: Designed for optimization

### ⚠️ Cons

1. **Very high stoploss**: 34.5% dangerous
2. **Complex configuration**: Many parameters to tune
3. **Requires optimization**: Not plug-and-play
4. **High win rate needed**: 68%+ to break even
5. **May overfit**: Many parameters = overfit risk

---

## VIII. Summary

Bandtastic is a **highly configurable multi-level Bollinger Band** strategy. Core value lies in **flexibility and adaptability**. Strategy suitable for experienced traders who can optimize parameters and want to capture extreme price movements.

---

*This document is based on strategy code*
