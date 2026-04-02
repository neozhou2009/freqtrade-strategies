# BigZ07: A "Low Drawdown, Fast In Fast Out" Trader

> **Nickname**: Bargain Hunter Gen 7  
> **Profession**: Quant world's "cautious type" — try to lose less, earn when there's opportunity  
> **Timeframe**: 5 minutes + 1 hour

---

## 1. What's This Thing?

BigZ07 is a **low drawdown, fast in fast out** quantitative trading strategy.

In plain English:
- It specializes in finds **dropped coins** to buy (buy at valleys)
- Runs after earning **2-3 points** (sell quickly)
- Its slogan is: **Try to lose less, earn when there's opportunity**

This strategy has **14 entry conditions**, like 14 different keys, as long as any one is satisfied, can open the door and enter.

---

## 2. Core Settings: Plainly Speaking It's "Run Fast"

### Profit-Taking Rules (ROI Table)

```
Just bought:    Run at 2.8% profit
After 10 min:   Run at 1.8% profit
After 40 min:   Run at 0.5% profit (even mosquito meat eat!)
After 180 min:  Run at 1.8% profit
```

**Translation**: This strategy **willing to sell at 0.5%**! Think it's too conservative? Yep, that's the design philosophy — **earn and run, don't be greedy**.

### Stoploss Rules

```
Traditional stoploss: -99% (turned off)
Custom stoploss: Has complex logic
Trailing stop: Dynamically adjusts after profiting
```

**Translation**: Don't look at traditional stoploss being off,they has smarter custom stoploss logic.

---

## 3. 14 Entry Conditions: I've Categorized Them for You

This strategy has 14 entry conditions, I've grouped them into 4 categories for you:

### 🎯 Category 1: RSI Oversold Faction (Conditions 0,3,8,9)
**Core Logic**: RSI low means oversold, buy!

**In Plain English**:
> "Dropped too much, time to rebound right?"

**Classic Lines**:
- Condition #0: `5-minute RSI < 30 + Price above EMA200` → "Big trend still there, short-term oversold"
- Condition #3: `5-minute RSI < 14 + 1-hour candles above EMA200` → "Extreme oversold, big cycle still there"
- Condition #8: `1-hour RSI < 20 + 5-minute RSI < 28` → "Big small cycles both oversold"
- Condition #9: `5-minute RSI < 10` → "Extremely oversold!"

### 📉 Category 2: Bollinger Band Faction (Conditions 1,2,5,12)
**Core Logic**: Price dropped to Bollinger lower rail

**In Plain English**:
> "Dropped to support level, buy!"

**Classic Lines**:
- Condition #1: `Close below Bollinger lower rail + Bearish candle + Volume contracting` → "Broke support, shrinking volume"
- Condition #5: `MACD golden cross + Price touches Bollinger lower rail` → "MACD turned bullish, price low"
- Condition #12: `Low breaks Bollinger lower rail + Volume contracting` → "Broke then shrinking volume"

### 🔧 Category 3: MACD Faction (Conditions 10,11)
**Core Logic**: Momentum turning strong

**In Plain English**:
> "MACD starting to exert force, buy!"

**Classic Lines**:
- Condition #10: `1-hour Bollinger lower rail + MACD histogram turns from negative to positive + 5-minute RSI low` → "Big cycle rebound signal"
- Condition #11: `MACD positive for 5 consecutive periods + Bollinger Band narrowing + RSI > 51` → "Consolidation complete, about to explode"

### 🌟 Category 4: Capital Flow Faction (Condition 13)
**Core Logic**: Rebound after massive capital outflow

**In Plain English**:
> "Panic selling, it's a big bottom!"

**Classic Lines**:
- Condition #13: `CMF < -0.435 + RSI < 22` → "Capital massively outflowed, oversold rebound"

These 14 conditions are like 14 keys, as long as one can unlock the door, the strategy enters! 🤣

---

## 4. Protection Mechanisms: Custom Stoploss is Core

BigZ07's core protection is **custom stoploss**, this logic is very smart:

- Monitors holding time
- Checks RSI levels
- Considers price position relative to EMA200

**In Plain English**: Won't blindly cut, judges based on market conditions.

---

## 5. Exit Logic: Relies on ROI and Stoploss

Strategy doesn't have active exit signals, mainly relies on:

| Exit Method | Trigger | Plain English |
|------------|---------|---------------|
| ROI | Time-based profit targets | "Run when reaching the point" |
| Trailing Stop | Pullback after profiting | "Don't give back what earned" |
| Custom Stoploss | Intelligent judgment | "Smart cutting" |

---

## 6. This Strategy's "Personality Traits"

### ✅ Advantages
1. Low drawdown design
2. 14 entry conditions provide variety
3. Fast turnover
4. Multi-timeframe analysis

### ⚠️ Disadvantages
1. May exit too early in bull markets
2. Complex stoploss logic
3. Requires understanding

---

## 7. Suitable Scenarios

| Market | Recommendation | Reason |
|--------|---------------|--------|
| Oscillating | ✅ Strong | Strategy excels here |
| High volatility | ✅ Recommended | Good for crypto |
| Strong bull | ⚠️ Caution | May exit early |
| Continuous decline | ❌ Not recommended | May face losses |

---

## 8. Summary

### One Sentence
> "A cautious trader that buys dips and sells fast."

### Who Should Use
- ✅ Risk-averse investors
- ✅ Short-term traders
- ✅ People who like dip buying

### Who Shouldn't Use
- ❌ Bull market chasers
- ❌ Long-term holders
- ❌ Aggressive traders

---

## 9. ⚠️ Risk Reminder

Fast-exit design means limited profits. Paper trade first, start small, understand the logic!

Surviving is most important! 🙏
