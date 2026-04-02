# BigZ07Next2: A "High-Frequency Cautious" Trading Robot

> **Nickname**: Bargain Hunter Gen 7 Evolution Gen 2  
> **Profession**: Quant world's "high-frequency type" — fast in fast out, multi-protection  
> **Timeframe**: 5 minutes + 1 hour

---

## 1. What's This Thing?

BigZ07Next2 is a **high-frequency trading strategy**, specially designed for Freqtrade quantitative trading robots. Simply put, it's a digital currency trading system that helps you **auto buy/sell**.

This strategy is modded from an old strategy called NostalgiaForInfinityV8, added a bunch of "protection measures", with one goal: **try to earn more, try to lose less**.

---

## 2. Core Settings: Plainly Speaking It's "Smart Protection"

### Profit-Taking Rules (ROI Table)

```
Hold 0-10 min:    Consider selling if profit > 2.8%
Hold 10-40 min:   Consider selling if profit > 1.8%
Hold 40-180 min:  Consider selling if profit > 0.5%
Hold 180+ min:    Consider selling if profit > 1.8%
```

**Translation**: The longer you hold the lower the requirements, willing to sell at 0.5%, even mosquito meat eat.

### Stoploss Rules

```
Stoploss line: -10% (must cut and run when losing 10%)
Trailing take-profit: Triggers at 2.5%, run if pullback 1%
Take-profit mode: Only sell when profitable
```

**Translation**: Max lose 10%, lock profits when earned, don't actively lose.

---

## 3. 14 Entry Conditions: I've Categorized Them for You

Strategy has **14 different entry methods**, like 14 martial arts moves, satisfies any one then buys, I've grouped them into 5 categories for you:

### 🎯 Category 1: RSI Oversold Faction (Conditions 0,3-4,8-9)
**Core Logic**: RSI low means oversold, buy!

**In Plain English**:
> "Dropped too much, time to rebound right?"

**Classic Lines**:
- Condition #0: `5-minute RSI < 30 + Price dropping last 3 days + Volume suddenly contracts` → "Dropped to right level, rebound imminent"
- Condition #4: `1-hour RSI < 16 + Price at Bollinger lower rail` → "Big cycle also oversold"
- Condition #9: `5-minute RSI < 10 + 1-hour RSI < 35` → "Extremely oversold!"

### 📉 Category 2: Bollinger Band Faction (Conditions 1-2,5,12)
**Core Logic**: Price dropped to Bollinger lower rail

**In Plain English**:
> "Dropped to support level, buy!"

**Classic Lines**:
- Condition #1: `Close below Bollinger lower rail + Volume contracting` → "Broke support, shrinking volume, about to rebound"
- Condition #5: `MACD golden cross + Price at Bollinger lower rail` → "MACD turned bullish, price low, enter"

### 🔧 Category 3: MACD Golden Cross Type (Conditions 6-7,10-11)
**Core Logic**: Momentum turning strong

**In Plain English**:
> "MACD starting to exert force, buy!"

**Classic Lines**:
- Condition #7: `1-hour RSI < 39 + MACD golden cross` → "Dual cycle resonance"
- Condition #10: `1-hour Bollinger lower rail + MACD turns positive` → "Big cycle rebound signal"
- Condition #11: `Bollinger Band narrowing + MACD positive for 5 consecutive periods + RSI > 51` → "ready to explode"

### 🌟 Category 4: Advanced Combo (Condition 12)
**Core Logic**: False breakout reversal

**In Plain English**:
> "Broke then came back, classic reversal"

### ⚡ Category 5: Capital Flow (Condition 13)
**Core Logic**: Extreme oversold + capital outflow

**In Plain English**:
> "Panic selling, big bottom!"

These 14 conditions are like 14 keys, as long as one can unlock the door, the strategy enters! 🤣

---

## 4. Protection Mechanisms: Multi-Layer Defense

Strategy has comprehensive protection:

| Protection | Function | Plain English |
|------------|----------|---------------|
| ROI Ladder | Time-based take-profit | "Run when reaching the point" |
| Trailing | Dynamic profit lock | "Don't give back what earned" |
| Custom Exit | 8 conditions | "Smart exiting" |
| Recovery | For losing positions | "Minimize losses" |

---

## 5. Exit Logic: More Complex Than Entry

Strategy has 8 exit conditions:

- ROI ladder exits
- Trailing stop exits
- Custom rule exits
- Recovery exits

**In Plain English**: Many ways to exit, ensures profits protected and losses minimized.

---

## 6. This Strategy's "Personality Traits"

### ✅ Advantages
1. 12-level take-profit protection
2. 14 entry methods
3. Fast in fast out
4. Recovery mechanisms

### ⚠️ Disadvantages
1. Very complex
2. May exit too early
3. Requires monitoring

---

## 7. Suitable Scenarios

| Market | Recommendation | Reason |
|--------|---------------|--------|
| Volatile | ✅ Strong | Strategy designed for this |
| Oscillating | ✅ Recommended | Good for range-bound |
| Strong bull | ⚠️ Caution | May exit early |
| Low volatility | ❌ Not recommended | Hard to trigger |

---

## 8. Summary

### One Sentence
> "A high-frequency cautious trader with multi-layer protection."

### Who Should Use
- ✅ High-frequency traders
- ✅ People who want comprehensive protection
- ✅ Those who can handle complexity

### Who Shouldn't Use
- ❌ Long-term holders
- ❌ People who want simple strategies
- ❌ Those unwilling to learn

---

## 9. ⚠️ Risk Reminder

High complexity requires thorough understanding. Paper trade first, start small!

Surviving is most important! 🙏
