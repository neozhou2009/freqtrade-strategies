# SlowPotato Strategy - In-Depth Analysis

> **Strategy ID**: #384 (384th of 465 strategies)  
> **Strategy Type**: Mean Reversion + Range Trading  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

SlowPotato is a mean reversion strategy based on 5-day price range, developed by jadex. Its core philosophy is elegantly simple: buy near the 5-day average low, sell near the 5-day average high, profiting by capturing intraday price fluctuations. The name "SlowPotato" hints at its "slow and steady" trading style.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 buy signal, price touches 5-day average low |
| **Sell Conditions** | 1 sell signal, price touches 5-day average high |
| **Protection Mechanism** | Tiered ROI + Trailing stop + Fixed stop-loss |
| **Timeframe** | 5 minutes (5m), referencing 5 days (1440 candles) |
| **Dependencies** | talib, qtpylib, technical |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table (tiered take-profit)
minimal_roi = {
    "0":  0.10,   # Exit immediately at 10% profit
    "30": 0.05,   # Exit at 5% profit after 30 minutes
    "60": 0.02    # Exit at 2% profit after 60 minutes
}

# Stop-loss setting
stoploss = -0.10  # 10% fixed stop-loss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.02      # Activate after 2% profit
trailing_stop_positive_offset = 0.03  # Trailing distance 3%
```

**Design Philosophy**:
- **Tiered take-profit**: Longer holding time, lower profit target, encouraging quick profits
- **Trailing stop**: Activates after 2% profit, locking in gains
- **Dual protection**: Fixed 10% stop-loss + trailing stop, multi-layered risk control

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'market',
    'sell': 'market',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}

order_time_in_force = {
    'buy': 'gtc',
    'sell': 'gtc'
}
```

**Note**: Uses all market orders with GTC (Good Till Cancelled) validity.

### 2.3 Special Configuration

```python
use_sell_signal = True          # Use sell signal
sell_profit_only = True         # Only sell when profitable
ignore_roi_if_buy_signal = True # Ignore ROI when buy signal present
process_only_new_candles = False # Process every tick
```

---

## III. Buy Conditions Explained

### 3.1 Single Buy Signal

The strategy employs a single-signal entry design:

```python
# Buy signal
(
    (dataframe['low'] <= dataframe['low'].rolling(1440).mean()) &  # Price at or below 5-day average low
    (dataframe['volume'] > 0)                                        # Has volume
)
```

**Condition Breakdown**:

| Condition | Technical Meaning | Logic Explanation |
|-----------|-------------------|-------------------|
| Low <= 5-day average low | Price touches support level | Price falls to 5-day mean lower bound |
| Volume > 0 | Trading activity present | Avoids zero-volume anomalies |

### 3.2 Buy Logic Analysis

This is a classic **mean reversion strategy**:
1. **5-day window**: 1440 5-minute candles = 5 trading days
2. **Average low**: Mean of all candle lows within 5 days
3. **Entry timing**: When price touches or falls below this average, considered "undervalued" territory

**Core Philosophy**:
> Price oscillates within a 5-day range. Touching the lower bound is a buying opportunity, waiting for reversion to upper bound to sell.

---

## IV. Sell Logic Explained

### 4.1 Basic Sell Signal

```python
# Sell signal
(
    (dataframe['high'] >= dataframe['high'].rolling(1440).mean()) &  # Price at or above 5-day average high
    (dataframe['volume'] > 0)                                         # Has volume
)
```

**Design Philosophy**:
- Triggers sell when price touches 5-day average high
- Symmetrical with buy logic, forming complete "buy low, sell high" cycle

### 4.2 Multi-Layer Exit Mechanism

| Exit Type | Trigger Condition | Priority |
|-----------|-------------------|----------|
| Tiered ROI | Holding time determines take-profit target | High |
| Sell signal | Price touches 5-day average high | Medium |
| Trailing stop | Activates after 2% profit | Medium |
| Fixed stop-loss | Loss reaches 10% | Low |

### 4.3 Tiered ROI Details

```
Holding Time    Take-Profit Target
────────────────────
0 minutes       10%
30 minutes      5%
60 minutes      2%
```

**Logic**:
- High target at entry (10%), hoping for quick profit
- Lower target over time, avoiding profit giveback
- After 60 minutes, only requires 2% profit, timely exit

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|--------------------|-------------------|------------|---------|
| Price Channel | 5-day average low | 1440 candles | Buy trigger |
| Price Channel | 5-day average high | 1440 candles | Sell trigger |
| Volume | Volume | Default | Filter condition |

### 5.2 Indicator Calculation

```python
# 5-day average low (buy line)
buy_line = dataframe['low'].rolling(1440).mean()

# 5-day average high (sell line)
sell_line = dataframe['high'].rolling(1440).mean()
```

### 5.3 Strategy Characteristics

- **No technical indicators needed**: Doesn't use MACD, RSI or other complex indicators
- **Purely price-driven**: Only looks at price position relative to historical range
- **Fixed window**: Always references 5-day data, no dynamic adjustment

---

## VI. Risk Management Features

### 6.1 Tiered Take-Profit System

| Holding Time | Take-Profit Target | Design Intent |
|--------------|-------------------|---------------|
| 0-30 minutes | 10% | Quick profit target |
| 30-60 minutes | 5% | Moderately lower requirements |
| 60+ minutes | 2% | Timely exit |

**Characteristics**: Encourages quick profits, more conservative over time.

### 6.2 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_stop_positive = 0.02      # Activate after 2% profit
trailing_stop_positive_offset = 0.03  # Trailing distance 3%
```

**How It Works**:
1. After entry, if price rises 2% profit, trailing stop activates
2. Stop line always trails 3% below highest price
3. If price pulls back more than 3%, triggers stop exit

**Example**:
- Entry price: 100
- Highest price: 110 (10% profit)
- Trailing stop line: 106.7 (110 × 0.97)
- If drops below 106.7, triggers sell

### 6.3 Profit Protection

```python
sell_profit_only = True  # Only respond to sell signal when profitable
```

**Note**: Even if price touches 5-day average high, if currently at a loss, won't sell. This protects the strategy from forced exit at a loss due to signal trigger.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Simple and intuitive logic**: Buy low, sell high, matches intuition
2. **Very few parameters**: Only relies on 5-day mean, no complex indicators
3. **Trailing stop**: Automatically locks in floating profits, protects gains
4. **Tiered ROI**: Encourages quick profits, avoids long holding periods
5. **Profit protection**: sell_profit_only ensures no selling at a loss

### ⚠️ Limitations

1. **Mean reversion assumption**: Assumes price oscillates within range, not suitable for trending markets
2. **Fixed window**: Doesn't adjust window size based on market volatility
3. **No trend filter**: May be repeatedly trapped in one-sided trends
4. **Slippage risk**: Liquidity may be poor near average high/low prices

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|--------------------|---------------------------|-------------|
| Sideways ranging market | Default configuration | Normal mean reversion logic |
| One-sided uptrend | Not recommended | Price continuously breaks upper bound, buy signals失效 |
| One-sided downtrend | Not recommended | Price continuously breaks lower bound, frequent stop-losses |
| High volatility | Wider stop-loss | 10% stop-loss may be too narrow |

---

## IX. Applicable Market Environment Details

SlowPotato is a classic **mean reversion strategy**. Based on its code architecture, it is most suitable for **sideways ranging markets** and performs poorly in trending markets.

### 9.1 Strategy Core Logic

- **Range trading**: Buy low, sell high within 5-day price range
- **Mean reversion**: Assumes price will revert to range center
- **Quick profit-taking**: Lower profit targets over longer holding periods

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 One-sided bull market | ⭐☆☆☆☆ | Price continuously breaks upper bound, buy signals don't trigger |
| 🔄 Sideways ranging | ⭐⭐⭐⭐⭐ | Perfect match for mean reversion logic |
| 📉 One-sided bear market | ⭐☆☆☆☆ | Price continuously breaks lower bound, frequent stop-losses |
| ⚡️ High volatility | ⭐⭐☆☆☆ | Range frequently broken, signals may fail |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|--------------------|-------------------|-------------|
| stoploss | -0.10 ~ -0.15 | Keep or moderately widen |
| trailing_stop_positive | 0.02 | Keep default |
| minimal_roi | Adjust appropriately | Based on trading pair volatility |

---

## X. Important Note: Risks of Mean Reversion

### 10.1 Learning Curve

SlowPotato strategy has a very low learning curve:
- Only relies on price mean, no complex indicators
- About 80 lines of code, easy to understand
- Core logic intuitive, matches trading intuition

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|----------------|-------------------|
| 1-10 pairs | 1GB | 2GB |
| 10-50 pairs | 2GB | 4GB |
| 50+ pairs | 4GB | 8GB |

### 10.3 Backtest vs Live Trading Differences

- Range calculation may be idealized in backtesting
- Slippage may erode profits in live trading
- Liquidity issues near average high/low prices in live trading

### 10.4 Recommendations for Manual Traders

Manual traders can adopt similar thinking:
1. Observe 5-day price range
2. Place buy orders at range lower bound
3. Place sell orders at range upper bound
4. Set stop-loss and take-profit

---

## XI. Summary

**SlowPotato** is a concise mean reversion strategy. Its core value lies in:

1. **Clear logic**: Buy low, sell high, simple and intuitive
2. **Very few parameters**: Only relies on price range, no complex indicators
3. **Comprehensive risk control**: Tiered ROI + trailing stop + profit protection

For quantitative traders, SlowPotato is an excellent mean reversion entry strategy. However, note it only works in sideways ranging markets and may fail in trending conditions. Recommend pairing with trend filter indicators or only enabling when market is determined to be ranging.

---