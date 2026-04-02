# EMASkipPump Strategy: The "Smart" Strategy That Specifically Avoids "Pumps"

> **Nickname**: Pump Prevention Pro  
> **Occupation**: Detects abnormal trading volume, skips "pump coins," only buys normal coins  
> **Timeframe**: 5 Minutes

---

## 1. What's This Strategy?

Put simply, **EMASkipPump** is specifically designed to **avoid getting scammed by "pumps"**!

Core idea:
- Detect abnormal trading volume (20x 30-period moving average = abnormal "pump")
- Find abnormal = **skip and don't buy**
- Wait for market to return to normal before trading

Like a matchmaking event: **see the date suddenly spend lavishly (abnormal volume) — turn and walk away, this isn't a good person**! 😂

This is a **5-minute level** short-term strategy, specifically for **pump prevention**!

---

## 2. Core Settings: "In and Out Fast"

### Take-Profit Rules (ROI Table)

```
Immediate exit (0 minutes)     → Run when profit reaches 10%!
```

**Translation**: 10% and run! This is a **short-term strategy**, not greedy!

### Stoploss Rules

```
Hard stoploss: -5%
```

**Translation**: -5% is relatively strict, indicating the strategy pursues **high-frequency trading**, cutting losses promptly!

---

## 3. 1 Buy Condition: Multi-Layer Filtering

This strategy's buy condition has **4 sub-conditions** — must satisfy ALL to buy:

### 🎯 Core Buy Condition

| Sub-condition | Requirement | Plain English |
|---------------|-------------|---------------|
| **Volume filter** | < 30-period mean × 20 | "Volume is normal, no pump" |
| **MA alignment** | Price < EMA5 < EMA12 | "Price below MAs, bearish" |
| **Extremum confirmation** | Close = period low | "Buy at the low point" |
| **Bollinger** | Price <= lower band | "Buy at support" |

**Plain English**:
> "Volume normal + price below MAs + buy at the low + touched Bollinger lower band — ALL four conditions met, buy!"

---

## 4. Exit Logic: Buy at Low, Sell at High

### 4.1 Sell Condition

| Sub-condition | Requirement | Plain English |
|---------------|-------------|---------------|
| **MA alignment** | Price > EMA5 > EMA12 | "Price above MAs, bullish" |
| **Extremum confirmation** | Close = period high | "Sell at the high point" |
| **Bollinger** | Price >= upper band | "Sell at resistance" |

**Plain English**:
> "Price rallied above MAs + sell at the high + touched Bollinger upper band — sell!"

### 4.2 Strategy Logic

```
Buy: Bearish alignment + touched support + buy at the low
Sell: Bullish alignment + touched resistance + sell at the high
```

**Plain English**: > "Buy at the low, sell at the high — this is a scalping approach!"

---

## 5. Technical Indicators: What "Weapons" Does This Strategy Use?

| Indicator | Period | Purpose | Plain English |
|-----------|--------|---------|---------------|
| **EMA5** | 5 | Short-term trend | "Average of last 5 candles" |
| **EMA12** | 12 | Medium-term trend | "Average of last 12 candles" |
| **EMA21** | 21 | Long-term trend | "Average of last 21 candles" |
| **Bollinger Bands** | 20, 2 | Volatility boundaries | "Price channel" |
| **MIN/MAX** | 12 | Extremum confirmation | "Period low/high" |

---

## 6. Risk Management: How Does This Strategy Protect Itself?

### 6.1 Pump Protection (Core Feature!)

```python
volume < volume_rolling_mean.shift(1) * 20
```

| Protection | Description |
|------------|-------------|
| **Volume detection** | > 20x 30-period mean = abnormal = skip |
| **Skip pumps** | Find abnormal volume, don't buy, wait for normal |

**Plain English**: > "See volume surge 20x? Must be the whale pumping — get out!"

### 6.2 Strict Stoploss

| Stoploss | Description |
|----------|-------------|
| **Hard stoploss** | -5%, relatively strict |
| **Reason** | Short-term strategy, cut losses promptly |

---

## 7. The Strategy's "Personality Traits"

### ✅ Pros (The Praise Section)

1. **Pump protection**: Specifically designed to avoid buying "pump coins"
2. **MA alignment**: Bullish/bearish alignment confirms trend
3. **Extremum trading**: Buy at period low, sell at period high
4. **Clear logic**: Code is concise, easy to understand
5. **Good for short-term**: 5-minute level, frequent trades

### ⚠️ Cons (The Rant Section)

1. **Counter-trend trading**: Buying when MA is bearish — may catch a falling knife
2. **False breakouts**: Bollinger lower band may be touched frequently
3. **Fixed volume threshold**: 20x may not suit all markets
4. **Needs volatility**: Can't trade without volatility

---

## 8. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 **Trending up** | Use sell condition | Sell in bullish alignment |
| 📉 **Dip bounce** | Use buy condition | Buy at support in bearish alignment |
| 🔄 **Oscillating market** | Reduce trading pairs | Perfect for selling high/buying low |
| ⚡️ **Abnormal volatility** | Skip | Pump protection auto-skips |

---

## 9. Bottom Line: How's This Strategy Really?

### One-Line Verdict
> "A short-term strategy specifically for pump prevention — buy at the low, sell at the high!"

### Who It's Good For:
- ✅ Short-term traders (5-minute level)
- ✅ People who want pump prevention (got burned before)
- ✅ Swing traders (buy at support, sell at resistance)
- ✅ People who like extremum trading

### Who It's NOT For:
- ❌ Long-term investors (timeframe too short)
- ❌ Beginners (counter-trend trading is risky)
- ❌ Trend traders

### My Suggestions

1. **Watch volume**: This is the core pump prevention mechanism
2. **Set stoploss**: -5% is the bottom line
3. **Don't fight the big trend**: Buy less in downtrends
4. **Stick to mainstream coins**: Altcoins have many false signals

---

## 10. What Markets Does This Strategy Make Money In?

### 10.1 Core Logic: Pump Prevention + Extremum Trading

**EMASkipPump's** money-making philosophy: **Not about catching every opportunity, but about avoiding getting scammed by "pumps"!**

- **Pump prevention**: Detect abnormal volume, skip "pump coins"
- **Extremum trading**: Buy at period low, sell at period high
- **MA alignment**: Confirm trend direction

### 10.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:---|:---:|:---|
| 📈 Trending up | ⭐⭐⭐⭐☆ | Sell in bullish alignment, can make some money |
| 📉 Dip bounce | ⭐⭐⭐⭐☆ | Buy in bearish alignment, buy at the low |
| 🔄 Oscillating market | ⭐⭐⭐⭐⭐ | Perfect for selling high/buying low! |
| ⚡️ Abnormal volatility | ⭐⭐⭐⭐⭐ | Auto-skips pumps, safe! |

**One-liner**: Oscillating market god, abnormal volatility guardian 😎

---

## 11. Want to Run This Strategy? Check These Configs First

### 11.1 Trading Pair Configuration

| Config Item | Recommended Value | Comments |
|-------------|-------------------|----------|
| Number of pairs | 10-20 | Can open more |
| Mainstream coins only | BTC/ETH | Altcoins have many false signals |
| Timeframe | 5 minutes | Don't change |

### 11.2 Key Config Settings

```yaml
# Recommended config
EMA_SHORT_TERM: 5
EMA_MEDIUM_TERM: 12
EMA_LONG_TERM: 21

minimal_roi:
  "0": 0.10

stoploss: -0.05
```

### 11.3 Hardware Requirements

This strategy has extremely low computational load, no hardware demands:

| Number of Pairs | Min RAM | Recommended RAM |
|----------------|---------|-----------------|
| 10-20 pairs | 1 GB | 2 GB |
| 50+ pairs | 2 GB | 4 GB |

### 11.4 Backtesting vs. Live Trading

Backtesting looks great, live trading fails because:
1. **Counter-trend buying**: Buy in bearish MA — get trapped
2. **False breakout**: Bollinger lower band touched frequently
3. **Volume threshold**: 20x may not suit all coins

**Recommended Process**:
1. Backtest for 3 months
2. Dry-run for 2 weeks
3. Small capital live trading for 1 month
4. Scale up only if no issues

---

## 12. Bonus: The Strategy Author's "Little Tricks"

1. **EMASkipPump name**: Skip = skip, Pump = pump — the author must have been burned by pumps!
2. **20x threshold**: The author must have tested extensively, this value is most reasonable
3. **-5% stoploss**: Relatively strict — the author is risk-averse
4. **5/12/21 EMA**: Fibonacci numbers — there's some magic to it!

---

## ⚠️ Final Warning: Risk Re-emphasis (Must Read!)

### Backtesting Looks Great, Live Trading Requires Caution

**EMASkipPump's** historical backtesting performance often looks **very good** — but there's a trap:

> **Counter-trend trading = catching a falling knife! Buying when MA is bearish may mean buying on the way down!**

Simply put: **Buying at the low point isn't always good — it might be a falling continuation!**

### Simple Strategy Risks

In live trading, simple logic may cause:
- **Counter-trend traps**: Buy in bearish MA, keeps falling
- **False breakout**: Bollinger lower band touched frequently
- **Fixed volume threshold**: 20x may not suit all markets

### My Suggestions (Sincere Advice)

```
1. Don't fight the big trend: Buy less in downtrends
2. Watch volume: This is the core pump prevention mechanism
3. Set stoploss: -5% is the bottom line
4. Diversify investments: Don't put all money on one coin
```

**Remember**: Pump prevention is good, but counter-trend trading can blow up! 🙏

---

**Final Reminder**: No matter how good the strategy, the market won't hesitate to teach you a lesson. Test with small capital — survival is the top priority! 🙏
