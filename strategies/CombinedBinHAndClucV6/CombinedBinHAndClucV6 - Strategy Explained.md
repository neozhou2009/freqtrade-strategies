# CombinedBinHAndClucV6 Strategy Explained: Bollinger Band Double-Knife, Ultimate Greed Edition

> **Nickname**: Bollinger Band Double-Knife · Ultimate Greed Edition  
> **Profession**: Oversold Rebound Expert (Trend-Full-Bandit + Anti-Chase)  
> **Timeframe**: 5 Minutes (5m)

---

## 1. What's This Strategy?

**CombinedBinHAndClucV6** is the **Ultimate Greed Edition** of the "double-knife" oversold rebound strategy:

- Merged from two classics: **BinHV45** + **ClucMay72018**
- Each has its own move—buy if either triggers
- Catches opportunities where price "drops too much and bounces back"

**V6 vs V5 Core Upgrades**:
- Higher take-profit (2.0% → 2.2%): Want more
- Trailing stop later (2.75% → 3.0%): Let trends run further
- Trailing stop more tolerant (pullback 1.25% → 1.5%): Don't get shaken
- Stricter exits (6 → 7 candles): Fewer false breakouts
- **New EMA200 trend filter**: Prevents chasing highs, only enters at reasonable levels

Like a fisherman with two nets who also learned to check the weather—won't cast nets in a storm (high prices), only when seas are calm (near the moving average). 🐟

---

## 2. Core Settings: "Greedier, more tolerant, won't chase highs"

### Take-Profit Rule

```
Cumulative return ≥ 2.2% → Take-profit triggered
```

**Translation**: Grab 2.2% and run, 0.2% more than V5. Every bit counts!

### Stop-Loss Rules

```
Fixed stop-loss: -99% (almost no limit)
Trailing stop: Activates after 3.0% profit, protects 1.5% of gains
Time stop-loss: Force exit if still in loss after 5 hours
```

---

## 3. 2 Entry Sets + 1 Filter: Here's the Breakdown

### 🎯 Set 1: BinHV45 Style (Rapid Sell-off Rebound)

**Core Logic**: Price suddenly crashes, breaks below the lower Bollinger Band, but can't drop more—bottom fishing!

**One-liner**: Price rapidly pierces the lower Bollinger Band with a short wick and high volatility—classic "last drop."

| Condition | Plain Translation |
|-----------|-----------------|
| Previous day's lower Bollinger Band valid | Confirm it's not a calculation error |
| Bollinger Band width > 0.8% of price | Enough volatility, there's meat to eat |
| Closing price change > 1.75% | The day really crashed hard |
| Lower wick < 25% of channel width | Close near the low, hit bottom |
| Close < previous day's lower Bollinger Band | Broke below the rail |
| Close ≤ previous day's close | Continued dropping or flat |
| Volume > 0 | Exclude abnormal candles |

---

### 📉 Set 2: ClucMay72018 Style (Volume-Shrinking Oversold)

**Core Logic**: Price breaks below the lower Bollinger Band, but volume is abnormally low—selling pressure dried up.

**One-liner**: Price breaks below the lower Bollinger Band with shrinking volume in a downtrend—selling pressure exhausted.

| Condition | Plain Translation |
|-----------|-----------------|
| Close < 50-day moving average | Confirm medium-term downtrend |
| Close < 98.5% of Bollinger Band lower rail | Clearly broke below the rail |
| Volume < 20x the 30-day average | Volume abnormally shrunken |
| Volume > 0 | Exclude abnormal candles |

---

### 🛡️ V6 New: EMA200 Trend Filter

**Core Logic**: Price can't be too far from EMA200, prevents chasing rally highs.

**Plain English**:
> "Price has risen too far above the moving average? Nah, not chasing. Wait for it to pull back near the average—that's safer."

**Specifics**:
| Condition | Plain Translation |
|-----------|-----------------|
| Price < EMA200 × 1.05 | Price within 5% above EMA200 |
| Volume > 0 | Exclude abnormal candles |

**This is V6's exclusive feature**: Older versions might enter when price is already very high. V6 puts a guard here—won't buy if price has risen too much.

---

## 4. Protection Mechanisms: 4 Layers + 1 New Shield

| Protection | Trigger | Plain English |
|------------|---------|---------------|
| Fixed stop-loss | Loss 99% | Almost never triggers |
| Time stop-loss ⭐ | >5 hrs and losing | "5 hours and still losing? Done" |
| Trailing stop ⭐⭐ | Profit 3.0% then activates | "Up 3%, 1.5% pullback and I'm gone" |
| Sell only in profit | Sell signal triggers but losing | "No selling when losing" |
| EMA200 filter ⭐⭐⭐ | V6 new | "Too high? Not chasing, wait for pullback" |

⭐⭐ **V6 Core Changes**: Trailing stop raised from V5's 2.75% to 3.0%, pullback deepened from 1.25% to 1.5%. V6 is greedier—let trends run further!

⭐⭐⭐ **V6 Exclusive**: EMA200 trend filter is V6's new fuse—prevents buying at trend-end highs.

The 5 layers of protection: like wearing an invisibility cloak, helmet, hiring a bodyguard, AND the bodyguard watches the weather forecast—"don't go out in a storm!" 🛡️

---

## 5. Exit Logic

### 5.1 Take-Profit Exit
```
Cumulative return ≥ 2.2% → Sell
```
**Plain English**: Grab 2.2% and run. (0.2% more than V5)

### 5.2 Signal Exit ⭐V6 Key Change
When **7 consecutive 5-minute candles** (was 6 in V5) are above the upper rail, sell triggers.

### 5.3 Trailing Stop Trigger
**Plain English**: "Up 3%, watching. Drop 1.5% from high? Done. V6 more tolerant—small pullbacks don't scare me."

### 5.4 Time Stop-Loss Trigger
Still losing after 5 hours? Exit.

---

## 6. V6 vs V5 vs V4 vs V3: Evolution

| Setting | V3 | V4 | V5 | V6 | Impact |
|---------|-----|-----|-----|-----|--------|
| Take-profit | 1.8% | 1.9% | 2.0% | 2.2% | Gradually increasing |
| Stop-loss | -10% | -99% | -99% | -99% | V4 loosened |
| Trailing activation | 3% | 2.5% | 2.75% | 3.0% | V6 later, bolder |
| Trailing pullback | 1% | 1% | 1.25% | 1.5% | V6 deeper, more tolerant |
| Time stop-loss | 36 hrs | 5 hrs | 5 hrs | 5 hrs | V4 shortened |
| Exit confirmation | 4 candles | 5 candles | 6 candles | 7 candles | Gradually stricter |
| Trend filter | None | None | None | EMA200 | V6 new |

**V6 Summary**: V6 = V5 + greedier (2.2%, 3.0%/1.5%) + more cautious (7 candles) + smarter (EMA200 filter)

---

## 7. When to Use V6

| Market | Recommendation | Reason |
|--------|---------------|--------|
| Wide-range sideways | ✅ Heavy use | Price hits Bollinger rails repeatedly |
| High volatility | ✅ Suitable | Easy triggers |
| Rapid drop rebound | ✅ Perfect | BinHV45 tailor-made |
| Trend continuation ⭐ | ✅ V6 optimized | V6's loose trailing suits trends |
| Pullback entries ⭐⭐ | ✅ V6 new | EMA200 filter's specialty |
| One-directional rally | ⚠️ May sell out | V6 optimized but may miss |
| One-directional drop | ⚠️ Use carefully | -99% may hold large losses |
| Low-volatility | ❌ No signals | Too quiet |
| Strong breakouts | ⚠️ May miss | EMA200 filter may miss breakout entries |

---

## 8. V6's Exclusive Feature: EMA200 Trend Filter

V6's biggest change is the new EMA200 trend filter—its purpose:

**Problem**: Older versions might enter when price is already very high ("buying at the mountain top").

**Solution**:
- Before triggering buy, check if price is too far from EMA200
- If price exceeds EMA200's 105% (up 5%+), skip the buy
- Avoids "chasing" at trend ends

**Best Use Cases**:
- **Pullback entries (V6's favorite)**: Price went from 100 to 120, then pulled back to 110. EMA200 at ~105. Price 110 close to 105—good entry timing
- **Refusing to chase (V6's brake)**: Price rocketed from 100 to 150, EMA200 still at 110. Price 150 too far from 110—V6 refuses to buy

---

## 9. ⚠️ Risk Re-emphasis

> **V6's core philosophy: "Let profits run, but don't chase rally highs." The market won't warn you. Light positions—survival first! 🙏**

**Key V6 Risks vs V5**:
1. **Trailing stop activates later (3.0%)**: Good for trends, bad if it reverses at 2.8%
2. **Trailing stop more tolerant (1.5%)**: Good for staying in, may exit lower from peak
3. **7 candles for exit**: Fewer false breakouts, may miss optimal exit
4. **EMA200 filter may be conservative**: Strong trends may be missed

```
1. Judge market: Sideways or trend continuation; one-directional drop needs caution
2. Small capital testing first
3. Watch fees: Choose low-fee platforms
4. Manually add stop-loss: V6's -99% too loose, set 5%-10%
5. Use EMA200 well: V6's core feature—buy pullbacks near the average, don't chase
```

**Remember**: V6's tagline is "let profits run, don't chase highs." Survival first!
