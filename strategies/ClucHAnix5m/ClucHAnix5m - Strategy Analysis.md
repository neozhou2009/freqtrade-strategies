# ClucHAnix5m Strategy Analysis

> **Strategy ID**: #94 (465 strategies, 94th)  
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Mean Reversion + Protection Mechanisms  
> **Timeframe**: 5 Minutes (5m) + 1-Hour Informational Layer

---

## I. Strategy Overview

ClucHAnix5m is a complex trend-following strategy based on Heikin Ashi (HA) candlestick charts and Bollinger Band mean reversion principles. This strategy is a 5-minute variant of the ClucHAnix series, fusing multiple technical indicators to identify potential reversal points and trend continuation signals, suitable for operation in moderately volatile market environments. The name "5m" indicates its focus on the 5-minute trading cycle.

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
- **ROI Table Design**: Uses a front-heavy gradient — expects higher initial profits (10.3%), gradually lowering targets as time passes. The 5-minute level is designed for fast in-and-out trading.
- **Stop Loss Design**: Primary stop loss set to -99%, effectively disabling fixed stop-loss and fully relying on the dynamic trailing stop in custom_stoploss.

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

**Design Philosophy**: All market orders, ensuring immediate execution and avoiding slippage risk. 5-minute-level trading demands high timeliness; market orders are the best choice.

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

**Design Intent**: Through Bollinger compression, HA close breaking below lower band, and ROC uptrend confirmation, capture opportunities for price to revert from extreme positions.

#### Condition #2: EMA Deviation + Lower Band Support
```python
# Logic
- rocr_1h > 0.5411 (1-hour ROC filter)
- ha_close < ema_slow (HA close must be below 50-period EMA)
- ha_close < 0.00785 * bb_lowerband (Close must hug lower band)
- hh_48_diff > 6.867 (48-hour high difference filter)
- ll_48_diff > -12.884 (48-hour low difference filter)
```

**Design Intent**: Rebound opportunities when price deviates excessively from EMA, with lower band support confirmation.

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

**Design Logic**: 5-minute-level trading requires quick reactions, so a more aggressive profit-taking gradient design is used — pursuing higher initial profits, then gradually lowering targets.

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

- **ROC Indicator**: Calculates 168-period (1-week) rate of change, filters counter-trend trades
- **SMA 200**: Identifies long-term trend direction
- **HL Percentage Change**: Calculates percentage change from high to low within 24/36/48 hours
- **CMF**: Chaikin Money Flow indicator, determines capital flow direction

---

## VI. Risk Management Highlights

### 6.1 Dynamic Trailing Stop

The strategy implements a complex dynamic trailing stop system:

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

- **bb_width < 0.043**: When Bollinger Band width is below this threshold, market is considered "dead fish" — triggers protective exit
- **Volume contraction detection**: volume_mean_12 < volume_mean_24 * 2.37

### 6.3 Counter-Trend Protection

- **sma_200_dec_20**: Confirms 1-hour long-term downtrend
- **ema_vwma_osc < 0**: Multi-period EMA-VWMA oscillator negative simultaneously
- **cmf < -0.25**: Capital outflow confirmation

---

## VII. Strategy Pros & Cons

### Pros

1. **Multi-dimensional filtering**: Uses both 5-minute and 1-hour timeframes simultaneously, effectively filters false signals
2. **Dynamic profit-taking design**: Dynamically adjusts stop-loss based on profit level
3. **Special scenario protection**: Dedicated exit logic for pump-and-dump and volatility contraction extremes
4. **Complete indicator system**: Integrates trend, momentum, volume, and capital flow
5. **5-minute high-frequency advantage**: Shorter trading cycles mean faster capital turnover and more opportunities

### Cons

1. **Many parameters**: Over 20 adjustable parameters, high overfitting risk
2. **Computation intensive**: Multi-period indicators require significant hardware
3. **Depends on 1-hour informational layer**: May miss best entry timing in fast markets
4. **Complex custom stop-loss logic**: Flexible but hard to understand and debug
5. **Transaction cost sensitive**: Higher frequency at 5-minute level, fees significantly impact returns

---

## VIII. Applicable Scenarios

| Market Environment | Recommendation | Description |
|--------------------|----------------|-------------|
| Slow bull trend | Enable | Bollinger Band mean reversion performs well on trend pullbacks |
| Ranging markets | Use with caution | Multi-condition filtering may miss opportunities |
| Pump and dump | Enable special exits | Has dedicated protection against post-pump dumps |
| Flat consolidation | Not recommended | Frequent 1-hour filtering misses consolidation opportunities |
| High-frequency trading | Applicable | 5-minute level suits traders seeking high turnover |

---

## IX. Applicable Market Environment Details

ClucHAnix5m is the 5-minute optimized variant of ClucHAnix, positioned as a "high-frequency trend-following strategy." It performs best in **moderately volatile trending markets** and poorly in **low-volatility consolidation**.

### 9.1 Core Strategy Logic

- **Heikin Ashi candlestick**: Smooths price fluctuations, eliminates noise, clearly reflects trends
- **Bollinger Band mean reversion**: Captures reversal opportunities at extreme band positions
- **1-hour trend filtering**: Filters counter-trend trades through ROC
- **Dynamic profit-taking stop-loss**: Adjusts risk parameters based on profit levels
- **5-minute high-frequency**: Shorter candles bring more opportunities but also higher costs

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Slow bull | Good | Effectively captures continued rallies after pullbacks |
| Ranging | Moderate | Multi-condition filtering reduces frequency, higher signal quality |
| Declining | Moderate | Has counter-trend protection but overall bullish bias |
| Pump and dump | Good | Special exits effectively protect profits |
| High-frequency trading | Excellent | 5-minute level brings more opportunities |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|---------------|-------------------|-------------|
| max_slip | 0.33-0.73 | Adjust based on exchange liquidity |
| rocr_1h | 0.54-0.65 | Higher value means stricter filtering |
| trailing_stop | True | Recommend enabling |
| Fee rate | < 0.1% | 5-minute level requires low fees |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

ClucHAnix5m involves extensive custom indicators and multi-layer logic nesting. Fully understanding it requires familiarity with HA candles, Bollinger Band mean reversion, custom trailing stop calculation, and multi-timeframe analysis.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 10-20 pairs | 2GB | 4GB |
| 20-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

### 10.3 Transaction Cost Considerations

- 5-minute trading frequency is high; pay special attention to fee rates
- Recommend using exchanges with low fees or maker orders
- Must include fees in backtesting calculations

### 10.4 Backtesting vs. Live Trading Differences

- Market orders with slippage protection — backtest assumed prices may deviate from live fills
- 1-hour informational layer requires additional historical data cache
- Custom stop-loss may have execution delays in extreme markets
- 5-minute level is more sensitive to network latency

### 10.5 Manual Trader Recommendations

This strategy is unsuitable for direct manual trading:
1. Multi-condition judgment requires real-time monitoring of multiple indicators
2. Dynamic profit-taking stop-loss logic is complex
3. Requires continuous monitoring of 1-hour market state
4. 5-minute changes too fast for human reaction

---

## XI. Summary

ClucHAnix5m is a meticulously designed complex trend-following strategy combining Heikin Ashi analysis, Bollinger Band mean reversion, multi-timeframe filtering, and dynamic profit-taking stop-loss. As a high-frequency 5-minute variant, it maintains the original strategy's advantages while offering more trading opportunities.

Its core value lies in:

1. **Multi-dimensional signal confirmation**: 5-minute and 1-hour multiple filtering significantly improves signal quality
2. **Intelligent risk management**: Dynamic trailing stop and special scenario protection effectively handle extremes
3. **Complete indicator system**: Integrates trend, momentum, volume, and capital flow
4. **High-frequency trading capability**: 5-minute level brings higher turnover rate

For quantitative traders, this strategy suits investors with technical backgrounds in moderately volatile markets. Pay special attention to:
- Reasonableness of parameter optimization, avoid overfitting historical data
- Transaction cost control, 5-minute level is more sensitive to fees
- Hardware and network environment requirements, high-frequency trading needs low latency

It is recommended to test with small capital for at least 1-2 months in live trading before gradually increasing positions.
