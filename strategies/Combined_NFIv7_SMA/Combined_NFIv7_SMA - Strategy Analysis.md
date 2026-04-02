# Combined_NFIv7_SMA Strategy Analysis

> **Strategy Number**: #128 (128th of 465 strategies)
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Rebound + Dynamic Take-Profit
> **Timeframe**: 5 Minutes (5m) + 1 Hour (1h) Dual Timeframe

---

## I. Strategy Overview

**Combined_NFIv7_SMA** is the 7th-generation variant of the NostalgiaForInfinityV7 series created by Freqtrade community developer **iterativ**, and is an upgraded version of NFIv6. The strategy inherits the core design philosophy of the Nostalgia For Infinity series, integrating multiple technical indicator protection mechanisms and multi-timeframe analysis to form a complex but efficient buy/sell signal system.

From the strategy architecture, Combined_NFIv7_SMA adopts a "protection layer + core signal" dual-layer filtering mechanism. Each buy condition group is equipped with EMA protection, SMA200 trend protection, and special protection mechanisms for "dips" and "pumps." The strategy adopts 5 minutes as the primary timeframe, with 1 hour for trend confirmation.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 26 independent buy signals (2 more than NFIv6), independently enableable/disableable |
| **Sell Conditions** | 8 basic sell signals + multi-layer dynamic take-profit + trailing stop |
| **Protection Mechanisms** | 8 groups of buy protection parameters |
| **Timeframe** | 5-minute primary + 1-hour informational |
| **Dependencies** | TA-Lib, technical (qtpylib), numpy, pandas, zema |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table (time: minimum profit rate)
minimal_roi = {
    "0": 0.10,      # Immediate: 10% profit
    "30": 0.05,     # After 30 minutes: 5% profit
    "60": 0.02,     # After 60 minutes: 2% profit
}

# Stop Loss Settings
stoploss = -0.10   # 10% hard stop-loss

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.005
trailing_stop_positive_offset = 0.030
```

**Key Difference from V6**: `trailing_stop_positive_offset` changed from 3.5% to 3.0% — trailing stop activates earlier in V7.

---

## III. Timeframe and Indicator System

### 3.1 Dual Timeframe Architecture

| Timeframe | Purpose | Period |
|-----------|---------|--------|
| 5 minutes | Primary trading timeframe, generates trade signals | Short-term |
| 1 hour | Informational timeframe, for trend confirmation and filtering | Long-term |

### 3.2 Core Indicator System

**1-Hour Timeframe Indicators**:
- EMA (12, 15, 20, 26, 35, 50, 100, 200)
- SMA 200 (trend judgment)
- RSI (14-period)
- Bollinger Bands (20-period, 2 standard deviations)
- Chaikin Money Flow (CMF)
- Hull Moving Average (HMA)

**5-Minute Timeframe Indicators**:
- EMA (12, 15, 20, 26, 35, 50, 100, 200)
- SMA (5, 30, 200)
- RSI (4 and 14 periods)
- MFI (Money Flow Index)
- Bollinger Bands (20 and 40 periods)
- EWO (Elliot Wave Oscillator)
- ZEMA (Zero-Lag EMA)
- Chopiness (market smoothness indicator)

---

## IV. Entry Conditions Details

### 4.1 New Conditions in V7 (Conditions #24 and #26)

**Type 7: ZEMA New Conditions** (Conditions 24, 26):
- Uses ZEMA (Zero-Lag EMA) as new entry judgment basis
- Condition #26 supports optimizable parameter configuration

The ZEMA (Zero-Lag EMA) is a variant of EMA that reduces lag, providing faster entry signals than traditional EMAs.

### 4.2 Main Buy Condition Categories

| Type | Conditions | Core Logic |
|------|-----------|------------|
| **RSI/MFI Oversold Rebound** | 1, 2 | RSI and MFI simultaneously oversold, with EMA and SMA200 trend protection |
| **Bollinger Band Rebound** | 3, 4 | BB40/BB20 lower band rapid rebound |
| **EMA Golden/Death Cross** | 5, 6, 7 | EMA12 crosses above EMA26 + various filters |
| **RSI Extreme Oversold** | 8, 18, 19, 20, 21 | RSI extremely low (<20 or similar) + volume expansion |
| **MA Offset** | 9, 10, 11, 14, 15, 16, 22 | Price below MA by certain percentage + confirmation |
| **EWO Oscillator** | 12, 13, 16, 17, 22, 23 | Elliot Wave Oscillator captures momentum reversal |
| **ZEMA** | 24, 26 | Zero-lag EMA for faster, more sensitive entry signals |

---

## V. Exit Conditions Details

### 5.1 Fixed Take-Profit Conditions (12-Level Dynamic Take-Profit)

```python
sell_custom_profit_0  = 0.01  (rsi < 34)
sell_custom_profit_1  = 0.02  (rsi < 35)
sell_custom_profit_2  = 0.03  (rsi < 37)
sell_custom_profit_3  = 0.04  (rsi < 42)
sell_custom_profit_4  = 0.05  (rsi < 43)
sell_custom_profit_5  = 0.06  (rsi < 45)
sell_custom_profit_6  = 0.07  (rsi < 48)
sell_custom_profit_7  = 0.08  (rsi < 54)
sell_custom_profit_8  = 0.09  (rsi < 55)
sell_custom_profit_9  = 0.10  (rsi < 54)
sell_custom_profit_10 = 0.12  (rsi < 42)
sell_custom_profit_11 = 0.20  (rsi < 34)
```

### 5.2 Trailing Stop (3 Modes)

- **Mode 1**: Profit 16-60%, RSI 20-50, 3% drawdown from high
- **Mode 2**: Profit 10-40%, RSI 20-50, 3% drawdown
- **Mode 3**: Profit 6-20%, 1h SMA200 declining, 5% drawdown

### 5.3 Long-Holding Protection

V7 adds **900-minute (approximately 15-hour) holding protection**: automatically exits when holding exceeds 15 hours with profit between 3-4%.

---

## VI. Protection Mechanism Deep Dive

### 6.1 Safe Dips (Safe Dips) Protection

12 levels (10-120) with different dip thresholds, preventing bottom-fishing at mid-slope.

### 6.2 Safe Pump (Safe Pump) Protection

12 levels (10-120) with 24/36/48-hour periods, preventing chasing at the top.

---

## VII. Strategy Pros & Cons

### Advantages

1. **Multi-Layer Protection**: 8 protection mechanisms significantly reduce false signals
2. **Dual-Timeframe Analysis**: Combines 5m and 1h, balancing short-term and long-term
3. **Refined Take-Profit**: 12-level dynamic take-profit maximizes profits
4. **Highly Configurable**: 26 buy conditions independently controllable
5. **New ZEMA Indicator**: Zero-lag EMA provides more sensitive entry signals

### Limitations

1. **High Complexity**: Large parameter count requires expertise and time for optimization
2. **Trading Frequency**: May generate many trades during bull markets
3. **Overfitting Risk**: Large parameter count may overfit historical data

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Bull Market / Wide Volatility** | Enable all conditions | Best performance |
| **Consolidation** | Reduce condition count | Protection triggers frequently |
| **Bear Market** | Reduce position count | Trading frequency decreases |
| **Extreme Volatility** | Use with caution | Price limits may affect execution |

---

## IX. Live Trading Notes

### 9.1 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| Bull Market | ⭐⭐⭐⭐⭐ | Clear trends; multi-condition resonance most effective |
| Volatile Market | ⭐⭐⭐☆☆ | Protection triggers frequently; may miss opportunities |
| Bear Market | ⭐⭐☆☆☆ | Protection triggers; trading frequency reduced |
| Extreme Volatility | ⭐⭐☆☆☆ | Price limit moves may affect execution |

---

## X. Summary

**Combined_NFIv7_SMA** is a refined upgrade from NFIv6, adding 2 new buy conditions (#24 and #26) and introducing the ZEMA indicator for more diverse entry signals.

Its core value lies in:
1. **Multi-Layer Protection**: 8 protection mechanisms reduce false signals
2. **Refined Take-Profit**: 12-level dynamic take-profit lets profits run
3. **Flexible Configuration**: 26 buy conditions independently controllable
4. **Dual Timeframe**: Balances short-term and long-term

For quantitative traders, test thoroughly in paper trading first, then gradually apply to live trading based on actual market performance.

---

*This document is automatically generated based on strategy source code.*
