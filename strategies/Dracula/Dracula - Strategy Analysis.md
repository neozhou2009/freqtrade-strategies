# Dracula Strategy: In-Depth Analysis

> **Strategy Number**: #151 (151st of 465 strategies)  
> **Strategy Type**: Bollinger Band Support/Resistance + Money Flow Multi-Condition Strategy  
> **Timeframe**: 1 Minute (1m) + 5 Minute Informational Layer

---

## I. Strategy Overview

**Dracula** is a complex multi-condition buy strategy developed by author 6h057. The core logic is based on Bollinger Band support/resistance identification, Chaikin Money Flow (CMF) indicator, and EMA trend confirmation — buying when the price touches the lower Bollinger Band and money is flowing in.

### Key Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signal groups |
| **Sell Conditions** | 5 custom exit signals (via custom_exit) |
| **Protection** | 1 set of buy protection parameters (stoploss protection) |
| **Timeframe** | 1 minute (main) + 5 minutes (informational layer) |
| **Dependencies** | TA-Lib, ta, numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table (time: minutes)
minimal_roi = {
    "0": 0.10,     # Immediate exit: 10% profit
    "30": 0.05,    # After 30 minutes: 5% profit
    "60": 0.02     # After 60 minutes: 2% profit
}

# Stoploss Settings
stoploss = -0.20   # -20% hard stoploss

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01        # 1% profit triggers trailing
trailing_stop_positive_offset = 0.03  # 3% offset triggers exit
```

**Design Philosophy**:
- **High initial ROI**: The 10% initial ROI indicates the strategy expects to capture large swings
- **Moderate stoploss**: -20% hard stoploss allows moderate volatility room
- **Aggressive trailing**: Trailing activates at 1% profit, but only triggers at 3% offset — suitable for trend continuation

### 2.2 Order Type Configuration

```python
# Using Freqtrade default configuration
order_types = {
    "entry": "limit",
    "exit": "limit",
    "stoploss": "market",
    "stoploss_on_exchange": False
}
```

---

## III. Entry Conditions Details

### 3.1 Protection Mechanism

The strategy has a built-in "stoploss protection" mechanism (`lost_protect`):

```python
lost_protect = (dataframe["ema"] > (dataframe["close"] * 1.07)).rolling(10).sum() == 0
```

**Protection Logic**: Over the past 10 candles, EMA has never been above 107% of the close price, ensuring no chasing after a significant rally.

### 3.2 Buy Condition Groups

#### Condition #1: Bollinger Lower Band Breakout + Money Inflow + Support Confirmation

```python
item_buy_logic = []
item_buy_logic.append(dataframe["volume"] > 0)                     # Has volume
item_buy_logic.append(dataframe["cmf"] > 0)                        # CMF > 0 (money inflow)
item_buy_logic.append(prev["bb_bbl_i"] == 1)                       # Previous candle touched lower band
item_buy_logic.append(prev["close"] >= prev1["support"])           # Price not below support
item_buy_logic.append(prev["ema"] < prev["close"])                 # EMA in downward trend
item_buy_logic.append((dataframe["open"] < dataframe["close"]))    # Current candle bullish
item_buy_logic.append(prev["open"] > prev["close"])                # Previous candle bearish (hammer pattern)
item_buy_logic.append((dataframe["bb_bbt"] > self.buy_bbt.value))  # Bollinger band width condition met
item_buy_logic.append(lost_protect)                                # Stoploss protection
```

#### Condition #2: Bollinger Lower Band Breakout + Direct Support

```python
item_buy_logic = []
item_buy_logic.append(dataframe["volume"] > 0)
item_buy_logic.append(dataframe["cmf"] > 0)
item_buy_logic.append(dataframe["bb_bbl_i"] == 1)                  # Current candle touched lower band
item_buy_logic.append(dataframe["open"] >= prev1["support"])      # Open price above support
item_buy_logic.append(prev["ema"] < prev["close"])
item_buy_logic.append((dataframe["open"] < dataframe["close"]))
item_buy_logic.append((dataframe["bb_bbt"] > self.buy_bbt.value))
item_buy_logic.append(lost_protect)
```

### 3.3 Core Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| buy_bbt | 0.023 | Bollinger band width threshold |
| ewo_high | 5.638 | EWO high threshold |
| ewo_low | -19.993 | EWO low threshold |
| low_offset | 0. | Buy price offset |
| rsi_buy | 61 | RSI buy threshold |

---

## IV. Exit Conditions Details

### 4.1 Custom Exit Signals

The strategy implements complex exit logic via the `custom_exit` function:

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| Resistance reversal | Previous candle broke upper band + current candle bearish + near resistance | sell_signal_1 |
| Strong reversal | Current candle broke upper band + current candle bearish + far from resistance | sell_signal_2 |
| Trend reversal | Current candle bearish + EMA above close by 107% | stop_loss |
| Lower Bollinger Band | Current candle bearish + near lower band + has profit | take_profit |
| SMA signal | Buy tag contains "sma" + profit >= 1% | sma |
| SMA stoploss | Buy tag contains "sma" + price above EMA49*high_offset | stop_loss_sma |

### 4.2 ROI Exit Priority

| Holding Time | Minimum Profit | Exit Triggered |
|-------------|----------------|----------------|
| 0 minutes | 10% | Exits immediately |
| 30 minutes | 5% | Exits if reached after 30 min |
| 60 minutes | 2% | Exits if reached after 60 min |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Category | Indicator | Parameters | Purpose |
|----------|-----------|------------|---------|
| **Trend** | EMA | 150 period | Long-term trend judgment |
| **Volatility** | Bollinger Bands | 20 period, 2x std dev | Support/resistance |
| **Money Flow** | CMF (Chaikin Money Flow) | 20 period | Money inflow/outflow |
| **Momentum** | RSI | 14 period | Overbought/oversold auxiliary |

### 5.2 Custom Indicators

The strategy contains two custom classes:

1. **SupResFinder**: Support/Resistance Identifier
   - `isSupport()`: Identifies support levels
   - `isResistance()`: Identifies resistance levels
   - `getSupport()`: Gets support level series
   - `getResistance()`: Gets resistance level series

2. **EWO**: Elliot Wave Oscillator (simplified)
   ```python
   def EWO(dataframe, ema_length=5, ema2_length=35):
       ema1 = ta.EMA(df, timeperiod=ema_length)
       ema2 = ta.EMA(df, timeperiod=ema2_length)
       emadif = (ema1 - ema2) / df["close"] * 100
       return emadif
   ```

---

## VI. Risk Management Features

### 6.1 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_stop_positive = 0.01      # Activates after 1% profit
trailing_stop_positive_offset = 0.03  # Triggers on 3% pullback from high
trailing_only_offset_is_reached = True  # Only trails after activation point
```

**How It Works**:
1. After profit reaches 1%, trailing stop activates
2. Exit triggered when price pulls back 3% from the highest point
3. Suitable for capturing trending continuation moves

### 6.2 Hard Stoploss Protection

```python
stoploss = -0.20  # -20%
```

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Multi-condition confirmation**: Buy requires multiple conditions (CMF, support, trend, etc.), high signal quality
2. **Money flow filtering**: CMF > 0 ensures money inflow, reduces false breakouts
3. **Support/resistance integration**: SupResFinder dynamically identifies support and resistance
4. **Complete protection**: lost_protect prevents chasing after rallies
5. **Custom exits**: 5 different exit scenarios covering various situations

### ⚠️ Cons

1. **Low signal frequency**: Complex conditions mean fewer trading opportunities
2. **Timeframe too short**: 1-minute candles have high noise, prone to false signals
3. **No trend filtering**: No EMA200-style trend judgment, may trade against the trend
4. **Many parameters**: buy_bbt, ewo_high, ewo_low require careful optimization

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Config | Notes |
|-------------------|-------------------|-------|
| **High volatility coins** | Default config | Bollinger band strategies suit high volatility |
| **Trending markets** | Enable trailing stop | Capture trend continuation |
| **Sideways oscillation** | Reduce trading pairs | Signal quality first |
| **Low volatility markets** | Pause usage | Bollinger bands narrow, no trading opportunities |

---

## IX. Applicable Market Environments in Detail

Dracula is a mean reversion + money flow strategy based on support/resistance levels.

### 9.1 Core Strategy Logic

- **Buy at Bollinger lower band**: Buy when price touches lower band, extreme oversold
- **Money flow confirmation**: CMF > 0 confirms money inflow, improves signal quality
- **Support level verification**: Buy price not below dynamically calculated support
- **Multi-scenario exits**: Different exit signals triggered based on market conditions

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---:|:---|
| 📈 Slow bull / oscillating upward | ★★★★☆ (Good) | Money flow confirmation catches upward trends |
| 🔄 Wide-range oscillation | ★★★★★ (Best) | Bollinger band support/resistance works best in ranges |
| 📉 One-way crash | ★★☆☆☆ (Poor) | Support levels may fail, continuously making new lows |
| ⚡️ Extreme consolidation | ★★★☆☆ (Fair) | Bollinger bands narrow, fewer signals |

### 9.3 Key Configuration Recommendations

| Config Item | Recommended Value | Notes |
|-------------|-------------------|-------|
| **Number of trading pairs** | 20-40 USDT pairs | Few signals, need more pairs |
| **Max open trades** | 3-5 orders | Strict conditions, don't over-allocate |
| **Timeframe** | 1m (recommend changing to 5m) | 1m noise too high |
| **Stoploss** | -20% | Keep default |

---

## X. Important Notes: The Cost of Complexity

### 10.1 Learning Curve

The strategy contains approximately 300 lines of code with custom classes and methods, a steep learning curve. Recommended approach:

1. First understand the support/resistance calculation logic of SupResFinder
2. Understand the CMF money flow indicator principle
3. Gradually adjust parameters and observe signal changes

### 10.2 Hardware Requirements

The strategy has moderate computational load, not demanding on VPS:

| Number of Pairs | Min RAM | Recommended RAM |
|----------------|---------|-----------------|
| 20-40 pairs | 512MB | 1GB |
| 40-80 pairs | 1GB | 2GB |

### 10.3 Backtesting vs. Live Trading Differences

1-minute candle data may differ between backtesting and live trading. Recommendations:
- Run in dry-run mode for 2-4 weeks first
- Observe whether signal trigger frequency matches expectations
- Small-capital live trading for 1 month before scaling up

### 10.4 Manual Trading Recommendations

Manual traders can reference this strategy's buy logic:
- Price touches Bollinger lower band + CMF > 0 + near support = buy signal
- Combine with overall market trend judgment (BTC direction)
- Consider changing timeframe to 5m to reduce noise

---

## XI. Summary

**Dracula** is a complex multi-condition strategy whose core value lies in:

1. **Money flow filtering**: CMF ensures money inflow, improving signal quality
2. **Dynamic support/resistance**: SupResFinder calculates support/resistance in real time
3. **Multi-scenario exits**: custom_exit covers 5 different exit scenarios
4. **Protection mechanism**: lost_protect prevents chasing after rallies

For quantitative traders, this is an excellent advanced strategy template. Recommendations:
- First understand the principle of each indicator
- Consider changing timeframe from 1m to 5m to reduce noise
- Adjust buy_bbt parameter for coins with different volatility
- Consider adding trend filtering (e.g., EMA200 trend judgment)

---
