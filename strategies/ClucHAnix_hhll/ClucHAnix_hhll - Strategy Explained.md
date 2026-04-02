# ClucHAnix_hhll Strategy: HA Candles + Bollinger Bands = The Refined Trend Hunter

> **Nickname**: HA Bollinger Band Hunter
> **Profession**: Multi-Condition Filtered Trend Follower
> **Timeframe**: 5 Minutes + 1-Hour Informative Layer

---

## 1. What's This Strategy?

Put simply, **ClucHAnix_hhll** is:
- A strategy that reads the market using "sneaky candles" (Heikin Ashi)
- Specifically hunting for opportunities like "price has fallen too hard and is about to bounce back"
- Only buys after passing the 1-hour "trend exam"
- Has a complex "trailing stop" to protect profits after buying

Think of it as a **cautious old hunter** lying in wait in the mountains:
1. First uses a "telescope" (1-hour ROC) to confirm there are animals on the other side of the mountain
2. Then sets a "trap" (Bollinger Bands) and waits for the perfect moment
3. Once the prey is caught, keeps a close eye — bolts at the slightest provocation 😅

---

## 2. Core Settings: Basically "Take the Money and Run"

### Take-Profit Rules (ROI Table)

```
Immediately after entry  →  Make 10.3%  ✅ Worth it!
After 3 minutes          →  Make 5%      ✅ Not bad
After 5 minutes          →  Make 3.3%    ✅ Acceptable
After 1 hour             →  Make 2.7%    ⚠️ Getting thin
After 2 hours            →  Make 1.1%    😴 Chicken feed
After 5 hours            →  Make 0.5%    💤 Run away already
```

**Translation**: This strategy wants to **act fast and exit quickly** — if it can make 3%+ within 5 minutes of entry, that's satisfying enough. The longer it holds, the lower the profit expectation — a "securing profits" mentality.

### Stop-Loss Rules

```
Until profit < -99%, stop-loss position is determined by custom_stoploss
```

**Translation**: This strategy **doesn't set a fixed stop-loss** — it relies entirely on a complex "dynamic stop-loss calculator." It adjusts stop-loss dynamically based on how much you're earning — the more you earn, the "looser" the stop; the less you earn, the "tighter" it gets.

---

## 3. 2 Buy Conditions: I've Categorized Them for You

This strategy's entry conditions need to pass a "two-layer exam" — here are the 2 categories:

### 🎯 Category #1: Bollinger Bands "Textbook" Buy
**Core Logic**: Price has dropped near the Bollinger lower band, showing a "can't go lower" signal, and the 1-hour trend is upward.

**Plain English**:
> "Dude, price has dropped to the lower Bollinger Band — it looks like it can't go much lower. And the 1-hour trend is looking good too. Buy?"

**Representative Conditions**:
- `bbdelta > ha_close * 0.01846` → Bollinger Band spread needs to be wide enough
- `closedelta > ha_close * 0.01009` → Closing price change needs to be significant
- `tail < bbdelta * 0.98973` → Lower wick can't be too long (otherwise it's a false signal)
- `ha_close < lower.shift()` → HA close needs to break below the Bollinger lower band
- `hh_48_diff > 6.867` → 48-hour highest point needs to be high enough
- `ll_48_diff > -12.884` → 48-hour lowest point can't be too low

---

### 📉 Category #2: EMA Deviation "Rebound" Buy
**Core Logic**: Price has deviated too far from EMA, creating a short-term regression demand.

**Plain English**:
> "Price has seriously deviated from the 50-day moving average — it's got to bounce back eventually! Buy?"

**Representative Conditions**:
- `ha_close < ema_slow` → HA close is below the 50-day EMA
- `ha_close < 0.00785 * bb_lowerband` → Close to the Bollinger lower band
- `hh_48_diff > 6.867` → 48-hour highest point filter
- `ll_48_diff > -12.884` → 48-hour lowest point filter

**⚠️ Shared Condition for Both**:
- `rocr_1h > 0.5411` → **The 1-hour ROC must be rising** — this is the "passing grade"!

---

## 4. Protection Mechanisms: 1 Layer of "Slippage Security Guard"

Each entry condition comes with a "slippage security guard," like subway security:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| Slippage Protection | max_slip = 0.73% | "The execution price can't be more than 0.73% higher than my quote — otherwise I'm not buying!" |

This strategy's slippage protection is relatively loose (0.73%), suitable for scenarios with average exchange liquidity.

---

## 5. Exit Logic: Flashier Than Entry

### 5.1 Tiered Take-Profit: Exit Based on Profit Level

```
Profit > 10.3%        →  Trailing stop takes over
Profit 5%-10.3%       →  Keep holding, wait for more
Profit 3.3%-5%        →  Consider running
Profit 1.1%-3.3%      →  Run fast, don't be greedy
Profit < 1.1%         →  Prepare to trigger hard stop-loss
```

**Plain English**:
- **At the start**: Big ambitions, want to earn 10%+
- **As time passes**: More "timid," any profit is fine
- **After 5 hours**: 0.5% is also fine, just don't lose

---

### 5.2 Special Scenario Exits (Trump Cards)

This strategy has **4 special exit skills** specifically for extreme market conditions:

| Scenario | Trigger Condition | Plain English |
|----------|-------------------|---------------|
| Dead Fish Market | Profit <-6.3%, price < EMA200, extremely low volatility | "This market is too boring — playing dead, bailing out first" |
| 48-Hour Surge | 1-hour gain >95%, profit -4% to -8%, multiple indicators weakening | "Rally was too strong, expecting a pullback — run!" |
| 36-Hour Surge | 1-hour gain >70%, profit -4% to -8%, multiple indicators weakening | "Gained too much, be careful" |
| 24-Hour Surge | 1-hour gain >60%, profit -4% to -8%, multiple indicators weakening | "Short-term gain was excessive —!" |

---

### 5.3 Basic Sell Signals (3)

**Classic Lines**:

1. **Signal #1**: `fisher > 0.48492 + price declining consecutively + EMA confirmation`
   > "Fisher indicator says overbought, and price is still falling — run!"

2. **Signal #2**: `close > 9-day MA + close > 24-day EMA*1.211 + RSI > 50`
   > "Price broke through the moving averages, but RSI is also high — be careful"

3. **Signal #3**: `9-day MA rising + price < 50-day HMA + price > 24-day EMA*0.907`
   > "Trend is weakening but not completely dead — take profits and run"

---

## 6. Strategy "Personality"

### ✅ Pros

1. **Multi-Timeframe Analysis**: Trades on 5 minutes but filters on 1 hour — won't trade against the trend
2. **Dynamic Take-Profit/Stop-Loss**: Automatically adjusts the "safety belt" based on earnings — smart!
3. **Specifically Guards Against "Surge and Crash"**: Has 4 special exit skills for extreme market conditions
4. **Rich Indicators**: Trend, momentum, volume, fund flow — all taken into account

### ⚠️ Cons

1. **Too Many Parameters**: 20+ parameters — you'll die optimizing them 😅
2. **Heavy Computation**: Every run calculates the 1-hour informational layer — low RAM VPS will lag
3. **1-Hour Filter Too Strict**: May cause missing many opportunities
4. **Too Complex**: Nearly 500 lines of code — average person can't understand it

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Slow Bull Rise | ✅ Enable | Clear trends, pullback entries tend to continue rising |
| Volatile Consolidation | ⚠️ Cautious | 1-hour filter will miss many opportunities |
| Extreme Volatility | ✅ Enable | Has specialized mechanisms — this is when it shows off |
| Sideways Decline | ❌ Disable | Strategy is overall long-biased, not suitable for sustained |

---

## 8. Summary: How Does This Strategy Really Stack Up?

### One-Line Verdict
> "A complex trend strategy combining Heikin Ashi candle analysis + Bollinger Bands mean reversion + multi-timeframe filtering — like a cautious old hunter lying in wait, striking when the moment is right, and running when things look bad."

### Who's It For?
- ✅ Quantitative traders who understand technical analysis
- ✅ People with patience for parameter optimization
- ✅ Mid-to-long-term investors
- ✅ Users with certain VPS configuration requirements

### Who's It NOT For?
- ❌ Beginner newcomers (too many parameters, can't understand)
- ❌ People who want simplicity (this strategy is more complex than a maze)
- ❌ Low-spec VPS (will run poorly)
- ❌ People who want "" (needs continuous monitoring and adjustment)

### My Recommendations
1. **Backtest First**: Run at least 3 months of data, check the equity curve
2. **Small Capital Testing**: Run live for 1-2 months, confirm effectiveness
3. **Watch Special Situations**: Check if surge/crash protection mechanisms activate
4. **Don't Mess with Parameters**: Changing one of 20+ parameters could ruin everything

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Using a "Telescope" to Filter False Signals

ClucHAnix_hhll is the "evolved version" of the Cluc series, positioned as a "high-volatility market protection-type trend strategy." The codebase is close to 500 lines — that's like a short novel 📚

**Its Money-Making Philosophy**: Use Heikin Ashi to smooth prices, use Bollinger Bands to find "extremes," use 1-hour ROC to filter "counter-trend."

- **Layer 1 (5 minutes)**: Watch short-term price changes, find "can't fall further" opportunities
- **Layer 2 (1 hour)**: Watch long-term trends, ensure you're not fighting the trend
- **Protection Layer**: Dynamic take-profit + special exits, handle various extreme situations

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:-----------|:------:|:------------------------|
| Slow Bull Rise | ⭐⭐⭐⭐ | When trends are clear, strategy effectively catches continued after pullbacks |
| Volatile Market | ⭐⭐⭐ | Multi-condition filtering reduces frequency, but signal quality is acceptable |
| Downtrend | ⭐⭐⭐ | Has counter-trend protection, but overall long bias not suitable for sustained |
| Extreme Volatility | ⭐⭐⭐⭐ | Special exit mechanisms come in handy here, protecting profits |

**One-Line Summary**: Performs best in **trending markets with volatility**, average in sideways and declining markets.

---

## 10. Want to Run This Strategy? Check These Settings First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Comment |
|-------------------|-----------------|---------|
| Number of Trading Pairs | 10-20 | Don't run too many — will crash your VPS |
| Timeframe | 5m + 1h | Must configure the 1-hour informational layer! |

### 10.2 Key Config File Settings

```yaml
# Must enable
use_custom_stoploss = True
trailing_stop = True

# Order Types
order_types:
  entry: market
  exit: market
```

### 10.3 Hardware Requirements (Important!)

This strategy has medium-to-high computational load and certain RAM requirements:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------------|-------------|-----------------|------------|
| 10-20 pairs | 2GB | 4GB | ✅ Smooth |
| 20-50 pairs | 4GB | 8GB | ⚠️ Barely |
| 50+ pairs | 8GB | 16GB | ❌ Will be very laggy |

**Warning**: This strategy needs to cache 1-hour data — insufficient RAM will cause errors! 😅

### 10.4 Backtest vs. Live Trading

- **Slippage Difference**: Strategy has slippage protection, but live execution price may deviate from backtest
- **1-Hour Delay**: Needs to accumulate 1-hour data before trading can begin
- **Special Exits**: Backtesting may not fully simulate actual "surge protection" effects

**Recommended Process**:
1. Paper backtesting: at least 3 months of data
2. Paper trading: 1-2 weeks
3. Small capital live trading: 1-2 months
4. Gradually increase position: confirm effectiveness before scaling up

**Don't go all-in right away** — even the best strategy needs a break-in period!

---

## 11. Bonus: Strategy Author's "Little Tricks"

Look closely at the code, and you'll find some interesting things:

1. **"Dead Fish" Market Detection**
   > "bb_width < 0.043 + shrinking volume = dead fish market confirmed"
   > Seems like the author has also suffered from sideways markets 😅

2. **48/36/24 Hour Gradient Protection**
   > Different time periods' gains correspond to different protection levels — the more recent the surge, the more sensitive the protection
   > The author must have been hit hard by "surge then crash" 😅

3. **Complex Trailing Stop Formula**
   > Uses linear interpolation for dynamic stop-loss — looks very professional
   > But actual effectiveness may need live trading verification

---

## 12. The Bottom Line

### One-Line Verdict
> "A complex trend strategy combining HA candles, Bollinger Bands, and multi-timeframe filtering — like a cautious old hunter who strikes when the moment is right and runs when things look bad."

### Who's It For?
- ✅ People with technical background who can understand complex code
- ✅ People with patience for parameter optimization and backtesting
- ✅ People with trading experience who understand "trends"
- ✅ Users with at least 4GB RAM VPS

### Who's It NOT For?
- ❌ Beginners (too many parameters, completely overwhelming)
- ❌ Lazy people (needs continuous monitoring and adjustment)
- ❌ People with very small capital running multiple pairs
- ❌ People seeking "simple and explosive" strategies

### Manual Trading Recommendations
This strategy is **NOT suitable for manual trading**:
1. Needs to monitor 5-minute and 1-hour data simultaneously
2. Bollinger Bands + ROC + EMA and other indicators must all be satisfied simultaneously
3. Dynamic take-profit/stop-loss calculations are too complex for manual computation

---

## ⚠️ Final Warning (Must Read!)

### Backtesting Looks Great — Be Careful in Live Trading

ClucHAnix_hhll's historical backtesting often **looks good** — but there's a trap:

> **Because it has many parameters (20+), the strategy easily "fits" the optimal solution for past market conditions, but this doesn't guarantee future profitability.**

Simply put: **Getting 100% by memorizing answers doesn't guarantee you'll pass next time.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may lead to:
- **Indicators Failing**: Some indicators may fail in specific market environments
- **Execution Delays**: Complex calculations may cause order execution delays
- **Overfitting Risk**: With 20+ parameters, it's easy to "fit" historical data during optimization
- **Hardware Dependency**: Insufficient RAM will cause a outright stop

### My Recommendations (Sincere Advice)

```
1. Backtest at least 3 months of data, check if the curve is stable
2. Test with small capital for 1-2 months, confirm strategy effectiveness
3. Don't randomly change parameters! Messing up one could ruin everything
4. Watch performance in extreme market conditions — that's the real test
5. Never all-in — test with light positions, survival is the top priority!
```

**Remember**: Strategies are written by humans, but markets are alive. Even the best strategy can fail. Test with light positions, survival is what matters! 🙏

---

**Final Reminder**: Complex strategies are like high-performance sports cars — incredibly powerful, but you need driving skills. Newcomers, don't try this lightly; even veterans should drive carefully! 🚗💨
