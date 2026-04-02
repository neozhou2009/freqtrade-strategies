# CryptoFrogHO3A2 Strategy Analysis

> **Strategy ID**: Batch 14 - 8th Strategy  
> **Strategy Type**: Third-Order Heiken Ashi + Aggressive ROI + Balanced Risk Control  
> **Timeframe**: 5 minutes (5m) + 1-hour informational layer

---

## I. Strategy Overview

**CryptoFrogHO3A2** is the second variant (A2) of the CryptoFrogHO3 series, providing a more balanced risk-reward ratio with parameter fine-tuning on top of HO3A1.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 3 independent buy modes |
| **Sell Conditions** | Multi-condition combinations + dynamic ROI + trailing stop |
| **Protection** | Linear-decay custom stop-loss + dynamic ROI |
| **Timeframe** | 5 minutes + 1-hour informational layer |
| **Dependencies** | TA-Lib, finta, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.051,       # 0-10 minutes: 5.1% profit
    "10": 0.02,       # 10-24 minutes: 2% profit
    "24": 0.01,       # 24-64 minutes: 1% profit
    "64": 0           # After 64 minutes: free exit
}

# Stop-Loss Setting
stoploss = -0.239     # -23.9% starting stop-loss

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.221
trailing_stop_positive_offset = 0.30
trailing_only_offset_is_reached = True
```

**Design Philosophy**:
- **Aggressive but moderate**: First target 5.1%, slightly lower than A1
- **Shorter ladder**: Completes all steps within 64 minutes
- **Moderate stop-loss**: -23.9% more conservative than A1's -29.9%

---

## III. Entry Conditions Details

Same three modes as HO3A1:
- Mode A: BB Expansion + Momentum Filtering
- Mode B: SAR + Stochastic RSI Oversold
- Mode C: DMI Crossover + Bollinger Band Bottom / SQZMI Squeeze

Volume filtering: `(dataframe['vfi'] < 0.0) & (dataframe['volume'] > 0)`

---

## IV. Risk Management Highlights

### 4.1 Linear-Decay Stop-Loss

```
Timeline (minutes): 0 ---- 166 ---->
Stop-loss value:       -8.5% ----> -2%
```

### 4.2 Trailing Stop

- Triggers when profit exceeds 30%
- Trailing distance 22.1%

---

## V. Strategy Pros & Cons

### Pros

1. **Aggressive but moderate**: 5.1% first target, more balanced risk-reward
2. **Shorter cycle**: Completes ladder within 64 minutes
3. **Moderate stop-loss**: -23.9% more conservative than A1
4. **Trend tracking**: Dynamic ROI lets profits run

### Cons

1. **Still needs high volatility**: 5.1% target requires some volatility
2. **May have large losses**: -23.9% starting stop-loss
3. **Parameter sensitivity**: Needs adjustment based on market

---

## VI. Summary

**CryptoFrogHO3A2** is the balanced version of HO3A1:

1. **Moderate ROI target**: 5.1% first target
2. **Shorter cycle**: Completes ladder within 64 minutes
3. **Balanced stop-loss**: -23.9% starting
4. **Dynamic ROI**: Lets profits run during trends

**Usage Recommendation**: Suitable for traders with some risk tolerance pursuing higher returns. Performs better in high-volatility markets.
