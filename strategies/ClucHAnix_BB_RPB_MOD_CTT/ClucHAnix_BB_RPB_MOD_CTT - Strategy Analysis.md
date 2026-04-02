# ClucHAnix_BB_RPB_MOD_CTT Strategy Analysis

> **Strategy ID**: #99 (465 strategies, 99th)  
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Mean Reversion + Custom Dynamic Stop-Loss + CTT Time Window Trading  
> **Timeframe**: 1 Minute (1m) + 1-Hour/1-Day Informational Layer

---

## I. Strategy Overview

ClucHAnix_BB_RPB_MOD_CTT is an advanced trend-following strategy based on Heikin Ashi (HA) candlesticks and Bollinger Band mean reversion principles. This strategy is an enhanced version of ClucHAnix_BB_RPB_MOD, introducing CTT (Custom Time Window Trading) — enabling or disabling trading signals during specific time windows to filter unfavorable trading periods. The name "CTT" represents the Custom Time Window Trading mechanism.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 8 independent entry signals (7 independently enable/disable), all require base protection filtering |
| **Exit Conditions** | 1 base exit signal + multi-layer dynamic profit-taking/stop-loss system (BB_RPB_TSL style) |
| **Protection Mechanisms** | 2 sets of entry protection parameters (BTC trend + Pump) + CTT time window filtering |
| **Timeframe** | Primary 1m + Informational 1h and 1d |
| **Dependencies** | technical, pandas_ta, talib, numpy, pandas, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,      # Immediate exit at 10% profit
    "60": 0.07,     # Profit drops to 7% after 1 minute
    "120": 0.05,    # Profit drops to 5% after 2 minutes
    "240": 0.03,    # Profit drops to 3% after 4 minutes
}

# Stop Loss
stoploss = -0.10   # Base stop-loss line -10%

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.001    # Activates trailing after 0.1% profit
trailing_stop_positive_offset = 0.012  # Trailing distance 1.2%
trailing_only_offset_is_reached = False
```

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'market',
    'sell': 'market',
    'emergencysell': 'market',
    'forcebuy': "market",
    'forcesell': 'market',
    'stoploss': 'market',
    'stoploss_on_exchange': False,
    'stoploss_on_exchange_interval': 60,
    'stoploss_on_exchange_limit_ratio': 0.99
}
```

### 2.3 CTT Custom Time Window Configuration

```python
# CTT Time Window Parameters
enable_ctt = BooleanParameter(default=True)      # Enable CTT mechanism
ctt_start_hour = IntParameter(0, 23, default=9)  # Daily trading start hour
ctt_end_hour = IntParameter(0, 23, default=23)   # Daily trading end hour
ctt_days = CategoricalParameter(['all', 'weekdays', 'weekends'], default='all')  # Trading date setting

# Special period exclusions
exclude_market_open = BooleanParameter(default=True)  # Exclude opening period
exclude_market_close = BooleanParameter(default=False) # Exclude closing period
```

**Design Philosophy**:
- CTT mechanism allows traders to trade only during specific time windows, filtering low-liquidity or abnormally volatile periods
- Configurable to only trade during active periods (e.g., 9:00-23:00)
- Can exclude special periods like market open/close to avoid getting caught

### 2.4 Custom Stop-Loss Parameters (BB_RPB_TSL Mechanism)

```python
# Hard stop-loss line
pHSL = DecimalParameter(-0.500, -0.040, default=-0.08)

# Profit threshold range 1
pPF_1 = DecimalParameter(0.008, 0.020, default=0.016)  # Trigger point
pSL_1 = DecimalParameter(0.008, 0.020, default=0.011)  # Corresponding stop-loss

# Profit threshold range 2
pPF_2 = DecimalParameter(0.040, 0.100, default=0.080)  # Trigger point
pSL_2 = DecimalParameter(0.020, 0.070, default=0.040)  # Corresponding stop-loss
```

---

## III. Entry Conditions Details

### 3.1 CTT Time Window Filtering Mechanism

CTT performs time window filtering before entry condition execution. Entry signals only generate within allowed time windows:

| Parameter | Default | Description |
|-----------|---------|-------------|
| enable_ctt | True | Enable CTT mechanism |
| ctt_start_hour | 9 | Daily trading start hour (UTC) |
| ctt_end_hour | 23 | Daily trading end hour (UTC) |
| ctt_days | all | Trading dates: all/weekdays/weekends |

### 3.2 Base Protection Mechanisms (2 Sets)

| Protection Type | Parameter Description | Default Value |
|----------------|---------------------|---------------|
| BTC trend protection | BTC 1-day vs 1-minute price change rate | > -0.311 |
| Pump intensity protection | Pump intensity must be below threshold | < 0.133 |

### 3.3 Entry Condition Details

8 independent entry conditions, 7 can be independently enabled/disabled. Identical to ClucHAnix_BB_RPB_MOD.

| Condition Group | Condition | Core Logic | Status |
|----------------|-----------|-----------|--------|
| RSI Oversold | lambo1, lambo2 | Multi-period RSI identifies oversold rebounds | lambo1 disabled, lambo2 enabled |
| Trend Confirmation | local_uptrend | MA bullish + lower band support | Enabled |
| Comprehensive | nfi_32 | RSI divergence + CTI weak trend | Enabled |
| Volatility Breakout | ewo_1, ewo_low | EWO extreme + RSI oversold | ewo_1 disabled, ewo_low enabled |
| Stochastic | cofi | Stochastic golden cross + trend confirmation | Disabled |
| Bollinger Regression | clucHA | HA candles + Bollinger Band mean reversion | Disabled |

---

## IV. Exit Logic Details

### 4.1 Multi-Layer Profit-Taking System (BB_RPB_TSL Mechanism)

Identical to ClucHAnix_BB_RPB_MOD:

```
Profit Range              Stop-Loss Strategy
──────────────────────────────────────────────────────
Profit < 1.6%           Uses hard stop pHSL = -8%
1.6% ≤ Profit < 8%     Linear interpolation: from -1.1% to -4%
Profit ≥ 8%             Stop line moves up: let profits run
```

### 4.2 Base Exit Signal (1 Total)

```python
# Exit signal: Fisher indicator reversal
- fisher > 0.38414
- ha_high ≤ ha_high.shift(1)
- ha_high.shift(1) ≤ ha_high.shift(2)
- ha_close ≤ ha_close.shift(1)
- ema_fast > ha_close
- ha_close * 1.07634 > bb_middleband
- volume > 0
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-----------------|-------------------|---------|
| Trend Indicators | EMA 8/14/26, SMA 15 | Determine price trend direction |
| Momentum Indicators | RSI 4/14/20, ROCR, Fisher | Identify overbought/oversold and momentum |
| Volatility Indicators | Bollinger Bands (20, 40 period), CTI | Determine volatility and support/resistance |
| Wave Indicators | EWO (Elliott Wave Oscillator) | Identify trend strength and turning points |
| Stochastic Indicators | Stoch FastK/FastD | Determine short-term overbought/oversold |

### 5.2 Custom Indicators

| Indicator | Formula | Purpose |
|---------|---------|---------|
| Pump intensity | (ZEMA_30 - ZEMA_200) / ZEMA_30 | Identify market Pump intensity |
| HA Candlestick | qtpylib.heikinashi() | Smooth price, clearer trend identification |
| CTT Time Window | Time filtering logic | Filter unfavorable trading periods |

---

## VI. Risk Management Highlights

### 6.1 CTT Time Window Filtering

CTT is a core distinctive feature, filtering unfavorable trading periods via time windows:

| Time Period | Trading Status | Description |
|------------|--------------|-------------|
| Within allowed window | Normal trading | Decide whether to buy based on other conditions |
| Outside allowed window | Trading prohibited | No trading even if buy conditions met |
| Exclude open/close | Special period filtering | Avoid liquidity risk |

### 6.2 Multi-Layer Dynamic Profit-Taking/Stop-Loss

| Profit Range | Stop-Loss Strategy | Protection Goal |
|-------------|-------------------|----------------|
| Profit < 1.6% | Hard stop -8% | Limit maximum loss |
| 1.6% ≤ Profit < 8% | Dynamic move 1.1%→4% | Protect realized profits |
| Profit ≥ 8% | Trailing stop | Let profits run |

### 6.3 Entry Conditions Independently Enable/Disable

Same 7 boolean parameters as ClucHAnix_BB_RPB_MOD.

### 6.4 Market Environment Protection

- **BTC trend protection**: Reduces buy signals when BTC falls
- **Pump intensity protection**: Reduces buy priority when market rallies rapidly

---

## VII. Strategy Pros & Cons

### Pros

1. **Multi-condition parallel**: 8 independent entry conditions cover various market patterns
2. **Dynamic profit-taking/stop-loss**: BB_RPB_TSL protects profits while letting them run
3. **CTT time filtering**: Filters unfavorable trading periods via time windows
4. **Self-adapting market**: BTC protection, Pump protection, and CTT adapt to different environments
5. **Conditions configurable**: Each entry independently enable/disable

### Cons

1. **Many parameters**: 50+ parameters, high optimization difficulty
2. **1-minute timeframe**: High-frequency trading demands high hardware and network
3. **Overfitting risk**: Multi-condition strategies easily overfit on historical data
4. **High computation**: Multi-indicator calculation may cause delays
5. **CTT time restrictions**: May miss some opportunities during disallowed periods

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|--------------------|-------------------------|-------------|
| Volatile markets | Enable lambo2, local_uptrend, nfi32, ewo_low | Capture oversold rebounds and trend continuation |
| Trending markets | Enable clucHA + extend ROI time | Let profits run |
| Ranging markets | Close all conditions, retain base protection only | Reduce frequent trading |
| BTC rising | Enable BTC protection | Follow the trend |
| Low-liquidity periods | Enable CTT, limit trading periods | Avoid getting caught |

---

## IX. Applicable Market Environment Details

ClucHAnix_BB_RPB_MOD_CTT is the Bollinger Band mean reversion + dynamic profit-taking/stop-loss + CTT time window version of the Cluc series. It performs best in **moderately volatile trending markets**, and should be used cautiously in extreme markets or inactive periods.

### 9.1 Core Strategy Logic

- **Multi-condition trend following**: 8 independent entry conditions capture various patterns
- **Bollinger Band mean reversion**: Find rebound opportunities when price touches lower band
- **Dynamic profit-taking/stop-loss**: BB_RPB_TSL auto-adjusts protection based on profit
- **CTT time window**: Filters unfavorable trading periods via time
- **Market environment filtering**: BTC and Pump protection avoid unfavorable environments

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Trending up | Excellent | Multi-conditions catch trend starts, dynamic profit-taking lets profits run |
| Ranging consolidation | Good | RSI oversold conditions capture range boundaries |
| Trending down | Poor | BTC protection filters some, but 1m hard to resist big trends |
| Extreme volatility | Poor | Pump protection + CTT help somewhat, but many parameters require caution |
| Low-liquidity periods | Excellent | CTT time filtering perfectly avoids these periods |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|---------------|------------------|-------------|
| max_open_trades | 3-5 | Adjust based on capital |
| ROI table | Default | Already optimized for 1m framework |
| CTT configuration | 9-23 UTC | Adjust based on target market |
| Custom stop-loss | Default | Already optimized for moderate volatility |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

50+ parameters require deep understanding of each indicator. Start with defaults and adjust gradually.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 5-10 pairs | 2 GB | 4 GB |
| 20-30 pairs | 4 GB | 8 GB |
| 50+ pairs | 8 GB | 16 GB |

**Note**: 1-minute framework + multi-indicator calculation + CTT time checks demand CPU. Ensure VPS performance is sufficient.

### 10.3 Backtesting vs. Live Trading Differences

- 1-minute framework backtest vs. live differences may be significant
- Multi-condition combinations may cause signal delays
- CTT time windows may cause backtest vs. live signal count differences
- Recommend small-capital live testing to verify

### 10.4 Manual Trader Recommendations

This strategy is unsuitable for manual trading. 8 entry conditions + CTT time checks + multi-layer dynamic profit-taking/stop-loss make manual execution nearly impossible.

---

## XI. Summary

**ClucHAnix_BB_RPB_MOD_CTT** is a highly complex trend-following strategy combining multi-condition entry, dynamic profit-taking/stop-loss, market environment filtering, and CTT time window trading. Its core value lies in:

1. **Multi-condition coverage**: 8 independent entry conditions cover oversold rebounds, trend continuation, mean reversion, and more
2. **Intelligent profit-taking/stop-loss**: BB_RPB_TSL auto-adjusts protection based on profit level
3. **CTT time filtering**: Filters unfavorable trading periods via time windows
4. **Self-adapting**: BTC protection, Pump protection, and CTT help avoid unfavorable environments

For quantitative traders, this strategy suits experienced traders who understand each parameter's meaning and conduct thorough backtesting and paper trading before live trading. **Not recommended for newcomers**.
