# strato Strategy Analysis

> **Strategy Number**: #26 (26th of 465 strategies)  
> **Strategy Type**: Stochastic RSI Momentum  
> **Timeframe**: 1 minute (1m)

---

## I. Strategy Overview

**strato** is a momentum strategy based on Stochastic RSI. The strategy uses Stochastic RSI (StochRSI) to capture short-term overbought/oversold opportunities, combined with K and D line crossovers to generate buy/sell signals. Key features are extremely short timeframe (1 minute) and quick turnover.

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | 1 condition: StochRSI K < 18 + K >= D |
| **Exit Conditions** | 1 condition: StochRSI K > 80 + D >= K |
| **Protection** | Hard stoploss |
| **Timeframe** | 1 minute |
| **Dependencies** | TA-Lib, technical |
| **Special Features** | Ultra short-term trading |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.012    # Immediate exit: 1.2% profit
}

# Stoploss setting
stoploss = -0.1  # -10% hard stoploss
```

**Design Logic**:
- **Low ROI**: 1.2% ROI, pursuing quick turnover
- **Standard Stoploss**: -10% hard stoploss

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "market",
    "exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": False,
}

order_time_in_force = {
    "entry": "GTC",
    "exit": "GTC",
}
```

**Description**: Uses market orders to ensure quick execution.

---

## III. Entry Conditions Explained

### 3.1 Entry Logic

```python
# Entry conditions
dataframe.loc[
    (
        (dataframe["k"] < 18) &           # StochRSI K < 18 (oversold)
        (dataframe["k"] >= dataframe["d"])  # K >= D (golden cross confirmation)
    ),
    "enter_long",
] = 1
```

**Logic Analysis**:
- **StochRSI Oversold**: K < 18, confirming short-term oversold
- **K Line Confirmation**: K >= D, confirming momentum strengthening

### 3.2 Indicator Calculation

```python
# RSI
dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

# Stochastic RSI
p = 14  # RSI period
d = 3   # D line period
k = 3   # K line period

srsi = (dataframe["rsi"] - dataframe["rsi"].rolling(p).min()) / (
    dataframe["rsi"].rolling(p).max() - dataframe["rsi"].rolling(p).min()
)
dataframe["k"] = srsi.rolling(k).mean() * 100
dataframe["d"] = dataframe["k"].rolling(d).mean()
```

---

## IV. Exit Logic Explained

### 4.1 Exit Conditions

```python
# Exit conditions
dataframe.loc[
    (
        (dataframe["k"] > 80) &           # StochRSI K > 80 (overbought)
        (dataframe["d"] >= dataframe["k"])  # D >= K (death cross confirmation)
    ),
    "exit_long",
] = 1
```

**Logic Analysis**:
- **StochRSI Overbought**: K > 80, confirming short-term overbought
- **D Line Confirmation**: D >= K, confirming momentum weakening

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|---------|---------|------|------|
| **Momentum** | RSI | 14 periods | Base momentum |
| **Momentum** | Stochastic RSI | 14/3/3 | Overbought/Oversold |

### 5.2 Stochastic RSI Calculation

```python
# SRSI = (RSI - RSI_min) / (RSI_max - RSI_min)
srsi = (rsi - rsi.rolling(14).min()) / (rsi.rolling(14).max() - rsi.rolling(14).min())

# K line = 3-period moving average of SRSI × 100
k = srsi.rolling(3).mean() * 100

# D line = 3-period moving average of K line
d = k.rolling(3).mean()
```

---

## VI. Risk Management Features

### 6.1 Hard Stoploss

```python
stoploss = -0.1  # -10%
```

**Description**: Standard stoploss, controlling single trade loss within 10%.

### 6.2 Low ROI Quick Exit

```python
minimal_roi = {"0": 0.012}  # 1.2%
```

**Purpose**:
- Exit at 1.2% profit
- With 1-minute timeframe for quick turnover

### 6.3 Market Orders

```python
order_types = {
    "entry": "market",
    "exit": "market",
    "stoploss": "market",
}
```

**Purpose**: Ensures quick execution, suitable for 1-minute ultra short-term trading.

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Simple Logic**: StochRSI golden/death cross, easy to understand
2. **Low Computation**: Few indicators, low hardware requirements
3. **Low ROI**: 1.2% ROI, quick turnover
4. **Market Orders**: Ensures quick execution
5. **High Learning Value**: Suitable for learning StochRSI strategies

### ⚠️ Limitations

1. **1-Minute Timeframe**: Signals extremely fast, needs low latency execution
2. **No Trend Filter**: No long-term trend judgment
3. **No BTC Correlation**: Does not detect Bitcoin market trend
4. **Fee Sensitive**: 1-minute trading is frequent, fees significantly impact profits
5. **Many False Signals**: 1-minute level has many false signals

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| **Ranging Market** | Default configuration | StochRSI most suitable for ranging markets |
| **Uptrend** | Default configuration | Low ROI enables quick turnover |
| **Downtrend** | Pause | No trend filter, easy to lose |
| **High Volatility** | Adjust stoploss | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |

---

## IX. Summary

**strato** is a simple StochRSI momentum strategy, its core value lies in:

1. **Simple Logic**: StochRSI golden/death cross, easy to understand
2. **Low Computation**: Few indicators, low hardware requirements
3. **Low ROI**: 1.2% ROI, quick turnover
4. **Market Orders**: Ensures quick execution
5. **High Learning Value**: Suitable for learning StochRSI strategies

For quantitative traders, this is an excellent ultra short-term learning template. Recommendations:
- Use as an introductory case for learning StochRSI strategies
- Understand 1-minute trading risks
- Can add trend filters, BTC correlation, etc. on this basis
- Note fee impact, testthoroughly before live trading

---
