# PrawnstarOBV Strategy In-Depth Analysis

> **Strategy Number**: #337 (337th of 465 strategies)  
> **Strategy Type**: Volume-Price Trend Following + Dynamic Take-Profit Protection  
> **Timeframe**: 1 Hour (1h)

---

## I. Strategy Overview

PrawnstarOBV is a trend-following strategy based on the On-Balance Volume (OBV) indicator. This strategy cleverly combines volume analysis with the Relative Strength Index (RSI), predicting price movements by capturing volume changes and seeking buying opportunities at market bottoms.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 3 independent buy signals, can trigger independently |
| **Sell Conditions** | No active sell signals, relies on ROI and trailing stop |
| **Protection Mechanisms** | Trailing stop + Tiered ROI take-profit |
| **Timeframe** | 1 Hour (1h) |
| **Dependencies** | talib, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.296,      # Take profit at 29.6% immediately
    "179": 0.137,    # Take profit at 13.7% after 179 minutes
    "810": 0.025,    # Take profit at 2.5% after 810 minutes
    "1024": 0        # Break-even exit after 1024 minutes
}

# Stop loss setting
stoploss = -0.15    # 15% stop loss
```

**Design Philosophy**:
- ROI uses a progressive design: the longer the holding time, the lower the target return
- The 29.6% initial target indicates the strategy aims for higher returns
- Break-even exit after 1024 minutes (approximately 17 hours) avoids prolonged positions

### 2.2 Trailing Stop Configuration

```python
trailing_stop = True
trailing_stop_positive = 0.001      # Activate trailing after 0.1% profit
trailing_stop_positive_offset = 0.04  # Start trailing only after 4% profit
trailing_only_offset_is_reached = True
```

**Design Philosophy**:
- Trailing stop activates only when profit reaches 4%
- Trailing stop distance is only 0.1%, very tight
- Purpose is to lock in profits and prevent giving back gains

### 2.3 Order Type Configuration

```python
order_types = {
    'buy': 'limit',          # Limit buy
    'sell': 'limit',         # Limit sell
    'stoploss': 'market',    # Market stop loss execution
    'stoploss_on_exchange': False
}
```

---

## III. Buy Conditions Detailed Analysis

### 3.1 Core Indicator System

The strategy uses two core indicators:

| Indicator | Parameters | Purpose |
|-----------|------------|---------|
| **OBV** | Default | On-Balance Volume, measures buying/selling pressure |
| **OBV SMA** | 7 periods | 7-day simple moving average of OBV |
| **RSI** | Default (14 periods) | Relative Strength Index |

### 3.2 Buy Condition Analysis

The strategy's buy logic consists of three independent conditions connected by OR:

#### Condition #1: OBV Golden Cross + RSI Confirmation
```python
(qtpylib.crossed_above(dataframe['obv'], dataframe['obvSma'])) &
(dataframe['rsi'] < 50)
```

**Logic**:
- OBV crosses above its 7-day moving average, indicating strengthening volume momentum
- RSI < 50 confirms the market is in a weak zone
- Combining both to find bottom reversal signals

#### Condition #2: OBV Deviation Anomaly
```python
((dataframe['obvSma'] - dataframe['close']) / dataframe['obvSma'] > 0.1)
```

**Logic**:
- When the deviation between OBV moving average and close price exceeds 10%
- Indicates significant divergence between volume momentum and price
- Could be a dip-buying opportunity

#### Condition #3: OBV Trend Strengthening + RSI Confirmation
```python
(dataframe['obv'] > dataframe['obv'].shift(1)) &
(dataframe['obvSma'] > dataframe['obvSma'].shift(5)) &
(dataframe['rsi'] < 50)
```

**Logic**:
- OBV higher than previous candle, momentum increasing
- OBV SMA higher than 5 candles ago, trend pointing upward
- RSI < 50 confirms market is in weak zone
- Triple confirmation improves signal reliability

### 3.3 Buy Condition Classification Summary

| Condition Group | Condition Number | Core Logic | Trigger Difficulty |
|-----------------|------------------|------------|-------------------|
| Cross Type | #1 | OBV crosses above MA + RSI weak | Medium |
| Deviation Type | #2 | Volume-price deviation anomaly | Higher |
| Trend Type | #3 | OBV trend upward + RSI weak | Medium |

---

## IV. Sell Logic Detailed Analysis

### 4.1 No Active Sell Signals

The strategy's `populate_exit_trend` function returns empty conditions:

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
        ),
        'sell'] = 1
    return dataframe
```

**Design Philosophy**:
- Strategy doesn't rely on technical indicators for active selling
- Completely relies on ROI take-profit and trailing stop mechanisms
- Simplifies decision process, avoids signal conflicts

### 4.2 Tiered Take-Profit System

The strategy uses a time-progressive ROI take-profit mechanism:

```
Holding Time          Target Return
─────────────────────────────
0 minutes            29.6%
179 minutes          13.7%
810 minutes          2.5%
1024 minutes         0% (break-even)
```

**Characteristics**:
- Initial target is high, pursuing larger gains
- Gradually lowers expectations over time
- Finally exits at break-even, controlling risk

### 4.3 Trailing Stop Mechanism

| Parameter | Value | Description |
|-----------|-------|-------------|
| Activation Threshold | 4% | Activates after 4% profit |
| Trailing Distance | 0.1% | Triggers on 0.1% pullback from peak |
| Activation Mode | Only after threshold reached | Prevents premature activation |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|--------------------|---------------------|---------|
| Volume Indicator | OBV | Measures buying/selling pressure comparison |
| Trend Indicator | OBV SMA(7) | Smooths OBV, determines trend direction |
| Momentum Indicator | RSI | Identifies overbought/oversold zones |

### 5.2 OBV Indicator In-Depth Analysis

OBV (On Balance Volume) is a cumulative indicator:

- **Calculation**: Accumulate volume on up days, subtract on down days
- **Core Logic**: Volume precedes price changes
- **Signal Meaning**:
  - OBV rising + price falling = Bottom may be forming
  - OBV falling + price rising = Top may be forming

### 5.3 Indicator Synergy

```
OBV ───┐
       ├──→ Buy signal determination
RSI ───┘
```

- OBV provides volume direction judgment
- RSI provides market strength zone confirmation
- Combining both improves signal reliability

---

## VI. Risk Management Features

### 6.1 Multi-Layer Stop Protection

```
First Layer: 15% fixed stop loss
Second Layer: Tiered ROI take-profit
Third Layer: Trailing stop activated after 4% profit
```

**Design Intent**:
- Fixed stop loss as last line of defense
- ROI take-profit locks in time value
- Trailing stop protects existing profits

### 6.2 Time Dimension Risk Control

| Time Node | Risk Control Measure |
|-----------|---------------------|
| Entry moment | OBV + RSI double confirmation |
| After 179 minutes | Target return drops to 13.7% |
| After 810 minutes | Target return drops to 2.5% |
| After 1024 minutes | Forced break-even exit |

### 6.3 Volume Risk Considerations

- OBV focuses on volume analysis
- May generate false signals in low liquidity markets
- Should be used with trading volume filters

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Volume-Price Combination**: Incorporates volume into analysis, more comprehensive than price-only analysis
2. **Triple Buy Conditions**: Different conditions confirm bottom from different angles, improving signal quality
3. **Comprehensive Protection**: Trailing stop + ROI take-profit + fixed stop loss triple protection
4. **Suitable for Trend Reversals**: Focuses on bottom catching, suitable for dip-buying

### ⚠️ Limitations

1. **No Active Sell**: Completely relies on stop-loss/take-profit mechanisms, may miss better exit points
2. **Unfavorable in Ranging Markets**: RSI < 50 restriction may cause frequent signals
3. **1-Hour Timeframe**: Slower signals, not suitable for high-frequency trading
4. **OBV False Signals**: Volume indicator may fail under certain market conditions

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| Bottom Reversal Period | Default configuration | Strategy core scenario |
| Oscillating Downtrend | Lower ROI targets | Reduce return expectations |
| Rapid Uptrend | Use with caution | Not strategy's design scenario |
| High Volatility Period | Tighten stop loss | Control risk |

---

## IX. Applicable Market Environment Details

PrawnstarOBV is a typical **dip-buying strategy**. Based on its code architecture and indicator combination, it's best suited for **bottom catching in oscillating markets**, while performing poorly in trending downtrends or rapid uptrends.

### 9.1 Strategy Core Logic

- **Volume Precedes**: OBV theory suggests volume precedes price changes
- **Weakness Confirmation**: RSI < 50 ensures entry only in weak market zones
- **Trend Reversal Capture**: OBV crossing above MA means capital starting to flow in

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:-----------|:------------------|:---------|
| 📈 Trending Up | ⭐⭐☆☆☆ | RSI < 50 restriction causes missed opportunities |
| 🔄 Oscillating Market | ⭐⭐⭐⭐⭐ | Core design scenario, capturing bottom reversals |
| 📉 Trending Down | ⭐⭐☆☆☆ | May catch falling knives |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | Signals may be frequent, needs filtering |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|--------------------|-------------------|-------|
| Stop Loss | -0.15 | Adjustable based on risk preference |
| Trailing Stop Offset | 0.04 | 4% activation, balances protection and room |
| Trading Pairs | Major coins | Better liquidity makes OBV more reliable |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Cost

- Need to understand OBV indicator calculation principles
- Need to understand the relationship between volume and price
- Need to understand trailing stop trigger mechanism

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|---------------|-------------------|
| 1-5 pairs | 2GB | 4GB |
| 5-20 pairs | 4GB | 8GB |
| 20+ pairs | 8GB | 16GB |

### 10.3 Backtest vs Live Trading Differences

- OBV signals in backtesting may differ from live trading
- 1-hour timeframe may overfit in backtesting
- Recommended to verify with multiple timeframes

### 10.4 Manual Trader Recommendations

- OBV + RSI combination can be used alone as entry reference
- Trailing stop mechanism can be directly borrowed
- ROI take-profit table can be adjusted per personal style

---

## XI. Summary

**PrawnstarOBV** is a trend reversal capture strategy centered on volume analysis. Its core value lies in:

1. **Volume-Price Combination**: Combining OBV volume analysis with RSI weakness confirmation
2. **Multiple Protection**: Trailing stop + ROI take-profit + fixed stop loss triple defense
3. **Focus on Bottoms**: RSI < 50 restriction ensures entry only in weak zones

For quantitative traders, this is a strategy suitable for bottom catching in oscillating markets, but be aware of its limitations in trending markets.