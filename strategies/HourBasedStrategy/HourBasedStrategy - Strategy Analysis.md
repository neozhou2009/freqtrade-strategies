# HourBasedStrategy Strategy: In-Depth Analysis

> **Strategy ID**: #198 (198th of 465 strategies)
> **Strategy Type**: Time Factor Strategy
> **Timeframe**: 1 Hour (1h)

---

## I. Strategy Overview

**HourBasedStrategy** is a quantitative trading strategy based on time factors. The core idea is to leverage market characteristic differences across trading sessions: enter during active sessions, exit during low-liquidity sessions. This design stems from the time patterns of cryptocurrency markets — volatility, liquidity, and trend persistence vary significantly across different trading sessions.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Within time window (4:00 - 24:00) + EMA trend confirmation |
| **Exit Conditions** | Specific session (21:00 - 22:00) + RSI reversal signal |
| **Protections** | Hard stop-loss -5% + Tiered ROI |
| **Timeframe** | 1 Hour |
| **Dependencies** | TA-Lib |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
minimal_roi = {
    "0": 0.528,    # Immediate exit: 52.8% profit
    "180": 0.113,  # After 3 hours: 11.3% profit
    "540": 0.089,  # After 9 hours: 8.9% profit
    "1440": 0      # After 1 day: 0% profit (break-even exit)
}

stoploss = -0.05    # -5% hard stop-loss
```

**Design Philosophy**:
- **Aggressive Primary ROI**: 52.8% immediate take-profit indicates strategy aims to capture large-scale moves
- **Tiered Decrease**: Lower take-profit expectations over time; adapting to trend decay characteristics
- **Loose Stop-Loss**: -5% provides sufficient volatility room for trades

### 2.2 Time Window Configuration

```python
# Entry time window: 4 AM to midnight
buy_hour = range(4, 25)  # 4:00 - 24:00 (UTC)

# Exit time window: 9 PM to 10 PM
sell_hour = [21, 22]     # 21:00 - 22:59 (UTC)
```

---

## III. Entry Conditions Details

### 3.1 Time Window Judgment

```python
# Core entry time condition
conditions.append(dataframe['hour'].isin([4, 5, 6, 7, 8, 9, 10, 11, 12, 
                                           13, 14, 15, 16, 17, 18, 19, 20, 
                                           21, 22, 23, 24]))
```

**Session Selection Logic**:
- **Avoid Early Morning Lull**: 0:00-4:00 typically the lowest global liquidity period
- **Cover Active Sessions**: Encompasses major trading sessions in Asia, Europe, and Americas
- **Total 21 Hours**: Only 3 hours per day prohibited from entry

### 3.2 Trend Confirmation Condition

```python
# EMA trend confirmation
conditions.append(dataframe['close'] > dataframe['EMA'])
```

**Logic**:
- Price above EMA confirms current uptrend
- Time window + trend confirmation dual filter reduces false signal probability

---

## IV. Exit Logic Details

### 4.1 Time Window Exit

```python
# Specific session exit
conditions.append(dataframe['hour'].isin([21, 22]))
```

**Session Selection Logic**:
- **21:00-23:00 UTC**: Pre-Americas session close; higher volatility
- **Profit-Taking Window**: Close positions when liquidity is sufficient

### 4.2 Technical Signal Exit

```python
# RSI reversal signal
conditions.append(dataframe['close'] < dataframe['EMA'])
```

**Logic**:
- Price falling below EMA is a trend reversal signal
- Forms symmetrical logic with entry condition

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Trend Indicator** | EMA (Exponential Moving Average) | Trend direction judgment |
| **Momentum Indicator** | RSI (Relative Strength Index) | Overbought/oversold judgment |
| **Time Factor** | Hour | Session selection |

### 5.2 Indicator Calculation Details

```python
# Time factor extraction
dataframe['hour'] = dataframe['date'].dt.hour

# EMA calculation (typical period 50 or 200)
dataframe['EMA'] = ta.EMA(dataframe, timeperiod=50)

# RSI calculation (typical period 14)
dataframe['RSI'] = ta.RSI(dataframe, timeperiod=14)
```

---

## VI. Risk Management Highlights

### 6.1 Hard Stop-Loss Protection

- **Stop-Loss Amplitude**: -5%
- **Trigger Mechanism**: Forced liquidation when price falls 5% below entry price
- **Design Philosophy**: Provides sufficient volatility room for trades while controlling maximum loss

### 6.2 Tiered ROI

| Holding Time | Take-Profit Target | Design Intent |
|-------------|-------------------|--------------|
| 0 minutes | 52.8% | Capture large-scale moves |
| 3 hours | 11.3% | Lower expectations; lock in profits |
| 9 hours | 8.9% | Further lower expectations |
| 24 hours | 0% | Break-even exit; avoid overnight risk |

---

## VII. Strategy Pros & Cons

### Strengths

1. **Simple Logic**: Time factor + trend confirmation; easy to understand and implement
2. **Session Avoidance**: Actively avoids low-liquidity sessions; reduces slippage risk
3. **Few Parameters**: Core parameters only time window and EMA period; low overfitting risk
4. **Beginner-Friendly**: Clear concepts; suitable for quantitative trading introduction

### Weaknesses

1. **Timezone Sensitive**: Time window needs adjustment based on exchange timezone
2. **Poor Holiday Performance**: Holiday liquidity patterns change; strategy effectiveness declines
3. **No Volatility Filter**: Does not distinguish between high and low volatility market environments
4. **Single Trend Indicator**: Only relies on EMA; prone to false signals in ranging markets

---

## VIII. Applicable Scenarios

| Market Environment | Recommendation | Notes |
|-------------------|---------------|-------|
| Trending Market | Enable | Time + trend dual confirmation most effective |
| Ranging Market | Use with Caution | EMA false signals frequent; need additional filters |
| Holidays | Disable | Liquidity patterns abnormal; strategy fails |
| Major Events | Use with Caution | Market behavior deviates from normal session patterns |

---

## IX. Applicable Market Environment Analysis

**HourBasedStrategy** is a time-factor-driven strategy. Its effectiveness is built on the time patterns of cryptocurrency markets — significant volatility and liquidity differences exist across different sessions.

### 9.1 Strategy Core Logic

- **Time Patterns**: Cryptocurrency markets have clear session effects
  - Asian Session (0:00-8:00 UTC): Lower volatility
  - European Session (8:00-16:00 UTC): Volatility rising
  - Americas Session (14:00-22:00 UTC): Highest volatility
  
- **Session Selection**: Strategy chooses 4:00-24:00 UTC as entry window; covers main active sessions

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| Trending Market | ⭐⭐⭐⭐☆ | Time + EMA dual confirmation effective |
| Ranging Market | ⭐⭐☆☆☆ | EMA false signals frequent |
| Low-Liquidity Sessions | ⭐⭐☆☆☆ | Strategy design has already avoided this |
| Strong Bear Market | ⭐⭐⭐☆☆ | Long logic may fail |

---

## X. Important Notes: Timezone and Configuration

### 10.1 Timezone Adjustment

The strategy uses UTC time; adjustment needed based on exchange timezone:

| Exchange | Timezone Offset | Suggested Entry Session |
|---------|----------------|----------------------|
| Binance (UTC+8) | +8 hours | 12:00-08:00 (local) |
| Coinbase (UTC-5) | -5 hours | 23:00-19:00 (local) |
| Kraken (UTC) | 0 | 04:00-00:00 (local) |

### 10.2 Backtesting vs. Live Trading Differences

- Time factor in backtesting may be overfitted to historical data
- Exchange maintenance windows need consideration in live trading
- Daylight saving time changes may affect strategy performance

### 10.3 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------------|------------|----------------|
| 10-20 pairs | 1GB | 2GB |
| 20-50 pairs | 2GB | 4GB |

---

## XI. Summary

**HourBasedStrategy** is a quantitative trading strategy with time factors as its core. Its core value lies in:

1. **Simple and Effective**: Time window + EMA trend confirmation; clear logic; easy to execute
2. **Session Avoidance**: Actively avoids low-liquidity sessions; reduces trading costs
3. **Risk Management**: Tiered ROI + Hard stop-loss dual protection

For quantitative traders, this is a good entry-level strategy. Recommendations:

- **Beginners**: Directly use default parameters for small-capital testing
- **Advanced**: Optimize time window based on target exchange's session characteristics
- **Professionals**: Combine with volatility indicators (e.g., ATR) to filter low-volatility environments

**Applicability Summary**: The strategy performs well in trending markets and should be used with caution in ranging markets. Thorough backtesting and paper trading verification are essential before deploying real capital.

---
