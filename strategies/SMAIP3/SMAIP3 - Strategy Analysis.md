# SMAIP3 Strategy In-Depth Analysis

> **Strategy ID**: #354 (354th of 465 strategies)  
> **Strategy Type**: Moving Average Deviation + Trend Filter + Hyperopt Optimization Strategy  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

SMAIP3 is a trend-following strategy based on moving average deviation principles, combining EMA trend filtering, MA deviation buying, and dynamic trailing stop mechanisms. Through the Hyperopt parameter optimization framework, this strategy achieves adaptive adjustment of buy/sell parameters, while including a built-in "bad trading pair" detection mechanism to filter high-risk trading environments.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 composite buy signal requiring 5 conditions to be met simultaneously |
| **Sell Condition** | 1 composite sell signal requiring 2 conditions to be met simultaneously |
| **Protection Mechanism** | Fixed stop-loss (-33.1%) + Trailing stop + Tiered ROI exit + Bad pair filtering |
| **Timeframe** | 5-minute primary timeframe |
| **Dependencies** | talib, pandas, datetime |
| **Special Features** | Hyperopt parameter optimization, bad trading pair detection |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.135,    # Exit immediately with 13.5% profit
    "35": 0.061,    # Exit with 6.1% profit after 35 minutes
    "86": 0.037,    # Exit with 3.7% profit after 86 minutes
    "167": 0        # Exit at break-even after 167 minutes
}

# Stop-loss Setting
stoploss = -0.331  # Fixed 33.1% stop-loss

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.098       # Start trailing after 9.8% profit
trailing_stop_positive_offset = 0.159  # Trigger when profit pulls back to 15.9%
trailing_only_offset_is_reached = True  # Only start trailing when offset is reached
```

**Design Philosophy**:
- ROI uses aggressive time-decreasing design with initial target profit as high as 13.5%
- Stop-loss is relatively wide (-33.1%), giving the strategy enough room for volatility
- Trailing stop is precisely designed: only starts after 9.8% profit, triggers sell when profit pulls back to 15.9%
- Trailing stop offset is higher than activation value, avoiding being shaken out too early

### 2.2 Order Type Configuration

```python
# Using default configuration
process_only_new_candles = True  # Only calculate on new candles
startup_candle_count = 30        # Requires 30 candles for warm-up
```

---

## III. Buy Conditions Detailed Analysis

### 3.1 Protection Mechanism

Strategy includes built-in "bad trading pair" detection mechanism:

```python
# Bad trading pair definition
dataframe['pair_is_bad'] = (
    (((dataframe['open'].shift(12) - dataframe['close']) / dataframe['close']) >= pair_is_bad_1_threshold) |
    (((dataframe['open'].shift(6) - dataframe['close']) / dataframe['close']) >= pair_is_bad_2_threshold)
).astype('int')
```

| Detection Type | Parameter Description | Default Value |
|----------------|----------------------|---------------|
| 12-period ago open price drop | Drop threshold of current price vs 12-period ago open | 13.0% |
| 6-period ago open price drop | Drop threshold of current price vs 6-period ago open | 7.5% |

**Design Purpose**: When price drops significantly in a short time, it's flagged as a high-risk trading pair to avoid buying.

### 3.2 Buy Condition Breakdown

The strategy uses a single composite buy condition requiring all 5 conditions to be met simultaneously:

```python
dataframe.loc[
    (
        (dataframe['ema_50'] > dataframe['ema_200']) &  # Trend filter
        (dataframe['close'] > dataframe['ema_200']) &  # Price above long-term MA
        (dataframe['pair_is_bad'] < 1) &                # Not a bad trading pair
        (dataframe['close'] < dataframe['ma_offset_buy']) &  # Price below deviation MA
        (dataframe['volume'] > 0)                       # Has volume
    ),
    'buy'] = 1
```

| Condition # | Condition Name | Logic Description | Purpose |
|-------------|----------------|-------------------|---------|
| #1 | Trend Filter | EMA50 > EMA200 | Confirm uptrend |
| #2 | Price Position | Close > EMA200 | Price above long-term MA |
| #3 | Bad Pair Filter | pair_is_bad < 1 | Avoid crashing pairs |
| #4 | Deviation Buy | Close < deviation MA | Buy on pullback |
| #5 | Volume Confirmation | Volume > 0 | Filter invalid signals |

### 3.3 Deviation MA Calculation

```python
# Buy deviation MA
ma_offset_buy = SMA/EMA(close, base_nb_candles_buy) * low_offset
# Default: EMA(18) * 0.968
```

**Calculation Logic**:
- Uses 18-period moving average (SMA or EMA)
- Multiplies by 0.968 deviation coefficient
- Forms a buy trigger line below the MA

---

## IV. Sell Logic Detailed Analysis

### 4.1 Tiered ROI Profit-Taking

The strategy uses a four-tier ROI exit mechanism:

```
Holding Time    Target Profit    Signal Name
────────────────────────────────────────────
0 minutes       13.5%            Aggressive profit
35 minutes      6.1%             Medium-term profit
86 minutes      3.7%             Break-even profit
167 minutes     0%               Forced exit
```

### 4.2 Trailing Stop Mechanism

```
Trailing Stop Trigger Process:
├── Profit reaches 9.8% → Start trailing stop
├── Price continues to rise → Stop-loss follows upward
└── Profit pulls back to 15.9% → Trigger sell
```

**Mechanism Features**:
- Requires 9.8% profit to start trailing, avoiding small profits being shaken out
- Offset value of 15.9% is higher than activation value, giving price enough volatility room
- Only starts trailing when offset is reached, reducing invalid triggers

### 4.3 Technical Sell Signal

```python
dataframe.loc[
    (
        (dataframe['close'] > dataframe['ma_offset_sell']) &  # Price above deviation MA
        (dataframe['volume'] > 0)                              # Has volume
    ),
    'sell'] = 1
```

```python
# Sell deviation MA
ma_offset_sell = SMA/EMA(close, base_nb_candles_sell) * high_offset
# Default: EMA(55) * 1.07
```

| Condition # | Condition Name | Logic Description | Purpose |
|-------------|----------------|-------------------|---------|
| #1 | Deviation Sell | Close > deviation MA | Sell when price above target level |
| #2 | Volume Confirmation | Volume > 0 | Filter invalid signals |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Trend | EMA50 | Medium-term trend judgment |
| Trend | EMA200 | Long-term trend judgment |
| Deviation | ma_offset_buy | Dynamic buy trigger line |
| Deviation | ma_offset_sell | Dynamic sell trigger line |
| Risk | pair_is_bad | Bad trading pair detection |

### 5.2 Hyperopt Optimization Parameters

| Parameter Category | Parameter Name | Value Range | Default Value |
|-------------------|----------------|-------------|---------------|
| Buy Parameters | base_nb_candles_buy | 16-60 | 18 |
| Buy Parameters | low_offset | 0.8-0.99 | 0.968 |
| Buy Parameters | buy_trigger | SMA/EMA | EMA |
| Sell Parameters | base_nb_candles_sell | 16-60 | 55 |
| Sell Parameters | high_offset | 0.8-1.1 | 1.07 |
| Sell Parameters | sell_trigger | SMA/EMA | EMA |
| Risk Parameters | pair_is_bad_1_threshold | 0.00-0.30 | 0.13 |
| Risk Parameters | pair_is_bad_2_threshold | 0.00-0.25 | 0.075 |

---

## VI. Risk Management Features

### 6.1 Bad Trading Pair Detection Mechanism

**Detection Logic**:
- 12-period ago open price drop vs current price ≥ 13% → Mark as bad pair
- 6-period ago open price drop vs current price ≥ 7.5% → Mark as bad pair

**Design Purpose**:
- Filter trading pairs with short-term crashes
- Avoid "catching falling knives" risk
- Dynamic adjustment, real-time detection

### 6.2 Trend Filter Dual Insurance

```
Trend Confirmation Mechanism:
├── EMA50 > EMA200 → Confirm short-term trend upward
└── close > EMA200 → Confirm price above long-term MA
```

**Dual Confirmation**: Only buy when both conditions are met, ensuring being in a clear uptrend.

### 6.3 Precision Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.098        # 9.8% activation
trailing_stop_positive_offset = 0.159  # 15.9% trigger
trailing_only_offset_is_reached = True # Only trail when offset reached
```

**Design Highlights**:
- Don't rush to trail, wait until profit reaches a certain level
- Give price enough volatility room
- Avoid being shaken out by small fluctuations

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Strict Trend Confirmation**: EMA50/200 dual filtering ensures buying in uptrend
2. **Bad Pair Filtering**: Avoids buying during crashes, proactive risk control
3. **Optimizable Parameters**: Auto-optimize parameters through Hyperopt framework
4. **Precision Trailing Stop**: Avoids small profits being shaken out
5. **Reasonable Buy Logic**: Trend up + buy on pullback

### ⚠️ Limitations

1. **Wide Stop-Loss**: 33.1% stop-loss may be too large, needs capital management coordination
2. **Parameter Dependency**: Default parameters may not suit all trading pairs
3. **Simple Sell Condition**: Only relies on deviation MA for selling, lacks multiple confirmations
4. **Aggressive Target**: 13.5% initial target may be hard to reach

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| Uptrend Pullback | Default configuration | Best scenario, buy pullbacks |
| Single-direction Rally | Adjust low_offset | May miss entry opportunities |
| Oscillating Market | Reduce trading | Trend filter will reduce signals |
| Single-direction Downtrend | Disable | Trend filter will prevent buying |

---

## IX. Applicable Market Environment Details

SMAIP3 strategy is a **trend-following + pullback buying strategy**. Based on its code architecture and Hyperopt optimization design, it is best suited for **pullback markets in uptrends**, while performing poorly in **oscillating or downtrending markets**.

### 9.1 Strategy Core Logic

- **Trend Confirmation**: EMA50 > EMA200 confirms uptrend
- **Position Confirmation**: close > EMA200 ensures price above long-term MA
- **Pullback Buy**: close < ma_offset_buy buys on pullback
- **Risk Filter**: pair_is_bad avoids crashing pairs
- **Deviation Sell**: close > ma_offset_sell exits at target level

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:------------------|:----------------|
| 📈 Uptrend Pullback | ⭐⭐⭐⭐⭐ | Best scenario, pullback buying most effective |
| 🔄 Sideways Oscillation | ⭐⭐⭐☆☆ | Trend filter reduces signals, occasional trades |
| 📉 Single-direction Downtrend | ⭐☆☆☆☆ | Trend filter prevents buying, basically no signals |
| ⚡️ High Volatility | ⭐⭐☆☆☆ | Bad pair detection may be oversensitive |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| Stop-loss | -0.25 ~ -0.35 | Adjust based on trading pair volatility |
| low_offset | 0.95 ~ 0.98 | Lower to increase entry opportunities |
| high_offset | 1.05 ~ 1.10 | Raise to extend holding time |
| Timeframe | 5m (default) | Try 15m for more stable signals |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

This strategy uses Hyperopt parameter optimization, requiring understanding of:
- EMA indicator's trend judgment principle
- MA deviation buy/sell logic
- Hyperopt parameter optimization usage
- Trailing stop trigger mechanism

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |

### 10.3 Backtesting vs Live Trading Differences

- **Hyperopt Overfitting Risk**: Optimized parameters may be overfitted to historical data
- **Live Trading Notes**: Bad pair detection may be oversensitive
- **Recommendation**: Use out-of-sample data to validate parameter effectiveness

### 10.4 Manual Trader Recommendations

- Wait for EMA50 to cross above EMA200 to confirm uptrend
- Consider buying when price pulls back near EMA50
- Pay attention to stop-loss settings, control single loss
- Can reference "bad trading pair" logic to avoid crashing coins

---

## XI. Summary

**SMAIP3 Strategy** is a **parameter-optimizable trend pullback buying strategy**. Its core value lies in:

1. **Strict Trend Confirmation**: Dual MA filtering ensures buying in uptrend
2. **Proactive Risk Control**: Bad pair detection avoids crash risk
3. **Precision Trailing Stop**: Gives price enough volatility room, avoiding early exit
4. **Optimizable Parameters**: Auto-find optimal parameters through Hyperopt

For quantitative traders, this is a strategy suitable for trending markets, but requires Hyperopt optimization for best results.