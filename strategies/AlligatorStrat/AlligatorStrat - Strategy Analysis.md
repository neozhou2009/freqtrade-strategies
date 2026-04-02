# AlligatorStrat Strategy In-Depth Analysis

> **Strategy ID**: #417 (417th of 465 strategies)  
> **Strategy Type**: SMA Trend Crossover + MACD Confirmation  
> **Timeframe**: 4 Hours (4h)

---

## I. Strategy Overview

AlligatorStrat is a trend-following strategy based on Simple Moving Average (SMA) crossovers and MACD indicator confirmation. Developed by Gert Wohlgemuth, the core concept is to capture short-term trend breakout opportunities using multi-period SMA crossovers as the primary entry signal, with MACD serving as the trend confirmation indicator.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signals (SMA crossover + MACD crossover), can trigger independently |
| **Sell Conditions** | 2 base sell signals + ROI take-profit |
| **Protection Mechanism** | Fixed stop-loss at -20% |
| **Timeframe** | 4 hours (longer timeframe, suitable for trend following) |
| **Dependencies** | talib, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.1  # 10% profit target
}

# Stop-loss setting
stoploss = -0.2  # 20% fixed stop-loss
```

**Design Rationale**:
- Single 10% profit target, pursuing moderate returns rather than greed
- 20% stop-loss is relatively wide, allowing for price fluctuations during trend formation
- 4-hour timeframe means fewer stop-loss triggers, suitable for medium-term positions

### 2.2 Order Type Configuration

The strategy uses default order type configuration without special specifications.

---

## III. Buy Conditions Detailed

### 3.1 Technical Indicator System

The strategy uses the following technical indicators:

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | SMA(5), SMA(8), SMA(13) | Determine short, medium, and long-term trends |
| Momentum Indicators | MACD, MACD Signal, MACD Histogram | Confirm trend direction and momentum |

### 3.2 Buy Conditions Explained

#### Condition #1: SMA Crossover + MACD Confirmation

```python
# Logic
- SMA(5) crosses above SMA(8) (short-term MA crosses above medium-term MA)
- MACD value > -0.00001 (MACD slightly above zero line)
- MACD > MACD Signal (MACD line above signal line)
```

**Interpretation**:
- This is the primary buy signal, requiring both conditions to be met simultaneously
- SMA crossover captures short-term momentum changes
- MACD confirms trend direction, avoiding false breakouts

#### Condition #2: MACD Crossover

```python
# Logic
- MACD crosses above MACD Signal (MACD golden cross)
```

**Interpretation**:
- Independent buy signal, can trigger alone
- Simple MACD golden cross strategy
- Serves as a supplementary signal to SMA crossover

### 3.3 Buy Conditions Summary Table

| Condition ID | Core Logic | Complexity |
|-------------|-----------|------------|
| #1 | SMA(5) crosses above SMA(8) + MACD confirmation | Medium |
| #2 | MACD golden cross | Simple |

---

## IV. Sell Logic Detailed

### 4.1 Sell Conditions

#### Signal #1: Trend Reversal Signal

```python
# Logic
- Close price < SMA(8) (price breaks below medium-term MA)
- MACD < MACD Signal (MACD below signal line)
```

**Interpretation**:
- Price breaking below medium-term MA suggests short-term trend weakness
- MACD confirms momentum decay
- Both conditions must be met simultaneously

#### Signal #2: MACD Death Cross

```python
# Logic
- MACD crosses below MACD Signal (MACD death cross)
```

**Interpretation**:
- Independent sell signal
- Simple MACD death cross strategy
- Serves as early warning for trend reversal

### 4.2 Sell Signals Summary Table

| Signal ID | Core Logic | Priority |
|-----------|-----------|----------|
| #1 | Price breaks below SMA(8) + MACD confirmation | Primary signal |
| #2 | MACD death cross | Auxiliary signal |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | SMA(5, 8, 13) | Determine trend direction and crossover signals |
| Momentum Indicators | MACD(12, 26, 9) | Confirm trend and momentum changes |

### 5.2 Indicator Calculation Notes

**SMA (Simple Moving Average)**:
- SMA(5): 5-period simple moving average, representing ultra-short-term trend
- SMA(8): 8-period simple moving average, representing short-term trend
- SMA(13): 13-period simple moving average, representing medium-term trend (calculated but not used for trading signals)

**MACD (Moving Average Convergence Divergence)**:
- Uses talib default parameters (12, 26, 9)
- MACD Line: 12-period EMA - 26-period EMA
- Signal Line: 9-period EMA of MACD
- Histogram: MACD - Signal

---

## VI. Risk Management Features

### 6.1 Fixed Stop-Loss Mechanism

The strategy employs a fixed 20% stop-loss:

```python
stoploss = -0.2  # 20% stop-loss
```

**Design Rationale**:
- Wide stop-loss range, adapted for 4-hour timeframe
- Allows for normal price fluctuations during trend formation
- Avoids being stopped out by short-term noise

### 6.2 ROI Target

Single 10% profit target:

```python
minimal_roi = {"0": 0.1}
```

**Design Rationale**:
- Moderate profit target
- Not pursuing extreme returns
- Combined with 4-hour timeframe, suitable for swing trading

### 6.3 Timeframe Advantage

- 4-hour cycle reduces market noise
- Lower trading frequency, reducing fees and slippage costs
- Suitable for trend-following strategies

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Simple and Intuitive**: Clear strategy logic using only SMA and MACD, two classic indicators
2. **Dual Confirmation**: Buy signals require SMA crossover + MACD confirmation, reducing false signals
3. **4-Hour Cycle**: Reduces market noise, suitable for trend following
4. **Independent Signals**: MACD golden cross can serve as an independent signal, increasing trading opportunities

### ⚠️ Limitations

1. **Lack of Trailing Stop**: Fixed stop-loss may miss opportunities for trend continuation
2. **Single ROI Target**: No staged take-profit, potentially missing larger profits
3. **Few Indicators**: Relying only on SMA and MACD may perform poorly in high volatility or ranging markets
4. **Author's Note**: Author explicitly states "doesn't really perform that well and it's just a proof of concept"

---

## VIII. Applicable Scenarios Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| Clear Trend | Standard configuration | SMA crossovers perform well in trending markets |
| Ranging Market | Use cautiously | SMA crossovers easily generate false signals |
| High Volatility | Reduce position size | Wide stop-loss may lead to larger losses |
| Low Volatility | Standard configuration | Suitable for stable trend markets |

---

## IX. Applicable Market Environment Details

AlligatorStrat is a **proof-of-concept trend-following strategy**. Based on its code architecture and author's notes, it performs best in **clear trending markets**, while performing poorly in **ranging and high-volatility markets**.

### 9.1 Strategy Core Logic

- **Trend Following**: Using SMA crossovers to capture trend direction
- **Momentum Confirmation**: MACD as auxiliary judgment for trend strength
- **Wide Stop-Loss**: 20% stop-loss gives trends enough room to develop

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:-----------|:------------------|:----------------|
| 📈 Clear Trend | ⭐⭐⭐⭐☆ | SMA crossovers effectively capture trend initiation |
| 🔄 Ranging Market | ⭐⭐☆☆☆ | Frequent crossovers lead to false signals and consecutive losses |
| 📉 Downtrend | ⭐☆☆☆☆ | Trend-following strategies not suitable for declining markets |
| ⚡️ High Volatility | ⭐⭐☆☆☆ | Wide stop-loss may lead to significant losses |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|------------------|-------|
| Timeframe | 4h (default) | Not recommended to modify |
| Stop-Loss | -0.15 ~ -0.25 | Can adjust based on risk preference |
| Minimal ROI | 0.08 ~ 0.12 | Can moderately adjust |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

Strategy logic is simple, suitable for beginners to learn and understand basic concepts of trend following.

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 1GB | 2GB |
| 10-50 pairs | 2GB | 4GB |

### 10.3 Backtesting vs Live Trading Differences

Due to the strategy's simplicity, differences between backtesting and live trading may be small, but still note:
- Slippage impact
- Liquidity issues
- Fee costs

### 10.4 Manual Trader Recommendations

Strategy logic is clear and can be executed manually:
1. Observe 4-hour chart
2. Wait for SMA(5) to cross above SMA(8)
3. Confirm MACD is above zero line and above signal line
4. Enter position and set 20% stop-loss and 10% take-profit

---

## XI. Summary

**AlligatorStrat** is a **proof-of-concept trend-following strategy**. Its core value lies in:

1. **Educational Value**: Demonstrates how to build a trend-following strategy combining SMA and MACD
2. **Simple Design**: Clear logic, easy to understand and modify
3. **Dual Confirmation**: SMA crossover + MACD confirmation reduces false signals

For quantitative traders, this strategy is more suitable as a learning template rather than for direct live trading. The author explicitly states this is a proof-of-concept strategy, and actual performance may not meet expectations. It's recommended to add more filter conditions, optimize take-profit and stop-loss logic, or combine with other indicators for improvement.

---

*Strategy Author: Gert Wohlgemuth*