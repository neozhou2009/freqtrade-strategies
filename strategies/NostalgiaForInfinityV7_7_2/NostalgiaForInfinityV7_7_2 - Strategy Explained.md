# NostalgiaForInfinityV7_7_2 — Strategy Explained (Plain English)

> **Nickname**: The "Playboy" / Choice-Paralysis Terminally Ill  
> **Profession**: Crypto Trend Hunter (part-time "Flying-Knife Terminator")  
> **Timeframe**: 5 minutes + 1 hour dual vision

---

## 1. What Is This Strategy?

Simply put, **NostalgiaForInfinityV7_7_2** is:
- A strategy that designed **44 buy conditions** so it doesn't miss any opportunity
- A strategy with a **graded profit-taking system** so it doesn't sell too early
- A strategy that gave each buy condition **"five-layer insurance"** so it doesn't lose

Like an old veteran who checks a potential partner's family history, inspects a house 30 times, and gets an appraisal — **cautious to the point of suffocation, but genuinely reliable** 😂

This strategy is one of the most famous open-source strategies in the Freqtrade ecosystem. Its philosophy:

> **"Better to miss a thousand opportunities than to make one wrong trade"**

---

## 2. Core Configuration

### Profit-Taking Rules (ROI Table)

```
Immediate:    10% profit → get out!
After 30 min: 5% profit → get out!
After 60 min: 2% profit → get out!
```

**Translation**: Actually this ROI table is mostly decorative. The real profit-taking is all done by those complex custom logic functions. Like company regulations — hung up for show, but actual work is all "flexible handling" 😏

### Stop Loss Rules

```
Loss 10% → admit defeat, cut losses
Profit 3% → trailing stop activates → protect profits
```

**Translation**: You get 10% breathing room, but once you're profitable, you guard those profits like a miser.

### Startup Requirements

```
Needs 480 candles (40 hours) before it starts working
```

**Translation**: This strategy is an "observer." It watches the market for 40 hours, calculates all the indicators, and only then is willing to act. Impatient people may find it slow 🐢

---

## 3. The 44 Buy Conditions: Classified for You

This strategy's buy conditions are outrageously numerous. Here are 10 categories:

### 🎯 Category 1: Trend Confirmation (4 conditions)
**Core logic**: EMA alignment up, RSI pulls back to oversold zone before entering.

**Classic lines**: Condition 1, 9, 18, 23

---

### 📉 Category 2: BB Retest (8 conditions)
**Core logic**: Price touches Bollinger lower band, wait for bounce signal.

**Classic lines**: Condition 2, 3, 4, 5, 6, 14, 42, 43

---

### 📊 Category 3: SMA Deviation (6 conditions)
**Core logic**: Price deviates too much from MA, expect mean reversion.

**Classic lines**: Condition 10, 11, 12, 13, 22, 25

---

### 🌊 Category 4: EWO Oscillation (11 conditions)
**Core logic**: Elder Wave Oscillator gives oversold or trend signals.

**Classic lines**: Condition 12, 13, 16, 17, 22, 29, 30, 31, 34, 36, 44

---

### 🎢 Category 5: CTI Trend Strength (10 conditions)
**Core logic**: CTI (trend strength indicator) is extremely low = sufficient pullback.

**Classic lines**: Condition 1, 3, 7, 8, 18, 20, 21, 26, 27, 28

---

### 📉 Category 6: Williams %R (7 conditions)
**Core logic**: Williams %R oversold (very negative) = entry.

**Classic lines**: Condition 23, 26, 27, 38, 40, 41, 43

---

### ⚡ Category 7: Quick Mode (5 conditions)
**Core logic**: Simplified conditions for fast entry.

**Classic lines**: Condition 32, 33, 34, 35, 36

---

### 📈 Category 8: PMax Signal (4 conditions)
**Core logic**: Pmax (profit maximization indicator) gives signals.

**Classic lines**: Condition 35, 36, 37, 38

---

### 🎌 Category 9: Ichimoku (1 condition)
**Core logic**: Classic Ichimoku Cloud complete signal.

**Classic lines**: Condition 39

---

### 📊 Category 10: ZLEMA Cross (1 condition)
**Core logic**: Zero-lag EMA cross.

**Classic lines**: Condition 40

---

## 4. Protection Mechanisms: 44 Layers of "Anti-Fool" Design

Each buy condition has protection parameters — like giving each soldier helmets, body armor, knee pads, elbow pads...

| Protection Type | Role | Plain English |
|----------------|------|---------------|
| **EMA Trend Filter** | Check if EMA is above EMA200 | "Is the short-term trend up? Don't bottom-fish in a downtrend!" |
| **Price Position Filter** | Close must be above specified EMA | "Don't buy mid-air, need support!" |
| **SMA200 Rising** | SMA200 rose in last N periods | "Long-term trend is up, safety first!" |
| **Safe Dips** | Prevent catching falling knives | "Drop too big? Nah, let it fly for a bit 🪃" |
| **Safe Pump** | Prevent chasing at tops | "Rise too big? Cool off, don't be the bag holder!" |
| **BTC Trend Filter** | Only buy when BTC not falling | "Big brother (BTC) isn't stable, little brother don't move!" |

And Safe Dips has **13 levels** from "tight defense" to "lying flat and accepting it":
```
Level 10 (Most Conservative): Won't buy if drop exceeds 2%
Level 130 (Most Aggressive): Will buy even with 90% drop!
```

**Note**: This strategy has persecution paranoia? But in the crypto market where "50% drop in a day is normal operation," being cautious is not unreasonable 😅

---

## 5. Sell Logic: Flashier Than Buy

### 5.1 Graded Profit-Taking

```
Profit ≥ 20%   → Sell when RSI < 30 (let profits run a bit)
Profit 12%–20% → Sell when RSI < 42 (almost there)
Profit 10%–12% → Sell when RSI < 46 (lock in)
Profit 9%–10%  → Sell when RSI < 50 (a little is enough)
...
Profit 1.2%–2% → Sell when RSI < 34 + CMF<0 (small profit, watch indicators too)
```

**Plain English**:
- More profit → calmer mindset, let RSI run higher before selling
- Less profit → nervous, sell as soon as RSI drops a bit
- CMF<0 → money flowing out, sell even small profits

Like playing mahjong:
> Winning big = lucky hand, play more rounds; winning small = pocket profits and quit! 🀄

### 5.2 Bear Market Profit-Taking (Below EMA200)

In a bear market, profit-taking is more aggressive:

```
Profit 9%–10%: RSI < 52 OR RSI > 82 → sell!
Profit 7%–8%: RSI < 54 OR RSI > 80 → sell!
```

**Plain English**:
> "In a bear market, rebounds can end anytime. RSI high = run, RSI low = also run — just run faster! 🏃"

### 5.3 Pump Special Profit-Taking

```
If 48h rise > 90% (pumped coin):
  Profit ≥ 20%  → Sell when RSI < 30
  Profit 10%–20% → Sell when RSI < 34
  ...
  Profit 1%–2%  → Sell when RSI < 34
```

**Plain English**:
> "This coin surged too hard, could crash anytime. Even just 1% profit, RSI drops = run! 🚀"

### 5.4 Special Scenario Exits

| Scenario | Trigger | Plain English |
|---------|---------|---------------|
| **Trailing Stop 1** | Profit 3%–5% + RSI 10–20 + drawdown > 5% | "Made some, RSI quiet, but drawdown big — protect the principal!" |
| **Trailing Stop 2** | Profit 10%–40% + drawdown > 3% | "Killing it! Drop 3% = lock in!" |
| **Recovery Exit** | Max loss > 12%, now profit 6% | "Survived the worst, now profitable? Run!" |
| **Long Holding Exit** | Profit 3%–4% + holding > 15 hours | "Held too long, small profit = run, capital needs to flow!" |
| **Pump Fast Exit** | Pump + Profit 7%–20% + holding < 30 min | "Bought and immediately made this much? Run, something's fishy!" |

---

## 6. Strategy Pros & Cons

### ✅ Pros

1. **Defensive to the extreme**: 44 protection layers — almost impossible to enter at wrong time (unless you intentionally disable all protection 😅)
2. **Rich signal types**: Trend-following, mean reversion, BB retest, Ichimoku Cloud... whatever type you want, it's here
3. **Very smart profit-taking**: Graded profit-taking + trailing stop + special scenario exits won't let you experience "profit rollercoaster"
4. **Community validated**: Most famous open-source strategy in Freqtrade, extensively real-trader tested
5. **Highly customizable**: Each of the 44 conditions independently switchable

### ⚠️ Cons

1. **Complex to the point of tears**: 4000+ lines of code, 44 buy conditions — understanding alone takes days. Beginners see it and just quit 😭
2. **High computation**: Needs 480 candles preheat, calculates tons of indicators. Old computers may freeze into PPT 💻
3. **Overfitting risk**: So many parameters, easily "memorizes answers" — perfect on history, terrible on future 📚
4. **Backtest deception**: Usually backtest looks amazing, but live can be way worse (slippage, delays, liquidity issues)
5. **Steep learning curve**: To fully understand this strategy, 1–2 months minimum

---

## 7. When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|---------------|--------|
| 📈 Slow bull | Use trend confirmation conditions | Trend up, pullbacks are opportunities |
| 🔄 Choppy | Use BB retest conditions | High volatility, more reversion opportunities |
| 📉 Bear | Reduce condition count | Fewer signals, low capital efficiency |
| ⚡️ Pumped coins | Be careful with safe_pump | Might miss strong coins |
| 😴 Sideways | Not recommended | Signals too sparse, capital idle |

---

## 8. ⚠️ Risk Reminder (Must Read!)

### Backtests Look Great — Live Trading Requires Caution

NostalgiaForInfinityV7_7_2's historical backtest performance is often **extremely impressive** — but there's a trap:

> **With so many parameters, the strategy easily "fits" past market optimal solutions, but doesn't guarantee future profitability.**

In simple terms: **A student who memorized past exam answers, but the new exam has completely different questions! 📚**

### Hidden Risks

- **Calculation timeout**: Too many indicators, processing can't keep up
- **Signal delay**: All protection conditions confirmed, price already moved
- **Overly conservative**: Protections too strict, missing opportunities
- **Maintenance nightmare**: Something breaks, no idea which condition failed

### My Suggestions

```
1. Don't directly use all 44 conditions
2. Select a condition subset you understand (5–10 conditions)
3. Test in simulated environment for at least 1 month
4. Test with small capital live, scale up gradually
5. Review regularly, don't "set and forget"
```

**Remember**: No matter how great a strategy, the market doesn't care. Small position testing, survival is paramount! 🙏

---

*This strategy is a great open-source project. Author iterativ team put in massive effort. Using this strategy is paying respects to open-source spirit. But respect aside, money is your own — use cautiously!*
