# CombinedBinHAndClucV8Hyper Strategy Analysis

> **Strategy Number**: #119 (Batch 12, 119th Strategy)
> **Strategy Type**: Multi-Factor Mean Reversion · Oversold Rebound Strategy
> **Timeframe**: 5 Minutes (5m) + 1 Hour (1h informational timeframe)

---

## I. Strategy Overview

CombinedBinHAndClucV8Hyper is a **multi-factor mean reversion** trading strategy—the **Hyperoptable-optimized version of V8**. It combines BinHV45 and ClucMay72018 with **custom take-profit** and **custom stop-loss protection**, enabling more precise capture of oversold rebound opportunities through hyperparameter optimization.

The core idea is: **on V8's foundation, introducing optimizable hyperparameters to allow the strategy to further adapt to different market environments through Hyperopt.**

**V8Hyper vs V8 Core Upgrades**:
- New optimizable entry parameters: BB40, BB20, RSI, MFI parameters
- New optimizable exit parameters: RSI threshold
- Custom take-profit mechanism: Dynamic take-profit across 4 ROI levels + 2 trailing levels
- Custom stop-loss mechanism: Time-based and trend-based smart stop-loss
- More flexible trailing configuration: Activates at 3.11% profit, triggers on 3.14% pullback
- Hard stop at -27.4% (more practical than V8's -99%)
- 5 entry conditions + multi-timeframe (5m + 1h) analysis

---

## II. Strategy Configuration Analysis

### 2.1 Basic Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `timeframe` | 5m | 5-minute candles |
| `inf_1h` | 1h | 1-hour informational timeframe for trend judgment |
| `minimal_roi` | {"0": 0.107, "15": 0.047, "75": 0.013, "106": 0} | Multi-level ROI take-profit |
| `stoploss` | -0.274 | Hard stop at -27.4% |
| `use_exit_signal` | True | Enable exit signal judgment |
| `exit_profit_only` | True | Only sell in profitable state |
| `exit_profit_offset` | 0.001 | Only allow selling after profit exceeds 0.1% |
| `ignore_roi_if_entry_signal` | True | Ignore ROI limit when entry signal appears |

### 2.2 Trailing Stop Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| `trailing_stop` | True | Enable trailing stop |
| `trailing_only_offset_is_reached` | False | Trail regardless of offset |
| `trailing_stop_positive` | 0.314 | Trailing stop distance 31.4% |
| `trailing_stop_positive_offset` | 0.411 | Activate trailing when profit reaches 41.1% |

> **V8Hyper Key Change**: Trailing stop activation and pullback are both large—suited for long-term trending markets. Hard stop at -27.4% is much more practical than V8's -99%.

---

## III. Entry Conditions Details

The strategy has **5 independent entry conditions**—meeting any one triggers a buy:

### 3.1 Condition One: BinHV45 Strategy (Rapid Sell-off in Major Uptrend)

```python
(dataframe['close'] > dataframe['ema_200_1h']) &
(dataframe['ema_50'] > dataframe['ema_200']) &
(dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
(((dataframe['open'].rolling(2).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_1.value) &
(((dataframe['open'].rolling(12).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_2.value) &
dataframe['lower'].shift().gt(0) &
dataframe['bbdelta'].gt(dataframe['close'] * self.buy_bb40_bbdelta_close.value) &
dataframe['closedelta'].gt(dataframe['close'] * self.buy_bb40_closedelta_close.value) &
dataframe['tail'].lt(dataframe['bbdelta'] * self.buy_bb40_tail_bbdelta.value) &
dataframe['close'].lt(dataframe['lower'].shift()) &
dataframe['close'].le(dataframe['close'].shift()) &
(dataframe['volume'] > 0)
```

**Combined Logic**: In a major uptrend, price dips slightly and pierces the lower Bollinger Band with sufficient volatility and a short lower wick—typical **oversold rebound in uptrend** pattern.

### 3.2 Condition Two: ClucMay72018 Strategy (Volume-Shrinking Oversold in Uptrend)

```python
(dataframe['close'] > dataframe['ema_200']) &
(dataframe['close'] > dataframe['ema_200_1h']) &
(dataframe['ema_50_1h'] > dataframe['ema_100_1h']) &
(dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
(((dataframe['open'].rolling(2).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_1.value) &
(((dataframe['open'].rolling(12).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_2.value) &
(dataframe['close'] < dataframe['ema_slow']) &
(dataframe['close'] < self.buy_bb20_close_bblowerband.value * dataframe['bb_lowerband']) &
(dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * self.buy_bb20_volume.value))
```

**Combined Logic**: In a major uptrend, price dips to the lower Bollinger Band with shrinking volume—typical **volume-shrinking oversold** pattern.

### 3.3 Condition Three: RSI Divergence Type (V8 New)

```python
(dataframe['close'] < dataframe['sma_5']) &
(dataframe['ssl_up_1h'] > dataframe['ssl_down_1h']) &
(dataframe['ema_50'] > dataframe['ema_200']) &
(dataframe['ema_50_1h'] > dataframe['ema_200_1h']) &
(((dataframe['open'].rolling(2).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_1.value) &
(((dataframe['open'].rolling(12).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_2.value) &
(((dataframe['open'].rolling(144).max() - dataframe['close']) / dataframe['close']) < self.buy_dip_threshold_3.value) &
(dataframe['rsi'] < dataframe['rsi_1h'] - self.buy_rsi_diff.value)
```

**Combined Logic**: Short-term price makes a new low but RSI doesn't—a **bottom divergence** signal.

### 3.4 Condition Four: Trend Pullback Type

**Combined Logic**: In a long-term uptrend, price pulls back to support while both RSI and MFI are in oversold territory.

### 3.5 Condition Five: EMA Crossover Type (V8Hyper Unique)

**Combined Logic**: At the 1-hour level, EMA forms a golden cross while price breaks below the lower Bollinger Band.

---

## IV. Exit Conditions Details

### 4.1 Condition One: Bollinger Band Upper Rail Breakout (Continuous Confirmation)

Continuous 3 candles' close prices all above the Bollinger Band upper rail—confirming valid breakout.

### 4.2 Condition Two: RSI Overbought

RSI exceeds 76.4, entering overbought territory.

### 4.3 Custom Exit: Multi-Level ROI + Trailing

**4-Level ROI Take-Profit**:
- Profit > 14% + RSI < 58 → Sell
- Profit > 8% + RSI < 56 → Sell
- Profit > 4% + RSI < 50 → Sell
- Profit > 1% + RSI < 50 → Sell
- Profit > 0% + < 4% + SMA200 trending down → Sell

**2-Level Trailing Take-Profit**:
- Profit 10%-40%, high-to-current pullback > 3% → Sell
- Profit 2%-10%, high-to-current pullback > 1.5% → Sell

---

## V. Custom Stop-Loss Mechanism

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    if (current_profit < 0) & (current_time - timedelta(minutes=280) > trade.open_date_utc):
        return 0.01
    elif (current_profit < self.sell_custom_stoploss_1.value):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        if (last_candle is not None):
            if (last_candle['sma_200_dec']) & (last_candle['sma_200_dec_1h']):
                return 0.01
    return 0.99
```

**Stop-Loss Logic**:
1. **Time Stop-Loss**: If in loss for 280+ minutes (~4.7 hours), force close
2. **Trend Stop-Loss**: If drop exceeds 5% AND SMA200 simultaneously trending down, force close

---

## VI. Risk Management Features

### 6.1 Multi-Layer Risk Control System

1. **Hard Stop-Loss**: -27.4% (much more practical than V8's -99%)
2. **Time Stop-Loss**: Loss for 280 minutes → force exit
3. **Trend Stop-Loss**: Loss > 5% + SMA200 trending down → force exit
4. **Trailing Stop**: Activate at 41.1% profit, 31.4% pullback triggers
5. **Multi-Level ROI Take-Profit**: 4 levels, dynamic exit based on profit level
6. **Multi-Level Trailing Take-Profit**: 2 levels, dynamic protection

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **5 Entry Conditions**: Covers multiple oversold rebound patterns
2. **Custom Take-Profit**: 4-level ROI + 2-level trailing, highly intelligent
3. **Custom Stop-Loss**: Time stop + trend stop, comprehensive protection
4. **Optimizable Hyperparameters**: Can adapt to different markets
5. **Multi-Timeframe**: 5m + 1h analysis, more robust
6. **Practical Hard Stop**: -27.4% much better than -99%

### ⚠️ Cons

1. **Hard Stop Relatively Wide**: -27.4% may cause significant losses
2. **Trailing Activation High**: 41.1% before trailing activates—may miss some profits
3. **Complex Multi-Factor**: 5 entry conditions increase overfitting risk
4. **Multi-Timeframe Dependency**: 1h trend affects 5m decisions
5. **Parameter Overfitting Risk**: Many optimizable parameters

---

## VIII. Summary

CombinedBinHAndClucV8Hyper is a **multi-factor mean reversion strategy** combining multiple oversold rebound logics with customizable take-profit and stop-loss.

**Core Advantages**:
- Multiple entry conditions covering various oversold rebound patterns
- Custom take-profit with 4-level ROI + 2-level trailing
- Custom stop-loss with time stop + trend stop
- Optimizable hyperparameters for market adaptation

**Core Risks**:
- Hard stop relatively wide, may cause significant losses
- High trailing activation, may miss small profits
- Parameter optimization increases overfitting risk

**Usage Suggestions**:
- Use with 4-6 trading pairs
- Use Volume Pairlist
- Exclude leveraged tokens (*BULL, *BEAR, *UP, *DOWN)
- Best used with USDT pairs

**Key Takeaways**:
- ✅ Multiple entry conditions, broadest adaptability
- ✅ Custom take-profit and stop-loss, comprehensive protection
- ✅ Hyperparameter optimizable, adaptable
- ⚠️ Wide hard stop, significant losses possible
- ⚠️ High trailing activation threshold
- ⚠️ Parameter overfitting risk
