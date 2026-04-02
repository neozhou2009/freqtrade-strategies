# Schism Strategy: The "Tai Chi Master" of Bottom Fishing

> **Nickname**: Tai Chi Grandmaster, Bottom-Fishing Philosopher, Trend Riding Expert  
> **Profession**: Specializes in picking "fallen into place" entry points, then riding trends all the way  
> **Timeframe**: 5 minutes (main arena) + 1 hour (God's eye view)

---

## 1. What Is This Strategy?

Simply put, **Schism** is a strategy that:
- Doesn't chase highs, specializes in bottom fishing—but with a method
- Doesn't rush to sell after entering, holds on if the trend is good
- "Reads other people's faces"—senses other trades' status to decide whether to sell

Like **a bottom-fishing expert who checks the big picture before entering, watches the trend while in, and looks at overall positions when selling** 🎯

**One-sentence summary**:
> "I bottom fish, but I'm not brainless about it; I hold positions, but I don't stubbornly hold; I stop loss, but I stop loss with technique."

---

## 2. Core Configuration: Simply Put, "Layers of Defense"

### Take-Profit Rules (ROI Table)

```
Holding Time        Profit Target
──────────────────────────────────
Just bought          10% (being greedy)
After 15 minutes     5% (quick in and out)
After 30 minutes     2.5% (cooling down)
After 1 hour         1% (that's about right)
After 2 hours        0.5% (even mosquito meat counts)
After 24 hours       0% (just don't lose money)
```

**Translation**:
- New positions, first think about making big (10%)
- The longer time goes, the lower the target—**"If you're not trending, hurry up and rise. If not, I'm out"**
- After 24 hours, **"Fine, breaking even is okay too"**

### Stop-Loss Rules

```
Hard stop-loss: -40% (this is the bottom line)
Dynamic stop-loss: slowly tightens from -3% to 0%
```

**Translation**:
- **Hard stop-loss -40%**: This is the "life-saving charm", if it really crashes, accept it
- **Dynamic stop-loss**: Just opened position gives you -3% room, as time goes on it tightens, finally becomes "break-even stop-loss"

### Key Setting

```python
ignore_roi_if_buy_signal = True  # This is the soul!
```

**Translation**:
> "If I'm still sending buy signals, it means the trend is still there, so ignore ROI for now, keep holding!"

---

## 3. Two Buy Condition Groups: I've Categorized Them For You

This strategy's buy conditions come in two types: **New Position** and **Position Continuation**.

### 🎯 Type 1: New Position Buy (Bottom Fishing Signal)

**Trigger Condition**: Currently no position in this coin

**Core Logic**: Bottom fish, but don't blindly fish

**Plain English**:
> "Price has fallen near the 3-day low, but don't be extreme. RSI can't be too miserable (can't be below 30), momentum indicators need to show 'fallen about enough', only then I'll make my move."

**Specific Conditions**:
```
1. RSI_1h >= 30          → "1-hour RSI hasn't fallen to extreme oversold"
2. Price <= 3-day low + 80% * daily volatility range
                         → "Bottom fish, but leave some safety margin"
3. RMI downtrend confirmed → "Confirm looking for reversal during downtrend"
4. RMI-slow >= 20        → "Momentum not too weak"
5. RMI-fast <= 20        → "Short-term momentum needs to be low (ready to bounce)"
6. Momentum Pinball <= 50 → "Momentum pinball indicator can't be too crazy"
7. Has volume            → "Someone needs to be trading"
```

**Classic Lines**:
- "Bottom fish when it's 'fallen enough', not when it's 'fallen to bottom'"
- "I look at 1-hour RSI, don't trick me with 5-minute"

---

### 📈 Type 2: Position Continuation Buy (Trend Confirmation Signal)

**Trigger Condition**: Currently have position in this coin

**Core Logic**: Confirm the trend is still there, don't let ROI interrupt

**Plain English**:
> "Since I'm already in position, let's see if the trend is still there. If still rising, ROI can wait, keep holding!"

**Specific Conditions**:
```
1. RMI uptrend confirmed      → "Trend still rising"
2. Current profit > peak profit * dynamic factor
                         → "Profit factor"—higher RMI means lower profit requirement
3. RMI-slow >= dynamic threshold → "Threshold grows with time: starts at 30 after 180 mins, reaches 70 after 720 mins"
```

**Dynamic Factor Calculation**:
```python
profit_factor = 1 - (rmi_slow / 400)
# rmi = 30 → factor = 0.925
# rmi = 80 → factor = 0.80
```

**Plain English Translation**:
- Higher RMI (stronger trend) means lower profit requirement
- **"Trend is this good, earning less is fine, keep holding!"**

---

## 4. Protection Mechanisms: 4-Layer "Anti-Stupid" Design

Each buy condition comes with a set of protection parameters, like **4 circuit breakers**:

| Protection Type | Function | Plain English |
|----------------|----------|----------------|
| **Hard stop-loss** | Cut at -40% | "Fall to -40% and I accept my fate, survival first" |
| **Dynamic stop-loss** | -3% → 0% | "Longer holding time means tighter stop-loss" |
| **Order timeout** | Cancel if slippage > 1% | "Price running too fast, won't buy/sell" |
| **Entry confirmation** | Reject if slippage > 1% | "Confirm price one more time before ordering, don't get scammed" |

**Commentary**:
> Is this strategy afraid users will slip up? 4 layers of protection! But then again, with crypto volatility, extra protection is reassuring 🤣

---

## 5. Sell Logic: Even More Refined Than Buying

### 5.1 Tiered Take-Profit: How Much to Make Before Running

```
Holding Time        Profit Target
──────────────────────────────────
0 minutes          10%       → "Just got in hoping to double? No, 10% is enough"
15 minutes         5%        → "15 minutes in, 5% is fine too"
30 minutes         2.5%      → "Half hour in, 2.5% works"
...and so on...
24 hours           0%        → "A day in, breaking even is fine"
```

**But!** There's a super important setting:

```python
ignore_roi_if_buy_signal = True
```

**Plain English**:
> "If position continuation buy signal is still there, ROI can stand aside! I'll keep holding!"

### 5.2 Dynamic Stop-Loss: Know When to Admit Defeat

```
Stop-loss threshold changes:
- Just opened: -3% (give you some room)
- After 300 minutes: 0% (break-even stop-loss)
```

**Trigger Conditions**:
```
1. Current profit < dynamic threshold (-3% to 0%)
2. Hasn't hit hard stop-loss (-40%)
3. RMI downtrend confirmed → "Trend broken"
4. Has volume
5. If was ever profitable: RMI crosses below 50 → "Trend weakening"
   If never profitable: RMI crosses below 10 → "This coin sucks, accept fate"
```

**Plain English**:
- **"Short holding time, giving you -3% room; longer holding, break-even stop-loss"**
- **"If ever made money, use RMI 50 to judge trend weakening; if always losing, get out at RMI 10"**

### 5.3 Global Position Awareness: Reading Other People's Faces

This is Schism's most unique feature: **It looks at other trades' status!**

```python
if has other trades:
    if still have free slots:
        # More free slots means more willing to hold
        hold_pct = (1 / free_slots) * -0.04
        # 1 slot → other trades average profit >= -4% before selling
        # 4 slots → other trades average profit >= -1% before selling
    else:
        # Full positions! Only allow biggest loser to sell
        conditions += [I am the biggest loser]
```

**Plain English Translation**:
- **"When there's room, I look at how other trades are doing. If everyone's losing, wait a bit; if only I'm losing, consider stopping out."**
- **"No room left? Biggest loser goes out first, make room for new opportunities."**

---

## 6. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Section)

1. **Principled bottom fishing**: Not blind bottom fishing, but conditional and confirmed
2. **Trend riding**: Once in, if trend is good keep holding, won't easily be interrupted by ROI
3. **Global perspective**: Looks at all positions' overall state, not just "minding my own business"
4. **Plenty of protection**: 4 layers of protection mechanisms, slippage, stop-loss, timeout all covered
5. **Dynamic adjustment**: Stop-loss threshold, profit factor all dynamically change with time and trend

### ⚠️ Weaknesses (Complaint Section)

1. **Only works in live trading**: Can't use backtesting! `ignore_roi_if_buy_signal` and position continuation signals don't work in backtesting
2. **Stop-loss too wide**: -40% hard stop-loss, for conservative players this is too exciting
3. **Database dependent**: Needs to access database to query other trade status, if system crashes strategy goes dumb
4. **Many parameters**: 5 buy parameters, sell parameters... a bunch, bad optimization can lead to overfitting
5. **High computation**: Multi-indicator, multi-timeframe, multi-trade awareness, old machines might lag

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **Slow bull market** | Default configuration | Trend continuation mechanism dominates |
| **Choppy market** | Lower RSI threshold | Bottom fishing signals will trigger frequently, watch out for fees |
| **One-sided crash** | Use with caution! | Bottom fishing signals may trigger too early, wide stop-loss is risky |
| **High volatility coins** | Expand ADR | Adapt to larger volatility ranges |

---

## 8. Summary: How's This Strategy Really?

### One-sentence evaluation
> "This is a veteran live trader's strategy—principled bottom fishing, patient holding, skilled stop-loss, global decision making."

### Who should use it?
- ✅ Traders with Freqtrade live experience
- ✅ Aggressive players who can accept -40% stop-loss
- ✅ People who like bottom fishing but don't want to "catch falling knives"
- ✅ Players who can handle database and system ops

### Who shouldn't use it?
- ❌ Newbie beginners (strategy logic complex, only for live trading)
- ❌ Conservative players (-40% stop-loss too exciting)
- ❌ People who only want to backtest to verify (core features don't work)
- ❌ Players with low-spec VPS (high computation overhead)

### My recommendation
1. **dry_run for two weeks first**: Familiarize yourself with strategy behavior, don't go live immediately
2. **Start with small positions**: Run 1-2 trading pairs first, see how it performs
3. **Lower stop-loss**: If you can't accept -40%, you can change it to -20% yourself
4. **Optimize parameters**: Default parameters might be optimized for specific coins, don't use directly

---

## 9. What Market Can This Strategy Make Money In?

### 9.1 Core Logic: Bottom Fishing + Trend Riding + Global Coordination

Schism's money-making philosophy:

- **Principled bottom fishing**: Look at 1-hour RSI, look at 3-day price range, look at momentum indicators—not blind bottom fishing
- **Trend riding**: Once in, if trend is good keep holding, won't be interrupted by ROI
- **Global coordination**: Look at all positions' overall state, avoid misoperations when fully invested

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:------------------|:--------------------------|
| 📈 **Slow bull market** | ⭐⭐⭐⭐⭐ | "This strategy is made for slow bulls! Bottom fish, ride to the top" |
| 🔄 **Choppy market** | ⭐⭐⭐☆☆ | "Bottom fishing signals will trigger, but choppy back-and-forth might hurt from fees" |
| 📉 **One-sided crash** | ⭐⭐☆☆☆ | "Bottom fishing might catch falling knives, wide stop-loss is risky" |
| ⚡️ **Rapid rise/fall** | ⭐☆☆☆☆ | "Order protection might fail, high slippage risk, use with caution" |

**One-sentence summary**:
> "Rebound markets after oscillating declines are Schism's home turf; one-sided crashes and extreme volatility are its weak points."

---

## 10. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Commentary |
|-------------------|------------------|------------|
| `max_open_trades` | 3-5 | Coordinate with global position awareness, don't open too many |
| `stake_amount` | Equal allocation | Don't play favorites, treat each trade the same |
| `timeframe` | 5m | Native configuration, don't change |
| `inf_timeframe` | 1h | Information layer configuration, don't change |

### 10.2 Key Config File Settings

```yaml
# config.json key configurations
{
    "max_open_trades": 3,
    "stake_currency": "USDT",
    "stake_amount": "unlimited",  # or fixed amount
    "dry_run": true,              # dry_run first!
    "dry_run_wallet": 1000,       # simulated funds
    "stoploss": -0.40             # consistent with strategy
}
```

### 10.3 Hardware Requirements (Important!)

This strategy has significant computation, has requirements for VPS:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-10 pairs | 2 GB | 4 GB | Smooth |
| 10-30 pairs | 4 GB | 8 GB | Might be a bit laggy |
| 30+ pairs | 8 GB | 16 GB | Old machines will struggle |

**Warning**: Strategy needs database access to query other trade status, memory overhead is significant in multi-pair scenarios! 😅

### 10.4 Backtesting vs Live Trading

**Big Pitfall Warning**:
- `ignore_roi_if_buy_signal` and position continuation signals **only work in live trading/dry run**
- Cannot access `Trade.get_trades()` data during backtesting
- **Backtesting results may differ significantly from live performance**

**Recommended Workflow**:
1. First backtest to verify buy signal quality
2. Then dry_run to verify dynamic logic
3. Finally small position live trading
4. **Don't go all-in based on backtesting results!**

**Don't go all-in right away**, no matter how good the strategy, it needs to be磨合!

---

## 11. Bonus: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Position continuation signal's elegance**:
   > "You think I just want to bottom fish? No, I also want to ride trends! `ignore_roi_if_buy_signal = True` is my secret weapon."

2. **Dynamic stop-loss philosophy**:
   > "Give you room when just opened, tighten over time—this is punishment for 'gave you a chance but you didn't deliver'."

3. **Global position awareness wisdom**:
   > "I don't just look at myself—I look at all positions' states. Full positions? Biggest loser goes out first. Have room? Wait and see."

4. **Profit factor's mathematical beauty**:
   > `profit_factor = 1 - (rmi_slow / 400)` — Higher RMI means lower profit requirement. This is the power of trend.

---

## 12. The Very End

### One-sentence evaluation
> "Schism is a 'principled bottom fisher'—doesn't blindly bottom fish, doesn't stubbornly hold, stops loss with technique, makes decisions globally."

### Who should use it?
- ✅ Freqtrade players with live experience
- ✅ People who want to bottom fish but fear "catching falling knives"
- ✅ People who can handle complex logic and multi-trade coordination
- ✅ Players with decent VPS specs

### Who shouldn't use it?
- ❌ People who only want backtest verification (core features don't work)
- ❌ Conservative players (-40% stop-loss too exciting)
- ❌ Newbie beginners (strategy logic complex)
- ❌ Single trading pair players (global awareness meaningless)

### Manual Trader Recommendations

Schism's core concepts can be borrowed:
- **Momentum-confirmed bottom fishing**: Look for reversals during RMI downtrend, don't chase highs
- **Trend riding**: After entering, if trend is still there, don't rush to sell
- **Dynamic stop-loss**: Longer holding means tighter stop-loss
- **Global perspective**: Look at all positions' overall state, don't just stare at one

---

## 13. ⚠️ Risk Emphasis Again (Must Read This Section)

### Backtesting Is Beautiful, Live Trading Be Careful

Schism's historical backtesting performance is often **impressive**—but this has a trap:

> **Because core features (position continuation signals, global position awareness) don't work in backtesting, backtesting results may be seriously distorted!**

Simply put: **What backtesting shows is not the real strategy behavior.**

### Hidden Risks of Complex Strategies

During live trading, complex logic may lead to:
- **Database access latency**: Querying other trade status takes time, might be too slow in extreme markets
- **Order timeout failure**: Order book data lag, slippage protection might not work
- **Memory overflow**: Multi-pair scenarios, memory usage might exceed limits
- **Parameter overfitting**: Default parameters might be optimized for a certain period, might not apply to the future

### My Advice (Real Talk)

```
1. dry_run for at least 1-2 weeks first, observe strategy behavior
2. Small position live trading, initial capital not more than 10% of total
3. Stop-loss can be lowered to -20% first, consider relaxing after adapting
4. Monitor system resources, ensure VPS won't lag
5. Record trading logs, regularly review
```

**Remember**: No matter how good the strategy, the market will humble you without warning. Light position testing, survival is most important! 🙏