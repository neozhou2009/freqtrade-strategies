# ClucHAnix Strategy: The "Refined Trend Hunter" Combining HA Candles + Bollinger Bands

> **Nickname**: HA Bollinger Band Hunter  
> **Profession**: Multi-condition filtered trend follower  
> **Timeframe**: 5 minutes + 1-hour informational layer

---

## 1. What's This Strategy?

In simple terms, **ClucHAnix** is a:
- Strategy that watches the market using "smoothed candles" (Heikin Ashi)
- Specifically finds "price dropped too hard, time to rebound" opportunities
- Only enters after passing the 1-hour "trend exam"
- Has a complex "trailing stop" protecting profits after entry

Think of it as a **cautious veteran hunter** lurking in the mountains, waiting for prey:
1. First uses a "telescope" (1-hour ROC) to confirm there's movement on the other side of the mountain
2. Then sets "traps" (Bollinger Bands) to wait for the perfect moment
3. When prey is caught, keeps a close eye — bolts at the first sign of danger 😅

---

## 2. Core Settings: "Take Profits and Run"

### Take-Profit Rules (ROI Table)

```
Immediately after opening    → 10.3% profit ✅ Worth it!
After 3 minutes              → 5% profit      ✅ Not bad
After 5 minutes              → 3.3% profit    ✅ Acceptable
After 1 hour                 → 2.7% profit    ⚠️ Getting thin
After 2 hours                 → 1.1% profit    😴蚊r leg
After 5 hours                 → 0.5% profit    💤 Run already
```

**Translation**: This strategy wants **speed and decisiveness** — if it can make 3%+ within 5 minutes of opening, it's pretty happy. The longer it drags, the lower its profit expectations — a "securing profits early" mindset.

### Stop Loss Rules

```
Before profit < -99%, stop-loss position is determined by custom_stoploss
```

**Translation**: This strategy **doesn't set a fixed stop-loss**, entirely relying on a complex "dynamic stop-loss calculator." It dynamically adjusts the stop position based on how much you're winning — the more you win, the "looser" the stop; win less, and the stop gets "tighter."

---

## 3. Two Entry Conditions: Categorized for You

This strategy's entry conditions need to pass a "two-layer exam." Here are the 2 categories:

### Condition 1: Textbook Bollinger Band Entry
**Core logic**: Price near lower Bollinger Band, showing "can't drop further" signals, and 1-hour trend is upward

**Plain English**:
> "Dude, price has dropped to the lower Bollinger Band, looks like it can't drop anymore. And the 1-hour trend over there is also good — buy or not?"

**Representative conditions**:
- `bbdelta > ha_close * 0.01846` → Bollinger Band needs to be open enough
- `closedelta > ha_close * 0.01009` → Close price change must be noticeable
- `tail < bbdelta * 0.98973` → Lower wick can't be too long (otherwise it's a false signal)
- `ha_close < lower.shift()` → HA close must break below lower band
- `hh_48_diff > 6.867` → 48-hour high must be high enough
- `ll_48_diff > -12.884` → 48-hour low can't be too low either

---

### Condition 2: EMA Deviation "Rebound" Entry
**Core logic**: Price deviates too far from EMA, short-term regression is likely

**Plain English**:
> "Price has deviated way too far from the 50-day EMA — it'll have to bounce back eventually! Buy or not?"

**Representative conditions**:
- `ha_close < ema_slow` → HA close below 50-day EMA
- `ha_close < 0.00785 * bb_lowerband` → Hugging lower band
- `hh_48_diff > 6.867` → 48-hour high filter
- `ll_48_diff > -12.884` → 48-hour low filter

**Both share a common condition**:
- `rocr_1h > 0.5411` → **1-hour ROC must be rising**, this is the "passing grade"!

---

## 4. Protection Mechanisms: 1 Layer of "Slippage Security Guard"

Every entry condition is equipped with a "slippage security guard," like airport security:

| Protection Type | Effect | Plain English |
|----------------|--------|---------------|
| Slippage protection | max_slip = 0.73% | "Fill price can't be more than 0.73% above my quote, otherwise I'm not buying!" |

This strategy's slippage protection is relatively loose (0.73%), suitable for exchanges with moderate liquidity.

---

## 5. Exit Logic: More Elaborate Than Entries

### 5.1 Tiered Take-Profit: How Much to Take and Run

```
Profit > 10.3%       → Trailing stop takes over
Profit 5%-10.3%     → Keep holding, wait for more
Profit 3.3%-5%      → Consider running
Profit 1.1%-3.3%    → Run fast, don't be greedy
Profit < 1.1%       → Prepare to trigger hard stop
```

**Plain English**:
- **Initially**: Ambitious, wants 10%+ profit
- **As time passes**: More and more "timid," okay with whatever it can get
- **After 5 hours**: 0.5% is fine too, just don't lose

---

### 5.2 Special Scenario Exits (Trump Cards)

This strategy has **4 special exit skills**, specifically for extreme market conditions:

| Scenario | Trigger Condition | Plain English |
|----------|-------------------|---------------|
| Dead fish market | Profit<-6.3%, price<EMA200, extremely low volatility | "This market is too boring, playing dead, exit first" |
| 48-hour pump | 1-hour gain >95%, profit -4% to -8%, multiple indicators weakening | "Rallied too hard before, gonna correct, run!" |
| 36-hour pump | 1-hour gain >70%, profit -4% to -8%, multiple indicators weakening | "Gained too much, be careful" |
| 24-hour pump | 1-hour gain >60%, profit -4% to -8%, multiple indicators weakening | "Short-term gain too large, bail!" |

---

### 5.3 Base Exit Signals (3 Total)

**Classic lines**:

1. **Signal #1**: `fisher > 0.48492 + price declining consecutively + EMA confirmation`
   > "Fisher indicator says overbought, and price is still falling — run!"

2. **Signal #2**: `close > 9-day MA + close > 24-day EMA*1.211 + RSI > 50`
   > "Price broke above the moving average, but RSI is also high — watch out"

3. **Signal #3**: `9-day MA rising + price < 50-day HMA + price > 24-day EMA*0.907`
   > "Trend is weakening but not dead yet, take profits and move on"

---

## 6. Strategy Personality

### Pros

1. **Multi-timeframe analysis**: Trades on 5 minutes but filters on 1 hour, won't trade against the trend
2. **Dynamic profit-taking stop-loss**: Automatically adjusts the "safety belt" based on earnings — smart!
3. **Specifically prevents "pump and dump"**: Has 4 special exit skills specifically for extreme conditions
4. **Rich indicators**: Trend, momentum, volume, capital flow all considered

### Cons

1. **Too many parameters**: 20+ parameters, optimization will kill you 😅
2. **Heavy computation**: Must calculate 1-hour informational layer every time, VPS RAM might not cut it
3. **1-hour filter too strict**: May cause missing many opportunities
4. **Too complex**: Code is nearly 500 lines, normal people can't understand it at all

---

## 7. When to Use It

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Slow bull rise | Enable | Clear trend, buying on pullbacks often continues upward |
| Ranging consolidation | Use with caution | 1-hour filter misses many opportunities |
| Pump and dump | Enable | Has specific countermeasures, it's showtime |
| Flat declining | Disable | Strategy is bullish-biased, unsuitable for sustained decline |

---

## 8. Bottom Line: Is This Strategy Any Good?

### One-Line Verdict
> "A complex trend strategy combining Heikin Ashi candlestick analysis + Bollinger Band mean reversion + multi-timeframe filtering, like a cautious veteran hunter — waits patiently, strikes at the right moment, runs when things look bad."

### Who's It For?
- Quantitative traders who understand technical analysis
- People patient enough to optimize parameters
- Investors running medium-to-long-term strategies
- Users with certain VPS configuration requirements

### Who's It NOT For?
- Newbies (too many parameters, can't follow)
- People seeking simplicity (this strategy is more complex than a maze)
- Low-spec VPS users (will crash)
- People wanting "passive income" (needs continuous monitoring and adjustment)

### My Advice
1. **Backtest first**: At least 3 months of data, see how it performs
2. **Small capital test**: Live test for 1-2 months, confirm effectiveness
3. **Watch special conditions**: Whether pump/dump protection mechanisms work
4. **Don't mess with parameters**: 20+ parameters, one wrong tweak could ruin everything

---

## 9. What Markets Does This Strategy Make Money In?

### 9.1 Core Logic: Using a "Telescope" to Filter False Signals

ClucHAnix is the "evolved version" of the Cluc series, positioned as a "high-volatility market protection trend strategy." Code volume approaches 500 lines — equivalent to a short novel 📚

**Its money-making philosophy**: Use Heikin Ashi to smooth prices, use Bollinger Bands to find "extremes," use 1-hour ROC to filter "counter-trend."

- **Layer 1 (5 minutes)**: Watch short-term price changes, find "can't drop further" opportunities
- **Layer 2 (1 hour)**: Watch long-term trend, ensure you're not trading against it
- **Protection Layer**: Dynamic profit-taking + special exits, handling various extreme situations

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English |
|:---|:---|:---|
| Slow bull rise | Good | Clear trend, strategy effectively catches continued rallies after pullbacks |
| Ranging market | Moderate | Multi-condition filtering reduces frequency but signal quality is okay |
| Declining trend | Moderate | Has counter-trend protection but overall bullish bias unsuitable for sustained decline |
| Pump and dump | Good | Special exit mechanisms show their worth here, protecting profits |

**One-line summary**: Performs best in markets with **clear trends + volatility**, average performance in consolidation and gradual decline.

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended | Commentary |
|---------------|-------------|------------|
| Number of pairs | 10-20 | Don't run too many, will crash your VPS |
| Timeframe | 5m + 1h | Must configure 1-hour informational layer! |

### 10.2 Key Config Settings

```yaml
# Must enable
use_custom_stoploss = True
trailing_stop = True

# Order types
order_types:
  entry: market
  exit: market
```

### 10.3 Hardware Requirements (Important!)

This strategy's computational load is moderate-to-high, with some VPS RAM requirements:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|-----------------|------------|
| 10-20 pairs | 2GB | 4GB | ✅ Smooth |
| 20-50 pairs | 4GB | 8GB | ⚠️ Barely |
| 50+ pairs | 8GB | 16GB | ❌ Will lag |

**Warning**: This strategy needs to cache 1-hour data, insufficient RAM will cause errors! 😅

### 10.4 Backtesting vs. Live Trading

- **Slippage differences**: Strategy has slippage protection but live fill prices may deviate from backtest
- **1-hour delay**: Needs to accumulate 1-hour data before trading can begin
- **Special exits**: Backtest may not fully simulate "pump protection" actual effects

**Recommended process**:
1. Paper backtesting: At least 3 months of data
2. Paper trading: 1-2 weeks
3. Small-capital live: 1-2 months
4. Gradually increase: Scale up after confirming effectiveness

**Don't go all-in right away**, even the best strategy needs a磨合 period!

---

## 11. Bonus: The Strategy Author's "Little Tricks"

Looking closely at the code, you can spot some fun design choices:

1. **"Dead fish" market detection**
   > "bb_width < 0.043 + volume contraction = dead fish market认定"
   > Seems the author has also suffered from consolidation markets 😅

2. **48/36/24-hour gradient protection**
   > Different time periods' gains correspond to different protection levels — the more recent the pump, the more sensitive the protection
   > The author must have been beaten by "pump and dump" before

3. **Complex trailing stop formula**
   > Uses linear interpolation to calculate dynamic stop — looks very professional
   > But actual effects may need live verification

---

## 12. The Bottom Line

### One-Line Verdict
> "A complex trend strategy combining HA candles, Bollinger Bands, and multi-timeframe filtering — like a cautious veteran hunter: strikes when the opportunity is right, runs at the first sign of trouble."

### Who's It For?
- People with technical background who can understand complex code
- People patient enough to optimize parameters and backtest
- People with trading experience who understand "trends"
- Users with VPS RAM of at least 4GB

### Who's It NOT For?
- Newbies (too many parameters, completely lost)
- Lazy people (needs continuous monitoring and adjustment)
- People with small capital running many pairs
- People seeking "simple and profitable" strategies

### Manual Trading Tips
This strategy is **NOT suitable for manual trading**:
1. Need to simultaneously monitor 5-minute and 1-hour data
2. Multiple indicators like Bollinger Bands + ROC + EMA must all be satisfied simultaneously
3. Dynamic profit-taking stop-loss calculations are too complex for manual computation

---

## 13. ⚠️ Final Warning (Must Read!)

### Backtesting Looks Great, But Live Trading Is a Different Beast

ClucHAnix's historical backtest often **looks good** — but here's the trap:

> **Because there are many parameters (20+), the strategy easily "fits" the optimal solution for past prices, but this doesn't guarantee future profitability.**

Simply put: **Memorized all the answers and got 100, doesn't guarantee you'll pass the next test.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may lead to:
- **Indicator failure**: Some indicators失效 in specific market environments
- **Execution delay**: Complex calculations may cause order execution delays
- **Overfitting risk**: 20+ parameters, easy to "fit" historical data during optimization
- **Hardware dependency**: Insufficient RAM will cause complete failure

### My Real Advice

```
1. Backtest at least 3 months, see if the equity curve is stable
2. Small-capital live test for 1-2 months, confirm strategy effectiveness
3. Don't mess with parameters! One wrong tweak could ruin everything
4. Watch performance during extreme conditions — that's when you truly test a strategy
5. Never all-in — test with light positions, staying alive is what matters!
```

**Remember**: Strategies are written by humans, but markets are alive. Even the best strategy can失效, test with light positions, staying alive is what matters! 🙏

**Final reminder**: Complex strategies are like sports cars — powerful performance, but require driving skills. Newcomers shouldn't try easily, experienced drivers must drive carefully too! 🚗💨
