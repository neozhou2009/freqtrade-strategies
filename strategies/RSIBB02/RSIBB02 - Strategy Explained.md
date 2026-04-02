# RSIBB02 Strategy: The "Bargain Hunter" Strikes Back

> **Nickname**: Bargain Hunter, Bottom-Fishing Expert  
> **Occupation**: The "bold but careful" trader who catches falling knives  
> **Timeframe**: 1 Hour (1h)

---

## I. What is This Strategy?

Simply put, **RSIBB02** is a strategy that:

- Only strikes when prices hit "rock bottom"
- Waits for RSI to say "don't worry, it can bounce" before buying
- Takes profits quickly, never gets greedy

It's like a bargain hunter camping in the supermarket clearance aisle—doesn't show up normally, only strikes when good stuff gets thrown onto the clearance shelf! 🛒

---

## II. Core Configuration: "Fast In, Fast Out"

### Take-Profit Rules (ROI Table)

```
Holding Time        Target Profit
─────────────────────────────────────
Just bought         24% and run
After 13 minutes    5% and run  
After 51 minutes    1% and run
After 135 minutes   Break even and run (just don't lose)
```

**Translation**: This strategy is impatient—right after buying, it still hopes for 24% profit, but after two hours, it's happy just breaking even. Classic "got profit, get out fast, don't wait until it becomes a loss" mentality.

### Stop-Loss Rule

```
Cut losses at 12.5%
```

**Translation**: Gives plenty of room for the bounce, but if it really doesn't work out, take the ~12% loss and walk away. A relatively "forgiving" stop-loss.

---

## III. One Buy Condition: Simple and Direct

This strategy has just one buy condition, but it's pretty strict:

### 🎯 The Only Buy Condition: Bottom-Fishing Skill

**Core Logic**: Price falls outside the lower Bollinger Band + RSI hasn't reached "completely hopeless" territory

**The code looks like this**:
```python
(dataframe['rsi'] > 19) &
(dataframe["close"] < dataframe['bb_lowerband'])
```

**In plain English**:
> "Bro, the price has fallen outside the Bollinger lower band, and RSI is still above 19 which means it's not completely dead. Jump in now, and you'll probably catch a bounce!"

**Condition Breakdown**:

| Condition | Technical Term | Plain English Translation |
|-----------|----------------|---------------------------|
| RSI > 19 | RSI not below 19 | Don't catch the "dead never bounces" knives |
| Close < BB Lower | Price below Bollinger lower band | Price is ridiculously cheap! |

**Side Note**: This Bollinger Band uses 4x standard deviation! Normal is 2x. What does that mean? It means normally you can't touch the lower band—only when there's a real "crash" will it trigger a signal. This strategy is a classic "coward"—only strikes at extreme bargains. 😂

---

## IV. Sell Logic: Take Profits While You Can

### 4.1 Take-Profit: How Much Before Running?

```
The longer you hold, the lower your expectations
─────────────────────────────────────────────
Just bought      24%? Nice!
After a while     5%? Okay fine
After ages       1%? Better than nothing
After 2 hours    Break even? Let's go...
```

**Plain English**:
- Just bought: I want the big win!
- After a while: Fine, good enough
- After a long time: Break even is fine, just don't lose...

This mindset is just like you waiting for packages on双十一 (Double 11) 📦

### 4.2 Technical Sell Signal

```python
(dataframe['rsi'] > 83) &
(dataframe["close"] > dataframe['bb_middleband'])
```

**Plain English**:
> "RSI has hit 83, price is back above the Bollinger middle line, this rebound is about done, time to get out!"

| Condition | Plain English Translation |
|-----------|---------------------------|
| RSI > 83 | Rally is too hot, correction coming |
| Close > BB Middle | Price is back to normal range |

**Side Note**: RSI 83! Do you know how high that is? That's already "extremely overbought." This strategy bottoms-fishes aggressively and exits just as aggressively.

---

## V. Technical Indicators: Just Two, Simple!

### Core Indicators

| Indicator | Parameters | What It's For |
|-----------|------------|---------------|
| RSI | Default 14-period | Judge if it's fallen too much / risen too much |
| Bollinger Bands | 20-period, 4x standard deviation | Draw a "box"—price outside the box is abnormal |

### Bollinger Band's Special Configuration

This strategy uses **4x standard deviation** Bollinger Bands!

- Normal Bollinger Bands: 2x standard deviation, price frequently touches upper/lower bands
- This strategy's Bollinger Bands: 4x standard deviation, price touching lower band is a "once in a blue moon" event

**Plain English**: These Bollinger Bands are drawn super wide, like casting a net across the Pacific Ocean. Normally you catch nothing, but when you do catch something, it's a big one! 🐟

---

## VI. This Strategy's "Personality"

### ✅ Strengths (The Praise)

1. **Simple Logic**: Just two indicators, anyone can understand, no PhD in math needed
2. **High Signal Quality**: 4x standard deviation Bollinger Bands—rare signals but high quality
3. **Clear Risk**: Maximum 12% loss, you know what you're getting into
4. **Concise Code**: Less than 100 lines, easy to modify

### ⚠️ Weaknesses (The Criticism)

1. **Too Few Signals**: 4x standard deviation Bollinger Bands might go months without a signal—boring!
2. **Doesn't Adapt to Trends**: This is a range-bound strategy, might keep stopping out or missing out in trending markets
3. **No Trailing Stop**: Won't move stop-loss up when profitable, profits might give back
4. **ROI Precision Too High**: Take-profit numbers precise to 10+ decimal places, clearly a product of "over-optimization" 😅

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|--------------------| -------|
| 🔄 Range-bound market | ✅ Use heavily | Best scenario, harvest back and forth |
| 📈 Bull market | ⚠️ Use cautiously | Might miss the main uptrend, always trying to catch bottoms |
| 📉 Bear market | ❌ Don't use | Catching falling knives halfway up the mountain, ouch |
| ⚡ High volatility | ⚠️ Use carefully | May trigger signals but rebounds might fail |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Review
> "Zen bottom-fishing, quick to take profits—few signals but steady, for patient people."

### Who Should Use It?
- ✅ People with patience to wait for signals
- ✅ People who like simple strategies
- ✅ Range-bound market traders
- ✅ Beginners learning strategy development

### Who Shouldn't Use It?
- ❌ High-frequency trading seekers
- ❌ Trend-chasing enthusiasts
- ❌ Small capital wanting quick multipliers
- ❌ Impatient signal-waiters

### My Recommendations
1. **Backtest First**: Check historical data performance
2. **Small Position Test**: Verify with small capital in live trading
3. **Pair with Other Strategies**: Use this for range-bound, something else for trends
4. **Adjust Parameters**: 4x standard deviation might be too wide, try 3x

---

## IX. In What Market Can This Strategy Make Money?

### 9.1 Core Logic: Extreme Market Bottom-Fishing

RSIBB02 is a classic "bottom-fishing bargain" strategy. Less than 100 lines of code, simple enough to make you wonder "can this really make money?"

**Its Money-Making Philosophy**:

- **Doesn't Chase Rallies**: Doesn't care if price goes to the moon
- **Only Bottom-Fishes**: Strikes only when price falls to "ridiculous" levels
- **Quick Escape**: Takes a little profit and runs, never looks back

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:---------------------------|
| 🔄 Range-bound | ⭐⭐⭐⭐⭐ | This is its home field! Bottom-fishing rebounds back and forth, making bank |
| 📈 One-way uptrend | ⭐⭐☆☆☆ | Always trying to bottom-fish, price just keeps going up, missed the boat |
| 📉 One-way downtrend | ⭐⭐☆☆☆ | Bottom-fishing halfway up the mountain, still falling after buying, stopped out |
| ⚡ High volatility | ⭐⭐⭐☆☆ | More signals but rebounds might fail, depends on luck |

**One-Sentence Summary**: Range-bound markets are its home field, trending markets are its nemesis.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Side Note |
|-------------------|-------------------|-----------|
| Number of pairs | 3-5 | Too few = not enough signals, too many = can't manage |
| Asset selection | Major coins + oscillating coins | Don't pick those mooning/volatility-coins |

### 10.2 Key Config File Settings

```yaml
# Timeframe
timeframe: 1h

# Stop-loss
stoploss: -0.125

# ROI (can simplify)
minimal_roi:
  0: 0.24
  13: 0.05
  51: 0.01
  135: 0
```

### 10.3 Hardware Requirements (Almost None!)

This strategy has minimal computation:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|--------------------| -----------|
| 1-10 pairs | 1 GB | 2 GB | Smooth as silk |
| 11-30 pairs | 2 GB | 4 GB | Fluid |
| 31+ pairs | 4 GB | 8 GB | No problem at all |

**Warning**: This strategy has almost no hardware requirements, but don't get greedy! Signals are already rare, more pairs just means wasted effort. 😅

### 10.4 Backtest vs Live Trading

Backtest performance might look pretty, but in live trading watch out for:
1. **Slippage**: Bid-ask spread might be huge in extreme markets
2. **Liquidity**: Might be no one to take the other side in crashes
3. **Time Delay**: Signal to execution has latency

**Recommended Process**:
1. Backtest with 6 months of historical data first
2. Small position live test for 1 month
3. Adjust parameters based on performance
4. Gradually increase capital

**Don't go all-in right away**—no matter how good the strategy, it needs testing!

---

## XI. Easter Egg: The Strategy Author's "Little Quirks"

Looking carefully at the code, you'll find some interesting things:

1. **Bollinger Bands use 4x standard deviation**
   > "Normal people use 2x? Nah, I want 4x! Better to have fewer signals but higher quality!"

2. **ROI precision to 10+ decimal places**
   > "This was calculated by the optimizer... don't ask why so precise, it's science!"

3. **RSI thresholds 19 and 83**
   > "Most people use 30 and 70, I insist on 19 and 83. Only the extreme of the extreme is my cup of tea!"

This strategy is like a **"Zen Hunter"**—squatting most of the time, but when it strikes, it's going for the biggest one!

---

## XII. The Very Last Bit

### One-Sentence Review
> "Simple to the point of ridiculousness, steady enough to be reassuring. A harvester in range-bound markets, a missed-opportunity king in trending markets."

### Who Should Use It?
- ✅ Beginners learning
- ✅ Range-bound market traders
- ✅ Patient people
- ✅ Those who don't want complex strategies
- ✅ Small capital retail traders

### Who Shouldn't Use It?
- ❌ High-frequency trading seekers
- ❌ Those who like chasing rallies and selling dips
- ❌ Large capital needing diversification
- ❌ Impatient signal-waiters
- ❌ Those who only want trend strategies

### For Manual Traders

This strategy can be completely executed manually!

1. Open TradingView or exchange chart
2. Set to 1-hour timeframe
3. Add RSI(14) and Bollinger Bands(20, 4)
4. Wait for price to touch outside lower Bollinger Band + RSI > 19 to buy
5. Sell when RSI > 83 or price returns to middle band

**No need to run a bot, can do it manually!** 🎯

---

## XIII. ⚠️ Risk Re-emphasis (Read This Section!)

### Backtesting is Beautiful, Live Trading Be Careful

RSIBB02's backtest performance might be pretty—but note:

> **Because signals are rare, each trigger is an "extreme market event," and extreme markets are often accompanied by unpredictable volatility.**

Simply put: **"History rhymes, but doesn't repeat exactly."**

### Hidden Risks of Simple Strategies

In live trading, this "simple" strategy has pitfalls:

- **Bottom-Fishing Failure**: Price might continue crashing after breaking below Bollinger lower band
- **Liquidity Crisis**: In extreme crashes, might not be able to sell at all
- **False Signals**: Some crashes are real collapses, not rebound opportunities
- **Time Cost**: Signals too sparse, might go weeks without a single trade

### My Recommendations (Real Talk)

```
1. Don't use this strategy alone, pair it with a trend strategy
2. Single position controlled at 5-10%
3. Backtest first, then small position live test
4. Don't rush to bottom-fish in big crashes, wait for market to stabilize
```

**Remember**: No matter how simple the strategy, the market is always more complex. Staying alive is what matters! 🙏

---

**Final Reminder**: This strategy is the art of "waiting"—99% of the time waiting, 1% of the time acting. Don't use it if you don't have patience! 🎯