# Cluc4werk Strategy In-Depth Analysis

> **Strategy ID**: #88 (8th in Batch 9)
> **Strategy Type**: Bollinger Bands + ROCR Trend Filter
> **Timeframe**: 1 Minute (1m)

---

## I. Strategy Overview

**Cluc4werk** is a short-cycle trading strategy based on Bollinger Bands and ROCR (Rate of Change Ratio) indicators. The strategy's core feature is using the 1-hour ROCR indicator for trend filtering, while combining a dual Bollinger Band system (40-period and 20-period) to capture short-term trading opportunities.

### Key Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 modes (BinHV variant + Cluc variant) |
| **Sell Conditions** | Price breaks Bollinger middle band |
| **Protection** | ROCR trend filter + Hard stop-loss |
| **Timeframe** | 1 Minute (main) + 1 Hour (informative) |
| **Dependencies** | TA-Lib, technical, qtpylib, numpy |
| **Special Features** | Multi-timeframe analysis, Dual Bollinger Band system |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.015,    # Immediate exit: 1.5% profit
    "20": 0.005,   # After 20 minutes: 0.5% profit
    "30": 0.001,   # After 30 minutes: 0.1% profit
}

# Stop-Loss Setting
stoploss = -0.01  # -1% hard stop-loss

# Trailing Stop Configuration
trailing_stop = False  # Not enabled

# Exit Signal Configuration
use_exit_signal = True
exit_profit_only = True
ignore_roi_if_entry_signal = True
```

**Design Philosophy**:
- **Multi-Tier ROI**: 3-tier decreasing ROI; exit threshold lowers as holding time extends
- **Tight Stop-Loss**: -1% hard stop-loss; relatively tight
- **Exit Signal Only**: exit_profit_only = True; exits only when profitable

### 2.2 Timeframe Configuration

```python
timeframe = '1m'  # Main timeframe: 1 minute

# Informative Timeframe
def informative_pairs(self):
    pairs = self.dp.current_whitelist()
    informative_pairs = [(pair, '1h') for pair in pairs]
    return informative_pairs
```

**Description**:
- Main timeframe: 1 minute (short-term trading)
- Informative timeframe: 1 hour (trend filtering)

---

## III. Entry Conditions Details

### 3.1 ROCR Trend Filter

```python
# 1-hour period ROCR filter
dataframe['rocr_1h'].gt(0.65)
```

**Meaning**: 1-hour period ROCR (168 periods) greater than 0.65 indicates 1-hour timeframe is in an uptrend.

### 3.2 Buy Conditions - Mode 1 (BinHV Variant)

```python
(
    dataframe['lower'].shift().gt(0) &
    dataframe['bbdelta'].gt(dataframe['close'] * 0.006) &
    dataframe['closedelta'].gt(dataframe['close'] * 0.013) &
    dataframe['tail'].lt(dataframe['bbdelta'] * 0.968) &
    dataframe['close'].lt(dataframe['lower'].shift()) &
    dataframe['close'].le(dataframe['close'].shift())
)
```

**Logic**:
- `lower.shift() > 0`: Bollinger lower band valid (not NaN)
- `bbdelta > close * 0.006`: Bollinger bandwidth > 0.6%
- `closedelta > close * 0.013`: Price change > 1.3%
- `tail < bbdelta * 0.968`: Lower shadow < 96.8% of bandwidth
- `close < lower.shift()`: Price < previous candle's Bollinger lower band
- `close <= close.shift()`: Price not higher than previous candle's close

### 3.3 Buy Conditions - Mode 2 (Cluc Variant)

```python
(
    (dataframe['close'] < dataframe['ema_slow']) &
    (dataframe['close'] < 0.013 * dataframe['bb_lowerband']) &
    (dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 28))
)
```

**Logic**:
- `close < ema_slow`: Price < EMA50 (weak trend)
- `close < 0.013 * bb_lowerband`: Price < Bollinger lower band × 0.013 (extremely low price)
- `volume < volume_mean_slow.shift(1) * 28`: Volume < 30-day average × 28 (ultra-low volume)

### 3.4 Combined Buy Logic

```python
dataframe.loc[
    (
        dataframe['rocr_1h'].gt(0.65)  # 1-hour trend filter
    ) &
    (
        # Mode 1 OR Mode 2
        (Mode 1 conditions) | (Mode 2 conditions)
    ),
    'buy'
] = 1
```

**Key Point**:
- Must satisfy 1-hour ROCR > 0.65 (trend filter)
- Satisfy either of the two buy modes to enter

---

## IV. Exit Logic Details

### 4.1 Sell Conditions

```python
(
    (qtpylib.crossed_above(dataframe['close'], dataframe['bb_middleband'])) &
    (dataframe['volume'] > 0)
)
```

**Logic**:
- `crossed_above(close, bb_middleband)`: Price crosses above Bollinger middle band
- `volume > 0`: Volume confirmation

**Combined Meaning**: Sell when price breaks above Bollinger middle band with volume confirmation.

### 4.2 ROI Exit Mechanism

| Time | Minimum Profit |
|------|----------------|
| 0 minutes | 1.5% |
| 20 minutes | 0.5% |
| 30 minutes | 0.1% |

### 4.3 Exit Signal Configuration

```python
use_exit_signal = True       # Enable exit signal
exit_profit_only = True      # Exit only when profitable
ignore_roi_if_entry_signal = True  # Ignore ROI if new entry signal
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameter | Purpose |
|-------------------|-------------------|-----------|---------|
| **Volatility Indicator** | Bollinger Bands | 40 periods, 2x std dev | BinHV variant |
| **Volatility Indicator** | Bollinger Bands | 20 periods, 2x std dev | Cluc variant |
| **Trend Indicator** | EMA | 50 periods | Price trend judgment |
| **Momentum Indicator** | ROCR | 28 periods (1m) / 168 periods (1h) | Trend filter |
| **Volume** | Volume MA | 30 periods | Volume filter |

### 5.2 Custom Bollinger Band Function

```python
def bollinger_bands(stock_price, window_size, num_of_std):
    rolling_mean = stock_price.rolling(window=window_size).mean()
    rolling_std = stock_price.rolling(window=window_size).std()
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return np.nan_to_num(rolling_mean), np.nan_to_num(lower_band)
```

**Description**: Custom 40-period Bollinger Band calculation for BinHV variant.

### 5.3 Multi-Timeframe Analysis

Strategy uses 1-hour ROCR indicator for trend filtering:

```python
# 1-minute ROCR
dataframe['rocr'] = ta.ROCR(dataframe, timeperiod=28)

# 1-hour ROCR
inf_tf = '1h'
informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=inf_tf)
informative['rocr'] = ta.ROCR(informative, timeperiod=168)
dataframe = merge_informative_pair(dataframe, informative, self.timeframe, inf_tf, ffill=True)
```

---

## VI. Risk Management Features

### 6.1 Tight Stop-Loss

```python
stoploss = -0.01  # -1%
```

**Description**: -1% tight stop-loss; suitable for short-term trading.

### 6.2 ROCR Trend Filter

```python
dataframe['proch'].gt(0.65)
```

**Function**:
- Only buy when 1-hour uptrend confirmed
- Avoid counter-trend trading
- Reduce false signals

### 6.3 ROI Exit Mechanism

| Time | Minimum Profit |
|------|----------------|
| 0 minutes | 1.5% |
| 20 minutes | 0.5% |
| 30 minutes | 0.1% |

**Strategy**: Quick accumulation of small profits; suitable for high-frequency trading.

---

## VII. Strategy Pros & Cons

### Advantages

1. **ROCR Trend Filter**: Uses 1-hour ROCR to filter; avoids counter-trend trades
2. **Dual Bollinger Bands**: 40-period + 20-period; covers different time dimensions
3. **Tight Stop-Loss**: -1% stop-loss; controls single-trade loss
4. **Quick Exit**: 1.5% initial ROI; quickly accumulates profits
5. **Multi-Timeframe**: Combines 1-minute and 1-hour analysis

### Limitations

1. **Medium Complexity**: Dual Bollinger Bands + multi-timeframe; requires experience to debug
2. **Parameter Sensitive**: ROCR threshold 0.65 may need per-market adjustment
3. **High Trading Frequency**: 1-minute timeframe may lead to overtrading
4. **Trend Dependent**: ROCR filter may miss trend start opportunities
5. **Informative Timeframe Delay**: 1-hour ROCR may lag

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|---------------------------|-------|
| **Ranging Market** | Adjust ROCR threshold | Lower ROCR threshold increases signals |
| **Uptrend** | Default configuration | ROCR filter effective |
| **Downtrend** | Pause trading | ROCR filter may fail |
| **High Volatility** | Adjust stop-loss | 1% stop-loss may be too tight |
| **Low Volatility** | Adjust ROI | May need to lower ROI threshold |

---

## IX. Applicable Market Environment Details

Cluc4werk is a strategy based on the "Bollinger Bands + ROCR Trend Filter" core philosophy.

### 9.1 Core Strategy Logic

- **ROCR Trend Filter**: 1-hour ROCR > 0.65; ensures uptrend
- **Dual Bollinger Bands**: 40-period + 20-period; covers different time dimensions
- **Price Breakout**: Sell when price breaks Bollinger middle band

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Uptrend | Four Stars | ROCR filter effective; trend-following |
| Wide-range Ranging | Three Stars | Bollinger signals frequent; may overtrade |
| Downtrend | Two Stars | ROCR filter may fail |
| Fast Fluctuation | Four Stars | 1-minute framework responsive |

### 9.3 Key Configuration Suggestions

| Configuration | Suggested Value | Notes |
|---------------|-----------------|-------|
| **Number of trading pairs** | 10-20 | Higher signal frequency |
| **Maximum open trades** | 2-4 | Control risk |
| **Position mode** | Fixed position | Recommend fixed position |
| **Timeframe** | 1m | Mandatory requirement |

---

## X. Important Notes: The Cost of Complexity

### 10.1 Medium Learning Curve

Strategy code is ~80 lines; requires understanding:
- Bollinger Band calculation
- ROCR indicator principle
- Multi-timeframe analysis

### 10.2 Low Hardware Requirements

Single timeframe calculation is light:

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|----------------|
| 10-20 pairs | 512MB | 1GB |
| 20-40 pairs | 1GB | 2GB |

### 10.3 Multi-Timeframe Notes

Strategy uses 1-hour informative timeframe:
- Requires historical 1-hour data
- Data delay may affect signal accuracy
- Needs stable data source for live trading

### 10.4 Manual Trading Suggestions

Manual traders can reference this strategy's approach:
- Observe both 1-minute and 1-hour charts simultaneously
- Use ROCR to confirm trend direction
- Set 1.5% take-profit and 1% stop-loss

---

## XI. Summary

**Cluc4werk** is a meticulously designed Bollinger Band + ROCR trend filter strategy, with core value in:

1. **ROCR Trend Filter**: 1-hour ROCR > 0.65; ensures trend-following trades
2. **Dual Bollinger Bands**: 40-period + 20-period; covers different time dimensions
3. **Tight Stop-Loss**: -1% stop-loss; controls single-trade loss
4. **Quick Exit**: 1.5% initial ROI; suitable for high-frequency trading
5. **Multi-Timeframe**: Combines 1-minute and 1-hour analysis

For quantitative traders, this is an excellent Bollinger Band + trend filter template. Recommendations:
- Use as an entry case for learning multi-timeframe analysis
- Understand ROCR indicator application methods
- Note trading frequency may be high; configure reasonably
- Sufficient testing before live trading; pay attention to slippage and fees
