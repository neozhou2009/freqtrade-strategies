# CofiBitStrategy: The Low-Key "Trend Bottom-Fishing Club"

> **Nickname**: Trend Bottom-Fishing Club, Cautious Veteran Driver
> **Profession**: Intraday Short-Term Trend Following Strategy
> **Timeframe**: 5 Minutes (5m)

---

## 1. What's This Strategy?

Simply put, **CofiBitStrategy** is:
- An intraday player checking the board every 5 minutes
- A trend follower, only trades markets with direction
- An oversold bottom-fishing club, specifically waits for price to drop to a good level before entering
- A cautious type, entry conditions are so many it's like doing a background check for marriage

Think of it as a **patient hunter** lurking on the trend hilltop, waiting until the prey (price) has fallen enough and the technical indicators all say "ready to act" — then calmly takes the shot 🎯

This strategy was shared by a Freqtrade community member called CofiBit — the typical "I don't chase highs, do whatever you want with the rally" kind of personality.

---

## 2. Core Settings: Basically "Staircase Take-Profit + Wide Stop-Loss"

### Take-Profit Rules (ROI Table)

```
Hold 0+ minutes    →  Make 10% and run
Hold 20+ minutes   →  Make 7% and run
Hold 30+ minutes   →  Make 6% and run
Hold 40+ minutes   →  Make 5% and run
```

**Translation**: Initially requires 10%, but as time passes the requirement gets lower — after all, a lot can happen overnight, take what you can get and secure profits. This is the classic "let profits run but also give yourself a safety net" design.

### Stop-Loss Rules

```
Stop-loss line: -25%
```

**Translation**: Tap out after losing a quarter. This stop-loss is quite loose, giving intraday fluctuations plenty of "room to run around," not easily shaken out by normal volatility. But it also means per-trade losses might sting a bit 😅

### Hyperparameters Overview

| Parameter | Default | Plain English |
|----------|---------|---------------|
| buy_fastx | 25 | Stochastic must be below 25 to buy (oversold zone) |
| buy_adx | 25 | ADX must be above 25 to open (must have trend) |
| sell_fastx | 75 | Stochastic above 75 runs (overbought zone) |

---

## 3. 5 Buy Conditions: I've Categorized Them For You

This strategy's entry conditions are a **Perfectionist's Dream** — must meet all 5 simultaneously before opening:

### 🎯 Category #1: Price Position (1 Condition)

**Core Logic**: Ensure not buying at the top

**Plain English**:
> "Open price must be below the 5-period EMA low — meaning price should be at the day's relatively low point, I'm not standing guard at the mountain top."

**Representative Condition**:
- **Condition #1**: `open < ema_low` → "Price must be low, I don't chase highs"

---

### 📈 Category #2: Momentum Indicators (3 Conditions)

**Core Logic**: Buy at golden cross in oversold zone

**Plain English**:
> "The stochastic must be in the oversold zone, and the K line must golden cross the D line — basically price has been beaten down to a low point, momentum is starting to strengthen, this is the time to bottom-fish."

**Representative Conditions**:
- **Condition #2**: `fastk crosses above fastd` → "Golden cross, momentum strengthening!"
- **Condition #3**: `fastk < 25` → "K value still in oversold zone, not overheated"
- **Condition #4**: `fastd < 25` → "D value also in oversold zone, double insurance"

---

### 🚀 Category #3: Trend Confirmation (1 Condition)

**Core Logic**: Only open positions in trending markets

**Plain English**:
> "ADX must be greater than 25 — meaning the market must have a clear direction, I'm not joining the chaos during sideways consolidation, saves me from getting slapped around."

**Representative Condition**:
- **Condition #5**: `adx > 25` → "Market has trend, not a scattered mess"

---

### 💡 Entry Logic One-Line Summary

**Low price + oversold golden cross + trend = Buy!**

Rock solid — belongs to the "veteran drivers understand caution" type.

---

## 4. Protection Mechanisms: Three "Firewalls"

Each entry condition comes with protection parameters, like wearing three layers of bulletproof vest for trading:

| Protection Type | Condition | Plain English |
|----------------|----------|---------------|
| **Trend Protection** | ADX > 25 | "No trend, no trade — sideways is a waste of time" |
| **Oversold Protection** | fastk < 25, fastd < 25 | "Must buy at low levels, never chase highs" |
| **Price Position Protection** | open < ema_low | "Must buy near support, not at the mountain top" |

The significance of these three firewalls:
1. Filters false signals from ranging markets.
2. Ensures not buying at high levels.
3. Only acts when trend is clear.

**Commentary**: Entry conditions are strict, but precisely because of this, false signals are few and win rate is higher. Signal frequency is low though — need patience 🤷

---

## 5. Exit Logic: Much Simpler Than Entry

### 5.1 Staircase Take-Profit: Exit Based on Profit

```
Just bought          →  Expecting 10%
After 20 minutes     →  7% is fine to run
After 30 minutes     →  6% is fine to run
After 40 minutes     →  5% is fine, secure profits
```

**Plain English**:
- **At entry**: High bar, won't leave without 10%
- **Time passes**: Requirement lowers, any profit is fine
- **Subtext**: "Profits must run, but can't be greedy either"

---

### 5.2 Two Scenarios That Trigger Selling (Either One)

| Scenario | Trigger Condition | Plain English |
|----------|------------------|---------------|
| **Price breaks high** | open ≥ ema_high | "Price broke through the day's high, about time to run" |
| **Indicator overbought** | fastk or fastd crosses above 75 | "KD indicators overheated, might cool down anytime, I'm out first" |

**Commentary**: Sell conditions are much simpler than entry — typical "careful entry, decisive exit" style.

---

### 5.3 Sell Signal Classic Lines

**Signal #1**: `open >= ema_high`
> "Price broke through the day's high, leaving now is not being greedy"

**Signal #2**: `fastk crosses 75` or `fastd crosses 75`
> "KD indicators overbought, overheated, I'm slipping out first"

---

## 6. Strategy "Personality"

### ✅ Pros

1. **Multi-Dimensional Filtering**: 5 conditions all must be met before opening — few false signals, high win rate
2. **Clear Logic**: Price position + momentum indicators + trend confirmation — combination is simple and clear
3. **Intraday Adaptation**: 5-minute level, suitable for cryptocurrency's high-volatility characteristics
4. **Adjustable Parameters**: Hyperparameters can fine-tune based on market environment, good flexibility
5. **Trend Following**: ADX filtering ensures trading only in trending markets, doesn't tangle with ranging markets

### ⚠️ Cons

1. **High Stop-Loss Risk**: -25% stop-loss, one bad trade could hurt significantly
2. **ADX Lag**: ADX responds slowly to trend changes, may miss best entry points
3. **Parameter Sensitivity**: Wrong parameter might flip from profit to loss, must be careful
4. **Sleeps in Ranging Markets**: No trend = no signals, anxious waiting during consolidation
5. **Tiring to Monitor**: 5-minute level, need to check the board frequently

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 **Uptrend Pullback** | Go for it! | Clear trend + pullback entry = optimal entry — made for this |
| 📉 **Downtrend Bounce** | Can try | Oversold rebound signals accurate, but watch stop-loss risk |
| 🔄 **Ranging Consolidation** | Better rest | ADX blocks most signals, low capital utilization |
| ⚡ **Unilateral Surge** | Not suitable | Too conservative at entry, may miss most of the rally |
| 😴 **Low-Volatility Market** | Don't use | Not enough fluctuation to trigger, strategy "hibernates" |

---

## 8. Summary: How Does This Strategy Really Stack Up?

### One-Line Verdict
> "A cautious intraday player's good choice: strict conditions, high win rate, but stop-loss stings."

### Who's It For?
- ✅ Intraday short-term veterans
- ✅ People who can accept max 25% loss per trade
- ✅ Bottom-fishing rebound hunters
- ✅ People with time to monitor (5-minute level)

### Who's It NOT For?
- ❌ Beginner newcomers: Stop-loss too big, easy to lose
- ❌ Long-term investors: Pure intraday strategy, holding for months you'll regret
- ❌ Chasers: This strategy never chases highs
- ❌ People without time to monitor: 5-minute level, need to watch the board

### My Recommendations
1. **Backtest first**: Run through historical data, see the results
2. **Then paper trade**: At least one month, verify the strategy
3. **Small position live**: Don't go all-in, test the waters first
4. **Adjust based on coin**: Big volatile coins can tighten the stop-loss

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Building a "Safety Net" With Multi-Conditions

CofiBitStrategy is a classic **trend following + oversold bottom-fishing** strategy. Code size isn't huge, but logic is rigorous — entry conditions must satisfy all 5 to open.

**Its Money-Making Philosophy**:
- **Low price entry**: Buy at relatively low prices, controllable risk
- **Oversold capture**: Uses stochastic to catch oversold rebound opportunities
- **Trend confirmation**: ADX filtering ensures trading only in clear trends
- **Multi-layer filtering**: Pursues high win rate, sacrifices high-frequency signals

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:-----------|:------:|:------------------------|
| 📈 **Uptrend Pullback** | ⭐⭐⭐⭐⭐ | Clear trend + pullback entry = optimal entry — designed for this market |
| 📉 **Downtrend Bounce** | ⭐⭐⭐⭐☆ | Oversold rebound signals accurate, but stop-loss may get hit |
| 🔄 **Ranging Consolidation** | ⭐⭐☆☆☆ | ADX filters block most signals, capital utilization low |
| ⚡ **Unilateral Surge** | ⭐☆☆☆☆ | Too conservative at entry, may miss most of the rally |
| 📊 **Low-Volatility Market** | ⭐☆☆☆☆ | Not enough fluctuation, can't trigger signals, strategy "sleeps" |

**One-Line Summary**: **Trending + volatile + pullback** markets are best — ranging and surges won't work.

---

## 10. Want to Run This Strategy? Check These Settings First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Comment |
|-------------------|-----------------|---------|
| Number of pairs | 1-10 | Too many to watch, too few not enough signals |
| Coin selection | High-volatility coins | Low-volatility coins make the strategy "sleep" |
| Timeframe | 5 Minutes | Don't change — this is how the strategy was designed |

### 10.2 Key Parameter Adjustment Suggestions

**Conservative (Recommended for Beginners)**:
```yaml
buy_fastx: 20    # Stricter, must be lower to buy
buy_adx: 30      # Only trade with stronger trends
sell_fastx: 70   # Take profits earlier, secure them
```

**Aggressive (Veteran Play)**:
```yaml
buy_fastx: 30    # Loosen entry conditions, catch more opportunities
buy_adx: 20      # Lower trend requirement
sell_fastx: 80   # Let profits run longer
```

**Stop-Loss Adjustment**:
- Particularly volatile coins: Can tighten to **-15%**
- Average volatility coins: Keep at **-25%**

### 10.3 Hardware Requirements (Medium)

Strategy computation isn't heavy, but 5-minute level needs continuous attention:

| Number of Pairs | Monitoring Requirement | Experience |
|----------------|----------------------|------------|
| 1-5 pairs | Medium | Check occasionally |
| 6-15 pairs | High | Recommend automation |
| 15+ pairs | Very High | Must use bots |

### 10.4 Backtest vs. Live

**Common Differences**:
- **Slippage**: Live fill price may be significantly worse than backtest
- **Liquidity**: Extreme markets may not fill
- **Mindset**: Live losing 25% and backtest losing 25% are totally different things

**Recommended Process**:
1. Historical data backtest verification
2. Paper trading test (at least 1 month)
3. Small-position live testing
4. Gradually increase position

**Don't go all-in right away** — even the best strategy needs a break-in period!

---

## 11. Bonus: Strategy Author's "Little Tricks"

Look closely at the code and you'll find some interesting designs:

1. **Staircase Take-Profit Time Setting**: 40 minutes is the dividing line
   > "Author probably observed that intraday returns become unstable after holding more than 40 minutes,， 5%"

2. **-25% Loose Stop-Loss**
   > "This guy probably got burned by many 'stopped out then bounced right back' trades, so just widened the stop-loss"

3. **ADX Threshold 25**
   > "This is textbook trend dividing line — shows the author is a by-the-book technical player"

4. **5-Minute Timeframe**
   > "5 minutes is neither too short (too noisy) nor too long (miss intraday swings) — the golden period for intraday players"

---

## 12. The Bottom Line

### One-Line Verdict
> "A cautious intraday bottom-fishing strategy: strict conditions, high win rate, stop-loss stings — suitable for experienced veterans."

### Who's It For?
- ✅ Intraday short-term veterans
- ✅ People who can handle 25% per-trade losses
- ✅ Bottom-fishing rebound players
- ✅ People with time to monitor the board

### Who's It NOT For?
- ❌ Beginner newcomers
- ❌ Emotionally unstable people
- ❌ Long-term investors
- ❌ People without time to watch the board

### Manual Trading Recommendations

If you want to manually use this strategy:
1. Set up alerts on TradingView (fastk/fastd golden cross + ADX condition)
2. Monitor and confirm price position
3. Execute stop-loss discipline strictly
4. Don't mess with parameters on impulse

---

## ⚠️ Final Warning (Must Read!)

### Backtesting Looks Great — Be Careful in Live Trading

CofiBitStrategy's historical backtest may look very good — but there's a trap:

> **Because this strategy has adjustable parameters, it's easy to "fit" the optimal solution for past market conditions, but this doesn't guarantee future profitability.**

Simply put: **Historical transcript ≠ Future transcript**

### Hidden Risks of Complex Strategies

In live trading, you may encounter:
- **High stop-loss risk**: 25% stop-loss isn't a joke, extreme markets will hit hard
- **ADX lag**: Slow to respond when trends change, may miss optimal entry
- **Parameter sensitivity**: Changing one parameter might make the whole strategy unprofitable
- **Low signal frequency**: Strict conditions might mean no signals for days

### My Recommendations (Sincere Advice)

```
1. Paper trade for at least one month before live trading
2. When backtesting, use out-of-sample data — don't just look at in-sample performance
3. Control parameter adjustments within ±20% of defaults
4. Adjust stop-loss based on coin volatility — don't -25%
5. Position control: Don't risk more than 10% of total capital on single trade
```

**Remember**: No matter how good a strategy is, the market doesn't care when it teaches you a lesson. Paper trade with light positions, survival is the top priority! 🙏

---

**Final Reminder**: This is just a tool, not a holy grail. Profitability depends on discipline, position management, and mindset — strategy is just one part. Happy trading!
