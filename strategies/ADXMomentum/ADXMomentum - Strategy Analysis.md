# ADXMomentum Strategy In-Depth Analysis

> **Strategy Number**: #411 (411th of 465 strategies)  
> **Strategy Type**: ADX Trend Following + Momentum Confirmation  
> **Timeframe**: 1 Hour (1h)

---

## 1. Strategy Overview

ADXMomentum is a classic trend-following strategy based on ADX (Average Directional Index) and momentum indicators. Originally derived from a C# implementation and ported to the Freqtrade framework by Gert Wohlgemuth. The strategy design is concise yet logically rigorous, using multi-dimensional indicator validation to confirm trend validity and avoid frequent trading in ranging markets.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | 4 conditions that must be met simultaneously (trend strength + momentum + direction) |
| **Exit Conditions** | 4 conditions (trend reversal signals) |
| **Protection Mechanism** | Fixed stop loss at -25%, fixed ROI target at 1% |
| **Timeframe** | 1 Hour (1h) |
| **Dependencies** | talib (ADX, PLUS_DI, MINUS_DI, SAR, MOM) |
| **Startup Candles** | 20 candles |

---

## 2. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.01  # Exit when 1% profit is reached
}

# Stop loss setting
stoploss = -0.25  # -25% stop loss
```

**Design Rationale**:
- **1% ROI Target**: Strategy pursues quick turnover, locking in small profits promptly
- **-25% Wide Stop Loss**: Provides sufficient room for trend fluctuations, avoiding being shaken out by oscillations

### 2.2 Order Type Configuration

The strategy does not explicitly configure `order_types`, using Freqtrade default settings.

---

## 3. Entry Conditions Detailed Analysis

### 3.1 Core Indicator Combination

The strategy uses 5 technical indicators to build entry signals:

| Indicator | Parameters | Purpose |
|-----------|------------|---------|
| ADX | 14 period | Measure trend strength |
| PLUS_DI | 25 period | Bullish direction strength |
| MINUS_DI | 25 period | Bearish direction strength |
| SAR | Default | Trend direction confirmation |
| MOM | 14 period | Momentum confirmation |

### 3.2 Entry Conditions Explained

#### Complete Entry Logic

```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (dataframe['adx'] > 25) &           # Condition 1: Sufficient trend strength
            (dataframe['mom'] > 0) &             # Condition 2: Positive momentum
            (dataframe['plus_di'] > 25) &        # Condition 3: Strong bullish power
            (dataframe['plus_di'] > dataframe['minus_di'])  # Condition 4: Bullish dominance
        ),
        'buy'] = 1
    return dataframe
```

#### Condition Analysis

| Condition # | Condition Content | Technical Meaning |
|-------------|-------------------|-------------------|
| Condition #1 | `adx > 25` | ADX above 25 indicates the market has a clear trend (not ranging) |
| Condition #2 | `mom > 0` | Momentum is positive, price is rising |
| Condition #3 | `plus_di > 25` | Bullish directional indicator above 25, strong bullish power |
| Condition #4 | `plus_di > minus_di` | Bullish directional indicator above bearish, confirming upward direction |

### 3.3 Entry Signal Classification

| Signal Dimension | Indicator | Judgment Standard |
|------------------|-----------|-------------------|
| **Trend Strength** | ADX | > 25 (strong trend) |
| **Trend Direction** | PLUS_DI vs MINUS_DI | Bullish dominance |
| **Momentum Confirmation** | MOM | Positive value (upward momentum) |
| **Comprehensive Judgment** | All four conditions met | Entry |

---

## 4. Exit Logic Detailed Analysis

### 4.1 Exit Signal System

The strategy employs a symmetric exit logic, mirroring the entry conditions:

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            (dataframe['adx'] > 25) &            # Trend still continuing
            (dataframe['mom'] < 0) &              # Momentum turned negative
            (dataframe['minus_di'] > 25) &        # Bearish power increasing
            (dataframe['plus_di'] < dataframe['minus_di'])  # Bearish dominance
        ),
        'sell'] = 1
    return dataframe
```

### 4.2 Exit Condition Analysis

| Condition # | Condition Content | Technical Meaning |
|-------------|-------------------|-------------------|
| Condition #1 | `adx > 25` | Trend still exists (not ranging) |
| Condition #2 | `mom < 0` | Momentum turned negative, price declining |
| Condition #3 | `minus_di > 25` | Bearish directional indicator above 25 |
| Condition #4 | `plus_di < minus_di` | Bearish directional indicator above bullish, confirming downtrend |

### 4.3 Exit Mechanism Summary

The strategy has three exit methods:

| Exit Method | Trigger Condition | Description |
|-------------|-------------------|-------------|
| **ROI Take Profit** | Profit ≥ 1% | Quickly lock in gains |
| **Stop Loss** | Loss ≥ 25% | Extreme situation protection |
| **Signal Exit** | All four conditions met | Trend reversal signal |

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Purpose |
|--------------------|-------------------|---------|
| **Trend Strength** | ADX (14) | Determine if market has a clear trend |
| **Directional Indicators** | PLUS_DI (25), MINUS_DI (25) | Determine bullish/bearish direction and strength |
| **Momentum Indicator** | MOM (14) | Confirm price momentum direction |
| **Trend Following** | SAR | Auxiliary trend judgment (calculated but not used) |

### 5.2 Indicator Coordination Logic

The core philosophy of the strategy is "multi-dimensional confirmation":

1. **ADX Confirms Environment**: Ensures not a ranging market (ADX > 25)
2. **DI Confirms Direction**: Bullish strength strong and exceeds bearish (PLUS_DI > MINUS_DI)
3. **MOM Confirms Momentum**: Upward price momentum exists (MOM > 0)
4. **Triple Verification Passed**: Only then generate entry signal

---

## 6. Risk Management Features

### 6.1 Fixed Percentage Stop Loss

```python
stoploss = -0.25  # -25% stop loss
```

**Design Philosophy**:
- Wide stop loss provides sufficient fluctuation room for trend
- Suitable for medium to long-term trend following at 1-hour level
- Avoids being shaken out by short-term oscillations

### 6.2 Quick Take Profit Mechanism

```python
minimal_roi = {"0": 0.01}  # Take profit at 1% profit
```

**Design Philosophy**:
- Quickly lock in profits
- Reduce drawdown risk
- Improve capital turnover rate

### 6.3 Signal Filter

The strategy builds a "signal filter" through 4 strict conditions:

- Only when trend is clear (ADX > 25)
- Direction confirmed (bullish dominance)
- Momentum confirmed (momentum positive)
- Strength sufficient (PLUS_DI > 25)

Then enter, significantly reducing false signals.

---

## 7. Strategy Advantages and Limitations

### ✅ Advantages

1. **Simple and Clear Logic**: Four entry conditions work together, easy to understand and optimize
2. **Reliable Trend Following**: ADX + DI combination is a classic trend judgment method
3. **Dual Confirmation Mechanism**: Trend direction + momentum direction dual verification
4. **Strong Parameter Interpretability**: All parameters have clear technical meaning

### ⚠️ Limitations

1. **Poor Performance in Ranging Markets**: ADX > 25 condition filters out ranging, but may miss opportunities in oscillations
2. **Wide Stop Loss**: -25% stop loss may be too large for risk-averse traders
3. **No Trailing Stop**: Does not use trailing stop, may miss larger trend gains
4. **SAR Indicator Not Used**: Code calculates SAR but does not use it for signal judgment

---

## 8. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|--------------------|---------------------------|-------------|
| **Strong Trend Market** | Default configuration | Best environment for ADX strategy, clear trend |
| **Ranging Market** | Not recommended | ADX condition difficult to meet, few trading opportunities |
| **High Volatility Market** | Widen stop loss | May need larger stop loss room |
| **Low Volatility Market** | Lower ADX threshold | Can reduce ADX threshold from 25 to 20 |

---

## 9. Applicable Market Environment Detailed Analysis

ADXMomentum belongs to the **trend-following strategy** type. Based on its code architecture, it is best suited for **clear single-direction trend market environments**, while performing poorly in **ranging markets**.

### 9.1 Strategy Core Logic

- **Trend First**: Must have ADX > 25 to enter, ensuring there's a trend to follow
- **Direction Confirmation**: PLUS_DI > MINUS_DI confirms bullish trend
- **Momentum Verification**: MOM > 0 confirms upward price momentum
- **Symmetric Exit**: Exit when signal reverses

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 **Strong Uptrend** | ⭐⭐⭐⭐⭐ | ADX condition met, trend following effective |
| 🔄 **Ranging Market** | ⭐☆☆☆☆ | ADX < 25, cannot generate signals |
| 📉 **Downtrend** | ⭐☆☆☆☆ | Long-only strategy, cannot profit in downtrend |
| ⚡️ **Extreme Volatility** | ⭐⭐☆☆☆ | May trigger stop loss, needs wider room |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|--------------------|-------------------|-------------|
| **Trading Pair Selection** | Strong trending coins | Such as BTC, ETH and other major coins |
| **Timeframe** | 1h (default) or 4h | 1h for intraday trading, 4h for medium-term |
| **ADX Threshold** | 20-25 | Can appropriately lower during high market volatility |

---

## 10. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

This strategy has simple logic and low learning cost. Suitable for:
- Beginners understanding trend-following strategies
- Learning ADX/DI indicator combination application
- Understanding signal filtering mechanisms

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 | 2GB | 4GB |
| 10-50 | 4GB | 8GB |
| 50+ | 8GB | 16GB |

### 10.3 Differences Between Backtesting and Live Trading

Strategy logic is simple, backtesting and live trading differences are relatively small, but still note:
- **Slippage Impact**: 1% ROI target can easily be eroded by slippage
- **Liquidity**: Ensure sufficient liquidity for trading pairs
- **Execution Delay**: Execution timing after signal changes

### 10.4 Suggestions for Manual Traders

This strategy's signal logic can be directly used for manual trading:
- ADX > 25 confirms trend
- PLUS_DI crossing above MINUS_DI confirms direction
- MOM > 0 confirms momentum
- Enter when all three conditions are met simultaneously

---

## 11. Summary

**ADXMomentum** is a **classic, concise, and reliable trend-following strategy**. Its core value lies in:

1. **Clear Logic**: Four entry conditions work together to form a complete trend judgment system
2. **Multi-dimensional Confirmation**: Trend strength + direction + momentum triple verification
3. **Easy to Optimize**: Strong parameter interpretability, suitable as a learning example for strategy development

For quantitative traders, ADXMomentum is an excellent starting point for understanding ADX/DI indicator application, suitable for use as a trend-following tool in clear trend markets.