# CryptoFrogHO Strategy Analysis

> **Strategy ID**: #136 (136th of 465 strategies)  
> **Strategy Type**: Smoothed Heiken Ashi + Bollinger Band Expansion + Ultra-Aggressive ROI + Dynamic Risk Control  
> **Timeframe**: 5 minutes (5m) + 1-hour informational layer

---

## I. Strategy Overview

**CryptoFrogHO** is the advanced optimization version of the CryptoFrog strategy (HO = Higher Order), further tuned by community developers for high-volatility markets. On top of the original core logic (Smoothed HA, BB Expansion, Linear-Decay Stop-Loss), this strategy significantly raises the ROI target and adds a more aggressive trailing stop mechanism.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 4 independent buy modes (1 more than original) |
| **Sell Conditions** | Multi-condition combinations + dynamic ROI + aggressive trailing |
| **Protection** | Linear-decay custom stop-loss + dynamic ROI + multi-level trailing |
| **Timeframe** | 5 minutes + 1-hour informational layer |
| **Dependencies** | TA-Lib, finta, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table - More aggressive than original
minimal_roi = {
    "0": 0.30,       # 0-30 minutes: 30% profit (vs original 21.3%)
    "30": 0.15,      # 30-72 minutes: 15% profit
    "72": 0.055,     # 72-144 minutes: 5.5% profit
    "144": 0         # After 144 minutes: free exit
}

# Stop-Loss Setting
stoploss = -0.065   # -6.5% starting stop-loss (vs original -8.5%, more conservative)

# Trailing Stop - More aggressive
trailing_stop = True
trailing_stop_positive = 0.008
trailing_stop_positive_offset = 0.055
trailing_only_offset_is_reached = False
```

**Design Philosophy**:
- **Ultra-high ROI target**: First target of 30%, one of the highest settings in Freqtrade strategies
- **Faster stepped exit**: Progressively lowered from 30% → 15% → 5.5%, shorter time windows
- **More conservative starting stop-loss**: -6.5% vs original -8.5%, reduces capital risk
- **Earlier trailing activation**: Starts trailing from 5.5% profit

### 2.2 Custom Stop-Loss Parameters

```python
custom_stop = {
    # Linear decay parameters - shorter time
    'decay-time': 144,           # Decay time (minutes), vs original 166
    'decay-delay': 0,            # Delay start time
    'decay-start': -0.065,       # Starting stop-loss
    'decay-end': -0.015,         # Ending stop-loss (closer to 0)

    # Profit and momentum
    'cur-min-diff': 0.025,       # Current vs minimum profit difference
    'cur-threshold': -0.015,     # Threshold for considering trailing
    'roc-bail': -0.025,          # ROC dynamic exit value
    'rmi-trend': 55,             # RMI trend threshold (stricter)

    # Positive trailing - more levels
    'pos-trail': True,           # Enable positive trailing
    'pos-threshold': 0.004,      # Profit threshold (lower)
    'pos-trail-dist': 0.012      # Trailing distance
}
```

---

## III. Entry Conditions Details

### 3.1 Core Entry Logic

CryptoFrogHO's buy signal adds one more mode compared to the original:

```
Buy signal = (Price condition) & (Informational layer condition) & (4 alternative modes) & (Volume condition)
```

#### 3.1.1 Price Condition Layer

```python
# Close price must be below 5-minute Smoothed Heiken Ashi low
(dataframe['close'] < dataframe['Smooth_HA_L'])
```

#### 3.1.2 Informational Layer Condition

```python
# 1-hour Hansen HA EMA confirms trend (same as original)
(dataframe['emac_1h'] < dataframe['emao_1h'])
```

### 3.2 Alternative Buy Conditions (Four Modes)

#### Mode A: BB Expansion + Momentum Filtering (Enhanced)

```python
# Bollinger Band expansion + squeeze ended + stricter MFI conditions
(dataframe['bbw_expansion'] == 1) & (dataframe['sqzmi'] == False)
& (
    (dataframe['mfi'] < 18)  # MFI lower (original 20)
    |
    (dataframe['dmi_minus'] > 32)  # DMI- higher (original 30)
)
```

#### Mode B: SAR + Stochastic RSI Oversold (Enhanced)

```python
# Price below SAR + stricter oversold conditions
(dataframe['close'] < dataframe['sar'])
& ((dataframe['srsi_d'] >= dataframe['srsi_k']) & (dataframe['srsi_d'] < 25))
& ((dataframe['fastd'] > dataframe['fastk']) & (dataframe['fastd'] < 20))
& (dataframe['mfi'] < 25)
```

#### Mode C: DMI Crossover + Bollinger Band Bottom (Same as original)

```python
# DMI- crosses above DMI+
((dataframe['dmi_minus'] > 32) & qtpylib.crossed_above(dataframe['dmi_minus'], dataframe['dmi_plus']))
& (dataframe['close'] < dataframe['bb_lowerband'])
# Or
# SQZMI squeeze mode
(dataframe['sqzmi'] == True)
& ((dataframe['fastd'] > dataframe['fastk']) & (dataframe['fastd'] < 18))
```

#### Mode D: HO New Addition - Dual Oversold Confirmation (New)

```python
# Two oversold indicators simultaneously satisfied
(dataframe['rsi'] < 25)  # RSI extremely low
& (dataframe['mfi'] < 20)  # MFI extremely low
& (dataframe['close'] < dataframe['bb_lowerband'])  # Price at Bollinger Band bottom
& (dataframe['volume'] > dataframe['volume'].rolling(20).mean() * 0.5)  # Volume not too low
```

### 3.3 Volume Filtering

```python
# VFI is negative and volume exists
(dataframe['vfi'] < 0.0) & (dataframe['volume'] > 0)
```

---

## IV. Exit Logic Details

### 4.1 Core Exit Logic

```python
# Close price above Heiken Ashi high
(dataframe['close'] > dataframe['Smooth_HA_H'])
& # 1-hour Hansen HA EMA confirms
(dataframe['emac_1h'] > dataframe['emao_1h'])
& # BB expansion + MFI/DMI overbought
(
    (dataframe['bbw_expansion'] == 1)
    &
    (
        (dataframe['mfi'] > 82)
        |
        (dataframe['dmi_plus'] > 32)
    )
)
& # Volume confirmation
(dataframe['vfi'] > 0.0) & (dataframe['volume'] > 0)
```

### 4.2 Dynamic ROI System

The strategy implements the `min_roi_reached_dynamic` function with enhanced features:

```python
# Trend detection - stricter thresholds
droi_trend_type = ['rmi', 'ssl', 'candle', 'any']

# Trend judgment logic (stricter)
- RMI trend: rmi-up-trend == 1 AND rmi > 55 (original 50)
- SSL trend: ssl-dir == 'up'
- Candle trend: candle-up-trend == 1

# In trend: Allow holding until trend ends
# During pullback: Exit half position when profit retraces to pullback_value
```

### 4.3 Multi-Level Trailing Stop

```python
# Level 1: Triggers when profit > 0.4%, trailing distance 1.2%
#
# Level 2: Triggers when profit > 2%, trailing distance 2%
```

---

## V. Technical Indicator System

### 5.1 Core Custom Indicators

| Indicator Name | Calculation Method | Purpose |
|---------------|-------------------|---------|
| **Smoothed HA** | Heiken Ashi smoothed (EMA 4) | Filters market noise, confirms price position |
| **Hansen HA EMA** | SMA based on 6-period HA | 1-hour trend confirmation |
| **BB Expansion** | Bollinger Band width breaks 1.1x of 4-period high | Volatility burst signal |
| **SQZMI** | Bollinger Band Squeeze indicator (finta) | Quiet period detection |
| **VFI** | Volume Flow Indicator | Money flow confirmation |
| **RMI** | Relative Momentum Index | Momentum trend judgment |
| **SROC** | Smoothed Rate of Change | Smoothed rate of change |

### 5.2 Standard Technical Indicators

| Indicator Category | Specific Indicators | Parameters | Purpose |
|-------------------|--------------------|-----------|---------|
| **Trend Indicators** | EMA, SMA | Multi-period | Trend judgment |
| **Momentum Indicators** | RSI, Stochastic RSI, RMI | 14/24 periods | Overbought/oversold |
| **Volatility Indicators** | Bollinger Bands | 20,1 | Support/resistance |
| **Trend Indicators** | DMI/ADX | 14 periods | Trend strength |
| **Volume** | VFI, MFI | - | Money flow |
| **Reversal Indicator** | SAR | 0.02, 0.2 | Trend reversal points |

---

## VI. Risk Management Highlights

### 6.1 Linear-Decay Stop-Loss

Shorter time window than original:

```
Timeline (minutes): 0 ---- 144 ---->
Stop-loss value:       -6.5% ----> -1.5%
```

**How it works**:
- Immediately applies -6.5% stop upon entry
- Linearly decays to -1.5% within 144 minutes
- Reaches loose stop faster than original

### 6.2 Dynamic ROI

| Condition | ROI Behavior |
|-----------|-------------|
| **In trend** | Ignore ROI table, continue holding until trend ends |
| **During pullback** | When profit retraces from high to pullback_value, sell half |
| **Ranging market** | Fall back to standard ROI table |

### 6.3 Aggressive Trailing Stop

Dual-level trailing system:
- Level 1: Triggers at profit > 0.4%, trailing distance 1.2%
- Level 2: Triggers at profit > 2%, trailing distance 2%

---

## VII. Strategy Pros & Cons

### Pros

1. **Higher ROI target**: 30% first target, more lucrative in high-volatility markets
2. **Dual oversold confirmation**: New 4th buy mode, stricter filtering
3. **More conservative starting stop-loss**: -6.5% vs -8.5%, reduces capital loss
4. **Faster stop-loss relaxation**: 144 minutes vs 166 minutes
5. **Multi-level trailing system**: Dual protection, profits won't fully retrace

### Cons

1. **30% target too high**: Unlikely to be reached in most markets
2. **More complex**: One more buy mode than original
3. **Computationally intensive**: Dual timeframe + multi-indicator
4. **Higher risk exposure**: High ROI target means higher potential losses

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Extremely high-volatility pairs** | Keep default parameters | 30% target needs extreme swings |
| **Mainstream coin stability** | Significantly lower ROI target | Adjust to 15-20% |
| **Clear trending markets** | Enable dynamic ROI | Let profits run |
| **Ranging markets** | Adjust decay-end | More aggressive stop-loss |

---

## IX. Applicable Market Environment Analysis

CryptoFrogHO is more aggressive than the original, suitable only for **ultra-high-volatility, strong-trend** markets.

### 9.1 Core Strategy Logic

- **Trend confirmation**: 1-hour Hansen HA EMA ensures trend-following trades
- **Volatility filtering**: BB expansion ensures entry at volatility burst
- **Momentum verification**: Stochastic RSI, DMI, SRSI multi-filter false signals
- **Entry logic**: Price below HA low + multiple oversold conditions (1 more mode than original)

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|---------:|
| Strong Uptrend | ⭐⭐⭐⭐⭐ | Ultra-high ROI + dynamic ROI catches super waves |
| Downtrend | ⭐⭐ | Stricter buy conditions, may enter counter-trend |
| Wide-range oscillation | ⭐⭐⭐ | BB expansion captures volatility turning points |
| Extreme volatility | ⭐⭐⭐⭐⭐ | 30% target + volatility detection |
| Consolidation | ⭐ | 30% target completely unreachable |

### 9.3 Key Configuration Recommendations

| Configuration Item | Default | Suggested | Notes |
|-------------------|---------|-----------|-------|
| minimal_roi."0" | 0.30 | 0.15-0.25 | Adjust based on volatility |
| decay-time | 144 | 100-180 | Adjust based on holding habits |
| decay-end | -0.015 | -0.025~-0.01 | More conservative stop |
| droi_trend_type | any | rmi | Stricter trend judgment |

---

## X. Summary

**CryptoFrogHO** is the high-order aggressive version of CryptoFrog. Its core value lies in:

1. **Higher profit expectation**: 30% first target vs 21.3%
2. **Stricter entry**: 4 modes vs 3, added dual oversold confirmation
3. **Safer stop-loss**: -6.5% starting vs -8.5%
4. **Faster market adaptation**: 144-minute decay vs 166 minutes

For quantitative traders, CryptoFrogHO is suitable for investors with extensive Freqtrade experience who pursue high returns. Start testing with a reduced ROI target and gradually find parameters suited to your risk tolerance.

**Usage Recommendation**: This strategy is designed for ultra-high-volatility markets and only suitable for extremely volatile trading pairs. Ensure proper capital management when using it.
