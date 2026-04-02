# CombinedBinHClucAndMADV5 Strategy Analysis

> **Strategy Number**: #123 (123rd of 465 strategies)
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Combination
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**CombinedBinHClucAndMADV5** is an upgraded version of CombinedBinHClucAndMADV3, developed and open-sourced by ilya. This strategy adds a fifth buy condition group using SSL Channels + EMA + RSI on top of MADV3, forming a more diversified signal filtering system.

The strategy integrates the buy logic of four classic strategies: BinHV45 (Bollinger Band 40-period rebound), ClucMay72018 (Bollinger Band 20-period low-volume), MACD Low Buy (MACD low-position buy), and the newly added SSL Channel strategy. Multi-dimensional indicator cross-validation improves signal reliability.

From a code architecture perspective, the strategy's core design philosophy uses technical indicator combinations across different time periods to capture trend opportunities while filtering out most market noise. The strategy adopts 5 minutes as the primary timeframe, with a 1-hour informational timeframe for higher-dimensional trend judgment.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 5 independent buy signals, independently enableable/disableable |
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
    "0": 0.021,     # Immediate exit: 2.1% profit
    "40": 0.005,    # After 40 minutes: 0.5% profit
}

# Stop Loss Settings
stoploss = -0.99  # Effectively disabled hard stop-loss

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = False
trailing_stop_positive = 0.01      # 1% trailing stop activation
trailing_stop_positive_offset = 0.025  # 2.5% offset trigger
```

**Design Philosophy**:
- The ROI table sets a dual exit point strategy: 2.1% profit for immediate exit, or 0.5% after 40 minutes of holding. This embodies "fast in, fast out" while providing a guaranteed exit for longer-held trades
- Trailing stop configuration is relatively aggressive with 1% positive tracking and 2.5% offset trigger, suitable for letting profits run in trending markets

### 2.2 Exit Signal Configuration

```python
use_exit_signal = True
exit_profit_only = True                    # Exit only when profitable
exit_profit_offset = 0.001                 # Minimum profit threshold 0.1%
ignore_roi_if_entry_signal = False         # Entry signal does NOT override ROI exit
```

**Important Difference from MADV3**: `ignore_roi_if_entry_signal = False` ensures ROI exit logic takes priority over new entry signals — a key distinction from MADV3.

---

## III. Entry Conditions Details

### 3.1 Five Independent Buy Conditions

| Condition Group | Condition # | Core Logic | Source Strategy |
|----------------|-------------|------------|-----------------|
| **BB20 Low Volume (Bull)** | #1 | BB20 lower band + EMA trend confirmation + volume filtering | ClucMay72018 |
| **BB20 Low Volume (Bear)** | #2 | BB20 lower band + RSI oversold + volume contraction | ClucMay72018 |
| **MACD Low Buy (Bull)** | #3 | MACD golden cross + volume contraction + BB lower band | MACD Low Buy |
| **MACD Low Buy (Bear)** | #4 | MACD golden cross + strong volume contraction + BB lower band | MACD Low Buy |
| **SSL Channel + RSI** | #5 | SSL channel bullish + EMA trend + RSI reversal | SSL Channels |

### 3.2 Condition #1: ClucMay72018 Bull Mode (Guarded)

```python
# ClucMay72018 Buy Conditions - Bull Mode (guarded)
(
    (dataframe['close'] > dataframe['ema_200']) &
    (dataframe['close'] > dataframe['ema_200_1h']) &
    (dataframe['close'] < dataframe['ema_slow']) &
    (dataframe['close'] < 0.99 * dataframe['bb_lowerband']) &
    (dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 21)) &
    (dataframe['volume'] > 0)
)
```

### 3.3 Condition #2: ClucMay72018 Bear Mode (Unguarded)

```python
# ClucMay72018 Buy Conditions - Bear Mode (unguarded)
(
    (dataframe['close'] < dataframe['ema_slow']) &
    (dataframe['close'] < 0.975 * dataframe['bb_lowerband']) &
    (dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 20)) &
    (dataframe['volume'] < (dataframe['volume'].shift() * 4)) &
    (dataframe['rsi_1h'] < 15) &
    (dataframe['volume'] > 0)
)
```

**Key Difference**: Uses more stringent Bollinger Band condition (0.975 vs 0.99), requires RSI_1h < 15 (extreme oversold), and has stricter volume requirements.

### 3.4 Condition #3: MACD Low Buy Bull Mode

```python
# MACD Low Buy Buy Conditions - Bull Mode
(
    (dataframe['close'] > dataframe['ema_200']) &
    (dataframe['close'] > dataframe['ema_200_1h']) &
    (dataframe['ema_26'] > dataframe['ema_12']) &
    ((dataframe['ema_26'] - dataframe['ema_12']) > (dataframe['open'] * 0.02)) &
    ((dataframe['ema_26'].shift() - dataframe['ema_12'].shift()) > (dataframe['open']/100)) &
    (dataframe['volume'] < (dataframe['volume'].shift() * 4)) &
    (dataframe['close'] < (dataframe['bb_lowerband'])) &
    (dataframe['volume'] > 0)
)
```

### 3.5 Condition #4: MACD Low Buy Bear Mode

```python
# MACD Low Buy Buy Conditions - Bear Mode
(
    (dataframe['ema_26'] > dataframe['ema_12']) &
    ((dataframe['ema_26'] - dataframe['ema_12']) > (dataframe['open'] * 0.03)) &
    ((dataframe['ema_26'].shift() - dataframe['ema_12'].shift()) > (dataframe['open']/100)) &
    (dataframe['volume'] < (dataframe['volume'].shift() * 4)) &
    (dataframe['close'] < (dataframe['bb_lowerband'])) &
    (dataframe['volume'] > 0)
)
```

**Key Difference**: Uses more stringent MACD difference condition (3% vs 2%), no EMA trend requirement.

### 3.6 Condition #5: SSL Channel + EMA + RSI Reversal (Newly Added)

```python
# SSL Channel Strategy (newly added condition)
(
    (dataframe['close'] < dataframe['sma_5']) &
    (dataframe['ssl_up_1h'] > dataframe['ssl_down_1h']) &
    (dataframe['ema_50'] > dataframe['ema_200']) &
    (dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
    (dataframe['rsi'] < dataframe['rsi_1h'] - 43.276) &
    (dataframe['volume'] > 0)
)
```

**Logic Analysis**:
- Close below SMA5 indicates short-term pullback
- 1h SSL channel must be in bullish alignment (ssl_up > ssl_down)
- Both 5m and 1h EMAs must be in bullish alignment (50 > 200)
- RSI divergence: 5m RSI must be at least 43.276 points below 1h RSI — a strong rebound signal
- This condition does not rely on volume limits, focusing on trend and momentum reversal signals

### 3.7 Buy Condition Summary

| Condition | Trend Requirement | Bollinger Band Condition | Volume Requirement | Price-Volume Feature |
|-----------|-------------------|-------------------------|-------------------|---------------------|
| **#1 Cluc Bull** | 5m + 1h EMA200 | BB20 × 0.99 | < 21× avg volume | Oversold rebound |
| **#2 Cluc Bear** | None | BB20 × 0.975 | < 20× avg + < prev | Extreme oversold |
| **#3 MACD Bull** | 5m + 1h EMA200 | BB20 lower band | < prev × 4 | Golden cross rebound |
| **#4 MACD Bear** | None | BB20 lower band | < prev × 4 | Strong golden cross rebound |
| **#5 SSL+RSI** | 5m + 1h EMA bullish | None | None | RSI divergence rebound |

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

### 4.2 ROI Dual Exit Point Mechanism

```python
minimal_roi = {
    "0": 0.021,     # Immediate exit: 2.1% profit
    "40": 0.005,    # After 40 minutes: 0.5% profit
}
```

**Key Difference from MADV3**: Adds a guaranteed exit point after 40 minutes. If still not triggered after 40 minutes, exit with just 0.5% profit — preventing long-holding from consuming fees.

### 4.3 Custom Stop-Loss Logic

```python
def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs) -> float:
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
| **Exponential Moving Average** | EMA5, EMA12, EMA26, EMA50, EMA200 | Trend judgment and dynamic support/resistance |
| **Simple Moving Average** | SMA5 | Short-term pullback identification |
| **Volume** | volume, volume_mean_slow (30) | Volume anomaly detection |
| **Relative Strength** | RSI (14) | Overbought/oversold judgment |

### 5.2 Informational Timeframe (1h) Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Exponential Moving Average** | EMA50_1h, EMA200_1h | Higher-dimensional trend confirmation |
| **Relative Strength** | RSI_1h (14) | Long-term overbought/oversold judgment |
| **SSL Channel** | ssl_up_1h, ssl_down_1h | Trend channel identification |

### 5.3 SSL Channel Indicator Details

```python
def SSLChannels(dataframe, length=7):
    df = dataframe.copy()
    df['ATR'] = ta.ATR(df, timeperiod=14)
    df['smaHigh'] = df['high'].rolling(length).mean() + df['ATR']
    df['smaLow'] = df['low'].rolling(length).mean() - df['ATR']
    df['hlv'] = np.where(df['close'] > df['smaHigh'], 1, 
                        np.where(df['close'] < df['smaLow'], -1, np.nan))
    df['hlv'] = df['hlv'].ffill()
    df['sslDown'] = np.where(df['hlv'] < 0, df['smaHigh'], df['smaLow'])
    df['sslUp'] = np.where(df['hlv'] < 0, df['smaLow'], df['smaHigh'])
    return df['sslDown'], df['sslUp']
```

---

## VI. Risk Management Features

### 6.1 RSI Divergence Filtering

Condition #5's unique RSI divergence mechanism:

```python
dataframe['rsi'] < dataframe['rsi_1h'] - 43.276
```

This requires 5m RSI to be at least 43.276 points below 1h RSI, representing:
- Short-term oversold degree far exceeding long-term
- Strong rebound momentum present
- Classic bottom divergence signal

### 6.2 Time Stop-Loss Mechanism

| Holding Time | Profit State | Behavior |
|-------------|---------------|----------|
| < 240 minutes | Profitable | Continue holding, chase trend |
| < 240 minutes | Losing | Continue holding, wait for reversal |
| >= 240 minutes | Profitable | Continue holding, let profits run |
| >= 240 minutes | Losing | **Forced exit** |

---

## VII. Strategy Pros & Cons

### Advantages

1. **Upgraded Strategy Fusion**: Adds SSL Channel conditions on top of MADV3, forming fusion of four strategies
2. **Multi-Timeframe Analysis**: Combines 5-minute, 1-hour, and SSL Channel for comprehensive market view
3. **Bull/Bear Dual Mode**: Each condition has parameter configurations for different market environments
4. **Strict Volume Filtering**: Effectively filters false breakouts through volume contraction
5. **RSI Divergence Innovation**: The newly added RSI divergence condition provides unique rebound signals
6. **ROI Dual Protection**: 40-minute guaranteed exit point prevents long-holding fee consumption

### Limitations

1. **Increased Condition Count**: 5 buy conditions increase potential for signal conflicts
2. **Strong Trend Dependency**: May underperform in volatile markets
3. **Single Sell Signal**: Relies solely on Bollinger middle band breakout
4. **Parameter Complexity**: Larger parameter space than MADV3, with higher optimization difficulty

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Clear Uptrend** | Enable conditions #1, #3 | Breakout signals capture trend initiation |
| **Volatile Rebound** | Enable conditions #2, #4 | Oversold rebound suitable for range-bound markets |
| **Fast Drop Followed by Rebound** | Enable condition #5 | RSI divergence captures strong rebounds |
| **Multi-Timeframe Confirmation** | Enable condition #5 | SSL Channel + EMA dual confirmation |

---

## IX. Live Trading Notes

**CombinedBinHClucAndMADV5** is an upgraded version of MADV3, adding SSL Channel strategy as the fifth buy condition on top of the original three-strategy fusion. With ~180 lines of code, it implements a more diversified signal verification system.

### 9.1 Core Strategy Logic

- **Multi-Strategy Complementarity**: BinHV45 excels at breakouts, ClucMay72018 at oversold rebounds, MACD Low at golden cross opportunities, SSL Channel at RSI divergence
- **Price-Volume Coordination**: All conditions emphasize volume cooperation
- **Trend Filtering**: Multiple conditions explicitly require EMA trend confirmation

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| Trending Up | ⭐⭐⭐⭐⭐ | EMA conditions easily satisfied; breakout signals frequent |
| Trending Down | ⭐⭐☆☆☆ | EMA200 conditions hard to satisfy; buy signals rare |
| Range-Bound | ⭐⭐⭐☆☆ | Multiple conditions may trigger; trend conditions filter some |
| High Volatility | ⭐⭐⭐☆☆ | Bollinger Band width expands; more signals but also more noise |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Notes |
|--------------|-------------------|-------|
| minimal_roi | {"0": 0.021, "40": 0.005} | 2.1% immediate or 0.5% after 40 minutes |
| trailing_stop_positive | 0.01 | 1% trailing stop |
| trailing_stop_positive_offset | 0.025 | 2.5% offset trigger |
| exit_profit_only | True | Exit only when profitable |

---

## X. Summary

**CombinedBinHClucAndMADV5** is an upgraded version of CombinedBinHClucAndMADV3 with more sophisticated design. Its core value lies in:

1. **Upgraded Strategy Fusion**: Achieves fusion of four classic strategies through the new SSL Channel condition
2. **RSI Divergence Innovation**: Unique RSI divergence condition provides new rebound signal sources
3. **Dual Mode Design**: Bull/bear dual mode configuration improves strategy adaptability
4. **ROI Dual Protection**: 40-minute guaranteed exit point provides more flexible risk management

For quantitative traders, this strategy is worth testing, especially for better performance in trending markets. Start with mainstream coins and expand to more trading pairs after gradual parameter optimization.

---

*This document is written based on the CombinedBinHClucAndMADV5 strategy source code.*
