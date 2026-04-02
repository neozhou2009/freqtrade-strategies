# GodtAlene Strategy Analysis

> **Strategy ID**: Community Strategy (unofficial)  
> **Strategy Type**: Trend Momentum Double-Confirmation Strategy  
> **Timeframe**: 1 Hour (1h) / 4 Hours (4h)

---

## I. Strategy Overview

**GodtAlene** is a "double insurance" strategy that blends trend-following with momentum confirmation. The strategy name comes from Danish, meaning "Good and Alone," implying its design philosophy: building robust trading signals by confirming trends and momentum across two independent dimensions, reducing losses from false breakouts.

The strategy's core logic is crystal clear: **SMA100 judges long-term trend direction, RSI confirms momentum shift timing**. SMA100 ensures only trend-confident trading; RSI avoids entry at trend endpoints. Both conditions must be met simultaneously to generate a buy signal, forming a "double insurance" mechanism.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | Double confirmation: Price above SMA100 + RSI breaks from oversold zone |
| **Sell Conditions** | Double exit: Price breaks below SMA100 OR RSI enters overbought zone |
| **Protection** | Hard stop-loss -6% + time decay ROI |
| **Timeframe** | 1 Hour / 4 Hours (suitable for swing trading) |
| **Dependencies** | TA-Lib (technical indicator calculation) |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.10,      # Immediate exit: 10% profit
    "120": 0.06,    # After 2 hours: 6% profit
    "480": 0.03     # After 8 hours: 3% profit
}

# Stop-Loss Settings
stoploss = -0.06    # Hard stop-loss: -6%
```

**Design Philosophy**:
- **High target take-profit**: Initial target set at 10%, reflecting trend trading profit potential
- **Time decay**: Longer holding = lower profit threshold, reflecting trend momentum decay reality
- **Moderate stop-loss**: -6% provides adequate price volatility room while controlling max single-trade loss

### 2.2 Timeframe Selection

The strategy recommends 1-hour or 4-hour timeframes:

| Timeframe | Candles per Day | Signal Frequency | Noise Level | Applicable Scenario |
|-----------|-----------------|-----------------|-------------|-------------------|
| 1 hour | 24 | Moderate | Moderate | Intraday swing |
| 4 hours | 6 | Lower | Lower | Trend swing |

Longer timeframes reduce market noise, making SMA100 more stable and RSI signals more reliable.

---

## III. Entry Conditions Details

### 3.1 Core Buy Logic

The strategy employs a double-confirmation mechanism to generate buy signals:

```python
# Buy Conditions
dataframe.loc[
    (
        # Condition 1: Price above SMA100 (trend confirmed)
        (dataframe['close'] > dataframe['sma_100']) &
        # Condition 2: RSI breaks up from oversold zone
        (dataframe['rsi'] > 40) &
        (dataframe['rsi'].shift(1) <= 40)
    ),
    'buy'
] = 1
```

**Logic Breakdown**:

| Condition | Code Expression | Technical Meaning |
|-----------|-----------------|-------------------|
| Trend confirmed | `close > sma_100` | Price above long-term MA, confirming uptrend |
| Momentum confirmed | `rsi > 40` | RSI has risen from oversold zone |
| Momentum trigger | `rsi.shift(1) <= 40` | Previous candle's RSI below 40 (oversold) |

### 3.2 SMA100 Trend Confirmation

**SMA100 Technical Significance**:

| Price Position | Trend Judgment | Recommendation |
|---------------|----------------|----------------|
| Price far above SMA100 | Strong uptrend | Suitable for going long |
| Price near SMA100 | Trend unclear | Observe |
| Price below SMA100 | Downtrend | Do not go long |

### 3.3 RSI Oversold Breakout Signal

**RSI 40 Threshold Technical Meaning**:

| RSI Zone | Value Range | Market State |
|---------|-------------|-------------|
| Oversold zone | RSI < 30 | Extremely oversold, high rebound probability |
| Relative oversold | 30 < RSI < 40 | Oversold but not extreme |
| Neutral zone | 40 < RSI < 60 | Bull/bear balance |
| Relative overbought | 60 < RSI < 70 | Overbought but not extreme |
| Overbought zone | RSI > 70 | Extremely overbought, high pullback probability |

---

## IV. Exit Conditions Details

### 4.1 Core Sell Conditions

The strategy also employs a double exit mechanism:

```python
# Sell Conditions
dataframe.loc[
    (
        # Condition 1: Price breaks below SMA100
        (dataframe['close'] < dataframe['sma_100']) |
        # Condition 2: RSI enters overbought zone
        (dataframe['rsi'] > 70)
    ),
    'sell'
] = 1
```

### 4.2 Momentum Overheat Sell

When RSI enters the overbought zone, it indicates the price has risen too sharply in the short term, increasing pullback probability. The strategy chooses to sell when RSI > 70 to promptly lock in profits.

### 4.3 OR Logic Exit Significance

The sell condition uses "OR" logic (|), meaning either condition triggers a sell:

```python
(Price breaks below SMA100) | (RSI > 70)
```

---

## V. Technical Indicator System

### 5.1 Core Indicator Combination

| Indicator Category | Specific Indicator | Purpose | Parameters |
|-------------------|-------------------|---------|------------|
| Trend Indicator | SMA | Trend direction judgment | Period 100 |
| Momentum Indicator | RSI | Overbought/oversold judgment | Period 14 (default) |

### 5.2 Indicator Synergy Analysis

**Complementary relationship of two indicators**:

| Dimension | SMA100 | RSI |
|-----------|--------|-----|
| Role | Trend direction | Momentum strength |
| Lag | More lagged | More leading |
| Stability | High | Moderate |
| Sensitivity | Low | High |

**Synergy effect**:
- SMA100 provides stable trend baseline
- RSI provides timely trading timing
- The combination ensures both correct trend direction and captures entry timing

---

## VI. Risk Management Highlights

### 6.1 Three-Layer Risk Protection

```
Layer 1: Technical signal exit (trend broken / momentum overheat)
    ↓
Layer 2: ROI take-profit exit (time decay)
    ↓
Layer 3: Hard stop-loss exit (-6%)
```

| Protection Layer | Trigger Condition | Protection Target |
|-----------------|-------------------|-------------------|
| Technical exit | SMA breaks or RSI > 70 | Trend reversal protection |
| ROI exit | Profit reaches target | Lock in profits |
| Hard stop-loss | Loss -6% | Principal protection |

### 6.2 Time Decay ROI Mechanism

```python
minimal_roi = {
    "0": 0.10,      # Immediately: 10%
    "120": 0.06,    # After 2 hours: 6%
    "480": 0.03     # After 8 hours: 3%
}
```

---

## VII. Strategy Pros & Cons

### Advantages

1. **Double confirmation mechanism**: SMA + RSI double filtering greatly reduces false signals
2. **Trend-conforming trading**: Only goes long when the uptrend is confirmed, avoiding counter-trend operations
3. **Moderate signal frequency**: Not over-trading, reducing fee costs
4. **Complete exit mechanism**: Technical exit + ROI + stop-loss three-layer protection
5. **Clear parameter logic**: Easy to understand, maintain, learn, and optimize

### Limitations

1. **MA lag**: SMA100 has noticeable lag; may miss early trend stages
2. **Poor oscillating performance**: Frequent signals during consolidation, may cause losses
3. **RSI false breakout**: Single RSI breakout may be a false signal
4. **Fixed parameters**: SMA100 and RSI 40/70 are fixed; need market adjustment
5. **No volume confirmation**: Lacks volume verification; may be misled by false breakouts

---

## VIII. Applicable Scenarios

| Applicable Scenarios | Not Applicable Scenarios |
|---------------------|------------------------|
| Clear uptrend markets | Oscillating consolidation markets |
| Swing trading | Intraday high-frequency trading |
| Moderate volatility markets | Extreme volatility markets |
| Learning and research purposes | Complex strategy replacement |

---

## IX. Summary

**GodtAlene** is a classic trend momentum double-confirmation strategy. Its core value lies in:

1. **Double insurance mechanism**: SMA100 confirms trend direction, RSI confirms momentum timing; their combination greatly improves signal quality
2. **Complete exit system**: Technical exit + ROI take-profit + hard stop-loss three-layer protection, complete risk control
3. **Moderate signal frequency**: Not over-trading, reducing fees and psychological pressure
4. **Clear logic framework**: Easy to understand, execute, and optimize

For quantitative traders, GodtAlene is a **well-structured strategy prototype**. It demonstrates how to combine trend and momentum indicators to build a robust trading system. It is recommended to add volume confirmation, multi-timeframe analysis, and other mechanisms to further improve signal quality.

**One-line evaluation**: Dual swords combined, stability surplus; thrives in trends, conceals in oscillation.
