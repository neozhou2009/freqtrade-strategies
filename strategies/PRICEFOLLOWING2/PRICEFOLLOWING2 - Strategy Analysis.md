# PRICEFOLLOWING2 Strategy In-Depth Analysis

> **Strategy Number**: #334 (334th of 465 strategies)  
> **Strategy Type**: Moving Average Crossover Trend Following + Multiple Confirmation Mechanism  
> **Timeframe**: 15 minutes (15m)

---

## I. Strategy Overview

PRICEFOLLOWING2 is an upgraded version of the PRICEFOLLOWING strategy, adopting a longer timeframe (15 minutes) and stricter buy/sell confirmation mechanisms. While retaining the core moving average crossover logic, the strategy adds price-to-Heikin Ashi close price relationship judgment and EMA difference percentage filtering, improving signal reliability.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 2 modes, includes EMA difference percentage filtering by default |
| **Sell Condition** | 2 modes, includes triple confirmation mechanism by default |
| **Protection Mechanism** | Stop loss -10% + trailing stop mechanism |
| **Timeframe** | Main timeframe 15m + informative timeframe 15m |
| **Dependencies** | talib, qtpylib, numpy, pandas |

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
stoploss = -0.1  # Fixed stop loss 10%

# Trailing stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.02      # Start trailing after 2% profit
trailing_stop_positive_offset = 0.03  # Trigger point 3%
```

**Design Rationale**:
- Time-decaying ROI targets encourage short-term profits
- Trailing stop activates after 3% profit to lock in gains
- Fixed 10% stop loss provides last line of defense

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',           # Limit buy
    'sell': 'limit',          # Limit sell
    'stoploss': 'limit',      # Limit stop loss
    'stoploss_on_exchange': False  # Stop loss not executed on exchange
}

order_time_in_force = {
    'buy': 'gtc',    # Good Till Cancelled
    'sell': 'gtc'
}
```

---

## III. Buy Condition Details

### 3.1 Optimizable Parameters

The strategy provides multiple optimizable parameters supporting Hyperopt hyperparameter optimization:

| Parameter Name | Type | Range | Default | Description |
|----------------|------|-------|---------|-------------|
| `rsi_value` | Int | 1-50 | 30 | RSI buy threshold |
| `rsi_enabled` | Boolean | - | False | Whether to enable RSI filter |
| `ema_pct` | Decimal | 0.0001-0.1 | 0.004 | EMA difference percentage threshold |

### 3.2 Buy Condition Logic

#### Mode 1: RSI Filter Enabled (rsi_enabled = True)
```python
Condition 1: RSI < rsi_value (default < 30)
Condition 2: EMA7 crosses below TEMA (crossover signal)
```

**Logic Explanation**:
- RSI below threshold indicates oversold condition
- EMA7 crossing below TEMA indicates short-term trend may be converting upward

#### Mode 2: RSI Filter Disabled (rsi_enabled = False, default)
```python
Condition 1: EMA7 crosses below TEMA (crossover signal)
Condition 2: ((last_tema - last_ema7) / last_tema) < ema_pct (default 0.004)
```

**Logic Explanation**:
- EMA7 and TEMA difference relative to TEMA ratio is below threshold
- This requires two moving averages to be close enough, reducing false breakouts

### 3.3 Differences from PRICEFOLLOWING

| Comparison Item | PRICEFOLLOWING | PRICEFOLLOWING2 |
|-----------------|----------------|-----------------|
| Timeframe | 5 minutes | 15 minutes |
| Buy Condition (RSI off) | EMA crossover + TEMA decline | EMA crossover + EMA difference percentage |
| Sell Condition (RSI off) | EMA crossover only | EMA crossover + price confirmation + percentage |

---

## IV. Sell Logic Details

### 4.1 Optimizable Parameters

| Parameter Name | Type | Range | Default | Description |
|----------------|------|-------|---------|-------------|
| `sell_rsi_value` | Int | 25-100 | 70 | RSI sell threshold |
| `sell_rsi_enabled` | Boolean | - | True | Whether to enable RSI sell filter |
| `ema_sell_pct` | Decimal | 0.0001-0.1 | 0.003 | EMA difference sell threshold |

### 4.2 Sell Condition Logic

#### Mode 1: RSI Sell Filter Enabled (sell_rsi_enabled = True, default)
```python
Condition 1: RSI < sell_rsi_value (default < 70)
Condition 2: EMA7 crosses above TEMA
```

**Logic Explanation**:
- RSI condition ensures selling when price is not overheated
- EMA7 crossing above TEMA indicates short-term momentum weakening

#### Mode 2: RSI Sell Filter Disabled (sell_rsi_enabled = False)
```python
Condition 1: EMA7 crosses above TEMA
Condition 2: best_bid < ha_close (best bid below Heikin Ashi close price)
Condition 3: ((last_tema - last_ema7) / last_ema7) < ema_sell_pct
```

**Logic Explanation**:
- All three conditions must be met simultaneously, forming strict sell confirmation
- best_bid < ha_close indicates current price is below smoothed price
- EMA difference percentage ensures trend has confirmed reversal

### 4.3 Sell Signal Comparison

| Strategy | Number of Conditions | Confirmation Mechanism |
|----------|---------------------|------------------------|
| PRICEFOLLOWING | 1 | EMA crossover only |
| PRICEFOLLOWING2 | 3 | EMA crossover + price confirmation + percentage |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Moving Averages** | EMA7, EMA24, TEMA(7) | Trend judgment, crossover signals |
| **Momentum** | RSI, ADX | Overbought/oversold judgment, trend strength |
| **Trend** | MACD, SAR | Trend confirmation, stop loss reference |
| **Candlestick** | Heikin Ashi | Smooth price fluctuation, price confirmation |
| **Cycle** | Hilbert Transform (Sine) | Cycle identification |

### 5.2 Informative Timeframe Indicators (15m)

The strategy uses 15 minutes as the information layer, providing higher-level trend judgment:

- **ETH/USDT 15m**: Ethereum trend reference
- **BTC/USDT 15m**: Bitcoin trend reference
- **RVN/USDT 15m**: Altcoin market sentiment reference

### 5.3 Indicator Calculation Code

```python
# Core indicator calculation
dataframe['ema7'] = ta.EMA(dataframe, timeperiod=7)
dataframe['ema24'] = ta.EMA(dataframe, timeperiod=24)
dataframe['tema'] = ta.TEMA(dataframe, timeperiod=7)
dataframe['rsi'] = ta.RSI(dataframe)
dataframe['adx'] = ta.ADX(dataframe)
dataframe['sar'] = ta.SAR(dataframe)

# MACD
macd = ta.MACD(dataframe)
dataframe['macd'] = macd['macd']
dataframe['macdsignal'] = macd['macdsignal']
dataframe['macdhist'] = macd['macdhist']

# Heikin Ashi
heikinashi = qtpylib.heikinashi(dataframe)
dataframe['ha_open'] = heikinashi['open']
dataframe['ha_close'] = heikinashi['close']

# Hilbert Transform
hilbert = ta.HT_SINE(dataframe)
dataframe['htsine'] = hilbert['sine']
dataframe['htleadsine'] = hilbert['leadsine']
```

---

## VI. Risk Management Features

### 6.1 Tiered Take Profit System

The strategy adopts a tiered take profit mechanism, combining ROI table and trailing stop:

```
Holding Time    Target Return    Trigger Condition
─────────────────────────────────────────────────────
0 minutes       4%               Effective immediately
30 minutes      3%               Time decay
60 minutes      2.5%             Further decay
Profit 3%       Trailing stop activates   Lock in profits
```

### 6.2 Trailing Stop Mechanism

```python
trailing_stop = True                    # Enable trailing stop
trailing_only_offset_is_reached = True  # Only activate after offset reached
trailing_stop_positive = 0.02           # Trail distance 2%
trailing_stop_positive_offset = 0.03   # Trigger point 3%
```

**How It Works**:
- After profit reaches 3%, trailing stop begins working
- Stop line follows highest price upward at 2% distance
- When price retraces more than 2%, triggers stop loss sell

### 6.3 Multiple Confirmation Mechanism

PRICEFOLLOWING2's sell signal is stricter than PRICEFOLLOWING:

```python
# Default sell requires three conditions simultaneously
conditions.append(qtpylib.crossed_above(dataframe['ema7'], dataframe['tema']))
conditions.append(dataframe['best_bid'] < haclose)
conditions.append(((last_tema - last_ema7) / last_ema7) < self.ema_sell_pct.value)
```

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **More Reliable Signals**: Multiple confirmation mechanism reduces false signals
2. **Longer Timeframe**: 15-minute frame filters short-term noise
3. **Price Confirmation**: Heikin Ashi close price provides additional confirmation
4. **Optimizable Parameters**: Supports Hyperopt hyperparameter optimization

### ⚠️ Limitations

1. **Fewer Entry Opportunities**: Multiple confirmations lead to lower signal frequency
2. **More Pronounced Lag**: 15-minute frame reacts more slowly
3. **Single Direction**: Long only, cannot profit from shorts
4. **Information Layer Underutilized**: Defined but not used in strategy logic

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| **Trending Up** | Default configuration (sell_rsi_enabled=True) | Multiple confirmation reduces false breakouts |
| **Oscillating Market** | sell_rsi_enabled=False | Strict sell conditions reduce frequent trading |
| **Rapid Fluctuation** | Not recommended | Signal lag may miss opportunities |
| **Slow Bull Market** | Default configuration | Trailing stop can capture trend |

---

## IX. Applicable Market Environment Details

PRICEFOLLOWING2 is a medium-complexity trend-following strategy, more conservative than PRICEFOLLOWING. Based on its code architecture and logic design, it is best suited for **stable trending markets**, while performing poorly in **rapid fluctuation**.

### 9.1 Strategy Core Logic

- **Timeframe Upgrade**: 15-minute frame is more stable than 5-minute, filters short-term noise
- **Multiple Confirmation**: Selling requires three conditions, more reliable than single condition
- **Price Reference**: Heikin Ashi close price provides smoothed price reference

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:-------------------|:---------|
| 📈 **Trending Up** | ⭐⭐⭐⭐⭐ | Multiple confirmation ensures capturing trend, trailing stop locks in profits |
| 🔄 **Oscillating Sideways** | ⭐⭐⭐☆☆ | Low signal frequency reduces fee losses |
| 📉 **Trending Down** | ⭐⭐☆☆☆ | Long only, no opportunities in downtrend |
| ⚡ **Violent Volatility** | ⭐⭐☆☆☆ | Signal lag may miss rapid opportunities |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| `rsi_enabled` | False | Off by default, use percentage filter |
| `sell_rsi_enabled` | True | RSI sell filter on is more robust |
| `ema_pct` | 0.003-0.005 | Adjust based on pair volatility |
| `stoploss` | -0.08 ~ -0.12 | Adjust based on risk preference |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

Strategy logic is slightly more complex than PRICEFOLLOWING, requiring understanding of:
- EMA difference percentage calculation and meaning
- Heikin Ashi smoothing principle
- Multiple confirmation mechanism synergy

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

### 10.3 Backtest vs Live Trading Differences

- Multiple confirmations may perform well in backtests but may miss optimal entry points in live trading due to delays
- 15-minute frame has fewer signals, requiring longer time to verify effectiveness
- Order book data (best_bid) may be incomplete in backtests

### 10.4 Manual Trader Recommendations

If you want to manually trade similar logic:
1. Use EMA7 and TEMA(7) as main signals
2. Calculate EMA difference percentage to confirm signal strength
3. Reference Heikin Ashi close price to judge price position
4. Set fixed stop loss 8-10%
5. Enable trailing stop after 3% profit

---

## XI. Summary

**PRICEFOLLOWING2** is a conservative upgraded version of PRICEFOLLOWING. Its core value lies in:

1. **More Reliable Signals**: Multiple confirmation mechanism reduces false signals, improves win rate
2. **More Stable Frame**: 15-minute timeframe filters short-term noise
3. **More Complete Risk Control**: Trailing stop + multiple confirmation dual protection
4. **Suitable for Trends**: Can effectively capture trend profits in clear trending markets

For quantitative traders, this is a more robust choice than PRICEFOLLOWING. Although signal frequency is lower, quality is higher. Suitable for traders who prefer fewer but more reliable trades over frequent trading. In stable trending markets, this strategy can effectively capture trend profits; in oscillating markets, due to low signal frequency, fee losses are relatively smaller.

---