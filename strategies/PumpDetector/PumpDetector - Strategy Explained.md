# PumpDetector Strategy: The J-Line Bottom Fisher

> **Nickname**: The Bottom-Fishing Expert  
> **Job**: Short-term trader specializing in picking up bargains in oversold zones  
> **Timeframe**: 5 Minutes (Ultra Short-Term)

---

## I. What is This Strategy?

Simply put, **PumpDetector** is:

- A strategy that keeps staring at the J-line of the KDJ indicator
- Waits to bottom-fish when J-line drops below 0
- Runs when J-line rises above 90 or starts turning down

It's like an old man fishing - doesn't move until the fish bites (J crosses above 0), then immediately pulls the rod, and reels in when the fish is full (J above 90) 🎣

---

## II. Core Configuration: Basically "Bottom-Fish and Run"

### Stop-Loss Rules

```
Hard stop-loss: Accept defeat at 10% loss
Trailing stop: NOT enabled!
```

**Translation**: This strategy relies on a single 10% stop-loss for protection, no trailing stop nonsense. Either profit or lose 10% and leave, clean and simple.

### Other Settings

```
Timeframe: 5 minutes (quick in and out)
Sell signal: ON (has active selling)
Sell only when profitable: ON (don't sell at a loss)
```

**Translation**: 5 minutes per candle, suitable for intraday short-term. Has active sell signals, not the type that holds to death.

---

## III. The Only Buy Condition: Simple and Direct

This strategy has only one buy condition, not like other strategies with fancy stuff:

### 🎯 J-Line Crosses Above 0

**Core Logic**: J value rises from negative past 0, meaning oversold rebound is starting

**Plain English**:
> "When J-line drops below 0, the market is overly panicked. Once it bounces back, that's a bottom-fishing opportunity!"

**Code snippet**:
```python
J-line crosses above 0
AND Volume > 0
```

**Interpretation**:
- What is J-line? The most sensitive line in the KDJ indicator
- J can be negative (more sensitive than K and D)
- J crossing above 0 = rebounding from extreme oversold
- This is the legendary "dropped too much, time to bounce"

---

## IV. What is J-Line? A Quick Guide for Beginners

KDJ indicator has three lines:

| Line | Calculation | Characteristic |
|------|-------------|----------------|
| K | Fast line | Quick response |
| D | Slow line | Slow response, for confirmation |
| J | 3K - 2D | Most sensitive, can go out of range |

**J-Line's Special Powers**:
- K and D can only wiggle between 0-100
- J can drop to negative (-20, -30 are possible)
- J can rise above 100 (120, 150 are not unheard of)

**So**:
- J < 0: Market extremely panicked, should rise soon
- J > 100: Market extremely greedy, should fall soon
- PumpDetector just watches for J < 0 opportunities

---

## V. Sell Logic: Two Escape Routes

The strategy designed two sell signals, whichever triggers first, you run:

### 🏃 Route #1: J-Line Crosses Above 90

```python
J-line crosses above 90
```

**Plain English**:
> "J-line hit 90, entering extreme overbought zone, might pull back soon, run first!"

### 🏃 Route #2: J-Line Crosses Below K-Line (and J > 50)

```python
J-line crosses below K-line
AND J > 50
```

**Plain English**:
> "J-line started turning down, death cross! And still in mid-to-high zone (>50), run before it drops more!"

### Sell Signal Summary Table

| Signal | Trigger Condition | Plain English Translation |
|--------|------------------|---------------------------|
| #1 | J crosses above 90 | Rose too much, should pull back |
| #2 | J crosses below K with J>50 | Momentum weakening, starting to fall |

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Time)

1. **Simple and Clear Signals**: One entry, two exits, no confusion
2. **Focused on Bottom-Fishing**: Only acts in oversold zones, doesn't chase highs
3. **Active Sell**: Has its own sell signals, not the hold-to-death type
4. **Good for Short-Term**: 5-minute timeframe, intraday trader's dream

### ⚠️ Cons (Complaint Time)

1. **Few Entry Opportunities**: J-line crossing above 0 doesn't happen often, might miss moves
2. **No Trailing Stop**: Can't automatically lock in profits after making money
3. **Hardcoded Parameters**: 18, 4, 4 are written in code, need to edit code to change
4. **Some Code is Unused**: Calculated var2, var3, var7... and never used them

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Oscillating Downtrend | ✅ Use heavily | J-line frequently drops negative, many bottom-fishing opportunities |
| Quick Pullback | ✅ Recommended | Great time to catch rebounds |
| Trending Up | ❌ Don't use | J-line stays high, can't buy in |
| Low Volatility Sideways | ❌ Don't use | No J<0 opportunities |

---

## VIII. Summary: How's This Strategy?

### One-Sentence Review
> "A simple and direct bottom-fishing strategy - buy when J drops below 0, sell when it hits 90 or turns, quick in and out."

### Who's It For?
- ✅ Short-term trading enthusiasts
- ✅ Bottom-fishing lovers
- ✅ Technical indicator believers
- ✅ People who don't want frequent trades

### Who's It NOT For?
- ❌ Trend followers
- ❌ High chasers
- ❌ People who need frequent signals
- ❌ Newbies who don't understand KDJ

### My Recommendations
1. **Use in oscillating markets**: This strategy has almost no signals in trending markets
2. **Can tweak entry threshold**: J crossing -5 or 5 can also be tried
3. **Add trailing stop**: Prevent giving back profits
4. **Multiple coins diversification**: Since signals are few, watch more pairs

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Oversold Rebound

PumpDetector is a **bottom-fishing rebound strategy**. Its money-making philosophy is:

> "Extremes reverse - when J-line drops to negative, panic is excessive, rebound is just a matter of time."

**Its Money-Making Philosophy**:
- **Oversold Capture**: J < 0 means market panic is excessive
- **Rebound Confirmation**: J crossing above 0 means reversal starting
- **Active Exit**: Leave when gained enough or turned, don't be greedy

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English Explanation |
|:-----------|:-------|:--------------------------|
| 📈 Trending Up | ⭐☆☆☆☆ | J-line stays at 80-100 or higher, can't buy in at all |
| 🔄 Oscillating Market | ⭐⭐⭐⭐⭐ | This is the main battlefield! J-line repeatedly crosses 0, many bottom-fishing opportunities |
| 📉 Trending Down | ⭐⭐☆☆☆ | J might stay in negative zone for a long time, catching falling knives |
| ⚡ High Volatility | ⭐⭐⭐⭐☆ | High volatility, J-line swings big, many bottom-fishing opportunities |

**One-Sentence Summary**: Oscillating markets are its home turf, go around during trending markets.

---

## X. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Recommended | Notes |
|------------|-------------|-------|
| Timeframe | 5 minutes | Don't change, this strategy is designed for short-term |
| Stop Loss | -0.10 | Can relax to -0.15 |
| Number of Pairs | 10-20 | Few signals, watch more coins |

### 10.2 Key Config File Settings

```yaml
# Stop loss setting
stoploss: -0.10

# Timeframe
timeframe: 5m

# Optional optimizations
trailing_stop: true          # Recommend enabling
trailing_stop_positive: 0.02 # Start trailing at 2% profit
trailing_stop_positive_offset: 0.05 # Only activate after 5% profit
```

### 10.3 Hardware Requirements

This strategy has moderate computational needs:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|---------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-30 pairs | 4GB | 8GB | Comfortable |
| 30+ pairs | 8GB | 16GB | No pressure |

### 10.4 Backtest vs Live

1. 5-minute timeframe might show many signals in backtesting
2. Live trading needs to consider slippage and execution delay
3. J-line changes fast, might miss optimal price in live trading

**Recommended Flow**:
1. Backtest first to get a feel
2. Paper trade for a few days
3. Small position live test
4. Confirm stability before scaling up

**Don't go all-in right away**, short-term strategies need more breaking in!

---

## XI. Bonus: The Author's "Little Tricks"

Look carefully at the code, you'll find some interesting things:

1. **Code Has Redundancy**
   > Calculated var2, var3, var7, var9... and never used them in buy/sell, probably "leftovers" from development

2. **Parameters From TradingView**
   > Strategy header shows source: `https://fr.tradingview.com/script/vDX9m7PJ-L2-KDJ-with-Whale-Pump-Detector/` - translated from TradingView script

3. **What is XSA?**
   > Custom weighted moving average function, more sensitive than regular SMA - author probably thought standard moving averages weren't enough

4. **"Whale Pump Detector"?**
   > Original script is named "Whale Pump Detector" - claims to detect big money entering, but it's just KDJ bottom-fishing 😂

---

## XII. Final Words

### One-Sentence Review
> "A simple and clear bottom-fishing strategy - buy when J is negative, sell at 90 or when turning. Few signals but clear."

### Who's It For?
- ✅ Short-term traders
- ✅ Bottom-fishing enthusiasts
- ✅ KDJ indicator believers
- ✅ People who don't need daily trades
- ✅ People willing to wait for opportunities

### Who's It NOT For?
- ❌ Trend followers
- ❌ Buy-high-sell-higher types
- ❌ People who need to trade every day
- ❌ Newbies who don't understand technical indicators
- ❌ People wanting to make money in bull markets

### Manual Trader Recommendations

The J-line usage in this strategy can be directly borrowed:
- J < 0: Watch, prepare to bottom-fish
- J crosses above 0: Confirm entry
- J > 90 or death cross: Consider exiting
- Safer with other confirming indicators

---

## XIII. ⚠️ Risk Reminder Again (Must Read)

### Backtesting Looks Great, But Be Careful in Live Trading

PumpDetector's logic is simple and clear - but there's a trap:

> **The simpler the signal, the easier it is to be "targeted" by the market. When everyone is waiting for J-line to cross above 0, the market might not cooperate.**

Simply put: **Signals everyone knows often don't work.**

### Hidden Risks of Short-Term Strategies

In live trading, this strategy might cause:
- **Missing Moves**: J-line crossing above 0 might be rare, missing big moves
- **Catching Falling Knives**: J-line can stay in negative zone, bottom-fishing too early
- **Slippage Loss**: 5-minute timeframe changes fast, live execution might not be ideal
- **Frequent Stop-Losses**: Failed bottom-fishing, repeatedly triggering 10% stop-loss

### My Honest Recommendations

```
1. Use in oscillating markets, avoid trending markets
2. Diversify across multiple coins, since signals are few
3. Stop-loss can be appropriately relaxed
4. Add trailing stop to lock profits
5. J-line entry threshold can be adjusted
```

**Remember**: J-line bottom-fishing makes sense, but the market never follows the script. Light position testing, staying alive is most important! 🙏

---

**Final Reminder**: The strategy is called "Whale Pump Detector", sounds fancy, but it's just KDJ bottom-fishing. Don't be fooled by the name, the logic is simple. But simple doesn't mean ineffective - the key is using it in the right scenario!