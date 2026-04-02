# Guacamole: The Multi-Indicator "Avocado Sauce" Mix Strategy

> **Nickname**: Mr. Guacamole, Indicator Melting Pot
> **Profession**: Multi-indicator momentum catcher + Orderbook precision manager
> **Timeframe**: 5 minutes (5m)

---

## 1. What Is This Thing?

Simply put, **Guacamole** is:
- A strategy that mixes KAMA, MACD, RMI, SAR multiple indicators together
- Also checks orderbook to confirm price
- Uses trailing stop to lock profits
- All parameters calculated via hyperopt optimization

Like making guacamole that requires mixing multiple ingredients, this strategy "mixes" multiple indicators together, each indicator must nod before placing an order 🥑

**One-Line Summary**: A "triple insurance" strategy of multi-indicator + orderbook + trailing stop.

---

## 2. Core Config: Basically "Run When Made Enough, Have Bottom Line When Lost"

### Profit-Taking Rules (ROI Table)

```
0 min     → Run at 13.34% profit
19 min    → Run at 7.46% profit
37 min    → Run at 4.21% profit
57 min    → Run at 2.68% profit
73 min    → Run at 1.23% profit
125 min   → Run at 0.37% profit
244 min   → Run at 0.25% profit
```

**Translation**: Right after buying requires 13% profit to sell, but the longer you hold the lower the threshold. After 4+ hours (244 min) run at 0.25% profit - main philosophy is "survival is most important".

### Stoploss Rules

```
Stoploss line: -10%
Trailing stop: Enabled
Trailing trigger: 1.85% profit
Trailing drawdown: 1.67%
```

**Translation**:
- Admit defeat at 10% loss
- After making 1.85% profit, activate "bodyguard mode"
- Auto-sell if pullback 1.67% from highest point

**In Plain English**: Admit defeat if lost too much, put insurance on after making profit, secure the victory 🛡️

---

## 3. Entry Conditions: Two Major Scenarios

This strategy divides entry into two scenarios: no position and has position.

### 🎯 Scenario 1: Open New Position When No Position (All 6 Conditions Must Be Met)

**Core Logic**: Multiple indicators confirm together, "everyone agrees before getting on board"

**In Plain English**:
> "I need KAMA saying up, MACD saying up, RMI saying up, volume must be normal, everyone nods before I buy!"

**6 Conditions Translated One by One**:

| Condition | Code | In Plain English |
|-----------|------|------------------|
| KAMA Trend | `kama-3 > kama-21` | Fast line higher than slow line, trend up |
| MACD Golden Cross | `macd > macdsignal` | MACD above signal line, momentum up |
| MACD Threshold | `macd > -0.75` | MACD can't be too low (threshold -0.75) |
| MACD Histogram Threshold | `macdhist > -1` | MACD histogram can't be too low |
| RMI Rising | `rmi > rmi.shift()` | RMI higher than previous candle, rising |
| RMI Threshold | `rmi > 49` | RMI greater than 49 |
| Volume Filter | `volume < volume_ma × 20` | Volume can't be 20x average (exclude anomalies) |

**Roast**: Conditions are really many! But this also means - doesn't act easily, acts with conviction 🎯

---

### 📈 Scenario 2: Add Position When Has Position (2 Conditions)

**Core Logic**: Already have position, only add when trend is super strong

**In Plain English**:
> "Already have goods? Then RMI must hit 75+, price still above SAR, before I dare add!"

**Conditions Translated**:

| Condition | Code | In Plain English |
|-----------|------|------------------|
| Price > SAR | `close > sar` | Price above parabolic SAR, trend up |
| RMI Super Strong | `rmi >= 75` | RMI hits 75, momentum explosive |

**Evaluation**: Adding position threshold is very high, won't add randomly - rational adding party ✋

---

## 4. Protection Mechanisms: Three-Layer "Bodyguards"

Although each entry condition doesn't have independent protection parameter groups, the strategy overall has three layers of protection:

| Protection Type | Parameter | In Plain English |
|----------------|-----------|------------------|
| **Hard Stoploss** | -10% | Cutforce at 10% loss, admit defeat |
| **Trailing Stop** | 1.67% drawdown | Put insurance on after profit, run if pullback 1.67% |
| **Order Timeout** | 1% price deviation | Cancel order if price runs too far, don't chase |

**In Plain English**:
- First layer: Admit defeat if lost too much (-10% stoploss)
- Second layer: Secure after making profit (trailing stop)
- Third layer: Don't chase if price runs too fast (order timeout)

"Three bodyguards" escorting, main philosophy is **survival is most important** 🛡️

---

## 5. Exit Logic: Much Simpler Than Entry

### 5.1 Exit Conditions (3 Conditions Simultaneously)

```python
# Check exit when has position
rmi < 30          # RMI enters oversold zone
current_profit > -0.03  # Loss not more than 3%
volume > 0        # Has volume
```

**In Plain English**:
> "RMI dropped below 30? Okay, let me see how much loss... less than 3% loss? Then sell!"

**Translation**:
- RMI < 30: Momentum turning weak, enters oversold
- Profit > -3%: Only sell if loss not more than 3% (avoid cutting at big loss)
- Volume > 0: Prevent abnormal data

**Evaluation**: Exit logic is very restrained - not sell on every dip, but wait for momentum confirmed weak, loss controllable before selling.

---

### 5.2 Order Timeout Check (Signature Feature)

**Buy Order Timeout**:
```python
if current_price > order_price × 1.01:
    cancel_order  # Price up over 1%, cancel don't chase
```

**Sell Order Timeout**:
```python
if current_price < order_price × 0.99:
    cancel_order  # Price down over 1%, cancel and re-list
```

**In Plain English**:
- Buy order placed, price up over 1%? Don't chase, cancel!
- Sell order placed, price down over 1%? Don't sell cheap, cancel and re-list!

**Roast**: This is afraid of slippage losing money - precision manager mode 💼

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Multi-Indicator Confirmation**: KAMA + MACD + RMI + SAR four indicators confirm together, signals reliable
2. **Orderbook Check**: Uses real-time orderbook price judgment, not dependent on candle close
3. **Order Timeout Protection**: Cancel order if price runs too fast, don't chase highs/lows
4. **Trailing Stop**: Lock profits after making them, don't let cooked duck fly away
5. **Parameters Optimized**: ROI and trailing parameters are hyperopt results (note: may also be overfitting)

### ⚠️ Cons (Roast Section)

1. **Many Conditions**: Entry requires all 6 conditions met, signals may be few
2. **No Trend Filter**: No EMA/SMA long-term trend judgment, easy to lose in downtrends
3. **No BTC Correlation**: Doesn't watch Bitcoinmarket, independent operation has risk
4. **Orderbook Dependent**: Needs exchange support orderbook API, backtest may be inaccurate
5. **Parameters May Overfit**: Hyperopt results may just be "memorizing answers"

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Slow Bull/Ranging Up | ✅ Recommended | Multi-indicator confirmation + trailing stop performs well |
| 🔄 Wide Ranging | ✅ Recommended | Multi-indicator combo suitable for ranging |
| 📉 One-Way Crash | ⚠️ Light Position or Pause | No trend filter, may lose consecutively |
| ⚡ Extreme Sideways | ⚠️ Signals Reduce | Too little volatility, conditions hard to trigger |

**One Line**: Most comfortable in ranging up, be careful in crash 📊

---

## 8. Summary: How Is This Strategy Really?

### One-Line Review
> **"Multi-indicator conservative + orderbook precision manager, suitable for ranging market steady players."**

### Who Should Use It?
- ✅ Ranging market traders
- ✅ Conservatives who like multi-indicator confirmation
- ✅ Players who can accept lower signal frequency
- ✅ Users with VPS supporting orderbook API

### Who Should NOT Use It?
- ❌ Aggressive players chasing high-frequency trading
- ❌ Players who only want to trade trend single-direction
- ❌ Users whose exchange doesn't support orderbook API
- ❌ Old players with too low computer specs

### My Recommendations
1. **Backtest First**: Verify performance on historical data
2. **Watch Overfitting**: Parameters are optimized, may just be "memorizing answers"
3. **Test Light**: Small amount live test first
4. **Use in Ranging**: Performs best in ranging up

---

## 9. What Markets Make Money With This?

### 9.1 Core Logic: Build "Defense Net" with Multi-Indicators

Guacamole is a multi-indicator momentum strategy. Core logic: **Multiple indicators confirm together, dare to act only then**.

**Its Money-Making Philosophy**:
- **Not Greedy**: ROI multi-level decreasing, longer hold lower threshold
- **Not Chase**: Order timeout check, don't chase if price runs too fast
- **Secure Profit**: Trailing stop locks gains

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|------------|-------------------|--------------------------|
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐☆ | Multi-indicator confirmation + trailing stop, easy money |
| 🔄 Wide Ranging | ⭐⭐⭐⭐☆ | Conditionsjust trigger, volatility not too big not too small |
| 📉 One-Way Crash | ⭐⭐☆☆☆ | No trend filter, easy to get trapped |
| ⚡ Extreme Sideways | ⭐⭐⭐☆☆ | Few signals, but won't lose randomly |

**One-Line Summary**: Most comfortable in ranging up, dodge in crash 📈

---

## 10. Want to Run This? Check These Configs First

### 10.1 Pair Configuration

| Config | Recommended Value | Roast |
|--------|------------------|-------|
| Number of Pairs | 20-40 pairs | Moderate signal frequency |
| Max Open Trades | 3-6 orders | Don't be greedy, control risk |
| Position Mode | Fixed Position | Simple and stable |

### 10.2 Hardware Requirements (Medium)

This strategy needs to calculate multiple indicators, has certain hardware requirements:

| Pairs | Minimum RAM | Recommended RAM | Experience |
|-------|-------------|-----------------|------------|
| 20-40 | 1GB | 2GB | Smooth |
| 40-80 | 2GB | 4GB | Stable |
| 80+ | 4GB | 8GB | No lag |

**Warning**: Orderbook API may increase network latency, recommend using stable VPS 😅

### 10.3 Orderbook Dependency (Important!)

Strategy uses `self.dp.orderbook()` to get real-time orderbook:
- **Needs exchange support** orderbook API
- **Live Trading Latency**: Orderbook data may have latency
- **Backtest Inaccurate**: Orderbook data may be inaccurate in backtest

### 10.4 Backtest vs Live Trading

**Backtest**:
- Orderbook data may be inaccurate
- Parameter optimization results may overfit
- Good historical performance ≠ Future profitable

**Recommended Process**:
1. Run historical backtest first, see strategy performance
2. Test with dry-run paper trading
3. Small amount live test
4. Gradually add position

**Don't go all-in immediately**, no matter how good the strategy needsbreak-in period!

---

## 11. Easter Egg: The Author's "Little Tricks"

Look carefully at the code, you'll find interesting things:

1. **ROI Parameters All Decimals**: `0.13336`, `0.07455`...
   > "These parameters are all hyperopt calculated, precise to 5 decimal places - but may also be 'memorizing answers'."

2. **Entry Conditions Have 6**:
   > "So many conditions, just don't want to act easily - conservative's self-cultivation."

3. **Adding Position Threshold Super High**: RMI must hit 75 to add
   > "Already have goods and still add? Must have explosive momentum before daring to add!"

4. **Order Timeout Check**: Cancel if 1% deviation
   > "Slippage? Doesn't exist, I cancel if price runs too fast!"

---

## 12. Final Final Words

### One-Line Review
> **"Multi-indicator + orderbook + trailing stop, good choice for ranging market steady players."**

### Who Should Use It?
- ✅ Ranging market traders
- ✅ Conservatives who like multi-indicator confirmation
- ✅ Players who can accept lower signal frequency
- ✅ Users with VPS supporting orderbook API

### Who Should NOT Use It?
- ❌ Aggressive players chasing high-frequency trading
- ❌ Players who only want to trade trend single-direction
- ❌ Users whose exchange doesn't support orderbook API
- ❌ Lazy people who want toeasy-money big money

### Manual Trading Recommendations

Manual traders can reference this strategy's approach:
- Observe KAMA, MACD, RMI multiple indicators simultaneously
- Set trailing stop to protect profits
- Don't chase highs/lows, set good price then place order

---

## 13. ⚠️ Risk Reminder Again (MUST READ This Section)

### Backtests Are Beautiful, Live Trading Needs Caution

Guacamole's historical backtest performance may be **very beautiful** - but here's a trap:

> **Parameters are hyperopt calculated, very likely just "memorizing answers" - perfectly fits historical data, but may not work in future.**

Simply put: **Got full marks on historical exam, doesn't mean next exam will also get full marks.**

### Hidden Risks of Complex Strategies

In live trading, multiple indicators and orderbook checks may lead to:
- **Too Few Signals**: All 6 conditions must be met, opportunities not many
- **Orderbook Latency**: Real-time data may have latency, affects judgment
- **Overfitting Trap**: Optimized parameters may just be memorizing answers
- **Crash Risk**: No trend filter, easy to lose consecutively in downtrends

### Orderbook Data Risks

Strategy depends on orderbook API, but:
- Orderbook data may be inaccurate in backtest
- Orderbook may have latency in live trading
- Some exchanges don't support orderbook API

### My Recommendations (Real Talk)

```
1. Run backtest first, see how strategy performs on your pairs
2. Test with dry-run paper trading for at least 1 month
3. Small amount live test, don't go all-in immediately
4. Use in ranging, pause or light position in crash
5. Watch overfitting risk, parameters may just be "memorizing answers"
```

**Remember**: No matter how good the strategy, the market won't say hello before teaching you a lesson. Light positions for testing, survival is most important! 🙏

---

**Final Reminder**: Multi-indicator combo is a double-edged sword - filters out false signals, but may also miss real opportunities. What fits you is the best! 🎯
