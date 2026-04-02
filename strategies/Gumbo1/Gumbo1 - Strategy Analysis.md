# Gumbo1 Strategy: In-Depth Analysis

> **Strategy ID**: #192 (192nd of 465 strategies)
> **Strategy Type**: Trend Reversal / Counter-Trend Bottom-Picking
> **Timeframe**: 5 Minutes (5m) + 1-Hour Informational Layer

---

## I. Strategy Overview

Gumbo1 is a trend reversal strategy based on the Elliott Wave Oscillator (EWO), T3 Moving Average, and Bollinger Bands. The core idea is to capture rebound opportunities at the end of a downtrend — when EWO shows an extremely negative value and price is near Bollinger Band support, it enters.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | EWO extreme negative value + T3/EMA position + 1-hour Bollinger Band confirmation |
| **Exit Conditions** | Stochastic overbought + T3 touching Bollinger middle band |
| **Protections** | Hard stop-loss + Multi-timeframe confirmation |
| **Timeframe** | 5 minutes (main) + 1 hour (informational layer) |
| **Dependencies** | TA-Lib, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,    # Immediate exit: 10% profit
    "20": 0.05,   # After 20 minutes: 5% profit
    "64": 0.03,   # After 64 minutes: 3% profit
    "168": 0      # After 168 minutes: break-even exit
}

# Stop-Loss Settings
stoploss = -0.25     # -25% hard stop-loss
```

**Design Philosophy**:
- **Loose Stop-Loss**: -25% stop-loss gives trades enormous room for volatility, suitable for capturing rebound opportunities
- **Tiered Take-Profit**: Decreasing from 10% to break-even, gradually locking in profits and avoiding greed

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

---

## III. Entry Conditions Details

### 3.1 Core Entry Logic

The strategy uses a triple-confirmation mechanism — all conditions must be met simultaneously:

| Condition # | Condition Name | Logic Description |
|-----------|---------------|-------------------|
| Condition 1 | EWO Extreme Negative | EWO < ewo_low threshold |
| Condition 2 | 1-Hour Bollinger Band Confirmation | bb_middleband_1h >= T3_1h |
| Condition 3 | Price Consolidation Signal | T3 <= EMA |

### 3.2 Entry Conditions Explained

#### Condition #1: EWO Extreme Negative Value
```python
dataframe['EWO'] < self.ewo_low.value
```

**Logic**:
- EWO (Elliott Wave Oscillator) is used to identify momentum extremes
- When EWO falls below the ewo_low threshold, it indicates downward momentum has reached an extreme
- Extreme negative values typically appear at the end of a downtrend, signaling potential reversal opportunity

#### Condition #2: 1-Hour Bollinger Band Confirmation
```python
dataframe['bb_middleband_1h'] >= dataframe['T3_1h']
```

**Logic**:
- Uses the 1-hour timeframe Bollinger middle band for trend confirmation
- When the Bollinger middle band is above the T3 moving average, long-term trend may be reversing
- Multi-timeframe confirmation increases signal reliability

#### Condition #3: T3 vs. EMA Position
```python
dataframe[f'T3_{self.t3_periods.value}'] <= dataframe['EMA']
```

**Logic**:
- T3 below EMA indicates short-term price is in consolidation or oversold state
- This positional relationship suggests price is about to choose a direction
- Provides timing confirmation for entry

### 3.3 Comprehensive Entry Signal Assessment

The strategy's entry logic can be summarized as:
> **Wait until it's oversold, then enter** — when EWO shows an extreme negative value, and multi-timeframe Bollinger Bands give support confirmation, enter at the price consolidation level.

---

## IV. Exit Logic Details

### 4.1 Exit Conditions

The strategy uses two independent exit signals:

```python
# Exit Signal 1: Stochastic overbought
dataframe[f'stoch_{self.stock_periods.value}'] > self.stoch_high.value

# Exit Signal 2: T3 touches Bollinger middle band
dataframe[f'T3_{self.t3_periods.value}'] >= dataframe['bb_middleband_40']
```

### 4.2 Exit Signal Details

| Signal Name | Trigger Condition | Technical Meaning |
|-------------|------------------|-------------------|
| Stochastic Overbought | Stochastic > 80 | Short-term price rise too large, potential pullback |
| T3 Touches Middle Band | T3 >= Bollinger Middle Band | Price has rebounded to resistance level |

### 4.3 ROI Tiered Take-Profit Mechanism

The strategy employs a phased take-profit approach:

| Holding Time | Target Profit | Design Intent |
|-------------|--------------|--------------|
| Immediate | 10% | Quickly lock in substantial profit |
| After 20 minutes | 5% | Gradually lower expectations |
| After 64 minutes | 3% | Conservative lock-in |
| After 168 minutes | Break-even | Time stop, avoid prolonged holding |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Momentum Indicator** | EWO (Elliott Wave Oscillator) | Identifies momentum extremes, recognizes trend reversal points |
| **Trend Indicator** | T3 Moving Average | Smooths price, identifies trend direction |
| **Trend Indicator** | EMA | Short-term trend reference |
| **Volatility Indicator** | Bollinger Bands | Confirms support/resistance, judges price position |
| **Oscillator Indicator** | Stochastic | Identifies overbought/oversold, confirms exit timing |

### 5.2 Informational Timeframe Indicators (1 Hour)

The strategy uses 1-hour timeframe as an informational layer, providing higher-dimensional trend judgment:

- **1-Hour Bollinger Middle Band**: Confirms long-term trend direction
- **T3_1h**: Compared with Bollinger middle band to judge support strength

---

## VI. Risk Management Highlights

### 6.1 Loose Stop-Loss Mechanism

```python
stoploss = -0.25  # -25%
```

**Design Philosophy**:
- Reversal market volatility is intense; sufficient space is needed
- Avoids the awkward situation of "bouncing right back after being stopped out"
- Suitable for high-volatility trading pairs

**Risk Warning**:
- Single trade loss may be significant
- Position sizing must be managed to control risk

### 6.2 Multi-Timeframe Confirmation

The strategy uses 5-minute main timeframe + 1-hour informational layer:

| Timeframe | Purpose |
|-----------|---------|
| 5 Minutes | Entry timing judgment |
| 1 Hour | Trend direction confirmation |

### 6.3 ROI Tiered Take-Profit

| Profit Target | Trigger Condition |
|--------------|-------------------|
| 10% | Immediate take-profit |
| 5% | After 20 minutes holding |
| 3% | After 64 minutes holding |
| Break-even | After 168 minutes holding |

---

## VII. Strategy Pros & Cons

### Strengths

1. **Multi-Indicator Confirmation**: EWO + T3 + Bollinger Bands triple confirmation improves signal reliability
2. **Strong Reversal Capture**: Specifically designed for trend reversal, excels at catching rebounds
3. **Loose Stop-Loss Room**: -25% stop-loss provides sufficient volatility space, suitable for volatile pairs
4. **Multi-Timeframe Verification**: 1-hour informational layer provides additional trend confirmation

### Weaknesses

1. **Many Parameters**: EWO, T3, Bollinger Bands, Stochastic parameters need adjustment
2. **Loose Stop-Loss Risk**: -25% stop-loss may result in large single-trade losses
3. **Reversal Failure Risk**: If trend doesn't reverse, may be trapped for extended periods
4. **Average Performance in Ranging Markets**: May trade frequently in markets without clear trends

---

## VIII. Applicable Scenarios

| Market Environment | Recommendation | Notes |
|-------------------|---------------|-------|
| End of Downtrend | Strongly Recommended | Core scenario, captures reversals |
| Slight Downward Ranging | Use with Caution | May frequently trigger stop-loss |
| Unilateral Upward | Not Recommended | Cannot capture upward moves |
| High Volatility | Adjust Parameters | May need wider stop-loss |

---

## IX. Applicable Market Environment Analysis

Gumbo1 is a typical **counter-trend bottom-picking strategy**. Based on its code architecture and logic, it is best suited for **rebound opportunities at the end of downtrends**, and performs poorly in unilateral upward or highly volatile markets.

### 9.1 Strategy Core Logic

- **Wait until oversold**: EWO extreme negative value indicates downward momentum has reached an extreme
- **Multi-Timeframe Confirmation**: 1-hour Bollinger Bands provide long-term trend support
- **Price Consolidation Confirmation**: T3/EMA position relationship judges entry timing

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| End of Downtrend | ★★★★★ | Core scenario, EWO extreme negative + rebound confirmation |
| Ranging Market | ★★★☆☆ | May frequently trigger entries and stop-losses |
| Unilateral Downtrend | ★★☆☆☆ | Trend doesn't reverse, sustained losses |
| Unilateral Uptrend | ★☆☆☆☆ | Cannot capture upward moves |

### 9.3 Key Configuration Recommendations

| Config Item | Suggested Value | Notes |
|------------|---------------|-------|
| stoploss | -0.20 ~ -0.25 | Adjust based on pair volatility |
| ewo_low | Negative value | More negative = stricter |
| stoch_high | 75-85 | Overbought threshold |

---

## X. Important Notes: The Cost of Complexity

### 10.1 Learning Curve

Gumbo1 involves multiple technical indicators:
- EWO (Elliott Wave Oscillator)
- T3 Moving Average
- Bollinger Bands
- Stochastic

Understanding each indicator's principles and interactions is necessary; beginners may need considerable time to become familiar.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------------|------------|----------------|
| Under 10 pairs | 2GB | 4GB |
| 10-30 pairs | 4GB | 8GB |
| Over 30 pairs | 8GB | 16GB |

### 10.3 Backtesting vs. Live Trading Differences

**Notes**:
- EWO extreme negative values in backtesting may be difficult to capture precisely in live trading
- Loose stop-loss may perform well in backtesting but face greater psychological pressure in live trading
- Multi-timeframe data synchronization may have delays

### 10.4 Manual Trading Suggestions

If you want to manually apply this strategy's logic:
1. Observe whether EWO has reached an extreme negative value
2. Confirm 1-hour Bollinger middle band position
3. Look for entry opportunities when price consolidates
4. Strictly enforce stop-loss; avoid holding through losses

---

## XI. Summary

**Gumbo1** is a counter-trend bottom-picking strategy focused on trend reversal. Its core value lies in:

1. **Multi-Indicator Confirmation Mechanism**: EWO + T3 + Bollinger Bands triple confirmation improves signal reliability
2. **Captures Reversal Opportunities**: Specifically designed for the end of downtrends, excels at catching rebounds
3. **Loose Stop-Loss Room**: -25% stop-loss provides sufficient volatility space, suitable for volatile trading pairs

For quantitative traders, Gumbo1 is a typical reversal strategy template, suitable for finding entry opportunities at the end of downtrends. Note the risks from loose stop-loss and use position management accordingly.

---
