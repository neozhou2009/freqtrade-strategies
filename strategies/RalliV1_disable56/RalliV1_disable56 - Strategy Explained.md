# RalliV1_disable56 Strategy: Professional Bear Market Bottom-Fisher

> **Nickname**: EWO Catcher, Bear Market Hunter
> **Occupation**: Specializes in fixing various forms of non-compliance (oversold)
> **Timeframe**: 5 minutes

---

## I. What Is This Strategy?

Simply put, **RalliV1_disable56** is:
- A "bottom-fisher" that specifically looks for opportunities during downtrends
- Uses Elliott Wave Oscillator (EWO), a relatively niche indicator
- Two different approaches for bull and bear markets - speaks human to humans, ghost to ghosts

Like a **contrarian investor specialized in bottom-fishing** 🤣

---

## II. Core Configuration: "Run When Profitable, Accept When Losing"

### Take-Profit Rules (ROI Table)

```
0 minutes: 4% profit then run
40 minutes: 3.2% is okay too
87 minutes: 1.8% still acceptable
After 201 minutes: Even mosquito-sized profit is fine
```

**Translation**: This strategy isn't greedy, 4% profit is satisfying. If waiting too long, even small gains are fine to exit.

### Stop-Loss Rules

```
Fixed stop-loss: -30% (this... is quite large)
Trailing stop: Activate at 3% profit, lock 0.5%
Time stop: Holding 140 minutes still losing? Kick out with -0.5%
```

**Translation**: Stop-loss set quite large (30%), but trailing stop and time stop provide backup - a "loose first, tight later" design.

---

## III. 4 Buy Conditions: I've Categorized Them For You

This strategy's buy conditions are **scenario-designed**, I've categorized them into 2 types:

### 🎯 Type 1: Bear Market Bottom-Fishing (3 conditions)

**Core Logic**: Below EMA100, oversold rebound

**Plain English**:
> "In a bear market, everyone's running, I'll go in and pick up chips - but wait for truly oversold moments."

**Representative Conditions**: #1, #2, #3

**Classic Lines**:
- **Condition #1**: `MA_buy < EMA_100 & EWO > 2.327` → "Momentum suddenly strengthening in bear market, could be reversal signal"
- **Condition #2**: `RSI < 25 & EWO > -2.327` → "Dropped enough, momentum improving, let's go!"
- **Condition #3**: `EWO < -20.988` → "Extremely extremely oversold, high bounce probability"

---

### 📈 Type 2: Bull Market Pullback (1 condition)

**Core Logic**: Above EMA100, pullback buying

**Plain English**:
> "In a bull market, everyone's buying, I wait for pullbacks to enter - chasing highs is impossible, never in my life will I chase highs."

**Representative Condition**: #4

**Classic Lines**:
- **Condition #4**: `MA_buy > EMA_100 & RSI_fast < 35 & EWO > 2.327` → "Bull market pullback, momentum still there, go!"

---

## IV. Protection Mechanism: Three "Firewalls"

Behind every buy condition is triple protection, like **wearing three layers of bulletproof vests**:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| Fixed stop-loss | -30% floor | "Maximum 30% loss, shouldn't happen... right?" |
| Trailing stop | Activates at 3% profit | "Made money, lock some, don't give it back" |
| Time stop | 140 minutes + loss | "Positions that dawdle too long don't stay" |

One complaint: 30% fixed stop-loss is **really quite large**, if hitting extreme market... 🙃

---

## V. Sell Logic: Two Paths Available

### 5.1 Sell Signal #1: Bull Market Reversal

```
HMA_50 > EMA_100 (major trend upward)
Close price > SMA_9 (breaking short-term MA)
Close price > MA_sell * 0.997 (breaking sell line)
RSI_fast > RSI_slow (momentum accelerating)
```

**Plain English**:
> "In bull market, price breaks through various MAs, momentum still accelerating - time to take profits."

---

### 5.2 Sell Signal #2: Bear Market Fake Breakout

```
Close price < EMA_100 (still bear market)
Close price > MA_sell * 0.991 (breaking short-term line)
RSI_fast > RSI_slow (momentum improving)
```

**Plain English**:
> "In bear market, price suddenly breaks out - could be fake breakout, run quickly!"

---

### 5.3 Smart Sell Refusal

There's also a fancy move:

```python
if RSI < 45 and HMA_50 > EMA_100:
    return False  # Refuse to sell
```

**Plain English**:
> "Long-term trend upward, but RSI not heated yet? Don't sell, might still go up!"

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliments)

1. **Dual-scenario adaptation**: Works in both bull and bear markets, won't lie flat like some strategies in bear markets
2. **EWO indicator unique**: Few people use this indicator, might have alpha others don't see
3. **Triple stop-loss**: Although fixed stop is large, trailing and time stops compensate
4. **Won't chase highs**: All buy conditions require "price below certain MA", no chasing

### ⚠️ Cons (Criticism)

1. **30% stop too large**: Really, 30% is quite scary, suggest adjusting smaller
2. **EWO extremes fixed**: -20.988 value might not apply to all coins
3. **Few sell signals**: Only 2 sell conditions, might miss some exit opportunities
4. **Too many parameters**: Optimizable parameters pile up, easy to overfit

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|--------------------|---------------|--------|
| Oscillating downward | Full use | Specializes in oversold rebounds |
| Slow bull | Lower ewo_high | Many pullback buying opportunities |
| Surge | Careful use | Strategy conservative, can't keep up |
| Sideways | Normal use | Both overbought/oversold signals available |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Review
> "A strategy specialized in picking up chips in bear markets, can also play bull market pullbacks, but don't expect it to chase surges."

### Who Should Use It?
- ✅ Contrarian investors who like bottom-fishing
- ✅ Patient holders who can accept larger drawdowns
- ✅ Regular oscillating market players
- ✅ People wanting to use EWO, this niche indicator

### Who Shouldn't Use It?
- ❌ Aggressive types who chase highs and cut lows
- ❌ People who can't accept 30% drawdown (suggest changing stop)
- ❌ Bull market only players
- ❌ Beginners not wanting to study EWO indicator

### My Recommendations
1. **Reduce stop-loss**: 30% to 10-15%, much better psychological tolerance
2. **Optimize per coin**: Different coins have different EWO extremes, need individual tuning
3. **Simulate before live**: Many parameters, easy to overfit
4. **Watch RSI_fast**: This is the core oversold signal source

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Using EWO to Find "Reversal Points"

RalliV1_disable56 is a variant of Rallipanos strategy series. 200+ lines of code, clear logic, mainly relies on EWO indicator for profit.

**Its Profit Philosophy**: Enter when others panic, exit when others get greedy.

- **EWO extreme negative**: Market panic, severe oversold, high reversal probability
- **Price deviation from MA**: Price too far from MA, mean reversion will return
- **RSI confirmation**: Momentum confirms oversold, not fake drop

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English Explanation |
|:-----------:|:------:|---------------------------|
| 📈 Slow bull | ⭐⭐⭐⭐☆ | Pullback buying works well, no chasing, steady profits |
| 🔄 Oscillating | ⭐⭐⭐⭐⭐ | Home turf! Eating overbought/oversold back and forth, fees become profits |
| 📉 Downtrend | ⭐⭐⭐☆☆ | Bear market bottom-fishing has chances, but timing hard to grasp |
| ⚡️ Surge | ⭐⭐☆☆☆ | Strategy too conservative, can't keep up with rhythm, just watch others profit |

**One-Sentence Summary**: Oscillating markets are its home turf, slow bull works too, surges forget it.

---

## X. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Recommended | Comment |
|------------|-------------|---------|
| Trading pair count | 10-30 | Too many can't handle |
| Volatility | Medium | Too stable coins EWO insensitive |
| Timeframe | 5 minutes | Must use 5 minutes, other cycles need re-optimization |

### 10.2 Key Config File Settings

```yaml
# config.json key configurations
"timeframe": "5m",
"startup_candle_count": 200,  # Need 200 candles to warm up
"trailing_stop": true,
"trailing_stop_positive": 0.005,
"trailing_stop_positive_offset": 0.03
```

### 10.3 Hardware Requirements (Important!)

This strategy has medium computation, VPS memory requirements not high:

| Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|--------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Normal |
| 50+ pairs | 8GB | 16GB | Slightly laggy |

**Warning**: If running 50+ pairs on old computer, might timeout 😅

### 10.4 Backtest vs. Live Trading

This strategy uses `process_only_new_candles = True`, backtest and live behavior consistent.

**Recommended Process**:
1. First Hyperopt optimize parameters (at least 1000 rounds)
2. Backtest with 6+ months data
3. Paper trade 1-2 weeks
4. Small capital live test
5. Gradually increase position

**Don't go all-in at start**, even good strategies need adaptation!

---

## XI. Bonus: The Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **disable56 meaning**: Commented out original strategy's #5 and #6 buy conditions, showing author found those two conditions ineffective
   > "Practice brings truth, ineffective conditions cut directly"

2. **Time stop 140 minutes**: Very precise number, possibly author's tested optimal time
   > "Wait too long without profit, better switch to another"

3. **EWO parameters 5/200**: Fast line 5, slow line 200, 40x difference
   > "Short-term momentum vs long-term trend, extreme values are opportunities"

---

## XII. The Final Final

### One-Sentence Review
> "A thoughtful bottom-fishing strategy, using EWO this niche indicator to find reversal points, good profit effect in oscillating markets."

### Who Should Use It?
- ✅ People who can accept larger drawdown (or willing to change stop)
- ✅ Contrarian thinkers who like bottom-fishing, dislike chasing highs
- ✅ Oscillating market players
- ✅ People with time for parameter optimization

### Who Shouldn't Use It?
- ❌ Weak psychological tolerance
- ❌ Only play surge markets
- ❌ Don't want to study EWO indicator
- ❌ No time for backtest optimization

### Manual Trader Advice
If you want to manually use this strategy's signals:
1. Watch when EWO rises from around -20
2. Start watching when RSI_fast < 35
3. Bull market use condition #4, bear market use conditions #1-3
4. Don't chase highs, wait for pullbacks!

---

## XIII. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting Is Beautiful, Live Trading Needs Caution

RalliV1_disable56's historical backtest may be **quite good** - but there's a trap:

> **This strategy has many optimizable parameters, easily "fits" past market optimal solutions, but doesn't guarantee future profits.**

Simply put: **Memorizing answers is easy, doing new problems is hard**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Parameter sensitive**: Switch coins, previously optimized parameters may fail
- **Overfitting**: More precise tuning, more future performance may drop
- **Signal reduction**: 4 buy conditions vs only 2 sell conditions, more entries fewer exits

### My Recommendations (Honest Truth)

```
1. Change 30% stop to 10-15%
2. Optimize parameters separately for 2-3 coins
3. Run at least 6 months backtest data
4. Paper trade at least 2 weeks before live
5. Monthly check if parameters need re-optimization
```

**Remember**: No matter how good the strategy, the market will humble you without warning. Light position testing, survival is most important! 🙏