# NFI5MOHO Strategy: The "Choice-Paralysis Terminally Ill" of Quantitative Trading

> **Nickname**: Strategy Player, Parameter Maniac, 21-Way Buy Religion  
> **Career**: Professional Bottom-Fisher, Part-time Trend Follower  
> **Timeframe**: 5 Minutes (watch) + 1 Hour (see big picture)

---

## 1. What's This Strategy?

In simple terms, **NFI5MOHO** is:
- 21 entry conditions, "wide net" approach to capture opportunities
- 8 sell conditions, plus 5-level take-profit + 3 trailing take-profit systems
- Various protection mechanisms — a "mom-type" strategy afraid you'll lose money

It's like a choice-paralysis terminally ill patient who asks "should I buy this coin?" 21 times before making a decision — but each time the question is different!

**Name Breakdown**:
- **NFI** = NostalgiaForInfinity (tribute to classic strategy series)
- **5M** = 5-minute framework + MultiOffset (multi-MA offset)
- **OHO** = Optimized (hyper-optimized) + HyperOpt

In short: **A "Frankenstein" strategy repeatedly optimized with parameters too numerous to count.**

---

## 2. Core Settings: "Greedy but Scared"

### Take-Profit Rules (ROI Table)

```
Immediately after buying: want 8% profit to exit
After 60 minutes: 4% profit also acceptable
After 90 minutes: 2% profit also acceptable
After 120 minutes: 1% profit also OK
```

**Translation**: Initially ambitious wanting 8%, but if the market doesn't cooperate and you've waited an hour, "a little money is fine." After two hours, "even a small profit works."

---

## 3. 21 Entry Conditions: I've Categorized Them for You

### 🎯 Category 1: Basic Bottom-Fish Group (Conditions 1-4)
**Core Logic**: Price has dropped enough, safe to bottom-fish.

### 📉 Category 2: Strict Bottom-Fish Group (Conditions 5-8)
**Core Logic**: Stricter conditions, only act when truly safe.

### 🔄 Category 3: Loose Bottom-Fish Group (Conditions 9-12)
**Core Logic**: Relaxed conditions, capture more opportunities.

### 📈 Category 4: Trend Pullback Group (Conditions 13-17)
**Core Logic**: In an uptrend, buy on pullback.

### 💥 Category 5: Extreme Oversold Group (Conditions 18-21)
**Core Logic**: RSI extreme oversold, bet on rebound.

---

## 4. Protection Mechanisms: Scared-You'd-Lose-Money "Mom"

### 4.1 Dip Protection (Don't Catch Falling Knives!)

| Protection Type | Current Candle | 2-Period | 12-Period | 144-Period |
|----------------|---------------|----------|-----------|------------|
| **Normal** | <2% | <14% | <32% | <50% |
| **Strict** | <1.5% | <6% | <24% | <40% |
| **Loose** | <2.6% | <24% | <42% | <66% |

### 4.2 Pump Protection (Don't Chase Highs!)

| Time Window | Check What | Plain English |
|------------|-----------|---------------|
| 24 hours | How much surged in last day | "Surged 50% today? Don't chase!" |
| 36 hours | How much surged in last day and a half | "Doubled in 1.5 days? Careful!" |
| 48 hours | How much surged in last two days | "Surged 80% in two days? Already risky!" |

---

## 5. Exit Logic: More Fabulous Than Entries

### 5.1 Tiered Take-Profit: How Much Profit Triggers an Exit?

```
Profit 1%-10% + RSI<33 → Exit, lock in gains
Profit 1%-10% + RSI<38 → Look again, RSI getting high
Profit 1%-10% + RSI<43 → RSI even higher, risk increasing
Profit 6%-30% + RSI<48 → Made good profit, RSI still healthy
Profit 30%-60% + RSI<50 → Made big money! RSI getting high, take what you have
```

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros

1. **Many Opportunities**: 21 entry conditions, one will suit you (and the market)
2. **Sufficient Protection**: Dip and Pump dual protection, won't let you chase or catch falling knives
3. **Flexible Take-Profit**: Tiered + trailing, can lock profits while letting winners run
4. **Multi-Timeframe**: 1h confirms 5m, big picture correct before acting
5. **Customizable**: Many parameters, can Hyperopt optimize to suit your style

### ⚠️ Cons

1. **Too Complex**: 100+ parameters, reading code makes your eyes spin
2. **Overfitting Risk**: So many parameters, many optimized for history,not necessarily effective for future
3. **High Computational Load**: Needs 300 candles warm-up, low-end VPS will lag
4. **Steep Learning Curve**: Fully understanding this strategy takes at least 2-4 weeks

---

## 7. Summary: What Do You Think of This Strategy?

### One-Line Rating
> "Quantitative world's Swiss Army Knife — fully featured, but requires skill to use."

---

## ⚠️ Risk Re-Emphasis

### Backtesting Looks Great, Live Trading Requires Caution

NFI5MOHO's historical backtesting performance is often **extremely impressive** — but there's a trap:

> **Because there are many parameters, the strategy can easily "fit" the optimal solution for past market conditions, but this doesn't mean it can definitely profit in the future.**

### My Recommendations

```
1. First dry-run for at least 1 month
2. Small-funds live test (5%-10% of total capital)
3. Weekly review, see which conditions trigger often
4. Adjust parameters regularly, but don't change too frequently
5. Never go all-in
```

**Remember**: No matter how good a strategy, the market won'tgive you a heads-up. Test with light positions — survival is most important!
