# ClucHAnix_hhll Strategy Analysis

> **Strategy #**: #101 (101st of 465 strategies)
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Bands Mean Reversion + Protection Mechanisms
> **Timeframe**: 5 Minutes (5m) + 1-Hour Informative Layer

---

## I. Strategy Overview

ClucHAnix_hhll is a complex trend-following strategy based on Heikin Ashi candle patterns and Bollinger Bands mean reversion principles. The strategy combines multiple technical indicators to identify potential reversal points and trend continuation signals, suitable for operation in moderately volatile market environments. The "Cluc" in the name derives from the "Cluc" series, while "hhll" stands for its unique "Highest-High / Lowest-Low" filtering mechanism.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signal paths, both requiring 1-hour ROCR filtering |
| **Sell Conditions** | 3 basic sell signals + multi-layer dynamic take-profit logic + special scenario stop-loss |
| **Protection Mechanisms** | 1 set of slippage protection parameters |
| **Timeframe** | Main 5m + Informative 1h |
| **Dependencies** | technical, talib, numpy, pandas |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.103,     # Immediate exit yields 10.3% profit
    "3": 0.05,      # Profit drops to 5% after 3 minutes
    "5": 0.033,     # Profit drops to 3.3% after 5 minutes
    "61": 0.027,    # Profit drops to 2.7% after 1 hour
    "125": 0.011,   # Profit drops to 1.1% after ~2 hours
    "292": 0.005,   # Profit drops to 0.5% after ~5 hours
}

# Stop-Loss Settings
stoploss = -0.99  # Uses custom stop-loss; fixed stop fully relies on custom_stoploss

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.001
trailing_stop_positive_offset = 0.012
trailing_only_offset_is_reached = False
```

**Design Philosophy**:
- **ROI Table Design**: Uses a "heavy-front, light-back" gradient approach — expecting higher profits early (10.3%), gradually lowering profit targets as time passes. This reflects the "securing profits early" risk management philosophy.
- **Stop-Loss Design**: Fixed stop-loss set at -99%, effectively disabling the fixed stop-loss, entirely relying on the dynamic trailing stop-loss implemented in the `custom_stoploss` function.

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "market",
    "exit": "market",
    "emergency_exit": "market",
    "force_entry": "market",
    "force_exit": "market",
    "stoploss": "market",
    "stoploss_on_exchange": False,
    "stoploss_on_exchange_interval": 60,
    "stoploss_on_exchange_limit_ratio": 0.99,
}
```

**Design Philosophy**: All orders use market orders, ensuring immediate execution and avoiding slippage risk.

---

## III. Entry Conditions Details

### 3.1 Protection Mechanism (1 Set)

The strategy configures a slippage protection mechanism for entry conditions:

| Protection Type | Parameter Description | Default Value |
|---------------|---------------------|---------------|
| Slippage Protection | max_slip controls max acceptable slippage percentage | 0.73% |

**Implementation Logic**: In the `confirm_trade_entry` method, the system checks the deviation between the current quote and the actual execution price. If slippage exceeds `max_slip`, the order is rejected.

### 3.2 Entry Conditions Details

The strategy has two independent entry paths, both requiring the 1-hour timeframe ROCR filtering condition first.

#### Condition #1: Bollinger Bands Mean Reversion + ROCR Filtering
```python
# Logic
- rocr_1h > 0.5411 (1-hour ROC must be in an upward trend)
- bbdelta > ha_close * 0.01846 (Bollinger Band width must reach a certain ratio)
- closedelta > ha_close * 0.01009 (Closing price change must be significant)
- tail < bbdelta * 0.98973 (Lower wick must not be too long)
- ha_close < lower.shift() (HA close must break below the Bollinger lower band)
- ha_close <= ha_close.shift() (Must show a downward trend)
- hh_48_diff > 6.867 (48-hour highest price difference filter)
- ll_48_diff > -12.884 (48-hour lowest price difference filter)
```

#### Condition #2: EMA Deviation + Bollinger Lower Band Support
```python
# Logic
- rocr_1h > 0.5411 (1-hour ROC filtering)
- ha_close < ema_slow (HA close must be below the 50-period EMA)
- ha_close < 0.00785 * bb_lowerband (Close must be close to the Bollinger lower band)
- hh_48_diff > 6.867 (48-hour highest price difference filter)
- ll_48_diff > -12.884 (48-hour lowest price difference filter)
```

### 3.3 Entry Conditions Classification

| Condition Group | Condition # | Core Logic |
|----------------|------------|------------|
| Bollinger Bands Mean Reversion | #1 | Confirms buy timing through Bollinger Band narrowing, HA breaking lower band, and rising ROCR trend |
| EMA Deviation Reversal | #2 | Captures rebound opportunities when price excessively deviates from EMA and then reverts |

---

## IV. Exit Conditions Details

### 4.1 Multi-Layer Take-Profit System

The strategy employs a dual take-profit mechanism combining the ROI table and trailing stop:

```
Profit Range       Threshold    Signal Name
---------------------------------------
0% - 1.1%         0.011       Base Take-Profit
1.1% - 3.3%       0.033       Medium-Term Take-Profit
3.3% - 5%         0.05        Short-Term Take-Profit
5% - 10.3%        0.103       Initial Take-Profit
> 10.3%            -           Trailing Stop Takes Over
```

### 4.2 Special Exit Scenarios

The strategy implements multiple custom sell signals to handle special market conditions:

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| Dead Fish Stop-Loss | Profit <-6.3%, price below EMA200, extremely low volatility | sell_stoploss_deadfish |
| 48-Hour Surge Stop-Loss | 1-hour gain >95%, profit -4% to -8%, multiple indicators weakening | sell_stoploss_p_48_1_1 |
| 36-Hour Surge Stop-Loss | 1-hour gain >70%, profit -4% to -8%, multiple indicators weakening | sell_stoploss_p_36_1_1 |
| 24-Hour Surge Stop-Loss | 1-hour gain >60%, profit -4% to -8%, multiple indicators weakening | sell_stoploss_p_24_1_1 |

### 4.3 Basic Sell Signals (3)

```python
# Sell Signal 1: Fisher Indicator Reversal + Bollinger Band Confirmation
- fisher > 0.48492
- ha_high declining for 3 consecutive candles
- ha_close declining
- ema_fast > ha_close
- ha_close * 0.97286 > bb_middleband

# Sell Signal 2: Breakout Confirmation
- close > sma_9
- close > ema_24 * 1.211
- rsi > 50
- rsi_fast > rsi_slow

# Sell Signal 3: Trend Weakening
- sma_9 rising more than 0.5% compared to 1 period ago
- close < hma_50
- close > ema_24 * 0.907
- rsi_fast > rsi_slow
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | EMA (3, 50, 24, 200), SMA (9, 200), HMA (50) | Determine price trend direction |
| Bollinger Bands | BB (20), BB (40) | Identify price volatility ranges and mean reversion opportunities |
| Momentum Indicators | ROCR (28), RSI (4, 14, 20), Fisher | Determine market momentum and overbought/oversold conditions |
| Volume | Volume Mean (12, 24, 30), CMF (20) | Validate price signals with volume confirmation |
| Special Indicators | HH_48, LL_48, EMA-VWMA Osc | Identify short-term extremes and trend strength |

### 5.2 Informative Timeframe Indicators (1h)

The strategy uses 1-hour as the informational layer, providing higher-dimensional trend judgment:

- **ROC Indicator**: Calculates the 168-period (1-week) rate of change in price, used to filter counter-trend trades.
- **SMA 200**: Identifies long-term trend direction, determining if price is in a long-term downtrend channel.
- **HL Percentage Change**: Calculates the percentage change from highest to lowest price within 24/36/48 hours, used to identify abnormal volatility.
- **CMF**: Chaikin Money Flow indicator, determines fund flow direction.

---

## VI. Risk Management Features

### 6.1 Dynamic Trailing Stop

The strategy implements a complex dynamic trailing stop system that adjusts stop-loss positions based on current profit levels:

| Profit Range | Stop-Loss Profit | Description |
|-------------|-----------------|-------------|
| > 6.4% | SL_2 + (profit - 6.4%) | High profit range, stop-loss follows profit upward |
| 1.1% - 6.4% | Linear interpolation | Dynamically calculated based on profit range |
| < 1.1% | -99% | Low profit range, uses hard stop-loss |

```python
# Parameter Configuration
pPF_1 = 0.011  # First profit-taking point
pPF_2 = 0.064  # Second profit-taking point
pSL_1 = 0.011  # First stop-loss profit
pSL_2 = 0.062  # Second stop-loss profit
```

### 6.2 Volatility Protection

The strategy includes volatility filtering in special scenario exits:

- **bb_width < 0.043**: When Bollinger Band width falls below the threshold, the market is considered "dead fish" conditions, triggering protective selling.
- **Volume Shrinkage Detection**: volume_mean_12 < volume_mean_24 * 2.37, detects abnormally shrinking volume.

### 6.3 Counter-Trend Protection

Multi-indicator filtering on the 1-hour timeframe avoids entries at trend reversal points:

- **sma_200_dec_20**: Confirms long-term downtrend at the 1-hour level.
- **ema_vwma_osc < 0**: Multi-period EMA-VWMA oscillator negative simultaneously.
- **cmf < -0.25**: Confirms capital outflow.

---

## VII. Strategy Pros & Cons

### Pros

1. **Multi-Dimensional Filtering**: Uses both 5-minute and 1-hour timeframes simultaneously, combined with multiple technical indicators, effectively filtering false signals.
2. **Dynamic Take-Profit Design**: Dynamically adjusts stop-loss positions based on profit levels, protecting profits while leaving room for further gains.
3. **Special Scenario Protection**: Designs specialized exit logic for extreme market conditions such as rapid surges followed by pullbacks and sharp volatility contraction.
4. **Complete Indicator System**: Integrates trend, momentum, volume, and fund flow analysis across multiple dimensions.

### Cons

1. **Many Parameters**: Over 20 adjustable parameters — high optimization difficulty, prone to overfitting.
2. **Computationally Intensive**: Requires calculating multi-period indicators and custom indicators, with higher hardware requirements.
3. **Depends on 1-Hour Informational Layer**: All entries require 1-hour ROCR confirmation, may miss optimal entry timing in fast-moving markets.
4. **Complex Custom Stop-Loss Logic**: Flexible but difficult to understand and debug.

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|--------------------|--------------------------|-------------|
| Slow Bull Trend | Enabled | Bollinger Bands mean reversion logic performs well during trend pullbacks |
| Volatile Market | Cautious | Multi-condition filtering may miss trading opportunities in volatile ranges |
| Extreme Volatility | Enable Special Exits | Strategy has specialized protection mechanisms for post-surge pullbacks |
| Range-Bound Consolidation | Not Recommended | Frequent 1-hour filtering will miss opportunities during consolidation |

---

## IX. Applicable Market Environment Details

ClucHAnix_hhll is a derivative of the Cluc series, positioned as a "high-volatility market protection-type trend-following strategy." Based on its code architecture and complex multi-layer filtering mechanism, it is best suited for **moderately volatile trending markets** and performs poorly in low-volatility sideways markets.

### 9.1 Core Strategy Logic

- **Heikin Ashi Candles**: Uses HA candles to smooth price fluctuations, eliminate short-term noise, and more clearly reflect trends.
- **Bollinger Bands Mean Reversion**: Captures reversal opportunities when price touches extreme Bollinger Band positions.
- **1-Hour Trend Filtering**: Filters counter-trend trades through longer-period ROC indicators.
- **Dynamic Take-Profit/Stop-Loss**: Dynamically adjusts risk management parameters based on profit levels.

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| Slow Bull | ⭐⭐⭐⭐ | Effectively captures continued after pullbacks when trends are clear |
| Volatile | ⭐⭐⭐ | Multi-condition filtering reduces trading frequency, but signal quality is high |
| Downtrend | ⭐⭐⭐ | Has counter-trend protection, but overall bias is long — not suitable for sustained |
| Extreme Volatility | ⭐⭐⭐⭐ | Special exit mechanisms effectively protect profits |

### 9.3 Key Configuration Recommendations

| Configuration Item | Suggested Value | Description |
|-------------------|-----------------|-------------|
| max_slip | 0.33-0.73 | Adjust based on exchange liquidity |
| rocr_1h | 0.54-0.65 | Higher values mean stricter filtering |
| trailing_stop | True | Trailing stop recommended |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

ClucHAnix_hhll involves a large number of custom indicators and multi-layer logical nesting. Understanding the complete logic requires:
- Familiarity with Heikin Ashi candle principles
- Understanding of Bollinger Bands mean reversion strategy
- Mastery of custom trailing stop calculation logic
- Knowledge of multi-timeframe analysis methods

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum RAM | Recommended RAM |
|-------------------------|-------------|-----------------|
| 10-20 pairs | 2GB | 4GB |
| 20-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

### 10.3 Backtesting vs. Live Trading Differences

- The strategy uses market orders with slippage protection; execution prices assumed in backtesting may deviate from live trading.
- 1-hour informative layer indicator calculations require additional historical data caching in live trading.
- Custom stop-loss trigger logic may have execution delays under certain extreme market conditions.

### 10.4 Manual Trading Recommendations

This strategy is not suitable for manual traders to use directly, reasons:
1. Multi-condition combination judgment requires real-time monitoring of multiple indicators.
2. Dynamic take-profit/stop-loss calculation logic is complex.
3. Requires continuous monitoring of 1-hour-level market conditions.

---

## XI. Summary

ClucHAnix_hhll is a meticulously designed complex trend-following strategy that combines Heikin Ashi candle analysis, Bollinger Bands mean reversion, multi-timeframe filtering, and dynamic take-profit/stop-loss mechanisms. Its core value lies in:

1. **Multi-Dimensional Signal Confirmation**: Significantly improves signal quality through 5-minute and 1-hour multi-layer filtering.
2. **Intelligent Risk Management**: Dynamic trailing stop and special scenario protection mechanisms effectively handle market extremes.
3. **Complete Indicator System**: Integrates trend, momentum, volume, and fund flow analysis tools across multiple dimensions.

For quantitative traders, this strategy is suitable for investors with solid technical foundations operating in moderately volatile markets. Special attention should be paid to the reasonableness of parameter optimization to avoid overfitting historical data. It is recommended to test with small capital in live trading for at least 1-2 months, confirming strategy effectiveness before gradually increasing position sizes.

---
