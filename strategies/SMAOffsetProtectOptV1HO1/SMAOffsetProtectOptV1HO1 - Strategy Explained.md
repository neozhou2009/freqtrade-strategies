# SMAOffsetProtectOptV1HO1 Strategy: The Aggressive Bottom Hunter

> **Nickname**: "Speed Hunter", "Impatient Bottom Picker"  
> **Occupation**: Aggressive bottom-picking quantitative hunter who likes quick in-and-out  
> **Timeframe**: 5 minutes (Flash mode)

---

## I. What is This Strategy?

Simply put, **SMAOffsetProtectOptV1HO1** is:
- **V1's aggressive variant**: All parameters have been re-tuned through "hyperparameter optimization"
- **Tiered ROI**: Wants 11.4% right after opening, drops to 6.3% after 36 minutes, 3.7% after 95 minutes, forces exit at 157 minutes
- **Easier to buy, more sensitive to sell**: Easier to enter, but also easier to exit
- **No longer "greedy"**: V1 ignores ROI when buy signal exists, HO1 obediently follows rules

It's like **an impatient bottom picker** — low entry threshold, but once in, wants to make big money. If time passes without making it, runs away quickly 🏃

---

## II. Core Configuration: Simply the "Tiered Escape Method"

### Take-Profit Rules (ROI Table) — This is the Key!

```
Time         Profit Target
────────────────────────
0 min        11.4%     ← Want big money right after opening!
36 min       6.3%      ← Can't wait, lower the bar
95 min       3.7%      ← Still dilly-dallying, lower again
157 min      0%        ← Forget it, just get out even!
```

**Translation**:
- **Just opened**: "I want to make 11.4%!" (Big ambitions 💪)
- **After 36 minutes**: "Fine, 6.3% will do..." (Starting to compromise)
- **After 95 minutes**: "3.7% and I'm out..." (Getting anxious)
- **After 157 minutes**: "Just don't lose money, get out!" (Totally zen)

It's like **a countdown level in a game**: The longer you wait, the lower the reward!

### Stop Loss Rules

```
Fixed Stop Loss: -10%
Trailing Stop: Enabled after 1% profit, trails at 0.1%
```

**Translation**:
- Lose 10% and accept defeat
- Once making money, use 0.1% "stickiness" to follow the price

---

## III. 2 Buy Conditions: Lower Thresholds

The buy conditions are exactly the same as V1, but **parameters are lowered**, making them easier to trigger!

### 🎯 Condition #1: Trend Pullback Buy

**Code Translation**:
```python
close < EMA(17) * 0.98   # Price is 2% below MA
AND EWO > 2.139          # Trend is up (V1 is 5.638, threshold dropped 62%!)
AND RSI < 65             # Not overheated (V1 is 61, relaxed)
```

**In Plain English**:
> "Price is 2% below the 17-period MA, EWO only needs to be 2.139, RSI can go up to 65. Much looser conditions!"

**Comparison with V1**:
| Parameter | V1 | HO1 | Change |
|-----------|----|----|--------|
| base_nb_candles_buy | 16 | 17 | About the same |
| low_offset | 0.978 | 0.98 | About the same |
| ewo_high | 5.638 | 2.139 | ↓ Dropped 62%! |
| rsi_buy | 61 | 65 | ↑ Relaxed 6.5% |

**Comment**: HO1 lowered ewo_high from 5.638 to 2.139, this is **significantly relaxing the buy threshold**! Originally needed clear trend to buy, now just needs slightly up trend to enter 🎢

---

### 🎯 Condition #2: Deep Oversold Buy

**Code Translation**:
```python
close < EMA(17) * 0.98   # Price is 2% below MA
AND EWO < -19.767       # Extremely oversold (about the same as V1)
```

**In Plain English**:
> "Same as V1, go pick up the pieces during a crash, no need to check RSI."

---

## IV. Protection Mechanism: Same as V1

| Protection Type | Purpose | In Plain English |
|----------------|---------|------------------|
| EWO Threshold | Judge trend strength | "Is this drop real or fake?" |
| RSI Filter | Prevent chasing highs | "Don't stand guard on the mountain top!" |

**EWO Fast/Slow Lines**: Still 50/200, using "long-term perspective" to judge trend like V1.

---

## V. Sell Logic: The Biggest Change is Here!

### 5.1 Sell Condition: Became Super Sensitive!

```python
close > EMA(17) * 0.99
```

**Translation**:
> "Price just needs to be 1% below the 17-period MA, and it sells!"

**Comparison with V1**:

| Parameter | V1 | HO1 |
|-----------|----|----|
| base_nb_candles_sell | 49 | 17 |
| high_offset | 1.006 | 0.99 |
| Sell Trigger | Price 0.6% above MA | Price 1% below MA |

**Comment**:
- V1: Wait for price to rise 0.6% above MA before selling (waiting for rise)
- HO1: Sell when price is still 1% below MA (eager to run)

It's like **an impatient person** — V1 is "wait until it rises then sell", HO1 is "run before it even rises" 🏃💨

### 5.2 Tiered ROI: The Longer, The More "Zen"

| Time | Target | Mindset |
|------|---------|----------|
| 0 min | 11.4% | "I'm gonna get rich!" 💰 |
| 36 min | 6.3% | "Okay, that's fine..." |
| 95 min | 3.7% | "Just making money is good..." |
| 157 min | 0% | "Breaking even is most important..." 🙏 |

**In Plain English**:
- Opening with hopes of 11.4%, which is high even in crypto
- Wait 36 minutes without reaching it, lower the standard
- Wait 2.5 hours without reaching it, just get out at break-even

### 5.3 Key Difference: No Longer "Greedy"

**V1's Setting**:
```python
ignore_roi_if_buy_signal = True
```
> "Ignore ROI when there's a buy signal, let profits keep flying!"

**HO1's Setting**:
```python
ignore_roi_if_buy_signal = False
```
> "I don't care if there's a buy signal, when ROI is reached, I run!"

**Comment**: V1 is "greedy mode", HO1 is "honest mode" — honestly follows ROI rules, no special treatment.

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **Good Tiered ROI Design**: The longer it waits, the more anxious it gets, avoids long-term holding
2. **Easier to Buy**: Easier to catch entry opportunities
3. **Forced Exit Mechanism**: Must leave after 157 minutes, won't hold indefinitely
4. **Hyperopt Optimized**: Parameters may perform better in certain markets

### ⚠️ Cons (Roast Time)

1. **ROI Target Too Aggressive**: 11.4% big target, hard for many coins to reach
2. **Selling Too Sensitive**: Price still 1% below MA and it sells, might miss subsequent gains
3. **Overfit Risk**: Hyperopt may cause parameters to only fit historical data
4. **Trade Frequency May Be Too High**: Easy buying + sensitive selling = frequent trading + fee killer

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| 📈 Strong Uptrend | 🟡 Careful | Selling too sensitive, may exit too early |
| ⚡ High Volatility | 🟢 Recommended | Aggressive ROI design fits big swings |
| 🔄 Mild Fluctuation | 🔴 Not Recommended | Easy buying + sensitive selling = frequent stop losses |
| 📉 One-sided Decline | 🔴 Don't Touch | ROI target almost impossible to reach |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Review
> "Impatient bottom picker, easy to enter and even faster to exit, suitable for high-volatility fast-paced markets."

### Who Should Use It?
- ✅ People who like quick in-and-out
- ✅ People who pursue high volatility markets
- ✅ People who don't want long-term holding
- ✅ People who can accept frequent trading

### Who Should NOT Use It?
- ❌ People who want profits to run (selling too sensitive)
- ❌ Ranging market traders (frequent trading = fee killer)
- ❌ Low volatility markets (11.4% target too hard)
- ❌ People who don't want to watch the market (157-minute forced exit requires attention)

### My Recommendations
1. **Adjust high_offset**: 0.99 is too sensitive, recommend changing to 1.00-1.01
2. **Lower ROI target**: 11.4% is too high for most coins
3. **Increase base_nb_candles_sell**: 17 is too short, recommend 25-35
4. **Run simulation first**: See how "impatient" this strategy really is

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Trading "Aggression" for "Speed"

SMAOffsetProtectOptV1HO1 is **V1's aggressive variant**. Its core changes:

> "Tune all parameters towards 'aggressive' — easier to buy, faster to sell, higher ROI target, more time pressure"

**Its Money-Making Philosophy**:
- **Aggressive Buying**: Lower threshold, more opportunities to enter
- **Sensitive Selling**: Quick profit locking, not greedy
- **Time Pressure**: Must leave after 157 minutes, no lingering
- **Tiered ROI**: The longer it waits, the more zen, finally break-even exit

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:------------------|:---------------------------|
| 📈 Strong Uptrend | ⭐⭐⭐⭐☆ | Can catch the trend, but might sell too early |
| ⚡ High Volatility | ⭐⭐⭐⭐⭐ | This strategy is designed for high volatility! |
| 🔄 Mild Fluctuation | ⭐⭐☆☆☆ | Easy buying + fast selling = fee bleeding |
| 📉 One-sided Decline | ⭐☆☆☆☆ | 11.4% target? Dream on! |

**One-Sentence Summary**: **This strategy is a "high volatility warrior", not a "ranging hunter"**

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Trading Pair Selection | High volatility coins | Don't choose stablecoins, ROI can't reach |
| Number of Trading Pairs | 3-10 | Don't be too many, this strategy trades frequently |
| Capital Allocation | 5-10% per pair | Leave some room |

### 10.2 Key Configuration File Settings

```yaml
# config.json key settings
"max_open_trades": 3-5,  # This strategy is frequent, don't open too many
"stake_currency": "USDT",
"stake_amount": "unlimited",  # Or fixed amount
"dry_run": true,  # Run simulation first! Absolutely!
```

### 10.3 Hardware Requirements

Same as V1, moderate computation:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|---------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Okay |
| 50+ pairs | 8GB | 16GB | Needs monitoring |

### 10.4 Backtest vs Live Trading

**The Trap of Hyperopt**:
- Backtest performance may be **extremely shiny** (because parameters are tuned)
- Live trading performance may be **discounted significantly**
- 11.4% ROI target is almost impossible in bear markets

**Recommended Process**:
1. Run dry_run for at least 1 week
2. Check actual trade frequency and signal quality
3. Adjust high_offset and ROI targets
4. Small position live trial
5. Continuous monitoring, adjust when problems found

---

## XI. Bonus: V1 vs HO1 Parameter Comparison

| Parameter | V1 | HO1 | Comment |
|-----------|----|----|---------|
| ROI | Fixed 1% | Tiered 11.4%→6.3%→3.7%→0% | HO1 more aggressive |
| ignore_roi_if_buy_signal | True | False | V1 greedy, HO1 honest |
| base_nb_candles_buy | 16 | 17 | About the same |
| base_nb_candles_sell | 49 | 17 | HO1 shorter = more sensitive |
| low_offset | 0.978 | 0.98 | About the same |
| high_offset | 1.006 | 0.99 | HO1 sells faster! |
| ewo_high | 5.638 | 2.139 | HO1 easier to buy |
| ewo_low | -19.993 | -19.767 | About the same |
| rsi_buy | 61 | 65 | HO1 more relaxed |

**Summary**:
- **Buying**: HO1 more relaxed (ewo_high lowered, rsi_buy increased)
- **Selling**: HO1 more sensitive (high_offset lowered, base_nb_candles_sell shortened)
- **ROI**: HO1 more aggressive (tiered targets vs fixed target)
- **Mindset**: V1 is "let profits fly", HO1 is "exit on time"

---

## XII. Final Final Words

### One-Sentence Review
> "Impatient version of V1, suitable for quick in-and-out in high volatility markets, but may exit too early."

### Who Should Use It?
- ✅ Short-term traders who like quick in-and-out
- ✅ High volatility market lovers
- ✅ People who can accept frequent trading
- ✅ People who have time to tune parameters

### Who Should NOT Use It?
- ❌ People who want profits to run
- ❌ Long-term residents of ranging markets
- ❌ People who don't want to watch frequently
- ❌ People who don't want to adjust default parameters

### Manual Trader Recommendations
If you want to manually use HO1's logic:
1. Draw a 17-period EMA (more sensitive than V1's 49-period)
2. Watch when price is 2% below EMA
3. Consider buying when EWO is just above 2.139 (low threshold)
4. Set tiered take-profit: 11.4%/6.3%/3.7%
5. Consider running when price returns to 1% below EMA
6. After 157 minutes, if still not profitable, force exit

---

## XIII. ⚠️ Risk Re-emphasis (Must Read Section)

### Backtesting Looks Great, Live Trading Needs Caution

HO1 is a **hyperopt version**, which means:
- Parameters are tuned from historical data
- Backtest performance may be **extremely shiny**
- But **historical optimal ≠ future optimal**

Simply put: **This is a "memorize the answers" strategy, if the test questions change, it might be stumped** 📚

### Hidden Risks of Complex Strategies

In live trading, HO1's settings may cause:
- **Frequent Trading**: Easy buying + sensitive selling = high frequency trading = fee killer
- **Premature Exit**: high_offset=0.99 might sell before the bounce
- **ROI Hard to Reach**: 11.4% target is almost impossible in some markets
- **Time Pressure**: 157-minute forced exit might miss big moves

### My Recommendations (Honest Truth)

```
1. Change high_offset to 1.00 or 1.01 first, don't be too sensitive
2. Lower ROI target, change 11.4% to 5-8%
3. Increase base_nb_candles_sell to 25-35
4. Run dry_run for a week, check trade frequency
5. If trade frequency is too high, keep adjusting parameters
6. Small position live trial, don't exceed 5% of total capital
```

**Remember**: Hyperopt = Historical fitting. No matter how good the strategy, it might flop in a different market. Light position testing, survival is most important! 🙏

---

**Final Reminder**: HO1 is an aggressive version designed for high volatility markets. If you use this strategy in low volatility markets, either adjust parameters or prepare to pay tuition.