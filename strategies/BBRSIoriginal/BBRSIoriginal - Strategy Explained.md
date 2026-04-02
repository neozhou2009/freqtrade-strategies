# BBRSIoriginal Strategy: The Simplest "Bottom-Fishing" Tool

> **Nickname**: Bollinger Band Bottom-Fisher  
> **Job**: Freqtrade's "Official Face" — The Gatekeeper of Beginner Village  
> **Timeframe**: 1 hour

---

## I. What is This Strategy?

Simply put, **BBRSIoriginal** is:

- Price breaks through Bollinger Band lower band → Buy!
- RSI shoots above 75, price returns to middle band → Sell!

That's it! This is Freqtrade's built-in default strategy, less than 100 lines of code, specifically for beginners to learn from.

Like a "bottom-fishing expert": **Staring at the Bollinger Band lower band, as soon as price breaks through, jump in, wait for the bounce, then sell** 🎣

---

## II. Core Configuration: Simply Put, "Waiting for Bargains"

### Take Profit Rules (ROI Table)

```
At open: Need 9.6% profit to sell
After 19 minutes: 3.6% is fine
After 69 minutes: 1.9% is OK
After 120 minutes: Any profit, just sell
```

**Translation**:
- Just opened, ambitious — "I want 9.6%!"
- After 19 minutes, getting impatient — "Fine, 3.6% works"
- After 1 hour, more impatient — "1.9% is OK too"
- After 2 hours — "Any profit, just run, don't waste time"

**Complaint**:
> This tiered ROI is interesting — at open "I have patience", after 2 hours "I don't want to wait anymore" 😂

### Stop Loss Rule

```
Stop loss: -36.828%
```

**Translation**:
- Only stop loss after losing more than 36.8%
- Means 100 bucks has to drop to 63 bucks before running

**Complaint**:
> This stop loss is ridiculously wide! Only run after losing a third? What kind of heart can withstand that? This is the legendary "either profit or hold"!

### Order Types

```
Buy: Limit order
Sell: Limit order
Stop loss: Limit order (executed locally)
```

**Translation**: All limit orders, ensuring price control. Stop loss not executed on exchange, controlled locally by Freqtrade.

---

## III. Buy Conditions: Price Breaks Bollinger Band Lower Band, Just Do It

### 🎯 Core Logic

**Just one condition**:

```python
close < bb_lowerband3  # Price breaks below 3-standard deviation Bollinger Band lower band
```

### What is "3-Standard Deviation Bollinger Band"?

Everyone knows Bollinger Bands: middle band is moving average, upper/lower bands are MA ± standard deviation.

- **1 standard deviation**: Covers about 68% of prices
- **2 standard deviations**: Covers about 95% of prices
- **3 standard deviations**: Covers about 99.7% of prices

**3-standard deviation Bollinger Band lower band**:
> Price dropping here means "statistically only 0.3% probability of reaching this position" — extreme oversold!

### Buy Signal in Plain English

> **"Price broke through the Bollinger Band lower band! This is extreme oversold, it must bounce! Buy buy buy!"**

**Note**:
- Doesn't check volume
- Doesn't check trend
- Purely looks at "is price low enough"

**This is a classic "catch falling knife" strategy** — buying when price crashes, betting it will bounce.

---

## IV. Sell Logic: Run When RSI Gets High

Sell requires both conditions to be met:

### Condition #1: RSI > 75

```python
RSI > 75  # RSI above 75
```

**Plain English**:
> "RSI hit 75, this is overbought, momentum is too strong!"

### Condition #2: Price Back Above Bollinger Band Middle Band

```python
close > bb_middleband  # Price above Bollinger Band middle band
```

**Plain English**:
> "Price has bounced back to middle band, bottom-fishing successful!"

### Both Conditions Must Be Met

```python
(RSI > 75) AND (close > bb_middleband) → Sell
```

**Plain English Translation**:
> "Price bounced to middle band, and RSI is overbought too — means the bounce is done, time to wrap up!"

---

## V. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **Ridiculously Simple**: Less than 100 lines of code, anyone can understand it. Freqtrade default strategy, beginners must learn.

2. **Classic Combination**: Bollinger Band + RSI, the "rice and noodles" of technical analysis, can't go too wrong.

3. **Reliable Extreme Signals**: 3-standard deviation Bollinger Band breakout is statistically really extreme, high signal quality.

4. **Comfortable 1-Hour Timeframe**: Not tiring like 5-minute, not slow like daily, friendly for part-time traders.

5. **Suitable for Manual Trading**: Simple signals, set an alert in TradingView and you can watch it.

### ⚠️ Cons (Complaint Time)

1. **Ridiculously Wide Stop Loss**: 36% stop loss?! Run after losing a third? What kind of heart can take that!

2. **Brain-Dead Bottom-Fishing**: No matter the trend, buy when it breaks lower band. In downtrends, this is "king of catching falling knives."

3. **Sparse Signals**: 3-standard deviation Bollinger Band breakouts don't happen every day, might be days without signals.

4. **Strict Sell Conditions**: RSI needs to hit 75, plus price back to middle band. Might bounce for a while, RSI just won't hit 75, finally forced out by ROI.

5. **Unused 4x Bollinger Band**: Code calculates 4-standard deviation Bollinger Band, but doesn't use it at all! What's this about? Maybe author forgot to delete it?

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 🔄 Range Bounce | Use carefully | This is its home turf, price goes back and forth through Bollinger Bands |
| 📈 Strong Uptrend | Don't use | Price won't break lower band, no signals |
| 📉 Sustained Downtrend | Definitely don't use | Frequent bottom-fishing, buying lower and lower, catching knives with bloody hands |
| ⚡ High Volatility | Can try | High volatility might trigger signals |

---

## VII. Summary: How Is This Strategy Really?

### One-Sentence Review
> **"Bollinger Band bottom-fishing textbook — simple code, clear logic, but needs modification for live trading."**

### Who Is It For?
- ✅ Freqtrade beginners (must-learn strategy)
- ✅ People wanting to understand Bollinger Band strategies
- ✅ Manual traders (simple signals)
- ✅ People wanting to modify and optimize on this foundation

### Who Is It NOT For?
- ❌ Direct live trading use (stop loss too wide, needs modification)
- ❌ Downtrend markets (will catch falling knives)
- ❌ High-frequency trading seekers (sparse signals)
- ❌ Risk-averse investors

### My Recommendations

1. **Learning First**: This is the best introductory textbook, understand it and you understand Freqtrade strategy basics.

2. **Must Modify Stop Loss**: 36% stop loss is unacceptable, suggest changing to 10%-15%.

3. **Add Trend Filter**: Add EMA or EWO in buy conditions to judge trend, avoid frequent bottom-fishing in downtrends.

4. **Can Manual Trade**: Set an alert in TradingView, Bollinger Band lower band breakthrough alerts, take a look manually before deciding.

---

## VIII. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: Mean Reversion School

BBRSIoriginal is a classic **"Mean Reversion Strategy"** — believing prices oscillate around moving averages, extreme deviations will revert.

**Its Money-Making Philosophy**:
- Bollinger Band lower band = extreme oversold = should bounce
- Bollinger Band middle band = normal price = bounce complete
- RSI > 75 = overbought = time to sell

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:---------------------------|
| 📈 Strong Uptrend | ⭐☆☆☆☆ | Price hangs around upper band all day, won't trigger buy at all |
| 🔄 Range Bounce | ⭐⭐⭐⭐⭐ | Perfect home turf! Price goes back and forth through bands, buy low sell high cycle |
| 📉 Sustained Downtrend | ⭐⭐☆☆☆ | Bottom-fishing every day, getting trapped every day, catching knives with bloody hands |
| ⚡ High Volatility No Direction | ⭐⭐⭐☆☆ | Signals exist, but quality might be mixed |

**One-Sentence Summary**:
> **Range bounce markets are its home turf, trending markets are its nightmare.**

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Must Modify Stop Loss

Default stop loss -36.828%, my recommendations:

| Risk Tolerance | Suggested Stop Loss | Note |
|---------------|--------------------|-------|
| Aggressive | -0.20 | 20% stop loss |
| Balanced | -0.15 | 15% stop loss |
| Conservative | -0.10 | 10% stop loss |

### 9.2 Trading Pair Selection

| Configuration Item | Recommended Value | Note |
|-------------------|------------------|-------|
| Number of Pairs | 10-20 pairs | Sparse signals, need more pairs to get trades |
| Pair Types | Major coins | Good liquidity, Bollinger Bands more reliable |
| Timeframe | 1h (default) | Can also try 30m or 2h |

### 9.3 Hardware Requirements (Super Low)

This strategy has minimal computation, any computer can run it:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-10 pairs | 512MB | 1GB | Smooth |
| 11-30 pairs | 1GB | 2GB | Normal |
| 31+ pairs | 2GB | 4GB | No problem |

**Complaint**:
> A Raspberry Pi can run this, resource requirements are negligible.

### 9.4 Backtest Recommendations

- At least 6 months data
- Sparse signals, single trade impact is large
- Recommend testing multiple time periods

---

## X. Bonus: "Little Secrets" in the Strategy

Look carefully at the code, and you'll find some interesting things:

1. **Calculated but Unused 4x Bollinger Band**:
   ```python
   bollinger = qtpylib.bollinger_bands(..., stds=4)  # Calculated
   # But completely unused later!
   ```
   > "Maybe author wanted to use it, then changed their mind? Or forgot?"

2. **Typical Price**:
   ```python
   typical_price = (High + Low + Close) / 3
   ```
   > "Bollinger Bands use typical price, not closing price — this detail is a bit pro!"

3. **Official Code Comments**:
   ```python
   """
   Default Strategy provided by freqtrade bot.
   You can override it with your own strategy
   """
   ```
   > "Official stamped default strategy, meaning 'you should probably modify it yourself.'"

---

## XI. Final Thoughts

### One-Sentence Review
> **"Freqtrade Beginner Village Gatekeeper — simple code, clear logic, suitable for learning, needs major modification for live trading."**

### Who Is It For?
- ✅ Freqtrade beginners (first strategy to learn)
- ✅ People wanting to understand Bollinger Band + RSI combination
- ✅ People wanting to modify and optimize on this foundation
- ✅ Manual traders (simple signals to follow)

### Who Is It NOT For?
- ❌ Direct live trading (stop loss too wide!)
- ❌ Downtrend markets
- ❌ High-frequency trading seekers
- ❌ Risk-averse investors

### Manual Trader Recommendations

Want to use this strategy manually? Simple:

1. Open TradingView
2. Add Bollinger Band indicator: period 20, standard deviation 3
3. Add RSI indicator: period 14
4. Set alerts:
   - Price breaks below Bollinger Band lower band → Alert
   - RSI > 75 and price > middle band → Alert

That's it, no code needed!

---

## XII. ⚠️ Risk Warning Again (Must Read)

### This Strategy is "Introductory Material", Not "Money-Making Machine"

BBRSIoriginal is Freqtrade's official default strategy, mainly for:

> **Teaching you how to write Freqtrade strategies, not for you to directly make money!**

### Three Major Risks

1. **Stop Loss Too Wide**: 36% stop loss, hit a "black swan" event and you could lose months of profits in a day.

2. **Brain-Dead Bottom-Fishing**: Frequently triggers buys in downtrends, buying lower and lower, finally harvested by stop loss.

3. **Sparse Signals**: 3-standard deviation Bollinger Band breakouts are rare, might only have a few trades a week.

### My Advice (From the Heart)

```
1. Change stop loss to 10%-15%, don't use the default 36%
2. Add a trend filter (like EMA100), forbid buying in downtrends
3. Pick more trading pairs (10-20), sparse signals need diversification
4. Backtest at least 6 months of data
5. Or — just use it as a template, modify it into a more suitable strategy
```

**Remember**: This is learning material, not a money printer. Understand it, modify it, transcend it! 🙏

---

**Strategy Source**: Freqtrade Official Default Strategy  
**Lines of Code**: About 80 lines  
**Nickname**: Bollinger Band Bottom-Fisher  
**Positioning**: Beginner Introductory Material