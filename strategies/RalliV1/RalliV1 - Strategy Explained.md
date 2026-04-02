# RalliV1 Strategy: A Masterpiece for Those with Analysis Paralysis

> **Nickname**: Six-Condition Maniac, Parameter Tuner's Delight
> **Occupation**: Wants everything, misses nothing
> **Timeframe**: 5 minutes (main) + 1 hour (info layer)

---

## I. What Is This Strategy?

Simply put, **RalliV1** is:
- A complex strategy with **6 buy conditions**
- A tuning maniac with **12 adjustable parameters**
- Uses a pile of technical indicators (EMA, SMA, HMA, RSI, EWO...)
- Born to "never miss any opportunity"

It's like someone with **a three-page dating checklist**: must be handsome, must be rich, must be gentle, must be funny, must cook... Result? **So many conditions, hard to find anyone satisfied** 🤣

---

## II. Core Configuration: "Layer Upon Layer" In Plain Terms

### Take-Profit Rules (ROI Table)

```
Time        Profit Target
────────────────────
0 minutes    4%      → Just bought, want 4%!
40 minutes   3.2%    → Didn't hit it, lower expectations
87 minutes   1.8%    → Lower a bit more
201 minutes  0%      → Whatever, just get out
```

**Translation**: Full of confidence at entry, aiming for 4% profit; after some time, just let it go; eventually let trailing stop decide.

Like dating:
- Just met: I want the perfect partner!
- 3 months later: Close enough is fine...
- 6 months later: Anyone decent will do 🤣

### Stop-Loss Rules

```
Fixed stop-loss: Lose 30% and cut (that's a big heart...)
Trailing stop: Activates at 3% profit, triggers on 0.5% pullback
Custom stop-loss: Holding 140 minutes with no profit → 0.5% tight stop
```

**Translation**:
- Fixed stop-loss at 30%, that takes some serious psychological strength
- But trailing stop protects - after 3% profit, starts "locking in gains"
- If holding for 2+ hours without profit, tightens stop and bails

---

## III. 6 Buy Conditions: I've Categorized Them For You

This strategy has an **insane number** of buy conditions. Let me break them into 3 categories:

### 🎯 Category 1: Downtrend Group (3 conditions)

**Core Logic**: MA < EMA100, looking for reversal opportunities in downtrend

**Plain English**:
> "It's a downtrend, prices are suppressed. I want to find those moments when EWO shows possible reversal and RSI shows oversold."

**Representative Conditions**: #1, #2, #3

**Classic Lines**:
- **Condition #1**: `MA < EMA100 AND close < MA * 0.975 AND EWO > 2.327`
  > "Down, but EWO shows bounce signs, let's bottom-fish!"

- **Condition #2**: `MA < EMA100 AND close < MA * 0.955 AND RSI < 25`
  > "Down even more! RSI below 25, this time it's really the bottom!"

- **Condition #3**: `MA < EMA100 AND EWO < -20.988`
  > "EWO dropped to extreme negative, bounce is coming!"

---

### 📈 Category 2: Uptrend Group (3 conditions)

**Core Logic**: MA > EMA100, looking for pullback entries in uptrend

**Plain English**:
> "It's an uptrend, wait for pullbacks to enter."

**Representative Conditions**: #4, #5, #6

**Classic Lines**:
- **Condition #4**: `MA > EMA100 AND close < MA * 0.975 AND RSI < 60`
  > "Pullback opportunity in uptrend! RSI not overbought yet, can buy!"

- **Condition #5**: `MA > EMA100 AND close < MA * 0.955 AND RSI < 25`
  > "Rallying well then suddenly dropping? Bottom-fish!"

- **Condition #6**: `MA > EMA100 AND EWO < -20.988`
  > "EWO went negative in uptrend, great opportunity to pick up bargains!"

---

### 🔧 Category 3: Special Conditions Group

**Common Requirements Across All Conditions**:

| Condition | Threshold | Plain English |
|-----------|-----------|---------------|
| RSI_fast | 4 < x < 35 | Fast RSI not too extreme |
| volume | > 0 | Must have volume |
| close | < ma_sell * high_offset | Price not too high |

**Translation**: No matter which condition, must meet three basic requirements: "volume is normal", "RSI not too extreme", "price not too high".

---

## IV. Protection Mechanism: 4-Layer "Fuse"

This strategy has four layers of stop-loss protection, like four fuses:

| Fuse | Trigger Condition | Plain English |
|------|-------------------|----------------|
| ROI Take-Profit | Profit target hit | "Made the target, bail!" |
| Trailing Stop | 0.5% pullback after 3% profit | "Profits shrinking, protect principal!" |
| Custom Stop-Loss | 140 minutes with no profit | "Held forever with no gain, stop!" |
| Fixed Stop-Loss | Lose 30% | "Giving up, cut loss!" |

This design is practical: **Take profits if possible, stop if not, never hold stubbornly!** But 30% fixed stop is indeed intense 😅

---

## V. Sell Logic: Even Flashier Than Buying

### 5.1 Sell Signals (2 conditions)

**Condition #1: Uptrend Confirmation Exit**
```
HMA50 > EMA100 AND
close > SMA9 AND
close > ma_sell * 1.0 AND
RSI_fast > RSI_slow
```

**Plain English**:
> "Price broke above moving averages, RSI momentum is up, gained enough, time to bail!"

**Condition #2: Downtrend Exit**
```
close < EMA100 AND
close > ma_sell * 0.991 AND
RSI_fast > RSI_slow
```

**Plain English**:
> "Downtrend, but price bounced a bit, better exit early!"

### 5.2 Sell Confirmation: Strategy That "Refuses" to Sell

This strategy has a `confirm_trade_exit` function:

```python
if RSI < 45 AND HMA50 > EMA100:
    return False  # Refuse to sell!
```

**Plain English**:
> "Wait! Sell signal triggered, but RSI hasn't hit 45, and trend is still up, I'll hold a bit more!"

It's like: your girlfriend says "let's break up", you say "no, I think there's still hope" 🤣

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliments)

1. **Many signals**: 6 buy conditions, basically finds entry in any market
2. **Tunable parameters**: 12 parameters to optimize, fits different assets
3. **Smart stop-loss**: Custom stop-loss function, won't stubbornly hold
4. **Has opinions**: Sell confirmation mechanism, refuses to sell easily in uptrend
5. **EWO innovation**: Uses Elliott Wave Oscillator for trend judgment, interesting

### ⚠️ Cons (Criticism)

1. **Too complex**: 6 buy conditions + 12 parameters, headache just looking at it
2. **Easy to overfit**: More parameters = easier to "memorize answers"
3. **High computation**: EMA, HMA, EWO pile of indicators, CPU under pressure
4. **Overlapping conditions**: Some conditions are basically the same, feels like padding
5. **Unused 1-hour timeframe**: Declared in code but not used, sitting on resources

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|---------------|--------|
| 📈 Slow bull oscillation | ⭐⭐⭐⭐⭐ Perfect | Multiple conditions catch pullbacks, lots of opportunities |
| 🔄 Range oscillation | ⭐⭐⭐⭐☆ Good | Frequent signals, watch for fees |
| 📉 One-sided downtrend | ⭐⭐☆☆☆ Careful | May have frequent stop-losses |
| ⚡ Rapid surge | ⭐⭐⭐☆☆ Okay | Some conditions may miss entries |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Review
> "Too many conditions to remember, too many parameters to tune, but design philosophy is worth learning."

### Who Should Use It?
- ✅ Parameter tuning enthusiasts (12 parameters await you)
- ✅ Quantitative researchers (learn complex strategy design)
- ✅ Patient players (needs repeated backtesting and optimization)
- ✅ Well-capitalized players (multiple assets to diversify risk)

### Who Shouldn't Use It?
- ❌ Beginners (too complex, easy to get confused)
- ❌ Simplicity seekers (300+ lines of code)
- ❌ Parameter-haters (12 parameters will drive you crazy)
- ❌ Small capital players (fees may eat profits)

### My Recommendations
1. **Use default parameters first**: Don't rush to tune, see baseline performance
2. **Tune in batches**: Only adjust 1-2 parameters at a time
3. **Walk-Forward analysis**: Verify parameter stability, avoid overfitting
4. **Control position sizing**: No matter how good the strategy, don't go all-in

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Building a "Safety Net" with Complexity

RalliV1 is a classic **"want everything" strategy**. 300+ lines of code - that's like a long academic paper! 📚

**Its Profit Philosophy**:
- Many conditions → Miss no opportunity
- Many parameters → Can fit any asset
- Smart stop-loss → Control risk

**Three Key Points**:
- **EMA Offset**: Price discount/premium relative to EMA determines entry/exit timing
- **EWO Judgment**: Elliott Wave Oscillator determines trend strength
- **RSI Filtering**: Multi-layer RSI (fast/slow/standard) prevents extreme market conditions

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English Explanation |
|:-----------:|:------:|---------------------------|
| 📈 Slow bull oscillation | ⭐⭐⭐⭐⭐ | All conditions find opportunities, awesome! |
| 🔄 Range oscillation | ⭐⭐⭐⭐☆ | Many signals, but watch fees |
| 📉 One-sided downtrend | ⭐⭐☆☆☆ | Many conditions can't stop the fall, frequent stop-losses |
| ⚡️ Rapid surge | ⭐⭐⭐☆☆ | Some conditions may miss the boat |

**One-Sentence Summary**: **Oscillating uptrend markets are heaven, one-sided downtrend markets are hell.**

---

## X. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Recommended | Comment |
|------------|-------------|---------|
| Trading pairs | 5-20 | Not too many, computation will explode |
| Timeframe | 5m | Default is fine, don't change |
| Startup candles | 200 | Need 200 candles to calculate indicators |

### 10.2 Key Config File Settings

```yaml
# Stop-loss
stoploss: -0.30  # 30% stop, big heart

# Trailing stop
trailing_stop: true
trailing_stop_positive: 0.005
trailing_stop_positive_offset: 0.03
trailing_only_offset_is_reached: true

# Sell settings
use_sell_signal: true
sell_profit_only: true
sell_profit_offset: 0.01
```

### 10.3 Hardware Requirements (Important!)

This strategy has **massive** computation, demanding on VPS memory:

| Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|--------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Decent |
| 10-30 pairs | 4GB | 8GB | A bit laggy |
| 30+ pairs | 8GB | 16GB | Old computer might not handle it |

**Warning**: Too many trading pairs and calculations may timeout, 5-minute candles might not finish computing! 😅

### 10.4 Backtest vs. Live Trading

**Backtesting looks great**, but be careful in live:
- Many parameters → Easy to overfit historical data
- Complex conditions → Live may behave differently than backtest
- High computation → Live may have delays

**Recommended Process**:
1. Backtest with default parameters, see baseline
2. Use Walk-Forward analysis, verify parameter stability
3. Paper trade, verify live performance
4. Small position live, confirm before scaling

**Don't go all-in at the start**, complex strategies are more prone to issues!

---

## XI. Bonus: The Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **1-hour timeframe declared but unused**
   > "I declared the 1h info layer, but... I'm just not using it~"

2. **EMA offset parameters**
   > "I don't use EMA values directly, I use EMA * 0.975 offsets, want to buy cheaper!"

3. **Custom stop-loss function**
   > "If you hold 140 minutes without profit, I'll tighten the stop and force you out!"

4. **Sell confirmation refusal mechanism**
   > "Sell signal triggered? Wait, let me check RSI and trend, looks like it could still go up... not selling!"

---

## XII. The Final Final

### One-Sentence Review
> "Complex but comprehensive, suitable for players willing to spend time tuning parameters."

### Who Should Use It?
- ✅ Quantitative researchers (learn complex strategy design)
- ✅ Parameter tuning enthusiasts (12 parameters await you)
- ✅ Patient players (need repeated backtesting)
- ✅ Multi-asset diversified players (suitable for running multiple coins)

### Who Shouldn't Use It?
- ❌ Beginners (too complex, easy to get confused)
- ❌ Parameter-haters (too many parameters)
- ❌ Simplicity seekers (code too long)
- ❌ Small capital players (fees may eat profits)

### Manual Trader Advice
If you want to borrow this strategy for manual trading...

**Forget it!** 😂

This strategy has too many conditions, impossible to calculate manually. But you can borrow some ideas:
- Use EMA offset to judge buy/sell timing
- Use EWO to judge trend strength
- Use multi-layer RSI to filter false signals

Simplify to 2-3 conditions for realistic manual trading.

---

## XIII. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting Is Beautiful, Live Trading Needs Caution

RalliV1's historical backtest may be **extremely good** - but there's a trap:

> **Because of many parameters, the strategy easily "fits" past market optimal solutions, but this doesn't guarantee future profits.**

Simply put: **You're memorizing answers, not learning knowledge.** 😅

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Calculation delay**: Candle updated but indicators not computed yet
- **Signal conflict**: Multiple conditions may give contradictory signals
- **Unstable parameters**: Today's optimal parameters may fail tomorrow
- **Overfitting risk**: More complex strategies more easily overfit historical data

### My Recommendations (Honest Truth)

```
1. Use default parameters first, don't rush to optimize
2. Use Walk-Forward analysis to verify parameter stability
3. Paper trade for at least 1 month
4. Live position控制在总资金的 10% 以内
5. If consecutive losses, stop immediately, re-evaluate
```

**Remember**: No matter how good the strategy, the market will humble you without warning. Light position testing, survival is most important!

---

**Final Reminder**: Complex strategies are like precision instruments - they look impressive but break more easily. Simple and reliable is often more important than complex and perfect! 🙏