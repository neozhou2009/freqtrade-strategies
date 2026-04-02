# Chandem Strategy: Momentum Breakout + Bollinger Band Top-Catching

> **Nickname**: Momentum Hunter
> **Profession**: Trend-following trader specializing in catching the moment price "turns from falling to rising"
> **Timeframe**: 5 Minutes

---

## 1. What's This Strategy All About?

Simply put, **Chandem** is a strategy that:
- Uses CMO indicator to find the turning point where price "turns from falling to rising"
- Sells when price rises "too ridiculously" (Bollinger upper band)
- Aims for BIG money (28%!) but also allows BIG losses (28%!)

Think of it like a **patient hunter**:
- Lurking in the grass waiting for prey to appear (CMO crosses above zero)
- Pull in the net when prey runs too far (price breaks Bollinger upper band)
- Eat the meatiest middle section 🍖

**Bottom Line**:
> "Enter when trend starts, exit when price reaches extreme — simple and brutal but effective!"

---

## 2. Core Settings: Basically "Make 28% and Run, Lose 28% and Give Up"

### Take-Profit Rule (ROI Table)

```
0 minutes      → 28.4% profit → Run!
16 hours      → 9.3% profit  → Run!
29 hours      → 6.6% profit  → Run!
51 hours      → 0% profit    → Run! (break-even)
```

**Translation in plain English**:
> "I'm greedy when I first enter — want 28%! But as time passes, my standards drop. Held for almost 2 days and still haven't made money? Then just break even and leave. Stop wasting time."

**What's the design intent?**
- Pursue windfalls: Want 28% immediately upon entry
- Time cost: Longer you hold, lower your target
- Admit defeat: Held 51 hours without profit = close the position

### Stop-Loss Rule

```
Hard stop-loss = -28%
```

**Translation in plain English**:
> "Cut losses at 28%, don't argue with the market. Yeah it hurts, but those are the rules."

**Plain talk**: This strategy is "bold" — wants big wins and allows big losses. Can you handle it?

### Trailing Stop

```
Profit reaches 1.013%    → Activate trailing
Profit reaches 10.858%   → Lock in 9.8% profit
```

**Translation in plain English**:
> "Once profit exceeds 10%, I start watching. If it drops back, I run once I've locked in 9.8% — won't be greedy!"

---

## 3. One Buy Condition: CMO Crosses Above Zero

Don't be fooled by all the code — **there's really only ONE buy condition**!

```
CMO today >= 0   AND   CMO yesterday < 0
```

### 🎯 Buy Signal: Momentum Shifts from Bearish to Bullish

**Plain English**:
> "Yesterday still falling happily, today actually starts rising — that's the turning point I want! Enter!"

### What's CMO? (Plain English Version)

CMO (Chande Momentum Oscillator) = **Chande Momentum Oscillator**

Don't be scared by the name — it's basically:
- **Negative value**: Recent days fell more than rose → Downward momentum dominates
- **Positive value**: Recent days rose more than fell → Upward momentum dominates
- **Turns from negative to positive**: Momentum shifts from "falling" to "rising" → **Buy signal!**

### Why 50 Periods?

```
50 candles of 5 minutes = ~4 hours
```

This means CMO looks at the **past 4 hours** of overall momentum, not just a few minutes of short-term fluctuation, but the shift in medium-term trend.

**Plain English**:
> "I don't care what happened 5 minutes ago; I only care whether over the past 4 hours you've been rising or falling. Shifting from falling to rising? That's my entry point!"

---

## 4. Protection Mechanisms: Three Layers of "Armor"

Chandem has **3 layers of protection** — greedy but also scared:

| Protection Layer | Trigger | Plain English |
|-----------------|---------|---------------|
| 🛡️ **Layer 1**: ROI take-profit | Profit reaches target (28%/9%/6%...) | "Made the target, leave, no clinging" |
| 🛡️ **Layer 2**: Trailing stop | Profit >= 10.858% then pulls back | "Made enough, lock in profits, won't let them go" |
| 🛡️ **Layer 3**: Hard stop-loss | Loss >= 28% | "Too painful, admit defeat" |

**Plain English summary**:
> "I allow you to make big money (28%), but you must allow me to lose big money (28%). If you make 10%, I'll start watching; once you've made less, I leave — greedy but protective!"

---

## 5. Sell Logic: Run When Price "Rises Too Ridiculously"

### Sell Condition: Price Breaks Bollinger Upper Band

```
Close price crosses above Bollinger upper band
```

**Plain English**:
> "Price rose to Bollinger's 'ceiling'! This means price has gotten 'too ridiculous' — Run!"

### What's a Bollinger Band? (Plain English Version)

**Bollinger Band** = The price's "track" or "corridor"

```
───────────── Upper band (ceiling) ← Rise to here = "too ridiculous"
      ↕ 股价
───────────── Middle band (average price)
      ↕ 股价
───────────── Lower band (floor)
```

- **Middle band**: Average price of the past 25 candles
- **Upper/Lower bands**: Middle ± 3.5x standard deviation
- **3.5x standard deviation**: Wider than normal 2x — only triggers when risen "especially ridiculously"

**Plain English**:
> "Normal Bollinger Bands are too sensitive; rise a little and you hit the upper band. I use 3.5σ to widen the track — only sell when risen 'absolutely nuts'! Eat the meatiest middle section!"

### The Art of Sell Timing

This strategy's sell logic is actually quite clever:

1. **Buy timing**: CMO crosses from negative to positive → Trend just starting
2. **Sell timing**: Price breaks Bollinger upper band → Trend nearing end

**Plain English**:
> "I'm a fish-body eater — don't eat the fish head (before trend starts) or fish tail (before trend ends); only eat the meatiest middle!"

---

## 6. Strategy "Personality"

### ✅ Strengths

| Strength | Description |
|---------|-------------|
| 🎯 **Concise signals** | 1 buy condition, 1 sell condition; crystal clear |
| 🧠 **Direct logic** | CMO cross above to buy; Bollinger upper band to sell; no tricks |
| 💪 **Strong resilience** | 28% stop-loss; gives price ample room to fluctuate |
| 🔒 **Disciplined** | Once trailing stop activates, won't be greedy |
| 🍖 **Pursues windfalls** | 28% ROI target; not one of those strategies that sells at 2% |

### ⚠️ Weaknesses

| Weakness | Description |
|---------|-------------|
| 💀 **Stop-loss too wide** | -28% stop-loss; single trade loss can be significant |
| 🎲 **High-risk, high-reward style** | High ROI + high stop-loss; completely high-risk high-reward style |
| 🚫 **No trend filter** | No MA trend confirmation; may buy counter-trend |
| 🚫 **No volume confirmation** | Signals don't verify volume; may be false breakouts |
| 😵 **May get chopped by ranging markets** | CMO oscillates around zero; frequent whipsaws |

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 **Uptrend** | ✅ Use boldly | CMO cross + Bollinger upper band; perfectly captures entire trend |
| 🔄 **Ranging Market** | ⚠️ Use carefully | Signals frequent; may get whipped both ways |
| 📉 **Downtrend** | ❌ Don't use | Counter-trend buy; easily buried |
| ⚡ **Extreme Volatility** | ⚠️ Tune parameters | Need CMO and Bollinger parameter adjustments |

**Plain English**:
> "This strategy is a trend trader's best friend; don't use it in ranging or downtrend markets — it'll teach you a lesson."

---

## 8. Summary: What Do I Think?

### One-Line Verdict
> "Simple, brutal momentum strategy — when trends come, eat big; when trends turn, admit defeat."

### Who's It For?
- ✅ Traders pursuing high returns who can handle large drawdowns
- ✅ Traders with patience to hold for hours to days
- ✅ People who believe in momentum indicators and like trend-following
- ✅ People who can accept 28% stop-loss "gambler's mindset"

### Who's It NOT For?
- ❌ People with small capital who can't absorb 28% loss
- ❌ People who like fast entry/exit and can't hold positions
- ❌ Conservative traders who panic at losses
- ❌ People who want "steady money with no risk" (doesn't exist!)

### My Suggestions
1. **Test on paper trading first**: Run at least 2 weeks to see effects
2. **Adjust stop-loss**: If you can't stomach 28%, change to 15-20%
3. **Add volume filter**: Manually confirm volume expands on entry
4. **Combine with trend**: Add an MA200 to confirm overall trend direction

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Capture the Trend's "Fish Body"

Chandem is a **momentum breakout strategy**, with a simple money-making philosophy:

> "Board the bus when the trend just starts, get off when price reaches extreme — eat the meatiest middle section!"

- **Boarding signal**: CMO turns from negative to positive = momentum shifts from bearish to bullish
- **Disembarking signal**: Price breaks Bollinger upper band = price has reached extreme

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English Explanation |
|:---|:---|:---|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | "Trend arrives, board it; rises wildly, run away; perfectly ate the fish body!" |
| 🔄 Ranging Market | ⭐⭐⭐☆☆ | "CMO oscillates around zero; buy-sell-buy-sell all fees." |
| 📉 Downtrend | ⭐⭐☆☆☆ | "Counter-trend buy; 'caught bottom at mid-mountain.'" |
| ⚡ Extreme Volatility | ⭐⭐⭐⭐☆ | "CMO sensitivity sufficient; can catch big moves." |

**Bottom Line**:
> "A friend of trend players, enemy of ranging markets."

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Suggested | Note |
|------------|-----------|------|
| Trading pairs | High-liquidity trending coins | "Don't test with those meme coins!" |
| Timeframe | 5 minutes | "Keep defaults; don't change" |
| Fees | < 0.1% | "High fees eat into profits" |

### 10.2 Parameter Tuning

| Parameter | Default | When to Adjust | How to Adjust |
|-----------|---------|----------------|---------------|
| CMO period | 50 | High volatility → reduce; Low volatility → increase | Adjust between 30-80 |
| Bollinger period | 25 | Strong trend → reduce; Ranging → increase | Adjust between 20-30 |
| Bollinger std dev | 3.5 | High volatility → increase; Low volatility → reduce | Adjust between 3.0-4.5 |

### 10.3 Hardware Requirements

This strategy's computation is light; ordinary VPS can run it:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|----------------|-------------|
| 5-10 pairs | 1 GB | 2 GB | Smooth |
| 20-30 pairs | 2 GB | 4 GB | Smooth |

**Warning**: 5-minute framework signal frequency is moderate; doesn't need fancy hardware 😅

### 10.4 Backtesting vs Live Trading

**Backtesting looks great; live requires caution**:

- Backtesting has no slippage; live does
- Backtesting assumes fills; live may have order failures
- Backtesting doesn't "teach you a lesson"; live does

**Recommended Process**:
1. Backtest first to see if parameters are reasonable
2. Paper trade for at least 2 weeks
3. Confirm strategy suits your style
4. Small-capital live test
5. Gradually increase position

**Don't go all-in right away**, even good strategies need a磨合 period!

---

## 11. Easter Egg: Strategy Author's "Little Tricks"

Looking closely at the code, you'll find some interesting things:

### 1. Why Use "Typical Price" for Bollinger Bands?

```python
typical_price = (High + Low + Close) / 3
```

**Plain English**:
> "I don't only look at close price; I also consider high and low. Because when price fluctuates wildly, close price may mislead — 'average price' is more reliable!"

### 2. Why ROI Is Weird (28.396%)?

**Plain English**:
> "These numbers are 'optimal solutions' from backtesting optimization. Don't ask why it's 28.396%; ask 'historically optimal' — but history doesn't guarantee future!"

### 3. Trailing Stop's Precise Decimals (10.858%)

**Plain English**:
> "Precise to 3 decimal places; shows these parameters were carefully tuned. But honestly, 10.8% and 10.9% make little difference — don't overthink it."

---

## 12. The Final Word

### One-Line Verdict
> "Chandem is a simple, brutal but effective momentum strategy — eat when trends come, admit defeat when trends turn."

### Who's It For?
- ✅ Aggressive traders who can handle large drawdowns
- ✅ Trend-following traders who believe in momentum
- ✅ Traders with patience to hold positions
- ✅ People willing to spend time tuning parameters

### Who's It NOT For?
- ❌ Conservative traders
- ❌ People who want "steady money with no risk"
- ❌ People with small capital who can't absorb 28% loss
- ❌ People without patience who like fast entry/exit

### Manual Trading Suggestions

If you want to manually use this strategy's logic:

1. **Monitor CMO**: Use TradingView to watch 50-period CMO
2. **Wait for cross signal**: Prepare to enter when CMO turns from negative to positive
3. **Confirm trend**: Ideally MA200 is upward; avoid counter-trend
4. **Check volume**: Volume expansion on entry is more reliable
5. **Set stop-loss and take-profit**: Adjust based on your risk tolerance

---

## 13. ⚠️ Risk Reminder (Must Read This Section)

### Backtesting Looks Good; Live Requires Caution

Chandem's historical backtesting may look **decent** — but there's a trap:

> **Because parameters were optimized, the strategy easily "fits" past market conditions, but doesn't guarantee future profitability.**

Simply put: **"Memorizing answers" and "knowing how to solve problems" are different things!**

### Hidden Risks of Complex Strategies

Live, pay attention to:

- **Wide stop-loss risk**: 28% stop-loss means single trade loss can be significant
- **Counter-trend risk**: No trend filter; may catch "falling knife at mid-mountain"
- **False breakout risk**: No volume confirmation; may be fake signals
- **Parameter sensitivity**: CMO period and Bollinger parameters significantly impact results

### My Suggestions (From the Heart)

```
1. Paper trade for at least 2 weeks; see if strategy suits your style
2. Adjust stop-loss to a range you can handle (e.g., -15% to -20%)
3. Add trend confirmation (e.g., MA200 or EMA trend)
4. Add volume filter (volume expansion on entry)
5. Start with small capital; gradually increase
```

### Special Reminder

⚠️ **28% stop-loss is no joke!**

If you have 10,000 U:
- Lose 28% = lose 2,800 U
- Consecutive 3 losses = lose 8,400 U
- You only have 1,600 U left……

**Remember**: No matter how good a strategy is, the market doesn't care. Test with small positions; survival matters most! 🙏

---

**Final Words**: Chandem is a simple, effective momentum strategy, but its risk-return profile requires your own judgment. If you can handle 28% stop-loss and believe in momentum indicators, try it — but paper trade first!
