# Combined_NFIv7_SMA_bAdBoY_20211204 Strategy: NFI Series' Old Fox

> **Nickname**: Old Fox · Pullback Hunter
> **Profession**: Multi-Condition Trend Hunter + Bollinger Band Rebound Pro
> **Timeframe**: 5 Minutes Main + 1 Hour Observation

---

## 1. What's This Strategy?

Simply put, **Combined_NFIv7_SMA_bAdBoY_20211204** is:
- 26 buy conditions, pick whichever fits
- 8 sell conditions gatekeeping every move
- 8 protection mechanisms built in

Like a **dating market veteran** — not only checks education (EMA protection), also family background (SMA200 trend), also asks about family of origin (dip protection), afraid of finding a "drain family" (rising sharply after buying) 🤣

---

## 2. Core Settings: "Give Trends Enough Room to Run"

### Take-Profit Rules (ROI Table)

```
Immediately run: 10%
After 30 min: 5%
After 60 min: 2%
```

**Translation**: Start with 10%? This strategy has big appetite! But after 1 hour drops to 2% — it wants you to hold and let the trend run~

### Stop-Loss Rules

```
Hard stop: -10%
Trailing stop: Activates after 3% rise, can lock more profits
```

**Translation**: -10% to cut? How patient! Trailing stop is even sneakier — can keep locking profits as it rises, wants both and also more 😅

---

## 3. 26 Buy Conditions: Let Me Sort Them Out

Too many to count. I've grouped them into 4 categories:

### 🎯 Category 1: Trend Start Type (Conditions 1-6)
**Core Logic**: EMA golden cross + Bollinger Band rebound + strict dip protection

**Plain English**:
> "Young one, trend just started, I'm not too late to enter!"

### 📈 Category 2: Momentum Acceleration Type (Conditions 7-14)
**Core Logic**: EWO momentum oscillator + volume confirmation + loose protection

**Plain English**:
> "This wave has momentum, I'll catch a ride!"

### 🛡️ Category 3: Trend Confirmation Type (Conditions 15-24)
**Core Logic**: SMA200 long-term trend + multi-timeframe confirmation

**Plain English**:
> "Daily chart trend is stable, I'll grab a bite!"

### 🔮 Category 4: Special Signal Type (Conditions 25-26)
**Core Logic**: ZEMA zero-lag MA + custom parameters

**Plain English**:
> "I use black-tech MA, what can you do?"

---

## 4. Protection Mechanisms: 8 Layers of "Armor"

| Protection Type | Role | Plain English |
|----------------|-------|---------------|
| **EMA Fast/Slow Protection** | Confirm short-term trend direction | "MA in bullish alignment before entering" |
| **SMA200 Rising** | Long-term trend confirmation | "200-day line going up I believe" |
| **Safe Dips** | Filter excessive drops | "Don't bottom-fish at mid-slope" |
| **Safe Pump** | Filter sharp rises | "Don't chase to the last baton" |
| **Dip Levels (10-110)** | How deep a fall is safe | "Higher level = braver to catch falling knives" |
| **Pump Levels (10-120)** | How much rise is abnormal | "Higher level = braver to buy tops" |

> This strategy really does **"check three generations"**, cautious to the max! But cautious is good — survival is most important 😅

---

## 5. Exit Logic: Fancier Than Entry

### 5.1 Basic Sell Signals (8)

**Classic Lines**:

1. **Signal #1 - RSI Overbought + Bollinger Band Break**:
   > "RSI surged past 70+, and price has been above the Bollinger upper band for 5 consecutive candles — run now!"

2. **Signal #2 - Dual RSI Overbought**:
   > "Both 5-minute and 1-hour RSI are at 70+?"

3. **Signal #3 - RSI Single Overbought**:
   > "RSI firmly broke above the threshold — run!"

4. **Signal #4 - Dual-Timeframe Momentum Divergence**:
   > "Both timeframes RSI are high together — isn't this divergence?"

---

### 5.2 Custom Stop-Loss: Varieties of Cutting Losses

| Scenario | Trigger | Signal Name |
|---------|---------|------------|
| Below EMA200 but RSI okay | Profit negative + Close<EMA200 + RSI above 1h | signal_stoploss_u_1 |
| Long-Holding Recovery | Holding>20 hours + Profit-8%~-4% + RSI strong | signal_stoploss_l_r_u_1 |
| Pump Protection Stop-Loss | 48h pump + Below EMA200 | signal_stoploss_p_2 |

---

### 5.3 Trailing Stop: Climbing Stop-Loss

- **Standard Trailing**: After >3% profit activates, can lock up to 60% profit
- **Below EMA200 Trailing**: Activates when price drops below EMA200
- **Long-Holding Trailing**: Special care for positions over 15 hours

---

## 6. The Strategy's "Personality Traits"

### ✅ Pros

1. **Many Conditions = Many Choices**: 26 buy conditions, always one fits the current market
2. **Many Protections = Die Less**: 8 layers, whatever happens some capital gets protected
3. **Dual Timeframe**: 1h confirms trend, 5m seizes opportunities, stable!
4. **Strong Trend-Following**: -10% to cut, gives trends sufficient room

### ⚠️ Cons

1. **Many Conditions = Eyes Glaze Over**: 26 conditions, ordinary people don't know which to enable
2. **Complex Parameters**: Hundreds of protection parameters, optimization drives you crazy
3. **Low Trading Frequency**: Too strict, many signals filtered out
4. **Eats Hardware**: Multi-timeframe + many indicators, VPS RAM must be enough

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|---------------------|--------|
| 🐂 Bull Market Up | Normal use | Clear trend, buy one accurate one |
| 📈 Drop Rebound | Reduce position | Rebound also eats, but don't be greedy |
| 🔄 Volatile Market | Reduce trading pairs | Easily slapped repeatedly |
| 💥 Wild Surge/Drop | Recommend pause | Pump protection too sensitive |

---

## 8. Summary

### One-Line Verdict
> **"NFI series' old fox, 26 conditions 8 protections, cautious to the point of making you anxious, but survival is most important!"**

### Who Should Use?
- ✅ Experienced quantitative traders (can read parameters)
- ✅ Trend followers (willing to hold long)
- ✅ Risk-conscious people (more protection = die less)
- ✅ Large capital players (40-80 trading pairs)

### Who Should NOT?
- ❌ Beginner novices (parameters too complex)
- ❌ Impatient people (low trading frequency)
- ❌ Small capital people
- ❌ High-frequency traders (not cut out for it)

---

## 9. What Markets Does It Make Money In?

### 9.1 Core Logic: Building "Defense Net" with Complexity

NFI series is **quantitative "playboy"** — 26 buy conditions means **26 dating candidates**, one by one interview, always one succeeds!

**Its Money Philosophy**:
- **Multi-Confirmation**: Not one family doesn't enter one door, trend right, indicators right, protections right
- **Trend Is King**: Don't care about one or two points, want the whole trend
- **Survival Most Important**: More protection layers is never too many, miss than buy wrong

### 9.2 Performance by Market

| Market Type | Rating | Plain English |
|:------------|:-------|:--------------|
| 📈 Slow Bull | ⭐⭐⭐⭐⭐ | Lie down making money, trend rises position flies |
| 🔄 Volatile | ⭐⭐⭐☆☆ | Too strict, might miss some opportunities |
| 💥 Wild Surge | ⭐⭐☆☆☆ | Pump protection triggers, buys then deletes |
| 📉 Bear Market | ⭐⭐☆☆☆ | Hard to catch rebounds in downtrend |

**Bottom Line**: **Bull market all day, volatile survive, bear market stay away!**

---

## 10. ⚠️ Risk Re-Ememphasis (Must Read!)

### Backtesting Looks Great, Live Trading Different

Historical backtesting often **looks extremely good** — but:

> **With many parameters, easily "fits" past markets, doesn't guarantee future profitability.**

Simply put: **It memorized historical answers, but next exam questions are different!**

### Hidden Risks of Complex Strategies

- **Signal Delay**: Too much computing, candle missed
- **Over-Protection**: Too strict, good opportunities filtered
- **Overfitting**: Historical perfect, live flop
- **Hardware Dependent**: VPS RAM insufficient, directly goes on strike

### My Suggestions

```
1. Paper trade 2 weeks first, don't rush live
2. Small money test, don't go all-in from the start
3. Periodic checks, market changes mean parameters may need adjustment
4. Take profits when available, don't dream of getting rich quick
5. Remember: survival is most important, as long as the green mountain stands, there is always firewood
```

**Remember**: No matter how good a strategy, the market teaches lessons without warning! Small position test, survival most important! 🙏

---

**Final Reminder**: This document is for reference only, not investment advice. Cryptocurrency trading carries big risk, enter cautiously!

---

> **Document Info**  
> **Strategy Source**: NostalgiaForInfinityV7 by iterativ  
> **Variant Version**: bAdBoY_20211204  
> **Creation Date**: 2021-12-04
