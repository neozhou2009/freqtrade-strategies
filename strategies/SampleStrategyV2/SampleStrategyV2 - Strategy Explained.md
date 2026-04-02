# SampleStrategyV2: Freqtrade's Official "Textbook" Strategy

> **Nickname**: Textbook Strategy  
> **Occupation**: Entry-level Teaching + Trend Following Demo  
> **Timeframe**: 5-minute main battlefield + 1-hour intelligence agency

---

## I. What is This Strategy?

Simply put, **SampleStrategyV2** is:
- Official example strategy (literally a textbook)
- 1 buy condition + 1 sell condition (clean and simple)
- RSI oversold rebound + TEMA momentum confirmation + Heikin Ashi trend
- 3 Hyperopt parameters for tuning

Like a beginner's textbook for quantitative trading, not complex, but everything it teaches is solid gold 📖

---

## II. Core Configuration: "Simple and Direct"

### Take-Profit Rules (ROI Table)

```
Just bought → Run at 4% profit
After 30 min → Run at 2% profit
After 60 min → Run at 1% profit
```

**Translation**: The longer you hold, the lower the profit target. Same design as complex strategies - don't be greedy.

### Stop-Loss Rules

```
Fixed stop loss: -20%
Trailing stop: Activates after 1% profit, locks profit at 0.5% pullback
```

**Translation**: 20% stop loss is relatively loose, suitable for volatile cryptocurrencies. Trailing stop protects small profits.

---

## III. Buy Condition: One Is Enough!

### 🎯 The Only Buy Signal

**Core Logic**: RSI oversold rebound + TEMA low position rising + HA trend upward

**Plain English**:
> "RSI drops below 30 then rebounds, TEMA starts rising near Bollinger lower band, Heikin Ashi trend is upward, volume is not zero."

**Detailed Breakdown**:

| Sub-condition | Code | Plain English |
|---------------|------|---------------|
| **RSI Cross** | crossed_above(rsi, 30) | "RSI crosses up from below 30, oversold starting to rebound" |
| **Trend Upward** | trend_dir > 0 | "Heikin Ashi trend direction is up" |
| **TEMA Low** | tema <= bb_middleband | "TEMA is below Bollinger middle band, position not high" |
| **TEMA Rising** | tema > tema.shift(1) | "TEMA is going up, momentum strengthening" |
| **Has Volume** | volume > 0 | "Market has activity, not a dead coin" |

**One Sentence**:
> "RSI says buy, TEMA says rising, HA says trend up - let's buy!"

---

## IV. Sell Condition: Also Just One!

### 🎯 The Only Sell Signal

**Core Logic**: RSI overbought + TEMA high position falling

**Plain English**:
> "RSI rises above 70 then crosses, TEMA starts falling above Bollinger middle band, time to run."

**Detailed Breakdown**:

| Sub-condition | Code | Plain English |
|---------------|------|---------------|
| **RSI Cross** | crossed_above(rsi, 70) | "RSI crosses up from below 70, overbought signal" |
| **TEMA High** | tema > bb_middleband | "TEMA is above Bollinger middle band, position high" |
| **TEMA Falling** | tema < tema.shift(1) | "TEMA is going down, momentum weakening" |
| **Has Volume** | volume > 0 | "Market has activity, can sell" |

**One Sentence**:
> "RSI says overbought, TEMA says starting to fall - time to retreat!"

---

## V. Technical Indicators: This Strategy's Toolkit

### Core Weapons

| Indicator | Purpose | Plain English |
|-----------|---------|---------------|
| **RSI(14)** | Overbought/oversold judgment | "Sentiment indicator, buy low sell high" |
| **TEMA(9)** | Triple Exponential MA | "Fast moving average, sensitive response" |
| **Bollinger Band(20)** | Volatility boundary | "Price corridor, sell upper buy lower" |
| **Heikin Ashi** | Price smoothing | "Smoothed candles, less noise" |
| **MACD(1h)** | Large cycle trend | "1-hour trend direction" |
| **ADX** | Trend strength | "How strong is the trend" |

### What is Heikin Ashi?

**Plain English Explanation**:
Heikin Ashi is a special candlestick smoothing technique. Regular candles are volatile with lots of noise. Heikin Ashi averages prices to make trends clearer.

Like adding a "noise reduction filter" to photos, trends become more visible.

**How trend_dir is Calculated**:
```
Trend direction = SMA(SMA(ha_close_sma288 - ha_open_sma288, 5), 5)
```

> Calculate the difference between HA close and open, then double smooth. Greater than 0 means uptrend.

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Clear Structure**: Concise code, great for learning
2. **Official Product**: Freqtrade official textbook, standardized and correct
3. **Hyperopt Friendly**: 3 parameters can be optimized
4. **Multi-indicator Verification**: RSI+TEMA+BB+HA multi-dimensional confirmation
5. **Easy to Extend**: Adding conditions on this basis is convenient

### ⚠️ Cons (Complaint Section)

1. **Too Few Buys**: Only one signal, might miss opportunities
2. **Loose Stop Loss**: 20% stop loss is a bit large, may lose more
3. **Insufficient Protection**: No pump protection, EMA filtering, or other safety measures
4. **Sparse Signals**: Strict conditions, may not get enough signals

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|--------------------|--------|
| **Uptrend** | Default configuration | Oversold pullback entry works well |
| **Oscillating Market** | Lower buy_rsi to 25 | Wait for deeper oversold |
| **High Volatility** | Widen stop loss to 25% | Avoid frequent stop losses |
| **Calm Market** | Raise sell_rsi to 75 | Extend holding time |

---

## VIII. Summary: How Is This Strategy Really?

### One-sentence Review
> "Textbook-level entry strategy - use it to learn Freqtrade, be careful using it for live trading"

### Who Should Use It?
- ✅ Freqtrade beginner learners
- ✅ Developers wanting to understand strategy framework
- ✅ Users wanting to do secondary development
- ✅ People who like simple strategies

### Who Shouldn't Use It?
- ❌ Users wanting high-frequency trading (too few signals)
- ❌ Users needing multi-layer protection (none here)
- ❌ Risk-averse users (20% stop loss too large)
- ❌ Users wanting direct live trading profit (needs optimization)

### My Advice
1. **Learn the code first**: This strategy is a textbook, understand before modifying
2. **Add buy conditions**: One signal isn't enough, add a few more
3. **Add protection mechanisms**: Like EMA filtering, pump protection
4. **Optimize parameters**: Use Hyperopt to find values suitable for your market
5. **Test thoroughly**: Dry-run verify before live trading

---

## IX. What Market Can This Strategy Make Money In?

### 9.1 Core Logic: Wait for Clear Oversold Rebound

SampleStrategyV2's logic is simple and clear:

**Buy Wait**: RSI drops below 30, then starts rebounding
**Sell Wait**: RSI rises above 70, then starts declining

Like waiting for a "clear signal", not vague, not conflicted.

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Uptrend | ⭐⭐⭐⭐☆ | When trend is up, oversold pullback entry works well |
| 🔄 Oscillating Sideways | ⭐⭐☆☆☆ | Single condition, too few signals, might miss opportunities |
| 📉 Downtrend | ⭐☆☆☆☆ | 20% stop loss may lose too much |
| ⚡ Fast Volatility | ⭐⭐☆☆☆ | HA smoothing may react slowly |

**One-sentence Summary**: Suitable for markets with clear trends, not for oscillation and downtrends.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Adjustable Parameters

| Parameter | Default | Range | Plain English |
|-----------|---------|-------|---------------|
| **buy_rsi** | 30 | 1-50 | "RSI cross threshold, buy below this" |
| **buy_trend_length** | 288 | 50-288 | "HA trend calculation period" |
| **sell_rsi** | 70 | 50-100 | "RSI cross threshold, sell above this" |

### 10.2 Hardware Requirements

This strategy has moderate computation:

```python
startup_candle_count: int = 1000
```

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|---------------------|------------|
| 20-40 | 2GB | 4GB | Normal |
| 40-80 | 4GB | 8GB | Smooth |

**Good News**: Uses less resources than complex strategies!

### 10.3 Backtest vs Real Trading

As an example strategy, backtest performance may be unstable:
- Few parameters, easy to optimize to historical optimum
- But lacks protection, high live trading risk

**Recommended Process**:
1. Read code, understand logic
2. Dry-run for at least a week
3. Use Hyperopt to optimize parameters
4. Test with small positions
5. Add protection mechanisms based on results

---

## XI. Bonus: Teaching Points Hidden in the Code

Looking carefully at the code, you'll find many teaching points:

1. **Rich Comments**: Every indicator has explanatory comments
   > "Author was afraid you wouldn't understand, comments written clearly"

2. **Optional Indicator Examples**: Many indicators commented out but code preserved
   > "Want to learn other indicators? Code is ready for you"

3. **plot_config Example**: Defined plotting configuration
   > "Can directly see strategy signals in FreqUI"

4. **order_types Example**: Shows order type configuration
   > "Limit buy limit sell, stop loss market execution"

---

## XII. Final Words

### One-sentence Review
> "Textbook strategy - must-read for learning Freqtrade, but needs your own additions for live trading"

### Who Should Use It?
- ✅ Freqtrade beginners
- ✅ Strategy learners
- ✅ Secondary developers
- ✅ Users who like simplicity

### Who Shouldn't Use It?
- ❌ Users wanting direct profit
- ❌ Users needing multiple signals
- ❌ Users needing protection mechanisms
- ❌ Risk-averse users

### Manual Trader Advice
This strategy's logic is simple, manual traders can reference it:
- Watch for RSI crossing 30 signal
- Check TEMA position and direction
- Use Heikin Ashi to confirm trend
- Manual execution is relatively feasible

---

## XIII. ⚠️ Risk Re-emphasis (Must Read)

### Example Strategy Trap

SampleStrategyV2 is a **teaching example**, not a live trading weapon:

> **Official documentation explicitly states: This is an example strategy, you need to optimize and adjust it yourself.**

Simply put: **Textbooks teach you how to write strategies, not for you to directly make money**

### Missing Protections

This strategy lacks many protections needed for live trading:
- **No EMA filtering**: May enter in downtrend
- **No pump protection**: May chase highs
- **No dip protection**: May bottom-fish during crashes
- **Loose stop loss**: 20% may lose too much

### My Advice (Heartfelt)

```
1. Use this strategy as a textbook, seriously learn the code structure
2. Add your own buy conditions on this basis
3. Add protection mechanisms (EMA, pump, dip protection)
4. Use Hyperopt to optimize parameters
5. Dry-run thoroughly before live trading
```

**Remember**: Textbook strategies are for learning, not for directly making money. Add your own ingredients before live trading!

---

**Final Reminder**: This is Freqtrade's official example strategy. After learning, recommend secondary development, adding more conditions and protection mechanisms before live trading. Don't take a textbook to war! 🙏