# ClucFiatROI Strategy Analysis

> **Strategy ID**: #X (Cluc Series)  
> **Strategy Type**: Bollinger Band Breakout + Fisher RSI + Tiered ROI Exit  
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

ClucFiatROI is a high-frequency intraday trading strategy based on Bollinger Band narrowing breakouts and Fisher-transformed RSI. The strategy captures breakout moves following Bollinger Band compression, combined with volume filtering and trend confirmation, to identify short-term trading opportunities in volatile markets. The "Fiat" moniker implies fine-grained ROI (Return on Investment) management, while "ROI" directly highlights its core feature: a tiered take-profit mechanism.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 2 entry modes (new position + pyramid), 6 Hyperopt-optimized parameters |
| **Exit Conditions** | Tiered ROI exit + signal-triggered exit + trailing stop |
| **Protection Mechanisms** | Order timeout protection + volume filtering + trailing stop |
| **Timeframe** | 5-minute primary |
| **Dependencies** | No external dependencies, uses only built-in Freqtrade indicators |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.04354,     # Exit at 4.35% after 0 minutes
    "5": 0.03734,     # Exit at 3.73% after 5 minutes
    "8": 0.02569,     # Exit at 2.57% after 8 minutes
    "10": 0.019,      # Exit at 1.90% after 10 minutes
    "76": 0.01283,    # Exit at 1.28% after 76 minutes
    "235": 0.007,     # Exit at 0.70% after 235 minutes
    "415": 0,         # After 415 minutes, rely on trailing stop
}

# Stop Loss
stoploss = -0.343  # -34.30%

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.0106     # Positive offset 1.06%
trailing_stop_positive_offset = 0.0367  # Trigger offset 3.67%
```

**Design Philosophy**:
- The tiered ROI reflects a "time换取 space" philosophy: the longer you hold, the lower the take-profit target
- The generous 34.30% stop loss gives the strategy ample room for volatility
- Trailing stop activates once profit reaches 3.67%, protecting at least 1.06% of gains

### 2.2 Order Type Configuration

```python
order_types = {
    'entry': 'limit',
    'exit': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}

order_time_in_force = {
    'entry': 'GTC',
    'exit': 'GTC'
}
```

### 2.3 Hyperopt-Optimized Parameters

**Entry Parameters (6 total)**:

```python
buy_params = {
    "bbdelta-close": 0.00642,      # Bollinger Band delta to close price ratio threshold
    "bbdelta-tail": 0.75559,      # Lower wick to delta ratio threshold
    "close-bblower": 0.01415,     # Close price to lower Bollinger Band ratio threshold
    "closedelta-close": 0.00883,  # Price change to close price ratio threshold
    "fisher": -0.97101,           # Fisher RSI threshold
    "volume": 18,                  # Volume multiple threshold
}
```

**Exit Parameters (2 total)**:

```python
sell_params = {
    "sell-bbmiddle-close": 0.95153,  # Bollinger middle band to close price ratio
    "sell-fisher": 0.60924,          # Fisher RSI sell threshold
}
```

---

## III. Entry Conditions Details

### 3.1 New Position Entry Conditions (Mode A)

New positions use a composite judgment with the following core logic:

```
Fisher RSI < -0.97101
AND (
    Condition Group A1: Bollinger Band Narrowing Breakout
    OR
    Condition Group A2: Trend Pullback
)
```

**Condition Group A1 - Bollinger Band Narrowing Breakout**:

| Condition | Parameter | Description |
|----------|----------|-------------|
| Bollinger delta width | `bb1-delta > close × 0.00642` | Ensure sufficient room for volatility |
| Price change | `closedelta > close × 0.00883` | Confirm meaningful price movement |
| Lower wick length | `tail < bb1-delta × 0.75559` | Short wick means weak seller support |
| Lower band breakout | `close < lower_bb1.shift()` | Close price breaks below previous candle's lower band |
| No price rise | `close ≤ close.shift()` | Close price not higher than previous candle |

**Condition Group A2 - Trend Pullback**:

| Condition | Parameter | Description |
|----------|----------|-------------|
| Trend confirmation | `close < ema_slow` | Price below 48-period EMA |
| Deep lower band penetration | `close < 0.01415 × lower_bb2` | Price deep in lower band region |
| Volume contraction | `volume < volume_mean_slow × 18` | Low volume may indicate false decline |

### 3.2 Position Addition Conditions (Mode B)

When an active position exists, entry conditions are simplified:

| Condition | Description |
|-----------|-------------|
| Price rising | `close > close.shift()` — Close above previous candle |
| Trend confirmation | `close > sar` — Price above SAR indicator, confirming uptrend |

### 3.3 Entry Condition Classification

| Condition Group | Trigger Scenario | Core Logic |
|----------------|-----------------|------------|
| A1 | Bollinger Band Breakout | Capture downward breakout after Bollinger Band compression, betting on a rebound |
| A2 | Trend Pullback | Bottom-fishing after volume contraction |
| B | Position Addition | Trend-confirmed addition to existing position |

---

## IV. Exit Logic Details

### 4.1 Tiered Take-Profit System

The strategy employs time-based tiered ROI exits:

```
Hold Time     Target     Cumulative Return
─────────────────────────────────────────
0 minutes     4.35%      Open profit immediately
5 minutes     3.73%      Quick exit
8 minutes     2.57%      Moderate reduction
10 minutes    1.90%      Allow more room
76 minutes    1.28%      Hold ~1.3 hours
235 minutes   0.70%      Hold ~4 hours
415+ minutes  0%         Rely on trailing stop
```

**Design Intent**:
- Immediately set a high take-profit target (4.35%) upon opening
- Gradually lower expected returns as time passes
- After 7 hours, fully rely on trailing stop

### 4.2 Signal-Triggered Exit

```python
# Exit signal conditions
conditions = (
    close × 0.95153 > mid_bb2    # Close price near Bollinger middle band
    AND ema_fast > close          # Fast EMA trending downward
    AND fisher_rsi > 0.60924     # Fisher RSI enters overbought zone
    AND volume > 0               # Volume present
)
```

### 4.3 Trailing Stop Mechanism

| Parameter | Value | Description |
|-----------|-------|-------------|
| Trigger offset | 3.67% | Trailing stop activates after profit reaches this value |
| Positive offset | 1.06% | Stop line set at 1.06% profit |
| Activation condition | Profit > 3.67% | Trailing stop not engaged before threshold |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|-------------------|-------------------|------------|---------|
| Bollinger Bands | BB1 | Period 40, based on close | Primary BB, delta calculation |
| Bollinger Bands | BB2 | Period 20, based on typical price | Secondary BB, exit judgment |
| Trend Indicators | EMA_fast | Period 6 | Fast trend judgment |
| Trend Indicators | EMA_slow | Period 48 | Slow trend judgment |
| Trend Indicators | SAR | Default parameters | Trend acceleration indicator |
| Momentum Indicators | RSI | Period 9 | Relative Strength Index |
| Momentum Indicators | Fisher RSI | RSI transformation | Normalized momentum signal |
| Volume | volume_mean_slow | Period 24 | Volume moving average |

### 5.2 Fisher-Transformed RSI

Fisher transformation normalizes RSI to a normal distribution. Core advantages:

- **Extreme value sensitivity**: More sensitive to overbought/oversold zones
- **Smoothness**: Reduces the jagged fluctuations of plain RSI
- **Threshold symmetry**: Buy threshold -0.97, sell threshold 0.61, forming a symmetric range

### 5.3 Bollinger Band Delta Calculation

```python
# Delta = Upper band - Lower band
bb1_delta = bb1_upper - bb1_lower

# Delta to close ratio
bb1_delta_close_ratio = bb1_delta / close
```

Delta represents Bollinger Band width; compressed delta means lower volatility, potentially brewing a big move.

---

## VI. Risk Management Highlights

### 6.1 Order Timeout Protection

| Scenario | Trigger Condition | Handling |
|----------|-------------------|----------|
| Buy order | Price rises more than 1% above order price | Auto-cancel |
| Sell order | Price falls more than 1% below order price | Auto-cancel |

**Design Purpose**: Prevent unfavorable fills during violent price swings.

### 6.2 Volume Filtering

New positions require volume to satisfy:

```python
volume < volume_mean_slow.shift(1) × 18
```

This ensures the strategy does not chase during abnormal volume spikes, avoiding buying at peaks.

### 6.3 ROI Ignore Mechanism

```python
ignore_roi_if_entry_signal = True
```

When a new entry signal appears during an existing position, the strategy ignores the current ROI take-profit plan, allowing position accumulation. This is a pyramid strategy that can amplify gains but also increases risk.

### 6.4 Profit-Only Exit

```python
exit_profit_only = True
exit_profit_offset = 0.01
```

Exit conditions only trigger when the position is profitable, with a 1% profit offset protection.

---

## VII. Strategy Pros & Cons

### Pros

1. **Dual entry modes**: Captures both Bollinger Band breakouts and trend pullbacks, increasing signal diversity
2. **Fisher transformation**: Normalizes RSI, reducing extreme value impact, improving signal quality
3. **Tiered ROI**: Dynamically adjusts take-profit targets based on hold time, balancing efficiency and room
4. **SAR confirmation**: Uses parabolic SAR to assist trend judgment and filter false signals
5. **Parameter optimization**: All 6 entry + 2 exit parameters are Hyperopt-optimized

### Cons

1. **High stop loss risk**: -34.30% stop may lead to significant single-trade losses
2. **Frequent trading**: 5-minute timeframe may generate excessive signals, increasing transaction costs
3. **Parameter sensitivity**: 8 adjustable parameters depend on historical data optimization, overfitting risk
4. **Bollinger Band limitations**: May repeatedly trigger false signals in sustained trending markets
5. **Low profit-to-loss ratio**: Take-profit 4% vs stop-loss 34%, requires ~8.5% win rate just to break even

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|--------------------|---------------------------|-------------|
| High volatility | Default parameters | Bollinger Band breakouts need volatility |
| Ranging markets | Default parameters | Price oscillating between bands is ideal |
| Trending markets | Use with caution | May trigger high stop loss or exit too early |
| Low volatility | Not recommended | Signal quality degrades without volatility |

### Recommended Operations

1. **Backtesting**: Use at least 3 months of historical data
2. **Parameter optimization**: Regularly re-run Hyperopt
3. **Capital management**: Single trade risk not exceeding 2-3% of total capital
4. **Monitor operation**: Close observation of signal accuracy initially
5. **Stop loss discipline**: Strictly enforce stop loss, never widen it

---

## IX. Applicable Market Environment Details

ClucFiatROI is a typical Bollinger Band breakout strategy. Based on its code architecture and logic, it performs best in **high-volatility ranging markets** and poorly in **sustained trending markets**.

### 9.1 Core Strategy Logic

- **Bollinger Band breakout**: Capture price breakout moves after Bollinger Band compression
- **Fisher RSI confirmation**: Use normalized momentum indicator to confirm oversold/overbought
- **Tiered take-profit**: Time-based dynamic exits, quick profit-taking
- **Volume filtering**: Avoid chasing, seek bottom-fishing opportunities after volume contraction

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Bull trend | Poor | Exits too early, misses big moves; Fisher RSI persistently overbought |
| Volatile oscillation | Excellent | Best scenario, Bollinger Bands provide repeated opportunities |
| Bear trend | Poor | Frequent bottom-fishing gets caught, may trigger 34% stop loss |
| Low-volatility consolidation | Very Poor | Bollinger Bands don't compress, no valid signals |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|---------------|-------------------|-------------|
| Pair selection | High-volatility coins | ETH, SOL and other major coins with moderate volatility |
| Timeframe | 5 minutes (default) | May try 15 minutes to reduce noise |
| Stop loss ratio | Not recommended to change | 34% is the optimized value |
| Trailing stop | Recommend enabling | Key mechanism for protecting profits |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

ClucFiatROI contains 8 Hyperopt-optimized parameters (6 entry + 2 exit). Understanding requires:

- Bollinger Band breakout logic
- Fisher transformation principles
- Tiered ROI mechanism
- Trailing stop trigger conditions

Newcomers should thoroughly test in a simulated environment before live trading.

### 10.2 Overfitting Risk

All 8 parameters are optimized on historical data, with the following risks:

- **Historical optimum ≠ Future optimum**: Parameters may be overfitted to historical prices
- **Market environment changes**: Parameters may失效 when volatility and trend patterns change
- **Parameter drift**: Need to periodically re-optimize parameters

### 10.3 Backtesting vs. Live Trading Differences

| Difference | Backtesting | Live Trading |
|------------|-------------|--------------|
| Slippage | Often ignored | Actually exists, affects returns |
| Execution | Assumes full fills | May partially fill or fail |
| Latency | No delay | Network delay affects fill prices |
| Liquidity | Not considered | Insufficient depth may prevent fills |

### 10.4 Manual Trader Suggestions

For traders who want to manually reference this strategy:

1. **Watch for Bollinger Band compression**: This is the core signal
2. **Combine with Fisher RSI**: Below -0.97 may be a buying opportunity
3. **Tiered take-profit**: Set batch take-profit orders
4. **Strict stop loss**: 34% is too large; manual traders should set 10-15%

---

## XI. Summary

**ClucFiatROI** is a cleverly designed high-frequency trading strategy that combines Bollinger Band narrowing breakouts with Fisher RSI confirmation to find short-term trading opportunities in volatile markets. Its core value lies in:

1. **Multi-dimensional confirmation**: Bollinger Bands + Fisher RSI + Volume + SAR multiple confirmations reduce false signals
2. **Dynamic exits**: Tiered ROI mechanism adjusts targets based on hold time, balancing efficiency and room
3. **Controlled risk**: Trailing stop protects profits; order timeout prevents extreme-price fills

For quantitative traders, ClucFiatROI provides a complete Bollinger Band breakout strategy framework suitable for short-term trading in volatile markets. However, be aware of the risks from its high stop loss (-34.30%). Use it with strict capital management and regular parameter optimization. For traders seeking steady returns, carefully evaluate its high-risk characteristics or consider adjusting the stop-loss ratio before use.
