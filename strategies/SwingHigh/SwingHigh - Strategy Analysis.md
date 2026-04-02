# SwingHigh Strategy In-Depth Analysis

> **Strategy ID**: #403 (403rd of 465 strategies)  
> **Strategy Type**: MACD + CCI Dual-Indicator Trend Following Strategy  
> **Timeframe**: 30 Minutes (30m)

---

## I. Strategy Overview

SwingHigh is a trend reversal capture strategy based on MACD and CCI indicators. Its core concept is to use MACD for trend direction and CCI extremes to identify oversold/overbought zones, seeking pullback entry opportunities during trend continuation.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 independent buy signal, MACD golden cross + CCI oversold combination |
| **Sell Conditions** | 1 basic sell signal, MACD death cross + CCI overbought combination |
| **Protection Mechanism** | Trailing stop mechanism to protect profit drawdowns |
| **Timeframe** | 30m primary timeframe |
| **Dependencies** | talib, qtpylib, numpy, pandas |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {"0": 0.16035, "23": 0.03218, "54": 0.01182, "173": 0}

# Stop loss setting
stoploss = -0.22274

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.08
trailing_stop_positive_offset = 0.10
trailing_only_offset_is_reached = True
```

**Design Philosophy**:
- **Tiered ROI**: From 16% to 0%, lowering profit targets as holding time increases, encouraging longer holds
- **Larger Stop Loss Space**: -22.27% stop loss gives the strategy enough "breathing room" to avoid being stopped out by normal fluctuations
- **Trailing Stop Mechanism**: Activates when profit reaches 10%, trailing distance of 8%, locking in most gains

### 2.2 Order Type Configuration

The strategy uses Freqtrade's default order type configuration.

---

## III. Buy Conditions Detailed

### 3.1 Single Buy Signal

#### Condition #1: MACD Golden Cross + CCI Extreme Oversold
```python
# Logic
- MACD line > MACD signal line (MACD golden cross state)
- CCI(13) <= -188.0 (extreme oversold)
- Volume > 0 (exclude invalid data)
```

**Design Philosophy**:
- MACD golden cross confirms upward trend
- CCI extreme oversold (-188) means price has deeply pulled back, presenting a rebound opportunity
- Dual confirmation avoids false signals

---

## IV. Sell Logic Detailed

### 4.1 Single Sell Signal

#### Signal #1: MACD Death Cross + CCI Extreme Overbought
```python
# Logic
- MACD line < MACD signal line (MACD death cross state)
- CCI(76) >= 231.0 (extreme overbought)
- Volume > 0 (exclude invalid data)
```

**Design Philosophy**:
- The CCI period for selling (76) is larger than for buying (13), reflecting a "fast in, slow out" approach
- CCI threshold of 231 is very high, only capturing extreme overbought conditions
- MACD death cross confirms trend reversal

### 4.2 Trailing Stop Mechanism

The strategy is configured with a comprehensive trailing stop:

| Parameter | Value | Description |
|-----------|-------|-------------|
| trailing_stop | True | Enable trailing stop |
| trailing_stop_positive | 0.08 | Trailing distance 8% |
| trailing_stop_positive_offset | 0.10 | Activates after 10% profit |
| trailing_only_offset_is_reached | True | Only trails after threshold reached |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Trend | MACD (default parameters) | Determine trend direction |
| Oscillator | CCI(13) for buying | Identify oversold entry points |
| Oscillator | CCI(76) for selling | Identify overbought exit points |

### 5.2 Indicator Parameter Differential Design

The strategy cleverly uses different CCI periods:
- **Buy CCI Period = 13**: Quick response to oversold signals
- **Sell CCI Period = 76**: Smooth out fluctuations, avoid premature selling

---

## VI. Risk Management Features

### 6.1 Trailing Stop Protection

Trailing stop is the core risk management mechanism of this strategy:

- Automatically activates when profit reaches 10%
- Stop loss line follows price increases, maintaining an 8% distance
- Locks in most profits, avoiding excessive drawdowns

### 6.2 Large Stop Loss Space

The -22.27% stop loss gives the strategy sufficient volatility tolerance, avoiding being stopped out by normal pullbacks.

### 6.3 Tiered Profit Taking

ROI tiered design:
- 0-23 minutes: Target 16%
- 23-54 minutes: Target 3.2%
- 54-173 minutes: Target 1.2%
- After 173 minutes: Allow 0 profit exit

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Clear Logic**: MACD + CCI dual confirmation, clear signals
2. **Fast In, Slow Out**: Buy with fast-period CCI, sell with slow-period CCI, aligning with trend following philosophy
3. **Trailing Stop**: Protects profits while allowing upside room
4. **Simple Parameters**: No over-optimization, avoiding overfitting

### ⚠️ Limitations

1. **Single Signal**: Only one buy/sell logic, adaptability may be limited
2. **Extreme Thresholds**: CCI thresholds (-188/231) are extreme, signals may be infrequent
3. **Ranging Market Risk**: Trend strategies may face frequent stop losses in sideways ranging markets

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Clear Trend | Default configuration | Best performance when trend is clear |
| Ranging Market | Adjust CCI thresholds | Can loosen CCI thresholds to increase signals |
| High Volatility | Increase stop loss | Consider adjusting stop loss to -25% or lower |

---

## IX. Applicable Market Environment Details

SwingHigh is a classic trend following strategy. Based on its code architecture and design philosophy, it is best suited for **markets with clear trends**, while performance may suffer in ranging markets.

### 9.1 Strategy Core Logic

- **MACD Trend Determination**: Confirms overall direction
- **CCI Extreme Capture**: Finds pullback entry points within trends
- **Fast In, Slow Out Design**: Quick entry response, patient exit

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:-----------|:------------------|:----------------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | MACD golden cross confirms trend, CCI oversold captures pullback entries |
| 📉 Clear Downtrend | ⭐⭐☆☆☆ | Strategy primarily goes long, cannot short in downtrend |
| 🔄 Wide Range | ⭐⭐⭐☆☆ | May face repeated stop losses in ranging markets, but large stop loss provides buffer |
| ⚡️ Narrow Sideways | ⭐☆☆☆☆ | CCI extremes rarely trigger, signals are scarce |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|--------------|-------------------|-------------|
| Stop Loss | -0.22 ~ -0.25 | Maintain larger stop loss space |
| Trailing Stop | Keep enabled | Key to locking in profits |
| CCI Buy Threshold | -180 ~ -200 | Can adjust based on market volatility |
| CCI Sell Threshold | 200 ~ 250 | Can adjust based on market volatility |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

SwingHigh has simple logic that is easy for beginners to understand. However, familiarity with MACD and CCI indicator characteristics is required.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

### 10.3 Differences Between Backtesting and Live Trading

Note when backtesting:
- CCI extreme thresholds may trigger more frequently in historical data
- Trailing stop execution may have subtle differences between backtesting and live trading
- Recommended to test on demo account for at least 1 month

### 10.4 Manual Trader Recommendations

If you want to manually apply this strategy:
1. Observe 30-minute MACD golden cross
2. Wait for CCI(13) to drop below -188
3. After entry, set trailing stop activated at 10% profit
4. Patiently wait for CCI(76) to rise above 231 before considering exit

---

## XI. Summary

**SwingHigh** is a concise and efficient trend following strategy. Its core value lies in:

1. **Simple Logic**: MACD + CCI dual indicators, easy to understand and debug
2. **Fast In, Slow Out**: Quick entry response, patient exit, aligning with trend trading philosophy
3. **Complete Protection**: Trailing stop effectively locks in profits

For quantitative traders, this is a strategy suitable for beginner learning, and can also serve as a primary strategy during trending markets. However, caution is needed in ranging markets, and it is recommended to use in combination with other strategies.

---