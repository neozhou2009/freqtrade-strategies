# Schism2MM Strategy Deep Dive

> **Strategy Number**: #377 (377th of 465 strategies)  
> **Strategy Type**: Multi-condition Rebound Trading + Dynamic Position Addition + Smart Stop-loss System  
> **Timeframe**: 5 minutes (5m) + 1 hour (1h information layer)

---

## 1. Strategy Overview

Schism2MM is a complex trend rebound strategy based on **Relative Momentum Index (RMI)** and **Local Extrema Detection**. Its core feature is using the scipy signal processing library to identify local price troughs, combined with multi-dimensional indicator filtering for precise entry during trend pullbacks. The strategy supports **dynamic position addition** and is equipped with a **linear growth stop-loss threshold** system based on holding time.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy logic sets (new position + add position), with local extrema detection |
| **Sell Conditions** | Dynamic stop-loss + trend reversal signal + portfolio profit management |
| **Protection Mechanisms** | 4-layer protection (stop-loss, order timeout, entry confirmation, price protection) |
| **Timeframe** | Main: 5m + Information: 1h |
| **Dependencies** | numpy, talib, qtpylib, arrow, scipy.signal, cachetools, technical |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.025,    # Take 2.5% profit immediately
    "10": 0.015,   # After 10 minutes: 1.5%
    "20": 0.01,    # After 20 minutes: 1%
    "30": 0.005,   # After 30 minutes: 0.5%
    "120": 0       # After 120 minutes: no profit requirement
}

# Stop-loss setting
stoploss = -0.10  # 10% fixed stop-loss
```

**Design Rationale**:
- Uses **decreasing ROI table** - longer holding means lower profit requirements
- After 120 minutes, profit requirement is abandoned, relying entirely on sell signals
- Combined with `ignore_roi_if_buy_signal = True`, ROI is not triggered when buy signal is valid

### 2.2 Order Type Configuration

```python
use_sell_signal = False      # Don't use standard sell signals
sell_profit_only = True      # Only sell when profitable
ignore_roi_if_buy_signal = True  # Ignore ROI when buy signal is valid
```

### 2.3 Buy Parameters

```python
buy_params = {
    'inf-pct-adr': 0.95,    # Price range: 3-day low + 95%*average daily range
    'inf-rsi': 65,          # 1-hour RSI threshold
    'mp': 53,               # Momentum ping-pong indicator threshold
    'rmi-fast': 41,         # Fast RMI threshold
    'rmi-slow': 33          # Slow RMI threshold
}
```

---

## 3. Buy Conditions Detailed Analysis

### 3.1 Core Indicator System

The strategy uses the following technical indicators:

| Indicator | Period | Purpose |
|-----------|--------|---------|
| **RMI-Slow** | 21 period, momentum 5 | Trend direction determination |
| **RMI-Fast** | 8 period, momentum 4 | Fast momentum capture |
| **ROC** | 6 period | Rate of change calculation |
| **MP** | 6-period RSI of ROC | Momentum ping-pong indicator |
| **RSI (1h)** | 14 period | Information layer trend confirmation |
| **ADR** | 1-day high - 3-day low | Average daily range |

### 3.2 Local Extrema Detection

The strategy uses `scipy.signal.argrelextrema` to detect local price troughs:

```python
min_peaks = argrelextrema(dataframe['close'].values, np.less, order=100)
for mp in min_peaks[0]:
    dataframe.at[mp, 'buy_signal'] = True
```

**Explanation**:
- `order=100` means finding local minima within 100 candles
- Detected trough positions are marked as `buy_signal = True`
- This is the **core entry timing identification mechanism**

### 3.3 Two Buy Logic Sets

#### Scenario 1: New Position (No Existing Position)

```python
# Condition combination
(1h_rsi >= 65) &                           # Information layer trend confirmation
(close <= 3d_low + 0.95*adr) &             # Price in low region
(rmi-dn-trend == 1) &                      # RMI downtrend
(rmi-slow >= 33) &                         # RMI not oversold
(rmi-fast <= 41) &                         # Fast RMI limited
(mp <= 53) &                               # Momentum ping-pong not high
(buy_signal == True) &                     # Local trough detected
(volume > 0)                               # Has volume
```

**Logic Interpretation**:
- Under the premise of **large timeframe uptrend** (1h RSI >= 65)
- Waiting for **price pullback to low region**
- RMI downtrend confirms pullback
- Local extrema detection confirms **trough position**

#### Scenario 2: Add Position (Existing Position)

```python
# Dynamic threshold calculation
rmi_grow = linear_growth(30, 70, 180, 720, open_minutes)  # 30-70 linear growth
profit_factor = 1 - (rmi-slow / 300)  # Profit factor

# Condition combination
(rmi-up-trend == 1) &                      # RMI uptrend
(current_profit > peak_profit * factor) &  # Profit protection
(rmi-slow >= rmi_grow) &                   # RMI linear growth threshold
(buy_signal == True) &                     # Local trough
(volume > 0)
```

**Add Position Features**:
- After holding more than 180 minutes, RMI threshold grows linearly from 30 to 70
- Profit protection: current profit > peak profit × factor
- Only add position in uptrend, avoid trading against trend

---

## 4. Sell Logic Detailed Analysis

### 4.1 Dynamic Stop-loss System

The strategy uses **time-weighted dynamic stop-loss**:

```python
loss_cutoff = linear_growth(-0.03, 0, 0, 300, open_minutes)
# Holding 0 minutes: allow 3% loss
# Holding 300 minutes: require profit
```

### 4.2 Sell Trigger Conditions

```python
# Basic conditions
(current_profit < loss_cutoff) &           # Profit below dynamic threshold
(current_profit > stoploss) &              # Above fixed stop-loss
(rmi-dn-trend == 1) &                      # RMI downtrend
(volume > 0)

# Exit threshold after profit
if peak_profit > 0:
    crossed_below(rmi-slow, 50)            # Was profitable: RMI falls below 50
else:
    crossed_below(rmi-slow, 10)            # Never profitable: RMI falls below 10
```

### 4.3 Portfolio Profit Management

When other positions exist, the strategy considers overall portfolio:

```python
if free_slots > 0:
    # When having free slots
    hold_pct = (free_slots / 100) * -1
    avg_other_profit >= hold_pct           # Other position profit threshold
else:
    # When no free slots
    biggest_loser == True                   # Only allow biggest loser to sell
```

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| Momentum | RMI(21,5), RMI(8,4) | Trend direction, overbought/oversold |
| Rate of Change | ROC(6), MP | Momentum strength measurement |
| Trend | RMI trend count | Trend confirmation |
| Price | 1d high, 3d low, ADR | Price position assessment |

### 5.2 Information Timeframe Indicators (1h)

The strategy uses 1h as information layer:

- **RSI(14)**: Confirm large timeframe trend
- **1d_high**: 24-hour high
- **3d_low**: 72-hour low
- **ADR**: Average daily range

### 5.3 Local Extrema Detection

```python
# Using scipy signal processing
from scipy.signal import argrelextrema
min_peaks = argrelextrema(close_values, np.less, order=100)
```

---

## 6. Risk Management Features

### 6.1 Multi-layer Stop-loss Protection

| Stop-loss Type | Trigger Condition | Description |
|---------------|-------------------|-------------|
| Fixed Stop-loss | Loss >= 10% | Hard exit |
| Dynamic Stop-loss | Profit < time threshold | Soft exit |
| RMI Stop-loss | RMI falls below threshold | Trend reversal |
| Portfolio Stop-loss | Overall position consideration | Fund management |

### 6.2 Order Timeout Protection

```python
def check_buy_timeout(self, pair, trade, order, **kwargs):
    # Buy order timeout: cancel when current price > order price * 1.01
    if current_price > order['price'] * 1.01:
        return True
    return False

def check_sell_timeout(self, pair, trade, order, **kwargs):
    # Sell order timeout: cancel when current price < order price * 0.99
    if current_price < order['price'] * 0.99:
        return True
    return False
```

### 6.3 Entry Price Protection

```python
def confirm_trade_entry(self, pair, order_type, amount, rate, **kwargs):
    # Entry confirmation: reject when price deviation > 1%
    if current_price > rate * 1.01:
        return False
    return True
```

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Local Extrema Detection**: Uses scipy signal processing to precisely identify trough positions
2. **Dynamic Position Addition**: Smart add-position logic based on holding time and profit
3. **Linear Growth Threshold**: Stop-loss and add-position thresholds adjust linearly over time
4. **Portfolio Profit Management**: Sell decisions considering overall positions

### ⚠️ Limitations

1. **High Complexity**: Involves scipy signal processing, linear growth functions, multi-dimensional conditions
2. **Parameter Sensitivity**: `order=100` extrema detection is sensitive to market structure
3. **Backtest Limitations**: Dynamic position addition and portfolio management may not be fully simulated in backtesting
4. **Live Trading Dependency**: `Trade` object queries only work in actual runtime

---

## 8. Suitable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Oscillating Uptrend | Default parameters | Strategy's design target scenario |
| Strong Trend | Adjust `inf-rsi` | Raise trend confirmation threshold |
| High Volatility | Adjust `inf-pct-adr` | Expand price range |
| Low Volatility | Lower stop-loss | `stoploss = -0.05` |

---

## 9. Suitable Market Environment Details

Schism2MM is a **rebound trading strategy**. Based on its code architecture and community long-term live trading verification, it is most suitable for **oscillating uptrend markets** and performs poorly in **one-sided downtrends**.

### 9.1 Strategy Core Logic

- **Local Extrema Detection**: Find price troughs within 100 candles
- **Trend Filter**: Require 1h RSI >= 65, ensuring large timeframe uptrend
- **Pullback Entry**: Enter when price pulls back to low region
- **Dynamic Position Addition**: Can add position after holding more than 3 hours

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:-----------:|:------------------:|----------|
| 📈 Oscillating Uptrend | ⭐⭐⭐⭐⭐ | Perfect match with strategy design, pullback buy + trend hold |
| 🔄 Sideways Oscillation | ⭐⭐⭐☆☆ | May trigger frequent stop-losses, local extrema detection may fail |
| 📉 One-sided Downtrend | ⭐⭐☆☆☆ | Trend filter may not respond in time, frequent stop-loss triggers |
| ⚡ High Volatility | ⭐⭐☆☆☆ | Extrema detection may be unstable, significant slippage impact |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| `order` (extrema) | 50-150 | Adjust detection range based on market volatility |
| `inf-rsi` | 60-70 | Trend confirmation threshold |
| `stoploss` | -0.08 ~ -0.12 | Adjust based on risk tolerance |

---

## 10. Important Note: The Cost of Complexity

### 10.1 Learning Cost

Schism2MM involves multiple advanced concepts:
- scipy signal processing (`argrelextrema`)
- Linear growth functions
- Portfolio profit management
- Dynamic stop-loss system

Recommend fully understanding each module before live deployment.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|----------------|-------------------|
| 1-10 | 2GB | 4GB |
| 10-30 | 4GB | 8GB |
| 30+ | 8GB | 16GB |

### 10.3 Backtest vs Live Trading Differences

**Backtest Limitations**:
- `Trade.get_trades()` not available in backtest
- Portfolio profit management fails in backtest
- Dynamic position addition may not be fully simulated

**Recommendation**: Use dry-run mode for thorough testing before live trading.

### 10.4 Manual Trading Suggestions

For manual trading:
1. Focus on pairs with 1h RSI >= 65
2. Use TradingView to mark local extrema points
3. Confirm entry with RMI indicator
4. Set 10% stop-loss and dynamic take-profit

---

## 11. Summary

**Schism2MM** is a **technology-intensive rebound trading strategy**. Its core value lies in:

1. **Scientific Extrema Detection**: Uses scipy signal processing to precisely locate troughs
2. **Smart Position Addition**: Dynamic add-position logic based on time and profit
3. **Multi-layer Risk Management**: Fixed stop-loss + dynamic stop-loss + portfolio management

For quantitative traders, this is a medium-complexity strategy suitable for **oscillating uptrend markets**, requiring certain Python and signal processing knowledge to fully understand and optimize.

---