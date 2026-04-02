# NFI46Frog Strategy Analysis

> **Strategy ID**: #262 (262nd of 465 strategies)  
> **Strategy Type**: Multi-condition Trend Following + Multi-layer Protection Mechanisms  
> **Timeframe**: 5 Minutes (5m) + 1 Hour (1h) Informational Layer

---

## I. Strategy Overview

NFI46Frog is a member of the NostalgiaForInfinity (NFI) series strategies, developed by iterativ. Named after "Frog", it hints at the strategy's flexibility to hop around in market volatility. The strategy captures multiple entry opportunities through 17 independent buy conditions, paired with refined dip and pump protection mechanisms, aiming for steady profits in trending markets.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 17 independent buy signals, each independently enableable/disableable |
| **Exit Conditions** | 8 basic sell signals + 40+ dynamic take-profit signals |
| **Protection Mechanisms** | Dip Protection (12 parameters) + Pump Protection (27 parameters) |
| **Timeframe** | 5m primary + 1h informational |
| **Dependencies** | talib, finta, qtpylib, cachetools, skopt |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,    # Immediate: 10%
    "30": 0.05,   # After 30 minutes: 5%
    "60": 0.02,   # After 60 minutes: 2%
}

# Stop Loss
stoploss = -0.10   # Fixed stop loss: -10%

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01        # Activates after 1% positive return
trailing_stop_positive_offset = 0.03  # Trigger threshold 3%
```

**Design Philosophy**:
- ROI table is relatively loose, allowing the strategy to continue running in favorable trends
- 10% fixed stop loss provides a bottom-line guarantee
- Trailing stop locks in profits, starting to trail after 3% positive return

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'trailing_stop_loss': 'limit',
    'stoploss': 'limit',
    'stoploss_on_exchange': False
}
```

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms (Dual Insurance System)

Each entry condition is equipped with two core protection parameter sets:

#### 3.1.1 Dip Protection (Decline Protection)

Prevents "catching a falling knife" during sharp declines, with three strictness levels:

| Protection Type | Parameter Set | Default Thresholds | Description |
|---------------|---------------|--------------------|--------------|
| **Normal** | threshold 1-4 | 2%/14%/32%/50% | Standard decline protection |
| **Strict** | threshold 5-8 | 1.5%/6%/24%/40% | Strict decline protection |
| **Loose** | threshold 9-12 | 2.6%/24%/42%/80% | Loose decline protection |

Inspection dimensions: current candle, 2-period, 12-period, 144-period

#### 3.1.2 Pump Protection (Surges Protection)

Prevents chasing after price surges, with three time windows and three strictness levels:

| Time Window | Parameter Set | Purpose |
|------------|---------------|---------|
| **12 hours** | threshold 1, 4, 7 | Short-term surge check |
| **24 hours** | threshold 7, 8, 9 | Medium-term surge check |
| **36 hours** | threshold 2, 5, 8 | Medium-to-long-term surge check |
| **48 hours** | threshold 3, 6, 9 | Long-term surge check |

### 3.2 Typical Entry Condition Examples

#### Condition #1: Trend Pullback Entry
```python
# Logic
- 1h EMA50 > EMA200 (long-term trend up)
- SMA200 uptrend
- safe_dips protection activated
- safe_pump_48 protection activated
- 36-period minimum gain > 2.2%
- RSI_1h in 30-80 range
- RSI < 36, MFI < 26 (short-term oversold)
```

#### Condition #8: Alligator Indicator Breakout
```python
# Logic
- Price above 1h EMA200's 98.8%
- Alligator lips > teeth > jaw (bullish alignment)
- All three lines rising
- RSI < 46
```

### 3.3 Classification of 17 Entry Conditions

| Condition Group | Condition Numbers | Core Logic |
|----------------|------------------|------------|
| **Trend Pullback** | 1, 5, 14 | Trend confirmation + pullback entry |
| **Oversold Rebound** | 2, 4, 6, 7 | RSI/MFI oversold + Bollinger lower band |
| **BB Breakout** | 3 | BB40 lower band breakout + tail confirmation |
| **Alligator** | 8 | Alligator bullish alignment |
| **MA Deviation** | 9, 10, 11, 12 | SMA deviation + RSI confirmation |
| **EWO Signals** | 12, 13, 16, 17 | Elliott Wave Oscillator |
| **EMA Deviation** | 15 | EMA12/26 deviation + RSI |

---

## IV. Exit Conditions Details

### 4.1 Tiered Take-Profit System (12 Levels)

The strategy employs a refined tiered take-profit mechanism, deciding exits based on profit rate and RSI status:

```
Profit Range           RSI Threshold    Signal Name
─────────────────────────────────────────────────────
> 20%                  < 34            signal_profit_11
10%-20%                < 42            signal_profit_10
9%-10%                 < 50            signal_profit_9
8%-9%                  < 54            signal_profit_8
7%-8%                  < 54            signal_profit_7
6%-7%                  < 49            signal_profit_6
5%-6%                  < 44            signal_profit_5
4%-5%                  < 43            signal_profit_4
3%-4%                  < 42            signal_profit_3
2%-3%                  < 38            signal_profit_2
1%-2%                  < 34            signal_profit_1
< 1%                   < 33            signal_profit_0
```

**Core Philosophy**: Higher profit yields looser RSI thresholds, allowing more upside room.

### 4.2 Special Exit Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| **Below EMA200 Exit** | Price below EMA200 + profit/RSI conditions | signal_profit_u_* |
| **Post-Surge Exit** | 48h/36h/24h surge markers + profit conditions | signal_profit_p_* |
| **Trend Decay Exit** | SMA200 declining + profit range | signal_profit_d_* |
| **Trailing Exit** | Profit range + drawdown magnitude + RSI | signal_profit_t_* |

### 4.3 Basic Sell Signals (8)

```python
# Sell Signal 1: RSI + BB Overbought (6 consecutive candles)
- RSI > 79.5
- Close above BB upper band for 6 consecutive candles

# Sell Signal 2: RSI + BB Overbought (3 consecutive candles)
- RSI > 81
- Close above BB upper band for 3 consecutive candles

# Sell Signal 3: Pure RSI Overbought
- RSI > 82

# Sell Signal 4: Dual Timeframe RSI Overbought
- RSI_5m > 73.4
- RSI_1h > 79.6

# Sell Signal 6: Below EMA200 Rebound
- Price below EMA200 but above EMA50
- RSI > 79

# Sell Signal 7: 1h RSI + EMA Death Cross
- RSI_1h > 81.7
- EMA12 crosses below EMA26

# Sell Signal 8: BB Relative Position
- Close > 110% of 1h BB upper band
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Trend Indicators** | EMA (12, 15, 20, 26, 35, 50, 100, 200), SMA (5, 30, 200) | Trend direction identification |
| **Momentum Indicators** | RSI (14), Stochastic Fast, StochRSI | Overbought/oversold identification |
| **Volatility Indicators** | Bollinger Bands (20, 40), ATR (14) | Volatility and price channels |
| **Volume Indicators** | MFI, VFI, CMF | Price-volume relationship analysis |
| **Trend Strength** | DMI (+DI, -DI, ADX) | Trend direction and strength |
| **Special Indicators** | EWO, Alligator, Chopiness | Market structure analysis |
| **Custom Indicators** | RMI, SSL Channels, SROC | Advanced signal confirmation |

### 5.2 Informational Timeframe Indicators (1h)

The strategy uses 1 hour as the informational layer for higher-dimensional trend judgment:

- EMA series (12, 15, 20, 26, 35, 50, 100, 200)
- SMA200 and its directional judgment
- RSI (14)
- Bollinger Bands (20, 2std)
- Chaikin Money Flow (CMF)
- Pump detection markers (24h/36h/48h windows)

---

## VI. Risk Management Highlights

### 6.1 Dip Protection Mechanism

Inspects decline magnitude across four time dimensions:

```python
safe_dips = (
    (open - close) / close < threshold_1          # Current candle
    & (open.rolling(2).max() - close) / close < threshold_2   # 2-period
    & (open.rolling(12).max() - close) / close < threshold_3  # 12-period
    & (open.rolling(144).max() - close) / close < threshold_4 # 144-period
)
```

### 6.2 Pump Protection Mechanism

Prevents chasing after surges:

```python
safe_pump = (
    price_change_magnitude < threshold           # Surge not exceeding threshold
    OR
    pullback_magnitude > current_height         # Or sufficient pullback already
)
```

### 6.3 Heiken Ashi Confirmation

The strategy uses smoothed Heiken Ashi candlesticks for signal confirmation, reducing false signals.

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Multi-Dimensional Protection**: Dip + Pump dual protection mechanism avoids incorrect entries during extreme market conditions
2. **Highly Customizable**: 17 entry and 8 exit conditions, all independently switchable, supporting hyperparameter optimization
3. **Multi-Timeframe**: 5m + 1h dual timeframe, balancing short-term signals and long-term trends
4. **Refined Take-Profit**: 12-level dynamic take-profit system, intelligent exit based on market conditions

### ⚠️ Cons

1. **High Complexity**: 100+ optimizable parameters, high cost to understand and debug
2. **Overfitting Risk**: Many optimizable parameters may produce excellent backtesting but poor live performance
3. **High Computational Load**: 400 startup candles + multiple indicator calculations, hardware-demanding
4. **Requires Optimization**: Default parameters may not suit all markets, requiring targeted adjustments

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| **Stable Uptrend** | Enable all entry conditions | Strategy's original design intent, optimal performance |
| **Ranging Market** | Enable conditions 2, 6, 7 | Oversold rebound conditions more effective |
| **Downtrend** | Disable or use light positions | Strategy not designed for counter-trend trading |
| **High Volatility** | Enable Strict protection | Tighter entry conditions |

---

## IX. Applicable Market Environment Details

NFI46Frog is a member of the NostalgiaForInfinity series. Based on its code architecture and community long-term live-trading validation, it is best suited for **stable uptrend markets**, and underperforms during **one-sided declines or sharp oscillations**.

### 9.1 Core Strategy Logic

- **Trend Following**: Most entry conditions require EMA50 > EMA200 or SMA200 uptrend
- **Pullback Entry**: Seeking short-term oversold opportunities within trends
- **Protection First**: Dip and Pump protection ensures no entries during extreme market conditions

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| 📈 Stable Uptrend | ⭐⭐⭐⭐⭐ | Original design intent, trend confirmation + pullback entry perfectly matched |
| 🔄 Wide Ranging | ⭐⭐⭐☆☆ | Oversold rebound conditions effective, but may have frequent stop-losses |
| 📉 One-Sided Decline | ⭐⭐☆☆☆ | Trend conditions not met, most signals filtered out |
| ⚡ High Frequency Volatility | ⭐☆☆☆☆ | Protection mechanisms significantly reduce signal frequency |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|--------------|-------------------|-------------|
| Number of Pairs | 40-80 pairs | Community recommended range |
| Concurrent Positions | 4-6 | Risk diversification |
| Blacklist | Leveraged tokens | Avoid abnormal volatility |

---

## X. Summary

**NFI46Frog** is a highly engineered trend-following strategy. Its core value lies in:

1. **Comprehensive Protection**: Dip + Pump dual protection mechanism, safely entering within trends
2. **Flexible Configuration**: 17 entry conditions covering multiple market opportunities
3. **Refined Take-Profit**: 12-level dynamic take-profit system, intelligently locking in profits
4. **Community Validated**: NFI series has been long-term live-trading validated

For quantitative traders, recommendations include:
- First test in a simulated environment
- Adjust protection parameters based on target market
- Enable hyperparameter optimization to find optimal configuration
- Pay attention to trading pair selection and blacklist settings
