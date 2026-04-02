# NFI47V2 Strategy: The Trading Machine of "Choice-Paralysis Terminally Ill"

> **Nickname**: Quantitative Player  
> **Career**: Simultaneously flirting with 17 signals, whoever passes counts  
> **Timeframe**: 5-Minute chart, but watching 1-Hour chart for big trends

---

## 1. What's This Strategy?

In simple terms, **NFI47V2** is:
- Has 17 entry conditions, each can trigger a buy
- Has 8 sell signals, plus 12-level take-profit
- Has three-layer protection mechanism, prevents chasing highs and catching falling knives
- Code over 1000 lines, 100+ parameters

It's like going on 17 blind dates simultaneously, each with different standards — whoever passes the criteria gets a date

---

## 2. Core Settings: Plain English — "Not Greedy, Not Panicked"

### Take-Profit Rules (ROI Table)

```
Immediately → take profit at 10%
After 30 minutes → take profit at 5%
After 60 minutes → take profit at 2%
```

**Translation**: Demanding when first buying, becomes more tolerant over time. Like when you first job-hunt requiring 20k monthly salary, then accept 10k after can't find work.

### Stop-Loss Rules

```
Fixed stop-loss: -10%
Trailing stop: activates after 1% profit, exits on 2.5% drawdown from high
```

---

## 3. 17 Entry Conditions: I've Categorized Them for You

### 🎯 Category 1: Trend Pullback Entry (2 conditions)
**Core Logic**: Major trend is upward — minor pullback is entry opportunity

### 📉 Category 2: Bollinger Band Lower Band Entry (6 conditions)
**Core Logic**: Price drops to BB lower band, usually an oversold signal

### 📊 Category 3: EMA Deviation Entry (5 conditions)
**Core Logic**: EMA12 and EMA26 show negative deviation, price oversold simultaneously

### 🐊 Category 4: Alligator Breakout Entry (1 condition)
**Core Logic**: Alligator multi-line bullish alignment, trend confirmed

### 🔮 Category 5: EWO Indicator Entry (6 conditions)
**Core Logic**: Elliott Wave Oscillator combined with SMA relative position

---

## 4. Protection Mechanisms: Three Layers of "Seatbelts"

### 🛡️ DIP Protection (Anti-Deep-Drop)

| Level | Meaning | Plain English |
|------|---------|---------------|
| Normal | Standard protection | "Don't buy into deep pits" |
| Strict | Strict protection | "Only buy small pits, not big ones" |
| Loose | Loose protection | "Deep pits are okay, opportunity is rare" |

### 🚀 PUMP Protection (Anti-Chasing-Highs)

| Time Window | Meaning | Plain English |
|------------|---------|---------------|
| 24 hours | Surged within the day? | "Surged 20% yesterday, don't chase today" |
| 36 hours | Surged within a day and a half? | "Surged too much recently, wait and see" |
| 48 hours | Surged within two days? | "Surged like crazy in two days, don't be the bag holder" |

---

## 5. Exit Logic: More Fabulous Than Entries

### 5.1 Tiered Take-Profit: How Much Profit Triggers an Exit?

```
Making 21.6%+ with RSI < 33.15 → Run!
Making 10%-21.6% with RSI < 45.16 → Run!
...
Making 0%-1.6% with RSI < 45.61 → Can also run!
```

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros

1. **Extremely Cautious**: Three-layer DIP + three-layer PUMP protection, chasing highs and catching falling knives nearly impossible
2. **Many Opportunities**: 17 entry conditions, one will always trigger
3. **Flexible Take-Profit**: 12-level take-profit, automatically adjusts based on market status
4. **Trend Confirmation**: Most conditions have 1-hour timeframe trend confirmation

### ⚠️ Cons

1. **Too Many Conditions**: 17 entry conditions, 1000+ lines of code — changing is headache-inducing
2. **Parameter Explosion**: 100+ parameters, optimization is a nightmare
3. **Slow Startup**: Needs 400 candles warm-up, equivalent to 33 hours of data
4. **Easy to Overfit**: More parameters = easier to "memorize answers"

---

## 7. Summary: What Do You Think of This Strategy?

### One-Line Rating
> "A cautious crazy player — flirting with 17 signals simultaneously, but flirting cautiously and professionally"

### Who's It For?
- ✅ Quantitative traders (fully automated)
- ✅ People who understand technical analysis
- ✅ People with VPS
- ✅ People who like trend-following strategies

### Who's It NOT For?
- ❌ Manual traders (too many conditions to judge in real-time)
- ❌ Beginner newbies
- ❌ People without programming foundation
- ❌ People wanting to get rich quick

---

## ⚠️ Risk Re-Emphasis (Must Read This Section)

### Backtesting Looks Great, Live Trading Requires Caution

NFI47V2's historical backtesting performance is often **extremely impressive** — but there's a trap:

> **Because there are many parameters, the strategy can easily "fit" the optimal solution for past market conditions, but this doesn't mean it can definitely profit in the future.**

### My Recommendations

```
1. Only use Strict-level protection parameters
2. Control trading pairs to 40-50
3. Dry-run for at least 1 month first
4. Live trade only with funds you can afford to lose
5. Check strategy performance regularly — stop if not working
```

**Remember**: No matter how good a strategy, the market won'tgive you a heads-up. Test with light positions — survival is most important!
