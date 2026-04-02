# EMA_CROSSOVER Strategy: The Most Classic "MA Crossover"

> **Nickname**: Classic MA Crossover / Freqtrade Sample Strategy  
> **Occupation**: Buys when short-term MA crosses above long-term MA, sells when it crosses below  
> **Timeframe**: 5 Minutes

---

## 1. What's This Strategy?

Put simply, **EMA_CROSSOVER** is the **most classic MA crossover strategy**, and one of Freqtrade's **sample strategies**!

Core logic:
- EMA10 (short-term) crosses above EMA100 (medium-term) → Buy
- EMA100 crosses above EMA10 → Sell
- That's it!

Like a straightforward guy at a matchmaking event: **She nods (short-term MA above) = chase, she shakes her head (long-term MA above) = run** — no hesitation! 😂

This is a **5-minute level** short-term strategy, targeting **small-profit quick accumulation**!

---

## 2. Core Settings: "Accumulate Small Profits Quickly"

### Take-Profit Rules (ROI Table)

```
Immediate exit (0 minutes)     → Run when profit reaches 4%!
After 30 minutes               → Run when profit reaches 2%!
After 60 minutes               → Run when profit reaches 1%!
```

**Translation**: This strategy isn't greedy! 4%, 2%, 1% — **accumulate small profits quickly**!

### Stoploss Rules

```
Hard stoploss: -10%
Trailing stop: Not enabled
```

**Translation**: -10% is relatively strict — cut losses promptly! Because the strategy pursues small profits, can't afford big losses!

---

## 3. 1 Buy Condition: EMA10 Crosses Above EMA100

This strategy's buy condition is painfully simple:

### 🎯 Core Buy Condition

| Condition | Requirement | Plain English |
|-----------|-------------|---------------|
| **EMA crossover** | EMA10 crosses above EMA100 | "Short-term MA crossed above long-term MA — golden cross!" |

**Plain English**:
> "The 10-day MA crossed above the 100-day MA — short-term trend turned bullish, buy!"

---

## 4. Exit Logic: Painfully Simple

### 4.1 Sell Condition: EMA100 Crosses Above EMA10

| Trigger Condition | Plain English |
|------------------|---------------|
| EMA100 crosses from below to above EMA10 | "Death cross — trend turned bearish, run!" |

### 4.2 ROI Table Exit

```
[0, 30) minutes     → Run when profit reaches 4%!
[30, 60) minutes   → Run when profit reaches 2%!
[60, ∞) minutes    → Run when profit reaches 1%!
```

**Plain English**: > "Lower expectations over time — quickly accumulate small profits!"

---

## 5. Technical Indicators: What "Weapons" Does This Strategy Use?

| Indicator | Period | Purpose | Plain English |
|-----------|--------|---------|---------------|
| **EMA10** | 10 | Short-term EMA | "Average of last 10 candles" |
| **EMA100** | 100 | Medium-term EMA | "Average of last 100 candles" |
| **EMA1000** | 1000 | Long-term EMA | "Average of last 1000 candles (reference only)" |

**Note**: EMA1000 is only for reference — it doesn't participate in buy/sell conditions!

---

## 6. Risk Management: How Does This Strategy Protect Itself?

### 6.1 Low ROI Target

| Time | Profit Target | Notes |
|------|---------------|-------|
| 0 minutes | 4% | Initial target |
| 30 minutes | 2% | Medium target |
| 60 minutes | 1% | Initial target |

**Design Philosophy**: Lower expectations over time — **quickly accumulate small profits**!

### 6.2 Strict Stoploss

| Stoploss | Notes |
|----------|-------|
| **Hard stoploss** | -10%, relatively strict |
| **Reason** | Strategy pursues small profits, can't afford big losses |

---

## 7. The Strategy's "Personality Traits"

### ✅ Pros (The Praise Section)

1. **Extremely simple logic**: Only uses EMA crossover, code is concise
2. **Small target easy to achieve**: 4% is easier than 50%
3. **Great for beginners**: Logic is clear, easy to understand
4. **Highly extensible**: Can add other indicators
5. **Freqtrade sample strategy**: Officially verified

### ⚠️ Cons (The Rant Section)

1. **No volume confirmation**: May produce false signals
2. **No trend filtering**: Doesn't judge major trend direction
3. **No trailing stop**: Trailing mechanism not enabled
4. **Many false signals**: EMA crossover frequent, many false signals

---

## 8. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 **Trending up** | Use freely | Golden cross = buy signal! |
| 📉 **Dip bounce** | Use buy condition | Bounce also profitable |
| 🔄 **Oscillating market** | Reduce trading pairs | Crossovers frequent, filter carefully |
| 😐 **Consolidation** | Don't use | Too many false signals |

---

## 9. Bottom Line: How's This Strategy Really?

### One-Line Verdict
> "The most classic MA crossover strategy — Freqtrade sample strategy, best for beginners!"

### Who It's Good For:
- ✅ Beginners (logic simple, easy to understand)
- ✅ Short-term traders (5-minute level)
- ✅ People pursuing small profits (4% target easy to achieve)
- ✅ People who want to extend strategies (can add indicators)

### Who It's NOT For:
- ❌ Long-term investors (timeframe too short)
- ❌ People pursuing big profits (target only 4%)
- ❌ People who don't want frequent trading

### My Suggestions

1. **Add volume confirmation**: Can reduce false signals
2. **Set stoploss**: -10% is the bottom line
3. **Don't be greedy**: Run at 4%, accumulate small profits
4. **Stick to mainstream coins**: Altcoins have many false signals

---

## 10. What Markets Does This Strategy Make Money In?

### 10.1 Core Logic: Judging Trends with MA Crossover

**EMA_CROSSOVER's** money-making philosophy: **Short-term MA above = long, long-term MA above = short!**

- **Golden cross**: EMA10 crosses above EMA100 = short-term trend turning bullish
- **Death cross**: EMA100 crosses above EMA10 = short-term trend turning bearish

### 10.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:---|:---:|:---|
| 📈 Trending up | ⭐⭐⭐⭐⭐ | Golden cross confirms trend, buy and hold |
| 📉 Dip bounce | ⭐⭐⭐⭐☆ | Bounce also profitable, but be careful |
| 🔄 Oscillating market | ⭐⭐☆☆☆ | Crossovers frequent, many false signals |
| 😐 Consolidation | ⭐☆☆☆☆ | Too many false signals, bleed out |

**One-liner**: Decent in trending markets, trash in oscillating markets 😎

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
ema10: 10
ema100: 100

minimal_roi:
  "0": 0.04
  "30": 0.02
  "60": 0.01

stoploss: -0.10
trailing_stop: false
```

### 11.3 Hardware Requirements

This strategy has extremely low computational load, no hardware demands:

| Number of Pairs | Min RAM | Recommended RAM |
|----------------|---------|-----------------|
| 10-20 pairs | 1 GB | 2 GB |
| 50+ pairs | 2 GB | 4 GB |

**Advantage**: Runs on old VPS!

### 11.4 Backtesting vs. Live Trading

Backtesting looks great, live trading fails because:
1. **False signals**: MA crosses back quickly after crossing
2. **No volume confirmation**: Too many false breakouts
3. **Slippage**: Live slippage can cause losses

**Recommended Process**:
1. Backtest for 3 months
2. Dry-run for 2 weeks
3. Small capital live trading for 1 month
4. Scale up only if no issues

---

## 12. Bonus: The Strategy Author's "Little Tricks"

1. **EMA10 + EMA100**: Classic short + medium combination!
2. **4% initial target**: The author knows small targets are easier to achieve
3. **-10% stoploss**: Strict stoploss protects capital
4. **Freqtrade sample**: This is an official sample strategy — must have been tested!

---

## ⚠️ Final Warning: Risk Re-emphasis (Must Read!)

### Backtesting Looks Great, Live Trading Requires Caution

**EMA_CROSSOVER's** historical backtesting performance often looks **very good** — but there's a trap:

> **MA crossover has many false signals — without volume confirmation = easily fooled by "false breakouts"!**

Simply put: **Short-term MA fluctuates frequently = many signals = many false signals!**

### Simple Strategy Risks

In live trading, simple logic may cause:
- **False signals**: Cross but crosses back quickly
- **Frequent trading**: Too many signals, fees eat profits
- **Consecutive losses**: Gets whipsawed multiple times in oscillating markets

### My Suggestions (Sincere Advice)

```
1. Add volume confirmation: Reduce false signals
2. Set stoploss: -10% is the bottom line
3. Don't be greedy: Run at 4%, accumulate small profits
4. Diversify investments: Don't put all money on one strategy
```

**Remember**: Simple = easy to understand ≠ easy to profit! More signals = more trades = more fees! 🙏

---

**Final Reminder**: No matter how good the strategy, the market won't hesitate to teach you a lesson. Test with small capital — survival is the top priority! 🙏
