# NFI4Frog Strategy: The "Choice-Paralysis Terminally Ill" of Quantitative Trading

> **Nickname**: Frog Prince  
> **Career**: Professional "Picky Selector"  
> **Timeframe**: 5 Minutes

---

## 1. What's This Strategy?

In simple terms, **NFI4Frog** is:
- **A "terminally ill choice-paralysis patient"** with 17 entry conditions
- **A "refuse to buy wrong, refuse to miss"** obsessive compulsive trader
- **Dip + Pump dual protection net** — coward (in a good way)
- **80+ parameters** as daily food — parameter maniac

It's like a blind date who checks "three generations of family history + credit report + zodiac sign + blood type" before meeting — an overbearing mom-type character

---

## 2. Core Settings: "Strict to the Point of Being Crazy"

### Take-Profit Rules

```
Immediately: take profit at 10%
After 30 minutes: take profit at 5%
After 60 minutes: take profit at 2%
```

**Translation**: The longer you hold, the lower the requirement — "too many things can happen overnight."

### Stop-Loss Rules

```
Hard stop-loss: -10%
Trailing stop: activates after making 3%, runs on 1% drawdown
```

---

## 3. 17 Entry Conditions: 7 Categories

### 🎯 Category 1: Trend Pullback Type (2 conditions)
**Core Logic**: Major trend up, small timeframe oversold — buy!

### 📉 Category 2: BB Lower Band Rebound Type (6 conditions)
**Core Logic**: Price near BB lower band, rebound likely.

### 🔄 Category 3: EMA Difference Type (5 conditions)
**Core Logic**: EMA12 and EMA26 difference detecting downward momentum.

### 🐊 Category 4: Alligator Type (1 condition)
**Core Logic**: Alligator mouth opens upward, trend starting.

### 📊 Category 5: MA Offset Type (5 conditions)
**Core Logic**: Price below some MA by a certain percentage — seems cheap.

### 🌊 Category 6: EWO Positive Type (3 conditions)
**Core Logic**: Elliott Wave Oscillator positive, short-term momentum stronger than long-term.

### 🕳️ Category 7: Pure Bottom-Fishing Type (1 condition)
**Core Logic**: EWO negative (extreme oversold), only requires Dip protection.

---

## 4. Protection Mechanisms: Two Layers of "Safety Net"

### First Gate: Dip Protection

| Inspection Dimension | Normal Version | Strict Version | Plain English |
|--------------------|--------------|----------------|----------------|
| Current candle decline | < 2% | < 1.5% | "This candle dropped okay" |
| 2 candles decline | < 14% | < 6% | "These two days dropped okay" |
| 12 candles decline | < 32% | < 24% | "This hour dropped okay" |
| 144 candles decline | < 50% | < 40% | "This half-day dropped okay" |

### Second Gate: Pump Protection

| Time Window | Inspection Logic | Plain English |
|------------|-----------------|---------------|
| 12 hours | Rise < 46% or sufficient pullback | "Surged too muchin half a day? Wait for pullback!" |
| 36 hours | Rise < 56% or sufficient pullback | "Surged too muchin a day and a half? Wait!" |
| 48 hours | Rise < 85% or sufficient pullback | "Surged too muchin two days? Wait!" |

---

## 5. Exit Logic: More "Scheming" Than Entries

### Tiered Take-Profit

```
Making > 25%    RSI < 50   Rush out!
Making > 8%     RSI < 48   Can leave
Making > 5%     RSI < 43   About right
Making > 3%     RSI < 36   Small profit also ok
Making > 1%     RSI < 30   Just made something
```

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros

1. **Ultra-Cautious**: Dip + Pump dual protection, won't "catch falling knives" or "chase at highs"
2. **Flexible Conditions**: 17 entry conditions independently switchable
3. **Scientific Take-Profit**: Tiered RSI take-profit + profit tracking + drawdown protection, triple insurance
4. **Informational Framework Support**: 1h trend confirmation reduces false signals

### ⚠️ Cons

1. **Too Many Parameters**: 80+ optimizable parameters — even those with choice paralysis get dizzy
2. **High Computational Load**: 17 conditions computed — small VPS may gasp
3. **Overfitting Risk**: More conditions = easier to "memorize answers," good historical ≠ good future
4. **High Learning Curve**: Understanding this strategy takes weeks, not something you grasp in a glance

---

## 7. Summary: What Do You Think of This Strategy?

### One-Line Rating
> "A strategy that pushes 'better to miss than to be wrong' to the extreme."

---

## ⚠️ Risk Re-Emphasis

### Backtesting Looks Great, Live Trading Requires Caution

> **Because there are many parameters, the strategy can easily "fit" the optimal solution for past market conditions, but this doesn't mean it can definitely profit in the future.**

### My Recommendations

```
1. First understand the logic: don't rush to backtest
2. Simplify conditions: pick 5-8 core conditions you trust most, don't enable all
3. Strict backtesting: at least 1 year historical data + 1-2 month dry-run validation
4. Go live in batches: test with small positions first, add capital when stable
```

**Remember**: No matter how good a strategy, the market won'tgive you a heads-up. Test with light positions — survival is most important!
