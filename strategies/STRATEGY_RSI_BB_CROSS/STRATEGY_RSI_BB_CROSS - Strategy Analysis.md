# STRATEGY_RSI_BB_CROSS Strategy Deep Analysis

> **Strategy ID**: #370 (370th of 465 strategies)  
> **Strategy Type**: RSI-Bollinger Band Percentage Crossover + Trend Confirmation  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

STRATEGY_RSI_BB_CROSS is a quantitative strategy based on the crossover between Bollinger Band percentage and RSI percentage. The core logic of this strategy is to compare the Bollinger Band position (price's relative position within the Bollinger Bands) with the RSI position (RSI's relative position within the overbought/oversold range), triggering trading signals when crossovers occur and trend persistence conditions are met.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 buy signal, based on BB% crossing above RSI% |
| **Sell Condition** | 1 basic sell signal, based on BB% crossing below RSI% |
| **Protection Mechanism** | No built-in protection parameter group |
| **Timeframe** | 5m main timeframe |
| **Dependencies** | talib, qtpylib, numpy, pandas |
| **Author** | Fractate_Dev |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "60": 0.01,  # 1% profit required after 60 minutes
    "30": 0.02,  # 2% profit required after 30 minutes
    "0": 0.04    # 4% profit required immediately
}

# Stop Loss Setting
stoploss = -0.10  # 10% stop loss

# Trailing Stop
trailing_stop = False  # Not enabled
```

**Design Rationale**:
- ROI uses a progressive design - the longer the holding period, the lower the take-profit threshold
- 10% stop loss is relatively loose, giving price enough room for fluctuation
- No trailing stop enabled, relying on fixed ROI and signal exits

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',        # Limit buy
    'sell': 'limit',       # Limit sell
    'stoploss': 'market',  # Market stop loss
    'stoploss_on_exchange': False
}

order_time_in_force = {
    'buy': 'gtc',   # Good Till Cancelled
    'sell': 'gtc'
}
```

---

## III. Buy Condition Details

### 3.1 Core Concept: Percentage Position Normalization

The strategy normalizes Bollinger Band position and RSI position to 0-1 percentages:

**Bollinger Band Percentage (BB%)**:
```python
bb_percent = (close - bb_lower) / (bb_upper - bb_lower)
```
- 0 = Price at Bollinger Band lower band
- 1 = Price at Bollinger Band upper band
- 0.5 = Price at Bollinger Band middle band

**RSI Percentage (RSI%)**:
```python
rsi_limit = 30
rsi_percent = (rsi - rsi_limit) / (100 - rsi_limit * 2)
```
- 0 = RSI at oversold line (30)
- 1 = RSI at overbought line (70)
- 0.5 = RSI at neutral zone (50)

### 3.2 Buy Condition: BB% Crosses Above RSI%

```python
dataframe.loc[
    (
        # BB% crosses above RSI%
        qtpylib.crossed_above(dataframe['bb_percent'], dataframe['rsi_percent']) &
        
        # Both in lower half
        (dataframe['bb_percent'] < 0.5) & 
        (dataframe['rsi_percent'] < 0.5) &
        
        # Trend confirmation: previous candle BB% continuously below RSI%
        (dataframe['bb_below_rsi_count'].shift(1))
    ),
    'buy'] = 1
```

**Condition Breakdown**:

| Condition | Description | Logical Purpose |
|-----------|-------------|-----------------|
| `crossed_above(bb_percent, rsi_percent)` | BB% crosses above RSI% | Price relative position starts exceeding RSI relative position |
| `bb_percent < 0.5` | BB% in lower half | Price relatively low |
| `rsi_percent < 0.5` | RSI% in lower half | RSI relatively low |
| `bb_below_rsi_count.shift(1)` | Previous 14 candles BB% continuously below RSI% | Trend persistence confirmation |

### 3.3 Trend Confirmation Mechanism

The strategy uses `_trend_length = 14` as the trend confirmation period:

```python
dataframe['bb_above_rsi_count'] = True
dataframe['bb_below_rsi_count'] = True
for i in range(_trend_length):
    dataframe['bb_above_rsi_count'] = (dataframe['bb_minus_rsi_percent'].shift(i) > 0) & dataframe['bb_above_rsi_count']
    dataframe['bb_below_rsi_count'] = (dataframe['bb_minus_rsi_percent'].shift(i) < 0) & dataframe['bb_below_rsi_count']
```

**Logic Explanation**:
- `bb_below_rsi_count = True`: BB% has been below RSI% for 14 consecutive candles
- `bb_above_rsi_count = True`: BB% has been above RSI% for 14 consecutive candles

---

## IV. Sell Logic Details

### 4.1 Sell Signal: BB% Crosses Below RSI%

```python
dataframe.loc[
    (
        # BB% crosses below RSI%
        qtpylib.crossed_below(dataframe['bb_percent'], dataframe['rsi_percent']) &
        
        # Both in upper half
        (dataframe['bb_percent'] > 0.5) & 
        (dataframe['rsi_percent'] > 0.5) &
        
        # Trend confirmation: previous candle BB% continuously above RSI%
        (dataframe['bb_above_rsi_count'].shift(1))
    ),
    'sell'] = 1
```

**Condition Breakdown**:

| Condition | Description | Logical Purpose |
|-----------|-------------|-----------------|
| `crossed_below(bb_percent, rsi_percent)` | BB% crosses below RSI% | Price relative position starts weakening relative to RSI relative position |
| `bb_percent > 0.5` | BB% in upper half | Price relatively high |
| `rsi_percent > 0.5` | RSI% in upper half | RSI relatively high |
| `bb_above_rsi_count.shift(1)` | Previous 14 candles BB% continuously above RSI% | Trend persistence confirmation |

### 4.2 Buy/Sell Logic Symmetry

The strategy design presents perfect symmetry:

| Dimension | Buy Condition | Sell Condition |
|-----------|---------------|----------------|
| Crossover Direction | BB% crosses above RSI% | BB% crosses below RSI% |
| Position Requirement | Both < 0.5 (lower half) | Both > 0.5 (upper half) |
| Trend Confirmation | BB% continuously below RSI% | BB% continuously above RSI% |

### 4.3 ROI Take-Profit Mechanism

| Holding Time | Target Return | Description |
|--------------|---------------|-------------|
| Immediately | 4% | Seek 4% profit opportunity immediately after entry |
| 30 minutes | 2% | Lower take-profit target after 30 minutes |
| 60 minutes | 1% | Further lower target after 60 minutes |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|-------------------|-------------------|------------|---------|
| Volatility | Bollinger Bands | Window 20, StdDev 2 | Price relative position judgment |
| Momentum | RSI | Period 14 | Overbought/oversold judgment |
| Custom | BB% | - | Price position within Bollinger Bands |
| Custom | RSI% | - | RSI position within overbought/oversold range |
| Custom | BB%-RSI% | - | Difference between the two, trend confirmation |

### 5.2 Bollinger Band Configuration

```python
bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
```

**Difference from STRATEGY_RSI_BB_BOUNDS_CROSS**:
- This strategy uses window=20 (standard Bollinger Bands)
- STRATEGY_RSI_BB_BOUNDS_CROSS uses window=14 (custom Bollinger Bands)

### 5.3 Visualization Configuration

```python
plot_config = {
    'main_plot': {
        'tema': {},
        'sar': {'color': 'white'},
    },
    'subplots': {
        "BB": {
            'bb_percent': {'color': 'red'},
            '1': {},  # Upper boundary reference line
            '0': {},  # Lower boundary reference line
        },
        "RSI_Percent": {
            'rsi_percent': {'color': 'red'},
            '1': {},
            '0': {},
        },
        "bb_minus_rsi_percent": {
            'bb_minus_rsi_percent': {},  # Difference
            '0': {},  # Zero line
        },
        "bb_rsi_count": {
            'bb_above_rsi_count': {},  # Above trend count
            'bb_below_rsi_count': {},  # Below trend count
        },
    }
}
```

---

## VI. Risk Management Features

### 6.1 Percentage Position Comparison

The core innovation of the strategy lies in normalizing indicators from two different dimensions for comparison:
- **Bollinger Band Percentage**: Reflects price position within statistical volatility range
- **RSI Percentage**: Reflects momentum position within overbought/oversold range

When crossovers occur between them, it means **the relative relationship between price position and momentum position has changed**, which is a signal of potential trend reversal.

### 6.2 Trend Persistence Filter

The 14-period trend confirmation ensures:
- Sufficient trend buildup before crossover
- Not a single candle's noise signal
- Buy/sell signals have symmetry

### 6.3 Zone Filter

Buy requires both to be in lower half (< 0.5), sell requires both to be in upper half (> 0.5):
- Avoids frequent trading in middle zone
- Ensures buying at relatively low positions, selling at relatively high positions

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Perfect Buy/Sell Logic Symmetry**: Buy and sell conditions perfectly correspond, clear logic
2. **Normalized Comparison**: Unifying indicators from different dimensions to percentages, easy to compare
3. **Zone Filter**: Ensures buying in low zone, selling in high zone
4. **Trend Confirmation**: 14-period persistence filter reduces false signals

### ⚠️ Limitations

1. **Crossover Signal Lag**: Crossover is post-confirmation, may miss optimal entry point
2. **No Trailing Stop**: Missing opportunities to lock in floating profits
3. **Hardcoded Parameters**: `_trend_length=14` and `rsi_limit=30` are hardcoded
4. **Fixed Bollinger Band Window**: 20 period may not suit all markets

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Oscillating Market | Default configuration | Percentage crossover performs excellently in oscillation |
| Trending Market | Use with caution | Crossover signals may lag |
| High Volatility | Adjust stop loss | May need tighter stop loss |
| Low Volatility | Default configuration | Percentage positions more stable |

---

## IX. Applicable Market Environment Details

STRATEGY_RSI_BB_CROSS is a **percentage crossover strategy**. Based on its code architecture and logic design, it is best suited for **oscillating markets**, while performance may be suboptimal in **one-way trend markets**.

### 9.1 Strategy Core Logic

- **Normalized Comparison**: Unifying Bollinger Band position and RSI position to 0-1 percentages
- **Crossover Signal**: When BB% crosses RSI%, the relative relationship between price position and momentum position changes
- **Zone Filter**: Ensures buying in lower half, selling in upper half

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:------------|:-------|:---------|
| 📈 Slow Bull Oscillation | ⭐⭐⭐⭐⭐ | Percentage crossover signals are clear in oscillation |
| 🔄 Sideways Oscillation | ⭐⭐⭐⭐⭐ | Perfect match! Buy low sell high |
| 📉 One-way Downtrend | ⭐⭐☆☆☆ | Buy signals may trigger but get trapped |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | Percentage positions volatile, signals may be unstable |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| Timeframe | 5m | Default design, suitable for intraday trading |
| Bollinger Band Window | 20 | Default value, consider optimization |
| RSI Period | 14 | Default value, classic setting |
| Trend Confirmation Period | 14 | Consistent with RSI period |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Cost

The strategy uses innovative percentage normalization methods, requiring understanding of:
- BB% and RSI% calculation methods
- Meaning of crossover signals
- Role of trend confirmation mechanism

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 | 2GB | 4GB |
| 10-50 | 4GB | 8GB |

Strategy calculation is moderate, modern VPS can easily run it.

### 10.3 Differences Between Backtesting and Live Trading

- Crossover signals appear stable in backtesting, but slippage may exist in live trading
- Trend confirmation requires 14 candles, signals have some lag

### 10.4 Suggestions for Manual Traders

If trading manually, focus on:
1. Relative positions of BB% and RSI%
2. 14 consecutive candles trend confirmation
3. Zone when crossover occurs (buy in lower half, sell in upper half)

---

## XI. Summary

**STRATEGY_RSI_BB_CROSS** is a **normalized percentage crossover strategy**. Its core value lies in:

1. **Innovative Percentage Comparison**: Unifying Bollinger Band position and RSI position to 0-1 percentages
2. **Symmetrical Buy/Sell Logic**: Buy and sell conditions perfectly correspond, clear logic
3. **Zone Filter Mechanism**: Ensures buying at relatively low positions, selling at relatively high positions

For quantitative traders, this strategy provides a concise and effective way to understand the relative relationship between price position and momentum position. The symmetry of buy/sell logic makes it easy to understand and debug, but note the lag of crossover signals.