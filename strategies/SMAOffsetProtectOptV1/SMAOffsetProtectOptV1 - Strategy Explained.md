# SMAOffsetProtectOptV1 Strategy: The MA Deviation Hunter with Protection

> **Nickname**: "Bottom Picker Pro", "Hunter on Both Sides of the Moving Average"  
> **Occupation**: Quantitative hunter specializing in picking up bargains near moving averages  
> **Timeframe**: 5 minutes (sprinter mode)

---

## I. What is This Strategy?

Simply put, **SMAOffsetProtectOptV1** is a strategy that:
- Buys when price deviates too far from the moving average (a "bottom picking" strategy)
- Uses Elliott Wave indicator to confirm trend direction
- Combined with RSI to prevent chasing highs
- Has a special design: ignores ROI limits as long as there's a buy signal, letting profits run

It's like **going to the market at closing time to find bargains** — waiting for prices to be pushed below the moving average by a certain percentage, then "picking up cheapies" 🛒

---

## II. Core Configuration: Simply "Take Profits + Greedy Mode"

### Take-Profit Rules (ROI Table)

```
Time        Profit Target
────────────────────────
0 min       1%
```

**Translation**: This strategy is a bit "greedy", default setting is to run after making 1%...

**BUT!** There's an anti-human design: `ignore_roi_if_buy_signal=True`

> "As long as there's still a buy signal in the market, I'm not running! Let the profits fly!"

This is like planning to take profits at 1%, but then realizing you can keep making more, so you let it ride 🚀

### Stop Loss Rules

```
Fixed Stop Loss: -10%
Trailing Stop: Enabled after 1% profit, trails at 0.1%
```

**Translation**:
- **Fixed Stop Loss**: Accept a 10% loss, no questions asked
- **Trailing Stop**: Once you start making money, use 0.1% "stickiness" to follow the price, locking in profits

---

## III. 2 Buy Conditions: I've Categorized Them for You

The buy conditions are actually quite simple, just 2, but each has its own character:

### 🎯 Condition #1: Trend Pullback Buy
**Core Logic**: Price pulls back below MA + trend still up + not chasing highs

**In Plain English**:
> "The MA is the dad, price is the kid. The kid ran away from home (price below MA), but dad is still healthy (EWO is positive), and the kid doesn't have a fever (RSI isn't high). Time to go find the kid!"

**Code Translation**:
```python
close < EMA * 0.978  # Price is about 2.2% below MA
AND EWO > 5.638      # Trend is up (EWO positive and relatively high)
AND RSI < 61         # Not overheated
```

---

### 🎯 Condition #2: Deep Oversold Buy
**Core Logic**: Price crashed hard + EWO extremely negative = oversold bounce opportunity

**In Plain English**:
> "Price got crushed so hard, EWO dropped to -20. Time to pick up the pieces! No need to check RSI, just do it!"

**Code Translation**:
```python
close < EMA * 0.978  # Price is about 2.2% below MA
AND EWO < -19.993    # Extremely oversold
```

**Comment**: This condition #2 is like a "bottom-picking maniac" specialty, specifically designed to catch bounces during crashes. Higher risk but potentially higher reward 🎰

---

## IV. Protection Mechanism: 2 Layers of "Anti-Traps"

Each buy condition has protection parameters, like **going through two security doors**:

| Protection Type | Purpose | In Plain English |
|----------------|---------|------------------|
| EWO Threshold | Judge trend strength | "Is this drop real or fake?" |
| RSI Filter | Prevent chasing highs | "Don't stand guard on the mountain top!" |

**What is EWO?** Full name is Elliott Wave Oscillator, it's essentially **the difference between fast EMA and slow EMA**. This strategy uses 50 and 200 period EMAs to calculate EWO, very "long-term perspective."

> Positive value = Fast line above slow line = Short-term stronger than long-term = Uptrend
> Negative value = Fast line below slow line = Short-term weaker than long-term = Downtrend

---

## V. Sell Logic: Simple and Direct

### 5.1 Single Sell Signal

Just one condition:

```python
close > EMA(49-period) * 1.006
```

**In Plain English**:
> "Price rises 0.6% above the 49-period MA, bye bye!"

### 5.2 Special Setting: Stick Around When Buy Signal Exists

`ignore_roi_if_buy_signal=True` is this strategy's "little trick":

**Scenario**:
1. Price rose 1%, supposed to sell
2. But strategy checks: "Hey, there's still a buy signal in the market!"
3. Strategy: "Then I'm not selling, holding on!"

**In Plain English**:
> "I was gonna run at 1% profit, but realized the market is still accumulating, so I'll wait!"

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **Clear Logic**: Nothing fancy, just MA offset + EWO confirmation + RSI filter, three simple tools
2. **Dual-Mode Buying**: Catches trend pullbacks AND oversold bounces, walking on two legs
3. **Greedy but Controlled**: `ignore_roi_if_buy_signal` lets winning positions fly longer
4. **Optimizable Parameters**: 7 parameters can be tuned, adaptable to different markets

### ⚠️ Cons (Roast Time)

1. **Informative Timeframe Not Really Used**: Defined 1h information layer, but all decisions on 5m, kinda wasteful
2. **Easily Harvested in Ranging Markets**: EMA offset strategies get chopped like韭菜 (chives) in sideways markets
3. **No Volatility Filter**: Doesn't consider ATR, may misjudge during high volatility

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| 📈 Slow Bull Trend | 🟢 Recommended | Pullback buying works great, trailing stop locks profits |
| 🔄 Mild Fluctuation | 🟡 Caution | Increase low_offset, reduce trade frequency |
| 📉 One-sided Decline | 🟡 Careful | Only use condition #2 for bounces, small position trial |
| ⚡ Severe Volatility | 🔴 Not Recommended | EMA lag, serious signal delay |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Review
> "Classic MA offset strategy, suitable for beginners to learn, but needs parameter tuning for live trading."

### Who Should Use It?
- ✅ Quantitative beginners: Clear logic, clean code, easy to understand
- ✅ People who like bottom picking: Both buy conditions are "buy the dip" style
- ✅ People who don't want frequent trading: Tune parameters larger, lower trade frequency

### Who Should NOT Use It?
- ❌ High-frequency trading seekers: This strategy is conservative
- ❌ People who want to profit in ranging markets: MA offset performs poorly in sideways
- ❌ People who don't want to tune parameters: Default parameters may not suit your coins

### My Recommendations
1. **Run backtest first**: See historical performance
2. **Then tune parameters**: Especially low_offset and ewo_high
3. **Small position live trial**: Throw in like $100 to test
4. **Observe signal quality**: Check if buy/sell timing is reasonable

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Using "Deviation" to Find Opportunities

SMAOffsetProtectOptV1 belongs to the **EMA Offset Strategy Series**. The core philosophy of this series is:

> "If price strays too far from the moving average, it will eventually come back"

Like a rubber band, if you stretch it too tight, it snaps back.

**Its Money-Making Philosophy**:
- **Pick bottoms, don't chase highs**: Only buy when price is below MA
- **Trend confirmation**: Use EWO to judge if it's a real drop or fake
- **RSI filter**: Prevent entering when overheated

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:------------------|:--------------------------|
| 📈 Slow Bull Trend | ⭐⭐⭐⭐⭐ | Pullback buying, chasing the bull's butt, perfect! |
| 🔄 Mild Fluctuation | ⭐⭐⭐☆☆ | Can make money, but fees might be painful |
| 📉 One-sided Decline | ⭐⭐☆☆☆ | Condition #2 can catch bounces, but easy to catch falling knife |
| ⚡ Severe Volatility | ⭐☆☆☆☆ | EMA hasn't reacted yet, price already ran away |

**One-Sentence Summary**: **This strategy is a "trend friend", not a "ranging warrior"**

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Number of Trading Pairs | 5-20 | Don't be greedy, can't watch them all |
| Timeframe | 5m | This is the strategy's designed timeframe |
| Capital Allocation | 5-10% per pair | Diversify risk |

### 10.2 Key Configuration File Settings

```yaml
# config.json key settings
"max_open_trades": 3-5,  # Not too many, can't watch them all
"stake_currency": "USDT",
"stake_amount": "unlimited",  # Or fixed amount
"dry_run": true,  # Run simulation first!
```

### 10.3 Hardware Requirements (Important!)

This strategy has moderate computation, not demanding on hardware:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|---------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Okay |
| 50+ pairs | 8GB | 16GB | Needs monitoring |

**Warning**: Although this strategy is simple, calculating EMA requires some data, `startup_candle_count = 30`, you need to wait for 30 candles after startup before trading can begin 😅

### 10.4 Backtest vs Live Trading

**Honest Truth**: EMA offset strategies are especially prone to **overfitting**!

Why? Because:
1. EMA period parameters (16/49) can be tuned to perfection on historical data
2. Offset coefficients (0.978/1.006) can be precisely matched to historical optimal
3. But historical optimal ≠ future optimal

**Recommended Process**:
1. Train on 70% data, test on 30% data
2. Run backtests on multiple time periods
3. Check if parameter performance is stable across different periods
4. **Don't go all-in on live trading right away**

---

## XI. Bonus: The Strategy Author's "Little Tricks"

Looking carefully at the code, you'll find some interesting designs:

1. **EWO uses 50/200 periods**: Much slower than default 5/35, showing author wants more stable trend judgment
   > "I don't seek speed, I seek stability!"

2. **Buy EMA is 16, Sell EMA is 49**: Fast to buy, slow to sell, interesting design
   > "Enter fast, exit slow — let profits run!"

3. **low_offset=0.978, high_offset=1.006**: Buy 2.2% low, sell 0.6% high, asymmetric design
   > "Pick bottoms ruthlessly, run away fast!"

---

## XII. Final Final Words

### One-Sentence Review
> "Entry-level EMA offset strategy, suitable for learning and tuning, but needs effort for live trading."

### Who Should Use It?
- ✅ Quantitative beginners who want to learn strategy principles
- ✅ People who like bottom-picking style
- ✅ People who have time to tune and optimize parameters
- ✅ People who want to understand EWO indicator

### Who Should NOT Use It?
- ❌ People who want plug-and-play
- ❌ Ranging market warriors
- ❌ People who don't want to learn parameter tuning
- ❌ High-frequency trading seekers

### Manual Trader Recommendations
If you don't run a bot but want to manually use this strategy's logic:
1. Draw a 16-period EMA
2. Watch when price drops about 2% below EMA
3. Check EWO (you can use TradingView indicator)
4. Consider entering when RSI is below 61
5. Consider exiting when price rises 0.6% above EMA

---

## XIII. ⚠️ Risk Re-emphasis (Must Read Section)

### Backtesting Looks Great, Live Trading Needs Caution

SMAOffsetProtectOptV1's historical backtest often **looks pretty good** — but there's a trap:

> **Because parameters can be optimized, the strategy can easily "fit" the optimal solution of past market conditions, but this doesn't guarantee future profits.**

Simply put: **Past performance does not guarantee future results** — this cliché is actually true.

### Hidden Risks of Complex Strategies

In live trading, simple logic can lead to:
- **Slippage**: Prices change instantly, backtests assume perfect execution
- **Latency**: Network delays can cause signal invalidation
- **Exchange Limits**: API limits can cause order failures
- **Extreme Events**: Black swan events can invalidate any strategy

### My Recommendations (Honest Truth)

```
1. Run dry_run mode for at least 1 week first
2. Check signal quality, see if buy/sell timing is reasonable
3. Tune parameters then run simulation again
4. Small position live trial (don't exceed 5% of total capital)
5. Continuous monitoring, adjust when problems found
```

**Remember**: No matter how good the strategy, when the market teaches you a lesson, it doesn't warn you first. Light position testing, survival is most important! 🙏

---

**Final Reminder**: EMA offset strategies perform well in trending markets but get harvested in ranging markets. Judge the current market environment before using!