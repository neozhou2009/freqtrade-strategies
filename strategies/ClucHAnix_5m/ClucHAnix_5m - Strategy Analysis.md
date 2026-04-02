# ClucHAnix_5m Strategy Analysis

> **Strategy ID**: #94 (465 strategies, 94th)  
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Mean Reversion + Protection Mechanisms  
> **Timeframe**: 5 Minutes (5m) + 1-Hour Informational Layer

---

## I. Strategy Overview

ClucHAnix_5m is a complex trend-following strategy based on Heikin Ashi (HA) candlestick charts and Bollinger Band mean reversion principles. This strategy is a 5-minute variant of the ClucHAnix series, fusing multiple technical indicators to identify potential reversal points and trend continuation signals, suitable for operation in moderately volatile market environments.

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

**Design Philosophy**: The ROI table uses a front-heavy gradient design with high initial profit targets (10.3%) that gradually reduce over time. The 5-minute timeframe is optimized for fast in-and-out trading. The -99% nominal stop-loss effectively disables fixed stops, relying entirely on custom_stoploss.

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

**Design Philosophy**: All market orders ensure immediate execution, critical for time-sensitive 5-minute trading.

---

## III. Entry Conditions Details

### 3.1 Protection Mechanism (1 Set)

| Protection Type | Parameter Description | Default Value |
|----------------|---------------------|---------------|
| Slippage protection | max_slip controls max acceptable slippage % | 0.73% |

### 3.2 Entry Condition Details

#### Condition #1: Bollinger Band Mean Reversion + ROCR Filtering
```python
# Logic
- rocr_1h > 0.5411 (1-hour ROC must be in uptrend)
- bbdelta > ha_close * 0.01846 (Bollinger Band width sufficient)
- closedelta > ha_close * 0.01009 (Close price change significant)
- tail < bbdelta * 0.98973 (Lower wick not too long)
- ha_close < lower.shift() (HA close breaks below lower band)
- ha_close <= ha_close.shift() (Must show downtrend)
- hh_48_diff > 6.867 (48-hour high difference filter)
- ll_48_diff > -12.884 (48-hour low difference filter)
```

**Design Intent**: Through Bollinger compression, HA lower band breakout, and ROC uptrend confirmation, capture mean reversion opportunities.

#### Condition #2: EMA Deviation + Lower Band Support
```python
# Logic
- rocr_1h > 0.5411 (1-hour ROC filter)
- ha_close < ema_slow (HA close below 50-period EMA)
- ha_close < 0.00785 * bb_lowerband (Close hugs lower band)
- hh_48_diff > 6.867 (48-hour high filter)
- ll_48_diff > -12.884 (48-hour low filter)
```

### 3.3 Entry Condition Classification

| Condition Group | Condition # | Core Logic |
|----------------|-------------|------------|
| Bollinger Band Mean Reversion | #1 | Bollinger compression + HA lower band breakout + ROC confirmation |
| EMA Deviation Repair | #2 | Rebound when price deviates excessively from EMA |

---

## IV. Exit Logic Details

### 4.1 Multi-Layer Take-Profit System

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
| Bollinger Bands | BB (20), BB (40) | Identify volatility ranges and mean reversion |
| Momentum Indicators | ROCR (28), RSI (4, 14, 20), Fisher | Determine overbought/oversold |
| Volume Indicators | Volume Mean (12, 24, 30), CMF (20) | Volume confirmation |
| Special Indicators | HH_48, LL_48, EMA-VWMA Osc | Short-term extremes and trend strength |

### 5.2 Informational Timeframe Indicators (1h)

- **ROC**: 168-period (1-week) rate of change, filters counter-trend trades
- **SMA 200**: Long-term trend direction
- **HL % Change**: High-to-low % within 24/36/48 hours, identifies abnormal volatility
- **CMF**: Chaikin Money Flow, determines capital flow direction

---

## VI. Risk Management Highlights

### 6.1 Dynamic Trailing Stop

| Profit Range | Stop-Loss Profit | Description |
|-------------|-----------------|-------------|
| > 6.4% | SL_2 + (profit - 6.4%) | Stop follows profit upward |
| 1.1% - 6.4% | Linear interpolation | Dynamically calculated |
| < 1.1% | -99% | Hard stop |

### 6.2 Volatility Protection

- **bb_width < 0.043**: "Dead fish" market triggers protective exit
- **Volume contraction**: volume_mean_12 < volume_mean_24 * 2.37

### 6.3 Counter-Trend Protection

- **sma_200_dec_20**: Confirms 1-hour long-term downtrend
- **ema_vwma_osc < 0**: Multi-period EMA-VWMA oscillator negative
- **cmf < -0.25**: Capital outflow confirmation

---

## VII. Strategy Pros & Cons

### Pros

1. **Multi-dimensional filtering**: 5-minute and 1-hour dual timeframes, effectively filters false signals
2. **Dynamic profit-taking design**: Adjusts stop-loss based on profit level
3. **Special scenario protection**: Dedicated exits for pump-and-dump and volatility contraction
4. **Complete indicator system**: Integrates trend, momentum, volume, capital flow
5. **5-minute high-frequency advantage**: Faster capital turnover and more opportunities

### Cons

1. **Many parameters**: 20+ adjustable parameters, high overfitting risk
2. **Computation intensive**: Multi-period indicators, significant hardware requirements
3. **Depends on 1-hour layer**: May miss best timing in fast markets
4. **Complex custom stop-loss logic**: Hard to understand and debug
5. **Transaction cost sensitive**: High frequency at 5-minute level

---

## VIII. Applicable Scenarios

| Market Environment | Recommendation | Description |
|--------------------|----------------|-------------|
| Slow bull trend | Enable | Bollinger Band mean reversion performs well on pullbacks |
| Ranging markets | Use with caution | Multi-condition filtering may miss opportunities |
| Pump and dump | Enable special exits | Has dedicated protection |
| Flat consolidation | Not recommended | 1-hour filtering misses consolidation opportunities |
| High-frequency trading | Applicable | 5-minute level suits high turnover |

---

## IX. Applicable Market Environment Details

ClucHAnix_5m is the 5-minute optimized variant of ClucHAnix, positioned as a "high-frequency trend-following strategy." Best in **moderately volatile trending markets**, poor in **low-volatility consolidation**.

### 9.1 Core Strategy Logic

- **Heikin Ashi**: Smooths price, eliminates noise, clearly reflects trends
- **Bollinger Band mean reversion**: Captures reversals at extreme positions
- **1-hour trend filtering**: Filters counter-trend through ROC
- **Dynamic profit-taking stop-loss**: Adjusts risk parameters based on profit
- **5-minute high-frequency**: More opportunities, higher costs

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Slow bull | Good | Catches continued rallies after pullbacks |
| Ranging | Moderate | Lower frequency but higher signal quality |
| Declining | Moderate | Has counter-trend protection, overall bullish bias |
| Pump and dump | Good | Special exits protect profits |
| High-frequency trading | Excellent | 5-minute level maximizes opportunities |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|---------------|-------------------|-------------|
| max_slip | 0.33-0.73 | Adjust based on exchange liquidity |
| rocr_1h | 0.54-0.65 | Higher = stricter filtering |
| trailing_stop | True | Recommend enabling |
| Fee rate | < 0.1% | 5-minute level requires low fees |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

Requires familiarity with HA candles, Bollinger Band mean reversion, custom trailing stop calculation, multi-timeframe analysis, and 5-minute high-frequency characteristics.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 10-20 pairs | 2GB | 4GB |
| 20-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

### 10.3 Transaction Cost Considerations

5-minute trading is high-frequency; pay special attention to fee rates. Recommend low-fee exchanges or maker orders. Include fees in all backtesting.

### 10.4 Backtesting vs. Live Trading Differences

- Market orders with slippage protection — backtest prices may deviate from live fills
- 1-hour layer requires historical data caching
- Custom stop-loss may have execution delays in extreme markets
- 5-minute level is more sensitive to network latency

### 10.5 Manual Trader Recommendations

Unsuitable for direct manual trading due to multi-condition judgment, complex dynamic stops, continuous 1-hour monitoring requirements, and the speed of 5-minute changes.

---

## XI. Summary

ClucHAnix_5m is a meticulously designed complex trend-following strategy combining Heikin Ashi analysis, Bollinger Band mean reversion, multi-timeframe filtering, and dynamic profit-taking stop-loss. As a high-frequency 5-minute variant, it maintains the original strategy's advantages while offering more trading opportunities.

Its core value lies in:

1. **Multi-dimensional signal confirmation**: 5-minute and 1-hour multiple filtering significantly improves signal quality
2. **Intelligent risk management**: Dynamic trailing stop and special scenario protection handle extremes
3. **Complete indicator system**: Integrates trend, momentum, volume, and capital flow
4. **High-frequency capability**: 5-minute level brings higher turnover

For quantitative traders, this strategy suits investors with technical backgrounds in moderately volatile markets. Pay attention to parameter optimization reasonableness, transaction cost control, and hardware/network requirements. Test with small capital for at least 1-2 months before gradually increasing positions.
