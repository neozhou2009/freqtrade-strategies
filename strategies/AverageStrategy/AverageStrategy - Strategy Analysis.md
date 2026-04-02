# AverageStrategy In-Depth Analysis

> **Strategy ID**: #421 (421st of 465 strategies)  
> **Strategy Type**: Dual Moving Average Crossover Trend Following  
> **Timeframe**: 4 Hours (4h)

---

## I. Strategy Overview

AverageStrategy is a classic dual moving average crossover strategy that trades based on crossover signals between short-term and long-term Exponential Moving Averages (EMA). Developed by Gert Wohlgemuth as a proof-of-concept strategy, it features clean code and clear logic, making it an ideal introductory example for learning Freqtrade strategy development.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Condition** | 1 independent buy signal (EMA Golden Cross) |
| **Exit Condition** | 1 basic sell signal (EMA Death Cross) |
| **Protection Mechanism** | Stop loss only, no additional protection layers |
| **Timeframe** | 4 Hours (4h) |
| **Dependencies** | talib, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.5  # 50% profit target
}

# Stop loss setting
stoploss = -0.2  # 20% stop loss
```

**Design Rationale**:
- **High ROI target (50%)**: As a 4-hour trend strategy, sufficient price fluctuation space is provided to avoid premature exits
- **Moderate stop loss (20%)**: Leaves adequate tolerance for 4-hour level volatility, avoiding stops triggered by normal fluctuations

### 2.2 Order Type Configuration

This strategy does not explicitly configure `order_types` and will use Freqtrade default settings.

---

## III. Entry Conditions Detailed

### 3.1 Core Entry Logic

#### Condition #1: EMA Golden Cross
```python
# Logic
- Short-term EMA (8-period) crosses above Long-term EMA (21-period)
- Using qtpylib.crossed_above() function to detect crossover
```

**Technical Principle**:
- **EMA 8**: Fast moving average, sensitive to price changes
- **EMA 21**: Slow moving average, reflects medium-term trend
- **Golden Cross Signal**: Short-term MA crossing above long-term MA indicates strengthening short-term momentum, potential upward trend

### 3.2 Indicator Calculation

```python
dataframe['maShort'] = ta.EMA(dataframe, timeperiod=8)
dataframe['maMedium'] = ta.EMA(dataframe, timeperiod=21)
```

---

## IV. Exit Logic Detailed

### 4.1 Basic Exit Signal

**Exit Signal #1: EMA Death Cross**
```python
# Trigger condition
- Long-term EMA (21-period) crosses above Short-term EMA (8-period)
- i.e., Short-term MA crosses below Long-term MA
```

**Technical Meaning**:
- Short-term momentum weakening, trend may turn downward
- Forms symmetrical trading logic with entry signal

### 4.2 Exit Mechanism Summary

| Exit Method | Trigger Condition | Description |
|-------------|-------------------|-------------|
| ROI Take Profit | Profit reaches 50% | Fixed target take profit |
| Death Cross Exit | EMA 8 crosses below EMA 21 | Trend reversal signal |
| Stop Loss | Loss reaches 20% | Risk control baseline |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|--------------------|-------------------|---------|
| Trend Indicator | EMA (8-period) | Short-term trend direction |
| Trend Indicator | EMA (21-period) | Medium-term trend direction |
| Signal Detection | crossed_above | Crossover signal capture |

### 5.2 EMA vs SMA Selection

The strategy chooses EMA (Exponential Moving Average) over SMA (Simple Moving Average) because:
- EMA assigns higher weight to recent prices
- Faster response to price changes
- More suitable for capturing trend turning points

---

## VI. Risk Management Features

### 6.1 Concise Risk Framework

This strategy adopts a minimal risk management approach:

| Risk Parameter | Setting | Description |
|----------------|---------|-------------|
| Stop Loss | -20% | Fixed percentage stop loss |
| Take Profit | +50% | Fixed target take profit |
| Trailing Stop | None | Not enabled |

### 6.2 Risk Characteristics

- **Pros**: Clear logic, few parameters, easy to understand and optimize
- **Cons**: Lacks dynamic risk control mechanisms, cannot adapt to market volatility changes

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Simple Logic**: Only ~50 lines of code, beginner-friendly, easy to learn and modify
2. **Classic and Reliable**: Dual MA crossover is one of the most classic trend-following methods
3. **Intuitive Parameters**: Only 2 MA parameters, easy to understand and optimize
4. **4-Hour Framework**: Reduces noise, suitable for capturing medium-term trends

### ⚠️ Limitations

1. **Trend Dependent**: Produces numerous false signals and consecutive stop losses in ranging markets
2. **Lag**: Moving averages are lagging indicators, entry and exit timing is delayed
3. **Lack of Filtering**: No additional trend confirmation or volatility filtering mechanisms
4. **Author's Note**: Original author explicitly states this is "proof of concept", performs poorly in live trading

---

## VIII. Suitable Scenarios

| Market Environment | Recommended Configuration | Description |
|--------------------|--------------------------|-------------|
| Clear Trend | Default or lower ROI | Performs well in trending markets |
| Ranging Market | Not recommended | Will generate many false signals |
| High Volatility | Increase stop loss | Avoid stops triggered by normal volatility |
| Beginner Learning | Default configuration | As introductory strategy learning framework |

---

## IX. Applicable Market Environment Details

AverageStrategy is an ultra-simple **trend-following beginner strategy**. Based on the classic principle of dual MA crossover, it is best suited for **markets with clear single-direction trends**, while performing poorly in **ranging sideways markets**.

### 9.1 Strategy Core Logic

- **Trend Following**: Captures trend initiation and reversal through MA crossovers
- **Symmetrical Trading**: Golden cross to buy, death cross to sell, symmetrical logic
- **Medium-term Perspective**: 4-hour framework suitable for capturing trends lasting days to weeks

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:-------------------|:---------|
| 📈 Strong Uptrend | ⭐⭐⭐⭐☆ | Effectively captures trends, but entry slightly delayed |
| 🔄 Sideways Range | ⭐☆☆☆☆ | Frequent crossovers lead to consecutive stop losses |
| 📉 Strong Downtrend | ⭐⭐☆☆☆ | Stays in cash, but lacks shorting mechanism |
| ⚡️ High Volatility | ⭐⭐☆☆☆ | May be triggered by noise false signals |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|---------------|-------------------|-------------|
| Trading Pairs | Major coins (BTC/ETH) | Good liquidity, more obvious trends |
| MA Periods | 8/21 or adjusted | Can optimize based on market characteristics |
| Stop Loss | -0.15 to -0.25 | Adjust based on 4h volatility |

---

## X. Important Note: Value as a Learning Strategy

### 10.1 Learning Value

As a proof-of-concept strategy, AverageStrategy's core value lies in:
- **Teaching Demonstration**: Showcases Freqtrade strategy basic framework
- **Code Template**: Can serve as starting point for developing complex strategies
- **Clear Logic**: Facilitates understanding of MA crossover strategy principles

### 10.2 Live Trading Considerations

- Author explicitly states the strategy performs poorly in live trading
- Recommended only as learning material, not for direct live trading
- If used live, additional filtering conditions and risk control mechanisms should be added

### 10.3 Improvement Directions

| Improvement Direction | Suggested Method |
|----------------------|------------------|
| Reduce False Signals | Add ADX trend strength filter |
| Dynamic Stop Loss | Introduce trailing stop or ATR stop |
| Entry Confirmation | Add RSI or volume filter |

---

## XI. Summary

**AverageStrategy** is a classic dual MA crossover beginner strategy. Its core value lies in:

1. **Teaching Demonstration**: Showcases the basic framework of Freqtrade strategy development
2. **Clear Logic**: Golden cross buy, death cross sell, easy to understand
3. **Extensibility**: Can serve as foundation template for more complex strategies

For quantitative trading beginners, this is an excellent starting point for understanding MA strategies and the Freqtrade framework. However, for live trading, it is recommended to add trend filtering, volatility control, and other enhancement mechanisms.

---

*Strategy Author: Gert Wohlgemuth*  
*Strategy Positioning: Proof of Concept / Learning Intro*