# ClucHAnix_BB_RPB_MOD2_ROI Strategy Analysis

> **Strategy ID**: #98 (465 strategies, 98th)  
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Mean Reversion + Dynamic Stop-Loss + ROI Optimization  
> **Timeframe**: 5 Minutes (5m) + 1-Hour/1-Day Informational Layer

---

## I. Strategy Overview

ClucHAnix_BB_RPB_MOD2_ROI is a complex trend-following strategy based on Heikin Ashi (HA) candlesticks and Bollinger Band mean reversion principles. This strategy is the 5-minute timeframe optimized version of ClucHAnix_BB_RPB_MOD, incorporating a more refined ROI (Return On Investment) profit-taking mechanism. The name "MOD2" indicates the second modification version, and "ROI" indicates it is optimized for the 5-minute timeframe with an improved profit-taking table.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 8 independent entry signals (7 independently enable/disable), all require base protection filtering |
| **Exit Conditions** | 1 base exit signal + multi-layer dynamic profit-taking/stop-loss system (BB_RPB_TSL style) |
| **Protection Mechanisms** | 2 sets of entry protection parameters (BTC trend protection + Pump intensity protection) |
| **Timeframe** | Primary 5m + Informational 1h and 1d |
| **Dependencies** | technical, pandas_ta, talib, numpy, pandas, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table (optimized for 5m framework)
minimal_roi = {
    "0": 0.05,       # Immediate exit at 5% profit
    "15": 0.04,      # Profit drops to 4% after 15 minutes (~3 candles)
    "51": 0.03,      # Profit drops to 3% after 51 minutes (~10 candles)
    "81": 0.02,      # Profit drops to 2% after 81 minutes (~16 candles)
    "112": 0.01,     # Profit drops to 1% after 112 minutes (~22 candles)
    "154": 0.0001,   # Profit drops to 0.01% after 154 minutes
    "240": -10       # After 240 minutes, close ROI limit, let profits run
}

# Stop Loss
stoploss = -0.99   # Base stop-loss line -99% (actually uses custom_stoploss)

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.001      # Activates trailing after 0.1% profit
trailing_stop_positive_offset = 0.012  # Trailing stop distance 1.2%
trailing_only_offset_is_reached = False
```

**Design Philosophy**:
- **ROI Table Design**: Fine-grained gradient design — immediately locks in 5% profit target upon opening. Gradually reduces: to 4% after 15 minutes (3 candles), 3% after 51 minutes (10 candles), etc. This design leaves more room for trend continuation in the 5-minute framework while implementing "let profits run" by closing ROI limits after 240 minutes (~48 candles).
- **Stop Loss Design**: Base stop loss at -99% (almost never triggers), through custom_stoploss implementing two-tier dynamic profit-taking/stop-loss mechanism.

### 2.2 Order Type Configuration

```python
order_types = {
    'entry': 'market',
    'exit': 'market',
    'emergency_exit': 'market',
    'force_entry': "market",
    'force_exit': 'market',
    'stoploss': 'market',
    'stoploss_on_exchange': False,
    'stoploss_on_exchange_interval': 60,
    'stoploss_on_exchange_limit_ratio': 0.99
}
```

### 2.3 Custom Stop-Loss Parameters (BB_RPB_TSL Mechanism)

```python
# Hard stop-loss line
pHSL = DecimalParameter(-0.500, -0.040, default=-0.32)

# Profit threshold range 1
pPF_1 = DecimalParameter(0.008, 0.020, default=0.020)  # Trigger point 2%
pSL_1 = DecimalParameter(0.008, 0.020, default=0.020)  # Corresponding stop-loss line 2%

# Profit threshold range 2
pPF_2 = DecimalParameter(0.040, 0.100, default=0.047)  # Trigger point 4.7%
pSL_2 = DecimalParameter(0.020, 0.070, default=0.046)  # Corresponding stop-loss line 4.6%
```

**Design Philosophy**:
- When profit > 2%, first-tier protection activates, stop line moves to 2%
- When profit > 4.7%, second-tier protection activates, stop line moves to 4.6%
- When profit > 4.7%, stop line moves linearly upward with profit growth, implementing "let profits run"

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms (2 Sets)

| Protection Type | Parameter Description | Default Value |
|----------------|---------------------|---------------|
| BTC trend protection | BTC 1-day vs 1-minute price change rate | > -0.311 |
| Pump intensity protection | Pump intensity must be below threshold | < 0.133 |

**Implementation Logic**:
- **BTC Protection**: Compares BTC/USDT 1-day and 1-minute price change rates to determine overall market trend. Only when BTC is in uptrend or stable are long positions allowed.
- **Pump Protection**: Calculates Pump intensity through ZEMA; reduces buy priority when market rapidly rises to avoid chasing.

### 3.2 Entry Condition Details

8 independent entry conditions, 7 can be independently enabled/disabled.

#### Condition #1: Lambo1
```python
# Logic
- lambo1_enabled = False (disabled by default)
- close < ema_14 * 1.054 (price below EMA14's 105.4%)
- rsi_4 < 18 (4-period RSI extremely oversold)
- rsi_14 < 26 (14-period RSI relatively low)
```

#### Condition #2: Lambo2
```python
# Logic
- lambo2_enabled = True (enabled by default)
- close < ema_14 * 0.981 (price below EMA14's 98.1%)
- rsi_4 < 44 (4-period RSI oversold)
- rsi_14 < 39 (14-period RSI relatively low)
```

#### Condition #3: Local Uptrend
```python
# Logic
- local_trend_enabled = True (enabled by default)
- ema_26 > ema_14 (short-term MA above mid-term MA, forming uptrend)
- ema_26 - ema_14 > open * 0.125 (MA divergence threshold)
- ema_26.shift() - ema_14.shift() > open / 100 (previous candle also satisfies MA bullish)
- close < bb_lowerband2 * 0.823 (price touches or near lower band)
- closedelta > close * 19.253 / 1000 (close price change significant)
```

#### Condition #4: NFI32
```python
# Logic
- nfi32_enabled = True (enabled by default)
- rsi_20 < rsi_20.shift(1) (RSI in downtrend)
- rsi_4 < 49 (4-period RSI oversold)
- rsi_14 > 15 (14-period RSI relatively high)
- close < sma_15 * 0.93391 (price below SMA15's 93.4%)
- cti < -1.09639 (CTI below threshold, indicating weak trend)
```

#### Condition #5: EWO1 (Elliott Wave Oscillator High)
```python
# Logic
- ewo_1_enabled = False (disabled by default)
- rsi_4 < 7 (4-period RSI extremely oversold)
- close < ema(buy) * 1.04116 (price below buy EMA)
- EWO > 5.249 (EWO at high level, strong uptrend)
- rsi_14 < 45 (14-period RSI relatively low)
- close < ema(sell) * 1.04116 (price below sell EMA)
```

#### Condition #6: EWO Low
```python
# Logic
- ewo_low_enabled = True (enabled by default)
- rsi_4 < 35 (4-period RSI oversold)
- close < ema(buy) * 0.97463 (price below buy EMA)
- EWO < -11.424 (EWO at low level, rebound opportunity in downtrend)
- close < ema(sell) * 1.04116 (price below sell EMA)
```

#### Condition #7: Cofi
```python
# Logic
- cofi_enabled = False (disabled by default)
- open < ema_8 * 0.639 (open below EMA8's 63.9%)
- fastk crosses above fastd (stochastic golden cross)
- fastk < 13 (fast line at low level)
- fastd < 40 (slow line at relatively low level)
- adx > 8 (ADX shows clear trend)
- EWO > 5.6 (EWO at high level)
```

#### Condition #8: ClucHA
```python
# Logic
- clucha_enabled = False (disabled by default)
- rocr_1h > 0.41663 (1-hour ROC shows uptrend)
- Condition Group A:
  * bbdelta > ha_close * 0.04796 (Bollinger Band width meets standard)
  * ha_closedelta > ha_close * 0.00931 (HA close change significant)
  * tail < bbdelta * 0.93112 (lower wick relatively short)
  * ha_close < lower.shift() (HA close breaks below lower band)
  * ha_close <= ha_close.shift() (HA close in downtrend)
- OR Condition Group B:
  * ha_close < ema_slow (price below long-term MA)
  * ha_close < bb_lowerband * 0.01645 (price touches lower band)
```

### 3.3 Entry Condition Classification

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

Strategy uses segmented dynamic profit-taking/stop-loss:

```
Profit Range              Stop-Loss Strategy
──────────────────────────────────────────────────────
Profit < 2%               Uses hard stop pHSL = -32%
2% ≤ Profit < 4.7%       Linear interpolation: from -2% to -4.6%
Profit ≥ 4.7%             Stop line moves up: let profits run
```

**Dynamic Stop-Loss Calculation Formula**:
```python
if current_profit > PF_2:  # profit > 4.7%
    sl_profit = SL_2 + (current_profit - PF_2)
elif current_profit > PF_1:  # 2% ≤ profit < 4.7%
    sl_profit = SL_1 + ((current_profit - PF_1) * (SL_2 - SL_1) / (PF_2 - PF_1))
else:  # profit < 2%
    sl_profit = HSL
```

### 4.2 Base Exit Signal (1 Total)

```python
# Exit signal: Fisher indicator reversal + HA trend reversal + Bollinger middle band resistance
- fisher > 0.38414 (Fisher indicator above threshold)
- ha_high ≤ ha_high.shift(1) (HA highest price in downtrend)
- ha_high.shift(1) ≤ ha_high.shift(2) (Highest price declining for 2 consecutive candles)
- ha_close ≤ ha_close.shift(1) (HA close in downtrend)
- ema_fast > ha_close (fast MA above price, trend weakening)
- ha_close * 1.07634 > bb_middleband (price touches Bollinger middle band)
- volume > 0 (volume support)
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

### 5.2 Informational Timeframe Indicators (1h + 1d)

- **1-hour informational layer**:
  - Heikin Ashi close
  - ROCR 168-period — reflects long-term momentum (7 days)

- **1-day informational layer**:
  - BTC/USDT close — for BTC trend protection

- **BTC protection indicator**:
  - BTC 1-day vs 1-minute price change rate

### 5.3 Custom Indicators

| Indicator | Formula | Purpose |
|---------|---------|---------|
| Pump intensity | (ZEMA_30 - ZEMA_200) / ZEMA_30 | Identify market Pump intensity |
| HA Candlestick | qtpylib.heikinashi() | Smooth price, clearer trend identification |

---

## VI. Risk Management Highlights

### 6.1 Multi-Layer Dynamic Profit-Taking/Stop-Loss

BB_RPB_TSL mechanism is the core risk management feature:

| Profit Range | Stop-Loss Strategy | Protection Goal |
|-------------|-------------------|----------------|
| Profit < 2% | Hard stop -32% | Limit maximum loss (loose) |
| 2% ≤ Profit < 4.7% | Dynamic move 2%→4.6% | Protect realized profits |
| Profit ≥ 4.7% | Trailing stop | Let profits run |

### 6.2 Entry Conditions Independently Enable/Disable

Same as ClucHAnix_BB_RPB_MOD: 7 boolean parameters for flexible market adaptation.

### 6.3 Market Environment Protection

- **BTC trend protection**: Reduces buy signals when BTC is falling
- **Pump intensity protection**: Reduces buy priority when market rapidly rises

---

## VII. Strategy Pros & Cons

### Pros

1. **Multi-condition parallel**: 8 independent entry conditions cover various market patterns
2. **Dynamic profit-taking/stop-loss**: BB_RPB_TSL protects profits while letting them run
3. **Self-adapting market**: BTC and Pump protection adapt to different environments
4. **Conditions configurable**: Each entry independently enable/disable
5. **ROI optimization**: Profit-taking table optimized for 5-minute framework, more suitable for medium-term trend following

### Cons

1. **Many parameters**: 40+ parameters, high optimization difficulty
2. **5-minute timeframe**: Some hardware and network requirements, but lower than 1m
3. **Overfitting risk**: Multi-condition strategies easily overfit on historical data
4. **High computation**: Multi-indicator calculation may cause delays

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|--------------------|-------------------------|-------------|
| Volatile markets | Enable lambo2, local_uptrend, nfi32, ewo_low | Capture oversold rebounds and trend continuation |
| Trending markets | Enable clucHA + extend ROI time | Let profits run |
| Ranging markets | Close all conditions, retain base protection only | Reduce frequent trading |
| BTC rising | Enable BTC protection | Follow the trend |

---

## IX. Applicable Market Environment Details

ClucHAnix_BB_RPB_MOD2_ROI is the 5-minute timeframe + ROI optimized version of the Cluc series. It performs best in **moderately volatile trending markets with medium-term trends**, and should be used cautiously in extreme markets.

### 9.1 Core Strategy Logic

- **Multi-condition trend following**: 8 independent entry conditions capture various entry patterns
- **Bollinger Band mean reversion**: Find rebound opportunities when price touches lower band
- **Dynamic profit-taking/stop-loss**: BB_RPB_TSL auto-adjusts protection based on profit level
- **Market environment filtering**: BTC and Pump protection avoid unfavorable environments
- **ROI optimization**: Gradient profit-taking table designed for 5-minute framework

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Trending up | Excellent | Multi-conditions capture trend starts, ROI table leaves room for trends |
| Ranging consolidation | Good | RSI oversold conditions capture range boundaries |
| Trending down | Poor | BTC protection filters some, but 5m hard to resist big trends |
| Extreme volatility | Poor | Pump protection helps some, but many parameters require caution |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|---------------|------------------|-------------|
| max_open_trades | 3-5 | Adjust based on capital |
| ROI table | Default | Already optimized for 5m framework |
| Custom stop-loss | Default | Already optimized for moderate volatility |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

Many parameters require deep understanding of each indicator's meaning. Start with defaults and adjust gradually.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 5-10 pairs | 2 GB | 4 GB |
| 20-30 pairs | 4 GB | 8 GB |
| 50+ pairs | 8 GB | 16 GB |

**Note**: 5-minute framework + multi-indicator calculation requires CPU, but lower than 1m. Ensure VPS performance is sufficient.

### 10.3 Backtesting vs. Live Trading Differences

- 5-minute framework backtest vs. live differences relatively smaller than 1m
- Multi-condition combinations may cause signal delays
- Recommend small-capital live testing to verify

### 10.4 Manual Trader Recommendations

This strategy is unsuitable for manual trading. 8 entry conditions + multi-layer dynamic profit-taking/stop-loss make manual execution nearly impossible.

---

## XI. Summary

**ClucHAnix_BB_RPB_MOD2_ROI** is a highly complex trend-following strategy combining multi-condition entry, dynamic profit-taking/stop-loss, and market environment filtering. Its core value lies in:

1. **Multi-condition coverage**: 8 independent entry conditions cover oversold rebounds, trend continuation, mean reversion, and more
2. **Intelligent profit-taking/stop-loss**: BB_RPB_TSL auto-adjusts protection based on profit level
3. **ROI optimization**: Gradient profit-taking table for 5-minute framework, more suitable for medium-term trends
4. **Self-adapting**: BTC and Pump protection help avoid unfavorable environments

For quantitative traders, this strategy suits experienced traders who understand each parameter's meaning and conduct thorough backtesting and paper trading. **Not recommended for newcomers**.
