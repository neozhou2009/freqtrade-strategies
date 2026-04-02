# Stavix2 Strategy: The "Long-Period" School of Cloud Believers

> **Nickname**: The Cloud Watcher  
> **Profession**: Ichimoku Cloud Trend-Follower  
> **Timeframe**: 1 minute (1m) — but parameters are "long"

---

## I. What Is This Strategy?

Simply put, **Stavix2** is:
- Completely relies on Ichimoku cloud for decisions
- Uses ultra-long period parameters (200/350) to filter noise
- Pursues trending markets, would rather miss than be wrong

Like **a patient hunter, crouching above the cloud waiting for trends, never pulling the trigger until the critical moment** 🎯

---

## II. Core Configuration: Simply Put, "Won't Leave Until 15% Profit"

### Take-Profit Rule (ROI Table)

```
Target profit: 15%
Won't leave until 15%
```

**Translation**: This strategy doesn't chase small gains, waits for big trends when it sees them.

### Stop-Loss Rule

```
Maximum loss: 10%
```

**Translation**: Gives trend markets enough breathing room, 10% stop-loss is medium to loose.

### Risk-Reward Ratio

```
Take-Profit : Stop-Loss = 15% : 10% = 1.5 : 1
```

**Translation**: One win covers 1.5 losses, reasonable risk-reward ratio.

---

## III. Single Buy Signal: Three Conditions All Must Be Met

This strategy's buy conditions are simple but strict, **three conditions must all be met**:

### 🎯 Single Entry Signal (All 3 conditions required)

**In plain English**:
> "I want to wait until price is completely above the cloud, AND the base line crosses above the conversion line - then I buy!"

**Translated to human language**:

| Condition | Code | Plain English |
|------|------|--------|
| Cloud Confirmation 1 | `close > senkou_span_a` | Close above cloud upper boundary |
| Cloud Confirmation 2 | `close > senkou_span_b` | Close above cloud lower boundary |
| Crossover Signal | `kijun_sen crosses above tenkan_sen` | Base line crosses above conversion line |

**Wait, there's a problem!**

In traditional Ichimoku:
- Conversion line crossing above base line = Buy signal
- Base line crossing above conversion line = Sell signal

But this strategy **reversed it!** It uses "base line crosses above conversion line" as buy signal.

> Either the author has a unique understanding, or it's optimization for specific markets. Anyway, this is non-traditional usage. 🤔

---

## IV. Single Sell Signal: Also Three Conditions

Sell logic is symmetric with buy:

### 🚪 Single Exit Signal (All 3 conditions required)

**In plain English**:
> "Price completely fell below the cloud, AND conversion line crosses above base line - then I surrender and leave!"

| Condition | Code | Plain English |
|------|------|--------|
| Cloud Confirmation 1 | `close < senkou_span_a` | Close below cloud upper boundary |
| Cloud Confirmation 2 | `close < senkou_span_b` | Close below cloud lower boundary |
| Crossover Signal | `tenkan_sen crosses above kijun_sen` | Conversion line crosses above base line |

**Reversed again!**

The sell signal uses "conversion line crosses above base line", which is a buy signal in traditional Ichimoku!

> Summary: This strategy's buy/sell signals are completely opposite to traditional Ichimoku. The author may have their own market understanding. 😏

---

## V. Ichimoku Parameters: "Slower" Than Standard by a Dozen Times

This is Stavix2's most unique feature — **ultra-long period parameters**:

### Cloud Parameter Comparison

| Parameter | Standard Value | This Strategy | Difference |
|------|--------|--------|------|
| Conversion Line (Tenkan) | 9 periods | **200 periods** | 22x! |
| Base Line (Kijun) | 26 periods | **350 periods** | 13x! |
| Lagging Span | 26 periods | **150 periods** | 6x! |
| Displacement | 26 periods | **75 periods** | 3x! |

### Converted to Actual Time (1-Minute Chart)

| Parameter | This Strategy | Actual Time |
|------|--------|---------|
| Conversion Line | 200 periods | 3.3 hours |
| Base Line | 350 periods | 5.8 hours |
| Lagging Span | 150 periods | 2.5 hours |
| Displacement | 75 periods | 1.25 hours |

**Rant**:
> Using 3-6 hour level trend lines on a 1-minute chart, this parameter choice feels like "using a sledgehammer to crack a nut". Either the author wants extreme smoothing, or the parameters aren't matched well. 😅

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **Minimalist Code**: Core logic under 30 lines, clean and neat
2. **Strong Trend Confirmation**: Triple AND condition, high signal quality
3. **Good Noise Filtering**: Ultra-long period parameters, not easily fooled by false signals
4. **Reasonable Risk-Reward**: 1.5:1 risk-reward ratio is decent
5. **Easy Visualization**: Ichimoku cloud can be drawn directly,一目了然

### ⚠️ Cons (Rant Time)

1. **Sparse Signals**: Long-period parameters = few signals, possibly no trades for days
2. **Parameter Mismatch**: 1-minute timeframe + 200/350 period parameters, doesn't fit well
3. **Non-Traditional Logic**: Buy/sell signals opposite to standard Ichimoku, confusing
4. **Single Indicator**: No volume, momentum or other auxiliary confirmation
5. **Not for Ranging**: Almost zero signals during sideways

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| Clear Trend | ✅ Use | Cloud effectively identifies trend direction |
| Sideways Ranging | ❌ Don't Use | Sparse signals, possibly false breakouts |
| High Volatility Trend | ✅ Use | Long period can filter noise |
| Low Volatility | ⚠️ Use Less | Cloud signals too slow |

---

## VIII. Conclusion: How's This Strategy Really?

### One-Sentence Verdict
> "Minimalist cloud strategy believer — little code, pure logic, few signals, long wait. For patient trend traders."

### Who Should Use It?
- ✅ Trend traders who believe in Ichimoku
- ✅ People with patience to wait for signals
- ✅ Not pursuing high-frequency trading
- ✅ People who like simple strategies

### Who Shouldn't Use It?
- ❌ People pursuing high-frequency signals
- ❌ Ranging market traders
- ❌ Newbies unfamiliar with Ichimoku
- ❌ Wanting quick strategy validation

### My Recommendations
1. **Adjust Timeframe**: Consider using 5m or 15m charts, parameters will match better
2. **Add Confirmation Indicators**: Can add RSI or MACD for auxiliary confirmation
3. **Mental Preparation**: Possibly long periods without signals, need patience
4. **Backtest Verification**: Must backtest, see if signal frequency meets expectations

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Cloud Trend Following

Stavix2 is a **trend-following representative**. Core philosophy:
- Price above cloud = Bullish market
- Price below cloud = Bearish market
- Only trade when trend is clear

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | Above-cloud buy signals accurate, follow the trend |
| 🔄 Sideways Ranging | ⭐⭐☆☆☆ | Sparse signals, occasional false breakouts |
| 📉 Clear Downtrend | ⭐⭐⭐☆☆ | Will sell and go flat, but won't make money |
| ⚡️ High Volatility No Trend | ⭐☆☆☆☆ | Frequent cloud crossings, many false signals |

**One-Sentence Summary**:
> "Only strikes when trend is clear. No trend? Then wait."

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Rant |
|--------|--------|------|
| Trading Pair Selection | Strong trending coins | Ranging coins have pitifully few signals |
| Timeframe | 5m or 15m better | 1m + long-period parameters doesn't fit well |
| Signal Frequency Expectation | 0-5 trades per day | Long period = few signals |

### 10.2 Hardware Requirements (Don't Need Much)

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|-----------|---------|---------|
| Any | 2GB | 4GB |

> Strategy calculation is minimal, any computer can run it.

### 10.3 Backtest vs. Live Trading

**Backtest Might Show**:
- Very few signals
- But single trade profit may be high

**Live Trading Might Encounter**:
- Waiting for signals until flowers wilt
- May react slowly when trend reverses

**Recommended Process**:
1. First backtest on 5m or 15m timeframe
2. See if signal frequency is acceptable
3. Then consider 1m timeframe live trading

---

## XI. Bonus: Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find:

1. **Only Ichimoku, no other indicators**:
   > "Less is more? Or too lazy to add?"

2. **Extremely exaggerated parameters**:
   > "200/350 periods, using on 1-minute chart — identifying half-day level trends"

3. **Buy/sell signals reversed from tradition**:
   > "Base line crosses above conversion line to buy? Not according to textbooks. Author may have their own market insights."

4. **Code minimalism to the extreme**:
   > "populate_indicators only has cloud, populate_entry_trend and populate_exit_trend each have 3 conditions. 30 lines of code done."

---

## XII. Finally, Finally

### One-Sentence Verdict
> "Minimalist cloud strategy — few signals, long wait, strong trends. For patient trend believers."

### Who Should Use It?
- ✅ People who believe in Ichimoku
- ✅ Patient trend traders
- ✅ Like simple strategies
- ✅ Can accept long periods without signals

### Who Shouldn't Use It?
- ❌ Pursuing high-frequency trading
- ❌ Ranging market traders
- ❌ Unfamiliar with Ichimoku
- ❌ Wanting quick validation

### Manual Trader Advice
This strategy is actually quite suitable for manual trading!
- Ichimoku cloud visualization is effective
- Conditions simple, manual judgment totally feasible
- Don't need to stare at 1-minute chart, can look at larger timeframes

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Parameter Mismatch Issue

This strategy's biggest issue: **1-minute timeframe + 200/350 period parameters**

```
Problem Analysis:
- 200 periods × 1 minute = 3.3-hour trend line
- 350 periods × 1 minute = 5.8-hour trend line
```

This means:
- Using half-day level trend confirmation on 1-minute chart
- Signals will be very sparse
- May miss many 1-minute level opportunities

### Risk of Sparse Signals

In live trading, you might encounter:
- **No trades for days**: Long-period parameters + AND conditions
- **Slow trend reversal**: By the time signal appears, trend has moved a bit
- **Missing fast moves**: Short-period fluctuations can't be captured

### My Recommendations (Real Talk)

```
1. Consider changing timeframe to 5m or 15m
2. Or reduce period parameters to standard values (9/26/52)
3. Add a confirmation indicator (RSI/MACD) to reduce false signals
4. Backtest to confirm signal frequency meets expectations
5. Prepare to wait patiently
```

**Remember**: No matter how good the strategy is, mismatched timeframe and parameters will greatly reduce effectiveness. Either change timeframe, or change parameters, don't force it.

---

**Final Reminder**: Ichimoku is a good tool, but parameters and timeframe must match. Don't use a stopwatch to time a marathon, and don't use a sundial to time a 100-meter sprint. 🙏