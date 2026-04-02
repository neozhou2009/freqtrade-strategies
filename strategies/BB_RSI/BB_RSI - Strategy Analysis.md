# BB_RSI Strategy Analysis

> **Strategy Number**: #43
> **Strategy Type**: Bollinger Band Mean Reversion + RSI Oversold
> **Timeframe**: 1 hour (1h)

---

## I. Strategy Overview

BB_RSI is a **simple yet effective Bollinger Band RSI combination strategy**, following classic price reversion theory — buy when price touches lower Bollinger Band and RSI is in oversold state, sell when price touches upper band and RSI is overbought. Developed by Leandro Handal, the code is concise and clear, making it an excellent case for quantitative trading beginners to learn and reference.

The strategy's design philosophy is based on **mean reversion principle** in statistics: price won't deviate from value forever — it will eventually return to reasonable levels. Bollinger Bands provide reference for extreme price positions, while RSI confirms market overbought/oversold state. The combination greatly improves signal quality.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Price < BB lower band + RSI > 7 |
| **Exit Conditions** | Price > BB upper band + RSI > 74 |
| **Protection** | Fixed stoploss -6.5%, trailing stop enabled |
| **Timeframe** | 1h |
| **Dependencies** | technical (qtpylib), talib |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
minimal_roi = {
    "0": 0.4,           # Immediate take-profit 40%!
    "335": 0.18834,    # 18.8% after 335 candles
    "564": 0.07349,    # 7.3% after 564 candles
    "1097": 0          # After that, rely on ROI
}

stoploss = -0.06491    # Stoploss -6.5%

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01036
trailing_stop_positive_offset = 0.02409
```

**Configuration Logic Analysis**:

- **minimal_roi Design**: Strategy adopts very aggressive initial take-profit target — 40%! This is an extremely high take-profit point, reflecting strategy designer's pursuit of high-certainty signals. Entry only triggered when price touches extreme Bollinger Band positions, expecting large rebound. As time extends, take-profit target gradually decreases: drops to 18.8% after 335 candles (about 14 days), to 7.3% after 564 candles (about 24 days), completely relies on trailing stop after 1097 candles (about 46 days). This design allows strategy to continue holding in long-term trend markets.

- **stoploss -6.5%**: This is a relatively conservative stoploss amplitude. Combined with 40% extremely high initial take-profit, profit/loss ratio is about 6.15:1 — profitable even with low win rate. Conservative stoploss design based on following assumption: after buying at extreme Bollinger Band positions, limited room for further decline.

- **trailing_stop Configuration**: Trailing stop activates after profit exceeds 2.41%, stoploss line moves up to lock 1.04% profit. This conservative trailing stop design aims to protect partial profits, but won't exit too early.

---

## III. Entry Conditions Details

### 3.1 Complete Entry Conditions

```python
dataframe.loc[
    (
        (dataframe["close"] < dataframe["bb_lowerband"])
        & (dataframe["rsi"] > 7)
    ),
    "entry"
] = 1
```

**Condition-by-Condition Analysis**:

**Condition One: Close Price < Bollinger Band Lower Band**

```python
dataframe["close"] < dataframe["bb_lowerband"]
```

- Bollinger Band lower band usually set at 2 standard deviations, representing statistical lower boundary of price
- Price below lower band indicates price has extremely deviated from mean
- This is core assumption of mean reversion trading

**Condition Two: RSI > 7**

```python
dataframe["rsi"] > 7
```

- RSI > 7 is a very subtle condition
- Purpose is to filter out situations where RSI is extremely oversold (close to 0)
- When RSI approaches 0, usually means downtrend is very strong — mean reversion may take longer
- RSI > 7 indicates although market is oversold, not yet to "despair" level — rebound probability higher

### 3.2 Overall Interpretation of Entry Logic

BB_RSI's entry logic is **dual extreme confirmation**:

1. **Price Extreme**: Price touches lower Bollinger Band, indicating price is extremely cheap
2. **Momentum Extreme but Not Excessive**: RSI in oversold region but not to extreme, retaining rebound space

This design ensures market is already in extreme state when buying, while retaining sufficient rebound momentum.

### 3.3 Limitations of Entry Conditions

- **No trend judgment**: Doesn't check market trend direction — may buy against trend in downtrend
- **Fixed RSI threshold**: 7 is very low threshold — may filter out some valid signals
- **Long only**: No shorting opportunities

---

## IV. Exit Conditions Details

### 4.1 Complete Exit Conditions

```python
dataframe.loc[
    (
        (dataframe["close"] > dataframe["bb_upperband"])
        & (dataframe["rsi"] > 74)
    ),
    "exit"
] = 1
```

**Condition Analysis**:

**Condition One: Close Price > Bollinger Band Upper Band**

```python
dataframe["close"] > dataframe["bb_upperband"]
```

- Price above upper band indicates price has extremely deviated from mean
- Suggests price may be "overvalued"

**Condition Two: RSI > 74**

```python
dataframe["rsi"] > 74
```

- RSI > 74 indicates market is in overbought state
- This is sell signal in traditional technical analysis

### 4.2 Overall Interpretation of Exit Logic

BB_RSI's exit logic is **symmetric extreme confirmation**:

- Price touches upper band (extremely overvalued)
- RSI confirms overbought (excessive momentum)

### 4.3 Take-Profit Strategy Details

| Holding Time | Take-Profit Target | Design Intent |
|-------------|-------------------|---------------|
| 0-14 days | 40% | Capture large rebound |
| 14-24 days | 18.8% | Medium-term continued profit |
| 24-46 days | 7.3% | Prevent profit giveback |
| 46 days+ | 0% | Completely rely on trailing stop |

### 4.4 Stoploss Mechanism

- **Fixed Stoploss**: -6.5%
- **Trailing Stop**: Activates after profit > 2.41%, locks 1.04% profit

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator | Parameters | Usage |
|-----------|------------|-------|
| RSI | period=14 | Identify overbought/oversold state |
| Bollinger Bands | window=20, stds=1 | Identify extreme price positions |

### 5.2 RSI Details

**Parameter Configuration**: period=14

- 14 is RSI default parameter — balances response speed and stability
- 14 days sufficient to cover complete market cycle

**Unique Application of RSI in This Strategy**:

- **When Buying**: RSI > 7 (rather than traditional < 30)
  - This is a very low selection
  - Purpose is to filter RSI extremely oversold situations
  - 7 means market just started oversold — still has rebound space

- **When Selling**: RSI > 74 (rather than traditional > 70)
  - This is a higher overbought threshold
  - Only sell when RSI reaches extremely high level
  - This design allows profits to fully run

### 5.3 Bollinger Bands Details

**Parameter Configuration**: window=20, stds=1

- **Special Note**: Uses 1 standard deviation here, rather than traditional 2
- 1 standard deviation covers about 68% of price distribution
- This means signals trigger more frequently — price更容易 touches 1 standard deviation boundary

| Bollinger Band Level | Coverage Range | Signal Frequency |
|---------------------|----------------|------------------|
| 1 Standard Deviation | 68% | High |
| 2 Standard Deviations | 95% | Medium |
| 3 Standard Deviations | 99.7% | Low |

---

## VI. Risk Management Features

### 6.1 Risk-Return Characteristics

| Dimension | Assessment |
|-----------|------------|
| Maximum Theoretical Loss | -6.5% (fixed stoploss) |
| Maximum Theoretical Profit | Unlimited (40%+ take-profit) |
| Expected Profit/Loss Ratio | About 6.15:1 (extremely high) |
| Signal Frequency | Low (requires price to touch extreme positions) |

### 6.2 Risk Control Mechanisms

| Mechanism | Description | Evaluation |
|-----------|-------------|------------|
| Fixed Stoploss | -6.5% | Conservative — gives enough rebound space |
| Conservative Trailing Stop | 2.41% trigger | May exit too early |
| RSI Filter | RSI > 7 buy | Unique design — filters extreme situations |

### 6.3 Risk Management Design Philosophy

- **High take-profit low stoploss**: 40% take-profit vs 6.5% stoploss design shows strategy pursues high certainty
- **Scarce signals**: Only triggers when price touches extreme positions — ensures each trade has large space
- **Allow profits to run**: 40% initial take-profit shows strategy not in hurry to exit

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Extremely simple**: Very small code volume — only 2 indicators, clear logic
2. **Classic combination**: Bollinger Band + RSI is technical analysis combination verified over decades
3. **Clear buy/sell points**: Conditions clear — not ambiguous — easy to execute
4. **No parameter tuning**: No need for complex hyperparameter optimization
5. **High profit/loss ratio**: 40% vs 6.5% design means doesn't need high win rate
6. **Conservative stoploss**: 6.5% stoploss relatively safe

### ⚠️ Cons

1. **Scarce signals**: Requires price to touch BB edges to trigger — may have no trades for long time
2. **No protection mechanisms**: No BTC correlation protection
3. **High take-profit hard to reach**: 40% initial take-profit may be difficult to trigger frequently in practice
4. **Ignores trend**: Doesn't consider trend direction — may buy against trend in downtrend
5. **Long only**: No shorting opportunities
6. **Special RSI threshold**: 7 is very low threshold — may not apply to all markets

---

## VIII. Parameter Optimization

| Parameter Category | Optimization Priority | Notes |
|-------------------|----------------------|-------|
| RSI Thresholds | Medium | Affects signal quality |
| BB Standard Deviations | Medium | Affects signal frequency |
| ROI Table | Low | Can adjust based on market |
| Stoploss | Low | Conservative design works well |

---

## IX. Live Trading Notes

### 9.1 Learning Curve

**Entry Difficulty**: ★☆☆☆☆ (Extremely Low)

This is an extremely concise strategy — very suitable for beginners:

- Only 2 core indicators
- Buy/sell conditions simple and clear
- No parameter optimization needed
- Very small code volume

### 9.2 Hardware & Resource Requirements

| Item | Requirement | Explanation |
|------|-------------|-------------|
| Computing Resources | Extremely Low | Only need to calculate RSI and Bollinger Bands |
| Memory Usage | Extremely Low | Few indicators |
| Network Requirements | Low | 1-hour data volume small |

### 9.3 Psychological Requirements

- **Patience**: Scarce signals — need long waiting
- **Discipline**: Must strictly execute stoploss
- **Error tolerance**: Accept 40% take-profit may be difficult to achieve
- **Don't rush**: Don't adjust strategy due to long time without signals

### 9.4 Risks to Note

1. **Scarce signal risk**: May have no trades for weeks
2. **Trend risk**: Doesn't judge trend — may trade against trend
3. **High take-profit risk**: 40% take-profit may be difficult to achieve
4. **Fixed parameter risk**: RSI > 7 threshold may not apply to all markets

---

## X. Summary

### 10.1 Core Evaluation

BB_RSI is a **simple yet effective** Bollinger Band RSI combination strategy. Its core value lies in **classic combination and high profit/loss ratio**. Strategy follows classic price reversion theory — identifies extreme price positions through Bollinger Bands, confirms overbought/oversold state through RSI. The combination greatly improves signal quality.

This strategy is especially suitable for:
- Quantitative trading beginners learning strategy design
- Investors pursuing simple trading
- Traders with patience to wait for high-certainty signals

### 10.2 Suitable For

| Investor Type | Suitability | Reason |
|--------------|-------------|--------|
| Quant Newbies | ⭐⭐⭐⭐⭐ | Extremely simple strategy — classic combination |
| Conservative Investors | ⭐⭐⭐⭐☆ | Conservative stoploss — clear signals |
| Medium-term Traders | ⭐⭐⭐⭐☆ | 1-hour timeframe |
| Aggressive Traders | ⭐⭐☆☆☆ | Scarce signals — may not be exciting enough |
| Short-term Traders | ⭐☆☆☆☆ | Not suitable |

### 10.3 Improvement Suggestions

If hoping to enhance this strategy, consider:

1. **Add trend filter**: Use 200-day moving average to judge market direction — only buy in uptrend
2. **Adjust RSI threshold**: Change RSI > 7 to more traditional < 30
3. **Add volume confirmation**: Require volume cooperation
4. **Reduce take-profit target**: Change 40% to 20-25%
5. **Add market correlation protection**: Pause buying during BTC decline

---

*This document is based on strategy code*
