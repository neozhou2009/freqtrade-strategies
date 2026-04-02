# NostalgiaForInfinityV7 — Strategy Analysis

> **Strategy ID**: #304 (out of 465 strategies)  
> **Strategy Type**: Multi-Condition Trend Following + Multi-Layer Dynamic Profit-Taking System  
> **Timeframe**: 5 minutes (5m) + 1 hour Informative Layer  
> **Author**: iterativ

---

## I. Strategy Overview

NostalgiaForInfinityV7 is the seventh-generation evolution of the NostalgiaForInfinity series — a complex trend-following strategy based on multi-dimensional technical indicator combinations. Named "Infinite Nostalgia," it actually represents a quantitatively optimized trading system refined through long-term iteration, integrating trend identification, momentum confirmation, volatility analysis, and other multi-dimensional technical analysis methods.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 26 independent buy signals, each independently enableable/disableable |
| **Sell Conditions** | 8 base sell signals + 12-level dynamic profit-taking system |
| **Protection** | Each buy condition equipped with independent protection parameter groups |
| **Timeframe** | Main: 5m + Informative: 1h |
| **Dependencies** | qtpylib, talib, technical.indicators (zema) |
| **Startup Candles** | 400 candles |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,    # Immediate: 10% profit
    "30": 0.05,   # After 30 min: 5% profit
    "60": 0.02,   # After 60 min: 2% profit
}

# Stop Loss
stoploss = -0.10  # 10% fixed stop loss

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01      # 1% trailing distance
trailing_stop_positive_offset = 0.03  # Activates after 3% profit
```

**Design Rationale**:
- ROI uses progressive profit targets, lowering expectations as holding time increases
- 10% stop is a hard risk control bottom line
- Trailing stop activates after 3% profit, ensuring profit maximization in trending markets

### 2.2 Order Type Configuration

All orders are limit orders, ensuring precise fill price control and avoiding slippage.

### 2.3 Key Configuration Recommendations

- Concurrent positions: 4–6
- Trading pairs: 40–80, volume-sorted
- Stable coin pairs (USDT, BUSD, etc.)
- Blacklist: *BULL, *BEAR, *UP, *DOWN (leveraged tokens)
- Timeframe: Must be 5 minutes

---

## III. Buy Conditions Details

### 3.1 Protection Mechanisms (26 Groups)

Each buy condition has an independent protection parameter group, building a "condition + protection" dual filtering system:

| Protection Type | Description | Default Example |
|----------------|-------------|-----------------|
| EMA Fast/Slow | Fast MA above slow MA | ema_26 > ema_200 |
| Close Position | Close above EMA | close > ema_200 |
| SMA200 Rising | SMA200 in rising state | sma_200 > sma_200.shift(28) |
| SMA200_1h Rising | 1h SMA200 in rising state | sma_200_1h > sma_200_1h.shift(50) |
| Safe Dips | Price drop within safe range | safe_dips_80 |
| Safe Pump | Price pullback after pump | safe_pump_24_70 |

### 3.2 Key Buy Conditions

**Condition #1** (Trend Confirmation Entry):
```python
# Protections
- ema_100 > ema_200
- sma_200 > sma_200.shift(28) (SMA200 in uptrend)
- safe_dips_80
- safe_pump_24_70_1h

# Core Logic
- 36-period min rise > 2.2%
- 1h RSI in 30–84 range
- 5m RSI < 36
- MFI < 36
```

**Condition #2** (Bollinger Lower Band Rebound):
```python
# Protections
- ema_20_1h > ema_200_1h
- safe_dips_50
- safe_pump_24_10_1h

# Core Logic
- RSI < RSI_1h - 39 (short-term oversold)
- MFI < 49
- close < bb20_2_low * 0.983
```

**Condition #3** (BB40 Volatility Breakout):
```python
# Protections
- ema_100 > ema_200
- ema_100_1h > ema_200_1h
- safe_pump_36_100_1h
- close > ema_200_1h * 0.986

# Core Logic
- bb40_2_delta > close * 0.059 (BB width sufficient)
- closedelta > close * 0.023 (significant price change)
- tail < bb40_2_delta * 0.418 (wick control)
- close < bb40_2_low.shift() (breaks lower band)
```

**Condition #8** (Volume Price Reversal):
```python
# Protections
- ema_12_1h > ema_200_1h
- close > ema_200
- safe_pump_24_120_1h

# Core Logic
- RSI < 29 (severely oversold)
- volume > volume.shift(1) * 2 (volume expansion)
- close > open (bullish candle)
- (close - low) > (close - open) * 3.5 (long lower wick)
```

### 3.3 26 Buy Conditions Classification

| Condition Group | Condition IDs | Core Logic |
|----------------|--------------|------------|
| Trend Following | 1, 4, 5, 18 | Trend entry, comprehensive protection |
| Oversold Rebound | 2, 3, 6, 7 | BB lower band / RSI oversold |
| EWO Momentum | 12, 13, 16, 17 | Elliott Wave Oscillator |
| MA Cross | 19, 24 | EMA cross / CMF combination |
| Extreme Bottom | 20, 21 | RSI extreme low values |
| Multi-Factor Verification | 9, 10, 11, 14, 15 | Multi-indicator resonance |
| Volume-Price Confirmation | 8, 22 | Volume confirmation |
| Simple Trigger | 23, 26 | Simplified conditions |

---

## IV. Sell Logic Details

### 4.1 Multi-Level Profit-Taking System

The strategy uses a graded profit-taking mechanism that dynamically decides exit timing based on current profit rate and RSI:

| Profit Range | RSI Threshold | Signal Name |
|-------------|--------------|-------------|
| > 20% | < 34 | signal_profit_11 |
| 10%–20% | < 42 | signal_profit_10 |
| 9%–10% | < 54 | signal_profit_9 |
| 8%–9% | < 48 | signal_profit_8 |
| 7%–8% | < 54 | signal_profit_7 |
| 6%–7% | < 45 | signal_profit_6 |
| 5%–6% | < 43 | signal_profit_5 |
| 4%–5% | < 37 | signal_profit_4 |
| 3%–4% | < 35 | signal_profit_3 |
| 2%–3% | < 35 | signal_profit_2 |
| 1%–2% | < 34 | signal_profit_1 |
| 0%–1% | < 34 | signal_profit_0 |

**Design Philosophy**: Higher profit → looser RSI threshold, ensuring profit-taking efficiency while avoiding premature exit.

### 4.2 Below EMA200 Special Profit-Taking

When price falls below EMA200, the strategy uses a more aggressive profit-taking system:

| Profit Range | RSI Threshold | Signal Name |
|-------------|--------------|-------------|
| > 20% | < 34 | signal_profit_u_11 |
| 12%–20% | < 42 | signal_profit_u_10 |
| 10%–12% | < 54 | signal_profit_u_9 |
| 9%–10% | < 55 | signal_profit_u_8 |
| 8%–9% | < 54 | signal_profit_u_7 |
| 7%–8% | < 56 | signal_profit_u_6 |
| 6%–7% | < 60 | signal_profit_u_5 |
| 5%–6% | < 59 | signal_profit_u_4 |
| 4%–5% | < 58 | signal_profit_u_3 |
| 3%–4% | < 57 | signal_profit_u_2 |
| 2%–3% | < 56 | signal_profit_u_1 |
| 1%–2% | < 35 | signal_profit_u_0 |

### 4.3 Special Sell After Pump

For pumps of different durations (24h/36h/48h), the strategy has dedicated profit-taking logic:

| Duration | Pump Threshold | Signal Series |
|---------|----------------|---------------|
| 48h | > 90% | signal_profit_p_1_* |
| 36h | > 72% | signal_profit_p_2_* |
| 24h | > 68% | signal_profit_p_3_* |

### 4.4 Trailing Stop Exit

```python
# Trailing Stop Configuration
- Profit range: 16%–60%
- Drawdown threshold: 3%
- RSI range: 20–50
```

Triggers when profit is above 16% and drawdown exceeds 3%, protecting profits in trending markets.

### 4.5 Base Sell Signals (8)

```python
# Sell Signal 1: RSI Overbought + BB Upper Break
- RSI > 79.5
- 5 consecutive candles close above BB upper

# Sell Signal 2: Extreme RSI Overbought
- RSI > 81
- 2 consecutive candles close above BB upper

# Sell Signal 3: Pure RSI Overbought
- RSI > 82

# Sell Signal 4: Dual Timeframe RSI Overbought
- RSI > 73.4 AND RSI_1h > 79.6

# Sell Signal 6: RSI Overbought Below EMA200
- close < ema_200
- close > ema_50
- RSI > 79

# Sell Signal 7: 1h RSI Overbought + EMA Death Cross
- RSI_1h > 81.7
- EMA12 crosses below EMA26

# Sell Signal 8: BB Upper Break
- close > bb20_2_upp_1h * 1.1
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|--------------------|---------|
| **MA System** | EMA 12/15/20/26/35/50/100/200 | Trend judgment, support/resistance |
| **MA System** | SMA 5/30/200 | Trend confirmation, entry signals |
| **Momentum** | RSI 14 | Overbought/oversold, momentum confirmation |
| **Volatility** | BB 20/40 | Volatility channel, breakout signals |
| **Volume** | MFI | Volume-price confirmation |
| **Special** | EWO (50/200) | Elliott Wave Oscillator |
| **Special** | CMF 20 | Fund flow direction |
| **Special** | Choppiness 14 | Market trend/chop judgment |
| **Special** | ZEMA 61 | Zero-lag MA |

### 5.2 Informative Timeframe Indicators (1h)

- EMA system (12/15/20/26/35/50/100/200)
- SMA200 and trend direction
- RSI momentum
- Bollinger Bands (20-period)
- CMF fund flow
- Pump detection (24h/36h/48h)
- Safe pump checks (safe_pump_*)

---

## VI. Risk Management Features

### 6.1 Multi-Layer Protection Parameters

Each buy condition is equipped with independent protection parameter combinations, forming "condition + protection" dual filtering:

| Protection Layer | Protection Type | Risk Avoidance |
|-----------------|-----------------|----------------|
| Layer 1 | EMA Trend | Avoid counter-trend trading |
| Layer 2 | SMA200 Direction | Avoid bottom-fishing in downtrends |
| Layer 3 | Safe Dips | Avoid chasing highs |
| Layer 4 | Safe Pump | Avoid buying after surges |
| Layer 5 | Close Position | Ensure price is in reasonable range |

### 6.2 Graded Profit-Taking

12-level profit thresholds combined with RSI conditions for dynamic profit-taking:
- Low profit: Strict RSI threshold, fast exit
- High profit: Looser RSI threshold, let profits run

### 6.3 Special Scenario Risk Control

| Scenario | Handling |
|---------|----------|
| Buy after pump | Check pullback magnitude, avoid chasing |
| Below EMA200 | Lower profit thresholds, faster exit |
| Long-holding loss | Exit on RSI rebound |
| Drop after pump | Special trailing stop to protect profits |

---

## VII. Strategy Pros & Cons

### ✅ Advantages

1. **Rich Conditions**: 26 buy conditions cover multiple market forms, reducing single-signal failure risk
2. **Comprehensive Protection**: Each condition has independent protection parameters, multi-layer risk filtering
3. **Dynamic Profit-Taking**: 12-level profit thresholds with RSI for intelligent profit-taking
4. **Multi-Timeframe**: 5-minute + 1-hour dual confirmation, improving signal quality
5. **Special Scenario Handling**: Dedicated responses for pump, EMA200 breach, and other scenarios

### ⚠️ Limitations

1. **High Parameter Complexity**: Hundreds of tunable parameters, difficult optimization
2. **Overfitting Risk**: Many conditions may cause excessive fitting to historical data
3. **High Computation Load**: Requires 400 candles startup, high hardware requirements
4. **Steep Learning Curve**: Understanding all logic requires significant time
5. **High Maintenance Cost**: Parameter tuning and market adaptation require ongoing attention

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|------------------------|-------|
| Clear uptrend | Enable conditions 1, 4, 5, 18 | Trend conditions perform best |
| Choppy market | Enable conditions 2, 3, 6, 7 | BB rebound strategy effective |
| High volatility | Enable conditions 8, 22 | Volume-price reversal captures opportunities |
| Downtrend | Disable some aggressive conditions | Cautious entry or stand aside |

---

## IX. Summary

**NostalgiaForInfinityV7** is a comprehensive complex quantitative trading strategy. Its core value lies in:

1. **Condition Richness**: 26 buy conditions cover multiple market forms
2. **Protection Multi-Layering**: Each condition has independent protection, constructing "31-layer fuse" style risk control
3. **Intelligent Profit-Taking**: 12-level dynamic profit-taking system balances efficiency and profit
4. **Framework Maturity**: 7 generations of iteration, relatively complete logic design

For quantitative traders, NostalgiaForInfinityV7 is a case study worth in-depth research. It demonstrates how to build a complete trading system through condition combinations, protection mechanisms, and dynamic profit-taking. But be vigilant about overfitting risks and maintenance costs from its complexity.

**Recommendations**:
- Beginners: Start by understanding core logic, start with small-scale trading
- Intermediate: Adjust enabled conditions and protection parameters based on backtest results
- Professionals: Consider developing simplified versions based on this framework
