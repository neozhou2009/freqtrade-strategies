# NotAnotherSMAOffsetStrategyHO: Strategy Explained

## 1. What Does This Strategy Do?

### 1.1 One-Line Summary

This is a strategy specifically designed to **find pullback buying opportunities in uptrends**, like buying famous brands on sale — trend is good, just temporarily discounted, grab it!

### 1.2 What Does the Name Mean?

**NotAnotherSMAOffsetStrategyHO** broken down:
- **NotAnother**: Don't underestimate me, I'm not just any strategy
- **SMA**: Simple Moving Average (though actually uses EMA)
- **Offset**: Offset — not only looking at whether price reaches MA, but by how much it deviates
- **HO**: Likely "High Optimization" — heavily optimized version

Simply put, this is a **"use MA to find bargains"** strategy.

---

## 2. Core Principles in Plain English

### 2.1 Strategy's Core Idea

Imagine you're climbing a mountain. This strategy: **wait for rest stops (price pullback), then you climb up to grab bargains**.

It doesn't buy at the peak (too expensive), doesn't wait at the bottom (may catch a falling knife), but chooses to buy at **the rest stop halfway up**.

### 2.2 What is "Offset"?

This is the strategy's smartest feature!

**Regular MA strategy**: Buy when price crosses above MA
- Problem: By the time it crosses, price has already risen; you bought expensive

**Offset strategy**: **Wait below MA to buy**
- Set offset coefficient 0.966, meaning buy when price falls to 96.6% of MA
- Equivalent to 3.4% off — like buying pants at 96.6 yuan when tagged 100 yuan

### 2.3 Why Three Buy Signals?

Like exams have multiple choice, judgment, and fill-in — different question types test different knowledge.

Three signals:
- **ewo1**: Normal pullback, straightforward buy
- **ewo2**: Deep pullback, brave bottom-fishing
- **ewolow**: Market panic, contrarian

No matter how the market moves, there's a corresponding tactic.

### 2.4 What is EWO?

EWO (Elliott Wave Oscillator) is simply **the difference between two MAs**:
- A fast MA (quick)
- A slow MA (slow)

When fast MA is above slow MA: EWO is positive, market rising
When fast MA is below slow MA: EWO is negative, market falling

The strategy uses EWO to judge: **Is the major trend up or down**

---

## 3. What Indicators Are Used?

### 3.1 Indicator Overview

| Indicator | Role | Analogy |
|-----------|------|---------|
| EMA | Trend line, major direction | Highway center line |
| HMA | Fast-reacting trend line | Gas pedal, go when pressed |
| SMA | Short-term trend | Speedometer, shows speed |
| RSI | Overbought/oversold, sentiment | Thermometer, market fever or cold |
| EWO | Trend strength | Compass, direction finding |
| Volume | Trading volume | Fuel gauge, how much gas in tank |

### 3.2 Three RSI Periods

RSI is a 0-100 number showing if market is "overheated" or "too cold."

The strategy uses three RSIs:
- **RSI_4** (fast): Like a stopwatch, reacts in seconds
- **RSI_14** (standard): Like a clock, normal time-reading
- **RSI_20** (slow): Like a calendar, sees long-term changes

Why three? Like weather — check current temperature (RSI_4), today's average (RSI_14), this week's trend (RSI_20).

### 3.3 EMA vs SMA

- **SMA**: Equal weight to all prices, arithmetic average
- **EMA**: Recent data weighted more, faster reaction

Strategy uses EMA as primary judgment because it's faster.

### 3.4 What is HMA?

HMA (Hull Moving Average) is **both fast AND smooth**.

Regular MAs are either fast but jittery, or smooth but slow. HMA is both. Strategy uses it to judge trend reversal because HMA reacts fast and catches problems early.

---

## 4. When to Buy?

### 4.1 Three Keys to Buy

| Signal | Market Situation | General Meaning |
|--------|-----------------|----------------|
| ewo1 | Bull normal pullback | Climbing, rest for a bit |
| ewo2 | Deep pullback | Dropped deep, bottom-fish |
| ewolow | Bear end | Fell to the bottom, wait for rebound |

### 4.2 Key 1: ewo1 (Main Buy Signal)

**Scenario**: Climbing a mountain, was steadily going up, suddenly tired and rested. ewo1 says: **Now resting, will climb again later, buy now!**

**Conditions**:
1. Fast RSI < 35: Market panicked, everyone selling
2. Price < MA's 96.6%: 3.4% cheaper
3. EWO > 3.422: Major trend still up, just temporarily fell
4. RSI < 52: Not overheated yet, okay to buy
5. Volume > 0: Not a dead market

**Win rate**: Highest, because following the trend

**Risk**: Medium, pullback may continue

### 4.3 Key 2: ewo2 (Deep Pullback)

**Scenario**: This climb not only tired but slipped, fell pretty deep. ewo2 says: **Fallen this much, near the bottom, go!**

**Conditions**:
1. Fast RSI < 35: Market panicked
2. Price < MA's 95.1%: ~5% cheaper
3. EWO > -4.58: Fell but not catastrophically
4. RSI < 52: Not overheated
5. RSI < 25: Extremely oversold
6. Volume > 0

**Win rate**: Medium

**Risk**: Higher, bottom-fishing can fail

### 4.4 Key 3: ewolow (Reversal Signal)

**Scenario**: Not climbing anymore, fell to the valley bottom. ewolow says: **Can't fall further, prepare for reversal!**

**Conditions**:
1. Fast RSI < 35: Market panicked
2. Price < MA's 96.6%: Relatively cheap
3. EWO < -8.562: Fell terribly
4. Volume > 0

**Win rate**: Lower

**Risk**: Highest, catching a falling knife

### 4.5 Signal Comparison

| Signal | Win Rate | Expected Return | Risk | Best Scenario |
|--------|----------|----------------|------|--------------|
| ewo1 | High | Medium | Medium | Bull pullback |
| ewo2 | Medium | Higher | Higher | Deep pullback |
| ewolow | Low | Highest | Highest | Bear reversal |

**Advice**: Beginners use ewo1 more; experts can try ewo2 and ewolow.

---

## 5. When to Sell?

### 5.1 Two Sell Signals

| Signal | Meaning | Analogy |
|--------|---------|---------|
| Condition 1 | Rose to target, time to sell | Arrived at stop |
| Condition 2 | Can't rise anymore, running away | Leaking, patch it fast |

### 5.2 Condition 1: Rose to Target, Sell

**Conditions**:
1. Price > short-term MA (SMA_9): Short-term trend up
2. Price > sell MA's 100.2%: Above baseline
3. RSI > 50: Market still strong
4. Fast RSI > Slow RSI: Momentum upward
5. Volume > 0

**Plain English**: Rose to the planned position, although may rise more, strategy suggests taking the money and running, don't be greedy.

### 5.3 Condition 2: Trend May Reverse, Get Out

**Conditions**:
1. Price < HMA (fast MA): Broke below fast trend line
2. Price > sell MA's 101.4%: Still profitable
3. Fast RSI > Slow RSI: Momentum still up (possibly fake)

**Plain English**: Rose to high ground but starting to fall, trend may change, protect your profits now.

### 5.4 Satisfy Either, Sell

The two conditions are **OR** — selling if either is met. Benefits:
- Condition 1 catches upwardmarkets
- Condition 2 catches reversal signals
- Hard to miss sell opportunities

---

## 6. How is Risk Controlled?

### 6.1 Stop-Loss: 35% Hard Bottom Line

```python
stoploss = -0.35
```

Bought at $100, drops to $65 → forced sell.

**Why 35%?** Crypto swings 10% in a day normally. Too tight gets stopped by normal fluctuation. 35% is balanced.

**Newbie advice**: If 35% feels harsh, change to 25% or 30% yourself.

### 6.2 Trailing Stop: Follow Price, Lock Profits

**How it works**:
1. After buying, don't rush
2. Wait for price to rise 3%, trailing stop activates
3. Stop line follows highest price, maintaining 0.5% distance
4. Price retraces to stop line → auto-sell

**Example**:
- Bought at $100
- Rose to $103 (3% gain), trailing stop activates
- Rose to $110, stop line at $109.45 ($110 × 99.5%)
- Dropped to $109.45 → auto-sell, locked 9.45% profit

**Benefit**: Whatever it rises, locks in more.

### 6.3 Tiered Take-Profit

| Holding Time | Profit Target | Meaning |
|-------------|--------------|---------|
| 0 min | 28.9% | Rose 28.9% immediately, sell now |
| 25 min | 10.5% | Held 25 min, 10.5% is fine |
| 80 min | 3.8% | Held 80 min, 3.8% is fine |
| 140 min | 0% | Held 140 min, sell even if breakeven |

**Design logic**:
- Just bought with a big bounce → run, don't be greedy
- Held longer → lower expectations
- Held over 140 min still not profitable → you're wrong, get out

### 6.4 Only Sell When Profitable

Strategy sets `sell_profit_only = True` — **don't sell losing trades!**

Unless triggered 35% stop-loss, sell signals don't execute in loss. Like: bought stock at $100, down $10, sell signal rang but strategy says "wait, that'd be cutting losses."

### 6.5 Risk Control Summary

| Measure | Trigger | Effect |
|---------|---------|--------|
| Fixed stop-loss | Loss 35% | Survival bottom line |
| Trailing stop | Profit 3% activates | Locks profits |
| Tiered ROI | Time + profit ratio | Controls greed |
| Profit-only sell | Profit >1% | Avoid cutting losses |
| Slippage protection | Slip >2% reject | Controls costs |

---

## 7. What Do Parameters Mean?

### 7.1 Buy Parameters

| Parameter | Value | Meaning | Adjustment |
|-----------|-------|---------|------------|
| base_nb_candles_buy | 16 | MA period for buying | Larger = smoother, smaller = more sensitive |
| low_offset | 0.966 | Main offset | Lower = need bigger discount, fewer signals |
| low_offset_2 | 0.951 | Backup offset | For bottom-fishing |
| ewo_high | 3.422 | ewo1 threshold | Positive means must be in uptrend |
| ewo_high_2 | -4.58 | ewo2 threshold | Expanded buy opportunities |
| ewo_low | -8.562 | ewolow threshold | For reversal signals |
| rsi_buy | 52 | RSI threshold | Lower = more conservative |

### 7.2 Sell Parameters

| Parameter | Value | Meaning |
|-----------|-------|---------|
| base_nb_candles_sell | 10 | Sell MA period (faster than buying) |
| high_offset | 1.014 | Price 1.4% above MA to consider selling |
| high_offset_2 | 1.002 | Price 0.2% above MA to consider selling |

**Why sell faster than buy?**
- Buy MA: 16 candles → slow, more observation
- Sell MA: 10 candles → fast, don't be greedy

---

## 8. Strategy Pros & Cons

### 8.1 Pros

**1. Triple buy signals, many opportunities**
- Bull has ewo1
- Deep pullback has ewo2
- Bear reversal has ewolow
- Whatever the market, there's a play

**2. Offset design, better entry prices**
- Not chasing buys, waiting for discounts
- 3-5% cheaper than crossing MA

**3. Comprehensive risk control**
- Stop-loss, trailing stop, tiered take-profit
- Slippage protection too
- Multiple insurance policies

**4. Good for optimization**
- Many adjustable parameters
- Can optimize for different coins and markets

**5. Clear labels**
- Every buy tagged (ewo1/ewo2/ewolow)
- Backtesting shows which signal makes the most money

### 8.2 Cons

**1. Stop-loss too wide**
- 35% loss for newbies is harsh
- One bad trade loses a third

**2. Too many parameters**
- Newcomers don't know how to adjust
- Wrong parameters = poor results

**3. Ranging market losses**
- If prices oscillate, MA useless
- Frequent buys/sells, eats fees

**4. Long only, no shorting**
- Makes money in bull, sits idle in bear
- Misses bear market opportunities

**5. No volume change analysis**
- Only checks volume > 0
- Doesn't analyze if volume increasing or decreasing

### 8.3 How to Maximize Strengths, Minimize Weaknesses

**Handle wide stop-loss**:
- Reduce stop-loss yourself, e.g., to 25%
- Or reduce position size, invest less per trade

**Handle parameter overload**:
- Start with default parameters in backtest
- Then optimize slowly, one parameter at a time

**Handle ranging markets**:
- Use strategy's built-in filters
- Or manually judge — don't run during ranging

**Handle long-only limitation**:
- Pair with another shorting strategy
- Or only run strategy when major trend is up

---

## 9. Who Is This For?

### 9.1 Ideal User Profile

**Suitable if you**:
- Have some quantitative trading basics
- Can handle moderate risk
- Have 2-4 hours daily to monitor
- Want short-to-medium term trades
- Interested in BTC, ETH, and major coins

**Not suitable if you**:
- Know nothing about quantitative trading
- Risk-averse (losing 10% keeps you up at night)
- Don't have time to monitor
- Want long-term investments
- Only play small coins

### 9.2 Newbie Advice

1. **Paper trade for one month first** — use virtual money, watch performance, don't rush live
2. **Start with low-risk parameters** — only use ewo1 signal, 10% position, 25% stop-loss
3. **Daily review** — analyze every trade's entry/exit, why profit, why loss, find patterns
4. **Control emotions** — strategy says buy → buy, strategy says sell → sell, don't manually intervene

### 9.3 Capital Allocation

| Capital | Suggested Per-Trade Position | Reason |
|---------|-----------------------------|--------|
| < $5000 | Not recommended | Fee proportion too high |
| $5000-$20000 | 20% | Under 5 trades, controllable risk |
| $20000-$100000 | 15% | Diversify across 6-7 trades |
| > $100000 | 10% | Conservative priority |

---

## 10. Common Questions

### Q1: Why called "NotAnother"?

**A**: Developer's little joke — means "this is not just another ordinary MA strategy." And indeed, this strategy is much more complex and refined than simple MA strategies.

### Q2: Is 35% stop-loss too high?

**A**: For crypto, 35% isn't really high. Bitcoin swings 10% in a day normally. Too tight gets stopped out by normal fluctuation.

**Advice**: Adjust to 20-25% if you can't handle it.

### Q3: Why 5-minute candles?

**A**: 5 minutes is the balance between short and medium:
- Shorter (1 min): Too noisy, too many false signals
- Longer (1 hr): Too few signals, miss too many opportunities

**Advice**: Newcomers can start with 15 minutes.

### Q4: Which of the three buy signals should I use?

**A**: Suggested order:
1. Newcomers: only ewo1
2. After familiar: add ewo2
3. Experts only: ewolow

### Q5: Can this be used on stocks?

**A**: In theory, but note:
- Stocks less volatile than crypto
- Need parameter adjustments
- Stop-loss can be smaller (e.g., 10%)

### Q6: How many trades per day?

**A**: Depends on volatility:
- High volatility: 3-5 per day possible
- Low volatility: may go all day without a signal
- Average: 1-2 per day

### Q7: How are fees calculated?

**A**: Per trade:
- Buy: one fee
- Sell: one fee
- One round trip: two fees

**Assuming 0.1% fee, buying $10,000**:
- Buy fee: $10
- Sell fee: $10 (assuming still selling $10,000)
- Total cost: $20

**Advice**: Use maker orders (limit orders) for lower fees.

### Q8: Backtest great, live bad — why?

**A**: Common issue, reasons:
- Backtest doesn't consider slippage
- Backtest fees may be set too low
- Past data, future may differ

**Advice**:
- Discount backtest results by 30%
- Verify with paper trading
- Test live with small money first

---

## 11. Practical Tips

### 11.1 Parameter Optimization Tips

**Step 1**: Run backtest with default parameters
```bash
freqtrade backtesting --strategy NotAnotherSMAOffsetStrategyHO
```

**Step 2**: Optimize optimizable parameters
```bash
freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --epochs 500 --spaces buy sell
```

**Step 3**: Re-backtest with optimal parameters, compare results

**Warning**: Don't over-optimize! Perfect historical fit may perform worse going forward.

### 11.2 Market Judgment Tips

Before running strategy, judge market state:

| Market State | How to Judge | Strategy Adjustment |
|-------------|-------------|---------------------|
| Bull | Price above long-term MA | Can increase position |
| Ranging | Oscillating, no clear direction | Reduce position or don't run |
| Bear | Price below long-term MA | Only use ewolow, reduce position |

### 11.3 Dynamic Stop-Loss Adjustment

Adjust stop-loss by market volatility:

- **High volatility** (wildmarkets): Widen stop to 40%
- **Low volatility** (quiet consolidation): Tighten stop to 25%

### 11.4 Multi-Coin Portfolio

Don't run just one coin — run multiple:

| Coin | Risk | Expected Return |
|------|------|----------------|
| BTC | Low | Steady |
| ETH | Medium | Medium |
| Other majors | High | Potentially high |

**Recommendation**: 60% BTC/ETH, 40% other majors.

---

## 12. Comparisons with Other Strategies

### 12.1 vs Regular MA Strategy

| Comparison | This Strategy | Regular MA Strategy |
|-----------|--------------|---------------------|
| Entry timing | Offset entry, position early | Cross entry, chase |
| Signal count | Three signals, many opportunities | Usually one signal |
| Risk control | Multiple protections | Usually just stop-loss |
| Complexity | Relatively complex | Simple |

**Conclusion**: This strategy is more refined, but needs more understanding.

### 12.2 vs Grid Strategy

| Comparison | This Strategy | Grid Strategy |
|-----------|--------------|--------------|
| Suitable market | Trending | Ranging |
| Trading frequency | Medium | High |
| Fees | Medium | High |
| Risk control | Active | Passive |

**Conclusion**: Use this strategy in trends, use grid in ranging markets.

### 12.3 vs High-Frequency Strategy

| Comparison | This Strategy | High-Frequency |
|-----------|--------------|---------------|
| Time frame | 5 minutes | Seconds |
| Frequency | Low | Extremely high |
| Tech requirement | Medium | Extremely high |
| Capital threshold | Low | High |

**Conclusion**: Retail traders use this strategy; institutions use high-frequency.

---

## 13. Summary — One Line to Remember

**"In an uptrend, wait for price to pull back below MA by a set percentage, buy in three batches, lock profits with trailing stop."**

### 13.1 Key Points

1. **Only trade pullbacks**: Not chasing, waiting for dips
2. **Triple signals**: Different depths for different markets
3. **Offset entry**: Find bargains below MA
4. **Multi-layer risk control**: Stop-loss + trailing + ROI
5. **Adjustable parameters**: Adapt to different markets

### 13.2 Pre-Launch Checklist

Before enabling strategy, confirm:

- [ ] Understand strategy principles
- [ ] Run backtest
- [ ] Exchange API set up
- [ ] Capital amount set
- [ ] Stop-loss set
- [ ] Notification methods set
- [ ] Time to monitor available

### 13.3 Final Thoughts

This strategy is a tool, not a holy grail. Even the best strategy needs:
- Understanding principles
- Strict execution
- Continuous learning
- Emotion control

Good luck trading!

---

*Document Version: 1.0*
*For: Quantitative trading beginners to intermediate players*
