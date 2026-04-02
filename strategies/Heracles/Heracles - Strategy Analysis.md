# Heracles Strategy: In-Depth Analysis

> **Strategy ID**: #193 (Note: duplicate ID in source data — this is the 12-hour ultra-long-term strategy)
> **Strategy Type**: Volatility Breakout / Ultra-Long-Term Trend
> **Timeframe**: 12 Hours (12h)

---

## I. Strategy Overview

Heracles is an ultra-long-term trend strategy based on capturing volatility extremes. The strategy name derives from the greatest hero of Greek mythology — Heracles — symbolizing strength and endurance. True to its name, this is a strategy requiring tremendous patience: 12-hour timeframe, with holding periods potentially exceeding 7 days.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Donchian Channel Percentile < Keltner Channel Width (extreme volatility compression) |
| **Exit Conditions** | MACD Signal crosses below EMA(12) |
| **Protections** | Hard stop-loss + Trailing stop |
| **Timeframe** | 12 Hours (ultra-long-term) |
| **Holding Period** | Can exceed 7.5 days |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.328,      # Immediate exit: 32.8% profit
    "27h": 0.179,    # After 27 hours: 17.9% profit
    "4d": 0.054,     # After 4 days: 5.4% profit
    "7.5d": 0        # After 7.5 days: break-even exit
}

# Stop-Loss Settings
stoploss = -0.0466              # -4.66% hard stop-loss
trailing_stop_positive = 0.024  # 2.4% trailing stop activation point
```

**Design Philosophy**:
- **Aggressive Take-Profit Target**: Initial target 32.8%, reflecting "capture big trends" positioning
- **Tiered Take-Profit Decrease**: Gradually lower expectations as holding time extends
- **Tight Stop-Loss**: -4.66% hard stop-loss + 2.4% trailing stop; strictly control risk

### 2.2 Order Type Configuration

```python
# Typical configuration (inferred)
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

### 2.3 Timeframe Characteristics

The 12-hour timeframe is Heracles' most distinctive feature:

| Comparison Dimension | Common Strategies | Heracles |
|--------------------|-------------------|---------|
| Typical Timeframe | 5m, 15m, 1h | 12h |
| Typical Holding Time | Several hours | Several days to a week |
| Signal Frequency | High | Low |
| Suitable For | Day traders | Trend investors |

---

## III. Entry Conditions Details

### 3.1 Core Entry Logic

The strategy's core entry condition can be summarized as:

```python
Donchian_Channel_Percentile < Keltner_Channel_Width
```

**Logic**:
- Donchian Channel Percentile reflects price's relative position within the range
- Keltner Channel Width reflects market volatility
- When percentile is below width, it indicates price is in a state of extreme volatility compression

### 3.2 Entry Conditions Explained

#### Volatility Compression Signal

**Technical Meaning**:
- Extreme volatility compression is a precursor to market direction selection
- Similar to "spring compression" principle: the tighter the compression, the greater the release energy
- Enter during low-volatility period; await trend breakout

**Entry Timing Judgment**:

| Market State | Donchian Percentile | Keltner Width | Signal |
|-------------|-------------------|---------------|--------|
| Extreme Compression | Very low | Relatively high | ✅ Buy |
| Normal Volatility | Medium | Medium | ⏸️ Wait |
| High Volatility | Very high | Very high | ❌ Don't buy |

### 3.3 Comprehensive Entry Signal Assessment

The strategy's entry logic can be summarized as:
> **Wait until volatility compresses to its extreme, then enter** — when Donchian Percentile is far below Keltner Width, it indicates market energy is accumulating and about to release.

---

## IV. Exit Logic Details

### 4.1 Exit Conditions

The strategy uses MACD and EMA crossover as the exit criterion:

```python
MACD_Signal crosses below EMA(12)
```

**Logic**:
- MACD Signal is the signal line of the MACD indicator
- EMA(12) is the fast exponential moving average
- When Signal crosses below EMA(12), it indicates short-term momentum is weakening

### 4.2 Exit Signal Details

| Signal Name | Trigger Condition | Technical Meaning |
|-------------|------------------|-------------------|
| MACD Momentum Decay | Signal < EMA(12) | Short-term upward momentum weakening |
| Trend Confirmation Reversal | Signal continuously below EMA | May be entering downtrend |

### 4.3 ROI Tiered Take-Profit Mechanism

The strategy employs a phased take-profit approach:

| Holding Time | Target Profit | Design Intent |
|-------------|--------------|--------------|
| Immediate | 32.8% | Capture main wave of big trend |
| After 27 hours | 17.9% | Lower expectations when trend continues |
| After 4 days | 5.4% | Conservative lock-in for long-term holding |
| After 7.5 days | Break-even | Time stop; forced exit |

**Design Philosophy**:
- Ultra-long-term strategy pursues big trends
- Tiered take-profit gradually locks in profits during trend continuation
- Time stop avoids indefinitely prolonged holding

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Volatility Indicator** | Keltner Channel | Measures market volatility width |
| **Position Indicator** | Donchian Channel | Judges price's relative position in range |
| **Trend Indicator** | MACD | Judges trend direction and momentum |
| **Trend Indicator** | EMA(12) | Fast trend reference; assists exit judgment |

### 5.2 Indicator Synergy Relationship

```
Entry Signal Chain:
Keltner Channel Width → Judge volatility state
        ↓
Donchian Channel Percentile → Judge price position
        ↓
Volatility Compression Confirmed → Enter

Exit Signal Chain:
MACD Signal → Momentum direction
        ↓
EMA(12) → Fast trend reference
        ↓
Signal crosses below EMA → Exit
```

### 5.3 Volatility Compression Principle

**Core Concept**:
- Low volatility state is a stage of market energy accumulation
- Volatility cannot remain at extreme lows forever
- Breakout direction can be assisted by other indicators

**Mathematical Expression**:
```
Volatility Compression Degree = Keltner_Width - Donchian_Percentile
Higher compression degree → Higher breakout probability
```

---

## VI. Risk Management Highlights

### 6.1 Hard Stop-Loss Combined with Trailing Stop

```python
stoploss = -0.0466              # Hard stop-loss
trailing_stop_positive = 0.024  # Trailing stop activation point
```

**Design Philosophy**:

| Stop-Loss Type | Trigger Condition | Protection Target |
|--------------|------------------|-----------------|
| Hard Stop-Loss | -4.66% | Limit maximum loss |
| Trailing Stop | Profit > 2.4% | Lock in profit space |

**Analysis**:
- Hard stop-loss is relatively tight (-4.66%); quick stop
- Trailing stop activation at 2.4%; locks early profits
- Combined: both protects principal and locks in profits

### 6.2 Time Stop Mechanism

The strategy's time stop design:

| Time Point | Profit Target | Meaning |
|-----------|-------------|---------|
| Immediate | 32.8% | Ideal target |
| 27 hours | 17.9% | Lower expectations |
| 4 days | 5.4% | Conservative lock-in |
| 7.5 days | Break-even | Time stop |

**Design Intent**:
- Ultra-long-term holding is not indefinite
- Lower profit expectations as time extends
- Forced break-even exit after 7.5 days

### 6.3 Holding Time Management

Ultra-long-term strategy special considerations:

| Risk Factor | Management Method |
|------------|------------------|
| Market changes | Time stop controls holding duration |
| Liquidity risk | Choose high-liquidity trading pairs |
| Overnight risk | 12h timeframe already includes overnight |

---

## VII. Strategy Pros & Cons

### Strengths

1. **Captures Big Trends**: 32.8% initial target reflects trend-following positioning
2. **No Need for Constant Monitoring**: 12h timeframe; low signal frequency
3. **Volatility Leads**: Enter before breakout; enjoy main wave
4. **Clear Risk Control**: Hard stop-loss + Trailing stop dual protection

### Weaknesses

1. **Long Holding Period**: Can exceed 7 days; long capital occupation
2. **Low Signal Frequency**: Requires patience to wait for opportunities
3. **Tight Stop-Loss Risk**: -4.66% may be triggered by normal volatility
4. **Not Suitable for Impatient**: Requires extreme patience

---

## VIII. Applicable Scenarios

| Market Environment | Recommendation | Notes |
|-------------------|---------------|-------|
| Post-Low-Volatility Breakout | Strongly Recommended | Core scenario; volatility compression then release |
| Trend Continuation | Recommended | Hold along with trend direction |
| Ranging Market | Not Recommended | Cannot form effective breakout |
| Unilateral Downward | Not Recommended | May continuously trigger stop-loss |

---

## IX. Applicable Market Environment Analysis

Heracles is a typical **volatility breakout strategy**. Based on its code architecture and logic, it is best suited for **trend breakout opportunities after low volatility**, and performs poorly in ranging or declining markets.

### 9.1 Strategy Core Logic

- **Volatility Compression Recognition**: Donchian Percentile below Keltner Width
- **Trend-Following Positioning**: Enter before breakout; enjoy main wave
- **Momentum Exit Mechanism**: Exit when MACD Signal crosses below EMA

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:-----------|:------:|:---------|
| Post-Low-Volatility Breakout | ★★★★★ | Core scenario; volatility compression then release |
| Trend Continuation | ★★★★☆ | Follow trend; capture profits |
| Ranging Market | ★★☆☆☆ | Frequent stop-losses; cannot form effective trend |
| Unilateral Downward | ★☆☆☆☆ | May suffer continuous stop-losses |

### 9.3 Key Configuration Recommendations

| Config Item | Suggested Value | Notes |
|------------|---------------|-------|
| Timeframe | 12h | Maintain ultra-long-term positioning |
| stoploss | -0.04 ~ -0.05 | Adjust based on pair volatility |
| trailing_stop_positive | 0.02 ~ 0.03 | Early profit lock-in |

---

## X. Important Notes: The Cost of Ultra-Long-Term Holding

### 10.1 Time Cost

Heracles' ultra-long-term characteristics bring special considerations:

| Dimension | Impact |
|---------|--------|
| Capital Occupation | May exceed 7 days |
| Opportunity Cost | Cannot participate in other trading opportunities |
| Psychological Pressure | Anxiety from prolonged holding |

### 10.2 Execution Recommendations

**Suitable For**:
- ✅ Patient trend investors
- ✅ Office workers unable to monitor frequently
- ✅ Traders pursuing big trends

**Not Suitable For**:
- ❌ Impatient traders
- ❌ People who like short-term quick in-and-out
- ❌ Small-capital traders needing high-frequency turnover

### 10.3 Backtesting vs. Live Trading Differences

**Notes**:
- 12h timeframe has few signals; backtesting sample may be insufficient
- Overnight risk during holding period needs consideration
- Long holding may miss other opportunities

### 10.4 Manual Trading Suggestions

If you want to manually apply this strategy's logic:
1. Use Keltner Channel to observe volatility width
2. Use Donchian Channel to judge price position
3. Prepare to enter when volatility compresses to its extreme
4. Set clear stop-loss level; strictly enforce

---

## XI. Summary

**Heracles** is an ultra-long-term trend strategy focused on volatility breakout. Its core value lies in:

1. **Volatility Compression Capture**: Enter during market energy accumulation stage; enjoy main wave after breakout
2. **Ultra-Long-Term Positioning**: 12h timeframe; holding up to 7+ days; suitable for patient investors
3. **Clear Risk Control**: Hard stop-loss + Trailing stop + Time stop triple protection

For quantitative traders, Heracles is a typical volatility breakout strategy template, suitable for finding entry opportunities during low-volatility periods. Note the capital occupation and psychological pressure from ultra-long-term holding; recommended to use with position management and mindset adjustment.

**One-Line Evaluation**: Ultra-long-term player; holds for a week at a time; suitable for patient trend investors.

---
