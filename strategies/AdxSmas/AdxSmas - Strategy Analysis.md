# AdxSmas Strategy Analysis

> **Strategy ID**: #416 (416th of 465 strategies)  
> **Strategy Type**: Trend Strength Filter + Moving Average Crossover  
> **Timeframe**: 1 Hour (1h)

---

## 1. Strategy Overview

AdxSmas is a classic trend trading strategy that combines the ADX (Average Directional Index) trend strength indicator with dual SMA (Simple Moving Average) crossover signals. The core logic is: only execute moving average crossover trades when trend strength is sufficient, thereby filtering out false signals from ranging markets.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 core buy signal (ADX > 25 + SMA golden cross) |
| **Sell Conditions** | 1 base sell signal (ADX < 25 + SMA death cross) |
| **Protection Mechanism** | 25% fixed stop loss |
| **Timeframe** | 1 Hour (1h) |
| **Dependencies** | talib, qtpylib |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.1   # Target ROI: 10%
}

# Stop Loss Settings
stoploss = -0.25  # 25% fixed stop loss
```

**Design Rationale**:
- **Single ROI Target**: 10% profit target, simple and direct
- **Wide Stop Loss**: 25% stop loss space gives trends enough room for volatility
- **Trend-Oriented**: Strategy relies on trend strength filtering, doesn't depend on frequent take-profit/stop-loss adjustments

### 2.2 Order Type Configuration

Strategy uses default order configuration, no special customization.

---

## 3. Buy Conditions Explained

### 3.1 Core Buy Logic

#### Condition #1: Trend Confirmed Golden Cross

```python
# Logic Breakdown
Condition 1: ADX > 25                    # Trend strength confirmation (ADX threshold)
Condition 2: SMA(3) crosses above SMA(6) # Short-term MA golden cross
```

**Trading Logic**:
1. **Trend Strength Filter**: ADX > 25 confirms market is in trending state, not consolidation
2. **Entry Signal**: Short-term SMA(3) crosses above long-term SMA(6), confirming trend direction
3. **Dual Confirmation**: Both conditions must be met simultaneously to trigger buy

### 3.2 ADX Indicator Analysis

**ADX (Average Directional Index)** is a classic indicator measuring trend strength:

| ADX Value | Trend Strength |
|-----------|----------------|
| 0-25 | No trend / Weak trend |
| 25-50 | Strong trend |
| 50-75 | Very strong trend |
| 75-100 | Extremely strong trend |

**Strategy uses ADX > 25 as threshold**, ensuring trades only occur when there's a clear trend.

### 3.3 SMA Crossover Analysis

| Moving Average | Period | Purpose |
|----------------|--------|---------|
| Short-term SMA | 3 | Quick response to price changes |
| Long-term SMA | 6 | Smooth short-term fluctuations |

**Parameter Characteristics**:
- Uses very short periods (3 and 6), belongs to fast-response type moving averages
- Suitable for capturing short-term trend changes
- Sensitive to price changes, but may generate more false signals

---

## 4. Sell Logic Explained

### 4.1 Base Sell Signal

```python
# Sell Conditions
Condition 1: ADX < 25                    # Trend strength weakening
Condition 2: SMA(6) crosses above SMA(3) # Short-term MA death cross
```

**Trading Logic**:
1. **Trend Weakening**: ADX < 25 indicates trend strength declining, market may be entering consolidation
2. **Direction Reversal**: Long-term SMA crosses above short-term SMA, indicating trend may be reversing
3. **Dual Confirmation**: Again requires both conditions simultaneously

### 4.2 Sell Signal Comparison

| Dimension | Buy Signal | Sell Signal |
|-----------|------------|-------------|
| ADX Condition | > 25 (trend exists) | < 25 (trend weakening) |
| SMA Condition | 3 crosses above 6 (golden cross) | 6 crosses above 3 (death cross) |
| Market State | Trend forming | Trend ending |

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|---------------------|---------|
| Trend Strength | ADX(14) | Filter false signals from ranging markets |
| Trend Direction | SMA(3), SMA(6) | Determine trade direction and entry timing |

### 5.2 Indicator Calculation Details

```python
# ADX Indicator
dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)

# Dual Moving Average System
dataframe['short'] = ta.SMA(dataframe, timeperiod=3)   # Short-term SMA
dataframe['long'] = ta.SMA(dataframe, timeperiod=6)     # Long-term SMA
```

**Indicator Characteristics**:
- **ADX(14)**: Standard period, balances sensitivity and stability
- **SMA(3, 6)**: Very short period combination, fast response but unstable

---

## 6. Risk Management Features

### 6.1 Fixed Stop Loss Mechanism

```python
stoploss = -0.25  # 25% fixed stop loss
```

**Design Considerations**:
- 25% stop loss is relatively wide, gives trends sufficient room for development
- Combined with ADX trend filtering, reduces false breakout risk
- Single ROI target (10%) with wide stop loss, risk-reward ratio approximately 1:0.4

### 6.2 Trend Filter Protection

Strategy implements implicit risk management through ADX threshold:

| Protection Mechanism | Implementation |
|---------------------|----------------|
| Ranging Market Filter | ADX > 25 to buy, avoiding consolidation losses |
| Trend Confirmation | Exit timely when ADX declines |
| Direction Confirmation | Dual SMA crossover ensures correct direction |

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Effective Trend Filtering**: ADX indicator effectively filters false signals from ranging markets
2. **Simple and Clear Logic**: Core logic is easy to understand and implement, minimal code
3. **Fast Response**: Short-period SMA quickly captures trend changes
4. **Classic Combination**: ADX + SMA is a time-tested classic combination

### ⚠️ Limitations

1. **Wide Stop Loss**: 25% stop loss may not suit low-risk-tolerance traders
2. **Too Short SMA Periods**: 3 and 6 combination is noise-sensitive, may generate excessive signals
3. **Single ROI Target**: 10% target may be too aggressive or conservative
4. **No Trailing Mechanism**: No trailing take-profit, may miss larger profits

---

## 8. Applicable Scenarios Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Strong Trend Market | Default configuration | ADX filter ensures trend capture |
| Weak Trend Market | Lower ADX threshold | May need ADX > 20 |
| High Volatility Market | Increase stop space | 25% may not be enough |
| Low Volatility Market | Keep default | ADX naturally filters |

---

## 9. Applicable Market Environment Details

AdxSmas is a classic **trend strength filter strategy**. Based on its code architecture and community long-term live trading verification experience, it is best suited for **medium-strength trend markets**, while performing poorly in **sideways consolidation and extreme volatility**.

### 9.1 Strategy Core Logic

- **Trend Identification**: Measure trend strength through ADX, avoid trading in consolidation
- **Direction Confirmation**: Short-period SMA crossover provides direction signals
- **Risk Control**: Wide stop loss gives trends room for volatility

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|-------------|-------------------|----------|
| 📈 Strong Uptrend | ⭐⭐⭐⭐⭐ | ADX high, SMA crossover effective, perfect capture |
| 🔄 Medium Trend | ⭐⭐⭐⭐☆ | ADX filtering effective, high signal quality |
| 📉 Strong Downtrend | ⭐⭐⭐☆☆ | Strategy defaults to long, shorting requires reverse configuration |
| ⚡️ Sideways Consolidation | ⭐⭐☆☆☆ | ADX filters most signals, but still some misjudgments |
| 🌀 High-Frequency Volatility | ⭐☆☆☆☆ | Short-period SMA too sensitive, signal chaos |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| ADX Threshold | 20-30 | Adjust based on market volatility, lower for low volatility |
| SMA Periods | 3/6 or 5/10 | Consider slightly longer periods to reduce noise |
| Stop Loss | -0.15 ~ -0.25 | Adjust based on risk tolerance |

---

## 10. Important Notes: The Cost of Complexity

### 10.1 Learning Curve

AdxSmas is one of the simplest strategies, with only about 50 lines of code. Core logic is clear, suitable for beginners learning Freqtrade strategy development as an introductory case.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|----------------|-------------------|
| 1-10 | 1GB | 2GB |
| 11-30 | 2GB | 4GB |
| 31+ | 4GB | 8GB |

**Note**: Strategy has minimal computation, one of the lightest strategies.

### 10.3 Backtesting vs Live Trading Differences

- **Backtesting**: ADX filtering might be too ideal in historical data
- **Live Trading**: ADX calculation has slight lag, may miss trend starting points
- **Slippage**: 1-hour timeframe has moderate slippage impact
- **Latency**: Not sensitive to latency

### 10.4 Manual Trading Recommendations

To manually execute this strategy:
1. Add ADX(14) indicator in TradingView
2. Add SMA(3) and SMA(6)
3. Wait for ADX > 25 and SMA golden cross to buy
4. Set 25% stop loss or observe ADX decline

---

## 11. Summary

**AdxSmas** is a **simple yet effective trend filtering strategy**. Its core values include:

1. **Trend Strength Filtering**: ADX indicator effectively reduces false signals in ranging markets
2. **Minimal Code**: About 50 lines of code, excellent case for learning strategy development
3. **Fast Response**: Short-period SMA captures trend changes in time
4. **Classic Combination**: ADX + SMA has been verified over time

For quantitative traders, AdxSmas provides an excellent basic framework, suitable as an introductory strategy or as a base for extending more complex logic. Recommended for medium-strength trend markets, adjust stop loss parameters based on personal risk tolerance.

---