# NFI46Z Strategy: The "Player" of Quantitative Trading — 29 Entry Conditions, There's Always One for You

> **Nickname**: Choice-Paralysis Terminally Ill Patient, Quantitative Player  
> **Career**: Trend Following + Refined Take-Profit Expert  
> **Timeframe**: 5 Minutes (work) + 1 Hour (see trends)

---

## 1. What's This Strategy?

In simple terms, **NFI46Z** is:
- **Entry conditions numerous to the point of being offensive**: 29 conditions, each independently switchable
- **Protection mechanisms layered**: Too much drop won't buy, too much rise won't buy, wrong trend won't buy
- **Take-profit logic refined to the point of beingintense**: Not "sell when you make money" but "based on how much you make, RSI, trend, Pump to decide when to sell"
- **Parameters numerous to the point of causing hair loss**: 200+ parameters, optimization can make you question your sanity

It's like someone checking three generations of family history, credit reports, zodiac signs, AND today's almanac before a blind date — **meticulous to the point ofintense**

---

## 2. Core Settings: Plain English — "I'm Not Greedy, But I'm Not Stupid"

### Take-Profit Rules (ROI Table)

```
0 minutes:     2.8% (take profit immediately)
10 minutes:    1.8%
40 minutes:    0.5%
3 hours:       1.8% (wait, it's back?)
```

**Translation**: This ROI table is interesting — when first buying (0 minutes) allows some greed, if after 40 minutes only making 0.5%, it accepts that. But after 3 hours if price has risen again, gives you a 1.8% chance to exit.

### Stop-Loss Rules

```
Fixed stop-loss: -10%
Trailing stop: activates after making 2.5%, triggers on 1% drawdown
Dynamic stop-loss: intelligently adjusted based on RSI and EMA
```

**Translation**: The 10% stop-loss is quite tolerant, indicating the strategy believes "it'll probably come back if I hold." But once making money, trailing stop activates — **don't let earned profits evaporate too much**.

---

## 3. 29 Entry Conditions: I've Categorized Them for You

This strategy's entry conditions are so many they can't even remember them themselves. I've organized them into 7 categories:

### 🎯 Category 1: Trend Pullback Type (5 conditions: #1, #5, #9, #10, #14)
**Core Logic**: Major trend is upward, short-term oversold appears, can bottom-fish

**Plain English**:
> "Look, this stock has been rising, now it's pulled back, RSI is also low, money flow is weak — is this an opportunity?"

---

### 📉 Category 2: Bollinger Band Breakout Type (11 conditions: #2, #3, #4, #6, #18, #21, #22, #23, #24, #25, #26)
**Core Logic**: Price breaks below BB lower band, may be oversold rebound opportunity

---

### 📊 Category 3: EMA Difference Type (5 conditions: #5, #6, #7, #14, #15)
**Core Logic**: EMA26 - EMA12 difference detection (MACD-like logic)

---

### 🐊 Category 4: Alligator Type (1 condition: #8)
**Core Logic**: Alligator indicator lips, teeth, jaw arrangement

---

### 🌊 Category 5: EWO Bottom-Fishing Type (4 conditions: #12, #13, #16, #17)
**Core Logic**: Elliott Wave indicator extreme negative values for bottom-fishing

---

### 📦 Category 6: Oversold Rebound Type (2 conditions: #19, #20)
**Core Logic**: Consecutive narrow-range volatility or RSI extreme oversold

---

### 🔥 Category 7: Pure RSI + Pump Type (4 conditions: #24, #27, #28, #29)
**Core Logic**: 1h RSI extremely low + Pump detection

---

## 4. Protection Mechanisms: 12 Layers of "Fuses"

### Dip Protection (Is the Drop Deep Enough?)

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| **Normal** | Standard decline check | "Dropped, but not too bad, can buy" |
| **Strict** | Strict decline check | "Dropped not nearly enough, won't buy!" |
| **Loose** | Loose decline check | "A little drop is fine, buy if you get the chance!" |

### Pump Protection (Did It Rise Too Much?)

| Protection Type | Time Window | Plain English |
|----------------|------------|---------------|
| **Normal 24h** | 24 hours | "Didn't surge too much in 24 hours, can buy" |
| **Normal 36h** | 36 hours | "Didn't surge too much in 36 hours, can buy" |
| **Normal 48h** | 48 hours | "Didn't surge too much in 48 hours, can buy" |
| **Strict** | Same | "Surge check even stricter!" |
| **Loose** | Same | "Surge check looser" |

---

## 5. Exit Logic: More Fabulous Than Entries

### 5.1 Tiered Take-Profit: How Much Profit Triggers an Exit?

```
Profit          RSI Condition      Triggers Exit
──────────────────────────────────────────────────
> 31.3%         RSI < 34.0        Making 31% and running
20%~31.3%       RSI < 38.5        Making 20% and running
11.1%~20%       RSI < 55.9        Making 11% and running
...
1%~2%           RSI < 31.1        Making 1% and running
```

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros

1. **intense Protection**: Dip + Pump dual protection, chased-high fear syndrome terminally ill, almost impossible to buy at highs
2. **Refined Take-Profit Logic**: Not "sell when making money" but comprehensive judgment based on profit amount, RSI, trend, Pump
3. **Many Conditions But Organized**: 29 conditions classified clearly, switch on whichever you want
4. **Dual Timeframe**: 5 minutes execution, 1 hour see big trends, avoids false breakouts
5. **Dynamic Stop-Loss**: Profitable positions given ample room, loss positions over 50 minutes become aggressive

### ⚠️ Cons

1. **Too Many Parameters**: 200+ parameters — optimization can make you question your sanity
2. **High Computational Load**: 400 candle warm-up, multi-indicator calculations, old computers may lag
3. **Steep Learning Curve**: Understanding all conditions requires significant time
4. **Not Suitable for Manual Trading**: 5-minute timeframe + complex logic, can't keep up manually

---

## 7. Summary: What Do You Think of This Strategy?

### One-Line Rating
> "Complex to the point ofintense, but complexity is for smarter money-making — provided you have the patience to understand it."

### Who's It For?
- ✅ Quantitative traders with some experience
- ✅ People who like refined control
- ✅ People willing to spend time optimizing parameters
- ✅ People with decent hardware (8GB+ memory)

### Who's It NOT For?
- ❌ Quantitative beginners
- ❌ People wanting "one trick to make money forever"
- ❌ Manual traders (5-minute timeframe + complex logic, can't keep up)
- ❌ Old computer users (computational load will lag)

---

## ⚠️ Risk Re-Emphasis (Must Read This Section)

### Backtesting Looks Great, Live Trading Requires Caution

NFI46Z's historical backtesting performance is often **extremely impressive** — but there's a trap:

> **Because there are many parameters, the strategy can easily "fit" the optimal solution for past market conditions, but this doesn't mean it can definitely profit in the future.**

### My Recommendations

```
1. First backtesting, understand general performance
2. Then dry-run, at least 1-2 weeks
3. Small-funds live test, confirm stability
4. Don't go all-in right away, even the best strategy needs a break-in period
5. Regularly check live performance, adjust promptly if deviations found
```

**Remember**: No matter how good a strategy, the market won'tgive you a heads-up. Test with light positions — survival is most important!
