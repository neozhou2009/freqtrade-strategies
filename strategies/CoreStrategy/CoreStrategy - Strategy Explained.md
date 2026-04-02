# CoreStrategy: The "Super Composite" of Quantitative Trading

> **Nickname**: Strategy Stamp Collector / The "Playboy" of Quantitative Trading  
> **Specialty**: Fusing 4 classic strategies into one ultra-complex monster  
> **Timeframe**: 5 minutes + 1-hour informational layer

---

## 1. What's This Strategy?

Simply put, **CoreStrategy** is:
- A strategy with **21 buy conditions** (advanced stage of choice paralysis)
- A strategy with **4 sell conditions**
- A "super Frankenstein's monster" combining 4 classic strategies (SMAOffset + V6 + V8 + V9)
- A strategy using **5-minute + 1-hour dual timeframe**

Think of it like someone who opens 4 shopping apps, compares 21 conditions, and still can't decide: "This one's cheaper, that one's got better reviews, oh this one has a coupon... which one do I actually buy?!" 😂

---

## 2. Core Configuration: It's Basically a "Hotpot"

### Take-Profit Rules (ROI Table)

```
0-38 minutes: Exit at 20% profit!
38-78 minutes: Exit at 7.4% profit!
78-194 minutes: Exit at 2.5% profit!
After 194 minutes: Exit whenever
```

**Translation**: This strategy is greedy — wants 20% right out of the gate! But as time passes, the target gets lower and lower — classic "shoot for the moon, then chicken out" 😅

### Stop-Loss Rules

```
Hard stop-loss: -22.8% (actually managed by custom logic)
Trailing stop: Yes! Starts trailing at 5% profit, exits on 0.5% drawdown from high
Custom stop-loss: After 4 hours of holding, dynamically handles based on trend and RSI
```

**Translation**: The official stop-loss looks loose (-22.8%), but the strategy actually has a whole set of complex "smart stop-loss" logic that decides whether to cut losses or hold for a rebound based on holding time, trend direction, and RSI levels.

---

## 3. The 21 Buy Conditions: Categorized for You

This strategy has way too many buy conditions, so I've organized them into 4 categories:

### 🎯 Category 1: SMAOffset Series (2 conditions)
**Core Logic**: EWO momentum indicator + price position

- **smaoffset_buy_condition_0**: EWO upward + RSI below 50 + price below moving average
  > "Price pulled back to the moving average, and momentum says it's going up — buy!"

- **smaoffset_buy_condition_1**: EWO extremely negative (<-19.8)
  > "It's dropped too much — time for a bounce!"

### 📉 Category 2: V8 Series (5 conditions, 4 enabled by default)
**Core Logic**: Multi-period EMA confirmation + Bollinger Band pullback

- **v8_buy_condition_0**: 1h EMA in bullish alignment + Bollinger Band contraction + breaks below lower band
  > "Long-term trend is up, short-term pulled back to Bollinger Band bottom — buy!"

- **v8_buy_condition_1**: Price above EMA200 + touches Bollinger Band lower band + volume contracted
  > "Long-term trend is up, short-term can't drop further — buy!"

- **v8_buy_condition_2**: SSL channel up + RSI 1h relatively strong
  > "1-hour trend is bullish, 5-minute RSI oversold — buy!"

- **v8_buy_condition_3**: SMA200 up + RSI 1h stronger than RSI 5m
  > "Long-term trend is up, and 1-hour beats 5-minute — more to come!"

- **v8_buy_condition_4**: Price > 1h EMA100 + EMA golden cross + touches Bollinger Band lower band
  > "Mid-term trend is up, MACD golden cross, pulled back to support — buy!"

### 📊 Category 3: V9 Series (10 conditions, ALL disabled by default)
**Core Logic**: RSI oversold + Bollinger Band bottom divergence

> **Warning**: All 10 of these conditions are turned off by default! The author probably doesn't trust them 👻

- **v9_buy_condition_1~10**: Various combos of RSI oversold, volume contraction, Bollinger Band bottom
- Translation: All sorts of "bottom-fishing" logic, but the author sent them to the doghouse

### 🔍 Category 4: V6 Series (4 conditions, enabled by default)
**Core Logic**: Bollinger Band mean reversion + volume contraction

- **v6_buy_condition_0**: Price above EMA200 + touches Bollinger Band lower band
- **v6_buy_condition_1**: Price < EMA50 + touches Bollinger Band lower band + RSI 1h not too low
- **v6_buy_condition_2**: Price above EMA200 + EMA golden cross + touches Bollinger Band lower band
- **v6_buy_condition_3**: EMA golden cross + volume contraction + touches Bollinger Band lower band

**Plain English**: The core idea is — "Price hit the Bollinger Band bottom, and (maybe) it's above the long-term moving average — buy!"

---

## 4. Minimum Conditions: Just 1 Gets You In!

```python
buy_minimum_conditions = 1
```

**Translation**: This strategy has 21 conditions, but you only need to satisfy **any 1** to buy! Suddenly choice doesn't seem so hard, right? 😆

---

## 5. Exit Logic: Fancier Than the Entry

### 5.1 Tiered Take-Profit: Exit at X% Profit

The strategy uses `custom_exit` to implement 5 layers of take-profit:

| Profit Level | RSI Condition | Plain English |
|--------------|---------------|---------------|
| > 30% | RSI < 58 | "Killing it! RSI is high — time to go!" |
| > 15% | RSI < 56 | "Nice profit! Indicators are warning — go!" |
| > 4% | RSI < 50 | "4% profit, RSI is warning — go!" |
| > 1% | RSI < 50 | "Take the profit, don't be greedy!" |
| 1-4% | SMA200 death cross | "Long-term trend turned down — don't linger!" |

**Plain English**: This strategy is a "take-profits-when-you-have-them" type — the more you earn, the stricter the conditions, terrified of letting profits slip away 🦆

### 5.2 Trailing Stop: Exit on Drawdown from High

```
Tier 1: 10%-40% profit → Exit on 3% drawdown from high
Tier 2: 2%-10% profit → Exit on 1.5% drawdown from high
```

**Plain English**: Sure, it wants 20%, but if profits start shrinking — bail immediately! Classic "grab your gains and run" 😎

### 5.3 Custom Stop-Loss: The "Smart Cut-Loss" After 4 Hours

The strategy has a `custom_stoploss` function that handles losing trades after 4 hours:

| Condition | Action |
|-----------|--------|
| SMA200 death cross (5m + 1h simultaneously) | Force cut! |
| RSI 1h < 30 (might be at bottom) | Keep holding, wait for rebound |
| Price breaks below open by 2.5% AND above EMA200 | Cut |
| Price breaks below open by 1.5% | Cut |

**Plain English**:
- "Held for 4 hours and still losing? Let me check if the trend is still okay..."
- "Trend still there? Keep waiting!"
- "Trend broken? Cut it!"

### 5.4 Basic Exit Signals (4 signals)

1. **SMAOffset exit**: Price breaks below moving average → "Trend broken, go!"
2. **V8 exit #0**: Price breaks above Bollinger Band upper band for 3 candles → "Hit the top, go!"
3. **V8 exit #1**: RSI 1h > 80 → "Overbought, go!"
4. **V9 exit #0**: Price breaks above Bollinger Band middle band → "Got the profit, go!"

---

## 6. The Strategy's "Personality"

### ✅ Pros

1. **Abundant conditions**: 21 conditions, configure however you want, there's always one for the current market
2. **Multi-period confirmation**: 1-hour layer helps see the big picture, avoids being fooled by 5-minute noise
3. **Smart stop-loss**: Not a simple one-size-fits-all — makes judgments based on holding time, trend, and momentum
4. **Volume filtering**: Multiple conditions require volume contraction, reducing false breakouts

### ⚠️ Cons

1. **Too complex**: 1000+ lines of code, 21 conditions, a nightmare to debug 😅
2. **Easy to overfit**: So many conditions, easy to "conveniently" fit historical data
3. **Heavy computation**: Dual timeframe + dozens of indicators, VPS takes a beating
4. **V9 all disabled**: 10 conditions shut down by default — what's wrong with them?

---

## 7. When to Use It?

| Market Environment | Recommended Move | Reason |
|-------------------|------------------|--------|
| 🚀 Strong uptrend | Enable V8 series | 20% target + trend confirmation, big gains available |
| 📉 Dip-buying | Enable smaoffset_1 | EWO negative value good for bottom-fishing |
| 🔄 Ranging market | Adjust ROI to 10-15% | Lower targets, avoid rollercoaster rides |
| 😴 Dead consolidation | Reduce trading pairs | Hard for multiple conditions to all fire |

---

## 8. Summary: What's the Verdict?

### One-Line Rating
> "The 'Playboy' of quantitative trading — so many choices, doesn't know which one to pick"

### Who Should Use It?
- ✅ Experienced quantitative traders
- ✅ Technical folks who enjoy tweaking parameters
- ✅ Perfectionists who can handle complexity

### Who Shouldn't?
- ❌ Beginners (too high a barrier)
- ❌ Lazy folks (can't maintain it)
- ❌ People who want simplicity (this is way too complex)

### My Recommendations

1. **Start small**: Only enable the smaoffset series first, add others gradually
2. **Default config first**: Author's tuning isn't necessarily best, but at least won't be terrible
3. **Test with small money**: Complex strategies break easily — validate first
4. **Watch live trading**: Big gap between backtest and live results possible!

---

## 9. What Markets Does This Make Money In?

### 9.1 Core Logic: Building a "Defense Net" with Complexity

CoreStrategy is the **largest code** strategy in the Freqtrade ecosystem, period. Over 1000 lines — equivalent to a short novel 📚

**Its money-making philosophy**: "As long as there are enough conditions, one of them will catch the move!"

- **Multi-period confirmation**: 5 minutes + 1 hour, avoid being tricked by short-term volatility
- **Momentum filtering**: EWO, RSI momentum indicators, avoid counter-trend bottom-fishing
- **Trend priority**: Requires EMA bullish alignment, go with the flow
- **Pullback entry**: Emphasizes buying at support (Bollinger Band lower band), not chasing

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English Explanation |
|:-----------|:------:|--------------------------|
| 📈 Strong uptrend | ⭐⭐⭐⭐⭐ | Multi-period confirmation + pullback entry, catches big swings |
| 🔄 Wide-range oscillation | ⭐⭐⭐⭐ | Bollinger Band mean reversion shines in ranging markets |
| 📉 Downtrend | ⭐⭐⭐ | Has bottom-fishing conditions, but overall bullish — may fight the trend |
| ⚡️ Fast volatility | ⭐⭐⭐⭐ | 20% aggressive target great for high-volatility pairs |
| 📊 Consolidation | ⭐⭐ | 21 conditions hard to all fire simultaneously — may go dormant |

**One-liner**: This strategy performs best in **clearly trending** markets and suffers from "choice paralysis" in **sideways oscillation** 😴

---

## 10. Before Running This Strategy: Check These Configs

### 10.1 Key Parameter Configuration

| Config Item | Default | Suggestion | Notes|
|------------|--------|------------|---|
| buy_minimum_conditions | 1 | Keep at 1 | Going higher might miss many opportunities |
| minimal_roi."0" | 0.20 | 0.15-0.25 | Want 20%? Depends on the market |
| trailing_stop_positive | 0.005 | Keep | Starts trailing from 0.5% profit — way too early! |
| ewo_high | 5.499 | 5-8 | Raising reduces false signals |
| rsi_buy | 50 | 45-55 | Lower = more conservative |

### 10.2 Recommended Condition Enable Combos

**Conservative version** (only verified ones on):
```python
smaoffset_buy_condition_0_enable = True
smaoffset_buy_condition_1_enable = True
v6_buy_condition_2_enable = True
v6_buy_condition_3_enable = True
v8_buy_condition_0_enable = True
v8_buy_condition_2_enable = True
v8_buy_condition_4_enable = True
```

**Aggressive version** (all on):
```python
# Everything enabled!
# Use at your own risk 😅
```

### 10.3 Hardware Requirements (Important!)

This strategy is computationally heavy:

| # of Trading Pairs | Min RAM | Recommended RAM | Experience |
|-------------------|---------|-----------------|-----------|
| 10-20 pairs | 2GB | 4GB | Runs, but may be slow |
| 20-50 pairs | 4GB | 8GB | Recommended config |
| 50+ pairs | 8GB | 16GB | Go crazy if you want |

**Warning**: Below-minimum RAM may cause **calculation timeouts**, missing buy/sell signals! 😅

### 10.4 Backtest vs Live Trading

**Common issues**:
- Backtest: 21 conditions freely combined, always finds "perfect parameters"
- Live: Too many conditions — might miss moves because one condition didn't fire
- Slippage: Complex strategy = long calculation time = larger live slippage

**Suggested process**:
1. Backtest with default params (at least 1 year of data)
2. Observe which conditions actually generated trades
3. Gradually disable conditions that "look useless"
4. Small-capital live validation (at least 1 month)
5. Adjust params based on live performance

**Don't go all-in from the start** — this strategy runs deep! 🚢

---

## 11. Easter Eggs: The Author's "Little Tricks"

Look closely at the code and you'll find interesting things:

1. **V9 series all disabled**: 10 buy conditions, not a single one on
   > "I'm not sure if these conditions are effective — don't use them yet, let me observe more"

2. **buy_minimum_conditions = 1**: 21 conditions exist, but only 1 needs to fire to buy
   > "Stop deliberating — good enough is good enough, signal fires, we go!"

3. **Custom stop-loss timing**: 4 hours (240 minutes) is the "line"
   > "Held over 4 hours and still losing? Let me check if the trend broke or if it's a fakeout..."

4. **EWO parameters**: ewo_low = -19.881, ewo_high = 5.499
   > "-19.88% is the extreme bounce point, 5.5% is the momentum explosion point"

---

## 12. The Bottom Line

### One-Line Rating
> "The 'Choice-Paralysis Late-Stage' patient of quantitative trading — 21 conditions, there's always one for you"

### Who Should Use It?
- ✅ Experienced quantitative traders
- ✅ Technical folks who enjoy studying strategy parameters
- ✅ Perfectionists who can handle complexity
- ✅ Patient long-term optimizers

### Who Shouldn't?
- ❌ Beginners (complexity is a turn-off)
- ❌ Lazy folks (can't maintain it)
- ❌ Impatient folks (slow calculation)
- ❌ People who want simplicity

### Manual Trading Recommendations

If you don't want to use automation, focus on these core signals:
1. **smaoffset_0**: Price pulled back to moving average + EWO > 5 + RSI < 50
2. **v8_buy_0**: 1h EMA bullish alignment + Bollinger Band contraction + breaks below lower band
3. **v6_buy_2**: Price above EMA200 + EMA golden cross + touches Bollinger Band lower band

Remember: **Trend first, buy pullbacks** — don't chase! 🚢

---

## ⚠️ Final Warning

### Backtests Look Great, Live Trading Is Another Story

CoreStrategy's backtest often **looks beautiful** — 21 conditions, any combination finds "perfect parameters." But there's a trap:

> **Because there are so many conditions, the strategy easily "fits" the optimal solution for past market behavior — but that doesn't guarantee future profitability.**

Simply put: **Getting a perfect score on memorized tests doesn't guarantee you'll pass the final exam** 📝

### Hidden Risks of Complex Strategies

In live trading, complex logic can cause:
- **Signal delay**: Heavy computation, may miss optimal buy/sell points
- **Over-trading**: More conditions = possibly more trades
- **Parameter drift**: Market changes, params need retuning
- **Equity curve volatility**: Multi-condition strategies may have big wins and losses, psychology takes a hit

### My Recommendations (Sincere Advice)

```
1. Run with default params first, observe for at least 1 month
2. Don't change multiple params at once — change one at a time
3. Test with small money — big gap between backtest and live is possible
4. Review regularly — see which conditions actually generate returns
5. Don't be greedy — complex strategies flip out more easily
```

**Remember**: No matter how good a strategy is, the market doesn't play favorites. Test with small capital — survival is what matters! 🙏

---

**Final reminder**: 21 conditions sound impressive, but **what suits you is what matters most**. Don't let complexity cloud your judgment! 👀
