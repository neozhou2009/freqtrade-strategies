# Combined_Indicators Strategy Analysis

> **Strategy Number**: #126 (126th of 465 strategies)
> **Strategy Type**: Multi-Strategy Combination + Bollinger Band Mean Reversion
> **Timeframe**: 1 Minute (1m)

---

## I. Strategy Overview

**Combined_Indicators** is a combined strategy fusing two classic intraday strategies, created by Freqtrade community developers. The strategy integrates the core logic of BinHV45 (Bollinger Band 40-period rebound strategy) and ClucMay72018 (Bollinger Band 20-period low-volume strategy), aiming to improve buy signal quality through dual-strategy cross-validation.

From a code architecture perspective, the strategy's design philosophy leverages the complementarity of different-period Bollinger Band indicators to capture price reversal opportunities. BinHV45 focuses on rapid rebounds after Bollinger Band contractions, while ClucMay72018 focuses on breakout opportunities in low-volume environments. This combination allows the strategy to adapt well to different market conditions.

The strategy adopts 1 minute as the primary timeframe — the most sensitive of all timeframes — capable of capturing the finest price fluctuations. This extremely high-frequency trading approach means the strategy generates a large number of trades, making it highly sensitive to trading slippage and fees.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent buy signals from different strategy sources |
| **Sell Conditions** | 1 basic sell signal + trailing stop |
| **Protection Mechanism** | Trailing stop + fixed take-profit |
| **Timeframe** | 1-minute primary timeframe |
| **Dependencies** | TA-Lib, technical (qtpylib), numpy, pandas |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table (time: minimum profit rate)
minimal_roi = {
    "0": 0.015
}

# Stop Loss Settings
stoploss = -0.0658

# Trailing Stop
trailing_stop = True
trailing_stop_positive = 0.0198
trailing_stop_positive_offset = 0.03082
trailing_only_offset_is_reached = True
```

**Design Philosophy**:
- ROI table set to a single exit point of 1.5% — a typical "fast in, fast out" design. Immediately exiting upon achieving 1.5% profit means the strategy pursues high-frequency small profits
- Hard stop-loss at -6.58% is relatively generous for a 1-minute timeframe, giving price sufficient room to fluctuate
- Trailing stop configured with 1.98% positive tracking and 3.082% offset trigger, allowing profits to run when trends are clear while protecting existing gains
- `trailing_only_offset_is_reached = True` ensures trailing stop only activates after price reaches the offset trigger, avoiding frequent triggers during volatile markets

### 2.2 Exit Signal Configuration

```python
use_exit_signal = True
exit_profit_only = False
ignore_roi_if_entry_signal = False
```

**Configuration Notes**:
- `exit_profit_only = False` allows sell signals to execute even when at a loss — different from most trend-following strategies
- This design aligns with the mean-reversion philosophy of selling when price reverts to the mean

---

## III. Entry Conditions Details

### 3.1 Condition #1: BinHV45 Strategy Rebound Signal

This uses BinHV45's core logic to capture rapid rebounds after Bollinger Band contractions:

```python
# BinHV45 Buy Conditions
(dataframe['lower'].shift().gt(0) &
 dataframe['bbdelta'].gt(dataframe['close'] * 0.00703) &
 dataframe['closedelta'].gt(dataframe['close'] * 0.01476) &
 dataframe['tail'].lt(dataframe['bbdelta'] * 0.03632) &
 dataframe['close'].lt(dataframe['lower'].shift()) &
 dataframe['close'].le(dataframe['close'].shift()))
```

**Logic Analysis**:
- `lower.shift().gt(0)`: Ensures previous Bollinger Band lower band is valid
- `bbdelta.gt(close * 0.00703)`: Bollinger Band width must exceed 0.703% of close — indicating sufficient volatility room
- `closedelta.gt(close * 0.01476)`: Price must have obvious fluctuation, exceeding 1.476%
- `tail.lt(bbdelta * 0.03632)`: Lower wick must be very short — price bounced quickly after touching the low, with minimal selling pressure
- `close.lt(lower.shift())`: Close must be below the previous period's BB lower band — a clear oversold signal
- `close.le(close.shift())`: Current close cannot be higher than previous close — ensuring price is in a downtrend

### 3.2 Condition #2: ClucMay72018 Strategy Low-Volume Breakout Signal

This uses ClucMay72018's core logic to capture opportunities in low-volume environments:

```python
# ClucMay72018 Buy Conditions
(dataframe['close'] < dataframe['ema_slow']) &
(dataframe['close'] < 0.98863 * dataframe['bb_lowerband']) &
(dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 34))
```

**Logic Analysis**:
- `close < ema_slow`: Price must be below the 50-period EMA, confirming overall downtrend
- `close < 0.98863 * bb_lowerband`: Price must be below the Bollinger lower band by about 1.14% — an extreme oversold signal
- `volume < volume_mean_slow.shift(1) * 34`: Volume must be extremely contracted, less than 1/34th of the 30-period average. This stringent condition ensures entry when liquidity dries up

### 3.3 Comparison of Two Buy Conditions

| Comparison Dimension | BinHV45 Condition | ClucMay72018 Condition |
|---------------------|-------------------|------------------------|
| **Source** | BinHV45 | ClucMay72018 |
| **Core Logic** | Bollinger Band rebound | Low-volume oversold |
| **Bollinger Band Period** | 40 periods | 20 periods |
| **Trend Judgment** | Local downtrend | 50 EMA-confirmed downtrend |
| **Volume Requirement** | None | Extreme contraction (< 1/34th avg) |
| **Signal Feature** | Captures rapid rebounds after sharp drops | Waits for volume exhaustion before reversal |

---

## IV. Exit Conditions Details

### 4.1 Basic Sell Signal

```python
# Sell Condition
dataframe.loc[
    (dataframe['close'] > dataframe['bb_middleband']),
    'sell'
] = 1
```

**Logic Analysis**: Sell triggers when close price breaks above Bollinger middle band (20-period moving average). This is a simple trend reversal signal.

### 4.2 Trailing Stop Mechanism

```python
trailing_stop = True
trailing_stop_positive = 0.0198        # 1.98% profit activates tracking
trailing_stop_positive_offset = 0.03082  # 3.082% offset trigger point
trailing_only_offset_is_reached = True   # Only activates after offset reached
```

### 4.3 Exit Mechanism Coordination

| Exit Method | Trigger Condition | Priority |
|-------------|-------------------|----------|
| **ROI Exit** | Profit >= 1.5% | Highest |
| **Trailing Stop** | Profit >= 3.082%, then retreats 1.98% | Medium |
| **Sell Signal** | Price breaks Bollinger middle band | Low (if exit_profit_only=True) |

---

## V. Technical Indicator System

### 5.1 BinHV45 Strategy Indicators

| Indicator Name | Calculation | Purpose |
|---------------|-------------|---------|
| `lower` | Bollinger Band 40-period lower band | Oversold boundary |
| `bbdelta` | Absolute value of mid-lower band difference | Bollinger Band width |
| `closedelta` | Absolute value of close price change | Price fluctuation magnitude |
| `tail` | Absolute value of close-low difference (lower wick) | Reversal strength |

### 5.2 ClucMay72018 Strategy Indicators

| Indicator Name | Calculation | Purpose |
|---------------|-------------|---------|
| `bb_lowerband` | Bollinger Band 20-period lower band | Oversold boundary |
| `bb_middleband` | Bollinger Band 20-period middle band | Sell judgment |
| `ema_slow` | 50-period exponential moving average | Trend judgment |
| `volume_mean_slow` | 30-period volume moving average | Volume filtering |

---

## VI. Risk Management Features

### 6.1 Generous Hard Stop-Loss Design

Hard stop-loss at -6.58% is quite generous for a 1-minute timeframe. The philosophy:
- 1-minute price fluctuations are frequent; too tight a stop-loss gets frequently triggered
- Generous stop-loss gives price sufficient room, avoiding being "noised out"
- Combined with ROI exit (1.5%), the strategy effectively uses an asymmetric risk-reward ratio

### 6.2 Dual Take-Profit Protection

- **ROI (1.5%)**: Ensures profits are locked in regardless of market fluctuation
- **Trailing Stop (1.98%)**: Lets profits run in trending markets while locking in partial gains

---

## VII. Strategy Pros & Cons

### Advantages

1. **Dual-Strategy Complementarity**: Combines two different logics, adapting to multiple market environments
2. **High-Frequency Trading**: 1-minute timeframe captures finest price fluctuations, high capital utilization
3. **Strict Volume Filtering**: ClucMay72018 condition requires extreme volume contraction, reducing false breakouts
4. **Multi-Layer Protection**: ROI + trailing stop + hard stop-loss — triple protection

### Limitations

1. **High Trading Costs**: 1-minute timeframe generates numerous trades; fees significantly erode profits
2. **Slippage Risk**: Limit orders in high-frequency scenarios may fail to fill
3. **Overfitting Risk**: Strategy contains multiple magic numbers that may overfit historical data
4. **Unsuitable for Trending Markets**: Mean-reversion design may underperform during strong trends
5. **Data Latency**: 1-minute data may be affected by exchange data latency

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Low-Volatility Consolidation** | Default config | Strategy best suited for consolidation; rebound logic effective |
| **High-Volatility Markets** | Increase take-profit threshold | Let profits run when volatility increases |
| **Trending Up** | Reduce position size | Strategy logic may conflict with trend direction |
| **Trending Down** | Use with caution | May be a pause in downtrend rather than rebound |

---

## IX. Live Trading Notes

**Combined_Indicators** is a typical **mean-reversion strategy** whose core assumption is that prices fluctuate around the Bollinger Band midline in the short term — oversold prices rebound, overbought prices pull back.

### 9.1 Core Strategy Logic

- **Bollinger Band 40-period (BinHV45)**: Captures rapid rebound opportunities, sensitive parameters for short-term trading
- **Bollinger Band 20-period (ClucMay72018)**: Captures low-volume reversal opportunities, more stringent parameters
- **Volume Filtering**: Requires extreme volume contraction to filter "false breakouts"

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| Trending Up | ⭐⭐☆☆☆ | Strategy logic conflicts with trend; may be outperformed |
| Trending Down | ⭐⭐⭐☆☆ | Short-term rebounds possible, but overall risk higher in downtrend |
| Consolidation | ⭐⭐⭐⭐⭐ | Most suitable environment; mean-reversion logic effective |
| Fast Fluctuation | ⭐⭐⭐☆☆ | Frequent signals but more noise; needs additional filtering |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Notes |
|--------------|-------------------|-------|
| `max_open_trades` | 1-2 | High-frequency strategy shouldn't open too many positions |
| `stake_amount` | Moderate | Based on total capital; recommended not exceeding 10% |
| `dry_run` | Test first | Must test in paper trading first |

---

## X. Summary

**Combined_Indicators** fuses two classic Bollinger Band strategies. Its core value lies in:

1. **Dual-Strategy Verification**: Either of two independent buy conditions can trigger entry, reducing single-strategy failure risk
2. **High-Frequency Trading**: 1-minute timeframe quickly captures small profit opportunities
3. **Strict Volume Filtering**: ClucMay72018 condition requires extreme volume contraction, reducing false signals

However, the strategy has clear limitations:
1. **High Trading Costs**: High-frequency trading causes severe fee accumulation
2. **Non-Transparent Parameters**: Multiple magic numbers' optimization logic is unclear
3. **Unsuitable for Trending Markets**: Mean-reversion logic may fail in trending markets

For quantitative traders: test thoroughly in paper trading first, closely monitor trading costs, consider adding extra filtering conditions, and do not blindly pursue high returns — the core of high-frequency strategies is stability, not profitability.

---

*This document is written based on Combined_Indicators strategy code v1.0 analysis.*
