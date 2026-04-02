# CCIStrategy Strategy In-Depth Analysis

> **Strategy ID**: #81 (81st of 465 strategies)
> **Strategy Type**: CCI Oversold/Overbought + Money Flow Confirmation + Trend Filter
> **Timeframe**: 1 Minute (1m)

---

## I. Strategy Overview

**CCIStrategy** is a trading strategy based on the Commodity Channel Index (CCI), incorporating money flow indicators and a trend filtering mechanism. The core logic is clear: use CCI to identify extreme oversold and overbought price levels, confirm capital flow direction with CMF (Chaikin Money Flow) and MFI (Money Flow Index), and finally filter out false signals through a multi-timeframe moving average system.

### Key Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 6 conditions combined: Dual CCI Oversold + Negative CMF + Oversold MFI + Trend Confirmation |
| **Sell Conditions** | 5 conditions combined: Dual CCI Overbought + Positive CMF + Downtrend Confirmation |
| **Protection** | No independent protection parameters; relies on hard stop-loss |
| **Timeframe** | Main: 1m + Informative: 5m (resampled 5x) |
| **Dependencies** | TA-Lib, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.1      # Immediate exit: 10% profit
}

# Stop-Loss Setting
stoploss = -0.02  # -2% hard stop-loss
```

**Design Philosophy**:
- **Low ROI Threshold**: Initial ROI set at 10%, indicating the strategy pursues quick, small profits
- **Tight Stop-Loss**: -2% hard stop-loss is relatively strict; combined with CCI's extreme signals, it enables quick exits
- **No Trailing Stop**: The strategy does not use trailing stop; relies on technical signals and ROI exit

### 2.2 Order Type Configuration

Uses Freqtrade default configuration (not explicitly defined in the strategy).

---

## III. Entry Conditions Details

### 3.1 Complete Buy Logic Analysis

```python
dataframe.loc[
    (
        # Condition 1: Long-term CCI Oversold
        (dataframe['cci_one'] < -100)
        # Condition 2: Short-term CCI Oversold
        & (dataframe['cci_two'] < -100)
        # Condition 3: Money flow is negative
        & (dataframe['cmf'] < -0.1)
        # Condition 4: Money Flow Index oversold
        & (dataframe['mfi'] < 25)

        # Condition 5: Mid-term trend is upward
        & (dataframe['resample_medium'] > dataframe['resample_short'])
        # Condition 6: Long-term moving average is below price
        & (dataframe['resample_long'] < dataframe['close'])
    ),
    'buy'] = 1
```

**Logic Analysis**:

1. **Dual CCI Confirmation**:
   - `cci_one` (170 periods) captures long-term oversold signals
   - `cci_two` (34 periods) captures short-term oversold signals
   - Both below -100 simultaneously indicates price is in extreme oversold territory

2. **Money Flow Confirmation**:
   - `CMF < -0.1`: Chaikin Money Flow is negative; capital is flowing out of the market
   - `MFI < 25`: Money Flow Index is at extremely low levels (traditional oversold line is 20)

3. **Trend Filter**:
   - `resample_medium > resample_short`: 50-day MA > 25-day MA, confirming mid-term uptrend
   - `resample_long < close`: 200-day MA is below price, confirming long-term upward trend

### 3.2 Indicator Calculations

```python
# CCI Calculation (two periods)
dataframe['cci_one'] = ta.CCI(dataframe, timeperiod=170)   # Long-term CCI
dataframe['cci_two'] = ta.CCI(dataframe, timeperiod=34)    # Short-term CCI

# RSI Calculation
dataframe['rsi'] = ta.RSI(dataframe)

# MFI Calculation
dataframe['mfi'] = ta.MFI(dataframe)

# Chaikin Money Flow Calculation
dataframe['cmf'] = self.chaikin_mf(dataframe)

# Bollinger Bands (for charting)
bollinger = qtpylib.bollinger_bands(dataframe['close'], window=20, stds=2)
dataframe['bb_lowerband'] = bollinger['lower']
dataframe['bb_upperband'] = bollinger['upper']
dataframe['bb_middleband'] = bollinger['mid']
```

---

## IV. Exit Logic Details

### 4.1 Sell Conditions

```python
dataframe.loc[
    (
        # Condition 1: Long-term CCI Overbought
        (dataframe['cci_one'] > 100)
        # Condition 2: Short-term CCI Overbought
        & (dataframe['cci_two'] > 100)
        # Condition 3: Money flow is positive
        & (dataframe['cmf'] > 0.3)
        # Conditions 4-5: Moving averages in bearish alignment (downtrend)
        & (dataframe['resample_sma'] < dataframe['resample_medium'])
        & (dataframe['resample_medium'] < dataframe['resample_short'])
    ),
    'sell'] = 1
```

**Logic Analysis**:

1. **Dual CCI Overbought**:
   - `cci_one > 100` and `cci_two > 100` both satisfied, confirming price is in extreme overbought territory

2. **Positive Money Flow**:
   - `CMF > 0.3`: Capital is flowing into the market but has reached a short-term peak

3. **Trend Reversal Confirmation**:
   - Moving averages in bearish alignment: `resample_sma < resample_medium < resample_short`
   - This indicates short-term, mid-term, and long-term trends are all downward

### 4.2 ROI Exit

| Holding Time | Minimum Profit Rate | Triggers Exit |
|-------------|---------------------|---------------|
| 0 minutes | 10% | Exit immediately when reached |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameter | Purpose |
|-------------------|-------------------|-----------|---------|
| **Trend Indicator** | CCI | 170 periods | Long-term oversold/overbought |
| **Trend Indicator** | CCI | 34 periods | Short-term oversold/overbought |
| **Momentum Indicator** | RSI | Default 14 periods | Momentum confirmation |
| **Money Flow Indicator** | MFI | Default 14 periods | Money flow oversold |
| **Money Flow Indicator** | CMF | 20 periods | Chaikin Money Flow direction |
| **Volatility Indicator** | Bollinger Bands | 20, 2 | Price boundaries (charting only) |

### 5.2 Resampled Indicators (Informative Timeframe 5m)

The strategy resamples 1m data by 5x (5m) and calculates multiple moving averages for trend filtering:

| Moving Average | Period | Purpose |
|---------------|--------|---------|
| resample_sma | 100 | Long-term trend |
| resample_medium | 50 | Mid-term trend |
| resample_short | 25 | Short-term trend |
| resample_long | 200 | Long-term support/resistance |

---

## VI. Risk Management Features

### 6.1 Hard Stop-Loss Mechanism

```python
stoploss = -0.02  # -2% hard stop-loss
```

- **2% Stop-Loss**: Relatively tight; combined with CCI's extreme value signals, enables quick exits on trend reversals
- **No Time Stop-Loss**: Strategy has no holding time limit

### 6.2 ROI Exit Mechanism

- **Single ROI Tier**: Initial ROI 10%, exit immediately when reached
- **Design Philosophy**: Pursues high-frequency, small profits; suitable for ranging markets

### 6.3 Risk Alerts

- **High Trading Frequency**: 1m timeframe has high trading frequency; be mindful of fee erosion
- **No Trailing Stop**: Relies on technical signals and fixed ROI; may miss major trends

---

## VII. Strategy Pros & Cons

### Advantages

1. **Multi-Indicator Confirmation**: Uses dual CCI + money flow + trend filtering; lower probability of false signals
2. **Fast Response**: 1m timeframe captures short-term opportunities
3. **Effective Trend Filtering**: Resampled moving average system filters counter-trend trades
4. **Clear Logic**: Buy and sell conditions are symmetric; easy to understand and execute

### Limitations

1. **High Trading Frequency**: 1m timeframe may generate large number of trades; high fee cost
2. **Parameter Sensitive**: CCI thresholds (±100) and CMF thresholds have significant impact on results
3. **Average Performance in Trending Markets**: Moving average trend confirmation works better in ranging markets
4. **No Independent Protection**: Lacks anti-slippage protection parameters

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|---------------------------|-------|
| **Ranging Market** | Default parameters | CCI oversold/overbought works best in ranging markets |
| **Volatile Market** | Adjust CCI thresholds | CCI signals more reliable during extreme volatility |
| **Low Volatility Market** | Not recommended | 1m framework has sparse signals in low volatility |
| **Trending Market** | Use with caution | Trend confirmation may lag |

---

## IX. Applicable Market Environment Details

### 9.1 Core Strategy Logic

CCIStrategy is a **trend-filtered mean reversion strategy**, with core logic at two levels:

1. **Mean Reversion Layer**: Uses CCI to identify extreme price deviations (buy on oversold, sell on overbought)
2. **Trend Filter Layer**: Uses resampled moving averages to confirm current trend direction; avoids counter-trend trades

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Uptrend | Three Stars | Moving average trend confirmation misses some gains; mean reversion signals may fight the trend |
| Downtrend | Three Stars | Moving average confirms downtrend; buy signals filtered, sell signals effective |
| Ranging Market | Four Stars | CCI oversold/overbought works best in ranging markets; mean reversion logic fully发挥作用 |
| Extreme Volatility | Four Stars | CCI is sensitive to extreme price movements; money flow indicators confirm momentum |

### 9.3 Key Configuration Suggestions

| Configuration | Suggested Value | Notes |
|---------------|-----------------|-------|
| Trading Pairs | High-liquidity coins | 1m framework needs good depth and low slippage |
| Trading Fees | < 0.1% | High-frequency strategies need low-fee environment |
| ROI | 5%-15% | Adjust based on market volatility |
| Stop-Loss | -2% or -3% | Set according to risk preference |

---

## X. Important Notes: The Cost of Complexity

### 10.1 Learning Curve

- **Indicator Understanding**: Need to understand CCI, CMF, MFI indicators
- **Parameter Tuning**: 170/34 period CCI and other parameters need adjustment per market
- **Resample Mechanism**: Need to understand how the resample function works

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|----------------|
| 5-10 pairs | 1 GB | 2 GB |
| 20-30 pairs | 2 GB | 4 GB |

### 10.3 Backtesting vs Live Trading Differences

- **Slippage Impact**: 1m framework is sensitive to slippage; live performance may be weaker than backtesting
- **Signal Delay**: Resample mechanism may introduce additional delay
- **Liquidity Risk**: High-frequency trading requires sufficient order book depth

### 10.4 Manual Trading Suggestions

1. Monitor both CCI periods reaching threshold (±100) simultaneously
2. Confirm MFI < 25 or CMF direction aligns with CCI
3. Check resampled moving average alignment
4. Avoid trading around news events

---

## XI. Summary

**CCIStrategy** is a **trend-filtered CCI mean reversion strategy**, with core value in:

1. **Multi-Period CCI Confirmation**: Uses 170 and 34 periods simultaneously, balancing long-term trends and short-term volatility
2. **Money Flow Validation**: Confirms capital flow direction through CMF and MFI; improves signal reliability
3. **Trend Filter Mechanism**: Uses resampled moving averages to avoid counter-trend trades
4. **Simple Profit Taking**: 10% ROI target + 2% stop-loss; pursues steady small profits

For quantitative traders, CCIStrategy is suitable for those pursuing **high-frequency, small-profit** trades, but need to pay attention to:
- Fee erosion on profits
- Market environment impact on CCI signal effectiveness
- 1m framework slippage risk

It is recommended to conduct sufficient testing on a paper trading account before live trading.
