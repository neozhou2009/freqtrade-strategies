# CryptoFrog Strategy Analysis

> **Strategy ID**: #133 (133rd of 465 strategies)  
> **Strategy Type**: Smoothed Heiken Ashi + Bollinger Band Expansion + Dynamic ROI/Stop-Loss  
> **Timeframe**: 5 minutes (5m) + 1-hour informational layer

---

## I. Strategy Overview

**CryptoFrog** is a complex multi-condition entry strategy created and shared by community developers. The strategy combines multiple technical indicators including Smoothed Heiken Ashi, Bollinger Band Expansion, Stochastic RSI, DMI, and VFI, building a unique trend-following and volatility-capture system. The strategy's core feature is its custom linear-decay stop-loss and dynamic ROI system.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | Multi-condition combinations (based on Heiken Ashi, BB Expansion, Stochastic RSI, DMI) |
| **Sell Conditions** | Multi-condition combinations (based on Heiken Ashi, BB Expansion, MFI, DMI) |
| **Protection** | Linear-decay custom stop-loss + dynamic ROI + trailing stop |
| **Timeframe** | 5 minutes + 1-hour informational layer |
| **Dependencies** | TA-Lib, finta, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.213,      # 0-39 minutes: 21.3% profit
    "39": 0.103,     # 39-96 minutes: 10.3% profit
    "96": 0.037,     # 96-166 minutes: 3.7% profit
    "166": 0         # After 166 minutes: free exit
}

# Stop-Loss Setting
stoploss = -0.085   # -8.5% starting stop-loss (managed by custom linear decay)

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.047
trailing_only_offset_is_reached = False
```

**Design Philosophy**:
- **Aggressive ROI**: First target of 21.3%, one of the higher settings in Freqtrade strategies
- **Stepped exit**: Progressively lowered from 21.3% → 10.3% → 3.7%
- **Linear-decay stop-loss**: From -8.5% starting, linearly decaying to -2% within 166 minutes

### 2.2 Custom Stop-Loss Parameters

```python
custom_stop = {
    # Linear decay parameters
    'decay-time': 166,           # Decay time (minutes)
    'decay-delay': 0,            # Delay start time
    'decay-start': -0.085,       # Starting stop-loss
    'decay-end': -0.02,          # Ending stop-loss
    
    # Profit and momentum
    'cur-min-diff': 0.03,        # Current vs minimum profit difference
    'cur-threshold': -0.02,      # Threshold for considering trailing stop
    'roc-bail': -0.03,           # ROC dynamic exit value
    'rmi-trend': 50,             # RMI trend threshold
    
    # Positive trailing
    'pos-trail': True,           # Enable positive trailing
    'pos-threshold': 0.005,      # Profit threshold to trigger trailing
    'pos-trail-dist': 0.015      # Trailing distance
}
```

---

## III. Entry Conditions Details

### 3.1 Core Entry Logic

CryptoFrog's buy signal is a complex multi-layer filtering system:

```
Buy signal = (Price condition) & (Informational layer condition) & (Multiple alternative condition combos) & (Volume condition)
```

#### 3.1.1 Price Condition Layer

```python
# Close price must be below 5-minute Smoothed Heiken Ashi low
(dataframe['close'] < dataframe['Smooth_HA_L'])
```

#### 3.1.2 Informational Layer Condition

```python
# 1-hour Hansen HA EMA confirms trend
(dataframe['emac_1h'] < dataframe['emao_1h'])
```

### 3.2 Alternative Buy Conditions (Three Modes)

The strategy provides three independent buy modes connected by `|`; any one mode satisfied triggers a buy:

#### Mode A: BB Expansion + Momentum Filtering

```python
# Bollinger Band expansion + Bollinger Band squeeze ended
(dataframe['bbw_expansion'] == 1) & (dataframe['sqzmi'] == False)
& (
    (dataframe['mfi'] < 20)  # MFI oversold
    |
    (dataframe['dmi_minus'] > 30)  # DMI- strong
)
```

#### Mode B: SAR + Stochastic RSI Oversold

```python
# Price below SAR
(dataframe['close'] < dataframe['sar'])
& ((dataframe['srsi_d'] >= dataframe['srsi_k']) & (dataframe['srsi_d'] < 30))
& ((dataframe['fastd'] > dataframe['fastk']) & (dataframe['fastd'] < 23))
& (dataframe['mfi'] < 30)
```

#### Mode C: DMI Crossover + Bollinger Band Bottom

```python
# DMI- crosses above DMI+
((dataframe['dmi_minus'] > 30) & qtpylib.crossed_above(dataframe['dmi_minus'], dataframe['dmi_plus']))
& (dataframe['close'] < dataframe['bb_lowerband'])
# Or
# SQZMI squeeze mode
(dataframe['sqzmi'] == True)
& ((dataframe['fastd'] > dataframe['fastk']) & (dataframe['fastd'] < 20))
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
        (dataframe['mfi'] > 80)
        |
        (dataframe['dmi_plus'] > 30)
    )
)
& # Volume confirmation
(dataframe['vfi'] > 0.0) & (dataframe['volume'] > 0)
```

### 4.2 Dynamic ROI System

The strategy implements the `min_roi_reached_dynamic` function to dynamically adjust ROI based on market trends:

```python
# Trend detection
droi_trend_type = ['rmi', 'ssl', 'candle', 'any']  # Configurable

# Trend judgment logic
- RMI trend: rmi-up-trend == 1
- SSL trend: ssl-dir == 'up'
- Candle trend: candle-up-trend == 1

# In trend: Allow holding until trend ends
# During pullback: Exit half position when profit retraces to pullback_value
```

### 4.3 Custom Stop-Loss Logic

```python
def custom_stoploss(...):
    # If profit below threshold
    if current_profit < cstp_threshold.value:
        # ROC mode
        if cstp_bail_how in ('roc', 'any'):
            if (sroc/100) <= cstp_bail_roc.value:
                return 0.001  # Exit immediately
        
        # Time mode
        if cstp_bail_how in ('time', 'any'):
            if trade_dur > cstp_bail_time.value:
                return 0.001  # Exit immediately
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

### 5.3 Informational Timeframe Indicators (1 Hour)

- Hansen HA EMA (emac_1h, emao_1h)
- Other indicators merged via merge_informative_pair

---

## VI. Risk Management Highlights

### 6.1 Linear-Decay Stop-Loss

This is CryptoFrog's most unique risk control mechanism:

```
Timeline (minutes): 0 ---- 166 ---->
Stop-loss value:     -8.5% ----> -2%
```

**How it works**:
- Immediately applies -8.5% stop upon entry
- Stop-loss line gradually moves toward 0 over time
- After 166 minutes, stop-loss stabilizes at -2%
- This both protects capital and gives losing positions more recovery time

### 6.2 Dynamic ROI

| Condition | ROI Behavior |
|-----------|-------------|
| **In trend** | Ignore ROI table, continue holding until trend ends |
| **During pullback** | When profit retraces from high to pullback_value, sell half position |
| **Ranging market** | Fall back to standard ROI table |

### 6.3 Positive Trailing Stop

When profit exceeds 0.5%:
- Trailing stop set 1.5% below current price
- Only enabled when in profit, protects profits

---

## VII. Strategy Pros & Cons

### Pros

1. **Unique indicator combination**: Smoothed HA + Hansen HA EMA provide unique trend perspective
2. **Volatility capture**: BB expansion detection enters before volatility bursts
3. **Linear-decay stop-loss**: Gives losing positions more time to recover
4. **Dynamic ROI**: Doesn't take profits during trends, lets profits run
5. **Multi-mode entry**: Three independent modes cover more scenarios

### Cons

1. **Numerous parameters**: Over 20 custom parameters, high optimization difficulty
2. **Computationally intensive**: Multi-indicator + multi-timeframe, heavy VPS load
3. **Aggressive ROI**: 21.3% first target hard to reach in low-volatility markets
4. **Complex logic**: Custom stop-loss and dynamic ROI require deep understanding

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **High-volatility pairs** | Keep default parameters | 21.3% target suitable for large swings |
| **Mainstream coin stability** | Lower ROI target | Adjust to 10-15% |
| **Clear trending markets** | Enable dynamic ROI | Let profits run |
| **Ranging markets** | Adjust decay-end | More aggressive stop-loss |

---

## IX. Applicable Market Environment Analysis

CryptoFrog is a highly specialized strategy, best suited for **high-volatility, strong-trend** markets.

### 9.1 Core Strategy Logic

- **Trend confirmation**: 1-hour Hansen HA EMA ensures trend-following trades
- **Volatility filtering**: BB expansion ensures entry at volatility burst
- **Momentum verification**: Stochastic RSI, DMI, SRSI multi-filter false signals
- **Entry logic**: Price below HA low + multiple oversold conditions

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|---------:|
| Strong Uptrend | ⭐⭐⭐⭐⭐ | Multi-trend confirmation + dynamic ROI catches big waves |
| Downtrend | ⭐⭐⭐ | Buy conditions may enter counter-trend |
| Wide-range oscillation | ⭐⭐⭐⭐ | BB expansion captures volatility turning points |
| Fast volatility | ⭐⭐⭐⭐⭐ | 21.3% target + volatility detection |
| Consolidation | ⭐⭐ | Complex conditions, may have long signal gaps |

### 9.3 Key Configuration Recommendations

| Configuration Item | Default | Suggested | Notes |
|-------------------|---------|-----------|-------|
| minimal_roi."0" | 0.213 | 0.10-0.20 | Adjust based on volatility |
| decay-time | 166 | 120-240 | Adjust based on holding habits |
| decay-end | -0.02 | -0.03~ -0.01 | More conservative stop |
| droi_trend_type | any | rmi | Stricter trend judgment |

---

## X. Summary

**CryptoFrog** is a highly specialized trend-following strategy whose core value lies in:

1. **Unique perspective**: Smoothed Heiken Ashi provides clear price structure
2. **Volatility detection**: BB expansion indicator catches volatility burst points
3. **Intelligent risk control**: Linear-decay stop-loss + dynamic ROI
4. **Multi-mode coverage**: Three buy modes adapt to different scenarios

For quantitative traders, CryptoFrog is suitable for investors with some Freqtrade experience who seek professional-grade strategies. Start with default parameters, validate with small-capital live trading, then fine-tune based on specific trading pairs and market conditions.

**Usage Recommendation**: This strategy is designed for high-volatility markets. Ensure you select high-volatility trading pairs and that your VPS has sufficient computational resources.
