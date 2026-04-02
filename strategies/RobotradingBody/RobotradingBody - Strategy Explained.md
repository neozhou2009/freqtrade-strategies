# RobotradingBody Strategy: The Minimalist's Bottom-Fishing Godsend

> **Nicknames**: Bottom-Fishing Maniac, One Candle Decides Everything  
> **Profession**: Reversal Trader  
> **Timeframe**: 4 hours (4h)

---

## 1. What Is This Strategy?

Simply put, **RobotradingBody** is a strategy that:
- Only looks at candlestick bodies — ultra-minimalist
- Buy on large bearish candles, sell on bullish candles
- Less than 100 lines of code, so simple it makes you doubt life

Like a robot that only knows two sentences: "Big drop? Buy! Went up a bit? Run!" 🤖

---

## 2. Core Configuration: "Bottom-Fish and Wait for Rebound"

### Take-Profit Rules (ROI Table)

```
Profit ≥ 90% → Take profit
```

**Translation**: Don't be scared by 90% — this is basically decoration. In actual operation, you sell when a bullish candle appears. Hitting 90%? Hmm, maybe that happens a few times in a lifetime 😅

### Stop-Loss Rules

```
Loss ≥ 10% → Stop-loss
```

**Translation**: Admit defeat at 10% loss. Gives the strategy some breathing room, won't get shaken out by small fluctuations.

### Buy Rules

```
Bearish candle + Body larger than historical mean × 3 → Buy
```

**Translation**: This bearish candle is way bigger than usual? Buy it!

### Sell Rules

```
Bullish candle → Sell
```

**Translation**: Went up a bit, run! Don't be greedy!

---

## 3. 1 Buy Condition: Ridiculously Simple

This strategy's buy condition can be explained in one sentence:

### 🎯 Bottom-Fish on Large Bearish Candles

**Core Logic**: Spot an abnormally large bearish candle (declining candle), rush in to bottom-fish.

**In Plain English**:
> "This bearish candle is several times bigger than usual — definitely oversold, rebound's coming, buy!"

**Specific Conditions**:
```python
# Open > Close → Bearish candle
# Body size > Historical average body × 3 → Large bearish candle
# Volume > 0 → Normal data
```

**Translation**:
> "Close price lower than open (bearish), and this candle is extra thick and long — three times bigger than usual... this is the perfect time to bottom-fish!"

---

## 4. Protection Mechanisms: 2 Layers of "Insurance"

Although the buy condition is simple, the strategy still comes with two layers of protection:

| Protection Type | Function | In Plain English |
|----------------|----------|------------------|
| Fixed Stop-Loss | Run when loss exceeds 10% | "Admit defeat at 10%, don't hold stubbornly" |
| ROI Target | Take profit at 90% | "Satisfied with 90%... though you'll basically never see it" |

**Complaint**: Honestly, this strategy's core protection isn't these parameters — it's the "quick in, quick out" style. Sell on any bullish candle, doesn't give you much chance to lose big 🤣

---

## 5. Sell Logic: Even Simpler Than Buying

### 5.1 Sell Conditions

```
Bullish candle → Sell
```

**In Plain English**:
- Sell immediately when any bullish candle appears (close higher than open)
- Doesn't need a large bullish candle, doesn't need limit up — any bullish candle triggers

**Subtext**:
> "Bottom-fished successfully, went up a bit — run fast, cash out!"

### 5.2 Logic Behind This Design

| Scenario | Result | In Plain English |
|----------|--------|------------------|
| Bottom-fish succeeds | Bullish candle appears, small profit exit | "Take small profit and run, don't be greedy" |
| Continues falling | Wait for stop-loss or next large bearish candle | "Might have caught the middle of the mountain" |
| Big rebound | Miss big gains | "Sold too early... but at least made money" |

---

### 5.3 Exit Method Summary

| Method | Trigger Condition | In Plain English |
|--------|------------------|------------------|
| Signal Sell | Bullish candle appears | "Run when it goes up" |
| Stop-Loss | Loss 10% | "Too much loss, admit defeat" |
| ROI Take-Profit | Profit 90% | "Dreams are beautiful..." |

---

## 6. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Session)

1. **Ridiculously Simple Code**: Less than 100 lines, even elementary students can understand
2. **Straightforward Logic**: Large bearish candle = buy, bullish candle = sell, what else needs explaining?
3. **Fast Calculation**: No complex indicators, computer runs lightning fast
4. **Optimizable Parameters**: Two parameters can be optimized, find the best configuration

### ⚠️ Weaknesses (Complaint Session)

1. **Easy to catch mid-mountain**: Large bearish candles can be followed by even larger ones
2. **Sells too early**: Run on any bullish candle, might miss big gains
3. **No trend judgment**: May repeatedly bottom-fish and get slapped in downtrends
4. **Too simple signals**: Just one candle's decision, reliability is questionable

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| High-Volatility Ranging | ✅ Recommended | Frequent rebounds after large bearish candles, perfect match |
| Rebound After Crash | ✅ Can use | Might catch the real bottom |
| One-Way Downtrend | ⚠️ Caution | May catch mid-mountain, consecutive stop-outs |
| One-Way Uptrend | ❌ Not Recommended | No buy opportunities, just waiting around |
| Low-Volatility Sideways | ❌ Don't use | No large bearish candles, strategy basically sleeps |

---

## 8. Summary: How Is This Strategy Really?

### One-Sentence Review
> "The minimalist's bottom-fishing godsend, but so simple it makes you nervous."

### Who Should Use It?
- ✅ Quant beginners wanting to learn strategy development
- ✅ Traders who like simple logic
- ✅ Players with time to optimize parameters
- ✅ Those who want to use it as a framework for modifications

### Who Should NOT Use It?
- ❌ Those pursuing complex multi-factor strategies
- ❌ Warriors wanting to bottom-fish in one-way downtrends
- ❌ Conservatives expecting stable profits
- ❌ Those who don't like stop-losses

### My Recommendations
1. **Backtest first**: Verify performance on different instruments
2. **Then optimize**: Two parameters can find optimal combination
3. **Add filters**: Consider adding a trend indicator to avoid counter-trend bottom-fishing
4. **Don't go all-in**: Light positions for testing — simple strategy doesn't mean no risk

---

## 9. In What Markets Can This Strategy Make Money?

### 9.1 Core Logic: Trading Simplicity for Certainty

RobotradingBody is the "minimalist" of the quant world. 80+ lines of code — what does that mean? A proper strategy starts at 200 lines minimum, this isn't even half!

**Its profit philosophy**: Simplicity is beauty, bottom-fishing must be fast

- **Simple Logic**: Large bearish candle = buy, bullish candle = sell, no complications
- **Fast Execution**: No complex calculations, execute immediately on signal
- **Optimizable**: Two parameters can be tuned, find the best combination

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 One-Way Uptrend | ⭐⭐☆☆☆ | No buy opportunities, strategy basically lies flat |
| 🔄 High-Volatility Ranging | ⭐⭐⭐⭐⭐ | Frequent bottom-fishing rebounds, strategy flies high |
| 📉 One-Way Downtrend | ⭐☆☆☆☆ | Catches mid-mountain, consecutive face-slaps |
| ⚡️ Low-Volatility Sideways | ⭐⭐☆☆☆ | No large bearish candle signals, strategy has no work |

**One-Sentence Summary**: Ranging markets are its home turf, downtrends are its nightmare.

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|------------------|---------|
| Timeframe | 4h or 1d | Original design is 4h, don't change to 5 minutes to die |
| Trading Pairs | High-volatility instruments | Pick those that often surge/plunge, don't pick stablecoins |

### 10.2 Key Settings in Config File

```yaml
# Parameter Optimization Suggestions
for_mult: 2-4        # Don't make multiplier too big, or no signals
for_sma_length: 50-150  # Medium period is most stable

# Risk Control
stoploss: -0.10      # Can adjust to -0.08 to reduce losses
minimal_roi: 0.5     # Can lower to 50%, don't expect 90%
```

### 10.3 Hardware Requirements (Important!)

This strategy's calculation volume is touchingly small:

| Number of Trading Pairs | Minimum RAM | Recommended RAM | Experience |
|------------------------|-------------|-----------------|------------|
| 1-50 pairs | 512MB | 1GB | Silky smooth |
| 50-100 pairs | 1GB | 2GB | Still silky smooth |
| 100+ pairs | 2GB | 4GB | Still silky smooth |

**Complaint**: This strategy's hardware requirements are low as dust — you can run it on a Raspberry Pi 😅

### 10.4 Backtesting vs Live Trading

**Backtesting results** may look great, but here are some pitfalls:
- Slippage and fees will eat small profits
- 90% ROI basically never triggers
- Candle confirmation has delays in live trading

**Recommended Process**:
1. Backtest first to verify logic
2. Test with different timeframes
3. Optimize the two parameters
4. Run on demo account first
5. Small capital live testing

**Don't go all-in immediately** — even the simplest strategy needs磨合!

---

## 11. Easter Egg: The Strategy Author's "Little Thoughts"

Look carefully at the code and you'll find some interesting things:

1. **Minimalist to the Extreme**: Even comments are rare, code is clean and crisp
   > "If I can write 1 line, I won't write 2 — minimalist self-cultivation"

2. **Optimizable Parameters**: Both parameters leave room for optimization
   > "Strategy is simple, tune the parameters slowly — there's always one that fits you"

3. **ROI Set at 90%**: Looks scary, actually just decoration
   > "Anyway we sell on bullish candles, what's the difference between 90% and 900%?"

4. **From TradingView**: Originally a public script ported over
   > "Share the good stuff, long live open source spirit"

---

## 12. Last But Not Least

### One-Sentence Review
> "So simple it makes you doubt life, but sometimes simple is best."

### Who Should Use It?
- ✅ Quant beginners wanting to learn strategy logic
- ✅ Minimalists who like clean code
- ✅ Players with time to tune parameters
- ✅ Developers who want to use it as a modification framework

### Who Should NOT Use It?
- ❌ Those pursuing complex strategies
- ❌ Conservatives who don't like frequent stop-outs
- ❌ Lazy people expecting passive income
- ❌ Warriors wanting to bottom-fish in downtrends

### Manual Trader Recommendations
If you want to use this strategy's logic for manual trading:
1. Watch 4-hour or daily charts
2. Wait for an abnormally large bearish candle
3. Buy, set 10% stop-loss
4. Sell when bullish candle appears
5. Don't be greedy, cash out

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtesting Looks Great, Be Cautious in Live Trading

RobotradingBody looks simple and effective, but has several hidden risks:

> **Simple strategy means thin logic. Buying on one large bearish candle might catch you mid-mountain.**

Simply put: **Easy to bottom-fish mid-mountain, rebound might just bounce once then continue falling.**

### Hidden Risks of Simple Strategies

In live trading, simple logic can lead to:
- **Too frequent signals**: Large bearish candles happen often, may open positions frequently
- **Many false breakouts**: Bottom-fishing might just be catching mid-mountain
- **Selling too early**: Run on any bullish candle, miss big gains
- **No filtering**: Buys in any situation, doesn't care if it's a downtrend

### My Recommendations (Honest Truth)

```
1. Add a trend filter first, avoid counter-trend bottom-fishing
2. Can reduce stop-loss a bit, like -8%
3. Can add large bullish candle judgment to sell conditions, don't run on small gains
4. Test multiple instruments and timeframes during backtesting
5. Run on demo account before live trading
```

**Remember**: The simpler the strategy, the more careful you need to be about its flaws. Simple doesn't equal guaranteed profit — bottom-fishing is a skill!

---

**Final Reminder**: The market will never follow your script — catching mid-mountain is normal. Light positions for testing, staying alive is most important! 🙏

---
