# NFIX_BB_RPB_c7c477d_20211030 Strategy Analysis

> **Strategy ID**: #281 (281st of 465 strategies)  
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Protection  
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**NFIX_BB_RPB_c7c477d_20211030** is a highly complex multi-condition quantitative trading strategy, belonging to the NostalgiaForInfinity series derivative. The strategy combines Bollinger Bands (BB), RSI, moving average crossovers, and other technical indicators, with a complete take-profit and stop-loss mechanism.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 39 independent buy signals, each condition can be independently enabled/disabled |
| **Exit Conditions** | 1 base sell signal + multi-layer dynamic take-profit logic |
| **Protection Mechanisms** | 39 sets of buy protection parameters (EMA/SMA crossover protection) |
| **Timeframe** | 5-minute primary timeframe + 1-hour/1-day informational timeframes |
| **Dependencies** | TA-Lib, technical, qtpylib, pandas_ta |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table (time: minimum profit rate)
minimal_roi = {
    "0": 0.10,    # Immediate exit: 10% profit
    "30": 0.05,   # After 30 minutes: 5% profit
    "60": 0.02,   # After 60 minutes: 2% profit
}

# Stop-Loss Settings
stoploss = -0.10  # -10% hard stop-loss

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01    # 1% trailing activation point
trailing_stop_positive_offset = 0.03  # 3% offset trigger
```

**Design Philosophy**:
- Uses a **time-decaying ROI** strategy: the longer the holding period, the lower the exit threshold
- Pairs with **trailing stop** to lock in profits, suitable for trending markets
- Hard stop-loss at -10% controls maximum loss per trade
- Custom dynamic stop-loss adjusts protection levels based on profit levels

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'trailing_stop_loss': 'limit',
    'stoploss': 'limit',
    'stoploss_on_exchange': False,
    'stoploss_on_exchange_interval': 60,
    'stoploss_on_exchange_limit_ratio': 0.99
}
```

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms (39 Sets)

The strategy equips each entry condition with an independent protection parameter set:
- EMA crossover protection
- SMA crossover protection
- Safe dip/rise filtering
- Volume confirmation

### 3.2 Entry Condition Classification

The strategy contains 39 entry conditions, which can be categorized as follows:

| Condition Group | Count | Core Logic |
|-----------------|-------|-----------|
| Bollinger Band Rebound | 8 | Price rebounds after touching the lower Bollinger Band |
| RSI Oversold | 6 | Buy when RSI is below a specific threshold |
| Moving Average Golden Cross | 10 | Short-term MA crosses above long-term MA |
| Volume Confirmation | 5 | Volume surge confirms signal validity |
| Multi-Indicator Combination | 10 | Multiple indicators confirm together |

### 3.3 Custom Stop-Loss Logic

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    if current_profit > 0.2:
        return 0.05   # Above 20% profit: breakeven stop-loss
    elif current_profit > 0.1:
        return 0.03   # Above 10% profit: 3% stop-loss
    elif current_profit > 0.06:
        return 0.02   # Above 6% profit: 2% stop-loss
    elif current_profit > 0.03:
        return 0.01   # Above 3% profit: 1% stop-loss
    return 1  # Use default stop-loss
```

---

## IV. Exit Logic Details

### 4.1 Multi-Layer Take-Profit System

```
Profit Range      Threshold    Action
──────────────────────────────────────────────
[0%, 3%]          0.03        Activate trailing stop
[3%, 6%]          0.06        Tighten stop-loss to 2%
[6%, 10%]         0.10        Tighten stop-loss to 3%
[10%, 20%]        0.20        Tighten stop-loss to 5%
[>20%]            >0.20       Extreme profit protection
```

### 4.2 Base Sell Signal

The strategy contains 1 main sell condition:
- RSI overbought + price touching the upper Bollinger Band

### 4.3 HOLD Trade Support

The strategy supports configuring take-profit strategies for specific trades via the `nfi-hold-trades.json` file:
- Set independent take-profit per trade ID
- Set independent take-profit per trading pair

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | EMA, SMA, ZEMA, VIDYA | Determine market trend direction |
| Volatility Indicators | Bollinger Bands (BB) | Identify price volatility ranges |
| Momentum Indicators | RSI, RMI, MACD | Confirm buy/sell timing |
| Volume | Volume, OBV | Confirm signal validity |
| Advanced Indicators | Ichimoku, VWAP | Multi-dimensional market analysis |

### 5.2 Multi-Timeframe Analysis

The strategy uses three timeframes:
- **Primary Timeframe**: 5 minutes - generates trading signals
- **Informational Timeframe 1**: 1 hour - trend judgment
- **Informational Timeframe 2**: 1 day - long-term trend confirmation

---

## VI. Risk Management Features

### 6.1 Dynamic Stop-Loss Protection

The strategy's custom_stoploss function dynamically adjusts stop-loss levels based on current profit, ensuring profit protection when market conditions reverse.

### 6.2 Trailing Stop Mechanism

- Trailing stop activates when profit reaches 1%
- Trailing distance is 3%
- Only takes effect after the offset point is reached

### 6.3 Exchange Stop-Loss

Supports placing stop-loss orders at the exchange level:
- Stop-loss order checks every 60 seconds
- Stop-loss price is 99% of the latest price

---

## VII. Strategy Pros & Cons

### Advantages

1. **Multi-Condition Confirmation**: 39 entry conditions provide rich trade opportunity filtering
2. **Adaptive Stop-Loss**: Dynamically adjusts stop-loss based on profit levels
3. **Multi-Timeframe**: Combines short-term and long-term trends for higher accuracy
4. **HOLD Support**: Allows manual intervention for specific trades
5. **High Customizability**: Each condition can be independently enabled/disabled

### Limitations

1. **High Complexity**: 39 conditions make it difficult to fully understand each logic
2. **Many Parameters**: High optimization difficulty, prone to overfitting
3. **Resource Intensive**: Multi-timeframe calculations are computationally heavy
4. **Frequent Signals**: May generate too many trading signals

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Trending Market | Enable trend-type conditions | Capture medium-term trends |
| Ranging Market | Enable mean-reversion conditions | Buy low, sell high |
| High-Volatility Pairs | Tighten stop-loss | Prevent large drawdowns |
| Stable Pairs | Relax take-profit | Reduce frequent trading |

---

## IX. Applicable Market Environment Details

**NFIX_BB_RPB_c7c477d_20211030** is a classic variant of the Nostalgia series. Based on its code architecture and community long-term live-trading experience, it is best suited for **markets with clear trends**, while performance may be average in frequently ranging markets.

### 9.1 Strategy Core Logic

- **Multi-Indicator Resonance**: Signals trigger when multiple indicators meet conditions simultaneously
- **Bollinger Band Combination**: Uses statistical regression theory to capture price anomalies
- **Dynamic Protection**: Adjusts risk management parameters based on market state

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:---|:---|:---|
| Trending Upward | StarsStarsStarsStarsStars | Multi-condition confirms trend, trailing stop locks in profits |
| Trending Downward | StarsStarsStarsStars | Moving average protection reduces counter-trend trades |
| Ranging Market | StarsStarsStars | Bollinger Band rebound conditions are effective |
| High Volatility | StarsStarsStarsStars | Adaptive stop-loss protects profits |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Curve

This strategy involves 39 independent entry conditions, requiring a deep understanding of each condition's technical principles and applicable scenarios. It is recommended to start with default configuration and adjust gradually.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------------|-------------|----------------|
| 20-40 pairs | 2GB | 4GB |
| 40-80 pairs | 4GB | 8GB |
| 80+ pairs | 8GB | 16GB |

### 10.3 Backtesting vs. Live Trading Differences

Complex strategies are prone to overfitting. Recommendations:
- Use longer time periods for backtesting
- Test across different market environments
- Verify with small capital before scaling up

---

## XI. Summary

**NFIX_BB_RPB_c7c477d_20211030** is a highly complex derivative of the Nostalgia series. Its core value lies in:

1. **Multi-Condition Filtering**: 39 conditions provide a comprehensive market analysis perspective
2. **Adaptive Risk Management**: Dynamically adjusts stop-loss to protect profits
3. **Flexible Configuration**: Supports customization per trading pair and trade ID

For quantitative traders, this is a strategy suited for trending markets, but requires time to understand the interaction logic between various conditions. It is recommended to start with default parameters and optimize only after small-capital verification.
