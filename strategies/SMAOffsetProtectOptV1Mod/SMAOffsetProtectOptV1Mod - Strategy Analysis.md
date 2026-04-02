# SMAOffsetProtectOptV1Mod Strategy Analysis

> **Strategy Number**: #363 (363rd of 465 strategies)  
> **Strategy Type**: SMA Offset + EWO Protection + RSI Filter Trend Following Strategy  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

SMAOffsetProtectOptV1Mod is a trend-following strategy based on Simple Moving Average offset (SMA Offset), combined with Elliott Wave Oscillator (EWO) as a protection mechanism and RSI as an auxiliary filter. The strategy captures entry opportunities during market pullbacks through a "buy low + trend confirmation" dual logic, while using trailing stops to lock in profits.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signals, can trigger independently |
| **Sell Conditions** | 1 base sell signal + tiered ROI take-profit + trailing stop |
| **Protection Mechanism** | EWO high/low threshold protection + RSI filter |
| **Timeframe** | Main timeframe 5m + informative timeframe 1h |
| **Dependencies** | talib, numpy, pandas, technical (ftt), qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.028,    # Immediate: 2.8%
    "12": 0.016,   # After 12 candles: 1.6%
    "37": 0.005    # After 37 candles: 0.5%
}

# Stop loss settings
stoploss = -0.10  # Fixed stop loss 10%

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.001      # Activate trailing after 0.1% profit
trailing_stop_positive_offset = 0.01  # Start trailing at 1% profit
trailing_only_offset_is_reached = True  # Only enable after offset is reached
```

**Design Philosophy**:
- ROI uses a stepped declining design, encouraging short-term profit taking
- Trailing stop is set conservatively, starting to trail at 1% profit to avoid being stopped out too early
- Fixed 10% stop loss provides the last line of defense

### 2.2 Order Type Configuration

```python
use_sell_signal = True        # Enable sell signal
sell_profit_only = True       # Only use sell signal when profitable
sell_profit_offset = 0.01     # Minimum profit requirement for sell signal: 1%
ignore_roi_if_buy_signal = False  # Do not ignore ROI
```

---

## III. Buy Conditions Detailed

### 3.1 Optimizable Parameters

The strategy uses Freqtrade's parameter optimization system, all key parameters can be optimized via HyperOpt:

| Parameter Type | Parameter Name | Default | Optimization Range | Description |
|----------------|----------------|---------|-------------------|-------------|
| **Buy** | base_nb_candles_buy | 16 | 5-80 | EMA period |
| **Buy** | low_offset | 0.973 | 0.9-0.99 | Price offset coefficient |
| **Buy** | ewo_high | 5.672 | 2.0-12.0 | EWO high threshold |
| **Buy** | ewo_low | -19.931 | -20.0 to -8.0 | EWO low threshold |
| **Buy** | rsi_buy | 59 | 30-70 | RSI buy threshold |
| **Sell** | base_nb_candles_sell | 20 | 5-80 | Sell EMA period |
| **Sell** | high_offset | 1.010 | 0.99-1.1 | Sell price offset |

### 3.2 Buy Conditions Detailed

#### Condition #1: Trend Confirmation Buy
```python
# Logic
- Price below EMA * low_offset (pullback buy)
- EWO > ewo_high (strong trend confirmation)
- RSI < rsi_buy (not overbought)
- Volume > 0 (validity check)
```

**Core Logic**: This is a "trend pullback buy" strategy. When price pulls back below EMA by a certain percentage, if EWO shows strong trend (> ewo_high), it means the trend is still strong and the pullback is a buying opportunity. RSI condition ensures not buying when overheated.

#### Condition #2: Deep Oversold Buy
```python
# Logic
- Price below EMA * low_offset (pullback buy)
- EWO < ewo_low (deeply negative)
- Volume > 0 (validity check)
```

**Core Logic**: This is an "oversold bounce" strategy. When EWO drops to extremely low levels (< ewo_low), it indicates extreme market pessimism and a potential rebound opportunity. This condition doesn't require RSI filtering, focusing on catching rebounds after extreme oversold conditions.

### 3.3 Buy Condition Classification

| Condition Group | Condition Number | Core Logic | Characteristics |
|-----------------|------------------|------------|-----------------|
| Trend Following | Condition #1 | High EWO + RSI filter | Stable, following the trend |
| Contrarian Bottom Fishing | Condition #2 | Low EWO + no RSI limit | Aggressive, catching bounces |

---

## IV. Sell Logic Detailed

### 4.1 Multi-tier Take Profit System

The strategy uses a three-tier ROI take-profit mechanism:

```
Holding Time    Target Profit    Description
────────────────────────────────
Immediate       2.8%             Highest profit target
12 candles     1.6%             Medium-term profit target
37 candles     0.5%             Lowest profit target
```

**Design Philosophy**: The longer the holding time, the lower the profit requirement. Encourages short-term profits while allowing room for longer holds.

### 4.2 Trailing Stop Mechanism

| Parameter | Value | Description |
|-----------|-------|-------------|
| trailing_stop | True | Enable trailing stop |
| trailing_stop_positive | 0.1% | Trailing distance |
| trailing_stop_positive_offset | 1% | Activation threshold |
| trailing_only_offset_is_reached | True | Only enable after threshold reached |

**Working Mechanism**:
1. When profit reaches 1%, trailing stop activates
2. Stop loss line follows price increase, maintaining 0.1% distance
3. Price retracement triggers stop, locking in profit

### 4.3 Base Sell Signal (1)

```python
# Sell signal 1: EMA offset sell
- Price > EMA(base_nb_candles_sell) * high_offset
- Volume > 0
```

**Trigger Condition**: When price rebounds above 1.01x EMA, it indicates short-term overheating and triggers a sell.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Trend | EMA (base_nb_candles_buy) | Buy baseline |
| Trend | EMA (base_nb_candles_sell) | Sell baseline |
| Oscillator | EWO (50, 200) | Trend strength assessment |
| Oscillator | RSI (14) | Overbought/oversold filter |

### 5.2 EWO (Elliott Wave Oscillator) Detailed

EWO is the core protection indicator of this strategy:

```python
def EWO(dataframe, ema_length=5, ema2_length=35):
    ema1 = ta.EMA(df, timeperiod=ema_length)
    ema2 = ta.EMA(df, timeperiod=ema2_length)
    emadif = (ema1 - ema2) / df['close'] * 100
    return emadif
```

**Parameters in Strategy**: fast_ewo = 50, slow_ewo = 200

**Interpretation**:
- EWO positive and large: Short-term EMA above long-term EMA, trend is upward
- EWO negative and small: Short-term EMA below long-term EMA, trend is downward
- EWO near zero: Trend unclear or ranging

### 5.3 Informative Timeframe Indicators (1h)

The strategy uses 1h as the information layer, providing higher-dimension trend judgment:

- Obtains 1h timeframe data for auxiliary analysis
- Although informative_timeframe is defined in code, main logic still executes on 5m

---

## VI. Risk Management Features

### 6.1 EWO Protection Mechanism

EWO (Elliott Wave Oscillator) as the core protection indicator:

| Protection Type | Parameter Description | Default |
|-----------------|----------------------|---------|
| EWO high threshold | Strong trend confirmation | 5.672 |
| EWO low threshold | Extreme oversold identification | -19.931 |

**Protection Logic**:
- When buying, EWO must be > ewo_high or < ewo_low
- Avoids buying when trend is unclear (EWO near zero)

### 6.2 RSI Filter Mechanism

```python
rsi_buy = IntParameter(30, 70, default=59)
```

**Design Philosophy**:
- RSI < rsi_buy ensures not buying in overbought territory
- Only applied to trend confirmation buys (Condition #1)
- Deep oversold buys don't use RSI filtering

### 6.3 Volume Verification

All buy and sell conditions require `volume > 0`:
- Ensures trades occur in valid market conditions
- Avoids trading when liquidity is depleted

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Dual Entry Logic**: Trend following + bottom fishing, adapting to different market phases
2. **Optimizable Parameters**: 7 HyperOpt parameters, suitable for optimization per trading pair
3. **Trailing Stop**: Locks in profits while giving trend room to develop
4. **EWO Protection**: Avoids entering when trend is unclear

### ⚠️ Limitations

1. **Poor Performance in Ranging Markets**: EMA offset strategies tend to get repeatedly stopped out in sideways markets
2. **Parameter Sensitivity**: Default parameters may not suit current markets, requires backtesting and optimization
3. **No Long/Short Distinction**: Strategy is long-only, cannot profit in falling markets
4. **Fixed Stop Loss**: 10% fixed stop may be too conservative or aggressive for highly volatile pairs

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|-------------------------|-------------|
| Clear Trend | Default parameters | Strategy performs best in trending markets |
| High Volatility | Lower low_offset | Increase buy threshold to avoid false breakouts |
| Ranging Market | Use cautiously or raise ROI | Increase take-profit levels to reduce trade frequency |
| Bear Market | Suspend usage | Strategy is long-only, high loss risk in bear markets |

---

## IX. Applicable Market Environment Detailed

SMAOffsetProtectOptV1Mod is a medium-complexity trend following strategy. Based on its code architecture and community long-term live trading experience, it performs best in **markets with clear trends**, while performing poorly in **ranging or falling markets**.

### 9.1 Core Strategy Logic

- **Trend Pullback Buy**: Wait for price to pull back below EMA before buying
- **Dual Protection**: EWO confirms trend + RSI filters overbought
- **Trailing Take Profit**: Activate trailing stop after 1% profit

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|-------------|-------------------|------------------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | Pullback buy + trailing stop perfectly配合 trend |
| 🔄 Ranging/Sideways | ⭐⭐☆☆☆ | Repeated EMA false breakout stops |
| 📉 Downtrend | ⭐☆☆☆☆ | Long-only, continuous losses |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | May get stopped out, but trailing stop provides protection |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|------------------|-------------|
| base_nb_candles_buy | 16-25 | Use longer period for trending markets |
| low_offset | 0.95-0.98 | Lower for high volatility |
| trailing_stop_positive_offset | 0.01-0.02 | Adjust based on pair volatility |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Cost

This strategy has approximately 170 lines of code, medium complexity:
- Need to understand EWO indicator principles
- Need to understand EMA offset strategy logic
- Need to master HyperOpt parameter optimization

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

### 10.3 Differences Between Backtesting and Live Trading

- Backtesting may perform too well due to parameter fitting
- Live trading slippage and fees will reduce returns
- Recommended to test on paper trading first

### 10.4 Recommendations for Manual Traders

Manual traders can learn from:
- EWO indicator for trend strength judgment
- EMA offset for entry price levels
- Trailing stop for position management

---

## XI. Summary

**SMAOffsetProtectOptV1Mod** is a classic EMA offset trend following strategy. Its core value lies in:

1. **Simple and Effective**: EMA offset + EWO protection core logic is clear and easy to understand
2. **Dual Entry**: Trend following + bottom fishing modes adapt to different market phases
3. **Controlled Risk**: Trailing stop + tiered ROI provides multiple layers of protection

For quantitative traders, this is a trend following strategy suitable for beginners to start with, but be aware of drawdown risks in ranging markets. It's recommended to conduct sufficient backtesting and paper trading tests, optimize parameters for target pairs before live trading.

---