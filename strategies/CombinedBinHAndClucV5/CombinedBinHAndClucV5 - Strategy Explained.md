# CombinedBinHAndClucV5 Strategy Explained: Bollinger Band Double-Knife, Greedier Edition

> **Nickname**: Bollinger Band Double-Knife · Greedier Edition  
> **Profession**: Oversold Rebound Expert (Trend-Full-Bandit type)  
> **Timeframe**: 5 Minutes (5m)

---

## 1. What's This Strategy?

**CombinedBinHAndClucV5** is the **greedier version** of the "double-knife" oversold rebound strategy:

- Merged from two classics: **BinHV45** + **ClucMay72018**
- Each has its own special move—buy if either triggers
- Catches opportunities where price "drops too much and bounces back"

**V5 vs V4 Core Upgrades**:
- Higher take-profit (1.9% → 2.0%): Want to earn a bit more
- Trailing stop later (2.5% → 2.75%): Let trends run further
- Trailing stop more tolerant (pullback 1% → 1.25%): Don't get shaken by small pullbacks
- Stricter exits (5 candles → 6 candles): Fewer false breakout interruptions

Like a seasoned fisherman casting two nets—the V5 fisherman is greedier, not satisfied with small gains, wanting to eat the entire wave. 🐟

---

## 2. Core Settings: "Greedier, more tolerant"

### Take-Profit Rule

```
Cumulative return ≥ 2.0% → Take-profit triggered
```

**Translation**: Grab 2.0% and run, 0.1% more than V4. Don't underestimate this 0.1%, it adds up!

### Stop-Loss Rules

```
Fixed stop-loss: -99% (almost no limit)
Trailing stop: Activates after 2.75% profit, protects 1.25% of gains
Time stop-loss: Force exit if still in loss after 5 hours
```

**Translation**:
- Fixed stop-loss almost never used—V5's philosophy: "Don't get spooked by short-term volatility"
- After 2.75% profit, activate the "shield"—exit on 1.25% pullback from high (more tolerant than V4)
- Still losing after 5 hours? Market exit

---

## 3. Two Sets of Entry Conditions: Here's the Breakdown

### 🎯 Set 1: BinHV45 Style (Rapid Sell-off Rebound)

**Core Logic**: Price suddenly crashes, breaks below the lower Bollinger Band, but can't drop anymore—bottom fishing!

**One-liner**: Price rapidly pierces the lower Bollinger Band with a short wick and high volatility—classic "last drop" pattern.

| Condition | Plain Translation |
|-----------|-----------------|
| Previous day's lower Bollinger Band is valid | Confirm it's not a calculation error |
| Bollinger Band width > 0.8% of price | Enough volatility, there's meat to eat |
| Closing price change > 1.75% | The day really crashed hard |
| Lower wick < 25% of channel width | Close near the low, hit bottom |
| Close < previous day's lower Bollinger Band | Broke below the rail, oversold |
| Close ≤ previous day's close | Continued dropping or flat |
| Volume > 0 | Exclude abnormal candles |

---

### 📉 Set 2: ClucMay72018 Style (Volume-Shrinking Oversold)

**Core Logic**: Price breaks below the lower Bollinger Band, but volume is abnormally low—selling pressure has dried up.

**One-liner**: Price breaks below the lower Bollinger Band with shrinking volume in a downtrend—selling pressure exhausted.

| Condition | Plain Translation |
|-----------|-----------------|
| Close < 50-day moving average | Confirm medium-term downtrend |
| Close < 98.5% of Bollinger Band lower rail | Clearly broke below the rail |
| Volume < 20x the 30-day average | Volume abnormally shrunken |
| Volume > 0 | Exclude abnormal candles |

---

## 4. Protection Mechanisms: 4 Layers

| Protection | Trigger | Plain English |
|------------|---------|---------------|
| Fixed stop-loss | Loss reaches 99% | Almost never triggers |
| Time stop-loss ⭐ | Holding > 5 hours and losing | "5 hours and still losing? Done" |
| Trailing stop ⭐⭐ | Profit reaches 2.75% then activates | "Gained enough, 1.25% pullback and I'm gone" |
| Sell only in profit | Sell signal triggers but losing | "No selling when losing" |

⭐ **V5 Core Changes**: Trailing stop activation raised from V4's 2.5% to 2.75%, pullback tolerance deepened from 1% to 1.25%. V5 is more greedy—let trends run further!

V5's bodyguard is more laid-back: "You run first, I'll watch for you. Wait until you're up 2.75% before I start paying attention!" 🛡️

---

## 5. Exit Logic

### 5.1 Take-Profit Exit

```
Cumulative return ≥ 2.0% → Sell
```

**Plain English**: Grab 2.0% and run. (0.1% more than V4)

### 5.2 Signal Exit ⭐V5 Key Change

When **6 consecutive 5-minute candles** (was 5 in V4) are above the Bollinger Band upper rail, sell triggers.

**Plain English**:
> "Six straight 5-minute candles above the upper rail? This rally is too strong—V5 is more cautious, makes you confirm one more candle."

### 5.3 Trailing Stop Trigger

**Plain English**:
> "Alright, it's climbing, I'll watch it. Drop 1.25% from the high? Done. V5 is more tolerant—small pullbacks don't scare me."

### 5.4 Time Stop-Loss Trigger

**Plain English**:
> "5 hours and still losing? Done."

---

## 6. Strategy "Personality"

### ✅ Pros

1. **Dual-Knife Hunter**: Two entry logics, covers both rapid sell-off and volume-shrinking rebounds
2. **V5 Braver Holdings**: 2.75% before trailing stop activates, lets profits run more than V4
3. **V5 More Tolerant**: 1.25% pullback tolerance, not shaken by small swings
4. **Higher Take-Profit**: 2.0% vs V4's 1.9%
5. **Stricter Exits**: 6 candles confirmation, fewer false breakouts

### ⚠️ Cons

1. **Sell-and-Miss Risk**: 2.0% take-profit may miss big moves, but V5 uses trailing stop to compensate
2. **5-Minute Noise**: Short timeframe is easily fooled by false signals
3. **One-Directional Drop May Be Hard to Bear**: -99% stop-loss essentially nonexistent
4. **Exit Conditions Stricter**: 6 candles may miss optimal exit

---

## 7. V5 vs V4 vs V3: Evolution Table

| Setting | V3 | V4 | V5 | Impact |
|---------|-----|-----|-----|--------|
| Take-profit | 1.8% | 1.9% | 2.0% | Gradually increasing |
| Stop-loss | -10% | -99% | -99% | V4 loosened, V5 maintained |
| Trailing activation | 3% | 2.5% | 2.75% | V4 earlier, V5 later→bolder |
| Trailing pullback | 1% | 1% | 1.25% | V5 deeper, more pullback tolerant |
| Time stop-loss | 36 hrs | 5 hrs | 5 hrs | V4 shortened, V5 maintained |
| Exit confirmation | 4 candles | 5 candles | 6 candles | Gradually stricter |

---

## 8. When to Use V5

| Market | Recommendation | Reason |
|--------|---------------|--------|
| Wide-range sideways | ✅ Heavy use | Price hits Bollinger rails repeatedly |
| High volatility | ✅ Suitable | High volatility, easy triggers |
| Rapid drop rebound | ✅ Perfect | BinHV45 tailor-made |
| Trend continuation ⭐ | ✅ V5 optimized | V5's loose trailing suits trend following |
| Trend pullback | ✅ V5 optimized | V5 eats more of the trend |
| One-directional rally | ⚠️ May sell out | V5 optimized but may still miss |
| One-directional drop | ⚠️ Use carefully | -99% stop-loss may hold large losses |
| Low-volatility | ❌ No signals | Too quiet to trigger |

---

## 9. V5 vs V4 Core Differences

| Setting | V4 | V5 | Key Difference |
|---------|-----|-----|----------------|
| Take-profit | 1.9% | 2.0% | Earn 0.1% more |
| Trailing activation | 2.5% | 2.75% | V5 lets trends run 0.25% more before protecting |
| Trailing pullback | 1% | 1.25% | V5 tolerates deeper pullbacks |

**One-liner**: V5 is V4's greedier version—lets profits run further, tolerates bigger pullbacks, wants to eat the whole wave.

---

## 10. ⚠️ Risk Re-emphasis

> **V5's core philosophy is "let profits run," but the market won't warn you when it's about to teach you a lesson. Light positions—survival is top priority! 🙏**

**V5's Key Risks vs V4**:
1. **Trailing stop activates later (2.75%)**: Good for riding trends, bad if it reverses at 2.5%
2. **Trailing stop more tolerant (1.25%)**: Good for staying in, bad for exiting at peak
3. **6 candles for exit**: Fewer false breakouts, but may miss optimal exit

```
1. Judge market: Use in sideways or trend continuation
2. Small capital testing first
3. Watch fees: Choose low-fee platforms
4. Manually add stop-loss: V5's -99% too loose, manually set 5%-10%
5. Don't expect to get rich
```

**Remember**: V5's tagline is "let profits run"—but never forget: market teaches lessons without warning. Light positions, survive first!
