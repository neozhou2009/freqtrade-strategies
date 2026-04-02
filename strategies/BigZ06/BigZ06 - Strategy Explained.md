# BigZ06: A "Scared of Death but Runs Fast" Trader

> **Nickname**: Quick Gunman  
> **Profession**: Quant world's "Escape Master" — earn a bit and run, never linger  
> **Timeframe**: 5 minutes + 1 hour

---

## 1. What's This Thing?

**BigZ06 = A "scared of death" but "runs fast" trader**

This strategy's founder ilya (a foreign programmer) got scared by crypto markets, designed this strategy. Its core thinking has three points:

1. **Buy during dips** — Don't chase rises, bottom fish
2. **Run after rising** — Don't be greedy, take profits and run
3. **Run fast, don't get stuck** — Don't stubbornly hold when losing, decide whether to cut within 50 minutes

Simply put: **Buy low sell fast, not greedy, desperately control drawdown**.

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
Traditional stoploss: -99% (not really 99% stoploss!)
Custom stoploss: Starts judging after 50 minutes
Trailing stop: Starts after 2.5% profit, run if pullback 1%
```

**Translation**: Don't look at traditional stoploss being off,they have smarter stoploss methods — give you 50 minutes to perform, if not then cut.

---

## 3. 14 Entry Conditions: I've Categorized Them for You

This strategy has 14 entry conditions, simply understand as **judging "whether dropped enough" from 14 different angles**, I've grouped them into 4 categories for you:

### 🎯 Category 1: RSI Oversold Faction (Conditions 0,3,8,9)
**Core Logic**: RSI low means oversold

**In Plain English**:
> "Dropped too much, time to rebound right?"

**Classic Lines**:
- Condition #0: `5-minute RSI < 30 + Past 3 candles declining` → "Dropped hard, rebound imminent"
- Condition #3: `RSI < 14 + Price at Bollinger lower rail` → "Extreme oversold, buy!"
- Condition #8: `1-hour RSI < 20 + 5-minute RSI < 28` → "Big small cycles both oversold"
- Condition #9: `5-minute RSI only 10` → "Extremely oversold, extremely high rebound probability!"

### 📉 Category 2: Bollinger Band Faction (Conditions 1,2,5,12)
**Core Logic**: Price dropped to Bollinger lower rail

**In Plain English**:
> "Dropped to support level, buy!"

**Classic Lines**:
- Condition #1: `Price touches Bollinger lower rail + Volume contracting` → "Selling exhausted, about to rebound"
- Condition #5: `MACD golden cross + Price at Bollinger lower rail` → "MACD turned bullish, price low, enter"
- Condition #12: `Price briefly pierces Bollinger lower rail then recovers` → "False breakout then reversal"

### 🔧 Category 3: MACD Faction (Conditions 10,11)
**Core Logic**: Momentum turning strong

**In Plain English**:
> "MACD starting to exert force, buy!"

**Classic Lines**:
- Condition #10: `1-hour Bollinger lower rail + MACD histogram turns from negative to positive` → "Big cycle rebound signal"
- Condition #11: `Bollinger Band narrowing + MACD positive for 5 consecutive candles + RSI > 51` → "Consolidation complete, about to explode"

### 🌟 Category 4: Capital Flow Faction (Condition 13)
**Core Logic**: Rebound after massive capital outflow

**In Plain English**:
> "Panic selling, it's a big bottom!"

**Classic Lines**:
- Condition #13: `CMF < -0.435 + RSI < 22 + Long-term trend upward` → "Capital massively outflowed, oversold rebound"

These 14 conditions are like 14 keys, as long as one can unlock the door, the strategy enters! 🤣

---

## 4. Protection Mechanisms: 3 Layers of "Bulletproof Vest"

Each entry condition comes with a set of protection parameters, like wearing 3 layers of bulletproof vest:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| Entry Filter | Must contract volume + above EMA200 | "Don't catch falling knives, bottom fish with trend" |
| 50-Minute Time Stoploss | Starts judging after holding over 50 minutes and still losing | "Give you 50 minutes to perform, if not then cut" |
| Trailing Stoploss | Mobile stoploss starts after profiting | "Don't give back what earned" |

**50-Minute Stoploss Logic**: This is the most unique design!

```
Holding over 50 minutes still losing money → Forced check:
├─ If 1-hour RSI still below 40 → Don't cut, wait for reversal
├─ If price dropped more than 3.5% below opening → Cut! Lose 1%
└─ If price dropped more than 2.5% below opening → Cut! Lose 1%
```

**In Plain English**: After 50 minutes either rebound or admit 1% loss and run, absolutely don't keep holding. 🤣

---

## 5. Exit Logic: More Buddhist Than Entry

### 5.1 Three Exit Methods

| Exit Method | Trigger Condition | Plain English |
|------------|------------------|---------------|
| Touches Bollinger Middle Rail | Closing price exceeds Bollinger middle rail | "Sell when rises to middle position" |
| Ladder ROI | Sell by time ladder | "Run when reaching the point" |
| Only Profit Not Loss | Only sell when profitable | "Wait for stoploss when losing" |

### 5.2 Ladder Take-Profit Table

```
Just bought → Run at 2.8% profit
After 10 min → Run at 1.8% profit
After 40 min → Run at 0.5% profit
After 180 min → Run at 1.8% profit
```

**In Plain English**: Willing to sell at 0.5%, shows really "afraid of greed"!

---

## 6. This Strategy's "Personality Traits"

### ✅ Advantages (Praise Session)

1. **Scared of Death**: Sets up layers of protection, wants to run at slightest wind
2. **Not Greedy**: Willing to run at 0.5%, absolutely doesn't linger
3. **Specializes in Picking Soft Persimmons**: Only buys oversold coins

### ⚠️ Disadvantages (Roast Session)

1. **Doesn't Earn Enough in Bull Markets**: Sells too early, misses big gains
2. **Complex Conditions**: 14 conditions, hard to understand
3. **Not Suitable for Strong Trends**: May underperform in one-sided markets

---

## 7. Suitable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Oscillating market | ✅ Strongly recommend | Strategy excels in range-bound conditions |
| High volatility | ✅ Recommended | Well-suited for volatile markets |
| Dip buying | ✅ Recommended | Excellent at capturing rebounds |
| Strong bull market | ⚠️ Caution | May exit too early |
| Continuous decline | ❌ Not recommended | May face consecutive losses |

---

## 8. Summary: How's This Strategy Anyway?

### One Sentence Evaluation
> "A 'scared of death but runs fast' short-term trader."

### Who Should Use It?
- ✅ Investors who prioritize drawdown control
- ✅ Short-term trading enthusiasts
- ✅ People who like dip buying
- ✅ Those who can accept "sold and still rising"

### Who Shouldn't Use It?
- ❌ Those wanting to catch every bull market gain
- ❌ Long-term holders
- ❌ Aggressive traders
- ❌ People unwilling to learn

---

## 9. ⚠️ Risk Reminder Again

BigZ06's fast-exit design means limited profits per trade. The strategy prioritizes survival over maximum gains.

**Remember**: 
- Paper trade first
- Start with small capital
- Understand the 50-minute stoploss logic
- Don't use all funds on one strategy

Surviving is most important! 🙏
