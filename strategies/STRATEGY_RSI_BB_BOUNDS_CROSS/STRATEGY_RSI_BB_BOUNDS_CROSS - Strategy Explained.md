# STRATEGY_RSI_BB_BOUNDS_CROSS Strategy: The Dual Boundary Sniper

> **Nickname**: Boundary Crosser, Dual-Standard Hero  
> **Occupation**: Oscillating Market Bottom-Fishing Expert  
> **Timeframe**: 5 minutes

---

## I. What is This Strategy?

Simply put, **STRATEGY_RSI_BB_BOUNDS_CROSS** is a strategy that:
- Converts RSI overbought/oversold levels into price lines
- Lets Bollinger Bands and RSI boundaries fight each other
- Specifically picks "dual-boundary approved" low points to buy

It's like **two inspectors must both nod before the deal closes** — one says "this price is low enough," the other says "this oversold level is deep enough," only then will you get a buy signal! 🎯

---

## II. Core Configuration: Simply Put, "Four-Level Take Profit + Loose Stop Loss"

### Take Profit Rules (ROI Table)

```
Just bought → Target 4%
30 minutes later → Target drops to 2%
60 minutes later → Target drops to 1%
```

**Translation**: When you first enter, you're confident and want 4%; after waiting 30 minutes and still not there? 2% works too; after waiting 1 hour and still grinding? 1% will let you exit too. This is called "start high, go low, take what you can get."

### Stop Loss Rule

```
Cut at 10% loss
```

**Translation**: Giving plenty of face, 10% drawdown room, suitable for medium volatility coins. But don't think having 10% means you can be reckless — when it's time to cut, cut.

---

## III. Buy Condition: Just One, But Strict

This strategy has **only one** buy condition, but with substance inside:

### 🎯 Buy Signal: Dual Boundary Confirmation + Trend Support

**Core Logic**: Bollinger Band lower band and RSI lower boundary both say "price is low enough," and they've been saying this for 14 consecutive candles, plus short-term momentum is starting to turn upward.

**Plain English Breakdown**:

| Condition | Code | Human Translation |
|-----------|------|-------------------|
| Trend confirmation | `lb_bb_under_rsi_trend` | "For 14 consecutive candles, Bollinger Band lower band has been below RSI lower boundary" |
| Current confirmation | `bb_lb < rsi_lb` | "Right now, Bollinger Band lower band is still below RSI lower boundary" |
| Previous candle confirmation | `bb_lb.shift(1) < rsi_lb.shift(1)` | "Previous candle was also like this, stable" |
| Momentum upward | `ema2 > ema2.shift(1)` | "2-period EMA is starting to head up" |

**Classic Line**:
> "Bro, Bollinger Band says this price is low enough, RSI price boundary also says it's low enough, and for 14 consecutive candles they've both thought so. Now EMA2 is also starting to lift, get on board!" 🚗

---

## IV. Black Tech: What is RSI Price Boundary?

The biggest highlight of this strategy is **converting RSI's 70/30 levels into price lines**!

### Plain English Principle

Normal RSI is a 0-100 number, 70 is called overbought, 30 is called oversold.

But this strategy says: "Too abstract! I'll turn 70 and 30 into actual prices!"

How? Using **momentum conversion**:
- `auc`: How strong recent rises have been (upward momentum)
- `adc`: How hard recent falls have been (downward momentum)

Then using a formula to calculate: "If RSI wants to reach 70, where would price need to go? If RSI wants to reach 30, where would price need to fall?"

**This forms two 'invisible boundaries'**:
- `rsi_ub`: Price level corresponding to RSI overbought (70)
- `rsi_lb`: Price level corresponding to RSI oversold (30)

### Why Do This?

**Because Bollinger Bands are statistical boundaries, RSI boundaries are momentum boundaries — two types of boundaries for cross-verification are more reliable!**

It's like dating:
- Bollinger Band boundary = Family background check
- RSI price boundary = Personality compatibility check

**Both pass, that's the one!** 💒

---

## V. Sell Logic: Laughably Simple

### Sell Signal: Run When EMA2 Drops

```python
(dataframe['ema2'] < dataframe['ema2'].shift(1))
```

**Plain English**:
> "EMA2 is starting to head down? Run!"

That simple! When buying, all kinds of conditions and confirmations; when selling, just watch EMA2 direction change.

**Critique**:
- Buying: As thorough as a background check
- Selling: As fast as running from police

This design has its reasoning: **Be cautious when bottom-fishing, be decisive when exiting**. But it may lead to frequent stops in oscillation.

---

## VI. This Strategy's "Personality Traits"

### ✅ Advantages (Praise Section)

1. **Innovative Dual Boundary System**: The RSI price boundary concept is clever, turning abstract RSI levels into actual prices
2. **Trend Persistence Filter**: 14-period trend confirmation, not decided by one candle
3. **Cautious Buying**: Multiple confirmations reduce false signals
4. **Smoothing Treatment**: 4-period smoothing on Bollinger Band lower band reduces noise

### ⚠️ Disadvantages (Critique Section)

1. **Too Simple Selling**: Just EMA2 direction change? Bro, you were so cautious buying, and selling is this casual?
2. **No Trailing Stop**: Floating profit can turn into loss, watching profits slip away
3. **Hardcoded Parameters**: `_trend_length=14` is hardcoded, need to modify code to optimize
4. **May Get Harvested in Oscillation**: EMA2 frequently turns in oscillation, buy/sell signals frequent

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| 📈 Slow Bull Oscillation | ⭐⭐⭐⭐⭐ | Perfect match! Pullback buying, momentum confirmation, oscillation take-profit |
| 🔄 Sideways Oscillation | ⭐⭐⭐⭐☆ | Dual boundary system performs well, but selling may be too sensitive |
| 📉 One-way Downtrend | ⭐⭐☆☆☆ | Buy signals will trigger, but may buy into increasingly losing positions |
| ⚡ High Volatility | ⭐⭐☆☆☆ | EMA2 frequently turns, will get repeatedly slapped |

---

## VIII. Summary: How is This Strategy Really?

### One-Sentence Review
> "Buying like a TCM doctor — looking, listening, questioning, feeling the pulse; selling like a Didi driver — leave immediately."

### Who Should Use It?
- ✅ Oscillating market lovers
- ✅ Bottom-fishing players
- ✅ People who study both RSI and Bollinger Bands
- ✅ Those who can accept fast selling style

### Who Should NOT Use It?
- ❌ People who like chasing rises and killing falls
- ❌ One-way trend markets
- ❌ People who need trailing profit
- ❌ High-frequency traders (selling too frequently)

### My Recommendations
1. **Test on oscillating coins first**: This strategy is naturally designed for oscillation
2. **Consider adding trailing stop**: Add your own trailing_stop to lock in floating profit
3. **Adjust sell condition**: EMA2 is too sensitive, consider switching to a more stable indicator
4. **Backtest parameter optimization**: Pull out `_trend_length` for hyperparameter optimization

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Dual Boundary Cross-Verification

This strategy's innovation is **RSI Price Boundary**, converting RSI overbought/oversold levels into actual price coordinates. It's like:

**Bollinger Band says**: "Based on statistics, this price is on the low side"
**RSI Boundary says**: "Based on momentum, this price is also on the low side"

**Both agree → Buy!**

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:------------|:-------|:--------------------------|
| 📈 Slow Bull Uptrend | ⭐⭐⭐⭐☆ | Pullback buying works well, but selling may let profits escape too early |
| 🔄 Sideways Oscillation | ⭐⭐⭐⭐⭐ | This is home turf! Dual boundary confirming oscillation lows, perfect |
| 📉 One-way Downtrend | ⭐⭐☆☆☆ | Buy signals will trigger, but stop losses will bleed |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | EMA2 will frequently trigger buy/sell, fees may eat profits |

**One-Sentence Summary**: A "bottom-fishing artifact" for oscillating markets, may not adapt well to one-way trends.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Note |
|-------------------|-----------------|------|
| Timeframe | 5m | Default design, don't change |
| Startup Period | 20 | Need enough data for indicators |
| Stop Loss | -0.10 | Loose stop loss, give room for fluctuation |

### 10.2 Key Settings in Configuration File

```yaml
# Suggest adding trailing stop
trailing_stop = True
trailing_stop_positive = 0.02
trailing_stop_positive_offset = 0.03
trailing_only_offset_is_reached = True
```

### 10.3 Hardware Requirements (Important!)

This strategy has moderate calculation requirements, not demanding on VPS:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-10 | 2GB | 4GB | Smooth |
| 10-50 | 4GB | 8GB | No problem |

**Warning**: RSI price boundary calculation is a bit complex, but modern CPUs handle it easily 😎

### 10.4 Backtesting vs Live Trading

- **Backtesting looks great**: Dual boundary confirmation signals are clear
- **Live trading note**: EMA2 sell may be too sensitive

**Suggested Process**:
1. Backtest 3 months of data first
2. Paper trade for 1-2 weeks
3. Small position live testing
4. Adjust parameters based on performance

**Don't go all-in right away**, no matter how good the strategy, it needs tuning!

---

## XI. Easter Egg: The Strategy Author's "Little Thoughts"

Looking carefully at the code, you'll find some interesting things:

1. **Bollinger Band Smoothing**: `_bb_smooth_length = 4`, the author knew Bollinger Band lower band has noise, actively applied smoothing
   > "Bro, I know raw data is too jittery, let me smooth it for you"

2. **Trend Period Matches RSI Period**: `_trend_length = 14`, same as RSI period, not a coincidence
   > "Using RSI's period to confirm trend, logically consistent"

3. **Lots of Commented-Out Code**: The author tried various approaches, finally leaving this version
   > "Tried countless paths, finally chose this one"

---

## XII. The Very Last Thing

### One-Sentence Review
> "Innovative dual boundary system, rigorous buying and decisive selling, worth trying in oscillating markets."

### Who Should Use It?
- ✅ Oscillating market lovers
- ✅ People who like innovative indicators
- ✅ Those who can accept fast selling style
- ✅ People with patience for parameter optimization

### Who Should NOT Use It?
- ❌ One-way trend seekers
- ❌ People who need trailing profit
- ❌ High-frequency traders
- ❌ People who don't like modifying code (hardcoded parameters)

### Suggestions for Manual Traders

If you're trading manually, you can use this strategy's concept like this:

1. **Draw Bollinger Bands**: Period 14, standard deviation 2
2. **Calculate RSI Price Boundaries**: Use formula to convert RSI 30/70 to prices
3. **Wait for Dual Boundary Resonance**: Bollinger Band lower band < RSI lower boundary
4. **Confirm Persistence**: 14 consecutive candles all like this
5. **EMA2 Upward**: Short-term momentum turning
6. **Buy!**

---

## XIII. ⚠️ Risk Re-emphasis (Must Read Section)

### Backtesting is Beautiful, Live Trading Needs Caution

RSI_BB_BOUNDS_CROSS's historical backtest performance may be **quite good** — but there's a trap:

> **Dual boundary confirmation looks stable, but situations where both indicators fail can also happen.**

Simply put: **"Two agreements don't equal certainty, just a lower probability of being wrong."**

### Hidden Risks of Complex Boundary Calculation

In live trading, RSI price boundary calculation may lead to:
- **Calculation Delay**: Complex momentum conversion may be slow in high-frequency scenarios
- **Boundary Failure**: Both boundaries may distort in extreme market conditions
- **Signal Lag**: 14-period confirmation means signal delay

### My Suggestion (Heartfelt Words)

```
1. Test on oscillating coins (like stablecoin pairs) first
2. Add trailing stop to lock in floating profit
3. Optimize sell condition, don't fully trust EMA2
4. Start with small positions, observe live performance
```

**Remember**: No matter how good the strategy, when the market teaches you a lesson, it doesn't give notice. Light position testing, staying alive is most important! 🙏

---

**Final Reminder**: RSI price boundary is a clever operation, but clever as it is, live verification is king. Good luck! 🍀