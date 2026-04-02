# SMAOPv1_TTF Strategy In-Depth Analysis

> **Strategy Number**: #357 (357th of 465 strategies)  
> **Strategy Type**: SMA Offset + TTF Trend Trigger + EWO Protection Combination Strategy  
> **Timeframe**: 5 minutes (5m) + 1 hour (1h) informative layer

---

## I. Strategy Overview

SMAOPv1_TTF is a multi-condition trend-following strategy that combines SMA Offset, Trend Trigger Factor (TTF), and Elliott Wave Oscillator (EWO). The strategy identifies entry opportunities through price deviation from moving averages, filters trends with EWO, and uses TTF as a dynamic exit signal, forming a complete trend trading system.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signals that can trigger entries independently |
| **Sell Conditions** | 2 base sell signals + trailing stop mechanism |
| **Protection Mechanisms** | Triple protection: EWO filter + RSI constraint + trailing stop |
| **Timeframe** | Main timeframe 5m + informative timeframe 1h |
| **Dependencies** | talib, numpy, qtpylib, technical |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.10,    # Immediately get 10% profit
    "30": 0.05,   # After 30 minutes, reduce to 5%
    "60": 0.02    # After 60 minutes, reduce to 2%
}

# Stop loss setting
stoploss = -0.10   # Fixed stop loss 10%

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.001
trailing_stop_positive_offset = 0.01
trailing_only_offset_is_reached = True
```

**Design Rationale**:
- ROI table uses a stepped decline design, initial target 10%, gradually lowering profit expectations as holding time extends
- Stop loss set at 10%, suitable for high volatility in cryptocurrency markets
- Trailing stop activates after 1% profit, locking in 0.1% positive profit to protect gains

### 2.2 Order Type Configuration

```python
use_sell_signal = True          # Enable sell signals
sell_profit_only = True         # Sell only when profitable
sell_profit_offset = 0.01       # Sell profit offset 1%
ignore_roi_if_buy_signal = True # Ignore ROI when buy signal is active
```

---

## III. Buy Conditions Explained

### 3.1 Optimizable Parameter Groups

The strategy provides multiple sets of optimizable parameters for Hyperopt search:

| Parameter Type | Parameter Name | Default | Optimization Range |
|----------------|----------------|---------|-------------------|
| MA Period | base_nb_candles_buy | 16 | 5-80 |
| Buy Offset | low_offset | 0.978 | 0.9-0.99 |
| EWO High Threshold | ewo_high | 5.638 | 2.0-12.0 |
| EWO Low Threshold | ewo_low | -19.993 | -20.0 to -8.0 |
| RSI Buy Threshold | rsi_buy | 61 | 30-70 |
| TTF Period | ttf_length | 15 | 1-50 |
| TTF Upper Trigger | ttf_upperTrigger | 100 | 1-400 |
| TTF Lower Trigger | ttf_lowerTrigger | -100 | -400 to -1 |

### 3.2 Buy Conditions Detailed

#### Condition #1: Trend Continuation Buy
```python
# Logic
- Price below offset MA (close < ma_buy * low_offset)
- EWO at high level (EWO > ewo_high), indicating strong trend
- RSI not overbought (RSI < rsi_buy)
- Volume > 0
```

**Interpretation**: This condition captures pullback opportunities in uptrends. When price pulls back below the offset MA, if EWO shows the trend remains strong and RSI is not overheated, it's a quality entry point.

#### Condition #2: Trend Reversal Buy
```python
# Logic
- Price below offset MA (close < ma_buy * low_offset)
- EWO at low level (EWO < ewo_low), indicating oversold
- Volume > 0
```

**Interpretation**: This condition captures oversold bounce opportunities. When EWO is at an extreme low, the market may be oversold with potential for a rebound.

### 3.2 Buy Condition Classification

| Condition Group | Condition # | Core Logic |
|-----------------|-------------|------------|
| Trend Continuation | #1 | Pullback buy + trend confirmation |
| Reversal Capture | #2 | Oversold buy + bounce expectation |

---

## IV. Sell Logic Explained

### 4.1 ROI Take Profit System

The strategy uses a stepped ROI take profit mechanism:

```
Holding Time      Target Profit
────────────────────────
0 minutes        10%
30 minutes       5%
60 minutes       2%
```

### 4.2 Trailing Stop Mechanism

```
Activation      Profit Offset    Locked Profit
─────────────────────────────────────
Profit > 1%     0.1%            Profit - 0.1%
```

### 4.3 Sell Signals (2 total)

#### Signal #1: MA Offset Sell
```python
# Sell signal 1: Offset MA breakout
- Price above offset MA (close > ma_sell * high_offset)
- Volume > 0
```

**Interpretation**: When price breaks above the offset MA, it indicates trend overheating, triggering profit-taking.

#### Signal #2: TTF Trend Trigger Sell
```python
# Sell signal 2: TTF crosses above trigger line
- TTF indicator crosses above 100 trigger line
- Volume > 0
```

**Interpretation**: TTF (Trend Trigger Factor) crossing above 100 indicates buying power has reached an extreme, suggesting potential reversal - a good time to take profits.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|---------------------|---------|
| Trend | EMA (Exponential Moving Average) | Offset buy/sell line calculation |
| Oscillator | EWO (Elliott Wave Oscillator) | Trend strength judgment |
| Momentum | RSI (Relative Strength Index) | Overbought/oversold filtering |
| Trend | TTF (Trend Trigger Factor) | Trend extreme identification |

### 5.2 TTF Indicator Explained

TTF (Trend Trigger Factor) is the core innovative indicator in this strategy:

```python
def ttf(df, ttf_length):
    buyPower = high.rolling(ttf_length).max() - low.shift(ttf_length).min()
    sellPower = high.shift(ttf_length).max() - low.rolling(ttf_length).min()
    ttf = 200 * (buyPower - sellPower) / (buyPower + sellPower)
    return ttf
```

**Calculation Logic**:
- **Buying Power**: Current period's highest price - Previous period's lowest price
- **Selling Power**: Previous period's highest price - Current period's lowest price
- **TTF Value**: Normalized to -100 to +100 range

**Interpretation**: TTF > 100 indicates buying power is extremely strong, possibly overheated; TTF < -100 indicates selling power is extremely strong, possibly oversold.

### 5.3 Informative Timeframe Indicators (1h)

The strategy uses 1 hour as the informative layer, providing higher-dimensional trend judgment:

- Supports 1-hour level trend confirmation
- Can be used for multi-timeframe analysis

---

## VI. Risk Management Features

### 6.1 Triple Buy Filtering

| Filter Layer | Indicator | Function |
|--------------|-----------|----------|
| First Layer | EWO | Trend direction confirmation |
| Second Layer | RSI | Overbought/oversold filtering |
| Third Layer | Volume | Liquidity guarantee |

### 6.2 Dynamic Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.001
trailing_stop_positive_offset = 0.01
trailing_only_offset_is_reached = True
```

**Protection Logic**:
- Trailing stop activates after profit reaches 1%
- Stop line follows price increases, locking in 99.9% of profit
- Effectively protects existing gains

### 6.3 Sell Only When Profitable

```python
sell_profit_only = True
sell_profit_offset = 0.01
```

**Interpretation**: The strategy only responds to sell signals when profitable at least 1%, avoiding exiting during small losses.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Multi-dimensional Entry Judgment**: Combines MA offset, EWO, RSI triple filtering for more reliable entry signals
2. **Trend and Reversal Coverage**: Two buy conditions capture trend continuation and reversal opportunities respectively
3. **Dynamic Exit Mechanism**: TTF indicator provides trend extreme identification, combined with ROI and trailing stop for flexible exits
4. **Large Optimization Space**: 11 adjustable parameters, suitable for optimization in different market environments

### ⚠️ Limitations

1. **High Parameter Sensitivity**: Many adjustable parameters, high risk of overfitting
2. **Underutilized Informative Timeframe**: Although 1h informative layer is defined, actual application in code is limited
3. **Obscure TTF Indicator**: Limited community verification, real performance needs further observation
4. **Questionable Performance in Ranging Markets**: Offset strategies may generate frequent false signals in sideways consolidation

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|--------------------|---------------------------|-------|
| Uptrend | Raise ewo_high | Trend continuation signals more effective |
| Downtrend | Lower ewo_low | Reversal signals need more extreme conditions |
| Ranging Market | Use with caution | Recommend reducing position size or pausing |
| High Volatility Coins | Loosen stop loss appropriately | Give price more room for fluctuation |

---

## IX. Applicable Market Environment Details

SMAOPv1_TTF is a trend-following strategy combining SMA offset and TTF trend trigger. Based on its code architecture and community experience, it performs best in **clear trend markets** and may underperform in **sideways ranging markets**.

### 9.1 Strategy Core Logic

- **MA Offset Entry**: Enter when price falls below MA by a certain percentage, waiting for regression
- **EWO Trend Filter**: Judge current trend strength through EWO, avoid trading against the trend
- **TTF Dynamic Exit**: Take profit in time when TTF reaches extremes, preventing profit giveback

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|-------------|-------------------|----------|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | MA offset captures pullbacks, TTF timely exits |
| 🔄 Ranging Market | ⭐⭐☆☆☆ | Frequent touches of offset lines, many false signals |
| 📉 Downtrend | ⭐⭐☆☆☆ | EWO low threshold can catch bounces but higher risk |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | Trailing stop protects profits but may be triggered frequently |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|--------------------|-------------------|-------|
| base_nb_candles_buy | 16-30 | Shorter periods for faster pace, longer for stability |
| low_offset | 0.95-0.98 | Larger offset for more conservative entries |
| ttf_upperTrigger | 80-120 | Higher for more aggressive profit-taking |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

The strategy involves non-standard indicators like EWO and TTF, requiring time to understand their calculation logic and meaning.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|---------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |

### 10.3 Backtest vs Live Trading Differences

- EWO and TTF performance in backtesting may differ from live trading
- Recommend running on paper trading for at least 2 weeks
- Note slippage impact on trailing stop in extreme markets

### 10.4 Manual Trader Recommendations

- Understand MA offset concept: Enter when price falls below MA by a certain percentage
- Watch for TTF > 100 extreme signals
- EWO positive indicates uptrend, negative indicates downtrend

---

## XI. Summary

**SMAOPv1_TTF** is a trend-following strategy combining SMA offset, EWO trend filtering, and TTF dynamic exit. Its core value lies in:

1. **Multiple Filtering Mechanism**: MA offset + EWO + RSI triple confirmation reduces false signals
2. **Trend and Reversal Coverage**: Two buy conditions cover different market phases
3. **Dynamic Exit System**: TTF + ROI + trailing stop combination protects profits

For quantitative traders, this is a strategy suitable for trending markets, but requires parameter optimization for specific trading pairs and attention to risk control in ranging markets.