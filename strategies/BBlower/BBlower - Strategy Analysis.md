# BBlower Strategy Analysis

> **Strategy Number**: #47
> **Strategy Type**: Multi-Level Bollinger Bands + RSI Momentum Confirmation
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

BBlower is a **multi-level Bollinger Band combined with RSI momentum confirmation** strategy. Its core design philosophy is to find buy opportunities at extreme Bollinger Band positions — and confirm momentum has reversed through RSI continuous rise. Strategy uses multiple Bollinger Band groups (1-4 standard deviations) to capture different levels of oversold conditions — while requiring RSI to rise for 5 consecutive candles — ensuring momentum already strengthened when buying.

Strategy uses 5-minute timeframe — belongs to **intraday trading strategy**. Different from simple oversold rebound strategies — BBlower particularly emphasizes **momentum confirmation** — requires RSI continuous rise indicating downtrend already slowed — uptrend may be starting.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | TEMA crosses above BB lower band + RSI rises 5 consecutive candles + RSI < 50 |
| **Exit Conditions** | Relies on ROI and trailing stoploss |
| **Protection** | Fixed stoploss -13.9% — trailing stop enabled |
| **Timeframe** | 5m |
| **Dependencies** | talib, technical |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# Return on investment settings
minimal_roi = {
    "0": 0.32477,    # Immediate take-profit 32.5%
    "220": 0.13561,  # 13.6% after 220 candles
    "962": 0.10732,  # 10.7% after 962 candles
    "2115": 0        # Zero after that
}

stoploss = -0.13912   # Stoploss -13.9%

# Trailing stoploss configuration
trailing_stop = True
trailing_stop_positive = 0.29846     # Positive trailing distance 29.8%!
trailing_stop_positive_offset = 0.30425  # Trigger offset 30.4%
```

**Configuration Logic Analysis**:

- **minimal_roi Design**: Strategy adopts very aggressive take-profit design — initial take-profit as high as 32.5%! This target quite bold — indicates strategy pursues large trend markets. As time extends — take-profit target gradually decreases: drops to 13.6% after 220 candles (about 18 hours) — to 10.7% after 962 candles (about 80 hours/3 days) — completely relies on trailing stoploss after 2115 candles (about 176 hours/7 days).

- **stoploss -13.9%**: 13.9% stoploss amplitude relatively moderate for 5-minute strategy. Design logic: after buying at oversold positions — price has rebound space — but need give enough volatility room.

- **trailing_stop Aggressive Configuration**: This is a very aggressive trailing stoploss configuration! Positive trailing distance 29.8% — trigger offset 30.4%. This means only activates trailing stoploss after profit exceeds 30.4% — locks 29.8% profit after activation. This design allows strategy to continue holding in large trend markets.

---

## III. Entry Conditions Details

### 3.1 Complete Entry Conditions

```python
dataframe.loc[
    (
        (RSI > RSI.shift(1)) &
        (RSI.shift(1) > RSI.shift(2)) &
        (RSI.shift(2) > RSI.shift(3)) &
        (RSI.shift(3) > RSI.shift(4)) &
        (RSI < 50) &
        qtpylib.crossed_above(TEMA, bb_lowerbandTA1)
    ),
    'entry'] = 1
```

**Condition-by-Condition Analysis**:

**Conditions One to Five: RSI Rises 5 Consecutive Candles**

```python
RSI > RSI.shift(1)  # Current RSI > 1 candle ago
RSI.shift(1) > RSI.shift(2)  # 1 candle ago > 2 candles ago
RSI.shift(2) > RSI.shift(3)
RSI.shift(3) > RSI.shift(4)
```

- This is strategy's core innovation point: requires RSI to rise 5 consecutive candles
- This indicates selling pressure gradually weakening — buying power accumulating
- Continuous 5-candle rise is a strong momentum reversal signal

**Condition Six: RSI < 50**

```python
RSI < 50
```

- Requires RSI still below neutral zone (below 50)
- This ensures when buying market still in relatively weak state — won't chase highs
- Simultaneously excludes situations where RSI already rebounded to high positions

**Condition Seven: TEMA Crosses Above Bollinger Band Lower Band**

```python
qtpylib.crossed_above(TEMA, bb_lowerbandTA1)
```

- TEMA (Triple Exponential Moving Average) crosses above Bollinger Band lower band
- This is price action confirmation — indicates price starting to rebound from extreme positions

---

## IV. Exit Conditions Details

### 4.1 Exit Logic

Strategy doesn't have explicit exit conditions — relies on:
- ROI table for take-profit
- Trailing stoploss for profit protection
- Fixed stoploss for loss control

### 4.2 Take-Profit Strategy

| Holding Time | Take-Profit Target | Design Intent |
|-------------|-------------------|---------------|
| 0 candles | 32.5% | Capture large trend moves |
| About 18 hours | 13.6% | Medium-term target |
| About 3 days | 10.7% | Reduced target |
| About 7 days+ | 0% | Rely on trailing stoploss |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator | Parameters | Usage |
|-----------|------------|-------|
| RSI | 14 | Momentum confirmation |
| TEMA | 9 | Price action signal |
| Bollinger Bands | Multiple (1-4 stds) | Identify extreme positions |

### 5.2 RSI Continuous Rise Logic

Strategy's unique feature is requiring RSI to rise 5 consecutive candles:
- Indicates momentum gradually strengthening
- Filters false oversold signals
- Provides early reversal confirmation

---

## VI. Risk Management Features

### 6.1 Risk-Return Characteristics

| Dimension | Assessment |
|-----------|------------|
| Maximum Theoretical Loss | -13.9% (fixed stoploss) |
| Maximum Theoretical Profit | Unlimited (trailing stoploss) |
| Expected Profit/Loss Ratio | About 2:1+ |
| Signal Frequency | Low (requires multiple confirmations) |

### 6.2 Risk Control Mechanisms

| Mechanism | Description | Evaluation |
|-----------|-------------|------------|
| Fixed Stoploss | -13.9% | Moderate — gives rebound space |
| Aggressive Trailing | Activates after 30.4% | Allows profits to run |
| RSI Confirmation | 5-candle rise | Filters false signals |

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Momentum confirmation**: RSI 5-candle rise filters false signals
2. **Multi-level BB**: Can capture different extreme levels
3. **High profit potential**: 32.5% initial take-profit
4. **Clear entry logic**: Conditions well defined
5. **Aggressive trailing**: Allows capturing large trends

### ⚠️ Cons

1. **Complex conditions**: Multiple confirmations may miss opportunities
2. **High stoploss**: 13.9% may cause significant losses
3. **Low signal frequency**: Many conditions reduce signals
4. **Aggressive trailing**: 30.4% offset very high

---

## VIII. Summary

BBlower is a **momentum-confirmed oversold rebound** strategy. Its core value lies in **RSI continuous rise confirmation and multi-level Bollinger Bands**. Strategy suitable for traders who can wait for high-certainty signals and want to capture large trend moves.

---

*This document is based on strategy code*
