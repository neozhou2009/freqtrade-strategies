# quantumfirst Strategy Explained (Plain English)

> **Strategy Number**: #464  
> **What it does**: Catches bounces when big money shows up  
> **Speed**: Medium (5-minute candles)

---

## The Big Picture

quantumfirst is like a "follow the smart money" strategy. It waits for a coin to be cheap (below its average price), then watches for a HUGE spike in volume — meaning big players are buying. Once that happens, it jumps in and rides the rebound.

**The simple version**: Price is low → Volume EXPLODES (4x normal!) → Big money is buying → Jump in → Ride the bounce → Get out → Profit

---

## How It Works (No Jargon)

### When to Buy (ALL conditions must be true)

1. **Price > 0.000002**: Filters out super cheap coins (avoid liquidity traps)
2. **Volume > 4x the average**: This is the BIG one. Volume has to be 4 times higher than the last 200 candles. Something's happening!
3. **Price below 40-period SMA**: Coin is trading below its average — it's "on sale"
4. **FastD > FastK**: Stochastic is crossing up (momentum shifting)
5. **RSI > 0**: RSI is positive (basically always true, just a sanity check)
6. **FastD > 0**: Stochastic is positive (also basically always true)
7. **Fisher RSI < 38.9**: Fancy math way of saying "oversold"

**Translation**: "This coin is cheap, and suddenly there's 4x normal volume. Smart money is buying. Let's go with them."

### When to Sell (TWO ways — either one triggers)

**Way 1: RSI Rebound**
- RSI crosses above 50 (back to neutral from oversold)
- MACD is still negative (trend not fully bullish yet)
- Minus DI is positive (some downward pressure remains)
- **Meaning**: "We got our bounce, time to take profits before it reverses again"

**Way 2: SAR + Fisher Combo**
- SAR flips above price (trend reversal signal)
- Fisher RSI > 0.3 (now overbought)
- **Meaning**: "Party's over, everyone's bought in, time to exit"

**Plus automatic profit-taking**:
- If you're up 5% right away → take profit
- After 20 minutes → happy with 4%
- After 40 minutes → happy with 3%
- After 80 minutes → happy with 2%
- After 24 hours → still want at least 1%

**And a trailing stop**: Once you're up 1%, it follows the price up, locking in gains if price drops 2% from the peak.

### Stop Loss

- **Hard stop**: -10% (moderate, not too tight, not too loose)
- **Trailing stop**: Activates at +1% profit, trails by 2%

---

## Why This Setup?

### The Good Stuff ✅

1. **Follows the money**: 4x volume doesn't lie. Someone big is buying.
2. **Fisher RSI is clever**: It's like RSI on steroids — makes extreme signals way more obvious.
3. **Two exit strategies**: Flexibility to get out different ways depending on how the trade plays out.
4. **Makes sense**: Buy low when volume spikes, sell when the bounce is done. Logical.

### The Not-So-Good Stuff ⚠️

1. **Price filter might miss stuff**: That 0.000002 cutoff might exclude some good low-priced coins.
2. **Volume requirement is strict**: 4x is A LOT. Might miss opportunities where volume is only 2-3x.
3. **Trailing stop is tight**: 1% activation, 2% trail might get you stopped out on normal wiggles.
4. **No extra protections**: Just the hard stop loss. No special safety nets.

---

## When to Use It

| Market Situation | Should You Use It? | Why |
|-----------------|-------------------|-----|
| Coin suddenly pumps on huge volume | ✅ YES! | This is exactly what it's built for |
| Choppy market with volume spikes | ✅ Probably | Good opportunities here |
| Steady uptrend | ❌ NO | Price won't be below the MA |
| Dead quiet market | ❌ NO | No volume spikes = no signals |

---

## Real Talk: What You Need to Know

### It's a "Smart Money Follower" Strategy

This strategy doesn't try to be clever. It just watches for when the big players make their move, then follows them.

**Capital tip**: This can run on more coins than mark_strat_opt since signals are more frequent. Maybe 20-30% of your portfolio.

### The Fisher RSI Thing

Fisher RSI sounds fancy, but here's what it does:
- Normal RSI: "Hmm, maybe oversold at 25"
- Fisher RSI: "OVERSOLD AT 3. BUY NOW!"

It takes the RSI and stretches it mathematically so extreme values are MORE extreme. Makes signals clearer.

### Hardware You'll Need

| How Many Coins | Minimum RAM | Recommended RAM |
|---------------|-------------|-----------------|
| 1-10 coins | 4GB | 8GB |
| 11-30 coins | 8GB | 16GB |
| 30+ coins | 16GB | 32GB |

### Backtest vs. Reality

- **Volume lag**: In backtest, volume is known. In real life, volume builds over the candle. You might enter late.
- **Price filter drift**: A coin at 0.0000019 today might be at 0.0000021 tomorrow. Your filter might randomly exclude it.
- **Over-optimized numbers**: That Fisher RSI value of 38.900000000000006? Yeah, that's suspiciously precise. Might not hold up.

---

## For Manual Traders

If you're not running this on a bot:

1. **Watch for volume spikes**: Set a volume alert for 3-4x average. When it fires, look at the chart.
2. **Check if price is below MA**: Make sure you're buying at a discount, not chasing.
3. **Use Fisher RSI < 39 as a guide**: When you see that, the coin is probably oversold.
4. **Wait for the stochastic cross**: Don't jump in early. Wait for FastD to cross above FastK.

---

## The Bottom Line

**quantumfirst** is for traders who want to follow smart money into oversold bounces. It's more active than mark_strat_opt, with more frequent signals.

**Think of it like**: Surfing — you wait for the big wave (volume spike), then ride it to shore.

**Best for**: 
- Medium-volatility coins
- Traders who want regular action (not waiting days for signals)
- Markets with clear volume patterns

**Not for**:
- Super low-volume coins (signals will be unreliable)
- Strong bull markets (price won't be below MA)
- People who hate checking volume charts

---

## Quick Reference Card

```
BUY WHEN:
✓ Price > 0.000002 (liquidity filter)
✓ Volume > 4x 200-period average (BIG MONEY!)
✓ Price < 40-period SMA (on sale)
✓ FastD > FastK (momentum crossing up)
✓ Fisher RSI < 38.9 (oversold)

SELL WHEN:
✓ RSI crosses above 50 + MACD < 0
✓ OR SAR > price + Fisher RSI > 0.3
✓ OR ROI hits target
✓ OR trailing stop activates

PROFIT TARGETS:
• Immediate: 5%
• 20 min: 4%
• 40 min: 3%
• 80 min: 2%
• 24 hours: 1%

STOP LOSS:
• Hard: -10%
• Trailing: Activates at +1%, trails 2%
```

---

## mark_strat_opt vs. quantumfirst: Which One?

Since you're translating both, here's a quick comparison:

| Feature | mark_strat_opt | quantumfirst |
|---------|---------------|--------------|
| **Speed** | 1-minute (fast) | 5-minute (medium) |
| **Signal frequency** | Very rare | Moderate |
| **Key signal** | 5 indicators all extreme | Volume 4x + oversold |
| **Stop loss** | -20% (wide) | -10% (moderate) |
| **Best market** | Extreme crashes | Volume-driven bounces |
| **Personality** | Sniper (wait, one shot) | Surfer (wait for wave, ride it) |

**Use both**: They complement each other. mark_strat_opt catches the rare big crashes, quantumfirst catches the regular volume-driven bounces.

---

**Remember**: This strategy needs volume to work. No volume = no signals. Make sure you're trading coins with decent liquidity.
