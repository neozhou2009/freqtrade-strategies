# TEMA Strategy: Fast Gun's Bollinger Band Dance

> **Nickname**: The Flash  
> **Job**: High-Frequency Trend Hunter, feeds on short-term volatility  
> **Timeframe**: 1 Minute (Fast as lightning)

---

## 1. What Is This Strategy?

Simply put, **TEMA** is:
- Fast: Uses triple exponential moving average, responds twice as fast as regular MAs
- Simple: Buy/sell conditions are just 3 each, easy to understand at a glance
- High-Frequency: 1-minute timeframe, can trade multiple times a day

Like **The Flash doing Tai Chi**, moves too fast to see, but the techniques are simple and direct. 🤣

TEMA stands for Triple Exponential Moving Average, sounds fancy, but it's just "a faster moving average."

---

## 2. Core Config: Basically "Take Profits While You Can"

### Take-Profit Rules (ROI Table)

```
Just bought      → Sell at 4%
Wait 30 minutes  → Sell at 2%
Wait 60 minutes  → Sell at 1%
```

**Translation**:
> "Make money early! Just got in, 4% profit and I'm out. The longer you wait, the lower the take-profit. Time is money, don't be greedy!"

This design is clever: **Short-term strategies need to be quick in and out**, dragging on gets you trapped.

### Stop-Loss Rules

```
Fixed Stop-Loss: -10%
Trailing Stop: Enabled
```

**Translation**:
> "Lose 10% and I fold, but when making money I follow the trend. Winner's mindset: small losses, big wins, let profits run."

---

## 3. One Buy Condition: TEMA Crosses Bollinger Band

The buy condition has one core concept, but verified in 3 steps:

### 🎯 Buy Condition Breakdown

```python
Buy Signal:
1. TEMA below Bollinger Band middle band (cheap zone)
2. TEMA rising (trend starting)
3. Has volume (not a data glitch)
```

**Plain English**:
> "TEMA is below the Bollinger Band middle band (price is cheap), then starts going up (trend starting), and there's volume (not a fake breakout), then buy!"

**Classic Line**:
```
TEMA <= Bollinger Band middle band?
AND TEMA rising?
AND Volume > 0?
→ BUY!
```
> "Price is cheap, trend going up, people are trading, go!"

---

## 4. Sell Logic: Symmetrical Operation

Sell is completely symmetrical to buy, like looking in a mirror:

### 4.1 Sell Condition Breakdown

```python
Sell Signal:
1. TEMA above Bollinger Band middle band (expensive)
2. TEMA falling (trend reversing)
3. Has volume
```

**Plain English**:
```
TEMA > Bollinger Band middle band?
AND TEMA falling?
AND Volume > 0?
→ SELL!
```
> "Price is expensive, trend going down, run!"

### 4.2 This Logic Has a Characteristic

**Simple Symmetry**: Buy and sell conditions are exact opposites:
- Buy: TEMA below middle band, going up
- Sell: TEMA above middle band, going down

No fancy multi-condition nonsense, just these 3.

---

## 5. What the Heck is TEMA?

### 5.1 Regular Moving Average Problems

SMA (Simple Moving Average): Too slow, price already ran away before it reacts
EMA (Exponential Moving Average): A bit faster, but still has some lag

**TEMA's Solution**:
> "I calculate EMA three times, eliminating all the lag!"

### 5.2 TEMA's Secret

```
TEMA = 3×EMA - 3×EMA(EMA) + EMA(EMA(EMA))
```

**Plain English**:
> "First EMA eliminates some lag, second eliminates more, third eliminates it completely!"

**Result**: TEMA is twice as fast as EMA, detects trend changes earlier.

### 5.3 TEMA Trade-offs

| MA Type | Response Speed | Noise |
|---------|---------------|-------|
| SMA | Slow | Low |
| EMA | Medium | Medium |
| **TEMA** | **The Flash** | High |

**Translation**: TEMA responds fast, but gets faked out by small fluctuations. That's why the strategy adds Bollinger Band middle band to filter false signals.

---

## 6. Strategy "Personality"

### ✅ Pros (Praise Section)

1. **Super Fast Response**: TEMA is twice as fast as regular MAs, catches trends just as they start
2. **Super Simple Logic**: Buy/sell are 3 conditions each, elementary schoolers can understand
3. **Adjustable Parameters**: RSI buy/sell thresholds can be auto-optimized
4. **Tiered Take-Profit**: Not greedy, take profits while you can

### ⚠️ Cons (Roast Section)

1. **Too Fast**: 1-minute timeframe, high trade frequency, fees eat a lot of profit
2. **Many False Signals**: Short-term volatility is high, TEMA gets faked out easily
3. **Calculated but Unused**: Code calculates a bunch of indicators (ADX, MACD, MFI, etc.) but trading signals don't use them
4. **No Trend Filter**: Gets trapped frequently in ranging markets, no filter for trend direction

---

## 7. Applicable Scenarios: When to Use?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ Use it! | TEMA follows quickly, Bollinger confirms entries |
| 📉 Clear Downtrend | ⭐⭐⭐⭐☆ Use it | Equally effective, but can only make money long |
| 📊 Volatile Trend | ⭐⭐⭐⭐☆ Can use | Trends within volatility can be caught |
| 🔄 Sideways Range | ⭐⭐☆☆☆ Use cautiously | Frequent false breakouts, stop-losses hit like crazy |

---

## 8. Summary: How's This Strategy Really?

### One-Liner Review
> "Fast and accurate short-term master, but fees and false signals are its two nemeses."

### Who Should Use It?
- ✅ High-frequency trading enthusiasts
- ✅ People who like simple logic
- ✅ Trending market players
- ✅ People with time to watch charts

### Who Shouldn't Use It?
- ❌ Office workers who can't watch charts
- ❌ Long-term only traders
- ❌ People who hate frequent trading
- ❌ High-fee exchanges

### My Suggestions
1. **Switch to 5-minute**: 1-minute is too exhausting, 5-minute is more stable
2. **Add trend filter**: Pair with ADX or larger timeframe MA, don't use in ranging markets
3. **Watch the fees**: High-frequency trading, fees are a big chunk
4. **Light position testing**: Test with small positions first, don't go heavy right away

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Fast Gun Trend Follower

TEMA is a **trend following strategy**. Its money-making philosophy:

> "When trend starts I follow, when trend reverses I run fast."

- **Fast Response**: TEMA is faster than EMA, detects trends earlier
- **Middle Band Confirmation**: Bollinger Band middle band as cheap/expensive divider
- **Tiered Take-Profit**: Not greedy, take profits and run

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:------------------|:---------------------------|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | TEMA follows fast, Bollinger confirms entries, making money like crazy |
| 📉 Downtrend | ⭐⭐⭐⭐☆ | Equally effective, but can only long, shorting relies on sell signals |
| 📊 Volatile Trend | ⭐⭐⭐⭐☆ | Small trends within volatility can be caught |
| 🔄 Sideways Range | ⭐⭐☆☆☆ | Slapped left and right, stop-losses hit like crazy |

**One-Liner Summary**: Fast gun in trending markets,韭菜 in ranging markets.

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config | Recommended Value | Notes |
|--------|------------------|-------|
| Timeframe | 5m (recommended) | 1m is too tiring, 5m is more stable |
| Trading Pairs | Trending coins | Don't pick those zombie coins sideways for months |
| Fees | Lower the better | High-frequency trading fees are huge |

### 10.2 Hardware Requirements

This is a high-frequency strategy, has resource requirements:

| Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|--------------|----------------|-------------------|------------|
| 1-10 pairs | 4GB | 8GB | A bit laggy |
| 10-50 pairs | 8GB | 16GB | Okay |

**Warning**: 1-minute timeframe, large data processing, old computers may lag! 😅

### 10.3 Backtesting vs Live Trading

**Backtesting Notes**:
- Need enough historical data (at least a few months)
- Remember to calculate fees
- High-frequency strategy backtest results are often optimistic

**Live Trading Challenges**:
- 1-minute timeframe, network latency matters
- High-frequency trading, slippage accumulates
- Exchange API rate limits

**Recommended Process**:
1. Switch to 5-minute timeframe first
2. Test with trending coins
3. Paper trade for 1-2 weeks
4. Confirm stable before live

---

## 11. Bonus: Strategy Author's "Little Secrets"

Looking at the code, found some interesting things:

1. **Calculated a bunch of unused indicators**: ADX, MACD, MFI, SAR, Stochastic, Hilbert Transform...
   > "I calculated all of these, but trading signals only use TEMA and Bollinger, you guys figure out the rest~"

2. **RSI parameters are optimizable**: `buy_rsi = IntParameter(10, 40, default=30)`
   > "I didn't use RSI parameters, but you can tune them with Hyperopt yourself"

3. **This is an official template**: Comments say "This is a strategy template to get you started"
   > "This isn't the final version, it's a template for you to learn, modify it yourself!"

4. **Candlestick patterns all commented out**: Hammer, Doji, Engulfing... all commented out
   > "These candlestick patterns I didn't use, you can uncomment and try them"

---

## 12. Final Words

### One-Liner Review
> "Fast is fast, but high-frequency is a double-edged sword—use it well it's a money machine, use it poorly it's a fee contributor."

### Who Should Use It?
- ✅ High-frequency trading enthusiasts
- ✅ Trending market players
- ✅ People who like simple logic
- ✅ People with time to watch charts

### Who Shouldn't Use It?
- ❌ Ranging market traders
- ❌ Long-term investors
- ❌ People who hate frequent trading
- ❌ High-fee exchange users

### Manual Trader Suggestions
TEMA can be used manually:
- Add TEMA indicator to TradingView (or use 3×EMA - 3×EMA(EMA) + EMA(EMA(EMA)))
- Overlay Bollinger Bands
- Watch for TEMA crosses with BB middle band
- Confirm with volume

---

## 13. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting Is Beautiful, Live Trading Needs Caution

TEMA's historical backtest may perform well—but high-frequency strategies have big pitfalls:

> **Fees and slippage can eat half your profits. High-frequency isn't that easy.**

Simply put: **Backtesting doesn't count fees, live trading fees are hard costs.**

### Hidden Risks of High-Frequency Strategies

In live trading watch out for:
- **Network Latency**: 1-minute timeframe, a few seconds delay might miss signals
- **Slippage Accumulation**: Frequent trading, slippage accumulates scarily
- **API Rate Limits**: Exchanges limit your request frequency
- **Data Anomalies**: Real-time data may have gaps

### My Advice (Heart-to-Heart)

```
1. Switch to 5-minute timeframe: Reduce trade frequency, lower fee impact
2. Add trend filter: Pair with ADX or daily MA, don't use in ranging markets
3. Choose low-fee exchanges: High-frequency trading fees are huge
4. Light position testing: Verify with small positions first, don't go all-in
```

**Remember**: Fast gun may look cool, but if you can't hit straight, bullets (fees) run out fast!

---

**Final Reminder**: No matter how simple the strategy, the market is boss. In trending markets it's a fast gun, in ranging markets it's 韭菜. Choose the right battlefield to make money! 🙏