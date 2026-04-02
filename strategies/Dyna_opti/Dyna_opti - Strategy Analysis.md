# Dyna_opti Strategy: In-Depth Analysis

> **Strategy Number**: #152 (152nd of 465 strategies)  
> **Strategy Type**: Bollinger Band Mean Reversion + Dynamic Take-Profit/Stoploss  
> **Timeframe**: 5 Minutes (5m) + 1 Hour Informational Layer

---

## I. Strategy Overview

**Dyna_opti** is a highly parameterized complex strategy developed by @werkkrew. It combines multiple technical indicators (Bollinger Bands, RMI, ATR, SSL Channel, etc.) and implements dynamic take-profit and custom stoploss mechanisms.

### Key Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 main buy condition + informational layer protection |
| **Sell Conditions** | Dynamic ROI + custom stoploss |
| **Protection** | 2 sets of buy protection parameters (informational layer filtering) |
| **Timeframe** | 5 minutes (main) + 1 hour (informational layer) |
| **Dependencies** | TA-Lib, technical, numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.18724,    # Immediate exit: 18.72% profit
    "20": 0.04751,   # After 20 minutes: 4.75% profit
    "30": 0.02393,   # After 30 minutes: 2.39% profit
    "72": 0          # After 72 minutes: break-even exit
}

# Stoploss Settings
stoploss = -0.28819  # -28.82% hard stoploss

# Dynamic ROI Configuration
use_dynamic_roi = True
droi_trend_type = 'any'           # Any of RMI/SSL/Candle trend
droi_pullback = False             # Whether pullback follows ROI table
droi_pullback_amount = 0.015     # Pullback threshold
```

### 2.2 Custom Stoploss Configuration

```python
use_custom_stoploss = True
cstp_threshold = -0.05           # Activates when profit < -5%
cstp_bail_how = 'time'            # Time / ROC / any method
cstp_bail_time = 961              # Force exit after 961 minutes
cstp_bail_roc = -0.018            # Exit when ROC < -1.8%
```

---

## III. Entry Conditions Details

### 3.1 Informational Layer Protection Mechanism

The strategy uses the 1-hour timeframe as an informational layer with two layers of protection:

```python
# Upper boundary protection
if inf_guard == 'upper' or 'both':
    conditions.append(
        close <= 3d_low + inf_pct_adr_top * adr
    )

# Lower boundary protection
if inf_guard == 'lower' or 'both':
    conditions.append(
        close >= 3d_low + inf_pct_adr_bot * adr
    )
```

### 3.2 Core Buy Condition (BinHV45 Strategy)

```python
# Bollinger Band breakout buy
conditions.append(
    bb_lowerband.shift() > 0 &                          # Previous candle has lower band
    bbdelta > close * bbdelta_close &                   # Bollinger band width sufficient
    closedelta > close * closedelta_close &             # Close price change sufficient
    tail < bbdelta * tail_bbdelta &                    # Lower wick short
    close < bb_lowerband.shift() &                     # Close price breaks below lower band
    close <= close.shift()                             # Close not above previous candle
)
```

---

## IV. Exit Conditions Details

### 4.1 Dynamic ROI System

The strategy uses `min_roi_reached_dynamic` for dynamic take-profit:

| Trend Type | Trigger Condition | ROI Value |
|-----------|-------------------|-----------|
| RMI Trend | RMI rising count >= 3 | 100% (no exit) |
| SSL Trend | SSL channel upward | 100% (no exit) |
| Candle Trend | 3+ consecutive bullish candles | 100% (no exit) |

### 4.2 Custom Stoploss Logic

```python
def custom_stoploss(...):
    if current_profit < cstp_threshold:     # Profit < -5%
        if cstp_bail_how == 'time':        # Time-based
            if trade_dur > cstp_bail_time: # Exceeds 961 minutes
                return 0.001               # Force exit
        if cstp_bail_how == 'roc':         # ROC-based
            if sroc <= cstp_bail_roc:      # ROC < -1.8%
                return 0.001
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Category | Indicator | Parameters | Purpose |
|----------|-----------|------------|---------|
| **Volatility** | Bollinger Bands | 12 period, 2x std dev | Price boundaries |
| **Momentum** | RMI | 24/21/8 periods | Momentum judgment |
| **Trend** | SSL-ATR | 21 period | Trend direction |
| **Volatility** | ATR | 24 period | Volatility |
| **Momentum** | SROC | 21/13/21 periods | Rate of change |

### 5.2 Custom Indicators

- **MA Streak**: Number of consecutive bullish/bearish candles
- **Percent Change Channel (PCC)**: Percentage change channel
- **Momentum Pinball**: ROC-based RSI

---

## VI. Risk Management Features

### 6.1 Multi-Layer Protection Mechanism

1. **Informational layer protection**: 1-hour timeframe ADR protection
2. **Dynamic ROI**: Adjusts take-profit based on trend strength
3. **Custom stoploss**: Dual protection based on time and momentum
4. **Generous hard stoploss**: -28.82% allows ample volatility room

### 6.2 Trend Judgment

The strategy uses three trend judgment methods:
- RMI momentum indicator
- SSL channel direction
- Candle consecutive rise/fall

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Highly parameterized**: Every parameter is optimizable
2. **Dynamic take-profit**: Adjusts exit strategy based on trend strength
3. **Multi-layer protection**: Informational layer + trend judgment + take-profit/stoploss
4. **Rich indicators**: Integration of more than ten technical indicators

### ⚠️ Cons

1. **Extremely complex**: Code exceeds 1000 lines
2. **Many parameters**: Prone to overfitting
3. **High computational load**: Demanding on hardware

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Config | Notes |
|-------------------|-------------------|-------|
| **Trending markets** | Enable dynamic ROI | Let profits run during trends |
| **High volatility** | Keep default | Generous stoploss suits high volatility |
| **Oscillating market** | Lower ROI thresholds | Reduce trend protection |

---

## IX. Applicable Market Environments in Detail

### 9.1 Core Strategy Logic

- **Bollinger Band breakout**: Buy when price breaks below the lower band
- **Trend protection**: Use RMI/SSL to judge trends
- **Dynamic exit**: Let profits run when trend continues, exit promptly when trend reverses

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---:|:---|
| 📈 Trending up | ★★★★★ | Dynamic ROI lets profits run |
| 🔄 Wide-range oscillation | ★★★★☆ | Bollinger band breakout effective in ranges |
| 📉 One-way down | ★★☆☆☆ | Trend protection may fail |
| ⚡️ Extreme consolidation | ★★★☆☆ | Complex calculation, mediocre effect |

---

## X. Important Notes: The Cost of Complexity

### 10.1 Learning Curve

The strategy code exceeds 1000 lines with extensive custom functions and complex logic. It is recommended to first understand the core indicator principles.

### 10.2 Hardware Requirements

The strategy has a massive computational load:

| Number of Pairs | Min RAM | Recommended RAM |
|----------------|---------|-----------------|
| 20-40 pairs | 2GB | 4GB |
| 40-80 pairs | 4GB | 8GB |

---

## XI. Summary

**Dyna_opti** is a highly complex advanced strategy suitable for experienced quantitative traders. Its core value lies in:

1. **Dynamic take-profit**: Intelligently adjusts exits based on trend strength
2. **Multi-layer protection**: Informational layer + trend judgment + take-profit/stoploss
3. **Highly customizable**: Every parameter is optimizable

**Recommendation**: Use only after fully understanding the strategy logic. Prevent overfitting.
