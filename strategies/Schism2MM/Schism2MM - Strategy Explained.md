# Schism2MM Strategy: The Trough Hunter

> **Nickname**: Trough Hunter, Rebound Harvester  
> **Job**: Trader who specializes in "buying the dip" after drops  
> **Timeframe**: 5 minutes (main battlefield) + 1 hour (big picture)

---

## 1. What Is This Strategy?

Simply put, **Schism2MM** is:
- A strategy that uses scipy scientific computing to find "price troughs"
- Specifically enters at the bottom when others panic
- Can even add positions! If you already have a position, you can buy more

Like an **experienced trader calmly picking up bargains during a market crash** 🏷️

---

## 2. Core Configuration: "Setting the Rules First"

### Take-Profit Rules (ROI Table)

```
Just bought: Run at 2.5% profit
After 10 minutes: Run at 1.5% profit
After 20 minutes: Run at 1% profit
After 30 minutes: Run at 0.5% profit
After 2 hours: No profit required, watch for signals
```

**Translation**: The longer you hold, the more zen you become. Sell signals have your back anyway.

### Stop-Loss Rule

```
Maximum loss: 10%
```

**Translation**: Lose 10% and you're out, no negotiation.

---

## 3. Buy Conditions: I've Categorized Them for You

This strategy's buy conditions come in two sets, I've grouped them into 2 categories:

### 🎯 Category 1: New Position (First Buy)

**Core Logic**: Large timeframe up + small timeframe down + trough detected

**In Plain English**:
> "Big brother (1 hour) is rising, little brother (5 minutes) is falling, and it's at the trough - time to pick up bargains!"

**Representative Conditions**:
1. 1h RSI >= 65 → "Big trend is upward"
2. Price <= 3-day low + 95% volatility → "Fell enough"
3. RMI downtrend → "Indeed falling"
4. Local trough detected → "This is the bottom"

**Classic Lines**:
- Condition #1: `1h_rsi >= 65` → "Big trend is solid, safe to buy the dip"
- Condition #2: `close <= 3d_low + 0.95*adr` → "Price is low enough, good margin of safety"
- Condition #4: `buy_signal == True` → "scipy says this is a trough, trust it!"

---

### 📈 Category 2: Add Position (Already Holding, Want to Buy More)

**Core Logic**: Held for over 3 hours + profit protection + trend upward

**In Plain English**:
> "Already held for 3 hours, still rising, might as well add some more!"

**Dynamic Threshold**:
```
RMI threshold = linearly grows from 30 to 70
(Longer you hold, higher the requirement)
```

**Classic Lines**:
- `rmi-up-trend == 1` → "Trend is up, adding in the right direction"
- `current_profit > peak_profit * factor` → "Previous profit still there, safe"
- `rmi-slow >= rmi_grow` → "Dynamic threshold reached, can add"

---

## 4. Protection Mechanisms: 4 Layers of "Safety Fuses"

Each buy condition comes with a set of protection parameters, like **four security doors**:

| Protection Type | Purpose | Plain English |
|----------------|---------|---------------|
| Fixed Stop-loss | Exit at 10% loss | "Lost too much, just run" |
| Dynamic Stop-loss | Higher requirements over time | "Held long enough without profit, leave" |
| Order Timeout | Cancel if price deviates 1% | "Price ran too fast, forget it" |
| Entry Confirmation | Reject if price deviates 1% | "Entry price wrong, better to miss it" |

This is like checking three generations of family history before a date, **extremely cautious** 🕵️

---

## 5. Sell Logic: Even Flashier Than Buy

### 5.1 Dynamic Stop-loss: How Much Loss Before Running

```
Held 0 minutes: Allow 3% loss
Held 150 minutes: Allow 1.5% loss
Held 300 minutes: Require profit
```

**Plain English**:
- Just bought: Small loss is fine, give some room for error
- Held for a while: You should be profitable by now, if not then leave

---

### 5.2 RMI Stop-loss Signal

| Scenario | RMI Threshold | Plain English |
|----------|--------------|---------------|
| Was profitable | RMI < 50 | "Rose but now falling back, protect profit and leave" |
| Never profitable | RMI < 10 | "Never got up, just take the loss and go" |

---

### 5.3 Portfolio Profit Management

This is the **most clever** part of this strategy - it considers **overall portfolio**:

```python
if has free slots:
    Other positions avg profit >= -free_slots * 0.01  # Small loss is okay
else:  # No free slots
    Only allow biggest loser to sell  # Make room for new opportunities
```

**Plain English**:
> "When there's room, be more lenient. When full, let the worst performer go first"

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Time)

1. **Scientific Bottom Fishing**: Uses scipy signal processing to find troughs, not guessing
2. **Can Add Positions**: Good market conditions allow scaling up, not wasting opportunities
3. **Dynamic Thresholds**: Stop-loss and add-position adjust over time, not rigid
4. **Portfolio Management**: Considers overall positions, not fighting alone

### ⚠️ Cons (Complaint Time)

1. **Too Complex**: scipy signal processing? Linear growth functions? Headache to learn
2. **Backtest Difficult**: Add-position logic, portfolio management can't be fully simulated in backtest
3. **Parameter Sensitive**: `order=100` extrema detection may fail in different markets
4. **Live Trading Only**: Many logics depend on `Trade` object, backtest won't work

---

## 7. Suitable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Oscillating Uptrend | Default parameters | Strategy designed for this |
| One-sided Downtrend | Don't use | Trend detection can't keep up, buying halfway down |
| High Volatility | Be careful | Extrema detection might get slapped |
| Sideways Oscillation | Observe | May trigger frequent stop-losses |

---

## 8. Summary: How's This Strategy Really?

### One-sentence Review
> "An advanced player using scientific methods to buy the dip, but only for oscillating uptrend markets."

### Who Should Use It?
- ✅ Technical types who know Python and signal processing
- ✅ Traders who like buying dips and rebound trading
- ✅ Players with live trading conditions for thorough testing
- ✅ Experienced traders who can handle complex code

### Who Shouldn't Use It?
- ❌ Newbies who get dizzy looking at code
- ❌ Players only doing backtesting (many logics won't run)
- ❌ Those who want to push hard in one-sided downtrends
- ❌ Lazy people looking for simple strategies

### My Suggestions
1. **Dry-run first**: Run in simulation for two weeks
2. **Understand scipy**: Learn how `argrelextrema` finds troughs
3. **Careful with parameters**: `order=100` may not fit all coins
4. **Watch the trend**: 1h RSI >= 65 is a hard requirement

---

## 9. What Market Can This Strategy Make Money?

### 9.1 Core Logic: Trough Rebound

Schism2MM is a **buy-the-dip strategy**. About 200 lines of code - what does that mean? Equivalent to **a short academic paper** 📚

**Its profit philosophy**: Precise entry during pullbacks in an uptrend

- **Scientific Extrema Detection**: scipy finds troughs, not guessing
- **Trend Filter**: 1h RSI ensures big direction is right
- **Dynamic Management**: Longer holding means higher requirements

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Performance Rating | Plain English Explanation |
|:-----------:|:-----------------:|---------------------------|
| 📈 Oscillating Uptrend | ⭐⭐⭐⭐⭐ | This is the strategy's home turf, pullback buy then sell on rise |
| 🔄 Sideways Oscillation | ⭐⭐⭐☆☆ | May repeatedly hit stop-losses, fees eat profits |
| 📉 One-sided Downtrend | ⭐⭐☆☆☆ | Trend filter can't keep up, buying halfway down the mountain |
| ⚡ High Volatility | ⭐⭐☆☆☆ | Extrema points jump around, stop-losses may get blown through |

**One-sentence Summary**: Makes money in oscillating uptrends, loses money in one-sided downtrends.

---

## 10. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Timeframe | 5m main + 1h info | Don't change to 1m, signals will be chaotic |
| `order` parameter | 50-150 | Use smaller values for high-volatility coins |
| Stop-loss | -0.08 ~ -0.12 | Adjust based on tolerance |

### 10.2 Hardware Requirements (Important!)

This strategy's computation is okay, but has scipy signal processing:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-30 pairs | 4GB | 8GB | Normal |
| 30+ pairs | 8GB | 16GB | Recommended |

**Warning**: scipy signal processing may eat memory with large data 😅

### 10.3 Backtest vs Live Trading

**Backtest Limitations**:
- `Trade.get_trades()` not available in backtest
- Add-position logic cannot be fully simulated
- Portfolio profit management fails

**Recommended Process**:
1. First understand the code logic
2. Dry-run for at least two weeks
3. Small capital live test
4. Observe add-position effects

**Don't go all-in from the start**, no matter how good the strategy, it needs breaking in!

---

## 11. Easter Egg: The Strategy Author's "Little Thoughts"

Looking carefully at the code, you'll find some interesting things:

1. **scipy Signal Processing**:
   > "Using scientific methods to find troughs is much more reliable than eyeballing it"

2. **Linear Growth Function**:
   ```python
   rmi_grow = linear_growth(30, 70, 180, 720, open_minutes)
   ```
   > "After holding 3 hours, RMI threshold slowly rises from 30 to 70, giving enough time for profit to fly"

3. **Portfolio Profit Management**:
   > "Lenient when there's room, let the worst performer go when full - this is veteran money management"

4. **1% Price Protection**:
   > "If entry price deviates more than 1%, don't play - better to miss than to be wrong"

---

## 12. Final Words

### One-sentence Review
> "Advanced strategy using scipy for scientific bottom-fishing, a money-making tool in oscillating uptrend markets."

### Who Should Use It?
- ✅ Quant players with technical skills
- ✅ Those who like buying dips and rebound style
- ✅ Have live testing conditions
- ✅ Rational types pursuing scientific methods

### Who Shouldn't Use It?
- ❌ Python newbies
- ❌ Players only doing backtesting
- ❌ Lazy people wanting simple strategies
- ❌ Warriors pushing hard in one-sided downtrends

### Manual Trading Suggestions
If you want to follow manually without a bot:
1. Add RMI(21,5) and RMI(8,4) indicators on TradingView
2. Set alerts for 1h RSI >= 65
3. Watch for local trough patterns
4. Set 10% stop-loss on entry

---

## 13. ⚠️ Risk Re-emphasis (Must Read)

### Backtest Looks Great, Live Trading Needs Caution

Schism2MM's backtest might **look okay** - but there's a trap:

> **Many core logics (add-position, portfolio management) can't run in backtest at all!**

Simply put: **Backtest can't test the real effect**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Add-position timing**: May miss the best add-position point
- **Portfolio management**: May misjudge across multiple coins
- **Extrema detection**: May fail when market structure changes
- **Slippage impact**: 5-minute timeframe is sensitive to slippage

### My Advice (Sincere Words)

```
1. Dry-run for at least two weeks, observe signal quality
2. Small capital live test for add-position effects
3. Watch if 1h RSI trend is accurate
4. Adjust order parameter for different coins
```

**Remember**: Scientific bottom-fishing is still bottom-fishing. How many have bought halfway down the mountain? Light position testing, survival is most important! 🙏

---