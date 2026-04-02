# RaposaDivergenceV1 Strategy Deep Analysis

> **Strategy Number**: #345 (345th of 465 strategies)  
> **Strategy Type**: RSI Divergence Trading + Peak-Valley Detection Algorithm  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

RaposaDivergenceV1 is a trend reversal strategy based on RSI divergence and price peak-valley detection. Developed by alb#1349, referencing technical articles from Raposa Technologies, this strategy uses scipy's `argrelextrema` function to detect local extrema in price, combined with RSI indicator divergence signals to identify trading opportunities at trend reversal points.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 buy signal, based on bullish divergence detection |
| **Sell Condition** | 1 sell signal, based on bearish divergence detection |
| **Protection Mechanism** | Fixed stop-loss + trailing stop + tiered ROI exit |
| **Timeframe** | 5m primary timeframe |
| **Dependencies** | talib, numpy, pandas, scipy, collections |

### ⚠️ Important Warning

The strategy author explicitly states in the code comments:
> "argrelextrema" might have look-ahead bias so results in backtest will not be reliable

This means the strategy may have **look-ahead bias** in backtesting, making backtest results unreliable. Live trading performance may differ significantly from backtest results.

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.15,     # Immediate: 15% profit
    "60": 0.02,    # After 60 minutes: 2% profit
    "120": 0.01,   # After 120 minutes: 1% profit
    "180": 0.001   # After 180 minutes: 0.1% profit
}

# Stop-loss settings
stoploss = -0.3   # 30% fixed stop-loss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01        # 1% positive trailing
trailing_stop_positive_offset = 0.02  # 2% activation threshold
trailing_only_offset_is_reached = True
```

**Design Philosophy**:
- Initial ROI target is set high (15%) but quickly degrades to lower levels
- 30% fixed stop-loss is relatively loose, relying on trailing stop to protect profits
- Trailing stop activates at 2% profit, trailing by 1%

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',        # Limit buy
    'sell': 'market',      # Market sell
    'stoploss': 'market',  # Market stop-loss
    'stoploss_on_exchange': False
}
```

### 2.3 Optimizable Parameters

| Parameter Type | Parameter Name | Range | Default | Description |
|---------------|----------------|-------|---------|-------------|
| **Buy Parameters** | k_value | 1-32 | 2 | Number of consecutive extrema needed for peak-valley confirmation |
| | order | 1-32 | 5 | Window size for extrema detection |
| | rsi_buy | 20-80 | 50 | RSI buy threshold |
| **Sell Parameters** | rsi_sell | 20-80 | 50 | RSI sell threshold |

---

## III. Buy Condition Details

### 3.1 Core Algorithm: Peak-Valley Detection

The strategy uses `scipy.signal.argrelextrema` function to detect local extrema in price. This is a mathematical method that identifies local maxima and minima by comparing adjacent data points.

```python
# Extrema detection function
from scipy.signal import argrelextrema

# Four extrema modes
- getHigherHighs(): Consecutive higher highs
- getLowerHighs(): Consecutive lower highs
- getHigherLows(): Consecutive higher lows
- getLowerLows(): Consecutive lower lows
```

### 3.2 Buy Signal Logic

```python
# Buy conditions
(dataframe['close_lows'] == -1) &     # Price forms higher lows
(dataframe['rsi_lows'] == -1) &       # RSI forms higher lows (bullish divergence)
(dataframe['rsi'] < 50) &             # RSI below 50
(dataframe['volume'] > 0)             # Has volume
```

**Core Logic**:
- Price forms higher lows (bullish divergence signal)
- RSI simultaneously forms higher lows (confirms divergence)
- RSI below 50 (not buying in overbought territory)

### 3.3 Peak-Valley Detection Principle

```python
def getHigherLows(data, order=5, K=2):
    """
    Detect consecutive higher lows
    order: extrema detection window size
    K: number of consecutive extrema needed for confirmation
    """
    # Get all local lows
    low_idx = argrelextrema(data, np.less, order=order)[0]
    lows = data[low_idx]
    
    # Ensure consecutive lows are higher
    for i, idx in enumerate(low_idx):
        if lows[i] < lows[i-1]:
            ex_deque.clear()  # Clear if not consecutive
        ex_deque.append(idx)
        if len(ex_deque) == K:  # Reached K confirmations
            extrema.append(ex_deque.copy())
```

---

## IV. Sell Logic Details

### 4.1 Multi-tier Take-Profit System

The strategy employs a tiered take-profit mechanism:

```
Profit Range       Threshold     Signal Name
──────────────────────────────────────────
0-60 minutes      15%           ROI_1
60-120 minutes     2%            ROI_2
120-180 minutes    1%            ROI_3
After 180 minutes  0.1%          ROI_4
```

### 4.2 Sell Signal Logic

```python
# Sell conditions
(dataframe['close_highs'] == 1) &     # Price forms lower highs
(dataframe['rsi_highs'] == -1) &      # RSI forms higher highs (bearish divergence)
(dataframe['rsi'] > 50) &             # RSI above 50
(dataframe['volume'] > 0)             # Has volume
```

**Core Logic**:
- Price forms lower highs (bearish divergence signal)
- RSI simultaneously forms higher highs (confirms divergence)
- RSI above 50 (not selling in oversold territory)

### 4.3 Sell Signal Evaluation

The strategy author explicitly states in comments:
> "sell signal seems like garbage"

This indicates the sell signal's reliability is questionable. It's recommended to rely on ROI and trailing stop for exits rather than the active sell signal.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|-------------------|---------|
| **Momentum** | RSI(14) | Divergence detection basis |
| **Extrema Detection** | argrelextrema | Peak-valley identification algorithm |

### 5.2 Peak-Valley Marking System

The strategy marks peak-valley status for each data point through the `getPeaks()` function:

| Mark | Meaning |
|------|---------|
| close_highs = 1 | Higher high (HH) |
| close_highs = -1 | Lower high (LH) |
| close_lows = 1 | Lower low (LL) |
| close_lows = -1 | Higher low (HL) |

---

## VI. Risk Management Features

### 6.1 Divergence Trading Risks

Inherent risks of divergence trading:
- **False divergence**: Price and indicator may produce multiple divergences before actually reversing
- **Lag**: Extrema confirmation requires K consecutive points, causing signal lag
- **Look-ahead bias**: argrelextrema may "see the future" in backtesting

### 6.2 Parameter Sensitivity

| Parameter | Impact | Recommendation |
|-----------|--------|----------------|
| order | Extrema detection window; larger = more stable but fewer signals | 5-10 is balanced |
| K value | Number of extrema needed for confirmation; larger = more reliable but later signals | 2-3 is appropriate |
| rsi_buy/sell | RSI thresholds, affecting entry timing | Adjust based on coin volatility |

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Solid theoretical foundation**: Divergence trading is a classic technical analysis method with clear economic logic
2. **Precise peak-valley detection**: Uses scipy scientific computing library for high algorithm reliability
3. **Clear reversal signals**: Bullish and bearish divergence signals are clear and easy to understand
4. **Optimizable parameters**: order and K values can be adjusted based on market characteristics

### ⚠️ Limitations

1. **Look-ahead bias**: argrelextrema may produce false signals in backtesting
2. **Unreliable sell signal**: Author admits sell signal quality is poor
3. **Low signal frequency**: Divergence signals don't occur frequently, may have long periods without trades
4. **Wide stop-loss**: 30% fixed stop-loss carries significant risk

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| Ranging market | Normal use | Divergence signals are more accurate |
| Trending market | Use with caution | Prone to false divergences |
| High volatility | Increase order | Filter noise extrema |
| Low volatility | Decrease order | Capture more signals |

---

## IX. Applicable Market Environment Details

RaposaDivergenceV1 is a divergence strategy based on technical analysis theory. Based on its code architecture and algorithm characteristics, it performs best in **oscillating trend-transition markets**, while performing poorly during **sustained trending periods**.

### 9.1 Strategy Core Logic

- **Bullish divergence buy**: Price makes new low but RSI doesn't, suggesting declining momentum
- **Bearish divergence sell**: Price makes new high but RSI doesn't, suggesting weakening momentum
- **Peak-valley confirmation**: Requires K consecutive extrema for confirmation, avoiding single-point noise

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 Sustained uptrend | ⭐☆☆☆☆ | Bearish divergence repeatedly appears but price continues rising, frequent stop-losses |
| 📉 Sustained downtrend | ⭐☆☆☆☆ | Bullish divergence repeatedly appears but price continues falling, frequent stop-losses |
| 🔄 Ranging market | ⭐⭐⭐⭐☆ | Divergence signals are more accurate during trend transitions |
| 🔄 Trend transition | ⭐⭐⭐⭐⭐ | Home field! Divergence is designed for reversals |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|------------------|-------|
| order | 5-10 | Adjust based on volatility |
| k_value | 2-3 | Number of extrema needed for confirmation |
| rsi_buy | 40-50 | Don't set in overbought territory |
| rsi_sell | 50-60 | Don't set in oversold territory |

---

## X. Important Warning: Backtesting Bias Risk

### 10.1 Look-ahead Bias

The `argrelextrema` function used by this strategy has a serious issue in backtesting:

```
In backtesting, argrelextrema may "see" future data points to confirm current extrema.
But in live trading, the current candle cannot confirm whether it's an extrema until subsequent data arrives.
```

**Consequences**:
- Backtest may show "perfect" entry and exit points
- Live trading signals will lag, missing optimal entry/exit timing
- Backtest profit does not equal live trading profit

### 10.2 Recommended Solutions

1. **For reference only**: Use divergence signals as auxiliary judgment, not as the sole entry basis
2. **Live verification**: Test with paper trading for extended periods, compare with backtest results
3. **Lower expectations**: Live performance may be significantly worse than backtesting

### 10.3 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|---------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

### 10.4 Manual Trading Recommendations

If using this strategy's signals for manual trading:
1. Learn divergence identification techniques, understand peak-valley patterns
2. Confirm divergence with other indicators (e.g., MACD, volume)
3. Don't rely solely on divergence signals, pay attention to trend direction
4. Set tighter stop-losses (recommend 10-15%)

---

## XI. Summary

**RaposaDivergenceV1** is a divergence trading strategy based on classic technical analysis theory. Its core value lies in:

1. **Solid theory**: Divergence is a classic technical analysis method with clear logic
2. **Precise algorithm**: Uses scipy scientific computing library for peak-valley detection
3. **Clear signals**: Bullish divergence buy, bearish divergence sell, simple rules

But special attention must be paid to:
- **Unreliable backtesting**: Has look-ahead bias, backtest results are for reference only
- **Poor sell signal quality**: Author recommends relying on ROI and trailing stop
- **Limited applicable scenarios**: Only performs well during trend transitions

For quantitative traders, this is a strategy with **more academic value than live trading value**, suitable for learning divergence detection algorithms, but should be used cautiously in live trading. Recommended as an auxiliary signal combined with other strategies.