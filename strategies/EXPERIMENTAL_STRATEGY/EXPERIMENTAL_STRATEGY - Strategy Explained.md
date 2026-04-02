# EXPERIMENTAL_STRATEGY: What's This Thing?

## 1. What Does This Strategy Do?

Hey, ever wondered if you could get a computer to trade crypto for you? Well, EXPERIMENTAL_STRATEGY is basically that — an automated trading bot. Don't let the "experimental" label scare you off; it's actually pretty solid. This strategy watches candlestick charts, crunches a bunch of technical indicators, and then tells you: "Hey, good time to buy!" or "Hey, maybe take profits now!"

In a nutshell, this strategy is a **trend-following + oversold bottom-catch hybrid**. What does that mean? When the market is doing well, it rides the trend up. When prices have tanked too hard, it buys the dip. When prices have run up too far, it sells. See? Not so complicated.

## 2. How Does This Strategy Make Money?

The strategy has two ways to pocket gains:

### Scenario 1: Catching a Rebound After a Dip

Think of it like shopping — everyone knows you should buy when things are on sale. This strategy watches the RSI and Stochastic indicators. When both say "way oversold" (prices dropped too much), AND the trend is still intact (ADX is strong enough), it says: "This is the moment! Time to buy the dip!"

But it's not blindly catching a falling knife. It needs several conditions to line up:
- RSI must be below 35 (oversold)
- Stochastic indicator must also be below 35 (confirming oversold)
- ADX must be above 30 (trend is still there)
- The bullish direction indicator (+DI) must be above 0.5 (direction is correct)

Think of it like grocery shopping: you don't just check if the price is good, you also check if the produce is fresh, if it's in season, and if the vendor is trustworthy. Multiple conditions all lining up = green light to buy.

### Scenario 2: Chasing a Strong Trend

Sometimes the market is on an absolute tear, going up and up. What do you do? The strategy says: "Get on board!"

When the trend is extremely strong (ADX above 65), AND it's a bullish trend (+DI above 0.5), the strategy fires a buy signal. This is called "momentum chasing" — price doesn't matter, the trend is powerful, so you follow it.

This is like seeing a crazy line outside a new restaurant and deciding to join it. "So many people in line, it must be good, right?"

## 3. When Does It Sell?

You gotta sell to actually lock in profits, right? This strategy has two exit scenarios:

### Exit Scenario 1: It's Gotten Too Expensive — Time to Go

When the RSI or Stochastic indicator crosses above 70 (overbought territory), AND some bearish pressure starts showing up (minus_di > 0), the strategy says: "That's enough! Take your profits and run!"

### Exit Scenario 2: It's Gone Way Too Far — Run for the Hills!

When ADX climbs above 70, the trend has gotten dangerously extreme. As the old saying goes: "What goes up too far must come down." At this point, bearish pressure is building up (minus_di > 0.5), and the strategy says: "Don't get greedy! Exit now!"

Think of it like playing mahjong — if you've won a good chunk, it's time to call it a night. Don't let those winnings slip away!

## 4. What "Weapons" Does This Strategy Use?

This strategy employs a whole arsenal of technical indicators. Let me break them down one by one:

### Weapon 1: ADX (The Trend Strength Meter)

ADX doesn't tell you which way the trend is going — it tells you **how strong the trend is**.

Think of it like sailing: ADX tells you how big the waves are:
- ADX below 25: Tiny ripples, the boat barely moves — this is a "range-bound market"
- ADX between 25 and 50: Moderate waves, the boat is making progress — "there's a trend"
- ADX above 50: Big waves, the boat is flying — "strong trend"
- ADX above 70: Waves are SO big the boat might capsize — "extreme trend"

The strategy requires ADX to be at least above 30 before buying, to make sure there's actually a trend before taking action. It won't waste time in "dead water" (flat markets).

### Weapon 2: RSI (The Strength Meter)

RSI stands for "Relative Strength Index." Put simply, it tells you if a price is "too expensive" or "too cheap."

- RSI above 70: Price is too high, might drop — called "overbought"
- RSI below 30: Price is too cheap, might rise — called "oversold"

The strategy sets the oversold threshold at 35 (instead of the usual 30) and the overbought at 70, a slightly more conservative setup.

### Weapon 3: Stochastic Indicator (The Fast/Slow Meter)

The Stochastic indicator answers: "Where is the current price in relation to its recent high-low range?"

- Indicator above 80: Price is near recent highs, might drop
- Indicator below 20: Price is near recent lows, might rise

The strategy uses "Stochastic Fast" (Stoch Fast), which responds more quickly to price changes.

### Weapon 4: +DI/-DI (The Direction Indicators)

These two indicators tell you which way the wind is blowing:
- +DI is high: Bulls are in charge, price going up
- -DI is high: Bears are in charge, price going down

For buying, the strategy requires +DI above 0.5, making sure the direction is actually upward. For selling, it requires -DI above 0, confirming bearish pressure has arrived.

### Weapon 5: MACD (The Trend Confirmer)

MACD is made of two lines — a fast one and a slow one — plus a histogram.
- Fast line crosses above slow line: Golden cross, bullish
- Fast line crosses below slow line: Death cross, bearish

However, this strategy calculates MACD but currently doesn't use it for signals. It's sitting in the "backup weapons" locker.

### Weapon 6: Bollinger Bands (The Price Channel)

Bollinger Bands are three lines: upper band, middle band, and lower band. Price usually bounces between these lines.
- Price hits the upper band: Might drop
- Price hits the lower band: Might bounce
- Channel gets narrow: Big move might be coming

Again, this strategy calculates Bollinger Bands but hasn't put them to use yet. Maybe for later.

### Weapon 7: Moving Averages (EMA and SMA)

A moving average smooths out past prices into a line:
- EMA (Exponential Moving Average): Gives more weight to recent prices, responds faster
- SMA (Simple Moving Average): Treats all prices equally, smoother

The strategy calculates EMA(10) and SMA(40) — one fast, one slow — but hasn't used them yet.

## 5. What Do the Time Settings Mean?

### Timeframe: 5 Minutes

This strategy uses 5-minute candlesticks, analyzing price action every 5 minutes. This is "short-term trading," ideal for folks who want to get in and out within a single day.

### Take-Profit: Tiered and Declining

The take-profit design is pretty clever — it **decreases over time**:

| Time After Opening | Profit Target |
|-------------------|---------------|
| Right after entry | 4% |
| After 20 minutes | 2% |
| After 30 minutes | 1% |
| After 40 minutes | 0% |

What does this mean? Here's the breakdown:
- If the price jumps 4% right after buying, take profits immediately
- If it didn't hit 4%, after 20 minutes even 2% is good enough
- After 30 minutes, even 1% will do
- After 40 minutes, get out even if it's break-even

Great design: **wants quick money, exits if it doesn't work, never holds on too long.**

### Stop-Loss: -10%

If you lose 10%, it's time to admit defeat and exit. This stop-loss is a bit wide — for a 5-minute trading timeframe, 10% is on the larger side. You might want to tweak this yourself.

## 6. What Are the Strategy's Strengths?

### Strength 1: It's Not Relying on One "Guess"

This strategy uses a whole bunch of indicators together to make decisions, like needing to pass multiple exam subjects before you pass overall. This cuts down on false signals so one wonky indicator going haywire won't trash your whole trade.

### Strength 2: Two Entry Methods, Handles Any Market

- Good market: Chase the trend, ride the gains
- Dropped too far: Buy the dip, grab the bargain

Whatever the market's doing, there's an opportunity.

### Strength 3: Trend Filtering, Doesn't Waste Time in Flat Markets

ADX must be above 30 to trade. This filters out a LOT of false signals in choppy markets. When the market keeps going up and down without direction, the strategy sits still — and that's pretty smart.

### Strength 4: Both Take-Profit and Stop-Loss, Risk Control is Decent

Tiered take-profit + fixed stop-loss means there's at least a risk boundary. You won't lose unlimited, and you won't wait forever for profits.

### Strength 5: Buy and Sell Logic Are Symmetric, Easy to Understand

When buying it checks certain indicators; when selling it checks similar ones. The logic is symmetrical — easy to understand and easy to optimize.

## 7. What Are the Strategy's Weaknesses?

### Weakness 1: Parameters Are Hard-Coded

RSI thresholds, ADX thresholds — all fixed numbers that can't automatically adjust to changing markets. Bull market might need one set of parameters, bear market another. This strategy won't figure that out on its own.

### Weakness 2: Chasing Could Buy You at the Top

Entry Signal 2 says "buy when the trend is extremely strong." But extremely strong trends are sometimes also at the TOP. Chasing in there could get you caught holding at a peak.

### Weakness 3: Stop-Loss is a Bit Wide

For 5-minute trading, a 10% stop-loss is on the wide side. You might see this happen: strategy says "hang in there," and then it gets stopped out at 10%. Ouch.

### Weakness 4: Some Indicators Are Calculated But Never Used

Bollinger Bands, MACD, moving averages — all computed but not put into signals. That's a bit wasteful.

### Weakness 5: No Position Management

The strategy doesn't say how much to buy or sell — it's all fixed quantity. If your capital goes up or down, there's no automatic adjustment.

## 8. What Situations Is This Strategy Good For?

### Good Markets:

1. **Pullbacks in an Uptrend**: The bottom-catch signal shines here
2. **Breakout Moves**: The momentum chase signal handles breakouts
3. **Coins with Moderate Volatility**: Too little volatility = no profit margin, too much = too risky

### Bad Markets:

1. **One-Sided Drops**: Buying the dip in a falling market is like catching a falling knife
2. **Flat/Choppy Markets**: ADX too low, strategy barely trades
3. **Extreme Mania Spikes**: Momentum chase might buy at the absolute top

### Good For:

1. **People with coding skills**: Can read the code, tweak parameters
2. **People with time to spare**: 5-minute timeframe needs regular attention
3. **People with moderate risk tolerance**: 10% stop-loss isn't small change

## 9. How to Use This Strategy?

### Step 1: Understand the Logic

Read this document a few times. Make sure you get when it buys, when it sells, and why it's designed that way.

### Step 2: Run Historical Backtesting

Don't jump in with real money right away! Test it with historical data first:
- Use Freqtrade's backtesting feature
- Pick at least 6 months of historical data
- Check return rate, max drawdown, win rate, and other metrics

### Step 3: Paper Trading

If backtesting looks good, run it on a simulated account for a while (at least 2 weeks) and see how it performs in real time.

### Step 4: Small-Capital Live Trading

If the simulated account is making money, try it with real money — but small! Don't go all-in right away!

### Step 5: Gradually Increase Capital

When small-capital live trading is consistently profitable, slowly add more capital. Remember: **there is risk in investing, so enter the market cautiously.**

## 10. How Can This Strategy Be Improved?

### Improvement 1: Make Parameters Adjustable

Right now everything is hard-coded. Turn them into adjustable parameters so you can optimize via backtesting to find the best combo.

### Improvement 2: Use Those "Dusty" Indicators

Bollinger Bands, MACD, moving averages — all calculated but not used. Add them to signal conditions:
- Buy when price is near Bollinger Band lower rail = safer entry
- MACD golden cross confirms buy signal
- Moving average support as buy reference

### Improvement 3: Add Volume Confirmation

When price moves, check the volume too. Rising volume on the way up = real strength. Rising price on falling volume = fake move.

### Improvement 4: Add Time Filtering

Some time periods just have bad market conditions. Set up "trading hours" — skip weekends, skip major news release times.

### Improvement 5: Dynamic Position Management

Add to positions when winning, reduce when losing — that's more scientific.

### Improvement 6: Add Market Environment Detection

Use different parameters for bull vs. bear markets:
- Bull market: More aggressive momentum-chase parameters
- Bear market: More conservative bottom-catch parameters

## 11. Quick Reference: Buy & Sell Signal Cheat Sheet

### Buy Signal Cheat Sheet:

**Signal 1: Oversold Rebound**
| Condition | Meaning |
|-----------|--------|
| RSI < 35 | Dropped too much, cheap |
| fastd < 35 | Confirms it's dropped too much |
| ADX > 30 | Trend is still supporting |
| +DI > 0.5 | Direction is upward |

**Signal 2: Strong Trend Chase**
| Condition | Meaning |
|-----------|--------|
| ADX > 65 | Trend is extremely strong |
| +DI > 0.5 | Bullish direction |

### Sell Signal Cheat Sheet:

**Signal 1: Overbought Exit**
| Condition | Meaning |
|-----------|--------|
| RSI crosses 70 OR fastd crosses 70 | Got too expensive |
| ADX > 10 | Basic trend confirmed |
| -DI > 0 | Bearish pressure appearing |

**Signal 2: Extreme Reversal**
| Condition | Meaning |
|-----------|--------|
| ADX > 70 | Trend peaked at extreme |
| -DI > 0.5 | Strong bearish pressure |

## 12. Real Case Simulations

### Case 1: Oversold Rebound Buy

Say a certain coin's price has dropped for several days in a row:

1. RSI dropped to 28, below 35 ✓
2. Stochastic fastd also dropped to 30, below 35 ✓
3. ADX is still 32, showing trend is still there ✓
4. +DI is 8, above 0.5 ✓

All conditions met, strategy fires a buy signal!

A few hours later, the price climbed 3%, RSI crossed above 70, strategy fires a sell signal, +3% profit. Done.

### Case 2: Momentum Chase Buy

Say a certain coin suddenly goes on a tear:

1. ADX spikes to 68, above 65 ✓
2. +DI is 15, above 0.5 ✓

Buy Signal 2 conditions met, strategy buys!

The trend is very strong at this point, price continues climbing to +5%. Then ADX hits 72, above 70, AND -DI starts showing up (above 0.5), strategy fires Sell Signal 2, exits with +5% profit.

### Case 3: Choppy Market, No Trading

Say the market is stuck in a sideways grind:

1. RSI hovers around 50
2. ADX is only 15, below 30

Because ADX is too low, trend isn't strong enough, strategy chooses **not to trade**, avoiding repeated small losses from choppy market whipsaws.

## 13. Final Summary

### One-Line Summary

This strategy: **when there's a trend, follow it; when it's dropped too much, buy the dip; when it's run up too far, sell; when the trend hits extreme, sell anyway.**

### Best Use Cases

- People with some coding background
- Willing to spend time on backtesting and optimization
- Moderate risk tolerance
- Primarily trading mainstream coins
- Short-term trading style

### Key Things to Watch Out For

1. **Don't go live right away**: Backtest first, then simulate, then small-capital live
2. **Watch the stop-loss**: 10% is a bit wide — adjust based on your own situation
3. **Be careful chasing momentum**: Buying at extreme trend peaks might get you caught
4. **Optimize parameters**: Different markets and coins may need different parameters

### Remember This

**Strategy is a tool; the person is the core.** No strategy is a "money printer." You need to keep learning, testing, and optimizing. This experimental strategy gives you a framework — how well you use it is up to you!

---

*This colloquial version is here to help you quickly grasp the core logic of the strategy. If you want to dive into the technical details, check out the "Strategy Analysis" version. Happy trading!*

---

*Disclaimer: The above content is for reference and study only, and does not constitute any investment advice. Quantitative trading involves risk, so invest cautiously!*
