# BigZ04_TSL4: A "Afraid of Loss but Wants to Earn" Strategy

> **Nickname**: Conservative Bottom Fisher  
> **Profession**: Quant world's "Art of War" type player — first seek not to lose, then seek to win  
> **Timeframe**: 5 minutes + 1 hour

---

## 1. What's This Thing?

Simply put, BigZ04_TSL4 is **a "afraid of loss but wants to earn" strategy**.

Its core thinking:
1. Only buy when price drops near Bollinger Band lower rail (pick up bargains)
2. Set 8% hard stoploss after buying (max lose 8%)
3. If making money, start trailing take-profit, lock more profits as price rises

This strategy is "Art of War" type — **first seek not to lose, then seek to win**.

---

## 2. Core Settings: Plainly Speaking It's "Survival First"

### Profit-Taking Rules (Trailing Take-Profit)

```
Profit < 1.6%: Stoploss = -8% (hard stoploss)
Profit 1.6%-8%: Stoploss = Linear interpolation (from 1.1% to 4%)
Profit > 8%: Stoploss = 4% + (Profit - 8%) (lock at least 4%)
```

**Translation**: The more you earn, the higher the stoploss, absolutely won't lose principal!

### Stoploss Rules

```
Hard stoploss: -8% (must cut and run when losing 8%)
Trailing take-profit: Starts protection after profit exceeds 1.6%
```

**Translation**: Max lose 8%, lock profits when earned, never let profits turn into losses.

---

## 3. 14 Entry Conditions: I've Categorized Them for You

This strategy has 14 entry conditions, core logic is **finding opportunities where price pulls back to Bollinger Band lower rail during uptrends**, I've grouped them into 5 categories for you:

### 🎯 Category 1: Bollinger Band Dip Buy (Conditions 0-2)
**Core Logic**: Price dropped to Bollinger lower rail, buy!

**In Plain English**:
> "Price dropped to Bollinger Band lower rail, buy!"

**Classic Lines**:
- Condition #0: `Close > 200-day MA + Price touches Bollinger lower rail + Volume contracting` → "Trend upward, dropped to support, go!"
- Condition #1: `Close < Bollinger lower rail + 1-hour RSI < 69` → "Broke support, RSI also low, safety margin enough"

### 📉 Category 2: RSI Oversold (Conditions 3-4)
**Core Logic**: RSI low means oversold

**In Plain English**:
> "Dropped too much, time to rebound right?"

**Classic Lines**:
- Condition #3: `RSI < 15 + Price at Bollinger lower rail` → "Extreme oversold, high rebound probability"
- Condition #4: `1-hour RSI < 20 + Price at Bollinger lower rail` → "Big cycle also oversold, safer"

### 🔧 Category 3: MACD Golden Cross (Conditions 5-7)
**Core Logic**: Momentum turning strong + oversold position

**In Plain English**:
> "MACD just golden crossed, moving averages also bullish, buy!"

**Classic Lines**:
- Condition #5: `EMA26 > EMA12 + MACD bar > 0 + Price at Bollinger lower rail` → "MACD turned bullish, price low, enter"

### 🌟 Category 4: Pure RSI Bargain Hunting (Conditions 8-9)
**Core Logic**: Both cycle RSI oversold

**In Plain English**:
> "Both cycle RSI oversold, bet on rebound"

**Classic Lines**:
- Condition #8: `1-hour RSI < 20 + 5-minute RSI < 28` → "Big small cycles both oversold, resonance signal"

### ⚡ Category 5: Advanced Combo (Conditions 10-12)
**Core Logic**: Multi-indicator resonance

**In Plain English**:
> "All signals met, buy!"

**Classic Lines**:
- Condition #10: `1-hour Bollinger lower rail + MACD turned positive + 5-minute RSI low` → "Big cycle level rebound signal"
- Condition #11: `MACD positive for 5 consecutive periods + Bollinger Band narrowing + RSI > 51` → "Consolidation complete, about to breakout"
- Condition #12: `Ground volume reversal` → "Volume shrunk to ice point, about to change"

These 14 conditions are like 14 keys, as long as one can unlock the door, the strategy enters! 🤣

---

## 4. Protection Mechanisms: 3 Layers of "Bulletproof Vest"

Each entry condition comes with a set of protection parameters, like wearing 3 layers of bulletproof vest:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| Hard Stoploss | Run when losing 8% | "Max lose 8%, can't be more" |
| Dynamic Take-Profit | Lock more profits as price rises | "Can't give back what earned" |
| Volume Filter | Must contract volume to buy | "Don't catch falling knives, wait until can't sell then buy" |

This protection mechanism basically took "afraid of loss" to the extreme! 🤣

---

## 5. Exit Logic: Simpler Than Entry

### 5.1 This Strategy Almost Doesn't Use Exit Signals!

Strategy set exit conditions but actual effect limited, mainly relies on:

| Exit Method | Trigger Condition | Plain English |
|------------|------------------|---------------|
| Hard Stoploss | Lose to 8% | "Lost enough, run" |
| Trailing Take-Profit | Dynamically lock after profiting | "Don't give back what earned" |

**One sentence: Entry relies on signals, exit relies on stoploss.**

---

## 6. This Strategy's "Personality Traits"

### ✅ Advantages (Praise Session)

1. **Cautious**: 14 filters, reduces false signals
2. **Conservative**: 8% hard stoploss, has loss ceiling
3. **Greedy with Limits**: Dynamic take-profit, locks more as earns more
4. **Buddhist Style**: Doesn't need to watch market daily

### ⚠️ Disadvantages (Roast Session)

1. **Doesn't Earn Enough in Bull Markets**: May sell early, miss subsequent gains
2. **Too Many Conditions**: 14 conditions, easy to overfit
3. **Not Suitable for One-Sided Markets**: Will miss out in surge, will stoploss in crash

---

## 7. Suitable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Oscillating market | ✅ Strongly recommend | Strategy excels in range-bound markets |
| Moderate volatility | ✅ Recommended | Suitable for normal volatility |
| Trend pullbacks | ✅ Recommended | Good at capturing pullback opportunities |
| Strong bull market | ⚠️ Caution | May exit too early |
| Extreme volatility | ❌ Not recommended | Hard stoploss may trigger frequently |

---

## 8. Summary: How's This Strategy Anyway?

### One Sentence Evaluation
> "A 'first seek not to lose, then seek to win' conservative strategy."

### Who Should Use It?
- ✅ Conservative investors who prioritize capital protection
- ✅ Traders who like oscillating markets
- ✅ People who can accept missing some bull market gains
- ✅ Those who want automated stoploss protection

### Who Shouldn't Use It?
- ❌ Those wanting to catch every bull market gain
- ❌ Aggressive traders
- ❌ People unwilling to accept conservative returns
- ❌ Those who don't understand stoploss mechanisms

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Build Defense with "Hard Stoploss + Trailing"

BigZ04_TSL4 is grid/trend hybrid strategy. Core thinking is: **buy at dips, protect with stoploss, lock profits with trailing**.

**Its money-making philosophy**: Capital protection first, profits second

- **Don't chase rises**: Only buy near Bollinger Band lower rail
- **Has loss ceiling**: Max lose 8%, no more
- **Locks profits**: Trailing ensures profits don't turn into losses

### 9.2 Different Market Performance (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Oscillating market | ⭐⭐⭐⭐⭐ | Best environment, repeatedly eat the spread |
| 🔄 Moderate volatility | ⭐⭐⭐⭐ | Suitable for normal conditions |
| 📉 Strong bull market | ⭐⭐ | May exit too early, miss gains |
| ⚡️ Extreme volatility | ⭐⭐ | Stoploss may trigger frequently |

**One sentence summary**: Oscillating market is home court, be careful in one-sided markets.

---

## 10. Want to Run This Strategy? First Look at These Configs

### 10.1 Trading Pair Configuration

| Config Item | Suggested Value | Roast |
|-------------|-----------------|-------|
| Simultaneous positions | 2-4 | Too few not enough opportunities, too many can't watch |
| Trading pairs | Major coins (BTC/ETH) | Don't touch small coins, poor liquidity |
| Timeframe | 5 minutes + 1 hour | Don't change, already tuned |

### 10.2 Configuration File Key Settings

```yaml
max_open_trades: 3
stake_amount: "unlimited"
dry_run_wallet: 1000
```

---

## 11. Finally Finally

### One Sentence Evaluation
> "A conservative strategy suitable for investors who prioritize capital protection."

### Who Should Use It?
- ✅ Conservative investors
- ✅ Oscillating market traders
- ✅ People who want stoploss protection
- ✅ Those who accept moderate returns

### Who Shouldn't Use It?
- ❌ Aggressive traders
- ❌ Bull market chasers
- ❌ People unwilling to learn

---

## 12. ⚠️ Risk Reminder Again (Must Read This Part)

### Conservative Design Trade-offs

BigZ04_TSL4's conservative design has trade-offs:

> **Capital protection comes at the cost of potential gains.**

Simple put: **You won't lose big, but also won't make big.**

### Hidden Risks

During live trading:
- **May underperform in bull markets**: Exits too early
- **Stoploss may trigger in crashes**: 8% loss per trade
- **Requires monitoring**: Need to watch performance

### My Suggestions (True Words)

```
1. Paper trade at least 1 month first
2. Start with small capital
3. Understand the stoploss logic thoroughly
4. Don't use in extreme bull markets
5. Diversify across strategies
```

**Remember**: No strategy is perfect. This one prioritizes survival over maximum gains. Choose based on your risk tolerance! 🙏
