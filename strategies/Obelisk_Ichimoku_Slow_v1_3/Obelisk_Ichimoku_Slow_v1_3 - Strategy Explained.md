# Obelisk_Ichimoku_Slow_v1_3: Plain English Breakdown

## 1. What Is This Strategy?

**One line**: A **"trend harvester"** — when a big move comes, get on early and hold all the way to the end without getting off.

Author says it straight: "The whole point is to buy into an uptrend and stay on as long as possible.

**Breaking down the name**:
- **Obelisk**: Author's handle
- **Ichimoku**: Uses the Japanese Ichimoku Cloud system
- **Slow**: Not chasing quick gains — slow and steady
- **v1.3**: Third version (v1.0 → v1.1 → v1.2 → v1.3)

**What it's NOT**:
- NOT a scalping strategy
- NOT frequent trading
- NOT a pullback strategy
- NOT good for ranging markets

---

## 2. Why Would You Use This?

### Pros

**1. Logic is crystal clear**
Strategy answers one question: "Is this an uptrend?" If yes, buy. If the trend breaks, sell. Simple.

**2. Multiple confirmations**
Four different indicators all must agree before it buys — like getting approval from four different experts. Wrong signal rate is very low.

**3. Doesn't chase, waits for pullbacks**
Instead of buying when price is rocketing up, it waits for price to pull back a bit first. Like shopping when things go on sale.

**4. Perfect for office workers**
Uses 1-hour candles — don't need to watch constantly. A trend can last days or weeks.

### Cons

**1. Slow to react**
Because it's "slow," by the time the signal fires, price has already moved some.

**2. Ranging markets hurt**
Sideways price action = signals fire, stop out, repeat. Fees accumulate.

**3. Start timing matters**
Author warns: "If you start this strategy when the market is topping, you might buy trends about to die."

---

## 3. The Core Tool: Ichimoku Cloud

This is the strategy's main weapon — a Japanese invention that looks like a cloud on your chart.

### The Cloud

Think of looking at the sky. You're above the clouds = good weather (bull). You're below = bad weather (bear).

The cloud has edges:
- **Green cloud**: A > B → uptrend
- **Red cloud**: A < B → downtrend
- Thick cloud: Strong support/resistance
- Thin cloud: Weak, easy to break through

### Five Lines

**1. Conversion Line (fast)**: Average of last 20 candles' high/low. Short-term trend.
**2. Base Line (slow)**: Average of last 60 candles' high/low. Medium-term trend.
**3. Leading A**: (Conversion + Base)/2, shifted 30 hours forward.
**4. Leading B**: 120-candle average, shifted 30 hours forward.
**5. Lagging Span**: Today's close, shifted 120 hours BACKWARD (like looking at today's price from 5 days ago).

### Strategy's Special: "Strong Green Cloud"
Must satisfy all three:
1. Cloud is green (A > B)
2. Conversion > Base (short-term up)
3. Base > cloud (medium confirming)

This triple confirmation = strong, unmistakable uptrend.

---

## 4. Weapon #2: SSL Channel

SSL is like a "trend detector" built with ATR.

How it works:
- Calculates a channel around price using ATR (market volatility ruler)
- When price is above the channel = bulls in charge
- When price is below = bears in charge

**SSL's three roles in this strategy:**
1. Confirms trend
2. Identifies pullback timing (wait for price to return to near SSL before buying)
3. Fires the ONLY exit signal

---

## 5. Weapon #3: EMA Double Moving Average

EMA = Exponential Moving Average. This strategy uses two:

- **EMA50**: Recent 50 hours of price
- **EMA200**: Last 200 hours of price

Conditions:
1. Price > EMA50 (current strength)
2. EMA50 > EMA200 (medium-term uptrend confirmed)

Classic bullish signal: "Golden Cross" style confirmation.

Added in v1.3 specifically to filter out weak trends and reduce bad entries.

---

## 6. Weapon #4: EFI (Elder Force Index)

EFI combines price change + volume:
```
EFI = (Today's close - Yesterday's close) × Today's volume
```
Then smoothed with EMA.

- EFI > 0: Price went up with volume = real buying, real move
- EFI < 0: Price fell with volume = real selling, real move

EFI acts as the "gatekeeper" — all other indicators could say "buy" but if EFI < 0 (no real money coming in), the strategy won't buy.

---

## 7. When Does It Buy?

First layer: Big trend confirmed
- Ichimoku says OK (weight 4) ✅
- SSL says OK (weight 3) ✅
- EMA says OK (weight 2) ✅

All three give thumbs up = "trending" state turns ON.

Second layer: Find entry timing
- EFI > 0 (real money flowing) ✅
- Open price < SSL_up (pulling back, not chasing) ✅
- Close price < SSL_up (still pulling back) ✅

Hour boundary requirement: Must be at the start of an hour (minute = 00) to avoid duplicate signals.

**Plain English**: The big picture is clearly up. Now we wait for price to breathe/pull back a little. When it does and real money is still coming in, we get in.

---

## 8. When Does It Sell?

**ONE condition**: SSL flips from bullish to bearish.

That's it. Nothing else.

No:
- Cloud break → doesn't sell
- EMA cross down → doesn't sell
- EFI turns negative → doesn't sell
- Time limit → doesn't sell

Only: SSL says trend is over → SELL.

### Why So Simple?

Author's logic:
- If trend is still up, don't sell just because price pulled back — let it breathe
- SSL flipping = the ONLY thing that reliably says "trend is done"
- v1.2 used cloud-top break as exit, but it was too sensitive — kept stopping out during normal pullbacks → v1.3 removed it

This is for **patient trend riders**. You get on, you stay on, you get off when SSL says "the trend is over."

---

## 9. Stop-Loss Setup

**10% stop-loss** — but author says it barely matters:

> "Setting a stop-loss doesn't make much sense since it will buy back into the trend on the next opportunity unless the trend has ended."

Translation: If the stop-loss fires but the trend is still going up, the strategy will immediately buy again via its entry signal. The only time stop-loss matters is when the trend is genuinely over — and the exit signal would have sold anyway.

So the stop-loss is more like "mental safety net" than a real trading rule.

### There's Also ROI
Stepped profit targets that DECAY over time:
- Immediate target: 10%
- After 60 hours: 7.2%
- After 120 hours: 4.9%
- After 240 hours: 2%
- After 360 hours: any profit is fine

Translation: "If we're not making new highs after a while, just take whatever profit we have."

---

## 10. What Markets Are Best?

### Best: Clear Uptrends
This is the strategy's home turf! When Bitcoin or crypto is in a sustained climb, this strategy shines.

### Good: Slow Grind Uptrends
Price slowly climbing without huge spikes — perfect for the "slow" approach.

### Not Great: Mainstream coins
BTC and ETH are stable and trend-y, but their trends can be slow and prolonged — might need patience.

### Bad: Ranging Markets
Price going sideways, up and down, no direction:
- SSL keeps flipping
- You keep getting stopped out
- Fees eat profits

### Bad: Violent Spikes
Big surges of 50% one day, drops of 30% the next day — indicators can't keep up with that volatility.

### Bad: Altcoin Crashes
Small coins that suddenly collapse — strategy might not react fast enough.

---

## 11. Backtesting Setup

### Timeframe
**1 hour** (can also backtest 5m or 1m for verification).

### Data Needed
**180 candles minimum** at startup. On 1-hour chart that's 7.5 days of data.

### Recommended Pairlist Setup
```python
pairlists = [
    VolumePairList(25),      # Top 25 by volume
    AgeFilter(10 days),      # Exclude brand new coins
    PriceFilter(),           # Exclude dirt cheap coins
    RangeStability(3 days)   # Exclude too-stable coins
]
```

---

## 12. Pitfalls to Watch

### Pitfall 1: Start Timing Is Critical
Author emphasizes: **Starting at a market top = buying dying trends.**

Look at the overall picture before starting. Don't start during peak euphoria.

### Pitfall 2: Don't Randomly Change Parameters
- Ichimoku parameters tuned for 1-hour chart
- EMA periods are 50 and 200 — changing might misalign everything
- Exit is just SSL — adding conditions probably makes it worse

Change one thing at a time, then backtest. Don't just tweak based on feel.

### Pitfall 3: Stop-Loss Is Weak
-10% seems wide. The real risk control is in pair selection and position sizing.

### Pitfall 4: Needs Enough Historical Data
First run needs 7.5 days of 1h candles. Before that, signals may be unreliable.

---

## 13. How to Get Started

### Step 1: Understand the Logic
- Trend following, not pullback catching
- Slow, not fast
- Long only, not shorting
- Buy on confirmation, exit on SSL reversal

### Step 2: Backtest
Run on historical data. Check: good periods, bad periods, max drawdown, annual returns.

### Step 3: Paper Trade
Paper trade for a while before real money.

### Step 4: Small Capital Live
Single trade < 10% of capital, total exposure < 50%.

### Step 5: Regular Check-Ins
Weekly holdings check, monthly performance review.

---

## Summary

Obelisk_Ichimoku_Slow_v1_3 is a **patient trend hunter**.

It waits quietly in the market, four radar systems (Cloud, SSL, EMA, EFI) scanning simultaneously. When prey (a confirmed trend) appears, it doesn't pounce immediately — waits for it to get closer (pullback entry).

Once it catches the trend, it hangs on tight and doesn't let go until SSL says the trend is actually over.

It won't chase prey around or get scared off by every little movement. That's the wisdom of a "slow" strategy.

**Three rules to remember:**
1. **Trend is king**: No trend = no trade
2. **Buy on pullback**: Wait for price to come back to you
3. **Hold patiently**: Don't let go until the trend is truly over

If you understand and commit to these three principles, this strategy can help you catch big moves.

---

*Strategy: Obelisk_Ichimoku_Slow_v1_3*
*Author: Obelisk*
*Document date: March 27, 2026*
