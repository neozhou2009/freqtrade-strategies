# DIV_v1 Strategy: In-Depth Analysis

## 1. Strategy Overview and Design Philosophy

### 1.1 Strategy Background and Origin

DIV_v1 is a quantitative implementation of a classic technical analysis theory — RSI Divergence trading strategy. Released by developer Sanka on September 7, 2021, its core design philosophy captures divergence between price and momentum indicators when markets enter oversold zones, thereby anticipating potential price reversal opportunities.

Divergence trading is one of the most valuable battlefield-proven trading methods in technical analysis. When price action and momentum indicators diverge, it often signals that the current trend momentum is exhausting and the market may be about to change direction. DIV_v1 programmatically implements this classic theory, automatically identifying divergence relationships between price lows and RSI indicator via precise mathematical algorithms.

Historical data shows divergence signals have high accuracy in predicting trend turning points. In ranging markets and trend pullback phases, effective divergence signals can achieve 60-70% win rates, making them one of the most valued signals by technical traders. However, divergence signals have obvious limitations — in one-directional trending markets, divergence signals often fail consecutively, leading to consecutive losses. DIV_v1's design fully considers this through multi-layer filtering mechanisms to improve signal reliability.

### 1.2 Core Design Philosophy

DIV_v1's design philosophy can be summarized as "momentum leads, reversal follows." This encompasses three core understandings:

**Layer 1: Momentum Precedes Price**

RSI, as a relative strength indicator, fundamentally measures the speed and magnitude of price changes. When price continuously falls but RSI stabilizes or rises, it conveys important information — although price is still declining, the speed and force of decline is weakening, selling momentum is exhausting, and buying support is accumulating. This momentum-level change often leads price-level reversals, providing traders with an early-positioned opportunity window.

**Layer 2: Divergence as Warning**

When price makes a new low but RSI does not make a new low (bullish divergence), it shows that although price is still making new lows, the momentum driving price down is weakening. This is a strong warning signal of imminent reversal.

**Layer 3: Oversold Zone Reliability**

The strategy strictly confines entry conditions to RSI < 30 oversold zone, significantly improving signal reliability. Divergence appearing in oversold zones has substantially higher reversal probability than divergence appearing in normal zones. The reason: oversold means the market has experienced significant decline, selling force is fully exhausted, and momentum exhaustion at this point is more likely a genuine trend reversal rather than a mid-decline consolidation.

### 1.3 Strategy Positioning and Applicable Scenarios

DIV_v1 is a typical short-term reversal strategy:
- **Trading Style**: Contrarian — enters on market over-sale, waits for price to revert to rationality
- **Holding Period**: Short to medium, typically minutes to hours
- **Risk-Return**: Medium risk, medium return
- **Best Market Environment**: Ranging markets, bull market pullbacks, moderate volatility
- **Unsuitable**: One-directional decline, extreme volatility

---

## 2. Technical Indicators Deep Dive

### 2.1 RSI (Relative Strength Index)

RSI is the core indicator of DIV_v1, introduced by J. Welles Wilder Jr. in 1978.

**Calculation**: RSI = 100 - (100 / (1 + RS)), where RS = average up amplitude / average down amplitude

**Parameters**: 14-period RSI (Wilder's standard):
```python
dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
```

**RSI Interpretation**:
- 70-100: Overbought zone
- 30-50: Oversold-adjacent zone
- 0-30: Oversold zone

DIV_v1's entry condition confines RSI to below 30 oversold zone — not simply using oversold signals, but finding divergence within oversold zones.

### 2.2 Divergence Detection Algorithm

The divergence detection is the most core logic, implemented in the `divergence()` function.

**Bullish Divergence Core Conditions**:
1. **Price makes new low**: Current ohlc_bottom < ohlc_bottom from i candles ago
2. **RSI does not make new low**: Current rsi_bottom > rsi_bottom from i candles ago
3. **Continuity confirmation**: Current recorded low not above previous candle's recorded low
4. **No intermediate disruption**: No lower price lows appear between two comparison points

**Time Window**: i ranges from 2 to 14, corresponding to 10-70 minutes on 5-minute timeframe.

---

## 3. Trading Signal Logic

### 3.1 Entry Signal Multi-Filter

DIV_v1's entry uses triple-filtering mechanism:

```python
dataframe.loc[
    (
        (dataframe["bullish_divergence"] == True) &
        (dataframe['rsi'] < 30) &
        (dataframe["volume"] > 0)
    ), 'buy'] = 1
```

**Condition 1**: Bullish divergence signal present
**Condition 2**: RSI in oversold zone (below 30)
**Condition 3**: Volume exists (execution feasibility)

### 3.2 Exit Signal Passive Design

`populate_exit_trend` returns empty DataFrame — exits entirely via ROI targets and stoploss:

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    return dataframe
```

This avoids overfitting from introducing additional prediction models for exit timing.

---

## 4. Risk Management

### 4.1 Fixed Stoploss

```python
stoploss = -0.15  # 15%
```

Balances giving price sufficient "breathing room" in pullback strategies while limiting maximum single-trade loss.

### 4.2 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.001  # 0.1%
trailing_stop_positive_offset = 0.02  # 2%
trailing_only_offset_is_reached = True
```

- Activates after 2% profit to confirm reversal success
- 0.1% tight trailing distance quickly exits on reversal failure
- Achieves "let profits run while protecting realized profits"

### 4.3 Tiered ROI

```python
minimal_roi = {
    "0": 0.103476,      # ~10.35%
    "3": 0.050496,      # ~5.05%
    "5": 0.033509,      # ~3.35%
    "61": 0.027522,      # ~2.75%
    "292": 0.005185,    # ~0.52%
    "399": 0            # 0%
}
```

Time-decreasing logic: rapidly rising prices = strong reversal, lock profits immediately; slowly rising prices = weaker reversal, lower expectations.

---

## 5. Strategy Pros & Cons

### Advantages

1. **Solid theoretical foundation**: Based on classic technical analysis theory validated over decades
2. **High signal quality**: Triple-filter mechanism ensures high-quality signals
3. **Complete risk management**: Fixed stoploss + trailing stop + decreasing ROI
4. **Strong parameter explainability**: Each parameter has clear financial meaning

### Limitations

1. **Underperforms in one-directional trends**: Consecutive divergence failures in strong trends
2. **Single-direction trading limitation**: Long-only, cannot profit from declining markets
3. **Lacks active exit logic**: Completely dependent on passive exits
4. **Parameter sensitivity**: Performance sensitive to parameter settings
