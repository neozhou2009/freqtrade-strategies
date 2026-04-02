# JustROCR Strategy Explained — The Lazy Person's Trend Follower

## 1. What Does This Strategy Do?

JustROCR is a momentum-chasing strategy—in simple terms, "discover it has risen, then buy."

Many beginners like bottom-fishing, thinking if price fell enough it should be bought. This strategy does the exact opposite—it doesn't bottom-fish, only chases momentum. Its logic: if a coin has risen more than 10% over the past three weeks, a trend has formed. Following that trend in, it will likely continue rising.

It's like surfing—surfing experts don't predict when waves form; they wait until waves are already forming, then chase them. JustROCR teaches you how to "surf" the crypto market.

Why is it called "JustROCR"? Because it uses only one indicator called ROCR, with nothing else fancy. "Just" means "only, merely"—the entire strategy relies on just this one indicator, simplified to the extreme.

This strategy is perfect for people who don't understand complex technical analysis. You don't need to know MACD, Bollinger Bands, or Elliott Wave Theory—just understand one indicator and you can follow trends and make money.

---

## 2. What Is the ROCR Magic Indicator?

ROCR's full name is Rate of Change Ratio.

Don't be scared by the name—the calculation is super simple:

**ROCR = Current Price ÷ Price N Periods Ago**

That's it! No complex formulas, no mysterious algorithms.

Example:
- Bitcoin current price: $50,000
- Price 500 candles ago: $45,000
- ROCR = 50,000 ÷ 45,000 = 1.11

This means Bitcoin has risen 11%.

ROCR values are easy to understand:
- ROCR = 1.00: No change
- ROCR > 1.00: Price rose, bigger number = more rise
- ROCR < 1.00: Price fell, smaller number = more fall

The biggest advantage of this indicator is its intuitiveness. At a glance, you know whether price has risen or fallen relative to history, and by how much.

JustROCR watches this ROCR value—when it exceeds 1.10 (meaning more than 10% rise), it decisively buys.

---

## 3. Why Use Such a Long Period of 499?

JustROCR uses 499 candles to calculate ROCR, on the 1-hour level.

499 hours is approximately 21 days, about three weeks.

Why such a long period? Three reasons:

**Reason 1: Filter noise**

Crypto's short-term fluctuations are wild—today up 5%, tomorrow down 3%, the day after up 2%. Watching too short a period makes these ups and downs dizzying, making you mistakenly think there's a trend.

Using a long period is like using a telephoto lens to take photos—close-range clutter gets blurred out, leaving only the main subject clearly visible. Three weeks is enough to filter short-term noise and show true trends.

**Reason 2: Reduce trading frequency**

Long periods mean fewer signals. This is actually good—more trades mean more fees and more mistakes. Fewer but higher-quality trades lead to better long-term returns.

**Reason 3: Capture big trends**

Big trends typically last longer. Using three weeks to judge trends filters out fleeting flickers and captures truly sustained major moves.

Of course, long periods have a downside: signals are lagged. By the time ROCR shows 1.10, the trend may already have risen 10%. That's the price of being a momentum chaser—you'll never buy at the absolute bottom, but you can buy at a trend-confirmed point.

---

## 4. When to Buy?

JustROCR's buy condition is so simple it makes you suspicious:

**When ROCR > 1.10, buy.**

That's it—no "and," "or," "if"—just buy whenever this indicator exceeds 1.10.

What does ROCR > 1.10 mean? It means current price is more than 10% higher than 499 hours ago.

Example:
- Ethereum current price: $2,200
- 21 days ago price: $2,000
- ROCR = 2,200 ÷ 2,000 = 1.10

At this point ROCR equals 1.10, the strategy hasn't bought yet. If price continues rising to $2,210, ROCR becomes 1.105, exceeds 1.10, and the strategy emits a buy signal.

Why wait for 10% rise to buy? Why not buy earlier?

Because a 10% rise isn't a small number. Rising this much means the coin really has upward momentum—not just random fluctuation. Like watching someone run—if they've only taken a few steps you can't tell if they're actually running, but if they've been running for 10 minutes straight, you know they're serious.

This is the strategy's philosophy: **I'd rather miss the fish head than miss the fish body.**

It doesn't care about catching the absolute bottom, only about following a confirmed trend for profit. Obviously, doing this misses the initial 10% profit, but换来 (trades for) higher certainty.

---

## 5. When to Sell?

Here's the most special thing about this strategy—**it has no active sell conditions!**

Look at the code:

```python
def populate_exit_trend(self, dataframe, metadata):
    dataframe.loc[
        (
        ),
        'sell'] = 1
    return dataframe
```

The condition section is empty! This means the strategy never actively tells you when to sell.

So how does it exit? Entirely via the stop-loss mechanism. It's like setting a "smart exit line" after buying a stock—as long as price doesn't fall below this line, hold; once it falls below, auto-sell.

Benefits of this design:

**Won't exit too early**

Many strategies set target prices like "sell when up 20%." But what if it continues rising after hitting 20%? You'd miss the big move. JustROCR doesn't set target prices, letting profits run as far as possible.

**Reduces judgment errors**

Exit timing is often harder to judge than entry timing. Not setting active exit conditions actually reduces judgment mistakes.

**Trusts trend power**

If what you bought is a genuine uptrend, it should continue for some time. Not actively selling gives trends sufficient room to develop.

Of course, this design has risks—if the trend suddenly reverses, you may give back significant profits. That's why the strategy emphasizes stop loss so much.

---

## 6. How Does Stop Loss Work?

JustROCR sets a fixed stop loss: **-20%**.

This means: if you buy at $100 and price falls below $80, the strategy auto-sells.

Why 20%, not 10% or 30%?

**10% is too tight**

Crypto volatility is high—10% swings in a single day are normal. If stop loss is set at 10%, normal fluctuations could trigger it, washing you out, then price rebounds. You'd unfairly lose money and miss the subsequent rise.

**30% is too loose**

If stop loss is 30%, a single loss is huge. $100 losing $30 requires a 43% gain to break even. A few consecutive losses and the account can't handle it.

**20% is just right**

20% is a balance—not so tight that normal crypto swings trigger it, yet still protecting you from major declines in genuine downtrends.

Plus, with trailing stop, actual losses are usually much less than 20%. Only in extreme situations (sudden crashes) would you lose the full 20%.

---

## 7. What Are the Benefits of Trailing Stop?

JustROCR enables trailing stop—a particularly clever function.

Regular stop loss is fixed—if you buy at $100 with stop at $80, no matter how high price rises, the stop stays at $80.

Trailing stop is dynamic—it follows price upward.

Example:
- Buy at $100, initial stop at $80 (20% loss)
- Price rises to $120, trailing stop may move up to $100 (breakeven)
- Price rises to $150, trailing stop may move up to $120 (locks in 20% profit)
- Price rises to $200, trailing stop may move up to $160 (locks in 60% profit)
- Price retraces to $160, triggers stop—sold at $160, 60% profit!

See? You bought at $100 but ultimately sold at $160, earning 60%. Without trailing stop, you might not have sold at $200, then price crashed back to $80 triggering stop—going from +100% to -20%.

Trailing stop benefits:
- **Auto-locks profits**
- **Lets profits run**
- **Overcomes greed and fear**

---

## 8. Strategy Advantages

**Advantage 1: Simplest possible**

Core strategy code under 30 lines, uses only one indicator. No advanced math needed, just understanding "current price divided by past price."

**Advantage 2: Won't bottom-fish at the mid-mountain**

Many beginners like bottom-fishing, buying more as it falls, resulting in mid-mountain positions. This strategy doesn't bottom-fish, only chases trends.

**Advantage 3: Auto-protects profits**

Trailing stop automatically locks profits—you don't worry about "gained but didn't exit, now at a loss."

**Advantage 4: Low overfitting risk**

Few parameters: ROCR period (499), entry threshold (1.10), stop loss (20%). Fewer parameters = lower overfitting risk.

**Advantage 5: Low trading frequency**

Long-period indicator means infrequent signals—saves fees, saves stress, each signal more reliable.

---

## 9. Strategy Disadvantages

**Disadvantage 1: Loses money in ranging markets**

Biggest disadvantage. If price wobbles within a range, ROCR repeatedly crosses 1.10—you buy, get stopped, sell; price rises again, you buy, get stopped again... After several rounds, fees and stops accumulate.

**Disadvantage 2: Signal lag**

Waits for ROCR > 1.10 to buy, by which time trend has already risen 10%. Misses the bottom 10%.

**Disadvantage 3: Trend reversals may give back profits**

No active exit conditions, entirely relying on stop loss. If trend reverses quickly, you may go from +50% to exiting at +20%—giving back that 30% in the middle.

**Disadvantage 4: Ignores volume**

This strategy completely ignores volume. Sometimes price rises but volume is low—this may not be a healthy rise and could reverse. But the strategy doesn't care, buying whenever ROCR exceeds 1.10.

**Disadvantage 5: Uses only one indicator**

Simplicity is an advantage but also a risk. No other indicators to confirm signals—if ROCR gives false signals, there's no backup plan.

---

## 10. What Markets Suit This?

**Best: Unilateral bull markets**

When market continuously rises—today up, tomorrow up, the day after still up—JustROCR performs great. ROCR stays above 1.10, you buy and price continues rising, trailing stop follows up, ultimately capturing big profits.

**Better: Mildly oscillating uptrends**

Price sometimes rises sometimes falls but overall upward. Trailing stop filters minor fluctuations, capturing big trends.

**Okay: Slow bull markets**

Slow but steady rises. ROCR may barely cross 1.10, limited profit room after buying, but at least won't lose.

**Best coin types: Mainstream coins**

Bitcoin, Ethereum and similar—they trend relatively stably, harder to manipulate, good liquidity, minimal trailing stop slippage.

**Not for: Wild altcoin markets**

Those extremely volatile altcoins—today up 50%, tomorrow down 30%. Such coins easily trigger repeated stops, wearing you down.

---

## 11. What Markets Don't Suit This?

**Ranging oscillating markets**

Price fluctuates within a range—up a bit today, down a bit tomorrow, ends up原地 (in the same place) after a week. This is a trend strategy's nightmare.

**Rapid drop markets**

If market suddenly crashes, JustROCR becomes passive. ROCR won't exceed 1.10 in downtrends so you won't buy, but if holding a position it may not sell fast enough before hitting stop.

**High volatility directionless markets**

Sometimes markets are volatile with big up and down moves but no overall direction—today up 10%, tomorrow down 10%. These lose money most easily.

**Low-liquidity markets**

Some small coins have very low volume, wide bid-ask spreads. When you want to stop loss, there may not be enough buyers, causing actual fills far worse than expected.

---

## 12. Notes for Using This Strategy

**First: Backtest!**

Don't start with real money! Backtest with historical data first—see how it performed over the past year or two. If backtesting loses money, don't use it.

**Second: Start with small money**

Even if backtesting looks good, don't go all-in. Start with small money to test the water.

**Third: Manage position size**

Don't put all money on one strategy, one coin. JustROCR is just one tool—combine with other strategies and coins.

**Fourth: Watch maximum drawdown**

Maximum drawdown is how much it fell from peak to trough. If drawdown exceeds your tolerance, consider pausing or adjusting.

**Fifth: Pay attention to market environment**

In clearly unsuitable environments (like ranging markets), consider pausing. Don't use momentum strategies in major bear markets.

**Sixth: Understand your coins**

Each coin has different characteristics. Bitcoin is relatively less volatile; altcoins are more volatile. May need to adjust stop-loss ratios for different coins.

**Seventh: Stay mentally steady**

Strategy runs with consecutive losses sometimes—this is normal. Don't doubt the strategy just from a few consecutive stops and quit. Long as overall returns are positive, short-term losses are acceptable.

**Eighth: Continuous monitoring**

Though automated, regularly check its performance. If performance continuously deteriorates, market conditions may have changed—need parameter adjustments or pausing.

---

## 13. Summary

JustROCR is an extremely simple momentum-chasing strategy. Its core: **wait for 10% rise, then buy; protect profits with trailing stop.**

It's like a lazy person's investment assistant:
- Doesn't require watching charts all day
- Doesn't need analyzing complex indicators
- Doesn't require judging when to sell

It automatically:
- Finds coins with established uptrends
- Buys at the right time
- Protects your profits
- Exits timely when trends reverse

It's suitable for:
- Beginners who don't understand complex technical analysis
- Office workers without time to watch charts
- People wanting simple strategies

It's not suitable for:
- Ranging markets
- People who want to buy at the absolute bottom
- Day traders who trade frequently

Remember: **No perfect strategy, only suitable strategies.** Some people use this well, some don't. Key is understanding its characteristics, using it in the right market environment, and managing risk well.

**Final reminder: Strategy is just a tool; the key to making money is execution and risk management.**

---

*This is the colloquial version of JustROCR Strategy.*
