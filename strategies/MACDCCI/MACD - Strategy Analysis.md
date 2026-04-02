# MACD Strategy Analysis

> **Strategy Number**: #189 (189th of 465 strategies)  
> **Strategy Type**: Trend Following / Momentum Indicator  
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**MACD** is one of the most classic strategies in quantitative trading, based on the Moving Average Convergence Divergence indicator created by Gerald Appel. MACD uses the difference between short-term and long-term exponential moving averages to judge trend direction and momentum changes.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Condition** | MACD > MACD Signal + CCI < threshold |
| **Exit Condition** | MACD < MACD Signal + CCI > threshold |
| **Protection** | Hard stop-loss |
| **Timeframe** | 5 Minutes |
| **Dependencies** | TA-Lib |
| **Optimizable** | CCI parameters support hyperopt optimization |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
minimal_roi = {
    "60":  0.01,   # After 60 minutes: 1% exit
    "30":  0.03,   # After 30 minutes: 3% exit
    "20":  0.04,   # After 20 minutes: 4% exit
    "0":   0.05    # Immediate: 5% exit
}

stoploss = -0.30  # -30% hard stop-loss
```

**Design Philosophy**:
- Uses time-decaying ROI: the longer you hold, the lower the profit requirement
- Paired with a wide stop-loss (-30%) to give trends room to breathe

### 2.2 Optimizable Parameters

```python
# Entry parameters (hyperopt-able)
buy_cci = IntParameter(low=-700, high=0, default=-50, space='buy', optimize=True)

# Exit parameters (hyperopt-able)
sell_cci = IntParameter(low=0, high=700, default=100, space='sell', optimize=True)

# Optimized default parameters
buy_params = {"buy_cci": -48}
sell_params = {"sell_cci": 687}
```

---

## III. Entry Conditions Details

### 3.1 Core Entry Logic

```python
# Entry Condition
(
    (dataframe['macd'] > dataframe['macdsignal']) &  # MACD golden cross
    (dataframe['cci'] <= self.buy_cci.value) &       # CCI oversold
    (dataframe['volume'] > 0)                        # Has volume
)
```

**Signal Interpretation**:
1. **MACD > Signal**: Fast line above slow line, trend is bullish
2. **CCI <= buy_cci**: CCI is in oversold territory (default -48)
3. **volume > 0**: Ensures it's not zero-volume

### 3.2 CCI Parameter Meaning

| Parameter Value | Meaning | Typical Range |
|-----------------|---------|---------------|
| 0 ~ -100 | Oversold zone | Default -48 |
| -100 ~ 100 | Neutral zone | |
| 100+ | Overbought zone | |

---

## IV. Exit Conditions Details

### 4.1 Core Exit Logic

```python
# Exit Condition
(
    (dataframe['macd'] < dataframe['macdsignal']) &  # MACD death cross
    (dataframe['cci'] >= self.sell_cci.value) &     # CCI overbought
    (dataframe['volume'] > 0)                        # Has volume
)
```

**Signal Interpretation**:
1. **MACD < Signal**: Fast line below slow line, trend is bearish
2. **CCI >= sell_cci**: CCI is in overbought territory (default 687)

---

## V. Technical Indicator System

### 5.1 MACD Indicator Details

| Indicator | Calculation Formula | Default Period |
|-----------|--------------------|----------------|
| **MACD Line** | EMA12 - EMA26 | 12, 26 |
| **Signal Line** | EMA9 of MACD | 9 |
| **Histogram** | MACD - Signal | - |

### 5.2 CCI Indicator Details

```
CCI = (Typical Price - SMA) / (0.015 × Mean Deviation)
```

| Zone | CCI Value | Signal Meaning |
|------|-----------|----------------|
| Oversold | < -100 | Potential bounce |
| Neutral | -100 ~ 100 | No clear signal |
| Overbought | > 100 | Potential pullback |

### 5.3 Indicator Combination Logic

```
Entry Signal = MACD golden cross + CCI oversold
Exit Signal = MACD death cross + CCI overbought
```

---

## VI. Risk Management

### 6.1 ROI Exit Strategy

| Time | Minimum Profit |
|------|---------------|
| 0 minutes | 5% |
| 20 minutes | 4% |
| 30 minutes | 3% |
| 60 minutes | 1% |

### 6.2 Stop-Loss Strategy

| Parameter | Value |
|-----------|-------|
| Hard Stop | -30% |
| Stop-Loss Type | Default market order |

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Classic & Reliable**: MACD is an indicator validated over decades
2. **Optimizable**: CCI parameters support hyperopt auto-optimization
3. **Dual Confirmation**: MACD trend + CCI momentum double confirmation
4. **Clear Logic**: Code is concise, easy to understand and modify

### ⚠️ Cons

1. **Lagging**: MACD itself is a lagging indicator
2. **Average Ranging Performance**: Many false signals in sideways markets
3. **Large Stop-Loss**: -30% stop is wide
4. **Parameter Sensitive**: CCI threshold needs adjustment per market

---

## VIII. Applicable Scenarios

| Market Environment | Performance | Description |
|-------------------|-------------|-------------|
| **Trending Up** | ⭐⭐⭐⭐⭐ | MACD golden cross + CCI oversold, perfect capture |
| **Trending Down** | ⭐⭐⭐⭐ | Same logic applied for shorting |
| **Ranging Upward** | ⭐⭐⭐ | Higher highs keep forming |
| **Sideways Ranging** | ⭐⭐ | Frequent crossovers increase false signals |

### 8.1 Timeframe Selection

| Timeframe | Characteristics | Best For |
|-----------|----------------|---------|
| 1m/5m | Frequent signals, high noise | Ultra-short term |
| 15m/1h | Balanced signal vs. stability | Medium-term |
| 4h/1d | Stable signals, high lag | Long-term trends |

---

## IX. Parameter Optimization

### 9.1 Default vs. Optimized Parameters

| Parameter | Default Value | Optimized |
|-----------|--------------|-----------|
| buy_cci | -50 | -48 |
| sell_cci | 100 | 687 |

### 9.2 Optimization Directions

| Parameter | Adjustment Suggestion |
|-----------|---------------------|
| buy_cci | -100 ~ 0 (more negative = stricter) |
| sell_cci | 0 ~ 700 (larger = stricter) |
| timeframe | Choose per trading style |
| stoploss | -0.20 ~ -0.40 |

---

## X. Live Trading Notes

### 10.1 CCI Parameter Anomaly

The optimized sell_cci = 687 looks extreme, but CCI's波动 range can be very wide:
- In extreme markets, CCI can easily exceed 500
- This means the exit condition becomes very "lenient"
- Actual selling relies mainly on MACD death cross

### 10.2 Difference from MACD_Cross

| Strategy | Entry Condition | Characteristics |
|----------|----------------|-----------------|
| **MACD** | MACD > Signal + CCI condition | Stricter conditions |
| **MACD_Cross** | MACD crosses above Signal | More lenient conditions |

---

## XI. Summary

**MACD** is a classic of quantitative trading, achieving dual verification of trend and momentum through the MACD and CCI combination.

Core value:
1. **Classic Pedigree**: MACD is one of the most widely used technical analysis indicators
2. **Optimizability**: Supports hyperopt parameter auto-optimization
3. **Dual Confirmation**: Trend (MACD) + Momentum (CCI)
4. **Clear Logic**: Code is concise, easy to understand and modify

Usage recommendations:
- Use optimized default parameters (buy_cci=-48, sell_cci=687)
- Suited for medium-to-short-term trading (5m-1h timeframe)
- Adjust stop-loss based on market volatility
- Best performance in clearly trending markets

---
