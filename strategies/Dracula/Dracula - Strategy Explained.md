# Dracula Strategy: The "Blood-Sucking" Philosophy of the Dark Lord

> **Nickname**: The Dark Lord / Bollinger Band Hunter  
> **Occupation**: Specializes in waiting for price to drop to the Bollinger lower band and then "sucking blood" (buying)  
> **Timeframe**: 1 Minute + 5 Minute Informational Layer

---

## 1. What's This Strategy?

Put simply, **Dracula** is a strategy that:
- Waits for price to drop to the Bollinger lower band (aka the "floor price")
- At the same time checks if money is flowing in (CMF > 0)
- Then checks if there's a support level nearby
- If all checks pass, it buys

Think of it like shopping on Taobao: you only buy when there's a "limited-time discount" + "in stock" + "store is still open" 😏

---

## 2. Core Settings: "How Low Will You Buy?"

### Take-Profit Rules (ROI Table)

```
Hold Time       Min Profit      Plain English
--------------------------------------------------
0 minutes       10%             Jumped 10% right away? Run!
30 minutes      5%              Held for half an hour, still up 5%? Could also run
60 minutes      2%              Held for an hour, 2% profit — sell it
```

**Translation**: This strategy sets a pretty high take-profit target right off the bat — 10%! Probably because if price has already dropped to the Bollinger lower band, the bounceback should be significant.

### Stoploss Rules

```
Hard stoploss: -20%
Trailing stop: activates after 1% profit, triggers on 3% pullback from high
```

**Translation**:
- Dropped 20% after buying? Cut your losses, no hesitation!
- Making money? Pull back 3% from the high and run — don't get greedy!

---

## 3. 2 Buy Conditions: Here's the Breakdown

This strategy's buy conditions are pretty complex, so I've grouped them into 2 categories:

### 🎯 Type #1: Lower Band + Money Inflow + Support Confirmation

**Core Logic**: Price just touched the lower Bollinger band, was above support previously, and money is still flowing in

**Plain English**:
> "Wow! Price hit the floor (lower Bollinger band), and money is still pouring in (CMF > 0), there's support ahead holding it up — it won't fall too far. Buy!"

**Key Conditions**:
- `bb_bbl_i == 1`: Price touched lower Bollinger band
- `cmf > 0`: Money inflow (money running into the market)
- `close >= support`: Price not below support
- `lost_protect`: EMA hasn't skyrocketed over the past 10 candles

---

### 🎯 Type #2: Lower Band + Direct Support

**Core Logic**: Price directly dropped to the lower Bollinger band, open price is above support

**Plain English**:
> "Opened above support, and price just touched the lower Bollinger band — perfect!"

**Key Conditions**:
- `bb_bbl_i == 1`: Touched lower band
- `open >= support`: Open price above support
- Other conditions same as Type #1

---

## 4. Protection Mechanism: 1 Layer of "Pitfall Protection"

This strategy has a "stoploss protection" (lost_protect), like adding a fuse for you:

| Protection Type | Effect | Plain English |
|-----------------|--------|----------------|
| lost_protect | Ensures EMA hasn't gone crazy | "Don't catch a falling knife after it's already rallied!" |

How it works: Over the past 10 candles, EMA has never been above 107% of the close price. If EMA has skyrocketed, it means the coin has already rallied a lot — so we stop buying to avoid chasing.

This strategy is pretty cautious — it knows that "chasing leads to death" 😅

---

## 5. Exit Logic: Fancier Than the Buy

Dracula has 5 types of exit scenarios — even more complex than the buy:

### 5.1 Resistance Reversal Exit

```
Trigger Conditions:
- Previous candle broke through upper Bollinger band
- Current candle closes bearish (down)
- Price near resistance level
```
> "Hit resistance and starting to close bearish — run!"

### 5.2 Strong Reversal Exit

```
Trigger Conditions:
- Current candle broke through upper Bollinger band
- Current candle closes bearish
- Open price far from resistance
```
> "Rallied too hard, broke through the upper band — it's gonna pull back, run!"

### 5.3 Trend Reversal Exit

```
Trigger Conditions:
- Current candle closes bearish
- EMA way above close (over 7%)
```
> "EMA has gone wild, price starting to drop — trend is shifting, run!"

### 5.4 Lower Bollinger Band Take-Profit

```
Trigger Conditions:
- Current candle closes bearish
- Price near lower Bollinger band
- Currently has profit
```
> "Dropped back to the lower band again — take the profit and run!"

### 5.5 SMA Signal Exit

```
Trigger Conditions:
- Buy tag contains "sma"
- Profit >= 1%
```
> "Up 1%, SMA signal triggered — run!"

---

## 6. The Strategy's "Personality Traits"

### ✅ Pros (The Praise Section)

1. **Strict conditions**: Must satisfy Bollinger + money flow + support simultaneously — fewer fake signals
2. **Money flow filtering**: CMF > 0 ensures real money inflow, not "fake rally"
3. **Dynamic support/resistance**: Support levels are calculated in real time, not rigid fixed values
4. **Protection mechanism**: Prevents chasing after rallies
5. **Multiple exit scenarios**: 5 different exit methods covering various situations

### ⚠️ Cons (The Rant Section)

1. **Too strict**: Often can't find qualifying trades
2. **1 minute too short**: Candle noise is too high, easy to get fooled by "fake signals"
3. **No trend judgment**: Doesn't check if you're in an uptrend or downtrend — easy to trade against the trend
4. **Parameters hard to tune**: buy_bbt, ewo parameters need careful adjustment

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Uptrend | Can use it | Money flow confirmation catches trends |
| 🔄 Oscillating market | Highly recommended | Bollinger bands work best in ranges |
| 📉 Downtrend | Don't use | No trend filtering, easy to catch a falling knife |
| ⚡️ Low volatility consolidation | Don't use | Bollinger bands narrow, no signals |

---

## 8. Bottom Line: How's This Strategy Really?

### One-Line Verdict
> "A cautious 'buy at the floor' strategy, but conditions are too strict — often can't find opportunities"

### Who It's Good For:
- ✅ Patient people (few signals, need to wait)
- ✅ People who like "buying the dip" (specializes in buying at Bollinger lower band)
- ✅ People who value signal quality (multi-condition confirmation, fewer fake signals)

### Who It's NOT For:
- ❌ People who want frequent trades (conditions too strict, no signals)
- ❌ Beginners (code is complex, hard to understand)
- ❌ People who like chasing rallies (this strategy buys on the way DOWN)

### My Suggestions

1. **Change timeframe from 1m to 5m**: 1-minute candles are too short, too noisy
2. **Add trend filtering**: Add EMA200 trend check — only go long in uptrends
3. **Don't be greedy**: 10% take-profit target is already high — take it when reached
4. **Observe more**: This strategy has few signals, but each one is "carefully selected"

---

## 9. What Markets Does This Strategy Make Money In?

### 9.1 Core Logic: Building a Safety Margin with "Buy the Dip"

Dracula is a classic **mean reversion + money flow confirmation** strategy. Code volume is about 300 lines, including a custom support/resistance calculator — like a small textbook on "quantitative investing" 📚

**Its money-making philosophy**:

- **Price always reverts**: Dropped to the lower Bollinger band, it will bounce back eventually
- **Money flow determinesauthentic vs fake**: Only a bounce with real money inflow is a real bounce
- **Support is the floor**: With support holding, it can't fall much further

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:---|:---:|:---|
| 📈 Uptrend | ⭐⭐⭐⭐☆ | Catches trends but might sell too early |
| 🔄 Oscillating market | ⭐⭐⭐⭐⭐ | This is its home turf! |
| 📉 Downtrend | ⭐⭐☆☆☆ | Support levels may not hold — too many knives |
| ⚡️ Consolidation | ⭐⭐⭐☆☆ | Bollinger bands narrow, not many opportunities |

**One-liner**: Best in oscillating markets — handle other markets as needed!

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Comments |
|-------------|-------------------|----------|
| Number of pairs | 20-40 | Strict conditions, need more coins |
| Max open trades | 3-5 | Few opportunities, but don't over-allocate |
| Timeframe | 5m | STRONGLY recommend changing! 1m is too short |

### 10.2 Key Config Settings

```yaml
# Recommended config
timeframe = "5m"        # Go up a level, don't use 1m
stoploss = -0.20        # Keep default
minimal_roi = {          # Can leave this as is
    "0": 0.10,
    "30": 0.05,
    "60": 0.02
}
```

### 10.3 Hardware Requirements (Important!)

Strategy has moderate computational load, not too demanding on VPS:

| Number of Pairs | Min RAM | Recommended RAM | Experience |
|-----------------|---------|-----------------|------------|
| 20-40 pairs | 512MB | 1GB | Smooth |
| 40-80 pairs | 1GB | 2GB | Decent |

### 10.4 Backtesting vs. Live Trading

**Notes**:
- 1m timeframe may differ between backtesting and live
- Support/resistance levels are dynamically calculated — may have "future function" issues
- Recommend backtesting with 5m or higher timeframe

**Recommended Process**:
1. Backtest first, observe signal frequency
2. Dry-run for 2-4 weeks
3. Small capital live trading for 1 month
4. Scale up only after confirming effectiveness

**Don't go all-in from the start** — even the best strategy needs arun-in period period!

---

## 11. Bonus: The Strategy Author's "Little Tricks"

Looking closely at the code, you'll find some interesting things:

1. **Custom Support/Resistance Calculator**
   > "I wrote the SupResFinder class myself to calculate support and resistance levels!"

2. **CMF Money Flow Indicator**
   > "I just watch where the money flows — a bounce without money inflow is a fake bounce!"

3. **lost_protect Protection**
   > "Want to chase? No way! If EMA goes crazy, I won't buy!"

---

## 12. Last but Not Least

### One-Line Verdict
> "A strict-condition, high-signal-quality 'buy at the floor' strategy — but requires patience to wait"

### Who It's Good For:
- ✅ Patient people
- ✅ People who value signal quality
- ✅ People who can handle low-frequency trading
- ✅ People with some quantitative background

### Who It's NOT For:
- ❌ People who want to trade every day
- ❌ Beginner players
- ❌ People who like chasing rallies and cutting losses quickly

### Manual Trading Tips

For manual trading, you can reference it like this:
- See price drop to the lower Bollinger band
- Open your trading software, check if CMF > 0
- Check if there's a support level ahead
- All three conditions met? Buy!

**Remember**: The core of this strategy is "wait for the floor, then buy" — don't chase rallies!

---

## ⚠️ Final Warning: Risk Re-emphasis (Must Read!)

### Backtesting Looks Great, Live Trading Requires Caution

Dracula's historical backtesting performance looks good — but there are pitfalls:

> **Because support/resistance levels are dynamically calculated, backtesting may use "future data" to calculate past support levels, which inflates backtest results.**

Simply put: **The support levels used in backtesting are actually you "peeking at the future"!**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Fewer signals**: Conditions too strict, often can't find opportunities
- **Parameter sensitivity**: Slight changes in buy_bbt etc. can completely change signals
- **Calculation delay**: Dynamic support/resistance needs real-time calculation, may have delays

### My Suggestions (Sincere Advice)

```
1. Test with 5m timeframe first, don't use 1m
2. Run dry-run for 2-4 weeks, observe signal frequency
3. Small capital live trading for 1 month, scale up after confirming effectiveness
4. Always set stoploss — never gamble!
5. Remember: oscillating markets are its home turf
```

**Remember**: Even the best strategy can't withstand the market teaching you a lesson. Test with small capital — survival is the top priority! 🙏
