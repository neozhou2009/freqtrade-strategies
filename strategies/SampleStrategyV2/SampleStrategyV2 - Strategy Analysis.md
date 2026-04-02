# SampleStrategyV2 Strategy Analysis

> **Strategy Number**: #372 (372nd of 465 strategies)  
> **Strategy Type**: RSI Trend Following + Heikin Ashi Trend Confirmation  
> **Timeframe**: 5 minutes (5m) + 1 hour (1h) informative layer

---

## I. Strategy Overview

**SampleStrategyV2** is a concise example strategy provided by Freqtrade officially, demonstrating the basic framework of strategy development and the application of common technical indicators. This strategy uses RSI overbought/oversold signals combined with TEMA (Triple Exponential Moving Average) and Bollinger Bands for trend following, and introduces Heikin Ashi smoothing technology for trend confirmation.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 composite buy signal |
| **Sell Conditions** | 1 composite sell signal |
| **Protection Mechanism** | Basic stop loss + trailing stop |
| **Timeframe** | Main timeframe 5m + informative timeframe 1h |
| **Dependencies** | talib, qtpylib, pandas |
| **Hyperopt Parameters** | buy_rsi, buy_trend_length, sell_rsi |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "60": 0.01,   # Exit at 1% profit after 60 minutes
    "30": 0.02,   # Exit at 2% profit after 30 minutes
    "0": 0.04     # Exit at 4% profit immediately
}

# Stop loss setting
stoploss = -0.20   # Fixed stop loss at 20%

# Trailing stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.005     # Start trailing at 0.5% profit
trailing_stop_positive_offset = 0.01  # Begin trailing at 1% profit
```

**Design Rationale**:
- ROI table adopts progressive design: higher short-term targets, lower long-term targets
- 20% fixed stop loss is relatively loose, suitable for volatile markets
- Trailing stop activates after reaching 1% profit, protecting small gains

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}

order_time_in_force = {
    'buy': 'gtc',
    'sell': 'gtc'
}
```

Buy and sell use limit orders, stop loss uses market orders to ensure execution.

---

## III. Buy Condition Detailed Analysis

### 3.1 Buy Signal Logic

The strategy uses a single composite buy condition, requiring multiple sub-conditions to be met simultaneously:

```python
# Buy signal
(
    # Main signal: RSI crosses above buy_rsi threshold from below
    (qtpylib.crossed_above(dataframe['rsi'], self.buy_rsi.value)) &
    
    # Trend confirmation: Heikin Ashi trend direction upward
    (dataframe['trend_dir'] > 0) &
    
    # Price position: TEMA below Bollinger Band middle band
    (dataframe['tema'] <= dataframe['bb_middleband']) &
    
    # Momentum confirmation: TEMA is rising
    (dataframe['tema'] > dataframe['tema'].shift(1)) &
    
    # Volume verification: volume not zero
    (dataframe['volume'] > 0)
)
```

### 3.2 Condition Breakdown

| Sub-condition | Description | Technical Meaning |
|---------------|-------------|-------------------|
| **RSI Cross** | RSI crosses above 30 from below | Oversold rebound signal |
| **Trend Upward** | trend_dir > 0 | Heikin Ashi trend is rising |
| **TEMA<BB Middle** | TEMA position is low | Price at relatively low level |
| **TEMA Rising** | TEMA is going up | Momentum starting to strengthen |
| **Volume>0** | Basic verification | Market has activity |

### 3.3 Hyperopt Parameters

```python
buy_rsi = IntParameter(low=1, high=50, default=30, space='buy', optimize=True, load=True)
buy_trend_length = IntParameter(low=50, high=288, default=288, space='buy', optimize=True, load=True)
```

- **buy_rsi**: RSI cross threshold, range 1-50, default 30
- **buy_trend_length**: Heikin Ashi trend calculation period, range 50-288, default 288

---

## IV. Sell Logic Detailed Analysis

### 4.1 Sell Signal Logic

```python
# Sell signal
(
    # Main signal: RSI crosses above sell_rsi threshold from below
    (qtpylib.crossed_above(dataframe['rsi'], self.sell_rsi.value)) &
    
    # Price position: TEMA above Bollinger Band middle band
    (dataframe['tema'] > dataframe['bb_middleband']) &
    
    # Momentum confirmation: TEMA is falling
    (dataframe['tema'] < dataframe['tema'].shift(1)) &
    
    # Volume verification: volume not zero
    (dataframe['volume'] > 0)
)
```

### 4.2 Condition Breakdown

| Sub-condition | Description | Technical Meaning |
|---------------|-------------|-------------------|
| **RSI Cross** | RSI crosses above 70 from below | Overbought signal |
| **TEMA>BB Middle** | TEMA position is high | Price at relatively high level |
| **TEMA Falling** | TEMA is going down | Momentum starting to weaken |
| **Volume>0** | Basic verification | Market has activity |

### 4.3 Hyperopt Parameters

```python
sell_rsi = IntParameter(low=50, high=100, default=70, space='sell', optimize=True, load=True)
```

- **sell_rsi**: RSI cross threshold, range 50-100, default 70

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|--------------------|---------------------|---------|
| **Momentum Type** | RSI(14) | Overbought/oversold judgment |
| **Momentum Type** | ADX | Trend strength |
| **Momentum Type** | MFI | Money flow |
| **Momentum Type** | MACD | Trend direction |
| **Momentum Type** | Stochastic Fast | Fast stochastic indicator |
| **Volatility Type** | BB(20) - STD2 | Price volatility boundary |
| **Trend Type** | TEMA(9) | Triple Exponential Moving Average |
| **Trend Type** | SAR | Parabolic SAR |
| **Smoothing Type** | Heikin Ashi | Price smoothing |
| **Cycle Type** | HT_SINE | Hilbert Transform Sine Wave |
| **Volatility Type** | ATR | Average True Range |

### 5.2 Heikin Ashi Trend Calculation

```python
# Heikin Ashi smoothing
heikinashi = qtpylib.heikinashi(dataframe)
dataframe['ha_open'] = heikinashi['open']
dataframe['ha_close'] = heikinashi['close']
dataframe['ha_high'] = heikinashi['high']
dataframe['ha_low'] = heikinashi['low']

# Trend direction calculation
dataframe['ha_open_sma288'] = ta.SMA(dataframe['ha_open'], timeperiod=self.buy_trend_length.value)
dataframe['ha_close_sma288'] = ta.SMA(dataframe['ha_close'], timeperiod=self.buy_trend_length.value)
dataframe['trend_dir'] = ta.SMA(ta.SMA(dataframe['ha_close_sma288'] - dataframe['ha_open_sma288'], timeperiod=5), timeperiod=5)
```

### 5.3 Informative Timeframe Indicators (1h)

The strategy uses 1h as the informative layer:

```python
informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe='1h')
macd = ta.MACD(informative)
informative['macd'] = macd['macd']
informative['macdsignal'] = macd['macdsignal']
informative['macdhist'] = macd['macdhist']
```

1h MACD is used for large-cycle trend judgment.

---

## VI. Risk Management Features

### 6.1 Basic Stop Loss

```python
stoploss = -0.20  # 20% stop loss
```

Relatively loose stop loss setting, suitable for volatile cryptocurrency markets.

### 6.2 Trailing Stop

```python
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.005     # Activate trailing at 0.5% profit
trailing_stop_positive_offset = 0.01  # Begin trailing at 1% profit
```

Trailing stop design:
- Trailing mechanism activates after reaching 1% profit
- Sell triggers on 0.5% pullback from high
- Locks in small profits

### 6.3 ROI Protection

```
Time        Profit Target
─────────────────────────
0 min       4%
30 min      2%
60 min      1%
```

Longer holding time means lower profit target, preventing profit giveback.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Clear Structure**: Concise code, easy to understand and modify
2. **Hyperopt Support**: 3 optimizable parameters, easy strategy tuning
3. **Official Example**: Provided by Freqtrade, standardized framework
4. **Heikin Ashi Smoothing**: Reduces noise signals, improves trend identification accuracy
5. **Multi-indicator Combination**: RSI+TEMA+BB+HA multi-dimensional verification

### ⚠️ Limitations

1. **Single Buy Condition**: Only one buy signal, low signal density
2. **Wide Stop Loss**: 20% stop loss may incur larger losses
3. **Lack of Protection Mechanisms**: No EMA filtering, pump protection, etc.
4. **Example Positioning**: Primarily for learning, live trading effectiveness needs verification

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|--------------------|---------------------------|-------------|
| **Trend Market** | Default configuration | RSI oversold rebound captures trend entry |
| **Volatile Market** | Lower buy_rsi | Wait for deeper oversold |
| **Calm Market** | Raise sell_rsi | Extend holding time |

---

## IX. Applicable Market Environment Details

**SampleStrategyV2** is an **entry-level trend following strategy**. Based on its concise design, it is most suitable for **markets with clear trends**, while signals may be sparse in oscillating markets.

### 9.1 Strategy Core Logic

- **RSI Oversold Rebound**: Wait for RSI to cross 30 to trigger buy
- **TEMA Position Verification**: Ensure price is at relatively low level
- **Heikin Ashi Trend**: Use smoothed price to confirm trend direction
- **Multiple Verification**: Buy requires multiple conditions to be met simultaneously

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 Uptrend | ⭐⭐⭐⭐☆ | Oversold pullback entry effective, trend confirmation accurate |
| 🔄 Oscillating Market | ⭐⭐☆☆☆ | Single condition, sparse signals |
| 📉 Downtrend | ⭐☆☆☆☆ | 20% stop loss may be too large |
| ⚡ Fast Volatility | ⭐⭐☆☆☆ | HA smoothing may lag |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|--------------------|-------------------|-------------|
| buy_rsi | 25-35 | Adjust based on market volatility |
| sell_rsi | 65-75 | Adjust based on trend strength |
| buy_trend_length | 200-288 | Longer period is more stable |

---

## X. Important Note: Learning vs Live Trading Difference

### 10.1 Learning Cost

Strategy code is concise, suitable for learning:
- Understand Freqtrade strategy framework
- Master common technical indicator applications
- Learn Heikin Ashi smoothing technology
- Understand Hyperopt parameter optimization

### 10.2 Hardware Requirements

```python
startup_candle_count: int = 1000
```

Needs 1000 candles of startup data, moderate computational resource requirements:

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 20-40 | 2GB | 4GB |
| 40-80 | 4GB | 8GB |

### 10.3 Backtest vs Real Trading Difference

As an example strategy, backtest performance may be unstable:
- Few parameters, easy to optimize
- But lacks protection mechanisms, high live trading risk
- Recommend dry-run testing before considering live trading

### 10.4 Manual Trader Advice

Conditions are relatively simple, manual traders can reference:
- Watch for RSI crossing 30 signal
- Check TEMA position and direction
- Use Heikin Ashi to determine trend

---

## XI. Conclusion

**SampleStrategyV2** is a **clear entry-level example strategy**. Its core value lies in:

1. **Teaching Demonstration**: Shows standard usage of Freqtrade strategy framework
2. **Concise Structure**: Easy to understand and secondary development
3. **Hyperopt Friendly**: 3 optimizable parameters for easy tuning

For quantitative traders, this strategy is suitable for **learning and secondary development**. You can add more buy conditions and protection mechanisms on this basis to gradually build a more complete strategy system.

---