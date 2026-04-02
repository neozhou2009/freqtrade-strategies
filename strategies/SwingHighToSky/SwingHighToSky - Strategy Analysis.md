# SwingHighToSky Strategy In-Depth Analysis

> **Strategy ID**: #404 (404th of 465 strategies)  
> **Strategy Type**: CCI + RSI Dual-Indicator Hyperopt Optimized Strategy  
> **Timeframe**: 15 Minutes (15m)

---

## I. Strategy Overview

SwingHighToSky is an enhanced version of the SwingHigh strategy, using CCI and RSI dual-indicator combination, with parameter dynamic adjustment through the Hyperopt optimization framework. Its core concept is to use CCI to identify oversold/overbought zones, combined with RSI to confirm momentum strength, achieving more precise entries and exits.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 independent buy signal, CCI oversold + RSI oversold combination |
| **Sell Conditions** | 1 basic sell signal, CCI overbought + RSI overbought combination |
| **Protection Mechanism** | Hyperopt optimizable parameters, adaptive to market changes |
| **Timeframe** | 15m primary timeframe |
| **Dependencies** | talib, qtpylib, numpy, pandas |
| **Interface Version** | IStrategy INTERFACE_VERSION = 2 |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {"0": 0.27058, "33": 0.0853, "64": 0.04093, "244": 0}

# Stop loss setting
stoploss = -0.34338
```

**Design Philosophy**:
- **Aggressive ROI**: Initial target of 27%, more aggressive than SwingHigh
- **Larger Stop Loss**: -34.34% stop loss space, suitable for high volatility markets
- **Longer Holding**: Maximum 244 minutes (about 4 hours), encouraging trend following

### 2.2 Hyperopt Parameter Optimization Configuration

The strategy uses IntParameter for parameter optimization:

```python
# Buy parameters
buy_cci = IntParameter(low=-200, high=200, default=100, space='buy', optimize=True)
buy_cciTime = IntParameter(low=10, high=80, default=20, space='buy', optimize=True)
buy_rsi = IntParameter(low=10, high=90, default=30, space='buy', optimize=True)
buy_rsiTime = IntParameter(low=10, high=80, default=26, space='buy', optimize=True)

# Sell parameters
sell_cci = IntParameter(low=-200, high=200, default=100, space='sell', optimize=True)
sell_cciTime = IntParameter(low=10, high=80, default=20, space='sell', optimize=True)
sell_rsi = IntParameter(low=10, high=90, default=30, space='sell', optimize=True)
sell_rsiTime = IntParameter(low=10, high=80, default=26, space='sell', optimize=True)
```

### 2.3 Optimized Parameter Values

```python
# Buy hyperspace params:
buy_params = {
    "buy_cci": -175,
    "buy_cciTime": 72,
    "buy_rsi": 90,
    "buy_rsiTime": 36,
}

# Sell hyperspace params:
sell_params = {
    "sell_cci": -106,
    "sell_cciTime": 66,
    "sell_rsi": 88,
    "sell_rsiTime": 45,
}
```

---

## III. Buy Conditions Detailed

### 3.1 Single Buy Signal

#### Condition #1: CCI Oversold + RSI Oversold
```python
# Logic
- CCI(72) < -175 (oversold zone)
- RSI(36) < 90 (confirm momentum weakness)
```

**Design Philosophy**:
- CCI period 72 is relatively long, filtering short-term noise
- CCI threshold -175 is extreme, seeking deep pullbacks
- RSI < 90 is a loose condition; normal RSI range is 0-100, so this may be a special usage

**Note**: The RSI condition `< 90` appears to be a very loose condition (since RSI normally ranges from 0-100), practically always satisfied. This may mean buy signals are primarily determined by CCI.

---

## IV. Sell Logic Detailed

### 4.1 Single Sell Signal

#### Signal #1: CCI Overbought + RSI Overbought
```python
# Logic
- CCI(66) > -106 (note: this is a negative value, not traditional overbought)
- RSI(45) > 88 (near overbought zone)
```

**Design Philosophy**:
- CCI sell threshold is -106, an interesting setting
- Normal CCI overbought should be >100, but here -106 is used
- This means sell signals may trigger even when CCI is still in negative territory

**Parameter Comparison Analysis**:

| Parameter | Buy | Sell | Analysis |
|-----------|-----|------|----------|
| CCI Period | 72 | 66 | Buy uses longer period, more stable |
| CCI Threshold | -175 | -106 | Buy more extreme, sell looser |
| RSI Period | 36 | 45 | Sell uses longer period |
| RSI Threshold | 90 | 88 | Similar thresholds |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Oscillator | CCI(72) for buying | Identify oversold entry points |
| Oscillator | CCI(66) for selling | Identify exit points |
| Momentum | RSI(36) for buying | Confirm momentum state |
| Momentum | RSI(45) for selling | Confirm momentum state |

### 5.2 Indicator Calculation Optimization

The strategy uses loops to pre-calculate all possible indicator values:

```python
# Buy indicators
for val in self.buy_cciTime.range:
    dataframe[f'cci-{val}'] = ta.CCI(dataframe, timeperiod=val)
for val in self.buy_rsiTime.range:
    dataframe[f'rsi-{val}'] = ta.RSI(dataframe, timeperiod=val)

# Sell indicators
for val in self.sell_cciTime.range:
    dataframe[f'cci-sell-{val}'] = ta.CCI(dataframe, timeperiod=val)
for val in self.sell_rsiTime.range:
    dataframe[f'rsi-sell-{val}'] = ta.RSI(dataframe, timeperiod=val)
```

This design supports Hyperopt quickly switching different period parameters without recalculation.

---

## VI. Risk Management Features

### 6.1 Hyperopt Adaptive Parameters

The strategy's biggest feature is parameter optimization:

| Parameter Space | Range | Description |
|----------------|-------|-------------|
| CCI Threshold | -200 ~ 200 | Covers extreme oversold to extreme overbought |
| CCI Period | 10 ~ 80 | Short-term to medium-term |
| RSI Threshold | 10 ~ 90 | Oversold to overbought |
| RSI Period | 10 ~ 80 | Short-term to medium-term |

### 6.2 Large Stop Loss Space

The -34.34% stop loss gives the strategy sufficient volatility tolerance:
- Suitable for high volatility markets
- Reduces probability of being stopped out by normal pullbacks
- Requires larger capital management coordination

### 6.3 Tiered Profit Taking

ROI tiered design:
- 0-33 minutes: Target 27%
- 33-64 minutes: Target 8.5%
- 64-244 minutes: Target 4.1%
- After 244 minutes: Allow 0 profit exit

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Optimizable Parameters**: Hyperopt framework supports automatic finding of optimal parameters
2. **Dual Indicator Confirmation**: CCI + RSI dual confirmation, more reliable signals
3. **Flexible Adaptation**: Can re-optimize parameters based on market changes
4. **Large Stop Loss Space**: Suitable for high volatility markets

### ⚠️ Limitations

1. **Overfitting Risk**: Parameter optimization may lead to overfitting historical data
2. **Loose RSI Condition**: RSI < 90 condition is almost always satisfied, actual signals determined by CCI
3. **Strange CCI Sell Threshold**: Sell threshold -106 is negative, inconsistent with traditional overbought definition
4. **No Trailing Stop**: Compared to SwingHigh, lacks trailing stop protection

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| High Volatility Market | Default configuration | Large stop loss space suitable for high volatility |
| Trending Market | Re-Hyperopt | Optimize parameters based on current market |
| Low Volatility Market | Reduce stop loss | -34% stop loss may be too large |

---

## IX. Applicable Market Environment Details

SwingHighToSky is a CCI + RSI strategy with optimizable parameters. Based on its code architecture and Hyperopt design, it is best suited for **markets needing adaptive adjustment**, while performance may decline in overfitting situations.

### 9.1 Strategy Core Logic

- **CCI Oversold Capture**: Seeks deep pullback entry points
- **RSI Confirmation**: Assists in confirming momentum state
- **Hyperopt Optimization**: Parameters can be adjusted based on market changes

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:-----------|:------------------|:----------------|
| 📈 Clear Trend | ⭐⭐⭐⭐☆ | Can capture pullbacks in trends, but lacks trailing stop |
| 🔄 Volatile Market | ⭐⭐⭐⭐⭐ | Can adapt through Hyperopt parameter adjustment |
| 📉 Downtrend | ⭐⭐☆☆☆ | Long only, cannot profit in downtrends |
| ⚡️ Sideways Market | ⭐⭐⭐☆☆ | CCI extremes may trigger, but effectiveness is average |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|--------------|-------------------|-------------|
| Hyperopt Space | buy, sell | Optimize buy and sell parameters |
| Backtest Period | 90-180 days | Avoid overfitting to recent data |
| Stop Loss | -0.30 ~ -0.35 | Maintain large stop loss space |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

SwingHighToSky introduces the Hyperopt parameter optimization framework, requiring understanding of:
- Freqtrade's Hyperopt mechanism
- Parameter space definition
- Overfitting risks

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

### 10.3 Differences Between Backtesting and Live Trading

Hyperopt optimization notes:
- **Overfitting Risk**: Optimized parameters may only apply to historical data
- **Look-Ahead Bias**: Ensure Hyperopt doesn't use future data
- **Regular Re-optimization**: Parameters may become invalid after market changes

### 10.4 Manual Trader Recommendations

If you want to manually apply this strategy:
1. Add CCI(72) and RSI(36) on 15-minute charts
2. Wait for CCI to drop below -175
3. Confirm RSI < 90 (usually always satisfied)
4. After entry, set stop loss at -34%
5. Exit when CCI(66) > -106 and RSI(45) > 88

---

## XI. Summary

**SwingHighToSky** is a parameter-optimizable CCI + RSI strategy. Its core value lies in:

1. **Adaptive Capability**: Hyperopt framework supports parameter optimization
2. **Dual Indicator Confirmation**: CCI + RSI combined signals
3. **Flexible Configuration**: Parameters can be adjusted based on market changes

For quantitative traders, this is a beginner-friendly strategy for learning Hyperopt optimization. However, note:
- Regularly re-optimize parameters
- Avoid overfitting
- Recommend adding trailing stop mechanism

---