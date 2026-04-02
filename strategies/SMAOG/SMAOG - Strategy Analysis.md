# SMAOG Strategy In-Depth Analysis

> **Strategy Number**: #356 (356th of 465 strategies)
> **Strategy Type**: Moving Average Offset + Multi-Layer Crash Protection + Momentum Exit
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

SMAOG is an evolved version of the SMAIP series, enhancing the crash protection mechanism (3-layer rolling detection) and more refined exit conditions on top of the original moving average offset strategy. The "OG" in the strategy name implies it is a "veteran-level" enhanced version.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 core buy signal (trend filter + price deviation + crash protection) |
| **Sell Condition** | 1 sell signal (with momentum filter) + trailing stop + ROI take-profit |
| **Protection Mechanism** | 3 sets of rolling window "bad pair" detection thresholds |
| **Timeframe** | 5-minute primary timeframe |
| **Dependencies** | talib (technical indicator calculation), freqtrade.strategy |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.10,   # Exit immediately if 10% profit achieved
    "30": 0.05,  # Exit at 5% after 30 minutes
    "60": 0.02   # Exit at 2% after 60 minutes
}

# Stop loss setting
stoploss = -0.23  # 23% fixed stop loss

# Trailing stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.005   # Start trailing after 0.5% profit
trailing_stop_positive_offset = 0.02  # Activate trailing after 2% profit
```

**Design Rationale**:
- ROI uses progressive design, the longer the holding time, the lower the take-profit threshold
- Trailing stop is more aggressive than SMAIP3v2 (0.5% vs 0.3%), locking in profits faster

### 2.2 Order Type Configuration

The strategy uses default order type configuration, suitable for most exchanges.

---

## III. Buy Condition Details

### 3.1 Protection Mechanism (3 Sets of Rolling Windows)

The strategy prevents buying in extreme market conditions through 3 layers of rolling window `pair_is_bad` detection mechanism:

| Protection Type | Rolling Window | Default Threshold | Detection Logic |
|----------------|----------------|-------------------|-----------------|
| pair_is_bad_0 | 144 candles | 0.555 (55.5%) | 12-hour lowest price drop |
| pair_is_bad_1 | 12 candles | 0.172 (17.2%) | 1-hour lowest price drop |
| pair_is_bad_2 | 2 candles | 0.198 (19.8%) | 10-minute lowest price drop |

**Logic Details**:
```python
pair_is_bad = (
    ((open.rolling(144).min() - close) / close >= 0.555) |   # 12-hour crash
    ((open.rolling(12).min() - close) / close >= 0.172) |    # 1-hour crash
    ((open.rolling(2).min() - close) / close >= 0.198)       # 10-minute crash
)
```

**Design Philosophy**: Covers short-term, medium-term, and long-term crash detection, providing comprehensive protection.

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
3. **Safety Check**: Not in "bad pair" status (3-layer protection)
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
# high_offset default 0.985, i.e., -1.5% above the average
```

---

## IV. Sell Logic Details

### 4.1 Sell Condition (with Momentum Filter)

```python
# Sell logic
(
    (dataframe['close'] > dataframe['ma_offset_sell']) &     # Price above sell threshold
    (                                                          # Momentum filter (any one)
        (dataframe['open'] < dataframe['open'].shift(1)) |   # Current open lower than previous
        (dataframe['rsi_exit'] < 50) |                        # RSI < 50
        (dataframe['rsi_exit'] < dataframe['rsi_exit'].shift(1))  # RSI declining
    ) &
    (dataframe['volume'] > 0)                                  # Has volume
)
```

**Design Rationale**: Unlike SMAIP3v2, SMAOG adds momentum filter conditions when selling, only selling when momentum weakens, avoiding premature exits during strong rallies.

### 4.2 Momentum Filter Condition Details

| Condition | Meaning | Design Purpose |
|-----------|---------|----------------|
| open < open.shift(1) | Current open lower than previous candle | Price starting to weaken |
| RSI(2) < 50 | RSI below neutral line | Momentum turning weak |
| RSI < RSI.shift(1) | RSI declining | Momentum decaying |

**Logic**: Satisfying any one of the above conditions indicates momentum is starting to weaken, acceptable to sell.

### 4.3 Multi-Layer Take-Profit System

| Profit Level | Exit Mechanism | Trigger Condition |
|-------------|----------------|-------------------|
| 10% | ROI take-profit | Immediate effect |
| 5% (after 30 min) | ROI take-profit | Position held over 30 minutes |
| 2% (after 60 min) | ROI take-profit | Position held over 60 minutes |
| 2%+ | Trailing stop activation | Profit exceeds 2% |
| 0.5%+ pullback | Trailing stop trigger | 0.5% pullback from peak |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | EMA50, EMA200 | Trend direction judgment |
| Momentum Indicators | RSI(2) | Exit momentum judgment |
| Offset Indicators | MA × offset | Dynamic buy/sell thresholds |
| Protection Indicators | rolling min | Crash detection |

### 5.2 Optimizable Parameters

The strategy provides rich optimizable parameters:

```python
# Buy parameters
base_nb_candles_buy = IntParameter(16, 45, default=26, optimize=False)
low_offset = DecimalParameter(0.8, 0.99, default=0.968, optimize=False)
buy_trigger = CategoricalParameter(['SMA', 'EMA'], default='SMA', optimize=False)

# Sell parameters
base_nb_candles_sell = IntParameter(16, 45, default=28, optimize=False)
high_offset = DecimalParameter(0.8, 1.1, default=0.985, optimize=False)
sell_trigger = CategoricalParameter(['SMA', 'EMA'], default='EMA', optimize=False)

# Protection parameters (optimizable)
pair_is_bad_0_threshold = DecimalParameter(0.0, 0.600, default=0.555, optimize=True)
pair_is_bad_1_threshold = DecimalParameter(0.0, 0.350, default=0.172, optimize=True)
pair_is_bad_2_threshold = DecimalParameter(0.0, 0.200, default=0.198, optimize=True)
```

**Note**: Buy and sell parameters have `optimize=False` set, meaning these parameters won't be optimized in Hyperopt; only protection parameters will participate in optimization.

---

## VI. Risk Management Features

### 6.1 Three-Layer Crash Protection

The strategy uses 3 layers of rolling window crash detection:

```python
# Short-term protection (10 minutes)
(open.rolling(2).min() - close) / close >= 0.198

# Medium-term protection (1 hour)
(open.rolling(12).min() - close) / close >= 0.172

# Long-term protection (12 hours)
(open.rolling(144).min() - close) / close >= 0.555
```

**Design Philosophy**: Covers crash situations at different time scales, preventing buying during extreme market conditions.

### 6.2 Momentum Exit Filtering

Adds momentum filter conditions when selling, avoiding premature exits during strong rallies:

- Price starting to weaken (open declining)
- Momentum turning weak (RSI < 50)
- Momentum decaying (RSI declining)

### 6.3 Progressive ROI Design

```python
minimal_roi = {
    "0": 0.10,   # Just entered, target 10%
    "30": 0.05,  # After 30 minutes, target drops to 5%
    "60": 0.02   # After 60 minutes, target drops to 2%
}
```

**Design Philosophy**: The longer the holding time, the lower the profit target, avoiding long-term lock-ups.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Three-Layer Crash Protection**: Short, medium, and long-term fully covered, safer than SMAIP3v2
2. **Momentum Exit Filter**: Doesn't sell during strong rallies, maximizing profits
3. **Progressive ROI**: Adjusts profit targets based on holding time
4. **Selective Parameter Optimization**: Protection parameters are optimizable, core parameters fixed

### ⚠️ Limitations

1. **Limited Parameter Optimization**: Buy/sell parameters have `optimize=False` set
2. **Large Stop Loss Space**: 23% stop loss may be too wide for conservative traders
3. **Increased Computation**: 3 rolling window calculations, increasing computational burden

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Clear Uptrend | Default configuration | Strategy's best performance environment |
| High Volatility Market | Raise protection thresholds | Stricter crash detection |
| Long-Term Trading | Adjust ROI timing | Adapt to longer holding periods |

---

## IX. Applicable Market Environment Details

SMAOG is an enhanced version of the SMAIP series, improving safety through multi-layer protection mechanisms, best suited for **clear uptrend markets**, with better protection capabilities during extreme market conditions.

### 9.1 Strategy Core Logic

- **Three-Layer Protection**: 10-minute, 1-hour, 12-hour three levels of crash detection
- **Trend is King**: Only buy when EMA50 > EMA200 and price > EMA200
- **Momentum Exit**: Doesn't sell during strong rallies, waits for momentum to weaken

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:-----------:|:-----------------:|-----------------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | Perfectly matches strategy logic, trend continuation after pullback buy |
| 🔄 Oscillating Uptrend | ⭐⭐⭐⭐☆ | Three-layer protection reduces crash buy risk |
| 📉 Downtrend | ⭐☆☆☆☆ | Trend filter blocks buying, but crash protection will mark more pairs |
| ⚡ High Volatility Sideways | ⭐⭐☆☆☆ | Frequent entries/exits, but three-layer protection may be too sensitive |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| Trading Pairs | Major coins | Good liquidity, crash detection more accurate |
| Rolling Window | Adjust based on coin volatility | Can appropriately relax thresholds for high volatility coins |
| ROI | Can adjust timing parameters | Adapt to different trading styles |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

Strategy logic is more complex than SMAIP3v2, requires understanding:
- Three-layer rolling window crash detection mechanism
- Momentum exit filter conditions
- Progressive ROI design

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|---------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

**Note**: 3 rolling window calculations will increase computational load, recommend appropriately increasing memory configuration.

### 10.3 Backtesting vs Live Trading Differences

- Rolling window calculation performance in live trading may differ from backtesting
- Momentum exit filtering may trigger frequently during high-frequency volatility

### 10.4 Manual Trader Recommendations

1. Understand the logic of three-layer crash protection
2. Observe actual effectiveness of momentum exit filter
3. Adjust protection thresholds based on trading pairs

---

## XI. Summary

**SMAOG** is an enhanced version of the SMAIP series, improving strategy safety through three-layer crash protection mechanisms and momentum exit filtering. Its core value lies in:

1. **Three-Layer Protection**: Short, medium, long-term crash detection fully covered
2. **Momentum Exit**: Doesn't sell during strong rallies, maximizing profits
3. **Progressive ROI**: Dynamically adjusts profit targets based on holding time

For quantitative traders, this is a strategy suitable for use in volatile uptrends, recommend adjusting protection thresholds based on actual trading pairs.