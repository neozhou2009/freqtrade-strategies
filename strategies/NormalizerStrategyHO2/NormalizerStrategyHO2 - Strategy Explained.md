# NormalizerStrategyHO2 Strategy: The Optimized "Price Position Detector"

> **Nickname**: Optimized Normalization Hunter, Hyperopt-Tuned Version  
> **Profession**: Mean reversion type, a "trained" version  
> **Timeframe**: 1 Hour (suitable for medium-term operation)

---

## 1. What's This Strategy?

Simply put, **NormalizerStrategyHO2** is:
- A mean reversion strategy based on normalization technology
- A Hyperopt-optimized version of the original NormalizerStrategy
- Multi-tier ROI take-profit design, pursuing "make big money quickly, make small money slowly"
- Uses math to quantify "expensive" and "cheap"

Think of it like having an original "price position detector" and then hiring someone to calibrate the parameters to make it theoretically more accurate. HO2 is that "calibrated version" 🔧

**What does "HO2" mean?**
- HO = Hyperopt Optimization (hyperparameter optimization)
- 2 = Second version/second optimization
- Basically "the version tuned with historical data"

---

## 2. Core Settings: Basically a "Four-Tier Take-Profit Table"

### Take-Profit Rules (ROI Table)

```
Holding time           Minimum profit target
────────────────────────────────────────────────
Immediately after buy   35% (I want the big one!)
After 6.75 hours         24.8% (Okay, that's acceptable)
After 14.6 hours         9.1% (Been a while, less profit is fine too)
After 26.4 hours          0% (Break even, I'm done)
```

**Translation**:
- This strategy is "greedy" — demands 35% profit right off the bat
- But if price drags its feet and holding time gets long, it becomes more "zen"
- After 26 hours, even break-even is acceptable, doesn't want to waste time anymore

**Difference from the original**:
- Original: Single target 18%, reach it and run
- HO2 version: Four-tier declining targets, 35% → 24.8% → 9.1% → 0%

### Stop-Loss Rules

```
Stop-loss line: -99%
```

**Translation**:
- Basically equals "no stop-loss" 🫠
- Price has to drop 99% before conceding defeat, how much heart does that take?
- This design is betting "mean reversion will definitely happen"

---

## 3. Entry Conditions: Low Normalized Price Zone

This strategy's entry logic boils down to one sentence:

**"Price is too cheap, time for a rebound, right?"**

### Target: Normalization Buy Method

Imagine a thermometer from 0 to 100:
- 0 = Lowest price in the historical range
- 100 = Highest price in the historical range
- 50 = Middle price

**Entry Condition**:
> "Thermometer reading below a certain threshold (e.g., 20), means it's cold now and should warm up"

**Plain English**:
> "This price is pretty cheap compared to recent history, according to historical patterns, shouldn't it bounce?"

---

## 4. Exit Logic: Four-Tier Stepped Take-Profit

### 4.1 Four-Tier Take-Profit Table

| Timepoint | Profit Target | Strategy Mindset |
|-----------|--------------|-----------------|
| Immediately | 35% | "I want big money!" |
| After 6.75 hours | 24.8% | "Okay, good enough" |
| After 14.6 hours | 9.1% | "Been a while, less profit is fine too" |
| After 26.4 hours | 0% | "Break even, I'm done, don't want to waste time" |

**Plain English**:
- Strategy demands 35% profit right off the bat — ambitious
- But if price doesn't cooperate and holding time gets long, it lowers expectations
- This is "time-decay take-profit" — the longer you wait, the more zen you become

### 4.2 Other Exit Scenarios

| Scenario | Trigger Condition | Plain English |
|----------|-------------------|---------------|
| Mean Reversion | Normalized value too high | "Price is too expensive, time to sell" |
| Stop-Loss | Lose 99% | "Completely give up" (rarely happens) |

---

## 5. The Strategy's "Personality Traits"

### Advantages (The Praise Section)

1. **Optimized**: Parameters tuned by Hyperopt, theoretically more accurate
2. **Multi-Tier Take-Profit**: Unlike the original's rigidity, gives price more time to perform
3. **High Return Target**: 35% initial target means only going for high-quality signals
4. **Time Management**: Lowers expectations as holding time increases, doesn't hold indefinitely
5. **Clear Logic**: Normalization concept is intuitive, unlike Nostalgia's complexity

### Limitations (The Roast Section)

1. **Overfitting Risk**: Hyperopt optimization may be "memorizing answers" — looks good historically, not necessarily future-proof 🤣
2. **Too Relaxed Stop-Loss**: -99% stop-loss is basically naked, extreme markets kill you directly
3. **Few Signals**: 35% target too high, may go a long time without a trade
4. **Optimization Trap**: Looks like perfect parameters, may just happen to match historical data
5. **Lacks Trailing Profit**: If price surges past 35%, can't make more

---

## 6. When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Wide Ranging | StarsStarsStarsStarsStars Strong recommendation | Best environment, price bounces within range repeatedly |
| Sideways Consolidation | StarsStarsStarsStars Recommended | Secondary best, suitable for range trading |
| Slow Bull | StarsStarsStars Usable | Catches pullbacks but misses the main trend |
| Narrow Ranging | StarsStarsStars Average | Too little volatility, hard to reach 35% target |
| Slow Bear | StarsStars Careful | Price keeps dropping, mean reversion may fail |
| Extreme Volatility | Star Not recommended | Price breaks range, normalization fails |

---

## 7. Difference from Original: What's Different in HO2?

| Comparison | Original NormalizerStrategy | HO2 Version |
|------------|----------------------------|--------------|
| ROI Design | Single 18% | Four-tier declining 35%→24.8%→9.1%→0% |
| Parameter Source | Manual settings | Hyperopt optimization |
| Stop-Loss | -99% | -99% (equally "zen") |
| Return Target | Medium | High (35%) |
| Trading Frequency | Medium | Possibly lower (high target=fewer signals) |
| Overfitting Risk | Low | High (all optimized ones have this risk) |

**One-Line Summary**:
> Original is a "regular person", HO2 is a "person who's been specially trained" — but not necessarily stronger, may just be better at "historical exams" 📝

---

## 8. Bottom Line: How's This Strategy Really?

### One-Word Verdict
> "An optimized normalization hunter, pursues high returns but scarce signals, Hyperopt optimization is a double-edged sword."

### Who Should Use It?
- Traders who believe in mean reversion
- Patient types who can endure long periods without trades
- Tech-savvy types who understand normalization
- Quantitative veterans familiar with Hyperopt limitations

### Who Should NOT?
- People seeking high-frequency trading
- Conservative types who can't accept -99% stop-loss
- Beginners who blindly trust optimized parameters
- People wanting mean reversion in strong trending markets

### My Advice
1. **Lower the target**: Reduce initial ROI from 35% to 15%-25%, more signals
2. **Add a stop-loss**: -99% is too zen, suggest setting -15% to -30% actual stop-loss
3. **Out-of-sample testing**: After optimizing with historical data, must verify on new data
4. **Use in ranging markets**: This strategy is designed for ranges, don't use in one-sided trends

---

## 9. What Markets Does This Strategy Make Money In?

### 9.1 Core Logic: Normalization + Hyperopt Optimization

NormalizerStrategyHO2 is a **mean reversion strategy**. Its core is simply:

> "Buy when cheap, sell when expensive, tune parameters with historical data."

Its Money-Making Philosophy:
- Use normalization to judge if price is "expensive"
- Use Hyperopt to find historically optimal parameters
- Use multi-tier ROI to manage holding time

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:---|:---|:---|
| Slow Bull | StarsStarsStars | Price keeps going up but you're still waiting for a dip, miss the action |
| Slow Bear | StarsStars | Price keeps dropping, you bottom-fish at half the mountain |
| Wide Ranging | StarsStarsStarsStarsStars | Best! Price bounces around, you buy low sell high, sweet |
| Narrow Ranging | StarsStarsStars | Usable but profit potential limited |
| Extreme Volatility | StarsStars | Price breaks range, all normalization parameters go haywire |
| Sideways Consolidation | StarsStarsStarsStars | Secondary best environment |

**One-Line Summary**:
> "This strategy is a ranging-market harvester, a one-sided trend's cash incinerator." 💸

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Commentary |
|-------------|-------------------|-------------|
| Number of trading pairs | 3-10 | Fewer means even fewer signals, more means can't manage |
| Timeframe | 1h (default) | Can try 30m or 4h |
| Simultaneous positions | 2-5 | Don't exceed 5, capital spreads too thin |

### 10.2 Parameter Adjustment Recommendations

```yaml
# Recommended adjusted parameters
minimal_roi:
  "0": 0.20      # From 35% to 20%, more signals
  "360": 0.12    # 6 hours later 12%
  "720": 0.06    # 12 hours later 6%
  "1440": 0      # 24 hours later break even

stoploss: -0.25  # Don't use -99%, 25% stop-loss is more respectful
```

### 10.3 Hardware Requirements (Not Important)

This strategy has low computational demand:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------------|-------------|----------------|-------------|
| 1-5 pairs | 1GB | 2GB | Silky smooth |
| 5-20 pairs | 2GB | 4GB | Smooth |
| 20+ pairs | 4GB | 8GB | No problem |

### 10.4 Backtest vs. Live Trading

**Important Warning**:
> Hyperopt-optimized strategies' backtest performance is often "stunning", live trading may "flop".

Reason:
- Parameters tuned for historical data
- Future market may not repeat history
- This is called "overfitting" — memorized the exam, new questions and you fail

**Recommended Process**:
1. Optimize parameters using 2022 data
2. Verify using 2023 data (out-of-sample testing)
3. Verify again using 2024 data
4. Only consider live trading if out-of-sample performance is acceptable

**Don't go all-in right away**, optimized strategies require extra caution! 🧪

---

## 11. Easter Egg: Hyperopt Optimization's "Little Secrets"

Think carefully about the HO2 version, a few interesting things:

1. **"Perfect" ROI Values**:
   > "405 minutes later 24.8%, 875 minutes later 9.1%, why are these numbers so precise?"
   
   Because these are the "optimal solutions" calculated by Hyperopt — the best-performing numbers on a certain historical dataset. But the question is: **Is this just happening to match that particular history?**

2. **35% Initial ROI's Ambition**:
   > "Demanding 35% right off the bat, isn't this strategy too greedy?"
   
   This probably means during optimization, the algorithm encountered a few big-profit trades, so parameters tuned toward "pursuing big profits". Future may not have such opportunities.

3. **-99% Stop-Loss's "Zen Mode"**:
   > "Stop-loss set to -99%, is it betting that mean reversion will definitely happen?"
   
   Basically betting "price will ultimately revert to the mean". But in extreme markets, some coins may go to zero, and then it's really zero.

---

## 12. The Very End

### One-Word Verdict
> "An optimized normalization strategy, multi-tier take-profit is a highlight, but Hyperopt optimization is a double-edged sword — perfect history doesn't guarantee perfect future."

### Who Should Use It?
- Veterans who understand mean reversion
- Patient types who can endure low-frequency trading
- Quant traders who know out-of-sample testing
- Timing players trading in ranging markets

### Who Should NOT?
- People seeking high-frequency trading
- People who can't accept long periods without signals
- Beginners who blindly trust optimized parameters
- People wanting mean reversion in strong trending markets

### Manual Trader Advice

If you're trading manually and want to learn from this strategy's approach:

1. **Learn to read normalization**: Use Williams %R or Stochastic RSI in TradingView, essentially similar
2. **Don't copy ROI**: 35% is too high, 10%-20% is more realistic for manual trading
3. **Must set stop-loss**: Don't copy the -99%, losing 20% you should admit defeat in manual trading
4. **Use in ranging markets**: Only when price bounces within a range does normalization strategy work
5. **Don't fight trends**: Mean reversion dies miserably in strong trending markets

---

## 13. Final Warning (Must Read!)

### Backtests Look Great, Live Trading Requires Caution

Hyperopt-optimized strategies often show **extremely impressive** historical backtest performance — but there's a trap:

> **Because parameters were specifically tuned for historical data, historical performance is 'perfect', but that doesn't guarantee future profitability.**

Simply put:
> **Past exam questions, perfect score; new exam questions, might fail.** 📝

### Hidden Risks of This Optimized Strategy

As an optimized strategy, HO2 has these hidden risks:

- **Overfitting Risk**: Parameters optimized for specific history, fail when market environment changes
- **Extreme Stop-Loss Risk**: -99% stop-loss, extreme markets can wipe you out
- **Few Signals Risk**: 35% high target means very few trading opportunities, may go months without a single trade
- **Data Peeking Risk**: Optimization may have unknowingly "seen" information it shouldn't have

### My Advice (Sincere Words)

```
1. [Must] Do out-of-sample testing: Verify on data different from optimization period
2. [Recommend] Lower initial ROI: From 35% to 15%-25%, improves trading frequency
3. [Recommend] Set actual stop-loss: -99% is too zen, suggest -15% to -30%
4. [Must] Test with small capital: Verify with small money first, then gradually increase
5. [Must] Observe live performance: Optimized strategy live performance often below expectations
```

**Remember**:
> "Hyperopt optimization is like exam answer memorization — perfect score on past exams, doesn't guarantee new exam success. Market is always changing, optimized parameters only represent 'worked in the past', not 'will work in the future'."

**Final Reminder**: No matter how good a strategy is, the market doesn't give warnings. Test with light positions, staying alive is what matters! 🙏

---

**Special Note**: This strategy is a Hyperopt-optimized version of the original NormalizerStrategy, with parameters optimized based on historical data. Before use, conduct sufficient out-of-sample testing to verify optimized parameter performance in new market environments. Overfitting risk is one of the most common issues in quantitative trading — please stay cautious.
