# mark_strat_opt Strategy Explained (Plain English)

> **Strategy Number**: #463  
> **What it does**: Catches crazy price drops and bounces  
> **Speed**: Super fast (1-minute candles)

---

## The Big Picture

Think of mark_strat_opt as a "panic buyer" strategy. When everyone is freaking out and selling like crazy, this strategy steps in and buys at rock-bottom prices, then waits for the bounce back.

**The simple version**: Price crashes hard → Multiple indicators scream "OVERSOLD!" → Buy → Wait for rebound → Sell → Profit

---

## How It Works (No Jargon)

### When to Buy (ALL 5 must be true)

1. **ADX > 49**: The trend is SUPER strong (we're in extreme territory)
2. **FastD < 30**: Stochastic says "way too cheap"
3. **MFI < 23**: Money is flowing out like crazy (capitulation)
4. **RSI < 34**: Classic oversold signal
5. **Price below Bollinger Band lower line × 4**: This is the kicker — price has to be EXTREMELY low, like 4 standard deviations below normal. This almost never happens.

**Translation**: All 5 conditions together mean "EVERYTHING is screaming this is a once-in-a-blue-moon crash, buy now!"

### When to Sell

The strategy sells when:
- ADX drops below 95 (trend weakening)
- FastD goes above 70 (now overbought)
- RSI shoots above 94 (super overbought)
- SAR flips above price (trend reversal confirmed)

**Plus automatic profit-taking**:
- If you're up 7% right away → take profit
- After 8 minutes → happy with 1%
- After 19 minutes → happy with 0.5%
- After 34 minutes → just get out break-even

**And a trailing stop**: Once you're up 7.5%, it follows the price up, locking in gains if price drops 9.8% from the peak.

### Stop Loss

- **Hard stop**: -20% (pretty wide, gives the trade room to breathe)
- **Trailing stop**: Activates at +7.5% profit, trails by 9.8%

---

## Why This Setup?

### The Good Stuff ✅

1. **Super selective**: Needs 5 things to line up perfectly. You won't trade often, but when you do, it's probably legit.
2. **Catches the big crashes**: That 4-standard-deviation Bollinger Band thing? That's like waiting for a 100-year flood. When it happens, you want to be there.
3. **Quick to take profits**: Doesn't get greedy. Takes money off the table fast.
4. **Easy to understand**: Buy when everything is oversold, sell when everything is overbought. Makes sense.

### The Not-So-Good Stuff ⚠️

1. **Rare signals**: You might wait days or weeks for a signal. Boring.
2. **Needs fast connection**: 1-minute candles mean you need a solid internet connection and API.
3. **Slippage danger**: When everyone's panicking, the price you see isn't always the price you get.
4. **Might be over-optimized**: Those super-specific numbers (like 38.9 for Fisher RSI) might be curve-fit to past data.

---

## When to Use It

| Market Situation | Should You Use It? | Why |
|-----------------|-------------------|-----|
| Market just crashed 20% in an hour | ✅ YES! | This is exactly what it's built for |
| Choppy, going down slowly | ⚠️ Maybe | Might get some signals, but not ideal |
| Quiet, boring market | ❌ NO | You'll wait forever |
| Market ripping higher | ❌ NO | Wrong strategy for this |

---

## Real Talk: What You Need to Know

### It's a "Sniper" Strategy

This isn't a machine gun. It's a sniper rifle. You might sit there for hours doing nothing, then BAM — one shot, one kill.

**Capital tip**: Don't put all your money in this. Maybe 10-20% of your portfolio. The rest of the time, your cash is just... waiting.

### Hardware You'll Need

| How Many Coins | Minimum RAM | Recommended RAM |
|---------------|-------------|-----------------|
| 1-5 coins | 4GB | 8GB |
| 6-20 coins | 8GB | 16GB |
| 20+ coins | 16GB | 32GB |

### Backtest vs. Reality

- **Backtest**: Looks amazing! Perfect entries, clean exits.
- **Real life**: Slippage happens. Your 7% profit might be 6%. Your -20% stop might be -22%.
- **Signal frequency**: Backtest might show 10 signals/month. Real life? Maybe 3.

---

## For Manual Traders

If you're not running this on a bot:

1. **Use it as an alarm**: Set alerts for these conditions. When they fire, look at the chart yourself.
2. **Check liquidity**: Before buying, make sure there's actually buyers when you want to sell.
3. **Don't FOMO**: If you miss the entry, wait for the next one. There will be another crash eventually.

---

## The Bottom Line

**mark_strat_opt** is for patient traders who want to catch the big crashes. It's not exciting day-to-day, but when it fires, it can make good money fast.

**Think of it like**: Insurance that pays you when the market has a heart attack.

**Best for**: 
- People who can wait
- High-volatility coins (BTC, ETH, etc.)
- As part of a diversified strategy portfolio (not your only strategy)

**Not for**:
- People who need action every day
- Low-volatility markets
- Full-portfolios (too signal-sparse)

---

## Quick Reference Card

```
BUY WHEN:
✓ ADX > 49 (strong trend)
✓ FastD < 30 (oversold)
✓ MFI < 23 (money fleeing)
✓ RSI < 34 (oversold)
✓ Price < BB lower band × 4 (EXTREME!)

SELL WHEN:
✓ Any sell signal triggers
✓ OR ROI hits target
✓ OR trailing stop activates

PROFIT TARGETS:
• Immediate: 7%
• 8 min: 1%
• 19 min: 0.5%
• 34 min: Break even

STOP LOSS:
• Hard: -20%
• Trailing: Activates at +7.5%, trails 9.8%
```

---

**Remember**: This strategy is a specialist, not a generalist. Use it for what it's good at, and pair it with other strategies for the times it sits idle.
