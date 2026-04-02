# CombinedBinHAndClucV8 Strategy Explained: Bollinger Band Double-Knife, Wind-Chasing Wave-Riding Edition

> **Nickname**: Bollinger Band Double-Knife · Wind-Chasing Wave-Riding Edition  
> **Profession**: Oversold Rebound Expert (Trend-Full-Bandit + Volume-Confirmed + Smart Stop)  
> **Timeframe**: 5 Minutes (5m)

---

## 1. What's This Strategy?

**CombinedBinHAndClucV8** is the **Wind-Chasing Wave-Riding Edition** of the "double-knife" oversold rebound strategy:

- Merged from two classics: **BinHV45** + **ClucMay72018**
- Each has its own move—buy if either triggers
- Catches opportunities where price "drops too much and bounces back"

**V8 vs V7 Core Upgrades**:
- Higher take-profit (2.5% → 3.0%): Pursuing higher returns
- Trailing stop "bolder" (activation 3.5% → 4.0%, pullback 2.0% → 2.5%): Let profits run further
- Stricter exits (8 → 10 candles): Fewer false breakouts
- **New volume expansion confirmation**: V8 exclusive! Only confirms buys when volume expands, filters false breakouts
- **Time stop refined**: Loss-cutting 3 hours (faster), profitable <1.5% 8 hours (longer)

Like a fisherman who's greedier, bolder, AND learned to read the currents—won't catch volume-shrinking false rebounds, exits losing nets early, holds winning nets longer. 🐟

---

## 2. Core Settings: "Greedier, more tolerant, reads volume"

### Take-Profit Rule

```
Cumulative return ≥ 3.0% → Take-profit triggered
```

**Translation**: Grab 3.0% and run, 0.5% more than V7!

### Stop-Loss Rules

```
Fixed stop-loss: -99% (almost no limit)
Trailing stop: Activates after 4.0% profit, protects 2.5% of gains
Smart time stop-loss: V8 refined
  - In loss: Force exit after 3 hours (faster than V7)
  - Profitable but <1.5%: Force exit after 8 hours (longer than V7)
```

---

## 3. 4 Entry Sets + 1 Filter: Here's the Breakdown

### 🎯 Set 1: BinHV45 Style (Rapid Sell-off Rebound)
Price rapidly pierces the lower Bollinger Band with a short wick and high volatility—classic "last drop" pattern.

### 📉 Set 2: ClucMay72018 Style (Volume-Shrinking Oversold)
Price breaks below the lower Bollinger Band with shrinking volume—selling pressure exhausted.

### 📊 Set 3: V8 New Volume Expansion Confirmation (Core New Feature!)

**Core Logic**: Price dropped enough isn't enough—volume must expand too—confirms rebound authenticity.

**Plain English**:
> "Price hit the target? Volume expanded too? This is a real rebound, not a fake-out! V8 doesn't fall for false breakouts."

| Condition | Plain Translation |
|-----------|-----------------|
| Volume > previous candle's 1.2x | Volume expanded by at least 20% |
| Volume mean > 0 | Volume average is valid |
| Price < EMA200 × 1.05 | Price within 5% above EMA200 |
| Volume > 0 | Exclude abnormal candles |

**This is V8's core new feature**: Only confirms buys when volume expands, filters false breakouts. V7 didn't have this, V8 is exclusive!

### 🛡️ EMA200 Trend Filter
Price can't be too far from EMA200—won't buy if risen too much.

---

## 4. Protection Mechanisms: 4 Layers + 1 Refined Shield

| Protection | Trigger | Plain English |
|------------|---------|---------------|
| Fixed stop-loss | Loss 99% | Almost never triggers |
| Refined time stop ⭐⭐⭐ | V8 refined | "Losses in 3h, small profits in 8h" |
| Trailing stop ⭐⭐ | Profit 4.0% then activates | "Up 4%, 2.5% pullback and I'm gone" |
| Sell only in profit | Sell signal but losing | "No selling when losing" |
| EMA200 filter | V7/V8 retained | "Too high? Not chasing" |

⭐⭐⭐ **V8 Core Changes**: Trailing stop raised from V7's 3.5% to 4.0%, pullback deepened from 2.0% to 2.5%. Loss-cutting time shortened from 4h to 3h. Small-profit holding time extended from 6h to 8h.

---

## 5. Exit Logic

### 5.1 Take-Profit Exit
```
Cumulative return ≥ 3.0% → Sell
```
**Plain English**: Grab 3.0% and run.

### 5.2 Signal Exit ⭐V8 Key Change
When **10 consecutive 5-minute candles** (was 8 in V7) are above the upper rail, sell triggers.

### 5.3 Trailing Stop Trigger
**Plain English**: "Up 4%, watching. Drop 2.5% from high? Done. V8 more tolerant."

### 5.4 Refined Time Stop-Loss ⭐⭐⭐ V8 Refined Upgrade

**Losing state**:
> "3 hours and still losing? Done, next!" (V7 gave 4 hours)

**Profitable but <1.5%**:
> "8 hours and only up 0.8%? Not worth it." (V7 gave 6 hours)

**Profitable ≥1.5%**:
> "Continuing to hold."

---

## 6. V8 vs V7 vs V6 vs V5: Evolution

| Setting | V5 | V6 | V7 | V8 | Impact |
|---------|-----|-----|-----|-----|--------|
| Take-profit | 2.0% | 2.2% | 2.5% | 3.0% | Gradually increasing |
| Stop-loss | -99% | -99% | -99% | -99% | Unchanged |
| Trailing activation | 2.75% | 3.0% | 3.5% | 4.0% | V8 latest, boldest |
| Trailing pullback | 1.25% | 1.5% | 2.0% | 2.5% | V8 deepest, most tolerant |
| Time stop-loss | 5 hrs | 5 hrs | Smart | Refined | V8: loss 3h, small profit 8h |
| Exit confirmation | 6 candles | 7 candles | 8 candles | 10 candles | Gradually stricter |
| Trend filter | None | EMA200 | EMA200 | EMA200 | V6 new |
| Volume confirmation | None | None | None | V8 new | V8 exclusive |
| Profit offset | 0.1% | 0.1% | 0.1% | 0.2% | V8 higher, safer |

**V8 Summary**: V8 = V7 + greedier (3.0%, 4.0%/2.5%) + more cautious (10 candles) + smarter (refined time stop) + more reliable (volume confirmation)

---

## 7. V8's Exclusive Features

### Volume Expansion Confirmation
**Problem**: Older versions only checked if price broke below the lower band, didn't check volume.

**Solution**: New 3rd entry condition—only buys when volume expands ≥20%, confirming real rebounds vs false breakouts.

### Refined Time Stop-Loss
| Scenario | V7 | V8 | Change |
|----------|-----|-----|--------|
| Loss state | 4 hrs | 3 hrs | V8 faster, more decisive |
| Small profit | 6 hrs | 8 hrs | V8 more patient |
| Normal profit | Hold | Hold | Same |

---

## 8. When to Use V8

| Market | Recommendation | Reason |
|--------|---------------|--------|
| Wide-range sideways | ✅ Heavy use | Many signals |
| High volatility | ✅ Suitable | Easy triggers |
| Rapid drop rebound | ✅ Perfect | BinHV45 tailor-made |
| Volume-expanded rebound ⭐⭐⭐ | ✅ V8 exclusive | V8 volume confirmation loves this |
| Trend continuation ⭐ | ✅ V8 optimized | V8's loose trailing suits trends |
| One-directional rally | ⚠️ May sell out | V8 optimized but may miss |
| One-directional drop | ⚠️ Use carefully | -99% may hold large losses |
| Low-volatility | ❌ No signals | Too quiet |

---

## 9. ⚠️ Risk Re-emphasis

> **V8's core philosophy: "Let profits run, exit losing trades quickly, only buy with volume confirmation." The market won't warn you. Light positions—survival first! 🙏**

**Key V8 Risks**:
1. **Trailing activates later (4.0%)**: Good for trends, bad if reverses at 3.5%
2. **Trailing more tolerant (2.5%)**: Good for staying in, bad for exiting lower from peak
3. **10 candles for exit**: Fewer false breakouts, may miss optimal exit
4. **Volume confirmation may filter**: New volume condition may filter some valid signals
5. **Loose stop-loss**: -99% nearly disabled

```
1. Judge market: Sideways or trend continuation
2. Small capital testing first
3. Watch fees: Choose low-fee platforms
4. Use volume confirmation well: V8's core feature
5. Don't expect to get rich: This is pocket change money
```

**Remember**: V8's tagline is "let profits run, exit losing trades quickly, only buy with volume confirmation." Survival first!
