# CombinedBinHAndClucHyperV0 Strategy Analysis

> **Strategy #**: #108 (8th in Batch 11)
> **Strategy Type**: Bollinger Bands + Dual Strategy Combination + Hyperparameter Optimization
> **Timeframe**: 1 Minute (1m)

---

## I. Strategy Overview

**CombinedBinHAndClucHyperV0** is a hyperparameter-optimized version of the CombinedBinHAndCluc series, developed by iterativ. The strategy combines **BinHV45** and **ClucMay72018**, two classic Bollinger Band trend strategies, using "OR gate" logic for buy signal composite filtering. Unlike the basic version, HyperV0 opens a large number of optimizable hyperparameters, allowing users to use Hyperopt to automatically find optimal parameter combinations.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 modes combined (BinHV45 OR ClucMay72018) |
| **Sell Conditions** | Price breaking Bollinger middle band |
| **Protection Mechanism** | Fixed stop-loss -10% + Trailing stop |
| **Timeframe** | 1 Minute |
| **Hyperparameter Count** | 12 optimizable parameters |
| **Dependencies** | TA-Lib, numpy, qtpylib, technical |
| **Special Features** | Custom stop-loss, slippage compensation calculation |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# Timeframe
timeframe = '1m'

# Sell Signal Settings
use_exit_signal = True
exit_profit_only = True
ignore_roi_if_entry_signal = False

# Stop-Loss Settings
stoploss = -0.1  # -10% hard stop-loss
trailing_stop = True  # Enable trailing stop
trailing_only_offset_is_reached = False
use_custom_stoploss = True  # Use custom stop-loss

# ROI Table (Profit targets at these levels)
minimal_roi = {
    "0": 0.10,    # Immediate exit: 10% profit
    "30": 0.05,   # After 30 minutes: 5% profit
    "60": 0.02    # After 60 minutes: 2% profit
}
```

**Design Philosophy**:
- **1-Minute Level**: Ultra short-term trading, capturing instant fluctuations.
- **10% Starting ROI**: Compared to 5-minute version, 1-minute needs larger fluctuation space.
- **Trailing Stop**: Locks in profits, leaves room for trending moves.
- **Staged ROI**: Progressively lowers profit expectations as time passes.

### 2.2 Optimized Entry Parameters

```python
buy_params = {
    # BinHV45 Mode Parameters
    'buy_a_bbdelta_rate': 0.0160,      # BB width threshold
    'buy_a_closedelta_rate': 0.0088,   # Price fluctuation threshold
    'buy_a_tail_rate': 0.9,            # Lower wick ratio
    'buy_a_time_window': 21,           # BB period
    'buy_a_min_sell_rate': 1.03,       # Sell threshold

    # ClucMay72018 Mode Parameters
    'buy_b_close_rate': 0.979,         # BB lower band ratio
    'buy_b_time_window': 20,           # BB period
    'buy_b_ema_slow': 50,              # EMA period
    'buy_b_volume_mean_slow_num': 20,  # Volume multiple
    'buy_b_volume_mean_slow_window': 30,  # Volume average period
}
```

### 2.3 Optimized Sell Parameters

```python
sell_params = {
    'sell_bb_middleband_window': 91,   # BB middle band period
    'sell_trailing_stop_positive_offset': 0.008,  # Trailing stop offset
}
```

---

## III. Entry Conditions Details

### 3.1 BinHV45 Mode (Entry Condition A)

**Trigger Conditions**:

```python
(
    # Previous candle's BB lower band exists
    dataframe[f'lower_{buy_a_time_window}'].shift().gt(0) &

    # BB width sufficient (> close × buy_a_bbdelta_rate)
    dataframe[f'bbdelta_{buy_a_time_window}'].gt(dataframe['close'] * buy_a_bbdelta_rate) &

    # Price fluctuation sufficient (> close × buy_a_closedelta_rate)
    dataframe[f'closedelta_{buy_a_time_window}'].gt(dataframe['close'] * buy_a_closedelta_rate) &

    # Lower wick short (< BB width × buy_a_tail_rate)
    dataframe[f'tail_{buy_a_time_window}'].lt(dataframe[f'bbdelta_{buy_a_time_window}'] * buy_a_tail_rate) &

    # Price breaks below previous BB lower band
    dataframe['close'].lt(dataframe[f'lower_{buy_a_time_window}'].shift()) &

    # Close not higher than previous close
    dataframe['close'].le(dataframe['close'].shift()) &

    # BB middle band above minimum sell price
    dataframe[f'bb_middleband_{sell_bb_middleband_window}'].gt(dataframe['close'] * buy_a_min_sell_rate)
)
```

**Logic Interpretation**:
1. **BB width verification**: Ensures sufficient market volatility space.
2. **Price fluctuation verification**: Filters sideways consolidation markets.
3. **Pattern verification**: Hammer pattern (short lower wick).
4. **Breakout verification**: Price breaks BB lower band support.
5. **Trend confirmation**: Close price weakening.
6. **Safety cushion verification**: BB middle band provides support protection.

### 3.2 ClucMay72018 Mode (Entry Condition B)

**Trigger Conditions**:

```python
(
    # Price below long-term MA (downtrend)
    (dataframe['close'] < dataframe[f'ema_slow_{buy_b_ema_slow}']) &

    # Price below BB lower band × buy_b_close_rate
    (dataframe['close'] < buy_b_close_rate * dataframe[f'bb_lowerband_{buy_b_time_window}']) &

    # Volume abnormally low (< avg × buy_b_volume_mean_slow_num)
    (dataframe['volume'] < (dataframe[f'volume_mean_slow_{buy_b_volume_mean_slow_window}'].shift(1) * buy_b_volume_mean_slow_num))
)
```

**Logic Interpretation**:
1. **Trend verification**: Price below EMA50, in downtrend.
2. **Support verification**: Price near or below BB lower band.
3. **Shrinking volume verification**: Volume extremely low, imminent reversal.

---

## IV. Exit Conditions Details

### 4.1 Technical Sell: BB Middle Band Breakout

```python
(dataframe['close'] > dataframe[f'bb_middleband_{sell_bb_middleband_window}'])
```

**Logic**: Triggers sell when price breaks above BB middle band. BB middle band period optimized to 91 (smoother than default 20).

### 4.2 ROI Take-Profit (Staged)

| Time | Profit Target |
|------|--------------|
| Immediate | 10% |
| After 30 minutes | 5% |
| After 60 minutes | 2% |

### 4.3 Custom Trailing Stop

```python
# Activates trailing stop when profit exceeds sell_trailing_stop_positive_offset
if current_profit_comp < sell_trailing_stop_positive_offset:
    return -1  # Don't trigger
else:
    return sell_trailing_stop_positive  # 0.001
```

**Special Feature**: Slippage compensation calculation — adjusts profit calculation based on difference between actual and expected fill prices.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator | Calculation Method | Function |
|-----------|-------------------|---------|
| **BB Middle Band** | 91-day SMA (optimizable) | Sell signal trigger line |
| **BB Lower Band** | N-day SMA - 2σ | Buy signal trigger line |
| **EMA50** | 50-day EMA (optimizable) | Trend judgment |
| **Volume Average** | 30-day volume average (optimizable) | Shrinking volume verification |

### 5.2 Custom Indicators (BinHV45 Mode)

| Indicator | Calculation Method | Function |
|-----------|-------------------|---------|
| **bbdelta** | \|middle - lower\| | BB width |
| **closedelta** | \|close - previous close\| | Price fluctuation magnitude |
| **tail** | \|close - low\| | Lower wick length |

### 5.3 Optimizable Parameters Summary

| Parameter | Default | Range | Function |
|-----------|---------|-------|----------|
| buy_a_bbdelta_rate | 0.016 | 0.004-0.016 | BB width threshold |
| buy_a_closedelta_rate | 0.0087 | 0.000-0.010 | Price fluctuation threshold |
| buy_a_tail_rate | 0.28 | 0.12-0.5 | Lower wick ratio |
| buy_a_time_window | 30 | 40-100 | BB period |
| buy_a_min_sell_rate | 1.004 | 1.004-1.1 | Sell threshold |
| buy_b_close_rate | 0.979 | 0.4-1.8 | BB lower band ratio |
| buy_b_volume_mean_slow_window | 30 | 100-300 | Volume period |
| buy_b_ema_slow | 50 | 40-100 | EMA period |
| buy_b_time_window | 20 | 100-300 | BB period |
| buy_b_volume_mean_slow_num | 20 | 10-100 | Volume multiple |
| sell_bb_middleband_window | 20 | 50-200 | Sell BB period |
| sell_trailing_stop_positive_offset | 0.008 | 0.01-0.03 | Trailing stop offset |

---

## VI. Risk Management Features

### 6.1 Stop-Loss Strategy

| Stop-Loss Type | Threshold | Description |
|---------------|-----------|-------------|
| **Hard Stop-Loss** | -10% | Forced liquidation at 10% loss |
| **Custom Stop-Loss** | Dynamic | Soft stop with slippage compensation |

### 6.2 Take-Profit Strategy

| Take-Profit Type | Threshold | Description |
|-----------------|-----------|-------------|
| **ROI Take-Profit** | 10%/5%/2% | Staged exit |
| **Trailing Stop** | 0.8% activation | Locks profits |

### 6.3 Slippage Compensation Mechanism

```python
# Calculate slippage ratio
slippage_ratio = trade.open_rate / trade_candle['close'] - 1
slippage_ratio = max(slippage_ratio, 0)

# Adjusted profit
current_profit_comp = current_profit + slippage_ratio
```

**Function**: More accurately calculates actual profit, avoids false trailing stop triggers caused by slippage.

---

## VII. Strategy Pros & Cons

### 7.1 Pros

1. **Hyperparameter Optimizable**: 12 parameters can be automatically optimized via Hyperopt.
2. **Dual Strategy Combination**: Two independent strategies complement each other, improving reliability.
3. **Slippage Compensation**: Custom stop-loss considers trading slippage.
4. **Trailing Stop**: Locks profits while leaving room for trending moves.
5. **1-Minute Level**: Suitable for high-volatility short-term operations.
6. **Staged ROI**: Adapts profit expectations to different holding durations.

### 7.2 Cons

1. **Parameter Sensitive**: Large number of hyperparameters may cause overfitting.
2. **1-Minute Noise**: High-frequency trading signals have higher noise.
3. **Trend Adaptability**: May fail in strong trending markets.
4. **High Complexity**: Requires understanding two sub-strategy logics.
5. **Backtesting Requirements**: Needs longer backtesting periods to verify.

---

## VIII. Applicable Scenarios

### 8.1 Recommended Scenarios

| Scenario | Description |
|----------|-------------|
| **High-Frequency Trading** | 1-minute level captures instant fluctuations |
| **Volatile Market** | BB convergence breakout after volatility |
| **Ultra-Short Operations** | Fast entry/exit swing trading |
| **Parameter Optimization** | Want to optimize parameters via Hyperopt |
| **Multi-Coin Allocation** | Run multiple trading pairs simultaneously |

### 8.2 Not Recommended Scenarios

| Scenario | Description |
|----------|-------------|
| **Long-Term Investment** | 1-minute level not suitable for long-term |
| **Low-Fee Coins** | High-frequency trading needs low fees |
| **Low-Volatility Market** | BB narrow, signals scarce |
| **Risk Averse** | 10% stop-loss relatively large |

---

## IX. Summary

**CombinedBinHAndClucHyperV0** is a version specifically designed for hyperparameter optimization in the CombinedBinHAndCluc series. By opening 12 adjustable parameters, it allows users to find optimal configurations based on specific market environments. The strategy combines BinHV45's pattern recognition and ClucMay72018's shrinking volume rebound logic, providing a complete high-frequency trading framework at the 1-minute level with custom trailing stop and slippage compensation.

**Core Points**:
- ✅ 12 hyperparameter optimizable, strong adaptability.
- ✅ Dual strategy combination, improves signal reliability.
- ✅ Custom stop-loss with slippage compensation, more precise.
- ✅ Trailing stop locks profits.
- ⚠️ High parameter complexity, overfitting risk.
- ⚠️ 1-minute level has high execution requirements.
- ⚠️ Needs low-fee environment.

**Usage Suggestions**:
- Beginners should first run with default parameters until stable, then optimize.
- Experienced users can use Hyperopt to find optimal parameters.
- Ensure trading fees are low enough (< 0.1%).
- Suggest forming combinations with other strategies to reduce single-strategy risk.
- Must conduct sufficient testing before live trading.
