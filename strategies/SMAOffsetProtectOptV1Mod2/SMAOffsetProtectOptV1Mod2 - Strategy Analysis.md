# SMAOffsetProtectOptV1Mod2 Strategy Analysis

> **Strategy Number**: #364 (364th of 465 strategies)  
> **Strategy Type**: SMA Offset + EWO Protection + RSI Filter + Antipump Protection Trend Following Strategy  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

SMAOffsetProtectOptV1Mod2 is an upgraded version of SMAOffsetProtectOptV1Mod, adding an "Antipump Protection" mechanism on top of the original foundation. By calculating price momentum strength (pump_strength), the strategy can identify and avoid buying after abnormal price pumps, thereby reducing the risk of being trapped. It also includes a sub-strategy `SMAOffsetProtectOptV1Mod2_antipump`, which can independently enable full antipump functionality.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signals + optional antipump protection |
| **Sell Conditions** | 1 base sell signal + four-tier ROI take-profit + trailing stop |
| **Protection Mechanism** | EWO high/low threshold protection + RSI filter + antipump protection |
| **Timeframe** | Main timeframe 5m + informative timeframe 1h |
| **Dependencies** | talib, numpy, pandas, technical (ftt), qtpylib |
| **Sub-strategy** | SMAOffsetProtectOptV1Mod2_antipump |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table (four-tier declining)
minimal_roi = {
    "0": 0.028,    # Immediate: 2.8%
    "10": 0.018,   # After 10 candles: 1.8%
    "30": 0.010,   # After 30 candles: 1.0%
    "40": 0.005    # After 40 candles: 0.5%
}

# Stop loss settings
stoploss = -0.10  # Fixed stop loss 10%

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.001      # Activate trailing after 0.1% profit
trailing_stop_positive_offset = 0.01  # Start trailing at 1% profit
trailing_only_offset_is_reached = True  # Only enable after offset is reached
```

**Design Philosophy**:
- ROI uses a four-tier stepped declining design, more refined than Mod1
- Trailing stop settings are the same as Mod1, conservative but protective
- Fixed 10% stop loss provides the last line of defense

### 2.2 Order Type Configuration

```python
use_sell_signal = True        # Enable sell signal
sell_profit_only = True       # Only use sell signal when profitable
sell_profit_offset = 0.01     # Minimum profit requirement for sell signal: 1%
ignore_roi_if_buy_signal = False  # Do not ignore ROI
```

### 2.3 Comparison with Mod1

| Feature | Mod1 | Mod2 |
|---------|------|------|
| ROI Tiers | 3 tiers | 4 tiers |
| Antipump Protection | None | Yes (pump_strength) |
| Additional Indicators | None | ZEMA 30/200 |
| Sub-strategy | None | antipump subclass |
| startup_candle_count | 30 | 200 |

---

## III. Buy Conditions Detailed

### 3.1 Optimizable Parameters

| Parameter Type | Parameter Name | Default | Optimization Range | Description |
|----------------|----------------|---------|-------------------|-------------|
| **Buy** | base_nb_candles_buy | 16 | 5-80 | EMA period |
| **Buy** | low_offset | 0.973 | 0.9-0.99 | Price offset coefficient |
| **Buy** | ewo_high | 5.672 | 2.0-12.0 | EWO high threshold |
| **Buy** | ewo_low | -19.931 | -20.0 to -8.0 | EWO low threshold |
| **Buy** | rsi_buy | 59 | 30-70 | RSI buy threshold |
| **Buy** | antipump_threshold | 0.25 | 0-0.4 | Antipump threshold |
| **Sell** | base_nb_candles_sell | 20 | 5-80 | Sell EMA period |
| **Sell** | high_offset | 1.010 | 0.99-1.1 | Sell price offset |

### 3.2 Buy Conditions Detailed

#### Condition #1: Trend Confirmation Buy
```python
# Logic
- Price below EMA * low_offset (pullback buy)
- EWO > ewo_high (strong trend confirmation)
- RSI < rsi_buy (not overbought)
- Volume > 0 (validity check)
```

**Core Logic**: Exactly the same as Mod1, waiting for pullback buying opportunities after trend confirmation.

#### Condition #2: Deep Oversold Buy
```python
# Logic
- Price below EMA * low_offset (pullback buy)
- EWO < ewo_low (deeply negative)
- Volume > 0 (validity check)
```

**Core Logic**: Exactly the same as Mod1, capturing rebound opportunities after extreme oversold conditions.

### 3.3 Antipump Protection Mechanism (antipump)

The core new functionality in Mod2, calculation logic as follows:

```python
# Calculate price momentum strength
zema_30 = ftt.zema(dataframe, period=30)
zema_200 = ftt.zema(dataframe, period=200)
pump_strength = (zema_30 - zema_200) / zema_30
```

**Antipump Logic** (only effective in antipump sub-strategy):
```python
dont_buy_conditions.append(
    (dataframe['pump_strength'] > self.antipump_threshold.value)
)
```

**Interpretation**:
- When pump_strength > antipump_threshold, buying is prohibited
- Default threshold is 0.25, meaning when short-term ZEMA is 25% higher than long-term ZEMA, it's considered abnormal
- Avoids chasing highs after a pump

### 3.4 Buy Condition Classification

| Condition Group | Condition Number | Core Logic | Antipump Protection |
|-----------------|------------------|------------|---------------------|
| Trend Following | Condition #1 | High EWO + RSI filter | Effective in sub-strategy |
| Contrarian Bottom Fishing | Condition #2 | Low EWO + no RSI limit | Effective in sub-strategy |

---

## IV. Sell Logic Detailed

### 4.1 Four-Tier Take Profit System

The strategy uses a four-tier ROI take-profit mechanism (one more tier than Mod1):

```
Holding Time    Target Profit    Description
────────────────────────────────
Immediate       2.8%             Highest profit target
10 candles     1.8%             Short-term profit target
30 candles     1.0%             Medium-term profit target
40 candles     0.5%             Lowest profit target
```

**Design Philosophy**:
- One more "10 candles" intermediate tier than Mod1
- More refined profit management, avoiding premature selling or excessive waiting

### 4.2 Trailing Stop Mechanism

| Parameter | Value | Description |
|-----------|-------|-------------|
| trailing_stop | True | Enable trailing stop |
| trailing_stop_positive | 0.1% | Trailing distance |
| trailing_stop_positive_offset | 1% | Activation threshold |
| trailing_only_offset_is_reached | True | Only enable after threshold reached |

### 4.3 Base Sell Signal (1)

```python
# Sell signal 1: EMA offset sell
- Price > EMA(base_nb_candles_sell) * high_offset
- Volume > 0
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Trend | EMA (base_nb_candles_buy) | Buy baseline |
| Trend | EMA (base_nb_candles_sell) | Sell baseline |
| Trend | ZEMA 30 | Short-term momentum (antipump) |
| Trend | ZEMA 200 | Long-term trend (antipump) |
| Oscillator | EWO (50, 200) | Trend strength assessment |
| Oscillator | RSI (14) | Overbought/oversold filter |
| Risk | pump_strength | Pump strength detection |

### 5.2 ZEMA (Zero Lag EMA) Detailed

Mod2 introduces ZLEMA (Zero Lag EMA) to calculate pump_strength:

```python
zema_30 = ftt.zema(dataframe, period=30)   # Short-term zero-lag EMA
zema_200 = ftt.zema(dataframe, period=200)  # Long-term zero-lag EMA
pump_strength = (zema_30 - zema_200) / zema_30
```

**Advantages**:
- ZLEMA reduces lag compared to traditional EMA
- Faster response to price changes
- More accurate identification of short-term pump behavior

### 5.3 pump_strength Interpretation

| pump_strength Value | Market State | Strategy Suggestion |
|--------------------|--------------|---------------------|
| < 0 | Short-term below long-term | Downtrend or pullback |
| 0 - 0.1 | Normal uptrend | Normal trading |
| 0.1 - 0.25 | Strong uptrend | Watch for risk |
| > 0.25 | Abnormal pump | Prohibit buying (antipump) |

---

## VI. Risk Management Features

### 6.1 EWO Protection Mechanism

Same EWO protection as Mod1:

| Protection Type | Parameter Description | Default |
|-----------------|----------------------|---------|
| EWO high threshold | Strong trend confirmation | 5.672 |
| EWO low threshold | Extreme oversold identification | -19.931 |

### 6.2 Antipump Protection Mechanism (New)

```python
antipump_threshold = DecimalParameter(0, 0.4, default=0.25)
```

**Design Philosophy**:
- Identifies abnormal short-term price increases
- Avoids chasing highs after pumps and getting trapped
- Only effective in `SMAOffsetProtectOptV1Mod2_antipump` sub-strategy

### 6.3 RSI Filter Mechanism

Same RSI filtering as Mod1:
- RSI < rsi_buy ensures not buying in overbought territory
- Only applied to trend confirmation buys (Condition #1)

### 6.4 Volume Verification

All buy and sell conditions require `volume > 0`.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Antipump Protection**: New pump_strength indicator, avoids chasing highs and getting trapped
2. **More Refined ROI**: Four tiers, more flexible profit management
3. **Sub-strategy Design**: Can choose to enable/disable antipump functionality
4. **Zero Lag Indicator**: ZEMA responds faster than EMA

### ⚠️ Limitations

1. **Increased Complexity**: Added ZEMA and pump_strength calculations compared to Mod1
2. **More Parameters**: Parameters to optimize increased from 7 to 8
3. **Antipump May Filter Opportunities**: True strong breakouts may also be mistakenly judged as pumps
4. **startup_candle_count increased to 200**: Requires more historical data

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|---------------------------|-------------|
| Normal Trend | Mod2 base version | No need for antipump protection |
| Abnormal Volatility | antipump sub-strategy | Enable antipump protection |
| High-risk Pairs | antipump + low threshold | Stricter protection |
| Low-volatility Pairs | Base version or high threshold | Avoid over-filtering |

---

## IX. Applicable Market Environment Detailed

SMAOffsetProtectOptV1Mod2 is an upgraded version of SMAOffsetProtectOptV1Mod, adding an antipump protection mechanism. It performs best in **markets with clear trends but occasional pumps**, while performing poorly in **continuously pumping or continuously falling markets**.

### 9.1 Core Strategy Logic

- **Trend Pullback Buy**: Wait for price to pull back below EMA before buying
- **Dual Protection**: EWO confirms trend + RSI filters overbought
- **Antipump Protection**: Identify abnormal pumps through pump_strength
- **Trailing Take Profit**: Activate trailing stop after 1% profit

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|-------------|-------------------|------------------|
| 📈 Normal Uptrend | ⭐⭐⭐⭐⭐ | Pullback buy + trailing take profit + antipump protection |
| 🚀 Fast Pump | ⭐⭐⭐⭐☆ | antipump can avoid chasing highs (sub-strategy) |
| 🔄 Ranging/Sideways | ⭐⭐☆☆☆ | EMA false breakout issues still exist |
| 📉 Downtrend | ⭐☆☆☆☆ | Long-only, cannot profit |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|------------------|-------------|
| antipump_threshold | 0.2-0.3 | Adjust based on pair volatility |
| base_nb_candles_buy | 16-25 | Use longer period for trending markets |
| trailing_stop_positive_offset | 0.01-0.02 | Adjust based on pair volatility |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Cost

This strategy has approximately 200 lines of code (including sub-strategy), medium-high complexity:
- Need to understand EWO indicator principles
- Need to understand EMA offset strategy logic
- Need to understand ZEMA and pump_strength
- Need to master HyperOpt parameter optimization

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

**Note**: startup_candle_count = 200, much higher than Mod1's 30, requires more historical data.

### 10.3 Differences Between Backtesting and Live Trading

- Backtesting may perform too well due to parameter fitting
- Antipump parameters need adjustment for different pairs
- Live trading slippage and fees will reduce returns

### 10.4 Recommendations for Manual Traders

Manual traders can learn from:
- pump_strength indicator to identify pumps
- ZEMA responds faster to trends than EMA
- Combine with EWO for trend strength judgment

---

## XI. Summary

**SMAOffsetProtectOptV1Mod2** is an evolved version of SMAOffsetProtectOptV1Mod, with core upgrades:

1. **Antipump Protection**: Identifies abnormal pumps through pump_strength, avoids chasing highs and getting trapped
2. **More Refined ROI**: Four-tier stepped take-profit, more flexible profit management
3. **Sub-strategy Design**: Can choose to enable antipump functionality, flexibly adapting to different markets

For quantitative traders, this is a strategy with added risk protection on top of Mod1, suitable for traders concerned about pump risks. However, pay attention to antipump parameter tuning to avoid over-filtering normal opportunities.

---