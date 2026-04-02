# Cluc7werk Strategy: The Aggressive "Lightning Hunter"

> **Nickname**: Lightning Hunter, Ten-Minute Sniper, Daredevil Captain
> **Profession**: Ultra short-term trader; professional bottom-caller
> **Timeframe**: 1 Minute (so fast it'll make you doubt人生)

---

## 1. What's This Strategy All About?

Simply put, **Cluc7werk** is a strategy that:
- Uses **Fisher RSI** to judge whether it's crashed enough
- When crashed, uses **Bollinger Bands** to find bottom-call opportunities
- Target profit **10%**; dares to dream big
- Stop-loss **-10%**; cuts losses fast

Think of it like a **scalper waiting at the hospital emergency room** — sees someone in an accident (crashed hard) and rushes in to捡便宜 goods, then resells. But the question is: how fast does the ambulance come? 🤔

---

## 2. Core Settings: Basically "Greedy AND Cowardly"

### Take-Profit Rule (ROI Table)

```
0 minutes     → Make 10% and run (wishful thinking!)
60 minutes   → Make 7% and run (acceptable)
120 minutes  → Make 5% and run (getting anxious)
240 minutes  → Make 3% and run (算了, whatever)
```

**Translation**: This strategy dreams of making 10% the moment it enters, like walking into a casino wanting big wins. But if luck doesn't hold, after 4 hours making 3% is acceptable. Eh.

### Stop-Loss Rule

```
Hard stop-loss: -10% (cut losses at 10%)
Trailing stop: activates at 1% profit, locks at 1.26%, exits on 1% pullback
```

**Translation**:
- Cut losses at 10%; don't drag
- Starts protecting once making 1%; locks stop when making 1.26%

**Gripe**: Strategy's target profit and stop-loss are symmetric — make 10% or lose 10%. Like gambling: either double or zero; exciting!

### Position Management

```
Maximum 5 simultaneous positions
```

**Translation**: Don't put all eggs in one basket; max 5 baskets.

---

## 3. Two Entry Conditions: Only Buy When Crashed Hard

This strategy's entry logic is simple: **only considers buying when crashed to the point mom doesn't recognize**. Specifically 2 modes:

### 🎯 Mode 1: BB Rebound (Good for sharp drop reversals)

**Core Logic**: Price breaks BB lower band but quickly bounces back — "false breakout"!

**Plain English**:
> "I thought it'd die, but it poked down then bounced right back; lower shadow short — this is deception!"

**Condition breakdown**:

| Condition | Value | Plain English |
|-----------|-------|---------------|
| BB width | > 0.732% | BB must be wide enough; can't be flat |
| Close change | > 1.825% | Must have obvious volatility; no boring stuff |
| Lower shadow | < 94.138% | Lower shadow must be short |
| Close position | < previous lower band | Must be "breakdown" pattern |
| Trend confirmation | ≤ previous close | Confirm still weak |

**Visual**: Price dives like跳水 then bounces right back; leaves just a short "needle." That's the opportunity!

---

### 📉 Mode 2: EMA Volume-Shrinking Pullback (Good for slow bleed stabilization)

**Core Logic**: Price is below long-term MA, breaks BB, and volume shrinks — nobody wants to sell!

**Plain English**:
> "Price fell all the way down; MAs压在头顶上; BB can't hold either, but volume getting smaller and smaller — dried up! Time to rebound!"

**Condition breakdown**:

| Condition | Value | Plain English |
|-----------|-------|---------------|
| Price position | < 48 EMA | Below long-term MA (weak zone) |
| Break level | < BB lower × 1.99% | Broke through BB |
| Volume | < 24 avg × 16 | Volume shrunk to floor |

**Visual**: Price like water slowly draining; only a few drops left (volume shrinks); time to rebound.

---

### 🔑 Gate Condition: Fisher RSI Must < -0.22987

This is the **mandatory prerequisite**!

**What's Fisher RSI?**
- Transforms ordinary RSI; values from 0-100 become -1 to 1
- **Below -0.23 ≈ RSI below 38** = oversold zone
- **Above 0.27 ≈ RSI above 63** = overbought zone

**Plain English**:
> "Only considers buying when crashed so hard your face turns green (RSI < 38); runs when risen so red it's glowing (RSI > 63)!"

---

## 4. Protection Mechanisms: Four "Fuses"

This strategy may seem aggressive, but has plenty of fuses:

| Protection Layer | Mechanism | Plain English |
|-----------------|-----------|---------------|
| Layer 1 | Fisher RSI filter | "Won't buy unless crashed hard enough" |
| Layer 2 | Dual modes complement | Both modes must satisfy before buying |
| Layer 3 | Hard stop-loss -10% | "Cut losses at 10%; don't hold" |
| Layer 4 | Trailing stop | "Start protecting once making 1%; lock when making 1.26%" |

**Gripe**: Strategy seems aggressive on surface but actually quite cowardly — cuts at 10% loss, starts protecting at 1% profit. But the problem is target profit is 10%; making 1% is just the beginning; may end up making just "fees" 🤣

---

## 5. Sell Logic: More Elaborate Than Entry

Sell must **simultaneously meet 4 conditions**:

| Condition | Value | Plain English |
|-----------|-------|---------------|
| Price position | ≥ 99.184% of BB middle | Price risen to BB middle |
| EMA direction | 6 EMA > close | Short-term MA turning down |
| Fisher RSI | > 0.26832 | Entered overbought zone |
| Volume | > 0 | Has volume; not garbage |

**Plain English**:
> "Risen to BB middle, MA starting to turn, already overbought — at this point don't you dare stay!"

**Gripe**: This sell condition is cleverly designed — needs price to reach position AND show weakness AND have overbought confirmation. Like **three people all nodding yes before leaving**.

---

## 6. Strategy "Personality"

### ✅ Strengths

1. **Clear target**: 10% profit; no nonsense
2. **Fast reaction**: Single signal buys; doesn't wait for consecutive confirmation
3. **Good protection**: 4-layer fuses; won't blindly lose
4. **Focus on oversold**: Only buys when crashed hard; has safety margin
5. **Simple parameters**: No multi-timeframe; just 1-minute

### ⚠️ Weaknesses

1. **Target too high**: 10% in single trades often unachievable; prone to "high open, low close"
2. **1-minute chart too short**: Noise so bad you'll question人生
3. **Single confirmation**: Unlike Cluc5werk needing 2 consecutive candles; may buy at mid-mountain
4. **Slippage killer**: Large volatility coins have big bid-ask spreads; actual profit eaten
5. **Psychological pressure**: Watching 1-minute charts; bad for心脏

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 High-volatility coins (meme coins) | ⭐⭐⭐⭐⭐ Strong recommend | Volatile enough; target profit achievable |
| 📉 Post-crash rebound | ⭐⭐⭐⭐☆ Recommend | Fisher RSI specializes in catching oversold |
| 🔄 Mild oscillation | ⭐⭐☆☆☆ Barely | Signals scarce; makes measly profits |
| 💀 Continuous bleed | ⭐☆☆☆☆ Don't use | Keeps buying, keeps losing |
| 🛑 Illiquid small coins | ❌ Don't touch | Slippage eats all profits |

---

## 8. Summary: What Do I Think?

### One-Line Verdict
> "Aggressive faction's conservative type; greedy ghost but scaredy-cat — wants 10% but starts protecting at 1% profit."

### Who's It For?
- ✅ Day-trading veterans (can monitor, fast reactions)
- ✅ Meme coin gamblers (volatile enough to satisfy appetite)
- ✅ People who can accept 10% stop-loss (strong psychology)
- ✅ People with time to watch charts (1-minute needs attention)

### Who's It NOT For?
- ❌ Office workers (no time to watch)
- ❌ Beginner newbies (1-minute charts will shatter心态)
- ❌ Conservative investors (this strategy too exciting)
- ❌ People who haven't backtested (don't live trade without testing)

### My Suggestions
1. **Paper trade first**: Run at least 1 month to see effects
2. **Pick volatile coins**: Bitcoin stable but not volatile enough; meme coins better
3. **Set stop-loss alerts**: 1-minute changes fast; need alerts when reaching stop-loss
4. **Don't change parameters**: These optimized; random changes cause problems

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Bottom-Call Rebounds

Cluc7werk's money-making philosophy is simple:

> "Buy when crashed hard; sell when risen; target 10%; stop at 10%."

**Its core skills**:

- **Oversold identification**: Uses Fisher RSI to precisely find "crashed hard" points
- **Pattern filter**: BB rebound + EMA volume-shrinking pullback dual modes
- **Fast entry/exit**: 1-minute chart; catch rebounds and run

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English |
|:---|:---|:---|
| 📈 Big surge then crash rebound | ⭐⭐⭐⭐⭐ | Its home turf! Crash means Fisher RSI must be oversold |
| 🔄 Mild oscillation | ⭐⭐☆☆☆ | Signals scarce; mostly waiting |
| 📉 Continuous bleed | ⭐☆☆☆☆ | Buy and keep bleeding; consecutive stops |
| ⚡️ Wild surge | ❌ Don't use | No oversold signals at all |
| 💀 Dead market | ❌ Don't use | Fisher RSI stuck in middle; nothing triggers |

**Bottom Line**: **This strategy designed specifically for "crash then rebound" markets; don't force it in other conditions.**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Suggested | Note |
|------------|-----------|------|
| Timeframe | 1 minute | Don't change to other; will break |
| Max positions | 5 | Default fine |
| Stop-loss | -10% | Can widen to -15% if brave |
| First target | 10% | Too high? Can lower to 5% |

### 10.2 Hardware Requirements (Important!)

Strategy uses 1-minute charts; system requirements:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|----------------|------------|
| 1-5 pairs | 2GB | 4GB | Normal |
| 5-20 pairs | 4GB | 8GB | Smooth |
| 20+ pairs | 8GB | 16GB | Need good config |

**Warning**: 1-minute data volume large; too many pairs will lag! 😅

### 10.3 Backtesting vs Live Trading

Backtesting may look great; live needs discount:

- **Slippage**: Large volatility coins bid-ask spreads large; actual profit eaten 1-2%
- **Execution delay**: 1-minute changes fast; from signal to execution price may have risen
- **Emotion swings**: Watching account fluctuate; prone to manual interference

**Recommended Process**:
1. Backtest 3 months of historical data
2. Paper trade 1 month
3. Small-capital live 1 month
4. Confirm stability then add capital

**Don't go all-in right away**, strategy needs磨合!

---

## 11. Easter Egg: Strategy Author's "Little Tricks"

Looking closely at the code, you'll find interesting things:

1. **Fisher RSI is premium**: Not ordinary RSI; mathematically transformed; signals more stable
   > "Author clearly a tech geek; likes using premium indicators"

2. **Parameters all to 5 decimal places**: Indicates大量 backtesting optimization
   > "Like `fisher: -0.22987`; not randomly set"

3. **Target profit 10% vs stop-loss 10%**: Interesting symmetric design
   > "Either make 10% or lose 10%; author a symmetry obsessive?"

4. **Dual entry modes**: BB rebound + EMA volume-shrinking; covers two scenarios
   > "Author afraid single mode misses opportunities; designed two entry positions"

5. **Low-threshold trailing stop**: Starts protecting once making 1%
   > "Author actually scared of losing; protects profit at slightest gain"

---

## 12. The Final Word

### One-Line Verdict
> "Cluc7werk is a敢想敢干 but 手心出汗 strategy — 10% target attractive, but 1-minute charts will teach you a lesson."

### Who's It For?
- ✅ Experienced day traders
- ✅ People trading high-volatility coins
- ✅ People who can accept symmetric risk (make 10% or lose 10%)
- ✅ People with time to watch charts

### Who's It NOT For?
- ❌ Beginner newbies
- ❌ Office workers (no time to watch)
- ❌ Conservative people
- ❌ People with weak hearts

### Manual Trading Suggestions

If not running with a bot but manually trading:

1. **Set price alerts**: Alert yourself at key levels
2. **Pre-draw support/resistance**: Know roughly where it'll rebound to
3. **Strict stop-loss**: Cut at 10% no matter what; don't hold
4. **Don't be greedy**: Consider selling when near BB middle

---

## 13. ⚠️ Risk Reminder (Must Read This Section)

### Backtesting Looks Good; Live Requires Caution

Cluc7werk's historical backtesting may **look tempting** — but there's a trap:

> **Because target is 10%, strategy easily "wins small, loses big" — most times making 3-5% and selling, occasionally losing 10%.**

Simply: **Makes not enough when winning; loses it all when losing.**

### Hidden Risks of Complex Strategies

Live, complex logic may cause:

- **Missed signals**: 1-minute changes fast; from signal to order price may have risen
- **Slippage eating profits**: Large volatility coins bid-ask spreads large; 3% profit may shrink to 1%
- **Fee killer**: Frequent trading fees not few; profits eaten
- **Emotion interference**: Watching account fluctuate; prone to manual interference

### My Suggestions (From the Heart)

```
1. Paper trade at least 1 month; see actual effects
2. Pick liquid mainstream coin pairs; avoid small coins
3. Target profit can lower to 5%; don't be too greedy
4. Stop-loss can widen to -15%; give yourself some room
5. Don't change parameters! These optimized
```

**Remember**:

- Strategy is dead; market is alive
- 10% target doesn't mean every trade makes 10%
- 1-minute noise lots; don't be fooled by fake signals
- Test with small positions; survival matters! 🙏

---

**Final Reminder**: No matter how good the strategy, the market doesn't care. Test with small positions; survival matters most! 🎯
