# CombinedBinHAndClucHyperV3 Strategy Analysis

> **Strategy #**: #109 (109th of 465 strategies)
> **Strategy Type**: Dual Strategy Combination + Hyperparameter Optimization + Dynamic Take-Profit
> **Timeframe**: 1 Minute (1m)

---

## I. Strategy Overview

CombinedBinHAndClucHyperV3 is a fused quantitative trading strategy that combines the entry logics of **BinHV45** and **ClucMay72018** to achieve multi-dimensional signal verification. The "HyperV3" designation indicates this is a third-version hyperparameter optimization (Hyperopt) version with enhanced market adaptability.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signals (BinHV45 + ClucMay72018), logically independent but can trigger simultaneously |
| **Sell Conditions** | 1 basic sell signal + dynamic trailing stop mechanism |
| **Protection Mechanisms** | Custom stop-loss + trailing stop + slippage compensation |
| **Timeframe** | 1 Minute (high-frequency trading) |
| **Dependencies** | talib.abstract, technical (qtpylib), numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,      # Exit at 10% profit within 0-30 minutes
    "30": 0.05,     # Exit at 5% profit within 30-60 minutes
    "60": 0.02,     # Exit at 2% profit after 60 minutes
}

# Stop-Loss Settings
stoploss = -0.06   # Fixed stop-loss: -6%

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = False
use_custom_stoploss = True
```

**Design Philosophy**:
- **ROI Staged Design**: Uses "front-heavy, back-light" staircase take-profit. Locks in profits quickly within 30 minutes at 10%, consistent with high-frequency "small wins accumulate" philosophy.
- **Fixed Stop-Loss -6%**: Relatively loose stop-loss, giving price some fluctuation space, avoiding being stopped out by market noise.
- **Custom Trailing Stop**: Dynamic take-profit via `custom_stoploss`, activates when profit exceeds `sell_trailing_stop_positive_offset`.

### 2.2 Order Type Configuration

```python
use_exit_signal = True           # Enable sell signal
exit_profit_only = True          # Sell only when profitable (avoid cutting losses)
ignore_roi_if_entry_signal = False  # Don't ignore ROI forced exit
```

---

## III. Entry Conditions Details

### 3.1 Protection Mechanism Parameter Groups

| Protection Type | Description | Default |
|---------------|-------------|---------|
| buy_a_time_window | BB period parameter | 30 |
| buy_a_atr_window | ATR volatility window | 14 |
| buy_a_bbdelta_rate | BB delta threshold | 0.014 |
| buy_a_closedelta_rate | Close price change rate threshold | 0.004 |
| buy_a_tail_rate | Lower wick ratio threshold | 0.47 |
| buy_a_min_sell_rate | Minimum sell price ratio | 1.062 |
| buy_a_atr_rate | ATR volatility ratio | 0.26 |

### 3.2 Entry Conditions Details

#### Condition #1: BinHV45 Strategy Entry Logic

```python
# Core Logic
(
    dataframe[f'lower_{buy_a_time_window}'].shift().gt(0) &
    dataframe[f'bbdelta_{buy_a_time_window}'].gt(dataframe['close'] * buy_a_bbdelta_rate) &
    dataframe[f'closedelta_{buy_a_time_window}'].gt(dataframe['close'] * buy_a_closedelta_rate) &
    dataframe[f'tail_{buy_a_time_window}'].lt(dataframe[f'bbdelta_{buy_a_time_window}'] * buy_a_tail_rate) &
    dataframe['close'].lt(dataframe[f'lower_{buy_a_time_window}'].shift()) &
    dataframe['close'].le(dataframe['close'].shift()) &
    dataframe[f'bb_typical_mid_{sell_bb_mid_slow_window}'].gt(
        dataframe['close'] * (buy_a_min_sell_rate + dataframe[f'atr_rate_{buy_a_atr_window}'] * buy_a_atr_rate)
    )
)
```

**Logic Breakdown**:
1. **BB Lower Band Support**: Current price breaks below BB lower band.
2. **BB Opening**: bbdelta (difference between BB middle and lower) sufficient, volatility expanding.
3. **Close Price Fluctuation**: closedelta sufficient.
4. **Lower Wicking Feature**: tail (lower wick) less than specified ratio of bbdelta, price rebounds quickly.
5. **Continuous Decline**: Current close ≤ previous close (continuous adjustment pattern).
6. **Dynamic Sell Threshold**: ATR volatility dynamically adjusts minimum sell point when buying.

#### Condition #2: ClucMay72018 Strategy Entry Logic

```python
# Core Logic
(
    (dataframe['close'] < dataframe[f'ema_slow_{buy_b_ema_slow}']) &
    (dataframe['close'] < buy_b_close_rate * dataframe[f'bb_typical_lower_{buy_b_time_window}']) &
    (dataframe['volume'] < (dataframe[f'volume_mean_slow_{buy_b_volume_mean_slow_window}'].shift(1) * buy_b_volume_mean_slow_num))
)
```

**Logic Breakdown**:
1. **Price below EMA**: Close below slow EMA (trend downward).
2. **Price below BB Lower Band**: Close below specified ratio of BB lower band.
3. **Shrinking Volume Buy**: Current volume below specified multiple of average (buy on dips).

### 3.3 Entry Conditions Summary

| Condition Group | Condition # | Core Logic | Source |
|----------------|------------|-----------|--------|
| Volatility Breakout | #1 | BB opening + price breaks lower band + wick rebound | BinHV45 |
| Shrinking Volume Rebound | #2 | Price below EMA + breaks BB lower band + volume shrinks | ClucMay72018 |

---

## IV. Exit Conditions Details

### 4.1 Trailing Take-Profit Mechanism

The strategy uses a custom `custom_stoploss` function to implement trailing take-profit:

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    # Calculate slippage compensation
    slippage_ratio = trade.open_rate / trade_candle['close'] - 1
    current_profit_comp = current_profit + slippage_ratio

    # Trigger: profit exceeds sell_trailing_stop_positive_offset
    if current_profit_comp < sell_trailing_stop_positive_offset:
        return -1    # Don't trigger, continue holding
    else:
        return sell_trailing_stop_positive  # Trigger trailing stop
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| sell_trailing_stop_positive_offset | 0.014 (1.4%) | Activates trailing when profit exceeds 1.4% |
| sell_trailing_stop_positive | 0.001 (0.1%) | Trailing stop range |

### 4.2 Basic Sell Signal

```python
# Sell Signal: Price breaks BB middle band
dataframe.loc[
    (dataframe['close'] > dataframe[f'bb_typical_mid_{sell_bb_mid_slow_window}']),
    'sell'
] = 1
```

**Logic Explanation**: Triggers sell when close price breaks above BB middle band, representing price reverting from oversold to normal.

### 4.3 Multi-Layer Take-Profit System

| Take-Profit Layer | Trigger Condition | Take-Profit Method |
|-----------------|------------------|-------------------|
| Fast Take-Profit | 0-30 minutes, profit ≥10% | ROI forced exit |
| Medium Take-Profit | 30-60 minutes, profit ≥5% | ROI exit |
| Conservative Take-Profit | 60+ minutes, profit ≥2% | ROI exit |
| Trailing Take-Profit | Profit ≥1.4% (incl. slippage) | Trailing stop exit |
| Middle Band Take-Profit | Price breaks BB middle | Signal exit |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Trend Indicator** | EMA(50) | Auxiliary price relative position judgment |
| **Volatility Indicator** | ATR(14) | Calculate dynamic sell threshold and volatility |
| **Bollinger Bands** | BB(20), BB(30), BB(91) | Judge oversold/overbought, generate buy/sell signals |
| **Volume** | Volume MA(30) | Identify shrinking volume rebound opportunities |

### 5.2 Custom Calculated Indicators

| Indicator | Formula | Purpose |
|-----------|---------|---------|
| bbdelta | mid - lower (absolute) | Measures BB opening width |
| closedelta | close - close.shift() (absolute) | Measures close price fluctuation |
| tail | close - low (absolute) | Measures lower wick length |
| bb_typical_mid | BB(typical_price) middle | Typical price BB middle band |
| bb_typical_lower | BB(typical_price) lower | Typical price BB lower band |
| atr_rate | ATR / close | Normalized volatility |

### 5.3 Informative Timeframe

This strategy focuses on 1-minute high-frequency trading and does not use additional informative timeframes. All indicators are calculated within the 1-minute timeframe.

---

## VI. Risk Management Features

### 6.1 Slippage Compensation Mechanism

```python
# Calculate open position slippage impact
slippage_ratio = trade.open_rate / trade_candle['close'] - 1
slippage_ratio = slippage_ratio if slippage_ratio > 0 else 0
current_profit_comp = current_profit + slippage_ratio
```

**Design Purpose**: In high-frequency trading, slippage significantly impacts profitability. This mechanism ensures profit calculation considers the difference between actual and quoted fill prices, avoiding premature take-profit triggers.

### 6.2 Dynamic Trailing Take-Profit

- **Activation Condition**: Profit exceeds 1.4% (including slippage).
- **Trailing Range**: 0.1%.
- **Advantage**: Protects profits while leaving room for market development.

### 6.3 Staged ROI Take-Profit

| Time Period | Minimum Profit Requirement | Design Philosophy |
|------------|--------------------------|------------------|
| 0-30 minutes | 10% | Capture profits quickly, reduce holding time |
| 30-60 minutes | 5% | Medium holding, wait for trend continuation |
| 60+ minutes | 2% | Long holding, exit on small profit |

---

## VII. Strategy Pros & Cons

### Pros

1. **Multi-Strategy Fusion**: Combines BinHV45 and ClucMay72018 entry logics, improving signal reliability.
2. **Hyperparameter Optimization**: Third-version Hyperopt tuning, parameters validated on historical data.
3. **Slippage Compensation**: Innovatively considers slippage in trailing take-profit, more accurately reflecting true profit.
4. **Staged Take-Profit**: ROI table well-designed, balancing fast profit capture and trend tracking.
5. **Strong Adaptability**: Two independent entry conditions complement each other across different market environments.

### Cons

1. **Timeframe Limitation**: 1-minute high-frequency trading sensitive to execution delay, live results may be affected by exchange API latency.
2. **Parameter Overfitting Risk**: Multiple hyperparameters may perform well on historical data but have questionable future adaptability.
3. **Trading Cost Sensitive**: 10% ROI threshold may significantly reduce actual returns after deducting fees.
4. **BB Parameter Sensitive**: Different trading pairs may need different BB period settings.

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|--------------------|--------------------------|-------------|
| **High-Volatility Coins** | max_open_trades=2, stake_amount moderate | High volatility means more trading opportunities |
| **Mainstream Coins** | BTC/ETH, high liquidity | Controllable slippage |
| **Short-Term Operations** | Intraday trading-oriented investors | Strategy designed for high-frequency |
| **Trending Markets** | Use with trend indicators | BB strategies perform better in trends |

---

## IX. Applicable Market Environment Details

CombinedBinHAndClucHyperV3 is positioned as a **high-frequency breakout** combination strategy in the Freqtrade ecosystem. Based on its code architecture and dual-strategy fusion, it is best suited for **high-volatility volatile markets** and may perform poorly in **sustained unilateral decline** environments.

### 9.1 Core Strategy Logic

- **Breakout Entry**: BinHV45 logic seeks rebound opportunities after price rapidly breaks BB lower band.
- **Shrinking Volume Buy**: ClucMay72018 logic buys on dips during shrinking volume.
- **Middle Band Exit**: Exit when price reverts to BB middle band.
- **Dynamic Protection**: ATR volatility dynamically adjusts buy thresholds.

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| Trending Uptrend | ⭐⭐⭐⭐☆ | BB strategies capture pullback buy opportunities in uptrends |
| Volatile Market | ⭐⭐⭐⭐⭐ | Most suitable environment, price oscillates between BB upper/lower bands |
| Sustained Decline | ⭐⭐☆☆☆ | Buy signals may appear during downtrend continuations, requires strict stop-loss |
| Extreme Volatility | ⭐⭐⭐⭐☆ | ATR dynamic adjustment adapts to high volatility, but watch slippage |

---

## X. Summary

CombinedBinHAndClucHyperV3 is a **fused high-frequency breakout strategy**. Its core value:

1. **Dual Strategy Complement**: BinHV45 captures volatility breakouts, ClucMay72018 captures shrinking volume pullbacks.
2. **Hyperparameter Optimization**: V3 version tuning, parameters validated on historical data.
3. **Fine-Grained Risk Control**: Slippage compensation + trailing take-profit + staged ROI.

For quantitative traders, this strategy is suitable for users with high-frequency trading experience, familiar with Bollinger Band technical analysis, and able to execute in low-latency environments. Average investors should start with default parameters and verify fully in paper trading before going live gradually.
