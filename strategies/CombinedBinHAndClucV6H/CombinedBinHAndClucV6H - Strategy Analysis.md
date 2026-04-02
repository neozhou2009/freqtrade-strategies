# CombinedBinHAndClucV6H Strategy Analysis

> **Strategy Number**: #120 (Batch 12, 120th Strategy)
> **Strategy Type**: Multi-Factor Mean Reversion · Oversold Rebound Strategy (Hyperparameter-Optimized Version)
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

CombinedBinHAndClucV6H is a **multi-factor mean reversion** trading strategy—the **hyperparameter-optimized version** of V6. It combines BinHV45 and ClucMay72018 signal logic and has been through hyperparameter automated search optimization to more precisely capture oversold rebound opportunities in specific market environments.

The core idea is: **when price deviates from the lower Bollinger Band and shows a clear contracting pattern, it is identified as a potential mean reversion signal.** Volume filtering and EMA200 trend judgment reduce false breakout probability. The Hyperoptable version further optimizes parameters based on V6.

**V6H vs V6 Core Optimization**:
- Hyperparameter automated search optimization finds better parameter combinations for target trading pairs
- Take-profit maintained at 2.2%
- Trailing stop activation starts from 3.0%, fine-tuned through optimization
- Trailing stop pullback from 1.5%, fine-tuned through optimization
- Exit confirmation maintained at 7 consecutive candles
- EMA200 trend filter retained, preventing chasing rally highs

---

## II. Strategy Configuration Analysis

### 2.1 Basic Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `timeframe` | 5m | 5-minute candles |
| `minimal_roi` | {"0": 0.022} | Take-profit at 2.2% cumulative return |
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
| `trailing_stop_positive` | 0.015 | Trailing stop distance 1.5% |
| `trailing_stop_positive_offset` | 0.03 | Activate trailing when profit reaches 3.0% |

> **V6H Key Change**: Retains V6's 2.2% take-profit, 3.0% trailing activation, 1.5% pullback design—parameters further refined through hyperparameter optimization.

---

## III. Entry Conditions Details

### 3.1 Condition One: BinHV45 Strategy (Rapid Sell-off Rebound)

```python
(dataframe['lower'].shift().gt(0) &
 dataframe['bbdelta'].gt(dataframe['close'] * 0.008) &
 dataframe['closedelta'].gt(dataframe['close'] * 0.0175) &
 dataframe['tail'].lt(dataframe['bbdelta'] * 0.25) &
 dataframe['close'].lt(dataframe['lower'].shift()) &
 dataframe['close'].le(dataframe['close'].shift()) &
 (dataframe['volume'] > 0))
```

**Combined Logic**: Price drops rapidly and pierces the lower Bollinger Band with sufficient volatility and a short lower wick—typical **oversold rebound** pattern.

### 3.2 Condition Two: ClucMay72018 Strategy (Volume-Shrinking Oversold)

```python
((dataframe['close'] < dataframe['ema_slow']) &
 (dataframe['close'] < 0.985 * dataframe['bb_lowerband']) &
 (dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 20)) &
 (dataframe['volume'] > 0))
```

**Combined Logic**: In a downtrend, price rapidly breaks below the lower Bollinger Band, but volume does not expand—downward momentum is insufficient.

### 3.3 Condition Three: EMA200 Trend Confirmation (V6H Retained Filter)

```python
(dataframe['close'] < dataframe['ema200'] * 1.05) &
(dataframe['volume'] > 0)
```

**Combined Logic**: V6H retains EMA200 trend filter, ensuring price hasn't deviated significantly from EMA200, avoiding entry at extreme rally highs.

### 3.4 Entry Signal Trigger Rules

The three conditions have an **OR relationship**—meeting any one generates a buy signal. V6H adds hyperparameter optimization on V6's foundation, making signals more precise.

---

## IV. Exit Conditions Details

### 4.1 Take-Profit Logic

- Take-profit triggers when cumulative return reaches **2.2%**
- `exit_profit_only = True` ensures selling only in profitable state
- `exit_profit_offset = 0.001` requires profit to exceed 0.1%

> **V6H Trait**: Retains V6's 2.2% take-profit target, parameters further refined through optimization.

### 4.2 Trailing Stop Logic

When open profit reaches **3.0%**, trailing stop activates:
- Stop-loss line moves up, locking in at least **1.5%** of profit
- If price continues to rise, the stop-loss line follows

> **V6H Key Change**: Retains V6's design philosophy (3.0% activation + 1.5% pullback), further refined through hyperparameter optimization.

### 4.3 Exit Signal Conditions

```python
(dataframe['close'] > dataframe['bb_upperband']) &
(dataframe['close'].shift(1) > dataframe['bb_upperband'].shift(1)) &
(dataframe['high'].shift(2) > dataframe['bb_upperband'].shift(2)) &
(dataframe['high'].shift(3) > dataframe['bb_upperband'].shift(3)) &
(dataframe['high'].shift(4) > dataframe['bb_upperband'].shift(4)) &
(dataframe['high'].shift(5) > dataframe['bb_upperband'].shift(5)) &
(dataframe['high'].shift(6) > dataframe['bb_upperband'].shift(6)) &
(dataframe['high'].shift(7) > dataframe['bb_upperband'].shift(7)) &
(dataframe['volume'] > 0)
```

> **V6H Retained**: 7 consecutive candles breaking upper rail strict exit condition, more robust after optimization.

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
3. **Trailing Stop**: Activate 1.5% trailing when profit exceeds 3.0%
4. **Take-Profit Threshold**: 2.2% cumulative return triggers automatic take-profit
5. **EMA200 Trend Filter**: Ensures buying at reasonable trend levels

> **V6H Core Design**: Further refined parameters on V6's foundation through hyperparameter optimization, retaining the "let profits run" philosophy.

---

## VI. Strategy Pros & Cons

### ✅ Pros

1. **Three-Factor Complementarity**: BinHV45 + ClucMay72018 + EMA200 trend filter, broadest adaptability
2. **Hyperparameter Optimization**: Automated search finds better parameters for target markets
3. **V6H More Precise Parameters**: Further refined on V6's foundation, more suited to specific markets
4. **Higher Take-Profit Target**: 2.2%, pursuing higher per-trade returns
5. **EMA200 Trend Filter**: Avoids chasing rally highs, V6H retains this trait
6. **Stricter Exits**: 7 consecutive candles, fewer false breakouts
7. **Clear Signals**: Entry conditions specific and quantifiable

### ⚠️ Cons

1. **5-Minute Period Noise**: High-frequency trading generates frequent costs
2. **Overfitting Risk**: V6H has historical backtest overfitting risk, may underperform in live trading
3. **Volatility-Dependent**: Mean reversion, performs limitedly in trending markets
4. **Parameter Generalizability**: Optimized parameters may only apply to specific markets
5. **Loose Stop-Loss Design**: -99% nearly disabled, may endure large floating losses
6. **V6H More "Greedy"**: 2.2% take-profit harder to reach in sideways markets

---

## VII. Summary

CombinedBinHAndClucV6H is a **hyperparameter-optimized hybrid mean reversion strategy** combining BinHV45 and ClucMay72018, with an EMA200 trend filter, further optimized through hyperparameter automated search.

**V6H's Core Upgrades**:
- Hyperparameter automated search on V6's foundation, parameters more refined
- Retains 2.2% take-profit, 3.0% trailing activation, 1.5% pullback
- Retains EMA200 trend filter
- Has parameter overfitting risk, requires out-of-sample testing

This strategy performs excellently in **high-volatility sideways markets**, **trend continuation/pullback markets**, and **optimized specific market environments**. The loose stop-loss design and overfitting risk require strong risk management ability.

**Key Takeaways**:
- ✅ Suitable for sideways markets, oversold rebounds
- ✅ Hyperparameter optimized for specific markets
- ✅ V6H retains EMA200 trend filter, pullback entries more robust
- ⚠️ Has parameter overfitting risk, requires out-of-sample testing
- ⚠️ Loose stop-loss, risk control relies on time stop-loss and trailing stop
- ⚠️ Poor performance in one-directional drops
