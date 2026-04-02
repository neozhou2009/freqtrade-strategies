# AdxSmas Strategy: The Trend Filter

> **Nickname**: Trend Quality Inspector, ADX Filter King  
> **Job**: Trend Trading 101  
> **Timeframe**: Hourly (1h)

---

## 1. What is This Strategy?

Simply put, **AdxSmas** is:
- First use ADX to check "does this market have a trend?"
- Only look at moving average crosses if there's a trend, lie flat if not
- Simple enough to have only 50 lines of code, beginner-level strategy

It's like **"a pedestrian who only crosses when there's a green light"** 🚦—ordinary MA strategies rush without looking, this strategy waits for ADX to say "there's a trend (green light)" before going, otherwise stays put during consolidation (red light).

---

## 2. Core Configuration: "Trade Based on Trend"

### Take Profit Rules (ROI Table)

```
Target ROI: 10%
```

**Translation**: Make 10% and leave, no greed.

### Stop Loss Rules

```
Fixed Stop Loss: -25%
```

**Translation**: Lose 25% and admit defeat. This stop is pretty wide, giving trends room to breathe.

---

## 3. Buy Condition: Double Confirmation Required

### 🎯 The Only Buy Condition: ADX + SMA Golden Cross

**Code Logic**:
```python
Condition 1: ADX > 25              # Is trend strength enough?
Condition 2: SMA(3) crosses above SMA(6)     # Is direction right?
```

**Plain English**:
> "First check ADX—this indicator tells us 'is there a trend right now'. ADX > 25 means clear trend, then look at moving averages. Short-term MA (3) crosses above long-term MA (6), means trend is going up, buy!"

**Analogy**:
Like buying a house 🏠:
- ADX > 25 = Confirms this neighborhood prices are rising (there's a trend)
- SMA golden cross = Now is a good time to buy (entry signal)

Both conditions must be met to buy, can't miss either!

### What is ADX?

**ADX (Average Directional Index)** is an indicator measuring trend strength:

| ADX Value | Trend Status | Plain English |
|-----------|--------------|----------------|
| 0-25 | No trend/weak trend | "This market is wobbling, don't touch" |
| 25-50 | Strong trend | "There's direction now, can look" |
| 50-75 | Very strong trend | "Trend very clear, good opportunity" |
| 75-100 | Extremely strong trend | "Too fierce, watch for reversal" |

**Strategy uses ADX > 25 as threshold**, meaning:
> "Only trade when trend strength is enough. Ranging market? Sorry, not even if you beg me."

---

## 4. Sell Logic: Leave When Trend is Gone

### 4.1 Sell Condition: ADX Decline + SMA Death Cross

**Code Logic**:
```python
Condition 1: ADX < 25              # Trend strength weakening
Condition 2: SMA(6) crosses above SMA(3)     # Direction reversing
```

**Plain English**:
> "ADX dropped below 25, trend is weakening. MA also death crossed, trend might reverse. Time to go, don't linger."

### 4.2 Buy vs Sell Comparison

| Dimension | Buy Signal | Sell Signal |
|-----------|------------|-------------|
| ADX Condition | > 25 (has trend) | < 25 (trend weakening) |
| SMA Condition | Golden cross (upward) | Death cross (downward/reversal) |
| Market State | Trend just formed | Trend ending |

**Plain English**:
> "When buying, need both conditions: strong trend, right direction. When selling also two conditions: weak trend, wrong direction. This is called 'strict in, strict out'."

---

## 5. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **Super Simple**: Only 50 lines of code, beginners can understand
2. **Effective Trend Filtering**: ADX really filters false signals in ranging markets
3. **Clear Logic**: ADX judges trend + SMA judges direction, simple and clear
4. **Great for Learning**: Perfect introductory case for Freqtrade strategy development

### ⚠️ Cons (Roast Time)

1. **Stop Too Wide**: 25% stop loss, some coins swing that much in a day
2. **SMA Too Short**: 3 and 6 MAs are too sensitive to noise
3. **Take Profit Too Simple**: Only one 10% target, not flexible
4. **No Trailing Take Profit**: When trend is strong could make more, but only 10%

---

## 6. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Strong Uptrend | ⭐⭐⭐⭐⭐ Full steam ahead | ADX high, perfect capture |
| Medium Trend | ⭐⭐⭐⭐☆ Normal use | Filtering effective, high signal quality |
| Sideways Consolidation | ⭐⭐☆☆☆ Use sparingly | ADX filters most signals, occasional misjudgment |
| High-Frequency Volatility | ⭐☆☆☆☆ Don't use | Short SMA too sensitive, signals all over |
| Downtrend | 🚫 Disable | Long only, downtrend is giving money away |

---

## 7. Summary: How Good Is This Strategy?

### One-Line Review
> "Entry-level trend strategy, ADX filtering is the highlight, so simple you'll think 'that's it?'"

### Who Should Use It?
- ✅ Quantitative trading beginners (simple code, clear logic)
- ✅ People wanting to learn Freqtrade
- ✅ People who like simple strategies
- ✅ People wanting to understand ADX indicator

### Who Shouldn't?
- ❌ Low risk tolerance (25% stop too wide)
- ❌ People wanting fine control (only one ROI target)
- ❌ Ranging market traders (will get filtered out)
- ❌ People seeking complex strategies (this is too simple)

### My Recommendations
1. **Learning purpose**: Use as first strategy to understand Freqtrade framework
2. **Parameter optimization**: Can change SMA periods to 5/10, less noise
3. **Add stop mechanism**: Add trailing stop yourself to protect profits
4. **Combine with others**: Use with other strategies to add signal filtering layer

---

## 8. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: Using ADX to Filter False Signals

AdxSmas is like **"a picky eater"** 🍽️:

- ADX > 25 = "This dish has meat (has trend), can eat"
- ADX < 25 = "This dish is vegetarian (consolidation), don't want"
- SMA golden cross = "Meat is cooked, can dig in"

**Its Money-Making Philosophy**:
> "I don't chase up and down, I only trade when trend is clear. Ranging? Sorry, not even if you invite me."

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Strong Uptrend | ⭐⭐⭐⭐⭐ | ADX high up, MA obediently golden crosses, perfect |
| 🔄 Medium Trend | ⭐⭐⭐⭐☆ | Filtering effective, good signal quality |
| 📉 Strong Downtrend | ⭐⭐⭐☆☆ | Strategy defaults to long, can't use in downtrend |
| ⚡️ Sideways Consolidation | ⭐⭐☆☆☆ | ADX filters signals, basically no trading |
| 🌀 High-Frequency Volatility | ⭐☆☆☆☆ | SMA too sensitive, buy today sell tomorrow |

**One-Line Summary**:
> "Trending markets are its home turf, ranging markets it chooses to lie flat."

---

## 9. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| Timeframe | 1h (default) | Can try 4h, signals more stable |
| Stop Loss | -0.25 | Wide, but gives trend room |
| Take Profit | 0.1 | 10%, no greed |

### 9.2 Areas for Optimization

```python
# Original parameters
dataframe['short'] = ta.SMA(dataframe, timeperiod=3)   # Too short
dataframe['long'] = ta.SMA(dataframe, timeperiod=6)    # Too short

# Recommended change
dataframe['short'] = ta.SMA(dataframe, timeperiod=5)   # Slightly longer
dataframe['long'] = ta.SMA(dataframe, timeperiod=10)   # Reduce noise
```

### 9.3 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|-------------------|------------|
| 1-10 | 1GB | 2GB | Smooth |
| 11-30 | 2GB | 4GB | Comfortable |
| 31+ | 4GB | 8GB | Perfect |

**Note**: This is one of the lightest strategies, minimal computation, old computers can run it.

### 9.4 Backtesting vs Live Trading

**Backtesting**: Looks okay, ADX filtering effective
**Live Trading**: ADX has slight lag, may miss trend starting points

**Recommended Process**:
1. Backtest first to see results
2. Small capital live test
3. Observe signal quality
4. Consider optimizing SMA parameters
5. Can add trailing stop

---

## 10. Bonus: The Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Code Origin**: Comments say this was converted from C# version
   > "This is a 'ported' strategy, translated from another platform"

2. **Minimalist Design**: Whole strategy is only about 50 lines
   > "Author might be saying: simplicity is beauty"

3. **ADX Threshold**: Chose the classic value of 25
   > "Textbook parameter, nothing fancy"

4. **Wide Stop Loss**: 25% stop space
   > "Gives trend enough breathing room, won't get shaken out easily"

---

## 11. Final Words

### One-Line Review
> "Entry-level trend strategy, simple code, clear logic, great for learning. ADX filtering is the essence."

### Who Should Use It?
- ✅ Quantitative trading beginners
- ✅ People wanting to understand ADX indicator
- ✅ People who like simple strategies
- ✅ People learning Freqtrade framework

### Who Shouldn't?
- ❌ Low risk tolerance (stop too wide)
- ❌ Ranging market traders (will get filtered)
- ❌ People seeking complex strategies (too simple)
- ❌ People wanting fine control (too few options)

### Manual Trading Recommendations
If you want to manually execute this strategy:
1. Add ADX(14) indicator in TradingView
2. Add SMA(3) and SMA(6)
3. Wait for ADX > 25 and SMA golden cross to buy
4. Set 25% stop loss or observe ADX decline to sell

---

## 12. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting Looks Okay, Live Trading Needs Caution

AdxSmas historical backtesting looks **okay**—but there's a problem:

> **ADX is a lagging indicator, by the time it confirms a trend, the trend may have already moved for a while.**

Simply put: **"Trend started a while ago, ADX then tells you it's time to enter."**

### Strategy's Hidden Risks

In live trading, watch out for these risks:
- **ADX lag**: Trend confirmation has delay, may miss best entry points
- **Stop too wide**: 25% may not suit volatile coins
- **SMA too short**: 3 and 6 MAs are noisy, frequent signals
- **Single take profit**: 10% target may be too rigid

### My Recommendations (Real Talk)

```
1. Use this strategy as a learning template
2. Optimize SMA periods (suggest changing to 5/10)
3. Add trailing stop to protect profits
4. Adjust ADX threshold for different markets
5. Small capital test, don't go all in right away
```

**Remember**: No matter how simple the strategy, the market isn't simple. Test with light positions, survival comes first! 🙏

---