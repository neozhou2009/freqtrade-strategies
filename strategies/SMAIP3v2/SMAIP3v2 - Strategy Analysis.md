# SMAIP3v2 Strategy In-Depth Analysis

> **Strategy Number**: #355 (355th of 465 strategies)
> **Strategy Type**: Moving Average Offset + Trend Filter + Dynamic Stop Loss
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

SMAIP3v2 is a trend-following strategy based on moving average offsets, capturing rebound opportunities after price pullbacks through dynamically calculated buy and sell thresholds. This strategy combines EMA trend filtering and a "bad pair" detection mechanism to avoid extreme market conditions while maintaining trend following.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 core buy signal (trend filter + price deviation) |
| **Sell Condition** | 1 base sell signal + trailing stop + ROI take-profit |
| **Protection Mechanism** | 2 sets of "bad pair" detection thresholds |
| **Timeframe** | 5-minute primary timeframe |
| **Dependencies** | talib (technical indicator calculation), freqtrade.strategy |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.026  # Exit immediately if 2.6% profit achieved
}

# Stop loss setting
stoploss = -0.23  # 23% fixed stop loss

# Trailing stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.003  # Start trailing after 0.3% profit
trailing_stop_positive_offset = 0.018  # Activate trailing after 1.8% profit
```

**Design Rationale**:
- ROI setting is relatively aggressive (2.6%), pursuing quick profits
- Stop loss space is large (23%), leaving room for trend fluctuations
- Trailing stop mechanism protects accumulated profits, avoiding profit giveback

### 2.2 Order Type Configuration

The strategy uses default order type configuration, suitable for most exchanges.

---

## III. Buy Condition Details

### 3.1 Protection Mechanism (2 Sets)

The strategy prevents buying in extreme market conditions through the `pair_is_bad` detection mechanism:

| Protection Type | Parameter Description | Default Value |
|----------------|----------------------|---------------|
| pair_is_bad_1 | Price drop threshold from open 12 candles ago to current close | 0.130 (13%) |
| pair_is_bad_2 | Price drop threshold from open 6 candles ago to current close | 0.075 (7.5%) |

**Logic**: When price experiences a sharp decline within the past 6-12 candles (exceeding the threshold), it is marked as a "bad pair" and buying is suspended.

### 3.2 Core Buy Condition

```python
# Buy logic
(
    (dataframe['ema_50'] > dataframe['ema_200']) &           # EMA50 above EMA200, trend up
    (dataframe['close'] > dataframe['ema_200']) &             # Close above EMA200
    (dataframe['pair_is_bad'] < 1) &                          # Not in bad pair status
    (dataframe['close'] < dataframe['ma_offset_buy']) &       # Price below buy threshold
    (dataframe['volume'] > 0)                                  # Has volume
)
```

**Condition Analysis**:
1. **Trend Confirmation**: EMA50 > EMA200, ensuring medium-term trend is upward
2. **Price Position**: Close > EMA200, ensuring position in long-term uptrend
3. **Safety Check**: Not in "bad pair" status, avoiding chasing highs or catching falling knives
4. **Buy Opportunity**: Price below dynamically calculated buy threshold (MA × low_offset)
5. **Liquidity**: Ensuring there is trading volume

### 3.3 Moving Average Offset Mechanism

The strategy uses dynamic offsets to calculate buy and sell thresholds:

```python
# Buy threshold calculation
ma_offset_buy = SMA/EMA(N candles) × low_offset
# low_offset default 0.968, i.e., 3.2% below the moving average

# Sell threshold calculation
ma_offset_sell = EMA(N candles) × high_offset  
# high_offset default 0.985, i.e., -1.5% above the average (slightly below the average)
```

---

## IV. Sell Logic Details

### 4.1 Sell Condition

```python
# Sell logic
(
    (dataframe['close'] > dataframe['ma_offset_sell']) &      # Price above sell threshold
    (dataframe['volume'] > 0)                                  # Has volume
)
```

**Design Rationale**: Exit with profit when price rebounds above the sell threshold.

### 4.2 Smart Exit Rejection Mechanism

The strategy implements a `confirm_trade_exit` method that rejects selling under certain conditions:

```python
# Exit rejection condition
if sell_reason in ['roi', 'sell_signal', 'trailing_stop_loss']:
    if (last_candle['open'] > previous_candle_1['open']) &    # Current candle opens higher
       (last_candle['rsi'] > 50) &                             # RSI > 50
       (last_candle['rsi'] > previous_candle_1['rsi']):       # RSI rising
        return False  # Reject exit
```

**Design Rationale**: When market momentum remains strong (higher open, rising RSI), reject the sell to capture more profit.

### 4.3 Multi-Layer Take-Profit System

| Profit Level | Exit Mechanism | Trigger Condition |
|-------------|----------------|-------------------|
| 2.6% | ROI take-profit | Immediate effect |
| 1.8%+ | Trailing stop activation | Profit exceeds 1.8% |
| 0.3%+ pullback | Trailing stop trigger | 0.3% pullback from peak |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | EMA50, EMA200 | Trend direction judgment |
| Momentum Indicators | RSI(2) | Exit confirmation judgment |
| Offset Indicators | MA × offset | Dynamic buy/sell thresholds |

### 5.2 Optimizable Parameters

The strategy provides rich optimizable parameters:

```python
# Buy parameters
base_nb_candles_buy = IntParameter(16, 60, default=18)  # Moving average period
low_offset = DecimalParameter(0.8, 0.99, default=0.968)  # Buy offset
buy_trigger = CategoricalParameter(['SMA', 'EMA'], default='SMA')  # MA type

# Sell parameters
base_nb_candles_sell = IntParameter(16, 60, default=26)  # Moving average period
high_offset = DecimalParameter(0.8, 1.1, default=0.985)  # Sell offset
sell_trigger = CategoricalParameter(['SMA', 'EMA'], default='EMA')  # MA type

# Protection parameters
pair_is_bad_1_threshold = DecimalParameter(0.0, 0.30, default=0.130)
pair_is_bad_2_threshold = DecimalParameter(0.0, 0.25, default=0.075)
```

---

## VI. Risk Management Features

### 6.1 Dual Trend Filtering

The strategy requires both medium-term trend (EMA50 > EMA200) and long-term trend (price > EMA200) confirmation before considering a buy, significantly reducing counter-trend trading risk.

### 6.2 Dynamic "Bad Pair" Detection

By monitoring price changes over the past 6-12 candles, identify crashing pairs and suspend buying:

```python
pair_is_bad = (
    ((open.shift(12) - close) / close >= 0.130) |  # 12 candles drop >= 13%
    ((open.shift(6) - close) / close >= 0.075)      # 6 candles drop >= 7.5%
)
```

### 6.3 Smart Exit Rejection

When an exit signal triggers, additionally check market momentum. If momentum remains strong, reject the exit and continue holding to maximize profit potential.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Rigorous Trend Confirmation**: Dual EMA filtering ensures trading only in uptrends
2. **Crash Avoidance Mechanism**: Bad pair detection prevents buying during extreme market conditions
3. **Complete Profit Protection**: Trailing stop + smart exit rejection dual protection
4. **Large Optimization Space**: Multiple parameters support Hyperopt optimization

### ⚠️ Limitations

1. **Large Stop Loss Space**: 23% stop loss may be too wide for conservative traders
2. **Average Performance in Sideways Markets**: As a trend strategy, may experience frequent small losses during sideways movement
3. **Single Timeframe**: Only uses 5-minute, lacking multi-timeframe confirmation

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Clear Uptrend | Default configuration | Strategy's best performance environment |
| Oscillating Uptrend | Lower low_offset | Adapt to more frequent pullbacks |
| High Volatility Market | Raise pair_is_bad threshold | Stricter risk control |

---

## IX. Applicable Market Environment Details

SMAIP3v2 is a typical trend-following strategy, best suited for **clear uptrend markets**, while performing poorly in sideways or downtrend markets.

### 9.1 Strategy Core Logic

- **Trend is King**: Only buy when EMA50 > EMA200 and price > EMA200
- **Buy on Pullbacks**: Wait for price to pull back below dynamic threshold before entering
- **Smart Holding**: Reject sells when momentum is strong, maximizing profits

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:-----------:|:-----------------:|-----------------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | Perfectly matches strategy logic, trend continuation after pullback buy |
| 🔄 Oscillating Uptrend | ⭐⭐⭐⭐☆ | Still profitable, but pullbacks may trigger stop loss |
| 📉 Downtrend | ⭐☆☆☆☆ | Trend filter will block most buys, low capital utilization |
| ⚡ High Volatility Sideways | ⭐⭐☆☆☆ | Frequent entries/exits, fees erode profits |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-----------------|-------------|
| Trading Pairs | Major coins | Good liquidity, more obvious trends |
| pair_is_bad threshold | Adjust based on volatility | Can appropriately relax for high volatility coins |
| ROI | Can raise to 3-5% | Adapt to different risk preferences |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

The strategy logic is relatively clear, but requires understanding:
- Moving average offset mechanism
- "Bad pair" detection principle
- Smart exit rejection logic

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|---------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |

### 10.3 Backtesting vs Live Trading Differences

- Smart exit rejection performance in backtesting may differ from live trading
- Slippage impact is more pronounced in high-frequency trading

### 10.4 Manual Trader Recommendations

1. Test in simulation environment for at least 1 month first
2. Observe actual trigger frequency of smart exit rejection
3. Adjust parameters based on actual trading pairs

---

## XI. Summary

**SMAIP3v2** is a well-designed trend-following strategy that implements pullback buying through moving average offsets, combined with smart exit mechanisms to maximize profits. Its core value lies in:

1. **Rigorous Trend Confirmation**: Dual EMA filtering, avoiding counter-trend trading
2. **Complete Risk Control**: Bad pair detection + trailing stop + smart exit rejection
3. **Strong Optimizability**: Supports Hyperopt for parameter optimization

For quantitative traders, this is a strategy suitable for use in clear uptrends. It is recommended to deploy during trending markets and appropriately reduce position size or pause during sideways periods.