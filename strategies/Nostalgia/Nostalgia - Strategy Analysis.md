# Nostalgia Strategy Analysis

> **Strategy ID**: #1 (1st of 465 strategies)  
> **Strategy Type**: Multi-Condition Trend Following + Protection Mechanisms  
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**Nostalgia** is a highly complex multi-condition quantitative trading strategy designed for the Freqtrade trading platform. Based on its name, it may be a modern reconstruction of a classic strategy, combining various classical technical indicators and risk management methods.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 31 independent buy signals, each condition can be independently enabled/disabled |
| **Exit Conditions** | 8 base sell signals + multi-layer dynamic take-profit logic |
| **Protection Mechanisms** | 31 sets of buy protection parameters (EMA/SMA/safe dip/safe pump) |
| **Timeframe** | 5-minute primary timeframe + 1-hour informational timeframe |
| **Dependencies** | TA-Lib, technical, qtpylib |

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

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "limit",      # Limit order entry
    "exit": "limit",       # Limit order exit
    "stoploss": "limit",   # Limit stop-loss order
    "stoploss_on_exchange": False,
    "exit_timeout_count": 0,
}
```

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms (31 Sets)

Each entry condition has an independent protection parameter set:

| Protection Type | Parameter Description | Default Example |
|-----------------|----------------------|-----------------|
| **Fast EMA** | Whether fast EMA is above EMA200 | ema_fast_len=26 |
| **Slow EMA** | Whether 1h slow EMA is above EMA200 | ema_slow_len=100 |
| **Close Price Protection** | Whether close price is above EMA | close_above_ema_fast_len=200 |
| **SMA200 Rising** | Whether SMA200 is in an uptrend | sma200_rising_val=28 |
| **Safe Dip** | Dip magnitude threshold protection | safe_dips_type=80 |
| **Safe Pump** | Pump magnitude threshold protection (anti-chase) | safe_pump_type=70 |
| **BTC Trend** | Whether BTC 1h is not in a downtrend | btc_1h_not_downtrend |

### 3.2 Typical Entry Condition Examples

#### Condition #1: RSI Oversold + Low MFI
```python
# Logic
- RSI(1h) between 30-84
- RSI(14) < 36 (oversold zone)
- MFI < 44 (low money flow)
- Price has minimum rise from 36-period low
```

#### Condition #2: Bollinger Band Lower Band Breakout
```python
# Logic
- RSI < RSI(1h) - 39 (relatively weak)
- MFI < 49
- Close price < BB lower band × 0.983 (deep break)
```

#### Condition #3: Bollinger Band 40-Period Reversal
```python
# Logic
- BB40 lower band > 0
- BB40 bandwidth change > close price × 5.9%
- Close change > close price × 2.3%
- Tail < BB40 bandwidth × 41.8%
- Close price < previous BB40 lower band
```

#### Conditions #5-7: EMA Crossover + Bollinger Band
```python
# Common Logic
- EMA26 > EMA12 (golden cross)
- EMA difference > open price × coefficient
- Close price < BB lower band × offset coefficient
```

### 3.3 31 Entry Conditions Classification

| Condition Group | Condition Numbers | Core Logic |
|-----------------|-------------------|------------|
| **Oversold Rebound** | 1, 7, 8, 18, 20, 21 | RSI/MFI low value + oversold signal |
| **Bollinger Band Strategy** | 2, 3, 4, 5, 6, 9, 10, 14, 18, 22, 23 | Price breaks BB lower band |
| **EMA Trend** | 5, 6, 7, 14, 15 | EMA golden cross + price position |
| **SMA Offset** | 9, 10, 11, 12, 13, 16, 17 | Price below SMA at specific ratio |
| **EWO Momentum** | 12, 13, 16, 17, 22, 23 | Elliott Wave Oscillator |
| **Special Conditions** | 19, 24, 25, 26, 27 | Combined indicators (Chopiness, Zema, Hull, Williams %R) |

---

## IV. Exit Logic Details

### 4.1 Multi-Layer Take-Profit System

The strategy uses a **tiered take-profit** mechanism, dynamically adjusting exit conditions based on profit rate:

```
Profit Range          RSI Threshold    Signal Name
─────────────────────────────────────────────────────
> 20%                 < 34            signal_profit_11
16%-20%               < 42            signal_profit_10
14%-16%               < 54            signal_profit_9
12%-14%               < 55            signal_profit_8
10%-12%               < 54            signal_profit_7
8%-10%                < 52            signal_profit_6
7%-8%                 < 45            signal_profit_5
6%-7%                 < 43            signal_profit_4
5%-6%                 < 42            signal_profit_3
4%-5%                 < 37            signal_profit_2
3%-4%                 < 35            signal_profit_1
2%-3%                 < 34            signal_profit_0
```

### 4.2 Special Exit Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| **EMA200 Below Exit** | Price < EMA200 + profit threshold met | signal_profit_u_* |
| **Pump Protection** | 48h/36h/24h pump detection + profit | signal_profit_p_* |
| **Downtrend** | SMA200 declining + profit range | signal_profit_d_* |
| **Trailing Take-Profit** | Max profit drawdown + RSI range | signal_profit_t_* |
| **Holding Duration** | Held > 900 minutes + profit | signal_profit_l_1 |
| **Williams %R** | R(480) > threshold + profit | signal_profit_w_* |

### 4.3 Base Sell Signals

```python
# Sell Signal 1: Continuous BB upper band breakout
- RSI > 79.5
- Close price > BB20 upper band (5 consecutive candles)

# Sell Signal 2: Short-term overbought
- RSI > 81
- Close price > BB20 upper band (2 consecutive candles)

# Sell Signal 4: Dual RSI overbought
- RSI > 73.4
- RSI(1h) > 79.6

# Sell Signal 6: EMA below overbought
- Close price < EMA200
- Close price > EMA50
- RSI > 79

# Sell Signal 7: 1h RSI extreme + EMA death cross
- RSI(1h) > 81.7
- EMA12 crosses below EMA26
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Trend Indicators** | EMA(12,15,20,25,26,35,50,100,200) | Trend judgment, protection mechanisms |
| **Momentum Indicators** | RSI(4,14,20), MFI, EWO | Overbought/oversold, momentum strength |
| **Volatility Indicators** | Bollinger Bands(20,2), BB(40,2) | Price boundaries, breakout signals |
| **Money Flow** | CMF(20) | Capital inflow/outflow |
| **Special Indicators** | Williams %R(480), StochRSI(96) | Extreme market identification |
| **Custom Indicators** | TSI, Hull(75), Zema(61), Zlema(68) | Smoothed trends, lag reduction |

### 5.2 Informational Timeframe Indicators (1h)

The strategy uses 1-hour timeframe as an information layer, providing higher-dimensional trend judgment:

- EMA/SMA trend confirmation
- RSI overbought/oversold (1h level)
- Pump/dip protection detection (24h/36h/48h)
- BTC trend correlation analysis

---

## VI. Risk Management Features

### 6.1 Dip Protection (Safe Dips)

11 levels of dip threshold protection, from strict to relaxed:

```
Level    Threshold 1    Threshold 2    Threshold 3    Threshold 4
──────────────────────────────────────────────────────────────────
10       1.5%           10%           24%           42%
50       2.0%           14%           32%           50%
80       2.4%           22%           38%           66%
100      2.6%           24%           42%           80%
110      2.7%           26%           44%           84%
```

### 6.2 Pump Protection (Safe Pump)

12 levels of pump detection to prevent chasing:

- Detection periods: 24h / 36h / 48h
- Threshold range: 0.42 - 2.0 (42% - 200% rise)
- Drawdown threshold: 1.4 - 3.0

### 6.3 Hold Trades

Supports external config file `hold-trades.json` to specify certain trading pairs to hold until target profit rate:

```json
{
  "profit_ratio": 0.005,
  "trade_ids": [123, 456]
}
```

---

## VII. Strategy Pros & Cons

### Advantages

1. **Highly Configurable**: 31 entry conditions can be independently enabled, adapting to different market environments
2. **Multi-Layer Protection**: 31 sets of protection parameters + 11-level dip protection + 12-level pump protection
3. **Dynamic Take-Profit**: Dynamically adjusts exit points based on profit rate and RSI
4. **Multi-Timeframe**: 5m execution + 1h trend confirmation + BTC correlation analysis
5. **Classic Indicator Combinations**: Integrates Bollinger Bands, RSI, EMA, EWO and other classic indicators

### Limitations

1. **High Complexity**: Many parameters, difficult optimization and debugging
2. **Depends on Historical Data**: Requires sufficient 1h and 5m historical data
3. **External Dependencies**: Requires TA-Lib and technical library support
4. **Overfitting Risk**: 31 conditions may lead to overfitting historical data
5. **Computationally Intensive**: Each cycle calculates many indicators, demanding on performance

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| **Ranging Market** | Enable conditions 2,3,4,9,10,14,18 | Bollinger Band strategy dominant |
| **Uptrend** | Enable conditions 1,5,6,7,15,16 | EMA trend + oversold rebound |
| **Downtrend** | Enable conditions 12,13,17,26,27 | EWO negative + extreme oversold |
| **High Volatility** | Enable all protection parameters | Strict dip/pump protection |
| **Low Volatility** | Relax protection thresholds | Reduce false filtering |

---

## IX. Applicable Market Environment Details

NostalgiaForInfinity (NFI) is one of the most well-known and complex open-source strategies in the Freqtrade ecosystem. Rather than relying on a single logic, it addresses complex and volatile crypto markets through **dozens of entry conditions, multi-layer trend filtering, and a dynamic risk management system**.

Based on its code architecture and community long-term live-trading experience, it is best suited for **ranging markets with clear trends**, while performance is poor during one-sided selloffs or sideways consolidation.

### 9.1 Strategy Core Logic: "Defense Net" Built with Complexity

NFI strategy code volume is typically 10,000+ lines, and its core architecture determines it leans toward **pursuing high win rates** rather than single-trade windfalls.

- **Multi-Dimensional Entry Conditions**: The strategy has 20-40 different entry conditions (such as oversold rebound, trend breakout, pullback confirmation, etc.). You don't need to guess which market condition will come; the strategy automatically triggers corresponding entry logic based on current market environment.
- **Strict Risk Filtering**: This is the strategy's essence. It real-time detects "24h/36h/48h rises" (Pump Detection) to avoid chasing; via "BTC 1h trend detection", if Bitcoin's broader market is in a downtrend, the strategy pauses most altcoin entries — an extremely important survival rule in crypto.
- **Dynamic Position Management**: Unlike simple grid or martingale strategies, NFI supports "Hold Support" feature, allowing "won't exit until profitable" rules for specific losing trades, or differentiated take-profit targets for different trading pairs, greatly enhancing ability to hold through drawdowns.

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:---|:---|:---|
| Slow Bull/Ranging Upward | StarsStarsStarsStarsStars (Best) | EMA/SMA trend filtering opens more entry conditions during upward trends, accumulates positions via Dip Buying, strongest profitability |
| Wide Ranging | StarsStarsStars (Neutral) | Its numerous take-profit conditions (auto-sell at resistance) can capture some band profits. But ranging markets produce many false breakouts, may increase trade frequency and wear costs |
| One-Sided Selloff | StarsStars (Poor) | Though has BTC trend filtering and stop-loss mechanism, NFI is essentially a **trend strategy**. In sudden selloffs (e.g., 312, 519 events), liquidity exhaustion may cause stop-loss slippage. However, its "multi-condition filtering" helps stop opening new positions early in selloffs, avoiding "bottom-fishing at half the mountain" |
| Extreme Sideways | Star (Extremely Poor) | When market volatility is extremely low with no clear trend, most NFI entry conditions won't trigger (indicator thresholds not met). Strategy goes into "dormancy", capital utilization low |

### 9.3 Key Configuration Recommendations

To run this strategy well, it cannot be used out of the box. Follow the developer's recommendations:

| Config Item | Recommended Value | Description |
|-------------|-------------------|-------------|
| **Number of Trading Pairs** | 40-80 USDT trading pairs | Such as BTC/USDT, ETH/USDT, etc., don't use BTC or ETH as quote currencies for trading pairs |
| **Maximum Open Trades** | 4-12 orders | max_open_trades recommended at 4-12 |
| **Position Mode** | Full margin mode | stake_amount: unlimited |
| **Timeframe** | 5m | Mandatory, cannot be changed |
| **Sell Signal** | use_exit_signal: true | Use strategy's custom sell signals |
| **Exit Profit Only** | exit_profit_only: false | Even if not profitable, sell if sell signal appears, for timely stop-loss |
| **Ignore ROI** | ignore_roi_if_entry_signal: true | If sell signal appears, ignore preset ROI take-profit table |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Extremely High Learning Curve

This strategy is nearly impossible to fine-tune by just tweaking a few parameters. Without Python basics, it's very difficult to understand its complex logic nesting.

### 10.2 Hardware Requirements

With 40-80 trading pairs calculating multiple indicators, VPS memory demands are high. Official recommendation is at least **4GB RAM**, otherwise may cause lag from calculation timeouts.

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------------|-------------|-----------------|
| 20-40 pairs | 2GB | 4GB |
| 40-80 pairs | 4GB | 8GB |
| 80+ pairs | 8GB | 16GB |

### 10.3 Backtesting vs. Live Trading Differences

NFI includes dynamic position adjustment and Hold Support features, which are difficult to fully simulate in regular backtesting. It is recommended to run in Dry-Run mode for 1-3 months first, observe live performance, then consider investing real money.

### 10.4 Manual Trader Advice

For manual traders, NFI is suitable when **the broader market is above MA20 and MAs are in bullish alignment**; for fully automated operation, it is recommended to enable **Bitcoin trend filtering**, which helps automatically "lie flat" for defense when the broader market turns bearish.

---

## XI. Summary

**Nostalgia** is a meticulously designed multi-strategy fusion system. Its core value lies in:

1. **Modular Design**: 31 entry conditions are like 31 independent strategies, flexibly combinable based on market state
2. **Risk Priority**: Multi-layer protection mechanisms ensure capital safety in extreme market conditions
3. **Classic Heritage**: Integrates decades of verified effective technical analysis indicators
4. **Modern Adaptation**: Compatible with Freqtrade v3 interface, deployable directly

For quantitative traders, this is a strategy template worth deep research. Recommendations:
- Backtest-verify with fewer conditions first
- Adjust protection parameters based on target trading pair characteristics
- Follow 1h timeframe trend confirmation signals
- Regularly evaluate each entry condition's contribution, optimize combinations
