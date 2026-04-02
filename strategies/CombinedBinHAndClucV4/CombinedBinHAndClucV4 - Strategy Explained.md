# CombinedBinHAndClucV4 Strategy Explained: Bollinger Band Double-Knife, Evolved

> **Nickname**: Bollinger Band Double-Knife · Evolved  
> **Profession**: Oversold Rebound Expert (Evolved)  
> **Timeframe**: 5 Minutes (5m)

---

## 1. What's This Strategy?

Put simply, **CombinedBinHAndClucV4** is the **evolved version** of the "double-knife" oversold rebound strategy:

- Merged from two classic strategies: **BinHV45** + **ClucMay72018**
- Each has its own special move—buy if either triggers
- Specifically catches opportunities where price "drops too much and bounces back"

**V4 vs V3 Core Upgrades**:
- Stop-loss widened (-10% → -99%): Don't get shaken out by market noise
- Trailing stop earlier (3% → 2.5%): Lock in profits earlier
- Time stop-loss shorter (36.7 hrs → 5 hrs): Don't let losses fester
- Stricter exits (4 candles → 5 candles): Confirm longer before letting you sell

Like an experienced fisherman with two nets—the V4 version is more patient and knows better how to protect himself. 🐟

---

## 2. Core Settings: "Let profits run, but don't hold on too long"

### Take-Profit Rule

```
Cumulative return ≥ 1.9% → Take-profit triggered
```

**Translation**: Grab 1.9% and run, don't get greedy. (0.1% more than V3)

### Stop-Loss Rules

```
Fixed stop-loss: -99% (almost no limit)
Trailing stop: Activates after 2.5% profit, protects 1% of gains (earlier than V3)
Time stop-loss: Force exit if still in loss after 5 hours (dramatically shortened from V3)
```

**Translation**:
- Fixed stop-loss is almost never used—V4's philosophy: "Don't get spooked by short-term volatility"
- After 3% profit, activate the "shield"—exit on 1% pullback from high (earlier protection than V3)
- Still losing after 5 hours? No more waiting, market exit (V3 gave you 36 hours, V4 is decisive)

---

## 3. Two Sets of Entry Conditions: Here's the Breakdown

### 🎯 Set 1: BinHV45 Style (Rapid Sell-off Rebound)

**Core Logic**: Price suddenly crashes, breaks below the lower Bollinger Band, but can't drop anymore—bottom fishing!

**One-liner**: Price rapidly pierces the lower Bollinger Band with a short wick and high volatility—classic "last drop" pattern.

| Condition | Plain Translation |
|-----------|-----------------|
| Previous day's lower Bollinger Band is valid | Confirm it's not a calculation error |
| Bollinger Band width > 0.8% of price | Enough volatility, there's meat to eat |
| Closing price change > 1.75% | The day really did crash hard |
| Lower wick < 25% of channel width | Close near the low, hit bottom |
| Close < previous day's lower Bollinger Band | Broke below the rail, oversold |
| Close ≤ previous day's close | Continued dropping or flat, confirms downtrend |
| Volume > 0 | Exclude abnormal candles |

---

### 📉 Set 2: ClucMay72018 Style (Volume-Shrinking Oversold)

**Core Logic**: Price breaks below the lower Bollinger Band, but volume is abnormally low—selling pressure has dried up.

**One-liner**: Price breaks below the lower Bollinger Band with shrinking volume in a downtrend—selling pressure exhausted, waiting for rebound.

| Condition | Plain Translation |
|-----------|-----------------|
| Close < 50-day moving average | Confirm medium-term downtrend |
| Close < 98.5% of Bollinger Band lower rail | Clearly broke below the rail |
| Volume < 20x the 30-day average | Volume abnormally shrunken |
| Volume > 0 | Exclude abnormal candles |

---

## 4. Protection Mechanisms: 4 Layers of "Protective Charms"

| Protection | Trigger | Plain English |
|------------|---------|---------------|
| Fixed stop-loss | Loss reaches 99% | Almost never triggers | V4 barely uses this, relies on other mechanisms |
| Time stop-loss ⭐ | Holding > 5 hours and losing | Force exit | "5 hours and still losing? I'm done waiting" |
| Trailing stop ⭐ | Profit reaches 2.5% then activates | Lock in profits | "Gained enough, 1% pullback and I'm gone" |
| Sell only in profit | Sell signal triggers but losing | Forbid selling | "No selling when losing, wait for break-even" |

⭐ **V4 Core Changes**: Time stop-loss shortened dramatically from 36 hours to 5 hours, trailing stop activation lowered from 3% to 2.5%.

The 4 layers of protection: bulletproof vest, helmet, and bodyguard all hired. But V4 decided to remove the vest—because it believes "time stop-loss is the real man! 🛡️

---

## 5. Exit Logic: Simpler Than Entry

### 5.1 Take-Profit Exit

```
Cumulative return ≥ 1.9% → Sell
```

**Plain English**: Grab 1.9% and run. (0.1% more than V3)

### 5.2 Signal Exit ⭐V4 Key Change

When **5 consecutive 5-minute candles** (was 4 in V3) are above the Bollinger Band upper rail, sell triggers.

**Plain English**:
> "Five straight 5-minute candles above the upper rail? This rally is too strong—V4 is more cautious, makes you confirm one more candle before selling."

### 5.3 Trailing Stop Trigger

Price goes up then drops? Exit when trailing stop line is hit.

**Plain English**:
> "Alright, it's climbing, I'll watch it. Drop 1% from the high? Done. V4 starts watching earlier (at 2.5%)."

### 5.4 Time Stop-Loss Trigger

Still losing after 5 hours? Get out.

**Plain English**:
> "V3 waited 36 hours to admit defeat, V4 only gives 5 hours. Much more decisive!"

---

## 6. Strategy "Personality"

### ✅ Pros

1. **Dual-Knife Hunter**: Two entry logics covering both rapid sell-off and volume-shrinking rebounds
2. **V4 Braver Holdings**: -99% stop-loss almost never used, not afraid of short-term volatility
3. **Earlier Protection**: 2.5% activates trailing stop, locks in gains earlier
4. **Decisive Stop-Loss**: 5-hour time stop-loss, won't wait around with you

### ⚠️ Cons

1. **Sell-and-Miss Master**: 1.9% take-profit too conservative, could soar right after you sell
2. **5-Minute Noise**: Short timeframe is easily fooled by false signals, and fees are high too
3. **One-Directional Drop May Be Hard to Bear**: -99% stop-loss is essentially nonexistent
4. **Exit Conditions Stricter**: 5 consecutive candles must break upper rail

---

## 7. Summary: V4 vs V3 Core Differences

| Setting | V3 | V4 | Impact |
|---------|-----|-----|--------|
| Take-profit line | 1.8% | 1.9% | Earn a tiny bit more |
| Stop-loss line | -10% | -99% | Almost disabled, tolerates bigger swings |
| Trailing activation | 3% | 2.5% | Earlier protection |
| Time stop-loss | 36 hours | 5 hours | Admit mistakes sooner, but may miss big trends |
| Exit confirmation | 4 candles | 5 candles | Stricter, fewer false breakouts |

### Who Should Use It?
- ✅ Traders who can identify sideways markets or trend continuation
- ✅ People who like short-term high-frequency trading
- ✅ People who can tolerate short-term floating losses (because -99% stop almost never triggers)
- ✅ People wanting to catch pullback entries in trend continuation

### Who Should NOT Use It?
- ❌ People who want to hold long-term for big trends
- ❌ People who hate frequent operations
- ❌ People who can't tolerate large short-term floating losses
- ❌ People using in one-directional downtrends

---

## 8. What Markets Does V4 Make Money In?

| Market Type | Rating | Plain English |
|:-----------|:-------|:--------------|
| 📈 Wide-range sideways | ⭐⭐⭐⭐⭐ | Perfect match, many signals |
| 🔄 High volatility | ⭐⭐⭐⭐ | Big swings, conditions trigger easily |
| 📉 Rapid drop rebound | ⭐⭐⭐⭐⭐ | BinHV45 tailor-made for this |
| 🎯 Shrinking-volume drop | ⭐⭐⭐⭐ | Cluc catches exhausted selling pressure |
| 📊 Trend continuation ⭐ | ⭐⭐⭐⭐⭐ | V4 optimized for this |
| 🚀 Sustained rally | ⭐⭐☆☆☆ | Buys and immediately sells out |
| 💀 Sustained drop | ⭐⭐☆☆☆ | -99% stop-loss may hold big floating losses, 5hr stop fires often |
| 😴 Low-volatility consolidation | ⭐⭐☆☆☆ | Too little volatility |

**Bottom line**: Swims in sideways markets, trend continuation even better, trending markets need caution.

---

## 9. ⚠️ Risk Re-emphasis

> **V4's -99% stop-loss almost disabled—you must be mentally prepared to endure large short-term floating losses. The 5-hour time stop-loss may fire frequently and get shaken out in trending markets.**

**Key V4 Risks vs V3**:
1. **-99% almost disabled**: One-directional drops may hold large floating losses
2. **5-hour time stop shortened**: Good for quick admits, but may miss longer-developing rebounds
3. **5 candles for exit**: Fewer false breakouts, but may miss optimal exit point

```
1. Judge market conditions first: Sideways or trend continuation use; one-directional drop needs caution
2. Small capital testing first
3. Watch fees: Choose low-fee platforms
4. Manually add stop-loss: V4's -99% too loose, manually set 5%-10%
5. Don't expect to get rich: This is pocket change money, not a wealth code
```

**Remember**: No matter how good a strategy, the market won't announce when it teaches you a lesson. Light positions—survival is top priority! 🙏
