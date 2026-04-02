# RSI Strategy In-Depth Analysis

> **Strategy Number**: #340 (340th of 465 strategies)  
> **Strategy Type**: Oversold Bounce + Overbought Sell Strategy  
> **Timeframe**: 15 minutes (15m) + 30-minute informative layer

---

## I. Strategy Overview

The RSI strategy is a classic overbought/oversold reversal strategy based on two momentum indicators: RSI (Relative Strength Index) and Williams %R. Its core philosophy is: buy in the RSI oversold zone, sell in the overbought zone, with Williams %R providing dual confirmation to improve signal quality.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 buy signal, RSI < 30 + Williams %R < -80 |
| **Sell Condition** | 1 sell signal, RSI > 70 + Williams %R > -20 (based on 30-minute informative layer) |
| **Protection Mechanism** | Fixed stop-loss -10%, trailing stop 1% |
| **Timeframe** | 15-minute main frame + 30-minute informative frame |
| **Dependencies** | talib, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.09  # Immediately take 9% profit
}

# Stop-loss setting
stoploss = -0.10  # 10% fixed stop-loss
```

**Design Rationale**:
- ROI setting is extremely simple: exit once profit reaches 9%
- Stop-loss is relatively conservative (-10%), contrasting with Quickie's -25%
- Strategy focuses more on risk control rather than pursuing extreme returns

### 2.2 Trailing Stop Configuration

```python
# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01  # Activate trailing stop after 1% profit
trailing_stop_positive_offset = 0.02  # Trigger when price retraces 2% from peak
```

**Trailing Stop Logic**:
1. When profit reaches 1%, trailing stop activates
2. Stop price moves up following the highest price
3. When price retraces more than 2% from peak, sell is triggered

This is a **"lock in floating profits"** mechanism to prevent profit giveback.

### 2.3 Order Type Configuration

```python
order_types = {
    'buy': 'limit',      # Limit buy
    'sell': 'limit',     # Limit sell
    'stoploss': 'market', # Market stop-loss
    'stoploss_on_exchange': False
}
```

---

## III. Buy Condition Details

### 3.1 Single Buy Condition

The RSI strategy has only one buy signal based on dual oversold confirmation:

```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (dataframe['rsi'] < 30) & 
        (dataframe['rperc'] < -80), 
        'buy'] = 1
    return dataframe
```

**Condition Analysis**:

| Condition | Logic | Meaning |
|-----------|-------|---------|
| RSI < 30 | Oversold zone | Price has fallen excessively, may rebound |
| Williams %R < -80 | Extremely oversold | Williams indicator confirms oversold status |

**Buy Logic Summary**:
When RSI is below 30 (traditional oversold threshold) and Williams %R is below -80 (extreme oversold), the strategy considers price has fallen too much and is about to rebound, triggering entry. This is an **oversold bounce strategy**—contrarian buying when the market is in panic.

### 3.2 Informative Timeframe Indicators

The strategy uses the `@informative('30m')` decorator to obtain 30-minute timeframe data:

```python
@informative('30m')
def populate_indicators_30m(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
    dataframe['rperc'] = ta.WILLR(dataframe, timeperiod=14)
    return dataframe
```

This means the main frame (15m) can access `rsi_30m` and `rperc_30m` indicators.

---

## IV. Sell Logic Details

### 4.1 Sell Signal

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (dataframe['rsi_30m'] > 70) & 
        (dataframe['rperc_30m'] > -20), 
        'sell'] = 1
    return dataframe
```

**Condition Analysis**:

| Condition | Logic | Meaning |
|-----------|-------|---------|
| RSI_30m > 70 | Overbought zone (30-minute) | Price has risen excessively, may pull back |
| Williams %R_30m > -20 | Extremely overbought (30-minute) | Williams indicator confirms overbought status |

**Sell Logic Summary**:
When the 30-minute RSI is above 70 (overbought) and Williams %R is above -20 (extreme overbought), the strategy considers price has risen too much and is about to pull back, triggering a sell. This is an **overbought sell strategy**—contrarian selling when the market is greedy.

### 4.2 Multi-tier Exit System

The strategy employs a **three-layer exit mechanism**:

| Priority | Exit Method | Trigger Condition |
|----------|-------------|-------------------|
| 1 | ROI Profit-taking | Profit reaches 9% |
| 2 | Trailing Stop | Price retraces 2% from peak (activated after 1% profit) |
| 3 | Signal Sell | RSI_30m > 70 and Williams %R_30m > -20 |

**Design Features**:
- Buy signal based on 15-minute timeframe
- Sell signal based on 30-minute timeframe (more stable confirmation)
- Trailing stop provides additional risk protection

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|---------------------|---------|
| Momentum Indicator | RSI (14) | Determine overbought/oversold status |
| Momentum Indicator | Williams %R (14) | Auxiliary confirmation of overbought/oversold |

### 5.2 Indicator Parameters

**RSI (Relative Strength Index)**:
```python
dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
```
- Period: 14
- Oversold threshold: < 30
- Overbought threshold: > 70

**Williams %R (Williams Indicator)**:
```python
dataframe['rperc'] = ta.WILLR(dataframe, timeperiod=14)
```
- Period: 14
- Oversold threshold: < -80
- Overbought threshold: > -20

### 5.3 Dual Timeframe Design

| Timeframe | Purpose | Indicators |
|-----------|---------|------------|
| 15m (Main Frame) | Buy Signal | RSI_15m, Williams %R_15m |
| 30m (Informative Frame) | Sell Signal | RSI_30m, Williams %R_30m |

**Design Rationale**:
- Buy uses shorter timeframe (15m) to capture faster oversold opportunities
- Sell uses longer timeframe (30m) to avoid being shaken out by short-term fluctuations

---

## VI. Risk Management Features

### 6.1 Fixed Stop-loss

```python
stoploss = -0.10  # 10% stop-loss
```

Characteristics:
- Relatively conservative stop-loss (-10%), stricter than Quickie's -25%
- Suitable for risk-averse traders
- Limits maximum loss per trade

### 6.2 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
```

**Trailing Stop Logic Diagram**:

```
Price movement example:
Buy price: 100
Peak price: 110 (10% profit)
Trailing stop activation point: 101 (1% profit)
Trigger sell price: 107.8 (2% retracement from 110)

Result: 7.8% profit (rather than waiting for RSI sell signal)
```

### 6.3 Multi-layer Protection Mechanism

| Protection Layer | Trigger Condition | Effect |
|-----------------|-------------------|--------|
| Fixed Stop-loss | Loss of 10% | Maximum loss limit |
| ROI Profit-taking | Profit of 9% | Target profit locked |
| Trailing Stop | 2% retracement after 1% profit | Floating profit protection |
| Signal Sell | RSI_30m > 70 and Williams %R_30m > -20 | Technical signal exit |

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Classic and Reliable**: RSI is the most classic overbought/oversold indicator, widely used
2. **Dual Confirmation**: RSI + Williams %R dual confirmation reduces false signals
3. **Trailing Stop**: Effectively locks in floating profits, prevents profit giveback
4. **Strict Risk Control**: -10% stop-loss + trailing stop, controllable risk
5. **Dual Timeframe**: Buy with short timeframe, sell with long timeframe, more stable

### ⚠️ Limitations

1. **Single Signal**: Only one buy and one sell signal, lacks flexibility
2. **Poor Performance in Ranging Markets**: RSI easily generates false signals in ranging markets
3. **May Miss Big Trends**: 9% ROI profit-taking may exit too early
4. **Oversold Doesn't Equal Reversal**: RSI < 30 may persist longer

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|---------------------------|-------|
| Range-bound After Downtrend Bounce | Default configuration | RSI oversold bounce strategy's home turf |
| Strong Trend Market | Not recommended | RSI may stay overbought/oversold for extended periods |
| Low Volatility Market | Use with caution | Fewer signals |
| High Volatility Market | Recommended | Overbought/oversold more defined |

---

## IX. Applicable Market Environment Details

The RSI strategy is a **mean-reversion strategy**. Based on its code architecture, it performs best in **oversold bounces within range-bound markets**, while performing poorly in strong trend markets.

### 9.1 Strategy Core Logic

- **Oversold Buy**: RSI < 30 + Williams %R < -80 = extreme oversold
- **Overbought Sell**: RSI > 70 + Williams %R > -20 = extreme overbought
- **Trailing Stop**: Locks in floating profits, prevents drawdowns
- **Dual Timeframe**: 15m for buying, 30m for selling

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|-------------|-------------------|-----------------|
| 📉 Oversold Bounce | ⭐⭐⭐⭐⭐ | Strategy designed exactly for this |
| 🔄 Range-bound Consolidation | ⭐⭐⭐⭐☆ | Frequent overbought/oversold signals, good results |
| 📈 Strong Uptrend | ⭐⭐☆☆☆ | RSI stays overbought, exits too early |
| 📉 Strong Downtrend | ⭐☆☆☆☆ | RSI stays oversold, signals fail |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|------------------|-------|
| Timeframe | 15m + 30m | Keep default |
| Stop-loss | -0.10 | Can adjust based on risk preference |
| ROI | 0.09 | Can raise appropriately to capture larger moves |
| RSI Threshold | 30/70 | Classic thresholds, recommend keeping |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

RSI strategy has simple concepts, suitable for beginners:
- RSI is one of the most common technical indicators
- Overbought/oversold concepts are easy to understand
- Dual confirmation reduces false signals

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

Strategy has low computational requirements, doesn't demand high hardware specs.

### 10.3 Backtesting vs Live Trading Differences

- **Backtesting Advantage**: Oversold bounce strategies perform well in historical data
- **Live Trading Risk**: RSI may stay in overbought/oversold zones for extended periods
- **Trailing Stop Impact**: Actual profit-taking points may differ from expectations

### 10.4 Manual Trading Recommendations

If manually using this strategy's logic:
1. Monitor RSI and Williams %R on 15-minute chart
2. When RSI < 30 and Williams %R < -80, prepare to buy
3. Set 9% profit target and 10% stop-loss
4. After 1% profit, set trailing stop at 2% retracement
5. When 30-minute RSI > 70 and Williams %R > -20, consider selling

---

## XI. Summary

**RSI** is a **classic and robust overbought/oversold strategy**. Its core value lies in:

1. **Classic Indicator**: RSI is one of the most widely used technical indicators with high reliability
2. **Dual Confirmation**: Williams %R as auxiliary confirmation improves signal quality
3. **Complete Risk Control**: Fixed stop-loss + trailing stop + ROI profit-taking, three layers of protection
4. **Dual Timeframe**: Buy with short timeframe, sell with long timeframe, more stable

For quantitative traders, this is a **suitable template as a base strategy**. You can add more filter conditions, adjust parameters, or combine other indicators on this foundation.

---