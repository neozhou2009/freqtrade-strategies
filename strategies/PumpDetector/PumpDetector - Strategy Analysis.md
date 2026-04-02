# PumpDetector Strategy In-Depth Analysis

> **Strategy Number**: #338 (338th of 465 strategies)  
> **Strategy Type**: KDJ Variant Bottom-Fishing Strategy + Active Take-Profit Mechanism  
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

PumpDetector is a bottom-fishing strategy based on a KDJ indicator variant, derived from the L2 KDJ with Whale Pump Detector script on TradingView. This strategy captures J-line oversold rebound signals for entry, and exits when the J-line enters overbought territory or shows a turning signal, focusing on short-term bottom-fishing operations.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 core buy signal: J-line crosses above 0 |
| **Sell Conditions** | 2 sell signals: J-line crosses above 90 or J-line crosses below K-line with J > 50 |
| **Protection Mechanism** | 10% fixed stop loss |
| **Timeframe** | 5 Minutes (5m) |
| **Dependencies** | talib, qtpylib, math, numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# Stop loss setting
stoploss = -0.10    # 10% stop loss

# Trailing stop
trailing_stop = False   # Trailing stop not enabled
```

**Design Philosophy**:
- 10% fixed stop loss is relatively loose, providing room for bottom-fishing volatility
- Trailing stop not enabled, relies on active sell signals
- Strategy focuses more on signal-driven rather than passive protection

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',          # Limit buy
    'sell': 'limit',         # Limit sell
    'stoploss': 'market',     # Market stop loss execution
    'stoploss_on_exchange': False
}

order_time_in_force = {
    'buy': 'gtc',            # Good Till Cancelled
    'sell': 'gtc'
}
```

### 2.3 Other Configuration

```python
timeframe = '5m'                    # 5-minute timeframe
startup_candle_count: int = 30      # Requires 30 candles for warmup
use_sell_signal = True              # Enable sell signals
sell_profit_only = True             # Sell only when profitable
ignore_roi_if_buy_signal = False    # Don't ignore ROI when buy signal present
```

---

## III. Buy Condition Detailed Analysis

### 3.1 Core Indicator System

The strategy uses a KDJ indicator variant with the following parameters:

| Parameter | Value | Description |
|-----------|-------|-------------|
| n1 | 18 | RSV calculation period |
| m1 | 4 | K value smoothing period |
| m2 | 4 | D value smoothing period |

### 3.2 XSA Custom Indicator

The strategy implements a custom weighted moving average function XSA:

```python
def xsa(dataframe, source, len, wei):
    # Custom weighted moving average
    # Parameters:
    #   source: data source column name
    #   len: calculation period
    #   wei: weight
```

**Design Philosophy**:
- XSA is a weighted moving average algorithm
- Newer data has higher weight
- Used to smooth KDJ indicator calculations

### 3.3 KDJ Variant Indicator Calculation

```python
# RSV calculation
dataframe['rsv'] = (close - low_n1_min) / (high_n1_max - low_n1_min) * 100

# K, D, J value calculation
dataframe['k'] = xsa(dataframe, source='rsv', len=m1, wei=1)
dataframe['d'] = xsa(dataframe, source='k', len=m2, wei=1)
dataframe['j'] = 3 * dataframe['k'] - 2 * dataframe['d']
```

**KDJ Indicator Analysis**:
- **K Value**: Smoothed RSV, fast response line
- **D Value**: Smoothed K, slow confirmation line
- **J Value**: 3K - 2D, most sensitive line

### 3.4 Auxiliary Indicator Calculation

The strategy also calculates several auxiliary variables:

```python
# Price volatility calculation
dataframe['var2'] = (xsa(var1_abs, len=3, wei=1) / xsa(var1_max, len=3, wei=1)) * 100
dataframe['var3'] = EMA(var2 * 10, timeperiod=3)

# Price range calculation
dataframe['var4'] = low.rolling(38).min()    # 38-period low
dataframe['var5'] = var3.rolling(38).max()    # 38-period max volatility

# Composite indicator
dataframe['var7'] = EMA(var7_data, timeperiod=3) / 618 * var3
dataframe['var9'] = xsa(var8, len=13, wei=8)   # Williams indicator variant
```

**Note**: These auxiliary variables are not used in current buy/sell logic, possibly retained calculations from strategy development.

### 3.5 Single Buy Condition

#### Condition: J-line Crosses Above 0

```python
(qtpylib.crossed_above(dataframe['j'], 0)) &   
(dataframe['volume'] > 0)
```

**Logic Analysis**:
- J-line crosses above 0 from negative territory, indicating rebound from extreme oversold
- Volume > 0 ensures valid trading
- This is a classic bottom-fishing signal

**J-line Characteristics**:
- J value can go below 0 (extreme oversold)
- J value can go above 100 (extreme overbought)
- J value crossing above 0 usually indicates short-term reversal opportunity

---

## IV. Sell Logic Detailed Analysis

### 4.1 Dual Exit Mechanism

The strategy designs two independent sell signals:

#### Sell Signal #1: J-line Crosses Above 90

```python
qtpylib.crossed_above(dataframe['j'], 90)
```

**Logic**:
- J-line enters highly overbought territory
- Crossing above 90 threshold from below
- Usually indicates short-term top

#### Sell Signal #2: J-line Crosses Below K-line with J > 50

```python
qtpylib.crossed_below(dataframe['j'], dataframe['k']) & 
(dataframe['j'] > 50)
```

**Logic**:
- J-line crosses below K-line from above, forming a death cross
- J value still above 50, in mid-to-high range
- Indicates short-term momentum weakening

### 4.2 Sell Condition Summary

| Signal Number | Trigger Condition | Market Meaning |
|---------------|-------------------|----------------|
| #1 | J crosses above 90 | Entering extreme overbought, pullback imminent |
| #2 | J crosses below K with J > 50 | High momentum weakening, starting to decline |

### 4.3 Sell Logic Design Philosophy

```
Entry: J rebounds from negative (bottom fishing)
Exit: J enters overbought zone or turns down (top catching)
```

**Complete Trading Cycle**:
1. J-line drops below 0, enters oversold zone
2. J-line rebounds and crosses above 0, triggers buy
3. Price rises, J-line enters overbought zone
4. J crosses above 90 or J crosses below K-line, triggers sell
5. Wait for next bottom-fishing opportunity

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|--------------------|---------------------|------------|---------|
| Momentum Indicator | K Value | Period 4 | Fast response line |
| Momentum Indicator | D Value | Period 4 | Slow confirmation line |
| Momentum Indicator | J Value | 3K-2D | Ultra-sensitive signal line |

### 5.2 KDJ Indicator In-Depth Analysis

KDJ indicator is a variant of the Stochastic indicator:

```
RSV = (Close - N-day Low) / (N-day High - N-day Low) × 100
K = M-day smoothing of RSV
D = M-day smoothing of K
J = 3K - 2D
```

**J-line Characteristics**:
- More sensitive than K and D lines
- Can extend beyond the 0-100 range
- Negative values indicate extreme oversold
- Values above 100 indicate extreme overbought

### 5.3 Auxiliary Calculation Variables

Although not used in current logic, the strategy also calculates:

| Variable | Period | Potential Use |
|----------|--------|---------------|
| var4 | 38 periods | Price range lower bound |
| var5 | 38 periods | Volatility upper bound |
| var7 | Composite | Composite indicator |
| var9 | 13 periods | Williams indicator variant |

---

## VI. Risk Management Features

### 6.1 Fixed Stop Loss Protection

```
Stop Loss Line: -10%
```

**Design Considerations**:
- 10% stop loss is relatively loose for 5-minute timeframe
- Provides enough room for bottom-fishing volatility
- Avoids being stopped by normal fluctuations

### 6.2 Active Take-Profit Mechanism

Unlike passive protection strategies, PumpDetector relies on active signal take-profit:

| Take-Profit Method | Trigger Condition | Description |
|--------------------|-------------------|-------------|
| Overbought Exit | J > 90 | Catching tops |
| Momentum Weakening | J crosses below K with J > 50 | Catching turns |

### 6.3 Signal-Driven Architecture

```
Entry Signal → Position Monitoring → Exit Signal
    ↓                  ↓
Stop Loss Protection  Stop Loss Protection
```

**Characteristics**:
- Clear entry and exit signals
- Doesn't rely on time-based take-profit
- Suitable for quick short-term in-and-out

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Clear Signals**: Entry and exit conditions are clear, easy to understand and tune
2. **Focused on Bottom-Fishing**: J-line crossing above 0 is classic oversold rebound signal
3. **Dual Take-Profit**: Overbought exit and death cross exit double protection
4. **5-Minute Timeframe**: Suitable for intraday short-term operations

### ⚠️ Limitations

1. **Single Entry Condition**: Only one entry point with J crossing above 0, opportunities may be few
2. **No Trailing Stop**: Missing profit protection opportunity
3. **Fixed Parameters**: KDJ parameters hardcoded, cannot dynamically adjust
4. **Redundant Auxiliary Variables**: Calculates multiple unused indicators

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| Oscillating Downtrend | Default configuration | Core bottom-fishing scenario |
| Quick Pullback | Default configuration | Catching rebound opportunities |
| Trending Up | Not recommended | J value stays high, no entry signals |
| Low Volatility Sideways | Not recommended | No obvious oversold opportunities |

---

## IX. Applicable Market Environment Details

PumpDetector is a **short-term bottom-fishing strategy**. Based on its KDJ variant design, it's best suited for **bottom catching in oscillating markets**, while performing poorly in trending uptrends or low volatility sideways markets.

### 9.1 Strategy Core Logic

- **J-line Oversold**: J value below 0 indicates market extremely oversold
- **Rebound Capture**: J crossing above 0 means short-term reversal beginning
- **Active Take-Profit**: Exit when J enters overbought or turns down

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:-----------|:-------------------|:---------|
| 📈 Trending Up | ⭐☆☆☆☆ | J value stays high, no entry opportunities |
| 🔄 Oscillating Market | ⭐⭐⭐⭐⭐ | Core scenario, frequent oversold rebounds |
| 📉 Trending Down | ⭐⭐☆☆☆ | J may stay in negative zone too long |
| ⚡ High Volatility | ⭐⭐⭐⭐☆ | High volatility, many bottom-fishing opportunities |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|--------------------|-------------------|-------|
| Stop Loss | -0.10 | Can be relaxed for 5-minute timeframe |
| Timeframe | 5m | Keep default |
| J-line Entry Threshold | 0 | Can try adjusting to -5 or 5 |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Cost

- Need to understand KDJ indicator calculation principles
- Need to understand J-line's special characteristics (can exceed 0-100)
- Need to understand XSA weighted average algorithm

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|---------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-30 pairs | 4GB | 8GB |
| 30+ pairs | 8GB | 16GB |

### 10.3 Backtest vs Live Trading Differences

- 5-minute timeframe may generate many signals in backtesting
- Live trading needs to consider slippage and execution delay
- KDJ indicator may produce frequent signals in high volatility markets

### 10.4 Manual Trader Recommendations

- Can use J-line crossing above 0 alone as bottom-fishing reference
- Safer when combined with other confirmation indicators
- J crossing above 90 or below K-line can be used as position reduction signals

---

## XI. Summary

**PumpDetector** is a short-term bottom-fishing strategy based on a KDJ variant. Its core value lies in:

1. **Clear Signals**: J-line crossing above 0 for entry, J-line entering overbought or turning down for exit
2. **Focused on Bottom-Fishing**: Only seeks entry opportunities in oversold zones
3. **Dual Take-Profit**: Overbought exit and death cross exit as double insurance

For quantitative traders, this is a strategy suitable for short-term operations in oscillating markets, but attention must be paid to signal frequency and market environment selection.