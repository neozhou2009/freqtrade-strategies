# CombinedBinHClucAndMADV9 Strategy Analysis

> **Strategy Number**: #129 (129th of 465 strategies)
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Combination
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**CombinedBinHClucAndMADV9** is the ninth-generation evolutionary version of the CombinedBinHClucAndMADV series, developed and open-sourced by ilya. This strategy further expands on MADV8 by adding more buy conditions, forming a more diversified nine-dimensional signal filtering system.

The strategy integrates buy logic from multiple classic strategies: BinHV45 (Bollinger Band 40-period rebound), ClucMay72018 (Bollinger Band 20-period low-volume), MACD Low Buy (MACD low-position buy), SSL Channel strategy, and others. Nine independent indicator cross-validation improves signal reliability.

From a code architecture perspective, the strategy uses technical indicator combinations across different time periods to capture trend opportunities while filtering out most market noise. It adopts 5 minutes as the primary timeframe, with 1 hour and 15 minutes as informational layers.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 9 independent buy signals, independently enableable/disableable |
| **Sell Conditions** | 1 basic sell signal + trailing stop |
| **Protection Mechanism** | Custom stop-loss logic (forced exit after 240 minutes) |
| **Timeframe** | 5-minute primary + 15-minute + 1-hour informational |
| **Dependencies** | TA-Lib, technical (qtpylib), numpy, pandas |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table (time: minimum profit rate)
minimal_roi = {
    "0": 0.021,     # Immediate exit: 2.1% profit
    "40": 0.005,    # After 40 minutes: 0.5% profit
}

# Stop Loss Settings
stoploss = -0.99  # Effectively disabled hard stop-loss

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = False
trailing_stop_positive = 0.01      # 1% trailing stop activation
trailing_stop_positive_offset = 0.025  # 2.5% offset trigger
```

### 2.2 Exit Signal Configuration

```python
use_exit_signal = True
exit_profit_only = True
exit_profit_offset = 0.001
ignore_roi_if_entry_signal = False
```

---

## III. Entry Conditions Details

### 3.1 Nine Independent Buy Conditions

| Condition Group | Condition # | Core Logic | Source Strategy |
|----------------|-------------|------------|-----------------|
| **BB20 Low Volume (Bull)** | #1 | BB20 lower band + EMA trend confirmation + volume filtering | ClucMay72018 |
| **BB20 Low Volume (Bear)** | #2 | BB20 lower band + RSI oversold + volume contraction | ClucMay72018 |
| **MACD Low Buy (Bull)** | #3 | MACD golden cross + volume contraction + BB lower band | MACD Low Buy |
| **MACD Low Buy (Bear)** | #4 | MACD golden cross + strong volume contraction + BB lower band | MACD Low Buy |
| **SSL Channel + RSI** | #5 | SSL channel bullish + EMA trend + RSI reversal | SSL Channels |
| **Enhanced Multi-Indicator** | #6 | Multi-indicator comprehensive verification | MADV6 Enhanced |
| **Trend Confirmation Enhanced** | #7 | EMA9 crossover + consecutive volume contraction | MADV9 New |
| **Volatility Breakout** | #8 | Bollinger Band width contraction + volume breakout | MADV9 New |
| **Multi-Timeframe Resonance** | #9 | 5m/15m/1h simultaneous confirmation | MADV9 New |

### 3.2 Conditions #7-9: New Conditions Detail

#### Condition #7: Trend Confirmation Enhanced
```python
# Logic
- close > EMA200 (1h)
- EMA9 crosses above EMA21 (golden cross)
- Volume contracted for 3 consecutive periods
- Price touching Bollinger lower band
```

#### Condition #8: Volatility Breakout Strategy
```python
# Logic
- Bollinger Band width contracted to historical lows
- RSI in 30-50 range
- Volume expands beyond moving average
- Price breaks above Bollinger middle band
```

#### Condition #9: Multi-Timeframe Resonance
```python
# Logic
- 5m: Price touches BB lower band
- 1h: EMA200 upward
- 15m: MACD golden cross
- Volume contraction confirmation
```

---

## IV. Exit Conditions Details

### 4.1 ROI Exit Mechanism

```python
minimal_roi = {
    "0": 0.021,     # Immediate exit: 2.1% profit
    "40": 0.005,    # After 40 minutes: 0.5% profit
}
```

### 4.2 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_stop_positive = 0.01      # 1% trailing stop activation
trailing_stop_positive_offset = 0.025  # 2.5% offset trigger
```

### 4.3 Custom Stop-Loss Logic

```python
def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs) -> float:
    hold_duration = (current_time - trade.open_date_utc).total_seconds() / 60
    if hold_duration > 240:
        return 0.0  # Exit signal
    return None
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Trend Indicators** | EMA200, EMA9, EMA21 | Market trend direction |
| **Volatility Indicators** | Bollinger Bands (20, 2), Bollinger Bands (40, 2) | Overbought/oversold zone identification |
| **Momentum Indicators** | RSI (14), MACD (12, 26, 9) | Buy/sell timing |
| **Volume Indicators** | Volume, Volume MA | False breakout filtering |
| **SSL Indicators** | SSL Channels | Trend confirmation |

### 5.2 Multi-Timeframe (15m)

- **MACD (15m)**: Medium-term momentum judgment
- **EMA Crossover (15m)**: Short-term trend confirmation

---

## VI. Risk Management Features

### 6.1 Multi-Condition Redundancy Design

Nine independent buy conditions provide signal redundancy:
- Even if some conditions fail, others can still trigger trades
- Different conditions adapt to different market environments

### 6.2 Three-Timeframe Verification

- **5 Minutes**: Primary trading cycle
- **15 Minutes**: Medium-term signal confirmation
- **1 Hour**: Long-term trend judgment

### 6.3 Dual Protection Mechanism

1. **Profit Protection**: Trailing stop locks in profits
2. **Time Protection**: 240-minute forced exit avoids long-term risk

---

## VII. Strategy Pros & Cons

### Advantages

1. **Multi-Condition Verification**: Nine independent buy conditions filter false signals from different dimensions
2. **Fast In, Fast Out**: 2.1% target take-profit with 40-minute time limit reduces holding risk
3. **Trend Combination**: Long-term EMA200 trend judgment improves signal accuracy
4. **Multi-Timeframe Resonance**: Three-cycle verification significantly improves signal reliability
5. **Flexible Configuration**: Each condition independently enableable/disableable
6. **Dual Protection**: Trailing stop + time stop-loss

### Limitations

1. **Excessive Parameters**: Nine buy conditions plus multiple parameter groups make optimization extremely difficult
2. **Sparse Signals**: Multi-condition combinations lead to very few trading signals
3. **High Computational Load**: Multi-indicator multi-timeframe calculations require significant hardware
4. **High Overfitting Risk**: Complex strategies easily overfit historical data

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Clear Unilateral Trend** | Enable all 9 conditions | Multi-condition filtering ensures high-confidence signals |
| **Volatile Market** | Disable conditions #3, #4, #7 | Reduce MACD false signals |
| **High Volatility** | Adjust take-profit to 3% | Give more room |
| **Low Volatility** | Adjust take-profit to 1.5% | Lower expectations |

---

## IX. Live Trading Notes

**CombinedBinHClucAndMADV9** is the ninth-generation evolutionary version of the Combined strategy series. On top of MADV8, it adds a ninth buy condition. It is best suited for **trending markets with clear direction** and performs average during sideways periods.

### 9.1 Core Strategy Logic

- **Multi-Condition Cross-Validation**: Nine buy conditions judge entry timing from different angles
- **Trend Filtering**: Uses EMA200 to determine major direction
- **Price-Volume Coordination**: Volume contraction is a common filter
- **Oversold Rebound**: Core logic captures oversold rebound opportunities
- **Multi-Timeframe Resonance**: 15m/1h multi-cycle verification

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| Uptrend | ⭐⭐⭐⭐⭐ | Multiple conditions coordinate with trend, accurately capturing pullback entries |
| Downtrend | ⭐⭐⭐☆☆ | Counter-trend trades have high risk; use with caution |
| Volatile Market | ⭐⭐⭐⭐☆ | Suitable for buy-low-sell-high but signals sparse |
| Extreme Volatility | ⭐⭐☆☆☆ | Multi-conditions may fail; slow to react |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Notes |
|--------------|-------------------|-------|
| Timeframe | 5m/15m/1h | Primary: 5m; observe: 15m and 1h |
| Trading Pair Selection | Mainstream coins | Better liquidity, more stable indicators |
| Minimum Profit | 0.1% | Avoid frequent tiny-profit trades |

---

## X. Summary

**CombinedBinHClucAndMADV9** is an extremely complex multi-condition combined strategy, suitable for experienced quantitative traders. Its core value lies in:

1. **Multi-Dimensional Signal Filtering**: Nine independent conditions verify trading signals from different angles
2. **Trend and Reversal Combination**: Captures both trend opportunities and reversal signals
3. **Multi-Timeframe Resonance**: 15m/1h multi-cycle verification significantly improves reliability
4. **Flexible Configuration**: Each condition independently controllable for different market environments

For quantitative traders, it is recommended to fully test in paper trading first, understand each condition's performance, then gradually apply to live trading.
