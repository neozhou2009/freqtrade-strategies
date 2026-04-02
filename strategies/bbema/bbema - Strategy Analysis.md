# bbema Strategy Analysis

> **Strategy Number**: #36  
> **Strategy Type**: Simple EMA Crossover + Bollinger Band Mean Reversion  
> **Timeframe**: 1 hour (1h)

---

## I. Strategy Overview

bbema is a concise cryptocurrency trading strategy that adopts a classic design combining EMA crossovers with Bollinger Band mean reversion. This strategy is one of Freqtrade's official default strategies, widely welcomed by beginners for its simple code and easy understanding.

The strategy's core logic is: generates entry signals when short-term EMA (10-period) crosses above medium-term EMA (50-period), viewed as uptrend confirmation; generates exit signals when short-term EMA crosses below medium-term EMA, viewed as downtrend confirmation. Bollinger Bands serve as auxiliary tool, helping identify extreme price positions.

This is a typical "trend following + mean reversion" combination strategy, suitable for long-term trend markets.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 1 independent entry signal (EMA golden cross) |
| **Exit Conditions** | 1 independent exit signal (EMA death cross) |
| **Protection** | No explicit protection mechanisms |
| **Timeframe** | 1 hour |
| **Dependencies** | talib, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.20    # Immediate exit requires 20% profit
}

# Stoploss setting
stoploss = -0.10  # 10% fixed stoploss
```

**Design Logic**:

20% immediate take-profit threshold is very aggressive; for 1-hour timeframe means requires considerable price movement to trigger. This reflects strategy author's expectation for long-term trends — rather wait for big trends than frequently take small profits.

10% fixed stoploss is one of standard settings in cryptocurrency market.

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "limit",
    "exit": "limit",
    "stoploss": "market",
    "stoploss_on_exchange": False,
}
```

---

## III. Entry Conditions Details

### 3.1 Single Entry Condition

```python
dataframe["close10"] = dataframe["close"].shift(periods=-10)
dataframe.loc[
    (qtpylib.crossed_above(dataframe["ema10"], dataframe["ema50"])), "buy"
] = 1
```

**Logic Breakdown**:

1. **ema10 > ema50**: 10-period EMA above 50-period EMA
2. **crossed_above**: Today EMA10 crosses above EMA50 (golden cross)

**Technical Meaning**:

EMA golden cross is classic trend confirmation signal. When short-term EMA crosses from below through long-term EMA, typically viewed as bullish signal.

---

## IV. Exit Logic Details

### 4.1 Single Exit Condition

```python
dataframe.loc[
    (qtpylib.crossed_above(dataframe["ema50"], dataframe["ema10"])), "sell"
] = 1
```

**Logic Breakdown**:

1. **ema50 > ema10**: 50-period EMA above 10-period EMA
2. **crossed_above**: Today EMA50 crosses above EMA10 (death cross)

**Symmetrical Design**:

Entry and exit conditions completely symmetrical; this design allows strategy to work effectively in both long and short directions.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Trend Indicator | EMA(10) | Short-term trend |
| Trend Indicator | EMA(50) | Medium-term trend |
| Volatility Indicator | Bollinger Bands (20,3) | Overbought/oversold |
| Price | Typical Price | Bollinger Band calculation |

### 5.2 Bollinger Band Explanation

Strategy calculates Bollinger Bands but doesn't directly use them for trading signals, only as visualization reference.

---

## VI. Risk Management Features

### 6.1 Fixed Stoploss

10% stoploss is standard setting, provides ample price fluctuation space.

### 6.2 Aggressive Take-Profit

20% take-profit target reflects strategy's expectation for big trends.

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Simple Code**: Easy to understand and modify
2. **Long-Short Symmetry**: Complete two-way trading system
3. **Simple Parameters**: Only two EMA parameters
4. **Learning Friendly**: Suitable for beginners

### ⚠️ Cons

1. **No Protection Mechanisms**: No filtering conditions
2. **Take-Profit Hard to Trigger**: 20% threshold relatively high
3. **No Trend Filtering**: Doesn't distinguish bull/bear markets

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration |
|-------------------|--------------------------|
| Clear trending market | Usable |
| Ranging market | Use with caution |

---

## IX. Detailed Applicable Market Environments

### Strategy Core Logic

bbema is classic EMA crossover strategy, core philosophy is "enter after trend confirmation".

### Performance in Different Market Environments

| Market Type | Performance Rating |
| :--- | :--- |
| 📈 Uptrend | ⭐⭐⭐⭐ |
| 📉 Downtrend | ⭐⭐⭐⭐ |
| 🔄 Ranging market | ⭐⭐ |

---

## X. Important Reminders

### Hardware Requirements

| Number of Pairs | Minimum Memory |
|----------------|----------------|
| 1-20 | 1GB |
| 20+ | 2GB |

---

## XI. Summary

bbema is a concise entry-level strategy, suitable for learning and basic trading. It represents "simple and effective" design philosophy, one of cornerstones of Freqtrade strategy library.

---

*Document Version: v1.0*  
*Strategy Series: EMA Crossover Trend Following*
