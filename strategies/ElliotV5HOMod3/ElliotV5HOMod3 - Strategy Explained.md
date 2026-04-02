# ElliotV5HOMod3: Plain and Simple

## 1. What Is This?

ElliotV5HOMod3 is an auto crypto trading strategy. The core idea: **don't buy at full price, wait for a discount; don't wait forever for maximum profits, lock in when you've made enough.**

Uses Elliott Wave theory — market prices move in waves. The strategy waits for the small retreating waves (pullbacks) to hop on, then sells when the tide carries you to shore.

## 2. Two Ways to Buy

### Way 1: Catch the Pullback Discount (Main Way)

Market is going up. Price pulls back a bit. Conditions:
- Price is about 2.2% below the moving average (a "discount")
- EWO > 3.34: Short-term dip, but overall still climbing strong
- RSI < 60: Hasn't gotten overheated
- Volume > 0

All four must line up. Strategy says: "OK, the discount is real, the trend is still good, this is a good entry."

### Way 2: Catch the Panic (High Risk/High Reward)

Market crashes hard, everyone panicking. Conditions:
- Price is ~2.2% below moving average
- EWO < -17.457: EXTREMELY oversold, like a rubber band pulled way too tight
- No RSI check (when EWO is this extreme, RSI is already in the gutter)

Why no RSI check? Because when EWO is at -17, RSI is definitely already below 60 (probably below 30). Adding that check would just filter out valid bottom-catch signals.

## 3. How It Sells

The strategy sells when price rises to about 1.1% above the sell MA.

But here's the thing: **technical sell signals are turned off!** It doesn't use them. Instead, it relies on:
- ROI target (7%)
- Trailing stop
- Fixed stop-loss
- Custom dynamic stop

This means: "Trust the numbers, not the charts" — emotions removed from exits.

## 4. How It Protects You

### Layer 1: Fixed Stop-Loss — 6%

This is the tightest stop among all the V5 variants. If you're down 6%, get out. 

This is good for capital preservation but means you might get stopped out by normal crypto volatility more often.

### Layer 2: Trailing Stop (The Lock)

After you make 3% profit:
- Trailing stop activates
- Tracks the peak, stays 0.5% below it
- If price pulls back 0.5% from peak → SELL

Example: Buy at $100, climbs to $103 (3% profit) → activates. Climbs to $110 → stop at $109.45. Drops to $109.45 → sells, locks in ~9.45% profit.

### Layer 3: Custom Dynamic Stop

This is smart — the stop tightens as you make more:

| If profit is... | Stop sits at... | Meaning |
|----------------|----------------|--------|
| Above 3% | 1% below current | Made enough, protect it |
| 1.8% to 3% | 0.5% below current | Starting to profit, guard it |
| Below 1.8% | Almost disabled | Let it breathe |

### Layer 4: ROI Target — 7%

Single flat target. Make 7% → sell. Done. Move on to the next trade.

This is simpler than some variants that tier their targets. Less adaptive to slow-and-steady trends, but cleaner.

## 5. The Indicators

### EWO

Short EMA (50) minus Long EMA (200), divided by price × 100.

Think of it like a car's dashboard: when the speedometer (short-term) shoots way above the trip average (long-term), you're accelerating. When it drops way below average, you're braking hard. EWO > 3.34 means accelerating. EWO < -17.457 means braking too hard — something's gotta give.

### EMA

Moving average of past prices. EMA(17) for buying, EMA(39) for selling. Why different lengths? Buy fast (react quickly), sell slow (don't panic exit).

### RSI

Classic overbought/oversold gauge. Below 60 for buying — don't buy when everyone's euphoric.

## 6. Pros and Cons

### Pros
- **Capital protective**: Tight -6% stop is conservative
- **Clear target**: 7% ROI, simple and decisive
- **Smart stops**: Dynamic stop tightens as you profit
- **Two modes**: Both pullback-buying and crash-catching

### Cons
- **Single ROI**: Not tiered — might exit too early in slow trends
- **Tight stop**: May get stopped out by normal swings more often
- **1-hour data unused**: Defined but not utilized

## 7. Who Is This For?

**Good for:**
- Conservative traders who prioritize not losing
- People who want clear, simple targets
- Those who understand Elliott Wave basics

**Not ideal for:**
- Aggressive traders who want to ride full trends
- People who can't handle being stopped out frequently
- Fans of complex multi-tiered exit strategies

## 8. Summary

ElliotV5HOMod3 is the "safety-first" variant in the V5 family:
- Tightest stop-loss (-6%)
- Single 7% target
- Dynamic stop that guards growing profits
- Two-entry design for trending and crash scenarios

Choose this variant if you want tighter capital control. Choose others if you want to ride trends longer.

**No strategy is perfect. Backtest first, start small, monitor always.**

---

*For learning reference only, not investment advice.*
