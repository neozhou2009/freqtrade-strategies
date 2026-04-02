# RalliV1 Strategy In-Depth Analysis

> **Strategy ID**: #343 (3rd of strategies #341-350 out of 465 total)
> **Strategy Type**: Multi-condition EMA Offset + Elliott Wave Oscillator Trend Following Strategy
> **Timeframe**: 5 minutes (5m) + 1 hour (1h)

---

## I. Strategy Overview

RalliV1 is a complex multi-condition trend following strategy that combines EMA offset price entries, Elliott Wave Oscillator (EWO) for trend determination, and multi-layer RSI filtering. With 6 independent buy conditions and 2 sell conditions, along with extensive hyperparameter optimization space, this strategy offers high customizability. The strategy also includes custom stop-loss logic and trade confirmation mechanisms, demonstrating professional strategy design principles.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 6 independent buy signals, individually optimizable |
| **Sell Conditions** | 2 base sell signals + ROI table + custom stop-loss |
| **Protection Mechanisms** | Fixed stop-loss -30% + trailing stop + custom stop-loss function |
| **Timeframe** | 5 minutes (main) + 1 hour (information layer) |
| **Dependencies** | talib, qtpylib, technical, freqtrade.persistence |
| **Hyperparameters** | 12 optimizable parameters (7 buy + 2 sell + 3 EWO) |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.04,    # Exit at 4% immediately
    "40": 0.032,  # Exit at 3.2% after 40 minutes
    "87": 0.018,  # Exit at 1.8% after 87 minutes
    "201": 0      # No limit after 201 minutes
}

# Stop-loss setting
stoploss = -0.30  # Fixed stop-loss 30%
```

**Design Philosophy**:
- Staged ROI: Pursue higher profits upon entry (4%), gradually lower expectations over time
- Wide stop-loss (-30%): Provides ample room for price fluctuation
- Remove ROI limit after 201 minutes: Let trailing stop dominate exits

### 2.2 Trailing Stop Configuration

```python
trailing_stop = True
trailing_stop_positive = 0.005       # Activate trailing after 0.5% profit
trailing_stop_positive_offset = 0.03  # Trigger stop when price retraces 3% from high
trailing_only_offset_is_reached = True  # Only activate after offset is reached
```

**Trailing Stop Logic**:
- When profit reaches 3%, trailing stop is activated
- Stop-loss line rises with price increases
- Retracement of 0.5% triggers stop

### 2.3 Order Type Configuration

```python
order_time_in_force = {
    'buy': 'gtc',   # Good Till Cancelled
    'sell': 'gtc'   # Good Till Cancelled
}
```

### 2.4 Sell Signal Configuration

```python
use_sell_signal = True           # Enable sell signals
sell_profit_only = True          # Only respond to sell signals when profitable
sell_profit_offset = 0.01        # Only allow sell when profit > 1%
ignore_roi_if_buy_signal = False  # ROI takes priority
```

---

## III. Buy Conditions In Detail

### 3.1 Hyperparameter System

The strategy includes 12 optimizable parameters:

| Parameter Type | Parameter Name | Default | Optimization Range |
|---------------|----------------|---------|-------------------|
| Buy Parameters | base_nb_candles_buy | 14 | 5-80 |
| Buy Parameters | low_offset | 0.975 | 0.9-0.99 |
| Buy Parameters | low_offset_2 | 0.955 | 0.9-0.99 |
| Buy Parameters | rsi_buy | 60 | 30-70 |
| Buy Parameters | rsi_buy_2 | 45 | 30-70 |
| EWO Parameters | ewo_high | 2.327 | 2.0-12.0 |
| EWO Parameters | ewo_high_2 | -2.327 | -6.0-12.0 |
| EWO Parameters | ewo_low | -20.988 | -20.0--8.0 |
| Sell Parameters | base_nb_candles_sell | 24 | 5-80 |
| Sell Parameters | high_offset | 0.991 | 0.95-1.1 |
| Sell Parameters | high_offset_2 | 0.997 | 0.99-1.5 |

### 3.2 Six Buy Conditions In Detail

#### Condition #1: Downtrend EWO High Value Buy

```python
# Condition 1: MA < EMA100, SMA9 < MA, price below MA * low_offset
(dataframe[f'ma_buy_{base_nb_candles_buy}'] < dataframe['ema_100']) &
(dataframe['sma_9'] < dataframe[f'ma_buy_{base_nb_candles_buy}']) &
(dataframe['rsi_fast'] < 35) &
(dataframe['rsi_fast'] > 4) &
(dataframe['close'] < dataframe[f'ma_buy_{base_nb_candles_buy}'] * low_offset) &
(dataframe['EWO'] > ewo_high) &
(dataframe['rsi'] < rsi_buy_2) &
(dataframe['volume'] > 0) &
(dataframe['close'] < dataframe[f'ma_sell_{base_nb_candles_sell}'] * high_offset)
```

**Logic Breakdown**:
- Trend determination: MA < EMA100, in downtrend
- Price position: Close price below 97.5% of MA
- EWO condition: EWO > 2.327 (positive value, indicates possible trend reversal)
- RSI filter: RSI < 45, fast RSI between 4-35

#### Condition #2: Downtrend EWO Negative Value Buy (Enhanced)

```python
# Condition 2: Similar to condition 1, but looser EWO condition, stricter RSI requirement
(dataframe[f'ma_buy_{base_nb_candles_buy}'] < dataframe['ema_100']) &
(dataframe['sma_9'] < dataframe[f'ma_buy_{base_nb_candles_buy}']) &
(dataframe['rsi_fast'] < 35) &
(dataframe['rsi_fast'] > 4) &
(dataframe['close'] < dataframe[f'ma_buy_{base_nb_candles_buy}'] * low_offset_2) &
(dataframe['EWO'] > ewo_high_2) &
(dataframe['rsi'] < rsi_buy_2) &
(dataframe['volume'] > 0) &
(dataframe['close'] < dataframe[f'ma_sell_{base_nb_candles_sell}'] * high_offset) &
(dataframe['rsi'] < 25)  # Additional condition: RSI < 25
```

**Feature**: Larger price discount (95.5%), but requires RSI < 25

#### Condition #3: Downtrend EWO Low Value Buy

```python
# Condition 3: Buy when EWO is negative
(dataframe[f'ma_buy_{base_nb_candles_buy}'] < dataframe['ema_100']) &
(dataframe['sma_9'] < dataframe[f'ma_buy_{base_nb_candles_buy}']) &
(dataframe['rsi_fast'] < 35) &
(dataframe['rsi_fast'] > 4) &
(dataframe['close'] < dataframe[f'ma_buy_{base_nb_candles_buy}'] * low_offset) &
(dataframe['EWO'] < ewo_low) &  # EWO < -20.988, deep negative value
(dataframe['volume'] > 0) &
(dataframe['close'] < dataframe[f'ma_sell_{base_nb_candles_sell}'] * high_offset)
```

**Feature**: Enter when EWO is extremely negative, catching oversold bounces

#### Condition #4: Uptrend EWO High Value Buy

```python
# Condition 4: MA > EMA100, in uptrend
(dataframe[f'ma_buy_{base_nb_candles_buy}'] > dataframe['ema_100']) &
(dataframe['rsi_fast'] < 35) &
(dataframe['rsi_fast'] > 4) &
(dataframe['close'] < dataframe[f'ma_buy_{base_nb_candles_buy}'] * low_offset) &
(dataframe['EWO'] > ewo_high) &
(dataframe['rsi'] < rsi_buy) &  # Use rsi_buy (default 60)
(dataframe['volume'] > 0) &
(dataframe['close'] < dataframe[f'ma_sell_{base_nb_candles_sell}'] * high_offset)
```

**Feature**: Finding pullback buying opportunities in uptrend

#### Condition #5: Uptrend EWO Negative Value Buy (Enhanced)

```python
# Condition 5: Similar to condition 4, but requires RSI < 25
(dataframe[f'ma_buy_{base_nb_candles_buy}'] > dataframe['ema_100']) &
(dataframe['rsi_fast'] < 35) &
(dataframe['rsi_fast'] > 4) &
(dataframe['close'] < dataframe[f'ma_buy_{base_nb_candles_buy}'] * low_offset_2) &
(dataframe['EWO'] > ewo_high_2) &
(dataframe['rsi'] < rsi_buy) &
(dataframe['volume'] > 0) &
(dataframe['close'] < dataframe[f'ma_sell_{base_nb_candles_sell}'] * high_offset) &
(dataframe['rsi'] < 25)
```

#### Condition #6: Uptrend EWO Low Value Buy

```python
# Condition 6: EWO is negative in uptrend
(dataframe[f'ma_buy_{base_nb_candles_buy}'] > dataframe['ema_100']) &
(dataframe['rsi_fast'] < 35) &
(dataframe['rsi_fast'] > 4) &
(dataframe['close'] < dataframe[f'ma_buy_{base_nb_candles_buy}'] * low_offset) &
(dataframe['EWO'] < ewo_low) &
(dataframe['volume'] > 0) &
(dataframe['close'] < dataframe[f'ma_sell_{base_nb_candles_sell}'] * high_offset)
```

### 3.3 Six Buy Conditions Classification

| Condition Group | Condition # | Core Logic |
|----------------|------------|------------|
| Downtrend Group | #1, #2, #3 | MA < EMA100, looking for reversal in downtrend |
| Uptrend Group | #4, #5, #6 | MA > EMA100, looking for pullback in uptrend |
| EWO High Value Group | #1, #4 | EWO > ewo_high, trend strength confirmation |
| EWO Negative Value Group | #2, #5 | EWO > ewo_high_2 + RSI < 25, dual confirmation |
| EWO Low Value Group | #3, #6 | EWO < ewo_low, oversold bounce |

---

## IV. Sell Logic In Detail

### 4.1 Tiered ROI Take-Profit System

The strategy uses a tiered ROI mechanism:

```
Time (minutes)    ROI Threshold    Description
────────────────────────────────────
0                 4%               Pursue 4% profit upon entry
40                3.2%             Lower expectations after 40 minutes
87                1.8%             Further lower after 87 minutes
201               0%               Remove ROI limit
```

**Design Philosophy**: High confidence upon entry expecting high profits; as time passes, lower expectations and let trailing stop dominate.

### 4.2 Sell Signals (2 Conditions)

#### Sell Signal #1: Uptrend Confirmation

```python
(dataframe['hma_50'] > dataframe['ema_100']) &           # HMA50 > EMA100
(dataframe['close'] > dataframe['sma_9']) &              # Price > SMA9
(dataframe['close'] > dataframe[f'ma_sell_{base_nb_candles_sell}'] * high_offset_2) &  # Price above sell MA
(dataframe['volume'] > 0) &
(dataframe['rsi_fast'] > dataframe['rsi_slow'])           # Fast RSI > Slow RSI
```

**Logic**: Sell when price breaks above multiple moving averages and RSI shows upward momentum.

#### Sell Signal #2: Downtrend Exit

```python
(dataframe['close'] < dataframe['ema_100']) &             # Price < EMA100
(dataframe['close'] > dataframe[f'ma_sell_{base_nb_candles_sell}'] * high_offset) &  # Price above sell MA
(dataframe['volume'] > 0) &
(dataframe['rsi_fast'] > dataframe['rsi_slow'])           # Fast RSI > Slow RSI
```

**Logic**: In downtrend, exit when price rebounds to a certain level.

### 4.3 Custom Stop-Loss Function

```python
def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs) -> float:
    if current_profit < 0.001 and current_time - timedelta(minutes=140) > trade.open_date_utc:
        return -0.005  # Set 0.5% stop-loss if holding > 140 minutes with no profit
    return 1  # Use default stop-loss otherwise
```

**Logic**: If position held for more than 140 minutes (approximately 2.3 hours) with no profit, trigger a tight 0.5% stop-loss.

### 4.4 Sell Confirmation Function

```python
def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                       rate: float, time_in_force: str, sell_reason: str,
                       current_time: datetime, **kwargs) -> bool:
    if sell_reason in ['sell_signal']:
        if (last_candle['rsi'] < 45) and (last_candle['hma_50'] > last_candle['ema_100']):
            return False  # Reject sell
    return True
```

**Logic**: If RSI < 45 and HMA50 > EMA100 (uptrend), reject sell signal and continue holding.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend | EMA(9, 14, 100) | Trend determination and price offset baseline |
| Trend | SMA(9) | Short-term trend confirmation |
| Trend | HMA(50, 9) | Hull Moving Average, for sell determination |
| Oscillator | RSI(14) | Standard RSI |
| Oscillator | RSI_fast(4) | Fast RSI, for buy filtering |
| Oscillator | RSI_slow(20) | Slow RSI, for sell filtering |
| Special | EWO(50, 200) | Elliott Wave Oscillator, trend strength determination |

### 5.2 Elliott Wave Oscillator (EWO)

```python
def EWO(dataframe, ema_length=5, ema2_length=35):
    ema1 = ta.EMA(df, timeperiod=ema_length)
    ema2 = ta.EMA(df, timeperiod=ema2_length)
    emadif = (ema1 - ema2) / df['low'] * 100
    return emadif
```

**EWO Usage**:
- Positive value (> ewo_high): Trend upward, possible buy
- Negative value (< ewo_low): Oversold condition, possible bounce
- Between -20.988 and 2.327: Neutral zone

### 5.3 Information Timeframe (1h)

The strategy declares 1 hour as information timeframe, but it's not actually used in the code. This may be a reserved extension interface.

---

## VI. Risk Management Features

### 6.1 Multiple Stop-Loss Mechanisms

```
Stop-Loss Priority: ROI Take-Profit > Trailing Stop > Custom Stop-Loss > Fixed Stop-Loss

1. ROI Take-Profit: Staged exits, from 4% down to 0%
2. Trailing Stop: Activates at 3% profit, triggers on 0.5% retracement
3. Custom Stop-Loss: Triggers 0.5% stop-loss after 140 minutes without profit
4. Fixed Stop-Loss: Maximum 30% loss
```

### 6.2 Sell Signal Filtering

| Filter Condition | Effect |
|-----------------|--------|
| sell_profit_only = True | Only respond to sell signals when profitable |
| sell_profit_offset = 0.01 | Only allow sell when profit > 1% |
| confirm_trade_exit | Reject sell when RSI < 45 and in uptrend |

### 6.3 Dynamic MA Offset

The strategy uses dynamically calculated MA values as price offset baselines:

```python
# Price discount when buying
close < ma_buy * low_offset   # Discounted buy

# Price premium when selling
close > ma_sell * high_offset # Premium sell
```

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Multi-dimensional entry**: 6 buy conditions covering uptrend and downtrend, increasing signal opportunities
2. **Rich hyperparameters**: 12 optimizable parameters for different market adaptation
3. **Smart stop-loss**: Custom stop-loss function tightens when position held too long
4. **Sell confirmation mechanism**: confirm_trade_exit prevents premature selling in uptrend
5. **EWO innovative application**: Uses Elliott Wave Oscillator to determine trend strength

### ⚠️ Limitations

1. **High complexity**: 6 buy conditions + multiple indicators, difficult to understand and optimize
2. **Many hyperparameters**: 12 parameters need extensive backtesting to optimize, overfitting risk
3. **High computational load**: Requires calculating multiple EMAs and EWO, performance demanding
4. **Overlapping conditions**: Some buy conditions overlap, may reduce actual effectiveness
5. **Unused 1-hour timeframe**: Declared but not implemented in code

---

## VIII. Applicable Scenarios Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Oscillating uptrend | Default configuration | Find entry opportunities during pullbacks |
| Strong trend uptrend | Adjust ewo_high | Raise high value threshold to reduce signals |
| Weak trend/sideways | Adjust stop-loss | Tighten stop-loss, reduce holding time |
| High volatility assets | Adjust offset parameters | Relax low_offset and high_offset |

---

## IX. Applicable Market Environment In Detail

RalliV1 is a **multi-condition comprehensive strategy**. Based on its code architecture, it is most suitable for **oscillating uptrend or trend pullback market environments**, while potentially unstable in extreme one-sided markets.

### 9.1 Core Strategy Logic

- **Multi-dimensional entry**: Cover different market states through 6 conditions
- **Trend + reversal combination**: Capture both trend continuation and reversal opportunities
- **EWO filtering**: Use Elliott Wave Oscillator to determine trend strength

### 9.2 Performance in Different Markets

| Market Type | Rating | Reason Analysis |
|:-----------:|:------:|-----------------|
| 📈 Slow bull oscillation | ⭐⭐⭐⭐⭐ | Multiple conditions capture pullback opportunities, excellent performance |
| 🔄 Range oscillation | ⭐⭐⭐⭐☆ | Many signals, watch for fees |
| 📉 One-sided downtrend | ⭐⭐☆☆☆ | May trigger frequent stop-losses |
| ⚡️ Rapid surge | ⭐⭐⭐☆☆ | Some conditions may miss entries |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|--------------|-------------------|-------------|
| stoploss | -0.30 | Default is wide, adjust based on risk tolerance |
| trailing_stop_positive_offset | 0.03 | Activate trailing after 3% profit |
| sell_profit_offset | 0.01 | Only respond to sell when profit > 1% |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Curve

RalliV1 is a complex strategy containing:
- 6 buy conditions
- 2 sell conditions
- 12 optimizable parameters
- Custom stop-loss function
- Sell confirmation mechanism

Beginners need considerable time to understand each component's function.

### 10.2 Hardware Requirements

| Trading Pairs | Minimum Memory | Recommended Memory |
|--------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-30 pairs | 4GB | 8GB |
| 30+ pairs | 8GB | 16GB |

Due to multiple EMA and EWO calculations, a capable VPS is recommended.

### 10.3 Backtest vs. Live Trading Differences

- **Backtest risk**: 12 parameters极易 lead to overfitting
- **Live recommendation**: Use Walk-Forward analysis to verify parameter stability
- **Optimization strategy**: Optimize parameters in batches, avoid optimizing all at once

### 10.4 Manual Trader Recommendations

Not recommended for manual traders to directly replicate this strategy because:
- Too many conditions, difficult to judge manually
- Need real-time calculation of multiple EMAs and EWO
- Suggest borrowing EWO indicator concept, simplify conditions

---

## XI. Summary

**RalliV1** is a **complex yet flexible multi-condition trend following strategy**. Its core value lies in:

1. **Multi-dimensional coverage**: 6 buy conditions cover different market states, increasing signal opportunities
2. **Tunable parameters**: 12 optimizable parameters adapt to different assets and markets
3. **Smart risk control**: Custom stop-loss + sell confirmation, multi-layer protection

For quantitative traders, RalliV1 is a good example for learning complex strategy design. It demonstrates how to combine multiple technical indicators into a complete trading system, while also reminding us: complexity is a double-edged sword that needs to be used cautiously.

If using this strategy, it is recommended to:
- Backtest with default parameters first to understand baseline performance
- Optimize a small number of parameters at a time to avoid overfitting
- Use Walk-Forward analysis to verify parameter stability
- Practice proper money management and diversify risk