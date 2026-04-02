# Combined_NFIv7_SMA_bAdBoY_20211204 Strategy Analysis

> **Strategy Number**: #130 (10th in Batch 13)
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Rebound + Dynamic Take-Profit
> **Timeframe**: 5 Minutes (5m) + 1 Hour (1h) Dual Timeframe

---

## I. Strategy Overview

**Combined_NFIv7_SMA_bAdBoY_20211204** is a variant of the NostalgiaForInfinityV7 series created by Freqtrade community developer **iterativ**. Created on December 4, 2021, the strategy inherits the core design philosophy of the Nostalgia For Infinity series, integrating multiple technical indicator protection mechanisms and multi-timeframe analysis.

From the strategy architecture, the strategy adopts a "protection layer + core signal" dual-layer filtering mechanism with 26 independent buy conditions and 8 sell conditions. Each condition includes protection combinations covering EMA, SMA200, Safe Dips, and Safe Pump mechanisms.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 26 independent buy signals (including #25), independently enableable/disableable |
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

1. **EMA Protection** — Fast/slow EMA relative position
2. **SMA200 Trend Protection** — Long-term trend direction
3. **Safe Dips Protection** — 11 levels (10-110)
4. **Safe Pump Protection** — 12 levels (10-120) with 24/36/48h periods

### 3.2 Core Buy Conditions

| Type | Conditions | Core Logic |
|------|-----------|------------|
| **Early Trend Start** | 1-6 | EMA crossover + Bollinger Band rebound with strict dip protection |
| **Momentum Acceleration** | 7-14 | EWO (Elliot Wave Oscillator) analysis |
| **SMA200 Trend Confirmation** | 15-24 | Emphasis on long-term trend protection |
| **ZEMA Special Signals** | 25-26 | Zero-lag EMA with custom parameters |

**Key Difference from Rallipanos version**: This version includes buy_condition_25 (not skipped), giving it broader coverage of ZEMA-based signals.

---

## IV. Exit Conditions Details

### 4.1 8 Basic Sell Conditions

1. **RSI + Bollinger Band Sell** — RSI overbought + consecutive BB upper band closes
2. **Dual RSI Sell** — 5m and 1h RSI both overbought
3. **RSI Single Overbought** — RSI exceeds main threshold
4. **Dual-Timeframe RSI Sell** — Both timeframes at high RSI
5. **EMA Relative Sell** — Close below EMA200 but above EMA50
6. **EMA Death Cross Sell** — EMA12 crosses below EMA26
7. **Bollinger Band Relative Sell** — Price breaks 1h BB upper band
8. **Custom Stop-Loss Sell** — Multi-layer custom risk management

### 4.2 Custom Stop-Loss Mechanism

Includes:
- **Base Stop-Loss**: Relative stop based on profit rate and RSI
- **Long-Holding Recovery Stop-Loss**: For positions held >20 hours
- **Pump Protection Stop-Loss**: Protective stop when abnormal volatility detected

### 4.3 Trailing Stop (3 Modes)

1. **Standard Trailing** — Profit 16%-60% range
2. **Below EMA200 Trailing** — Profit protection when price drops below EMA200
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

1. **Pre-Entry Protection**: 8 protection mechanisms filter high-risk signals
2. **Mid-Holding Management**: Trailing stop and dynamic take-profit protect profits
3. **Extreme Scenario Handling**: Custom stop-loss for prolonged drawdowns

### 6.2 Pump and Dip Protection

Same multi-level structure as other NFIv7 variants, with 11-12 levels and 24/36/48h windows.

---

## VII. Strategy Pros & Cons

### Advantages

1. **Multi-Condition Redundancy**: 26 buy + 8 sell conditions provide high redundancy
2. **Strong Adaptability**: Multi-level protection adapts to different volatility markets
3. **Strong Trend-Following**: -10% stop-loss allows trends to fully develop
4. **Dual-Timeframe Confirmation**: 1h trend confirmation reduces short-term noise

### Limitations

1. **High Parameter Complexity**: Requires expertise for optimization
2. **Potentially Low Trading Frequency**: Strict protection may filter signals
3. **Sensitive to Market Conditions**: May underperform in highly volatile markets
4. **High Resource Consumption**: Multi-timeframe calculation requires resources

---

## VIII. Applicable Scenarios

### Recommended
- Mainstream coin trading (BTC, ETH, etc.)
- Trend-clear markets (bull or clear rebound)
- Medium-to-long-term trading
- Strategy combinations with other strategies

### Not Recommended
- High-volatility small coins
- Sideways consolidation
- Low-liquidity markets

---

## IX. Live Trading Notes

### Performance by Market Type

| Market Phase | Performance Rating | Recommended Adjustment |
|--------------|-------------------|----------------------|
| Early Bull | ⭐⭐⭐⭐⭐ | Normal use |
| Late Bull | ⭐⭐⭐☆☆ | Reduce position size |
| Bear Market | ⭐⭐☆☆☆ | Reduce trading pairs |
| Volatile | ⭐⭐⭐☆☆ | Increase stop-loss width |

---

## X. Summary

**Combined_NFIv7_SMA_bAdBoY_20211204** is a powerful multi-condition trend-following strategy. It inherits the excellent genes of the NostalgiaForInfinity series through 26 independent buy conditions and 8 sell conditions combined with multi-layer technical indicator protection mechanisms.

Core advantages:
- Multi-condition redundancy provides stability
- Dual-timeframe confirmation improves signal quality
- Flexible parameter configuration adapts to different markets
- Complete dynamic take-profit and trailing stop mechanisms

For experienced traders willing to invest time in strategy management, this is a worthwhile option.

---

> **Strategy Source**: NostalgiaForInfinityV7 by iterativ
> **Variant Version**: bAdBoY_20211204
> **Creation Date**: 2021-12-04
