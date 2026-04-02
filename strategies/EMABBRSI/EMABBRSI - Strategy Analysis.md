# EMABBRSI Strategy: In-Depth Analysis

> **Strategy Number**: #155 (155th of 465 strategies)  
> **Strategy Type**: EMA Crossover + Bollinger Band Breakout + RSI Confirmation  
> **Timeframe**: 1 Hour (1h)

---

## I. Strategy Overview

**EMABBRSI** is a comprehensive strategy combining EMA crossover, RSI, and Bollinger Band breakout. Operating on a 1-hour timeframe, it uses multiple buy conditions to improve signal quality.

### Key Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 3 independent conditions (Bollinger breakout / EMA200 support / Golden cross) |
| **Sell Conditions** | 2 conditions (upper Bollinger band + RSI overbought / Death cross) |
| **Timeframe** | 1 Hour |
| **Dependencies** | TA-Lib, technical |

---

## II. Strategy Configuration

```python
minimal_roi = {
    "0": 0.1414,    # 14.14%
    "25": 0.0459,   # 4.59%
    "41": 0.0207,   # 2.07%
    "67": 0         # Break-even
}

stoploss = -0.20   # -20%
```

---

## III. Entry Conditions

### Condition 1: Bollinger Lower Band Breakout

```python
(dataframe['rsi'] > 33) &
qtpylib.crossed_above(dataframe['close'], dataframe['bb_lowerband3'])
```

### Condition 2: EMA200 Support

```python
(dataframe['close'].shift(1) > dataframe['ema200']) &
(dataframe['low'] < dataframe['ema200']) &
(dataframe['close'] > dataframe['ema200'])
```

### Condition 3: Golden Cross

```python
qtpylib.crossed_above(dataframe['ema50'], dataframe['ema200'])
```

---

## IV. Exit Conditions

### Condition 1: Upper Bollinger Band + RSI Overbought

```python
(dataframe['close'] > dataframe['bb_lowerband']) &
(dataframe['rsi'] > 91)
```

### Condition 2: Death Cross

```python
qtpylib.crossed_below(dataframe['ema50'], dataframe['ema200'])
```

---

## V. Technical Indicators

| Indicator | Period | Purpose |
|----------|--------|---------|
| EMA7, EMA25 | Short-term | Fast trend |
| EMA50 | Medium-term | Medium trend |
| EMA200 | Long-term | Long-term trend |
| RSI | 14 | Overbought/oversold |
| Bollinger Bands | 20, 2/3 | Volatility boundaries |

---

## VI. Risk Management Features

### 6.1 No Independent Protection Mechanism

The strategy has no independent protection parameters, relying primarily on:
- Generous hard stoploss (-20%)
- Time stoploss (break-even after 67 minutes)
- Multi-condition filtering to reduce false signals

### 6.2 Multi-Condition Combination Advantage

The three buy conditions complement each other to improve signal quality.

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Multi-condition confirmation**: 3 types of indicators filter, reducing false signals
2. **Medium-to-long term strategy**: 1-hour level, no need to watch daily
3. **Clear logic**: Each condition has explicit logic
4. **Suitable for trending markets**: Good performance in trending markets

### ⚠️ Cons

1. **Few signals**: Strict conditions, may not buy for a long time
2. **RSI > 91 too strict**: Rarely triggers in practice
3. **No protection mechanism**: May suffer consecutive losses in oscillating markets

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Config | Notes |
|-------------------|-------------------|-------|
| Trending up | Use freely | Golden cross + Bollinger breakout |
| Dip bounce | Use condition 1 | Bollinger lower band bounce |
| Oscillating market | Reduce trading pairs | Few signals |
| Consolidation | Don't use | Many false signals |

---

## IX. Applicable Market Environments in Detail

### 9.1 Core Strategy Logic

- Bollinger breakout: Catch oversold bounce
- EMA200 support: Catch long-term MA support
- Golden cross: Confirm trend turning bullish

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---:|:---|
| Trending up | ★★★★★ | Golden cross confirms trend |
| Dip bounce | ★★★★☆ | Bollinger lower band bounce effective |
| Oscillating market | ★★★☆☆ | Bollinger for selling high/buying low |
| Consolidation | ★★☆☆☆ | MA crosses whip-saw each other |

---

## X. Important Notes

### 10.1 Signal Frequency

RSI > 91 sell condition is too strict — rarely triggers in practice. The strategy mainly relies on ROI exit.

### 10.2 Hardware Requirements

The strategy has extremely low computational load, no hardware demands.

---

## XI. Summary

EMABBRSI is a comprehensive strategy combining multiple technical indicators, operating on a 1-hour timeframe, suitable for capturing medium-to-long term trends. The strategy has clear logic, but the RSI > 91 sell condition is too strict — in practice it mainly relies on ROI exit.
