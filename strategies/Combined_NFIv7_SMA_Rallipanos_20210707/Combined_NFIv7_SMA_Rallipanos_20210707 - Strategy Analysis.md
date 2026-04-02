# Combined_NFIv7_SMA_Rallipanos_20210707 Strategy Analysis

> **Strategy Number**: #129 (9th in Batch 13)
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Rebound + Dynamic Take-Profit
> **Timeframe**: 5 Minutes (5m) + 1 Hour (1h) Dual Timeframe

---

## I. Strategy Overview

**Combined_NFIv7_SMA_Rallipanos_20210707** is a variant of the NostalgiaForInfinityV7 series created by Freqtrade community developer **iterativ**. Created on July 7, 2021, the strategy inherits the core design philosophy of the Nostalgia For Infinity series, integrating multiple technical indicator protection mechanisms and multi-timeframe analysis.

From the strategy architecture, the strategy adopts a "protection layer + core signal" dual-layer filtering mechanism. Each buy condition group is equipped with EMA protection, SMA200 trend protection, and special protection mechanisms for "dips" and "pumps." The 5-minute primary timeframe captures short-term opportunities while the 1-hour timeframe confirms long-term direction.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 26 independent buy signals, independently enableable/disableable |
| **Sell Conditions** | 8 basic sell signals + multi-layer dynamic take-profit + trailing stop |
| **Protection Mechanisms** | 8 groups (EMA, SMA200, Dip, Pump, etc.) |
| **Timeframe** | 5-minute primary + 1-hour informational |
| **Dependencies** | TA-Lib, technical (qtpylib), numpy, pandas, zema |

---

## II. Strategy Configuration Analysis

### Basic Risk Parameters

```python
minimal_roi = {
    "0": 0.10,      # Immediate: 10% profit
    "30": 0.05,     # After 30 minutes: 5% profit
    "60": 0.02,     # After 60 minutes: 2% profit
}

stoploss = -0.10   # 10% hard stop-loss

trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.005
trailing_stop_positive_offset = 0.030
```

---

## III. Entry Conditions Details

### 3.1 Protection Mechanisms

1. **EMA Protection** — Price vs. EMA relative position
2. **SMA200 Trend Protection** — Long-term trend direction confirmation
3. **Safe Dips Protection** — 11 levels (10-110) for dip filtering
4. **Safe Pump Protection** — 12 levels (10-120) with 24/36/48h periods

### 3.2 Core Buy Conditions

| Type | Conditions | Core Logic |
|------|-----------|------------|
| **Early Capture** | 1-6 | EMA crossover + Bollinger Band rebound with strict dip protection |
| **Momentum Acceleration** | 7-14 | EWO (Elliot Wave Oscillator) analysis for trend acceleration |
| **Trend Confirmation** | 15-24 | SMA200 trend confirmation for pullback entries |
| **ZEMA Ultimate** | 26 | Zero-lag EMA with optimizable parameters |

---

## IV. Exit Conditions Details

### 4.1 8 Basic Sell Conditions

1. **RSI + Bollinger Band Sell** — Overbought signal
2. **Dual RSI Sell** — Multi-timeframe momentum divergence
3. **EMA Relative Sell** — Price far from moving average
4. **RSI Below Threshold Sell** — Momentum exhaustion
5. **1h RSI Sell** — Long-term overbought
6. **Bollinger Band Relative Sell** — Price touching Bollinger upper band
7. **Custom Profit Ladder Sell** — Stepped take-profit
8. **Custom Loss Sell** — Stop-loss protection

### 4.2 Dynamic Take-Profit (12 Levels)

```python
# Profit ladder: 1% → 2% → 3% → ... → 20%
# Corresponding RSI thresholds: 34 → 35 → 37 → ... → 34
```

### 4.3 Trailing Stop (3 Modes)

1. **Standard Trailing** — Profit 16%-60% range
2. **Below EMA200 Trailing** — Protects profits when price drops below EMA200
3. **Long-Holding Trailing** — Positions held over 900 minutes (~15 hours)

---

## V. Technical Indicator System

### 5.1 1-Hour Timeframe Indicators

| Indicator | Period | Purpose |
|-----------|--------|---------|
| EMA | 12, 15, 20, 26, 35, 50, 100, 200 | Trend judgment |
| SMA | 200 | Long-term trend |
| RSI | 14 | Momentum |
| BB | 20, 2 std | Volatility |
| CMF | 20 | Money flow |
| Pump Protection | 24/36/48h | Filter sharp rises |

### 5.2 5-Minute Timeframe Indicators

| Indicator | Period | Purpose |
|-----------|--------|---------|
| EMA | 12, 15, 20, 26, 35, 50, 100, 200 | Trend judgment |
| SMA | 5, 30, 200 | Trend/support/resistance |
| BB | 20, 40 (2 std) | Volatility/rebound |
| RSI | 4, 14, 20 | Momentum |
| MFI | 14 | Money flow |
| EWO | 50, 200 | Momentum oscillator |
| ZEMA | 61 | Zero-lag EMA |
| Chopiness | 14 | Market smoothness |

---

## VI. Risk Management Features

### 6.1 Multi-Layer Protection

1. **Pre-Entry Protection**: 8 different protection mechanisms filter high-risk signals
2. **Mid-Holding Management**: Trailing stop and dynamic take-profit protect profits
3. **Extreme Scenario Handling**: Custom stop-loss and recovery mechanisms for prolonged drawdowns

### 6.2 Pump Protection (Pump Protection)

- 24/36/48h three time windows detect price volatility
- 12 different threshold levels (10-120) adapt to different volatility coins
- Distinguishes "safe pump" (can buy) from "dangerous pump" (sell)

### 6.3 Dip Protection (Dip Protection)

- 11 levels (10-110) correspond to different buying strengths
- 4 time windows (0/2/12/144 candles) for price change detection
- Higher levels allow larger pullback depths

---

## VII. Strategy Pros & Cons

### Advantages

1. **Multi-Condition Redundancy**: 26 buy conditions and 8 sell conditions provide high redundancy
2. **Strong Adaptability**: Multi-level protection adapts to different volatility markets
3. **Strong Trend-Following**: Generous stop-loss allows trends to fully develop
4. **Dual-Timeframe Confirmation**: 1h trend confirmation reduces short-term noise

### Limitations

1. **High Parameter Complexity**: Large number of adjustable parameters requires expertise
2. **Potentially Low Trading Frequency**: Strict protection may filter valid signals
3. **Sensitive to Market Conditions**: May underperform in highly volatile markets
4. **High Resource Consumption**: Multi-timeframe calculation requires more resources

---

## VIII. Applicable Scenarios

### Recommended
- Mainstream coin trading (BTC, ETH, etc.)
- Trend-clear markets (bull or clear rebound)
- Medium-to-long-term trading

### Not Recommended
- High-volatility small coins
- Sideways consolidation
- Low-liquidity markets

---

## IX. Live Trading Notes

### Best Market Conditions

| Market Type | Performance Rating | Notes |
|:------------|:------------------|:------|
| Bull Market | ⭐⭐⭐⭐⭐ | Clear trends, 10% take-profit easily triggered |
| Bear Market | ⭐⭐☆☆☆ | Strict risk control needed |
| Volatile Market | ⭐⭐⭐☆☆ | Pair with other strategies |

---

## X. Summary

**Combined_NFIv7_SMA_Rallipanos_20210707** is a powerful multi-condition trend-following strategy. Inheriting the excellent genes of the NostalgiaForInfinity series, it forms a complete trading system through 26 independent buy conditions and 8 sell conditions combined with multi-layer technical indicator protection mechanisms.

Core advantages:
- Multi-condition redundancy provides stability
- Dual-timeframe confirmation improves signal quality
- Flexible parameter configuration adapts to different markets
- Complete dynamic take-profit and trailing stop mechanisms

For experienced traders willing to invest time in strategy management, this is a worthwhile option. However, remember: no strategy is all-powerful; continuous monitoring and adjustment remain necessary.

---

> **Strategy Source**: NostalgiaForInfinityV7 by iterativ
> **Variant Version**: Rallipanos_20210707
> **Creation Date**: 2021-07-07
