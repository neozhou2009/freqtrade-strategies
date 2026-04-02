# SwingHighToSky Strategy: The "Upgraded Bottom-Fisher" with Adjustable Parameters

> **Nickname**: Evolved Bottom-Fisher, Hyperopt Player  
> **Job**: Specializes in bottom-fishing, can also tune its own parameters  
> **Timeframe**: 15 Minutes

---

## I. What is This Strategy?

Simply put, **SwingHighToSky** is the "upgraded version" of SwingHigh:
- Replaced MACD with RSI
- Added Hyperopt parameter optimization
- Larger stop loss, more willing to gamble

It's like you used to only know how to buy dips, now you can also tune parameters to find the optimal solution 🤣

---

## II. Core Configuration: "Tune Your Own Parameters, Boldly Gamble"

### Profit Taking Rules (ROI Table)

```
Hold 0-33 minutes: Take 27% and run
Hold 33-64 minutes: Take 8.5% and run
Hold 64-244 minutes: Take 4.1% and run
After 244 minutes: Run even without profit
```

**Translation**: More aggressive than SwingHigh! Starts out wanting 27%, even greedier than the original 16%. But holding time is longer too, up to 4 hours max.

### Stop Loss Rules

```
Hard Stop Loss: -34.34% (Cut at this loss)
Trailing Stop: None! This strategy居然 doesn't have trailing stop!
```

**Translation**: Even larger stop loss space at -34%! But surprisingly no trailing stop - this is worse than SwingHigh. When you make money, you need to watch it yourself.

---

## III. Parameter Optimization: This Strategy's "Secret Weapon"

### 3.1 What is Hyperopt?

Simply put, Hyperopt lets the computer find optimal parameters for you.

**Plain English**:
> "You tell me which parameters can be tuned and their ranges, I'll run hundreds of backtests to find the most profitable combination."

### 3.2 Optimizable Parameters

| Parameter | Range | Optimized Value |
|-----------|-------|----------------|
| CCI Buy Threshold | -200 ~ 200 | -175 |
| CCI Buy Period | 10 ~ 80 | 72 |
| RSI Buy Threshold | 10 ~ 90 | 90 |
| RSI Buy Period | 10 ~ 80 | 36 |
| CCI Sell Threshold | -200 ~ 200 | -106 |
| CCI Sell Period | 10 ~ 80 | 66 |
| RSI Sell Threshold | 10 ~ 90 | 88 |
| RSI Sell Period | 10 ~ 80 | 45 |

**Comment**: All 8 parameters can be optimized! This is delegating decision paralysis to the computer 😅

---

## IV. 1 Buy Condition: Buy When CCI Drops Hard

### 🎯 The Only Buy Condition: CCI Oversold + RSI Confirmation

**Core Logic**:
- CCI(72) < -175 (oversold)
- RSI(36) < 90 (momentum confirmation)

**Plain English**:
> "CCI uses 72-period to watch oversold, buy when it drops below -175. RSI uses 36-period to confirm."

**The Code Looks Like This**:
```python
(dataframe[f'cci-{self.buy_cciTime.value}'] < self.buy_cci.value) &
(dataframe[f'rsi-{self.buy_rsiTime.value}'] < self.buy_rsi.value)
```

**Comment**: RSI < 90 this condition... normal RSI is between 0-100, < 90 is almost always true. So it's basically just looking at CCI! Is this RSI just here for decoration? 🤔

---

## V. 1 Sell Condition: Sell When CCI Recovers

### 📉 The Only Sell Condition: CCI Recovery + RSI Overbought

**Core Logic**:
- CCI(66) > -106 (note: negative value!)
- RSI(45) > 88 (near overbought)

**Plain English**:
> "Sell when CCI recovers from -175 to -106. RSI over 88 also confirms sell."

**The Code Looks Like This**:
```python
(dataframe[f'cci-sell-{self.sell_cciTime.value}'] > self.sell_cci.value) &
(dataframe[f'rsi-sell-{self.sell_rsiTime.value}'] > self.sell_rsi.value)
```

**Note**: Sell threshold is -106, still negative! Normal CCI overbought is > 100, here using a negative value... probably a "special solution" found by Hyperopt optimization.

**Let's Compare**:
- Buy: CCI < -175
- Sell: CCI > -106
- Only 69 points apart! Buy and sell points are very close.

---

## VI. The "Personality" of This Strategy

### ✅ Advantages (Praise Section)

1. **Optimizable Parameters**: Adapts to different markets, can "evolve"
2. **Dual Indicator Confirmation**: CCI + RSI, more reliable signals (though RSI is a bit decorative)
3. **Flexible Adjustment**: Can re-Hyperopt when market changes
4. **Large Stop Loss Space**: -34% can handle big swings

### ⚠️ Disadvantages (Criticism Section)

1. **No Trailing Stop**: No one helps lock profits when making money, need to watch yourself
2. **Overfitting Risk**: Hyperopt may only work on historical data
3. **Strange RSI Condition**: < 90 is almost always true, pretty useless
4. **Strange CCI Sell Threshold**: -106 is negative, traditional overbought should be positive

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Clear Trend | 🟢 Use it! | Can catch pullbacks, remember to set your own profit taking |
| 🔄 Volatile Market | 🟢 Re-optimize | Use Hyperopt to tune parameters for the market |
| 📉 Clear Downtrend | 🔴 Don't use | Long only |
| ⚡️ Sideways Range | 🟡 Be careful | May have few signals |

---

## VIII. Comparing SwingHigh: Upgrade or Downgrade?

| Feature | SwingHigh | SwingHighToSky |
|---------|-----------|----------------|
| Timeframe | 30m | 15m |
| Main Indicators | MACD + CCI | CCI + RSI |
| Stop Loss | -22% | -34% |
| Trailing Stop | ✅ Yes | ❌ No |
| Parameter Optimization | ❌ No | ✅ Yes |
| Complexity | Simple | Medium |

**Plain English Review**:
> "SwingHighToSky removed trailing stop and added parameter optimization. If you like tuning parameters yourself, use ToSky. If you like set-and-forget, use the original."

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Tunable Bottom-Fishing

SwingHighToSky's money-making philosophy:

> "I know how to buy dips, and I can tune my own parameters. When the market changes, I just re-optimize once."

- **CCI Oversold**: Find deep pullback points
- **RSI Confirmation**: Though a bit decorative, better than nothing
- **Hyperopt Optimization**: Re-find optimal parameters when market changes

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:-----------|:------------------|:--------------------------|
| 📈 Clear Trend | ⭐⭐⭐⭐☆ | "Can buy dips, but no trailing stop might miss some profits" |
| 🔄 Volatile Market | ⭐⭐⭐⭐⭐ | "Here's the advantage! Re-Hyperopt to find optimal parameters" |
| 📉 Downtrend | ⭐⭐☆☆☆ | "Long only, just watching in downtrend" |
| ⚡️ Sideways Range | ⭐⭐⭐☆☆ | "May have few signals, but can tune parameters to adapt" |

**One-Liner Summary**: Good for people who like to tinker with parameters, market changes mean re-optimize, quite flexible.

---

## X. Want to Run This Strategy? Check These Configs First

### 10.1 Hyperopt Usage Guide

```bash
# Optimize buy parameters
freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces buy --strategy SwingHighToSky

# Optimize sell parameters
freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces sell --strategy SwingHighToSky

# Optimize both
freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --spaces buy sell --strategy SwingHighToSky
```

**Note**: Remember to write new parameters into the strategy file after optimization!

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Fluid |
| 50+ pairs | 8GB | 16GB | May slow down during Hyperopt |

**Hyperopt Note**: Optimization requires heavy computation, recommend using a high-performance machine.

### 10.3 Backtesting vs Live Trading

**Backtesting Notes**:
- Hyperopt may overfit historical data
- Recommend validating with different time periods
- Don't just optimize with recent data

**Recommended Flow**:
1. Use 180 days of data for Hyperopt
2. Validate parameters with another 90 days of data
3. Run demo for 1 month
4. Only go live after confirming stability

**Don't use "optimal parameters" for live trading right away**, might just be overfitting!

---

## XI. Bonus: The Author's "Little Tricks"

Looking carefully at the code, you'll find some interesting things:

1. **RSI Threshold is Strange**: Buy RSI < 90, Sell RSI > 88
   > "Author, your RSI usage is a bit... unconventional? Normal RSI < 30 is oversold, > 70 is overbought."

2. **CCI Sell Threshold is Negative**: -106 is still negative
   > "Traditional CCI overbought is > 100, here using -106... this is a 'special solution' found by Hyperopt."

3. **No Trailing Stop**: SwingHigh had it, ToSky removed it
   > "Maybe thought parameter optimization is enough, don't need trailing stop? A bit confusing."

4. **Author Comment**: Copyright says "Free For Use"
   > "Free to use, author is generous. But whether it works well... test it yourself."

---

## XII. The Very End

### One-Liner Review
> "A bottom-fishing strategy with tunable parameters, good for tinkerers. But no trailing stop is a regret."

### Who Should Use It?
- ✅ People who like to tinker with parameters
- ✅ People willing to regularly re-optimize
- ✅ High volatility market traders
- ✅ People with Hyperopt experience

### Who Shouldn't Use It?
- ❌ People who want "plug and play"
- ❌ People who don't have time to tune parameters
- ❌ Ranging market traders
- ❌ People afraid of overfitting

### Manual Trader Recommendations
If you want to manually use this strategy:
1. Open a 15-minute candlestick chart
2. Add CCI(72) and RSI(36)
3. Wait for CCI to drop below -175
4. Confirm RSI < 90 (basically always satisfied)
5. Enter, set stop loss at -34%
6. Watch yourself, when CCI recovers above -106 consider exiting
7. Remember to set your own profit taking, this strategy has no trailing stop!

---

## XIII. ⚠️ Risk Emphasis Again (Must Read)

### The Trap of Hyperopt Optimization

SwingHighToSky's biggest risk is **overfitting**:

> **Historical optimal ≠ Future optimal. You found the most profitable parameters in the past, but the market is changing.**

Simply put: **"Good test scores don't mean you'll be good at work."**

### Signs of Overfitting

If you find:
- Backtesting returns are insane
- Live trading performs much worse
- Parameter values are particularly "strange" (like RSI < 90)

You might be overfitted.

### Risk of No Trailing Stop

This strategy **has no trailing stop**! This means:
- No one helps lock profits when making money
- Drawdowns can be large
- Need to set manual profit taking yourself

### My Suggestion (From the Heart)

```
1. Use multiple time periods for Hyperopt validation, don't just look at one period
2. Be wary of "strange" parameters
3. Add your own trailing stop configuration
4. Test lightly, don't go all-in from the start
5. Regularly re-optimize parameters
```

**Remember**: Parameter optimization is a double-edged sword. Used well, it adapts to the market; used poorly, it's overfitting. Staying alive is most important! 🙏

---

**Final Reminder**: No matter how good the strategy is, the market will humble you without warning. Test lightly, stay alive! 🙏