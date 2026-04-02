# CombinedBinHAndCluc2021 Strategy Analysis

> **Strategy #**: #106 (6th in Batch 11)
> **Strategy Type**: Bollinger Bands + Triple Strategy Combination
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**CombinedBinHAndCluc2021** is a triple-strategy combination trading strategy that combines the buy logics of BinHV45, ClucMay72018, and BBRSI. The strategy uses "OR gate" logic for buy signal composite filtering, focusing on capturing deeply oversold after Bollinger Band convergence.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 3 strategies combined (BinHV45 + ClucMay72018 + BBRSI) |
| **Sell Conditions** | 2 modes: Technical signal (price > BB middle band) + ROI exit |
| **Protection Mechanism** | Hard stop-loss -9% + Low ROI exit |
| **Timeframe** | 5 Minutes |
| **Dependencies** | TA-Lib, technical |
| **Special Features** | Multi-strategy logic combination, three Bollinger Band systems |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.01    # Immediate exit: 1% profit
}

# Stop-Loss Settings
stoploss = -0.09  # -9% hard stop-loss
```

**Design Philosophy**:
- **Ultra-Low ROI**: Only 1% ROI, pursuing fast high-frequency turnover.
- **Loose Stop-Loss**: -9% hard stop, giving sufficient fluctuation space.
- **Short-Term Thinking**: Suitable for fast trades in high-volatility markets.

---

## III. Entry Conditions Details

### 3.1 Entry Logic (Strategy 1: BinHV45)

```python
# BinHV45 Strategy Entry Conditions
(
    lower.shift().gt(0) &                          # Previous BB lower band > 0
    bbdelta.gt(close * 0.008) &                    # BB width > 0.8%
    closedelta.gt(close * 0.0175) &                # Price change > 1.75%
    tail.lt(bbdelta * 0.25) &                     # Lower wick < 25% of width
    close.lt(lower.shift()) &                      # Current price < previous lower band
    close.le(close.shift())                        # Current price <= previous close
)
```

**Logic Analysis**: Price deeply breaks Bollinger Band, forming a hammer pattern, and the market has sufficient fluctuation space.

### 3.2 Entry Logic (Strategy 2: ClucMay72018)

```python
# ClucMay72018 Strategy Entry Conditions
(
    close < ema100 &                               # Price < EMA100
    close < 0.985 * bb_lowerband &                # Price < BB lower band × 0.985
    volume < volume_mean_slow.shift(1) * 20        # Volume < avg × 20
)
```

**Logic Analysis**: Price deeply breaks Bollinger Band and is below EMA100, with normal volume (not main operator selling).

### 3.3 Entry Logic (Strategy 3: BBRSI)

```python
# BBRSI Strategy Entry Conditions
(
    rsi < 12 &                                   # RSI < 12 (deeply oversold)
    close < bb_lowerband4                        # Price < 4σ BB lower band
)
```

**Logic Analysis**: Extreme oversold state, extremely high rebound probability.

### 3.4 Combination Logic

```python
# Any of the three strategies triggers a buy
(BinHV45 conditions) | (ClucMay72018 conditions) | (BBRSI conditions)
```

**Explanation**: Three strategy logics connected by OR — buy when any one is satisfied. This design ensures capturing oversold opportunities under different market states.

---

## IV. Exit Conditions Details

### 4.1 Technical Sell: Bollinger Middle Band Breakout

```python
# Sell Condition
dataframe.loc[
    (close > bb_middleband),  # Price > BB middle band
    "sell",
] = 1
```

**Logic Analysis**: Price reverts from lower band to middle band, mean reversion process complete, triggers sell.

### 4.2 ROI Exit

```python
minimal_roi = {"0": 0.01}  # 1% profit immediately exits
```

**Explanation**: Ultra-low threshold, paired with technical signals for fast exit. Pursues high-frequency turnover, accumulates small wins.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Parameters | Purpose |
|-------------------|---------------------|------------|---------|
| **Volatility Indicator** | Bollinger Bands | 40 period, 2σ | BinHV45 strategy |
| **Volatility Indicator** | Bollinger Bands | 20 period, 2σ | ClucMay72018 strategy |
| **Volatility Indicator** | Bollinger Bands | 20 period, 4σ | BBRSI strategy (extreme oversold) |
| **Trend Indicator** | EMA | 100 period | Trend filtering |
| **Momentum Indicator** | RSI | Default | Overbought/oversold judgment |
| **Volume** | Volume MA | 30 period rolling | Volume filtering |

### 5.2 Multi-Bollinger Band System

The strategy uses three independent Bollinger Band systems covering different market states:

| Bollinger Band | Period | Std Dev | Strategy | Capture Level |
|---------------|--------|---------|----------|--------------|
| BB1 | 40 | 2 | BinHV45 | General oversold |
| BB2 | 20 | 2 | ClucMay72018 | Short-term oversold |
| BB4 | 20 | 4 | BBRSI | Extreme oversold (deep discount) |

---

## VI. Risk Management Features

### 6.1 Hard Stop-Loss

```python
stoploss = -0.09  # -9%
```

**Explanation**: Loose stop-loss design, giving price sufficient fluctuation space, suitable for high-volatility markets.

### 6.2 Low ROI Fast Exit

```python
minimal_roi = {"0": 0.01}  # 1%
```

**Function**: 1% profit can exit, pursuing fast turnover. Paired with technical signals (price reverts to middle band) for fast liquidation. Suitable for short-term operation "accumulate small wins" philosophy.

### 6.3 Volume Filtering

```python
volume < volume_mean_slow.shift(1) * 20
```

**Function**: Excludes abnormally high volume, prevents being misled by market manipulation or false breakouts.

---

## VII. Strategy Pros & Cons

### Pros

1. **Multi-Strategy Combination**: 3 classic strategy logics, covering different scenarios, improving signal reliability.
2. **Extreme Oversold Capture**: BBRSI conditions capture extreme oversold opportunities, extremely high rebound probability.
3. **Fast Turnover**: 1% ROI + middle band exit, high capital utilization.
4. **Pattern Recognition**: BinHV45 mode effectively identifies hammer patterns.
5. **Moderate Computation**: Though using three Bollinger Band systems, calculation logic is concise.

### Cons

1. **No Trend Filtering**: No long-term trend judgment, may counter-trend buy in downtrends.
2. **No BTC Correlation**: Does not detect Bitcoin market trends.
3. **Low ROI**: 1% may exit trending markets prematurely.
4. **Timeframe Limitation**: Only applicable to 5-minute level.
5. **Multi-Bollinger Calculation**: Three Bollinger Band systems increase computation.

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Description |
|--------------------|--------------------------|-------------|
| **High-Volatility Market** | Strongly recommended | Loose stop-loss suitable for high volatility |
| **Volatile Market** | Recommended | Mean reversion logic suitable for volatile markets |
| **Unilateral Uptrend** | Use cautiously | May miss subsequent rally |
| **Unilateral Downtrend** | Pause | No trend filtering, may lose consecutively |
| **Low-Volatility Market** | Not recommended | Signals scarce, ROI hard to achieve |

---

## IX. Applicable Market Environment Details

### 9.1 Core Strategy Logic

- **Multi-Strategy Combination**: BinHV45 + ClucMay72018 + BBRSI three logics.
- **Deep Oversold Capture**: Captures opportunities when price deeply breaks Bollinger Bands.
- **Fast Exit**: Price reverts to middle band or 1% profit immediately exits.
- **Mean Reversion**: Based on belief that price will always revert to the mean.

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| Bull Rally | ★★★★★ | Deeply oversold then rebound probability extremely high |
| Wide Volatile | ★★★★☆ | Mean reversion suitable for volatile markets |
| Downtrend | ★★☆☆☆ | No trend filtering, may counter-trend buy |
| Extreme Sideways | ★★★☆☆ | Too little fluctuation, signals reduce |

---

## X. Summary

**CombinedBinHAndCluc2021** is a mature multi-strategy combination trading strategy. Its core value lies in:

1. **Triple Strategy Combination**: BinHV45 + ClucMay72018 + BBRSI three classic logics complement each other.
2. **Deep Oversold Capture**: Multi-layer captures when price deeply breaks Bollinger Bands.
3. **Extreme Signal Identification**: BBRSI conditions identify extreme oversold, extremely high rebound probability.
4. **Fast Turnover**: 1% ROI + middle band exit, pursuing accumulation of small wins.
5. **Clean and Efficient**: Code logic clear, easy to understand and modify.

**Usage Suggestions**:
- Suitable for investors with some quantitative trading experience.
- Suggest using in volatile or high-volatility markets.
- Use cautiously or pause in downtrends.
- Conduct sufficient backtesting verification before live trading.
- Can adjust ROI parameters based on market conditions.
