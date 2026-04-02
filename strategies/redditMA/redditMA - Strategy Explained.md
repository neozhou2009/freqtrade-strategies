# redditMA Strategy: Two Lines, Simple Truth

> **Nickname**: The "Minimalist" of Quant Trading  
> **Profession**:极简主义 Trend Follower (Minimalist Trend Follower)  
> **Timeframe**: 15 minutes

---

## 1. What Is This Strategy?

Simply put, **redditMA** is:
- A strategy using only two lines
- Buy on golden cross, sell on death cross
- No fancy indicators whatsoever
- Code so short you'll doubt your life

Like a **monk who only drinks plain water**, while everyone else is studying complex martial arts manuals, he just says: "One moving average rules them all." 🧘

---

## 2. Core Configuration: Just "Follow the Trend"

### Take-Profit Rules (ROI Table)

```
Just bought       → Run when you make 50%
After 30 min      → Run when you make 30%
After 60 min      → Run when you make 12.5%
After 120 min     → Run when you make 6%
After 180 min     → Run when you make 1%
```

**Translation**: This is called "time-decreasing take-profit." When you first buy, you're ambitious, wanting 50%; as time passes, you become more peaceful, even 1% is fine. Like when you first start dating, you say you'll be together forever; after a while, you're happy if you don't fight 😂

### Stoploss Rules

```
Lose 10% → Cut losses and leave
```

**Translation**: Simple and brutal. Down 10%, admit defeat, no hesitation.

---

## 3. One Buy Condition: Just This One!

This strategy's buy condition is **really just one**, I don't even need to categorize:

### 🎯 The Only Condition: EMA Golden Cross

**Code**:
```python
qtpylib.crossed_above(dataframe['FASTMA'], dataframe['SLOWMA'])
```

**Plain English**:
> "Fast line crosses above slow line from below, going up, BUY!"

That's it. No RSI, no MACD, no volume, no Bollinger Bands... just two lines crossing.

**The Two Lines Are**:
- **Fast Line**: EMA(34) — The line with the longer period (naming is counter-intuitive here, but don't overthink it)
- **Slow Line**: EMA(13) — The line with the shorter period

When the short one crosses up from below, buy. When the short one crosses down from above, sell.

---

## 4. Protection Mechanisms: Zero Layers!

Each buy condition comes with a set of protection parameters? **Not here!**

| Protection Type | Available? |
|---------|---------|
| RSI Filtering | ❌ No |
| Volume Confirmation | ❌ No |
| Bollinger Band Filtering | ❌ No |
| Multi-Timeframe Confirmation | ❌ No |
| Any Other Filtering | ❌ No |

**This Strategy's Creed**:
> "Complexity is the root of all evil, simplicity is the true path." 🙏

A quick roast: This strategy is like **a motorcyclist without a helmet**—either very brave or very naive. But in some cases, simple just works.

---

## 5. Sell Logic: Also Just One Line!

### 5.1 Sell Signal: EMA Death Cross

**Code**:
```python
qtpylib.crossed_below(dataframe['FASTMA'], dataframe['SLOWMA'])
```

**Plain English**:
> "Fast line crosses below slow line from above, going down, RUN!"

Again, two lines, cross once, leave.

### 5.2 Tiered Take-Profit

Besides the death cross sell, there's also a **time-decreasing ROI**:

| Holding Time | Profit to Run |
|---------|----------|
| 0 minutes (just bought) | 50% |
| 30 minutes | 30% |
| 60 minutes | 12.5% |
| 120 minutes | 6% |
| 180 minutes | 1% |

**Plain English**:
- Just bought, expecting to make half your money back
- Held for half an hour, 30% is fine
- Held for an hour, 10%+ is enough
- Held for two hours, 6% is satisfying
- Held for three hours, even 1% is not bad

This logic is like **a dating app's user retention strategy**: new users get the best recommendations; as time passes, just throw some content at them, as long as you don't leave 🤣

### 5.3 Special Configuration

```python
sell_profit_only = True  # Only respond to sell signals when profitable
ignore_roi_if_buy_signal = True  # Ignore ROI when buy signal is present
```

**Translation**:
- When losing, don't sell even on death cross (wait to break even)
- When buy signal is present, don't rush to exit via ROI (might be an add position opportunity)

---

## 6. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Session)

1. **Extreme Simplicity**: Code is just 70 lines, not much more complex than your "Hello World"
2. **Fast Computation**: Just two EMAs, even a Raspberry Pi can run it
3. **Clear Logic**: No ambiguity, no hidden logic
4. **Learning Friendly**: Excellent textbook for learning strategy development
5. **Easy to Modify**: Want to add features? Just add them, no historical baggage

### ⚠️ Weaknesses (Roast Session)

1. **Signal Noise**: In ranging markets, the two lines can cross 800 times, fees will hurt your heart
2. **No Trend Judgment**: It doesn't know if the market is trending or ranging, just jumps on any signal
3. **Lag**: EMA is a lagging indicator; by the time it crosses, the trend might be almost over
4. **No Volume**: Might buy under unhealthy volume conditions
5. **Single Timeframe**: Can't see the big picture, easy to get lost in short-term fluctuations

---

## 7. Usage Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| Strong Trend Market | ✅ Enable | EMA can follow the trend, makes good money |
| Ranging Market | ❌ Don't Use | Will get slapped repeatedly |
| Beginner Learning | ✅ Recommended | Simplest strategy, understand at a glance |
| Low-Config Device | ✅ Perfect | Minimal computation, no resource drain |

---

## 8. Summary: How Is This Strategy Really?

### One-Sentence Evaluation
> "A model of simplicity, and also the price of simplicity."

### Who Should Use It?
- ✅ Beginners just starting out (for learning)
- ✅ People who want to modify strategies themselves (good foundation to modify)
- ✅ Low-configuration VPS users (doesn't consume resources)
- ✅ Followers of strong trend markets

### Who Should NOT Use It?
- ❌ People who want to make money lying down (will lose in ranging markets)
- ❌ People pursuing high win rates (signal noise is large)
- ❌ People who don't want to do parameter optimization (default parameters may not suit all coins)
- ❌ People who frequently switch strategies (needs long-term operation in trend markets)

### My Recommendations
1. **Learn first, then trade live**: Use this strategy as a textbook, understand every line
2. **Add filters**: At least add RSI or volume confirmation
3. **Do parameter optimization**: EMA periods can be adjusted based on the asset
4. **Only use in trend markets**: Let it rest during ranging markets

---

## 9. In What Markets Can This Strategy Make Money?

### 9.1 Core Logic: Eat Trends with Two Lines

redditMA is the **"minimalist" of quantitative trading**. 70 lines of code, what does that mean? Shorter than a normal Python script 📚

**Its Money-Making Philosophy**:
- **Follow the Trend**: EMA direction is market direction
- **Don't Guess Tops/Bottoms**: Be a follower, not a predictor
- **Simple and Brutal**: Cross = signal, no hesitation

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Strong Trend Market | ⭐⭐⭐⭐⭐ | Like riding a bike with the wind, goes forward without pedaling |
| 🔄 Ranging Market | ⭐☆☆☆☆ | Like being in a washing machine, spins you dizzy |
| 📉 Downtrend | ⭐⭐☆☆☆ | Death cross runs away in time, but don't try to catch the bottom |
| ⚡️ High Volatility | ⭐⭐☆☆☆ | By the time you see the cross, the move is already over |

**One-Sentence Summary**: **A follower in trend markets, a victim in ranging markets**.

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Roast |
|--------|--------|------|
| Trading Pairs | BTC/USDT, ETH/USDT | Major coins have strong trends |
| Timeframe | 15m (default) | Can try 1h or 4h |
| EMA Periods | 13/34 (default) | Classic combo, but optimizable |

### 10.2 Key Config File Settings

```yaml
# Stoploss
stoploss: -0.10

# ROI (optional, use strategy default)
minimal_roi:
  0: 0.5
  30: 0.3
  60: 0.125
  120: 0.06
  180: 0.01
```

### 10.3 Hardware Requirements (Important!)

This strategy has minimal computation, hardware requirements are **low as dust**:

| Trading Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------|---------|---------|------|
| 1-10 | 512MB | 1GB | Silky smooth |
| 10-50 | 1GB | 2GB | Fluent |
| 50+ | 2GB | 4GB | No pressure |

**Warning**: If you can't even run this, your VPS should probably be thrown away 😅

### 10.4 Backtest vs Live Trading

Due to strategy simplicity, differences between backtest and live trading are relatively small:
- Main difference comes from slippage (stoploss is market order)
- Ranging market backtests may look good, live trading gets wrecked by fees

**Recommended Process**:
1. Backtest to see if logic is correct
2. Run on demo account for a while
3. Live trade with small capital to test
4. Add capital after confirming effectiveness

**Don't go all-in immediately**, even the simplest strategy needs磨合 (breaking in)!

---

## 11. Easter Egg: The Strategy Author's "Little Tricks"

Look closely at the code, you'll find some interesting things:

1. **Counter-Intuitive Naming**:
   > "Fast line is EMA(34), slow line is EMA(13)... wait, that's wrong, right?"
   
   Yes, the code naming is a bit counter-intuitive, but the logic is correct. Maybe the author did it on purpose, testing whether readers truly understand the logic or just look at names.

2. **History in Comments**:
   ```python
   """
   3. sma ema with complicated support
   4. sma ema with simple support
   ...
   """
   ```
   This shows the strategy went through multiple iterations, from complex to simple. The author probably tried various tricks, finally discovering: **simple is best**.

3. **Missing informative_pairs**:
   ```python
   def informative_pairs(self):
       return []
   ```
   Returns an empty list. The author might be saying: **I only look at this one timeframe, don't care about the rest**.

---

## 12. The Final Word

### One-Sentence Evaluation
> "Plain water in quantitative strategies—bland and tasteless, but essential."

### Who Should Use It?
- ✅ Beginners just starting out
- ✅ People who want to learn strategy principles
- ✅ Low-configuration VPS users
- ✅ People who like concise code
- ✅ Followers of strong trend markets

### Who Should NOT Use It?
- ❌ People who want to make money lying down
- ❌ People who want to make money in ranging markets
- ❌ People who don't do parameter optimization
- ❌ People who pursue complex logic

### Manual Trading Recommendations

This strategy's logic **can be directly used for manual trading**:

1. Open TradingView, look at the 15-minute chart
2. Add EMA(13) and EMA(34)
3. Buy on golden cross, sell on death cross
4. Set 10% stoploss
5. Adjust profit targets based on holding time

**That's it**. You don't even need to run freqtrade, just do it manually 🤣

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtests Are Beautiful, Live Trading Requires Caution

redditMA's backtests may look great—excellent performance in trend markets. But there's a trap:

> **Because the strategy is so simple, it gets continuously harvested in ranging markets.**

Simply put: **When trends come, you make bank; when ranging happens, you lose until you doubt life**.

### Hidden Risks of Simple Strategies

In live trading, simple strategies can lead to:
- **Frequent Trading**: In ranging markets, can trade dozens of times a day, fees explode
- **Signal Lag**: EMA is a lagging indicator; by the time it crosses, you may have missed the optimal entry
- **Cannot Adapt to Market Changes**: No dynamic parameters, when the market changes, it's done
- **Emotional Pressure**: During consecutive stoplosses, you'll doubt whether you should change parameters

### My Recommendations (Real Talk)

```
1. Only enable in trend markets
2. Add at least one trend filter (like ADX)
3. Do parameter optimization, find the best EMA periods for your trading pairs
4. Strictly control positions, don't exceed 5%
5. Set daily/weekly stoploss limits
```

**Remember**: No matter how simple the strategy, the market is not simple. Trend following has worked for decades, but ranging markets are also the norm.

---

**Final Reminder**: No matter how good the strategy, the market won't greet you before teaching you a lesson. Light position testing, staying alive is most important! 🙏

---

*As the last of 465 strategies, redditMA concludes with perfect simplicity. It tells us: sometimes, the simplest answer is the best answer.*
