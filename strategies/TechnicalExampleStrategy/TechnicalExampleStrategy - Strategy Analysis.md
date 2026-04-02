# TechnicalExampleStrategy Strategy Deep Dive

> **Strategy Number**: #407 (407th of 465 strategies)  
> **Strategy Type**: Single-Indicator Reversal Strategy  
> **Timeframe**: 5 minutes (5m)

---

## 1. Strategy Overview

TechnicalExampleStrategy is an ultra-minimalist money flow reversal strategy. It uses only the Chaikin Money Flow (CMF) indicator to determine buy and sell timing, with very simple core logic: buy when money flows out, sell when money flows in.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 independent buy signal (CMF < 0) |
| **Sell Condition** | 1 basic sell signal (CMF > 0) |
| **Protection Mechanism** | Only basic stop-loss, no additional protection |
| **Timeframe** | 5 minutes (5m) |
| **Dependencies** | technical.indicators (cmf) |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.01  # Exit at 1% profit
}

# Stop-loss setting
stoploss = -0.05  # 5% stop-loss
```

**Design Philosophy**:
- Uses ultra-simple ROI setting, exit immediately at 1% profit
- Stop-loss set at -5%, relatively conservative risk control
- No trailing stop, strategy pursues quick profit-taking

### 2.2 Order Type Configuration

This strategy does not specify order types and uses default configuration.

---

## 3. Buy Condition Details

### 3.1 Protection Mechanism

This strategy has no special protection mechanism, relying only on basic stop-loss.

### 3.2 Buy Condition Details

#### Condition #1: CMF Money Outflow Signal

```python
# Logic
- CMF(21) < 0  # Money outflow state
```

**Core Indicator Explanation**:

| Indicator | Parameter | Purpose |
|-----------|-----------|---------|
| CMF (Chaikin Money Flow) | Period 21 | Measures money inflow/outflow |

**Chaikin Money Flow (CMF) Indicator Principle**:
- CMF was developed by Marc Chaikin to measure buying and selling pressure
- CMF > 0 indicates money inflow (strong buyer power)
- CMF < 0 indicates money outflow (strong seller power)
- Value range is between -1 and +1

**Strategy Logic Interpretation**:
When CMF < 0, it means the market is in a money outflow state, and the price may be undervalued. The strategy chooses to buy at this point, betting on a reversal of the money outflow.

---

## 4. Sell Logic Details

### 4.1 Sell Signal

```python
# Sell signal: CMF money inflow
- CMF(21) > 0  # Money inflow state
```

**Logic Interpretation**:
When CMF > 0, market money starts flowing in, seller pressure weakens, and buyer power increases. At this point, the strategy chooses to sell to realize profits.

### 4.2 ROI Exit Mechanism

| Profit Rate | Trigger Time | Description |
|-------------|--------------|-------------|
| 1% | Any time | Exit upon reaching |

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Volume Indicator | CMF (Chaikin Money Flow) | Money flow direction determination |

### 5.2 CMF Indicator Details

**Chaikin Money Flow (CMF)** is a volume-weighted price momentum indicator:

```
CMF = Σ(Buying/Selling Power × Volume) / Σ(Volume)
```

Where buying/selling power is calculated:
```
Buying/Selling Power = ((Close - Low) - (High - Close)) / (High - Low)
```

**Key Parameters**:
- Period: 21 (approximately 1.75 hours of 5-minute candles)
- Signal threshold: 0 (positive/negative boundary)

---

## 6. Risk Management Features

### 6.1 Minimalist Risk Control

The strategy uses the most basic risk management approach:

| Risk Control Type | Parameter Value | Description |
|------------------|-----------------|-------------|
| Stop-loss | -5% | Maximum loss per trade |
| Take-profit | 1% | Target profit per trade |
| Trailing Stop | None | Not enabled |

### 6.2 Risk Characteristics

- **Low complexity**: Relies only on a single indicator, clear logic
- **Counter-trend trading**: Buys during money outflow, a counter-trend bottom-fishing strategy
- **Quick in and out**: 1% take-profit + CMF reversal sell, pursues quick turnover

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Minimalist design**: Only about 40 lines of code, easy to understand and maintain
2. **Clear logic**: Single indicator, clear buy and sell conditions
3. **Money flow oriented**: Uses volume information to capture market money flow changes

### ⚠️ Limitations

1. **Single indicator risk**: Only relies on CMF, lacks multi-dimensional validation
2. **Counter-trend bottom-fishing risk**: Buying during money outflow may catch a falling knife
3. **No protection mechanism**: No trailing stop, may give back profits after reversal
4. **False signal risk**: CMF may frequently generate false signals in ranging markets

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Ranging Market | Use with caution | CMF may frequently cross zero line |
| One-way Downtrend | Not recommended | High risk of counter-trend bottom-fishing |
| Reversal Market | Worth trying | Potential rebound after money outflow bottoms |
| Learning Research | Recommended | Excellent for strategy learning and introduction |

---

## 9. Applicable Market Environment Details

TechnicalExampleStrategy is an ultra-minimalist teaching example strategy. Based on its code architecture and single indicator characteristics, it is best suited for **learning and research purposes**, while performance in live trading may be unstable.

### 9.1 Strategy Core Logic

- **Counter-trend buying**: Buys during money outflow, betting on reversal
- **Trend-following selling**: Sells during money inflow, locking in profits
- **Quick turnover**: 1% take-profit, pursuing quick profit realization

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:------------------|:----------------|
| 📈 Slow Bull | ⭐⭐☆☆☆ | Counter-trend buying logic contradicts trend |
| 🔄 Ranging | ⭐⭐⭐☆☆ | Money flow frequently changes in ranging markets |
| 📉 Downtrend | ⭐☆☆☆☆ | Extremely high counter-trend bottom-fishing risk |
| ⚡ Reversal | ⭐⭐⭐⭐☆ | Suitable for catching bottom reversal signals |

### 9.3 Key Configuration Recommendations

| Configuration Item | Suggested Value | Description |
|-------------------|-----------------|-------------|
| Stop-loss | -3% to -5% | Adjust based on risk preference |
| Take-profit | 1% to 2% | Maintain quick turnover |
| CMF Period | 14 to 21 | Try different periods |

---

## 10. Important Reminder: Strategy Positioning

### 10.1 Teaching Example Nature

This strategy is named "TechnicalExampleStrategy", indicating its positioning from the name:

- **Official Example**: Serves as a teaching example for technical indicator usage
- **Not Production Ready**: Not recommended for direct live trading
- **Learning Value**: Excellent for understanding CMF indicator and strategy writing framework

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 1GB | 2GB |
| 10-50 pairs | 2GB | 4GB |

The strategy is minimalist with very low hardware requirements.

### 10.3 Improvement Suggestions

If used for live trading, consider the following improvements:

1. **Add filter conditions**: Combine with trend indicators (e.g., EMA, ADX) to filter false signals
2. **Adjust CMF threshold**: Don't use 0 as threshold, use more extreme values (e.g., buy at -0.1)
3. **Add trailing stop**: Protect realized profits
4. **Add volume filter**: Ensure sufficient liquidity

---

## 11. Summary

**TechnicalExampleStrategy** is an ultra-minimalist money flow reversal strategy example. Its core value lies in:

1. **Teaching demonstration**: Shows how to use custom technical indicator libraries
2. **Clean code**: Excellent starting point for learning Freqtrade strategy writing
3. **Clear logic**: Single indicator buy/sell logic, easy to understand

For quantitative trading learners, this is an excellent introductory strategy; however, for live trading, it's recommended to add more filter conditions and improve risk management mechanisms on this foundation.

---

*Strategy Number: #407*