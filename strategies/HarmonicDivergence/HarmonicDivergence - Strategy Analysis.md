# HarmonicDivergence Strategy: In-Depth Analysis

> **Strategy ID**: #196 (196th of 465 strategies)
> **Strategy Type**: Multi-Indicator Divergence Trading / Reversal Capture
> **Timeframe**: 15 Minutes (15m)

---

## I. Strategy Overview

**HarmonicDivergence** is a reversal capture strategy based on multi-indicator divergence recognition. The core idea is: when price makes a new low but technical indicators do not make a new low (bullish divergence), enter to capture potential trend reversal opportunities.

"Harmonic" in technical analysis often refers to harmonious proportional relationships in price patterns, while "Divergence" refers to inconsistency between price and indicator movement. The strategy monitors divergences across up to 11 technical indicators, constructing a multi-confirmation mechanism to improve signal reliability.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Bullish divergence signal + Keltner Channel breakout confirmation |
| **Exit Conditions** | ROI tiered take-profit + Trailing stop + Hard stop-loss |
| **Protections** | Hard stop-loss + Trailing stop dual protection |
| **Timeframe** | 15 Minutes (main) |
| **Indicator Coverage** | 11 divergence detection indicators |
| **Dependencies** | TA-Lib, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.05,    # Immediate exit: 5% profit
    "10": 0.03,   # After 10 minutes: 3% profit
    "30": 0.02,   # After 30 minutes: 2% profit
    "60": 0.01    # After 60 minutes: 1% profit
}

# Stop-Loss Settings
stoploss = -0.10    # -10% hard stop-loss

# Trailing Stop
trailing_stop = 0.007        # 0.7% activation threshold
trailing_stop_positive = 0.01  # 1% positive trailing
```

**Design Philosophy**:
- **Tiered Take-Profit**: Decreasing from 5% to 1%, gradually locking in profits while capturing reversal opportunities
- **Moderate Stop-Loss**: -10% provides reasonable volatility room, avoiding being stopped out by normal oscillation
- **Trailing Stop**: 0.7% activation threshold, protects earned profits after profitability

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

---

## III. Entry Conditions Details

### 3.1 Divergence Detection Core Logic

Divergence trading is a classic method in technical analysis. Its theoretical basis:

**Bullish Divergence (Buy Signal)**:
- Price makes a new low (current price < previous low)
- But technical indicator does not make a new low (current indicator value > previous indicator low)
- This indicates downward momentum is exhausted and may be about to reverse

### 3.2 The 11 Divergence Detection Indicators

The strategy monitors divergence across the following 11 technical indicators:

| # | Indicator Name | Category | Divergence Detection Features |
|---|-------------|---------|------------------------------|
| 1 | RSI (Relative Strength Index) | Momentum | Classic divergence indicator; overbought/oversold judgment |
| 2 | Stochastic | Oscillator | High sensitivity; suitable for capturing short-term reversals |
| 3 | ROC (Rate of Change) | Momentum | Price change rate; identifies momentum decay |
| 4 | Ultimate Oscillator | Composite Momentum | Multi-period weighted; reduces false signals |
| 5 | Awesome Oscillator | Momentum | Market driving force change; trend strength judgment |
| 6 | MACD | Trend Momentum | Histogram divergence; trend reversal confirmation |
| 7 | CCI (Commodity Channel Index) | Trend | Periodic divergence; channel position judgment |
| 8 | CMF (Chaikin Money Flow) | Money Flow | Price-volume divergence; money flow judgment |
| 9 | OBV (On-Balance Volume) | Volume | Price-volume divergence; verifies price trend |
| 10 | MFI (Money Flow Index) | Money | Volume-price combined overbought/oversold judgment |
| 11 | ADX (Average Directional Index) | Trend Strength | Trend strength divergence; direction judgment |

### 3.3 Filter Conditions

The strategy uses two channel indicators as filter conditions:

**Keltner Channel**:
- A volatility channel based on ATR (Average True Range)
- When price breaks through channel boundary, confirms entry signal
- Effectively filters false breakouts and noise signals

**Bollinger Bands**:
- A volatility channel based on standard deviation
- Assists in judging price's relative position
- Provides additional confirmation during extreme volatility

### 3.4 Comprehensive Entry Signal Assessment

The strategy's entry logic can be summarized as:

> **Multi-indicator divergence + Channel breakout confirmation** — triggers buy when at least one indicator shows bullish divergence and price breaks through the Keltner Channel.

```python
# Pseudocode example
# Divergence detection (using RSI as example)
price_lower_low = dataframe['close'] < dataframe['close'].shift(n)
rsi_higher_low = dataframe['RSI'] > dataframe['RSI'].shift(n)
divergence = price_lower_low and rsi_higher_low

# Channel breakout confirmation
channel_breakout = dataframe['close'] > dataframe['kc_upper']

# Buy signal
buy_signal = divergence and channel_breakout
```

---

## IV. Exit Logic Details

### 4.1 Tiered Take-Profit System

The strategy employs a phased take-profit approach based on holding time:

| Holding Time | Target Profit | Design Intent |
|-------------|--------------|--------------|
| Immediate | 5% | Quickly lock in substantial profit |
| After 10 minutes | 3% | Gradually lower expectations |
| After 30 minutes | 2% | Conservative lock-in |
| After 60 minutes | 1% | Time stop; avoid prolonged holding |

### 4.2 Trailing Stop Mechanism

```python
trailing_stop = 0.007           # 0.7% pullback triggers trailing
trailing_stop_positive = 0.01   # Activates after 1% profit
```

**Working Mechanism**:
1. When profit reaches 1%, trailing stop activates
2. Price pullback of 0.7% triggers stop
3. Stop price dynamically moves up with highest price
4. Locks in earned profits; prevents profit from evaporating

### 4.3 Hard Stop-Loss Protection

```python
stoploss = -0.10  # -10%
```

**Design Philosophy**:
- Reversal market volatility is intense; some room is needed
- 10% stop-loss is relatively moderate; avoids being stopped out by normal oscillation
- Forms dual protection with trailing stop

---

## V. Technical Indicator System

### 5.1 Core Indicator Classification

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Momentum Indicators** | RSI, ROC, Stochastic, Ultimate Oscillator, Awesome Oscillator, MACD | Detect momentum changes; identify divergence |
| **Trend Indicators** | CCI, ADX | Judge trend direction and strength |
| **Volume Indicators** | CMF, OBV, MFI | Verify price divergence; price-volume analysis |
| **Channel Indicators** | Keltner Channel, Bollinger Bands | Filter false signals; confirm breakout validity |

### 5.2 Indicator Synergy Mechanism

The strategy's indicator system design reflects the concept of **multi-dimensional confirmation**:

1. **Momentum Dimension**: RSI, Stochastic, etc. detect price momentum changes
2. **Trend Dimension**: CCI, ADX judge trend direction and strength
3. **Volume Dimension**: CMF, OBV, MFI verify money flow direction
4. **Volatility Dimension**: Keltner Channel, Bollinger Bands confirm breakout validity

### 5.3 Divergence Signal Priority

Although the strategy monitors 11 indicators, divergence signal reliability varies:

| Priority | Indicator | Reliability Notes |
|---------|----------|----------------|
| High | MACD | Trend confirmation; fewer false signals |
| High | RSI | Classic indicator; thoroughly validated historically |
| Medium | Ultimate Oscillator | Multi-period weighted; stable signals |
| Medium | CMF | Price-volume combined; money flow verification |
| Low | Stochastic | High sensitivity but many false signals |

---

## VI. Risk Management Highlights

### 6.1 Multi-Layer Protection Mechanism

```
Protection Layer    Trigger Condition           Function
────────────────────────────────────────────────────────────
Hard Stop-Loss      Loss reaches -10%           Limit maximum loss
Trailing Stop       Pullback 0.7% after profit  Lock in earned profits
ROI Take-Profit     Profit target reached       Phased profit lock-in
```

### 6.2 Position Management Recommendations

The characteristics of divergence strategies require reasonable position management:

| Risk Type | Recommended Config | Notes |
|---------|------------------|-------|
| Single Trade Risk | 1-2% of account capital | Divergence signals may fail |
| Maximum Positions | 3-5 trading pairs | Diversify risk |
| Correlation Control | Avoid same sector | Divergence signals may trigger simultaneously |

### 6.3 Signal Filtering Mechanism

The strategy uses Keltner Channel and Bollinger Bands as filters:

```python
# Filter logic
keltner_filter = dataframe['close'] > dataframe['kc_upper']
bollinger_filter = dataframe['close'] < dataframe['bb_upper']

# Only divergence signals meeting filter conditions trigger buy
```

---

## VII. Strategy Pros & Cons

### Strengths

1. **Multi-Indicator Confirmation**: 11 indicators' divergence detection; signals verified through multiple layers; high reliability
2. **Captures Reversal Points**: Divergence is a classic reversal signal; suitable for capturing trend turning points
3. **Rich Dimensions**: Covers momentum, trend, volume three dimensions; comprehensive market state analysis
4. **Complete Protection Mechanism**: Hard stop-loss + Trailing stop + Tiered take-profit; three layers of protection

### Weaknesses

1. **Complex Divergence Recognition**: Divergence detection for 11 indicators requires precise algorithms; possible live trading delays
2. **False Divergence Risk**: In strong trends, divergence signals may frequently fail
3. **Parameter Sensitivity**: Time window selection for divergence judgment greatly impacts results
4. **Average Performance in Ranging Markets**: In sideways oscillation, divergence signals are frequent but unreliable

---

## VIII. Applicable Scenarios

| Market Environment | Recommendation | Notes |
|-------------------|---------------|-------|
| End of Downtrend | Strongly Recommended | Bullish divergence signals accurate; capture rebounds |
| Pullback in Uptrend | Recommended | Identify end of pullback |
| Slight Downward Ranging | Use with Caution | Many false divergences; need strict filtering |
| Unilateral Uptrend | Not Recommended | Cannot capture upward moves |
| High Volatility | Adjust Parameters | Divergence signals may distort |

---

## IX. Applicable Market Environment Analysis

HarmonicDivergence is a typical **divergence reversal strategy**. Based on its code architecture and divergence trading principles, it is best suited for **trend reversal points**, and performs poorly in unilateral trends or violent oscillation.

### 9.1 Strategy Core Logic

- **Bullish Divergence Capture**: Price new low + indicator not new low = potential reversal
- **Multi-Indicator Verification**: 11 indicators improve signal reliability
- **Channel Filtering**: Keltner Channel breakout confirms entry timing

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| End of Downtrend | ★★★★★ | Core scenario; bullish divergence signals accurate |
| Ranging Market | ★★☆☆☆ | Many false divergences; stop-loss pressure |
| Unilateral Downward | ★☆☆☆☆ | Divergence signals continuously fail |
| Unilateral Upward | ★☆☆☆☆ | No buy signals; strategy holds no position |

### 9.3 Key Configuration Recommendations

| Config Item | Suggested Value | Notes |
|------------|---------------|-------|
| stoploss | -0.08 ~ -0.12 | Adjust based on pair volatility |
| trailing_stop | 0.005 ~ 0.01 | Appropriately widen during high-volatility reversal markets |
| minimal_roi | Tiered decrease | Lock in profits; avoid profit evaporation |

---

## X. Important Notes: The Cost of Complexity

### 10.1 Learning Curve

HarmonicDivergence involves divergence judgment across 11 technical indicators:
- Requires understanding each indicator's meaning and applicable scenarios
- Requires mastering algorithmic implementation of divergence recognition
- Requires understanding reliability differences between different indicators' divergence signals

For beginner traders, it is recommended to first master divergence judgment for RSI and MACD, the two core indicators, before gradually expanding to other indicators.

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|-----------------|------------|----------------|
| Under 10 pairs | 2GB | 4GB |
| 10-30 pairs | 4GB | 8GB |
| Over 30 pairs | 8GB | 16GB |

### 10.3 Backtesting vs. Live Trading Differences

**Notes**:
- Divergence recognition in backtesting may be overly idealized
- Indicator calculations in live trading have delays
- Keltner Channel breakout confirmation may have slippage

### 10.4 Manual Trading Suggestions

If you want to manually apply this strategy's logic:
1. First observe whether price has made a new low
2. Check whether RSI or MACD shows divergence
3. Wait for price to break through recent resistance for confirmation
4. Strictly enforce stop-loss; divergence has high failure rate

---

## XI. Summary

**HarmonicDivergence** is a reversal capture strategy focused on divergence trading. Its core value lies in:

1. **Multi-Dimensional Divergence Detection**: 11 indicators cover momentum, trend, volume three dimensions; improves signal reliability
2. **Classic Technical Pattern**: Divergence is a long-validated reversal signal in technical analysis
3. **Complete Protection Mechanism**: Hard stop-loss + Trailing stop + Tiered take-profit; three layers of risk control

For quantitative traders, HarmonicDivergence is a typical divergence strategy template, suitable for finding entry opportunities at trend reversal points. Note the false breakout risk of divergence signals; recommended to use with other trend confirmation indicators and strictly enforce position management.

---
