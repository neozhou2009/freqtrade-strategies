# DIV_v1 Strategy: Plain English Edition

## 1. What Does This Strategy Do?

### One-Line Summary

DIV_v1 is a "bottom-fishing bounce" strategy — specifically designed to buy when price has fallen too much and shows signs of exhaustion, then profit from the bounce.

### Plain English Explanation

Imagine you're shopping at a supermarket. Something that usually costs $100 is now on sale for $80. You might think "that's cheaper, I could buy some." But what if it keeps falling to $60, $50, or even $40? How do you know when you've actually hit the "bottom"?

This strategy helps you judge: when has price hit bottom and it's time to buy?

But it doesn't simply say "buy when it's fallen a lot" — that gets you caught catching a falling knife. This strategy uses an indicator called RSI to help judge — when price is still falling, but RSI stops falling and starts rising, what does that mean? It means sellers are decreasing, buyers are starting to accumulate, and price might bounce!

### What Does the Strategy Name Mean?

DIV stands for Divergence (背离), v1 = first version.

What is "divergence"? Simply: price and indicator "get out of sync" — price goes down, indicator goes up. They're "diverging" from each other. That's a divergence signal.

Two types:
- **Bullish divergence (bottom divergence)**: Price makes new low, indicator doesn't → might rise
- **Bearish divergence (top divergence)**: Price makes new high, indicator doesn't → might fall

This strategy only uses bullish divergence, specifically for bottom-fishing.

---

## 2. What the Heck is RSI?

### Basic Concept

RSI = "Relative Strength Index" — one of the most classic and commonly used indicators in technical analysis, invented in 1978 and still going strong.

RSI is a number from 0 to 100:
- **Above 70**: Market "overheated" — price rose too fast, might pull back
- **Below 30**: Market "oversold" — price fell too fast, might bounce
- **Between 30-70**: Normal fluctuation zone

### Life Analogy

Think of RSI like a car's gas and brake:
- **High RSI (above 70)** = brake pressed too hard, engine overheating, need to ease up
- **Low RSI (below 30)** = gas tank nearly empty, need to refuel

This strategy specifically looks for "brake pressed too hard" situations — when RSI is below 30, market is oversold, time to pick up bargains and wait for bounce.

---

## 3. What Exactly IS Divergence?

### Nature of Divergence

Divergence is an important concept in technical analysis — simply put, "price action and indicator action are inconsistent."

Imagine you're watching someone climb stairs:
- **Normal case**: Climb one floor, get a bit tired; climb another floor, get more tired. Physical effort and climbing height are "in sync."
- **Divergence case**: Still climbing but getting easier, or getting more tired but still climbing. This is "divergence" — effort and performance not in sync.

In crypto terms:
- **Normal uptrend**: Price rises + RSI rises = momentum sufficient, will continue rising
- **Diverging uptrend**: Price still rising + RSI no longer rising = momentum weakening, might fall

This strategy watches for this "inconsistency." When price makes a new low but RSI doesn't make a new low, sellers' momentum is exhausted, buyers might counterattack. That's our entry signal!

---

## 4. How Does the Strategy Decide When to Buy?

The strategy requires BOTH conditions simultaneously:

**Condition 1: Price below Bollinger Band lower band**
This means price has become "too cheap" — cheap to an abnormal degree.

**Condition 2: RSI below 40**
This means market sentiment is very pessimistic — price has fallen enough.

When both conditions appear together, it's like two friends both saying: "Now is a great time to buy!"

Why both conditions? Because one indicator can lie, but both lying together is much less likely. Like how two people colluding to lie is harder than one person lying.

---

## 5. How Does the Strategy Decide When to Sell?

DIV_v1's exit logic is beautifully simple: **Sell when close price breaks above the Bollinger Band upper band.**

This symmetric structure — enter at lower band breakout, exit at upper band breakout — captures the complete mean reversion: from lower band bounce to upper band, completing a full volatility cycle.

---

## 6. What If Price Keeps Falling?

DD has "three lines of defense":

**First Defense: Fixed Stoploss at -15%**
If your loss reaches 15% after buying, the system auto-sells. This is more conservative than the original -32.745%.

**Second Defense: Trailing Stop**
After profit reaches 2%, the trailing stop activates. When price climbs, the stop level follows up. If price retraces 0.1% from peak, it sells and locks in profits.

**Third Defense: Time Stop**
- Immediately after entry: profit exceeds 10.35% → sell
- After 3 minutes: profit exceeds 5.05% → sell
- After 5 minutes: profit exceeds 3.35% → sell
- After 399 minutes (~6.5 hours): sell regardless!

---

## 7. What Market Conditions Suit This Strategy?

**Best for: Ranging markets**
Price bouncing back and forth in a range. DD is like a money-printing machine:
- Price hits lower band → buy
- Price hits upper band → sell
- Repeat...

**Bad for: Trending markets**
Price keeps going one direction. DD gets crushed:
- Price hits lower band → strategy buys
- Price keeps falling, lower still
- Strategy gets stopped out or trapped

---

## 8. Summary

**One-line**: Buy when price is "too cheap," sell when price is "not so cheap anymore."

**Buy conditions**: Close below Bollinger Band lower band AND RSI < 40

**Sell conditions**: Close above Bollinger Band upper band, OR stoploss triggered, OR trailing stop triggered, OR time limit reached

**Best for**: Ranging markets, not trending markets

**Risk control**: Fixed stoploss at -15%, trailing stop after 2% profit, maximum holding ~6.5 hours

**Final reminder**: Even the best strategy isn't a money printer. Markets always change. Backtest more, validate more, find what works for you!
