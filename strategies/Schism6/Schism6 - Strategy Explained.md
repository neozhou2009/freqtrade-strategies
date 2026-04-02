# Schism6 Strategy: The "Time-Thinking" Smart Dip Hunter

> **Nickname**: The Time Philosopher
> **Role**: Trend Pullback Hunter
> **Timeframe**: 5 minutes + 1 hour dual engine

---

## I. What is This Strategy?

Simply put, **Schism6** is:
- Dual timeframe analysis (big timeframe for direction, small for entry)
- Dynamic parameter system (longer holding = more lenient rules)
- Smart position management (watching global slots for decisions)

Like a **short-term trader with big-picture thinking**, it checks the 1-hour trend first, then finds pullback opportunities on the 5-minute chart, and gets more patient the longer it holds.

---

## II. Core Configuration: "Take Profits, But Don't Rush"

### Take Profit Rules (ROI Table)

```
Immediately  → 2.5% profit? Consider exiting
10 minutes   → 1.5% is fine too
20 minutes   → 1% is acceptable
30 minutes   → 0.5% - better than nothing
2 hours      → Break-even? Time to leave
```

**Translation**: This strategy is a "quick-handed short-termer" - take profits and go, don't be greedy. No profit after 2 hours? Break-even retreat, don't be friends with time.

### Stop-Loss Rules

```
Hard stop-loss: -10% (final line of defense)
Dynamic stop-loss: -3% at 0 min, break-even at 5 hours holding
```

**Translation**: Strict stop-loss when just entering (-3%), gets more lenient the longer you hold, giving the trend time to develop.

---

## III. Buy Conditions: Two Scenarios, Each With Its Own Logic

### Scenario 1: How to Buy When Empty?

This strategy's entry logic is a bit complex, let me break it down:

**First Check the Big Picture (1-hour level)**:
- RSI >= 65 → Market is strong, not buying dip in weakness

**Then Check Specific Price Level**:
- Price <= 3-day low + 87% of range
- Meaning: Enter near support level

**Finally Check Entry Timing (RMI indicator)**:
- RMI slow >= 33 (not extremely weak)
- RMI fast <= 41 (fast line not overbought)
- During RMI downtrend (in pullback)

**Plain English**:
> "Big timeframe strong, small timeframe pulling back, position near support - that's when I strike."

**Classic Lines**:
- Condition: `RSI(1h) >= 65` → "Following the trend"
- Condition: `Price <= 3-day low + 87% ADR` → "Cheap is cheap"
- Condition: `RMI downtrend` → "Buy when others are fearful"

---

### Scenario 2: How to Add When Already Holding?

Already have a position? Strategy checks if it can add:

**Conditions**:
1. RMI uptrend (trend continuing)
2. Current profit > peak profit × dynamic factor
3. RMI slow >= linear growth threshold

**What is Linear Growth?**

```
Holding 3 hours → Add threshold RMI >= 30
Holding 6 hours → Add threshold RMI >= 50
Holding 12 hours → Add threshold RMI >= 70
```

**Plain English**:
> "The longer you hold, the higher the threshold for adding. Just bought? Can add. Been holding all day? Don't mess around."

This prevents **adding at high positions**, protecting existing profits.

---

## IV. Sell Logic: Three Signals, Each Smarter Than the Last

### 4.1 Dynamic Stop-Loss: More Lenient Over Time

```
Just entered     → Stop at -3%
Holding 2.5 hrs  → Stop at -1.5%
Holding 5 hours  → Break-even exit
```

**Plain English**:
> "New positions get strict stop-loss, old positions get a chance to turn around."

### 4.2 Trend Reversal Signals

| Scenario | Trigger Condition | Plain English |
|----------|-------------------|----------------|
| Had profit before | RMI crosses below 50 | "Trend weakening, time to go" |
| Never made money | RMI crosses below 10 | "Completely dead, cut losses" |

### 4.3 Slot Management: The Big Picture

This is where the strategy is smartest:

```python
if has free slots:
    Other pairs need to be profitable to sell
    # Avoid selling too early and missing rebounds
else:
    Only sell the biggest loser
    # When slots are tight, prioritize releasing worst position
```

**Plain English**:
> "Slots available? No rush. Slots full? Clear the worst one first."

---

## V. This Strategy's "Personality"

### Pros (The Good Stuff)

1. **Multi-Timeframe Confirmation**: Not blindly buying dips, checks big timeframe first
2. **Dynamic Risk Control**: Auto-adjusts risk parameters based on holding time, human-like
3. **Global View**: Makes decisions watching all positions, not isolated single trades
4. **Peak Protection**: Sets protection after making money, won't let profit turn to loss
5. **Entry Confirmation**: Rejects limit orders if price deviates too much, prevents slippage

### Cons (The Not-So-Good Stuff)

1. **High Complexity**: So many parameters, beginners get dizzy
2. **Depends on Live Data**: Backtesting can't run add-on logic, only live can verify
3. **High Computational Cost**: Queries database every time, gets slow with many pairs
4. **Hard to Tune**: Buy parameters are optimized, may need redo for different markets

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Slow Bull Uptrend | ✅ Default parameters | Pullback dip-buying strategy's perfect home |
| Moderate Oscillation | ⚠️ Raise stop-loss | May stop out frequently, but can catch swings |
| Rapid Decline | ❌ Don't use | Multi-timeframe RSI fails, buying halfway down |
| Extreme Volatility | ❌ Stay away | High slippage, distorted indicators |

---

## VII. What Market Can This Strategy Make Money In?

### 7.1 Core Logic: The Trend Pullback Hunter

Schism6 is a **trend pullback strategy**. Its profit philosophy:

> **"Big timeframe strong + Small timeframe pullback = Golden entry point"**

- **Multi-Timeframe**: 1-hour for direction, 5-minute for entry
- **Support Entry**: Uses ADR to calculate support zones, not blind buying
- **Dynamic Risk Control**: Gives trends enough time to develop

### 7.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English |
|-------------|--------|---------------|
| Slow Bull Trend | ⭐⭐⭐⭐⭐ | Pullbacks are adding opportunities, strategy matches perfectly |
| Moderate Oscillation | ⭐⭐⭐☆☆ | Can profit but fees hurt, patience for breakout |
| Sustained Decline | ⭐⭐☆☆☆ | RSI strength fails, buying halfway down the slide |
| Extreme Volatility | ⭐☆☆☆☆ | Indicators jumping around, slippage exploding, stay away |

**One Line Summary**: Use in bull pullbacks, hide in bear oscillations.

---

## VIII. Want to Run This Strategy? Check These Configs First

### 8.1 Trading Pair Configuration

| Configuration | Recommended | Comment |
|--------------|-------------|---------|
| startup_candle_count | 72 | Need enough historical data for indicators |
| inf_timeframe | 1h | Can try 4h |
| stoploss | -0.10 | Default, depends on your risk tolerance |

### 8.2 Hardware Requirements (Important!)

This strategy queries database every time, has VPS requirements:

| Trading Pairs | Min Memory | Recommended | Experience |
|--------------|-----------|-------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 11-30 pairs | 4GB | 8GB | Decent |
| 30+ pairs | 8GB | 16GB | Need good machine |

**Warning**: With many pairs, `populate_trades` becomes a performance bottleneck.

### 8.3 Backtesting vs Live

**Here's the catch**: Backtesting returns empty data from `populate_trades`, so:
- Add-on logic won't trigger
- Slot management logic won't execute
- Dynamic stop-loss only relies on ROI table

**Recommended Process**:
1. Backtest to verify basic logic first
2. Dry-run for a few days to see add-on effects
3. Small capital live verification
4. Gradually increase position

**Don't go all-in from the start** - backtesting and live are quite different for this strategy!

---

## IX. Easter Egg: The Strategy Author's "Little Details"

Look carefully at the code, you'll find some interesting designs:

1. **TTLCache**: Current price cached for 5 minutes
   > "Don't call API too often, exchange will ban you"

2. **Order Timeout Cancel**: Cancel if price deviates 1%
   > "Too much slippage? Not doing it, principle matters"

3. **Entry Confirmation**: Same 1% deviation rejection
   > "Limit order means limit price, don't try to trick me"

4. **ignore_roi_if_buy_signal**: Ignore ROI when buy signal exists
   > "Forget ROI, adding opportunity is here!"

---

## X. Summary: How Good Is This Strategy?

### One-Line Verdict
> "Like an experienced short-term trader, has big-picture view, knows risk control, and adjusts dynamically."

### Who Should Use It?
- ✅ Experienced quant developers (can understand code logic)
- ✅ Traders familiar with trend pullback strategies
- ✅ People with time to watch and optimize parameters
- ✅ Investors who understand "time for space"

### Who Shouldn't Use It?
- ❌ Newbie beginners (too many parameters, discouraging)
- ❌ Those only looking at backtests (can't run add-on logic)
- ❌ Those wanting passive income (needs continuous optimization)
- ❌ Those trading in sustained decline markets (buying halfway down)

### My Recommendation
1. **Understand First**: Figure out what RMI, ADR, linear growth functions are
2. **Then Backtest**: Verify basic entry/exit logic
3. **Then Dry-Run**: See add-on and slot management effects
4. **Finally Live**: Start small, gradually increase

---

## XI. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting Looks Great, Live Needs Caution

Schism6 is elegantly designed - but there's a trap:

> **Because add-on logic can't run in backtesting, live performance may differ greatly from backtesting.**

Simply put: **Backtesting only shows basic logic, add-ons are the strategy's soul.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Slow database queries**: Many pairs will lag
- **Dynamic parameter drift**: Holding time calculation may have deviations
- **Slippage risk**: 5-minute level has high volatility
- **API rate limiting**: Frequent price queries may get blocked

### My Suggestion (Honest Truth)

```
1. Start with small capital, no more than 10% of total position
2. Run a few pairs first, don't be greedy
3. Check logs daily, understand strategy decisions
4. Record every add-on and stop-loss trigger
5. Fine-tune parameters based on live performance
```

**Remember**: No matter how good the strategy, the market teaches lessons without warning. Test lightly, staying alive is most important!

---