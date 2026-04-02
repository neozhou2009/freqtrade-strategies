# FixedRiskRewardLoss: The Risk-Counting Accountant

> **Nickname**: The Risk Calculator  
> **Profession**: Quant world's "accountant" — calculates risk/reward ratio for every single trade  
> **Timeframe**: 5 minutes (short-term player)

---

## 1. What Is This Thing?

Simply put, **FixedRiskRewardLoss** is:
- An **educational example strategy** (not for making money, for learning)
- Demonstrates how to calculate risk/reward ratios
- Demonstrates how to implement breakeven stoploss

Like an actuary who calculates "how much can I lose, how much must I win" before buying anything: "For this trade, I can lose max 100, must make at least 350 to be worth it!" 🧮

---

## 2. Core Config: Basically "Penny-Pinching"

### Stoploss Rules

```
Hard stoploss: Cut at 10% loss (safety net)
Custom stoploss: Risk/reward ratio 3.5:1 + breakeven mechanism
```

**Translation**: This strategy's focus is teaching you money management, trading logic is secondary.

---

## 3. Entry Conditions: No Conditions

### 🎯 Always Buy

**Core Logic**: None

**In Plain English**:
> "I'm just an example strategy, entry logic is whatever, the point is stoploss techniques!"

**Code Translation**:
```python
# Entry conditions
dataframe.loc[:, "buy"] = 1  # Always buy
```

**Roast**: This entry condition is so simple it's speechless, but it's an example strategy, the point is teaching you money management! 🤣

---

## 4. Stoploss Mechanism: This Is the Main Event

### 4.1 Risk/Reward Ratio 3.5:1

**Core Logic**:
1. Calculate initial risk (ATR × 2)
2. Take-profit target = Risk × 3.5
3. Ensure every trade makes at least 3.5x the risk

**In Plain English**:
> "For this trade I can lose max 100U, so I must make at least 350U to be worth it!"

**Code Translation**:
```python
# Risk calculation
risk = entry_price - initial_stoploss
take_profit_target = entry_price + risk × 3.5
```

**Classic Lines**:
- "This is the main character of this strategy, entry logic is just a sidekick!"
- "Learn this and you can calculate whether every trade is worth it!"

---

### 4.2 Breakeven Mechanism

**Trigger Condition**: Profit reaches 1x risk

**In Plain English**:
> "Made 1x risk (e.g., risk 100, made 100), quickly move stoploss to breakeven, this trade at least can't lose!"

**Code Translation**:
```python
# Breakeven logic
if current_profit >= 1x risk:
    stoploss = entry_price + fees  # Breakeven
```

---

### 4.3 Three-Stage Stoploss

| Stage | Condition | Stoploss Level | In Plain English |
|-------|-----------|----------------|------------------|
| **Initial** | Just entered | ATR × 2 stoploss | "Set a stoploss first, max lose this much" |
| **Breakeven** | Made 1x risk | Entry price + fees | "Made enough, secure the bag first" |
| **Take Profit** | Made 3.5x risk | Take-profit target | "Reached target, cash out" |

---

## 5. Exit Logic: No Technical Exits

### 5.1 Technical Exit: Doesn't Exist

```python
# Exit signals
dataframe.loc[:, "sell"] = 0  # No exit signals set
```

**In Plain English**:
> "I exit via stoploss, why would I need exit signals?"

**Roast**: This strategy is truly "minimalist", even saved on exit signals 🤣

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **High Learning Value**: Top choice for learning money management
2. **Risk/Reward Ratio**: Shows how to calculate and implement fixed risk/reward
3. **Breakeven Mechanism**: Shows how to lock in principal after profit
4. **ATR Adaptive**: Adjusts stoploss based on volatility
5. **Clean Code**: Around 100 lines, easy to understand

### ⚠️ Cons (Roast Section)

1. **Can't Live Trade**: No entry logic, will lose money in live trading
2. **No Trend Filter**: Buys regardless of market direction
3. **No BTC Correlation**: Doesn't know when Bitcoin crashes
4. **No Technical Exit**: Exits entirely via stoploss
5. **Example Nature**: It's not meant to make money originally

---

## 7. When to Use It?

| Use Case | Recommended Action | Reason |
|---------|-------------------|--------|
| **Learning Money Management** | Highly Recommended | This is designed for learning |
| **Learning Risk/Reward Ratio** | Highly Recommended | Standard example of risk/reward ratio |
| **Learning Breakeven Stoploss** | Highly Recommended | Standard example of breakeven mechanism |
| **Live Trading** | Not Recommended | No entry logic |
| **Modified for Live Trading** | Considerable | Add entry logic and protections |

---

## 8. Summary: How Is This Strategy Really?

### One-Line Review
> **"An accountant that can't make money but can teach you how to manage it"**

### Who Should Use It?
- ✅ People who want to learn money management
- ✅ People who want to learn risk/reward ratio calculation
- ✅ Quant beginners (simple code)
- ✅ People who want to develop their own strategies

### Who Should NOT Use It?
- ❌ People who want to make money directly in live trading
- ❌ Those looking for mature strategies
- ❌ People who don't want to modify code

### My Recommendations
1. **Learning First**: Don't think about live trading directly, learn first
2. **Understand Principles**: Get the risk/reward ratio calculation
3. **Modify and Improve**: Add your own logic on this basis
4. **Live Test**: Consider live trading after modification and improvement

---

## 9. What Can You Learn From This Strategy?

### 9.1 Core Technology: Money Management

This strategy is one of Freqtrade's official examples, specifically demonstrating money management features.

**You Can Learn**:
- Risk/reward ratio calculation and implementation
- Breakeven stoploss mechanism
- ATR adaptive stoploss
- Advanced usage of `custom_stoploss()` function

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|------------|-------------------|--------------------------|
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐☆ | Risk/reward management works in trends |
| 🔄 Wide Ranging | ⭐⭐☆☆☆ | May trigger stoploss frequently |
| 📉 One-Way Crash | ⭐☆☆☆☆ | No trend filter, easy to lose consecutively |
| ⚡️ Extreme Sideways | ⭐⭐☆☆☆ | Too little volatility, ATR stoploss may be too wide |

**One-Line Summary**: **Good for learning, forget about live trading**

---

## 10. Want to Run This? Check These Configs First

### 10.1 Pair Configuration

| Config | Recommended Value | Roast |
|--------|------------------|-------|
| **Number of Pairs** | 10-20 pairs | Example strategy, don't use too many |
| **Quote Currency** | USDT | Don't use BTC/ETH as quote |
| **Max Open Trades** | 1-3 orders | Control risk |
| **Timeframe** | 5m | Mandatory, can't change |

### 10.2 Hardware Requirements (This Strategy Is Friendly!)

This strategy has minimal computation, very low VPS requirements:

| Pairs | Minimum RAM | Recommended RAM | Experience |
|-------|-------------|-----------------|------------|
| 10-20 | 512MB | 1GB | Runs easily |

**Warning**: This is one of the few quant strategies that can run on a Raspberry Pi 😅

### 10.3 Backtest vs Live Trading

`custom_info` behaves differently in live trading vs backtest:

**In Backtest**:
- Can use entry time index directly
- Data is pre-loaded

**In Live Trading**:
- Need to use `get_loc(method="ffill")` to find nearest data
- Data is updated in real-time

**Recommended Process**:
1. Understand code logic first
2. Backtest to see stoplosseffects
3. Paper trade to observe live behavior
4. Modify and improve before considering live trading

---

## 11. Easter Egg: The Author's "Little Tricks"

Look carefully at the code, you'll find interesting things:

1. **Detailed Comments**: Lots of comments in the code
   > "Afraid you won't understand, I'll write as clearly as possible!"

2. **Entry Logic Set Directly to 1**: `dataframe.loc[:, "buy"] = 1`
   > "My focus is teaching you money management, entry logic is whatever!"

3. **Risk/Reward Ratio 3.5**: This value is empirical
   > "3.5 is a good ratio, you can change it to 3 or 4!"

---

## 12. Final Final Words

### One-Line Review
> **"An accountant that can't make money but can teach you to manage it"**

### Who Should Use It?
- ✅ People who want to learn money management
- ✅ Quant beginners
- ✅ People who want to develop their own strategies

### Who Should NOT Use It?
- ❌ People who want to make money directly in live trading
- ❌ People who don't want to modify code

### Manual Trading Recommendations
Manual traders can learn money management approach:
- Calculate risk/reward ratio before every trade
- Adjust stoploss to breakeven after certain profit
- Adjust stoploss distance based on volatility

---

## 13. ⚠️ Risk Reminder Again (MUST READ This Section)

### This Is an Example Strategy!

FixedRiskRewardLoss is an **educational example strategy**, not a production strategy:

> **This strategy has no entry logic, direct live trading will lose money.**

Simply put: **It's a textbook, not a money printer!**

### Hidden Risks of Example Strategies

In live trading, simple logic can lead to:
- **Consecutive Losses**: No entry conditions, random entry has low win rate
- **Ranging Market Whipsaw**: May trigger stoploss frequently
- **No Trend Protection**: Will buy even in downtrends

### My Recommendations (Real Talk)

```
1. Treat this strategy as a textbook, don't live trade directly
2. Understand risk/reward ratio calculation principles
3. Add your own entry logic on this basis
4. Add trend filters, BTC correlation and other protection mechanisms
5. Consider live trading after improvement
```

**Remember**: This is a textbook, after learning you need to write your own strategy!

---

**Final Reminder**: No matter how good the strategy, the market won't say hello before teaching you a lesson. Light positions for testing, survival is most important! 🙏
