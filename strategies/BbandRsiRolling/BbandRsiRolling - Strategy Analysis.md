# BbandRsiRolling Strategy Analysis

> **Strategy Number**: #52  
> **Strategy Type**: Rolling RSI Optimized Trend Reversal Strategy  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

BbandRsiRolling is an optimized variant of the BbandRsi strategy, developed by Michael Fourie. This strategy introduces the concept of Rolling RSI on top of the original version, identifying more stable oversold states by calculating the minimum value of RSI over the past N candles. This improvement allows the strategy to better filter out false signals caused by short-term fluctuations, improving entry signal quality.

Compared to the original BbandRsi, BbandRsiRolling adopts a shorter 5-minute timeframe, making the strategy more sensitive and able to capture shorter-term trading opportunities. Meanwhile, the strategy's ROI table has become more complex, containing multiple take-profit gradients, reflecting the author's efforts to optimize parameters through historical backtesting.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 1 independent entry signal (Rolling RSI minimum < 37 and price breaks below lower Bollinger Band) |
| **Exit Conditions** | 0 (relies entirely on ROI mechanism for exit) |
| **Protection** | No independent protection parameter group |
| **Timeframe** | 5 minutes (high-frequency trading) |
| **Dependencies** | talib, technical |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
minimal_roi = {
    "0": 0.03279,
    "259": 0.02964,
    "536": 0.02467,
    "818": 0.02326,
    "965": 0.01951,
    "1230": 0.01492,
    "1279": 0.01502,
    "1448": 0.00945,
    "1525": 0.00698,
    "1616": 0.00319,
    "1897": 0
}

stoploss = -0.08
```

**Design Logic**:

This is a carefully optimized ROI table containing 11 take-profit gradients. The overall design philosophy is **"fast in, fast out"**, with higher early take-profit targets (3.279%), gradually reducing take-profit targets as holding time extends. This design reflects the following strategy logic:

1. **Early Quick Profits**: Short-term after opening (0-259 minutes, about 4.3 hours) set 3.279% take-profit target
2. **Mid-term Moderate Returns**: Holding 259-1230 minutes (about 4-20 hours) take-profit target reduces to 1.5-3%
3. **Long-term Minimal Exit**: Holding over 1600 minutes (about 27 hours), take-profit target reduces to around 0.3%

The stoploss is set at -8%, which is a relatively tight stoploss range. Combined with the 5-minute high-frequency timeframe, the strategy can quickly identify and exit losing positions.

---

## III. Entry Conditions Details

### 3.1 Condition Analysis

```python
# Entry condition
(dataframe['rsi'].rolling(8).min() < 37) & (dataframe['close'] < dataframe['bb_lowerband'])
```

**Condition Details**:

**Condition One: Rolling RSI Minimum < 37**

- Uses an 8-candle rolling window to calculate RSI minimum value
- Traditional RSI < 30 may be overly sensitive,easily produces false signals
- Rolling RSI.min() < 37 requires at least 1 candle in the past 8 candles to have RSI below 37
- This ensures the market is indeed in a relatively weak state

**Condition Two: Close Price < Lower Bollinger Band**

- Same logic as original BbandRsi
- Price breaking below lower Bollinger Band means price is at a relatively low position
- Expects price to regress to the Bollinger Band middle band

**Dual Confirmation Mechanism**:

This combination ensures:
1. Momentum level: Market is in weak state (RSI condition)
2. Price level: Price is at relatively low position (Bollinger Band condition)

When both are satisfied simultaneously, entry signal reliability is significantly improved.

---

## IV. Exit Logic Explained

### 4.1 Exit Mechanism

The strategy's `populate_exit_trend` function is empty, relying entirely on the ROI mechanism for exit:

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
        ),
        'sell'] = 1
    return dataframe
```

As can be seen, exit conditions are set to empty, meaning the strategy will not have any active exit signals.

### 4.2 ROI Layered Exit Analysis

| Holding Time (minutes) | Take-Profit Threshold | Take-Profit Gradient |
|-----------------------|----------------------|---------------------|
| 0 - 259 | 3.279% | 3.279% |
| 259 - 536 | 2.964% | 2.964% |
| 536 - 818 | 2.467% | 2.467% |
| 818 - 965 | 2.326% | 2.326% |
| 965 - 1230 | 1.951% | 1.951% |
| 1230 - 1279 | 1.492% | 1.492% |
| 1279 - 1448 | 1.502% | 1.502% |
| 1448 - 1525 | 0.945% | 0.945% |
| 1525 - 1616 | 0.698% | 0.698% |
| 1616 - 1897 | 0.319% | 0.319% |
| 1897+ | 0% | Exit near cost |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Usage |
|-------------------|-------------------|-------|
| Momentum Indicator | RSI (14) | Identify oversold/overbought states |
| Momentum Indicator | RSI.rolling(8).min() | Rolling RSI minimum value |
| Trend Indicator | Bollinger Bands (20, 2) | Identify price relative position |

### 5.2 Indicator Calculation Details

**RSI Calculation**:

```python
dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
dataframe['rsi'].rolling(8).min()  # Rolling minimum
```

- RSI base period: 14 (standard setting)
- Rolling window: 8 candles (about 40 minutes)
- Condition threshold: 37 (original was 30)

**Bollinger Band Calculation**:

```python
bollinger = qtpylib.bollinger_bands(
    qtpylib.typical_price(dataframe), 
    window=20, 
    stds=2
)
```

- Exactly the same as original BbandRsi
- Uses typical price calculation
- Standard 20,2 parameters

---

## VI. Risk Management Features

### 6.1 Tight Stoploss

The -8% stoploss setting is tighter compared to original BbandRsi's -25%, meaning:

1. **Stricter Risk Control**: Maximum single trade loss is 8%
2. **Higher Accuracy Requirement**: Needs higher win rate to be profitable
3. **Suitable for High-Frequency Trading**: 5-minute framework + 8% stoploss, strategy is more agile

### 6.2 Layered Take-Profit

The 11-level ROI table design reflects the philosophy of refined risk management:

- **Early High Targets**: Capture short-term large fluctuations
- **Mid-term Balanced Targets**: Balance returns and time cost
- **Long-term Low Targets**: Ensure not holding positions too long

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Rolling RSI Filtering**: Reduces false signals from short-term fluctuations
2. **High-Frequency Trading**: 5-minute framework captures more trading opportunities
3. **Refined ROI**: Multi-level take-profit targets optimize returns
4. **Tight Stoploss**: -8% stoploss reduces maximum single trade loss
5. **Concise Code**: Maintains original strategy's simplicity

### ⚠️ Limitations

1. **No Exit Signals**: Relies entirely on ROI, may miss best exit points
2. **Over-optimization Risk**: 11-level ROI table may have overfitting
3. **High-Frequency Risk**: 5-minute framework easily affected by short-term noise
4. **No Protection Mechanisms**: Lacks common trading protection logic

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Explanation |
|-------------------|--------------------------|-------------|
| High Volatility Coins | Adjust ROI Table | Increase early take-profit in high volatility |
| Major Coins | Default Configuration | Good liquidity, low slippage |
| Trending Market | Adjust stoploss to -10% | Give trend more room |
| Range-bound Market | Keep Default | Suitable for range consolidation |

---

## IX. Applicable Market Environments Explained

### 9.1 Strategy Core Logic

- **Counter-trend Trading**: Buy at relative weakness
- **Rolling Confirmation**: Filter false signals through rolling RSI
- **Time-decreasing Take-Profit**: More conservative the longer you hold

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
| :--- | :--- | :--- |
| 📈 Uptrend | ⭐⭐⭐ | Counter-trend buying may miss main rally |
| 🔄 Range Consolidation | ⭐⭐⭐⭐ | Rolling RSI effectively filters noise |
| 📉 Downtrend | ⭐⭐ | Higher risk for counter-trend buying |
| ⚡️ High Volatility | ⭐⭐⭐⭐ | High-frequency trading captures volatility |

---

## X. Important Reminders: The Cost of Complexity

### 10.1 Backtest Risk

The 11-level ROI table likely has overfitting risk. Parameters that performed best in historical data may not be effective in the future.

### 10.2 Live Trading Considerations

- Trading fees generated by high-frequency trading cannot be ignored
- Slippage may be amplified in high-frequency environments
- Exchange API rate limits need to be considered

---

## XI. Summary

BbandRsiRolling is a targeted optimization of the original BbandRsi. It retains the core RSI + Bollinger Band logic while introducing the rolling RSI concept to filter false signals, and uses a more aggressive 5-minute timeframe to increase trading frequency.

The strategy's core value lies in:

1. **Signal Optimization**: Rolling RSI improves signal quality
2. **High-Frequency Trading**: More trading opportunities
3. **Refined Take-Profit**: Multi-level ROI optimizes returns

For traders who want to improve strategy effectiveness while maintaining simplicity, BbandRsiRolling is a choice worth trying.

---

*This document is based on the BbandRsiRolling strategy source code, for learning reference only, not investment advice.*
