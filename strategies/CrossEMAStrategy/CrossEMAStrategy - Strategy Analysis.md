# CrossEMAStrategy Strategy Analysis

> **Strategy ID**: #132 (132nd of 465 strategies)  
> **Strategy Type**: Dual EMA Crossover + Stochastic RSI Momentum  
> **Timeframe**: 1 hour (1h)

---

## I. Strategy Overview

**CrossEMAStrategy** is a clean trend-following strategy combining the classic dual EMA crossover system with the Stochastic RSI momentum indicator. Created by Crypto RobotFr and shared via YouTube and GitHub, it is one of the simplest strategies in the Freqtrade ecosystem.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 core condition (EMA golden cross + Stochastic RSI oversold) |
| **Sell Conditions** | 1 core condition (EMA death cross + Stochastic RSI overbought) |
| **Protection** | No independent entry protection parameters |
| **Timeframe** | 1 hour |
| **Dependencies** | ta (technical analysis library) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,      # 0-30 minutes: 10% profit
    "30": 0.05,     # 30-60 minutes: 5% profit
    "60": 0.02      # After 60 minutes: 2% profit
}

# Stop-Loss Setting
stoploss = -0.99  # -99% (actually managed by trailing stop)

# Trailing Stop
trailing_stop = True
```

**Design Philosophy**:
- **Aggressive first target**: Seeks 10% profit within 30 minutes of entry, suitable for high-volatility moves
- **Stepped exit**: Progressively lowered from 10% → 5% → 2%, balancing quick profit-taking with holding endurance
- **Extremely loose hard stop-loss**: -99% effectively disables traditional stop-loss; trailing stop takes over risk control

### 2.2 Order Type Configuration

```python
# Order Type Configuration
order_types = {
    "entry": "limit",
    "exit": "limit",
    "stoploss": "market",
    "stoploss_on_exchange": False
}

# Exit Signal Configuration
use_exit_signal = True
exit_profit_only = True
ignore_roi_if_entry_signal = False
```

---

## III. Entry Conditions Details

### 3.1 Core Entry Logic

The strategy uses a single entry condition combining trend confirmation with momentum filtering:

```python
# Buy condition
(dataframe['ema28'] > dataframe['ema48']) &  # EMA28 crosses above EMA48 (golden cross)
(dataframe['stoch_rsi'] < self.buy_stoch_rsi.value) &  # Stochastic RSI below threshold
(dataframe['volume'] > 0)  # Volume confirmation
```

**Triple-filter mechanism**:

| Filter Layer | Condition | Function |
|-------------|-----------|----------|
| **Trend Layer** | EMA28 > EMA48 | Confirm short-term trend is up |
| **Momentum Layer** | Stochastic RSI < buy threshold | Ensure price is in oversold zone, avoid chasing |
| **Quality Layer** | volume > 0 | Eliminate zero-volume false signals |

### 3.2 Adjustable Parameters

```python
# Buy-side Stochastic RSI threshold
buy_stoch_rsi = DecimalParameter(0.5, 1, decimals=3, default=0.8, space="buy")
```

**Parameter notes**:
- Range: 0.5 ~ 1.0
- Default: 0.8
- Meaning: Buy triggers when Stochastic RSI is below this threshold; higher = more conservative

---

## IV. Exit Logic Details

### 4.1 Core Exit Logic

```python
# Sell condition
(dataframe['ema28'] < dataframe['ema48']) &  # EMA28 crosses below EMA48 (death cross)
(dataframe['stoch_rsi'] > self.sell_stoch_rsi.value) &  # Stochastic RSI above threshold
(dataframe['volume'] > 0)  # Volume confirmation
```

**Signal logic**:

| Condition | Meaning |
|-----------|---------|
| EMA28 < EMA48 | Short-term trend turns down, death cross formed |
| Stochastic RSI > sell threshold | Momentum indicator shows overbought, price may top out |
| volume > 0 | Volume confirmation, avoids false breakouts |

### 4.2 Adjustable Parameters

```python
# Sell-side Stochastic RSI threshold
sell_stoch_rsi = DecimalParameter(0, 0.5, decimals=3, default=0.2, space="sell")
```

**Parameter notes**:
- Range: 0 ~ 0.5
- Default: 0.2
- Meaning: Sell triggers when Stochastic RSI is above this threshold; lower = more conservative

### 4.3 Trailing Stop

The strategy enables trailing stop:
- Automatically adjusts stop-loss point as price moves favorably
- With an extremely loose hard stop (-99%), actual risk control is primarily done by the trailing stop

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|-------------------|-------------------|-----------|---------|
| **Trend Indicator** | EMA (Exponential Moving Average) | 28, 48 | Dual EMA crossover for trend change judgment |
| **Momentum Indicator** | Stochastic RSI | Default 14-period | Overbought/oversold judgment |
| **Volume** | volume | - | Signal validity confirmation |

### 5.2 Indicator Calculation Details

#### EMA (Exponential Moving Average)
```python
dataframe['ema28'] = ta.trend.ema_indicator(dataframe['close'], 28)
dataframe['ema48'] = ta.trend.ema_indicator(dataframe['close'], 48)
```
- **EMA28**: Short-term EMA, more sensitive to price changes
- **EMA48**: Long-term EMA, filters short-term noise
- **Golden cross meaning**: EMA28 crossing above EMA48 indicates short-term momentum exceeds long-term, uptrend forming

#### Stochastic RSI
```python
dataframe['stoch_rsi'] = ta.momentum.stochrsi(dataframe['close'])
```
- **Stochastic RSI**: Maps RSI values to 0-1 range
- **Value < 0.2**: Oversold zone, potential rebound opportunity
- **Value > 0.8**: Overbought zone, potential correction pressure

### 5.3 Indicator Synergy Logic

```
Buy signal = EMA28 > EMA48 (trend turns up) + Stochastic RSI < 0.8 (price pulled back)
Sell signal = EMA28 < EMA48 (trend turns down) + Stochastic RSI > 0.2 (price rebounded)
```

This design ensures:
1. Won't chase buys after trend has already started
2. Won't hold counter-trend positions after trend has ended

---

## VI. Risk Management Highlights

### 6.1 Stepped ROI Exit

| Time Zone | Profit Target | Strategy Intent |
|-----------|--------------|-----------------|
| 0-30 minutes | 10% | Pursue quick profits in high-volatility moves |
| 30-60 minutes | 5% | Mid-term holding target, adapts to medium volatility |
| After 60 minutes | 2% | Prevent profit retracement, maintain flexibility |

**Design philosophy**: Early targets are aggressive, suitable for catching breakout moves; later targets are conservative, ensuring at least some profit is preserved.

### 6.2 Trailing Stop Mechanism

```python
trailing_stop = True
```

- **No hard trailing start**: Enabled from first profit
- **Dynamic adjustment**: Continuously raises stop-loss as price makes new highs
- **Paired with loose hard stop**: -99% hard stop effectively doesn't trigger; trailing stop handles all risk control

### 6.3 Pros & Cons of Ultra-Simplified Risk Control

| Advantage | Disadvantage |
|-----------|--------------|
| Strategy logic is clear and simple | No fixed stop-loss point for extreme losses |
| Fast backtest/live calculation | May experience larger drawdowns in one-sided moves |
| Few parameters, easy to optimize | Market adaptability depends on parameter tuning |

---

## VII. Strategy Pros & Cons

### Pros

1. **Extremely minimal code**: Entire strategy is only ~100 lines, easy to understand and modify
2. **Minimal parameters**: Only 2 adjustable parameters (buy/sell stoch_rsi thresholds), low optimization difficulty
3. **Dual filtering mechanism**: EMA confirms trend + Stochastic RSI filters false signals, reduces noise
4. **Efficient computation**: Only 3 indicators, fast backtest and live execution
5. **Historically validated**: Strategy author provided backtest data from 2017-2021

### Cons

1. **No independent protection mechanism**: Lacks dedicated capital protection, volatility protection parameters
2. **Hard stop-loss is nominal**: -99% threshold doesn't actually function in practice
3. **Single timeframe**: Only uses 1 hour, no multi-period confirmation
4. **Parameter sensitivity**: Default parameters may need adjustment for different markets

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Clear one-sided trending markets** | Keep default parameters | EMA crossover effectively catches trends |
| **High-volatility pairs** | Lower buy_stoch_rsi to 0.7 | Buy earlier, avoid missing moves |
| **Low-volatility pairs** | Raise buy_stoch_rsi to 0.9 | Wait for clearer oversold signals |
| **Ranging markets** | Adjust ROI table | Lower first target to 5-8% |

---

## IX. Applicable Market Environment Analysis

CrossEMAStrategy is one of the **simplest-coded** strategies in the Freqtrade ecosystem, focusing on the combination of dual EMA crossover and Stochastic RSI momentum. It performs best in **clear trending, moderate-volatility** markets.

### 9.1 Core Strategy Logic

- **Trend priority**: EMA crossover is the core, ensures trend-following trades
- **Momentum filtering**: Stochastic RSI avoids buying after trend has started
- **Simplicity first**: Removes complex multi-condition systems, focuses on core logic

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|---------:|
| Strong Uptrend | ⭐⭐⭐⭐⭐ | EMA golden cross effectively catches uptrend waves |
| Strong Downtrend | ⭐⭐⭐⭐ | Death cross signals effectively avoid downtrends |
| Wide-range oscillation | ⭐⭐⭐ | Crossover signals may produce frequent false signals in oscillation |
| Fast volatility | ⭐⭐⭐⭐ | 30-minute 10% target suitable for fast moves |
| Consolidation | ⭐⭐ | Frequent crossovers may lead to over-trading |

### 9.3 Key Configuration Recommendations

| Configuration Item | Suggested Value | Notes |
|-------------------|-----------------|-------|
| buy_stoch_rsi | 0.7-0.9 | Adjust based on market volatility; higher = more conservative |
| sell_stoch_rsi | 0.1-0.3 | Lower = more conservative; may miss some profits |
| minimal_roi."0" | 0.08-0.15 | Adjust based on volatility |
| timeframe | 1h | Keep; strategy designed specifically for 1h |

---

## X. Summary

**CrossEMAStrategy** is a minimalist trend-following strategy whose core value lies in:

1. **Simplicity**: Minimal code, easy to understand and modify
2. **Dual filtering**: EMA trend confirmation + Stochastic RSI momentum filtering
3. **Few parameters**: Only 2 adjustable parameters, clear optimization direction
4. **High-speed computation**: Suitable for running on large batches of trading pairs

For quantitative traders, CrossEMAStrategy is suitable as a beginner strategy or a benchmark for quick screening. Start with default parameters, observe strategy performance in live trading, then fine-tune based on specific trading pairs and market conditions.

**Usage Recommendation**: Since the strategy has no independent protection mechanism, it is recommended to use with external risk management tools in live trading, or to manually monitor abnormal market conditions.
