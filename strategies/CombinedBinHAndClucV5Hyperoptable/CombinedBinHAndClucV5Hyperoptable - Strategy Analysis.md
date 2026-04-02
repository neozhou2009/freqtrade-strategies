# CombinedBinHAndClucV5Hyperoptable Strategy Analysis

> **Strategy Number**: #119 (Batch 12, 119th Strategy)
> **Strategy Type**: Multi-Factor Mean Reversion · Oversold Rebound Strategy (Hyperparameter-Optimized Version)
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

CombinedBinHAndClucV5Hyperoptable is a **multi-factor mean reversion** trading strategy—the **hyperparameter-optimized version** of CombinedBinHAndClucV5. It combines BinHV45 and ClucMay72018 signal logic and has been through hyperparameter optimization to more precisely capture oversold rebound opportunities in sideways markets.

The core idea is: **when price deviates from the lower Bollinger Band and shows a clear contracting pattern, it is identified as a potential mean reversion signal.** Volume filtering and EMA trend judgment reduce false breakout probability. The Hyperoptable version further optimizes parameters based on V5, tailoring the strategy to specific market environments.

**Hyperoptable vs V5 Core Optimization**:
- Parameters optimized through hyperparameter automated search, finding better parameter combinations for target trading pairs
- Take-profit threshold, trailing stop parameters finely tuned
- Entry/exit condition thresholds may be adjusted to fit optimization objectives

---

## II. Strategy Configuration Analysis

### 2.1 Basic Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `timeframe` | 5m | 5-minute candles |
| `minimal_roi` | {"0": 0.02} | Take-profit at 2.0% cumulative return |
| `stoploss` | -0.99 | Stop-loss nearly disabled (-99%) |
| `use_exit_signal` | True | Enable exit signal judgment |
| `exit_profit_only` | True | Only sell in profitable state |
| `exit_profit_offset` | 0.001 | Only allow selling after profit exceeds 0.1% |
| `ignore_roi_if_entry_signal` | True | Ignore ROI limit when entry signal appears |

### 2.2 Trailing Stop Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| `trailing_stop` | True | Enable trailing stop |
| `trailing_only_offset_is_reached` | True | Only activate trailing after profit reaches offset |
| `trailing_stop_positive` | 0.0125 | Trailing stop distance 1.25% |
| `trailing_stop_positive_offset` | 0.0275 | Activate trailing when profit reaches 2.75% |

> **Hyperoptable Key Change**: Parameters optimized through hyperparameter search, potentially micro-tuned for specific markets.

---

## III. Entry Conditions Details

### 3.1 Condition One: BinHV45 Strategy

```python
(dataframe['lower'].shift().gt(0) &
 dataframe['bbdelta'].gt(dataframe['close'] * 0.008) &
 dataframe['closedelta'].gt(dataframe['close'] * 0.0175) &
 dataframe['tail'].lt(dataframe['bbdelta'] * 0.25) &
 dataframe['close'].lt(dataframe['lower'].shift()) &
 dataframe['close'].le(dataframe['close'].shift()) &
 (dataframe['volume'] > 0))
```

**Signal Interpretation**:

| Condition | Meaning |
|----------|---------|
| `lower.shift() > 0` | Confirm lower Bollinger Band is valid |
| `bbdelta > close * 0.008` | Channel width at least 0.8% of price |
| `closedelta > close * 0.0175` | Closing price differs from previous close by more than 1.75% |
| `tail < bbdelta * 0.25` | Lower wick less than 25% of channel width |
| `close < lower.shift()` | Close breaks below previous day's lower Bollinger Band |
| `close <= close.shift()` | Close not higher than previous day's close |
| `volume > 0` | Exclude zero-volume abnormal candles |

**Combined Logic**: Price drops rapidly and pierces the lower Bollinger Band with sufficient volatility and a short lower wick—typical **oversold rebound** pattern.

### 3.2 Condition Two: ClucMay72018 Strategy

```python
((dataframe['close'] < dataframe['ema_slow']) &
 (dataframe['close'] < 0.985 * dataframe['bb_lowerband']) &
 (dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 20)) &
 (dataframe['volume'] > 0))
```

**Signal Interpretation**:

| Condition | Meaning |
|----------|---------|
| `close < ema_slow` | Price below 50-day EMA, confirming medium-term downtrend |
| `close < 0.985 * bb_lowerband` | Price clearly below Bollinger Band lower rail |
| `volume < volume_mean_slow.shift(1) * 20` | Volume less than 20x the 30-day average |
| `volume > 0` | Exclude zero-volume abnormal candles |

**Combined Logic**: In a downtrend, price rapidly breaks below the lower Bollinger Band, but volume does not expand—downward momentum is insufficient.

### 3.3 Entry Signal Trigger Rules

The two conditions have an **OR relationship**—meeting either one generates a buy signal.

---

## IV. Exit Conditions Details

### 4.1 Take-Profit Logic

- Take-profit triggers when cumulative return reaches **2.0%**
- `exit_profit_only = True` ensures selling only in profitable state
- `exit_profit_offset = 0.001` requires profit to exceed 0.1%

### 4.2 Trailing Stop Logic

When open profit reaches **2.75%**, trailing stop activates:
- Stop-loss line moves up, locking in at least **1.25%** of profit
- If price continues to rise, the stop-loss line follows
- If price drops back to touch the trailing stop line, close at market price

> **Hyperoptable Key Change**: Parameters optimized through hyperparameter search, may be better suited to target market's volatility characteristics.

### 4.3 Exit Signal Conditions

```python
(dataframe['close'] > dataframe['bb_upperband']) &
(dataframe['close'].shift(1) > dataframe['bb_upperband'].shift(1)) &
(dataframe['high'].shift(2) > dataframe['bb_upperband'].shift(2)) &
(dataframe['high'].shift(3) > dataframe['bb_upperband'].shift(3)) &
(dataframe['high'].shift(4) > dataframe['bb_upperband'].shift(4)) &
(dataframe['high'].shift(5) > dataframe['bb_upperband'].shift(5)) &
(dataframe['high'].shift(6) > dataframe['bb_upperband'].shift(6)) &
(dataframe['volume'] > 0)
```

> **Hyperoptable Change**: Exit condition thresholds may be micro-adjusted after optimization.

**Combined Logic**: When price stays above the Bollinger Band upper rail for 6 consecutive 5-minute candles, trigger a sell.

### 4.4 Custom Stop-Loss Logic

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    if (current_time - timedelta(minutes=300) > trade.open_date_utc) & (current_profit < 0):
        return 0.01
    return 0.99
```

**Special Handling**: If held for more than **300 minutes (5 hours)** and still in loss, force market exit.

---

## V. Risk Management Features

### 5.1 Multi-Layer Risk Control System

1. **Fixed Stop-Loss**: -99% nearly disabled
2. **Time Stop-Loss**: Force exit at market if still in loss after 5 hours
3. **Trailing Stop**: Activate 1.25% trailing when profit exceeds 2.75%
4. **Take-Profit Threshold**: 2.0% cumulative return triggers automatic take-profit

> **Hyperoptable Core Design**: Parameters optimized for specific market environments, further improving strategy performance on top of V5.

---

## VI. Strategy Pros & Cons

### ✅ Pros

1. **Dual-Factor Complementarity**: BinHV45 + ClucMay72018, broader adaptability
2. **Hyperparameter Optimization**: Automated search finds better parameter configurations for target markets
3. **More Precise Tuning**: Hyperoptable version optimized for specific trading pairs or market environments
4. **Clear Signals**: Entry conditions specific and quantifiable

### ⚠️ Cons

1. **5-Minute Period Noise**: High-frequency trading generates frequent costs
2. **Overfitting Risk**: Hyperoptable version has historical backtest overfitting risk, may underperform in live trading
3. **Volatility-Dependent**: Mean reversion, performs limitedly in trending markets
4. **Parameter Generalizability**: Optimized parameters may only apply to specific markets, performance may drop on different markets
5. **Loose Stop-Loss Design**: -99% nearly disabled, may endure large floating losses

---

## VII. Applicable Scenarios

### ✅ Recommended
- **Sideways Markets**: Price fluctuates around Bollinger Band rails
- **High-Volatility Pairs**: High volatility more easily triggers conditions
- **Trend Continuation**: Optimized parameters better suit trend pullback entries
- **Optimized Specific Trading Pairs**: Hyperopted for specific pairs

### ❌ Not Recommended
- **One-Directional Uptrend**: May sell too early
- **One-Directional Downtrend**: Time stop-loss triggers repeatedly
- **Non-Optimized New Trading Pairs**: Parameters optimized for specific pairs, may not work on new pairs
- **Long-Term Investment**: 5-minute timeframe unsuitable

---

## VIII. Summary

CombinedBinHAndClucV5Hyperoptable is a **hyperparameter-optimized hybrid mean reversion strategy** combining BinHV45 and ClucMay72018.

**Hyperoptable Version's Core Features**:
- Hyperparameter automated search optimization, parameters finely tuned for specific markets
- Retains V5's 2.0% take-profit and trailing stop design (2.75% activation + 1.25% pullback)
- Has parameter overfitting risk, requires out-of-sample testing
- May outperform base version V5 in its optimized target markets

**Key Takeaways**:
- ✅ Suitable for sideways markets, oversold rebounds
- ✅ Hyperparameter optimized for specific markets
- ⚠️ Has parameter overfitting risk, requires out-of-sample testing
- ⚠️ Loose stop-loss, risk control relies on time stop-loss and trailing stop
- ⚠️ Parameter generalizability may be limited, re-validation needed for new markets
