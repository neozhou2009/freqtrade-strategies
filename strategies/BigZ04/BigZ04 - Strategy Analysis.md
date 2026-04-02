# BigZ04 Strategy Analysis

> **Strategy Number**: #59  
> **Strategy Type**: BigZ03 Improved Version with Added Condition 10  
> **Timeframe**: 5 minutes (5m) + Information Timeframe 1h

---

## I. Strategy Overview

BigZ04 is an **improved version** of BigZ03, developed by ilya. This strategy optimizes entry conditions on the basis of BigZ03, adding condition 10 (1-hour oversold + MACD reversal), making signals richer. The strategy maintains the core design philosophy of "low drawdown, quick sell", but provides more entry opportunities through added conditions.

### Core Features

| Feature | Configuration Value |
|---------|-------------------|
| Timeframe | 5 minutes (5m) |
| Information Timeframe | 1 hour (1h) |
| Take-Profit (ROI) | 0-10 min: 2.8%, 10-40 min: 1.8%, 40-180 min: 0.5%, 180+ min: 1.8% |
| Stoploss | -0.99 (use custom stoploss) |
| Trailing Stop | Enabled, positive 1%, trigger offset 2.5% |
| Number of Entry Conditions | 13 (1 more than BigZ03) |
| Recommended Number of Pairs | 2-4 |
| Core Feature | Added Condition 10: 1-hour oversold + MACD reversal |

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
```

### 2.2 Parameter Configuration

BigZ04 maintains the same parameter settings as BigZ03, core difference lies in enabling condition 10:

```python
buy_params = {
    # Condition switches
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
    "buy_condition_10_enable": True,  # [Added] 1-hour oversold + MACD reversal
    "buy_condition_11_enable": False, # Narrow range breakout
    "buy_condition_12_enable": True,  # False breakout pattern
    
    # Core parameters
    "buy_bb20_close_bblowerband_safe_1": 0.989,
    "buy_bb20_close_bblowerband_safe_2": 0.982,
    "buy_volume_pump_1": 0.4,
    "buy_volume_drop_1": 3.8,
    "buy_volume_drop_2": 3.0,
    "buy_volume_drop_3": 2.7,
    "buy_rsi_1h_1": 16.5,
    "buy_rsi_1h_2": 15.0,
    "buy_rsi_1h_3": 20.0,
    "buy_rsi_1h_4": 35.0,
    "buy_rsi_1h_5": 39.0,
    "buy_rsi_1": 28.0,
    "buy_rsi_2": 10.0,
    "buy_rsi_3": 14.2,
    "buy_macd_1": 0.02,
    "buy_macd_2": 0.03,
}
```

### 2.3 Differences from BigZ03

| Feature | BigZ03 | BigZ04 |
|---------|--------|--------|
| Number of Entry Conditions | 12 | **13** |
| Condition 10 Status | Disabled by default | **Enabled by default** |
| Condition 11 Status | Disabled by default | Disabled by default (same) |
| Parameter Configuration | Same | Same (no changes) |

---

## III. Entry Conditions Details

BigZ04 contains **13 entry conditions**, where condition 10 is the newly added core feature.

### Conditions 0-9: Basic Conditions (Same as BigZ03)

Conditions 0-9 are exactly the same as BigZ03, briefly reviewed here:

**Condition 0**: RSI Oversold + Decline Pattern
- Requires price above EMA200
- 5-minute RSI below 30
- 3 candles ago was big bullish (now declining)
- 1-hour RSI below 71

**Condition 1**: Lower Bollinger Band + Bearish Candle
- Price touches lower band (0.989x)
- 1-hour RSI below 69
- Volume contraction

**Condition 2**: Deep Lower Band
- Price breaks below lower band (0.982x)
- Simple and direct

**Condition 3**: Above 1-hour EMA200 + RSI Oversold
- 1-hour level uptrend
- 5-minute RSI below 14.2

**Condition 4**: Extremely Low 1-hour RSI
- 1-hour RSI below 16.5
- Paired with 5-minute lower band

**Condition 5**: MACD Golden Cross + Lower Bollinger Band
- MACD golden cross in progress
- Price simultaneously touches lower band

**Conditions 6-7**: MACD+RSI Combinations
- Different RSI threshold combinations

**Conditions 8-9**: Dual RSI Oversold
- 5-minute and 1-hour RSI simultaneously oversold

### Condition 10: 1-hour Oversold + MACD Reversal (Newly Added Core)

This is BigZ04's core newly added feature, designed to capture large-level trend reversals:

```python
(
    # 1-hour RSI extremely oversold (<35)
    (dataframe["rsi_1h"] < 35.0) &
    
    # 1-hour price below lower Bollinger Band
    (dataframe["close_1h"] < dataframe["bb_lowerband_1h"]) &
    
    # MACD histogram positive (bullish momentum)
    (dataframe["hist"] > 0) &
    
    # 2 candles ago MACD histogram negative (golden cross in progress)
    (dataframe["hist"].shift(2) < 0) &
    
    # 5-minute RSI below 40.5
    (dataframe["rsi"] < 40.5) &
    
    # MACD histogram strong enough (>open price*0.12%)
    (dataframe["hist"] > dataframe["close"] * 0.0012) &
    
    # Bullish confirmation
    (dataframe["open"] < dataframe["close"])
)
```

**Condition 10 Deep Analysis**:

| Element | Requirement | Significance |
|---------|-------------|--------------|
| rsi_1h < 35 | 1-hour RSI oversold | Big cycle oversold |
| close_1h < bb_lowerband_1h | 1-hour price below lower band | Position oversold |
| hist > 0 | MACD histogram positive | Momentum turned bullish |
| hist.shift(2) < 0 | 2 candles ago negative | Golden cross in progress |
| rsi < 40.5 | 5-minute RSI relatively low | Small cycle cooperation |
| hist > close * 0.0012 | MACD histogram strong enough | Rebound has strength |
| open < close | Bullish candle | Close confirmation |

**Condition 10 Design Logic**:

1. **Big Cycle Oversold**: 1-hour RSI below 35 indicates market extremely oversold, high rebound probability
2. **Position Oversold**: Price below lower Bollinger Band is strong oversold signal
3. **Momentum Reversal**: MACD from negative to positive, indicates decline momentum exhausted
4. **Dual Confirmation**: 5-minute RSI also needs to cooperate, but can't be too high (avoid chasing highs)
5. **Strength Verification**: MACD histogram must be strong enough, ensure rebound has sustainable momentum

### Condition 11: Narrow Range Oscillation Breakout (Disabled by Default)

Same as BigZ03, disabled by default.

```python
# Consecutive 10 candles range less than 1%
((dataframe["high"] - dataframe["low"]) < dataframe["open"] / 100)
```

### Condition 12: False Breakout Pattern

```python
(
    (dataframe["close"] < dataframe["bb_lowerband"] * 0.993) &
    (dataframe["low"] < dataframe["bb_lowerband"] * 0.985) &
    (dataframe["close"].shift() > dataframe["bb_lowerband"])
)
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

### 4.2 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.025
```

### 4.3 Custom Stoploss

```python
if holding_time < 50 minutes:
    Don't actively stoploss
else:
    if rsi_1h < 30:  # Note is 30, not 35
        Continue holding
    elif still falling:
        Stoploss
```

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

If 1-hour RSI still very low (< 30) after 50 minutes, continue holding, avoid stoplossing at lowest point.

### 6.3 Volume Protection

All conditions include volume filtering, exclude zombie coins and pumpdump situations.

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Added Condition 10**: Specifically captures big cycle reversals, increases signal source
2. **Multi-Cycle Resonance**: 1-hour judges direction, 5-minute grasps timing
3. **Maintains Simplicity**: Exit logic not complex, easy to understand
4. **Richer Signals**: 13 conditions cover more patterns
5. **Unchanged Parameters**: Same parameters as BigZ03, easy to compare

### ⚠️ Limitations

1. **Increased Signal Volume**: Condition 10 will make trading more frequent
2. **False Reversal Risk**: 1-hour oversold doesn't necessarily rebound immediately
3. **Lagging Entry**: May miss lowest point waiting for MACD golden cross
4. **Many Conditions Hard to Analyze**: 13 conditions, don't know which makes money

---

## VIII. Applicable Scenarios

### 8.1 Recommended Scenarios

- **Rebound after big drop**
- **Wide range oscillation**
- **High liquidity major coins**

### 8.2 Not Recommended Scenarios

- **Sideways range market** (easily repeatedly stopped out)
- **Continuous decline market** (each oversold may continue falling)
- **Low volatility coins** (difficult to trigger take-profit)

---

## IX. Summary

BigZ04 is a **"condition enhanced"** version of BigZ03, achieving "more signal sources" through added condition 10.

**Key Points**:
- ✅ Added condition 10, specifically captures big cycle reversals
- ✅ Multi-cycle resonance, 1-hour judges direction, 5-minute grasps timing
- ✅ Maintains simplicity, exit logic not complex
- ⚠️ Signal volume increases, trading more frequent
- ⚠️ May miss lowest point, lagging entry

**Usage Recommendations**:
1. First understand BigZ03: Understand basic version
2. Focus on condition 10: Observe performance of newly added condition
3. Monitor trading frequency: Condition 10 will increase trades
4. Compare with BigZ03: Run both versions simultaneously, compare effects

---

*This document is based on BigZ04 strategy source code, for learning reference only, not investment advice.*
