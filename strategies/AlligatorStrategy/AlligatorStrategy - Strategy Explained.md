# AlligatorStrategy: When the Alligator Opens Its Mouth, It Only Swallows Bull Stocks

> **Nickname**: The Perfectionist 🎯  
> **Profession**: Bullish Alignment Sniper  
> **Timeframe**: 1 Hour

---

## I. What Is This Strategy?

Simply put, **AlligatorStrategy** is:
- Wait for perfect bullish alignment (6 EMAs lined up from short to long)
- Wait for oversold pullback (Stoch RSI drops to low level)
- Buy, then let trailing stop protect profits

It's like **a picky matchmaker** 💍—only acts when conditions are perfect, quality over quantity!

Author's backtest data: Made **1324%** in one year! But... maximum drawdown is also **169%** (negative means leverage or reinvestment), this is a high-risk, high-reward strategy.

---

## II. Core Configuration: Simply Put, "Trend Is King"

### Take-Profit Rules (ROI Table)

```
Immediately after entry: 10% profit required
After 30 min drops to: 5% profit required
After 60 min drops to: 2% profit required
```

**Translation**: High expectations on entry, want 10%; as time passes, expectations drop, 2% is fine too. Like dating—high standards at first, lower as time goes on 🤣

### Stop-Loss Rules

```
Fixed stop-loss: -99% (basically useless)
Trailing stop: Enabled
```

**Translation**: 99% stop-loss means "I don't stop-loss." Real protection comes from trailing stop—when you make money, stop-loss line follows up, locking in profits.

---

## III. 1 Buy Condition: But Let Me Break It Down for You

This strategy has only 1 buy condition, but it contains 7 sub-conditions:

### 🎯 The Only Condition: Perfect Bullish Alignment + Oversold Reversal

**Plain English**:
> "6 moving averages lined up nicely from top to bottom (short>medium>long), and Stoch RSI has dropped enough—time to charge!"

**Breaking it down**:

| Condition | Plain English |
|-----------|--------------|
| EMA7 > EMA30 | Ultra-short-term stronger than short-term |
| EMA30 > EMA50 | Short-term stronger than short-medium term |
| EMA50 > EMA100 | Short-medium term stronger than medium-term |
| EMA100 > EMA121 | Medium-term stronger than medium-long term |
| EMA121 > EMA200 | Medium-long term stronger than long-term |
| Stoch RSI < 0.82 | Oversold, bargain hunting time |
| Volume > 0 | Trading activity exists |

**Classic Lines**:
```
if all EMAs perfectly aligned and Stoch RSI oversold:
    print("Opportunity! Let's go!")
else:
    print("Doesn't meet criteria, keep waiting...")
```

---

## IV. Protection Mechanism: 2 Layers of "Life Insurance"

### Protection #1: Trailing Stop

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| Trailing Stop | Moves stop-loss up after profit | "Made money? Don't give it back" |

This is powerful! For example, if you made 50%, stop-loss line will follow up to say 40% profit. If price pulls back, automatically take profit at 40%, won't give back profits.

### Protection #2: Tiered ROI

```
Made 10%? Can leave!
Waited 30 min? 5% and leave!
Waited 60 min? 2% and leave!
```

**Plain English**: Time is money, the longer you hold, the lower your expectations—quick in and out.

---

## V. Sell Logic: One Way to Exit

### 5.1 The Only Sell Signal: Trend Reversal + Overbought

```
EMA121 > EMA7  AND  Stoch RSI > 0.2
```

**Plain English**:
- EMA121 runs above EMA7: Trend starting to reverse
- Stoch RSI also rose enough: Time to go

**Translation**:
> "Price broke below EMA121, and Stoch RSI is up too—trend might reverse, run quickly!"

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Time)

1. **Strict Filtering**: All 6 EMAs must align, quality over quantity
2. **Precise Entry**: Buy during trend pullbacks, great value
3. **Auto Protection**: Trailing stop automatically locks profits
4. **Impressive Backtest**: Author's data shows 1324% return (though drawdown is also big)

### ⚠️ Cons (Roast Time)

1. **Too Picky**: Perfect bullish alignment rarely appears, might wait a year for just a few opportunities
2. **Scary Drawdown**: 169% max drawdown, account could be cut in half twice
3. **Only Works in Bull Markets**: Completely doesn't work in bear markets—no bullish alignment
4. **Many Rejected Signals**: 3045 signals rejected, only 258 executed, pass rate only 7.8%

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Strong Bull Market | ✅ Highly Recommended | Perfectly captures uptrend |
| Ranging Market | ⚠️ Use Cautiously | Too few entry opportunities |
| Bear Market | ❌ Don't Use | No bullish alignment, strategy takes a break |
| High Volatility | ⚠️ Adjust Parameters | Might get washed out |

---

## VIII. Summary: How Good Is This Strategy?

### One-Sentence Review
> "Bull market god strategy, bear market daydream."

### Who Should Use It?
- ✅ Patient trend traders
- ✅ People who can handle big drawdowns
- ✅ People who only trade in bull markets
- ✅ People who understand Hyperopt parameter optimization

### Who Shouldn't Use It?
- ❌ People who want to trade frequently
- ❌ Risk-averse individuals
- ❌ People who want to make money in bear markets too
- ❌ Newbies

### My Advice
1. **Only use in bull markets**: Strategy basically doesn't work in bear markets
2. **Set real stop-loss**: -99% is too loose, change to -15% or -20%
3. **Optimize parameters**: Use Hyperopt to optimize buy_stoch_rsi and sell_stoch_rsi
4. **Control position size**: Don't go all-in when big drawdown comes

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Building "Entry Barrier" with Perfectionism

AlligatorStrategy is an **extremely picky trend strategy**. About 200+ lines of code—what does that mean? A carefully designed trend-following template.

**Its Money-Making Philosophy**: Only trade the strongest trends, quality over quantity

- **Bullish Alignment**: All 6 EMAs must align, ensuring perfect trend
- **Oversold Entry**: Buy on pullbacks, not chasing highs
- **Auto Take-Profit**: Trailing stop + tiered ROI, let profits run

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:-----------|:------------------|:--------------------------|
| 📈 Strong Bull Market | ⭐⭐⭐⭐⭐ | Perfect! Bullish alignment, Stoch RSI oversold, profit on entry |
| 🔄 Ranging Market | ⭐⭐☆☆☆ | Bullish alignment rarely forms, strategy basically idle |
| 📉 Bear Market | ☆☆☆☆☆ | No bullish alignment, strategy completely doesn't work |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | Might get washed out, but can catch trends when they come |

**One-Sentence Summary**: Money printing machine in bull markets, decorative piece in bear markets.

### 9.3 Strategy's "Pickiness Index"

Let me calculate:
- Backtest period: 2020-09-11 to 2021-08-26 (about 350 days)
- Valid buy signals: 258
- Rejected signals: 3045
- Pass rate: 258 / (258 + 3045) = 7.8%

**Translation**: Out of every 13 signals, only 1 passes! This strategy is pickier than a mother-in-law 😂

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|------------------|---------|
| Timeframe | 1h (default) | Not recommended to change |
| Trading Pairs | Bull coins first | Bear coins have no bullish alignment |
| Number of Pairs | 10-30 | Too few means even fewer opportunities |

### 10.2 Parameter Optimization Suggestions

```python
# Buy threshold (oversold level)
buy_stoch_rsi: 0.75-0.85  # Default 0.82

# Sell threshold (overbought level)
sell_stoch_rsi: 0.15-0.25  # Default 0.2
```

**Recommendation**: Run Hyperopt once to find parameters best suited for your trading pairs.

### 10.3 Hardware Requirements (Medium)

This strategy has medium computation needs, requires 6 EMAs + Stoch RSI:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|---------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Sufficient |
| 50+ pairs | 8GB | 16GB | Stable |

### 10.4 Backtesting vs Live Trading

Author's backtest data looks impressive, but note:
- Backtest period was 2020-2021 major bull market
- 169% drawdown—if your capital isn't enough, might get liquidated
- Pass rate only 7.8%, most signals rejected

**Recommended Process**:
1. Backtest in different periods (including bear markets)
2. Adjust parameters for different markets
3. Paper trade test for at least 1 month
4. Start live trading with small capital
5. Add position after confirming viability

---

## XI. Easter Egg: Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **EMA121**: Why 121?
   > 121 = 11², author might have used Fibonacci or square number series

2. **stoploss = -0.99**: Why -99%?
   > "I don't set stop-loss, let trailing stop protect"—author is confident

3. **3045 rejected signals**:
   > "Quality over quantity, 1 out of 13 signals passes, I'm picky and proud"

4. **startup_candle_count = 200**:
   > Needs 200 candles for warm-up, 1-hour cycle means 8+ days of data

---

## XII. Final Words

### One-Sentence Review
> "Bull market hunter, bear market hermit—the perfectionist's trading path."

### Who Should Use It?
- ✅ Trend traders
- ✅ Patient long-term players
- ✅ People who can handle big drawdowns
- ✅ Smart people who only trade in bull markets

### Who Shouldn't Use It?
- ❌ Frequent trading enthusiasts
- ❌ Risk-averse individuals
- ❌ People who want to make money in bear markets too
- ❌ People without patience to wait for perfect signals

### Manual Trader Recommendations
Strategy can be executed manually:
1. Open 1-hour chart
2. Add EMA(7, 30, 50, 100, 121, 200) and Stoch RSI
3. Wait for 6 EMAs to line up from top to bottom (7>30>50>100>121>200)
4. Wait for Stoch RSI below 0.82
5. Enter position, set trailing stop
6. Run when EMA121 gets above EMA7

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Part)

### Backtesting Looks Great, Live Trading Be Careful

AlligatorStrategy's backtest data is indeed impressive—**1324% return**! But there are traps:

> **Backtest period was 2020-2021 major bull market, any trend strategy could make money.**

Simply put: **In bull markets even pigs can fly, doesn't mean the strategy is really good.**

### High Returns, High Risks

In live trading, note:
- **169% max drawdown**: What does that mean? If you put in 100, worst case lose to -69 (if using leverage)
- **Too many rejected signals**: 3045 signals rejected, strategy is very picky
- **Only works in bull markets**: No bullish alignment in bear markets, strategy takes a break

### My Advice (Real Talk)

```
1. Only use in clear bull markets
2. Set real stop-loss (-15% to -20%), don't use -99%
3. Optimize parameters with Hyperopt
4. Control position size, don't go all-in
5. Be mentally prepared: big drawdowns will come
```

**Remember**: Making money in bull markets is easy, surviving in bear markets is hard. No matter how good the strategy, when the market teaches you a lesson, it doesn't knock first. Light position testing, survival comes first! 🙏

---

**Final Reminder**: This strategy has "Alligator" in the name, but don't expect it to bite in bear markets—in bear markets, it hibernates 🐊💤