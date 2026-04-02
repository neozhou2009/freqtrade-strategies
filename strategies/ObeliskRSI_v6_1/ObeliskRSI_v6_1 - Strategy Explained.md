# ObeliskRSI_v6_1: Plain English Breakdown

## 1. What Is This Strategy?

**Simple answer**: It's a **"buy the dip" strategy**.

Core idea: When prices fall hard, buy. When they bounce back, sell and take profits. Like shopping at a supermarket sale — buy when it's discounted, sell when prices return to normal.

The strategy uses RSI to judge when things are "on sale" (oversold) and when they're "back to normal" (overbought). RSI is like a thermometer — tells you if the market is "cold" (oversold) or "hot" (overbought).

"RSI" in the name = the core indicator. "v6.1" = version 6, first improvement. Released March 2021.

---

## 2. What Is RSI?

RSI stands for "Relative Strength Index." It scores prices from 0 to 100.

Think of it this way: watch a product's price changes. If it's been rising more often and by more, RSI goes high. If falling more often and by more, RSI goes low.

- Near 0: fell too much → might bounce
- Near 100: rose too much → might pull back
- Around 50: bulls and bears roughly equal

**Traditional rules**: RSI < 30 = oversold; RSI > 70 = overbought.

This strategy doesn't use those exact numbers — it tuned its own.

---

## 3. Buy and Sell Rules

### Buy Rules: Be Greedy When Others Are Fearful

The strategy buys when RSI drops below a threshold. But the threshold changes based on whether we're in a bull or bear market:

**Bull Market (market is strong overall)**:
- RSI drops below 35 → **BUY**

**Bear Market (market is weak)**:
- RSI drops below 21 → **BUY**

Why the difference? Because in bull markets, pullbacks are gentle — price won't fall as far before bouncing. Set the bar higher (35) to catch more buy opportunities. In bear markets, drops are brutal — set the bar much lower (21) to avoid catching falling knives.

### Sell Rules: Take Profits, Don't Be Greedy

**Bull Market**: RSI rises above 69 → **SELL**
**Bear Market**: RSI rises above 55 → **SELL**

Same philosophy: in bull markets let profits run longer (69 is high), in bear markets grab profits sooner (55 is lower).

---

## 4. How Does It Know Bull or Bear?

**The clever part**: the strategy figures out the market mode itself.

Here's how:
1. Take the 5-minute candle data, merge it into 1-hour chunks
2. Calculate RSI on those 1-hour chunks
3. If this long-period RSI > 60 → **BULL MARKET MODE**
4. If not → **BEAR MARKET MODE**

**Plain English analogy**: 5-minute RSI = today's weather; 1-hour RSI = the season. The season affects what you do today. If it's summer (bull), you tolerate some clouds (moderate pullback). If it's winter (bear), you need it to be really cold (extreme oversold) before you buy.

This prevents getting fooled by short-term moves. Price might dip for a minute, but if the season (long-term trend) is still up, the strategy considers it a bull market pullback and may buy.

---

## 5. When to Take Profits — ROI Mechanism

Knowing when to buy and sell is one thing, but knowing **how much to aim for** is another. This strategy has a carefully designed profit target system.

### Stepped Profit Targets

| Time Holding | Target Profit |
|-------------|--------------|
| Just bought | 15% |
| After 35 minutes | 4% |
| After 65 minutes | 1% |
| After 115 minutes | 0% (force exit) |

**What this means**:
- Jumped 15% right away → sell fast and lock it in
- Didn't jump that fast, held 35 min → as long as you have 4% profit, sell
- Held 65 min → even 1% is fine, just don't lose
- Held 115 min (~2 hours) → close no matter what, even at break-even

**Why this makes sense**: The longer you hold without making good profits, the more you wonder if this trade is any good. Better to close and move on than stay stuck waiting.

---

## 6. Stop-Loss — Dynamic and Smart

### The Usual Stop-Loss
A big safety net: **-30%**. If you lose 30%, it force-exits. This is the last resort.

### The Cool Part: Dynamic Stop-Loss
The stop-loss line isn't fixed — it **moves over time**:

Imagine you bought a stock:
- Right after buying, you're okay giving it some room — maybe it drops 10% and you don't panic
- But the longer you hold and it's still losing, you get more nervous
- Eventually you say "okay even flat or slightly negative, I'm out"

That's exactly what this dynamic stop does. It uses a math function called "ease-in cubic" to make the stop tighten slowly at first, then faster later.

- **Just opened**: stop at -30% — lots of room
- **As time passes**: stop line slowly rises
- **Around 110 minutes**: stop line near 0% — almost any loss triggers exit

This gives new positions time to develop while protecting older positions.

---

## 7. What Markets Does It Work In?

### Best: Ranging Markets
Price bouncing around in a range — up, down, up, down. This strategy shines here because price keeps returning to "oversold" and bouncing back — exactly what this strategy catches.

**Like fishing**: when water level (price) drops very low, you cast your net. When it rises back up, you pull in your catch.

### Not Great: One-Direction Bull Markets
You might think "strong uptrend = easy money!" But this strategy is a dip-buyer. If the market keeps going up without significant pullbacks:
- Strategy waits for a dip that never comes
- You watch others profit while you sit on the sidelines

**Like waiting for a sale that never comes**: You want to buy at a discount, but the store never discounts.

### Risky: Prolonged Falling Markets
If price keeps dropping, dropping, dropping:
- Strategy keeps buying at what looks like "oversold"
- Each time it drops further → gets stopped out
- Repeat → accumulates losses

**Like catching falling knives**: You think the knife has landed, but it keeps falling. Each time you try to catch it, it cuts you.

Author recommends: if a pair gets stopped out twice consecutively, pause trading that pair for a while.

---

## 8. What Pairs Work Best?

### Recommended
SXP, MATIC, SUSHI, CHZ

These are:
- High enough volume (easy to trade, low slippage)
- Good volatility (regular pullback opportunities)
- Not the absolute biggest (BTC, ETH too stable)

**Like choosing a fishing spot**: Want enough fish (volatility), clear water (liquidity), not too deep not too shallow.

### NOT Recommended: BTC and ETH

These are too stable! They don't drop/rise enough for this strategy:
- Pullbacks are too shallow — RSI doesn't get oversold enough
- Even when you buy, the gains aren't big enough to hit profit targets

**Like trying to fish in a bathtub**: There's no fish!

---

## 9. Risks to Watch

### Risk 1: Catching Falling Knives
Biggest risk. RSI says "oversold" but price keeps falling. You buy, it drops more. That's the price of left-side trading.

### Risk 2: Missing Strong Trends
In a sustained uptrend, you wait for pullbacks that don't come. You miss the whole move.

### Risk 3: Consecutive Stop-Outs
In a falling market, might buy → stop → buy → stop → buy → stop. Without the protection mechanism, losses accumulate.

### Risk 4: Slippage
Signal says buy at $100, but by the time your order fills, price is $101. Backtesting doesn't capture this. Live is usually worse.

### Risk 5: Fees
Every trade costs fees. High-frequency strategies especially feel this. This strategy's frequency is moderate, but still watch it.

### Risk 6: Wrong Pair Selection
If you pick a bad pair (like BTC for this strategy), it may barely trade or perform poorly.

---

## 10. How to Use This Well

### Step 1: Pick the Right Pairs
Per author: high volatility, high liquidity. SXP, MATIC, SUSHI, CHZ recommended. Avoid BTC/ETH.

### Step 2: Set Up Protections
Add the consecutive loss guard:
```json
"protections": [{"StoplossGuard": lookback 720, trade_limit 2, stop_duration 720}]
```
This pauses a pair after 2 consecutive stop-outs — prevents catching knives repeatedly.

### Step 3: Position Sizing
Don't bet everything on one pair. Suggested:
- Max 5-10% per pair
- Run 5-10 pairs at once
- Keep reserve cash

### Step 4: Paper Trade First
At least 1-2 weeks in paper trading through different market conditions.

### Step 5: Regular Check-Ins
Daily log review, weekly summary, monthly evaluation. If 5+ consecutive losses on any pair, something may be wrong.

---

## 11. Parameter Tuning

### Buy Thresholds
- `bull-buy-rsi-value` (default 35): Higher = more aggressive (buy earlier, more chances)
- `bear-buy-rsi-value` (default 21): Higher = more aggressive

### Sell Thresholds
- `bull-sell-rsi-value` (default 69): Higher = hold longer for bigger gains
- `bear-sell-rsi-value` (default 55): Higher = hold longer

### Stop Time
- `custom_stop_ramp_minutes` (default 110): Higher = more patient, longer to force exit

### Tuning Tips
Don't tune too aggressively:
- Each change needs re-validation
- "Perfect" history parameters often don't work in the future
- Check quarterly, only change if long-term performance clearly deteriorated

---

## 12. Pros and Cons Summary

### Pros
1. **Clear logic**: Simple dip-buying — easy to understand
2. **Adapts to market**: Bull/bear modes use different parameters
3. **Risk-controlled**: Stop-loss, dynamic stop, time limit — won't get trapped forever
4. **Good for volatile pairs**: RSI bounces create real opportunities

### Cons
1. **Bad for trending markets**: Long uptrends = no trades; long downtrends = getting stopped out
2. **Parameter-sensitive**: Different pairs/seasons need different settings
3. **Backtest looks better than live**: Slippage and delays hurt real performance
4. **Left-side risk**: Buying before confirmation means sometimes catching knives

### Who Is This For?
**YES if**: experienced quant trader, can handle some risk, willing to learn and optimize, understand crypto markets

**NO if**: complete beginner, want steady returns, can't watch/adjust regularly, can't handle 30% drawdown

---

## 13. Final Thoughts

ObeliskRSI_v6_1 is a well-designed strategy — clean code, clear logic. It doesn't pile on dozens of indicators; it focuses on doing one thing well: using RSI to spot oversold dips and catch the bounces.

The author himself says "backtest looks better than live" and "I'm not sure what I'm doing" — refreshingly honest. It reminds us: no perfect strategy, just continuous learning.

**If you're a quant beginner**: this strategy is great for learning. Small codebase, but covers important concepts: multi-period analysis, dynamic parameters, stop-loss, profit targets, risk control. Study it and your quant knowledge jumps.

**If you want to use it live**:
1. Paper trade first
2. Pick right pairs
3. Set up protections
4. Control position size
5. Monitor regularly

Good luck!

---

*Strategy Author: Obelisk (brookmiles)*
*Document written by: AI Assistant*
*Disclaimer: Learning reference only, not investment advice. All investing has risk — be careful.*
