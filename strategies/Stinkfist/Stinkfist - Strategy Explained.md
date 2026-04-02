# Stinkfist Strategy: The "Deep Dive Hunter" for Volatile Markets

> **Nickname**: Deep Dive Hunter  
> **Specialty**: Volatile Market Bottom-Fishing Expert  
> **Timeframe**: 5 minutes (main) + 1 hour (auxiliary)

---

## I. What Is This Strategy?

Simply put, **Stinkfist** is:
- A "bottom-fishing" strategy that excels at finding opportunities in volatility
- Has dedicated position addition logic (the longer you hold, the higher the threshold)
- Comes with three layers of price protection
- Even has BTC and ETH exclusive versions

Like an **experienced deep dive hunter** 🤿 — observing from the surface (1-hour informative layer) to determine dive position, then diving into the water (5-minute execution) to catch prey. And this guy is extra cautious — checks safety equipment three times before diving!

---

## II. Core Configuration: "Steady Bottom-Fishing" in Plain Terms

### Take-Profit Rules (ROI Table)

```
Time         Profit Target
────────────────────
Immediate    5%
10 minutes   2.5%
20 minutes   1.5%
30 minutes   1%
12 hours     0.5%
24 hours     Close and leave
```

**Translation**: Just bought in? Target is 5% profit. The longer you hold, the lower the target — kind of like chasing a date, passion drops over time.

### Stop-Loss Rules

```
Stop-loss line: -40%
```

**Translation**: 40% hard stop-loss! That's very loose. Like your mom saying "come find me after losing 40%" — gives plenty of room for error. But if it actually triggers, it's gonna hurt 😅

---

## III. Buy Conditions: Two Scenarios, Two Logic Sets

This strategy has **two buy logic sets**, let me break them down:

### 🎯 Scenario 1: New Position (4 conditions must ALL be met)

**Core Logic**: Find opportunities near 3-day lows

**In Plain English**:
> "Wait for price to drop to the 3-day low + 80% volatility range area, momentum indicator shows oversold, consecutive decline starts to rebound, and moving averages form a golden cross — THEN dare to enter."

**4 Conditions Detailed**:

| Condition | Plain English Translation |
|-----------|--------------------------|
| Price Position | Price ≤ 3-day lowest + 80% daily volatility range (bottom-fishing zone) |
| Momentum Pinball < 30 | Momentum indicator shows oversold condition |
| Streak ROC > Lower Band | Rate of change starting to rebound |
| MA Cross == 1 | MA golden cross confirms trend reversal |

### 🔄 Scenario 2: Position Addition (Dynamic Growth Logic)

**Core Logic**: Decide whether to add based on holding time and profit

**In Plain English**:
> "Already bought? Then check the situation. The longer you hold, the higher the addition threshold (RMI grows from 30 to 70). And your current trade needs to be profitable to add — losing money? No addition for you!"

**Dynamic Threshold Table**:

| Holding Time | RMI Threshold | Addition Difficulty |
|--------------|---------------|---------------------|
| 0 minutes | 30 | Pretty easy |
| 3 hours | 50 | Medium difficulty |
| 6 hours | 60 | Pretty hard |
| 12 hours | 70 | Very hard |

---

## IV. Protection Mechanism: Three Layers of "Anti-Pitfall" Design

Every buy comes with three protection layers, like three insurance policies:

| Protection Type | Function | Plain English |
|-----------------|----------|---------------|
| Entry Price Protection | Reject when order price vs. current price deviation > 1% | "Don't try to slip me!" |
| Buy Timeout Check | Cancel order when price deviation > 1% | "Price changed? Don't want it!" |
| Sell Timeout Check | Cancel order when price deviation < 1% | "Price changed? Not selling!" |

Like going shopping:
1. **Before entering**: Ask price first, if current price is 1%+ higher than listed price, walk away
2. **After ordering**: If price changed again, just cancel the order
3. **When selling**: Same logic, prevent getting ripped off

---

## V. Sell Logic: "Run" Depending on Situation

### 5.1 Dynamic Stop-Loss: The Longer You Hold, The Tighter

```
Holding Time      Stop-Loss Threshold
─────────────────────────
0 minutes         -3%
300 minutes       0% (must be profitable to sell)
```

**Plain English**:
- Just bought: Allowed to lose 3% before running
- Held 5 hours: Must be profitable to sell (dynamic threshold becomes 0%)

This tells you: **The longer you hold, the stricter the stop-loss — don't stubbornly hold!**

### 5.2 Sell Signal Combination

| Condition | Plain English |
|-----------|---------------|
| RMI Trend Reversal | RMI trend is heading down |
| Profit Judgment | Run when RMI < 50 if profitable, RMI < 10 if not profitable |
| Global Position Management | Considers all positions when deciding to sell this one |

### 5.3 Global Perspective: This Strategy "Sees the Big Picture"

```python
# Strategy tracks all positions
other_trades = Number of other trades
avg_other_profit = Average profit of other trades
biggest_loser = Is this one the biggest loser?
free_slots = How many open slots left
```

**Plain English**:
> "This strategy looks at all your positions. If this one is the biggest loser, it'll handle it first. If there are still open slots, might wait a bit."

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Section)

1. **Cautious Bottom-Fishing**: Three price protection layers, not rushing at every low price
2. **Dynamic Adjustment**: Longer hold = higher threshold — prevents mindless adding
3. **Global Perspective**: Looks at all positions' comprehensive performance, not isolated judgment
4. **Exclusive Versions**: BTC and ETH have optimized parameter versions
5. **Informative Layer Assistance**: Uses 1-hour timeframe for auxiliary judgment, broader view

### ⚠️ Cons (Complaint Section)

1. **Stop-Loss Too Loose**: 40% stop-loss, really gonna hurt if triggered
2. **High Complexity**: Pile of custom indicators, hard to troubleshoot issues
3. **Position Addition Risk**: Adding during trend reversal may amplify losses
4. **Real-time Data Dependency**: Frequent price and orderbook fetching, high VPS requirements

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Volatile Uptrend | Recommended | This strategy is designed for volatility |
| Ranging Volatility | Recommended | Use informative layer to find entry points |
| One-sided Decline | Use Cautiously | Position addition logic may amplify losses |
| Low-volatility Sideways | Not Recommended | Lacks clear trend signals |

---

## VIII. Sub-strategy Versions: BTC and ETH Exclusive Optimization

### 🪙 Stinkfist_BTC (BTC Version)

```python
buy_params = {
    'inf-pct-adr': 0.91556,  # Higher entry threshold
    'mp': 66,                # Higher momentum threshold
}
use_sell_signal = False      # Disable sell signals
```

**Plain English**: BTC version is more "zen" — higher entry threshold, and simply disables sell signals, fully relying on ROI table to exit. Like "I won't actively sell, let the system sell for me."

### 💎 Stinkfist_ETH (ETH Version)

```python
buy_params = {
    'inf-pct-adr': 0.81628,  # Moderate entry threshold
    'mp': 40,                # Lower momentum threshold
}
trailing_stop = True         # Enable trailing stop
trailing_stop_positive = 0.014
trailing_stop_positive_offset = 0.022
```

**Plain English**: ETH version is more aggressive — lower entry threshold, and enables trailing stop, suitable for ETH's volatility characteristics.

---

## IX. What Market Can This Strategy Make Money?

### 9.1 Core Logic: Deep Digging for Volatility Opportunities

Stinkfist is a **volatile market bottom-fishing strategy**. Its money-making philosophy:

- **Informative Layer Observation**: Use 1-hour timeframe to see 3-day lows and volatility range
- **Dynamic Position Addition**: Longer hold = higher threshold — prevents mindless adding
- **Global Management**: Look at all positions' comprehensive performance
- **Price Protection**: Three layers of mechanism to prevent slippage

### 9.2 Performance in Different Markets (Human Version)

| Market Type | Rating | Plain English Explanation |
|-------------|--------|---------------------------|
| 📈 Volatile Uptrend | ⭐⭐⭐⭐⭐ | This is home turf! Use volatility to find pullback buying opportunities |
| 🔄 Ranging Volatility | ⭐⭐⭐⭐☆ | Strategy design intent, effective with informative layer |
| 📉 One-sided Decline | ⭐⭐☆☆☆ | Position addition logic may get you deeper and deeper |
| ⚡ Low-volatility Sideways | ⭐⭐☆☆☆ | Can't find signals, low capital utilization |

**One-sentence Summary**: Volatility is friend, one-sided decline is enemy!

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Number of Pairs | Start with 1-5 | Don't be greedy, complex strategy needs gradual approach |
| Timeframe | 5m + 1h | Don't change, this combination is intentional |
| max_open_trades | 3-5 | Leave room for position addition logic |

### 10.2 Hardware Requirements (Important!)

This strategy needs real-time price and orderbook data, has hardware requirements:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|-------------------|------------|
| 1-5 pairs | 2 GB | 4 GB | Smooth |
| 5-20 pairs | 4 GB | 8 GB | Okay |
| 20+ pairs | 8 GB | 16 GB | Watch for timeouts |

**Warning**: This strategy frequently calls API to get current prices, low-spec VPS may timeout!

### 10.3 Backtest vs. Live Trading

Live trading may differ from backtest:
- **Price Protection Logic**: Backtest can't fully simulate slippage protection
- **Position Addition Logic**: More sensitive in live trading
- **Global Position Management**: Backtest may not fully reflect

**Recommended Flow**:
1. Backtest with default parameters first
2. Then dry-run with single pair
3. Confirm price protection mechanism works normally
4. Gradually expand to multiple pairs

**Don't go all-in from the start**, no matter how good the strategy is, it needs磨合!

---

## XI. Easter Egg: Strategy Author's "Little Thoughts"

Looking closely at the code, you'll find some interesting things:

1. **Strategy Name from Tool Band's Song**:
   > "Stinkfist is Tool band's classic song, embodying the design philosophy of deep digging."

2. **All Custom Indicators Self-Implemented**:
   > "MA Streak, PCC, MAC all self-implemented, no external library dependency — this author is a hardcore player!"

3. **Cache Mechanism Uses TTLCache**:
   > "Price cached for 5 minutes, reduces API calls — this author is detail-oriented!"

---

## XII. Final Words

### One-Sentence Review
> "Deep dive hunter for volatile markets, triple protection + dynamic position addition + global perspective, but watch out for one-sided decline risk!"

### Who Is It For?
- ✅ Volatile market lovers
- ✅ Traders who like bottom-fishing
- ✅ People who can handle complex strategies
- ✅ Those with sufficient VPS resources

### Who Is It NOT For?
- ❌ One-sided bull market chasers
- ❌ People who like simple strategies
- ❌ Low-spec VPS users
- ❌ People who can't tolerate 40% stop-loss

### Manual Trading Recommendations
1. Use 1-hour timeframe to see 3-day lows
2. Wait for price to enter "bottom-fishing zone" (3-day low + 80% volatility)
3. Use RMI and moving averages to confirm trend
4. Set dynamic stop-loss, don't stubbornly hold

---

## XIII. ⚠️ Risk Emphasis Again (Must Read This Section)

### Backtest Looks Beautiful, Live Trading Be Careful

Stinkfist's historical backtest performance may look **great** — but there's a trap:

> **Complex strategies easily "fit" past market's optimal solution, but this doesn't guarantee future profits.**

Simply put: **Past report card doesn't equal final exam score!**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Price Protection Frequent Triggers**: Orders may keep getting cancelled during high volatility
- **Suboptimal Position Addition Timing**: Adding during trend reversal amplifies losses
- **Too Many API Calls**: Frequent price fetching may cause rate limiting

### My Recommendations (Honest Words)

```
1. Start testing from BTC or ETH exclusive versions
2. Initially only use 1-2 trading pairs
3. Set tighter stop-loss than 40% (like -20%)
4. Observe price protection trigger frequency
5. Confirm acceptable before scaling up
```

**Remember**: Volatile markets are opportunities, but also traps. No matter how good the strategy, the market won't give notice when teaching lessons. Light position testing, survival comes first! 🙏