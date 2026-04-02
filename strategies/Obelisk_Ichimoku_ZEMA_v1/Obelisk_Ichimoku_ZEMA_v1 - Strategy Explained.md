# Obelisk_Ichimoku_ZEMA_v1: Plain English Breakdown

## Written For You

This article breaks down Obelisk_Ichimoku_ZEMA_v1 in the simplest terms possible. No fancy math, no complex jargon.

⚠️ **Heads up**: The author says this is "experimental" — meaning it's not proven in live trading yet. Use it to learn, not for your life savings.

---

## 1. What Is This Strategy?

**Simple answer**: A **trend-following strategy** that catches mid-to-long-term trends and finds good entry points.

Think of it like surfing: you don't predict when a wave is coming, you wait for one and ride it. This strategy does the same — waits for a clear trend, then catches a wave.

Runs on **Freqtrade** (a crypto trading platform), uses **5-minute candles** as the main timeframe, but judges the big picture direction using **1-hour candles**.

The dual-timeframe thing: look at the map (1-hour) to know which direction to go, look at the road signs (5-minute) to know when to jump in.

---

## 2. What's the Ichimoku Cloud?

This strategy's main tool is the Japanese Ichimoku Cloud. Think of it as a weather forecast for the market.

**The Cloud**:
- Green cloud = sunny (uptrend)
- Red cloud = rainy (downtrend)
- Being above the cloud = you're above the weather
- Being below = you're stuck in the rain

**The Five Lines**:
1. **Conversion Line** (period 20): Short-term weather — changes fast
2. **Base Line** (period 60): Medium-term weather — more stable
3. **Leading A**: Future cloud edge (average of the two lines above, pushed forward)
4. **Leading B**: Other future cloud edge (longer average, pushed forward)
5. **Lagging Span**: "Past looking at present" — plots today's price in yesterday's position

The strategy uses **custom non-standard parameters** (20-60-120-30 instead of the usual 9-26-52-26). Why? The author wanted bigger, slower, more reliable signals rather than quick noisy ones.

---

## 3. What's ZEMA?

Zero Lag EMA — it's like a moving average but without the usual "half-second delay."

Regular moving averages are always behind — price moves but the line lags. ZEMA fixes this with some math tricks so the line follows price more closely.

**Why it matters here:**
- Buy ZEMA (default period 72): Long-period = wait for stable trends
- Sell ZEMA (default period 51): Shorter-period = more responsive to price changes

Translation: **Buying needs more proof** (longer ZEMA), **selling is more decisive** (shorter ZEMA). The author designed it so you enter carefully, exit fast.

---

## 4. What's SSL ATR?

SSL is another way to read trends. It draws a "channel" around price using ATR (a volatility ruler):

- When price is above the channel's upper line = bulls winning
- When price is below the channel's lower line = bears winning

The strategy uses SSL as a trend confirmer — "if Ichimoku says up AND SSL says up, then it's really an uptrend."

---

## 5. When Does It Buy? (Three Conditions)

All three must be true:

### Condition 1: Ichimoku Data Is Ready
Ichimoku needs at least 120 candles to calculate everything. If data isn't ready, no signals.

### Condition 2: NOT in a Bear Trend
Bear trend means ALL of these:
- Conversion < Base (short-term falling)
- Price below cloud bottom
- Future cloud is red
- Lagging Span below cloud

If any of these → the strategy won't buy.

### Condition 3: Price Is Below ZEMA Buy Line
Current close must be BELOW the ZEMA buy line × a multiplier (default ~1.004, meaning about 0.4% below).

Translation: Wait for price to come down a bit before buying. Don't chase.

---

## 6. When Does It Sell?

When close goes ABOVE the ZEMA sell line × multiplier (default ~0.964, meaning about 3.6% above the line).

That's it. Just one simple condition.

But wait — there's a twist: the strategy won't sell just because of this if it's still in an uptrend!

---

## 7. What's the "Smart Exit"?

This is the clever part. The strategy checks before selling due to hitting ROI targets:

```
If we're selling because we hit our profit target
AND the trend is still going up
THEN don't sell! Stay in the trade!
```

This is the "let profits run" philosophy. Even if you hit your "take profit" number, if the trend hasn't ended, the strategy keeps holding.

The only way it then exits is when either:
1. The trend actually ends (SSL flips bearish), OR
2. The stop-loss kicks in

---

## 8. How Are Stops Set?

### Stop-Loss: -29.4%

That's a HUGE stop — you can lose almost 30% before the strategy bails.

This seems scary, but the logic is: **the author believes in giving trades room to breathe**. If the trend is really up, a 29% pullback is just noise. If the trend ends, the exit signal will fire anyway.

⚠️ **This is aggressive.** Make sure your position sizing accounts for this.

### ROI (Profit Targets)
Stepped targets that get lower the longer you hold:
- Right away: 7.8%
- After 40 minutes: 6.2%
- After 99 minutes: 3.9%
- After 218 minutes: 0% (any profit is fine)

Translation: "First aim high. If not getting there fast, lower expectations. If it's been almost 4 hours and still not profitable, just take whatever you've got."

---

## 9. The Dual Timeframe Setup

**Main timeframe**: 5-minute — where trades actually happen
**Trend timeframe**: 1-hour — the "big picture" check

Here's how it works:
1. Get 1-hour price data
2. Calculate Ichimoku and SSL on the 1-hour chart
3. Map those indicators down to the 5-minute chart
4. Calculate ZEMA on the 5-minute chart
5. Make buy/sell decisions on 5-minute signals

It's like having a wise mentor (1-hour) telling you the market direction, while you (5-minute) look for the exact moment to act.

---

## 10. Parameters — Can You Change Them?

Yes! Four things you can tune:

### Buy Parameters
- **`low_offset`** (default ~1.004): How far below ZEMA price must be to buy. Lower = more aggressive entry.
- **`zema_len_buy`** (default 72): How many candles ZEMA uses for buy decisions. Longer = more conservative.

### Sell Parameters
- **`high_offset`** (default ~0.964): How far above ZEMA price must be to sell. Higher = hold longer.
- **`zema_len_sell`** (default 51): How many candles ZEMA uses for sell decisions. Shorter = exit faster.

**How to tune?**
- Freqtrade has a "hyperopt" feature that tries thousands of combinations automatically
- BUT: don't over-tune to historical data — what worked last year might not work next year

---

## 11. Strengths

1. **Well-researched theory**: Ichimoku is a decades-old, battle-tested system
2. **Multiple confirmations**: Not just one indicator, several must agree
3. **Catches real trends**: History shows it performs well in trending markets
4. **Smart exit**: Won't cut winners short just because a profit target was hit
5. **Tunable**: Parameters let you adapt it

---

## 12. Weaknesses / Pitfalls

1. **⚠️ Experimental tag**: Author says it hasn't been fully tested in live trading
2. **Stop-loss is wide**: -29.4% is nearly 1/3 of your money. Could be devastating if you don't size positions carefully.
3. **Needs lots of data**: First 500 candles (~41 hours on 5m) can't produce signals
4. **Locked to 5-minute**: You can't change the timeframe, code will error
5. **Lagging Span is confusing**: Beginners might think it uses future data (it doesn't, but the math looks that way)

---

## 13. Who Is This For?

### YES, use it if:
- You're a trend-following enthusiast
- You can stomach large drawdowns
- You want to learn and experiment
- You know some Python and can read the code
- You're patient and disciplined

### NO, skip it if:
- You want something ready to use out of the box
- You can't handle a potential 30% loss on one trade
- You want plug-and-play with no learning
- You're new to all of this

---

## 14. Practical Tips

### Backtesting
```bash
freqtrade backtesting --strategy Obelisk_Ichimoku_ZEMA_v1 --timeframe 5m
```

Get at least 500 candles of data (~41 hours), download 1h AND 5m data.

### Don't Forget Fees
5-minute trades = many trades. Fees add up fast. Set at least 0.1% per trade in your backtest.

### Start Small
The wide stop means position sizing is critical. Don't bet your whole account on one pair.

---

## 15. Improvement Ideas (From the Strategy Itself)

1. **Add volatility filter**: When ADX is low (no trend), don't trade
2. **Dynamic stops**: Instead of -29.4%, use 2× ATR as your stop
3. **Staged entries**: Buy half now, add more if trend confirms
4. **Time filter**: Skip Asian session if you want (lower volume = noisier)

---

## 16. Some Honest Thoughts

When studying this strategy, you can tell the developer is thorough:
- All the Ichimoku parameters are doubled (20 instead of 9, 60 instead of 26, etc.) = more stability
- Smart exit keeps you in winners = overcoming the fear of taking profits
- Wide stop = trust in the trend

The wide stop is a double-edged sword. Good for traders with big accounts and strong nerves. Dangerous for smaller accounts or nervous traders.

Also: **any strategy is only as good as the person running it**. Can you stomach seeing -20% on one trade and NOT manually closing it because you trust the system? If not, you need a different strategy.

---

## Quick Reference

| Item | Value |
|------|-------|
| Type | Trend following |
| Direction | Long only |
| Timeframe | 5m (main), 1h (trend) |
| Stop-Loss | -29.4% |
| Buy when | Price below ZEMA buy line |
| Sell when | Price above ZEMA sell line (but smart exit may hold) |
| Best for | Trending markets, patient traders |
| Not for | Ranging, nervous traders |

---

**Final word**: Strategy is a tool. The tool is only as good as the craftsman. Understand it, test it, then decide if it's right for you.

---

*Strategy: Obelisk_Ichimoku_ZEMA_v1*
*Author: Obelisk*
*Status: Experimental*
*Platform: Freqtrade*
