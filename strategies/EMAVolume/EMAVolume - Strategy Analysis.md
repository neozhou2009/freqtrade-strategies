# EMAVolume Strategy Analysis

> **Strategy Number**: #29 (29th of 465 strategies)  
> **Strategy Type**: EMA Crossover + Volume Confirmation  
> **Timeframe**: 15 minutes (15m)

---

## I. Strategy Overview

**EMAVolume** is a trend following strategy based on EMA crossover and volume confirmation, developed by Gert Wohlgemuth. The strategy uses dual EMA crossover (13/34) to generate buy/sell signals, and confirms signal validity through volume filtering. Key feature is simple logic, suitable for learning EMA crossover strategies.

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | 1 condition: EMA golden cross + volume confirmation |
| **Exit Conditions** | 1 condition: EMA death cross |
| **Protection** | Hard stoploss |
| **Timeframe** | 15 minutes |
| **Dependencies** | TA-Lib, technical |
| **Special Features** | Volume filtering |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.5    # Immediate exit: 50% profit
}

# Stoploss setting
stoploss = -0.2  # -20% hard stoploss
```

**Design Logic**:
- **High ROI**: 50% ROI, expecting to capture large trends
- **Loose Stoploss**: -20% hard stoploss, giving ample room for fluctuation

### 2.2 Order Type Configuration

Uses Freqtrade default configuration.

---

## III. Entry Conditions Explained

### 3.1 Entry Logic

```python
# Entry conditions
dataframe.loc[
    (
        (qtpylib.crossed_above(dataframe["ema13"], dataframe["ema34"])) &  # EMA13 crosses above EMA34
        (dataframe["volume"] > dataframe["volume"].rolling(window=10).mean())  # Volume > 10-period avg
    ),
    "buy",
] = 1
```

**Logic Analysis**:
- **EMA Golden Cross**: EMA13 crosses above EMA34, confirming short-term trend strengthening
- **Volume Confirmation**: Volume greater than 10-period average, confirming signal validity

### 3.2 Indicator Calculation

```python
# EMA
dataframe["ema13"] = ta.EMA(dataframe, timeperiod=13)
dataframe["ema34"] = ta.EMA(dataframe, timeperiod=34)
dataframe["ema7"] = ta.EMA(dataframe, timeperiod=7)
dataframe["ema21"] = ta.EMA(dataframe, timeperiod=21)
dataframe["ema50"] = ta.EMA(dataframe, timeperiod=50)
dataframe["ema200"] = ta.EMA(dataframe, timeperiod=200)

# Volume moving average
dataframe["volume_mean"] = dataframe["volume"].rolling(window=10).mean()
```

---

## IV. Exit Logic Explained

### 4.1 Exit Conditions

```python
# Exit conditions
dataframe.loc[
    (qtpylib.crossed_below(dataframe["ema13"], dataframe["ema34"])),  # EMA13 crosses below EMA34
    "sell",
] = 1
```

**Logic Analysis**:
- **EMA Death Cross**: EMA13 crosses below EMA34, confirming short-term trend weakening

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|---------|---------|------|------|
| **Trend** | EMA | 7/13/21/34/50/200 periods | Multi-layer trend judgment |
| **Volume** | Volume MA | 10 periods | Volume filtering |

### 5.2 Multi-Layer EMA System

The strategy calculates multiple EMAs, but entry/exit only uses 13/34 EMA:

| EMA | Period | Purpose |
|-----|------|------|
| EMA7 | 7 | Ultra short-term trend (unused) |
| EMA13 | 13 | Short-term trend (entry/exit) |
| EMA21 | 21 | Medium short-term trend (unused) |
| EMA34 | 34 | Medium-term trend (entry/exit) |
| EMA50 | 50 | Medium-term trend (unused) |
| EMA200 | 200 | Long-term trend (unused) |

**Note**: Although multiple EMAs are calculated, actual trading signals only use 13/34 EMA crossover.

---

## VI. Risk Management Features

### 6.1 Loose Hard Stoploss

```python
stoploss = -0.2  # -20%
```

**Description**: Loose stoploss, giving ample room for fluctuation.

### 6.2 High ROI Exit

```python
minimal_roi = {"0": 0.5}  # 50%
```

**Purpose**:
- Exit at 50% profit
- Expecting to capture large trends

### 6.3 Volume Filtering

```python
dataframe["volume"] > dataframe["volume"].rolling(window=10).mean()
```

**Purpose**:
- Confirm signal validity
- Exclude low volume false signals

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Simple Logic**: EMA crossover + volume, easy to understand
2. **Volume Filtering**: Excludes low volume false signals
3. **High ROI**: 50% ROI, expecting to capture large trends
4. **Low Computation**: Few indicators, low hardware requirements
5. **High Learning Value**: Suitable for learning EMA crossover strategies

### ⚠️ Limitations

1. **No Trend Filter**: No long-term trend judgment (e.g., EMA200)
2. **No BTC Correlation**: Does not detect Bitcoin market trend
3. **High ROI**: 50% ROI may exit too early
4. **15m Timeframe**: Lower signal frequency
5. **Multi-Layer EMA Unused**: Calculated multiple EMAs but only uses 13/34

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|---------|---------|------|
| **Uptrend** | Recommended | EMA crossover performs well in trends |
| **Ranging Market** | Not recommended | EMA crossover has many false signals in ranging |
| **Downtrend** | Pause | No shorting mechanism, doesn't trade when trend down |
| **High Volatility** | Adjust stoploss | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |

---

## IX. Applicable Market Environments

EMAVolume is a trend following strategy based on the core philosophy of "EMA crossover + volume confirmation".

### 9.1 Strategy Core Logic

- **EMA Crossover**: 13/34 EMA golden cross to buy, death cross to sell
- **Volume Confirmation**: Volume greater than 10-period average
- **High ROI**: 50% ROI, expecting to capture large trends

### 9.2 Performance in Different Markets

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ★★★★☆ | EMA crossover + volume confirmation performs well |
| 🔄 Wide Ranging | ★★☆☆☆ | EMA crossover has many false signals in ranging |
| 📉 Single-sided Crash | ★★☆☆☆ | No shorting mechanism, no long-term trend filter |
| ⚡️ Extreme Sideways | ★★☆☆☆ | Too little volatility, signals decrease |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|--------|--------|------|
| **Number of Pairs** | 20-40 | Moderate signal frequency |
| **Max Open Trades** | 3-6 | Control risk |
| **Position Mode** | Fixed position | Recommended fixed position |
| **Timeframe** | 15m | Mandatory requirement |

---

## X. Important Notes: EMA Crossover Usage

### 10.1 Low Learning Cost

Strategy code is about 40 lines, logic is clear, suitable for beginners.

### 10.2 Low Hardware Requirements

Only calculates EMA and volume, low VPS requirements:

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------|---------|---------|
| 20-40 pairs | 512MB | 1GB |
| 40-80 pairs | 1GB | 2GB |

### 10.3 Volume Filtering Advantages

- **Confirm Signal Validity**: Excludes low volume false signals
- **Reduces False Signals**: Only trades when volume increases
- **Flexible Adjustment**: Can adjust filtering by modifying window

### 10.4 Manual Trading Recommendations

Manual traders can reference this strategy's EMA crossover approach:
- Use EMA13/34 golden cross to buy, death cross to sell
- Confirm volume increases
- Set loose stoploss (e.g., -20%)

---

## XI. Summary

**EMAVolume** is a simple EMA crossover strategy, its core value lies in:

1. **Simple Logic**: EMA crossover + volume, easy to understand
2. **Volume Filtering**: Excludes low volume false signals
3. **High ROI**: 50% ROI, expecting to capture large trends
4. **Low Computation**: Few indicators, low hardware requirements
5. **High Learning Value**: Suitable for learning EMA crossover strategies

For quantitative traders, this is an excellent EMA crossover learning template. Recommendations:
- Use as an introductory case for learning EMA crossover strategies
- Understand volume filtering usage
- Can add trend filters, BTC correlation, etc. on this basis
- Note that high ROI may exit large trends too early

---
