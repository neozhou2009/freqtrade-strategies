# MACD_TRI_EMA Strategy Analysis

> **Strategy Number**: #9 (9th of 465 strategies)  
> **Strategy Type**: MACD + TEMA Momentum Trend  
> **Timeframe**: 5 minutes (5m)

---

## 1. Strategy Overview

**MACD_TRI_EMA** is a concise momentum trend strategy combining MACD crossover signals with TEMA (Triple Exponential Moving Average) trend filtering. The "TRI" in the strategy name likely refers to the TEMA indicator, with overall design追求 simple and effective.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 1 condition: MACD golden cross + Price > TEMA |
| **Exit Conditions** | 1 condition: MACD death cross |
| **Protection** | Hard stoploss |
| **Timeframe** | 5 minutes |
| **Dependencies** | TA-Lib, technical (qtpylib) |
| **Special Features** | TEMA trend filtering |

---

## 2. Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "120": 0.0,    # After 120 minutes: exit at breakeven
    "30": 0.04,    # After 30 minutes: 4% profit exit
    "15": 0.06,    # After 15 minutes: 6% profit exit
    "10": 0.15,    # After 10 minutes: 15% profit exit
}

# Stoploss setting
stoploss = -0.03  # -3% hard stoploss
```

**Design Logic**:
- **Time-decreasing ROI**: Longer hold time means lower exit threshold
- **Short-term High Returns**: 15% profit exit within 10 minutes
- **Strict Stoploss**: -3% hard stoploss, controls single trade loss

### 2.2 Order Type Configuration

Uses Freqtrade default configuration.

---

## 3. Entry Conditions Explained

### 3.1 Entry Logic

```python
# Entry conditions
dataframe.loc[
    (
        qtpylib.crossed_above(dataframe["macd"], dataframe["macdsignal"])  # MACD golden cross
        & (dataframe["close"].shift(1) > dataframe["tema"].shift(1))        # Previous candle price > TEMA
    ),
    "buy",
] = 1
```

**Logic Analysis**:
- **MACD Golden Cross**: MACD line crosses above signal line from below, momentum turning strong
- **TEMA Filter**: Price above TEMA, confirms uptrend
- **Delayed Confirmation**: Uses `shift(1)` to confirm previous candle already met conditions

### 3.2 Indicator Calculation

```python
# MACD calculation
macd = ta.MACD(dataframe)
dataframe["macd"] = macd["macd"]
dataframe["macdsignal"] = macd["macdsignal"]

# TEMA calculation (Triple Exponential Moving Average)
dataframe["tema"] = ta.TEMA(dataframe, timeperiod=13)
```

**TEMA Characteristics**:
- **Triple Smoothing**: Applies triple smoothing to EMA
- **Low Lag**: Responds faster than traditional EMA
- **Trend Filter**: Price above TEMA confirms uptrend

---

## 4. Exit Logic Explained

### 4.1 Exit Conditions

```python
# Exit conditions
dataframe.loc[
    (qtpylib.crossed_above(dataframe["macdsignal"], dataframe["macd"])),  # MACD death cross
    "sell",
] = 1
```

**Logic Analysis**:
- **MACD Death Cross**: MACD signal line crosses above MACD line, momentum weakening
- **Single Condition**: Only MACD cross triggers exit, no additional filters
- **Momentum Exit**: Exits on momentum deterioration

### 4.2 ROI Exit

Time-based profit taking:
- 15% profit after 10 minutes
- 6% profit after 15 minutes
- 4% profit after 30 minutes
- Breakeven after 120 minutes

### 4.3 Hard Stoploss

```python
stoploss = -0.03  # -3%
```

**Purpose**: Strict stoploss limits losses on failed trades.

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator | Parameters | Usage |
|-----------|------------|-------|
| **MACD** | Standard (12, 26, 9) | Momentum and crossover signals |
| **TEMA** | 13 periods | Trend filtering |

### 5.2 Indicator Characteristics

- **MACD**: Standard momentum indicator with signal line crossovers
- **TEMA**: Triple Exponential Moving Average with reduced lag

---

## 6. Risk Management Features

### 6.1 Time-based ROI

**Mechanism**:
- High early thresholds (15% in 10 min) capture quick moves
- Gradually降低 thresholds for longer holds
- Breakeven after 2 hours prevents extended losses

### 6.2 Strict Stoploss

```python
stoploss = -0.03  # -3%
```

**Purpose**:
- Limits single trade loss to 3%
- Strict compared to other strategies
- Suitable for high-frequency 5m timeframe

---

## 7. Strategy Strengths and Limitations

### ✅ Strengths

1. **Simple Logic**: Only 2 indicators, easy to understand
2. **Fast Exits**: Time-based ROI captures quick profits
3. **Trend Filter**: TEMA ensures trading with trend
4. **Strict Risk Control**: -3% stoploss limits losses
5. **Low Lag**: TEMA responds quickly to price changes

### ⚠️ Limitations

1. **Simple Exit**: Only MACD cross for exit, may exit too late
2. **No Volume Filter**: Doesn't confirm volume on entries
3. **No BTC Correlation**: Doesn't account for Bitcoin direction
4. **Strict Stoploss**: May get stopped out on normal volatility
5. **No Trailing Stop**: Doesn't lock in profits on big moves

---

## 8. Recommended Usage Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Trending Market** | Default configuration | Momentum strategies excel in trends |
| **Ranging Market** | Adjust TEMA period | May generate whipsaw signals |
| **High Volatility** | Widen stoploss | -3% may be too tight |
| **Low Volatility** | Keep default | Suitable for low volatility |

---

## 9. Summary

**MACD_TRI_EMA** is a simple momentum trend strategy. Its core value lies in:

1. **Simplicity**: Only MACD and TEMA, easy to understand
2. **Fast Profits**: Time-based ROI captures quick moves
3. **Trend Confirmation**: TEMA filter ensures trend alignment
4. **Strict Risk**: -3% stoploss limits losses

For quantitative traders, this demonstrates:
- Simple momentum strategy design
- TEMA as trend filter
- Time-based profit taking
- Strict risk management

**Recommendations**:
- Consider adding volume confirmation
- May benefit from trailing stop addition
- Test on various pairs for optimal performance
- Adjust stoploss based on pair volatility

---
