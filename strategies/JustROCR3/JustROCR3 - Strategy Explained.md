# JustROCR3 Strategy Explained — The "Small Losses, Big Wins" Momentum Strategy

## Opening: What Is This Strategy?

JustROCR3 is a simple, direct momentum-tracking strategy. Its core idea in one sentence: **when price rises more than 10% over two days, chase in and buy, then use trailing stop to protect profits.**

Sounds simple, right? Exactly—this strategy pursues simplicity. It uses only one indicator called ROCR, sets one buy threshold, then relies on strict stop loss to control risk. Unlike those strategies with tons of indicators and lots of lines, JustROCR3 is: "recognize one signal, take action."

The strategy name is interesting. "Just" means "only," implying it uses just one indicator; "ROCR" is the indicator name; "3" is probably the version number.

---

## Chapter 1: Understanding ROCR First

ROCR's full name is Rate of Change Ratio. The calculation is super simple:

**ROCR = Current Price ÷ Price N Days Ago**

Example: Bitcoin current price $55,000, N days ago $50,000, ROCR = 55,000 ÷ 50,000 = 1.1

What does this mean?
- ROCR > 1: Price rose, bigger number = bigger rise
- ROCR = 1: No change
- ROCR < 1: Price fell, smaller number = bigger fall

ROCR measures "how much price changed over this period"—just ratio, no complicated formula.

JustROCR3 uses period 499. On 5-minute candles, 499 periods is about 41 hours, almost two days. So this strategy watches: **is current price higher or lower than two days ago?**

---

## Chapter 2: How Does It Buy and Sell?

JustROCR3's rules are super simple.

**Buy condition, just one: ROCR > 1.10**

Meaning: when current price has risen more than 10% compared to two days ago, buy.

Why wait for 10% rise?
1. **Confirms trend is real**: Rising 2-3% might be normal fluctuation; rising 10% means someone is really buying
2. **Avoids false breakouts**: Price often spikes then drops—waiting for 10% filters many false moves
3. **Trades safety for some profit**: Misses the 0% to 10% range but avoids being trapped in false breakouts

**Sell condition? Interestingly—none!**

The strategy won't actively sell because "price is enough" or "indicator changed." Its selling relies entirely on two mechanisms:

1. **Fixed stop loss**: If price drops 1% after buying, immediately stop out
2. **Trailing stop**: If making money, stop line follows upward, locking in profits

So the strategy's philosophy: **just manage the buy, let stop loss decide when to exit.**

---

## Chapter 3: Stop Loss—The Core of This Strategy

JustROCR3's stop loss is the most interesting and controversial part.

**Fixed stop loss: 1%**

What does this mean? After buying, if price drops more than 1%, the strategy auto-sells.

1% is extremely tight. Many coins swing more than 1% in a single day!

Why so tight?
- **Fast error recognition**: If it drops right after buying, the judgment was wrong—exit quickly
- **Control losses**: Each stop loss is only 1%; even 10 consecutive stops equal only 10%
- **Avoid slow bleed**: Don't let small losses become big losses

This design says: "I'm betting you'll rise after I buy. If you actually rise, I hold; if you drop, I immediately admit defeat and minimize the loss."

**Trailing stop: Let profits run**

Only fixed stop loss? If it rises 50% then drops back to cost basis, you'd exit at breakeven. So the strategy also enables trailing stop.

Trailing stop means: **as price rises, the stop line follows upward.**

Example:
- Buy at $100, stop line at $99 (1% down)
- Price rises to $120, trailing stop moves up to, say, $110
- Price rises to $150, trailing stop moves up to $138
- Price retraces to $138, triggers stop—sold, 38% profit!

Trailing stop benefit: **you don't worry about rising then falling back—you lock in profits as it climbs.**

---

## Chapter 4: How This Strategy Makes Money

JustROCR3's money-making logic: "small losses, big wins."

**When losing**: Stop loss is 1%, each loss is small.

**When winning**: Catch a big trend, might rise 20%, 50% or more—trailing stop locks in most of it.

The math:
Assume 10 trades:
- 6 stop outs, each losing 1%, total -6%
- 3 small wins, averaging 5% each, total +15%
- 1 big win, +30%

Total across 10 trades: 15% + 30% - 6% = 39%

This is the core of momentum strategy: **don't need every trade to win, just need wins to win big and losses to stay small.**

---

## Chapter 5: When Is This Strategy Best?

JustROCR3 is best in: **markets with clear upward trends.**

Imagine:
- Bitcoin rises from $30,000 to $40,000
- Small pullbacks along the way, quickly rising again
- You use this strategy—might get stopped out a few times, but ultimately capture most of the rise

**When it's not suitable:**

1. **Ranging markets**: Price wobbles up and down—ROCR repeatedly crosses 1.10, you buy and get stopped, repeat
2. **Rapid reversals**: You chase in, price immediately reverses—1% stop might not even be fast enough
3. **Low-liquidity coins**: Stop loss may not execute at expected price, actual loss bigger than 1%

**Suitable trader types:**
- Momentum believers
- People who can accept frequent stops (good mentality)
- People who don't want to watch charts
- People with sufficient capital

---

## Chapter 6: A Complete Trade Example

Bitcoin current price $50,000, price two days ago $45,000, ROCR = 50,000 ÷ 45,000 = 1.11.

Since 1.11 > 1.10, buy condition met, strategy buys at $50,000 on next candle open.

**Scenario A: Bought right, trend continues**

Price rises:
- Rises to $52,000, trailing stop moves to $51,500
- Rises to $55,000, trailing stop moves to $54,000
- Rises to $60,000, trailing stop moves to $58,000
- Pulls back to $58,000, triggers stop—sold!

Result: +16% profit, trade done.

**Scenario B: Bought wrong, trend reverses**

Price drops:
- Falls from $50,000 to $49,500, down 1%, triggers fixed stop

Result: -1% loss, trade done.

**Scenario C: Oscillates, rises then falls**

Price first rises then drops:
- Rises from $50,000 to $53,000, trailing stop moves to $52,500
- Then price starts dropping, falls to $52,500, triggers stop

Result: +5% profit, trade done.

Three scenarios, only B loses, and only 1%! Both A and C are wins, just different amounts.

---

## Chapter 7: Where Do These Parameters Come From?

**ROCR period: 499**

Why 499? Compares current price to 499 five-minute candles ago, about two days.

This parameter likely went through extensive backtesting. Too short (like 100) gets interfered with by short-term fluctuations; too long (like 1000) might miss early trend stages.

**Entry threshold: 1.10**

Why 10%? This threshold is high enough to filter most noise signals; but also low enough not to miss too many opportunities.

If set to 1.05 (5%), signals increase but so do false signals.
If set to 1.15 (15%), signals decrease but might miss many good opportunities.

**Stop loss: 1%**

Extremely strict. Most strategies set stops at 2-5%.

Why so strict?
1. Strategy bets "once I buy, it will rise"—if not rising, judgment was wrong
2. Strict stop ensures each loss is small
3. Believes when a trend comes, price won't pull back much

---

## Chapter 8: What Are the Risks?

**Risk 1: Ranging markets repeatedly stop out**

Biggest risk. In sideways markets, ROCR may repeatedly cross 1.10—you repeatedly buy and get stopped out. Each stop is only 1%, but accumulate over many rounds.

10 stops = 10%, 20 stops = 20%. Each loss is small but adds up.

**Risk 2: Slippage makes actual losses bigger**

Theoretically 1% stop = 1% loss. But in execution, price may skip right past your stop price—especially in big drops or illiquid coins. What you set as 1% loss might actually become 3-5%.

**Risk 3: Missing continued rise after stop-out**

Example: You buy, rises to $120, trailing stop at $110, then price retraces to $110 and stops out. But after you exit, price rises to $200! You only captured 10% and missed the subsequent 80%.

This is the price of trailing stop: **protects profits but might miss bigger profits.**

**Risk 4: Parameters might be overfitted**

499 is too specific—this might be optimized from historical data. If market characteristics change in the future, these parameters might stop working.

---

## Chapter 9: How to Use This Strategy Well?

**Suggestion 1: Choose right coins**

Not all coins suit this strategy. Choose:
- Good liquidity
- Has momentum characteristics
- You're familiar with

**Suggestion 2: Control position size**

1% stop loss only represents maximum loss per trade equals 1% of principal. But if you go all-in, even a few consecutive stops could significantly draw down your account.

Recommendation: Use only 10-20% of capital per trade. Even if stopped, impact on total funds is limited.

**Suggestion 3: Accept consecutive stops**

This is the hardest psychological hurdle. Momentum strategy inherently has low win rate—only 30-40% of trades might be winners.

If you make 10 trades and 6 get stopped out, remember this is normal! Don't doubt the strategy, change parameters, or quit just because of consecutive stops.

**Suggestion 4: Don't manually intervene**

Many people see price drop and can't bear to stop, manually cancel the stop. Or see price rise and want to hold longer, manually delay selling.

Don't do this! Once you enable the strategy, let it run. The point of the strategy is disciplined execution—manual intervention breaks that discipline.

**Suggestion 5: Proper capital management**

If you accept the "small losses, big wins" logic, you need sufficient capital to survive through consecutive losing periods.

Example: Account has $10,000, each stop is $100. If 20 consecutive stops = $2,000 loss, account left with $8,000. Can you hold on until the winning trade comes?

The key to capital management: survive the worst-case scenario so you live to see the good times.

---

## Chapter 10: Compared with Other Strategies

**vs. Moving average strategy**
- MA more smoothed, slower response but fewer false signals
- ROCR faster response, captures trends earlier but more false signals

**vs. breakout strategy**
- Breakout looks at absolute price, ROCR looks at relative change rate
- Breakout more suitable for long-term, ROCR more suitable for medium/short-term

**vs. mean reversion strategy**
- Mean reversion buys dips, JustROCR3 chases rises
- Mean reversion suitable for ranging markets, JustROCR3 suitable for trending markets

Some experts use multiple strategies: trending markets use momentum strategies, ranging markets use mean reversion.

---

## Chapter 11: Can This Strategy Be Improved?

**Idea 1: Add volume confirmation**

Currently only looks at price change rate—can add volume confirmation: only buy when ROCR > 1.10 AND volume expands. This filters "fake rises"—price up but no volume might be a false breakout.

**Idea 2: Adjust parameters based on market volatility**

1% stop loss too tight during high volatility; 1.10 threshold too low during low volatility.

Can introduce a volatility indicator (like ATR)—widen stop and raise threshold when volatility high; do opposite when low.

**Idea 3: Add exit conditions**

Currently entirely relies on stop loss—sometimes price rises a lot then falls back, only capturing small profit.

Can add an active exit condition: when ROCR drops below 1.05, proactively sell instead of waiting for trailing stop.

**Idea 4: Multi-timeframe confirmation**

Currently only looks at 5-minute chart—can simultaneously check trend direction on 15-minute or 1-hour charts. Only buy when multiple timeframes align—this reduces false signals.

---

## Chapter 12: Suggestions for Beginners

**First: Don't use real money initially**

Run paper trading for a while first. See how the strategy performs on your coins. Get used to its trading frequency, stop frequency, profit cycles.

**Second: Don't change parameters**

The most common beginner mistake: seeing the strategy lose money and immediately changing parameters. 499 to 300, 1.10 to 1.08, stop from 1% to 2%...

Please don't! Parameters were optimized—changing them only makes things worse. Use default parameters for a while, understand the strategy's characteristics, then consider minor adjustments.

**Third: Keep a trade journal**

Record every trade: when bought, what price, what was ROCR, how high it went, when sold, profit or loss.

This tells you:
- Strategy's win rate on your coins
- Average profit and average loss
- What situations trigger stops, what situations generate big wins

**Fourth: Accept strategy's limitations**

No perfect strategy. JustROCR3 performs well in trending markets, poorly in ranging markets. A tool has scenarios it's suited for.

Do understand this tool's characteristics, use it in appropriate scenarios, rather than expecting it to perform well in all conditions.

---

## Chapter 13: Final Summary

JustROCR3 is a simple but effective momentum-tracking strategy. Its core principles:

1. **Use ROCR to find trends**: Price up more than 10% from two days ago means a trend exists
2. **Strict stop loss保命 (protects life)**: If doesn't rise after buying, 1% immediately admits defeat
3. **Trailing stop保利润 (protects profits)**: When rising, stop follows upward, locking in profits
4. **Let profits奔跑 (run)**: Don't proactively take profit, let market decide when to exit

This strategy suits those:
- Who believe in momentum trading
- Who can accept frequent small stops
- Who don't want to spend time watching charts
- Who have sufficient capital to survive through drawdowns

But it also has limitations:
- Consecutive stops in ranging markets
- Parameters might be overfitted
- Might miss some opportunities
- Requires disciplined execution

Finally: strategy is just a tool. Whether it makes money depends on how you use it. Understanding the strategy's logic, knowing its pros and cons, using it in appropriate markets, maintaining discipline—these matter more than the strategy itself.

Happy trading!

---

*Disclaimer: This document is for education and reference only, not investment advice. Cryptocurrency trading has high risks; please make careful decisions based on your own situation, and don't invest more than you can afford to lose.*
