# SMAIP3 Strategy: The Trend Pullback Sniper

> **Nickname**: MA Deviation Hunter  
> **Profession**: Trend Pullback Sniper + Parameter Optimization Expert  
> **Timeframe**: 5 minutes

---

## I. What Is This Strategy?

Simply put, **SMAIP3** is:
- Specifically buys pullbacks in uptrends
- Uses MA deviation to decide buy/sell points
- Auto-detects "bad trading pairs" to avoid risk
- Parameters can be auto-optimized through Hyperopt

It's like **waiting for a car to slow down on the highway before getting on** - doesn't chase highs, only enters on pullbacks! 🎯

---

## II. Core Configuration: "Wait for Pullback Before Buying"

### Profit-Taking Rules (ROI Table)

```
0 minutes   → Run with 13.5% profit (aggressive)
35 minutes  → Run with 6.1% profit
86 minutes  → Run with 3.7% profit
167 minutes → Run at break-even
```

**Translation**: Wants 13.5% right off the bat, over time break-even is fine too. Typical "take any profit and run" type.

### Stop-Loss Rules

```
Fixed stop-loss: -33.1% (Very wide!)
Trailing stop: Activates after 9.8% profit
Trailing trigger: When profit pulls back to 15.9%
```

**Translation**:
- Stop-loss is very wide, gives plenty of volatility room
- Starts trailing after making 9.8%
- Sells when profit pulls back to 15.9%
- Gives price plenty of "breathing room"

---

## III. Buy Conditions: 5 Conditions, All Required

This strategy's buy conditions are as **strict as airport security**:

### 🎯 Condition #1: Trend Is Up

```python
dataframe['ema_50'] > dataframe['ema_200']
```

**Plain English**:
> "Short-term MA (50-period) is above long-term MA (200-period), trend is up!"

### 📈 Condition #2: Price Above Long-term MA

```python
dataframe['close'] > dataframe['ema_200']
```

**Plain English**:
> "Price is standing above the 200-period MA, not in a downtrend!"

### 🚫 Condition #3: Not a "Bad Trading Pair"

```python
dataframe['pair_is_bad'] < 1
```

**Plain English**:
> "This coin isn't crashing! If it dropped over 13% in the last 12 candles or 7.5% in the last 6 candles, I'm not buying!"

### 📉 Condition #4: Price Below Deviation MA

```python
dataframe['close'] < dataframe['ma_offset_buy']
```

**Plain English**:
> "Price has pulled back, now 3.2% below the MA, time to buy!"

### 🔊 Condition #5: Has Volume

```python
dataframe['volume'] > 0
```

**Plain English**:
> "Not a dead coin, someone is trading."

---

## IV. Sell Logic: Simple and Direct

This strategy's sell logic is much simpler than the buy:

### Sell Condition: Price Above Deviation MA

```python
dataframe['close'] > dataframe['ma_offset_sell']
```

**Plain English**:
> "Price rose 7% above the MA, sell!"

**Critique**: Buy has 5 conditions, sell has only 2 (price + volume), not symmetrical at all 😅

---

## V. Protection Mechanism: Three Layers of "Safety Net"

| Protection Type | Function | Plain English |
|-----------------|----------|---------------|
| Fixed stop-loss -33.1% | Run if losing too much | "Maximum 33% loss, too painful to continue" |
| Trailing stop | Follow the rise when profitable | "Start watching closely after 9.8% profit" |
| Bad pair detection | Avoid crashing coins | "I don't touch crashing coins" |

**Critique**:
- 33% stop-loss is really wide... some coins drop 33% and are dead
- But gives enough volatility room, not easily shaken out

### The Genius of Bad Pair Detection

```
Detection Logic:
├── 12-period ago open price vs current price
│   └── Drop ≥ 13% → Mark as "bad trading pair"
└── 6-period ago open price vs current price
    └── Drop ≥ 7.5% → Mark as "bad trading pair"
```

**Plain English**:
> "If this coin dropped 13% in the last 12 candles or 7.5% in the last 6 candles, it's crashing, I'm not buying!"

---

## VI. This Strategy's "Personality"

### ✅ Pros (Praise Section)

1. **Strict Trend Confirmation**: EMA50/200 dual filtering, no counter-trend trading
2. **Pullback Buying**: Doesn't chase highs, waits for pullbacks
3. **Bad Pair Filtering**: Auto-avoids crashing coins, this design is clever
4. **Precision Trailing Stop**: Doesn't trail immediately on profit, gives volatility room
5. **Optimizable Parameters**: Hyperopt can auto-find optimal parameters

### ⚠️ Cons (Critique Section)

1. **Stop-Loss Too Wide**: 33% stop-loss, some coins are dead after 33% drop
2. **Few Buy Signals**: 5 conditions all need to be met, signals are rare
3. **Sell Too Simple**: Just one deviation sell, no multiple confirmations
4. **Target Too Aggressive**: 13.5% target is a bit greedy
5. **Needs Optimization**: Default parameters may not suit your trading pairs

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Uptrend pullback | ✅ Use it! | This is its home turf, pullback buying works best |
| One-way rally | ⚠️ Might miss | Trend confirmation takes time, might not get pullback |
| Sideways oscillation | ⚠️ Few signals | Trend filter filters out most signals |
| One-way downtrend | ❌ Don't use | Trend filter prevents buying altogether |

---

## VIII. Summary: How's This Strategy Really?

### One-Liner Evaluation
> "Textbook trend pullback buying strategy, bad pair detection is clever, but stop-loss is too wide."

### Who Should Use It?
- ✅ Traders who like buying pullbacks, not chasing highs
- ✅ Players who have time for Hyperopt optimization
- ✅ People who can accept wide stop-losses
- ✅ People who want to trade pullbacks in trending markets

### Who Shouldn't Use It?
- ❌ People who like chasing rallies
- ❌ People who set tight stop-losses
- ❌ People who want to make money in sideways markets
- ❌ People who don't have time to tune parameters

### My Recommendations
1. **Do Hyperopt optimization first**: Default parameters may not be optimal
2. **Adjust stop-loss**: 33% is too wide, suggest 15-25%
3. **Lower initial target**: 13.5% is greedy, adjust to 8-10% is more realistic
4. **Add trend indicator**: Can add ADX to confirm trend strength

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Trend Pullback Buying

SMAIP3 strategy is a **trend-following + pullback buying strategy**. About 150 lines of code, clean and efficient.

**Its Money-Making Philosophy**: **Go with the trend, enter on pullbacks**

- **Trend Confirmation**: EMA50 above EMA200, confirms uptrend
- **Position Confirmation**: Price above EMA200, not downtrend
- **Pullback Buy**: Price below deviation MA, buy on pullback
- **Risk Filter**: Detect bad pairs, avoid crashing coins
- **Deviation Sell**: Price above deviation MA, take profit

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:------------------|:--------------------------|
| 📈 Uptrend pullback | ⭐⭐⭐⭐⭐ | This is its home turf! Waiting for pullback to buy works best |
| 🔄 Sideways oscillation | ⭐⭐⭐☆☆ | Trend filter filters out signals, basically no trades |
| 📉 One-way downtrend | ⭐☆☆☆☆ | Trend filter prevents buying, smartly avoided |
| ⚡️ High volatility | ⭐⭐☆☆☆ | Bad pair detection might be too sensitive, missing opportunities |

**One-Liner Summary**: Use SMAIP3 for uptrend pullback markets, forget about oscillating or downtrending markets!

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Critique |
|-------------------|------------------|----------|
| Number of pairs | 5-20 | Too few = fewer signals |
| Volatility | Medium-high | Volatile coins have pullback opportunities |
| Liquidity | Must be good | Otherwise slippage eats profits |

### 10.2 Hyperopt Parameter Explanation

```python
# Buy Parameters
base_nb_candles_buy = 18   # MA period, optimizable
low_offset = 0.968         # Deviation coefficient, smaller = earlier buy
buy_trigger = "EMA"       # SMA or EMA

# Sell Parameters
base_nb_candles_sell = 55  # MA period, optimizable
high_offset = 1.07        # Deviation coefficient, larger = longer hold
sell_trigger = "EMA"      # SMA or EMA

# Risk Parameters
pair_is_bad_1_threshold = 0.13  # 12-period drop threshold
pair_is_bad_2_threshold = 0.075 # 6-period drop threshold
```

### 10.3 Hardware Requirements

This strategy doesn't need much computation, hardware requirements are low:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Runs easily |
| 10-50 pairs | 4GB | 8GB | No problem |

### 10.4 Backtesting vs Live Trading

**Be careful with Hyperopt-optimized parameters!**

**Recommended Process**:
1. Do Hyperopt optimization with historical data
2. Validate parameter effectiveness with out-of-sample data
3. Run paper trading for a week
4. Small capital live test
5. Continuously monitor and adjust

**Don't go all-in from the start**, optimized parameters might be overfitted!

---

## XI. Bonus: The Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **Bad pair detection is a good design**
   > "I don't touch crashing coins, this detection logic is simple but effective 👍"

2. **Trailing stop is precisely designed**
   > "Doesn't trail immediately on profit, waits until 9.8% to start, gives plenty of volatility room"

3. **Buy is complex, sell is simple**
   > "Buy has 5 conditions, sell has only 2... maybe author wants to buy carefully, sell happily?"

4. **Stop-loss is set a bit wide**
   > "33% stop-loss, this is for altcoins right? Main coins probably don't need this wide 😅"

5. **Lots of Hyperopt parameters**
   > "8 optimizable parameters, enough to tune all kinds of variations"

---

## XII. Final Words

### One-Liner Evaluation
> "Steady trend pullback buying strategy, bad pair detection is clever, but stop-loss and target need adjustment."

### Who Should Use It?
- ✅ Traders who like buying pullbacks, not chasing highs
- ✅ People who have time for parameter optimization
- ✅ Players who can accept wide stop-losses
- ✅ 5-minute timeframe short-term traders

### Who Shouldn't Use It?
- ❌ People who like chasing rallies
- ❌ People who set tight stop-losses
- ❌ People who want to make money in sideways markets
- ❌ People who don't have time to tune parameters

### Manual Trader Recommendations

If you trade manually, you can reference this logic:
- Wait for EMA50 to cross above EMA200, confirm uptrend
- Consider buying when price pulls back near EMA50
- Avoid coins that crashed in short time
- Set stop-loss properly (suggest 15-20%), don't be greedy

---

## XIII. ⚠️ Risk Emphasis Again (Must Read This Part)

### The Trap of Hyperopt Optimization

SMAIP3 is a **parameter-optimized strategy** - but there's a trap:

> **Optimized parameters might be "memorizing answers" - performing great on historical data but not necessarily effective in the future.**

Simply put: **Doing well on past tests doesn't mean you'll pass the real exam**

### Risk of Wide Stop-Loss

33% stop-loss looks like it gives enough room, but also has risks:
- **Capital management difficulty**: Single loss can be huge
- **Mental challenge**: Watching 20% floating loss is painful
- **Might miss stop-loss**: Drop too fast might blow through

### Hidden Risks in Live Trading

In live trading, watch out for:
- **Bad pair detection sensitivity**: Might miss some opportunities
- **Trend judgment lag**: EMA confirmation takes time
- **Can't buy pullback**: Might never get the pullback

### My Recommendations (Honest Truth)

```
1. Adjust stop-loss to 15-25%, don't use 33%
2. Adjust initial target to 8-10%, don't be greedy for 13.5%
3. Validate optimized parameters with out-of-sample data
4. Monitor bad pair detection, might need to adjust thresholds
```

**Remember**: No matter how good the strategy, when the market teaches you a lesson, it won't give notice. Light position testing, survival is most important! 🙏