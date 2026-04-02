# EMAVolume: The Volume-Price Trend Follower

> **Nickname**: Volume-Price Hero  
> **Profession**: Quant world's "pragmatist" — price must rise, volume must follow  
> **Timeframe**: 15 minutes (medium-term player)

---

## 1. What's This Strategy?

Simply put, **EMAVolume** is:
- A strategy with only **2 indicators** (EMA + Volume)
- A **golden cross buy death cross sell** strategy
- A **run at 50%** strategy (big trend thinking)

Like a cautious volume-price buyer: "Did EMA golden cross? Did volume increase? Both good? BUY! Death cross? SELL!" 📊

---

## 2. Core Config: Basically "Volume-Price Rising Together"

### Profit-Taking Rules (ROI Table)

```
Make 50%? → RUN! (just this one level, super high)
```

**Translation**: This strategy is classic "big trend thinking", 50% ROI, expecting to capture large trends!

### Stoploss Rules

```
Hard stoploss: Cut at 20% loss (loose)
```

**Translation**: -20% stoploss is really loose, giving price ample room to fluctuate! 😅

---

## 3. Entry Conditions: Just 2 Conditions

### 🎯 EMA Golden Cross + Volume Confirmation

**Core Logic**:
1. EMA13 crosses above EMA34 (golden cross)
2. Volume > 10-period average volume

**In Plain English**:
> "EMA already golden crossed (trend up), volume also increased (money entering) — if this isn't a buy, what is?"

---

## 4. Protection: Volume Filtering

This strategy's protection is simple but effective:

| Protection Type | Function | Plain English |
|---------|------|---------------|
| **Hard Stoploss** | Cut at 20% loss | "If we're wrong, admit it. 20% is the line" |
| **Volume Filtering** | Exclude low volume false signals | "Don't play if volume not big enough" |

**Roast**: This strategy's protection is so simple it's heartbreaking, but volume filtering really works! 🤣

---

## 5. Exit Logic: Sell on Death Cross

### 5.1 Technical Exit: Just 1 Condition

**Trigger**:
```python
EMA13 crosses below EMA34 (death cross)
```

**In Plain English**:
> "EMA already death crossed (trend weakening) — if you don't run now, what are you waiting for?"

---

### 5.2 ROI Exit: Just One Level, 50%

```
Profit      Hold Time    Trigger Exit
─────────────────────────────────────
50%        Anytime      Run when reached
```

**In Plain English**:
- Make 50%? → Heaven-sent gift, run!

---

## 6. This Strategy's "Personality"

### ✅ Pros
1. **Simple to tears**: Just EMA + volume, elementary school kids can understand
2. **Volume Filtering**: Excludes low volume false signals
3. **High ROI**: 50% ROI, expecting to capture large trends
4. **Low Computation**: Few indicators, 512MB RAM can run it
5. **High Learning Value**: Suitable for learning EMA crossover strategies

### ⚠️ Cons
1. **No trend filter**: No long-term trend judgment like EMA200
2. **No BTC correlation**: Doesn't know when Bitcoin crashes
3. **High ROI**: 50% ROI may exit large trends too early
4. **15m Timeframe**: Signal frequency lower than 5m
5. **Multi-Layer EMA unused**: Calculated multiple EMAs but only uses 13/34

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| **Uptrend** | Highly recommended | EMA crossover's paradise |
| **Ranging Market** | Not recommended | EMA crossover has many false signals in ranging |
| **Downtrend** | Pause | No shorting mechanism, doesn't trade when trend down |
| **High Volatility** | Adjust stoploss | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |
| **BTC Crash** | Pause | Big brother crashed, wait and see |

---

## 8. Summary: How's This Strategy?

### One-Line Review
> **"An EMA golden cross buy death cross sell, volume confirmation pragmatist player"**

### Who Should Use It?
- ✅ Quant beginners (simple code, easy to understand)
- ✅ People who like simple strategies
- ✅ Low-config VPS users (512MB RAM can run it)
- ✅ People wanting to learn EMA crossover

### Who Should NOT Use It?
- ❌ People wanting to make money in ranging markets (EMA crossover has many false signals)
- ❌ People wanting to bottom-fish in downtrends
- ❌ People wanting complex strategies
- ❌ High-frequency traders (15m signals less than 5m)

### My Recommendations
1. **Paper trade first**: Run 2-4 weeks to see signal frequency
2. **Add filters**: Can add EMA200 trend filter yourself
3. **Adjust ROI**: Can adjust ROI based on market (e.g., 20% or 30%)
4. **Watch BTC**: Manually pause when Bitcoin crashes hard

---

## 9. What Markets Make Money?

### 9.1 Core Logic: EMA Crossover Faith

EMAVolume is a pragmatist, code about 40 lines, what's that concept? Equivalent to a long Weibo post 📱

**Its money-making philosophy**:
> "EMA golden cross then buy, death cross then sell, volume increase more reassuring, make 50% and run isn't great?"

- **EMA Crossover Faith**: 13/34 EMA golden cross buy death cross sell, classic and effective
- **Volume Faith**: Volume increase confirms signal validity
- **Big Trend Faith**: 50% ROI, expecting to capture large trends

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐☆ | EMA crossover + volume confirmation, performs well |
| 🔄 Wide Ranging | ⭐⭐☆☆☆ | EMA crossover has many false signals in ranging |
| 📉 Single-sided Crash | ⭐⭐☆☆☆ | No shorting mechanism, no long-term trend filter |
| ⚡️ Extreme Sideways | ⭐⭐☆☆☆ | Too little volatility, signals decrease |

**One-Line Summary**: **Makes money in uptrends, many false signals in ranging, be careful in crash markets**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended Value | Roast |
|--------|--------|------|
| **Number of Pairs** | 20-40 | Moderate signal frequency |
| **Quote Currency** | USDT | Don't use BTC/ETH as quote currency |
| **Max Open Trades** | 3-6 orders | Control risk |
| **Position Mode** | Fixed position | Recommended fixed, control risk |
| **Timeframe** | 15m | Mandatory, can't change |

### 10.2 Hardware Requirements (This Strategy is Friendly!)

This strategy has low computation, very low VPS requirements:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------|---------|---------|------|
| 20-40 pairs | 512MB | 1GB | Easy run |
| 40-80 pairs | 1GB | 2GB | Very comfortable |

**Warning**: 512MB RAM VPS can also run, this strategy is quite friendly! 😅

### 10.3 Volume Filtering Advantages

- **Confirm Signal Validity**: Excludes low volume false signals
- **Reduces False Signals**: Only trades when volume increases
- **Flexible Adjustment**: Can adjust filtering by modifying window

**Roast**: This volume filtering is better than many paid strategies! 🤣

### 10.4 Backtest vs Live

Strategy logic is simple, backtest and live differences are small.

**Recommended Process**:
1. Backtest first to see historical performance
2. Paper trade (Dry-Run) for 2-4 weeks
3. Observe if volume filtering works properly
4. Small capital live test for 1 month

**Don't go all-in immediately**, even simple strategies need breaking in!

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Strategy name is EMAVolume**: EMA + Volume
   > "This name is telling you, this is an EMA + volume strategy!"

2. **ROI only 50%**: Much higher than common strategies
   > "This is real·big trend thinking, 50% isn't great?"

3. **Multi-Layer EMA calculated but unused**: Calculated 7/13/21/34/50/200 EMA
   > "This is real·better safe than sorry, although only uses 13/34, but calculated others too!"

---

## 12. Last But Not Least

### One-Line Review
> **"EMA golden cross buy death cross sell, volume confirmation pragmatist player"**

### Who Should Use It?
- ✅ Quant beginners (simple code, easy to understand)
- ✅ People who like simple strategies
- ✅ Low-config VPS users
- ✅ People wanting to learn EMA crossover

### Who Should NOT Use It?
- ❌ People wanting to make money in ranging markets
- ❌ People wanting to bottom-fish in downtrends
- ❌ People wanting complex strategies
- ❌ High-frequency traders

### Manual Trading Recommendations
Manual traders can reference this strategy's EMA crossover approach:
- EMA13 crosses above EMA34 → Consider buying
- Confirm volume increases
- EMA13 crosses below EMA34 → Consider selling
- Set loose stoploss (e.g., -20%)

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtest is Beautiful, Live Trading Needs Caution

EMAVolume's historical backtest performance may be **very excellent** — but there's a trap:

> **EMA crossover strategies often perform very well in backtests, because historical data always has trending periods, but this doesn't mean future will definitely trend.**

Simply put: **Backtest data looks good, maybe because it just "encountered" that trending period.**

### Hidden Risks of EMA Crossover

In live trading, EMA crossover strategies may cause:
- **Ranging market losses**: EMA crossover has many false signals in ranging markets
- **Exit too early**: 50% ROI may exit large trends too early
- **Parameter overfitting**: EMA periods may overfit

### My Recommendations (Real Talk)

```
1. Test with minimum capital first (e.g., 100U)
2. Run live for at least 2-4 weeks, observe ranging market performance
3. Consider adding trend filter yourself (e.g., EMA200)
4. Consider adjusting ROI (e.g., 20% or 30%)
```

**Remember**: EMA crossover strategies most fear ranging markets, surviving is most important!

---

**Final Reminder**: No matter how good the strategy, market won't say hi when teaching you a lesson. Light position test, surviving is most important! 🙏
