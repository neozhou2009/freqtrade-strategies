# CombinedBinHAndCluc2021Bull Strategy Analysis

> **Strategy #**: Batch 11, #7
> **Strategy Type**: Bollinger Bands + Multi-Strategy Combination (Bull Market Edition)
> **Timeframe**: 5 Minutes (5m)

---

## I. Strategy Overview

**CombinedBinHAndCluc2021Bull** is a combination strategy that integrates the buy logics of BinHV45, ClucMay72018, and BBRSI, specifically designed for bull market environments. The strategy's core is: buy when price deeply breaks Bollinger Bands, sell when price reverts to the Bollinger middle band.

### Core Features

| Feature | Description |
|---------|-------------|
| **Strategy Type** | Multi-Strategy Combination (Bull Market Edition) |
| **Buy Conditions** | 3 strategies combined (BinHV45 + ClucMay72018 + BBRSI), any one satisfied |
| **Sell Conditions** | 1 condition: price > Bollinger middle band |
| **Timeframe** | 5 Minutes |
| **Stop-Loss** | -9% Hard Stop-Loss |
| **ROI** | 1% Immediate Exit |
| **Dependencies** | TA-Lib, technical |
| **Strategy Code Lines** | ~60 lines |

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

| Parameter | Value | Design Intent |
|-----------|-------|---------------|
| minimal_roi | 0.01 | Single low ROI, pursues fast turnover, suitable for fast entries/exits in bull markets |
| stoploss | -0.09 | Loose stop-loss, gives sufficient fluctuation space, tolerates normal oscillations |

---

## III. Entry Conditions Details

The strategy uses three independent entry logics — any one satisfied triggers a buy.

### 3.1 Entry Logic (Strategy 1: BinHV45)

```python
(
    lower.shift().gt(0) &                          # Previous BB lower band > 0
    bbdelta.gt(close * 0.008) &                    # BB width > 0.8%
    closedelta.gt(close * 0.0175) &                # Price change > 1.75%
    tail.lt(bbdelta * 0.25) &                     # Lower wick < 25% of width
    close.lt(lower.shift()) &                     # Current price < previous lower band
    close.le(close.shift())                        # Current price <= previous close
)
```

**Conditions Analysis**:

| Condition | Meaning |
|-----------|---------|
| lower.shift().gt(0) | BB lower band valid, non-zero |
| bbdelta.gt(close * 0.008) | BB width sufficient, good volatility |
| closedelta.gt(close * 0.0175) | Price decline significant, exceeds 1.75% |
| tail.lt(bbdelta * 0.25) | Lower wick short, lower support present |
| close.lt(lower.shift()) | Price deeply breaks BB lower band |
| close.le(close.shift()) | Price continuing to fall, not reversing |

**Comprehensive Judgment**: Price deeply breaks BB, width sufficient, rebound likely.

### 3.2 Entry Logic (Strategy 2: ClucMay72018)

```python
(
    close < ema100 &                               # Price < EMA100
    close < 0.985 * bb_lowerband &                # Price < BB lower band × 0.985
    volume < volume_mean_slow.shift(1) * 20        # Volume < avg × 20
)
```

**Conditions Analysis**:

| Condition | Meaning |
|-----------|---------|
| close < ema100 | Price below 100-period EMA, in downtrend |
| close < 0.985 * bb_lowerband | Price below BB lower band by 1.5%, deeply oversold |
| volume < avg × 20 | Volume normal, excludes abnormal volume |

**Comprehensive Judgment**: Price below EMA100 and deeply below BB, volume normal, high rebound probability.

### 3.3 Entry Logic (Strategy 3: BBRSI)

```python
(
    rsi < 12 &                                   # RSI < 12 (extreme oversold)
    close < bb_lowerband4                        # Price < 4σ BB lower band
)
```

**Conditions Analysis**:

| Condition | Meaning |
|-----------|---------|
| rsi < 12 | RSI far below normal oversold threshold 30, extreme oversold |
| close < bb_lowerband4 | Price breaks 4σ BB lower band, extreme breakout |

**Comprehensive Judgment**: Extreme oversold + extreme price breakout, extremely high rebound probability.

### 3.4 Combination Logic

```python
# Any of the three strategies triggers a buy
(BinHV45 conditions) | (ClucMay72018 conditions) | (BBRSI conditions)
```

---

## IV. Exit Conditions Details

### 4.1 Technical Sell Conditions

```python
dataframe.loc[
    (close > bb_middleband),  # Price > BB middle band
    "sell",
] = 1
```

**Logic Analysis**: Price reverts from BB lower band to middle band, mean reversion complete, triggers sell.

### 4.2 ROI Exit

```python
minimal_roi = {"0": 0.01}  # 1% profit immediately exits
```

**Dual Exit Mechanism**: Technical sell signal OR reaching 1% profit, either triggers exit.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Parameters | Purpose |
|-------------------|---------------------|------------|---------|
| **Volatility Indicator** | Bollinger Bands | 40 period, 2σ | BinHV45 strategy |
| **Volatility Indicator** | Bollinger Bands | 20 period, 2σ | ClucMay72018 strategy |
| **Volatility Indicator** | Bollinger Bands | 20 period, 4σ | BBRSI strategy |
| **Trend Indicator** | EMA | 100 period | Trend filtering |
| **Momentum Indicator** | RSI | Default | Overbought/oversold judgment |
| **Volume** | Volume MA | 30 period rolling | Volume filtering |

### 5.2 Multi-Bollinger Band System

The strategy uses three independent BB systems covering different oversold levels:

| Bollinger Band | Period | Std Dev | Strategy | Capture Level |
|---------------|--------|---------|----------|--------------|
| BB1 | 40 | 2 | BinHV45 | General oversold |
| BB2 | 20 | 2 | ClucMay72018 | Short-term oversold |
| BB4 | 20 | 4 | BBRSI | Extreme oversold (deep discount) |

---

## VI. Risk Management Features

### 6.1 Hard Stop-Loss Mechanism

```python
stoploss = -0.09  # -9%
```

**Characteristics**: Loose stop-loss design, gives price sufficient fluctuation space, suitable for "mean reversion" strategy characteristics.

### 6.2 Low ROI Fast Exit

```python
minimal_roi = {"0": 0.01}  # 1%
```

**Function**:
- 1% profit can exit, pursues fast turnover.
- Paired with technical signals (price reverts to middle band) for dual exit.
- Suitable for high-frequency trading in bull market environments.

### 6.3 Volume Filtering

```python
volume < volume_mean_slow.shift(1) * 20
```

**Function**: Excludes abnormally high volume signals, prevents false signals from market manipulation.

---

## VII. Strategy Pros & Cons

### Pros

| Advantage | Description |
|-----------|-------------|
| **Multi-Strategy Combination** | 3 classic strategy logics, covering different oversold levels |
| **Extreme Oversold Capture** | BBRSI catches extreme oversold, extremely high rebound probability |
| **Fast Turnover** | 1% ROI + middle band exit, high capital utilization |
| **Bull Market Dedicated** | Specifically designed for bull markets, high rebound probability |
| **Moderate Computation** | Reasonable number of indicators, low hardware requirements |

### Cons

| Limitation | Description |
|------------|-------------|
| **No Trend Filtering** | Lacks long-term trend judgment logic |
| **No BTC Correlation** | Does not detect Bitcoin market trends |
| **Bear Market Risk** | May lose consecutively in bear markets |
| **Low ROI** | 1% may exit trending markets prematurely |
| **Multi-Bollinger Calculation** | Three BB systems increase computation overhead |

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Action | Description |
|--------------------|-------------------|-------------|
| **Bull Market** | Strongly recommend | Designed for bull markets, extremely high rebound probability |
| **Volatile Market** | Recommend | Mean reversion suitable for volatile markets |
| **Bear Market** | Pause | No trend filtering, may lose consecutively |
| **High Volatility** | Keep default | Loose stop-loss suitable for high-volatility environments |
| **Low Volatility** | Adjust ROI | Can appropriately raise ROI threshold |
| **BTC Crash** | Pause | Linkage risk, suggest standing by |

---

## IX. Applicable Market Environment Details

### 9.1 Core Logic

CombinedBinHAndCluc2021Bull trades on the philosophy of "deeply oversold + mean reversion":
- **Multi-Strategy Combination**: BinHV45 + ClucMay72018 + BBRSI triple filtering.
- **Deeply Oversold**: Captures opportunities when price deeply breaks BB.
- **Fast Exit**: Price reverts to middle band or reaches 1% profit immediately exits.

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| Bull Market | ★★★★★ | Designed for bull markets, extremely high rebound probability |
| Wide Volatile | ★★★★☆ | Mean reversion suitable for volatile markets |
| Bear Market | ★★☆☆☆ | No trend filtering, may lose consecutively |
| Extreme Sideways | ★★★☆☆ | Too little fluctuation, signals reduce |

---

## X. Summary

**CombinedBinHAndCluc2021Bull** is a combination strategy specifically designed for bull markets. Core value:

1. **Multi-Strategy Combination**: Integrates BinHV45, ClucMay72018, BBRSI three classic logics.
2. **Deeply Oversold Capture**: Three BB systems cover different oversold levels.
3. **Fast Turnover**: 1% ROI + middle band exit, high capital utilization.
4. **Bull Market Dedicated**: Designed for bull market environments, high rebound probability.
5. **Moderate Computation**: Low hardware requirements.

| Suggestion | Description |
|------------|-------------|
| **Learning Value** | Entry case for multi-strategy combinations |
| **Core Understanding** | Deeply oversold + mean reversion trading logic |
| **Usage Timing** | Only use in bull markets or volatile markets |
| **Risk Control** | Promptly pause strategy in bear markets |

*Strategy #: Batch 11, #7 | Type: Bollinger Multi-Strategy Combination | Timeframe: 5m*
