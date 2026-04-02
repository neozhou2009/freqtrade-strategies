# RaposaDivergenceV1 Strategy: The Divergence Hunter

> **Nickname**: Reversal Hunter, Peak-Valley Detective  
> **Job**: Specializes in finding divergence signals, catching reversal points  
> **Timeframe**: 5 minutes

---

## I. What is This Strategy?

Simply put, **RaposaDivergenceV1** is:
- A strategy that specifically looks for "divergence" signals
- Price and RSI indicator moving in opposite directions? It enters
- Uses mathematical methods to precisely find peak and valley points

It's like a **detective with a magnifying glass looking for turning points** 🔍

### ⚠️ First, Let's Talk About a Big Pitfall

The author wrote in the code:
> "argrelextrema might have look-ahead bias so results in backtest will not be reliable"

**Translation**: This strategy's backtest results might be inaccurate because it uses a "future function." During backtesting, it might "see the future" to confirm signals, but live trading can't do that.

---

## II. Core Configuration: Profit Targets Are Pretty Aggressive

### Take-Profit Rules (ROI Table)

```
0 minutes: Make 15% and run!
60 minutes: 2% is fine too...
120 minutes: Even 1% is okay
After 180 minutes: Even 0.1% is good enough
```

**Translation**: Initially wants to make 15%, but after waiting an hour, only wants 2%. Expectations drop pretty fast.

### Stop-Loss Rules

```
Fixed stop-loss: -30% (30% again...)
Trailing stop: Activates after 2% profit, locks in 1%
```

**Translation**: Stop-loss is set pretty wide, but trailing stop provides some protection.

---

## III. Buy Condition: Only Bullish Divergence

### Core Logic (Plain English Version)

What is **bullish divergence**?
- Price makes a new low
- But RSI indicator doesn't make a new low
- Meaning: Downward momentum is exhausting, might bounce!

**In plain English**:
> "Price is still falling, but with less force — prepare to buy the dip!"

### Buy Condition Breakdown

```python
Price forms a higher low (bullish divergence)
RSI also forms a higher low (confirmation)
RSI < 50 (not buying in overbought territory)
Has volume
```

### Peak-Valley Detection Algorithm

This strategy uses a mathematical function called `argrelextrema` to find peak and valley points.

**Plain English**:
> "Like finding the highest and lowest points of a mountain range — automatically identified using mathematical methods."

Parameter explanation:
| Parameter | Default | Plain English |
|-----------|---------|---------------|
| order | 5 | Look at 5 candles on each side to determine if it's a peak/valley |
| K value | 2 | Need 2 consecutive extrema to confirm a real peak/valley |

---

## IV. Sell Condition: Bearish Divergence (But Author Says It Doesn't Work Well)

### Sell Logic

What is **bearish divergence**?
- Price makes a new high
- But RSI indicator doesn't make a new high
- Meaning: Upward momentum is exhausting, might drop!

**Plain English**:
> "Price is still rising, but with less force — prepare to exit!"

### But the Author Said...

> "sell signal seems like garbage"

**Translation**: The sell signal seems like trash...

**My Advice**: Don't count on the sell signal, rely on ROI and trailing stop to exit.

---

## V. Protection Mechanisms: Just These Few

| Protection Type | Parameter | Plain English |
|----------------|-----------|---------------|
| Fixed stop-loss | -30% | "If losing big, run" |
| Trailing stop | 1% @ 2% profit | "Lock in some profit after making some" |
| Tiered ROI | 15%→2%→1%→0.1% | "The longer you wait, the less picky you are" |

Simple and rough, no complex protection logic.

---

## VI. This Strategy's "Personality Traits"

### ✅ Advantages (Compliment Section)

1. **Solid theory**: Divergence is classic technical analysis, not some esoteric stuff
2. **Precise algorithm**: Uses scipy scientific computing library, not self-made hacks
3. **Clear signals**: Bullish divergence buy, bearish divergence sell, simple rules
4. **Few parameters**: Just 4 parameters, unlike some strategies with dozens

### ⚠️ Disadvantages (Roast Section)

1. **Future function**: Backtest results are unreliable, this is the most fatal issue
2. **Poor sell signal**: Author admits the sell signal is garbage
3. **Few signals**: Divergence doesn't happen often, might not see a signal for days
4. **Stop-loss too big**: 30% stop-loss, if you hit a trending market you're screwed

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Oscillating transition | Can use | Divergence signals are more accurate |
| Single-direction trend | Don't use | Will get repeatedly stopped out |
| High volatility | Increase order | Filter noise extrema |
| Low volatility | Decrease order | Capture more signals |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Review
> "A divergence strategy with more academic value than live trading value. Backtest looks good but don't take it seriously."

### Who Is It For?
- ✅ Programmers who want to learn divergence detection algorithms
- ✅ Players in oscillating trend-transition markets
- ✅ People who can accept differences between backtest and live trading
- ✅ People willing to manually confirm signals

### Who Is It NOT For?
- ❌ People who rely on backtest results to make decisions
- ❌ Players in single-direction trending markets
- ❌ People who need frequent trading (few signals)
- ❌ People who can't accept 30% drawdown

### My Advice
1. **For learning only**: This strategy's greatest value is learning peak-valley detection algorithms
2. **Use as auxiliary**: Use divergence signals as auxiliary, not as the sole basis
3. **Reduce stop-loss**: 30% is really too big, change to 10-15%
4. **Paper trading test**: Run at least 2 weeks of paper trading before live, compare differences

---

## IX. In What Markets Can This Strategy Make Money?

### 9.1 Core Logic: Finding Reversal Points

RaposaDivergenceV1 is a pure divergence strategy. About 200+ lines of code, mainly relies on scipy's `argrelextrema` to find peaks and valleys.

**Its money-making philosophy**: Enter when price and indicator "disagree."

- **Bullish divergence**: Price still falling, but RSI says "can't fall anymore"
- **Bearish divergence**: Price still rising, but RSI says "can't rise anymore"

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Sustained uptrend | ⭐☆☆☆☆ | Bearish divergence keeps appearing, price keeps rising, stopped out all the way |
| 📉 Sustained downtrend | ⭐☆☆☆☆ | Bullish divergence keeps appearing, price keeps falling, stopped out all the way |
| 🔄 Oscillating transition | ⭐⭐⭐⭐⭐ | Home field! Divergence is designed for this |
| 🔄 Oscillating no-transition | ⭐⭐⭐☆☆ | Many signals but might not be accurate |

**One-sentence summary**: Divergence strategies only work during trend transitions; single-direction trends will slap you in the face.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Number of pairs | 10-20 | Few signals, need more pairs |
| Volatility | Medium | Too stable = no divergence, too volatile = too many false signals |
| Timeframe | 5 minutes | Default setting |

### 10.2 Configuration File Key Settings

```yaml
# config.json key configurations
"timeframe": "5m",
"startup_candle_count": 40,  # Warmup needs 40 candles
"trailing_stop": true,
"trailing_stop_positive": 0.01,
"trailing_stop_positive_offset": 0.02
```

### 10.3 Hardware Requirements (Important!)

This strategy has moderate computational load, scipy's peak-valley detection isn't too heavy:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|---------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Normal |
| 50+ pairs | 8GB | 16GB | Slightly laggy |

### 10.4 Backtest vs. Live Trading

**This is key!**

```
Backtest might show: 70% win rate, 300% return
Live might show: 40% win rate, 50% return

Why? Because argrelextrema "sees the future."
```

**Recommended Process**:
1. Take backtest results with a grain of salt, multiply by 0.5 for a more realistic estimate
2. Run paper trading for at least 2 weeks, compare signal lag
3. Test with small capital live, verify actual performance
4. Manually confirm divergence signals before entering

---

## XI. Bonus: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **Author roasts their own sell signal**: `sell signal seems like garbage`
   > "This sell signal is trash, don't count on it"

2. **Warning about future function**: `argrelextrema might have look-ahead bias`
   > "Backtest looks good but isn't accurate, I already told you"

3. **Parameter range design**: order and K value ranges are both 1-32, but defaults are 5 and 2
   > "Defaults are good enough, but you can adjust"

---

## XII. Final Words

### One-Sentence Review
> "An honest strategy — the author themselves said the sell signal is garbage and backtest is unreliable. Good for learning divergence algorithms, use with caution in live trading."

### Who Is It For?
- ✅ Programmers wanting to learn divergence detection algorithms
- ✅ Players in oscillating transition markets
- ✅ People who can accept backtest ≠ live trading
- ✅ People willing to manually confirm signals

### Who Is It NOT For?
- ❌ People who rely on backtests to make decisions
- ❌ Players in single-direction trending markets
- ❌ People who need high-frequency trading
- ❌ People who can't accept 30% drawdown

### Manual Trading Recommendations
If you want to use this strategy's signals manually:
1. Learn to identify divergence patterns (price and RSI moving in opposite directions)
2. Wait for peak-valley confirmation before entering, don't rush to buy the dip
3. Confirm with other indicators (like MACD, volume)
4. Set smaller stop-loss (10-15%), don't copy the strategy's 30%

---

## XIII. ⚠️ Risk Emphasis (Must Read)

### Backtest Is Beautiful, Live Trading Needs Caution

RaposaDivergenceV1's historical backtest performance might be **very good** — but there's a big pitfall:

> **argrelextrema "sees the future" to confirm peak-valley points, but live trading can't do that.**

Simply put: **Backtest has x-ray vision, live trading doesn't.**

### Look-Ahead Bias

What is a future function?
```
During backtest:
  Candle #100 is confirmed as a low point because candles #101, #102, #103 are all higher

During live trading:
  Candle #100 just closed, you don't know what #101, #102, #103 will be
```

**Consequences**:
- Backtest signals "precisely" appear at the lowest point
- Live signals need to wait several candles before confirmation
- Missing the best entry timing

### My Advice (Real Talk)

```
1. Treat this strategy as learning material, don't count on it to make money
2. If you must use it, combine with other indicators for manual confirmation
3. Change stop-loss to 10-15%, 30% is too big
4. Paper trading test, compare differences between backtest and live
5. Use divergence signals as auxiliary, not as the sole basis
```

**Remember**: Divergence strategies are accurate during trend transitions, but will get slapped repeatedly in single-direction trends. Test with small positions, staying alive is most important! 🙏