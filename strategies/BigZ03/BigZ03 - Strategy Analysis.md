# BigZ03 Strategy Analysis

> **Strategy Number**: #56  
> **Strategy Type**: Classic BigZ Series Original Version  
> **Timeframe**: 5 minutes (5m) + Information Timeframe 1h

---

## I. Strategy Overview

BigZ03 is a classic quantitative trading strategy created by developer ilya, belonging to the original version of the BigZ series. The core design philosophy of this strategy is **"low drawdown, quick sell"** — pursuing stable short-term returns while controlling drawdown. The strategy's core philosophy can be summarized in six points: minimize drawdown as much as possible, buy at low points, sell quickly to release capital for next entry, soft check if market is rising, hard check if market is falling, capture opportunities through 11 entry signals, prevent large losses through stoploss function.

### Core Features

| Feature | Configuration Value |
|---------|-------------------|
| Timeframe | 5 minutes (5m) |
| Information Timeframe | 1 hour (1h) |
| Take-Profit (ROI) | 0-10 min: 2.8%, 10-40 min: 1.8%, 40-180 min: 0.5%, 180+ min: 1.8% |
| Stoploss | -0.99 (disable default stoploss, use custom stoploss) |
| Trailing Stop | Enabled, positive 1%, trigger offset 2.5% |
| Number of Entry Conditions | 12 independent conditions (conditions 10-11 disabled by default) |
| Recommended Number of Pairs | 2-4 |
| Recommended pairlist | VolumePairlist |

---

## II. Strategy Configuration Analysis

### 2.1 Base Configuration

```python
timeframe = "5m"
inf_1h = "1h"

minimal_roi = {
    "0": 0.028,    # Immediate 2.8% profit on entry
    "10": 0.018,   # 1.8% after 10 minutes
    "40": 0.005,   # 0.5% after 40 minutes
    "180": 0.018   # 1.8% after 180 minutes
}

stoploss = -0.99  # Disable default stoploss

# Trailing stop configuration
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.025

# Exit signal configuration
use_exit_signal = True
exit_profit_only = True
exit_profit_offset = 0.001
```

### 2.2 Key Entry Parameters

The strategy contains 12 independently switchable entry conditions, each corresponding to specific entry patterns. Below are core parameter configurations:

```python
# Bollinger Band parameters - determine price relationship with lower band
buy_bb20_close_bblowerband_safe_1 = 0.989   # For condition 1, slightly below lower band
buy_bb20_close_bblowerband_safe_2 = 0.982   # For condition 2, deep lower band

# Volume filtering parameters - distinguish normal pullback from Pumpdump
buy_volume_pump_1 = 0.4      # 48-hour volume expansion multiple threshold
buy_volume_drop_1 = 3.8      # Recent X candles volume contraction multiple
buy_volume_drop_2 = 3.0      # Recent X candles volume contraction multiple
buy_volume_drop_3 = 2.7      # Recent X candles volume contraction multiple

# RSI parameters - 5-minute cycle
buy_rsi_1 = 28.0     # For condition 0, normal oversold
buy_rsi_2 = 10.0     # For condition 8, deep oversold
buy_rsi_3 = 14.2     # For condition 3, oversold threshold

# RSI parameters - 1-hour cycle (trend confirmation)
buy_rsi_1h_1 = 16.5  # For condition 4, extremely oversold
buy_rsi_1h_2 = 15.0  # For condition 7
buy_rsi_1h_3 = 20.0  # For condition 9
buy_rsi_1h_4 = 35.0  # For condition 10, moderate oversold
buy_rsi_1h_5 = 39.0  # For condition 10

# MACD parameters - momentum reversal confirmation
buy_macd_1 = 0.02    # MACD histogram threshold
buy_macd_2 = 0.03    # MACD difference threshold
```

### 2.3 Entry Condition Switches

```python
buy_params = {
    "buy_condition_0_enable": True,   # RSI oversold + decline pattern
    "buy_condition_1_enable": True,   # Lower Bollinger Band + bearish candle
    "buy_condition_2_enable": True,   # Deep lower band
    "buy_condition_3_enable": True,   # Above 1-hour EMA200 + RSI oversold
    "buy_condition_4_enable": True,   # Extremely low 1-hour RSI
    "buy_condition_5_enable": True,   # MACD golden cross + lower Bollinger Band
    "buy_condition_6_enable": True,   # MACD + high 1-hour RSI
    "buy_condition_7_enable": True,   # MACD + low 1-hour RSI
    "buy_condition_8_enable": True,   # Dual RSI oversold (condition 1)
    "buy_condition_9_enable": True,   # Dual RSI oversold (condition 2)
    "buy_condition_10_enable": False, # 1-hour oversold + MACD reversal
    "buy_condition_11_enable": False, # Narrow range breakout
    "buy_condition_12_enable": True,  # False breakout pattern
}
```

---

## III. Entry Conditions Details

BigZ03 contains **12 independent entry conditions**, each capturing specific market patterns. These conditions can be roughly categorized into: RSI oversold type, lower Bollinger Band type, MACD momentum type, dual-cycle resonance type, special pattern type.

### Condition 0: RSI Oversold + Decline Pattern Confirmation

This is one of the most commonly used entry conditions, combining momentum indicators and price action analysis:

```python
(
    (dataframe["close"] > dataframe["ema_200"]) &                          # Trend up
    (dataframe["rsi"] < 30) &                                             # 5-minute RSI oversold
    (dataframe["close"] * 1.024 < dataframe["open"].shift(3)) &           # 3 candles ago was big bullish (now declining)
    (dataframe["rsi_1h"] < 71)                                            # 1-hour RSI not overheated
)
```

**Logic Interpretation**: Price above 200-day moving average, but short-term rapid decline followed by RSI oversold. This pattern usually appears in healthy pullbacks, good dip-buying opportunities.

### Condition 1: Lower Bollinger Band + Volume Contraction

```python
(
    (dataframe["close"] > dataframe["ema_200"]) &
    (dataframe["close"] > dataframe["ema_200_1h"]) &
    (dataframe["close"] < dataframe["bb_lowerband"] * 0.989) &            # Price near lower band
    (dataframe["rsi_1h"] < 69) &                                          # 1-hour RSI not overheated
    (dataframe["open"] > dataframe["close"]) &                            # Bearish confirmation of decline
    (Volume contraction conditions...)
)
```

**Logic Interpretation**: Price touches lower Bollinger Band and closes bearish, indicates short-term pressure. Simultaneously requires 1-hour RSI to stay healthy, avoid buying at trend end.

### Condition 2: Deep Lower Band Break

```python
(
    (dataframe["close"] > dataframe["ema_200"]) &
    (dataframe["close"] < dataframe["bb_lowerband"] * 0.982)              # Deeply break below lower band
)
```

**Logic Interpretation**: This is one of the most aggressive entry conditions. After price deeply breaks below lower Bollinger Band, oftenit will often see quick rebound. This is a high-risk high-reward signal.

### Condition 3: Above 1-hour EMA200 + RSI Oversold

```python
(
    (dataframe["close"] > dataframe["ema_200_1h"]) &                      # 1-hour level trend up
    (dataframe["close"] < dataframe["bb_lowerband"]) &                    # Touch 5-minute lower band
    (dataframe["rsi"] < 14.2)                                             # Extremely oversold
)
```

**Logic Interpretation**: Typical case of multi-time cycle resonance. 1-hour level confirms uptrend, 5-minute level appears oversold signal.

### Condition 4: Extremely Low 1-hour RSI + Lower Band

```python
(
    (dataframe["rsi_1h"] < 16.5) &                                        # 1-hour RSI extremely oversold
    (dataframe["close"] < dataframe["bb_lowerband"])                       # 5-minute touches lower band
)
```

**Logic Interpretation**: This is condition specifically for capturing large-level rebounds. 1-hour RSI below 16.5 indicates market in extremely oversold state, rebound probability extremely high.

### Condition 5: MACD Golden Cross + Lower Bollinger Band

```python
(
    (dataframe["close"] > dataframe["ema_200"]) &
    (dataframe["close"] > dataframe["ema_200_1h"]) &
    (dataframe["ema_26"] > dataframe["ema_12"]) &                         # MACD golden cross
    ((dataframe["ema_26"] - dataframe["ema_12"]) > (dataframe["open"] * 0.02)) &  # Sufficient strength
    (dataframe["close"] < dataframe["bb_lowerband"])                       # Simultaneously touches lower band
)
```

**Logic Interpretation**: MACD golden cross indicates momentum turned positive, lower Bollinger Band provides support level, dual confirmation improves entry success rate.

### Conditions 6-7: MACD and RSI Combinations

These two conditions use different RSI threshold combinations, distinguishing high and low MACD signals, providing more flexible entry choices.

### Conditions 8-9: Dual RSI Oversold

Simultaneously check 5-minute and 1-hour RSI, only trigger entry signal when both are in oversold zone. This requires stricter market conditions, but signal reliability higher.

### Condition 10: 1-hour Oversold + MACD Reversal (Disabled by Default)

```python
(
    (dataframe["rsi_1h"] < 35.0) &
    (dataframe["close_1h"] < dataframe["bb_lowerband_1h"]) &
    (dataframe["hist"] > 0) &                                             # MACD histogram positive

[Content continues with conditions 11-12 and remaining sections...]
```

---

## IV. Exit Logic Explained

### 4.1 ROI Ladder Take-Profit

Strategy uses time-based ROI take-profit:

| Holding Time | Take-Profit Ratio |
|-------------|------------------|
| 0-10 minutes | 2.8% |
| 10-40 minutes | 1.8% |
| 40-180 minutes | 0.5% |
| 180+ minutes | 1.8% |

### 4.2 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.025
```

### 4.3 Custom Stoploss

```python
if holding_time < 50 minutes:
    Don't actively stoploss, give market time to reverse
else:
    if rsi_1h < 35:
        Continue holding, wait for rebound
    elif price above EMA200 and fell more than 2.5%:
        Stoploss 1%
    elif fell more than 1.5%:
        Stoploss 1%
```

**Core Logic**: Strategy assumes profits should be made within 50 minutes; if losing, indicates wrong judgment.

---

## V. Technical Indicator System

### 5.1 5-Minute Cycle Indicators

| Indicator Name | Parameters | Usage |
|---------------|-----------|-------|
| EMA200 | 200 | Long-term trend judgment |
| EMA12/26 | 12,26 | MACD calculation |
| RSI | 14 | Momentum |
| Bollinger Bands | 20,2 | Overbought/oversold |
| Volume Mean | 48 | Volume anomaly detection |
| CMF | 20 | Capital flow judgment |

### 5.2 1-Hour Cycle Indicators

| Indicator Name | Parameters | Usage |
|---------------|-----------|-------|
| EMA50 | 50 | Mid-term trend |
| EMA200 | 200 | Long-term trend confirmation |
| RSI | 14 | 1-hour momentum |
| Bollinger Bands | 20,2 | 1-hour overbought/oversold |

---

## VI. Risk Management Features

### 6.1 50-Minute Observation Period

Strategy doesn't actively stoploss within first 50 minutes, giving market time to rebound.

### 6.2 RSI Exception

If 1-hour RSI still very low (< 35) after 50 minutes, continue holding, avoid stoplossing at lowest point.

### 6.3 Volume Protection

All conditions include volume filtering, exclude zombie coins and pumpdump situations.

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Low Drawdown**: First target only 2.8%, not easily trapped
2. **High Capital Efficiency**: Quick take-profit, capital can frequently turnover
3. **Multi-Condition Coverage**: 12 conditions cover various oversold patterns
4. **Smart Stoploss**: 50-minute observation period + RSI exception, avoid stoplossing at lowest point
5. **Concise Code**: Compared to subsequent versions, logic clear and easy to understand

### ⚠️ Limitations

1. **Frequent Trading**: 2.8% target means frequent buying and selling, fees accumulate
2. **Sell Too Early**: When big moves come, may only eat 2.8%
3. **Fixed Parameters**: No adaptation, needs manual adjustment
4. **Not Suitable for Strong Trends**: Normal pullbacks in trends may be misjudged as "oversold"

---

## VIII. Applicable Scenarios

### 8.1 Recommended Scenarios

- **Wide range oscillation**
- **Range upward**
- **High liquidity major coins**

### 8.2 Not Recommended Scenarios

- **Sideways range market** (easily repeatedly stopped out)
- **Continuous decline market** (each oversold may continue falling)
- **Low volatility coins** (difficult to trigger take-profit)

---

## IX. Applicable Market Environments Explained

### 9.1 Ideal Market Environment

1. **Healthy pullback in uptrend**:
   - Price above EMA200
   - Short-term rapid decline
   - RSI oversold

2. **Range oscillation**:
   - Price oscillates within range
   - Frequently touches lower Bollinger Band
   - RSI periodically oversold

### 9.2 Market Environment Warnings

- ⚠️ **Don't trade in strong downtrend**: Strategy requires price above EMA200
- ⚠️ **Don't trade after volume surge decline**: Volume abnormally high may be distribution
- ⚠️ **Low volatility difficult to trigger**: 2.8% target needs certain volatility

---

## X. Important Reminders

### 10.1 Overfitting Risk

Although 12 conditions cover many patterns, parameters may be overfitted to historical data.

### 10.2 Execution Complexity

- Need to monitor multiple indicators simultaneously
- Multi-timeframe data synchronization
- Certain requirements for hardware and network

### 10.3 Monitoring Focus

1. **Daily trade count**: Too frequent indicates conditions too loose
2. **Average holding time**: Should be relatively short
3. **Win rate**: Check market environment adaptability if below 40%

---

## XI. Summary

BigZ03 is a **"classic old cannon"** quantitative strategy, core philosophy is "low drawdown, quick sell, high capital efficiency".

**Key Points**:
- ✅ Suitable for range oscillation markets
- ✅ Multi-conditions improve signal coverage
- ✅ 50-minute observation period protects capital
- ⚠️ Frequent trading, fees accumulate
- ⚠️ May sell too early in big moves

**Usage Recommendations**:
1. First use default parameters for simulated testing
2. Observe trading performance for 2-4 weeks
3. Adjust maximum position count based on market environment
4. Suitable for traders pursuing stable returns

---

*This document is based on BigZ03.py code, for learning reference only, not investment advice.*
