# Schism2: The Dynamic Trading Advanced Player

> **Nickname**: Dynamic Master  
> **Profession**: Quant world's "smart player" — dynamically adjusts buy/sell based on trade state  
> **Timeframe**: 5 minutes (short-term player)

---

## 1. What's This Strategy?

Simply put, **Schism2** is:
- A strategy that **dynamically adjusts buy/sell** (based on trade state)
- A strategy that watches **1h big trend**
- A strategy that supports **BTC/ETH staking**

Like a smart buyer who acts based on situation: "Have position? Then keep buying! No position? Wait for oversold! Other trades? Check slot situation!" 🧠

---

## 2. Core Config: Basically "Dynamic Adjustment"

### Profit-Taking Rules (ROI Table)

```
Make 5% right after buying? → RUN!
Hold 10 minutes and make 2.5%? → RUN!
Hold 20 minutes and make 1.5%? → RUN!
Hold 30 minutes and make 1%? → RUN!
Hold 720 minutes and make 0.5%? → RUN! (12 hours already)
Hold 1440 minutes? → Run at breakeven! (24 hours, really can hold)
```

**Translation**: This strategy is classic "long-term thinking", exits at breakeven after 24 hours, really can hold!

### Stoploss Rules

```
Hard stoploss: Cut at 30% loss (loose)
Dynamic stoploss: Grows from -3% to 0%, completes in 300 minutes
```

**Translation**: Dynamic stoploss is this strategy's highlight, loose early strict later! 😅

---

## 3. Entry Conditions: Two Situations

This strategy's entry conditions have two situations:

### 🎯 Situation 1: No Position (Normal Entry)

**Core Logic**:
1. Price <= 3-day low + ADR percentage
2. 1h RSI >= 57
3. RMI downtrend
4. RMI slow >= 24
5. RMI fast <= 49
6. Momentum Pinball <= 64

**In Plain English**:
> "Price pulled back to 3-day low, 1h RSI also high, RMI also confirmed downtrend — if this isn't a buy, what is?"

### 🎯 Situation 2: With Position (Continuous Entry)

**Core Logic**:
1. RMI uptrend
2. Current profit > Peak profit × factor
3. RMI slow >= growth value

**In Plain English**:
> "Trend still going up, profit also okay — keep buying, don't stop!"

**Roast**: This strategy is really "flexible", two logics for with/without position! 🤣

---

## 4. Protection: Dynamic Stoploss + Multi-Trade Management

This strategy's protection is more luxurious than all previous strategies:

| Protection Type | Function | Plain English |
|---------|------|---------------|
| **Hard Stoploss** | Cut at 30% loss | "If we're wrong, admit it. 30% is the line" |
| **Dynamic Stoploss** | Grows from -3% to 0% | "Loose early, strict later" |
| **Multi-Trade Management** | Adjust exit based on free slots | "Slots tight, prioritize selling biggest losers" |
| **Price Caching** | Cache current price for 5 minutes | "Don't keep asking exchange, cache it" |

**Roast**: This strategy's protection is really luxurious, dynamic stoploss + multi-trade management! 🤣

---

## 5. Exit Logic: More Complex Than Entry

### 5.1 Dynamic Stoploss: Grows Based on Time

**Trigger**:
```python
# Stoploss threshold grows from -3% to 0%, completes in 300 minutes
loss_cutoff = linear_growth(-0.03, 0, 0, 300, open_minutes)

if current_profit < loss_cutoff:
    if rmi_dn_trend == 1:
        # Exit
```

**In Plain English**:
> "Just opened, loss within 3% don't sell. After 300 minutes, loss 1% must sell — longer time, stricter!"

### 5.2 Multi-Trade Management: Adjust Based on Free Slots

**Trigger**:
```python
if free_slots > 0:
    # Few free slots, more willing to sell
    hold_pct = (1 / free_slots) * -0.04
    avg_other_profit >= hold_pct
else:
    # No free slots, allow largest losing trade to exit
    biggest_loser == True
```

**In Plain English**:
> "Have free slots? Then wait. No free slots? Then biggest loser runs first, make room!"

**Roast**: This strategy is really "smart", even slot management considered! 🤣

---

### 5.3 ROI Exit: 6-Level Profit Taking

```
Profit      Hold Time    Trigger Exit
─────────────────────────────────────
5%         Anytime      Run when reached (big profit)
2.5%       After 10min  Run when reached (medium profit)
1.5%       After 20min  Run when reached (small profit)
1%         After 30min  Run when reached (tiny profit)
0.5%       After 720min Run when reached (12 hours already)
0%         After 1440min Run at breakeven (24 hours already)
```

**In Plain English**:
- Make 5% right after buying? → Heaven-sent gift, run!
- Hold 12 hours and make 0.5%? → Still need to run, time cost!
- Hold 24 hours and still no profit? → Run at breakeven, really not playing!

---

## 6. This Strategy's "Personality"

### ✅ Pros
1. **Dynamic Buy/Sell**: Dynamically adjusts based on trade state
2. **Multi-Timeframe**: 1h confirms trend, reduces false signals
3. **Multi-Trade Management**: Adjusts exit strategy based on free slots
4. **BTC/ETH Support**: Additional staking currency confirmation
5. **Price Caching**: Reduces API calls, improves efficiency
6. **Hyperopt Optimization**: Can auto-find best parameters

### ⚠️ Cons
1. **Extremely High Complexity**: Dynamic logic + multi-timeframe, headache to debug
2. **Live Trading Only**: Backtest cannot test dynamic logic
3. **No BTC Market Correlation**: Doesn't know when Bitcoin crashes (unless staking is BTC)
4. **High Computation**: Multi-indicator + dynamic data increases computation
5. **Parameter sensitive**: Optimized parameters may overfit

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| **Ranging Market** | Highly recommended | Multi-timeframe most suitable for ranging markets |
| **Uptrend** | Highly recommended | Dynamic buy/sell + multi-timeframe performs well |
| **Downtrend** | Pause or light position | Dynamic stoploss will manage losses |
| **High Volatility** | Adjust parameters | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |
| **BTC Crash** | Pause | Big brother crashed, wait and see |

---

## 8. Summary: How's This Strategy?

### One-Line Review
> **"A dynamically adjusts buy/sell, watches 1h trend, manages multi-trades advanced player"**

### Who Should Use It?
- ✅ People who like advanced strategies
- ✅ People who can accept high complexity
- ✅ People with quant basics
- ✅ Friends with VPS 4GB+ RAM

### Who Should NOT Use It?
- ❌ People who like simple strategies (this strategy has many conditions)
- ❌ People who only want backtest (dynamic logic live trading only)
- ❌ People who don't want to optimize parameters
- ❌ Pure quant beginners (need to understand dynamic trade state)

### My Recommendations
1. **Paper trade first**: Run 2-4 weeks to see if dynamic logic works properly
2. **Add filters**: Can add BTC correlation filter yourself
3. **Adjust parameters**: Can use Hyperopt to optimize parameters
4. **Watch BTC**: Manually pause when Bitcoin crashes hard

---

## 9. What Markets Make Money?

### 9.1 Core Logic: Dynamic Trading Faith

Schism2 is a smart player, code about 400 lines, what's that concept? Equivalent to a long article 📄

**Its money-making philosophy**:
> "Have position then keep buying, no position then wait for oversold! Slots tight, prioritize selling biggest losers, let profits run!"

- **Dynamic Buy/Sell Faith**: Dynamically adjusts based on trade state
- **Multi-Timeframe Faith**: 1h more reliable than 5m
- **Multi-Trade Management Faith**: Adjusts exit based on free slots
- **BTC/ETH Faith**: Additional staking currency confirmation

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐⭐ | Dynamic buy/sell + multi-timeframe, perfect match |
| 🔄 Wide Ranging | ⭐⭐⭐⭐☆ | Born for ranging markets, harvests back and forth |
| 📉 Single-sided Crash | ⭐⭐⭐☆☆ | Dynamic stoploss will manage losses |
| ⚡️ Extreme Sideways | ⭐⭐⭐☆☆ | Too little volatility, signals decrease but risk also low |

**One-Line Summary**: **Makes money in ranging and uptrends, dynamic stoploss manages in crash markets**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended Value | Roast |
|--------|--------|------|
| **Number of Pairs** | 20-40 | Moderate signal frequency |
| **Quote Currency** | USDT | Don't use BTC/ETH as quote currency (unless you want extra confirmation) |
| **Max Open Trades** | 4-6 orders | Control risk |
| **Position Mode** | Fixed position | Recommended fixed, control risk |
| **Timeframe** | 5m | Mandatory, can't change |

### 10.2 Hardware Requirements (High Level)

This strategy uses multi-indicator + dynamic data, high computation:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------|---------|---------|------|
| 20-40 pairs | 2GB | 4GB | Can run |
| 40-80 pairs | 4GB | 8GB | Comfortable |

**Warning**: Don't try with below 2GB RAM VPS, this strategy really consumes resources 😅

### 10.3 Live Trading Only

Dynamic trade data not available in backtest:
- `populate_trades()` function only works in live/dry_run mode
- Backtest cannot test dynamic buy/sell logic
- Need sufficient dry-run testing before live trading

**Roast**: This strategy is "live trading exclusive", backtest people be careful! 🤣

### 10.4 Backtest vs Live

Strategy logic is complex, backtest and live differences mainly from:
- Dynamic trade data not available in backtest
- Hyperopt overfitting
- Multi-timeframe data delays

**Recommended Process**:
1. Use Hyperopt to optimize parameters first (static part)
2. Paper trade (Dry-Run) for 2-4 weeks
3. Observe if dynamic logic works properly
4. Small capital live test for 1 month

**Don't go all-in immediately**, even good strategies need breaking in!

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Strategy name is Schism2**: Schism (split) + 2 (2nd version)
   > "This name is telling you, this is a split strategy, already 2nd version!"

2. **ROI has 6 levels**: Last level is 1440 minutes (24 hours)
   > "Hold 24 hours and still don't run? Really can hold!"

3. **Dynamic stoploss grows from -3% to 0%**: Completes in 300 minutes
   > "This is real·loose early strict later, give you chance to run!"

4. **Multi-trade management based on free slots**: Slots tight, prioritize selling biggest losers
   > "This is real·smart, even slot management considered!"

---

## 12. Last But Not Least

### One-Line Review
> **"Dynamic Buy/Sell + Multi-Timeframe, advanced smart player"**

### Who Should Use It?
- ✅ People who like advanced strategies
- ✅ People who can accept high complexity
- ✅ People with quant basics
- ✅ Friends with VPS 4GB+ RAM

### Who Should NOT Use It?
- ❌ People who like simple strategies
- ❌ People who only want backtest
- ❌ People who don't want to optimize parameters
- ❌ Pure quant beginners

### Manual Trading Recommendations
Manual traders can reference this strategy's dynamic approach:
- Adjust buy/sell decisions based on trade state
- Use multi-timeframe to confirm trend
- Adjust exit strategy based on free slots

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtest is Beautiful, Live Trading Needs Caution

Schism2's historical backtest performance may be **very excellent** — but there's a trap:

> **Dynamic logic not available in backtest, good backtest data doesn't mean good live trading.**

Simply put: **Backtest can only test static part, dynamic logic needs live testing.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Dynamic logic errors**: Dynamic trade state may have errors
- **Overfitting risk**: Hyperopt results may overfit
- **Computation delays**: Multi-indicator + dynamic data may have delays

### My Recommendations (Real Talk)

```
1. Test with minimum capital first (e.g., 100U)
2. Run live for at least 2-4 weeks, observe if dynamic logic works properly
3. Use Hyperopt to optimize parameters but verify
4. Consider adding BTC correlation filter yourself
```

**Remember**: The more complex the strategy, the more alert to overfitting risk. Surviving is most important!

---

**Final Reminder**: No matter how good the strategy, market won't say hi when teaching you a lesson. Light position test, surviving is most important! 🙏
