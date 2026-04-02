# CombinedBinHAndCluc2021 Strategy: A "Three-in-One" Oversold Hunter

> **Nickname**: Oversold Hunter / Three-in-One Catcher
> **Profession**: Quantitative "Smart Buyer" — specifically waits for deep discounts
> **Timeframe**: 5 Minutes (short-term player)

---

## 1. What's This Strategy?

Simply put, **CombinedBinHAndCluc2021** is:
- A strategy using **3 different strategy logics** (BinHV45 + ClucMay72018 + BBRSI)
- A strategy with **ultra-low targets** (makes 1% and runs)
- A strategy **specifically catching oversold rebounds**

Think of it as a smart shopper who only shops during "mega sales":
> "BinHV45 says on sale? ClucMay72018 says on sale? BBRSI says deep discount? Buy if any is satisfied, run away at the slightest rise!"

---

## 2. Core Settings: Basically "Deep Oversold + Fast Exit"

### Take-Profit Rules (ROI Table)

```
Make 1%? → Run! (just this one level, super fast)
```

**Translation**: This strategy is the "small profit, high turnover" mentality, 1% and done, not greedy!

### Stop-Loss Rules

```
Hard stop-loss: Cut at 9% loss (quite loose)
Trailing stop: None
```

**Translation**: -9% stop-loss gives price sufficient fluctuation space, typical "waiting for rebound" thinking 😅

---

## 3. Entry Conditions: Any of Three Strategies, Buy When Satisfied

This strategy has three entry modes — buy when any one is satisfied:

### 🎯 Mode 1: BinHV45 Strategy

**Core Logic** (all 6 conditions must be met):
1. Previous Bollinger lower band > 0
2. Bollinger width > 0.8%
3. Price change > 1.75%
4. Lower wick < 25% of width
5. Current price < previous lower band
6. Current price <= previous close

**Plain English**:
> "Bollinger width wide enough, price broke below previous lower band, and still falling — time to bottom-fish?"

### 🎯 Mode 2: ClucMay72018 Strategy

**Core Logic** (all 3 conditions must be met):
1. Price < EMA100 (below long-term moving average)
2. Price < BB lower band × 0.985 (1.5% below)
3. Volume < avg × 20

**Plain English**:
> "Price below EMA100, and below BB lower band by 1.5%, volume also normal — might be worth buying!"

### 🎯 Mode 3: BBRSI Strategy (Most Aggressive!)

**Core Logic** (all 2 conditions must be met):
1. RSI < 12 (extremely oversold!)
2. Price < 4σ BB lower band

**Plain English**:
> "RSI is at 12 (normal is 30), and price broke through 4σ BB — this is a DEEP discount, buying buying buying!"

**Commentary**: BBRSI conditions are truly aggressive, once in a lifetime! 🤣

---

## 4. Protection Mechanisms: Loose Stop-Loss + Fast Exit

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| **Hard Stop-Loss** | Cut at 9% loss | "Mistakes happen, 9% is the bottom line" |
| **ROI Exit** | Make 1% and run | "Small profit, high turnover" |
| **Technical Exit** | Run when price reverts to middle band | "Mean reversion complete, secure profits" |

**Commentary**: Protection mechanism is simple and brutal, but 1% ROI is truly fast! 🤣

---

## 5. Exit Logic: Rise a Little and Run

### 5.1 Technical Sell: Just 1 Condition

**Trigger Condition**:
```python
Price > Bollinger middle band
```

**Plain English**:
> "Price reverted from lower band to middle band, mean reversion complete — why wait?"

### 5.2 ROI Exit: Just 1 Level, 1%

```
Profit Rate    Holding Time    Trigger Exit
──────────────────────────────────────────
1%             Anytime         Run immediately
```

---

## 6. Strategy "Personality"

### ✅ Pros

1. **Multi-Strategy Combination**: 3 classic strategy logics, covering different scenarios
2. **Extreme Oversold Capture**: BBRSI catches extreme oversold opportunities
3. **Fast Turnover**: 1% ROI + middle band exit, high capital utilization
4. **Pattern Recognition**: BinHV45 effectively identifies hammer patterns
5. **Moderate Computation**: Clear logic, low hardware requirements

### ⚠️ Cons

1. **No trend filtering**: No long-term trend judgment
2. **No BTC correlation**: Bitcoin crashes, it doesn't know
3. **Low ROI**: 1% may miss big trends
4. **Downtrend Risk**: May counter-trend buy
5. **Multi-Bollinger Computation**: Three BB systems increase computation

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **High-Volatility Market** | Strongly recommend | Loose stop-loss handles volatility |
| **Volatile Market** | Recommend | Mean reversion suitable for volatile |
| **Unilateral Uptrend** | Use cautiously | May miss subsequent rally |
| **Downtrend** | Pause | No trend filtering, easy to lose |
| **Low-Volatility** | Not recommend | Signals reduce |

---

## 8. Summary: How Does This Strategy Really Stack Up?

### One-Line Verdict
> **"A fast harvester using three BB systems, specifically catching oversold rebounds"**

### Who's It For?
- ✅ People who like multi-strategy combinations
- ✅ Traders in high-volatility markets
- ✅ People who accept fast turnover
- ✅ Friends with VPS RAM over 1GB

### Who's It NOT For?
- ❌ Traders in downtrends
- ❌ People seeking big trends (1% is too "conservative")
- ❌ People who don't monitor markets
- ❌ Pure quantitative beginners

### My Recommendations
1. **Judge the market**: Only use in volatile or high-volatility markets
2. **Add trend filtering**: Can add EMA200 trend judgment yourself
3. **Adjust ROI**: Can adjust based on market (e.g., 2% or 3%)
4. **Watch BTC**: Be careful when Bitcoin crashes

---

## 9. Market Performance: What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: The Faith of Mean Reversion

**Its Money-Making Philosophy**:
> "Price dropped too hard will always revert — I wait for that deeply oversold moment, make 1% and run!"

- **BB Faith**: Price is within 2σ 95% of the time
- **Mean Reversion Faith**: Price reverting from lower band to middle band is high probability
- **Small Profit Faith**: 1% fast turnover, accumulate small wins

### 9.2 Performance in Different Markets

| Market Type | Rating | Plain English Explanation |
|:-----------|:------:|:------------------------|
| Bull Rally | ⭐⭐⭐⭐⭐ | Deeply oversold then rebound probability extremely high |
| Wide Volatile | ⭐⭐⭐⭐☆ | Mean reversion suitable for volatile markets |
| Downtrend | ⭐⭐☆☆☆ | No trend filtering, easy to lose |
| Extreme Sideways | ⭐⭐⭐☆☆ | Too little fluctuation, signals reduce |

**One-Line Summary**: **Makes money in high-volatility and volatile markets, be careful in downtrends**

---

## 10. Configuration Suggestions: Want to Run This? Check These First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Suggestion |
|-------------------|-----------------|-----------|
| **# of Trading Pairs** | 20-40 | Signal frequency moderate |
| **Quote Currency** | USDT | Don't use BTC/ETH |
| **Max Positions** | 3-6 orders | Control risk |
| **Position Mode** | Fixed position | Suggest fixed |
| **Timeframe** | 5m | Mandatory |

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 20-40 pairs | 512MB | 1GB |
| 40-80 pairs | 1GB | 2GB |

**Warning**: 512MB RAM can run it, low barrier! 😅

---

## 11. Bonus: Strategy's "Little Tricks"

1. **Three BB Systems**: 2σ, 2σ, 4σ
   > "2σ not enough? Use 4σ! One of them will trigger!"

2. **ROI Only 1%**: Much lower than common strategies
   > "True small profit, high turnover, 1% and done!"

3. **BBRSI Conditions**: RSI < 12 + 4σ
   > "This catches once-in-a-hundred-year opportunities!"

---

## 12. The Bottom Line

### One-Line Verdict
> **"Three BB systems + mean reversion, a fast harvester for oversold rebounds"**

### Who's It For?
- ✅ People who like multi-strategy combinations
- ✅ Traders in high-volatility markets
- ✅ People who accept fast turnover
- ✅ People who understand mean reversion

### Who's It NOT For?
- ❌ Traders in downtrends
- ❌ People seeking big trends
- ❌ People who don't monitor markets

### Manual Trading Recommendations
- Observe multiple BB systems simultaneously
- Consider buying when deeply oversold
- Exit when price reverts to middle band

---

## ⚠️ Final Warning (Must Read!)

### Backtesting Looks Great — Be Careful in Live Trading

CombinedBinHAndCluc2021's historical backtest may **look very good** — but there's a trap:

> **Deep oversold strategies perform well in some markets, but doesn't mean they work in all markets.**

### Hidden Risks

In live trading may cause:
- **Downtrend losses**: No trend filtering, may counter-trend buy
- **Consecutive stop-outs**: Market continues falling, may trigger stop-loss consecutively
- **Low ROI missing big trends**: 1% may exit prematurely

### My Recommendations (Sincere Advice)

```
1. Test first with minimum capital (e.g., 100U)
2. Run live for at least 2-4 weeks, observe strategy performance
3. Firmly pause when in downtrends
4. Consider adjusting ROI parameters (e.g., 2% or 3%)
5. Suggest pairing with trend filtering
```

**Remember**: This strategy is "oversold rebound" thinking, be careful in downtrends! Survival is the top priority!

---

**Final Reminder**: Strategy is good, but market is boss. Paper trade with light positions, survival is the top priority! 🙏
