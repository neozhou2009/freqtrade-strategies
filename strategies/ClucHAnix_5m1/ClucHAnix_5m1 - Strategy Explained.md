# ClucHAnix_5m1 Strategy: The "Picky" Bollinger Band Strategy

> **Nickname**: The Picky One, Optimization Freak, Timing Expert  
> **Profession**: 5-minute trend catcher, specifically "picking at the edges" of Bollinger Bands  
> **Timeframe**: 5 Minutes (primary) + 1 Hour (informational, for the big picture)

---

## 1. What's This Strategy?

In simple terms, **ClucHAnix_5m1** is a:
- Short-term strategy using "smoothed candles" (Heikin Ashi) to eliminate noise
- Specifically watching the lower Bollinger Band, waiting for price to drop too far before bottom-fishing
- Extremely strict about the big picture — 1-hour ROC must exceed 0.79 before it will buy

Think of it as a **picky foodie** — won't just eat anything. First confirms the restaurant (market) is truly in an uptrend, then waits until the dish (price) really drops to a bargain before picking up chopsticks (buying) 🥢

Breaking down the name:
- **Cluc** = series "family name"
- **HAnix** = Heikin Ashi + Bollinger Band architecture
- **_5m1** = 5-minute timeframe, version 1

---

## 2. Core Settings: "Fast In, Fast Out, Take Profits Early"

### Take-Profit Rules (ROI Table)

```
Immediately after buying          10% and run
After 30 minutes                  5% and run
After 1 hour                      2% and run
```

**Translation**: This impatient fellow wants to lock in profits as soon as possible. Think about it — if you can make 10% right after buying, you run. If you haven't made more after half an hour, you'd be happy with 5%. If it's been dragging for an hour, 2% is fine too, just run!

Much simpler than its big brother ClucHAnix_5m — brother had 6 tiers of take-profit, this kid has just 3, keeping it simple and clean.

### Stop Loss Rules

```python
# Nominal stop loss
stoploss = -0.99  # Almost like not setting one

# What really matters is this dynamic trailing stop:
Profit exceeds 6.4%   → Stop line moves up, locking in most profits
Profit 1.1%-6.4%     → Stop position dynamically calculated by profit
Profit below 1.1%    → Hard stop at -10%
```

**Translation**: This strategy doesn't do fixed stops — it uses a "dynamic lifeline." The more you earn, the higher the protection line rises. The motto is "don't give back profits you've already made."

---

## 3. Two Entry Conditions: Categorized for You

This strategy's entry conditions follow two paths, but both **must first pass one checkpoint** — 1-hour ROC > 0.79.

This threshold is ridiculously high! The big brother version was only 0.54, but this kid jumped straight to 0.79, a **47% increase**! Meaning: **"The big picture isn't strong enough, I won't buy."**

### Condition 1: Bollinger Band Oversold Rebound (Condition #1)

**Core logic**: Price breaks below the lower Bollinger Band, but the drop has "structure," not random chaos.

**Plain English**:
> "Price has broken below the lower Bollinger Band, and the Bollinger Band has opened up (indicating enough volatility), price movement has amplitude (not a fake drop), wick is short (the drop was decisive) — time to buy and wait for a rebound!"

**Specific conditions** (all must be satisfied):
1. 1-hour ROC > 0.79 → Big picture must be strong
2. Bollinger Band width > close × 1.889% → Band must be open
3. Close price change > close × 0.916% → Price must fluctuate
4. Lower wick < Bollinger Band width × 72.2% → Wick can't be too long
5. HA close < lower Bollinger Band → Broke below the band
6. HA close ≤ previous close → Still falling

**Classic tagline**:
- The essence of Condition #1: `ha_close < lower.shift()` → "Close broke below the lower Bollinger Band, bottom-fishing opportunity!"

### Condition 2: EMA Deviation Rebound (Condition #2)

**Core logic**: Price is too far from the 50-period EMA, it must regress eventually, confirmed by lower Bollinger Band.

**Plain English**:
> "Price is way too far from the 50-day MA, like a rubber band stretched too far — it has to snap back. If price happens to be near the lower Bollinger Band, this is a bottom-fish!"

**Specific conditions** (all must be satisfied):
1. 1-hour ROC > 0.79 → Big picture must be strong
2. HA close < 50-period EMA → Price below long-term average
3. HA close < lower Bollinger Band × 1.27% → Hugging the lower band

**Classic tagline**:
- The essence of Condition #2: `ha_close < ema_slow` → "Price has deviated too far from the MA, regression is inevitable!"

---

## 4. Protection Mechanisms: Dynamic Trailing Stop保命

This strategy's stop loss is "alive," unlike rigid fixed stops:

| Profit Range | Stop Position | Plain English |
|-------------|--------------|---------------|
| < 1.1% | -10% | "Just bought, admit defeat after losing 10%" |
| 1.1% - 6.4% | Linear calculation | "Made some money, stop line rises as profit grows" |
| > 6.4% | Follows profit upward | "Making big money! Stop line closely follows, don't let profits escape" |

**Commentary**: This design is clever. Unlike some strategies that use fixed stops even when winning, causing all gains to be given back in a single pullback, this one is **"the more you earn, the tighter the protection"** — the motto is "don't give back what's already in your pocket!"

There's also a **trend filtering protection**:
- 1-hour ROC must > 0.79 before buying
- This acts as a "big picture bodyguard," directly blocking counter-trend orders

---

## 5. Exit Logic: More Elaborate Than Entries

### 5.1 Base Exit Signal

**Trigger conditions** (all must be satisfied):
1. Fisher indicator > 0.39 → Overbought
2. HA highest price declining for 3 consecutive candles → Can't rise anymore
3. HA close declining → Starting to fall
4. 3-period EMA > close price → MA pressing down on price from above
5. Close > Bollinger middle band × 99.75% → Near the middle band
6. Volume present → Not a fake breakout

**Plain English**:
> "Fisher says overbought, candles going down for 3 straight times, MAs starting to press on price, and price has climbed to the middle of the Bollinger Band — time to run or when?!"

### 5.2 Tiered Take-Profit

| Time | Target Profit | Description |
|------|--------------|-------------|
| Just bought | 10% | Best case, run immediately |
| After 30 minutes | 5% | Acceptable, lock in profits |
| After 1 hour | 2% | Barely acceptable, just run |

**Plain English**:
- Make 10% right after buying? Don't wait, run!
- After 30 minutes still at 5%? Time to go, don't be greedy!
- After an hour still dragging? Take 2% and go — time is money too!

---

## 6. Strategy Personality

### Pros

1. **Picky but reliable**: 0.79 ROC threshold only buys in strong markets, reduces counter-trend traps
2. **Simple and clean**: ROI only has 3 tiers, much simpler than the 6-tier big brother version
3. **Smart stop loss**: Dynamic trailing stop, tighter protection the more you earn
4. **Classic principles**: Bollinger Band mean reversion is a time-tested strategy with clear logic
5. **Many high-frequency opportunities**: 5-minute level, potentially dozens of opportunities per day

### Cons

1. **Threshold too high**: 0.79 ROCR may cause missing many profitable opportunities
2. **Fee sensitive**: Too many trades, fees are a significant expense — need a low-fee exchange
3. **Parameters may be overfitted**: These numbers are all optimized, past performance doesn't guarantee future results
4. **Not suitable for consolidation**: ROC can't reach 0.79 during consolidation, strategy basically "lies flat"
5. **Depends on 1-hour confirmation**: All entries wait for 1-hour data confirmation, slight delay

---

## 7. When to Use It

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Slow bull trend | Enable | Best environment — buy on pullbacks, trend continues |
| Ranging markets | Applicable | Bollinger Band mean reversion has advantages in ranging markets |
| Declining trend | Use with caution | Only goes long, but ROC threshold auto-filters |
| Pump and dump | Applicable | Has dynamic stop-loss to protect profits |
| Flat consolidation | Not recommended | ROC can't reach 0.79, strategy basically hibernates |

---

## 8. Bottom Line: Is This Strategy Any Good?

### One-Line Verdict
> "A picky Bollinger Band strategy — only bottom-fishes in strong markets, would rather miss than buy wrong."

### Who's It For?
- People who like **high-frequency trading** and pursue capital turnover
- People with **low-fee** channels
- People who can accept **larger stop-loss** (-10%) swings
- Professional traders who understand **trend following**
- People with **patience** for strategy optimization and parameter tuning

### Who's It NOT For?
- People who like **long-term holding**
- People with **high fees**
- People who are **risk-averse**
- People with **no quantitative trading experience**
- People who specialize in **consolidation markets**

### My Advice
1. **Backtest first**: Test strategy effectiveness with historical data
2. **Check indicators**: Confirm win rate, profit-to-loss ratio, max drawdown
3. **Paper trade**: Run in paper-trading mode for 1-2 weeks to observe
4. **Small capital**: Start with small real capital for testing
5. **Scale up gradually**: Increase position only after confirming effectiveness

---

## 9. What Markets Does This Strategy Make Money In?

### 9.1 Core Logic: Trading "Pickiness" for Safety

ClucHAnix_5m1 is the **"Picky Version" of the ClucHAnix series**. Code isn't too complex, but the logic is clever — it doesn't chase opportunities, it pursues **"buying correctly."**

**Its money-making philosophy**:
- **Pick the big picture**: Only buys when 1-hour ROC > 0.79, follows the trend
- **Pick the position**: Only buys near lower Bollinger Band, low absorption has safety margins
- **Pick the timing**: Regression after EMA deviation, rides the momentum

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English |
|:---|:---|:---|
| Slow bull trend | Excellent | "Designed exactly for this market! Buy on pullbacks, trend continues, beautiful" |
| Ranging markets | Good | "Bollinger Band mean reversion has advantages in ranging markets, buy low sell high" |
| Declining trend | Poor | "Only goes long, but ROC threshold auto-filters, basically doesn't buy" |
| Pump and dump | Moderate | "Has dynamic stop-loss protection, but extreme markets may have big slippage" |
| Flat consolidation | Very Poor | "ROC can't reach 0.79, strategy lies flat, basically doesn't trade" |

**One-line summary**: This strategy is most comfortable in markets **trending up but occasionally pulling back**, and most miserable in **flat consolidation**.

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended | Commentary |
|---------------|-------------|------------|
| Number of pairs | 10-20 | Diversify risk, don't put all eggs in one basket |
| Per-pair position | 2-5% | Each pair shouldn't exceed 5% of total capital |
| Total position | <50% | Keep some cash for extreme situations |

### 10.2 Key Config Settings

```yaml
# Take-profit table
minimal_roi:
  "0": 0.10    # 10% take-profit
  "30": 0.05   # 5% take-profit after 30 minutes
  "60": 0.02   # 2% take-profit after 60 minutes

# Stop loss (nominally, actually uses dynamic stop)
stoploss: -0.99

# Trailing stop
trailing_stop: true
trailing_stop_positive: 0.001
trailing_stop_positive_offset: 0.012
```

### 10.3 Hardware Requirements (Important!)

5-minute-level computation isn't too heavy, but running many pairs simultaneously still has requirements:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|-----------------|------------|
| 10-20 pairs | 2GB | 4GB | Smooth |
| 20-50 pairs | 4GB | 8GB | Good |
| 50+ pairs | 8GB | 16GB | Recommend splitting |

**Warning**: If RAM isn't enough, calculation timeouts may occur, missing trading opportunities!

### 10.4 Backtesting vs. Live Trading

**Key differences**:
1. **Slippage**: Backtesting uses theoretical prices, live fills may slip a few percentage points
2. **Fees**: If backtesting doesn't include fees, results will be very misleading
3. **Liquidity**: Small-cap coins may not get the desired fill price

**Recommended process**:
1. Backtest with historical data, check win rate and profit-to-loss ratio
2. Paper trade for 1-2 weeks, observe real performance
3. Small-capital live test, confirm execution没有问题
4. Scale up gradually, don't go all-in right away

**Don't go all-in right away**, even the best strategy needs a磨合 period!

---

## 11. Bonus: The Strategy Author's "Little Tricks"

Looking closely at the code, you can spot some fun design choices:

1. **ROCR threshold set at 0.79 is not random**
   > "This number came from hyperopt optimization, meaning it performed best near 0.79 in historical data. But remember, history doesn't guarantee future!"

2. **ROI table only has 3 tiers, half of the big brother's**
   > "Simplified design, reduced overfitting risk. Less is sometimes more, complexity can be bad."

3. **Lower wick requirement dropped from 0.99 to 0.72**
   > "Relaxed the entry condition, allowing longer wicks, meaning more trading opportunities."

4. **Dynamic stop-loss breakpoints (1.1% and 6.4%)**
   > "These two numbers are also optimized, finding the balance between 'protecting profits' and 'giving profit room.'"

---

## 12. The Bottom Line

### One-Line Verdict
> "A picky trend catcher — would rather miss than buy wrong, suitable for patient experienced traders."

### Who's It For?
- Traders with quantitative experience
- Investors who can accept high-frequency trading
- Short-term scalpers pursuing capital turnover
- People with low-fee channels

### Who's It NOT For?
- Quantitative beginners
- Exchange users with high fees
- People who like long-term holding
- Risk-averse people

### Manual Trading Tips

If you're a manual trader, you can learn a few tricks from this strategy:
1. **Trend filtering**: First check big-period ROC to confirm trend, then do small-period
2. **Bollinger Band bottom-fishing**: After price breaks below lower band, wait for stabilization before entering
3. **Dynamic stop loss**: The more you earn, the higher the stop line rises

---

## 13. ⚠️ Final Warning (Must Read!)

### Backtesting Looks Great, But Live Trading Is a Different Beast

ClucHAnix_5m1's historical backtest may **look beautiful** — but here's the trap:

> **Because all parameters are optimized, the strategy easily "memorizes test answers," but this doesn't guarantee future profitability.**

Simply put: **"Perfect historical transcript ≠ guaranteed future good grades."**

### Hidden Risks of Complex Strategies

In live trading, watch out for these pitfalls:
- **Fees eating profits**: Too many 5-minute trades, fees may devour most of your profits
- **Uncontrollable slippage**: Market orders may have fills far from expectations
- **Liquidity risk**: Small-cap coins may not get the fill prices you want
- **Overfitting trap**: Too well-optimized parameters may just be "memorizing historical data"

### My Real Advice

```
1. Backtest, but don't blindly trust backtest results
2. Paper trade for at least 2 weeks, observe real performance
3. Start with small capital, no more than 10% of your funds
4. Fees! Fees! Fees! Find a low-fee exchange
5. Review regularly, adjust parameters based on market changes
```

**Remember**: No matter how good the strategy, the market doesn't care when it comes to teach you a lesson. Test with light positions, staying alive is what matters! 🙏

**Final reminder**: This strategy has very high requirements for the big picture (ROC > 0.79), and may not trade at all in ranging or declining markets. If you can't handle "not trading for long periods," this strategy may not suit your personality.
