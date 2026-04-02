# JustROCR5 Strategy Explained — The "Tiger Slot" Momentum Catcher

## Chapter 1: What Does This Strategy Do?

Imagine standing in front of a slot machine that just paid out big—wouldn't you want to give it another spin?

JustROCR5 does exactly this in crypto: it looks for coins that are "in a hot streak"—when prices start surging, it buys right away, takes profit, and runs.

Specifically, on a 1-minute chart, when a coin has risen >10% in the past 5 minutes AND is still rising in the last 2 minutes, it buys immediately. Sell at 5% profit, cut losses at 1%.

Simple, right? Just 30 lines of code. The whole logic: **chase momentum, but with strict stops**.

This strategy is perfect for crypto. Why? Because crypto volatility is wild—sometimes prices surge 10%+ in minutes. JustROCR5 is built to catch exactly these short-term explosive moves.

---

## Chapter 2: What Is ROCR?

ROCR = Rate of Change Ratio. Calculation:

**ROCR = Current Price ÷ Past Price**

Example:
- Bitcoin 5 minutes ago: $100
- Bitcoin now: $110
- ROCR(5) = 110 ÷ 100 = 1.10

This means 10% rise in 5 minutes.

ROCR interpretation:
- >1: Price went up, bigger = more
- =1: No change
- <1: Price fell, smaller = more down

ROCR is better than other indicators because it's just simple division—no complex formulas, intuitive.

---

## Chapter 3: How Does the Strategy Work?

### Step 1: Watch the Market

Every minute, calculate two ROCR values:
- ROCR(5): Past 5-minute price change
- ROCR(2): Past 2-minute price change

### Step 2: Wait for Signal

Two conditions must both be true:
- ROCR(5) > 1.10 (5 min rise >10%)
- ROCR(2) > 1.01 (2 min rise >1%)

### Step 3: Buy

Signal fires → immediate buy.

### Step 4: Wait for Outcome

1. Profit 5% → auto-sell, happy profit
2. Loss 1% → trigger stop, admit defeat
3. Keep rising → sell at 5% if it hits that level

---

## Chapter 4: Why This Design?

### Why Two ROCR Values?

Just one indicator can cause problems.

Say you only use ROCR(5) > 1.10:
- Coin surged 12% in first 3 minutes
- But last 2 minutes it's been pulling back
- ROCR(5) still > 1.10
- You'd buy at the high!

Like chasing a limit-up stock—you jump in, next day it limit-down opens.

So ROCR(2) confirms: are the last 2 minutes still rising?

Both must pass = reliable signal.

### Why 5 Minutes and 2 Minutes?

5 minutes is short enough to catch short-term explosions.
2 minutes is fresh enough to confirm trend still alive.

Shorter than this (like 10 seconds) gets drowned in noise. Longer (like 1 hour) misses the whole opportunity.

### Why Take Profit 5%, Stop Loss 1%?

**Take profit 5%**:
- Entry already showed >10% surge → strong momentum
- Another 5% is very achievable
- Don't be greedy, take what's given

**Stop loss 1%**:
- Momentum strategy assumes momentum will continue
- If it drops 1%, momentum probably failed
- Cut fast

**Most important: 5:1 ratio**

Win once = can lose five times and still break even!

Example: 10 trades
- Win 3 times, 5% each = +15%
- Lose 7 times, 1% each = -7%
- Net = +8%

Only 30% win rate and still profitable!

---

## Chapter 5: Who Is This For?

### Good For:

**Programmatic traders**: Know Python, use freqtrade
**High-frequency enthusiasts**: Like fast in-and-out, no overnight holds
**Risk-averse**: Can handle small losses per trade
**Disciplined traders**: Follow rules, no emotional trading

### Not For:

**Get-rich-quick dreamers**: This makes steady small money, not overnight riches
**Can't-watch-daily types**: Needs stable internet and equipment
**Emotional traders**: Panic selling kills this strategy
**No-tech folks**: Need to configure at least basic Python/freqtrade

---

## Chapter 6: How to Use It?

1. Install freqtrade
2. Drop JustROCR5.py into strategies folder
3. Configure trading pairs (BTC/USDT, ETH/USDT recommended)
4. Backtest first: see how it did over past year
5. Paper trade: test on live market with fake money
6. Small real money: start with $100-500 you can afford to lose

---

## Chapter 7: How Will It Lose Money?

### False Breakouts

Worst problem:
- Price suddenly surges, ROCR condition met
- Strategy buys
- Price immediately reverses
- Triggers 1% stop loss

Very common in ranging markets.

### Momentum Sudden Death

Sometimes momentum comes and goes fast:
- Price surges
- Strategy buys
- Sudden bad news
- Price gap-down, slippage beyond 1%

Even with stop loss, actual fill may be worse than 1%.

### Trading Costs

Invisible killer:
- Every trade: 0.1% fee
- 10 trades/day = 1% in fees alone

If strategy makes 2-3% per trade, fees take a big chunk.

---

## Chapter 8: What Are the Pros?

### Simple to Understand

30 lines, clear logic. Even beginners can read and understand.

### Sound Logic

Chase momentum, follow trends. Momentum is a real market phenomenon.

### Controllable Risk

1% stop loss means even bad trades don't hurt much. Good for sleep.

### Good Risk-Reward

5:1 ratio. Even with low win rate, can be profitable.

### Fast Execution

No overnight holds. A few minutes to hours per trade.

---

## Chapter 9: What Are the Cons?

### Few Signals

Conditions are strict. Not every day has opportunities.

### False Signal Risk

Ranging markets cause whipsaws.

### Slippage Impact

High-frequency trades mean more slippage damage.

### Fee Pressure

Frequent trades = more fees.

### Needs Tech Support

Stable internet required.

---

## Chapter 10: Can It Be Improved?

### Adjust Parameters

Feel signals too few? Lower 1.10 to 1.08
Feel too many bad trades? Raise 1.10 to 1.15

### Add Filters

**Volume filter**: Only buy when volume spikes
**Trend filter**: Only buy when larger timeframe is also up
**Volatility filter**: Avoid extreme volatility periods

### Add Exit Signal

Currently no active exit—just waits for stop/profit. Can add:
- ROCR(2) < 0.99 → exit
- Time stop: exit if held too long without profit

---

## Chapter 11: Compared with Other Strategies?

### vs. MA Strategy

MA strategies use moving average crosses, slower, smoother.
JustROCR5 faster, noisier.

### vs. Grid Strategy

Grid works in ranging markets, JustROCR5 works in trending markets.

### vs. Martingale

Martingale is gambling. JustROCR5 has discipline.

---

## Chapter 12: Notes for Use

### Mental Preparation

Accept frequent stops. This is normal. Sometimes 5 stops then 1 big win makes it all back.

Don't intervene manually. Once the system is running, let it run.

Watch long-term, not trade-by-trade.

### Tech Setup

Stable internet. Wired or solid WiFi. Mobile hotspot backup when traveling.

Reliable server. VPS recommended if possible.

Low-fee exchange. Fees kill high-frequency strategies.

### Money Prep

Use闲钱 (spare money). Only what you can afford to lose.

Keep margin. Enough balance for consecutive losses.

Start small. $100-500 first, add more only after proving it works.

---

## Chapter 13: Final Tips

### Learn First, Then Act

Don't rush real money. Backtest → paper trade → small real money.

### Stay Consistent

Don't change parameters just because of a few losses. That breaks the system.

### Keep Records

Log every trade. Review regularly to find patterns.

### Control Emotions

Automation's best feature: removes emotions. Don't override it.

### Keep Learning

Markets evolve, strategies need tuning. Stay curious.

---

**Summary:**

JustROCR5 is a simple, effective momentum strategy. It catches short-term price explosions with strict stops. If you can follow rules and manage emotions, this small strategy might deliver steady returns.

But remember: **no perfect strategy, only suitable strategies.** Know its strengths and weaknesses, use it in the right market, manage risk—that's how to win.

---

*This is the colloquial version of JustROCR5 Strategy.*
