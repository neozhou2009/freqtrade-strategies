# Strategy003: The Picky Bottom-Fisher

> **Nickname**: The Eight-Condition Master
> **Occupation**: Professional Selective Bottom-Fisher
> **Timeframe**: 5-minute chart

---

## I. What is This Strategy?

Simply put, **Strategy003** is:
- A "pickier" bottom-fishing strategy than Strategy002
- Needs 8 conditions met before taking action
- Added trend filtering to avoid bottom-fishing against the trend

It's like someone whose dating requirements are "must have house, car, savings, height, education, looks, healthy parents, and good personality" - the more conditions, the fewer candidates 🤣

---

## II. Core Configuration: Same as Strategy002

### Take-Profit Rules (ROI Table)

```
Holding Time     Target Profit
─────────────────────────────
Just bought      5%
20 minutes later 4%
30 minutes later 3%
60 minutes later 1%
```

**Translation**: Same tiered take-profit as Strategy002, the longer you hold, the lower the requirement.

### Stop-Loss Rules

```
Hard Stop-Loss: Forced exit at 10% loss
Trailing Stop: If you've made 2%, exit when it drops back 1%
```

**Translation**: Same stop-loss strategy as Strategy002, no need to explain again.

---

## III. Buy Conditions: All Eight Must Be Met

This strategy's buy conditions are much more complex than Strategy002, with 8 sub-conditions divided into groups:

### 🎯 Group 1: Deep Oversold Confirmation (3 conditions)

| Condition | Indicator | Requirement | Plain English |
|-----------|-----------|-------------|---------------|
| #1 | RSI | < 28 | "SUPER oversold!" (stricter than 30) |
| #2 | RSI | > 0 | "Data is valid" (exclude anomalies) |
| #3 | Fisher RSI | < -0.94 | "EXTREME oversold!" (near the -1 limit) |

**Plain English**:
> Strategy: "RSI needs to be below 28, not 30, need it more extreme!"
> Strategy: "Fisher RSI also needs to be below -0.94, almost at -1!"
>
> This is looking for that "can't fall any further" extreme oversold state.

### 🎯 Group 2: Money Depletion Confirmation (1 condition)

| Condition | Indicator | Requirement | Plain English |
|-----------|-----------|-------------|---------------|
| #4 | MFI | < 16.0 | "Everyone who wanted to sell has sold" |

**Plain English**:
> MFI is the Money Flow Index, below 16 means selling pressure is fully released.
> It's like a store clearance sale - all inventory is gone, no one left to sell.

### 🎯 Group 3: Price Low Position Confirmation (1 condition)

| Condition | Indicator | Requirement | Plain English |
|-----------|-----------|-------------|---------------|
| #5 | Close vs SMA40 | Price < SMA | "Price below mid-term moving average" |

**Plain English**:
> SMA40 is the 40-period simple moving average, price needs to be below this line.
> Ensures you're really buying at a "low position," not chasing highs.

### 🎯 Group 4: Trend Filter (choose 1 of 2)

| Condition | Indicator | Requirement | Plain English |
|-----------|-----------|-------------|---------------|
| #6a | EMA50 vs EMA100 | EMA50 > EMA100 | "Mid-term trend is up" |
| #6b | EMA5 vs EMA10 | Golden cross | "Short-term starting to bounce" |

**Plain English**:
> This group is "either/or":
> - Either EMA50 is above EMA100 (mid-term trend upward)
> - Or EMA5 just crossed above EMA10 (short-term bounce starting)
>
> This is **not bottom-fishing against the trend!** If the trend is still going down, even if oversold, won't buy.

### 🎯 Group 5: Momentum Reversal Confirmation (2 conditions)

| Condition | Indicator | Requirement | Plain English |
|-----------|-----------|-------------|---------------|
| #7 | FastD vs FastK | FastD > FastK | "Momentum starting to go up" |
| #8 | FastD | > 0 | "Momentum is valid" |

**Plain English**:
> Stochastic Fast's D line needs to be above the K line, showing momentum is turning upward.
> And D line must be greater than 0, excluding anomalies.

---

## IV. Protection Mechanism: Same as Strategy002

| Protection Type | Trigger Condition | Plain English |
|-----------------|-------------------|---------------|
| Fixed Stop-Loss | 10% loss | "Lost too much, accept it and leave" |
| Trailing Stop | Profit drawdown 1% (after profit > 2%) | "Made money and want to run? Not so fast!" |

**Critique**: The conditions doubled compared to Strategy002, but stop-loss settings are exactly the same. This might be an area for optimization - theoretically, stricter conditions could accept looser stop-losses?

---

## V. Sell Logic: Same as Strategy002

The sell signal is simple:

```python
SAR > Close Price  AND  Fisher RSI > 0.3
```

**Plain English**:

1. **SAR > Close Price**: Price broke below the SAR "umbrella"
2. **Fisher RSI > 0.3**: Momentum has exited the extreme oversold zone

> Strategy: "SAR has flipped, Fisher RSI has also left extreme oversold..."
> Strategy: "**SELL!**"

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Time)

1. **High Signal Quality**: 8 conditions filter out only "premium picks"
2. **Has Trend Filter**: Doesn't bottom-fish against the trend, avoids catching falling knives
3. **Money Flow Confirmation**: MFI ensures selling pressure is fully released
4. **Extreme Value Capture**: Fisher RSI < -0.94 captures true bottoms

### ⚠️ Cons (Critique Time)

1. **Too Few Signals**: 8 conditions all met? Might wait forever 🙄
2. **Overfitting Risk**: More conditions = better historical performance, worse live trading
3. **Missing Opportunities**: Waiting for "perfect signals" might miss good bounces
4. **Hard to Debug**: 8 conditions, hard to troubleshoot when something goes wrong

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|--------------------|----------------|--------|
| Reversal after deep correction | ✅ Recommended | Designed exactly for this scenario |
| Oscillating downtrend | ✅ Can use | Can capture high-quality signals |
| Continuous crash | ⚠️ Use cautiously | Conditions too strict, might miss |
| One-way uptrend | ❌ Don't use | No buy opportunities |

---

## VIII. Summary: How Good Is This Strategy?

### One-Sentence Review
> "A quality-over-quantity bottom-fisher, filtering premium picks with eight conditions"

### Who Should Use It?
- ✅ Traders who prioritize signal quality
- ✅ People who don't mind low trading frequency
- ✅ Those who want to avoid false signals
- ✅ Patient people who can wait

### Who Should NOT Use It?
- ❌ People who want frequent trades
- ❌ People who don't like waiting
- ❌ Trend-following traders
- ❌ People without patience to debug parameters

### My Recommendations

1. **Backtest against Strategy002**: See if the extra 4 conditions really improved win rate
2. **Consider relaxing some conditions**: e.g., RSI < 28 to < 30, Fisher RSI < -0.94 to < -0.9
3. **Keep the trend filter**: EMA trend filter is good stuff, recommend keeping
4. **Small position testing**: Few signals, go light and slow

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: The Art of Selectivity

Strategy003's philosophy is: **Better to miss than to make mistakes.**

Unlike Strategy002 which buys when "four conditions are met," it requires "all eight conditions in place." It's like dating - Strategy002 says "just needs a house," Strategy003 says "needs house, car, savings, height, education, looks, healthy parents, and good personality" - more conditions means (theoretically) higher success rate, but fewer opportunities.

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Reversal after deep correction | ⭐⭐⭐⭐⭐ | This strategy was born for this scenario |
| 🔄 Oscillating downtrend | ⭐⭐⭐⭐☆ | Can catch high-quality bounces, but few signals |
| 📉 Continuous crash | ⭐⭐☆☆☆ | Conditions too strict, might not get a single signal |
| ⚡️ One-way uptrend | ⭐☆☆☆☆ | Nothing for you here, go home and rest |

**One-Sentence Summary**: **Those who can wait should use it, those who can't should go around.**

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Comment |
|-------------------|-----------------|---------|
| Number of trading pairs | 20-50 | Too few signals, need more targets |
| Timeframe | 5m | Default setting, don't change |

### 10.2 Parameter Tuning Recommendations

| Parameter | Default Value | Try Adjusting | Reason |
|-----------|---------------|---------------|--------|
| RSI | < 28 | 30 | Slightly relax, increase signals |
| Fisher RSI | < -0.94 | -0.9 | Slightly relax |
| MFI | < 16 | 20 | Slightly relax |
| EMA group | Keep | - | Trend filter is important |

### 10.3 Hardware Requirements

This strategy needs a bit more computing power, but still manageable:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-10 | 2GB | 4GB | Smooth |
| 10-50 | 4GB | 8GB | Stable |

---

## XI. Bonus: Strategy002 vs Strategy003 Comparison

| Comparison Item | Strategy002 | Strategy003 |
|-----------------|-------------|-------------|
| Number of buy conditions | 4 | 8 |
| RSI threshold | < 30 | < 28 |
| Money flow indicator | None | MFI < 16 |
| Trend filter | None | EMA moving average group |
| Oversold confirmation | Bollinger lower band | Fisher RSI < -0.94 |
| Pattern confirmation | Hammer | None |
| Signal frequency | Low | Very low |
| Theoretical win rate | Medium | High (theoretically) |
| Debugging difficulty | Simple | Medium |

**The Author's Thinking**:
> Strategy003 seems to be an "evolved version" of Strategy002. The author felt 4 conditions weren't enough, so added 4 more.
>
> But... are more conditions really better?
>
> Backtesting might look great, but live trading might have almost no signals in a year.
>
> Recommend backtesting both strategies yourself before deciding which to use.

---

## XII. The Very End

### One-Sentence Review
> "A strictly selective bottom-fishing strategy, for patient quality-seekers"

### Who Should Use It?
- ✅ People who prefer high win rate over high frequency
- ✅ People with patience to wait for signals
- ✅ People who dislike false signals
- ✅ People who want to learn multi-indicator combinations

### Who Should NOT Use It?
- ❌ People who want frequent trades
- ❌ Impatient people
- ❌ People who don't like debugging parameters
- ❌ People expecting daily operations

### Manual Trader Recommendations

If you're a manual trader, this strategy's logic can be simplified:

1. Find coins with RSI < 28
2. Check if Fisher RSI is also < -0.94
3. Check if MFI is < 16
4. See if EMA50 is above EMA100 (trend upward)
5. If all met, consider entering

---

## XIII. ⚠️ Risk Reminder Again (Read This Part!)

### Backtesting Looks Great, Live Trading Needs Caution

Strategy003's biggest risk is **overfitting**:

> **More conditions make it easier to "fit" parameter combinations that look good historically.**

Simply put: **You memorized past test answers, but next time the exam questions are different.**

### Hidden Risks of Complex Strategies

- **Too Few Signals**: Might go months without a signal, easy to lose patience
- **Missing Opportunities**: Waiting for "perfect signals" might miss lots of profitable opportunities
- **Hard to Debug**: 8 conditions, hard to troubleshoot which one is wrong
- **Live Trading Deviation**: Good historical performance ≠ good future performance

### My Recommendations (Real Talk)

```
1. Backtest against Strategy002, see if added conditions really help
2. Consider relaxing some conditions, increase signal frequency
3. Keep the trend filter (EMA group), this is the essence
4. Small position testing, don't go all-in
5. If signals are really too few, consider reducing condition count
```

**Remember**: No matter how good the strategy is, no signals means useless. More conditions are a double-edged sword - used well it's selection, used poorly it's self-comfort. 🙏

---