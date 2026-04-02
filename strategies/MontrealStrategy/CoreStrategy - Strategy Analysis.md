# CoreStrategy Strategy Analysis

> **Strategy ID**: #131 (131st of 465 strategies)  
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Mean Reversion + EWO Momentum  
> **Timeframe**: 5 minutes (5m) + 1-hour informational layer

---

## I. Strategy Overview

**CoreStrategy** is a complex multi-condition entry strategy that integrates the core logic of several classic strategies (including SMAOffsetProtectOpt, CombinedBinHClucAndMADV6, CombinedBinHClucV8, CombinedBinHClucAndMADV9). It constructs a multi-layered entry filtering system through 21 independent buy conditions. The strategy uses a 5-minute primary timeframe paired with a 1-hour informational layer for trend confirmation.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 21 independent buy conditions (individually enableable/disableable) |
| **Sell Conditions** | 4 basic exit signals + multi-layer dynamic take-profit logic |
| **Protection** | Custom stop-loss logic, no independent entry protection parameters |
| **Timeframe** | 5 minutes + 1-hour informational layer |
| **Dependencies** | TA-Lib, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.20,      # 0-38 minutes: 20% profit
    "38": 0.074,    # 38-78 minutes: 7.4% profit
    "78": 0.025,    # 78-194 minutes: 2.5% profit
    "194": 0        # After 194 minutes: free exit
}

# Stop-Loss Setting
stoploss = -0.228  # -22.8% hard stop-loss (actually managed by custom stop-loss logic)

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.005
trailing_stop_positive_offset = 0.049
```

**Design Philosophy**:
- **Aggressive ROI**: First target of 20% profit, suitable for high-volatility markets
- **Stepped Exit**: Progressively lowered from 20% → 7.4% → 2.5%, balancing profit-taking with holding endurance
- **Loose Hard Stop-Loss**: -22.8% is actually managed by custom logic, providing more flexible risk control

### 2.2 Order Type Configuration

```python
# Order Type Configuration
order_types = {
    "entry": "limit",
    "exit": "limit",
    "stoploss": "market",
    "stoploss_on_exchange": False
}

# Exit Signal Configuration
use_exit_signal = True
exit_profit_only = True
exit_profit_offset = 0.001
ignore_roi_if_entry_signal = True
```

---

## III. Entry Conditions Details

### 3.1 Condition Group Overview

The strategy contains 21 buy conditions, divided into 4 main series:

| Condition Group | Condition Numbers | Core Logic | Default Status |
|----------------|------------------|------------|----------------|
| **SMAOffset** | smaoffset_buy_condition_0/1 | EWO momentum + RSI filtering | Enabled by default |
| **V6 (CombinedBinHClucAndMADV6)** | v6_buy_condition_0~3 | Bollinger Band mean reversion + volume filtering | Partially enabled |
| **V8 (CombinedBinHClucV8)** | v8_buy_condition_0~4 | Multi-period EMA confirmation + Bollinger Band | Mostly enabled |
| **V9 (CombinedBinHClucAndMADV9)** | v9_buy_condition_0~10 | RSI oversold + Bollinger Band bottom divergence | Disabled by default |

### 3.2 Condition #1: smaoffset_buy_condition_0 (EWO High Rebound)

```python
# Logic
- Price < MA buy line * low_offset
- EWO > ewo_high (default 5.499)
- RSI < rsi_buy (default 50)
```

**Core Logic**: Price is at a relatively low level after a pullback, while EWO shows strong upward momentum, forming a "rebound" pattern.

### 3.3 Condition #2: smaoffset_buy_condition_1 (EWO Bottom-Fishing)

```python
# Logic
- Price < MA buy line * low_offset
- EWO < ewo_low (default -19.881)
```

**Core Logic**: Extremely negative EWO indicates potential bottom-fishing opportunities after a significant drop, filtered by price position.

### 3.4 Conditions #3-7: V8 Series (Multi-Period Trend Confirmation)

Common characteristics of V8 series conditions:
- Requires 1-hour EMA to be in upward bullish alignment
- Requires 5-minute price pullback to be within threshold
- Uses Bollinger Band middle band breakout or price touching lower band as signals

#### v8_buy_condition_0
- 1h EMA50 > 1h EMA200 AND 5m EMA50 > 5m EMA200
- Bollinger Band contraction pattern (bbdelta, closedelta, tail comprehensive judgment)
- Price breaks below Bollinger Band lower band

#### v8_buy_condition_1
- Both 5m and 1h close prices above EMA200
- 1h EMA50 > EMA100 > EMA200
- Price touches Bollinger Band lower band + volume contraction

#### v8_buy_condition_2
- SSL Channel 1h upward
- 5m price above EMA50 and EMA200
- RSI 1h-RSI spread > threshold

#### v8_buy_condition_3
- 200-period SMA upward trend (5m and 1h)
- RSI 1h > threshold, RSI 5m < threshold
- MFI < threshold

#### v8_buy_condition_4
- Price > 1h EMA100
- EMA golden cross (EMA26 > EMA12)
- Price touches Bollinger Band lower band + volume contraction

### 3.5 Conditions #8-17: V9 Series (Conservative Entry)

Most V9 series conditions are disabled by default, characterized by:
- Emphasis on RSI oversold
- Emphasis on volume contraction
- Emphasis on price near Bollinger Band lower band

### 3.6 Conditions #18-21: V6 Series (Bollinger Band Mean Reversion)

#### v6_buy_condition_0
- Close > EMA200 (5m and 1h)
- Price < Bollinger Band lower band * 0.99
- Volume contraction

#### v6_buy_condition_1
- Price < EMA50
- Price < Bollinger Band lower band * 0.975
- RSI 1h < 15 (buy prohibited)

#### v6_buy_condition_2
- Both 5m and 1h prices above EMA200
- EMA26 > EMA12 (golden cross pattern)
- Price touches Bollinger Band lower band

#### v6_buy_condition_3
- EMA26 > EMA12
- Volume contraction
- Price touches Bollinger Band lower band

### 3.7 Minimum Condition Count

```python
buy_minimum_conditions = 1  # Only 1 condition needs to be met to enter
```

---

## IV. Exit Logic Details

### 4.1 Multi-Layer Dynamic Take-Profit System

The strategy uses the `custom_exit` function to implement 5-layer ROI exit:

| Profit Zone | Threshold | RSI Condition | Signal Name |
|------------|-----------|--------------|-------------|
| High take-profit | > 30% | RSI < 58 | roi_target_4 |
| Mid-high take-profit | > 15% | RSI < 56 | roi_target_3 |
| Mid take-profit | > 4% | RSI < 50 | roi_target_2 |
| Low take-profit | > 1% | RSI < 50 | roi_target_1 |
| SMA death cross exit | 1-4% | SMA200 downward | roi_target_5 |

### 4.2 Trailing Stop Exit

The strategy implements a two-phase trailing stop:

| Phase | Profit Zone | Drawdown Trigger |
|-------|-------------|------------------|
| Phase 1 | 10%-40% | 3% drawdown from high |
| Phase 2 | 2%-10% | 1.5% drawdown from high |

### 4.3 Custom Stop-Loss Logic

The `custom_stoploss` function implements intelligent stop-loss:

```python
def custom_stoploss(...):
    if current_profit > 0:
        return 0.99  # Don't actively stop-loss when in profit
    
    # After 240 minutes of position open (~4 hours)
    if current_time > trade_time_50:
        # If SMA200 is downward (5m and 1h both confirmed)
        if (sma_200_dec) & (sma_200_dec_1h):
            return 0.01  # Force stop-loss
        
        # RSI 1h < 30 indicates potential bottom
        if rsi_1h < 30:
            return 0.99  # Continue holding, wait for rebound
        
        # Price breaks below open price by 2.5% AND above EMA200
        if current_rate * 1.025 < candle["open"]:
            if current_rate > ema_200:
                return 0.01  # Stop-loss
        
        # Price breaks below open price by 1.5%
        if current_rate * 1.015 < candle["open"]:
            return 0.01  # Stop-loss
```

### 4.4 Basic Exit Signals (4 signals)

| Signal # | Condition | Signal Name |
|----------|-----------|-------------|
| 1 | Price breaks below MA sell line (smaoffset) | smaoffset_sell_condition_0 |
| 2 | Price breaks above Bollinger Band upper band for 3 consecutive candles | v8_sell_condition_0 |
| 3 | RSI 1h > 80 | v8_sell_condition_1 |
| 4 | Price breaks above Bollinger Band middle band by 1.01x | v9_sell_condition_0 |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Trend Indicators** | EMA 12/26/50/200, SMA 5/200 | Multi-period trend judgment |
| **Momentum Indicators** | RSI (14), MFI (14), EWO | Overbought/oversold judgment |
| **Volatility Indicators** | Bollinger Bands (20, 40), ATR | Volatility and support/resistance |
| **Volume** | volume, volume_mean_slow (30) | Volume contraction confirmation |

### 5.2 Custom Indicators

| Indicator Name | Calculation Method | Purpose |
|---------------|-------------------|---------|
| **EWO** | (EMA5 - EMA35) / close * 100 | Elliot Wave Oscillator, momentum strength |
| **SSL Channel** | ATR-based price channel | 1h trend direction |
| **Bollinger Band Variant** | bbdelta, closedelta, tail | Bollinger Band contraction pattern recognition |

### 5.3 Informational Timeframe Indicators (1 Hour)

- EMA50, EMA100, EMA200
- SMA200 (used to judge 20-period trend decay)
- RSI (14)
- SSL Channels (20-period)

---

## VI. Risk Management Highlights

### 6.1 Time-Based Hard Stop-Loss

The strategy implements tiered processing for losing positions held over 4 hours:

| Condition | Action |
|-----------|--------|
| SMA200 death cross simultaneously | Immediate stop-loss (1% stop-loss line) |
| RSI 1h < 30 | Continue holding, wait for rebound |
| Price breaks below open price by 2.5% AND above EMA200 | Stop-loss |
| Price breaks below open price by 1.5% | Stop-loss |

### 6.2 Stepped ROI Exit

- Early targets are aggressive (20%), suitable for high-volatility pairs
- Later targets are conservative (2.5%), preventing profit retracement

### 6.3 Trailing Stop Protection

- Only enabled after profit reaches a certain threshold
- Two-phase drawdown control, balancing profit protection with holding endurance

---

## VII. Strategy Pros & Cons

### Pros

1. **Multi-Condition Filtering**: 21 independent conditions provide abundant options; can enable/disable for different market environments
2. **Multi-Period Confirmation**: 1-hour informational layer provides higher-perspective trend judgment
3. **Intelligent Stop-Loss**: Dynamic stop-loss logic based on time, trend, and RSI
4. **Flexible Configuration**: buy_minimum_conditions can adjust entry strictness
5. **Volume Filtering**: Multiple conditions include volume contraction requirements, filtering false breakouts

### Cons

1. **Numerous Parameters**: 21 conditions × multiple parameters, high optimization difficulty
2. **Computationally Intensive**: Multi-timeframe + multi-indicator, long backtest/live trading time
3. **Some Conditions Disabled**: V9 series' 10 conditions are all disabled by default, potential overfitting risk
4. **Loose Hard Stop-Loss**: -22.8% is actually managed by custom logic; full understanding required

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **High-volatility pairs** | Enable V8/V6 series | 20% aggressive target suitable for large swings |
| **Mainstream coin stability** | Enable smaoffset series | EWO filtering more suitable for clear trending markets |
| **Ranging markets** | Adjust ROI table | Lower first target to 10-15% |
| **Long-term holding** | Enable V9 series | RSI oversold conditions suitable for bottom-fishing |

---

## IX. Applicable Market Environment Analysis

CoreStrategy is one of the largest and most complex strategies in the Freqtrade ecosystem, integrating the core logic of 4 classic strategies. It performs best in **high-volatility, strong-trend** markets and averages in **low-volatility, long-consolidation** environments.

### 9.1 Core Strategy Logic

- **Multi-Condition Stacking**: Only 1 condition needs to be met to enter, but buy_minimum_conditions can be increased for stricter entry
- **Trend Priority**: Multiple conditions require 1h EMA bullish alignment, ensuring trend-following trades
- **Momentum Confirmation**: EWO, RSI momentum indicators throughout multiple conditions
- **Pullback Entry**: Emphasizes buying at support (Bollinger Band lower band) after price pullback

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|---------:|
| Strong Uptrend | ⭐⭐⭐⭐⭐ | Multi-period EMA confirmation + pullback entry logic |
| Wide-range oscillation | ⭐⭐⭐⭐ | Bollinger Band mean reversion conditions capture swings |
| Downtrend | ⭐⭐⭐ | Some bottom-fishing conditions effective, but overall bullish bias |
| Fast volatility | ⭐⭐⭐⭐ | 20% aggressive target suitable for high volatility |
| Consolidation | ⭐⭐ | Multiple conditions hard to satisfy simultaneously |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| buy_minimum_conditions | 1 | Keep loose to capture more signals |
| minimal_roi."0" | 0.15-0.25 | Adjust based on volatility |
| trailing_stop_positive | 0.005 | Relatively tight trailing trigger threshold |
| ewo_high | 5-8 | Increase to reduce false signals |

---

## X. Summary

**CoreStrategy** is a highly complex multi-condition trend-following strategy that integrates the best of multiple classic strategies from the Freqtrade community. Its core value lies in:

1. **Flexibility**: 21 independently configurable conditions, adapting to various market environments
2. **Multi-Period Perspective**: 1-hour informational layer provides higher-dimensional trend confirmation
3. **Intelligent Risk Control**: Custom stop-loss logic combines time, trend, and momentum dimensions
4. **Community Validated**: Based on multiple live-validated strategies

For quantitative traders, CoreStrategy is suitable for investors with some Freqtrade experience. Start with default configuration, gradually understand and adjust each condition series' enable status, and find the configuration best suited to the current market environment.

**Usage Recommendation**: Start with default parameters for small-capital live trading tests, observe strategy performance across different market environments, then adjust the ROI table and condition enable status based on actual conditions.
