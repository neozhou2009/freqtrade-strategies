# TDSequentialStrategy: Counting to Nine for Reversals

> **Nickname**: The Count Master  
> **Job**: Reversal Hunter, specializes in catching "what goes up must come down"  
> **Timeframe**: 1 Hour

---

## 1. What Is This Strategy?

Simply put, **TDSequentialStrategy** is:
- A counting game: Count to 9, then reverse
- A reversal hunter: Catches moments when trends get "too tired"
- A perfectionist: Just counting to 9 isn't enough, must verify "perfection conditions"

Like **counting the nine cold days of winter**, counting until the weather warms up. Same here - counting consecutive price drops/rises, when it reaches the 9th candle, it thinks: time to reverse! 🤣

---

## 2. Core Config: Basically "Small Stop-Loss + Trailing Profit"

### Take-Profit Rules (ROI Table)

```
Target Profit: 500% (basically just for show)
```

**Translation**: This ROI setting is purely decorative. Waiting for 500% to sell would take forever. The strategy actually exits on signals, not ROI.

### Stop-Loss Rules

```
Fixed Stop-Loss: -5%
Trailing Stop: Enabled
Only Sell When Profitable: Yes
```

**Translation**: Lose 5% and you're out. Make money and it follows the trend, letting profits run. And it has a temper: won't respond to sell signals when losing, must be profitable to sell.

---

## 3. One Buy Condition: Buy When Counting to 9

This strategy's buy condition is unique, with one core concept: **TD Sequential sequence completion**.

### 🎯 The Only Buy Condition

**Core Logic**: 9 consecutive candles with closing price lower than closing price 4 candles ago

**Plain English**:
> "Candle 1's close is lower than candle -3's close, candle 2 is lower than candle -2... when you count to candle 9, if each one is lower than the one 4 candles back, that's a buy signal!"

**But there's a "perfection condition"**:
> "The low of candle 8 or 9 must be lower than the low of candle 6 or 7. Like saying: if it hasn't dropped deep enough, I'm not buying!"

**Classic Line**:
```
Close < Close 4 candles ago, 9 times in a row?
AND Low of candle 8/9 < Low of candle 6/7?
→ BUY!
```
> "Dropped this long, should bounce right? But if it hasn't dropped hard enough, I'm not touching it~"

---

## 4. Sell Logic: Symmetrical Operation

### 4.1 Sell Conditions

Sell is completely symmetrical to buy:
- **Sequence Complete**: 9 consecutive candles with close higher than 4 candles ago
- **Perfection Condition**: High of candle 8/9 higher than high of candle 6/7

**Plain English**:
```
Close > Close 4 candles ago, 9 times in a row?
OR High of candle 8/9 > High of candle 6/7?
→ SELL!
```
> "Risen this long, should pull back right? Take profits while you can!"

### 4.2 Interesting Temper

```python
sell_profit_only = True  # Only sell when profitable
```

**Plain English**:
> "I won't sell when losing money. Must wait until profitable to exit. What if it goes back up later?"

This temper is a bit stubborn, but also a protection mechanism.

---

## 5. TD Sequential Theory: What's the Big Deal?

TD Sequential is a system invented by technical analysis guru **Tom DeMark**, famous on Wall Street and in crypto circles.

### 5.1 Core Concept

**Human Version**:
- Trends can't continue forever
- After consecutive drops/rises to a certain point, it's time for a rest
- Counting to 9 is an "exhaustion signal"

### 5.2 Why Count "9"?

Tom DeMark discovered:
- After 9 consecutive candles moving in the same direction, reversal probability increases
- This isn't mysticism, it's statistical patterns
- Many traders use this system, creating a "self-fulfilling prophecy"

---

## 6. Strategy "Personality"

### ✅ Pros (Praise Section)

1. **Solid Theory**: Tom DeMark's famous name, not some random indicator
2. **Simple Logic**: Just counting + verification, elementary schoolers can understand
3. **Reversal Specialist**: Specifically catches "extreme reversal" turning points
4. **Small Codebase**: Not many parameters, less likely to overfit

### ⚠️ Cons (Roast Section)

1. **Killer in Trending Markets**: In one-way trends, it keeps shouting "reversal" mid-way, then gets slapped
2. **Counting Gets Interrupted**: Any candle not satisfying conditions resets the count, wasted effort
3. **Lagging**: Must wait for 9th candle to finish before entering, could be too late
4. **Single Timeframe**: Only looks at 1-hour, no larger timeframe confirmation

---

## 7. Applicable Scenarios: When to Use?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| 🔄 Ranging Market | ⭐⭐⭐⭐⭐ Use it! | Perfectly captures range boundaries |
| 📊 Sideways Consolidation | ⭐⭐⭐⭐☆ Use it | High/low points in consolidation zones are accurate |
| 📈 Strong Uptrend | ⭐⭐☆☆☆ Use cautiously | Will call sell too early, miss big gains |
| 📉 Strong Downtrend | ⭐⭐☆☆☆ Use cautiously | Will keep calling buy, catching falling knives |

---

## 8. Summary: How's This Strategy Really?

### One-Liner Review
> "God of ranging markets, pit of trending markets. Makes money for those who know how, loses for those who don't."

### Who Should Use It?
- ✅ Veterans familiar with TD Sequential theory
- ✅ High-frequency traders in ranging markets
- ✅ Strategy developers who like simple logic
- ✅ Reversal trading enthusiasts

### Who Shouldn't Use It?
- ❌ Perma-bulls in one-way trends
- ❌ Impatient types who hate waiting
- ❌ People who want complex multi-condition filters
- ❌ One-direction-only players

### My Suggestions
1. **Observe the market first**: Confirm if it's ranging or trending, use it in ranging, avoid in trending
2. **Add trend filter**: Add a larger timeframe moving average, only take reversals in the direction of the larger trend
3. **Adjust stop-loss**: 5% may be too tight, can loosen to 7-10% for high-volatility coins
4. **Be patient**: Sequence counting takes time, don't rush entries

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Extremes Reverse

TDSequentialStrategy is a **reversal strategy**. Its money-making philosophy:

> "Trees don't grow to the sky, prices don't fall to hell. Count to 9, that's about right."

- **Sequence Counting**: 9 consecutive moves in same direction, time to rest
- **Perfection Condition**: Must drop/rise deep/high enough to enter
- **Reversal Trading**: Go opposite of the previous direction

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:------------------|:--------------------------|
| 🔄 Ranging Market | ⭐⭐⭐⭐⭐ | Range boundaries are its home turf, buying low selling high with precision |
| 📊 Sideways Consolidation | ⭐⭐⭐⭐☆ | Breakouts/pullbacks after consolidation can be captured |
| 📈 Strong Uptrend | ⭐⭐☆☆☆ | Keeps calling sell while it rises, then it keeps rising |
| 📉 Strong Downtrend | ⭐⭐☆☆☆ | Keeps calling buy while it drops, then it keeps dropping |

**One-Liner Summary**: God of ranging markets, getting rekt in trending markets.

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config | Recommended Value | Notes |
|--------|------------------|-------|
| Timeframe | 1h (default) | Can also try 4h, more stable |
| Trading Pairs | Ranging coins | Don't pick those one-way shitcoins |

### 10.2 Hardware Requirements

This strategy has minimal computation, doesn't need much:

| Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|--------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | No pressure |

### 10.3 Backtesting vs Live Trading

**Backtesting looks pretty** because:
- Reversal points are clear in history
- Sequence counting won't be interrupted

**Live Trading Challenges**:
- Real-time candles may be incomplete, sequences get interrupted
- By the time signal appears, might have missed best entry

**Recommended Process**:
1. Run on paper trading for 1-2 weeks first
2. Observe quality of sequence signals
3. Confirm suitable for current market environment before live

---

## 11. Bonus: Strategy Author's "Little Secrets"

Looking at the code, found some interesting designs:

1. **"Perfection Condition" naming**: In code called `exceed_low` and `exceed_high`, translates to "breakthrough low" and "breakthrough high"
   > "I counted to 9, but price didn't drop hard enough, I'm not buying!"

2. **Sequence interruption reset**: Any candle not satisfying conditions, counter resets to zero
   > "Oops, broke the streak, start over. 1, 2, 3..."

3. **Only needs 30 candles to start**: `startup_candle_count: int = 30`
   > "Give me 30 candles and I can start working"

---

## 12. Final Words

### One-Liner Review
> "Count to 9 and reverse, simple and effective—but only if the market cooperates."

### Who Should Use It?
- ✅ Traders doing ranging markets
- ✅ People familiar with TD Sequential theory
- ✅ Strategy players who like simple logic
- ✅ Reversal trading enthusiasts

### Who Shouldn't Use It?
- ❌ Trend-following momentum players
- ❌ Impatient types who hate waiting
- ❌ People wanting complex multi-condition filters
- ❌ One-direction-only traders

### Manual Trader Suggestions
TD Sequential can be used manually:
- Set up TD Sequential indicator on TradingView
- Watch for 9 sequences forming
- Note if "perfection condition" is satisfied
- Confirm with support/resistance levels

---

## 13. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting Is Beautiful, Live Trading Needs Caution

TDSequentialStrategy's historical backtest may perform well—but note:

> **Biggest pitfall of reversal strategies: getting repeatedly trapped in trending markets.**

Simply put: **In one-way trends, it's a contrary indicator.**

### Hidden Risks of Complex Strategies

In live trading watch out for:
- **Sequence Interruption**: Real-time candles may interrupt sequences, missing signals
- **Lag**: By 9th candle finishes, price may have already bounced
- **False Signals**: When oscillation isn't intense enough, reversal may fail

### My Advice (Heart-to-Heart)

```
1. Judge market type first: Use in ranging, avoid in trending
2. Add larger timeframe confirmation: Add a daily MA, only trade with the trend
3. Widen stop-loss: 5% may be too tight, 7-10% is safer
4. Light position testing: Verify with small positions first, don't go heavy
```

**Remember**: Count to 9 and reverse? Market says: Not necessarily!

---

**Final Reminder**: No matter how classic the strategy, the market will humble you without warning. It's god in ranging markets, it's a pit in trending markets. Choosing the right battlefield is most important! 🙏