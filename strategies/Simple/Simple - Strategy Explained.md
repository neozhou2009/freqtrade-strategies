# Simple Strategy: The "Minimalist" That Lives Up to Its Name

> **Nickname**: Less is More  
> **Job**: Quick-Draw Trend Follower  
> **Timeframe**: 5 minutes

---

## I. What Is This Strategy?

Simply put, **Simple** is:
- Only uses 3 indicators (MACD, Bollinger Bands, RSI)
- Only has 1 buy condition
- Only has 1 sell condition
- Take-profit at 1%, stop-loss at 25%

Just like its name - Simple, so simple it can't be simpler. The person who wrote the book was probably a minimalist too, thinking "trading doesn't need to be complicated."

---

## II. Core Configuration: Basically "Quick In, Quick Out"

### Take-Profit Rule (ROI Table)

```python
"0": 0.01  # Run at 1% profit
```

**Translation**: Get out with 1% profit, no greed. Buy at $100, sell at $101. Coffee hasn't even cooled down yet, trade is done.

### Stop-Loss Rule

```python
stoploss = -0.25  # Stop-loss at 25% loss
```

**Translation**: This stop-loss is ridiculously wide! Buy at $100, has to drop to $75 before giving up. Either make $1 and run, or lose $25 and admit defeat. This math is a bit extreme, right?

---

## III. 1 Buy Condition: Triple Confirmation Required

Although called Simple, the buy condition isn't simple at all - three indicators must all be satisfied!

### 🎯 Buy Condition Breakdown

```python
(
    (dataframe['macd'] > 0) &                              # Condition 1
    (dataframe['macd'] > dataframe['macdsignal']) &        # Condition 2
    (dataframe['bb_upperband'] > dataframe['bb_upperband'].shift(1)) &  # Condition 3
    (dataframe['rsi'] > 70)                                # Condition 4
)
```

**Plain English Translation**:

| Condition | Code | Human Language |
|-----------|------|----------------|
| Condition 1 | MACD > 0 | "Trend is going up, not down" |
| Condition 2 | MACD > Signal | "Momentum is strengthening, just broke through" |
| Condition 3 | Bollinger upper band up | "Price is breaking out, volatility increasing" |
| Condition 4 | RSI > 70 | "Already risen quite a bit" |

**Classic Line**:
> "MACD golden cross confirms trend, Bollinger band up confirms breakout, RSI above 70 confirms strength... Alright, all four conditions met, let's go!"

---

### 🤔 Wait, RSI > 70?

Smart readers might ask: **RSI above 70 is overbought, right? Shouldn't you sell when overbought?**

Good question! This strategy's thinking is:
- **Normal logic**: RSI > 70 = overbought = should sell
- **Simple logic**: RSI > 70 = strong = keep buying!

This is a "chase the rally" strategy, believing "the strong get stronger." In strong trends, overbought can become more overbought, RSI can go to 90 or even 95.

So this strategy's motto is:
> "Who cares about overbought or not, if the trend is there, get on board!"

---

## IV. Sell Logic: Run at RSI 80

### Sell Condition

```python
(dataframe['rsi'] > 80)
```

**Plain English**:
> "RSI hit 80? That's too crazy, I'm out!"

That simple. RSI breaks 80, sell. Doesn't matter how much profit or loss.

### Profit Space Analysis

From RSI 70 entry to RSI 80 exit:
- Usually has some price gain (depends on market)
- But if RSI turns down from 70, you're screwed
- 1% take-profit will trigger before RSI 80

---

## V. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Simplicity to the max**: 3 indicators, 1 buy point, 1 sell point, elementary schoolers can understand
2. **Fast execution**: Low computation, old computers can run it
3. **Has theoretical support**: From published trading book, not made up

### ⚠️ Cons (Roast Section)

1. **Stop-loss too wide**: 25% loss before stopping, who can handle that?
2. **Take-profit too early**: Run at 1%, miss big trends
3. **Buy at high**: RSI > 70 to buy, like buying tickets at the mountain top
4. **No trailing stop**: Floating profit can become floating loss

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|--------------------|--------|
| Strong trend bull market | ✅ Can use | Follow trend, quick in and out |
| Ranging market | ❌ Don't use | RSI whipsaws between 70-80 repeatedly |
| Bear market | ❌ Don't use | No buy signals, or buy and get trapped |
| High volatility | ⚠️ Use cautiously | Wide stop-loss might save you, or lose more |

---

## VII. Summary: How Is This Strategy Really?

### One-Sentence Review
> "Named Simple, logic is indeed simple, but take-profit and stop-loss settings are a bit extreme."

### Who Should Use It?
- ✅ Quantitative beginners: Simple code, easy to understand and modify
- ✅ Trend traders: Believe "strong get stronger"
- ✅ Short-term lovers: Quick in and out, no lingering

### Who Shouldn't Use It?
- ❌ Risk averse: 25% stop-loss is too wide
- ❌ Trend followers: 1% take-profit too short, can't catch big trends
- ❌ Ranging market traders: This strategy gets repeatedly slapped in ranging markets

### My Recommendations

1. **Adjust stop-loss**: Change from 25% to around 10%, protect capital
2. **Expand take-profit**: Change from 1% to 2-3%, give trend some room
3. **Add trailing stop**: Pair with trailing stop to lock in floating profits
4. **Only use in trending markets**: Don't bother in ranging markets

---

## VIII. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: "Quick-Draw" Momentum Chaser

Simple is a classic **short-term trend breakout strategy**. Its profit philosophy is:
- **Believe in strong getting stronger**: Enter only when RSI > 70, chasing strength
- **Quick in and out**: 1% take-profit or RSI > 80 and run
- **No left-side trading**: Don't catch falling knives, only chase rallies

### 8.2 Performance in Different Markets (Plain Speak Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Strong trend bull | ⭐⭐⭐⭐☆ | RSI 70-80 is normal rise, chasing works |
| 🔄 Ranging market | ⭐⭐☆☆☆ | RSI goes back and forth through 70-80, buy then drop, sell then rise |
| 📉 Bear market | ⭐☆☆☆☆ | MACD < 0 never buys, or buy and get trapped |
| ⚡️ High volatility | ⭐⭐⭐☆☆ | Wide stop-loss might save you, or might lose more |

**One-sentence summary**: Only suitable for trending markets, forget about ranging and bear markets.

---

## IX. Want to Run This Strategy? Check These Configs First

### 9.1 Trading Pair Configuration

| Config Item | Recommended Value | Comment |
|-------------|------------------|---------|
| Number of pairs | 5-20 | Too many can't monitor, too few miss opportunities |
| Timeframe | 5 minutes | Keep default, this is the designed period |
| Pair type | High liquidity majors | Altcoins too volatile, easily stopped |

### 9.2 Hardware Requirements (Important!)

This strategy is lightweight, low computation:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|--------------------| -----------|
| 1-10 pairs | 1GB | 2GB | Smooth |
| 10-50 pairs | 2GB | 4GB | Fluid |
| 50+ pairs | 4GB | 8GB | Sufficient |

**Good news**: Old computers can run it too, no VPS needed!

### 9.3 Backtest vs Live

**Note**:
- Backtest may overstate RSI 70-80 gains
- Live trading has slippage and fees, 1% profit might become 0.5%
- Recommend setting take-profit to 1.5-2% for buffer

---

## X. Bonus: The Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **RSI period set to 7**: More sensitive than default 14, reacts faster
   > "Don't want to wait too long, signals come quicker!"

2. **Bollinger period set to 12**: Narrower than default 20, breakouts more frequent
   > "More breakout signals, more trading opportunities"

3. **Buy comment says "optional filter, need to investigate"**: Author isn't sure if RSI > 70 is necessary
   > "This condition might need research... eh, let it be for now"

---

## XI. Final Words

### One-Sentence Review
> "Simple strategy lives up to its name, simple to the max. But take-profit and stop-loss need optimization, don't copy default parameters."

### Who Should Use It?
- ✅ Quantitative beginners: One of the best entry strategies
- ✅ People who want to learn: Clear code, good for studying
- ✅ Short-term traders: Quick in-out style

### Who Shouldn't Use It?
- ❌ People seeking high win rates: This strategy may not have high win rate
- ❌ People seeking big profits: 1% take-profit can't catch big trends
- ❌ Risk averse: 25% stop-loss is too exciting

### Manual Trader Recommendations

If you trade manually, you can borrow this thinking:
1. Look at overall trend (MACD > 0)
2. Wait for momentum confirmation (MACD golden cross)
3. Check price breakout (Bollinger upper band up)
4. Confirm strength (RSI > 70)
5. After entry, set take-profit and stop-loss

But remember: Manual trading can use smaller stop-loss and bigger take-profit!

---

## XII. ⚠️ Risk Emphasis (Must Read)

### Backtesting is Beautiful, Live Trading Be Careful

Simple strategy's historical backtests might look okay - but there's a trap:

> **Because logic is simple, many think it's "robust." But actually, simple strategies often rely too much on specific market conditions.**

Simply put: **Backtest is tailwind, live trading might be headwind.**

### Hidden Risks of Simple Strategies

In live trading, simple strategies may cause:
- **Market environment changes**: Strategy only fits trending markets, ranging markets repeatedly stop out
- **Parameter sensitivity**: Few parameters, but each is critical
- **Slippage erodes profit**: 1% profit, fees plus slippage might leave 0.5%

### My Recommendations (Real Talk)

```
1. Test with small capital first, don't go all-in
2. Adjust stop-loss to 10-15%, protect capital
3. Raise take-profit to 2-3%, give trend some room
4. Add trailing stop to lock in floating profit
5. Only use in trending markets, turn off in ranging markets
```

**Remember**: No matter how simple the strategy, the market isn't simple. Light position testing, survival is most important! 🙏

---