# SuperTrendPure Strategy: The Minimalist Who Trades with Just One Line

> **Nickname**: "The Single-Line Warrior", "One Moving Average to Rule Them All"
> **Profession**: Trend Following Specialist
> **Timeframe**: 1 Hour

---

## I. What Is This Strategy?

Simply put, **SuperTrendPure** is:
- Watch only one line (the SuperTrend line)
- Buy when price breaks above, sell when it breaks below
- No fancy conditions whatsoever

Like your friend telling you: "Buy when price crosses this line, run when it falls below" — that simple! 🤣

**The Philosophy**: Simplicity is ultimate sophistication. If one indicator can solve the problem, never use two.

---

## II. Core Configuration: "Steady Progress" in Plain Terms

### Take-Profit Rules (ROI Table)

```
Just bought: Run at 8.7% profit
After 6 hours without 8.7%: Run at 5.8% profit
After 14 hours without that: Take 2.9% profit
After 37 hours without that: Get out at breakeven, I'm done with you
```

**Translation**: This strategy is a bit "impatient" — high targets right after buying, but the longer you hold, the more eager to exit. But this makes sense — trend strategies need to strike while the iron is hot. Holding too long means the trend might be over.

### Stop Loss Rules

```
Hard stop loss: Accept defeat at -26.5% loss
Trailing stop: After making 14.4%, run on any pullback from the high
```

**Translation**:
- **Hard stop loss at -26.5%**: Pretty wide stop loss, giving the trend plenty of room for pullbacks. After all, trend trading requires patience to let profits run.
- **Trailing stop**: Automatically protects profits after making money, preventing "letting the duck fly away."

---

## III. 1 Buy Condition: That's It, Seriously

The buy condition is so simple it makes you question reality:

### 🎯 The One and Only Buy Condition

**Core Logic**: Price crosses above SuperTrend line from below, with volume.

**In Plain English**:
> "Price broke above the upper band, buy!"

That's one sentence. No "MACD golden cross", no "RSI oversold", no "moving average bullish alignment" — nothing, just this one line.

---

## IV. Sell Logic: Symmetry at Its Finest

Buy on upward cross, sell on downward cross. Completely symmetrical!

### Basic Sell Signal

```python
Price breaks below SuperTrend line + Volume exists = Sell
```

**In Plain English**:
> "Price broke below the lower band, run!"

This is the purest trend-following philosophy: **Follow the trend, retreat when it ends.**

---

## V. The SuperTrend Indicator: What Is This Magic Line?

You might ask: What exactly is this magical line?

### How SuperTrend Is Constructed

SuperTrend is essentially a dynamic support/resistance line drawn using **ATR (Average True Range)**:

```
Upper Band = (High + Low) / 2 + 2 × ATR
Lower Band = (High + Low) / 2 - 2 × ATR
```

**Translation**:
- Take the midpoint of each day's high and low
- Add 2 times volatility upward (upper band)
- Subtract 2 times volatility downward (lower band)
- Whichever band price is above, display that band

### Parameters Used in This Strategy

| Parameter | Value | Plain Explanation |
|-----------|-------|-------------------|
| **ATR Period** | 8 candles | Calculate average volatility over last 8 hours |
| **ATR Multiplier** | 2 times | Band width = 2 times volatility |

**Characteristics**: Period 8 is quite short, fast response; Multiplier 2 is standard, not too sensitive or too slow.

---

## VI. This Strategy's "Personality"

### ✅ Advantages (The Praise)

1. **Minimalist Design**: One indicator, one page of code, understand in five minutes. Perfect starting point for learning quant.
2. **Strong Trend Capture**: When a big trend comes, this strategy eats the whole move.
3. **Solid Risk Control**: Tiered take-profit + trailing stop, knows when to advance and retreat.
4. **High Efficiency**: Can run 100 pairs without breaking a sweat.

### ⚠️ Disadvantages (The Critique)

1. **Ranging Markets Are a Nightmare**: In sideways markets, this strategy gets slapped repeatedly — buy in and it drops below, sell out and it rallies... "Getting hit from both sides."
2. **Slow Entry**: Being a trend indicator, it always waits for the trend to establish before entering — can't catch the head or tail of the fish.
3. **Only One Dimension**: Doesn't look at volume changes, momentum, divergences... What if this line lies to you?
4. **Parameter Sensitive**: Slightly changing ATR period and multiplier can make a huge difference in performance.

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|--------------------|--------|
| **Big Bull Market** | 🚀 Go heavy | Trend strategy heaven, make money while lying down |
| **Ranging Market** | 🛑 Stop using | Getting slapped from both sides, fees will bankrupt you |
| **Bear Market** | 🔕 Stay in cash | No shorting mechanism, just watch |
| **Extreme Volatility** | ⚠️ Light position test | When volatility is high, bands widen, signals decrease |

---

## VIII. Summary: How Good Is This Strategy?

### One-Sentence Verdict
> "The minimalist of the quant world — if one line can solve it, never use two."

### Who Should Use It?
- ✅ Quant beginners (simple code, clear logic)
- ✅ Trend strategy enthusiasts (simplicity is sophistication)
- ✅ Manual traders (clear signals, easy to execute)
- ✅ Low-spec computer users (minimal computation)

### Who Should NOT Use It?
- ❌ Ranging market harvesters (this strategy gives money away in sideways markets)
- ❌ High-frequency traders (1-hour timeframe, too slow)
- ❌ Complex strategy lovers (no fancy stuff here)
- ❌ Those seeking extreme win rates (trend strategies generally have lower win rates)

### My Advice
1. **Understand SuperTrend first**: Learn how this line is derived.
2. **Pick trending coins**: Don't torture yourself with sideways coins.
3. **Add other filters**: Like adding a moving average direction filter to reduce false signals.
4. **Be patient**: Trend strategies need time, don't be impatient.

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Simple to the Extreme

SuperTrendPure is two words: **TREND**.

The code is only 90 lines — what does that mean? Shorter than this article! Its money-making philosophy is:

> "Get on when the trend comes, get off when the trend ends."

- **No bottom fishing**: Wait for the trend to establish before entering
- **No top picking**: Wait for the trend to break before exiting
- **No overthinking**: Clear signals, simple execution

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 **Unilateral Uptrend** | ⭐⭐⭐⭐⭐ | Trend strategy heaven, eat from start to finish |
| 🔄 **Consolidation/Ranging** | ⭐⭐☆☆☆ | Getting slapped repeatedly, buy today sell tomorrow, fees making you cry |
| 📉 **Unilateral Downtrend** | ⭐⭐⭐☆☆ | Stay in cash and watch, no loss but no gain either |
| ⚡️ **Extreme Volatility** | ⭐⭐⭐☆☆ | Bands widen, fewer signals, actually dodged fake breakouts |

**One-Sentence Summary**: **Great in trends, terrible in ranging markets.**

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Commentary |
|--------------------|-------------------|------------|
| Timeframe | 1h or 4h | 15 minutes is too noisy, daily is too slow |
| Number of pairs | Whatever you want | Minimal computation, run as many as you like |
| Coin selection | Trending coins | Don't pick sideways coins, you'll cry |

### 10.2 Hardware Requirements (Important!)

This strategy has minimal computation, almost no hardware requirements:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|--------------------| -----------|
| 1-10 pairs | 1GB | 2GB | Silky smooth |
| 10-50 pairs | 2GB | 4GB | Silky smooth |
| 50+ pairs | 4GB | 8GB | Still silky smooth |

**Warning**: If your computer can't run this strategy, your computer might need to retire... 😅

### 10.3 Backtest vs Live Trading

Because the strategy is simple, backtest and live trading differences are small:
- ✅ No resampling issues (single timeframe)
- ✅ No look-ahead bias (indicator calculation has no forward-looking)
- ⚠️ Main cost is slippage, especially in fast markets

**Recommended Process**:
1. First backtest to select coins (pick trending ones)
2. Run paper trading for 1-2 weeks
3. Small position live trading
4. Confirm stability before increasing position

**Don't go all-in right away** — no matter how simple the strategy, it needs to be proven!

---

## XI. Bonus: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **Built-in SuperTrend function**: Didn't use a third-party library, wrote it from scratch!
   > "Better to rely on yourself than others — self-written is most reliable."

2. **Hardcoded parameters**: ATR period 8, multiplier 2, written directly in the code.
   > "Parameter optimization? Doesn't exist, just use this!"

3. **startup_candle_count = 50**: Only needs 50 candles to start working.
   > "I'm efficient, don't need to look at ancient history."

---

## XII. Final Words

### One-Sentence Verdict
> "The best choice for quant beginners — simple to the extreme, which is sophisticated."

### Who Should Use It?
- ✅ Quant beginners (simple code, clear logic)
- ✅ Trend trading enthusiasts (catch the trend, you win)
- ✅ Manual traders (clear signals, easy to execute)
- ✅ Low-spec computer users (almost no resources needed)

### Who Should NOT Use It?
- ❌ Ranging market harvesters (giving money away in sideways markets)
- ❌ High-frequency traders (too slow)
- ❌ Complex strategy enthusiasts (this strategy has no complexity)
- ❌ Those seeking high win rates (trend strategies have lower win rates)

### Advice for Manual Traders
This strategy is perfect for manual trading:
1. Open TradingView
2. Add SuperTrend indicator (ATR period 8, multiplier 2)
3. Buy when price breaks above upper band, sell when it breaks below lower band
4. Set your stop loss and trailing stop

That's it! No need to stare at charts, no analysis needed, just follow the line.

---

## XIII. ⚠️ Risk Re-emphasis (READ THIS!)

### Backtests Look Great, Live Trading Requires Caution

SuperTrendPure's historical backtests often look good — especially in trending markets. But there's a trap:

> **Trend strategies continuously lose money in ranging markets, and markets are ranging 70% of the time.**

Simply put: **That big trend you're waiting for might take a very, very long time...**

### Hidden Risks of Simple Strategies

In live trading, even simple strategies have pitfalls:
- **Fake breakouts**: Price just breaks out then falls back, classic "bull trap"
- **Slippage costs**: When trend breaks happen, markets are often fast, slippage isn't small
- **Psychological pressure**: Can you stick with it after consecutive stop losses?

### My Honest Advice

```
1. Use this strategy to learn quant first, don't expect to make money right away
2. Pick trending coins (mainstream ones like BTC, ETH)
3. Actively reduce position or pause strategy during ranging periods
4. Don't constantly change parameters — more isn't better, and neither is constant tweaking
```

**Remember**: Simple strategies don't guarantee profits, but simple strategies let you **quickly understand WHY you're making money or losing money** — that's the value of learning! 🙏

---

**Final Reminder**: No matter how good the strategy, when the market teaches you a lesson, it won't give advance notice. Test with small positions, survival comes first!