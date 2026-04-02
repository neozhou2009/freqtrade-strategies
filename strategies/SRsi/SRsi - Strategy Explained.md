# SRsi Strategy: So Simple It Makes You Doubt Life - The "Quick In, Quick Out" Player

> **Nickname**: The "Minimalist" of the Strategy World  
> **Occupation**: Overbought/Oversold Sniper  
> **Timeframe**: 1 minute (fast enough to make you dizzy)

---

## I. What is This Strategy?

Simply put, **SRsi** is a strategy that:
- Uses Stochastic RSI to determine overbought/oversold conditions
- K-line golden cross to buy, death cross to sell
- That's it!

It's like when you're at the farmers market buying vegetables, you buy when you see the price drop to historical lows, sell when it rises to historical highs. No fancy indicators, no complex logic, just "simple and rough." 🤣

**Less than 50 lines of code** - the "minimalist" of the strategy world.

---

## II. Core Configuration: Basically "Make 1.2% and Run, Lose 15% and Accept It"

### Take Profit Rules (ROI Table)

```
Immediately after buying → Sell at 1.2% profit
```

**Translation**: This strategy isn't greedy, make 1.2% and walk away.

### Stop Loss Rules

```
Fixed stop loss: -15% (accept losing 15%)
```

**Translation**: Stop loss is set quite loose, giving price enough room to fluctuate.

---

## III. 1 Buy Condition: Let Me Translate to Plain English

### 🎯 The Only Buy Condition: Oversold Golden Cross

```python
(dataframe['k'] < 15) &              # K-line in oversold zone
(dataframe['k'] >= dataframe['d'])   # K-line crossing above D-line
```

**Plain English Translation**:
> "K-line value is below 15 (meaning oversold, price is cheap), then K-line starts going up and crosses above D-line (golden cross), this is when you buy!"

**Analogy**:
It's like when you see a discounted item at the supermarket, the price has already dropped to historical lows (K<15), and then you notice the price starting to rise (golden cross), you buy in, waiting for it to bounce back.

---

## IV. 1 Sell Condition: Simple and Direct

### 📉 The Only Sell Condition: Overbought Death Cross

```python
(dataframe['k'] > 75) &              # K-line in overbought zone
(dataframe['d'] >= dataframe['k'])   # K-line crossing below D-line
```

**Plain English Translation**:
> "K-line value is above 75 (meaning overbought, price is expensive), then K-line starts going down and breaks below D-line (death cross), this is when you sell!"

**Analogy**:
It's like when the stock you bought rises to historical highs (K>75), and then you notice the price starting to drop (death cross), quickly sell to lock in profits.

---

## V. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **Dead Simple**: Less than 50 lines of code, anyone can understand
2. **Few Parameters**: Just 3 parameters (p=14, k=3, d=3), won't overfit
3. **Fast Execution**: Tiny computation load, even old computers can run
4. **Classic Logic**: Overbought/oversold + golden/death cross, technical analysis 101

### ⚠️ Cons (Complaint Time)

1. **Too Simple**: No risk control protection, like a "naked" strategy
2. **Too Many Signals**: On 1-minute timeframe, buy/sell signals might flood your screen
3. **Poor Trend Performance**: One-way markets will repeatedly slap you in the face
4. **Stop Loss Too Wide**: -15% stop loss is a bit large for a short-term strategy

**Complaint**: This strategy is like someone going to the North Pole in shorts and a tank top - simple is simple, but protection is too little! 😅

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| 🔄 Sideways Oscillation | ✅ Highly Recommended | Strategy is designed for oscillation |
| 📈 One-way Uptrend | ❌ Not Recommended | Will sell too early, miss the move |
| 📉 One-way Downtrend | ❌ Not Recommended | Will repeatedly catch falling knives |
| ⚡️ Extreme Volatility | ⚠️ Be Careful | Too much noise in 1-minute timeframe |

**One-Sentence Summary**: **Oscillation is its home field, trends are its nemesis.**

---

## VII. Summary: How Is This Strategy Really?

### One-Sentence Review
> "So simple it makes you doubt life, but precisely because it's simple, it doesn't easily have bugs."

### Who Is It For?
- ✅ Quantitative newbies (little code, easy to understand)
- ✅ People who want to learn strategy writing
- ✅ Oscillation market lovers
- ✅ People who don't want to tune parameters

### Who Is It NOT For?
- ❌ People chasing high returns (take profit is too low)
- ❌ Trend traders (this strategy eats oscillation)
- ❌ People needing complex risk control (no risk control)
- ❌ Exchanges with high fees (frequent trading is costly)

### My Advice
1. **Learn First**: This is a good template for beginners
2. **Add Risk Control**: Add your own stop loss protection, circuit breakers
3. **Tune Parameters**: Try different overbought/oversold thresholds
4. **Change Timeframe**: 1-minute is too noisy, try 5-minute or 15-minute

---

## VIII. What Market Can This Strategy Make Money In?

### 8.1 Core Logic: The "Spread Harvester" Eating Oscillations

SRsi is a classic oscillation strategy, its money-making philosophy is:

> **"Buy low, sell high, repeatedly harvest small fluctuations."**

- **Oversold Buying**: K < 15, price is "too cheap"
- **Overbought Selling**: K > 75, price is "too expensive"
- **Cross Confirmation**: Wait for golden/death cross to confirm direction

### 8.2 Performance in Different Markets (Plain English)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:---------------------------|
| 📈 Slow Bull Trend | ⭐⭐☆☆☆ | "Just bought then sold, watching it go up" |
| 🔄 Sideways Oscillation | ⭐⭐⭐⭐⭐ | "Oscillation is my money-making tool" |
| 📉 One-way Downtrend | ⭐⭐☆☆☆ | "Oversold then oversold again, catching knives halfway" |
| ⚡️ Extreme Volatility | ⭐⭐☆☆☆ | "1-minute timeframe is too noisy, too many signals" |

**One-Sentence Summary**: **Makes money every day in oscillation, gets slapped every day in trends.**

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Timeframe | 1m (or 5m) | 1-minute is too noisy, 5-minute is more stable |
| Stop loss | -0.10 | Can tighten a bit |
| Take profit | 0.01 | Enough for short-term |

### 9.2 Hardware Requirements (Basically None!)

This strategy has tiny computation load, any VPS can run it:

| Trading Pair Count | Minimum Memory | Recommended Memory | Experience |
|-------------------|----------------|-------------------|------------|
| 1-20 pairs | 1GB | 1GB | Opens instantly |
| 20-50 pairs | 1GB | 2GB | Still fast |
| 50+ pairs | 2GB | 4GB | No pressure |

**Comment**: You can run this strategy on a Raspberry Pi! 😄

### 9.3 Backtesting vs Live Trading

The benefit of simple strategies is **not easily overfitting**, but the downside is **lacking risk control**:

- Signals might be too many, need to consider fees
- Slippage might erode profits
- 1-minute timeframe is noisy, suggest switching to 5-minute

**Recommended Process**:
1. First try switching to 5-minute timeframe
2. Add trading fees in backtest
3. Paper trade for a few days
4. Small position live trading

---

## X. Bonus: The "Minimalist Aesthetics" of This Strategy

Looking at the code is like reading a poem, short and powerful:

```python
# Buy: K < 15 AND K >= D (golden cross)
# Sell: K > 75 AND D >= K (death cross)
# Stop loss: -15%
# Take profit: 1.2%
# That's it!
```

**Doesn't Have**:
- No multi-layer validation
- No anti-pump mechanism
- No dynamic stop loss
- No HyperOpt parameters
- No informational timeframe

**Only Has**:
- One buy condition
- One sell condition
- One stop loss
- One take profit

This is the aesthetic of minimalism! 🌸

---

## XI. The Very End

### One-Sentence Review
> "Must-learn for beginners, use with caution in live trading - unless you add risk control."

### Who Is It For?
- ✅ Quantitative newbies (learning strategy writing)
- ✅ People who want to understand Stochastic RSI
- ✅ Oscillation market traders
- ✅ People who like clean code

### Who Is It NOT For?
- ❌ People chasing high returns
- ❌ People needing complex risk control
- ❌ Trend trading lovers
- ❌ People who don't want to modify code themselves

### Improvement Suggestions

If you want to use this strategy live, suggest adding:

```
1. Trailing stop (trailing_stop)
2. Anti-pump mechanism (don't buy on abnormal price surges)
3. Circuit breaker (pause after consecutive losses)
4. Switch to 5-minute or 15-minute timeframe
5. Adjust overbought/oversold thresholds (e.g., K<20 buy, K>80 sell)
```

---

## XII. Manual Trader Advice

This strategy has simple logic, manual traders can consider:

1. **Open TradingView**, search for "Stoch RSI" indicator
2. **Set parameters**: RSI=30, K=3, D=3, Stochastic=14
3. **Wait for signals**:
   - K-line drops below 15, then golden cross → consider buying
   - K-line rises above 75, then death cross → consider selling
4. **Note**: Combine with support/resistance, volume and other indicators for confirmation

When trading manually, you can use this as an auxiliary tool, don't rely on it alone.

---

## XIII. ⚠️ Risk Reminder Again (Must Read)

### Backtests Are Beautiful, Live Trading Needs Caution

SRsi might perform beautifully in backtesting in sideways oscillating markets, but:

> **Simple strategies in complex markets can get slapped by various unexpected events.**

### Hidden Risks of Simple Strategies

In live trading, the cost of simplicity is:
- **No Risk Control Protection**: No circuit breakers, no anti-pump
- **Too Many Signals**: Might trade frequently on 1-minute timeframe
- **Fee Erosion**: High-frequency trading fees are the invisible killer
- **Slippage Impact**: Fast volatility might cause execution price deviation

### My Advice (Real Talk)

```
1. Don't directly use default parameters for live trading
2. At least switch to 5-minute timeframe
3. Add trailing stop and circuit breaker mechanisms
4. Include fees (0.1%) in backtesting
5. Paper trade for at least 2 weeks
```

**Remember**: Simple ≠ Profitable. No matter how simple the strategy, the market is狡猾. Light position testing, staying alive is most important! 🙏

---

**Final Reminder**: This strategy is a classic template for quantitative beginners, code is clean and easy to understand. But precisely because it's simple, you must add more protection mechanisms before live trading. Learn it, but don't go all-in directly!