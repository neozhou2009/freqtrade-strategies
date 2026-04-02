# SMAOffsetV2 Strategy Analysis

> **Strategy ID**: #366 (Batch 361-370 of 465 strategies)  
> **Strategy Type**: SMA Offset + EMA Trend Filter + Dynamic Stop Loss  
> **Timeframe**: 5 minutes (5m) + 1 hour informative layer

---

## 1. Strategy Overview

SMAOffsetV2 is a trend-following strategy based on Simple Moving Average offset (SMA Offset), with trend detection and custom stop loss mechanisms added on top of the original SMAOffset. This strategy uses EMA fast/slow lines (20/25) to determine trend direction, only looking for SMA offset buying opportunities in uptrends, while controlling risk through a dynamic stop loss mechanism.

The strategy design philosophy is simple and clear: **Only buy when trend is upward, enter when price pulls back below the moving average, exit when price returns above the moving average or trend reverses**.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 buy signal (trend filter + SMA offset) |
| **Sell Condition** | 1 sell signal (two sub-conditions with OR logic) |
| **Protection Mechanism** | Dynamic stop loss (time + loss dual condition trigger) |
| **Timeframe** | 5m (main) + 1h (informative layer trend judgment) |
| **Dependencies** | talib, pandas, freqtrade.persistence |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 1,    # 100% (almost never uses ROI)
}

# Stop loss setting
stoploss = -0.20  # Fixed stop loss -20%

# Custom stop loss
use_custom_stoploss = True
```

**Design Philosophy**:
- ROI set to 100%, essentially abandoning ROI take-profit, relying on sell signals and stop loss
- 20% fixed stop loss as the last line of defense
- Custom stop loss function provides more flexible risk control

### 2.2 Order Type Configuration

```python
use_sell_signal = True      # Use sell signal
sell_profit_only = True     # Use sell signal only when profitable
process_only_new_candles = True  # Process only on new candles
```

---

## 3. Buy Condition Detailed Analysis

### 3.1 Trend Filter Mechanism

The strategy uses 1-hour timeframe EMA to determine trend:

```python
# 1-hour EMA indicators
dataframe['ema_fast'] = ta.EMA(dataframe, timeperiod=20)
dataframe['ema_slow'] = ta.EMA(dataframe, timeperiod=25)

# Trend judgment
dataframe['go_long'] = (
    (dataframe['ema_fast'] > dataframe['ema_slow'])
).astype('int') * 2
```

**Logic Interpretation**:
- go_long = 2: EMA fast line > EMA slow line, uptrend
- go_long = 0: EMA fast line ≤ EMA slow line, downtrend

### 3.2 Buy Condition

```python
# Trigger conditions
- go_long > 0 (1-hour uptrend)
- Close price < sma_30_offset (price below SMA(20) × 0.96)
- Volume > 0
```

**Detailed Analysis**:

| Condition | Parameter | Description |
|-----------|-----------|-------------|
| Trend filter | EMA(20) > EMA(25) | Only buy in 1-hour uptrend |
| SMA offset | SMA(20) × 0.96 | Price 4% below moving average |
| Volume | > 0 | Trading activity exists |

**Design Intent**:
- Through 1-hour trend filter, avoid bottom-fishing in downtrend
- 4% offset amplitude is relatively large, ensuring sufficient price discount
- Simple and clear, one condition to enter

---

## 4. Sell Logic Detailed Analysis

### 4.1 Sell Conditions (Two Sub-conditions with OR Logic)

```python
# Sell signal
(
    (go_long == 0)           # Trend reversal (sub-condition 1)
    |
    (close > sma_30_offset_pos)  # Price breaks above upper offset (sub-condition 2)
)
&
(volume > 0)
```

**Sub-condition Details**:

| Sub-condition | Trigger Logic | Description |
|---------------|--------------|-------------|
| #1 Trend reversal | go_long == 0 | 1-hour EMA death cross, trend turns down |
| #2 Price breakout | close > SMA(20) × 1.012 | Price 1.2% above moving average |

**Logic Interpretation**:
- **Trend reversal**: 1-hour EMA fast line crosses below slow line, indicating possible trend reversal
- **Price breakout**: Price rises to 1.2% above moving average, reaching profit target

### 4.2 Dynamic Stop Loss Mechanism

The strategy implements a custom stop loss function, providing intelligent risk control:

```python
def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs) -> float:

    # Condition: Held for more than 40 minutes + loss exceeds 10%
    if current_time - timedelta(minutes=40) > trade.open_date_utc and current_profit < -0.1:
        return -0.01  # Tighten stop loss to -1%

    return -0.99  # Default: almost never triggers stop loss
```

**Working Mechanism**:
- **Default state**: Stop loss -99% (almost never triggers)
- **Trigger condition**: Held > 40 minutes AND loss > 10%
- **After trigger**: Stop loss tightens to -1%, quick stop loss

**Design Intent**:
- Give the strategy enough time to "self-rescue", avoid premature stop loss
- If still losing more than 10% after 40 minutes, acknowledge judgment error and stop quickly

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|-------------------|---------------------|------------|---------|
| Trend | EMA | 20/25 periods | 1-hour trend judgment |
| Trend | SMA | 20 periods | Price offset reference baseline |
| Volume | Volume | - | Liquidity confirmation |

### 5.2 Informative Timeframe Indicators (1h)

The strategy uses 1 hour as the informative layer, providing higher-dimensional trend judgment:

```python
# 1-hour timeframe
informative_timeframe = '1h'

# Informative layer indicators
ema_fast = EMA(20)  # Fast line
ema_slow = EMA(25)  # Slow line
go_long = (ema_fast > ema_slow) * 2  # Trend signal
```

**Workflow**:
1. Get 1-hour candlestick data
2. Calculate EMA(20) and EMA(25)
3. Determine if fast line is above slow line
4. Merge trend signal into 5-minute data

---

## 6. Risk Management Features

### 6.1 Dynamic Stop Loss System

The strategy adopts intelligent dynamic stop loss, different from traditional fixed stop loss:

| Stop Loss Type | Trigger Condition | Stop Loss Value | Description |
|---------------|-------------------|-----------------|-------------|
| Initial state | Any situation | -99% | Almost never triggers |
| Dynamic tightening | Held > 40 minutes AND loss > 10% | -1% | Quick stop loss |

**Advantages**:
- Avoid being stopped out by normal volatility
- Give strategy enough time to recover
- Quick stop loss after confirming failure

### 6.2 Trend Filter Protection

- Only buy in 1-hour uptrend
- Immediately sell when trend reverses
- Avoid counter-trend trading

### 6.3 Profit Protection

```python
sell_profit_only = True     # Use sell signal only when profitable
```

This setting ensures sell signals don't trigger at a loss, avoiding selling during floating losses.

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Clean Logic**: One buy condition, two sell conditions, clear and easy to understand
2. **Trend Filter**: Uses 1-hour EMA to determine trend, avoids counter-trend trading
3. **Dynamic Stop Loss**: Gives strategy recovery time, quick stop when failed
4. **Small Code Size**: Easy to understand and further develop

### ⚠️ Limitations

1. **Fixed Parameters**: Buy parameters are hardcoded, not as flexible as HyperOpt versions
2. **Large Offset**: 4% offset may miss some opportunities
3. **No Trailing Stop**: No trailing take-profit mechanism, may "ride the rollercoaster"
4. **Trend Dependent**: May perform poorly in ranging markets

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Uptrend | Default configuration | Trend filter ensures trend-following trading |
| Ranging market | Not recommended | Frequent EMA crossovers may cause repeated stop losses |
| Downtrend | Not recommended | Trend filter will block buying |
| High volatility | Increase offset parameters | Avoid being triggered by normal volatility |

---

## 9. Applicable Market Environment Detailed

SMAOffsetV2 is a simplified version of the SMA Offset series, focusing on trend following. Based on its code architecture, it is most suitable for **markets with clear trends**, and performs poorly in **sideways oscillation**.

### 9.1 Strategy Core Logic

- **Trend Filter**: Only buy when 1-hour EMA is in golden cross state
- **Price Offset Entry**: Enter when price is 4% below SMA
- **Dual Exit**: Exit when trend reverses or price breaks out

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:------------------|:----------------|
| 📈 Slow bull trend | ⭐⭐⭐⭐⭐ | Trend filter works, many pullback buying opportunities |
| 🔄 Sideways oscillation | ⭐⭐☆☆☆ | EMA frequently crosses, trend judgment fails |
| 📉 One-sided decline | ⭐⭐⭐⭐☆ | Trend filter blocks buying, stay out and avoid risk |
| ⚡️ Severe volatility | ⭐⭐⭐☆☆ | Offset amplitude may be penetrated |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|------------------|-------------|
| Trading pair | Major coins/stablecoins | Clear trend, good liquidity |
| Stop loss | Keep -20% | As last line of defense |
| Dynamic stop loss time | 40 minutes | Can adjust based on trading pair |

---

## 10. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

This strategy has clean code, low learning cost:
- Only involves EMA and SMA, two basic indicators
- Clear logic, suitable for beginners to learn
- No complex parameter optimization

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-30 pairs | 4GB | 8GB |
| 30+ pairs | 8GB | 16GB |

### 10.3 Difference Between Backtesting and Live Trading

- **Advantage**: Simple logic, small difference between backtesting and live trading
- **Note**: Dynamic stop loss time judgment may have slight differences in live trading
- **Recommendation**: Suitable as a starting point for learning strategy framework

### 10.4 Suggestions for Manual Traders

If you want to manually use the logic of this strategy:
1. Use 1-hour EMA(20) and EMA(25) to determine trend
2. In uptrend, wait for price to pull back 4% below 20 SMA
3. Set 20% fixed stop loss
4. When 1-hour EMA death cross or price rises 1.2% above SMA, sell

---

## 11. Summary

**SMAOffsetV2** is a **trend-following strategy with clean logic**. Its core value lies in:

1. **Trend Filter**: 1-hour EMA ensures trend-following trading
2. **Dynamic Stop Loss**: Intelligent stop loss mechanism balances recovery time and risk control
3. **Clean Code**: Easy to understand and further develop
4. **Suitable for Learning**: A good starting point for understanding Freqtrade strategy development

For quantitative traders, this is a strategy framework suitable for entry and further development. It is recommended to conduct sufficient backtesting and paper trading verification before actual use.