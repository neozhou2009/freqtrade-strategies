# Apollo11 Strategy In-Depth Analysis

> **Strategy ID**: #420 (420th of 465 strategies)  
> **Strategy Type**: Multi-Signal Trend Following + Custom Stop Loss + Multi-Layer Protection  
> **Timeframe**: 15 minutes (15m)  
> **Author**: Shane Jones (https://twitter.com/shanejones)  
> **Original Repository**: https://github.com/shanejones/goddard

---

## 1. Strategy Overview

Apollo11 is a complex multi-signal trend following strategy developed by Shane Jones with community contributor assistance. The strategy integrates multiple technical analysis methods including EMA trends, Bollinger Band breakouts, and Fibonacci retracements, equipped with a dynamic stop loss system and 5-layer protection mechanism, making it a "defensive offensive strategy" suitable for intermediate quantitative traders.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 3 independent entry signals, can be independently enabled/disabled |
| **Exit Conditions** | No active exit signals, relies on ROI and custom stop loss |
| **Protection Mechanisms** | 5 protection parameter groups (cooldown, max drawdown, stop loss protection, low profit protection ×2) |
| **Timeframe** | 15 minutes (15m) |
| **Startup Candles** | 480 candles (approximately 5 days of data) |
| **Dependencies** | talib, qtpylib, freqtrade.persistence.Trade |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.10,   # After 0 minutes, exit at 10% profit
    "30": 0.05,  # After 30 minutes, exit at 5% profit
    "60": 0.02,  # After 60 minutes, exit at 2% profit
}

# Stop loss settings
stoploss = -0.16  # 16% fixed stop loss
```

**Design Rationale**:
- ROI table uses progressive take-profit, the longer the time, the lower the take-profit threshold
- Initial target of 10% is relatively high, suitable for catching larger movements
- After 60 minutes drops to 2%, ensuring at least partial profit is locked
- 16% fixed stop loss is relatively wide, giving trades enough room for fluctuation

### 2.2 Trailing Stop Configuration

```python
trailing_stop = False  # Disable standard trailing stop
use_custom_stoploss = True  # Use custom stop loss
use_sell_signal = False  # Disable exit signals
```

**Design Rationale**:
- Disable standard trailing stop, use more flexible custom stop loss logic instead
- Custom stop loss can dynamically adjust based on holding time and profit
- Doesn't rely on technical indicator exits, focuses on entry timing

### 2.3 Custom Stop Loss Logic

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    # Profit protection tiers
    if current_profit > 0.20:  # Profit > 20%
        return 0.04  # Stop loss moves up to 4% profit
    if current_profit > 0.10:  # Profit > 10%
        return 0.03  # Stop loss moves up to 3% profit
    if current_profit > 0.06:  # Profit > 6%
        return 0.02  # Stop loss moves up to 2% profit
    if current_profit > 0.03:  # Profit > 3%
        return 0.01  # Stop loss moves up to 1% profit
    
    # Loss stop loss relief (based on holding time)
    if current_profit <= -0.10:  # Loss > 10%
        if trade.open_date_utc + timedelta(hours=60) < current_time:
            return current_profit / 1.75  # Tighten stop loss after 60 hours
    
    if current_profit <= -0.08:  # Loss > 8%
        if trade.open_date_utc + timedelta(hours=120) < current_time:
            return current_profit / 1.70  # Further tighten after 120 hours
    
    return -1  # Use default stop loss
```

**Stop Loss Logic Details**:

| Profit Range | Stop Loss Position | Protection Effect |
|--------------|-------------------|-------------------|
| > 20% | Lock in 4% profit | Strong protection |
| > 10% | Lock in 3% profit | Medium-strong protection |
| > 6% | Lock in 2% profit | Medium protection |
| > 3% | Lock in 1% profit | Light protection |
| -10% (after 60h) | Dynamic tightening | Time-limited stop loss |
| -8% (after 120h) | Dynamic tightening | Time-limited stop loss |

---

## 3. Entry Conditions Detailed

### 3.1 Signal Control Switches

```python
buy_signal_1 = True  # EMA trend crossover signal
buy_signal_2 = True  # Bollinger Band + Fibonacci signal
buy_signal_3 = True  # Volume-weighted breakout signal
```

Each signal can be independently enabled or disabled for strategy optimization and backtesting analysis.

### 3.2 Entry Signal #1: EMA Trend Crossover + VWMACD

**Indicator Configuration**:
```python
s1_ema_xs = 3    # Ultra-short period EMA
s1_ema_sm = 5    # Short period EMA
s1_ema_md = 10   # Medium period EMA
s1_ema_xl = 50   # Long period EMA
s1_ema_xxl = 240 # Ultra-long period EMA (trend baseline)
```

**Trigger Conditions**:
```python
conditions = [
    dataframe["vwmacd"] < dataframe["signal"],           # VWMACD below signal line
    dataframe["low"] < dataframe["s1_ema_xxl"],           # Low below 240 EMA
    dataframe["close"] > dataframe["s1_ema_xxl"],         # Close above 240 EMA
    qtpylib.crossed_above(dataframe["s1_ema_sm"], dataframe["s1_ema_md"]),  # 5 EMA crosses above 10 EMA
    dataframe["s1_ema_xs"] < dataframe["s1_ema_xl"],      # 3 EMA below 50 EMA
    dataframe["volume"] > 0,                             # Volume exists
]
```

**Logic Interpretation**:
1. **VWMACD Condition**: Volume-weighted MACD below signal line, indicating momentum not yet overheated
2. **Price Position**: Low touches 240 EMA but close is above it, typical "false breakout then return"
3. **EMA Crossover**: 5 EMA crosses above 10 EMA, short-term trend strengthening signal
4. **Relative Position**: 3 EMA below 50 EMA, ensuring not chasing highs
5. **Volume Confirmation**: Must have volume as prerequisite

**Signal Tag**: `buy_signal_1`

### 3.3 Entry Signal #2: Bollinger Band Lower + Fibonacci Support

**Indicator Configuration**:
```python
s2_ema_input = 50          # EMA period
s2_ema_offset_input = -1   # EMA offset
s2_bb_sma_length = 49      # Bollinger Band SMA period
s2_bb_std_dev_length = 64  # Standard deviation period
s2_bb_lower_offset = 3     # Lower band offset (3 standard deviations)
s2_fib_sma_len = 50        # Fibonacci SMA period
s2_fib_atr_len = 14        # ATR period
s2_fib_lower_value = 4.236 # Fibonacci extension coefficient
```

**Trigger Conditions**:
```python
conditions = [
    qtpylib.crossed_above(dataframe["s2_fib_lower_band"], dataframe["s2_bb_lower_band"]),  # Fibonacci lower band crosses above Bollinger lower band
    dataframe["close"] < dataframe["s2_ema"],  # Close below offset EMA
    dataframe["volume"] > 0,                     # Volume exists
]
```

**Logic Interpretation**:
1. **Extreme Oversold Detection**: When Fibonacci extension lower band (4.236 × ATR) crosses above Bollinger lower band (3 standard deviations), indicates price is at extreme oversold
2. **Price Position Confirmation**: Close below offset EMA, ensuring buy timing is at low position
3. **Volume Confirmation**: Must have volume

**Signal Tag**: `buy_signal_2`

### 3.4 Entry Signal #3: Volume-Weighted Breakout

**Indicator Configuration**:
```python
s3_ema_long = 50   # Long period EMA
s3_ema_short = 20  # Short period EMA
s3_ma_fast = 10    # Fast volume-weighted MA
s3_ma_slow = 20    # Slow volume-weighted MA
```

**Trigger Conditions**:
```python
conditions = [
    dataframe["low"] < dataframe["s3_bb_lowerband"],   # Low below Bollinger lower band
    dataframe["high"] > dataframe["s3_slow_ma"],       # High above slow volume-price MA
    dataframe["high"] < dataframe["s3_ema_long"],      # High below long period EMA
    dataframe["volume"] > 0,                           # Volume exists
]
```

**Logic Interpretation**:
1. **Bollinger Band Penetration**: Price touches Bollinger lower band, indicating oversold
2. **Volume-Price Breakout**: High breaks above slow volume-weighted MA, indicating capital involvement
3. **Trend Confirmation**: High still below 50 EMA, avoiding high-position chasing
4. **Volume Confirmation**: Must have volume

**Signal Tag**: `buy_signal_3`

### 3.5 Entry Condition Classification Summary

| Condition Group | Condition ID | Core Logic | Signal Tag |
|-----------------|--------------|------------|------------|
| Trend Following | #1 | EMA crossover + VWMACD + 240 EMA support | buy_signal_1 |
| Extreme Oversold | #2 | Bollinger Band + Fibonacci extension double confirmation | buy_signal_2 |
| Volume-Price Breakout | #3 | Bollinger Band + Volume-weighted MA combination | buy_signal_3 |

---

## 4. Exit Logic Detailed

### 4.1 No Active Exit Signals

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[(), "sell"] = 0
    return dataframe
```

The strategy doesn't use technical indicator-driven exit signals, relying entirely on ROI table and custom stop loss mechanisms to exit.

### 4.2 Tiered ROI Take-Profit

```
Time (minutes)    Minimum Profit Threshold    Signal Name
───────────────────────────────────────────────────────────
0                 10%                         ROI_0
30                5%                          ROI_30
60                2%                          ROI_60
```

**Take-Profit Logic**:
- Immediately after opening requires 10% profit
- After 30 minutes lowers requirement to 5%
- After 60 minutes further lowers to 2%
- After 60 minutes, completely relies on stop loss

### 4.3 Custom Stop Loss Dynamic Adjustment

| Stage | Profit Range | Stop Loss Position | Description |
|-------|--------------|--------------------|-------------| 
| Profit Protection 1 | > 20% | Lock in 4% profit | High return protection |
| Profit Protection 2 | > 10% | Lock in 3% profit | Medium-high return protection |
| Profit Protection 3 | > 6% | Lock in 2% profit | Medium return protection |
| Profit Protection 4 | > 3% | Lock in 1% profit | Light protection |
| Time Stop Loss 1 | < -10%, holding > 60h | Dynamic tightening | Long-term loss handling |
| Time Stop Loss 2 | < -8%, holding > 120h | Dynamic tightening | Very long-term loss handling |

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Usage |
|--------------------|--------------------|-------|
| EMA Series | 3, 5, 10, 20, 50, 200, 240 EMA | Trend judgment, support/resistance |
| Bollinger Bands | 20 period, 3 standard deviations | Oversold detection, volatility range |
| ATR | 14 period | Volatility measurement |
| Volume-Weighted MA | 10, 20 period VWMA | Volume-price relationship analysis |
| VWMACD | 12, 26, 9 parameters | Volume-weighted MACD |
| Fibonacci Extension | 4.236 × ATR | Extreme support level |

### 5.2 Indicator Calculation Details

**EMA Calculation**:
```python
dataframe["s1_ema_xs"] = ta.EMA(dataframe, timeperiod=3)   # Ultra-short
dataframe["s1_ema_sm"] = ta.EMA(dataframe, timeperiod=5)   # Short
dataframe["s1_ema_md"] = ta.EMA(dataframe, timeperiod=10)  # Medium
dataframe["s1_ema_xl"] = ta.EMA(dataframe, timeperiod=50)  # Long
dataframe["s1_ema_xxl"] = ta.EMA(dataframe, timeperiod=240) # Ultra-long
```

**Bollinger Band Calculation**:
```python
s3_bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
dataframe["s3_bb_lowerband"] = s3_bollinger["lower"]
```

**Volume-Weighted MACD Calculation**:
```python
dataframe["fastMA"] = ta.EMA(dataframe["volume"] * dataframe["close"], 12) / ta.EMA(dataframe["volume"], 12)
dataframe["slowMA"] = ta.EMA(dataframe["volume"] * dataframe["close"], 26) / ta.EMA(dataframe["volume"], 26)
dataframe["vwmacd"] = dataframe["fastMA"] - dataframe["slowMA"]
dataframe["signal"] = ta.EMA(dataframe["vwmacd"], 9)
```

**Fibonacci Extension Lower Band**:
```python
s2_fib_atr_value = ta.ATR(dataframe, timeframe=14)
s2_fib_sma_value = ta.SMA(dataframe, timeperiod=50)
dataframe["s2_fib_lower_band"] = s2_fib_sma_value - s2_fib_atr_value * 4.236
```

---

## 6. Risk Management Features

### 6.1 Multi-Layer Protection Mechanism

```python
@property
def protections(self):
    return [
        # Protection 1: Cooldown Period
        {
            "method": "CooldownPeriod",
            "stop_duration": to_minutes(minutes=0),  # 0 minute cooldown
        },
        # Protection 2: Maximum Drawdown Protection
        {
            "method": "MaxDrawdown",
            "lookback_period": to_minutes(hours=12),  # 12 hour lookback
            "trade_limit": 20,                        # Minimum 20 trades
            "stop_duration": to_minutes(hours=1),     # Stop for 1 hour
            "max_allowed_drawdown": 0.2,              # Maximum 20% drawdown
        },
        # Protection 3: Consecutive Stop Loss Protection
        {
            "method": "StoplossGuard",
            "lookback_period": to_minutes(hours=6),   # 6 hour lookback
            "trade_limit": 4,                         # Minimum 4 trades
            "stop_duration": to_minutes(minutes=30),  # Stop for 30 minutes
            "only_per_pair": False,                   # All pairs
        },
        # Protection 4: Low Profit Protection (Short Period)
        {
            "method": "LowProfitPairs",
            "lookback_period": to_minutes(hours=1, minutes=30),  # 1.5 hour lookback
            "trade_limit": 2,                         # Minimum 2 trades
            "stop_duration": to_minutes(hours=15),    # Stop for 15 minutes
            "required_profit": 0.02,                 # 2% minimum profit
        },
        # Protection 5: Low Profit Protection (Long Period)
        {
            "method": "LowProfitPairs",
            "lookback_period": to_minutes(hours=6),   # 6 hour lookback
            "trade_limit": 4,                         # Minimum 4 trades
            "stop_duration": to_minutes(minutes=30),  # Stop for 30 minutes
            "required_profit": 0.01,                  # 1% minimum profit
        },
    ]
```

### 6.2 Protection Mechanism Details

| Protection Type | Trigger Condition | Stop Duration | Description |
|-----------------|-------------------|---------------|-------------|
| Cooldown Period | After each sell | 0 minutes | Can trade again immediately |
| Maximum Drawdown | 20 trades within 12h with >20% drawdown | 1 hour | Overall risk control |
| Stop Loss Protection | ≥4 stop losses within 6h | 30 minutes | Prevent consecutive losses |
| Low Profit Protection (Short) | ≥2 trades with <2% profit within 1.5h | 15 minutes | Short-term return filter |
| Low Profit Protection (Long) | ≥4 trades with <1% profit within 6h | 30 minutes | Long-term return filter |

### 6.3 Custom Stop Loss Smart Protection

The strategy's custom stop loss implements a dynamic mechanism of "the more profit, the stronger the protection":

- **Tiered Protection**: For each profit level reached, stop loss moves up one level
- **Time Stop Loss**: When holding too long with serious loss, gradually tighten stop loss
- **Progressive Exit**: Avoid "either double or zero" extreme situations

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Multi-Signal Fusion**: 3 independent entry signals covering trend following, extreme oversold, and volume-price breakout scenarios
2. **Dynamic Stop Loss**: 5-tier profit protection + time stop loss, smart and flexible
3. **Multi-Layer Protection**: 5 protection groups, controlling risk from multiple dimensions
4. **Volume Weighting**: Uses VWMACD and volume-weighted MA, effectively filtering false signals
5. **Configurable Parameters**: All key parameters are configurable for optimization

### ⚠️ Limitations

1. **No Active Exit**: Relies on ROI and stop loss, may miss optimal exit points
2. **Large Startup Data Requirement**: Needs 480 candles (about 5 days) of warmup data
3. **Many Parameters**: Difficult to optimize, overfitting risk exists
4. **Long Only**: No short logic, not suitable for bear markets

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|--------------------|---------------------------|-------------|
| Moderate Uptrend | Enable all 3 signals | Utilize trend and oversold signals to catch opportunities |
| Oscillating Market | Only enable signal 2 | Focus on extreme oversold rebounds |
| High Volatility | Signals 1+3 | Combine trend and volume-price breakout |
| Downtrend | Use cautiously | May reduce max_open_trades |

---

## 9. Applicable Market Environment Details

Apollo11 is a **defensive offensive strategy**. Through multi-layer protection mechanisms and dynamic stop loss, it strictly controls risk while pursuing returns, most suitable for **moderate trend or oscillating-to-upside** market environments.

### 9.1 Strategy Core Logic

- **Trend Following Primary**: Signal 1 and Signal 3 both rely on EMA trends
- **Oversold Rebound Secondary**: Signal 2 catches extreme oversold opportunities
- **Defense First**: 5-layer protection ensures risk is controllable
- **Profit Protection**: Dynamic stop loss locks in profits

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 Moderate Uptrend | ⭐⭐⭐⭐⭐ | Trend following signals perform best, take-profit mechanism effective |
| 🔄 Oscillating Market | ⭐⭐⭐⭐☆ | Oversold signal catches rebounds, protection mechanisms reduce losses |
| 📉 Downtrend | ⭐⭐☆☆☆ | Frequent stop loss triggers, recommend reducing position |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | May misjudge trends, need parameter adjustment |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|--------------------|-------------------|-------------|
| max_open_trades | 3-5 | Moderate position count |
| stake_amount | 2-5% | Single position control |
| startup_candle_count | 480+ | Ensure sufficient warmup data |

---

## 10. Important Reminder: The Price of Complexity

### 10.1 Learning Cost

This strategy involves multiple technical indicators and complex condition combinations:
- Need to understand EMA trend systems
- Need to understand Bollinger Bands and Fibonacci extensions
- Need to understand volume-weighted indicators
- Need to understand custom stop loss logic

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|----------------|--------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-30 pairs | 4GB | 8GB |
| 30+ pairs | 8GB | 16GB |

### 10.3 Backtesting vs Live Trading Differences

Due to the strategy using volume-weighted indicators and custom stop loss:
- Stop loss logic in backtesting may differ from live trading
- Volume data may differ across exchanges
- Recommend testing in simulation environment first

### 10.4 Advice for Manual Traders

For manual traders, you can learn from the strategy:
- **Dynamic Stop Loss**: The idea of adjusting stop loss position based on profit and time
- **Multi-Signal Confirmation**: Don't rely on single indicator, verify from multiple dimensions
- **Protection Mechanisms**: Build your own risk management framework

---

## 11. Summary

**Apollo11** is a carefully designed multi-signal trend following strategy. Its core value lies in:

1. **Signal Diversity**: 3 independent signals covering different market states
2. **Risk Control**: 5-layer protection mechanism + dynamic stop loss forms complete risk control system
3. **Configurability**: All parameters open for optimization adjustment
4. **Community Verified**: From GitHub open-source project, tested by community

For quantitative traders, this is a strategy framework worth in-depth study and optimization. Recommend understanding each signal logic first, then making parameter adjustments, and finally small-position live verification.