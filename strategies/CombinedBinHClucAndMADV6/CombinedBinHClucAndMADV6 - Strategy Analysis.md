# CombinedBinHClucAndMADV6 Strategy Analysis

> **Strategy Number**: #124 (124th of 465 strategies)
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Combination
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**CombinedBinHClucAndMADV6** is an evolutionary version of CombinedBinHClucAndMADV5, developed and open-sourced by ilya. This strategy further expands on MADV5 by adding a sixth buy condition group, forming a more diversified six-dimensional signal filtering system.

The strategy integrates buy logic from four classic strategies: BinHV45 (Bollinger Band 40-period rebound), ClucMay72018 (Bollinger Band 20-period low-volume), MACD Low Buy (MACD low-position buy), and SSL Channel strategy. Six independent indicator cross-validation improves signal reliability.

From a code architecture perspective, the strategy uses technical indicator combinations across different time periods to capture trend opportunities while filtering out most market noise. It adopts 5 minutes as the primary timeframe, with 1 hour for higher-dimensional trend judgment.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 6 independent buy signals, independently enableable/disableable |
| **Sell Conditions** | 1 basic sell signal + trailing stop |
| **Protection Mechanism** | Custom stop-loss logic (forced exit after 240 minutes) |
| **Timeframe** | 5-minute primary + 1-hour informational |
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

### 3.1 Six Independent Buy Conditions

| Condition Group | Condition # | Core Logic | Source Strategy |
|----------------|-------------|------------|-----------------|
| **BB20 Low Volume (Bull)** | #1 | BB20 lower band + EMA trend confirmation + volume filtering | ClucMay72018 |
| **BB20 Low Volume (Bear)** | #2 | BB20 lower band + RSI oversold + volume contraction | ClucMay72018 |
| **MACD Low Buy (Bull)** | #3 | MACD golden cross + volume contraction + BB lower band | MACD Low Buy |
| **MACD Low Buy (Bear)** | #4 | MACD golden cross + strong volume contraction + BB lower band | MACD Low Buy |
| **SSL Channel + RSI** | #5 | SSL channel bullish + EMA trend + RSI reversal | SSL Channels |
| **Enhanced Multi-Indicator** | #6 | Enhanced multi-indicator verification | MADV6 New |

### 3.2 Condition #6: Enhanced Multi-Indicator Verification

```python
# Logic
- close > EMA200 (1h)
- SSL Channel in bullish alignment
- RSI < 35 (oversold zone)
- Volume contracted for 2 consecutive periods
- Price touching Bollinger lower band
```

**Design Philosophy**:
- Combines multi-dimensional indicators for confirmation, requiring multiple conditions simultaneously
- Emphasizes consecutive volume contraction, improving signal reliability
- Combines RSI oversold zone with price position judgment to increase rebound probability

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
| **Trend Indicators** | EMA200, EMA9, EMA21 | Market trend direction judgment |
| **Volatility Indicators** | Bollinger Bands (20, 2), Bollinger Bands (40, 2) | Overbought/oversold zone identification |
| **Momentum Indicators** | RSI (14), MACD (12, 26, 9) | Buy/sell timing judgment |
| **Volume Indicators** | Volume, Volume MA | False breakout filtering |
| **SSL Indicators** | SSL Channels | Trend confirmation |

### 5.2 Informational Timeframe (1h) Indicators

- **EMA200 (1h)**: Long-term trend judgment
- **RSI (1h)**: Macro momentum analysis
- **Price Position (1h)**: Overall market relative position

---

## VI. Risk Management Features

### 6.1 Multi-Condition Redundancy Design

The strategy achieves signal redundancy through six independent buy conditions:
- Even if some conditions fail, other conditions can still trigger trades
- Different conditions adapt to different market environments
- Each condition can be independently enabled/disabled

### 6.2 Dual Protection Mechanism

1. **Profit Protection**: Trailing stop ensures gained profits won't fully retreat
2. **Time Protection**: 240-minute forced exit avoids long-term risk

---

## VII. Strategy Pros & Cons

### Advantages

1. **Multi-Condition Verification**: Six independent buy conditions filter false signals from different dimensions
2. **Fast In, Fast Out**: 2.1% target take-profit with 40-minute time limit reduces holding risk
3. **Trend Combination**: Combines long-term EMA200 trend judgment, improving signal direction accuracy
4. **Flexible Configuration**: Each condition can be independently enabled/disabled for easy optimization
5. **Dual Protection**: Trailing stop + time stop-loss dual protection mechanism

### Limitations

1. **Excessive Parameters**: Six buy conditions plus multiple parameter groups make optimization difficult
2. **Sparse Signals**: Multi-condition combinations lead to fewer trading signals, potentially missing opportunities
3. **Computational Load**: Multi-indicator calculation has higher hardware requirements
4. **Overfitting Risk**: Complex strategies easily overfit historical data

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Clear Unilateral Trend** | Enable all 6 conditions | Multi-condition filtering ensures high-confidence signals |
| **Volatile Market** | Disable conditions #3, #4 | Reduce MACD golden cross false signals |
| **High Volatility** | Adjust take-profit to 3% | Give more volatility room |
| **Low Volatility** | Adjust take-profit to 1.5% | Lower profit expectations |

---

## IX. Live Trading Notes

**CombinedBinHClucAndMADV6** is the latest evolutionary version of the Combined strategy series. On top of MADV5, it adds a sixth buy condition. It is best suited for **trending markets with clear direction** and performs average during sideways consolidation periods.

### 9.1 Core Strategy Logic

- **Multi-Condition Cross-Validation**: Six buy conditions judge entry timing from different angles
- **Trend Filtering**: Uses EMA200 to determine major direction, avoiding counter-trend trades
- **Price-Volume Coordination**: Volume contraction is a common filtering condition across multiple conditions
- **Oversold Rebound**: Core logic captures oversold rebound opportunities

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| Uptrend | ⭐⭐⭐⭐⭐ | Multiple conditions coordinate with trend, accurately capturing pullback entries |
| Downtrend | ⭐⭐⭐☆☆ | Counter-trend trades have high risk; use with caution |
| Volatile Market | ⭐⭐⭐⭐☆ | Suitable for buy-low-sell-high but signals are sparse |
| Extreme Volatility | ⭐⭐☆☆☆ | Multi-conditions may fail; slow to react |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Notes |
|--------------|-------------------|-------|
| Timeframe | 5m/1h | Primary: 5 minutes; observe: 1 hour |
| Trading Pair Selection | Mainstream coins | Better liquidity, more stable indicators |
| Minimum Profit | 0.1% | Avoid frequent trades with tiny profits |

---

## X. Summary

**CombinedBinHClucAndMADV6** is a highly complex multi-condition combined strategy, suitable for experienced quantitative traders. Its core value lies in:

1. **Multi-Dimensional Signal Filtering**: Six independent conditions verify trading signals from different angles
2. **Trend and Reversal Combination**: Can both capture trend opportunities and identify reversal signals
3. **Flexible Configuration**: Each condition can be independently controlled to adapt to different market environments

For quantitative traders, it is recommended to fully test in paper trading first, understand each condition's performance, then gradually apply to live trading. Complex strategies require more time and effort for maintenance and optimization.
