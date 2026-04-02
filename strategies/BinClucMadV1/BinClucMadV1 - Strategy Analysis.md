# BinClucMadV1 Strategy Analysis

> **Strategy ID**: #73 (Batch 08, #73)  
> **Strategy Type**: Multi-Condition Trend Reversal + Bollinger Band Range Trading  
> **Timeframe**: 5 minutes (primary) + 1 hour (informational)

---

## I. Strategy Overview

BinClucMadV1 is a highly complex quantitative trading strategy that synthesizes buy logic from multiple classic trading strategies (BinCluc, CombinedBinHCluc, MAD variants, and more). The strategy employs multi-timeframe analysis (5-minute primary cycle + 1-hour informational cycle) combined with multi-condition stacking to capture reversal opportunities in ranging markets.

Compared to BinClucMad (original version), BinClucMadV1 makes the following optimizations:
- Introduced stricter RSI protection mechanism
- Added SSL Channel trend confirmation
- Optimized parameter thresholds for certain buy conditions
- Improved custom stop-loss logic

### Core Characteristics

| Attribute | Description |
|-----------|-------------|
| **Buy Conditions** | 16 independent buy signals (4 V6 + 4 V8 + 8 V9), independently enableable/disableable |
| **Sell Conditions** | 3 basic sell signals + multi-layer dynamic take-profit logic |
| **Protection Mechanisms** | 5 core protection parameter groups (RSI, volume, Bollinger Band position, EMA position, SSL Channel) |
| **Timeframe** | 5 minutes (primary) + 1 hour (informational) |
| **Stop-Loss Method** | Custom conditional stop-loss (stoploss=-0.10, actual use via custom_stoploss) |
| **Trailing Stop** | Enabled (1% positive, 3% offset) |
| **Suitable Market** | Ranging markets, range-bound price action |

### Minimal ROI Configuration

| Holding Time | Minimal Return |
|--------------|---------------|
| 0–15 minutes | 8.0% |
| 15–45 minutes | 4.5% |
| 45–180 minutes | 2.0% |
| 180+ minutes | 0% |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {"0": 0.08, "15": 0.045, "45": 0.02, "180": 0}

# Stop-Loss Settings
stoploss = -0.10

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01           # 1% positive trail
trailing_stop_positive_offset = 0.03    # 3% offset activates it
```

**Design Philosophy**:
- The moderate initial ROI (8%) balances the need for quick take-profits with allowing larger gains
- The stepped ROI structure ensures reasonable profits are locked in across different holding durations
- The 10% stop-loss paired with custom stop-loss logic provides sufficient room while controlling risk
- The 3% trailing stop offset is relatively conservative, placing greater emphasis on risk control

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "market",       # Market entry
    "exit": "market",        # Market exit
    "stoploss": "market",  # Market stop-loss
    "stoploss_on_exchange": False,
}

use_exit_signal = True
exit_profit_only = True           # Sell only when profitable
exit_profit_offset = 0.001        # Minimum profit threshold 0.1%
ignore_roi_if_entry_signal = False  # Keep ROI exit mechanism
```

### 2.3 Minimum Buy Condition Count

```python
buy_minimum_conditions = IntParameter(1, 2, default=1, space='buy', optimize=False, load=True)
```

---

## III. Entry Conditions Details

The strategy contains 16 independent buy conditions. Meeting the specified count (default: 1) triggers a buy signal. Using "OR" logic, entry is triggered as long as the minimum number of conditions is met.

### 3.1 Protection Mechanisms (5 Core Parameter Groups)

Each buy condition is equipped with an independent protection parameter set:

| Protection Type | Parameter Name | Default Value | Purpose |
|----------------|---------------|---------------|---------|
| **RSI Oversold** | buy_rsi | 38.5 | Short-term oversold detection |
| **1-Hour RSI** | buy_rsi_1h | 67.0 | Mid-to-long-term oversold detection |
| **Volume Protection** | buy_volume_ratio | 4.0 | Volume contraction filter |
| **Bollinger Band Position** | buy_bb_offset | 0.985 | Near Bollinger Band lower band |
| **EMA Position** | buy_ema_diff | 0.0 | EMA trend confirmation |

### 3.2 V6 Series Buy Conditions (4 conditions)

The V6 series represents the classic Cluc mode variants, characterized by seeking entry near the Bollinger Band lower band while price is above EMA200.

#### Condition 0: Cluc Classic Mode
```python
(dataframe['close'] > dataframe['ema200']) & 
(dataframe['close'] > dataframe['ema200_1h']) & 
(dataframe['close'] < dataframe['ema50']) &
(dataframe['close'] < dataframe['bb_lowerband'] * 0.99) &
(volume_cond)
```
**Core Logic**: Price above long-term moving averages, buy on pullback to Bollinger Band lower band.

#### Condition 1: Cluc Variant (Enhanced RSI Protection)
```python
(dataframe['close'] < dataframe['ema50']) &
(dataframe['close'] < dataframe['bb_lowerband'] * 0.975) &
(dataframe['rsi_1h'] < 15) &
(volume_cond)
```
**Core Logic**: Stricter RSI protection to avoid buying during sharp declines.

#### Condition 2: MACD Golden Cross Confirmation
```python
(dataframe['close'] > dataframe['ema200']) &
(dataframe['close'] > dataframe['ema200_1h']) &
(dataframe['ema26'] > dataframe['ema12']) &
(dataframe['macdh'] > dataframe['open'] * 0.02) &
(dataframe['close'] < dataframe['bb_lowerband'])
```
**Core Logic**: Bollinger Band lower band buy with MACD bullish alignment.

#### Condition 3: Pure MACD Signal
```python
(dataframe['ema26'] > dataframe['ema12']) &
(dataframe['macdh'] > dataframe['open'] * 0.03) &
(dataframe['close'] < dataframe['bb_lowerband'])
```
**Core Logic**: Simplified MACD buy signal.

### 3.3 V8 Series Buy Conditions (4 conditions)

The V8 series introduces more technical indicator combinations and trend confirmation.

#### Condition 0: RSI Oversold + SSL Confirmation
```python
(dataframe['rsi'] < 35) &
(dataframe['ssl_up_1h'] > dataframe['ssl_down_1h']) &
(dataframe['ema50_1h'] > dataframe['ema200_1h'])
```
**Core Logic**: RSI oversold with 1-hour cycle trend confirmation.

#### Condition 1: Dual RSI Oversold
```python
(dataframe['rsi_1h'] < 20) &
(dataframe['rsi'] < 28) &
(volume_cond)
```
**Core Logic**: Dual RSI oversold confirmation.

#### Condition 2: RSI Variant
```python
(dataframe['rsi_1h'] < 35) &
(dataframe['rsi'] < 10)
```
**Core Logic**: Different threshold RSI combination.

#### Condition 3: SSL Channel Trend
```python
(dataframe['close'] < dataframe['sma_5']) &
(dataframe['ssl_up_1h'] > dataframe['ssl_down_1h']) &
(dataframe['ema50_1h'] > dataframe['ema200_1h']) &
(dataframe['rsi'] < dataframe['rsi_1h'] - 43.276)
```
**Core Logic**: SSL Channel confirms trend, paired with RSI divergence.

### 3.4 V9 Series Buy Conditions (8 conditions)

The V9 series represents more complex condition combinations with additional filtering mechanisms.

#### Condition 0: Basic Bollinger Rebound
```python
(close_above_ema) & (close_above_ema_1h) &
(close < bb_lower * 0.99) &
(volume_slow > volume_slow_shift * 0.4) &
(volume < prev_volume * 4) &
(body_check)
```
**Core Logic**: Comprehensive rebound signal near Bollinger Band lower band.

#### Condition 1: Simplified Bollinger Rebound
```python
(close_above_ema) &
(close < bb_lower * 0.982) &
(volume_cond)
```
**Core Logic**: Simplified Bollinger Band rebound condition.

#### Condition 2: RSI Oversold Rebound
```python
(close_above_ema_1h) &
(close < bb_lower) &
(dataframe['rsi'] < 14.2) &
(volume_cond)
```
**Core Logic**: Buy at RSI extreme oversold values.

#### Condition 3: 1-Hour RSI Oversold
```python
(dataframe['rsi_1h'] < 16.5) &
(close < bb_lower) &
(volume_cond)
```
**Core Logic**: 1-hour RSI oversold judgment.

#### Condition 4: MACD Golden Cross + Bollinger Rebound
```python
(close_above_ema) & (close_above_ema_1h) &
(macd_golden_cross) &
(close < bb_lower) &
(volume_cond)
```
**Core Logic**: MACD golden cross paired with Bollinger Band lower band.

#### Condition 5: Simplified MACD Rebound
```python
(dataframe['ema26'] > dataframe['ema12']) &
(dataframe['macdh'] > dataframe['open'] * 0.03) &
(close < bb_lower)
```
**Core Logic**: Simplified MACD signal.

#### Condition 6: 1-Hour RSI + MACD
```python
(dataframe['rsi_1h'] < 15) &
(dataframe['ema26'] > dataframe['ema12']) &
(dataframe['macdh'] > dataframe['open'] * 0.02)
```
**Core Logic**: 1-hour RSI paired with MACD combination.

#### Condition 7: SSL Trend Confirmation
```python
(close < sma_5) &
(ssl_up_1h > ssl_down_1h) &
(ema_50_1h > ema_200_1h) &
(rsi_diff)
```
**Core Logic**: SSL Channel trend confirmation entry.

---

## IV. Exit Logic Details

### 4.1 Sell Conditions List

| Condition | Trigger Condition | Default State |
|-----------|------------------|--------------|
| v9_sell_0 | Close breaks Bollinger middle band ×1.01 | Disabled |
| v8_sell_0 | 3 consecutive candles break Bollinger upper band | Enabled |
| v8_sell_1 | RSI > 80 | Enabled |

### 4.2 Detailed Explanations

#### v9_sell_condition_0
```python
dataframe["close"] > dataframe["bb_middleband"] * 1.01
```
Sell when close breaks above Bollinger Band middle band (1.01×). Characterized by quick profit-taking.

#### v8_sell_condition_0
```python
(dataframe["close"] > dataframe["bb_upperband"]) &
(dataframe["close"].shift(1) > dataframe["bb_upperband"].shift(1)) &
(dataframe["close"].shift(2) > dataframe["bb_upperband"].shift(2))
```
Three consecutive candles' close prices are all above Bollinger Band upper band — a typical high-point reversal signal.

#### v8_sell_condition_1
```python
dataframe["rsi"] > 80
```
RSI enters an extremely overheated zone (>80), facing potential pullback.

### 4.3 Custom Exit Logic

The strategy contains custom exit logic (custom_exit), dynamically adjusting based on holding time and profit situation:

```python
def custom_exit(...):
    # Start checking after holding for 30+ minutes
    # Decide whether to sell based on current profit and market state
```

---

## V. Technical Indicator System

### 5.1 Bollinger Bands

```python
window=20, stds=2
```

- **bb_lowerband**: Bollinger Band lower band — entry reference
- **bb_middleband**: Bollinger Band middle band — exit reference
- **bb_upperband**: Bollinger Band upper band — exit reference

### 5.2 Exponential Moving Averages (EMA)

| Period | Purpose |
|--------|---------|
| EMA5 | Short-term trend (sell conditions only) |
| EMA12 | MACD fast line |
| EMA26 | MACD slow line |
| EMA50 | Mid-term trend (1-hour cycle) |
| EMA200 | Long-term trend watershed |

### 5.3 Relative Strength Index (RSI)

- **Current Cycle RSI**: 14-period, short-term oversold detection
- **1-Hour Cycle RSI**: Mid-to-long-term oversold detection

### 5.4 Volume Indicators

- **volume**: Current volume
- **volume_mean_slow**: 30-period volume moving average
- **Volume contraction condition**: Current volume < previous volume × 4

### 5.5 SSL Channels

Trend confirmation indicators based on ATR and moving averages:
- **ssl_up**: Uptrend
- **ssl_down**: Downtrend

### 5.6 MACD Indicators

- **ema12**: Fast line
- **ema26**: Slow line
- **macdh**: MACD histogram

---

## VI. Risk Management Highlights

### 6.1 Custom Stop-Loss Logic (custom_stoploss)

The strategy's core risk control mechanism:

```python
def custom_stoploss(...):
    if current_profit > 0:
        return 0.99  # Do not actively stop-loss when profitable, rely on trailing stop
    else:
        # After holding for over 60 minutes
        trade_time_60 = trade.open_date_utc + timedelta(minutes=60)
```

#### Three Handling Methods in Loss State:

1. **RSI Bottom Zone** (1-hour RSI < 30)
   - Continue holding, wait for reversal
   - Return 0.99, do not trigger stop-loss

2. **Price Has Not Continued Falling**
   - If current price × 1.02 < opening price of candle 60 minutes ago
   - Minor stop-loss of 1%

3. **Other Loss Situations**
   - If current price × 1.01 < opening price of candle 60 minutes ago
   - Minor stop-loss of 1%

### 6.2 Trailing Stop

```python
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01      # 1% positive trail
trailing_stop_positive_offset = 0.03  # 3% offset activates it
```

### 6.3 ROI Ladder

| Time Range | Minimal Return |
|------------|---------------|
| 0–15 minutes | 8.0% |
| 15–45 minutes | 4.5% |
| 45–180 minutes | 2.0% |
| 180+ minutes | 0% |

---

## VII. Strategy Pros & Cons

### Strengths

1. **Multi-Condition Parallelism**: 16 independent buy conditions covering a wide range of market patterns
2. **Dual Timeframe**: Combines 1-hour trend judgment to reduce counter-trend trades
3. **Smart Stop-Loss**: Dynamically adjusts stop-loss based on market state after 60 minutes
4. **SSL Channel Integration**: Introduces SSL trend confirmation to improve signal quality
5. **Strictly Quantitative**: All conditions have explicit numerical values, reducing subjective judgment
6. **Volume Filtering**: Multiple conditions require volume contraction, avoiding chasing highs

### Weaknesses

1. **Conditions Are Numerous**: 16 "OR" conditions may lead to signal flooding
2. **Numerous Parameters**: High optimization difficulty, easy to overfit
3. **Complex and Hard to Interpret**: Difficult to explain why a particular signal triggered
4. **Unsuitable for Trending Markets**: Designed for ranging markets, may suffer frequent losses when trends develop
5. **Development Version Traits**: As V1, may require more live trading validation

---

## VIII. Applicable Scenarios

### Recommended Use Cases

1. **Ranging Markets**: Price range-bound with clear support and resistance
2. **Short-Term Trading**: 5-minute cycle, suitable for intraday trading
3. **Pair Selection**: Major coins with larger trading volumes
4. **Combined Use**: Can serve as part of a multi-strategy portfolio

### Not Recommended Cases

1. **Strong Trending Markets**: Prone to buying at highs during one-sided rallies or sell-offs
2. **Low Volatility Markets**: Insufficient volatility to trigger buy conditions
3. **Newly Listed Coins**: Abnormal volume, may generate false signals

---

## IX. Applicable Market Environment Details

### 9.1 Optimal Market Conditions

- **Moderate Volatility**: Bollinger Bands have sufficient width for price to reach lower band
- **Stable Volume**: No extreme volume contractions or surges
- **Range-Bound Oscillation**: Price repeatedly oscillates above and below EMA200
- **Has Rebound History**: Markets that quickly rebound after oversold conditions

### 9.2 Environment Adaptability

| Market Environment | Suitability | Notes |
|-------------------|-------------|-------|
| Ranging Uptrend | ★★★★☆ | Suitable for buying on pullbacks |
| Ranging Downtrend | ★★★☆☆ | Oversold buys may continue falling |
| Trending Uptrend | ★★☆☆☆ | Easy to miss and potentially chase highs |
| Trending Downtrend | ★☆☆☆☆ | Not recommended for counter-trend buying |
| High Volatility | ★★★★☆ | Bollinger Band strategies naturally suit it |
| Low Volatility | ★☆☆☆☆ | Insufficient volatility to trigger |

---

## X. Summary: The Cost of Complexity

### 10.1 Signal Interpretation Difficulty

This strategy contains 16 buy conditions and 3 sell conditions. In live trading:
- Difficult to explain "why buy"
- Difficult to backtest "which condition triggered"
- Optimization may affect interconnected components

### 10.2 Overfitting Risk

- Numerous parameters can be optimized
- Historically good parameters may not work for the future
- Recommended to use default parameters or only fine-tune slightly

### 10.3 Backtesting Notes

1. **Slippage**: Uses market orders, must consider slippage impact
2. **Liquidity**: Small-cap coins may not accommodate large capital
3. **Timeframe**: 1-hour informational cycle requires sufficient historical data
4. **Custom Stop-Loss**: Needs to simulate market state after 60 minutes
5. **Version Traits**: V1 is the first official iteration — requires more live trading validation

---

## XI. Risk Reminder

BinClucMadV1 is a complex quantitative trading system synthesizing multiple classic strategy concepts. Its core logic:

1. **Seek buy opportunities near the Bollinger Band lower band**
2. **Confirm reversal with RSI oversold and MACD golden cross**
3. **Confirm trend direction through SSL Channel**
4. **Control risk via custom stop-loss and trailing stop**

This strategy is suitable for quantitative traders with trading experience who can accept complex logic. For beginners, it is recommended to start from single-condition strategies and gradually understand the combination logic of various indicators.

**Risk Warning**:
- The strategy's stoploss is set to -0.10, actual risk depends on custom_stoploss logic
- 16 buy conditions may generate numerous signals requiring proper filtering
- In extreme market conditions, significant losses may occur
- V1 version is the first official release — recommended to validate with small positions first

---

*Document version: V1.0*  
*Last updated: 2025*  
*Strategy series: BinClucMad Family*
