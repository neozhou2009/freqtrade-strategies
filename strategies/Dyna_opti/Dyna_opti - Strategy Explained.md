# Dyna_opti Strategy: The Parameter Tuner's "Ultimate Weapon"

> **Nickname**: Parameter Optimization Master / Complexity Monster  
> **Occupation**: Uses a dozen indicators in various combinations trying to "beat the market"  
> **Timeframe**: 5 Minutes + 1 Hour Informational Layer

---

## 1. What's This Strategy?

Put simply, **Dyna_opti** is a strategy that:
- Buys on Bollinger Band breakouts
- Then uses RMI, SSL Channel, candlestick patterns, and more to judge trends
- If the trend looks good, hold; if not, run
- A highly complex strategy

Like an super cautious chef making a dish: puts in a dozen different seasonings, each precisely weighed 😵

---

## 2. Core Settings: "We've Got Protection for Everything"

### Take-Profit Rules (ROI Table + Dynamic ROI)

```
Hold Time       Min Profit      Plain English
--------------------------------------------------
0 minutes       18.72%          Up 18.72% right after buying? You must be a god!
20 minutes      4.75%           Held 20 minutes, still up 4.75%? Alright then
30 minutes      2.39%           Half an hour, 2.39% profit — run
72 minutes      0%              Over an hour, don't be greedy — break even and run
```

**Dynamic ROI**: If the trend looks good (RSI rising, SSL up, candles consecutive up), won't sell until profit reaches 100%!

**Translation**: This strategy is clever! Wants big money right from the start (18.72%), but the longer you wait, the lower the requirement. But if trend analysis says "it's gonna keep rising," it holds on for dear life!

### Stoploss Rules

```
Hard stoploss: -28.82%
Custom stoploss:
  - Activates when profit < -5%
  - Force sells after 961 minutes (~16 hours)
  - Or if ROC drops to -1.8%
```

**Translation**: This strategy is super patient — can endure 16 hours of losses! But once the trend reverses, it runs fast!

---

## 3. 1 Buy Condition + Informational Layer Protection

This strategy doesn't have many buy conditions, but its protection layers are super thick:

### 🛡️ Informational Layer Protection (1-Hour Level)

> "Coins I want to buy need to be within a reasonable price range based on the past 3 days"

| Protection Type | Logic | Plain English |
|----------------|-------|---------------|
| **Upper boundary** | Price can't exceed 3-day low + 79.2% of daily volatility range | "Don't buy too high!" |
| **Lower boundary** | Price can't be below 3-day low + 17.2% of daily volatility range | "Don't buy too low!" |

**Plain English**: It's like checking historical average prices when buying a house — can't buy at the highest or lowest point, must be in the "reasonable range"!

### 🎯 Core Buy Condition (Bollinger Band Breakout)

This strategy has only 1 core buy condition, but it has 5 sub-conditions — must satisfy ALL to buy:

| Sub-condition | Requirement | Plain English |
|---------------|-------------|---------------|
| 1. Lower band exists | Previous candle has lower Bollinger band | "First, there must be a lower band" |
| 2. Band width sufficient | bbdelta > close * 0.043 | "Volatility must be big enough" |
| 3. Close change sufficient | closedelta > close * 0.027 | "Move must be obvious enough" |
| 4. Lower wick short | tail < bbdelta * 0.358 | "Not a fake breakout" |
| 5. Price broke below band | close < bb_lowerband.shift() | "Really broke through!" |

**Plain English**:
> "Price dropped to the Bollinger lower band, and all indicators check out — buy!"

This is like speed dating — ALL 5 conditions must be met before they'll "get married" (buy)! 😅

---

## 4. Exit Logic: 100x More Complex Than the Buy

### 4.1 Dynamic ROI: Hold When Trend Is Good

This strategy's take-profit isn't fixed — it's **dynamic** — adjusts based on trend strength:

| Trend Type | Judgment Method | After Trigger |
|------------|-----------------|---------------|
| **RMI Trend** | RMI consecutively up 3 candles | Won't sell until 100% profit |
| **SSL Trend** | SSL channel upward | Won't sell until 100% profit |
| **Candle Trend** | 3 consecutive up candles | Won't sell until 100% profit |

**Plain English**:
> "As long as the trend continues, hold on! Sell only when the trend ends!"

### 4.2 Special Scenario Exits

| Scenario | Trigger Condition | Plain English |
|----------|-------------------|---------------|
| Time stoploss | Held over 961 minutes (16 hours) | "Held too long, let's go" |
| Momentum stoploss | ROC drops to -1.8% | "Fell too hard, can't handle it" |
| Hard stoploss | Loss exceeds -28.82% | "Loss too big, must leave" |

### 4.3 Basic ROI Table Exits

```python
[0, 20) minutes     → Run when profit reaches 18.72%!
[20, 30) minutes   → Run when profit reaches 4.75%!
[30, 72) minutes   → Run when profit reaches 2.39%!
[72, ∞) minutes    → Dynamic ROI takes over
```

---

## 5. Technical Indicators: What "Weapons" Does This Strategy Use?

### 5.1 Core Indicators

| Category | Indicator | Parameters | Purpose | Plain English |
|----------|-----------|------------|---------|---------------|
| **Volatility** | Bollinger Bands | 12 period, 2x | Price boundaries | "Price channel" |
| **Momentum** | RMI | 24/21/8 periods | Momentum judgment | "RSI's relative" |
| **Trend** | SSL-ATR | 21 period | Trend direction | "Trend indicator" |
| **Volatility** | ATR | 24 period | Volatility | "Volatility size" |
| **Momentum** | SROC | 21/13/21 periods | Rate of change | "Speed indicator" |

### 5.2 Custom Indicators (The Author's "Secret Recipes")

| Indicator | Principle | Plain English |
|-----------|-----------|---------------|
| **MA Streak** | Number of consecutive up/down candles | "How many days in a row did it rise?" |
| **Percent Change Channel** | Percentage change channel | "Price change range" |
| **Momentum Pinball** | ROC-based RSI | "Momentum version of RSI" |

**Rant**: The author must be an indicator collector — adds every new indicator they see! 😅

---

## 6. Risk Management: How Does This Strategy "Protect Itself"?

### 6.1 Multi-Layer Protection Mechanism

This strategy's protection is thicker than a city wall:

| Protection Layer | Effect | Trigger Condition |
|------------------|--------|------------------|
| **Informational layer** | 1-hour filter | Won't buy if price not in reasonable range |
| **Dynamic ROI** | Won't sell when trend is good | RMI/SSL/candle trend upward |
| **Custom stoploss** | Exit promptly when losing | Profit < -5% + time/ROC triggered |
| **Hard stoploss** | Last defense | Loss -28.82% |

### 6.2 Trend Judgment Trio

The strategy uses three methods to judge trends — any one triggered counts as good trend:

1. **RMI**: Variant of Relative Strength Index — consecutive rise counts as good trend
2. **SSL Channel**: Price above means uptrend
3. **Candlesticks**: 3 consecutive up candles count as good trend

**Plain English**: Like checking weather forecasts — only go out when all three forecasts say "sunny"!

---

## 7. The Strategy's "Personality Traits"

### ✅ Pros (The Praise Section)

1. **Tons of indicators**: A dozen indicators, there's always one that fits
2. **Dynamic take-profit**: Won't sell when trend is good — lets profits run
3. **Complete protection**: Informational layer + trend judgment + take-profit/stoploss
4. **Adjustable parameters**: Every parameter can be optimized — a paradise for parameter tuners
5. **Highly parameterized**: Built for parameter optimization

### ⚠️ Cons (The Rant Section)

1. **Too complex**: Over 1000 lines of code, can't even read it
2. **Easy to overfit**: Too many parameters, easy to "memorize the answers"
3. **High hardware demands**: Running 80 coins? Need 8GB RAM!
4. **High learning curve**: Beginners stay away — need quantitative background

---

## 8. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 **Trending market** | Enable dynamic ROI | Let profits run in trends, make big money! |
| 🔄 **High volatility** | Keep default | Generous stoploss suits high volatility |
| 📉 **Oscillating market** | Lower ROI thresholds | Reduce trend protection, more short-term trades |
| 😐 **Consolidation** | Reduce trading pairs | Protection may fail, don't buy randomly |

---

## 9. Bottom Line: How's This Strategy Really?

### One-Line Verdict
> "A super complex, parameter-heavy, high-end strategy for parameter-tuning enthusiasts"

### Who It's Good For:
- ✅ People with quantitative experience
- ✅ People who like tuning parameters
- ✅ People with high-end computers
- ✅ Patient people
- ✅ People willing to spend time learning

### Who It's NOT For:
- ❌ Beginners (too complex to understand)
- ❌ People with low-end computers (can't handle the calculations)
- ❌ People who want simple strategies (simpler is better)
- ❌ People who want to justpassive income (need constant monitoring)

### My Suggestions

1. **Understand the core logic first**: Bollinger breakout + trend judgment
2. **Don't mess with parameters randomly**: Default parameters are what the author optimized
3. **Mind your hardware**: 80 trading pairs need lots of memory
4. **Test with small money**: This strategy is too complex — simulate more before live trading

---

## 10. What Markets Does This Strategy Make Money In?

### 10.1 Core Logic: Building a "Defense Network" with Complexity

**Dyna_opti's** money-making philosophy: **Cross-validate with a dozen indicators to reduce fake signals!**

- **Bollinger breakout**: Catch oversold bounces
- **Trend protection**: Don't buy if trend isn't good
- **Dynamic exit**: Sell only when trend reverses

### 10.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:---|:---:|:---|
| 📈 Trending up | ⭐⭐⭐⭐⭐ | Dynamic ROI lets profits run — makes a fortune when trend comes! |
| 🔄 Wide-range oscillation | ⭐⭐⭐⭐☆ | Bollinger breakout effective in ranges — can catch bounces |
| 📉 One-way down | ⭐⭐☆☆☆ | Trend protection may fail — easy to get stopped out repeatedly |
| ⚡️ Extreme consolidation | ⭐⭐⭐☆☆ | Complex calculation, mediocre effect |

**One-liner**: Bull market = rich, oscillating = okay, bear market = be careful 😎

---

## 11. Want to Run This Strategy? Check These Configs First

### 11.1 Trading Pair Configuration

| Config Item | Recommended Value | Comments |
|-------------|-------------------|----------|
| Number of pairs | 20-40 | Don't go too many, can't calculate |
| Mainstream coins only | BTC/ETH/BNB | Altcoin indicators easilyfail |
| Trading time | 24/7 | Crypto never sleeps |

### 11.2 Key Config Settings

```yaml
# Recommended config
minimal_roi:
  "0": 0.18724
  "20": 0.04751
  "30": 0.02393
  "72": 0

stoploss: -0.28819
use_dynamic_roi: true
use_custom_stoploss: true
```

### 11.3 Hardware Requirements (Important!)

This strategy has enormous computational load, demanding on VPS memory:

| Number of Pairs | Min RAM | Recommended RAM | Experience |
|-----------------|---------|-----------------|------------|
| 20-40 pairs | 2 GB | 4 GB | Barely runs |
| 40-80 pairs | 4 GB | 8 GB | Smooth |
| 80+ pairs | 8 GB | 16 GB | Flying |

**Warning**: Old VPS may crash — calculation timeout! 😅

### 11.4 Backtesting vs. Live Trading

Backtesting looks great, live trading fails because:
1. **Slippage**: Live slippage can cause bid-ask spread issues
2. **Network delay**: Command delay may miss best timing
3. **Liquidity**: Can't buy enough quantity in small trading pairs

**Recommended Process**:
1. Backtest for 3 months
2. Dry-run for 2 weeks
3. Small capital live trading for 1 month
4. Scale up capital only if no issues

**Don't go all-in from the start** — even the best strategy needs arun-in period period!

---

## 12. Bonus: The Strategy Author's "Little Tricks"

1. **Dyna_opti name**: Dynamic Optimization = Dynamic Optimization, the author must be a parameter enthusiast!
2. **1-hour informational layer**: The author must have been burned by "intraday fake breakouts" — so added long-term protection
3. **16-hour time stoploss**: The author must have held coins for days before — too long!
4. **A dozen indicators**: The author must be an indicator collector — adds every new indicator they discover

---

## ⚠️ Final Warning: Risk Re-emphasis (Must Read!)

### Backtesting Looks Great, Live Trading Requires Caution

**Dyna_opti's** historical backtesting performance often looks **very good** — but there's a trap:

> **Because there are many parameters, the strategy can easily "fit" the optimal solution for past market conditions — but this doesn't guarantee future profitability.**

Simply put: **Memorizing answers doesn't guarantee you'll ace the exam!**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Calculation timeout**: Too many indicators, VPS can't process in time
- **Signal conflicts**: Multiple indicators give conflicting signals
- **Hard to debug**: When something goes wrong, you don't know where the problem is
- **Overfitting**: Parameters too "perfect" — might be "memorized answers"

### My Suggestions (Sincere Advice)

```
1. Don't worship parameters: Optimization is just math, not predicting the future
2. Diversify investments: Don't put all money on one strategy
3. Test with small money: Run for a month first to see the effect
4. Monitor continuously: Parameters may need periodic updates
5. Understand the logic: Don't just use it without knowing why
```

**Remember**: Complex doesn't mean effective, simple strategies are sometimes more reliable! Markets are alive, strategies are static! 🙏

---

**Final Reminder**: No matter how good the strategy, the market won't hesitate to teach you a lesson. Test with small capital — survival is the top priority! 🙏
