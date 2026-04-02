# ElliotV2: What's This Strategy?

## 1. What Does This Strategy Do?

Put simply, ElliotV2 is an automated trading strategy that helps you "buy low, sell high" in the cryptocurrency market.

Its name contains "Elliot" because it uses an indicator called the "Elliott Wave Oscillator." This indicator was invented by Ralph Nelson Elliott, a guy who spent years observing the stock market back in the 1930s. He noticed that price movements follow wave-like patterns — up and down in cycles. Market sentiment swings between optimism and pessimism, and these swings show up in price movements. Uptrends break into several waves, and downtrends do the same. If you can spot these wave patterns, you can buy and sell at the right moments.

This strategy is designed to catch these "waves" — buy at wave troughs, sell at wave peaks. Sounds simple, right? But executing it reliably is hard. ElliotV2 uses modern computer programs to automatically judge these timing points.

It's specifically built for Freqtrade, a quantitative trading software. If you've got a cryptocurrency exchange account and configure this software, it can trade automatically for you — no need to stare at charts all day.

---

## 2. How Does It Decide When to Buy?

This strategy has two sets of buy methods, like having two different keys for two different locks. This way it can adapt to different market conditions — opportunities whether things are going up or coming down.

### Key 1: Catching a Pullback Discount

Imagine a stock that's been going up in price, steadily climbing. But once in a while, some traders want to lock in profits and sell, pushing the price down a bit. This is called a "pullback" or "retracement."

The strategy jumps in during moments like this:
- The price drops to just below the moving average (about 2.2% lower)
- The big trend is still rising (judged by the EWO indicator)
- There's still upward momentum (confirmed by RSI, which must be below 63)

All three conditions met? Strategy buys.

Think of it like this: you've had your eye on a popular product for a while. Normally it's sold out, but one day there's a small discount promotion — you pounce. But you don't buy blindly. You first check if the product is actually good (trend still there), if the discount is real (price is low enough), and if others are still buying it (momentum is there).

### Key 2: Bottom-Catching After a Crash

Sometimes the market panics and everyone sells, driving prices way down. But when things drop too far, they tend to bounce back, right? Like a rubber band pulled too tight — it's gonna snap back.

The strategy also jumps in during moments like this:
- The price drops to below the moving average (again about 2.2% lower)
- The EWO indicator is especially low (below -13.043, meaning things have gotten really grim)

Notice the second set of logic doesn't have an RSI check. Why? Because when EWO is already below -13, the market is in full panic mode — RSI is definitely low too. Adding an RSI check would be redundant and might filter out valid opportunities.

This is like going shopping during a clearance sale. You grab bargains while the market is depressed, then wait for things to recover. Of course, bottom-catching carries risk — you might catch a falling knife — which is why the strategy has stop-loss protection.

---

## 3. What Is This EWO Thing?

EWO stands for Elliott Wave Oscillator. Don't let the name intimidate you — the principle is dead simple. It compares two moving averages of different lengths and measures how far apart they are.

Here's the math:
- Calculate a fast line: EMA of the last 50 candlesticks
- Calculate a slow line: EMA of the last 200 candlesticks
- Subtract the two, divide by the current price, multiply by 100

That gives you the EWO value.

What does it mean?
- A big positive EWO means the fast line is way above the slow line — short-term momentum is strong
- A big negative EWO means the fast line is way below the slow line — short-term momentum is weak
- EWO near zero means the two lines are roughly equal — the market is choppy, no clear direction

ElliotV2 uses EWO in two zones:
- EWO above 4.471: This is a "pullback in an uptrend" — the market's big picture is still rising, just taking a breather. Use Key 1 to hop on.
- EWO below -13.043: This is "things have dropped too far" — possibly excessive panic. Use Key 2 to gamble on a rebound.

These numbers (4.471 and -13.043) weren't pulled out of thin air — they were optimized through extensive historical data testing to find the sweetest spot.

---

## 4. What's EMA? Why Use Two Different Ones?

EMA stands for Exponential Moving Average.

To understand it, let's start with regular SMA (Simple Moving Average). SMA takes the closing prices of the last N candlesticks, adds them up, and divides by N. For example, a 5-day SMA adds up the last 5 days of closes and divides by 5.

EMA is different: more recent data gets heavier weight. Today's price impacts the EMA the most, yesterday's next, the day before even less. This makes it more responsive to the latest price action.

ElliotV2 uses two EMAs of different lengths:
- Buy side: 31-period EMA — a medium-length period
- Sell side: 99-period EMA — a much longer period

Why different lengths for buying and selling?

Buying uses a shorter EMA because you need to find entry opportunities in a relatively short time window. The 31-period EMA is more responsive to price changes and helps you find good entry points.

Selling uses a longer EMA because you want to make sure the trend is genuinely established before exiting, not getting shaken out by short-term fluctuations. The 99-period EMA is more stable and won't wig out from minor moves.

In short: act fast when getting in, stay calm when getting out. Be quick to seize opportunities when entering; be steady when exiting to make sure you've actually locked in real profits.

---

## 5. How Does It Decide When to Sell?

The sell logic is way simpler than the buy logic — just one condition.

The strategy sets a "profit-taking line" — when the price climbs to about 5.4% above the moving average, it sells.

How is this calculated? Using the 99-period EMA as a baseline, multiplied by 1.054. For example, if the EMA is at $100, the profit-taking line is at $105.40. When price hits that, sell.

Why 5.4%? This was optimized for results. Set it too low and you might sell right after buying, making peanuts. Set it too high and you might wait forever and never get there — then the price crashes back down.

This 5.4% offset gives the price enough room to run, without being too greedy.

Of course, that's just signal-based selling. The strategy has other ways to exit, like stop-losses and trailing stops, which we'll cover later.

---

## 6. What Does the RSI Indicator Do?

RSI stands for Relative Strength Index.

Its value ranges from 0 to 100, used to judge whether the market is "overbought" or "oversold":
- Above 70 is typically considered "overbought" — price might pull back
- Below 30 is typically considered "oversold" — price might bounce

But this isn't absolute. Sometimes overbought can keep getting more overbought, and oversold can keep getting more oversold. RSI is just a reference.

ElliotV2 uses RSI in the first buy logic:
- It requires RSI to be below 63

Why 63 instead of 30 (traditional oversold)? Because if you wait until RSI hits 30, you might have already missed the best entry point. 63 is a middle ground — not too aggressive (buying in overbought territory, might drop immediately), not too conservative (waiting too long, missing opportunities).

Note: The second buy logic (oversold bottom-catching) doesn't use RSI at all. Because at that point EWO is already extremely low (below -13.043), the market is already panicking hard, RSI is certainly low too — no need to double-check.

---

## 7. How Are Stop-Loss and Take-Profit Set?

This strategy's risk management is pretty solid, with "three lines of defense" protecting your money.

### Line 1: Fixed Stop-Loss

This is the most basic protection: if you lose more than 17.9%, the strategy automatically sells to stop the bleeding. That's it, game over, move on.

Some folks might say: "17.9% is a LOT. Can we tighten it up?"

But the cryptocurrency market is volatile — a single day can swing 10% or more. If your stop-loss is too tight, you get shaken out right before price bounces back — and that hurts worse.

17.9% was calculated and tested. It protects your capital while not triggering too easily from normal fluctuations.

### Line 2: Trailing Stop

This is a "rising tide lifts all boats" mechanism — brilliant in its simplicity. Here's the logic:

- It doesn't activate until you've made 4.9% profit
- Once active, it follows the highest price, staying 1% below the peak
- The moment price pulls back and hits this line, it auto-sells

Here's an example:

Say you bought at $100:
- Price climbs to $105, you're up 5%. Trailing stop activates, stop line at $105 × 0.99 = $103.95
- Price keeps climbing to $110, stop line moves up to $110 × 0.99 = $108.90
- Price keeps climbing to $120, stop line moves up to $120 × 0.99 = $118.80
- Suddenly price starts dropping and hits $118.80 — TRIGGERED! You sold and locked in around 18.8% profit.

This is like flying a kite: the higher the kite flies, the more string you let out, but you always keep it within reach to reel back in. The moment the kite starts dropping, you reel it in.

The beauty of trailing stops: if the price keeps climbing, you keep riding it. If it reverses, you protect most of your gains — you won't give back all your profits.

### Line 3: Tiered Profit-Taking

This sets different profit targets based on how long you've been holding:

| Holding Time | Profit Target |
|--------------|--------------|
| Just bought | 15.4% |
| After 18 hours | 7.4% |
| After 50 hours | 3.9% |
| After 165 hours (~7 days) | 2% |

Why does the target drop the longer you hold?

Because your capital is tied up. If a trade is stuck for a week without making money, that capital's opportunity cost is accumulating. Instead of staying locked in a non-profitable position, better to free up the capital and find the next opportunity.

Think of it like borrowing money for a business: in the first few days the interest is low, so you can wait for a better price. But after a month, the interest has piled up — at that point, even a small profit is worth taking.

These three lines of defense work together: stop-loss protects your capital, trailing stop protects your profits, tiered profit-taking controls time costs. A complete protection system.

---

## 8. What Coins Is This Strategy Good For?

Simply put: mainstream coins with moderate volatility and good liquidity.

**Good for:**
- BTC (Bitcoin) — biggest market cap, best liquidity
- ETH (Ethereum) — second biggest, very stable too
- Other mainstream coins like SOL, ADA, AVAX, etc.

**Not so good for:**
- Newly listed coins — not enough historical data, indicators can't calculate properly
- Extremely volatile altcoins — conditions might not trigger before getting washed out, or stop-losses get hit constantly
- Illiquid coins — bid-ask spread is huge, slippage is severe, actual fill prices might differ significantly from what you expect

The timeframe is 5-minute candlesticks — a relatively short cycle, suitable for intraday or short-term trading. If you want to use a longer timeframe (like 1 hour or 4 hours), you'd need to retune the parameters, because different cycles optimize to different results.

---

## 9. What Are the Strategy's Strengths?

### 1. Logic Is Clear and Easy to Understand

The core of this strategy is just two entry conditions, one exit condition, plus three lines of defense. No stacking dozens of indicators until you're completely lost. You can easily understand what it's doing and why — why it buys, why it sells.

### 2. Risk Management Is Solid

Fixed stop-loss, trailing stop, tiered profit-taking — three lines of defense protecting your capital. This isn't a "either you hit the jackpot or you blow up" strategy. It's got a systematic risk control mechanism.

### 3. Parameters Are Adjustable

The strategy exposes 7 main parameters for optimization. You can tune them for different coins and different market environments — not rigid.

### 4. Handles Different Market Conditions

Two entry logics: one catches trend pullbacks (buy while rising), one catches oversold bounces (buy while falling). Either way, the market's moving, you're making money.

### 5. Has Theoretical Backing

Based on Elliott Wave theory, not just made up out of nowhere. Of course, theory is theory — actual results still depend on backtesting and live trading.

---

## 10. What Risks Does This Strategy Have?

### 1. Choppy Markets Can Lose Money

This strategy is fundamentally a trend strategy, best suited for markets with a clear direction (either up or down). If the market is stuck in a sideways grind — up and down but not going anywhere — it might buy and sell repeatedly, losing a bit on fees and spread each time.

Like fishing: you catch fish when the current is strong; but if the water is still, dragging the net around catches nothing.

### 2. Stop-Loss Might Be Too Wide

17.9% stop-loss is too wide for many people. If you put in $10,000, one trade could lose $1,790. Can you stomach that? If it feels too wide, you can adjust it — but note that adjusting it might affect overall performance.

### 3. Parameters Don't Stay the Same Forever

Current parameters were optimized on 2023 data. Markets change. 2024, 2025 might perform differently. Need to re-optimize periodically, or use different parameters for different periods.

### 4. Rapid Reversals Might Not React Fast Enough

Both EMA and EWO are calculated from historical data — there's inherent lag. If the market suddenly reverses (say a big black-swan event), the strategy might not react in time, still trading in the original direction.

### 5. Requires Some Technical Foundation

Although the strategy runs automatically, to use it well you need to understand its logic, know how to backtest, how to optimize parameters, and how to analyze results. It's not a download-and-forget money printer.

---

## 11. How to Use This Strategy?

### Step 1: Set Up the Environment

You need:
1. Python and Freqtrade software installed
2. A cryptocurrency exchange account (like Binance, OKX, etc.)
3. Exchange API keys configured in Freqtrade

### Step 2: Download the Strategy

Put the ElliotV2.py file into Freqtrade's strategy directory (usually user_data/strategies/).

### Step 3: Backtest

Before trading with real money, backtest with historical data:

```bash
freqtrade backtesting --strategy ElliotV2 --timerange 20230101-20231231
```

Backtesting will tell you: how much money this strategy made in that period, max drawdown, win rate, etc.

### Step 4: Optimize Parameters

If the default parameters don't look great, use hyperopt to optimize:

```bash
freqtrade hyperopt --strategy ElliotV2 --spaces buy sell --timerange 20230101-20231231 -j 4
```

This automatically searches for the best parameter combination. Watch out though: over-optimizing can lead to overfitting — it might look great on historical data but fail on future data. Use out-of-sample data to verify.

### Step 5: Simulated Trading (Dry Run)

Run it on a simulated account for a while first:

```bash
freqtrade trade --strategy ElliotV2 --dry-run
```

Simulated trading doesn't execute real trades, just simulates the strategy's logic with fake money. This lets you observe how it performs in the live market.

### Step 6: Real Trading

Once simulated trading looks good, go live:

```bash
freqtrade trade --strategy ElliotV2
```

Start with a small amount, like just 10%-20% of your total capital. Only increase once you're consistently profitable.

---

## 12. What Parameters Can Be Adjusted?

The strategy exposes 7 main parameters, defined in the code using IntParameter and DecimalParameter:

| Parameter | Default | Range | Role |
|-----------|---------|-------|------|
| base_nb_candles_buy | 31 | 5-80 | Buy EMA period |
| base_nb_candles_sell | 99 | 5-80 | Sell EMA period |
| low_offset | 0.978 | 0.9-0.99 | Buy price offset |
| high_offset | 1.054 | 0.99-1.1 | Sell price offset |
| ewo_high | 4.471 | 2.0-12.0 | EWO high threshold (trend entry) |
| ewo_low | -13.043 | -20.0--8.0 | EWO low threshold (bottom entry) |
| rsi_buy | 63 | 30-70 | RSI entry upper limit |

**Tips for tuning:**

**Want to be more aggressive (trade more frequently, enter faster):**
- Lower low_offset (e.g., 0.95, so price only needs to be 5% below EMA to enter)
- Raise ewo_high (e.g., 8.0, trend entry triggers more easily)
- Raise rsi_buy (e.g., 70, allows entries at higher RSI)
- Shorten EMA period (e.g., buy with 20-period)

**Want to be more conservative (trade less, but higher quality):**
- Raise low_offset (e.g., 0.99, wait for bigger dips)
- Lower ewo_high (e.g., 3.0, only enter when trend is very strong)
- Lower rsi_buy (e.g., 50, wait for lower RSI)
- Lengthen EMA period (e.g., buy with 50-period)

**Want to exit faster:**
- Lower high_offset (e.g., 1.03, sell at 3% profit)
- Shorten sell EMA period

**Want to hold longer:**
- Raise high_offset (e.g., 1.08, don't sell until 8% profit)
- Lengthen sell EMA period

Of course, you can't just tweak things however you want. The best approach is hyperopt optimization — let the computer find the best combo for you.

---

## 13. Final Advice

### 1. No Strategy Guarantees Profits

This is the most important point: every strategy has losing periods, ElliotV2 included. Quantitative trading can improve win rates and control risk, but it can't guarantee wins.

Backtesting results looking great doesn't mean the future will be the same. Markets change, strategies need to evolve too.

### 2. Good Backtesting ≠ Good Live Performance

Running well on historical data doesn't guarantee the future will match because:
- Backtesting might have survivorship bias (if this time period looks great, another might look terrible)
- Backtesting doesn't account for slippage, network latency, and other real-world trading issues
- Market structure evolves; patterns that worked before might not work later

So always do simulated trading before going live, and start with small money.

### 3. Position Management Matters

Don't put all your money in one basket. Start with 10%-20% of your capital, and only increase once you've confirmed the strategy is consistently profitable.

Also keep some reserve capital. If you hit a string of losses and need to average down or wait for opportunities, you've got ammunition.

### 4. Check In Regularly

A strategy isn't a set-it-and-forget-it tool. Check weekly or monthly how it's performing. If performance notably worsens, you might need to:
- Tweak parameters
- Pause the strategy
- Analyze if the market has changed

### 5. Keep Learning

The cryptocurrency market evolves fast — new coins, new concepts, new plays keep emerging. Keep learning new knowledge, understanding what's happening in the market, to better adjust your strategy.

### 6. Stay Emotionally Steady

The biggest danger in systematic trading is the urge to intervene. Once you've set it up, let it run. Only intervene if there's a clear problem to fix. Frequent meddling usually backfires.

Good luck with your trading! Quantitative trading is a marathon, not a sprint. Only by persistently learning and optimizing can you go the distance.
