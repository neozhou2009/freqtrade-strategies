# EMA_CROSSOVER Strategy: In-Depth Analysis

> **Strategy Number**: #159 (159th of 465 strategies)  
> **Strategy Type**: EMA Crossover  
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**EMA_CROSSOVER** is a classic EMA crossover strategy, and one of Freqtrade's sample strategies. The strategy uses three EMAs (10, 100, 1000 periods) for crossover judgment.

### Key Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1: EMA10 crosses above EMA100 |
| **Sell Conditions** | 1: EMA100 crosses above EMA10 |
| **Timeframe** | 5 Minutes |
| **Dependencies** | TA-Lib, technical |

---

## II. Strategy Configuration

```python
minimal_roi = {
    "60": 0.01,   # 1%
    "30": 0.02,   # 2%
    "0": 0.04     # 4%
}

stoploss = -0.10  # -10%

trailing_stop = False  # Not enabled
```

**Characteristics**:
- **Low ROI target**: Initial only 4%
- **Strict stoploss**: -10%

---

## III. Entry Conditions Details

```python
dataframe.loc[
    (dataframe['ema10'].crossed_above(dataframe['ema100'])),
    'buy'
] = 1
```

**Logic**: EMA10 crosses above EMA100, forming a short-term trend reversal.

---

## IV. Exit Conditions Details

```python
dataframe.loc[
    (dataframe['ema100'].crossed_above(dataframe['ema10'])),
    'sell'
] = 1
```

**Logic**: EMA100 crosses above EMA10, forming a short-term trend reversal (death cross).

---

## V. Technical Indicators

| Indicator | Period | Purpose |
|----------|--------|---------|
| EMA10 | 10 | Short-term EMA |
| EMA100 | 100 | Medium-term EMA |
| EMA1000 | 1000 | Long-term EMA |

---

## VI. Risk Management

### 6.1 Multi-Level ROI

| Time (minutes) | Profit |
|---------------|--------|
| 0 | 4% |
| 30 | 2% |
| 60 | 1% |

**Design Philosophy**: Lower profit expectations over time, quickly accumulate small profits.

### 6.2 Stoploss Settings

```python
stoploss = -0.10  # -10%
```

Relatively strict stoploss, controlling losses promptly.

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Extremely simple logic**: Only uses EMA crossover, code is concise
2. **Low ROI target**: Easier to achieve, quickly accumulates small profits
3. **Easy to understand**: Great for beginners to learn
4. **Highly extensible**: Can add other indicators

### ⚠️ Cons

1. **No volume confirmation**: May produce false signals
2. **No trend filtering**: Doesn't judge major trend direction
3. **No trailing stop**: Trailing mechanism not enabled

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Config | Notes |
|-------------------|-------------------|-------|
| Trending up | Use freely | Golden cross = buy signal |
| Dip bounce | Use buy condition | Bounce also profitable |
| Oscillating market | Reduce trading pairs | Crossovers frequent |
| Consolidation | Don't use | Too many false signals |

---

## IX. Applicable Market Environments in Detail

### 9.1 Core Strategy Logic

- Golden cross: EMA10 crosses above EMA100 = short-term trend turning bullish
- Death cross: EMA100 crosses above EMA10 = short-term trend turning bearish

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---:|:---|
| Trending up | ★★★★★ | Golden cross confirms trend |
| Dip bounce | ★★★★☆ | Bounce also profitable |
| Oscillating market | ★★☆☆☆ | Crossovers frequent, many false signals |
| Consolidation | ★☆☆☆☆ | Too many false signals |

---

## X. Important Notes

### 10.1 False Signal Risk

MA crossover false signals are numerous — without volume confirmation, it's easy to be fooled by "false breakouts"!

### 10.2 Hardware Requirements

The strategy has extremely low computational load, no hardware demands.

---

## XI. Summary

**EMA_CROSSOVER** is a classic EMA crossover strategy template with simple and clear logic. The strategy is designed for small-profit quick accumulation, suitable for day trading and short-term operations.
