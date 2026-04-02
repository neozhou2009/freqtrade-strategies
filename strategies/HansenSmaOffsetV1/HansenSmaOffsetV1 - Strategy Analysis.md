# HansenSmaOffsetV1 Strategy: In-Depth Analysis

> **Strategy ID**: #195 (195th of 465 strategies)
> **Strategy Type**: Range Breakout
> **Timeframe**: 15 Minutes (15m)

---

## I. Strategy Overview

**HansenSmaOffsetV1** is a range breakout strategy based on SMA offset bands. The strategy constructs a price channel by calculating upper and lower offsets of a Simple Moving Average, buying when price touches the lower band and selling when it touches the upper band, capturing rebound and pullback opportunities in range-bound markets.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 1 buy signal, based on lower band breakout and green candle confirmation |
| **Exit Conditions** | 1 sell signal, based on upper band breakout and red candle confirmation |
| **Protections** | Hard stop-loss -10%, tiered ROI take-profit |
| **Timeframe** | 15 Minutes |
| **Dependencies** | TA-Lib, qtpylib, numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,   # Immediate exit: 10% profit
    "30": 0.05,  # After 30 minutes: 5% profit
    "60": 0.02,  # After 60 minutes: 2% profit
}

# Stop-Loss Settings
stoploss = -0.10  # Hard stop-loss -10%
```

**Design Philosophy**:
- **Aggressive Take-Profit**: Immediate exit set at 10%, pursuing quick profits
- **Time Decay**: Longer holding time means lower take-profit threshold, reducing holding risk
- **Symmetrical Stop-Loss**: -10% stop-loss and 10% immediate take-profit form a symmetrical risk-reward ratio

### 2.2 Order Type Configuration

The strategy uses default order type configuration with no special settings.

---

## III. Entry Conditions Details

### 3.1 Entry Signal Logic

The strategy has only one entry signal, with simple logic:

```python
# Entry signal: lower band breakout + green candle confirmation
dataframe.loc[
    (
        (dataframe['high'] < dataframe['smad1']) &    # High below lower band
        (dataframe['hopen'] < dataframe['hclose'])     # Heikin-Ashi green candle
    ),
    'buy'] = 1
```

### 3.2 Condition Analysis

| Condition | Technical Meaning | Market Logic |
|---------|------------------|-------------|
| `high < smad1` | Candle high below SMA lower band | Price breaks below support, touching range bottom |
| `hopen < hclose` | Heikin-Ashi green candle | Short-term momentum turning strong, rebound signal confirmed |

### 3.3 Entry Condition Classification

| Condition Type | Core Logic | Signal # |
|--------------|-----------|---------|
| Range Reversal | Lower band breakout + green candle confirmed | Condition #1 |

---

## IV. Exit Logic Details

### 4.1 Exit Signal Logic

The strategy has only one exit signal:

```python
# Exit signal: upper band breakout + red candle confirmation
dataframe.loc[
    (
        (dataframe['low'] > dataframe['smau1']) &      # Low above upper band
        (dataframe['hopen'] > dataframe['hclose'])     # Heikin-Ashi red candle
    ),
    'sell'] = 1
```

### 4.2 Condition Analysis

| Condition | Technical Meaning | Market Logic |
|---------|------------------|-------------|
| `low > smau1` | Candle low above SMA upper band | Price breaks above resistance, touching range top |
| `hopen > hclose` | Heikin-Ashi red candle | Short-term momentum turning weak, pullback signal confirmed |

### 4.3 Exit Condition Classification

| Condition Type | Core Logic | Signal # |
|--------------|-----------|---------|
| Range Reversal | Upper band breakout + red candle confirmed | Condition #1 |

---

## V. Technical Indicator System

### 5.1 Core Indicators

The strategy uses two types of technical indicators: SMA offset bands and Heikin-Ashi smoothed price.

| Indicator Category | Specific Indicator | Calculation | Purpose |
|-------------------|--------------------|-------------|---------|
| **Trend Indicator** | SMA Offset Upper Band | SMA(20) × 1.05 | Resistance identification |
| **Trend Indicator** | SMA Offset Lower Band | SMA(20) × 0.95 | Support identification |
| **Smoothed Indicator** | Heikin-Ashi Close | (O+H+L+C) / 4 | Price smoothing |
| **Smoothed Indicator** | Heikin-Ashi Open | (prev 2 O+C) / 2 | Trend confirmation |
| **Auxiliary Indicator** | HA Close MA | SMA(hclose, 6) | Short-term trend |
| **Auxiliary Indicator** | HA Open MA | SMA(hopen, 6) | Short-term trend |

### 5.2 SMA Offset Band Explained

SMA offset bands are the core indicators of this strategy. Construction method:

```python
# Upper band: SMA(20) + 5%
dataframe['smau1'] = ta.SMA(dataframe['close'], timeperiod=20) * 1.05

# Lower band: SMA(20) - 5%
dataframe['smad1'] = ta.SMA(dataframe['close'], timeperiod=20) * 0.95
```

**Design Features**:
- Fixed offset of ±5%, constructing a channel approximately 10% wide
- Channel adjusts dynamically to market volatility
- Upper band as resistance, lower band as support

### 5.3 Heikin-Ashi Smoothed Price

The strategy uses a simplified Heikin-Ashi price for trend confirmation:

```python
# HA Close: average of four prices
dataframe['hclose'] = (dataframe['open'] + dataframe['high'] + 
                       dataframe['low'] + dataframe['close']) / 4

# HA Open: average of previous 2 candles' open and close
dataframe['hopen'] = ((dataframe['open'].shift(2) + 
                       dataframe['close'].shift(2)) / 2)

# HA High: max of three prices
dataframe['hhigh'] = dataframe[['open', 'close', 'high']].max(axis=1)

# HA Low: min of three prices
dataframe['hlow'] = dataframe[['open', 'close', 'low']].min(axis=1)
```

**Design Features**:
- Smooths price noise, filters false signals
- Green candle (hopen < hclose) indicates uptrend
- Red candle (hopen > hclose) indicates downtrend

---

## VI. Risk Management Highlights

### 6.1 Tiered Take-Profit Mechanism

The strategy uses a time-decaying ROI take-profit mechanism:

| Holding Time | Take-Profit Threshold | Risk Appetite |
|-------------|----------------------|---------------|
| Immediate exit | 10% | Aggressive |
| After 30 minutes | 5% | Moderate |
| After 60 minutes | 2% | Conservative |

**Design Philosophy**:
- Longer holding time means greater risk exposure
- Lowering take-profit threshold locks in existing profits
- Avoids uncertainty of prolonged holding

### 6.2 Hard Stop-Loss Protection

```python
stoploss = -0.10  # 10% fixed stop-loss
```

**Features**:
- Forms 1:1 risk-reward ratio with immediate take-profit
- Maximum single-trade loss controlled at 10%
- No trailing stop; simple and direct execution

### 6.3 Signal Filtering Mechanism

The strategy filters false signals through dual conditions:

| Filter Layer | Function | Effect |
|-------------|---------|--------|
| Band Breakout | Price must exceed channel boundary | Excludes in-channel oscillation |
| Candle Pattern | HA green/red candle confirmation | Excludes false breakouts |

---

## VII. Strategy Pros & Cons

### Strengths

1. **Simple Logic**: Entry and exit rules are clear, easy to understand and maintain
2. **Few Parameters**: Only depends on SMA period and offset ratio; low overfitting risk
3. **Range Adaptation**: Performs well in ranging markets, captures rebounds and pullbacks
4. **Computationally Efficient**: Simple indicator calculations, low resource consumption

### Weaknesses

1. **Weak in Trend Markets**: Will frequently trade counter-trend in unilateral trends
2. **False Signal Risk**: No trend direction filter; may frequently get stopped out in ranging markets
3. **Fixed Offset**: 5% offset doesn't adapt to all market volatility environments
4. **No Volume Confirmation**: Lacks volume verification; signal reliability limited

---

## VIII. Applicable Scenarios

| Market Environment | Recommendation | Notes |
|-------------------|---------------|-------|
| Range-bound | Suitable | Core matching scenario; strategy's original design intent |
| Sideways Consolidation | Suitable | Upper and lower bands trigger frequently; capture ranging gains |
| Unilateral Trend | Use with Caution | Frequent counter-trend trades; need to adjust offset or pause |
| High Volatility | Use with Caution | Fixed 5% offset may be too narrow; need to widen channel |

---

## IX. Applicable Market Environment Analysis

**HansenSmaOffsetV1** is a typical range trading strategy. Based on its code architecture and logic, it is best suited for **ranging sideways markets**, and performs poorly during **unilateral trend markets**.

### 9.1 Strategy Core Logic

- **Mean Reversion Philosophy**: Price tends to revert after deviating from moving average
- **Channel Trading Mode**: Classic range strategy of buy at lower band, sell at upper band
- **Trend Confirmation Filter**: HA candle patterns provide short-term momentum verification

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| Slow Bull Trend | ⭐⭐☆☆☆ | After buying at lower band, price continues rising but exits too early at upper band |
| Ranging Sideways | ⭐⭐⭐⭐⭐ | Core matching scenario; bands trigger frequently; stable returns |
| Downtrend | ⭐⭐☆☆☆ | After buying at lower band, price continues falling; frequent stop-loss triggers |
| High Volatility | ⭐⭐⭐☆☆ | Fixed channel width may generate many false signals |

### 9.3 Key Configuration Recommendations

| Config Item | Suggested Value | Notes |
|------------|---------------|-------|
| SMA Period | 20 | Default; balances sensitivity and stability |
| Offset Ratio | 5% | Default; can adjust for high-volatility markets |
| Stop-Loss Ratio | -10% | Symmetrical with immediate take-profit |
| Number of Pairs | 15 | Author's suggested holding number |
| Stake Mode | unlimited | Author's suggested capital management mode |

---

## X. Important Notes: Strategy Usage Considerations

### 10.1 Market Identification

Before using this strategy, determine whether the market is in a ranging state:

- **Ranging Signal**: Price repeatedly crosses within the SMA channel
- **Trend Signal**: Price continuously runs on one side of the channel
- **Recommendation**: In trend markets, consider pausing the strategy or widening the offset

### 10.2 Parameter Optimization Space

| Parameter | Default | Optimization Direction |
|---------|---------|----------------------|
| SMA Period | 20 | Can adjust 15-30 based on market characteristics |
| Offset Ratio | 5% | Can widen to 7-10% in high-volatility markets |
| Stop-Loss Ratio | -10% | Adjust based on risk appetite |

### 10.3 Signal Confirmation Suggestions

The strategy lacks volume confirmation; recommended to combine with:

- Volume surge to confirm breakout validity
- RSI or MACD to assist in judging overbought/oversold
- Multi-timeframe confirmation of trend direction

### 10.4 Backtesting vs. Live Trading Differences

Range strategies may perform excellently in backtesting, but in live trading:

- Slippage may erode profits
- High trade frequency means significant fee impact
- When ranging transitions to trend, may suffer consecutive losses

---

## XI. Summary

**HansenSmaOffsetV1** is a simply designed, clearly logical range breakout strategy. Its core value lies in:

1. **Simple and Effective**: SMA offset bands construct channel; HA candles confirm signals; rules transparent and easy to execute
2. **Range Adaptation**: Specifically designed for ranging markets; captures mean reversion opportunities
3. **Easy to Understand**: Few parameters; beginner-friendly; easy to understand and optimize

For quantitative traders, this strategy is a good starting point for learning range trading logic. However, use cautiously or combine with trend filters in trend markets. It is recommended to adjust the offset based on target market volatility characteristics and add volume or trend direction filters to improve signal quality.

---
