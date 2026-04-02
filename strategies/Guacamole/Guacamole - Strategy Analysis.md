# Guacamole Strategy Analysis

> **Strategy Number**: #7 (7th of 465 strategies)  
> **Strategy Type**: Multi-Indicator Momentum Strategy (with Orderbook Check)  
> **Timeframe**: 5 minutes (5m)

---

## 1. Strategy Overview

**Guacamole** is a complex multi-indicator momentum strategy combining KAMA, MACD, RMI, SAR and other technical indicators, with an orderbook check mechanism to optimize order execution. The strategy name comes from its "mixing multiple ingredients" characteristic, like making guacamole requires mixing various ingredients.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Multi-condition combination (KAMA + MACD + RMI + Volume) |
| **Exit Conditions** | RMI oversold + profit check |
| **Protection** | Trailing stop + Order timeout check |
| **Timeframe** | 5 minutes |
| **Dependencies** | TA-Lib, technical |
| **Special Features** | Orderbook check, order timeout cancellation |

---

## 2. Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table (hyperopt results)
minimal_roi = {
    "0": 0.13336,
    "19": 0.07455,
    "37": 0.04206,
    "57": 0.02682,
    "73": 0.01225,
    "125": 0.0037,
    "244": 0.0025,
}

# Stoploss setting
stoploss = -0.10  # -10%

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01673
trailing_stop_positive_offset = 0.01851
trailing_only_offset_is_reached = False
```

**Design Logic**:
- **Multi-level ROI**: 7-level decreasing ROI, longer hold time means lower exit threshold
- **Trailing Stop**: 1.67% trailing activation, 1.85% offset trigger
- **Hyperopt Optimized**: ROI and trailing parameters from hyperopt results

### 2.2 Order Type Configuration

Uses Freqtrade default configuration, but implements order timeout check function.

---

## 3. Entry Conditions Explained

### 3.1 Entry Logic (No Position)

```python
# Entry conditions when no position
conditions = [
    dataframe["kama-3"] > dataframe["kama-21"],           # KAMA fast > slow
    dataframe["macd"] > dataframe["macdsignal"],          # MACD > signal line
    dataframe["macd"] > params["macd"],                   # MACD > threshold
    dataframe["macdhist"] > params["macdhist"],           # MACD hist > threshold
    dataframe["rmi"] > dataframe["rmi"].shift(),          # RMI rising
    dataframe["rmi"] > params["rmi"],                     # RMI > threshold
    dataframe["volume"] < (dataframe["volume_ma"] * 20),  # Volume < avg × 20
]
```

**Logic Analysis**:
- **KAMA Trend**: 3-period KAMA > 21-period KAMA, confirms short-term uptrend
- **MACD Golden Cross**: MACD line above signal line, momentum upward
- **MACD Threshold**: MACD and MACD histogram above optimized thresholds
- **RMI Momentum**: RMI indicator rising and above threshold
- **Volume Filter**: Excludes abnormally high volume (possible manipulation)

### 3.2 Entry Conditions (With Position)

```python
# Add position conditions when already holding
conditions = [
    dataframe["close"] > dataframe["sar"],    # Price > SAR
    dataframe["rmi"] >= 75,                   # RMI >= 75
]
```

**Note**: When already holding, only consider adding position when trend is strong.

### 3.3 Hyperparameters

Strategy uses hyperopt-optimized parameters:
- MACD threshold
- MACD histogram threshold
- RMI threshold

---

## 4. Exit Logic Explained

### 4.1 Exit Conditions

```python
# Exit conditions
dataframe.loc[
    (
        (dataframe["rmi"] < params["rmi"])    # RMI below threshold
        & (dataframe["profit"] > 0)            # Still in profit
    ),
    "sell",
] = 1
```

**Logic Analysis**:
- **RMI Decline**: RMI falling below threshold indicates momentum weakening
- **Profit Protection**: Only exits when still in profit
- **Momentum Exit**: Exits on momentum deterioration, not price levels

### 4.2 ROI Exit

Multi-level ROI table provides time-based exits:
- Early exit at 13.3% profit
- Gradually降低 thresholds over time
- Final exit at 0.25% after 244 minutes

### 4.3 Trailing Stop

```python
trailing_stop_positive = 0.01673  # 1.67%
trailing_stop_positive_offset = 0.01851  # 1.85%
```

**Mechanism**: Trailing activates after 1.85% profit, trails at 1.67% distance.

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator | Parameters | Usage |
|-----------|------------|-------|
| **KAMA** | 3, 21 periods | Trend direction |
| **MACD** | Standard | Momentum |
| **RMI** | Custom | Relative Momentum Index |
| **SAR** | Default | Parabolic SAR for trend |
| **Volume MA** | Custom | Volume filter |

### 5.2 Indicator Characteristics

- **KAMA**: Kaufman Adaptive Moving Average, adapts to volatility
- **MACD**: Standard momentum indicator
- **RMI**: Relative Momentum Index, combines RSI with momentum
- **SAR**: Parabolic SAR for trend following

---

## 6. Risk Management Features

### 6.1 Order Timeout Check

Strategy implements order timeout monitoring:
- Cancels orders that don't fill within timeout period
- Prevents stale orders from executing
- Ensures fresh entry signals

### 6.2 Trailing Stop

Protects profits in trending conditions:
- Activates after 1.85% profit
- Trails at 1.67% distance
- Locks in gains during strong moves

### 6.3 Multi-level ROI

Time-based profit taking:
- Higher thresholds for early exits
- Lower thresholds for longer holds
- Ensures capital turnover

---

## 7. Strategy Strengths and Limitations

### ✅ Strengths

1. **Multi-Indicator Confirmation**: Multiple indicators reduce false signals
2. **Hyperopt Optimized**: Parameters optimized for best performance
3. **Order Management**: Orderbook check and timeout prevent bad fills
4. **Flexible Exit**: Multiple exit methods (ROI, trailing, technical)
5. **Volume Filter**: Excludes suspicious volume patterns

### ⚠️ Limitations

1. **Complex Logic**: Many conditions increase complexity
2. **Hyperopt Dependent**: Performance relies on optimized parameters
3. **No BTC Correlation**: Doesn't account for Bitcoin market direction
4. **Many Parameters**: Requires careful monitoring and adjustment
5. **Orderbook Dependency**: Requires orderbook data availability

---

## 8. Recommended Usage Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Trending Market** | Default configuration | Momentum strategies excel in trends |
| **Ranging Market** | Adjust RMI thresholds | May generate fewer signals |
| **High Volatility** | Keep default | Volume filter helps avoid manipulation |
| **Low Volatility** | Adjust ROI table | Lower thresholds for smaller moves |

---

## 9. Summary

**Guacamole** is a sophisticated multi-indicator momentum strategy. Its core value lies in:

1. **Indicator Diversity**: Combines KAMA, MACD, RMI, SAR for comprehensive analysis
2. **Optimized Parameters**: Hyperopt results provide tested configurations
3. **Order Management**: Advanced order handling with timeout checks
4. **Multiple Exits**: ROI, trailing, and technical exits for flexibility

For quantitative traders, this demonstrates:
- Multi-indicator combination techniques
- Hyperopt parameter optimization
- Order management best practices
- Comprehensive exit strategies

**Recommendations**:
- Study the indicator combinations for learning
- Re-run hyperopt for current market conditions
- Monitor order timeout settings
- Test on various pairs before deployment

---
