# ADX_15M_USDT2 Strategy: The DI Crossover Strategy That's "Suspiciously Simple"

> **Nickname**: The Bottom-Fisher (but might be backwards)  
> **Occupation**: Trend Reversal Catcher  
> **Timeframe**: 15 Minutes

---

## I. What Exactly Is This Strategy?

Simply put, **ADX_15M_USDT2** is:
- Uses only one indicator (DI crossover) to decide buy/sell
- Stop-loss wide enough to be ridiculous (31.9%!)
- Code short enough to read in an elevator
- Buy signal might be installed backwards

Like a **mechanic showing up with just one screwdriver to fix a plane**—brave, but something feels off 🤣

---

## II. Core Configuration: Basically "All-In and Wait for Reversal"

### Take-Profit Rules (ROI Table)

```
Just bought and it's up 10.3%? Run!
Waited 102 minutes (1.7 hours) and still 7.6%? Run!
Waited 275 minutes (4.6 hours) and still 4.2%? Run!
Waited 588 minutes (almost 10 hours)? Fine, take whatever profit and get out!
```

**Translation**: This strategy has strong profit appetite, wanting 10% right off the bat. But if you "only make 4%," it accepts that too—consider it a wasted effort.

### Stop-Loss Rules

```
When down to -31.94%... just wait a bit more?
```

**Translation**: This is the most ridiculous part—the stop-loss is at -32%! What does that mean? You invest 100 bucks, and it won't cut losses until it hits 68 bucks. Either the author is extremely confident, or... forgot to set it properly?

---

## III. 1 Buy Condition: Simple Enough to Be Suspicious

### 🎯 The Only Condition: MINUS_DI Crosses Above PLUS_DI

**Core Logic**: Downward momentum line breaks above upward momentum line → Buy

**Plain English**:
> "Downward trend is starting to overpower upward trend, hurry up and buy!"

**Wait... that doesn't seem right?**

In traditional technical analysis, MINUS_DI crossing above PLUS_DI is a **short signal** because it means downward momentum is starting to dominate. But this strategy treats it as a buy signal. Two possibilities:
1. Bottom-fishing logic: Buy when downward momentum just starts, wait for bounce
2. Author got it backwards

```python
# The actual code is just this one line
(qtpylib.crossed_above(dataframe['minus_di'], dataframe['plus_di']))
```

---

## IV. Protection Mechanism: Basically Non-Existent

| Protection Type | Function | Plain English |
|-----------------|----------|---------------|
| Stop-Loss | -31.94% | "Lose half? No problem, I can hold!" |
| Take-Profit | Tiered ROI | "Take profits when you got 'em" |
| Trailing Stop | None | "Why run? Hold to the death" |

**Complaint**: This strategy's protection mechanism is like hanging your house keys on the doorknob—theoretically there, but practically useless 🤡

---

## V. Sell Logic: Conditions So Harsh They'll Almost Never Trigger

### 5.1 Technical Sell Signals

```
To trigger a sell, ALL conditions must be met:
1. ADX > 91 (extreme trend strength)
2. MINUS_DI > 91 (extreme downward momentum)
3. PLUS_DI crosses above MINUS_DI (reversal signal)
```

**Plain English**:
- ADX and DI indicators normally range from 0-100
- What does 91 mean? Basically a "once in a century" extreme value
- The probability of all three conditions being met simultaneously is about the same as winning the lottery

**Conclusion**: The "technical sell" in this strategy will almost never trigger; it mainly exits through the ROI table and stop-loss.

---

### 5.2 Actual Exit Methods

| Exit Method | Trigger Condition | Plain English |
|-------------|-------------------|----------------|
| ROI Take-Profit | Reach profit target | "Made enough, time to bail!" |
| Stop-Loss | Loss > 31.94% | "Better run before it's all gone!" |
| Technical Signal | ADX > 91 + DI > 91 + crossover | "A once-in-a-century miracle!" |

---

## VI. This Strategy's "Personality"

### ✅ Pros (Yes, there are some...)

1. **Simple Code**: 60 lines, even beginners can understand
2. **Low Computation**: Any computer can run it
3. **High Extensibility**: Reserved slots for many indicators

### ⚠️ Cons (Complaint Time)

1. **Signal Direction Questionable**: MINUS_DI crossing above PLUS_DI is supposed to be a short signal!
2. **Stop-Loss Too Wide**: -32% stop-loss, is this faith-based trading?
3. **Sell Conditions Virtually Useless**: ADX > 91 basically never triggers
4. **No Filtering Whatsoever**: One crossover and you charge in, too reckless

---

## VII. Applicable Scenarios: When Should You Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|-------------------|--------|
| Oscillating Reversal | Can try | DI crossover might catch reversal points |
| One-Way Trend | Not recommended | Signal direction might be opposite |
| High Volatility | Be cautious | Too much noise, signal too simple will get fooled |
| Want to Learn Strategy | Recommended | Simple code, good for beginners |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Review
> "A DI crossover strategy so simple it makes you question life"

### Who Should Use It?
- ✅ Beginners wanting to learn strategy coding
- ✅ Researchers wanting to verify DI crossover signal effectiveness
- ✅ Experimenters with sufficient risk tolerance

### Who Shouldn't Use It?
- ❌ Newbies wanting stable profits
- ❌ Conservative investors with large capital
- ❌ People who don't want to modify code themselves

### My Recommendations
1. **Flip the signal direction**: Change MINUS_DI crossing above to PLUS_DI crossing above
2. **Tighten stop-loss**: -32% is too wide, suggest around -10%
3. **Enable ADX filter**: There's a commented ADX > 45 condition in the code, uncomment it
4. **Lower take-profit threshold**: 10% take-profit at start is too aggressive, can lower to 5-7%

---

## IX. What Market Can This Strategy Make Money In?

### 9.1 Core Logic: Using DI Crossover to Catch Reversals

This strategy has about 60 lines of code. What does that mean? A high school essay is longer than this 📝

**Its Money-Making Philosophy**:
> "At the moment of trend reversal, I charge in!"

- **Reversal Capture**: DI crossover means direction change
- **Extreme Exit**: Judge trend termination at extreme ADX values
- **Time Control**: ROI table forces exit

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Strong Uptrend | ⭐⭐☆☆☆ | Will enter too early, then get trapped |
| 🔄 Oscillating Reversal | ⭐⭐⭐⭐☆ | Right on target, reversal signal works |
| 📉 Plunging Market | ⭐⭐☆☆☆ | Signal direction might be opposite, keep dropping |
| ⚡️ High-Frequency Volatility | ⭐⭐⭐☆☆ | Too much noise, signals easily fooled |

**One-Sentence Summary**: This is designed for oscillating reversal markets; don't bother with trending markets.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Complaint |
|--------------------|-----------------|-----------|
| Timeframe | 15m | Default setting, good enough |
| Number of Trading Pairs | 3-10 pairs | Too many signals get messy |
| Stop-Loss | Change to -10% | -32% is ridiculous |

### 10.2 Key Configuration File Settings

```yaml
# Suggested modifications
stoploss: -0.10  # Originally -0.32, too wide
minimal_roi:
  "0": 0.05      # Originally 0.10, lower a bit
  "60": 0.03
  "120": 0.01
  "180": 0
```

### 10.3 Hardware Requirements (This Strategy Saves Resources)

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|:-----------------------:|:--------------:|:-----------------:|:----------:|
| 1-10 pairs | 512MB | 1GB | Smooth |
| 10-50 pairs | 1GB | 2GB | Smooth |
| 50+ pairs | 2GB | 4GB | Still smooth |

**Good News**: This strategy doesn't need a powerful computer; even a Raspberry Pi can run it 😂

### 10.4 Backtesting vs Live Trading

**Backtesting Notes**:
- Since sell signals almost never trigger, backtesting mainly looks at ROI and stop-loss
- May hold positions for long periods until stop-loss or ROI exit

**Suggested Process**:
1. First get the signal direction right
2. Tighten stop-loss
3. Small capital backtesting
4. Paper trading for a week
5. Small position live trading

**Don't go all-in right away**—this strategy's original version has obvious logic issues!

---

## XI. Bonus: The Author's "Little Secrets"

Look carefully at the code, and you'll find some interesting things:

1. **Commented-out buy conditions**:
   ```python
   # (dataframe['adx'] > 45) &
   # (dataframe['minus_di'] > 26) &
   # (dataframe['plus_di'] > 33) &
   ```
   > "Maybe the author also felt the signal was too simple, added filter conditions but then commented them out"

2. **Calculated but unused indicators**:
   - SAR (Parabolic Stop and Reverse)
   - MOM (Momentum)
   > "Reserved slots, waiting for you to fill them"

3. **Sell threshold set to 91**:
   > "Maybe meant to express 'only sell at extremes,' but 91 is really too extreme"

---

## XII. Final Words

### One-Sentence Review
> "Minimalist DI crossover strategy to the extreme, but signal direction needs rethinking"

### Who Should Use It?
- ✅ Beginners wanting to learn strategy code structure
- ✅ Developers wanting to build strategies based on DI indicator
- ✅ Quantitative enthusiasts with time to debug and optimize

### Who Shouldn't Use It?
- ❌ People wanting to make money directly
- ❌ People who don't want to modify code
- ❌ People with low risk tolerance

### Manual Trading Recommendations

If you want to manually execute this strategy's logic:
1. Open TradingView, add DI indicator
2. Wait for MINUS_DI to cross above PLUS_DI
3. Then think... should you do the opposite?

---

## XIII. ⚠️ Risk Re-emphasis (This Section Is Must-Read)

### Backtesting Looks Great, Live Trading Needs Caution

ADX_15M_USDT2's historical backtesting might look okay—but there's a trap:

> **Simple strategies are easy to "fit," but also easy to overfit. More importantly, this strategy's signal direction might be problematic.**

Simply put: **Good historical performance doesn't guarantee future profits, and you might be trading in the wrong direction.**

### Hidden Risks of Simple Strategies

In live trading, overly simple logic can lead to:
- **Many False Signals**: One DI crossover and you enter, too much noise
- **Direction Might Be Wrong**: MINUS_DI crossing above is traditionally a short signal
- **Stop-Loss Too Wide**: -32% stop-loss means you might lose one-third

### My Advice (Honest Truth)

```
1. Change buy signal to PLUS_DI crossing above MINUS_DI (long signal)
2. Change stop-loss to -10% or tighter
3. Uncomment the ADX > 45 filter condition
4. Small capital backtesting verification
5. Paper trading for a week
6. Then decide whether to go live
```

**Remember**: No matter how simple the strategy, when the market teaches you a lesson, it doesn't give advance notice. Test with small positions, survival comes first! 🙏

---