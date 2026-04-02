# ClucFiatSlow Strategy Analysis

> **Strategy ID**: #92 (465 strategies, 92nd)  
> **Strategy Type**: Bollinger Band Breakout + Fisher RSI + Mid-to-Low Frequency Swing Trading  
> **Timeframe**: 15 Minutes (15m)

---

## I. Strategy Overview

ClucFiatSlow is a mid-to-low frequency trading strategy based on Bollinger Bands and inverse Fisher-transformed RSI. It is the slower version of ClucFiatROI. The strategy captures breakout moves following Bollinger Band compression, combined with volume filtering and trend confirmation, to identify medium-cycle trading opportunities in volatile markets. Compared to the ROI version's 5-minute timeframe, the Slow version uses a 15-minute timeframe, significantly reducing trading frequency and market noise interference.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 2 independent entry modes (new position + pyramid) |
| **Exit Conditions** | Tiered ROI + trailing stop + signal-triggered exit |
| **Protection Mechanisms** | Order timeout protection + volume filtering + stop-loss mechanism |
| **Timeframe** | 15m primary |
| **Dependencies** | ta-lib (technical indicator calculation) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.03562,     # Immediate exit at 3.56%
    "15": 0.02987,    # Exit at 2.99% after 15 minutes
    "30": 0.01854,    # Exit at 1.85% after 30 minutes
    "60": 0.01321,    # Exit at 1.32% after 60 minutes
    "180": 0.009,     # Exit at 0.90% after 180 minutes
    "360": 0.005,     # Exit at 0.50% after 360 minutes
    "720": 0,         # After 720 minutes, no ROI target
}

# Stop Loss
stoploss = -0.252

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.0091
trailing_stop_positive_offset = 0.0258
trailing_only_offset_is_reached = True
```

**Design Philosophy**:
- Tiered ROI design encourages early profit-taking, gradually lowering expected returns as hold time increases
- After 720 minutes (12 hours), fully relies on trailing stop, allowing the strategy to capture larger moves in trends
- 25.2% stop loss is more conservative than the ROI version, suitable for the risk control philosophy of mid-to-low frequency trading

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "limit",
    "exit": "limit",
    "stoploss": "market",
    "stoploss_on_exchange": False,
}

order_time_in_force = {
    "entry": "GTC",
    "exit": "GTC",
}
```

### 2.3 Entry Parameters (Hyperopt-Optimized)

```python
buy_params = {
    "bbdelta-close": 0.00835,      # Bollinger Band delta to close price ratio threshold
    "bbdelta-tail": 0.68234,       # Lower wick to delta ratio ceiling
    "close-bblower": 0.01082,      # Close price to lower Bollinger Band ratio
    "closedelta-close": 0.00765,   # Price change to close price ratio threshold
    "fisher": -0.88923,            # Fisher RSI entry threshold (oversold zone)
    "volume": 24,                  # Volume multiple ceiling
}
```

### 2.4 Exit Parameters

```python
sell_params = {
    "sell-bbmiddle-close": 0.96312,  # Bollinger middle band to close price ratio
    "sell-fisher": 0.57234,          # Fisher RSI exit threshold (overbought zone)
}
```

---

## III. Entry Conditions Details

### 3.1 Protection Mechanism Overview

The strategy has multi-layered protection mechanisms ensuring entry signal validity:

| Protection Type | Parameter Description | Default Value |
|-----------------|----------------------|---------------|
| Order timeout protection | Cancel buy order if price exceeds order price by 1% | 0.01 |
| Volume filtering | New position volume must be below 24× the moving average | 24 |
| Fisher filtering | Fisher RSI must be below threshold before buying | -0.88923 |

### 3.2 Entry Mode Classification

The strategy uses dual entry modes designed for different market states:

#### Mode A: New Position Entry

**Prerequisite**: Fisher RSI < -0.88923 (market in oversold state)

Satisfy **either Condition Group A1 or Condition Group A2**:

**Condition Group A1 - Bollinger Band Narrowing Breakout**:
```python
# Core logic
- bbdelta > close × 0.00835        # Bollinger Band width sufficient
- closedelta > close × 0.00765     # Price has clear movement
- tail < bbdelta × 0.68234          # Short lower wick (weak seller support)
- close < lower_bb1.shift()          # Close breaks below lower Bollinger Band
- close ≤ close.shift()             # Close not above previous candle
```

**Condition Group A2 - Trend Pullback**:
```python
# Core logic
- close < ema_slow                  # Price below 72-period EMA
- close < 0.01082 × lower_bb2       # Price deep in lower band region
- volume < volume_mean × 24          # Volume contraction (low-volume decline)
```

#### Mode B: Adding to Existing Position

When an active position already exists, entry conditions are simplified:

```python
# Adding logic
- close > close.shift()             # Price above previous candle
- close > sar                       # Price above SAR indicator (trend confirmed)
```

### 3.3 Entry Condition Summary

| Mode | Condition Group | Core Logic | Market Meaning |
|------|----------------|-----------|---------------|
| New position | A1 | Breaks below lower band after Bollinger compression | Breakout reversal signal |
| New position | A2 | Price far from EMA with volume contraction | Oversold rebound opportunity |
| Adding | B | Price rising with confirmed uptrend | Trend-following addition |

---

## IV. Exit Logic Details

### 4.1 Multi-Layer Take-Profit System

The strategy uses a tiered ROI take-profit mechanism:

```
Hold Time      Target     Design Intent
────────────────────────────────────────────
0 minutes      3.56%      Immediate profit target
15 minutes     2.99%      Short-term hold target
30 minutes     1.85%      Medium-short term target
60 minutes     1.32%      1-hour target
180 minutes    0.90%      3-hour target
360 minutes    0.50%      6-hour target
720+ minutes   0%         Rely on trailing stop
```

### 4.2 Trailing Stop Mechanism

```python
# Trigger conditions
trailing_stop_positive_offset = 0.0258  # Activates after 2.58% profit
trailing_stop_positive = 0.0091         # Stop line locks in at 0.91% profit
```

**Mechanism description**:
- Activates trailing stop after profit reaches 2.58%
- Stop line locks at 0.91% profit position
- As price continues rising, stop line moves up
- Ensures at least partial profit is retained

### 4.3 Exit Signal Trigger Conditions

```python
# Exit signal
- close × 0.96312 > mid_bb2      # Close price near Bollinger middle band
- ema_fast > close                # 9-period EMA trending downward
- fisher_rsi > 0.57234            # Fisher RSI enters overbought zone
- volume > 0                       # Volume present
```

### 4.4 Special Exit Scenarios

| Scenario | Trigger Condition | Handling |
|----------|-------------------|----------|
| Order timeout | Sell price below order price by 1% | Cancel order |
| ROI trigger | Time-profit target reached | Exit at target price |
| Signal trigger | Exit condition combination met | Exit at market price |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|-------------------|-------------------|------------|---------|
| Bollinger Bands | BB1 | Period 40, based on close | Primary BB, delta calculation |
| Bollinger Bands | BB2 | Period 20, based on typical price | Secondary BB, exit judgment |
| Trend Indicators | EMA_fast | Period 9 | Fast trend judgment |
| Trend Indicators | EMA_slow | Period 72 | Slow trend judgment (longer than ROI version) |
| Trend Indicators | SAR | Default parameters | Trend acceleration indicator |
| Momentum Indicators | RSI | Period 9 | Relative Strength Index |
| Momentum Indicators | Fisher RSI | RSI transformation | Normalized momentum signal |
| Volume | volume_mean_slow | Period 32 | Volume moving average (longer than ROI version) |

### 5.2 Indicator Calculation Details

**Fisher RSI Calculation**:
```python
# RSI normalized transformation
rsi = ta.RSI(dataframe, timeperiod=9)
fisher_rsi = 0.5 * log((1 + rsi_normalized) / (1 - rsi_normalized))
```

**Bollinger Band Delta Calculation**:
```python
# Bollinger Band width
bb1_delta = bb1_upper - bb1_lower
# Price change
closedelta = abs(close - close.shift())
```

---

## VI. Risk Management Highlights

### 6.1 Stop Loss Mechanism

| Type | Parameter Value | Description |
|------|----------------|-------------|
| Hard stop | -25.20% | Single trade maximum loss limit |
| Trailing stop trigger | +2.58% | Trailing stop activates after this profit |
| Trailing stop position | +0.91% | Stop line lock-in position |

Compared to the ROI version's 27% stop loss, the Slow version uses a more conservative 25.2% stop loss, reflecting the mid-to-low frequency strategy's risk control philosophy.

### 6.2 Order Timeout Management

```python
# Buy order timeout
if buy_price > order_price × 1.01:
    cancel_order()  # Price up more than 1%, cancel order

# Sell order timeout
if sell_price < order_price × 0.99:
    cancel_order()  # Price down more than 1%, cancel order
```

### 6.3 Volume Filtering

```python
# New position volume limit
volume < volume_mean_slow.shift(1) × 24
```

Volume filtering prevents chasing during abnormal volume spikes. Compared to the ROI version's 18× limit, the Slow version relaxes to 24×, allowing a larger volume fluctuation range.

### 6.4 Position Management

```python
exit_profit_only = True           # Only allow exits when profitable
exit_profit_offset = 0.009        # Exit profit offset 0.9%
ignore_roi_if_entry_signal = True # Ignore ROI when entry signal appears
```

---

## VII. Strategy Pros & Cons

### Pros

1. **Dual timeframe design**: 15-minute primary with 72-period EMA reduces noise interference
2. **Dual entry modes**: Captures both breakout and pullback opportunities, increasing signal count
3. **Fisher transformation**: Normalizes RSI to [-1, 1] range, reducing extreme value impact
4. **Tiered ROI**: Dynamically adjusts take-profit targets based on hold time, balancing return and risk
5. **Trailing stop**: Protects realized profits while allowing larger gains when trends extend
6. **Longer hold time**: 720-minute ROI period suits traders who can't watch screens frequently

### Cons

1. **Moderate stop loss**: -25.20% stop loss can still result in significant single-trade losses
2. **Parameter sensitivity**: 6 entry + 2 exit parameters depend on Hyperopt optimization
3. **Bollinger Band dependency**: May失效 in sustained trending markets
4. **Longer holds**: Faces overnight risk and sudden news risk
5. **Profit-to-loss ratio challenge**: Take-profit 3.56% vs stop-loss 25.2%, requires high win rate

---

## VIII. Applicable Scenarios

| Market Environment | Recommendation | Description |
|--------------------|----------------|-------------|
| Volatile markets | Recommended | Bollinger Band breakouts need volatility |
| Ranging markets | Recommended | Price oscillating between bands captures swings |
| Swing trading | Recommended | Intraday to overnight hold periods |
| Mid-to-low frequency trading | Recommended | For investors who don't want frequent trading |
| Strong trending bull | Use with caution | May exit too early and miss big rallies |
| Strong trending bear | Use with caution | May trigger higher stop loss |
| Low volatility markets | Not recommended | Signal quality degrades without volatility |
| Ultra-short-term trading | Not recommended | 15-minute timeframe unsuitable for high frequency |

---

## IX. Applicable Market Environment Details

ClucFiatSlow is the mid-to-low frequency version of the Cluc series, positioned as a "steady swing trading hunter." Based on its code architecture and parameter design, it performs best in **volatile market swing trading** and poorly in **sustained trending markets**.

### 9.1 Core Strategy Logic

- **Timeframe advantage**: 15-minute timeframe is more stable than 5-minute, reducing false signals
- **Bollinger Band philosophy**: Ambush at volatility compression, profit from breakouts
- **Conservative stop loss**: 25.2% reflects mid-to-low frequency strategy's risk control
- **Long-period EMA**: 72-period moving average observes longer-term trends

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Mildly rising | Good | Swing trades can profit but may exit prematurely |
| Volatile oscillation | Excellent | Core scenario, Bollinger Band breakouts most effective |
| Sustained decline | Poor | May trigger stop loss or get caught buying the dip |
| High-frequency volatility | Moderate | 15-minute timeframe may miss quick moves |
| Consolidation | Poor | Bollinger Bands compress without breakout, sparse signals |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|---------------|-------------------|-------------|
| Number of pairs | 5-15 | Diversify risk, avoid single-asset concentration |
| Per-trade capital | 3-5% | Control total risk exposure under 25% stop loss |
| Backtest period | ≥ 3 months | Ensure coverage of multiple market states |
| Parameter optimization frequency | Quarterly | Regularly re-optimize parameters |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

ClucFiatSlow has 6 entry parameters and 2 exit parameters, 8 adjustable parameters total. Understanding each parameter's meaning and interactions requires time investment. Users should:

1. Test in simulated environment for 1-2 weeks first
2. Compare backtest results with live trading performance
3. Understand the math behind Bollinger Bands and Fisher RSI

### 10.2 Parameter Optimization Risk

Multi-parameter strategies have **overfitting risk**: parameters optimized on historical data may not work for the future. Specific manifestations:

- Excellent backtest performance but live trading losses
- Parameters perform very differently across market environments
- Need to periodically re-optimize parameters

### 10.3 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 1-5 pairs | 2GB | 4GB |
| 5-15 pairs | 4GB | 8GB |
| 15-30 pairs | 8GB | 16GB |

### 10.4 Backtesting vs. Live Trading Differences

**Backtesting limitations**:
- Cannot simulate slippage and liquidity issues
- Historical data doesn't include all market events
- Parameters may be overfitted to historical data

**Recommended process**:
1. Historical backtesting (≥3 months)
2. Paper trading (≥1 month)
3. Small-capital live trading (≤10% of capital)
4. Gradually increase position size

---

## XI. Summary

**ClucFiatSlow** is a cleverly designed mid-to-low frequency trading strategy — the slower version of ClucFiatROI. Through a 15-minute timeframe and longer EMA period (72-period), it maintains the ability to capture breakout opportunities while significantly reducing trading frequency and market noise interference.

Its core value lies in:

1. **Stable timeframe**: 15-minute is more stable than 5-minute, suitable for traders who can't watch screens frequently
2. **Longer hold periods**: 720-minute ROI period allows holding through an entire day, convenient for day-job workers
3. **Conservative risk control**: 25.2% stop loss is more conservative than the ROI version, reflecting mid-to-low frequency philosophy
4. **Flexible exit mechanism**: Tiered ROI + trailing stop combination balances profit protection with trend following

For quantitative traders, ClucFiatSlow provides a practical framework for swing trading in volatile markets. It is recommended to use it with strict risk management after thorough backtesting and small-capital live validation. Remember: **numerous parameters mean regular optimization is needed; past performance does not guarantee future returns**.
