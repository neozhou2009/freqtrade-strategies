# ClucHAnix Strategy Analysis

> **Strategy ID**: #93 (465 strategies, 93rd)  
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Mean Reversion + Protection Mechanisms  
> **Timeframe**: 5 Minutes (5m) + 1-Hour Informational Layer

---

## I. Strategy Overview

ClucHAnix is a complex trend-following strategy based on Heikin Ashi (HA) candlestick charts and Bollinger Band mean reversion principles. The strategy fuses multiple technical indicators to identify potential reversal points and trend continuation signals, suitable for operation in moderately volatile market environments. The "Cluc" in the name comes from the Cluc series, while "HAnix" represents its unique architecture combining Heikin Ashi (average candles) with Bollinger Band analysis.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 2 independent entry signal paths, both require 1-hour ROCR filtering |
| **Exit Conditions** | 3 base exit signals + multi-layer dynamic profit-taking logic + special scenario stop-loss |
| **Protection Mechanisms** | 1 set of slippage protection parameters |
| **Timeframe** | Primary 5m + Informational 1h |
| **Dependencies** | technical, talib, numpy, pandas |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.103,     # Immediate exit at 10.3% profit
    "3": 0.05,      # Profit drops to 5% after 3 minutes
    "5": 0.033,     # Profit drops to 3.3% after 5 minutes
    "61": 0.027,    # Profit drops to 2.7% after 1 hour
    "125": 0.011,   # Profit drops to 1.1% after ~2 hours
    "292": 0.005,   # Profit drops to 0.5% after ~5 hours
}

# Stop Loss
stoploss = -0.99  # Uses custom stop-loss, fully relies on custom_stoploss

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.001
trailing_stop_positive_offset = 0.012
trailing_only_offset_is_reached = False
```

**Design Philosophy**:
- **ROI Table Design**: Uses a front-heavy gradient design — expects high initial profits (10.3%), gradually lowering targets as time passes. Aligns with the "securing profits early" risk management philosophy.
- **Stop Loss Design**: Primary stop loss set to -99%, effectively disabling fixed stop-loss and fully relying on the dynamic trailing stop implemented in the custom_stoploss function.

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

**Design Philosophy**: All market orders, ensuring immediate execution and avoiding slippage risk.

---

## III. Entry Conditions Details

### 3.1 Protection Mechanism (1 Set)

The strategy configures slippage protection for entry conditions:

| Protection Type | Parameter Description | Default Value |
|----------------|---------------------|---------------|
| Slippage protection | max_slip parameter controls max acceptable slippage percentage | 0.73% |

**Implementation Logic**: In the confirm_trade_entry method, the system checks the deviation between current quote and actual fill price. If slippage exceeds max_slip, the order is rejected.

### 3.2 Entry Condition Details

The strategy has two independent entry paths, both requiring the 1-hour ROCR filtering condition first.

#### Condition #1: Bollinger Band Mean Reversion + ROCR Filtering
```python
# Logic
- rocr_1h > 0.5411 (1-hour ROC must be in uptrend)
- bbdelta > ha_close * 0.01846 (Bollinger Band width must reach certain ratio)
- closedelta > ha_close * 0.01009 (Close price change must be significant)
- tail < bbdelta * 0.98973 (Lower wick must not be too long)
- ha_close < lower.shift() (HA close must break below lower band)
- ha_close <= ha_close.shift() (Must show downtrend)
- hh_48_diff > 6.867 (48-hour high difference filter)
- ll_48_diff > -12.884 (48-hour low difference filter)
```

#### Condition #2: EMA Deviation + Lower Band Support
```python
# Logic
- rocr_1h > 0.5411 (1-hour ROC filter)
- ha_close < ema_slow (HA close must be below 50-period EMA)
- ha_close < 0.00785 * bb_lowerband (Close must hug lower band)
- hh_48_diff > 6.867 (48-hour high difference filter)
- ll_48_diff > -12.884 (48-hour low difference filter)
```

### 3.3 Entry Condition Classification

| Condition Group | Condition # | Core Logic |
|----------------|-------------|------------|
| Bollinger Band Mean Reversion | #1 | Confirms buy timing through Bollinger compression, HA lower band breakout, and ROC uptrend |
| EMA Deviation Repair | #2 | Rebound opportunity when price deviates excessively from EMA |

---

## IV. Exit Logic Details

### 4.1 Multi-Layer Take-Profit System

The strategy employs a dual take-profit mechanism combining the ROI table and trailing stop:

```
Profit Range        Threshold     Signal Name
──────────────────────────────────────────────────
0% - 1.1%           0.011        Base take-profit
1.1% - 3.3%         0.033        Medium-term take-profit
3.3% - 5%           0.05         Short-term take-profit
5% - 10.3%          0.103        Initial take-profit
> 10.3%             -            Trailing stop takes over
```

### 4.2 Special Exit Scenarios

The strategy implements several custom exit signals for special market conditions:

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| Dead fish stop-loss | Profit <-6.3%, price below EMA200, extremely low volatility | sell_stoploss_deadfish |
| 48-hour pump stop-loss | 1-hour gain >95%, profit -4% to -8%, multiple indicators weakening | sell_stoploss_p_48_1_1 |
| 36-hour pump stop-loss | 1-hour gain >70%, profit -4% to -8%, multiple indicators weakening | sell_stoploss_p_36_1_1 |
| 24-hour pump stop-loss | 1-hour gain >60%, profit -4% to -8%, multiple indicators weakening | sell_stoploss_p_24_1_1 |

### 4.3 Base Exit Signals (3 Total)

```python
# Exit Signal 1: Fisher Indicator Reversal + Bollinger Band Confirmation
- fisher > 0.48492
- ha_high declining for 3 consecutive candles
- ha_close declining
- ema_fast > ha_close
- ha_close * 0.97286 > bb_middleband

# Exit Signal 2: Breakout Confirmation
- close > sma_9
- close > ema_24 * 1.211
- rsi > 50
- rsi_fast > rsi_slow

# Exit Signal 3: Trend Weakening
- sma_9 rises more than 0.5% vs 1 period ago
- close < hma_50
- close > ema_24 * 0.907
- rsi_fast > rsi_slow
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|--------------------|---------|
| Trend Indicators | EMA (3, 50, 24, 200), SMA (9, 200), HMA (50) | Determine price trend direction |
| Bollinger Bands | BB (20), BB (40) | Identify price volatility ranges and mean reversion opportunities |
| Momentum Indicators | ROCR (28), RSI (4, 14, 20), Fisher | Determine market momentum and overbought/oversold |
| Volume Indicators | Volume Mean (12, 24, 30), CMF (20) | Verify volume confirmation of price signals |
| Special Indicators | HH_48, LL_48, EMA-VWMA Osc | Identify short-term extremes and trend strength |

### 5.2 Informational Timeframe Indicators (1h)

The strategy uses 1 hour as an informational layer for higher-dimensional trend judgment:

- **ROC Indicator**: Calculates 168-period (1-week) rate of change, used to filter counter-trend trades
- **SMA 200**: Identifies long-term trend direction, determines if price is in a long-term downtrend channel
- **HL Percentage Change**: Calculates percentage change from high to low within 24/36/48 hours, identifies abnormal volatility
- **CMF**: Chaikin Money Flow indicator, determines capital flow direction

---

## VI. Risk Management Highlights

### 6.1 Dynamic Trailing Stop

The strategy implements a complex dynamic trailing stop system, dynamically adjusting stop-loss positions based on current profit levels:

| Profit Range | Stop-Loss Profit | Description |
|-------------|-----------------|-------------|
| > 6.4% | SL_2 + (profit - 6.4%) | High profit range, stop follows profit upward |
| 1.1% - 6.4% | Linear interpolation | Dynamically calculated by profit range |
| < 1.1% | -99% | Low profit range, uses hard stop |

```python
# Parameter configuration
pPF_1 = 0.011  # First take-profit point
pPF_2 = 0.064  # Second take-profit point
pSL_1 = 0.011  # First stop-loss profit
pSL_2 = 0.062  # Second stop-loss profit
```

### 6.2 Volatility Protection

The strategy includes volatility filtering in special scenario exits:

- **bb_width < 0.043**: When Bollinger Band width falls below this threshold, market is considered "dead fish" condition, triggering protective exit
- **Volume contraction detection**: volume_mean_12 < volume_mean_24 * 2.37, detects abnormally contracted volume

### 6.3 Counter-Trend Protection

Through multiple indicator filtering on the 1-hour timeframe, avoids entering at trend reversal points:

- **sma_200_dec_20**: Confirms 1-hour long-term downtrend
- **ema_vwma_osc < 0**: Multi-period EMA-VWMA oscillator negative simultaneously
- **cmf < -0.25**: Capital outflow confirmation

---

## VII. Strategy Pros & Cons

### Pros

1. **Multi-dimensional filtering**: Uses both 5-minute and 1-hour timeframes simultaneously, combined with multiple technical indicators, effectively filters false signals
2. **Dynamic profit-taking design**: Dynamically adjusts stop-loss position based on profit level, protecting profits while leaving room for gains
3. **Special scenario protection**: Designs dedicated exit logic for extreme conditions like rapid pump-and-dump and sharp volatility contraction
4. **Complete indicator system**: Integrates analysis tools across multiple dimensions: trend, momentum, volume, capital flow

### Cons

1. **Many parameters**: Over 20 adjustable parameters, high optimization difficulty, easy to overfit
2. **Computation intensive**: Requires multi-period indicator calculations and custom indicators, high hardware requirements
3. **Depends on 1-hour informational layer**: All entries require 1-hour ROCR confirmation, may miss best entry timing in fast-changing markets
4. **Complex custom stop-loss logic**: Flexible but difficult to understand and debug

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|--------------------|----------------|-------------|
| Slow bull trend | Enable | Strategy's Bollinger Band mean reversion performs well on trend pullbacks |
| Ranging markets | Use with caution | Multi-condition filtering may miss ranging opportunities |
| Pump and dump | Enable special exits | Strategy has dedicated protection against post-pump dumps |
| Flat consolidation | Not recommended | Frequent 1-hour filtering misses consolidation opportunities |

---

## IX. Applicable Market Environment Details

ClucHAnix is a derivative of the Cluc series, positioned as a "high-volatility market protection trend-following strategy." Based on its code architecture and complex multi-layer filtering, it performs best in **moderately volatile trending markets** and poorly in **low-volatility consolidation**.

### 9.1 Core Strategy Logic

- **Heikin Ashi candlestick**: Uses HA candles to smooth price fluctuations, eliminate short-term noise, more clearly reflect trends
- **Bollinger Band mean reversion**: Captures reversal opportunities when price touches extreme Bollinger Band positions
- **1-hour trend filtering**: Filters counter-trend trades through longer-period ROC indicator
- **Dynamic profit-taking stop-loss**: Dynamically adjusts risk management parameters based on profit levels

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Slow bull | Good | Can effectively capture continued rallies after pullbacks when trend is clear |
| Ranging | Moderate | Multi-condition filtering reduces trading frequency but signal quality is higher |
| Declining | Moderate | Has counter-trend protection but overall bullish bias unsuitable for sustained decline |
| Pump and dump | Good | Special exit mechanism effectively protects profits |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|---------------|-------------------|-------------|
| max_slip | 0.33-0.73 | Adjust based on exchange liquidity |
| rocr_1h | 0.54-0.65 | Higher value means stricter filtering |
| trailing_stop | True | Recommend enabling trailing stop |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

ClucHAnix involves extensive custom indicators and multi-layer logic nesting. Fully understanding it requires:
- Familiarity with Heikin Ashi candlestick principles
- Understanding of Bollinger Band mean reversion strategies
- Mastery of custom trailing stop calculation logic
- Understanding of multi-timeframe analysis methods

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 10-20 pairs | 2GB | 4GB |
| 20-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

### 10.3 Backtesting vs. Live Trading Differences

- Strategy uses market orders with slippage protection; backtest-assumed fill prices may deviate from live trading
- 1-hour informational layer indicator calculations require additional historical data caching in live trading
- Custom stop-loss trigger logic may have execution delays in some extreme market conditions

### 10.4 Manual Trader Recommendations

This strategy is unsuitable for direct manual trading because:
1. Multi-condition combination judgment requires real-time monitoring of multiple indicators
2. Dynamic profit-taking stop-loss calculation logic is complex
3. Requires continuous monitoring of 1-hour market state

---

## XI. Summary

ClucHAnix is a meticulously designed complex trend-following strategy that combines Heikin Ashi candlestick analysis, Bollinger Band mean reversion, multi-timeframe filtering, and dynamic profit-taking stop-loss techniques. Its core value lies in:

1. **Multi-dimensional signal confirmation**: Significantly improves signal quality through 5-minute and 1-hour multiple filtering
2. **Intelligent risk management**: Dynamic trailing stop and special scenario protection mechanisms effectively handle market extremes
3. **Complete indicator system**: Integrates analysis tools across dimensions: trend, momentum, volume, capital flow

For quantitative traders, this strategy is suitable for investors with some technical background operating in moderately volatile markets. Pay special attention to the reasonableness of parameter optimization and avoid overfitting historical data. It is recommended to test with small capital for at least 1-2 months in live trading, and gradually increase positions only after confirming strategy effectiveness.
