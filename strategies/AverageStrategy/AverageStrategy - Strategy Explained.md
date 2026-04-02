# AverageStrategy: The "Hello World" of Quantitative Trading

> **Nickname**: MA Rookie, The Rite of Passage  
> **Profession**: Trend Following Apprentice  
> **Timeframe**: 4 Hours

---

## I. What is This Strategy?

Simply put, **AverageStrategy** is:
- A dual moving average crossover strategy
- Golden cross to buy, death cross to sell
- Code so clean it'll make you cry

It's like the "Hello World" of quantitative trading — just like your first program usually prints "Hello World", this is the first strategy you write when learning Freqtrade 🤣

**The author said it themselves**: This is just a "proof of concept", and it doesn't perform well in live trading. So don't expect it to make money, but it's absolutely top-tier for learning the framework!

---

## II. Core Configuration: Basically "Buy and Sell"

### Take Profit Rules (ROI Table)

```python
minimal_roi = {"0": 0.5}  # Run at 50%
```

**Translation**: Sell automatically at 50% profit. This target is set pretty high, meaning it's designed for trending markets, not quick in-and-out trades.

### Stop Loss Rules

```python
stoploss = -0.2  # Cut at 20% loss
```

**Translation**: Accept defeat at 20% loss. For a 4-hour level strategy, this stop loss is pretty loose, since larger timeframes have bigger swings.

---

## III. 1 Entry Condition: Simple Enough to Cry

This strategy's entry condition is ridiculously simple:

### 🎯 The Only Condition: EMA Golden Cross

**Core Logic**: Short-term MA crosses above long-term MA

**Plain English**:
> "When EMA 8 (the fast line) crosses above EMA 21 (the slow line) from below, it means short-term momentum just got stronger, the trend might be going up — buy!"

**Code looks like this**:
```python
qtpylib.crossed_above(dataframe['maShort'], dataframe['maMedium'])
```

Just one line! Makes you think "that's it?"

---

## IV. Exit Logic: Beautifully Symmetrical

### Death Cross Exit

| Signal | Condition | Plain English |
|--------|-----------|----------------|
| Death Cross | EMA 8 crosses below EMA 21 | "Short-term momentum is weakening, trend might go down — sell!" |

**Perfect logical symmetry**: Golden cross buy, death cross sell — clean and efficient, no dragging feet.

---

## V. This Strategy's "Personality"

### ✅ Pros (The Good Stuff)

1. **Extremely simple**: Only about 50 lines of code total, beginners understand instantly
2. **Classic and reliable**: Dual MA crossover is the grandfather of technical analysis, still used after centuries
3. **Few parameters**: Just two MA parameters, easy to tune, no parameter explosion
4. **Learning friendly**: Perfect as your first strategy

### ⚠️ Cons (The Bad Stuff)

1. **Author said it doesn't work**: Original quote "doesn't really perform that well", which means "not great performance"
2. **Gets killed in ranging markets**: When moving sideways, MAs keep crossing, you'll get repeatedly slapped
3. **Serious lag**: By the time MAs cross, half the move is already gone
4. **No filtering**: No trend confirmation, no risk control, just bare-bones

---

## VI. Suitable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|--------------------|--------|
| Strong Uptrend | Give it a try | Can follow trends |
| Sideways Range | Don't use | Will get repeatedly stopped out |
| Crash | Not applicable | No shorting mechanism |
| High Volatility | Use cautiously | May get caught by noise fake breakouts |

**Bottom line**: Use it when there's a trend, don't bother when there isn't.

---

## VII. Summary: How's This Strategy Really?

### One-liner
> "It's for learning, not for making money. But once you learn it, you've got the basics down."

### Who should use it?
- ✅ Freqtrade beginners
- ✅ People wanting to understand MA crossover principles
- ✅ Developers needing a strategy template
- ✅ Teaching demonstrations

### Who shouldn't use it?
- ❌ Those wanting to make money directly (author said it doesn't work)
- ❌ Those in ranging markets
- ❌ Those seeking high win rates
- ❌ Those requiring complex risk control

### My Advice

```
1. First use it to learn the framework, understand populate_indicators, populate_entry_trend, populate_exit_trend
2. Then add stuff: add ADX to filter trend strength, add RSI to filter overbought/oversold
3. Then consider live trading, small position testing
```

**Remember**: This is a brick, meant to attract jade. Don't expect the brick itself to build a house, but it can help you learn the basics of house-building.

---

## VIII. What Market Can This Strategy Make Money In?

### 8.1 Core Logic: Trend Following 101

AverageStrategy is the **textbook example of a trend following strategy**.

**Its money-making philosophy**:
- **Go with the flow**: Enter only after trend forms, no bottom-fishing or top-calling
- **Symmetrical trading**: Buy and sell with consistent logic
- **Medium-term perspective**: 4-hour framework, suitable for swings lasting days to weeks

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English |
|:------------|:-------------------|:--------------|
| 📈 Strong Uptrend | ⭐⭐⭐⭐☆ | Can follow trends, but entry is a bit late |
| 📉 Strong Downtrend | ⭐⭐☆☆☆ | Will stay in cash, but no shorting opportunity |
| 🔄 Sideways Range | ⭐☆☆☆☆ | Repeatedly slapped, losing fees until you doubt life |
| ⚡️ High Volatility | ⭐⭐☆☆☆ | May get caught by fake breakouts |

**One sentence summary**: Use it when there's a trend, don't waste fees when there isn't.

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration | Recommended Value | Commentary |
|---------------|-------------------|------------|
| Trading Pairs | BTC/USDT, ETH/USDT | Major coins have obvious trends, don't use small caps |
| MA Parameters | 8/21 (default) | Can adjust, but don't make too small, too much noise |

### 9.2 Key Configuration Settings

```yaml
# This strategy needs simple configuration
timeframe: 4h
stoploss: -0.2
minimal_roi: {"0": 0.5}
```

### 9.3 Hardware Requirements (Easy)

This strategy has minimal computational needs, any computer can run it:
- RAM: 1GB is enough
- CPU: Even a Raspberry Pi works
- VPS: Cheapest one is fine

**Advantage**: Very low resource usage, can run multiple pairs without worry.

---

## X. Easter Egg: The Author's "Little Quirks"

Looking carefully at the code, you'll find some interesting things:

1. **Author is brutally honest**:
   > "doesn't really perform that well and its just a proof of concept"
   
   Translation: This strategy doesn't perform well, it's just proof of concept. The author is honestly adorable!

2. **Casual variable naming**:
   ```python
   dataframe['maShort']  # OK, fine
   dataframe['maMedium']  # This is called "medium" not "long"?
   ```
   You'll notice he uses "short" and "medium", not "short" and "long". Maybe because 21-period seems like medium-term to him?

3. **Concise comments**:
   ```python
   # buys and sells on crossovers - doesn't really perfom that well
   ```
   So direct it makes you laugh — the author states the strategy's flaws right in the code.

---

## XI. Final Words

### One-liner Review
> "It's the first step on the learning journey, but definitely not the destination for making money."

### Who should use it?
- ✅ Freqtrade beginners
- ✅ People wanting to understand MA strategies
- ✅ Developers needing code templates

### Who shouldn't use it?
- ❌ Those wanting passive income
- ❌ Those wanting to profit in ranging markets
- ❌ Those seeking high win rates and returns

### Advice for Beginners

```
1. Get this strategy running, learn Freqtrade's basic framework
2. Add ADX to filter trend strength, win rate will improve a lot
3. Add volume confirmation, fewer fake breakouts
4. Add dynamic stop loss, less profit giveback
5. After doing all the above, consider small capital live trading
```

**Remember**: This is a door-knocking brick, not a gold brick. After knocking open the door, you still need to build the house yourself.

---

## XII. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting is Beautiful, Live Trading is Dangerous

The author themselves said this strategy doesn't perform well, what do you expect? 😅

**This strategy's problem**:
> **Too simple, so simple it has no fault tolerance.**

Simply put: **Follow the trend and get some soup, get repeatedly butchered when there's no trend.**

### Improvement Directions

If you really want to use it live:
- **Add trend filtering**: Only enter when ADX > 25
- **Add volume confirmation**: Trust only volume breakouts
- **Add dynamic stop loss**: ATR stop or trailing stop

### My Honest Advice

```
1. First run backtesting, feel the characteristics of MA strategies
2. Learn its code structure, understand what each function does
3. Build on top of it, modify it into your own strategy
4. Don't go live directly, unless you want to pay tuition
```

**Remember**: Learning strategies and using strategies are two different things. This strategy is for learning, not for making money.

---

**Final Reminder**: MA strategies are required learning for quantitative trading. Only by understanding the principles can you understand why more complex strategies are designed the way they are. Keep going! 💪