# CombinedBinHAndCluc2021Bull Strategy: A "Three-in-One" Bull Market Harvester

> **Nickname**: Bull Market Hunter
> **Profession**: Quantitative "Collector" — collecting the best of 3 classic strategies
> **Timeframe**: 5 Minutes (short-term player)

---

## 1. What's This Strategy?

Simply put, **CombinedBinHAndCluc2021Bull** is:
- A strategy using **3 different strategy logics** (BinHV45 + ClucMay72018 + BBRSI)
- A strategy **specifically designed for bull markets**
- A strategy that **runs at 1%** (ultra-fast turnover)

Think of it as a smart shopper who only shops during major sales:
> "BinHV45 says on sale? ClucMay72018 says on sale? BBRSI says mega sale? Buy if any is satisfied, sell at original price and run!"

---

## 2. Core Settings

### Take-Profit Rules (ROI Table)

```
Make 1%? → Run! (just this level, super fast)
```

**Plain English**: This strategy is "small profit, high turnover" — 1% and done, not greedy, pursues fast turnover!

### Stop-Loss Rules

```
Hard stop-loss: Cut at 9% loss (loose enough)
```

**Plain English**: -9% stop-loss is truly generous, giving price sufficient fluctuation space, typical "mean reversion" thinking.

---

## 3. Entry Conditions: Any of Three Strategies, Buy When Satisfied

This strategy has three entry modes — buy when any one is satisfied:

### 🎯 Mode 1: BinHV45 Strategy

**Core Logic**:
1. Previous BB lower band > 0
2. BB width > 0.8%
3. Price change > 1.75%
4. Lower wick < 25% of width
5. Current price < previous lower band
6. Current price <= previous close

**Plain English**:
> "BB width wide enough, price broke below previous lower band, and still falling — time to bottom-fish?"

---

### 🎯 Mode 2: ClucMay72018 Strategy

**Core Logic**:
1. Price < EMA100
2. Price < BB lower band × 0.985 (1.5% below)
3. Volume < avg × 20

**Plain English**:
> "Price below EMA100, and below BB lower band by 1.5%, volume normal — why not buy?"

---

### 🎯 Mode 3: BBRSI Strategy (Most Aggressive!)

**Core Logic**:
1. RSI < 12 (extreme oversold!)
2. Price < 4σ BB lower band

**Plain English**:
> "RSI is at 12 (normal is 30), and price broke through 4σ BB — this is DEEP discount, buy!"

**Commentary**: BBRSI conditions are truly aggressive, RSI < 12 + 4σ, once-in-a-lifetime opportunity! 🤣

---

## 4. Protection Mechanisms

This strategy's protection is simple but effective:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| **Hard Stop-Loss** | Cut at 9% loss | "Mistakes happen, 9% is the bottom line" |
| **ROI Exit** | Make 1% and run | "Small profit, high turnover" |
| **Technical Exit** | Run when price reverts to middle band | "Mean reversion complete, secure profits" |

---

## 5. Exit Logic

### 5.1 Technical Sell: Just 1 Condition

**Trigger Condition**:
```python
Price > BB middle band
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
2. **Deeply Oversold Capture**: BBRSI catches extreme oversold opportunities
3. **Fast Turnover**: 1% ROI + middle band exit, high capital utilization
4. **Bull Market Dedicated**: Designed for bull markets, high rebound probability
5. **Small Computation**: Few indicators, low hardware requirements

### ⚠️ Cons

1. **No trend filtering**: No long-term trend judgment
2. **No BTC correlation**: Bitcoin crashes, doesn't know
3. **Bear Market Risk**: May lose consecutively in bear markets
4. **Low ROI**: 1% ROI may miss big trends
5. **Multi-BB Computation**: Three BB systems increase computation

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **Bull Market** | Strongly recommend | Born for bull markets, extremely high rebound probability |
| **Volatile Market** | Recommend | Mean reversion suitable for volatile markets |
| **Downtrend** | Pause | No trend filtering, easy to lose consecutively |
| **High Volatility** | Suitable | Loose stop-loss handles volatility |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small swings |
| **BTC Crash** | Pause | Big brother fell, standing by first |

---

## 8. Summary

### One-Line Verdict
> **"A fast harvester using three BB systems, specifically designed for bull markets"**

### Who's It For?
- ✅ People who like multi-strategy combinations
- ✅ Traders in bull market environments
- ✅ People who accept fast turnover
- ✅ Friends with VPS RAM over 1GB

### Who's It NOT For?
- ❌ Traders in bear markets (will lose consecutively)
- ❌ People seeking big trends (1% ROI too "conservative")
- ❌ People who don't monitor markets (need to judge bull/bear)
- ❌ Pure quantitative beginners (need to understand mean reversion)

---

## 9. Market Performance

### Core Logic: The Faith of Mean Reversion

**Its Money-Making Philosophy**:
> "Price dropped too hard will always revert — waiting for that deeply oversold moment, make 1% and run, isn't that?"

- **BB Faith**: Price within 2σ 95% of the time
- **Mean Reversion Faith**: Price reverting from lower band to middle band is high probability
- **Small Profit Faith**: 1% fast turnover, accumulate small wins

### Performance in Different Markets

| Market Type | Rating | Plain English Explanation |
|:-----------|:------:|:------------------------|
| Bull Market | ⭐⭐⭐⭐⭐ | Born for bull markets, extremely high rebound probability |
| Wide Volatile | ⭐⭐⭐⭐☆ | Mean reversion suitable for volatile markets |
| Bear Market | ⭐⭐☆☆☆ | No trend filtering, easy to lose consecutively |
| Extreme Sideways | ⭐⭐⭐☆☆ | Too little fluctuation, signals reduce but risk also low |

**One-Line Summary**: **Makes money in bull and volatile markets, be careful in bear markets**

---

## 10. Configuration Suggestions

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Description |
|-------------------|-----------------|-------------|
| **# of Trading Pairs** | 20-40 | Signal frequency moderate |
| **Quote Currency** | USDT | Don't use BTC/ETH as quote |
| **Max Positions** | 3-6 orders | Control risk |
| **Position Mode** | Fixed position | Suggest fixed, control risk |
| **Timeframe** | 5m | Mandatory, can't change |

### 10.2 Hardware Requirements

| Number of Pairs | Minimum RAM | Recommended RAM |
|----------------|-------------|-----------------|
| 20-40 pairs | 512MB | 1GB |
| 40-80 pairs | 1GB | 2GB |

**Good News**: 512MB RAM VPS can run it, quite friendly!

---

## 11. Bonus: Strategy's "Little Tricks"

1. **Strategy name "CombinedBinHAndCluc2021Bull"**: Combined + Bull
   > "The name tells you — this is a bull market dedicated combo strategy!"

2. **Three BB Systems**: 2σ, 2σ, 4σ
   > "2σ not enough? Then 4σ! One will trigger!"

3. **ROI Only 1%**: Much lower than common strategies
   > "True small profit, high turnover, 1% and run isn't?"

---

## 12. The Bottom Line

### One-Line Verdict
> **"Three BB systems + mean reversion, a fast harvester dedicated to bull markets"**

### Manual Trading Recommendations
Manual traders can reference this strategy's multi-BB approach:
- Observe multiple BB systems simultaneously
- Consider buying when deeply oversold
- Exit when price reverts to middle band

### My Recommendations
1. **Judge bull/bear first**: Only use in bull or volatile markets
2. **Add filtering**: Can add EMA200 trend filtering yourself
3. **Adjust ROI**: Can adjust based on market (e.g., 2% or 3%)
4. **Watch BTC**: Manually pause strategy when Bitcoin crashes

---

## ⚠️ Final Warning (Must Read!)

### Backtesting Looks Great — Be Careful in Live Trading

CombinedBinHAndCluc2021Bull's historical backtest may **perform exceptionally well** — but there's a trap:

> **Bull market strategies often perform well in bull market backtests, but doesn't guarantee future will be bull market.**

Simply put: **Good backtest data may be because it just "encountered" that bull market period.**

### Hidden Risks of Bull Market Strategies

In live trading, bull market strategies may cause:
- **Bear market consecutive losses**: May stop out consecutively in bear markets
- **Trend reversal risk**: Big loss if not pausing promptly when bull turns to bear
- **Low ROI missing big trends**: 1% ROI may exit prematurely

### My Recommendations (Sincere Advice)

```
1. Test first with minimum capital (e.g., 100U)
2. Run live at least 2-4 weeks, confirm current market is bull
3. Firmly pause strategy in bear markets
4. Consider adjusting ROI parameters (e.g., 2% or 3%)
```

**Remember**: This is a bull market strategy, must pause in bear markets! Survival is the top priority!

---

**Final Reminder**: Strategy is good, but market doesn't care. Paper trade with light positions, survival is the top priority! 🙏

---

*Strategy #: Batch 11, #7 | Nickname: Bull Market Hunter | Timeframe: 5m*
