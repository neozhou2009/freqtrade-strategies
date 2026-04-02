# ema: The "Minimalist" EMA Cross Trader

> **Nickname**: Cross Man  
> **Profession**: Quant world's "minimalist" — if 4 EMAs can solve it, never use 5  
> **Timeframe**: 5 minutes (short-term player)

---

## 1. What's This Strategy?

Simply put, **ema** is:
- A strategy with only **2 indicators** (EMA + SMA)
- A strategy with **golden cross buy, death cross sell**
- A strategy with **only 60 lines of code** (super simple!)

Like a decisive buyer who only looks at one indicator: "EMA golden cross? Buy! Death cross? Sell!" ⚡

**Nickname origin**: Strategy is literally called "ema", so simple the name is the indicator name 😅

---

## 2. Core Settings: Simply "Golden Cross Buy, Death Cross Sell"

### Profit-Taking Rules (ROI Table)

```
Make 10% right after buying? → RUN!
Hold 30 minutes and make 5%? → RUN!
Hold 60 minutes and make 2%? → RUN!
```

**Translation**: This strategy is classic "trend-following thinking", 10% ROI is relatively high, expects to capture big trends!

### Stoploss Rules

```
Hard stoploss: Cut at 10% loss
Trailing stop: Activates after 2% profit, run if pulls back 1%
```

**Translation**: Trailing stop is the highlight, automatically follows price after making money!

---

## 3. Entry Conditions: Just 1 Condition

### 🎯 EMA Difference Golden Cross

**Core Logic**:
1. Calculate weighted combination of (EMA6-EMA24) and (EMA11-EMA25)
2. Calculate 29-period SMA of this combination as signal line
3. Buy on golden cross

**In Plain English**:
> "EMA difference crossed above signal line (golden cross), trend is here, get on!"

**Code Translation**:
```python
# EMA difference calculation (note: variable names differ from actual periods)
ema6 = EMA(9-period)    # Actual period 9
ema24 = EMA(18-period)  # Actual period 18
ema11 = EMA(32-period)  # Actual period 32
ema25 = EMA(64-period)  # Actual period 64

# EMA difference weighted combination
ema = (ema6 - ema24) * 0.6 + (ema11 - ema25) * 0.5

# Signal line
ema2 = SMA(ema, 29-period)

# Golden cross buy
Buy when ema crosses above ema2
```

**Roast**:
- Parameter naming is a bit messy, variable called ema6 actually uses 9-period 😅
- But core logic is simple: short-term EMA difference crosses above signal line = buy!

---

## 4. Protection: Trailing Stop Is the Highlight

This strategy's protection is simple but effective:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| **Hard Stoploss** | Cut at 10% loss | "Lost 10% means trend judgment wrong, run fast" |
| **Trailing Stop** | Auto-follows price after profit | "Activates after 2%, runs if pulls back 1%" |

**Trailing Stop Illustration**:
```
Profit
  ↑
10% ─ ─ ─ ─ ─ ─ ─ ─ ─┐
  │                    │
 5% ─ ─ ─ ─ ─ ─ ─ ─ ─┤ ← ROI exit point
  │                    │
 2% ─ ─ ─ ─ ─ ─ ─ ─ ─┤ ← Trailing activation point
  │                    │
 1% ─ ─ ─ ─ ─ ─ ─ ─ ─┤ ← Trailing trigger point
```

**Roast**: This strategy is "simple is beautiful" — no fancy protections, just trailing! 🤣

---

## 5. Exit Logic: As Simple As Entry

### 5.1 Technical Exit: Death Cross

**Trigger**:
```python
# Death cross exit
When ema crosses below ema2
```

**In Plain English**:
> "EMA difference crossed below signal line (death cross), trend is over, run!"

**Roast**: Entry is golden cross, exit is death cross — symmetric and elegant!

---

### 5.2 ROI Exit: 3-Level Take-Profit

```
Profit      Hold Time    Trigger Exit
─────────────────────────────────────
10%         Anytime      Run when reached (big profit)
5%          After 30 min Run when reached (medium profit)
2%          After 60 min Run when reached (small profit)
```

**In Plain English**:
- Make 10% right after buying? → Pie from heaven, run!
- Hold 30 minutes and make 5%? → Not bad, run!
- Hold 60 minutes and make 2%? → Small but OK, run!

---

## 6. This Strategy's "Personality Traits"

### ✅ Advantages (Praise Session)

1. **Simplicity**: Only EMA and SMA, easy to understand
2. **Dual confirmation**: Short and medium-term differences confirm each other
3. **Signal smoothing**: SMA reduces false signals from noise
4. **Trend-following**: Captures large trends with high ROI
5. **Trailing stop**: Lets profits run while protecting gains

### ⚠️ Disadvantages (Roast Session)

1. **No trend filter**: No higher timeframe trend confirmation
2. **No BTC correlation**: Doesn't know when Bitcoin crashes
3. **Parameter naming confusion**: Variable names don't match actual periods
4. **Lag**: EMA/SMA combination has inherent lag
5. **Ranging losses**: May lose in sideways markets

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **Strong uptrend** | Default configuration | EMA cross captures trends well |
| **Ranging market** | Pause or light position | May have many false signals |
| **Downtrend** | Pause | Strategy only goes long |
| **High volatility** | Adjust stoploss | May need wider stoploss |
| **Low volatility** | Adjust ROI | May need lower ROI thresholds |
| **BTC crash** | Pause | Big brother crashed, watch first |

---

## 8. Summary: How's This Strategy?

### One-Sentence Review
> **"A minimalist EMA cross strategy with dual difference confirmation and trailing stop"**

### Who Should Use It?
- ✅ People who like simple strategies
- ✅ People learning EMA cross strategies
- ✅ People with quantitative foundation
- ✅ Friends who understand trend-following

### Who Should NOT Use It?
- ❌ People who want complex strategies (this is too simple)
- ❌ People who don't understand EMA lag
- ❌ People unwilling to accept ranging losses
- ❌ Pure newbies (need to understand trend-following first)

### My Recommendations
1. **Understand EMA lag**: Moving averages have inherent lag
2. **Accept ranging losses**: Trend strategies lose in sideways
3. **Dry-run test**: Test at least 1-2 weeks before live trading
4. **Start small**: Begin with small capital, increase after confirming stability
5. **Consider adding filter**: Add higher timeframe trend filter for protection

---

## 9. What Markets Make Money with This Strategy?

### 9.1 Core Logic: EMA Cross + Signal Line

ema is a **trend-following strategy**. Its core philosophy is:

> "Moving averages cross = trend change. Golden cross = buy, death cross = sell. Simple!"

- **EMA faith**: Exponential moving averages react faster than SMA
- **Dual difference faith**: Short + medium confirm each other
- **Trend-following faith**: Cut losses, let profits run

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Strong uptrend | ⭐⭐⭐⭐☆ | EMA cross captures trends well |
| 🔄 Wide ranging | ⭐⭐☆☆☆ | May have many false signals in ranging |
| 📉 Single-sided crash | ⭐☆☆☆☆ | Strategy only goes long, will lose |
| ⚡️ Extreme sideways | ⭐⭐☆☆☆ | Lag may cause late entries/exits |

**One-sentence summary**: **Makes money in strong trends, loses in ranging and crashes**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended Value | Roast |
|--------------|------------------|-------|
| Number of pairs | 15-30 | Moderate signal frequency |
| Max positions | 3-5 | Control risk, don't be greedy |
| Position mode | Fixed position | Recommended fixed, control risk |
| Timeframe | 5m | Mandatory, can't change |

### 10.2 Hardware Requirements (Low Level)

This strategy uses only EMA and SMA, minimal computation:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|-----------------|------------|
| 15-30 pairs | 512MB | 1GB | Easy |
| 30-60 pairs | 1GB | 2GB | Comfortable |

**Warning**: Simple doesn't mean ineffective — EMA cross is a classic for a reason!

### 10.3 EMA Cross Characteristics

EMA cross strategies have known characteristics:
- **Lag**: Moving averages have inherent lag
- **Trend-following**: Works well in trends, poorly in ranging
- **Simple logic**: Easy to understand and modify

**Roast**: This strategy is "what you see is what you get" — no hidden complexity! 🤣

### 10.4 Backtest vs Live Trading

**Recommended process**:
1. Backtest with default parameters first
2. Understand EMA lag impact
3. Dry-run test at least 1-2 weeks
4. Small capital live test
5. Confirm stability before adding capital

**Don't go all-in immediately**, even simple strategies need testing!

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Variable naming quirk**: ema6 is actually 9-period
   > "Don't trust variable names, trust the actual values!"

2. **Dual EMA difference**: (ema6-ema24) and (ema11-ema25)
   > "One difference might lie, two differences confirm!"

3. **Weighted combination**: 0.6 and 0.5 weights
   > "Short-term matters more, but medium-term confirms!"

4. **Only 60 lines**: Super simple code
   > "Why complicate things when simple works?"

---

## 12. Last But Not Least

### One-Sentence Review
> **"4 EMAs + SMA signal line + trailing stop — suitable for beginners learning EMA cross strategies"**

### Who Should Use It?
- ✅ Simplicity believers
- ✅ People wanting to learn EMA cross strategies
- ✅ 5-minute timeframe traders
- ✅ People who understand trend-following

### Who Should NOT Use It?
- ❌ Complexity seekers
- ❌ People who don't understand EMA lag
- ❌ People unwilling to accept ranging losses
- ❌ Pure newbies without trend-following knowledge

### Manual Trader Recommendations

You can reference ema's approach:
- Use multiple EMA differences for confirmation
- Apply smoothing to reduce noise
- Set trailing stop to protect profits
- Exit on death cross or ROI target

But with 4 EMAs to watch, let the robot handle it 🤖

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtest Is Beautiful, Live Trading Needs Caution

ema's historical backtest performance may look **very good** — but there's a trap:

> **EMA cross strategies often look great in backtests on trending data, but suffer in ranging markets.**

Simply put: **"Backtest on trends = beautiful, live in ranging = painful."**

### Hidden Risks of EMA Cross Strategies

In live trading, EMA cross strategies may cause:
- **Ranging losses**: Many false signals in sideways markets
- **Lag losses**: Late entries and exits due to MA lag
- **Trend reversal losses**: Whipsaws at trend changes
- **Overconfidence**: Simple logic may lead to overconfidence

### My Recommendations (Real Talk)

```
1. Backtest on different market conditions (trending AND ranging)
2. Understand EMA lag and its impact on entries/exits
3. Consider adding higher timeframe trend filter
4. Dry-run test at least 1-2 weeks, observe behavior in different markets
5. Small capital live test, don't exceed 10% of total capital
```

**Remember**: Simple strategies are elegant but not magic. Light position test, staying alive is most important! 🙏

---

**Final reminder**: EMA cross is a classic for a reason — it works in trends. But no strategy works everywhere. Understand when your strategy works, and when to sit out!
