# PRICEFOLLOWING Strategy In-Depth Analysis

> **Strategy Number**: #333 (333rd of 465 strategies)  
> **Strategy Type**: Trend Following + EMA Crossover System  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

PRICEFOLLOWING is a trend-following strategy based on EMA (Exponential Moving Average) crossovers. It uses the crossover between EMA7 and TEMA (Triple Exponential Moving Average) as the core buy/sell signal, with RSI indicator as an optional filter, supplemented by Heikin Ashi candlestick charts for trend confirmation. The strategy design is simple and straightforward, suitable for beginners to learn and understand how moving average crossover systems work.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 2 modes (RSI enabled/disabled), core is EMA7 and TEMA crossover |
| **Sell Condition** | 2 modes (RSI enabled/disabled), triggered by reverse crossover |
| **Protection Mechanism** | Fixed stop loss 10% + Dynamic trailing stop (2%/3% threshold) |
| **Timeframe** | Main timeframe 5m + Informative timeframe 15m (multi-pair monitoring) |
| **Dependencies** | numpy, pandas, talib, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "60": 0.025,  # 2.5% profit exit after 60 minutes
    "30": 0.03,   # 3% profit exit after 30 minutes
    "0": 0.04     # 4% profit exit immediately
}

# Stop loss settings
stoploss = -0.1  # 10% fixed stop loss

# Trailing stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.02       # Start trailing after 3% profit
trailing_stop_positive_offset = 0.03  # Trailing stop distance 2%
```

**Design Rationale**:
- **Tiered ROI**: Higher profit targets require shorter holding periods, reflecting a "take profits quickly" philosophy
- **Dual stop loss mechanism**: Fixed 10% stop loss as a safety net, trailing stop to lock in floating profits
- **Trailing trigger condition**: Trailing stop only activates after profit reaches 3%, avoiding premature exit due to minor fluctuations

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'limit',
    'stoploss_on_exchange': False
}

order_time_in_force = {
    'buy': 'gtc',
    'sell': 'gtc'
}
```

**Design Rationale**:
- All orders use limit orders to avoid slippage
- GTC (Good Till Cancel) order type, orders remain active until filled or cancelled
- Stop loss not executed on exchange, managed internally by Freqtrade

---

## III. Buy Condition Details

### 3.1 Optimizable Parameters

The strategy provides 3 buy-related optimizable parameters:

| Parameter Name | Type | Range | Default | Description |
|----------------|------|-------|---------|-------------|
| `rsi_value` | IntParameter | 1-50 | 30 | RSI buy threshold |
| `rsi_enabled` | BooleanParameter | True/False | False | Whether to enable RSI filter |
| `ema_pct` | DecimalParameter | 0.0001-0.1 | 0.004 | EMA difference percentage threshold (defined but not used in code) |

### 3.2 Buy Condition Logic

#### Mode 1: RSI Enabled (rsi_enabled = True)

```python
# Condition combination
Conditions = [
    dataframe['rsi'] < self.rsi_value.value,           # RSI < 30 (default)
    qtpylib.crossed_below(dataframe['ema7'], dataframe['tema'])  # EMA7 crosses below TEMA
]
```

**Logic Interpretation**:
1. RSI indicator below threshold (default 30), indicating oversold market condition
2. EMA7 crosses below TEMA from above, indicating short-term trend weakening
3. Buy signal triggers when both conditions are met simultaneously

**Note**: This logic appears somewhat contradictory—EMA7 crossing below TEMA is a bearish signal, yet the strategy chooses to buy, possibly reflecting a "contrarian" or "mean reversion" approach.

#### Mode 2: RSI Disabled (rsi_enabled = False, default)

```python
# Condition combination
Conditions = [
    qtpylib.crossed_below(dataframe['ema7'], dataframe['tema']),  # EMA7 crosses below TEMA
    dataframe['tema'] < dataframe['tema'].shift(1)                 # TEMA declining
]
```

**Logic Interpretation**:
1. EMA7 crosses below TEMA
2. TEMA is in a downtrend (current value < previous candle value)
3. Buy signal triggers when both conditions are met simultaneously

**Core Philosophy**: Buy during TEMA decline when short-term EMA7 also crosses below it. This is a "buy the dip" strategy, possibly related to mean reversion or bottom-fishing logic.

### 3.3 Buy Condition Summary

| Mode | Condition # | Core Logic | Description |
|------|-------------|------------|-------------|
| RSI Enabled | Condition 1 | RSI < threshold | Oversold filter |
| RSI Enabled | Condition 2 | EMA7 crosses below TEMA | Moving average crossover signal |
| RSI Disabled | Condition 1 | EMA7 crosses below TEMA | Moving average crossover signal |
| RSI Disabled | Condition 2 | TEMA downtrend | Trend confirmation |

---

## IV. Sell Logic Details

### 4.1 Sell Condition Logic

#### Mode 1: RSI Sell Enabled (sell_rsi_enabled = True, default)

```python
conditions = [
    dataframe['rsi'] < self.sell_rsi_value.value,                 # RSI < 70 (default)
    qtpylib.crossed_above(dataframe['ema7'], dataframe['tema'])   # EMA7 crosses above TEMA
]
```

**Logic Interpretation**:
1. RSI below 70 (not overbought condition)
2. EMA7 crosses above TEMA
3. Sell signal triggers when both conditions are met simultaneously

**Note**: RSI < 70 condition is quite loose and practically doesn't serve as an effective filter.

#### Mode 2: RSI Sell Disabled (sell_rsi_enabled = False)

```python
conditions = [
    qtpylib.crossed_above(dataframe['ema7'], dataframe['tema'])   # EMA7 crosses above TEMA
]
```

**Logic Interpretation**:
- Single condition: Sell when EMA7 crosses above TEMA

### 4.2 Sell Condition Summary

| Mode | Condition # | Core Logic | Description |
|------|-------------|------------|-------------|
| RSI Enabled | Condition 1 | RSI < 70 | Non-overbought filter |
| RSI Enabled | Condition 2 | EMA7 crosses above TEMA | Moving average crossover signal |
| RSI Disabled | Condition 1 | EMA7 crosses above TEMA | Sole signal |

### 4.3 ROI Forced Exit

The strategy sets a tiered ROI exit mechanism:

| Holding Time | Profit Threshold | Description |
|--------------|------------------|-------------|
| Immediately | 4% | Exit if 4% profit immediately after buy |
| 30 minutes | 3% | Exit at 3% profit after 30 minutes |
| 60 minutes | 2.5% | Exit at 2.5% profit after 60 minutes |

**Note**: `ignore_roi_if_buy_signal = True`, meaning ROI is ignored if a buy signal exists. However, this is sell logic, and this setting mainly affects holding decisions.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | EMA7, EMA24, TEMA(7) | Moving average system, core trading signals |
| Momentum Indicators | RSI | Overbought/oversold determination |
| Trend Indicators | ADX | Trend strength (calculated but not used in code) |
| Trend Indicators | MACD | Trend direction (calculated but not used in code) |
| Trend Indicators | SAR | Parabolic SAR (calculated but not used in code) |
| Cycle Indicators | Hilbert Sine Wave | Cycle analysis (calculated but not used in code) |
| Chart Patterns | Heikin Ashi | Trend smoothing, price confirmation |

### 5.2 Informative Timeframe Indicators (15m)

The strategy uses 15 minutes as the information layer to monitor multiple pairs:

```python
def informative_pairs(self):
    return [
        ("ETH/USDT", "15m"),
        ("BTC/USDT", "15m"),
        ("RVN/USDT", "15m")
    ]
```

**Usage Explanation**:
- Provides higher-level market trend reference
- Can be used for multi-pair correlation analysis
- Defined but not actually used in trading logic

### 5.3 Heikin Ashi Candlesticks

The strategy calculates Heikin Ashi indicators:

```python
heikinashi = qtpylib.heikinashi(dataframe)
dataframe['ha_open'] = heikinashi['open']
dataframe['ha_close'] = heikinashi['close']
dataframe['ha_high'] = heikinashi['high']
dataframe['ha_low'] = heikinashi['low']
```

**Heikin Ashi Characteristics**:
- Smooths price fluctuations, filters market noise
- More clearly displays trend direction
- Calculated but not used in core trading logic

---

## VI. Risk Management Features

### 6.1 Dual Stop Loss Mechanism

| Stop Loss Type | Parameter Value | Trigger Condition | Description |
|---------------|-----------------|-------------------|-------------|
| Fixed Stop Loss | -10% | Any case with 10% loss | Hard protection |
| Trailing Stop | +2% | Activates after 3% profit | Locks in floating profits |

**Trailing Stop Workflow**:
1. Wait for profit to reach 3% after buy (`trailing_stop_positive_offset`)
2. Activate trailing stop, stop line follows price at 2% distance (`trailing_stop_positive`)
3. Exit when price retraces to touch the stop line

### 6.2 Tiered ROI Exit

```
Holding Time        Profit Threshold
────────────────────────────────────
Immediately         4%
30 minutes          3%
60 minutes          2.5%
```

**Design Rationale**: Longer holding times require lower profit targets, encouraging timely profit-taking.

### 6.3 Order Execution Protection

- **Limit Orders**: Avoid market order slippage
- **Profit-Only Sell**: `sell_profit_only = True`, only sell when profitable
- **Signal Protection**: `ignore_roi_if_buy_signal = True`, don't force ROI exit when buy signal exists

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Simple Logic**: Core is just EMA crossover, easy to understand and maintain
2. **Optimizable Parameters**: Provides 5 Hyperopt optimizable parameters
3. **Dual Stop Loss Protection**: Fixed stop loss + trailing stop dual safeguard
4. **Information Layer Monitoring**: 15-minute timeframe multi-pair monitoring provides market overview
5. **Short Startup Period**: `startup_candle_count = 15`, only needs 15 candles to start calculating

### ⚠️ Limitations

1. **Contradictory Buy Logic**: EMA7 crossing below TEMA is bearish signal, but strategy chooses to buy, logic is unclear
2. **Redundant Indicators**: Calculated ADX, MACD, SAR, Hilbert indicators but not used in trading logic
3. **Loose RSI Filter**: RSI < 70 for selling hardly constitutes an effective filter
4. **Unused Parameter**: `ema_pct` parameter defined but not actually applied in code
5. **Unutilized Information Layer**: 15-minute data fetched but not used in strategy

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Oscillating Downtrend | RSI Enabled | Use RSI oversold for bottom fishing |
| Trending Down | Default Configuration | Buy during TEMA decline |
| Rapid Fluctuation | Trailing Stop | Lock in floating profits |
| High Volatility Pairs | Widen Stop Loss | Avoid premature stop out |

---

## IX. Applicable Market Environment Details

PRICEFOLLOWING is a trend-following strategy based on moving average crossovers. From the code logic, it adopts a "buy on dips, sell on rallies" contrarian approach, opposite to traditional trend-following strategies.

### 9.1 Strategy Core Logic

- **Buy Signal**: EMA7 crosses below TEMA + TEMA downtrend = bottom fishing during decline
- **Sell Signal**: EMA7 crosses above TEMA = profit taking during rise
- **Core Philosophy**: Mean reversion, buy low sell high, not chase high sell low

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:-------------------|:---------|
| 📈 Slow Bull Uptrend | ⭐⭐☆☆☆ | Strategy operates contrarian, sells during uptrend and hard to buy back at low prices |
| 🔄 Oscillating Sideways | ⭐⭐⭐⭐⭐ | Mean reversion philosophy, suitable for high sell low buy |
| 📉 Downtrend | ⭐⭐⭐☆☆ | Bottom fishing may succeed, but stop loss risk is high |
| ⚡ Violent Volatility | ⭐⭐☆☆☆ | Trailing stop may be frequently triggered |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| RSI Enabled | True | Safer to buy at RSI oversold |
| RSI Threshold | 25-30 | Lower end of oversold zone |
| Trailing Stop Offset | 0.03-0.05 | Adjust based on pair volatility |
| Timeframe | 5m-15m | Avoid noise from lower timeframes |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

The strategy code is relatively simple, about 200 lines, suitable for beginners to learn basic principles of moving average crossover systems. However, note:

- Understanding of Heikin Ashi indicator
- Difference between EMA and TEMA
- How trailing stop mechanism works

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-5 pairs | 1GB | 2GB |
| 5-20 pairs | 2GB | 4GB |
| 20+ pairs | 4GB | 8GB |

Strategy calculation is small, hardware requirements are low.

### 10.3 Backtest vs Live Trading Differences

- **Signal Lag**: Moving average crossover signals are inherently lagging, live performance may be worse than backtest
- **Slippage Impact**: Limit orders reduce slippage but may not fill
- **Market Changes**: Strategy optimized based on historical data, future markets may change

### 10.4 Manual Trader Recommendations

1. Understand whether "buy on dip" logic suits your trading style
2. Pay attention to TEMA slope changes to confirm trend direction
3. Use larger timeframes (like 1H) to confirm overall market trend
4. Strictly execute stop loss, avoid large losses from failed bottom fishing

---

## XI. Summary

**PRICEFOLLOWING** is a mean reversion strategy based on EMA crossovers. Its core value lies in:

1. **Simple Logic**: Moving average crossover as core signal, easy to understand and implement
2. **Mean Reversion Philosophy**: Buy on dips, sell on rallies, opposite to chasing highs
3. **Sound Risk Control**: Fixed stop loss + trailing stop dual protection

For quantitative traders, this is a good starting point for learning moving average systems. However, be aware of the strategy's contrarian logic and the confusion that many calculated but unused indicators may bring. Recommend thorough backtesting before actual use and adjust parameters based on target market characteristics.

---