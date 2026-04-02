# Quickie Strategy In-Depth Analysis

> **Strategy Number**: #339 (339th of 465 strategies)  
> **Strategy Type**: Momentum Quick Trading Strategy  
> **Timeframe**: 5 minutes (5m)

---

## I. Strategy Overview

Quickie is a momentum-based quick trading strategy developed by Gert Wohlgemuth. Its core philosophy is fast position closure and avoiding excessive losses, hence the name "Quickie". The strategy employs moderate stop-loss settings to control risk while capturing momentum.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 buy signal, based on ADX trend strength + TEMA momentum + Bollinger Band position |
| **Sell Condition** | 1 sell signal, based on ADX extreme + TEMA reversal + Bollinger Band breakout |
| **Protection Mechanism** | Fixed stop-loss at -25%, tiered ROI profit-taking |
| **Timeframe** | 5 minutes |
| **Dependencies** | talib, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "100": 0.01,  # Exit with 1% profit after 100 minutes
    "30": 0.03,   # Exit with 3% profit after 30 minutes
    "15": 0.06,   # Exit with 6% profit after 15 minutes
    "10": 0.15,   # Exit with 15% profit after 10 minutes
}

# Stop-loss setting
stoploss = -0.25  # 25% fixed stop-loss
```

**Design Rationale**:
- ROI uses a **reverse-tiered design**: shorter holding periods target higher profits; longer periods target lower profits
- This design encourages quick profit-taking, aligning with the "Quickie" philosophy
- Stop-loss is relatively wide (-25%), giving prices sufficient room to fluctuate

### 2.2 Order Type Configuration

The strategy does not explicitly configure `order_types`, using default settings:
- Buy/Sell are limit orders
- Stop-loss is a market order

---

## III. Buy Condition Details

### 3.1 Single Buy Condition

Quickie has only one buy signal but combines four independent filter conditions:

```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (dataframe['adx'] > 30) &
            (dataframe['tema'] < dataframe['bb_middleband']) &
            (dataframe['tema'] > dataframe['tema'].shift(1)) &
            (dataframe['sma_200'] > dataframe['close'])
        ),
        'buy'] = 1
    return dataframe
```

**Condition Analysis**:

| Condition | Logic | Meaning |
|-----------|-------|---------|
| ADX > 30 | Trend strength filter | Market has a clear trend (ADX > 25 indicates trend) |
| TEMA < BB_middleband | Position filter | Price is below Bollinger middle band (relatively low position) |
| TEMA > TEMA.shift(1) | Momentum confirmation | TEMA starts rising (short-term momentum turns positive) |
| SMA_200 > close | Long-term trend filter | Close price below 200-day SMA (looking for bounces in downtrend) |

**Buy Logic Summary**:
In a strong trend market (ADX > 30), when price is below the Bollinger middle band and starts to rebound (TEMA rising), while price is below the 200-day SMA, a buy signal is triggered. This is a **counter-trend buy strategy**—seeking short-term rebound opportunities within a long-term downtrend.

---

## IV. Sell Logic Details

### 4.1 Sell Signal

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (dataframe['adx'] > 70) &
            (dataframe['tema'] > dataframe['bb_middleband']) &
            (dataframe['tema'] < dataframe['tema'].shift(1))
        ),
        'sell'] = 1
    return dataframe
```

**Condition Analysis**:

| Condition | Logic | Meaning |
|-----------|-------|---------|
| ADX > 70 | Trend extreme filter | Trend strength reaches extreme level (possibly overbought) |
| TEMA > BB_middleband | Position filter | Price is above Bollinger middle band (relatively high position) |
| TEMA < TEMA.shift(1) | Momentum confirmation | TEMA starts declining (short-term momentum turns negative) |

**Sell Logic Summary**:
When trend strength reaches an extreme (ADX > 70), price is above the Bollinger middle band and starts to pull back (TEMA declining), a sell signal is triggered. This is a **momentum reversal exit strategy**—taking profits quickly when momentum peaks.

### 4.2 Multi-tier Profit-taking System

The strategy implements tiered profit-taking through the ROI table:

| Holding Time | Target Profit | Trigger Scenario |
|--------------|---------------|------------------|
| 10 minutes | 15% | Quick rally, immediate profit-taking |
| 15 minutes | 6% | Moderate gain, partial profit-taking |
| 30 minutes | 3% | Steady rise, conservative profit-taking |
| 100 minutes | 1% | Extended holding, minimal profit exit |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|-------------------|---------------------|---------|
| Trend Strength | ADX (Average Directional Index) | Determine trend existence and strength |
| Momentum Indicator | TEMA (Triple Exponential Moving Average) | Smooth price changes, capture short-term momentum |
| Trend Indicator | SMA (Simple Moving Average) | 200-day SMA to judge long-term trend |
| Volatility Indicator | Bollinger Bands (20, 2) | Determine relative price position |

### 5.2 Indicator Parameters

```python
# MACD (for plotting, not trading signals)
macd = ta.MACD(dataframe)
dataframe['macd'] = macd['macd']
dataframe['macdsignal'] = macd['macdsignal']
dataframe['macdhist'] = macd['macdhist']

# TEMA (Triple Exponential Moving Average)
dataframe['tema'] = ta.TEMA(dataframe, timeperiod=9)

# SMA (Simple Moving Average)
dataframe['sma_200'] = ta.SMA(dataframe, timeperiod=200)
dataframe['sma_50'] = ta.SMA(dataframe, timeperiod=200)  # Note: This is a code error

# ADX (Average Directional Index)
dataframe['adx'] = ta.ADX(dataframe)

# Bollinger Bands (20-period, 2 standard deviations)
bollinger = qtpylib.bollinger_bands(dataframe['close'], window=20, stds=2)
```

**Code Note**: The strategy calculates `sma_50` using `timeperiod=200`, which is a code error—`sma_50` and `sma_200` are actually the same value. However, `sma_50` is not used in the trading logic, so it doesn't affect strategy operation.

---

## VI. Risk Management Features

### 6.1 Tiered ROI Profit-taking

Quickie uses a **time-profit dual-dimension** profit-taking mechanism:

- **Quick profit-taking priority**: Exit immediately at 15% profit within 10 minutes
- **Time penalty mechanism**: Longer holding periods result in lower profit targets
- **Maximum holding limit**: Even with only 1% profit, exit after 100 minutes

### 6.2 Fixed Stop-loss

```python
stoploss = -0.25  # 25% fixed stop-loss
```

Characteristics:
- Relatively wide stop-loss (-25%), suitable for volatile cryptocurrency markets
- No trailing stop-loss, executed when price triggers
- Gives price sufficient "breathing room"

### 6.3 No Trailing Stop

The strategy does not enable trailing stop (`trailing_stop`), which contrasts with the "Quickie" name—quick buy signals, but relatively conservative profit-taking/stop-loss.

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Simple Logic**: Only one buy and one sell signal each, clear conditions, easy to understand and debug
2. **Trend Confirmation**: Uses ADX to ensure trading only in clear trends, avoiding false signals in ranging markets
3. **Quick Profit-taking**: Tiered ROI design encourages quick profits, aligning with short-term trading philosophy
4. **Multi-dimensional Filtering**: Combines trend strength, momentum, and relative position for higher signal quality

### ⚠️ Limitations

1. **Wide Stop-loss**: -25% stop-loss may be too wide for conservative traders
2. **No Trailing Stop**: Cannot lock in floating profits, may lose gains during significant pullbacks
3. **Counter-trend Buy Risk**: Buying in long-term downtrend carries "catching a falling knife" risk
4. **ADX Extreme Judgment**: ADX > 70 as sell condition may exit too early in strong trends

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| Strong Trend Market | Default configuration | ADX filter ensures trading only in trends |
| High Volatility Market | Tighten stop-loss appropriately | Default -25% may be too wide |
| Ranging Market | Not recommended | ADX > 30 condition may trigger frequently with poor signal quality |
| Early Bull Market | Raise ROI targets appropriately | Quick profit-taking may miss large moves |

---

## IX. Applicable Market Environment Details

Quickie is a **trend-following short-term strategy**. Based on its code architecture, it performs best in **moderately strong trend markets**, while performing poorly in extreme conditions.

### 9.1 Strategy Core Logic

- **Trend Filter**: ADX > 30 ensures entry only when there's a clear trend
- **Momentum Confirmation**: Rising TEMA confirms positive short-term momentum
- **Position Judgment**: Buy below Bollinger middle band, sell above
- **Long-term Trend Hedge**: Requires price below 200-day SMA (counter-trend buy)

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|-------------|-------------------|-----------------|
| 📈 Moderate Uptrend | ⭐⭐⭐⭐⭐ | ADX > 30 with rising price, perfect match for buy conditions |
| 🔄 Range-bound Consolidation | ⭐⭐☆☆☆ | ADX difficult to sustain > 30, few signals |
| 📉 Downtrend | ⭐⭐⭐☆☆ | Meets SMA_200 > close condition, but bounces may be weak |
| ⚡️ Extreme Volatility | ⭐⭐☆☆☆ | ADX > 70 sell may exit too early, missing continued gains |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| Timeframe | 5m (default) | Strategy designed for short-term, not recommended to change |
| Stop-loss | -0.15 ~ -0.20 | Can tighten based on risk preference |
| ADX Entry Threshold | 25~30 | Lowering threshold can increase signal quantity |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

Quickie has simple logic, suitable for beginners to learn and understand:
- Only one buy signal and one sell signal
- Moderate number of indicators (4 core indicators)
- Clear logical relationships (AND condition combinations)

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |
| 50+ pairs | 8GB | 16GB |

The strategy has low computational requirements and doesn't demand high hardware specs.

### 10.3 Backtesting vs Live Trading Differences

- **Backtesting Advantage**: Tiered ROI performs well in backtests
- **Live Trading Risk**: Quick profit-taking may miss large moves
- **Slippage Impact**: Relatively minor at 5-minute timeframe

### 10.4 Manual Trading Recommendations

If manually using this strategy's logic:
1. Wait for ADX to break above 30 (confirm trend)
2. Watch when price is below Bollinger middle band
3. Enter when TEMA starts rising
4. Set 15% profit target and 25% stop-loss
5. Exit if 15% is reached within 10 minutes

---

## XI. Summary

**Quickie** is a **concise and efficient momentum short-term strategy**. Its core value lies in:

1. **Clear Logic**: One buy/one sell signal each, four filter conditions, easy to understand and verify
2. **Quick Profit-taking**: Tiered ROI design encourages quick profits, avoiding drawdowns
3. **Trend Filtering**: ADX ensures trading only in trends, reducing false signals

For quantitative traders, this is a **base strategy suitable for learning and modification**. You can add trailing stops, optimize stop-loss ratios, or add more filter conditions on this foundation.

---