# BBRSIoriginal Strategy In-Depth Analysis

> **Strategy ID**: #436 (436th of 465 strategies)  
> **Strategy Type**: Bollinger Band Oversold Reversal + RSI Momentum Confirmation  
> **Timeframe**: 1 hour (1h)

---

## I. Strategy Overview

BBRSIoriginal is one of the default strategies provided by Freqtrade officially, representing the most basic and classic Bollinger Band + RSI combination strategy. It uses extreme Bollinger Band breakthroughs as buy signals, with RSI overbought as sell confirmation, representing the standard paradigm for technical analysis entry-level strategies. The code is concise and clear, highly suitable for beginners to learn and understand the basic architecture of quantitative trading strategies.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 core buy signal (price breaks below 3-standard deviation Bollinger Band lower band) |
| **Sell Conditions** | 2-condition combined sell (RSI > 75 and price above Bollinger Band middle band) |
| **Protection Mechanism** | No independent protection mechanism configured, relies on basic stop loss and ROI |
| **Timeframe** | 1 hour (1h) |
| **Dependencies** | talib, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table (tiered exit)
minimal_roi = {
    "0": 0.09638,    # Immediately: 9.638%
    "19": 0.03643,   # After 19 minutes: 3.643%
    "69": 0.01923,   # After 69 minutes: 1.923%
    "120": 0         # After 120 minutes: sell at any profit
}

# Stop loss setting
stoploss = -0.36828  # 36.828% stop loss

# No trailing stop configuration
```

**Design Rationale**:
- ROI uses tiered exit mechanism, decreasing profit requirements over time
- Stop loss value -36.828% is very loose, indicating strategy tolerates large drawdowns
- No trailing stop, relies on fixed ROI and sell signals

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',           # Limit order buy
    'sell': 'limit',          # Limit order sell
    'stoploss': 'limit',      # Limit order stop loss
    'stoploss_on_exchange': False  # Stop loss not executed on exchange
}

order_time_in_force = {
    'buy': 'gtc',   # Good Till Cancel
    'sell': 'gtc',  # Good Till Cancel
}
```

**Design Rationale**:
- All limit orders used, ensuring controllable execution prices
- GTC orders don't expire until filled or manually cancelled
- Stop loss executed locally by Freqtrade, not dependent on exchange stop loss functionality

---

## III. Buy Conditions Detailed Analysis

### 3.1 Core Buy Logic

The strategy employs extremely simple buy logic:

```python
dataframe.loc[
    (
        (dataframe["close"] < dataframe['bb_lowerband3'])
    ),
    'buy'] = 1
```

**Translation**: When closing price falls below the 3-standard deviation Bollinger Band lower band, a buy signal is triggered.

### 3.2 Indicator Calculation Details

#### Dual Bollinger Band System

The strategy simultaneously calculates two sets of Bollinger Bands:

```python
# 4-standard deviation Bollinger Bands (not used in buy)
bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=4)
dataframe['bb_lowerband'] = bollinger['lower']
dataframe['bb_middleband'] = bollinger['mid']
dataframe['bb_upperband'] = bollinger['upper']

# 3-standard deviation Bollinger Bands (used in buy)
bollinger3 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
dataframe['bb_lowerband3'] = bollinger3['lower']
dataframe['bb_middleband3'] = bollinger3['mid']
dataframe['bb_upperband3'] = bollinger3['upper']
```

**Technical Details**:
- Uses Typical Price (Typical Price = (High + Low + Close) / 3) rather than just closing price
- 20-period is the standard Bollinger Band configuration
- 3-standard deviation is an extreme parameter, meaning price is at a statistically "abnormally low" position

### 3.3 Buy Signal Analysis

| Condition | Technical Meaning | Statistical Significance |
|-----------|------------------|--------------------------|
| close < bb_lowerband3 | Price breaks below Bollinger Band lower band | Price is outside 99.7% confidence interval |

**Signal Characteristics**:
- **Extreme Oversold**: 3-standard deviation is an extreme condition, statistically occurring < 0.3%
- **Counter-trend Entry**: Buying when price crashes, expecting mean reversion
- **No Volume Filter**: Doesn't check volume, purely price-driven

**Potential Risks**:
- Price breaking below 3-standard deviation may be "catching falling knives"
- No trend filter, may buy multiple times in downtrends
- Sparse signals, only triggered during extreme market conditions

---

## IV. Sell Logic Detailed Analysis

### 4.1 Sell Signal Architecture

The strategy employs a dual-condition combined sell:

```python
dataframe.loc[
    (
        (dataframe['rsi'] > 75) &
        (dataframe["close"] > dataframe['bb_middleband'])
    ),
    'sell'] = 1
```

**Translation**: When RSI > 75 and price is above Bollinger Band middle band, a sell signal is triggered.

### 4.2 Sell Condition Analysis

| Condition | Technical Meaning | Description |
|-----------|------------------|-------------|
| RSI > 75 | RSI overbought | Momentum reaches extreme high |
| close > bb_middleband | Price returns above middle band | Mean reversion complete |

**Signal Characteristics**:
- **Dual Confirmation**: Requires both RSI and price conditions to be met
- **RSI Threshold Aggressive**: 75 rather than traditional 70, waiting for more extreme overbought
- **Bollinger Band Middle Band**: Price returning to middle band indicates bounce has occurred

### 4.3 Sell Logic Summary

**Complete Entry to Exit Path**:
1. Price crashes through 3-standard deviation Bollinger Band lower band → Buy
2. Price bounces back above Bollinger Band middle band → First condition met
3. RSI simultaneously reaches above 75 → Second condition met
4. Both conditions met → Sell

**Typical Holding Period**:
- Based on tiered ROI configuration, maximum 120 minutes (2 hours) forced exit
- Normally, waiting for RSI overbought confirmation may hold for hours to days

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameters | Purpose |
|-------------------|---------------------|------------|---------|
| Volatility Indicator | Bollinger Bands (4x) | 20-period, 4x standard deviation | Calculated (unused) |
| Volatility Indicator | Bollinger Bands (3x) | 20-period, 3x standard deviation | Buy signal |
| Momentum Indicator | RSI | Default period (14) | Sell confirmation |

### 5.2 Typical Price

The strategy uses typical price to calculate Bollinger Bands:

```python
typical_price = (High + Low + Close) / 3
```

**Advantages**:
- Better represents the true price level of the candle than closing price alone
- Takes into account the range of high and low points
- Smoother, reduces noise

### 5.3 Indicator Relationship Diagram

```
Buy Signal Chain:
Price drops → close < bb_lowerband3 → Trigger buy

Sell Signal Chain:
Price bounces → close > bb_middleband
            + RSI > 75
            → Trigger sell
```

---

## VI. Risk Management Features

### 6.1 Tiered ROI Exit Mechanism

The strategy uses time-decreasing ROI table:

| Time Point | Minimum Return Rate | Description |
|-----------|--------------------|-------------|
| 0 minutes | 9.638% | High return expected at open |
| 19 minutes | 3.643% | Lower expectation after 19 min |
| 69 minutes | 1.923% | Further lowered after 1 hour |
| 120 minutes | 0% | Sell at any profit after 2 hours |

**Design Logic**:
- Expects high returns at open, unwilling to take profit easily
- Gradually lowers return expectations over time
- Forced exit after 2 hours, avoiding capital occupation

### 6.2 Loose Stop Loss Design

```python
stoploss = -0.36828  # 36.828%
```

**Analysis**:
- 36.828% is a very loose stop loss
- Allows price to draw down deeply
- Indicates strategy designer believes in reliability of Bollinger Band oversold signals
- Also implies: may endure multiple large floating losses

### 6.3 No Protection Mechanism

The strategy doesn't configure protections, meaning:
- No consecutive loss protection
- No single coin protection
- Completely relies on stop loss and ROI

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Extremely Simple Architecture**: Less than 100 lines of code, beginner-friendly, easy to understand and modify.

2. **Classic Combination**: Bollinger Band + RSI is a classic technical analysis combination, with clear principles and unambiguous signals.

3. **Reliable Extreme Signals**: 3-standard deviation Bollinger Band lower band is a statistically extreme position, high signal quality.

4. **Mean Reversion Logic**: Buying at extreme oversold, waiting for reversion to middle band, fits "buy low sell high" intuition.

5. **1-Hour Timeframe Comfortable**: Not too tiring (like 5-minute), not too slow (like daily), friendly for part-time traders.

### ⚠️ Limitations

1. **No Trend Filter**: May repeatedly "catch falling knives" in downtrends, leading to consecutive losses.

2. **Stop Loss Too Loose**: 36% stop loss is unacceptable for most traders.

3. **Sparse Signals**: 3-standard deviation Bollinger Band breakouts are extreme events, may have no trades for long periods.

4. **Strict Sell Conditions**: RSI > 75 and price back to middle band, may miss some profit opportunities.

5. **4x Bollinger Band Unused**: Code calculates but doesn't use it, possibly a design artifact.

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Range Bounce Market | Use default parameters | Mean reversion strategy performs best in ranging markets |
| Sustained Downtrend | Turn off or significantly adjust stop loss | Will frequently trigger buys but hard to get sells |
| Strong Uptrend | Not applicable | Price rarely breaks below Bollinger Band lower band |
| High Volatility | Applicable | High volatility needed to trigger Bollinger Band breakouts |

---

## IX. Applicable Market Environment Details

BBRSIoriginal is Freqtrade's official default strategy, representing the **most basic Bollinger Band + RSI combination**. It performs best in **range bounce markets**, while performing poorly in **trending markets**.

### 9.1 Strategy Core Logic

- **Counter-trend Entry**: Price breaks below Bollinger Band lower band, considered "oversold", expecting bounce
- **Trend-following Exit**: Price returns to middle band and RSI overbought, confirms bounce is over
- **Mean Reversion**: Relies on statistical principle of price oscillating around Bollinger Band middle band

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:-------------------|:---------|
| 📈 Strong Uptrend | ⭐☆☆☆☆ | Price rarely breaks below Bollinger Band lower band, almost no signals |
| 🔄 Range Bounce | ⭐⭐⭐⭐⭐ | Perfectly matches strategy logic, buy low sell high cycle |
| 📉 Sustained Downtrend | ⭐⭐☆☆☆ | Frequently triggers buys, but may not get sells |
| ⚡ High Volatility No Direction | ⭐⭐⭐☆☆ | More signals, but quality varies |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| Timeframe | 1h (default) | Can also try 30m or 2h |
| Stop Loss Adjustment | -0.15 to -0.25 | Default 36% too wide, recommend tightening |
| ROI Adjustment | Adjust based on backtest | Default values may need optimization |
| Add Trend Filter | Optional | Add EMA or EWO filter |

---

## X. Important Reminder: Simple Doesn't Mean Effective

### 10.1 Learning Cost

BBRSIoriginal is the best learning sample:
- Concise code, clear comments
- Direct logic, easy to understand
- Suitable as a foundation template for modifications

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 512MB | 1GB |
| 11-30 pairs | 1GB | 2GB |
| 31+ pairs | 2GB | 4GB |

The strategy is extremely lightweight with almost no performance pressure.

### 10.3 Differences Between Backtesting and Live Trading

Due to sparse signals (3-standard deviation Bollinger Band breakouts rarely occur), note during backtesting:
- Need sufficient historical data (at least 6 months)
- May have few trades, limited statistical significance
- Single trade profit/loss has large impact on overall results

### 10.4 Manual Trading Recommendations

This strategy is suitable for manual traders to reference:
- Simple signals, easy to observe
- 1-hour timeframe doesn't require continuous monitoring
- Can set alerts in TradingView for Bollinger Bands (20, 3) and RSI(14)

---

## XI. Conclusion

**BBRSIoriginal** is a classic paradigm of Bollinger Band mean reversion strategy. Its core value lies in:

1. **Educational Value**: Concise code, the best introductory material for learning Freqtrade strategy development.

2. **Clear Logic**: Bollinger Band oversold buy + RSI overbought sell, dual conditions clear.

3. **High Extensibility**: As a foundation template, can easily add trend filters, volume confirmation, protection mechanisms and other advanced features.

For quantitative traders, it's recommended to use it as a **learning starting point** or **strategy foundation framework**, modifying and optimizing based on actual market environment and personal risk preferences. Not recommended to use default parameters directly for live trading, especially the 36% stop loss needs reassessment.

---

**Strategy File Location**: `/home/neozh/freqtrade-strategies/strategies/BBRSIoriginal/BBRSIoriginal.py`  
**Strategy Source**: Freqtrade Official Default Strategy  
**Suitable For**: Quantitative trading beginners, strategy development learners