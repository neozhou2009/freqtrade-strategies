# BbRoi Strategy Analysis

> **Strategy Number**: #50
> **Strategy Type**: Bollinger Band Middle Rail Breakout + EMA Trend Confirmation
> **Timeframe**: 15 minutes (15m)

---

## I. Strategy Overview

BbRoi is a **trend confirmation** Bollinger Band strategy — core design philosophy is to find buy opportunities in middle-to-upper Bollinger Band zone — and confirm trend already formed through EMA bullish arrangement. Strategy doesn't pursue buying at lowest point — but pursues following trend after trend started.

Strategy's entry conditions require price between Bollinger Band middle and upper rails (strong zone) — while requiring EMA to form bullish arrangement (short-term EMA > long-term EMA) — this ensures when buying market already in clear uptrend. Exit conditions triggered through RSI overbought or falling below 97% of Bollinger Band middle rail.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | BB middle < Price < BB upper + EMA bullish arrangement |
| **Exit Conditions** | RSI > 75 or fall below 97% of BB middle rail |
| **Protection** | Fixed stoploss -23.7% — trailing stop enabled |
| **Timeframe** | 15m |
| **Dependencies** | technical, talib |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# Return on investment settings
minimal_roi = {
    "0": 0.17552,    # Immediate take-profit 17.6%
    "53": 0.11466,   # 11.5% after 53 candles
    "226": 0.06134,  # 6.1% after 226 candles
    "400": 0         # Zero after 400 candles
}

stoploss = -0.23701   # Stoploss -23.7%!

# Trailing stoploss configuration
trailing_stop = True
trailing_stop_positive = 0.01007      # Positive trailing distance 1%
trailing_stop_positive_offset = 0.01821  # Trigger offset 1.8%
trailing_only_offset_is_reached = True  # Only activate when offset reached
```

**Configuration Logic Analysis**:

- **minimal_roi Design**: Strategy adopts decreasing ROI design — initial take-profit 17.6% — this is relatively aggressive target. As holding time increases — take-profit target gradually decreases: drops to 11.5% after 53 candles (about 13 hours) — to 6.1% after 226 candles (about 56 hours/2 days) — completely relies on trailing stoploss after 400 candles (about 100 hours/4 days).

- **stoploss -23.7%**: This is a relatively high stoploss amplitude — reflects strategy designer's tolerance for trend markets. Combined with 17.6% initial take-profit — profit/loss ratio about 0.74:1. This design based on following assumption: in trend markets — may exist relatively deep pullbacks — need give enough volatility space.

- **trailing_stop Configuration**: Strategy uses relatively conservative trailing stoploss configuration — only activates after profit exceeds 1.8% — locks 1% profit after activation. This conservative design aims to protect profits — but may cause exiting too early in large trend markets.

---

## III. Entry Conditions Details

### 3.1 Complete Entry Conditions

```python
# 1. Price between BB middle and upper rails
(dataframe["close"] > dataframe["bb_middleband"]) &
(dataframe["close"] < dataframe["bb_upperband"]) &

# 2. Price > short-term and long-term EMA
(dataframe["close"] > dataframe["ema9"]) &
(dataframe["close"] > dataframe["ema200"]) &

# 3. EMA bullish arrangement
(dataframe["ema20"] > dataframe["ema200"])
```

**Condition-by-Condition Analysis**:

**Condition One: Price Between BB Middle and Upper Rails**

```python
(dataframe["close"] > dataframe["bb_middleband"]) &
(dataframe["close"] < dataframe["bb_upperband"])
```

- Bollinger Band middle rail is 20-day moving average — represents medium-term market cost
- Bollinger Band upper rail represents price volatility upper boundary
- Price between both indicates market in relatively strong state
- Don't buy at lowest — but also don't buy at highest

**Condition Two: Price Above EMA**

```python
(dataframe["close"] > dataframe["ema9"]) &
(dataframe["close"] > dataframe["ema200"])
```

- EMA9 is short-term average — represents recent market consensus
- EMA200 is long-term average — represents long-term market trend
- Price above both indicates market in relatively strong state

**Condition Three: EMA Bullish Arrangement**

```python
(dataframe["ema20"] > dataframe["ema200"])
```

- EMA20 above EMA200 indicates medium-term trend above long-term trend
- This is trend confirmation — ensures buying in uptrend
- Avoids counter-trend trading

---

## IV. Exit Conditions Details

### 4.1 Exit Conditions

Strategy exits when:
- RSI > 75 (overbought)
- Or price falls below 97% of BB middle rail (trend weakening)

### 4.2 Take-Profit Strategy

| Holding Time | Take-Profit Target | Design Intent |
|-------------|-------------------|---------------|
| 0 candles | 17.6% | Capture initial trend move |
| About 13 hours | 11.5% | Medium-term target |
| About 2 days | 6.1% | Prevent profit giveback |
| About 4 days+ | 0% | Rely on trailing stoploss |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator | Parameters | Usage |
|-----------|------------|-------|
| Bollinger Bands | 20, 2 | Identify strong zone |
| EMA | 9/20/200 | Trend confirmation |
| RSI | 14 | Overbought exit |

### 5.2 Trend Confirmation Logic

Strategy uses multiple EMAs for trend confirmation:
- EMA9: Short-term momentum
- EMA20: Medium-term trend
- EMA200: Long-term trend
- All must align bullishly for entry

---

## VI. Risk Management Features

### 6.1 Risk-Return Characteristics

| Dimension | Assessment |
|-----------|------------|
| Maximum Theoretical Loss | -23.7% (fixed stoploss) |
| Maximum Theoretical Profit | Unlimited (trailing stoploss) |
| Expected Profit/Loss Ratio | About 0.75:1 |
| Signal Frequency | Medium (requires trend confirmation) |

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Trend confirmation**: Multiple EMA confirmations
2. **Strong zone entry**: Buys in strength — not weakness
3. **Clear exit rules**: RSI overbought or trend break
4. **Avoids counter-trend**: EMA filter prevents逆势
5. **Defined risk**: Clear stoploss level

### ⚠️ Cons

1. **High stoploss**: 23.7% may cause significant losses
2. **May miss early moves**: Waits for trend confirmation
3. **Conservative trailing**: May exit too early
4. **Complex conditions**: Multiple confirmations may miss opportunities
5. **Trend dependent**: Performs poorly in ranging markets

---

## VIII. Summary

BbRoi is a **trend-confirmed Bollinger Band** strategy. Core value lies in **buying in strong zone with trend confirmation**. Strategy suitable for traders who want to follow established trends rather than catching bottoms.

---

*This document is based on strategy code*
