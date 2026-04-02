# TechnicalExampleStrategy: The Simplest Beginner Strategy

> **Nickname**: The Minimalist Representative  
> **Occupation**: Teaching Example / Introductory Material  
> **Timeframe**: 5 minutes

---

## 1. What is This Strategy?

Simply put, **TechnicalExampleStrategy** is:
- Only 40 lines of code
- Uses only one indicator
- Logic so simple even elementary schoolers can understand

It's like a "Strategy Writing 101 Tutorial" telling you how to write Freqtrade strategies 📚

---

## 2. Core Configuration: "Quick In, Quick Out"

### Take-profit Rules (ROI Table)

```
0 minutes: Sell at 1% profit
```

**Translation**: Whenever you make 1%, sell immediately. Don't be greedy.

### Stop-loss Rule

```
Stop-loss: Accept defeat at 5% loss
```

**Translation**: If you lose 5%, cut your losses and leave. Don't fight it.

---

## 3. The 1 Buy Condition: Simple to the Extreme

### 🎯 The Only Buy Condition: Buy When Money Flows Out

**Core Logic**: Watch the CMF indicator

**Plain English**:
> "Buy when money flows out (CMF < 0), sell when money flows in."

**What is CMF?**

CMF (Chaikin Money Flow) is called the "Chaikin Money Flow Indicator", simply put:
- CMF > 0: Money flowing in (someone is buying)
- CMF < 0: Money flowing out (someone is selling)

**This strategy's logic**:
> "I buy when everyone is selling, and I sell when someone starts buying."

Sounds like "bottom fishing", but could also be "catching a falling knife" 😅

---

## 4. Sell Logic: Also Single-minded

### Sell Condition

```
Sell when CMF > 0
```

**Plain English**:
> "When money starts flowing in, hurry up and sell."

### Other Exit Methods

- Sell at 1% profit (ROI take-profit)
- Sell at 5% loss (stop-loss)

---

## 5. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **Insanely simple**: Code short enough to understand at a glance
2. **Teaching gem**: Perfect for learning Freqtrade strategy framework
3. **Low resource usage**: Can run on potato computers

### ⚠️ Cons (Roast Time)

1. **Too simple**: Only one indicator, easily taught a lesson by the market
2. **Counter-trend bottom-fishing**: Buying during money outflow may catch falling knives
3. **No protection**: No trailing stop, profits may turn back into losses
4. **Suffers in ranging markets**: CMF crossing zero line back and forth causes frequent trades

---

## 6. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Learning Research | ✅ Highly recommended | Exactly its purpose |
| Ranging Market | ⚠️ Caution | May trigger frequent stop-losses |
| One-way Downtrend | ❌ Don't use | Bottom-fishing halfway down |
| Reversal Market | 🤔 Worth a try | Money outflow bottom may rebound |

---

## 7. Summary: How Good is This Strategy?

### One-sentence Review
> "Teaching example, not a live trading weapon."

### Who Should Use It?
- ✅ Freqtrade beginner learners
- ✅ People wanting to understand CMF indicator
- ✅ Developers needing strategy code templates
- ✅ Researchers doing strategy experiments

### Who Should NOT Use It?
- ❌ People wanting to make money directly in live trading
- ❌ People pursuing high win rates
- ❌ People who don't want to modify code

### My Suggestions

1. **Treat it as teaching material**: Clear code structure, great example for learning
2. **Don't use it directly in live trading**: Add some filter conditions first
3. **Can be improved**: Add trend judgment, adjust CMF threshold

---

## 8. CMF Indicator in Plain English

### How is CMF Calculated?

Simply put, it looks at "whether buying power or selling power is stronger":

```
Buying/Selling Power = ((Close - Low) - (High - Close)) / (High - Low)
CMF = Sum of (Buying/Selling Power × Volume) for all candles / Sum of Volume for all candles
```

**Translated to human language**:
- Close near High → Buyers strong
- Close near Low → Sellers strong
- Multiplied by volume → Big money carries more weight

### CMF Value Meaning

| CMF Value | Meaning |
|-----------|---------|
| CMF > 0.1 | Strong money inflow, buyers dominate |
| CMF > 0 | Money inflow, buying bias |
| CMF = 0 | Buying and selling balanced |
| CMF < 0 | Money outflow, selling bias |
| CMF < -0.1 | Strong money outflow, sellers dominate |

---

## 9. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Comment |
|-------------------|-----------------|---------|
| Number of pairs | 5-20 | More is pointless |
| Timeframe | 5 minutes | Only one timeframe |
| CMF Period | 21 (default) | Can try 14 |

### 9.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|--------------------|------------|
| 1-10 pairs | 1GB | 2GB | Smooth |
| 10-50 pairs | 2GB | 4GB | Acceptable |

**Don't worry**: Strategy is so simple, even old computers can run it 😂

---

## 10. Easter Egg: What Does the Strategy Name Tell Us?

**TechnicalExampleStrategy** = "Technical Example Strategy"

From the name we know:
1. **Official example**: This is a Freqtrade official or community teaching example
2. **Not for live trading**: Real live strategies wouldn't be called "Example"
3. **Code template**: Copy and modify it, faster than writing from scratch

---

## 11. If I Want to Improve It, How?

### Plan 1: Add Trend Filter

```python
# Add an EMA to judge trend
dataframe['ema'] = ta.EMA(dataframe, timeperiod=200)

# Only buy in uptrend
(dataframe['close'] > dataframe['ema']) & 
(dataframe['cmf'] < -0.1)  # Change CMF threshold to -0.1
```

### Plan 2: Add Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.005  # Start trailing after 0.5% profit
trailing_stop_positive_offset = 0.01  # Trailing distance
```

### Plan 3: Add Volume Filter

```python
# Only buy when volume is sufficient
(dataframe['volume'] > dataframe['volume'].rolling(20).mean())
```

---

## 12. The Very Last Word

### One-sentence Review
> "Great for beginners, needs improvement for live trading."

### Who Should Use It?
- ✅ Beginner learning
- ✅ Code template
- ✅ CMF research

### Who Should NOT Use It?
- ❌ Direct live trading
- ❌ Pursuing stable returns

### Suggestions for Manual Traders

You can borrow this strategy's thinking:
- Pay attention to money flow (can use other money flow indicators)
- Buy in panic, sell in greed
- But must combine with trend judgment, don't bottom-fish in downtrends

---

## 13. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting Looks Good, Live Trading Be Careful

TechnicalExampleStrategy's historical backtesting might be okay—but it has an obvious problem:

> **Only one indicator, no multi-dimensional validation, lots of false signals.**

Simply put: **Bottom-fishing halfway down happens often.**

### Hidden Risks of Minimalist Strategies

In live trading, simple logic can lead to:
- **Ranging market losses**: CMF frequently crosses zero line, back and forth slaps
- **Trending market trapped**: Counter-trend buying, buying more as it drops
- **Slippage costs**: Frequent trading, fees and slippage eat profits

### My Suggestion (Honest Words)

```
1. Use it as teaching material to learn
2. Improve before considering live trading
3. Add trend filters
4. Adjust CMF threshold (e.g., buy at -0.1, sell at 0.1)
5. Small position testing, survival is most important
```

**Remember**: No matter how simple the strategy, the market isn't simple. Light position testing, survival first! 🙏

---

*Strategy Number: #407*