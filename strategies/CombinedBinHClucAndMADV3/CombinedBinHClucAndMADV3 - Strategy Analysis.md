# CombinedBinHClucAndMADV3 Strategy Analysis

> **Strategy Number**: #122 (122nd of 465 strategies)
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Combination
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**CombinedBinHClucAndMADV3** is a combined strategy fusing three classic quantitative trading strategies, developed and open-sourced by ilya. The strategy integrates the buy logic from BinHV45 (Bollinger Band 40-period rebound), ClucMay72018 (Bollinger Band 20-period low-volume), and MACD Low Buy (MACD low-position buy) strategies, improving signal reliability through multi-dimensional indicator cross-validation.

From a code architecture perspective, the strategy's core design philosophy uses technical indicator combinations across different time periods to capture trend opportunities while filtering out most market noise. The strategy adopts 5 minutes as the primary timeframe, with a 1-hour informational timeframe for higher-dimensional trend judgment.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 3 independent buy signals, independently enableable/disableable |
| **Sell Conditions** | 1 basic sell signal + trailing stop |
| **Protection Mechanism** | Custom stop-loss logic (forced exit after 240 minutes of holding) |
| **Timeframe** | 5-minute primary + 1-hour informational |
| **Dependencies** | TA-Lib, technical (qtpylib), numpy, pandas |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table (time: minimum profit rate)
minimal_roi = {
    "0": 0.021,    # Immediate exit: 2.1% profit
}

# Stop Loss Settings
stoploss = -0.99  # Effectively disabled hard stop-loss

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = False
trailing_stop_positive = 0.01      # 1% trailing activation
trailing_stop_positive_offset = 0.025  # 2.5% offset trigger
```

**Design Philosophy**:
- The hard stop-loss set to -99% means the strategy almost entirely relies on custom stop-loss logic (`custom_stoploss`) for risk control
- The ROI table sets only one exit point (2.1%), indicating the strategy prefers to exit quickly after gaining some profit rather than holding long-term
- Trailing stop configuration is relatively aggressive: 1% positive tracking with 2.5% offset trigger, suitable for letting profits run in trending markets

### 2.2 Order Type Configuration

```python
order_types = {
    'entry': 'limit',       # Limit order entry
    'exit': 'limit',        # Limit order exit
    'stoploss': 'market',   # Market order stop-loss
    'stoploss_on_exchange': False
}
```

### 2.3 Exit Signal Configuration

```python
use_exit_signal = True
exit_profit_only = True                    # Exit only when profitable
exit_profit_offset = 0.001                 # Minimum profit threshold 0.1%
ignore_roi_if_entry_signal = True          # Entry signal can override ROI exit
```

---

## III. Entry Conditions Details

### 3.1 Three Independent Buy Conditions

| Condition Group | Condition # | Core Logic | Source Strategy |
|----------------|-------------|------------|-----------------|
| **BB40 Rebound** | #1 | BB40 lower band breakout + EMA trend confirmation + volume-price verification | BinHV45 |
| **BB20 Low Volume** | #2 | BB20 lower band low-volume rebound + EMA trend confirmation | ClucMay72018 |
| **MACD Low Buy** | #3 | MACD golden cross + volume contraction + BB lower band | MACD Low Buy |

### 3.2 Condition #1: BinHV45 Strategy Logic

```python
# BinHV45 Buy Conditions
(
    (dataframe['close'] > dataframe['ema_200_1h']) &
    (dataframe['ema_50'] > dataframe['ema_200']) &
    (dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
    dataframe['lower'].shift().gt(0) &
    dataframe['bbdelta'].gt(dataframe['close'] * 0.031) &
    dataframe['closedelta'].gt(dataframe['close'] * 0.018) &
    dataframe['tail'].lt(dataframe['bbdelta'] * 0.233) &
    dataframe['close'].lt(dataframe['lower'].shift()) &
    dataframe['close'].le(dataframe['close'].shift()) &
    (dataframe['volume'] > 0)
)
```

**Logic Analysis**:
- First confirms overall uptrend via EMA200 (both 1h and 5m timeframes)
- Bollinger Band width and close change conditions identify the "squeeze" pattern before price breakout
- Tail condition filters candles with obvious lower wicks — a typical reversal signal
- Close must be below the BB40 lower band of the previous candle — core trigger point for the buy signal

### 3.3 Condition #2: ClucMay72018 Strategy Logic

```python
# ClucMay72018 Buy Conditions
(
    (dataframe['close'] < dataframe['ema_slow']) &
    (dataframe['close'] < 0.985 * dataframe['bb_lowerband']) &
    (dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 20)) &
    (dataframe['volume'] < (dataframe['volume'].shift() * 4)) &
    (dataframe['volume'] > 0)
)
```

**Logic Analysis**:
- Price must be below EMA50 — confirms downtrend
- Close must be below 98.5% of Bollinger lower band — ensures price is deep in oversold territory
- Volume constraints are the core highlight: requires volume to be both below 5% of the 30-period average AND below 25% of the previous candle's volume
- This extreme volume contraction effectively filters out most false breakout signals

### 3.4 Condition #3: MACD Low Buy Strategy Logic

```python
# MACD Low Buy Buy Conditions
(
    (dataframe['ema_26'] > dataframe['ema_12']) &
    ((dataframe['ema_26'] - dataframe['ema_12']) > (dataframe['open'] * 0.02)) &
    ((dataframe['ema_26'].shift() - dataframe['ema_12'].shift()) > (dataframe['open']/100)) &
    (dataframe['volume'] < (dataframe['volume'].shift() * 4)) &
    (dataframe['close'] < (dataframe['bb_lowerband'])) &
    (dataframe['volume'] > 0)
)
```

**Logic Analysis**:
- MACD must be in golden cross state with sufficiently large difference (exceeding 2% of open price)
- MACD difference must also be expanding on the previous candle — trend continuation confirmation
- Volume must be significantly contracted (less than 1/4 of the previous candle) — classic "low volume bottom" pattern
- Close must be below Bollinger lower band; combined with MACD golden cross, forms an "oversold rebound" signal combination

### 3.5 Buy Condition Summary

| Condition | EMA Trend Requirement | Bollinger Band Condition | Volume Requirement | Price-Volume Feature |
|-----------|----------------------|-------------------------|-------------------|---------------------|
| **#1 BinHV45** | 5m + 1h multi-period confirmation | BB40 lower band breakout | No special requirement | Breakout type |
| **#2 ClucMay72018** | No explicit requirement | BB20 lower band × 0.985 | Extreme contraction | Rebound type |
| **#3 MACD Low** | MACD golden cross confirmation | BB20 lower band | Contracted | Rebound type |

---

## IV. Exit Conditions Details

### 4.1 Basic Sell Signal

```python
# Sell Condition
(
    (dataframe['close'] > dataframe['bb_middleband'] * 1.01) &
    (dataframe['volume'] > 0)
)
```

**Logic Analysis**:
- Sell triggers when price breaks above Bollinger middle band (+1% buffer)
- This design follows the "let profits run" philosophy — continue holding as long as the trend extends
- Bollinger middle band has dynamic characteristics, adjusting with price movement, providing adaptive reference for take-profit

### 4.2 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_only_offset_is_reached = False
trailing_stop_positive = 0.01          # 1% trailing stop
trailing_stop_positive_offset = 0.025  # 2.5% offset trigger
```

### 4.3 Custom Stop-Loss Logic

```python
def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs) -> float:
    # Forced exit if holding > 240 minutes and at a loss
    if (current_profit < 0) & (current_time - timedelta(minutes=240) > trade.open_date_utc):
        return 0.01  # Exit position
    return 0.99     # Maintain position
```

---

## V. Technical Indicator System

### 5.1 Primary Timeframe (5m) Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Bollinger Band** | BB40 (lower, mid, bbdelta, closedelta, tail) | Price squeeze and breakout identification |
| **Bollinger Band** | BB20 (bb_lowerband, bb_middleband, bb_upperband) | Overbought/oversold zone judgment |
| **Exponential Moving Average** | EMA12, EMA26, EMA50, EMA200 | Trend judgment and dynamic support/resistance |
| **Volume** | volume, volume_mean_slow (30) | Volume anomaly detection |
| **Relative Strength** | RSI (14) | Overbought/oversold judgment |

### 5.2 Informational Timeframe (1h) Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Exponential Moving Average** | EMA50_1h, EMA200_1h | Higher-dimensional trend confirmation |
| **Relative Strength** | RSI_1h (14) | Long-term overbought/oversold judgment |

---

## VI. Risk Management Features

### 6.1 Multi-Dimensional Trend Confirmation

The strategy requires consistent EMA trends across multiple timeframes, effectively filtering counter-trend signals.

### 6.2 Volume Anomaly Filtering

All three buy conditions include volume verification logic — a key mechanism preventing false breakouts.

### 6.3 Time Stop-Loss Mechanism

The 240-minute limit in custom stop-loss is a simple yet effective risk control tool.

---

## VII. Strategy Pros & Cons

### Advantages

1. **Multi-Strategy Fusion**: Integrates three market-tested classic strategies
2. **Multi-Timeframe Analysis**: Combines 5-minute and 1-hour timeframes for comprehensive market view
3. **Strict Volume Filtering**: Effectively filters false breakouts through volume contraction conditions
4. **Custom Stop-Loss Protection**: 240-minute time stop-loss prevents prolonged losing positions
5. **Simple Exit Logic**: Break above Bollinger middle band to sell, avoiding over-optimization

### Limitations

1. **Strong Trend Dependency**: May underperform in volatile markets due to trend confirmation in buy conditions
2. **Single Sell Signal**: Relies solely on Bollinger middle band breakout, potentially missing larger trend moves
3. **Limited Parameter Space**: Fewer adjustable parameters compared to complex strategies
4. **High Liquidity Requirements**: Low-volume conditions may fail to find qualifying trades in low-liquidity markets

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Clear Uptrend** | Enable BinHV45 condition | Breakout signals capture trend initiation |
| **Volatile Rebound** | Enable ClucMay72018 condition | Oversold rebound suitable for range-bound markets |
| **Fast Drop Followed by Rebound** | Enable MACD Low condition | MACD golden cross + oversold captures rebound |
| **High Volatility** | Reduce trailing stop offset | Give trend more room to extend |

---

## IX. Live Trading Notes

**CombinedBinHClucAndMADV3** is one of the most classic combined strategies in the Freqtrade ecosystem, with moderate code volume (~150 lines). Based on its architecture and indicator characteristics, it performs best in **markets with clear trends** and may be average in **high-volatility volatile** environments.

### 9.1 Core Strategy Logic

- **Multi-Strategy Complementarity**: BinHV45 excels at breakout moves, ClucMay72018 at oversold rebounds, MACD Low at MACD golden cross opportunities
- **Price-Volume Coordination**: All conditions emphasize volume cooperation, avoiding "volume-less rally" false signals
- **Trend Filtering**: BinHV45 explicitly requires EMA trend confirmation — key to avoiding counter-trend trades

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| Trending Up | ⭐⭐⭐⭐⭐ | EMA conditions easily satisfied; breakout signals fire frequently |
| Trending Down | ⭐⭐☆☆☆ | 1h EMA200 conditions hard to satisfy; buy signals rare |
| Range-Bound | ⭐⭐⭐☆☆ | ClucMay72018 and MACD Low may trigger; trend conditions filter some signals |
| High Volatility | ⭐⭐⭐☆☆ | Bollinger Band width expands; more signals but also more noise |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Notes |
|--------------|-------------------|-------|
| minimal_roi | {"0": 0.021} | 2.1% take-profit, consistent with fast-in-fast-out nature |
| trailing_stop_positive | 0.01 | 1% trailing stop, giving trend sufficient room |
| trailing_stop_positive_offset | 0.025 | 2.5% offset trigger, ensuring some profit before activation |
| exit_profit_only | True | Exit only when profitable, avoiding loss-cutting panic |

---

## X. Summary

**CombinedBinHClucAndMADV3** is a cleverly designed multi-strategy combined trading strategy. Its core value lies in:

1. **Strategy Fusion**: Achieves multi-dimensional signal verification through integrating three classic strategies
2. **Simple and Efficient**: Moderate code volume, clear logic, easy to understand and maintain
3. **Risk Control**: Additional protection layer through custom stop-loss and time stop-loss
4. **Wide Adaptability**: Three conditions each have different focuses, adaptable to various market environments

For quantitative traders, this strategy is a good entry-level choice — learning multi-strategy fusion design while gaining reasonable returns in actual trading. Start testing with mainstream coins and expand to more trading pairs after gradual parameter optimization.

---

*This document is written based on the CombinedBinHClucAndMADV3 strategy source code.*
