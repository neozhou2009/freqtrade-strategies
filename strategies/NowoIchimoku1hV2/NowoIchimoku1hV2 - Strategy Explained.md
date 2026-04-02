# NowoIchimoku1hV2: What's This Strategy Doing?

## Chapter 1: What Is This Strategy?

NowoIchimoku1hV2 is a cryptocurrency trading strategy with a simple core idea: **find uptrends, ride them, take profits, and get out.**

Breaking down the name:
- **Nowo** = New version
- **Ichimoku** = Ichimoku Cloud, a Japanese trend-reading tool
- **1h** = Uses 1-hour candlesticks
- **V2** = Second generation

This strategy **only goes long, never short** — it only buys when predicting prices will rise, never sells short when predicting a drop. Why? Because crypto tends to go up more than down over time, and riding the rise is more reliable than guessing the fall.

## Chapter 2: What Is the Ichimoku Cloud?

The Ichimoku Cloud sounds fancy but is essentially a "trend map." It draws what looks like a cloud — green clouds mean uptrends, red clouds mean downtrends, and inside the cloud means sideways.

Five components:

**1. Conversion Line (Blue Line)**
Adds the highest and lowest prices of the last 9 candles and divides by 2. Very responsive — changes quickly with price. Think of it as the "short-term weather vane."

**2. Base Line (Red Line)**
Adds the highest and lowest prices of the last 26 candles and divides by 2. Slower — represents the medium-term direction. Think "medium-term steering wheel."

**3. Leading Span A**
Averages the Conversion and Base Lines, then pushes 30 candles into the future. Sounds magical? It literally plots into the future!

**4. Leading Span B**
Adds the highest and lowest prices of the last 52 candles, divides by 2, then pushes 26 candles into the future.

**5. The Cloud**
The area between Leading Span A and Leading Span B is the cloud. If A is above B, the cloud is green (uptrend); if B is above A, the cloud is red (downtrend).

What is the cloud for? **The cloud is like a wall.** Price above the cloud = bulls have the power. Price below the cloud = bears have the power.

## Chapter 3: Another Helper — Bollinger Bands

In addition to the cloud, this strategy also uses Bollinger Bands. What are those?

Imagine a moving average (say, 20-hour average price), then draw a line above it (average + 2.5× standard deviation) and a line below it (average - 2.5× standard deviation). The three lines form a channel — that's Bollinger Bands.

Bollinger Bands have a special property: **price spends most of its time inside the band.** When it runs outside the band, it often means "this is overdone" — a pullback may follow.

This strategy only uses the upper Bollinger Band (the top line) to judge whether price has risen too aggressively. When it breaks above the upper band, consider selling.

Specifically, this strategy uses the **Hull Moving Average** for Bollinger Bands' middle line. HMA is faster and smoother than regular MAs — no half-second delays.

## Chapter 4: When Does It Buy?

The strategy's buy conditions are extremely strict — all seven conditions must be met simultaneously. Like clearing seven checkpoints, one missing means no buy.

### Checkpoint 1: Must Be a Bullish Candle

Closing price must be above opening price — buyers won this hour.

### Checkpoint 2: Price Must Stand Above the Cloud

Current price must be above the "forward-shifted cloud upper boundary" by a certain ratio (default 0.603).

Why shift forward? Because the cloud is literally drawn into the future. To compare current price to the cloud, you have to "pull the cloud back" to align it.

### Checkpoint 3: Price Must Also Be Above the Cloud Lower Boundary

Not just clearing the cloud upper — must also clear the cloud lower, ensuring price is completely above the cloud.

### Checkpoint 4: Cloud Must Be Green

The cloud's color must be green (uptrend), not red (downtrend). If the cloud is red, the macro environment is bad — don't buy.

### Checkpoint 5: Conversion Line Must Be Above Base Line

Short-term weather vane above the medium-term steering wheel — short-term momentum is charging upward.

### Checkpoint 6: Price Must Be Above the 25-Hour-Ago Conversion Line

Not just the current Conversion Line must be high — must also be higher than the historical Conversion Line. This confirms the trend isn't a fleeting spike.

### Checkpoint 7: Price Must Be Above the 50-Hour-Ago Cloud Upper

Look even further back — price must break through deeper resistance from even earlier.

**All seven conditions met = BUY signal issued.** That's extremely strict! The purpose: **better to miss an opportunity than to make a mistake.**

## Chapter 5: A Smart "Brake" System

This strategy has a clever design: **after buying once, you must wait for the cloud to turn red then green before buying again.**

Imagine:
1. Cloud is green → can buy
2. Bought → can't buy a second time for now
3. Cloud turns red → reset, ready to buy again
4. Cloud turns green again → can buy again

What's the benefit?
- **Avoids repeatedly adding to positions in the same trend**: If it keeps rising, you'd want to keep buying, but you might end up buying at the top.
- **Forces waiting for trend confirmation**: Only when the market goes through a "pullback-restart" process is buying safer.

This is like waiting for a green light at an intersection: the light turns green, you can go, but after going once you wait for the next cycle — no running through multiple lights in a row.

## Chapter 6: When Does It Sell?

Buying is hard; selling is even harder. This strategy has four exit scenarios:

### Scenario 1: Overbought StochRSI

StochRSI is an indicator that judges "overboughtness." When its value exceeds 80, it means the short-term rise has been too aggressive and may need a rest.

When StochRSI exceeds 80 AND you've already made at least 3.6% profit (default), the strategy says ""that's enough, take the money and run" and sets a very tight stop — sell at the slightest pullback.

### Scenario 2: Breakout Then Pullback

When price breaks through the Bollinger upper band, it means it ran up hard. But usually after breaking out, there are pullbacks. The strategy seizes this opportunity: when it first breaks out, immediately set a very tight stop — sell if there's any pullback at all.

The benefit: **chase the momentum but don't be greedy — when you sense weakness, run.**

### Scenario 3: Reached the Preset Target

This strategy has an interesting target calculation:

1. Record your entry price (e.g., $100)
2. Find the cloud lower at entry time (e.g., $90)
3. Calculate the distance: $100 - $90 = $10
4. Multiply that distance by 1.918×: $10 × 1.918 = $19.18
5. Target price = $100 + $19.18 = $119.18

Meaning: **the farther the cloud lower is from your entry, the higher you set your target; the closer it is, the lower your target.**

Why? A distant cloud lower means high volatility and strong trends — you can wait longer. A close cloud lower means low volatility and weak trends — take profits early.

### Scenario 4: Cloud Lower Broken

The cloud lower is like a support line. If price breaks below your entry's cloud lower (with a 97.1% discount), the cloud support has failed — trend may be reversing, get out.

The discount exists because sometimes price "fake breaks" — pokes through then bounces back. A 97% buffer avoids getting shaken out by false breakouts.

### The Final Floor

If none of the above four scenarios trigger, there's a floor stop: **-34.5% unconditional exit.** This is the last safety rope — prevents unlimited losses.

## Chapter 7: There's Also a Time Factor

The strategy has "time-decaying profit target" settings:

| Holding Time | Minimum Profit Required |
|-------------|------------------------|
| Just bought | 42.7% |
| After 448 hours | 20.2% |
| After 1,123 hours | 8.9% |
| After 2,355 hours | 0% |

What does this mean?

- Right after buying, the target is a hearty 42.7%.
- Holding over 448 hours (~19 days), target drops to 20.2%.
- Holding over 1,123 hours (~47 days), target drops to 8.9%.
- Holding over 2,355 hours (~98 days), any profit is fine — just don't lose money.

Why? **Time is an opportunity cost.** If you've been holding for nearly 100 days and haven't made much, maybe this opportunity itself isn't great — get out and find the next one.

## Chapter 8: Can These Parameters Be Adjusted?

Yes! The strategy offers five tunable parameters:

### Entry Parameter
**close_above_shifted_upper_cloud** (default 0.603)
- Controls how much higher than the cloud upper price must be to buy
- Higher value = stricter conditions = fewer buy signals but possibly more accurate

### Exit Parameters
**srsi_k_min_profit** (default 3.6%)
- When StochRSI is overbought, minimum profit required to take profits
- Higher value = can wait longer, potentially more profit but more drawdown risk

**above_upper_min_profit** (default 1.1%)
- When breaking the Bollinger upper, minimum profit required to take profits
- Lower value = easier to trigger

**limit_factor** (default 1.918)
- Dynamic profit target multiplier
- Higher value = higher target = possibly longer holding

**lower_cloud_factor** (default 0.971)
- Cloud lower stop-loss discount
- Lower value = tighter stop, but may get shaken out by false breakouts

These parameters can be optimized through historical data backtesting to find the best combination for the current market.

## Chapter 9: What Are the Advantages?

### Advantage 1: Steady and Reliable
Seven conditions all verify together — hard to buy on a false breakout. Better to miss than to be wrong.

### Advantage 2: Has Its Own Brake
After buying, must wait for cloud red then green before buying again — won't impulsively add positions.

### Advantage 3: Smart Selling
Four exit conditions cover all scenarios — overbought, pullback after breakout, target reached, support broken — all have corresponding handling.

### Advantage 4: Self-Adapting
Targets aren't fixed but dynamically adjust based on market state at entry. Big volatility = big appetite; small volatility = small appetite.

### Advantage 5: Time-Conscious
The longer you hold, the lower the profit requirement — won't stubbornly hold a losing position forever.

## Chapter 10: What Are the Disadvantages?

### Disadvantage 1: Long Only
Can only make money when rising — must sit idle during bear markets. May have no trading opportunities for extended periods.

### Disadvantage 2: Slow to React
The Ichimoku's Base Line uses 26 candles, Leading Span B uses 52 candles. On the hourly chart, that's 26 and 52 hours. Price may not keep up with fast reversals.

### Disadvantage 3: May Be Misled by Parameters
Five tunable parameters give lots of optimization room, but also easy to "over-fit" — parameters perfectly matching historical data but useless for the future.

### Disadvantage 4: Can't Handle Extreme Markets
Though there's a -34.5% stop, in a flash crash the stop price may not even fill.

## Chapter 11: A Complete Trade Example

### Scenario
Let's say you're looking at Bitcoin at $60,000 one day.

### Step 1: Observe the Market
- The Ichimoku cloud is green — macro trend is bullish.
- Conversion Line is above Base Line — short-term momentum is upward.
- Price is standing above the cloud.

### Step 2: Wait for Signal
- This hour closed — it's a bullish candle (close > open).
- Check all seven conditions — ALL MET!
- Strategy issues buy signal. You buy at $60,500.

### Step 3: Set Protections
- Cloud lower at entry: $58,000.
- Dynamic profit target: $60,500 + ($60,500 - $58,000) × 1.918 = $65,294.
- Cloud lower stop: $58,000 × 0.971 = $56,318.

### Step 4: During Holding
- Price slowly rises to $63,000, then pulls back to $61,500.
- No stop-loss triggered — keep holding.
- Cloud is still green, trend hasn't changed.

### Step 5: Exit

**Ending A (Ideal)**:
- Price continues rising, StochRSI exceeds 80.
- You've already made 8%, exceeding the 3.6% threshold.
- Strategy sets a tight stop — sell on the slightest pullback.
- Finally sell at $65,000, making ~7.4%.

**Ending B (Normal)**:
- Price rises to $64,000 then starts pulling back.
- It broke through the Bollinger upper, you've made 5%.
- Strategy triggers tight stop, sells during the pullback.
- Finally sell at $62,500, making ~3.3%.

This is a typical trade — might make more or less, but the key is **controlling risk, not letting small losses become big ones.**

## Chapter 12: Who Is This For?

### Good Fit
- **Believers in long-term crypto bullishness**: Strategy only goes long, suits bullish outlooks.
- **Comfortable with medium-to-long holding**: Trades may last weeks to months.
- **Want systematic trading**: All rules in code, no relying on gut feelings.
- **Patient for signals**: May see only one signal every few days or even weeks.
- **Seek steady returns**: Not seeking to get rich overnight, want long-term stable profits.
- **Can stomach some drawdown**: Strategy stop is 34.5% — need mental preparation.
- **Have basic coding knowledge**: Can read strategy logic, easy to optimize and adjust.

### Not Good Fit
- **Quick in-and-out traders**: This is medium-to-long-term, not for day trading.
- **Short sellers**: Strategy has no short logic.
- **Impatient for signals**: May wait weeks for a signal — need patience.
- **Can't handle 30%+ drawdowns**: Max possible loss is 34.5%.
- **Get-rich-quick seekers**: Strategy pursues stability, not aggression.
- **Complete beginners at technical analysis**: While the strategy runs automatically, understanding the logic is important.
- **Tiny capital**: With only a few hundred dollars, fees eat all the profits.

## Chapter 13: How to Get the Best Results?

### Tip 1: Pick the Right Pairs
Best for volatility-regular coins: BTC, ETH. Small-cap coins may be too volatile or illiquid.
**Recommended**: BTC, ETH, BNB
**Not recommended**: Tiny market cap altcoins, newly launched coins (no history), irregular volatility coins

### Tip 2: Control Position Size
Don't bet everything on one trade. Recommended:
- Single trade ≤ 2%-5% of total capital
- Concurrent positions ≤ 20% of total capital
- Always keep some cash for emergencies

For a $100,000 account:
- Max per trade: $2,000-$5,000
- Max concurrent positions: $20,000
- Keep $80,000 in reserve

### Tip 3: Diversify
Run this strategy on several different coins simultaneously, don't put all eggs in one basket.

### Tip 4: Watch Major News
For major events (Fed meetings, regulatory announcements, exchange hacks, hard forks), consider pausing the strategy or manual intervention.

### Tip 5: Regular Check-Ins
Check trading records weekly, do monthly summaries, evaluate if parameters need adjusting quarterly.

**When to adjust?**
- More than 5 consecutive losses
- Win rate significantly dropped
- Signal frequency abnormal
- Maximum drawdown exceeding expectations

### Tip 6: Keep a Trading Journal
Record entry time and price, buy condition triggers, market changes during holding, exit reason and P&L, and your reflections. Long-term records reveal patterns.

### Tip 7: Paper Trade First
If you're new, paper trade for a while before using real money. At least 1-2 months, experience a complete market cycle (up and down), confirm you can handle the strategy's drawdown.

## Chapter 14: Q&A

**Q: Why long only, no shorting?**
A: Strategy design is to capture uptrends. Ichimoku is more effective at judging uptrends, and crypto markets have more upside opportunities long-term. To short, you'd need a separate short strategy.

**Q: What if signals are too few?**
A: Seven conditions are very strict — few signals is normal, and "few" isn't bad:
- Few signals = high quality
- Better to miss than to be wrong
- Consider running the strategy on multiple pairs simultaneously

If truly too few (none in a month):
- Lower the `close_above_shifted_upper_cloud` parameter
- Switch to a more volatile pair
- Check if the market is in a ranging period

**Q: Maximum loss?**
A: Theoretically up to 34.5% (fixed stop). In reality, flash crashes, exchange failures, or liquidity crunches could cause losses beyond that — keep a safety margin.

**Q: How long is normal holding?**
A: From the time-decay ROI settings:
- Ideal: days to weeks
- Normal: weeks to months
- Maximum: ~100 days (2,355 hours)

If holding over 2 months with no profit, something may be wrong.

**Q: Can combine with other strategies?**
A: Yes, and recommended. E.g.:
- This strategy for longs, another for shorts
- This strategy for trends, a ranging strategy for sideways markets
- Different pairs with different strategies

Key: control total position, don't exceed risk tolerance.

**Q: Need to frequently adjust parameters?**
A: Not recommended. Reasons:
- Easy to over-fit historical data
- Each adjustment needs re-validation
- Stable parameters are more reliable

Recommendation: check quarterly if parameters are still suitable; only adjust if long-term performance is clearly deteriorating.

**Q: Backtest looks great but live doesn't work?**
A: Very common. Possible reasons:
- Backtest data not comprehensive enough
- Over-fit to historical data
- Market environment changed
- Live has slippage and fees

Solutions:
- Use longer historical data for backtesting
- Validate across multiple time periods
- Test with paper trading first
- Check slippage and fee settings

## Chapter 15: Summary

NowoIchimoku1hV2 is a **steady trend-following strategy** — uses Ichimoku Cloud for trend direction, Bollinger Bands for overbought assistance, strict entry conditions, and smart exit mechanisms.

Key characteristics:
- **Seven checkpoints**: All seven conditions met before buying — high signal quality
- **Red-green cycle**: After buying once, must wait for cloud red then green before buying again — avoids chasing
- **Four-layer safety net**: Four exit conditions protect profits — risk is controllable
- **Dynamic targets**: Auto-adjust expectations based on market volatility — more flexible
- **Time decay**: Longer holding = lower requirements — won't stubbornly hold losers

This strategy doesn't trade frequently — it pursues catching big trends and profiting from them. If you believe crypto will go up long-term and don't want to watch charts all day, this strategy may suit you.

But remember: **even the best strategies lose money sometimes. Only trade with money you can afford to lose.**

### Three Final Reminders

1. **Understand before using**: Don't blindly run a strategy — fully understand its logic first.
2. **Start small**: When first using it, start with minimum position size.
3. **Keep learning**: Markets change, strategies must evolve too.

Happy trading!
