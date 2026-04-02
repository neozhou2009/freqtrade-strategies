# Apollo11 Strategy: The "Moon Landing Program" of Quant Trading

> **Nickname**: Three-Eye Radar, Defensive Offensive Master  
> **Job**: Multi-Signal Fusion Strategy / Risk Control Expert  
> **Timeframe**: 15 minutes (15m)  
> **Author**: Shane Jones (Twitter: @shanejones)

---

## 1. What Is This Strategy?

Simply put, **Apollo11** is:
- A "radar" with triple signal scanning
- A "defense tower" protected by 5 layers of fuses
- A "profit harvester" with dynamic stop loss locking

Like a hunter equipped with 3 different radars—one watching trends, one finding oversold, one tracking volume-price—whichever goes off, you can shoot 🎯

**One-sentence summary**: A defensive offensive strategy, trading complexity for safety.

---

## 2. Core Configuration: Simply Put, "Protect When Profiting, Limit When Losing"

### Take Profit Rules (ROI Table)

```
After 0 minutes: Sell at ≥ 10% profit
After 30 minutes: Sell at ≥ 5% profit
After 60 minutes: Sell at ≥ 2% profit
```

**Translation**: Just bought? Need 10% to sell. 30 minutes later? 5% is fine. After an hour? Even 2% is good enough. This isn't greed, it's "the longer you wait, the more conservative you get."

### Stop Loss Rules

```
Fixed stop loss: Admit defeat at 16% loss
Dynamic stop loss: More profit = tighter protection
  - Profit > 20%: Lock in 4% profit
  - Profit > 10%: Lock in 3% profit
  - Profit > 6%: Lock in 2% profit
  - Profit > 3%: Lock in 1% profit
```

**Translation**: Made money? Don't panic, I'll guard it for you. The more you make, the tighter I guard.

### Special Handling for Long Holdings

```
Loss > 10%, holding > 60 hours: Dynamically tighten stop loss
Loss > 8%, holding > 120 hours: Further tighten
```

**Plain English**:
> "Held for 2.5 days and still losing 10%? Fine, stop holding on, I'll help you stop loss."

---

## 3. 3 Entry Signals: I've Categorized Them for You

This strategy's entry conditions are quite complex, I've grouped them into 3 categories:

### 🎯 Category 1: Trend Following Type (Signal #1)

**Core Logic**: Follow the big trend, wait for pullback to board

**Indicator Configuration**:
- 240 EMA (Ultra-long trend line)
- 5 EMA / 10 EMA (Short trend crossover)
- VWMACD (Volume-weighted MACD)

**Trigger Conditions** (Plain English translation):
1. VWMACD below signal line → "Momentum not yet overheated"
2. Low broke 240 EMA but close recovered → "Fake breakdown, real support"
3. 5 EMA crosses above 10 EMA → "Short trend starting to look up"
4. 3 EMA below 50 EMA → "Not chasing at high position"

**Plain English**:
> "Big trend is up, short-term pullback to support, then small trend starts turning. Time to board!"

**Suitable Scenario**: Moderate uptrend market, trend is clear but not overheated.

---

### 📉 Category 2: Extreme Oversold Type (Signal #2)

**Core Logic**: Be greedy when others are fearful, buy bottoms at extreme oversold

**Indicator Configuration**:
- Bollinger lower band (3 standard deviations, very wide)
- Fibonacci extension lower band (4.236 × ATR, even wider)
- 50 EMA offset line

**Trigger Conditions** (Plain English translation):
1. Fibonacci lower band crosses above Bollinger lower band → "Price has fallen to grandma's house"
2. Close below offset EMA → "Still at low position"
3. Volume exists → "Someone is trading"

**Plain English**:
> "Price broke below Bollinger lower band, even below Fibonacci extension's extreme level. At this point? Others are fearful, I'm greedy!"

**Suitable Scenario**: Rebounds after crashes, bottom fishing at oscillation range edges.

**Roast**: This signal triggers very rarely, but when it does, it's usually a nice bottom fishing opportunity. Just need patience 🤣

---

### 📊 Category 3: Volume-Price Breakout Type (Signal #3)

**Core Logic**: Price oversold + capital involvement = Rebound opportunity

**Indicator Configuration**:
- Bollinger lower band (oversold detection)
- Volume-weighted MA (volume-price relationship)
- 50 EMA (trend confirmation)

**Trigger Conditions** (Plain English translation):
1. Low below Bollinger lower band → "Oversold"
2. High above slow volume-price MA → "Capital starting to get involved"
3. High still below 50 EMA → "Not at high position"
4. Volume exists → "Confirmed valid"

**Plain English**:
> "Price is oversold, but big money is starting to secretly buy in. Follow the smart money!"

**Suitable Scenario**: Bottom reversals, accumulation phase.

---

## 4. Protection Mechanisms: 5 Layers of "Fuses"

Each entry signal comes with 5 layers of protection, like installing 5 fuses on the strategy:

| Protection Type | Trigger Condition | Stop Duration | Plain English |
|-----------------|-------------------|---------------|---------------|
| Cooldown Period | After each sell | 0 minutes | "Can buy again immediately" (seems useless 🤣) |
| Maximum Drawdown | 20 trades within 12h with >20% drawdown | 1 hour | "Lost too much, take a break" |
| Stop Loss Protection | ≥4 stop losses within 6h | 30 minutes | "Consecutively trapped, calm down" |
| Low Profit Protection (Short) | ≥2 trades with <2% profit within 1.5h | 15 minutes | "This pair isn't working, take a break" |
| Low Profit Protection (Long) | ≥4 trades with <1% profit within 6h | 30 minutes | "Not making money long-term, pause a bit" |

**Roast**: These 5 layers of protection are like putting 5 bulletproof vests on the strategy. A bit over the top, but better than naked exposure 🛡️

---

## 5. Exit Logic: No Active Selling, All Relies on Stop Loss and ROI

### 5.1 No Technical Exit Signals

This strategy **doesn't use technical indicators to judge exits**, completely relies on:
- ROI table (the longer the time, the lower the take-profit threshold)
- Custom stop loss (profit protection + time stop loss)

**Plain English**:
> "I only handle entry timing, exit timing is left to stop loss and ROI."

### 5.2 Tiered ROI Take-Profit

```
Just bought: Only sell at 10% profit
After 30 minutes: Sell at 5% profit
After 1 hour: Sell at 2% profit
After 1+ hours: Let stop loss decide
```

**Translation**:
- "New position? I want to make it big!"
- "Held for half an hour and still haven't made 10%? 5% is fine too."
- "It's been an hour already, 2% and I'm out."

---

## 6. This Strategy's "Personality Traits"

### ✅ Advantages (Compliment Section)

1. **Multi-Dimensional Signals**: 3 signals cover trend, oversold, volume-price, don't rely on single judgment
2. **Protection in Place**: 5 layers of protection mechanisms, from drawdown to stop loss to low profit, layers of defense
3. **Dynamic Stop Loss**: More profit = tighter protection, scientific profit locking
4. **Open Parameters**: All parameters adjustable, easy to optimize
5. **Community Verified**: From open-source project, someone has used it

### ⚠️ Disadvantages (Roast Section)

1. **No Active Selling**: Misses optimal technical exit points, all relies on stop loss
2. **Too Many Parameters**: 7 EMAs alone, optimizing gives headaches
3. **Large Startup Data**: Needs 480 candles (5 days data) for warmup
4. **Overfitting Risk**: So many indicators, backtesting looks good but live trading might flop

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|-------------------|--------|
| Moderate Uptrend | ✅ Enable all 3 signals | Trend signals most effective |
| Oscillating Market | ✅ Enable signal 2 | Focus on oversold rebounds |
| High Volatility | ⚠️ Enable signals 1+3 | Combine trend and volume-price |
| Downtrend | ❌ Use cautiously | May trigger frequent stop losses |

---

## 8. Summary: How Is This Strategy Really?

### One-Sentence Review
> "A defensive offensive strategy, trading complexity for safety. Suitable for intermediate to advanced players willing to study parameters."

### Who Should Use It?
- ✅ Intermediate to advanced quantitative traders—can understand various indicators
- ✅ People focused on risk control—5 layers of protection is reassuring
- ✅ People who like optimizing parameters—many open parameters
- ✅ People with live trading experience—know the difference between backtesting and live

### Who Shouldn't Use It?
- ❌ Beginners—too many parameters, easy to get confused
- ❌ People who want to save effort—needs debugging and optimization
- ❌ Short-term maniacs—15-minute timeframe not for ultra-short-term
- ❌ People pursuing simplicity—this strategy is quite complex

### My Advice
1. **Backtest with default parameters first**: Understand the strategy's basic performance
2. **Understand each signal one by one**: Don't optimize everything at once
3. **Focus on protection mechanisms**: This strategy's core advantage is risk control
4. **Small position live trading**: Good backtesting doesn't mean good live trading

---

## 9. What Market Can This Strategy Make Money In?

### 9.1 Core Logic: Using Complexity to Build a "Defense Net"

Apollo11 is a **defensive offensive strategy**. 200+ lines of code, 10+ indicators, what does that mean? Equivalent to a fully equipped special forces soldier 🎖️

**Its Money-Making Philosophy**: Better to earn less than to lose big

- **Trend Following Primary**: Signals 1 and 3 both follow trends
- **Oversold Rebound Secondary**: Signal 2 specializes in bottom fishing
- **Protection Mechanism Safety Net**: 5 layers of protection prevent consecutive losses
- **Dynamic Stop Loss Profit Locking**: The more earned, the tighter the guard

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Moderate Uptrend | ⭐⭐⭐⭐⭐ | Trend aligns, signals 1 and 3 work great, take-profit on point |
| 🔄 Oscillating Market | ⭐⭐⭐⭐☆ | Signal 2 bottom fishing effective, protection mechanisms reduce losses |
| 📉 Downtrend | ⭐⭐☆☆☆ | Frequent stop loss triggers, recommend reducing position |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | Trend judgment may be wrong, need parameter adjustment |

**One-sentence summary**: Suitable for moderate uptrend or oscillating markets, be careful in downtrend markets.

---

## 10. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|--------------------|-------------------|---------|
| max_open_trades | 3-5 | Not too many, protection mechanisms will limit you |
| stake_amount | 2-5% | Single position, don't go all-in |
| startup_candle_count | 480+ | Must be this much, one less won't work |

### 10.2 Key Config File Settings

```json
{
    "max_open_trades": 4,
    "stake_amount": "unlimited",
    "tradable_balance_ratio": 0.99,
    "fiat_display_currency": "USD",
    "dry_run": true,
    "cancel_open_orders_on_exit": false,
    "unfilledtimeout": {
        "buy": 10,
        "sell": 30
    }
}
```

### 10.3 Hardware Requirements (Important!)

This strategy has moderate computation, has certain memory requirements for VPS:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|--------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-30 pairs | 4GB | 8GB | Smooth |
| 30+ pairs | 8GB | 16GB | Watch CPU |

**Warning**: 480 candle warmup + 10+ indicator calculations, low-spec VPS might lag 😅

### 10.4 Backtesting vs Live Trading

Due to custom stop loss, backtesting and live trading may differ:
- Volume-weighted indicators may differ across exchanges
- Stop loss logic may not be precise in backtesting
- Recommend dry_run testing first

**Recommended Process**:
1. Backtest to understand basic performance
2. dry_run to test actual signals
3. Small position live verification
4. Optimize parameters based on performance

**Don't go all-in on day one**, no matter how good the strategy, it needs磨合!

---

## 11. Easter Egg: The Strategy Author's "Little Thoughts"

Looking carefully at the code, you'll find some interesting things:

1. **Signal Switch Design**: `buy_signal_1 = True` etc. switch design
   > "I've reserved optimization space for you, turn on whichever you want"

2. **240 EMA as Trend Baseline**: Ultra-long period EMA
   > "I use 240 EMA to judge big trend,不服?"

3. **Fibonacci 4.236× Extension**: Extreme oversold detection
   > "Normal people use 1.618, I use 4.236. This is real bottom fishing!"

4. **5-Layer Protection Mechanism**: Layers of defense
   > "I'd rather miss out than be wrong. Safety first!"

5. **Custom Stop Loss Tiered Protection**: Profit in 4 tiers
   > "Made 3%, guard 1%. Made 20%, guard 4%. Stair-step protection, scientific!"

---

## 12. Final Words

### One-Sentence Review
> "A defensive offensive strategy, suitable for intermediate to advanced players. Worth diving deep if you're willing to study parameters."

### Who Should Use It?
- ✅ Intermediate to advanced quantitative traders
- ✅ People focused on risk control
- ✅ People who like multi-signal confirmation
- ✅ People with time to optimize parameters

### Who Shouldn't Use It?
- ❌ Quantitative beginners—too many parameters, easy to get confused
- ❌ People who want to save effort—needs debugging
- ❌ Ultra-short-term players—15-minute timeframe not suitable
- ❌ People pursuing simplicity—this strategy is complex

### Advice for Manual Traders

This strategy has good reference value for manual traders:

1. **Dynamic Stop Loss**: Learn this tiered profit protection approach
2. **Multi-Signal Confirmation**: Don't place orders based on just one indicator
3. **Protection Mechanisms**: Set up a few layers of "fuses" for yourself too
4. **Time Stop Loss**: Holding too long without profit? Consider stopping loss

---

## 13. ⚠️ Risk Re-emphasis (This Part Is a Must-Read)

### Backtesting Looks Great, Live Trading Requires Caution

Apollo11's historical backtesting performance might be very good—but there's a trap:
> **Because there are so many parameters, the strategy can easily "fit" the optimal solution for past market conditions, but this doesn't mean it will definitely profit in the future.**

Simply put: **A student who memorizes answers won't do well on a different test.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Slippage Loss**: Time difference between signal trigger and order placement
- **Volume Differences**: Backtesting volume data may not be accurate
- **Stop Loss Imprecision**: Custom stop loss may fail in extreme markets
- **Over-Protection**: 5 layers of protection may cause you to miss some opportunities

### My Advice (Honest Words)

```
1. dry_run for at least a week first
2. Observe signal trigger frequency and quality
3. Compare backtesting results with dry_run results
4. Small position live trading, gradually increase
5. Record every trade, periodically review
```

**Remember**: No matter how good the strategy, when the market teaches you a lesson, it won't give advance notice. Test with small positions, survival is most important! 🙏

---

**Final Reminder**: No matter how complex the strategy, the market is always more complex. Respect the market, control risk!