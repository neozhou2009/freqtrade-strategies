# BigZ07Next: A "Super Cautious but Wants to Earn" Trader

> **Nickname**: Bargain Hunter Gen 7 Evolution  
> **Profession**: Quant world's "patient type" — rather miss out than buy wrong  
> **Timeframe**: 5 minutes + 1 hour

---

## 1. What's This Thing?

**BigZ07Next is a "brain" for trading robots.**

You can imagine it as a super cautious fund manager, this manager:

- 📊 Looks at **5-minute charts** daily for specific buy/sell decisions
- 🔭 Simultaneously looks at **1-hour charts** to judge big trend direction
- 🤔 Simultaneously enables **14 different entry methods**
- 🛡️ Equipped with **8 different exit protections**
- ⏰ Can hold positions for long time, waiting for breakout opportunities

Simply put: **This is a "rather miss out than buy wrong" conservative strategy, but once it buys, it will try every way to help you earn and run.**

---

## 2. Core Settings: Plainly Speaking It's "Survival First"

### Profit-Taking Rules (ROI Table)

```
Hold 0-10 min:    Consider selling if profit > 2.8%
Hold 10-40 min:   Consider selling if profit > 1.8%
Hold 40-180 min:  Consider selling if profit > 0.5%
Hold 180+ min:    Consider selling if profit > 1.8%
```

**Translation**: Quick rise in short time means might be "pump", run fast.

### Stoploss Rules

```
Stoploss line: -10% (must cut and run when losing 10%)
Trailing take-profit: Enabled (stays after earning, dynamically adjusts sell point)
Take-profit mode: Only sell when profitable
```

**Translation**: Max lose 10%, lock profits when earned, don't actively sell when losing (wait for breakout).

---

## 3. 14 Entry Conditions: I've Categorized Them for You

Strategy has 14 different "entry packages", as long as **any 1** is satisfied, will buy, I've grouped them into 6 categories for you:

### 🎯 Category 1: Oversold Rebound Type (Condition 0)
**Core Logic**: RSI oversold + volume contraction

**In Plain English**:
> "Dropped too hard, time to rebound, and needs to drop slowly"

**Classic Lines**:
- Condition #0: `5-minute RSI < 30 + 1-hour RSI < 71 + Close dropping for 3 consecutive days + Volume can't be too crazy` → "Dropped to right level, rebound imminent"

### 📉 Category 2: Bollinger Band Bargain Type (Conditions 1-2)
**Core Logic**: Price breaks below Bollinger lower rail

**In Plain English**:
> "Price fell below Bollinger Band, normally will bounce back"

**Classic Lines**:
- Condition #1: `Close below Bollinger lower rail + 1-hour RSI < 69 + Volume contracting` → "Broke support, shrinking volume, about to rebound"
- Condition #2: `Close < Bollinger lower rail + Volume contracting` → "More conservative bottom fishing"

### 🔧 Category 3: 1-Hour Trend Confirmation Type (Conditions 3-4)
**Core Logic**: Big cycle upward, small cycle oversold

**In Plain English**:
> "Big direction is rising, now just small pullback, buy inopportunistically"

**Classic Lines**:
- Condition #3: `1-hour candles above EMA200 + 5-minute RSI < 14 + Volume contracting` → "Big cycle upward, small cycle extreme oversold"
- Condition #4: `1-hour RSI < 16 + Price at Bollinger lower rail` → "Big cycle also oversold"

### ⚡ Category 4: MACD Golden Cross Type (Conditions 5-7)
**Core Logic**: Momentum turning strong + cheap price

**In Plain English**:
> "MACD just turned bullish, price also dropped to support, can buy"

**Classic Lines**:
- Condition #5: `MACD golden cross + Price < Bollinger lower rail` → "MACD turned bullish, price low, enter"
- Condition #7: `1-hour RSI < 17 + MACD golden cross + Volume contracting` → "Double insurance"

### 🌟 Category 5: Dual RSI Oversold Type (Conditions 8-9)
**Core Logic**: Both cycle RSI oversold

**In Plain English**:
> "Short-term and long-term both oversold, rebound probability very high"

**Classic Lines**:
- Condition #8: `5-minute RSI < 28 + 1-hour RSI < 15` → "Big small cycles both oversold, resonance signal"

---

## 4. Protection Mechanisms: Multi-Layer Defense

Strategy has comprehensive protection:

| Protection | Function | Plain English |
|------------|----------|---------------|
| ROI | Time-based take-profit | "Run when reaching the point" |
| Trailing | Dynamic profit lock | "Don't give back what earned" |
| Custom Exit | 50+ rules | "Smart exiting" |
| Pump Protection | Detects abnormal volatility | "Run when pump detected" |

---

## 5. Exit Logic: More Complex Than Entry

Strategy has 8 basic exit conditions plus 50+ custom rules:

- ROI ladder exits
- Trailing stop exits
- Custom rule exits
- Recovery exits for losing positions

**In Plain English**: Many ways to exit, ensures profits protected and losses minimized.

---

## 6. This Strategy's "Personality Traits"

### ✅ Advantages
1. Comprehensive protection
2. 14 entry methods
3. Can hold long for breakout
4. Pump protection

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
> "A patient, cautious trader with comprehensive protection."

### Who Should Use
- ✅ Patient investors
- ✅ People who want comprehensive protection
- ✅ Those who can handle complexity

### Who Shouldn't Use
- ❌ Impatient traders
- ❌ People who want simple strategies
- ❌ Those unwilling to learn

---

## 9. ⚠️ Risk Reminder

High complexity requires thorough understanding. Paper trade first, start small!

Surviving is most important! 🙏
