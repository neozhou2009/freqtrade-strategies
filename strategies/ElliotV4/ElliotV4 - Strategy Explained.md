# ElliotV4: What's This Strategy?

## 1. What Does This Thing Do?

ElliotV4 is a strategy that helps you automatically buy and sell cryptocurrency. Its core idea is simple: **buy when the price is on sale, sell when it's risen enough to make money**. You don't have to stare at charts all day — the strategy judges when to buy and when to sell automatically.

This strategy uses something called the "Elliott Wave theory." This theory was developed by a guy named Elliott in the 1930s. After decades of market observation, it's still widely used today. The theory says market prices don't move randomly — they move in waves, like ocean tides. Sometimes big waves push prices in one direction (main trends), and sometimes smaller waves move in the opposite direction (corrections). This strategy tries to catch the rhythm of these waves, getting on during small pullback waves within big upward waves, then riding them to profit. You don't need to count which wave you're on — the strategy uses the EWO indicator to judge this automatically. This indicator quantifies wave theory, much more reliable than manually counting waves.

## 2. What's EWO?

EWO stands for Elliott Wave Oscillator, the soul of this strategy and where the "Elliot" in the name comes from.

Imagine using a short string (50-period moving average) and a long string (200-period moving average) to measure price movement. The short string reacts quickly, the long string reacts slowly. When prices are climbing hard, the short string shoots way above the long one; when prices are crashing, the short string drops way below. EWO turns the distance between these two strings into a number, so you can instantly tell if prices are "overextended" or "way too beaten down."

**How is it calculated?**
```
EWO = (Short Moving Average - Long Moving Average) ÷ Current Price × 100
```

For example:
- Current price: $100
- Short moving average (50-period): $105
- Long moving average (200-period): $95
- EWO = (105 - 95) ÷ 100 × 100 = 10

That 10 tells you recent gains are outpacing the long-term average — market sentiment is pretty bullish.

**How to read the numbers?**

| EWO Value | Market State | What It Means |
|-----------|-------------|--------------|
| Positive (e.g., 5) | Recent gains exceed average | Possibly in an uptrend |
| Negative (e.g., -5) | Recent losses exceed average | Possibly in a downtrend |
| Very large positive (> 2.34) | Climbing very hard | Might pull back, or might keep going |
| Very small negative (< -17.457) | Crashed very hard | Oversold, might bounce |

The strategy uses these two extremes as buy signals — when climbing hard, wait for a pullback to buy; when crashed very hard, bottom-catch.

**Why not use MACD instead?**

MACD also compares two moving averages, but it has a problem — different priced assets give wildly different MACD values. Bitcoin costs tens of thousands, Ethereum a few thousand. The same percentage move might produce MACD values that differ by 10x. EWO solves this by dividing by current price, standardizing the difference. Whether it's Bitcoin or Ethereum, EWO values are directly comparable, making it easier to set universal thresholds.

## 3. How Does the Strategy Decide to Buy?

The strategy has two completely different buy approaches — like having two different shopping strategies.

### Buy Approach 1: Snagging a Discount

**Scenario**: Something's been climbing steadily, then suddenly goes on sale!

Picture this: you've had your eye on those sneakers at $100, and they've been climbing for a while. Suddenly they drop to $98 on a small sale. And it's been popular (high EWO means it's been doing well), but the heat's died down a bit (RSI isn't super high). Why not buy?

**Specific conditions:**
1. Price below moving average × 0.983 (roughly a 1.7% "discount")
2. EWO greater than 2.34 (it's been climbing strong, trend is intact)
3. RSI below 61 (hasn't overheated, still room to climb)
4. Some selling happening (volume > 0, always satisfied)

Why the RSI condition? Because if RSI is already sky-high (like 80), even though there's a pullback, it might drop further. So the strategy requires RSI below 61 to exclude overheated situations.

### Buy Approach 2: Bottom-Catching

**Scenario**: Something crashed hard — like, way too hard.

Picture a stock that went from $100 to $50 to $30. Everyone's panicking. Some brave souls start buying because "it bounced hard enough, it has to rebound, right?"

**Specific conditions:**
1. Price below moving average × 0.983 (also on sale)
2. EWO below -17.457 (it's crashed very hard, market is in extreme panic)
3. Some selling happening

Why doesn't this look at RSI? Because bottom-catching is fundamentally betting on a bounce. RSI is probably already down to 20 or 10 at this point. Adding an RSI condition would be pointless and would filter out valid opportunities. Bottom-catching is high risk, high reward — doesn't need extra rules.

### Why Two Buy Approaches?

Because the market gives two kinds of opportunities:
1. **Normal opportunity**: Surged for a bit, took a breather, keeps going. Wait for pullback to buy.
2. **Extreme opportunity**: Something bad happened, panic selling. Can catch a rebound from the panic.

### Comparison of the Two

| | Approach 1 (Discount) | Approach 2 (Bottom-Catch) |
|---|---------------------|------------------------|
| How often | Pretty common | Rare (only in crashes) |
| Market state | Normal volatility | Market crash |
| Risk level | Medium | High |
| Potential return | Trend continues, steady gains | Technical rebound, potentially big |
| Needs confirmation? | RSI required | No RSI needed |
| Suited for | Steady types | Aggressive types |

## 4. How Does the Strategy Decide to Sell?

The sell logic is simpler. The strategy has just one rule: **wait for the price to climb above the moving average, then sell.**

**Specific conditions:**
- Price above moving average × 0.992
- Volume > 0

Wait, 0.992? That's not above 1.0 — isn't that below the average?

Because the strategy uses EMA (Exponential Moving Average), price can shoot up quickly then pull back. If you wait until price is strictly above the moving average, you might miss the best sell point. So the strategy uses 0.992 — meaning it starts considering exits as price gets close to the average, getting out slightly ahead.

**But there's more to exits!**

The strategy actually doesn't rely on this sell signal much, because it has better tools — ROI and Trailing Stop.

Set with: `use_sell_signal = False`

Meaning: by default, don't use technical signals to sell. Let ROI and trailing stop manage exits.

## 5. What Does ROI Mean?

ROI means "Return on Investment target." This strategy sets several profit milestones:

| Time | Profit Target | What It Means |
|------|-------------|--------------|
| Just bought | 21.5% | Aiming big from the start |
| After 40 min | 3.2% | Getting impatient, lower target OK |
| After 87 min | 1.6% | Really impatient now |
| After 201 min | 0% | Just don't lose money, get me out |

**What does this look like in practice?**

Think of it like selling secondhand stuff:
1. **Just listed**: Want 21.5% profit, waiting for the big buyer
2. **40 minutes in**: No such luck. Fine, 3.2% profit is OK
3. **87 minutes in**: Still nothing? 1.6% will do
4. **201 minutes in**: Come on, just break even and I'm out

This design is humane: wants high returns at first, but won't wait forever. The longer it waits, the more willing to compromise on profit.

**Why design it this way?**

Markets change. Right after buying, conditions might be great and there's hope for big gains. But if you've waited a long time with no upward movement, the market might have shifted — better to close the position and find the next opportunity.

This is the concept of "time cost" — money locked in a non-profitable position is money not chasing opportunities elsewhere.

## 6. What's a Trailing Stop?

### Imagine You're Climbing a Mountain

You're climbing up, and each time you reach a new high point, you plant a flag. If you later fall back past a flag, you retreat immediately.

Trailing stop works the same way:

1. **Condition met first**: Profit hits 4.9% before it starts tracking
2. **Track the peak**: Remember the highest profit
3. **Retreat condition**: If profit drops back to just 1%, sell

### An Example

You buy at $100:
- Climbs to $101, profit 1% — not tracking (hasn't hit 4.9% yet)
- Climbs to $104, profit 4% — not tracking (still not 4.9%)
- Climbs to $105, profit 5% — starts tracking! Remember the high is 5%
- Climbs to $110, profit 10% — update the high to 10%
- Drops to $108, profit 8% — fine, still above 1%
- Drops to $105, profit 5% — fine, still above 1%
- Drops to $101, profit 1% — hit the line! Sell!

### Why This Design?

If you set a tight stop from the start — say, exit if profit drops to just 1% — you might get shaken out after making 5% when there's a minor pullback. Giving it a 4.9% "runway" lets profits run before protecting them.

It's like raising a child: when they're young, give them freedom to explore. When they've grown and proven themselves capable, set some rules.

### Trailing Stop Parameters

```python
trailing_stop = True                        # Turn on trailing stop
trailing_stop_positive = 0.01               # Stop line: 1% below peak
trailing_stop_positive_offset = 0.049       # Activation: 4.9% profit
trailing_only_offset_is_reached = True     # Must hit 4.9% before tracking
```

In short:
- Profit < 4.9%: Let it fluctuate freely
- Profit >= 4.9%: Start tracking; if it pulls back to just 1%, sell

## 7. Stop-Loss: The Last Line of Defense

### Fixed Stop-Loss: 10%

No matter what the fancy stuff above does, here's the bottom line: **if you lose more than 10%, you're done, get out.**

This is the hard floor protecting your capital. Sometimes markets mysteriously tank with no warning. With this rule, you avoid catastrophic losses.

### Why 10%?

It's a balance:
- **Too tight (like 3%)**: Normal fluctuations will knock you out, you'll get whipsawed constantly
- **Too loose (like 20%)**: If things really crash, you lose a lot
- **10%**: Just right for 5-minute-level trading — gives price enough room to breathe

### Multiple Lines of Defense

This strategy's risk control is like an onion — layer after layer:

| Layer | Mechanism | When It Triggers | What It Does |
|-------|-----------|----------------|--------------|
| Outer | Technical indicators | Price breaks moving average | Trend broke, exit |
| 2nd | ROI targets | Time's up, profit target hit | Don't want to wait, lock profits |
| 3rd | Trailing stop | Profit pulls back to 1% | Protect gains you've made |
| Inner | Fixed stop-loss 10% | Down 10% | Never lose more than this |

So many layers — at least one will work. Like home security: first the yard gate, then the front door, then the bedroom door, and finally the safe.

## 8. What's a Moving Average? Why Does It Matter?

### Moving Average = "Average Line"

Simple concept: take the last N prices, add them up, divide by N, and draw a line. That's a moving average.

For example, a 5-day moving average adds up the last 5 days of closing prices and divides by 5. Calculate it each day and connect the dots — that's your line.

### This Strategy Uses EMA

EMA (Exponential Moving Average) gives recent prices more weight — it's more responsive to current trends.

For example:
- SMA (simple average): Last 10 days, each day is 10% weight
- EMA (exponential average): Today's might be 20%, yesterday 15%, 10 days ago just 5%

EMA responds faster, better for short-term trading.

### The Moving Averages in This Strategy

- **Buy moving average**: Default 14-period, judges buy timing
- **Sell moving average**: Default 24-period, judges sell timing

Why is the sell moving average longer? Because you don't want to panic when selling. A longer-period average is more stable, won't get fooled by small fluctuations.

### Can You Change It?

Yes! This strategy is specifically designed to be tunable:
- Buy MA period: Changeable between 5 and 80
- Sell MA period: Changeable between 5 and 80

How do you know what to change it to? Test it with historical data (backtesting) and see which number works best.

## 9. What's RSI?

### RSI = Relative Strength Index

It measures whether recent gains or losses are bigger:
- **Above 70**: Gaining too fast, might drop (overbought)
- **Below 30**: Losing too fast, might bounce (oversold)
- **Around 50**: Balanced, no clear direction

### How Is It Calculated?

The formula is complicated, but here's the plain version:
1. Add up all gains from the last 14 days
2. Add up all losses from the last 14 days
3. Calculate what percentage of total movement was gains
4. Map to a 0-100 scale

More gains = high RSI; more losses = low RSI.

### How Does This Strategy Use It?

This strategy requires RSI below 61 when buying — meaning "don't buy when it's super hot."

61 is more loose than the traditional 70. Why? Because this strategy is a "pullback buyer" — waiting for price to pull back from a high before buying. If you wait until RSI is below 30 (traditional oversold), you've probably already missed the drop and bought way too late.

61 is a middle-ground: not chasing the highs, but not waiting until everything's on fire either.

## 10. Can You Change the Parameters?

### Yes, and There Are Quite a Few

This strategy has many tunable parameters, letting you adjust for different market conditions.

#### Buy-Related

| Parameter | Range | Default | What It Does |
|----------|-------|---------|-------------|
| MA period | 5-80 | 14 | How many candles for the MA |
| Discount rate | 0.9-0.99 | 0.983 | How big a "discount" to buy |
| EWO high threshold | 2.0-12.0 | 2.34 | How high EWO must be for good entry |
| EWO low threshold | -20 to -8 | -17.457 | How low EWO must be for bottom entry |
| RSI upper limit | 30-70 | 61 | How high RSI can be and still buy |

#### Sell-Related

| Parameter | Range | Default | What It Does |
|----------|-------|---------|-------------|
| Sell MA period | 5-80 | 24 | How many candles for sell MA |
| Premium rate | 0.99-1.1 | 0.992 | How far above MA to sell |

### How Do You Tweak Them?

Through backtesting. Use historical data to try different parameter values and pick the ones that performed best.

But be careful — don't overfit. What does that mean? If you tune parameters so they perfectly fit historical data, they might not work on future data.

Think of it like tailoring clothes: make them too perfectly fitted to your current body, and if you gain or lose weight, they won't fit anymore. Same with parameters — tune them too tightly to current market conditions, and when the market changes, they won't work.

### Different Markets, Different Settings

**Trending markets (steady up or down)**:
- EWO high threshold can be lower (like 2-3), easier to trigger
- RSI upper limit can be higher (like 65), don't miss opportunities
- MA period can be shorter, responds faster

**Choppy markets (wobbling around)**:
- EWO high threshold should be higher (like 4-6), reduce false signals
- RSI upper limit should be lower (like 50-55), wait for better entry points
- MA period can be longer, filters noise

**High-volatility markets (big swings)**:
- Stop-loss can be wider
- Trailing stop activation can be higher
- EWO low threshold can be even lower

## 11. What Timeframe Does It Use?

### 5-Minute Level

This strategy uses 5-minute candlestick charts. Each candle records the open, high, low, and close prices for a 5-minute period.

**5-minute level pros:**
- Lots of signals: many trading opportunities in a day
- Fast response: can quickly react to market changes
- Short-term: no need to hold positions for days

**5-minute level cons:**
- More noise: more false signals
- Higher demands: needs stable execution system
- Higher costs: frequent trading means more fees

### There's Also 1-Hour Auxiliary

The strategy also references 1-hour-level data to see the bigger picture.

Like looking at a map:
- 5-minute is zooming in, seeing every detail
- 1-hour is zooming out, seeing the big direction

You need both for a complete picture.

### What Does startup_candle_count = 39 Mean?

When starting up, the strategy needs 39 candles of historical data to start calculating indicators. Some indicators (like EMA) need historical data to calculate accurately.

39 5-minute candles = 195 minutes = 3 hours 15 minutes. So the strategy needs about 3+ hours of data before it's ready.

## 12. What to Watch Out For?

### Strengths

**1. Logic is simple**
Just a few indicators: EWO, moving average, RSI. Each has a clear meaning — unlike those "black box" strategies where you have no idea what they're doing.

**2. Risk is controllable**
Stop-loss, trailing stop, ROI — several lines of defense. Even if your judgment is wrong, you won't lose too much.

**3. Lots of opportunities**
Two buy modes — one waits for pullbacks, one bottom-catches — there's opportunity in most market conditions.

**4. Can be optimized**
Parameters can be tuned, adapts to different coins and market conditions.

### Weaknesses

**1. Too many parameters**
Many tunable parameters, but that also means easy to tune wrong. Too aggressive tuning gives great historical results but poor future results.

**2. Choppy markets are rough**
When price chops around without direction, you get constantly whipsawed — buy and it drops, sell and it climbs, consecutive stop-losses.

**3. Bottom-catching is risky**
Approach 2 bets on extreme reversals. Can catch a falling knife. Keeps dropping after you buy, catches you at mid-mountain.

**4. 5-minute is too short**
Demands fast internet and system stability. A few seconds delay in ordering and the price changes.

### Real-World Advice

**Backtest first**
Don't go live right away. Test on historical data to see how the strategy performed in the past. If it lost money historically, don't expect it to make money in the future.

**Start with small money**
Start with fake money or small stakes first. Don't go all-in immediately. Once it's consistently profitable, gradually increase.

**Watch it closely early on**
At the beginning, watch how it trades closely. Understand its logic, so when something goes wrong you know where to look.

**Don't tweak parameters constantly**
Don't tweak every day, but don't never tweak either. Generally review once a quarter or twice a year to see if parameters need updating.

## 13. Summary — One Line to Remember It

**ElliotV4 is a "wait for a discount to buy, take profits when you've made enough" strategy — uses EWO to find buy points, moving averages and trailing stops to find sell points, and multi-layer risk controls to protect your money.**

### Good For:

- **People who don't want to chase**: Like waiting for pullbacks, don't like buying at highs
- **Bottom-catchers**: Brave enough to buy when everyone's panicking
- **Patient people**: Willing to wait for opportunities, not jumping at everything
- **People willing to optimize**: Understand that one set of parameters won't work forever

### Not Good For:

- **Get-rich-quick folks**: No such strategy exists. Come on.
- **People who can't handle volatility**: Every strategy has losing periods
- **People who don't want to do homework**: Every strategy needs testing and monitoring
- **Slow internet folks**: 5-minute level needs fast execution

### Final Thoughts

There's no holy grail in quantitative trading. ElliotV4 is a good strategy, but it's not a money printer.

Before using:
- Backtest! Backtest! Backtest!
- Start with fake money!
- Understand the logic!

After using:
- Monitor performance!
- Adjust timely!
- Control risk!

Remember this: **The strategy is a tool; the person is what makes money.** Even the best strategy will lose money in the wrong hands; even the worst strategy can make money with the right approach. The key is understanding it, adapting to it, and controlling it.

---

**Disclaimer**: This article explains strategy principles. It's not telling you to buy anything. Quantitative trading has risks — invest cautiously. Historical performance doesn't guarantee future results. Don't gamble with your living expenses.
