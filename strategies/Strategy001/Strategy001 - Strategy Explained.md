# Strategy001: EMA Beginner's First Lesson

> **Nickname**: "The Moving Average Crossover Master"  
> **Profession**: Trend Following Novice Guide  
> **Timeframe**: 5 minutes

---

## I. What Is This Strategy?

Simply put, **Strategy001** is:
- An entry-level strategy using EMA moving averages to determine trend direction
- Combined with Heikin Ashi candlesticks to filter false signals
- Equipped with trailing stop for automatic protection

Like a **driving school practice car** 🚗 — simple, safe, easy to learn. Master it before driving a sports car!

---

## II. Core Configuration: "Take Profits and Run"

### Take Profit Rules (ROI Table)

```
Holding Time    Target Profit
────────────────────
Immediate       5%
20 minutes      4%
30 minutes      3%
60 minutes      1%
```

**Translation**: Make 5% right after entering? Run immediately! The longer you hold, the lower the target. Time is money's enemy 💰

### Stop Loss Rules

```
Fixed Stop Loss: -10% (Lose 10% and surrender)
Trailing Stop: Activates at 2% profit, exits on 1% pullback
```

**Translation**: Give the trend some pullback room, but never let profits slip away once you're ahead!

---

## III. 1 Entry Condition: Simple as It Gets

This strategy has **one** entry condition, but in three steps:

### 🎯 The Only Entry Condition: EMA Golden Cross + HA Confirmation

**Plain English**:
> "When EMA20 crosses above EMA50, check if the HA candle is green and price is above EMA20. If all three conditions are met, buy!"

**Code looks like this**:
```python
EMA20 crosses above EMA50      # Golden cross signal
HA close > EMA20               # Price above moving average
HA open < HA close             # Green candle
```

**Classic Lines**:
- "Short-term MA golden cross! Trend is starting!"
- "Heikin Ashi is green? Direction confirmed!"
- "Price holding above EMA20? Good to enter!"

---

## IV. Exit Logic: Even Simpler Than Entry

### 4.1 Signal Exit

**Plain English**:
> "EMA50 crosses above EMA100 (a bit counterintuitive), but price has fallen below EMA20 and HA candle turned red? Then run!"

**Code looks like this**:
```python
EMA50 crosses above EMA100     # Trend continuation signal
HA close < EMA20               # Price below moving average
HA open > HA close             # Red candle
```

### 4.2 Multiple Exit Mechanisms

| Exit Method | Trigger Condition | Plain English |
|-------------|-------------------|---------------|
| ROI Exit | Time + profit target met | "Made enough, run" |
| Trailing Stop | Pullback after profit | "Don't give back profits" |
| Fixed Stop Loss | 10% loss | "Surrender and stop" |

---

## V. This Strategy's "Personality"

### ✅ Pros (Compliment Time)

1. **Clean Code**: Less than 100 lines, beginners can understand in a week
2. **Clear Logic**: EMA + HA, classic trend following combo
3. **Controllable Risk**: Trailing stop for automatic protection, no worries about pullbacks

### ⚠️ Cons (Roast Time)

1. **Oscillating Markets Kill**: No trend means golden/death crosses back and forth 😅
2. **Signal Lag**: EMA is a lagging indicator, half the move is gone by the cross
3. **Fixed Parameters**: No hyperparameter optimization, gotta edit code to adjust

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Clear Trend | Run with confidence | Golden cross + HA green bars work perfectly |
| 🔄 Oscillating Market | Stay away | Golden/death crosses will slap you back and forth |
| 📉 Downtrend | Don't touch | Long strategy going against the trend is dangerous |
| ⚡ High Volatility | Be careful | Might get shaken out |

---

## VII. Summary: How Good Is This Strategy?

### One-Line Review
> "Freqtrade strategy development's Hello World. Must learn, but be careful in live trading"

### Who Is It For?
- ✅ Beginners just getting into Freqtrade
- ✅ Developers wanting to learn strategy code structure
- ✅ People who need a simple strategy template to modify

### Who Is It NOT For?
- ❌ Lazy people wanting to make money directly
- ❌ Day traders pursuing high-frequency trading
- ❌ Victims of oscillating markets

### My Recommendation
1. **Read and understand the code first**: This is the best learning material
2. **Paper trade test**: Get familiar with strategy behavior
3. **Add your own logic**: Modify based on this foundation
4. **Small position live trading**: Validate your improvements

---

## VIII. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: Using Moving Averages to Determine Trends

Strategy001 is an **entry-level trend following strategy**. Less than 100 lines of code. What does that mean? Equivalent to **an elementary school essay** 📝

**Its Profit Philosophy**: Once a trend forms, follow it. When profitable, use trailing stop to protect gains.

- **Moving Average Cross**: Identify trend initiation
- **HA Candles**: Filter false breakouts
- **Trailing Stop**: Protect profits

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|--------------------------|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | This is its home turf! Follow the trend and profit |
| 🔄 Oscillating Market | ⭐⭐☆☆☆ | Golden/death crosses back and forth, fees eat profits |
| 📉 Downtrend | ⭐☆☆☆☆ | Long strategy going against trend, forget about profits |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | Easy to get shaken out, but stop loss protection exists |

**One-Line Summary**: Get in when there's a trend, hide when there isn't!

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Trading Pairs | BTC/USDT and other majors | Good liquidity, low slippage |
| Timeframe | 5m (default) | Can try 15m to reduce noise |
| Max Positions | 3-5 | Don't be greedy |

### 9.2 Config File Key Settings

```yaml
# config.json key settings
"max_open_trades": 3,
"stake_currency": "USDT",
"stake_amount": "unlimited",
"dry_run": true,  # Paper trade first!
```

### 9.3 Hardware Requirements (Easy)

This strategy has minimal computation, basically no hardware requirements:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-30 pairs | 4GB | 8GB | Fluid |

**Warning**: Don't think simple strategy means easy money just because hardware requirements are low! 😅

### 9.4 Backtest vs Live Trading

As an entry-level strategy, backtest and live trading differences are relatively small, but still note:

**Recommended Process**:
1. Paper trade for 1-2 weeks
2. Small position live trading (5-10% of capital)
3. Observe win rate and profit factor
4. Gradually increase position or improve strategy

**Don't go all in from the start**, no matter how simple the strategy!

---

## X. Bonus: The Strategy Author's "Little Tricks"

Look carefully at the code, you'll find some interesting things:

1. **Minimalist to the Extreme**: Author Gerald Lonlas clearly wanted to write a teaching template
   > "Deleted everything that could be deleted, only keeping the core logic"

2. **Clever Use of Heikin Ashi**: Not all strategies use HA, here it confirms trends
   > "Candlesticks too messy? Smooth them with HA"

3. **1% Trailing Stop**: This parameter is interesting, run on 1% pullback
   > "Profit protection needs to be ruthless, don't try to catch the last bit"

---

## XI. Final Words

### One-Line Review
> "The Hello World of strategies. Must learn, but don't expect it to make you rich"

### Who Is It For?
- ✅ Freqtrade beginners
- ✅ People wanting to learn strategy development
- ✅ People needing templates to modify
- ✅ Clear trend markets

### Who Is It NOT For?
- ❌ People wanting to make easy money
- ❌ Victims of oscillating markets
- ❌ High-frequency trading enthusiasts
- ❌ Counter-trend traders

### Manual Trader Recommendations

If you use this logic manually:
1. Switch to 5-minute chart
2. Add EMA20, EMA50, EMA100
3. Switch candlesticks to Heikin Ashi
4. Wait for golden cross + green candle + price holding above EMA20
5. Enter, set trailing stop

---

## XII. ⚠️ Risk Emphasis Again (Must Read This)

### Backtesting Looks Great, Live Trading Needs Caution

Strategy001 may perform well in backtesting—but there's a trap:

> **Simple strategy doesn't mean stable profits. Market condition changes can make it fail.**

Simply put: **Past performance ≠ Future returns**

### Hidden Risks of Entry-Level Strategies

In live trading, simple strategies may encounter:
- **Frequent stop losses in oscillating markets**: Without trends, golden/death crosses happen constantly
- **Signal lag**: By the time golden cross confirms, half the move is gone
- **Limit orders not executing**: Want to stop loss during a crash but can't

### My Recommendation (Real Talk)

```
1. First use this strategy as learning material
2. Paper trade for two weeks, observe performance in different markets
3. Try modifying parameters or adding filter conditions
4. Small position live trading to validate your improvements
5. Continuously iterate, form your own strategy
```

**Remember**: Strategies are dead, markets are alive. Learn others' strategies, eventually make them your own.

---

**Final Reminder**: No matter how simple the strategy, the market will teach you a lesson without warning. Test with small positions, survival is most important! 🙏