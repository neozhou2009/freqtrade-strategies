# Strategy001_custom_sell In-Depth Analysis

> **Strategy Number**: #392 (392nd of 465 strategies)  
> **Strategy Type**: EMA Crossover + Heikin Ashi + RSI Custom Exit  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

Strategy001_custom_sell is an enhanced version of Strategy001, adding RSI-based custom exit conditions on top of the original EMA crossover + Heikin Ashi trend following logic. This improvement enables the strategy to actively take profits when RSI is overbought and profitable, improving capital turnover efficiency.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Condition** | 1 buy signal (same as Strategy001) |
| **Exit Condition** | 1 base exit signal + RSI custom exit |
| **Protection Mechanism** | Trailing stop mechanism + RSI overbought exit |
| **Timeframe** | 5-minute main timeframe |
| **Dependencies** | talib, qtpylib |
| **Difference from Strategy001** | Added RSI indicator + custom_sell function |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "60":  0.01,   # After 60 minutes, exit at 1% profit
    "30":  0.03,   # After 30 minutes, exit at 3% profit
    "20":  0.04,   # After 20 minutes, exit at 4% profit
    "0":   0.05    # Immediately, exit at 5% profit
}

# Stop loss setting
stoploss = -0.10   # Fixed stop loss at -10%

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01      # Activate after 1% profit
trailing_stop_positive_offset = 0.02  # Offset at 2%
```

**Design Rationale**:
- ROI table identical to Strategy001, using time decay design
- Trailing stop parameters remain consistent, balancing profit protection and trend following
- 10% fixed stop loss gives trend enough pullback room

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',           # Use limit orders for buying
    'sell': 'limit',          # Use limit orders for selling
    'stoploss': 'market',     # Use market orders for stop loss
    'stoploss_on_exchange': False
}
```

### 2.3 Exit Configuration

```python
use_sell_signal = True       # Enable signal exit
sell_profit_only = True      # Only respond to sell signal when profitable
ignore_roi_if_buy_signal = False  # ROI doesn't override buy signal
```

---

## III. Entry Conditions Detailed

### 3.1 Technical Indicators

The strategy adds RSI indicator on top of Strategy001:

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | EMA20, EMA50, EMA100 | Determine trend direction and strength |
| Candlestick | Heikin Ashi open, close | Filter noise, confirm trend |
| Oscillator | RSI (14) | Determine overbought/oversold, used for custom exit |

### 3.2 Entry Condition Logic

```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            qtpylib.crossed_above(dataframe['ema20'], dataframe['ema50']) &
            (dataframe['ha_close'] > dataframe['ema20']) &
            (dataframe['ha_open'] < dataframe['ha_close'])  # green bar
        ),
        'buy'] = 1
    return dataframe
```

**Entry Signal Trigger Conditions (same as Strategy001)**:

| Condition # | Description | Technical Meaning |
|-------------|-------------|-------------------|
| Condition 1 | EMA20 crosses above EMA50 | Short-term moving average golden cross, trend strengthening signal |
| Condition 2 | HA close > EMA20 | Price above short-term MA, confirms uptrend |
| Condition 3 | HA open < HA close | Heikin Ashi green candle, trend confirmation |

---

## IV. Exit Logic Detailed

### 4.1 Base Exit Signal (populate_exit_trend)

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            qtpylib.crossed_above(dataframe['ema50'], dataframe['ema100']) &
            (dataframe['ha_close'] < dataframe['ema20']) &
            (dataframe['ha_open'] > dataframe['ha_close'])  # red bar
        ),
        'sell'] = 1
    return dataframe
```

**Base Exit Signal Conditions**:

| Condition # | Description | Technical Meaning |
|-------------|-------------|-------------------|
| Condition 1 | EMA50 crosses above EMA100 | Medium-term trend signal |
| Condition 2 | HA close < EMA20 | Price below short-term MA |
| Condition 3 | HA open > HA close | Red candle, downtrend confirmation |

### 4.2 Custom Exit Logic (custom_sell)

This is the core enhancement of Strategy001_custom_sell:

```python
def custom_sell(self, pair: str, trade: 'Trade', current_time: 'datetime', 
                current_rate: float, current_profit: float, **kwargs):
    # Get current candlestick data
    dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
    current_candle = dataframe.iloc[-1].squeeze()
    
    # RSI overbought + profitable exit
    if (current_candle['rsi'] > 70) and (current_profit > 0):
        return "rsi_profit_sell"
    
    return None
```

**Custom Exit Trigger Conditions**:

| Condition # | Description | Technical Meaning |
|-------------|-------------|-------------------|
| Condition 1 | RSI > 70 | Overbought condition, potential pullback |
| Condition 2 | Current profit > 0 | Ensures exit only when profitable |
| Exit Reason | "rsi_profit_sell" | Facilitates log analysis and backtest statistics |

**Design Advantages**:
- **Active Profit Taking**: Locks in profits when RSI overbought, doesn't wait for trend reversal
- **Profit Protection**: Only triggers when profitable, avoids selling at a loss
- **Capital Efficiency**: Early profit taking releases capital, improves turnover rate

### 4.3 Multiple Exit Mechanisms Comparison

| Exit Mechanism | Strategy001 | Strategy001_custom_sell | Difference |
|----------------|-------------|------------------------|------------|
| ROI Exit | ✅ | ✅ | Same |
| Trailing Stop | ✅ | ✅ | Same |
| Fixed Stop Loss | ✅ | ✅ | Same |
| Signal Exit | ✅ | ✅ | Same |
| RSI Custom Exit | ❌ | ✅ | **New** |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Moving Average | EMA20 | Short-term trend, dynamic support/resistance |
| Moving Average | EMA50 | Medium-term trend, golden/death cross signals |
| Moving Average | EMA100 | Long-term trend, filter oscillations |
| Candlestick | Heikin Ashi | Filter noise, confirm trend direction |
| Oscillator | RSI (14) | Overbought/oversold determination, custom exit trigger |

### 5.2 RSI Indicator Detailed

**Relative Strength Index (RSI)** calculation formula:
```
RSI = 100 - (100 / (1 + RS))
Where RS = Average Gain / Average Loss
```

**RSI's Role in This Strategy**:
- **Period**: 14 (standard parameter)
- **Overbought Threshold**: 70 (RSI > 70 considered overbought)
- **Trigger Condition**: Overbought + profitable

**Why Choose RSI > 70**:
- RSI above 70 indicates recent gains are excessive
- May face short-term pullback or consolidation
- Actively taking profits at this point locks in gains

---

## VI. Risk Management Features

### 6.1 Triple Protection Mechanism

| Protection Layer | Mechanism | Trigger Condition | Purpose |
|-----------------|-----------|-------------------|---------|
| First Layer | RSI Custom Exit | RSI > 70 and profitable | Active profit taking, improve efficiency |
| Second Layer | Trailing Stop | 1% pullback after 2% profit | Protect profits |
| Third Layer | Fixed Stop Loss | 10% loss | Limit maximum loss |

### 6.2 Advantages of RSI Exit

**Comparison with Traditional Exit**:

| Scenario | Traditional Signal Exit | RSI Custom Exit |
|----------|------------------------|-----------------|
| Rapid Price Surge | Wait for MA death cross | Exit immediately on RSI overbought |
| Short-term Spike and Pullback | May miss the high | Take profit near the high |
| Capital Turnover | Long wait time | Early capital release |

### 6.3 Risk Parameter Summary

| Parameter | Value | Description |
|-----------|-------|-------------|
| Fixed Stop Loss | -10% | Maximum single trade loss |
| Trailing Stop Activation | +2% | Profit threshold to start trailing |
| Trailing Stop Distance | 1% | Pullback trigger value |
| Maximum Target Profit | 5% | Immediate take-profit target |
| RSI Overbought Threshold | 70 | Custom exit trigger |

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Active Profit Taking**: RSI overbought exit mechanism locks in profits early during price surges
2. **High Capital Efficiency**: Early profit taking releases capital, increases trading opportunities
3. **Maintains Simplicity**: Only adds minimal code on top of Strategy001, easy to understand and maintain

### ⚠️ Limitations

1. **RSI False Signals**: In strong trends, RSI may stay overbought for extended periods, early exit misses gains
2. **Fixed Parameters**: RSI 70 threshold may not suit all coins
3. **Trend Dependent**: Same as Strategy001, performs poorly in oscillating markets

### Comparison with Strategy001

| Dimension | Strategy001 | Strategy001_custom_sell |
|-----------|-------------|------------------------|
| Entry Signal | Same | Same |
| Exit Signal | Base exit | Base exit + RSI exit |
| Profit Taking Efficiency | Passive | Active |
| Capital Turnover | Average | Higher |
| Applicable Scenarios | Trend markets | Trend markets + Volatile markets |

---

## VIII. Applicable Scenarios Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Clear Trend Market | Default configuration | Good trend following effect |
| Volatile Market | RSI exit has advantage | Early profit taking on spikes |
| Oscillating Market | Reduce position or pause | RSI may trigger frequently |
| Strong Trend Market | Consider raising RSI threshold | Avoid early profit taking and missing gains |

---

## IX. Applicable Market Environment Detailed

Strategy001_custom_sell is an **enhanced trend-following strategy**. Adding RSI custom exit on top of Strategy001 makes it perform better in **volatile markets**.

### 9.1 Strategy Core Logic

- **Trend Identification**: EMA golden cross to identify trend initiation (same as Strategy001)
- **Trend Confirmation**: Heikin Ashi candlesticks to filter noise (same as Strategy001)
- **Active Profit Taking**: RSI overbought to lock in profits early (new)

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|-------------|-------------------|------------------|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | EMA golden cross + HA green bars + RSI profit taking work perfectly together |
| 🔄 Volatile Market | ⭐⭐⭐⭐☆ | RSI exit takes profits early on spikes |
| 📉 Downtrend | ⭐☆☆☆☆ | Counter-trend longs, very few signals |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | RSI triggers frequently, may exit too early |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| RSI Overbought Threshold | 70-80 | Can raise threshold in strong trends |
| RSI Period | 14 | Standard parameter, can adjust per coin |
| Minimum Profit Requirement | >0% | Ensure exit only when profitable |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Cost

On top of Strategy001, need to additionally understand:
- RSI indicator calculation and meaning
- How custom_sell function works
- Balance between overbought exit and trend following

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-5 pairs | 2GB | 4GB |
| 5-20 pairs | 4GB | 8GB |
| 20+ pairs | 8GB | 16GB |

### 10.3 Difference Between Backtesting and Live Trading

RSI custom exit may differ between backtesting and live trading:
- In backtesting, RSI signal triggers precisely
- In live trading, limit orders may not execute, missing optimal exit points
- In strong trends, RSI may stay overbought for extended periods, early exit causes missing gains

### 10.4 Recommendations for Manual Traders

If using this strategy's logic manually:
1. Wait for EMA20 to cross above EMA50
2. Confirm Heikin Ashi green candle
3. Price holding above EMA20
4. Set trailing stop
5. **New**: Monitor RSI, consider profit taking when above 70 and profitable

---

## XI. Summary

**Strategy001_custom_sell** is an **enhanced strategy that adds active profit taking capability to an entry-level strategy**. Its core value lies in:

1. **Active Profit Taking**: RSI overbought exit mechanism locks in profits during surges
2. **Capital Efficiency**: Early profit taking releases capital, increases trading opportunities
3. **Easy to Learn**: Only adds minimal code on top of Strategy001

For traders already familiar with Strategy001, Strategy001_custom_sell provides a great advanced example, demonstrating how to use the `custom_sell` function to implement custom exit logic.

---