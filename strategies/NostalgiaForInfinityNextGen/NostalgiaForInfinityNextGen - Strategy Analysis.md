# NostalgiaForInfinityNextGen Strategy Analysis

> **Strategy ID**: #287 (287th of 465 strategies)  
> **Strategy Type**: NFI Series - Multi-Condition Trend Following + Next-Gen Optimization  
> **Timeframe**: 15 Minutes (15m) + 1 Hour (1h)

---

## I. Strategy Overview

**NostalgiaForInfinityNextGen** (abbreviated NFI NextGen) is the "next generation" evolution of NostalgiaForInfinity (NFI). As a further optimized version of NFI Next, NextGen comprehensively adapts and streamlines the strategy based on the original's core multi-condition architecture for medium-period trading.

The "NextGen" naming signifies "next generation," reflecting the strategy author's continuous optimization of the Next version and specialized adaptation for medium-period trading characteristics. Compared to the Next version, NextGen adopts a 15-minute timeframe with more refined entry conditions, better suited for medium-term trend following.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 21 independent buy signals, each condition can be independently enabled/disabled |
| **Exit Conditions** | 6 base sell signals + multi-layer dynamic take-profit logic |
| **Protection Mechanisms** | 21 sets of buy protection parameters (EMA/SMA/safe dip/safe pump/BTC trend) |
| **Timeframe** | 15-minute primary timeframe + 1-hour informational timeframe |
| **Dependencies** | pandas, numpy, TA-Lib, technical, qtpylib, pandas_ta |

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
- Initial ROI at 10%, pursuing relatively high profit targets
- The 15-minute timeframe allows relatively longer holding periods, suitable for capturing medium-short-term trends
- Pairs with **trailing stop** to lock in profits, suitable for trending markets
- Hard stop-loss at -10% controls maximum loss per trade

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms (21 Sets)

Each entry condition has an independent protection parameter set:

| Protection Type | Parameter Description | Options |
|-----------------|----------------------|---------|
| **Fast EMA** | Whether fast EMA is enabled and its length | 26/50/100/200 |
| **Slow EMA** | Whether slow EMA is enabled and its length | 26/50/100/200 |
| **Close Price Protection** | Whether close price is above EMA | 12/20/26/50/100/200 |
| **SMA200 Rising** | Whether SMA200 is in an uptrend | 20/30/36/44/50 period verification |
| **SMA200 1h Rising** | 1h period SMA200 trend confirmation | 20/30/36/44/50 |
| **Safe Dip** | Dip magnitude threshold protection | 10/50/80/100/130 etc. |
| **Safe Pump** | Pump magnitude threshold protection | 10/20/30/50/70/100/120 etc. |
| **Safe Pump Period** | Detection period | 24h/36h/48h |
| **BTC Trend** | Whether BTC 1h is not in a downtrend | True/False |

### 3.2 Typical Entry Condition Examples

#### Condition #1: EMA Trend Confirmation + Protection
```python
# Default protection configuration
- Slow EMA enabled: EMA100
- SMA200 rising verification: 36 periods
- Safe dip: level 80
- Safe pump: level 70, 24h period
```

#### Condition #3: Dual EMA Confirmation
```python
# Protection configuration
- Fast EMA enabled: EMA100
- Slow EMA enabled: EMA100
- Safe dip: level 80
- Safe pump: level 100, 36h period
```

#### Condition #5: EMA Golden Cross Detection
```python
# Protection configuration
- Fast EMA enabled: EMA100
- Slow EMA enabled: EMA26
- No dip/pump protection (more aggressive entry)
```

### 3.3 21 Entry Conditions Classification

| Condition Group | Condition Numbers | Core Logic |
|-----------------|-------------------|------------|
| **Strict Protection Group** | 1-3 | Multi-protection + trend confirmation |
| **Trend Following Group** | 4-7 | EMA trend + momentum confirmation |
| **Relaxed Entry Group** | 8-12 | Fewer protection conditions |
| **1h Confirmation Group** | 13-15 | High-period trend verification |
| **Aggressive Entry Group** | 16-18 | Fast signal response |
| **BTC Correlation Group** | 19-20 | BTC trend filtering |
| **Special Conditions Group** | 21 | Specific market environment signals |

---

## IV. Exit Logic Details

### 4.1 Multi-Layer Take-Profit System

```
Profit Range          Threshold        Exit Strategy
───────────────────────────────────────────────────────
> 10%              Immediate        ROI initial exit
5%-10%             30 minutes       ROI secondary exit
2%-5%              60 minutes       ROI tertiary exit
< 2%               Hold             Wait for signal or stop-loss
```

### 4.2 Special Exit Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| **BB Upper Band Breakout** | Continuous upper band breakout | Overbought exit |
| **RSI Extreme** | RSI overbought threshold | Momentum exit |
| **Below EMA** | Price breaks below EMA200 | Trend exit |
| **Trailing Stop** | Profit drawdown triggers | Protection exit |

### 4.3 Base Sell Signals (6 Total)

```python
# Sell Signal 1: Continuous BB upper band breakout
- RSI > 79.5
- Close price > BB20 upper band (3 consecutive candles)

# Sell Signal 2: Short-term overbought
- RSI > 81
- Close price > BB20 upper band (2 consecutive candles)

# Sell Signals 3-6: Other technical signals
- Dual RSI overbought
- EMA death cross
- High-period trend reversal
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Trend Indicators** | EMA(26,50,100,200) | Trend judgment, protection mechanisms |
| **Momentum Indicators** | RSI(4,14,20), MFI, EWO | Overbought/oversold, momentum strength |
| **Volatility Indicators** | Bollinger Bands(20,2) | Price boundaries, breakout signals |
| **Money Flow** | CMF, OBV | Capital inflow/outflow |
| **Special Indicators** | Zema, VIDYA, Hull | Smoothed trends, lag reduction |

---

## VI. Risk Management Features

### 6.1 Multi-Level Dip Protection (Safe Dips)

Dip threshold protection from levels 10 to 130:

```
Level    Protection Strength    Applicable Scenario
─────────────────────────────────────────────────────
10       Relaxed                Strong trending market
50       Medium                General market
80       Relatively Strict      Volatile market
100      Strict                High-risk environment
130      Extremely Strict       Extreme market
```

### 6.2 BTC Trend Filtering

Some entry conditions require BTC 1h not in a downtrend:
- Prevents buying altcoins when BTC is crashing
- Reduces systemic risk
- Conditions 19-20 have this protection enabled by default

---

## VII. Strategy Pros & Cons

### Advantages

1. **Refined Conditions**: 21 entry conditions covering main market environments, more focused than Next version
2. **Period Adaptation**: 15-minute timeframe better suited for medium-short-term trend following
3. **Complete Protection**: 21 sets of protection parameters, refined risk management
4. **Multi-Period Verification**: 15m execution + 1h trend confirmation
5. **Flexible Configuration**: Each condition can be independently enabled/disabled
6. **Computational Efficiency**: Refined conditions mean higher computational efficiency

### Limitations

1. **Lower Signal Frequency**: Signal frequency relatively lower on 15-minute timeframe
2. **Slower Reaction**: Slightly slower reaction than 5-minute version
3. **Depends on Historical Data**: Requires sufficient 1h and 15m historical data
4. **Learning Curve**: Understanding all conditions still requires time

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| **Trending Upward** | Enable all conditions | Trend filtering opens more entry opportunities |
| **Ranging Market** | Enable protection groups 1-6 | Strict protection filters false signals |
| **High Volatility** | Enable BTC filtering conditions | Prevent systemic risk |
| **Low Volatility** | Relax protection thresholds | Increase trading opportunities |

---

## IX. Applicable Market Environment Details

NostalgiaForInfinityNextGen is the next-gen optimized version of the NFI series. Based on its code architecture and community long-term live-trading experience, it is best suited for **medium-long-term trends with clear direction** and has limited performance during one-sided selloffs or extreme sideways consolidation.

### 9.1 Strategy Core Logic

- **Refined Entry Conditions**: 21 different entry conditions, optimized for 15-minute timeframe
- **Strict Risk Filtering**: Real-time detection of "24h/36h/48h rises" prevents chasing
- **Multi-Period Confirmation**: 15m execution + 1h trend confirmation, double insurance
- **BTC Trend Correlation**: Via "BTC 1h trend detection" reduces systemic risk

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:---|:---|:---|
| Slow Bull/Ranging Upward | StarsStarsStarsStarsStars | 15m period catches trend pullbacks, steady accumulation |
| Wide Ranging | StarsStarsStarsStars | Protection filters false breakouts, reduces stop-losses |
| One-Sided Selloff | StarsStarsStars | BTC trend filtering helps avoid systemic risk |
| Extreme Sideways | StarsStars | Few signal triggers, low capital utilization |

---

## X. Summary

**NostalgiaForInfinityNextGen** is the next-gen optimized version of the NFI series. Its core value lies in:

1. **Refined Conditions**: 21 entry conditions, further optimized on the Next version
2. **Period Adaptation**: 15-minute timeframe better suited for medium-short-term trend following
3. **Complete Protection**: 21 sets of protection parameters, refined risk management
4. **Efficiency Improvement**: Higher computational efficiency, lower resource usage

For quantitative traders, this is a strategy that balances complexity and efficiency. Recommendations:
- Backtest-verify with fewer conditions first
- Adjust protection parameters based on target trading pair characteristics
- Follow 1h timeframe trend confirmation signals
- Enjoy fewer signals but higher quality
