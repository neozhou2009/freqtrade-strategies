# RSIBB02 Strategy Deep Dive

> **Strategy ID**: #341 (341st of 465 strategies)  
> **Strategy Type**: RSI + Bollinger Band Reversal Strategy  
> **Timeframe**: 1 Hour (1h)

---

## I. Strategy Overview

RSIBB02 is a classic reversal strategy based on the combination of RSI (Relative Strength Index) and Bollinger Bands. This strategy captures bounce opportunities when price touches the lower Bollinger Band while RSI is in oversold territory, using dual indicator filtering to reduce false signal risk. It is suitable for swing trading in range-bound markets.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 buy signal (RSI > 19 AND price < Bollinger lower band) |
| **Sell Condition** | 1 base sell signal (RSI > 83 AND price > Bollinger middle band) |
| **Protection Mechanism** | Tiered ROI + Fixed stop-loss |
| **Timeframe** | 1 Hour (1h) |
| **Dependencies** | talib, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.24140975952086036,   # Exit when 24.14% profit is reached immediately
    "13": 0.049595065708988986, # Lower to 4.96% target after 13 minutes
    "51": 0.01046521346331895,  # Lower to 1.05% target after 51 minutes
    "135": 0                    # Break-even exit after 135 minutes
}

# Stop-loss setting
stoploss = -0.12515406445006344  # Fixed stop-loss at approximately -12.5%
```

**Design Rationale**:
- Uses a tiered ROI mechanism that gradually lowers profit expectations as holding time increases
- Initial ROI target is high at 24.14%, showing the strategy seeks quick, substantial gains
- Stop-loss is set at -12.5%, providing room for price fluctuation

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'limit',
    'stoploss_on_exchange': False
}

order_time_in_force = {
    'buy': 'gtc',
    'sell': 'gtc',
}
```

**Design Rationale**:
- Uses limit orders exclusively to reduce slippage costs
- Stop-loss is executed locally rather than on the exchange, suitable for non-24/7 monitoring scenarios

---

## III. Buy Condition Details

### 3.1 Buy Signal Logic

The strategy employs a single buy condition that requires two technical indicator conditions to be met simultaneously:

```python
# Buy condition
(
    (dataframe['rsi'] > 19) &
    (dataframe["close"] < dataframe['bb_lowerband'])
)
```

#### Condition Analysis

| Condition | Description | Technical Meaning |
|-----------|-------------|-------------------|
| RSI > 19 | RSI not below 19 | Avoids extreme oversold conditions, confirms rebound potential |
| Close < BB Lower | Close price below lower Bollinger Band | Price is at statistical low (4 standard deviations) |

### 3.2 Buy Signal Characteristics

**Bollinger Band Parameters**:
- Period: 20 candles
- Standard deviation multiplier: 4x (wider than the typical 2x)

**Signal Interpretation**:
- The 4x standard deviation lower Bollinger Band is extremely wide; price touching the lower band is an extreme anomaly event
- RSI > 19 filters out the most extreme oversold situations, avoiding catching a falling knife
- The combination of these two conditions forms a "deep dip rebound" entry logic

---

## IV. Sell Logic Details

### 4.1 Tiered ROI Take-Profit System

The strategy uses a four-level dynamic take-profit mechanism:

```
Holding Time       Target Profit Rate
───────────────────────────────────────
0 minutes          24.14%
13 minutes         4.96%
51 minutes         1.05%
135 minutes        0% (break-even)
```

**Take-Profit Logic**:
- Strategy has high expectations for quick profits, with initial target as high as 24%
- Profit targets decrease rapidly as time progresses
- Break-even exit after 2 hours 15 minutes avoids prolonged capital occupation

### 4.2 Technical Sell Signal

```python
# Sell condition
(
    (dataframe['rsi'] > 83) &
    (dataframe["close"] > dataframe['bb_middleband'])
)
```

#### Sell Condition Analysis

| Condition | Description | Technical Meaning |
|-----------|-------------|-------------------|
| RSI > 83 | RSI exceeds 83 | Entering overbought territory, rebound may be ending |
| Close > BB Middle | Close price above middle Bollinger Band | Price has reverted to mean, rebound essentially complete |

**Design Intent**:
- RSI > 83 is a classic overbought signal, suggesting short-term rally may be overextended
- Price returning above the middle Bollinger Band indicates it has recovered from extreme lows to normal range
- Dual confirmation prevents premature exit

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|--------------------|---------------------|------------|---------|
| Momentum | RSI | Default 14-period | Determine overbought/oversold conditions |
| Trend | Bollinger Bands | 20-period, 4x standard deviation | Identify price boundaries |

### 5.2 Indicator Calculation Details

**RSI Calculation**:
```python
dataframe['rsi'] = ta.RSI(dataframe)  # Using TA-Lib default 14-period
```

**Bollinger Band Calculation**:
```python
bollinger = qtpylib.bollinger_bands(
    qtpylib.typical_price(dataframe),  # Using typical price (high+low+close)/3
    window=20,                          # 20-period
    stds=4                               # 4x standard deviation
)
dataframe['bb_lowerband'] = bollinger['lower']
dataframe['bb_middleband'] = bollinger['mid']
dataframe['bb_upperband'] = bollinger['upper']
```

**Key Parameter Analysis**:
- 4x standard deviation Bollinger Bands are the distinctive feature of this strategy
- Standard Bollinger Bands use 2x standard deviation; 4x means a much wider lower band
- Only extreme market conditions will touch the lower band, reducing signal frequency but improving quality

---

## VI. Risk Management Features

### 6.1 Fixed Stop-Loss Protection

```python
stoploss = -0.12515406445006344  # Approximately -12.5%
```

**Design Features**:
- Fixed stop-loss at approximately 12.5%, which is moderately tight for a swing strategy
- Works with tiered ROI to form a "quick profit, controlled loss" risk framework
- Stop-loss magnitude is smaller than initial ROI target (24%), providing a foundation for positive expectation

### 6.2 Tiered ROI Risk Control

| Time Point | ROI Target | Risk Implication |
|------------|------------|------------------|
| 0 minutes | 24.14% | Quick profit, no greed |
| 13 minutes | 4.96% | Moderate concession, lock in gains |
| 51 minutes | 1.05% | Minimum profit, ensure win rate |
| 135 minutes | 0% | Time stop, capital turnover |

**Risk Control Logic**:
- Dynamic take-profit over time dimension, lowering expectations as holding extends
- Avoids prolonged capital lock-up, improves capital efficiency

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Simple and Clear Logic**: RSI + Bollinger Band combination is classic technical analysis, easy to understand and verify
2. **High Signal Quality**: 4x standard deviation Bollinger Bands filter out significant noise
3. **Controllable Risk**: Tiered ROI + fixed stop-loss provides dual protection with defined maximum loss
4. **Concise Code**: Strategy code is only about 100 lines, low maintenance cost

### ⚠️ Limitations

1. **Single Signal Dependency**: Only one buy signal, lacks signal diversity
2. **Weak Trend Adaptation**: Pure reversal strategy, may experience consecutive stop-losses in trending markets
3. **No Trailing Stop**: Fixed stop-loss cannot move up to protect profits as gains grow
4. **Overfitting Signs**: ROI values are precise to many decimal places, suggesting optimization overfitting risk

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|--------------------|---------------------------|-------|
| Range-bound market | Default configuration | Strategy is designed for oversold bounces, best in ranging markets |
| Slow bull market | Reduce position | May miss main uptrend, needs pairing with trend strategy |
| One-way downtrend | Use cautiously | Rebound strategies prone to frequent stop-losses in bear markets |
| High volatility | Appropriately widen stop-loss | Increase stop-loss space for extreme fluctuations |

---

## IX. Applicable Market Environment Details

RSIBB02 is a typical **range-bound market reversal strategy**. Based on its code architecture and technical indicator combination, it is best suited for **range-bound markets with clear support and resistance**, and performs poorly in trending markets.

### 9.1 Strategy Core Logic

- **Deep Dip Rebound**: Captures mean reversion opportunities after price deviates significantly
- **Dual Indicator Filtering**: RSI confirms momentum, Bollinger Bands confirm position
- **Quick Take-Profit**: Tiered ROI design encourages quick profit realization

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:-----------------|
| 📈 One-way uptrend | ⭐⭐☆☆☆ | Reversal strategy misses main rally, high risk of being left behind |
| 🔄 Range-bound market | ⭐⭐⭐⭐⭐ | Best scenario, consistent profit from buying low and selling high |
| 📉 One-way downtrend | ⭐⭐☆☆☆ | Rebounds may fail, frequent stop-losses |
| ⚡️ High volatility | ⭐⭐⭐☆☆ | May trigger extreme conditions, but stop-loss protection may be insufficient |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| Trading pair selection | Major coins + oscillating coins | Select assets with regular price fluctuations |
| Position management | 5-10% per position | Reversal strategies require controlled single-trade risk |
| Maximum open positions | 3-5 | Avoid spreading focus across too many signals |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Curve

RSIBB02 is one of the **most concise strategies** among 465 strategies, with only about 100 lines of code. Beginners can easily understand its logic, making it suitable as an introductory learning case.

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 1 GB | 2 GB |
| 11-30 pairs | 2 GB | 4 GB |
| 31+ pairs | 4 GB | 8 GB |

**Note**: Strategy has minimal computational requirements, almost no hardware demands.

### 10.3 Backtest vs Live Trading Differences

- **Backtest Advantage**: Simple strategies backtest quickly, easy to verify
- **Live Trading Risk**: Oversold rebounds rely on market liquidity, slippage may be significant in extreme conditions
- **Recommendation**: Verify with historical data first, then test with small positions in live trading

### 10.4 Manual Trading Suggestions

RSIBB02's trading logic can be executed manually:
1. Set up a 1-hour timeframe chart
2. Add RSI(14) and Bollinger Bands(20, 4)
3. Consider buying when price touches lower Bollinger Band and RSI > 19
4. Sell when RSI > 83 or price returns to middle Bollinger Band

---

## XI. Summary

**RSIBB02** is a concise and effective deep dip rebound strategy. Its core value lies in:

1. **Clear Logic**: RSI + Bollinger Band combination is classic technical analysis, easy to understand and execute
2. **Controllable Risk**: Tiered ROI + fixed stop-loss forms a complete risk framework
3. **Simple Maintenance**: Minimal code, suitable for learning and further development

For quantitative traders, RSIBB02 is an excellent introductory strategy that can serve as a starting point for learning strategy development frameworks. However, note that this strategy is better suited for range-bound markets and should be used alongside other strategies in trending markets.

---