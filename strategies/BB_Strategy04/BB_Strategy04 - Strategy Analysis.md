# BB_Strategy04 Strategy Analysis

> **Strategy Number**: #44
> **Strategy Type**: Bollinger Band Range Breakout
> **Timeframe**: 1 hour (1h)

---

## I. Strategy Overview

BB_Strategy04 is a simple strategy based on Bollinger Band range breakout. Strategy logic is very direct: buy when price falls below inner lower Bollinger Band, sell when price breaks above inner upper Bollinger Band.

This is a typical **breakout trading strategy**, based on following assumption: price will continue trend after breaking through key positions.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 1 condition |
| **Exit Conditions** | 1 condition |
| **Protection** | Stoploss price dynamically calculated |
| **Timeframe** | 1h |
| **Dependencies** | technical (qtpylib), talib |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
minimal_roi = {
    "0": 0.22597784040439192,  # Immediate take-profit 22.6%
    "180": 0.06269048445164815,    # 6.3% after 180 candles
    "613": 0.037662786960331776,    # 3.8% after 613 candles
    "2004": 0                           # After that, rely on ROI
}
stoploss = -0.32530922906811843   # Stoploss -32.5%!

# Trailing stop
trailing_stop = True
```

**Design Logic**:
- Extremely high stoploss amplitude (-32.5%) combined with aggressive take-profit targets
- Strategy designed for long-term holding — accepts large volatility
- Bollinger Band inner layer (1 standard deviation) as key position

---

## III. Entry Conditions Details

### Condition: Price Breaks Through Bollinger Band Inner Lower Band

```python
dataframe.loc[
    (
        (dataframe['close'] < dataframe['bb_lowerband2'])
        & (dataframe['close'] > dataframe['bb_lowerband2'] * (1 + self.stoploss))
    ),
    'entry'] = 1
```

**Logic Interpretation**:
- Buy when close price falls below 2 standard deviation lower Bollinger Band
- Simultaneously requires close price above stoploss line (bb_lowerband2 * (1 + stoploss))
- This means entry price must be above forced stoploss position

---

## IV. Exit Conditions Details

### Condition: Price Breaks Through Bollinger Band Inner Upper Band

```python
dataframe.loc[
    (
        (dataframe['close'] > dataframe['bb_upperband2'])
    ),
    'exit'] = 1
```

**Logic Interpretation**:
- Sell when close price breaks above 2 standard deviation upper Bollinger Band
- This is a simple breakout sell strategy

---

## V. Technical Indicator System

### Indicator Configuration

| Indicator | Parameters | Usage |
|-----------|------------|-------|
| RSI | Default period (14) | Identify overbought/oversold |
| Bollinger Bands | window=24*3=72, stds=1 | Identify price volatility range |
| Bollinger Bands | window=72, stds=2 | Inner/outer boundaries |

---

## VI. Risk Management Features

### 6.1 Stoploss Strategy

- Stoploss position dynamically calculated as: bb_lowerband2 * (1 + stoploss)
- Stoploss distance very large — about 32.5%

### 6.2 Wisdom of Dynamic Stoploss

Unique feature of this strategy is **dynamic stoploss mechanism**:
- Stoploss price not fixed — floats with Bollinger Band lower band
- When Bollinger Band lower band moves up, stoploss price automatically moves up
- This design allows strategy to adapt to markets with different volatility

### 6.3 ROI Strategy Analysis

| Time Range | Take-Profit Target | Explanation |
|-----------|-------------------|-------------|
| 0 candles | 22.6% | Extremely high take-profit — requires large rebound |
| About 7.5 days | 6.3% | Medium-term holding target |
| About 25 days | 3.8% | Reduced target |
| About 83 days+ | 0 | Return to normal ROI |

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Extremely simple**: Very small code volume
2. **Clear**: Buy/sell conditions clear
3. **Automatic stoploss calculation**: Stoploss position dynamically calculated based on Bollinger Bands

### ⚠️ Cons

1. **No technical indicator confirmation**: Doesn't rely on RSI, MACD, etc.
2. **High stoploss**: 32.5% stoploss amplitude relatively large
3. **Low signal frequency**: Requires price to break through extreme Bollinger Band positions

---

## VIII. Parameter Optimization

| Parameter Category | Optimization Priority | Notes |
|-------------------|----------------------|-------|
| Stoploss | High | Critical for risk control |
| ROI Table | Medium | Affects profit-taking behavior |
| BB Period | Medium | Affects signal frequency |
| BB Standard Deviations | Low | Default values work |

---

## IX. Live Trading Notes

### 9.1 Learning Curve

**Entry Difficulty**: ★★☆☆☆ (Low)

This is a simple strategy — suitable for beginners:

- Simple logic
- Clear buy/sell conditions
- Dynamic stoploss mechanism
- Small code volume

### 9.2 Hardware & Resource Requirements

| Item | Requirement | Explanation |
|------|-------------|-------------|
| Computing Resources | Low | Only need to calculate Bollinger Bands |
| Memory Usage | Low | Few indicators |
| Network Requirements | Low | 1-hour data volume small |

### 9.3 Psychological Requirements

- **Patience**: May have few signals — need waiting
- **Discipline**: Must strictly execute stoploss
- **High risk tolerance**: 32.5% stoploss requires strong psychological quality
- **Long-term thinking**: Strategy designed for long-term holding

### 9.4 Risks to Note

1. **High stoploss risk**: 32.5% stoploss may cause large losses
2. **No trend filter**: May trade against trend
3. **Low signal frequency**: May have no trades for long time
4. **Dynamic stoploss lag**: Stoploss may not adjust quickly enough

---

## X. Summary

### 10.1 Core Evaluation

BB_Strategy04 is a **simple Bollinger Band breakout strategy**. Its core value lies in **dynamic stoploss mechanism and clear signals**. Strategy follows classic breakout theory — enters when price breaks through Bollinger Band boundaries.

This strategy is especially suitable for:
- Quantitative trading beginners learning strategy design
- Investors pursuing simple trading
- Traders with high risk tolerance

### 10.2 Suitable For

| Investor Type | Suitability | Reason |
|--------------|-------------|--------|
| Quant Newbies | ⭐⭐⭐⭐☆ | Simple strategy — easy to understand |
| High Risk Tolerance | ⭐⭐⭐⭐⭐ | 32.5% stoploss requires strong psychology |
| Long-term Traders | ⭐⭐⭐⭐☆ | Designed for long-term holding |
| Conservative Investors | ⭐☆☆☆☆ | Too high stoploss |
| Short-term Traders | ⭐⭐☆☆☆ | Signal frequency low |

### 10.3 Improvement Suggestions

If hoping to enhance this strategy, consider:

1. **Add trend filter**: Use moving averages to judge market direction
2. **Reduce stoploss**: Change 32.5% to more reasonable 10-15%
3. **Add volume confirmation**: Require volume cooperation
4. **Add technical indicator confirmation**: Use RSI or MACD for confirmation
5. **Adjust ROI table**: Make take-profit targets more realistic

---

*This document is based on strategy code*
