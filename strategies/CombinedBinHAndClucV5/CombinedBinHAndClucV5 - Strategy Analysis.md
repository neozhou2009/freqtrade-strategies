# CombinedBinHAndClucV5 Strategy Analysis

> **Strategy Number**: #117 (Batch 12, 117th Strategy)
> **Strategy Type**: Multi-Factor Mean Reversion · Oversold Rebound Strategy
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

CombinedBinHAndClucV5 is a **multi-factor mean reversion** trading strategy that combines the signal logic of two classic strategies—**BinHV45** and **ClucMay72018**—to capture oversold rebound opportunities in sideways markets.

The core idea is: **when price deviates from the lower Bollinger Band due to short-term volatility and shows a clear contracting pattern, it is identified as a potential mean reversion signal.** Volume filtering and EMA trend judgment are used to reduce false breakout probability.

The strategy runs on a **5-minute** short-term timeframe by default, emphasizing fast entry and exit.

**V5's Core Upgrade over V4**:
- Take-profit threshold raised from 1.9% to 2.0%, pursuing higher per-trade returns
- Trailing stop activation threshold raised from 2.5% to 2.75%, giving trends more room to develop
- Trailing stop pullback depth deepened from 1% to 1.25%, avoiding being shaken out by short-term pullbacks
- Exit signal changed from 5 consecutive candles to 6 consecutive candles breaking the upper rail, reducing false breakout interference

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

> **V5 Key Change**: Trailing stop activation raised from V4's 2.5% to 2.75%, pullback depth deepened from 1% to 1.25%, giving trends more room.

### 2.3 Order Types

```python
order_types = {
    'entry': 'limit',    # Limit order entry
    'exit': 'limit',     # Limit order exit
    'stoploss': 'market' # Stop-loss uses market order
}
```

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
| `bbdelta > close * 0.008` | Channel width at least 0.8% of price, ensuring sufficient volatility |
| `closedelta > close * 0.0175` | Closing price differs from previous close by more than 1.75% |
| `tail < bbdelta * 0.25` | Lower wick less than 25% of channel width, close near the day's low |
| `close < lower.shift()` | Close breaks below the previous day's lower Bollinger Band |
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
| `close < ema_slow` | Price below the 50-day EMA, confirming medium-term downtrend |
| `close < 0.985 * bb_lowerband` | Price clearly below Bollinger Band lower rail |
| `volume < volume_mean_slow.shift(1) * 20` | Volume less than 20x the 30-day average (abnormally shrunken) |
| `volume > 0` | Exclude zero-volume abnormal candles |

**Combined Logic**: In a downtrend, price rapidly breaks below the lower Bollinger Band, but volume does not expand—downward momentum is insufficient, a corrective rebound may come.

### 3.3 Entry Signal Trigger Rules

The two conditions have an **OR relationship**—meeting either one generates a buy signal.

---

## IV. Exit Conditions Details

### 4.1 Take-Profit Logic

- Take-profit triggers when cumulative return reaches **2.0%**
- `exit_profit_only = True` ensures selling only in profitable state
- `exit_profit_offset = 0.001` requires profit to exceed 0.1%

> **V5 Change**: Take-profit raised from V4's 1.9% to 2.0%.

### 4.2 Trailing Stop Logic

When open profit reaches **2.75%** (`trailing_stop_positive_offset`), trailing stop activates:

- Stop-loss line moves up, locking in at least **1.25%** of profit
- If price continues to rise, the stop-loss line follows
- If price drops back to touch the trailing stop line, close at market price

> **V5 Key Change**: Activation threshold raised from 2.5% to 2.75%, pullback depth deepened from 1% to 1.25%—strategy is bolder, giving trends more room.

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

> **V5 Change**: Changed from 5 consecutive candles to 6 consecutive candles breaking the upper rail.

**Combined Logic**: When price stays above the Bollinger Band upper rail for 6 consecutive 5-minute candles, trigger a sell.

### 4.4 Custom Stop-Loss Logic

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    if (current_time - timedelta(minutes=300) > trade.open_date_utc) & (current_profit < 0):
        return 0.01
    return 0.99
```

**Special Handling**:
- If held for more than **300 minutes (5 hours)** and still in loss, force market exit
- Purpose: prevent floating losses from expanding while giving trends more room

---

## V. Technical Indicator System

### 5.1 Bollinger Band Indicators

| Indicator | Calculation | Purpose |
|-----------|-------------|---------|
| `mid` / `lower` | Custom Bollinger Bands (40, 2) | Core indicator for BinHV45 |
| `bbdelta` | `\|mid - lower\|` | Bollinger Band channel width |
| `bb_lowerband` | qtpylib.bollinger_bands (20, 2) | Bollinger Band used by Cluc |
| `bb_middleband` | Bollinger Band middle rail | Trend reference |
| `bb_upperband` | Bollinger Band upper rail | Sell signal trigger |

### 5.2 Moving Average Indicators

| Indicator | Period | Purpose |
|-----------|--------|---------|
| `ema_slow` | 50 | Judge medium-term trend direction |

### 5.3 Volatility Indicators

| Indicator | Formula | Meaning |
|-----------|---------|---------|
| `closedelta` | `\|close - close.shift(1)\|` | Intraday closing price volatility |
| `tail` | `\|close - low\|` | Lower wick length |

### 5.4 Volume Indicators

| Indicator | Period | Purpose |
|-----------|--------|---------|
| `volume_mean_slow` | 30 | Volume moving average for volume-shrinking filter |

---

## VI. Risk Management Features

### 6.1 Multi-Layer Risk Control System

1. **Fixed Stop-Loss**: -99% nearly disabled, relies on other risk controls
2. **Time Stop-Loss**: Force exit at market if still in loss after 5 hours
3. **Trailing Stop**: Activate 1.25% trailing when profit exceeds 2.75%
4. **Take-Profit Threshold**: 2.0% cumulative return triggers automatic take-profit

> **V5 Core Design Philosophy**: Further "loosening" on V4's foundation, giving trends more room while using time stop-loss to prevent long floating losses.

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Dual-Factor Complementarity**: BinHV45 + ClucMay72018, broader adaptability
2. **V5 Optimized Trend Space**: Trailing stop at 2.75%, pullback depth 1.25%, trends won't shake you out easily
3. **V5 Higher Take-Profit**: From 1.9% to 2.0%, higher per-trade returns
4. **V5 Stricter Exit**: 6 consecutive candles before selling, fewer false breakouts
5. **Clear Signals**: Entry conditions specific and quantifiable

### ⚠️ Cons

1. **5-Minute Period Noise**: High-frequency trading generates frequent costs
2. **V5 More "Greedy"**: 2.0% take-profit harder to reach in sideways markets
3. **Volatility-Dependent**: Mean reversion, performs limitedly in trending markets
4. **V5 Stricter Exit**: 6 consecutive candles may miss optimal exit
5. **V5 Loose Stop-Loss**: -99% nearly disabled, may endure large floating losses in extreme drops

---

## VIII. Applicable Scenarios

### ✅ Recommended
- **Sideways Markets**: Price fluctuates around Bollinger Band rails
- **High-Volatility Pairs**: High volatility more easily triggers conditions
- **Trend Continuation**: V5's loose design suits pullback entries
- **Trend Following**: V5 optimized trailing parameters, can "eat" more of the trend

### ❌ Not Recommended
- **One-Directional Uptrend**: May sell too early (but V5 has optimized)
- **One-Directional Downtrend**: Time stop-loss triggers repeatedly
- **Low-Volatility Markets**: Entry conditions hard to meet
- **Long-Term Investment**: 5-minute timeframe unsuitable

---

## IX. Summary

CombinedBinHAndClucV5 is a **hybrid mean reversion strategy** combining BinHV45 and ClucMay72018.

**V5's Core Upgrades**:
- Take-profit raised from 1.9% to 2.0%
- Trailing stop activation raised from 2.5% to 2.75%, pulling back deeper to 1.25%
- Exit conditions changed from 5 to 6 consecutive candles

This strategy performs excellently in **high-volatility sideways markets** and **trend continuation markets**. The loose stop-loss design requires strong risk management.

**Key Takeaways**:
- ✅ Suitable for sideways markets, oversold rebounds
- ✅ V5 optimized for trend continuation, pursuing higher returns
- ⚠️ Loose stop-loss, risk control relies on time stop-loss and trailing stop
- ⚠️ High-frequency trading, costs need close attention
- ⚠️ Poor performance in one-directional drops
