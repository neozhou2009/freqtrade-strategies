# ActionZone Strategy Analysis

> **Strategy ID**: #415 (415th of 465 strategies)  
> **Strategy Type**: Trend Following + Dynamic Stop Loss Protection  
> **Timeframe**: 1 Day (1d)

---

## 1. Strategy Overview

ActionZone is a medium-to-long-term strategy based on dual EMA trend following, employing a "zone trading" philosophy. It defines market states (bullish zone/bearish zone) through the relative position of fast and slow moving averages, and generates trading signals based on price positioning relative to these moving averages. The strategy introduces a dynamic stop-loss mechanism based on the lowest price, protecting profits while allowing trends to fully develop.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 core buy signal (trend + price breakout composite condition) |
| **Sell Conditions** | Base sell signal + custom trend sell logic |
| **Protection Mechanism** | Dynamic stop loss (based on lowest price) + trailing stop + custom position management |
| **Timeframe** | 1 Day (1d) |
| **Max Positions** | 3 trading pairs |
| **Dependencies** | talib, qtpylib, numpy, pandas |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,    # Immediately: 10%
    "60": 0.05,   # After 60 minutes: 5%
    "120": 0.02,  # After 120 minutes: 2%
    "180": 0.01,  # After 180 minutes: 1%
}

# Stop Loss Settings
stoploss = -0.10  # 10% fixed stop loss

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.02      # Activate after 2% profit
trailing_stop_positive_offset = 0.01  # Offset 1%
```

**Design Rationale**:
- **Tiered ROI**: Gradually lowers profit targets as holding time increases, encouraging timely profit taking
- **Dual Stop Loss**: 10% fixed stop loss as the last line of defense, trailing stop to lock in trend profits
- **Trailing Stop Trigger Condition**: Requires 2% profit first to activate, avoiding premature shakeouts during consolidation

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',          # Limit buy
    'sell': 'limit',          # Limit sell
    'stoploss': 'market',     # Market execution for stop loss
    'stoploss_on_exchange': False
}

order_time_in_force = {
    'buy': 'gtc',            # Good Till Cancel
    'sell': 'gtc'
}
```

---

## 3. Buy Conditions Explained

### 3.1 Protection Mechanism (Core Feature)

ActionZone employs an innovative dynamic stop-loss mechanism based on historical price lows:

| Protection Type | Parameter Description | Implementation |
|-----------------|----------------------|----------------|
| **Dynamic Stop Loss** | Based on periodic lowest price | 14-period MIN calculation |
| **Trailing Stop** | Activates after 2% profit | trailing_stop configuration |
| **Fixed Stop Loss** | 10% hard stop | stoploss configuration |
| **Position Management** | Max loss $10 calculation | custom_stake_amount |

### 3.2 Buy Condition Details

#### Condition #1: Trend Breakout Buy

```python
# Logic Breakdown
Condition 1: fastMA > slowMA        # Fast line above slow line (bullish trend confirmed)
Condition 2: close > fastMA         # Price breaks above fast line (buy signal triggered)
Condition 3: volume > 0             # Volume confirmation
```

**Trading Logic**:
1. **Trend Confirmation**: 12-period EMA > 26-period EMA confirms bullish trend
2. **Entry Timing**: Price breaks above 12-period EMA from below
3. **Volume Verification**: Ensures genuine trading activity

### 3.3 Position Management Algorithm

```python
def custom_stake_amount(self, pair, current_time, current_rate, ...):
    stop_price = last_candle['lowest']  # Dynamic stop price
    volume_for_buy = max_loss_per_trade / (current_rate - stop_price)
    use_money = volume_for_buy * current_rate
    return use_money
```

**Calculation Logic**:
- Preset maximum loss: $10
- Stop distance = Current price - Lowest price
- Buy amount = $10 / Stop distance
- Actual investment = Buy amount × Current price

---

## 4. Sell Logic Explained

### 4.1 Multi-Layer Take Profit System

The strategy employs a dual exit mechanism with tiered ROI + trailing stop:

```
Holding Time      Target ROI      Trigger Method
─────────────────────────────────────────────────
Immediately       10%             ROI trigger
After 60 min      5%              ROI trigger
After 120 min     2%              ROI trigger
After 180 min     1%              ROI trigger
Any time          Dynamic         Trailing stop trigger
```

### 4.2 Custom Sell Logic

```python
def custom_sell(self, pair, trade, current_time, current_rate, ...):
    # Trend reversal sell
    if last_candle['fastMA'] < last_candle['slowMA']:
        return True  # Fast line crosses below slow line, trend turning bearish
    return False
```

### 4.3 Base Sell Signal (1 signal)

```python
# Sell signal: Trend reversal + Price breakdown
Signal trigger conditions:
1. fastMA < slowMA          # Fast line below slow line (bearish trend)
2. close < fastMA           # Price breaks below fast line (sell signal)
3. volume > 0               # Volume confirmation
```

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | EMA(12), EMA(26) | Define market zones (bullish/bearish) |
| Price Indicators | MIN(14) | Calculate dynamic stop loss level |
| Volume Indicators | Volume | Signal validity verification |

### 5.2 Indicator Calculation Details

```python
# Lowest Price Indicator
lowest = ta.MIN(dataframe, timeperiod=14)  # 14-period lowest price

# Dual Moving Average System
fastEMA = ta.EMA(dataframe, timeperiod=12)  # Fast line: 12-day exponential MA
slowEMA = ta.EMA(dataframe, timeperiod=26)  # Slow line: 26-day exponential MA
```

**Indicator Meanings**:
- **EMA(12)**: Quickly reflects recent price changes, serves as short-term trend reference
- **EMA(26)**: Smooths price fluctuations, serves as medium-term trend baseline
- **MIN(14)**: Tracks the lowest support level over 14 days for risk control

---

## 6. Risk Management Features

### 6.1 Dynamic Stop Loss Mechanism

ActionZone's core innovation lies in the dynamic stop loss based on the lowest price:

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, ...):
    stoploss_price = last_candle['lowest']  # 14-period lowest price
    if stoploss_price < current_rate:
        return (stoploss_price / current_rate) - 1  # Convert to percentage
    return 1  # Maintain current stop loss
```

**Advantages**:
- Stop loss level moves up as price rises (tracking the lowest price)
- Gives trends enough room for volatility
- Sets protection at key support levels

### 6.2 Trailing Stop Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| trailing_stop | True | Enable trailing stop |
| trailing_only_offset_is_reached | True | Only activate after offset reached |
| trailing_stop_positive | 0.02 | Start trailing after 2% profit |
| trailing_stop_positive_offset | 0.01 | Trailing offset 1% |

### 6.3 Position Risk Control

```python
max_loss_per_trade = 10  # USD - Maximum loss per trade
max_open_trades = 3      # Maximum simultaneous positions
```

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Dynamic Risk Control**: Stop loss based on lowest price automatically adjusts with trend evolution, protecting profits while allowing trend development
2. **Scientific Position Management**: Dynamically calculates position size based on stop distance, ensuring controllable risk per trade
3. **Effective Trend Following**: Dual EMA system is simple and reliable, suitable for capturing medium-to-long-term trends
4. **Multi-Layer Exit Mechanism**: Tiered ROI + trailing stop + custom sell, flexibly responding to different market conditions

### ⚠️ Limitations

1. **Slow Daily Response**: Daily timeframe is less sensitive to short-term fluctuations, may miss rapid market movements
2. **Poor Performance in Ranging Markets**: Trend following strategies tend to generate false signals during sideways consolidation
3. **Stop Loss May Be Too Wide**: Stop loss based on 14-day lowest price may be far away in volatile markets
4. **Trend Dependency**: Strategy is essentially trend following, requires clear directional markets to be profitable

---

## 8. Applicable Scenarios Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Clear Uptrend | Default configuration | Best environment for trend following strategies |
| Oscillating Uptrend | Lower max_open_trades | Reduce position count to lower risk |
| Sideways Consolidation | Disable strategy | Trend strategies struggle to profit in ranging markets |
| Downtrend | Disable or short | Default configuration designed for long positions |

---

## 9. Applicable Market Environment Details

ActionZone is a classic **trend following strategy**. Based on its code architecture and community long-term live trading verification experience, it is best suited for **clear trend markets**, while performing poorly in **sideways consolidation and downtrends**.

### 9.1 Strategy Core Logic

- **Trend Identification**: Judge bullish/bearish state through EMA(12) and EMA(26) relative positions
- **Entry Timing**: Enter when price breaks above fast line, ensuring momentum direction
- **Risk Control**: Dynamic tracking stop loss + fixed stop loss dual protection
- **Position Management**: Risk-based position calculation ensures controllable loss per trade

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|-------------|-------------------|----------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | Dual EMA system effectively captures trends, dynamic stop loss allows profits to run |
| 🔄 Oscillating Uptrend | ⭐⭐⭐☆☆ | May generate false signals but overall can follow the uptrend direction |
| 📉 Downtrend | ⭐☆☆☆☆ | Strategy primarily designed for longs, should avoid in downtrends |
| ⚡️ High Volatility Sideways | ⭐☆☆☆☆ | Frequent false breakouts lead to repeated stop losses, accumulating losses |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| max_loss_per_trade | $5-$20 | Adjust based on account size, ensure controllable risk per trade |
| max_open_trades | 2-4 | Daily timeframe holding periods are longer, not recommended to have too many |
| min_price_period | 14 | Stop loss calculation period, can be adjusted based on market volatility |

---

## 10. Important Notes: The Cost of Complexity

### 10.1 Learning Curve

ActionZone has relatively concise code (about 150 lines) with clear core logic, suitable for beginners to understand and modify. However, understanding the dynamic stop loss and position management mechanisms requires some quantitative trading foundation.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|----------------|-------------------|
| 1-5 | 2GB | 4GB |
| 6-15 | 4GB | 8GB |
| 16+ | 8GB | 16GB |

**Note**: Daily timeframe strategy has low computational requirements, hardware requirements are relatively low.

### 10.3 Backtesting vs Live Trading Differences

- **Backtesting**: Trends are clear in historical data, signals are distinct
- **Live Trading**: Trend identification lags, actual profits may be lower than backtesting
- **Slippage**: Daily trading slippage impact is relatively small
- **Latency**: Daily timeframe is not sensitive to latency

### 10.4 Manual Trading Recommendations

To manually execute this strategy:
1. Set up EMA(12) and EMA(26) in TradingView
2. Wait for price close to confirm breakout
3. Manually set stop loss at 14-day lowest price
4. Adjust position size for risk control

---

## 11. Summary

**ActionZone** is a **simple yet effective trend following strategy**. Its core values include:

1. **Dynamic Risk Control**: Stop loss mechanism based on lowest price protects capital while giving trends room
2. **Scientific Position Management**: Risk budget mechanism ensures controllable loss per trade
3. **Clear Trading Logic**: Dual EMA system is simple and intuitive, easy to understand and execute
4. **Suitable for Medium-to-Long-Term Investment**: Daily timeframe reduces noise, captures major trends

For quantitative traders, ActionZone provides an excellent trend following framework suitable as a base strategy for extension and optimization. Recommended for clear trend markets, use with caution in ranging markets.

---