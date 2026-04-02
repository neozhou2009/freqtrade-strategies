# ichiV1: The 8-Timeframe Ichimoku Player

> **Nickname**: Octopus  
> **Profession**: Quant world's "multitasking expert" — watches 8 timeframes simultaneously  
> **Timeframe**: 5 minutes (short-term player)

---

## 1. What's This Strategy?

Simply put, **ichiV1** is:
- A strategy that watches **8 timeframes** (5m/15m/30m/1h/2h/4h/6h/8h)
- A strategy using **Ichimoku Cloud**
- A **Fan confirmation** strategy

Like a super cautious buyer who asks 8 friends before buying: "Is 5m trend up? Is 15m up? ... Is 8h up? All up then buy!" 🐙

---

## 2. Core Config: Basically "Multi-Layer Confirmation"

### Profit-Taking Rules (ROI Table)

```
Make 5.9% right after buying? → RUN!
Hold 10 minutes and make 3.7%? → RUN!
Hold 41 minutes and make 1.2%? → RUN!
Hold 114 minutes? → Run at breakeven! (2 hours, enough!)
```

**Translation**: This strategy is classic "trend following thinking", 5.9% ROI is relatively high, expecting to capture large trends!

### Stoploss Rules

```
Hard stoploss: Cut at 27.5% loss (loose)
Trailing stop: Yes, but no specific parameters configured
```

**Translation**: -27.5% stoploss is really loose, giving price ample room to fluctuate! 😅

---

## 3. Entry Conditions: Must Satisfy N Conditions

This strategy's entry conditions have 3 parts:

### 🎯 Condition 1: Trend Above Cloud (Up to 8 Levels)

**Core Logic**:
- Level 1: 5m trend > Cloud
- Level 2: 15m trend > Cloud
- ...
- Level 8: 8h trend > Cloud

**In Plain English**:
> "5m to 8h all timeframes above cloud — if this isn't a buy, what is?"

### 🎯 Condition 2: Trend Bullish (Up to 8 Levels)

**Core Logic**:
- Level 1: 5m close > open
- Level 2: 15m close > open
- ...
- Level 8: 8h close > open

**In Plain English**:
> "5m to 8h all timeframes are bullish candles — if this isn't a buy, what is?"

### 🎯 Condition 3: Fan Confirmation

**Core Logic**:
1. Fan magnitude gain >= 1.002
2. Fan magnitude > 1
3. Fan magnitude continuously rising (3 candles)

**In Plain English**:
> "1h trend stronger than 8h trend, and still strengthening — if this isn't a buy, what is?"

**Roast**: This strategy is really "cautious", needs to satisfy so many conditions! 🤣

---

## 4. Protection: Multi-Layer Trend Filtering

This strategy's protection is more luxurious than all previous strategies:

| Protection Type | Function | Plain English |
|---------|------|---------------|
| **Hard Stoploss** | Cut at 27.5% loss | "If we're wrong, admit it. 27.5% is the line" |
| **Trailing Stop** | Automatically follows price after profit | "Has trailing, but parameters not specified" |
| **Multi-Layer Trend Filtering** | 8 timeframe confirmation | "8 friends all agree then buy" |

**Roast**: This strategy's protection is really luxurious, 8 timeframe confirmation! 🤣

---

## 5. Exit Logic: Run When Trend Crosses

### 5.1 Technical Exit: Just 1 Condition

**Trigger**:
```python
5m trend crosses below 2h trend
```

**In Plain English**:
> "5m trend already crossed below 2h trend (trend weakening) — if you don't run now, what are you waiting for?"

---

### 5.2 ROI Exit: 4-Level Profit Taking

```
Profit      Hold Time    Trigger Exit
─────────────────────────────────────
5.9%       Anytime      Run when reached (big profit)
3.7%       After 10min  Run when reached (medium profit)
1.2%       After 41min  Run when reached (small profit)
0%         After 114min Run at breakeven (2 hours already)
```

**In Plain English**:
- Make 5.9% right after buying? → Heaven-sent gift, run!
- Hold 2 hours and still no profit? → Run at breakeven, enough!

---

## 6. This Strategy's "Personality"

### ✅ Pros
1. **Multi-Timeframe**: 8 timeframes confirm trend
2. **Ichimoku Cloud**: Cloud filters trends
3. **Fan**: Measures trend strength
4. **Heikin Ashi**: Smooth candles reduce noise
5. **Hyperopt Optimization**: Can auto-find best parameters
6. **Loose Stoploss**: -27.5% stoploss, giving ample room

### ⚠️ Cons
1. **Extremely High Complexity**: 8 timeframes + Ichimoku Cloud, headache to debug
2. **No BTC correlation**: Doesn't know when Bitcoin crashes
3. **Parameter sensitive**: Optimized parameters may overfit
4. **High Computation**: Multi EMA + Ichimoku Cloud increases computation
5. **Stoploss too loose**: -27.5% stoploss, may hurt badly in extreme conditions

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| **Uptrend** | Highly recommended | Multi-timeframe + cloud filtering, perfect match |
| **Ranging Market** | Not recommended | Trend strategy has many false signals in ranging |
| **Downtrend** | Auto pause | Multi-layer trend filtering blocks most trades |
| **High Volatility** | Adjust parameters | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |
| **BTC Crash** | Auto pause | Multi-layer trend filtering blocks entries |

---

## 8. Summary: How's This Strategy?

### One-Line Review
> **"An 8 timeframe, Ichimoku Cloud, Fan confirmation octopus player"**

### Who Should Use It?
- ✅ People who like advanced strategies
- ✅ People who can accept high complexity
- ✅ People with quant basics
- ✅ Friends with VPS 4GB+ RAM

### Who Should NOT Use It?
- ❌ People who like simple strategies (this strategy has many conditions)
- ❌ People wanting to make money in ranging markets (trend strategy has many false signals)
- ❌ People who don't want to optimize parameters
- ❌ Pure quant beginners (need to understand multi-timeframe)

### My Recommendations
1. **Paper trade first**: Run 2-4 weeks to see signal frequency
2. **Add filters**: Can add BTC correlation filter yourself
3. **Adjust parameters**: Can use Hyperopt to optimize parameters
4. **Watch BTC**: Although strategy has multi-layer trend filtering, manually pause when Bitcoin crashes hard

---

## 9. What Markets Make Money?

### 9.1 Core Logic: Multi-Timeframe Faith

ichiV1 is an octopus, code about 200 lines, what's that concept? Equivalent to a long article 📄

**Its money-making philosophy**:
> "One timeframe may lie, eight timeframes together won't all lie! Only trade above cloud, lie flat in downtrend!"

- **Multi-Timeframe Faith**: 8 timeframes confirm, reduces false signals
- **Cloud Faith**: Only trade above cloud
- **Fan Faith**: Measures trend strength

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐⭐ | Multi-timeframe + cloud filtering, perfect match |
| 🔄 Wide Ranging | ⭐⭐☆☆☆ | Trend strategy has many false signals in ranging |
| 📉 Single-sided Crash | ⭐⭐⭐☆☆ | Multi-layer trend filtering blocks most trades, auto lies flat |
| ⚡️ Extreme Sideways | ⭐⭐☆☆☆ | Too little volatility, signals decrease |

**One-Line Summary**: **Makes money in uptrends, many false signals in ranging, auto lies flat in crash markets**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended Value | Roast |
|--------|--------|------|
| **Number of Pairs** | 20-40 | Moderate signal frequency |
| **Quote Currency** | USDT | Don't use BTC/ETH as quote currency |
| **Max Open Trades** | 3-6 orders | Control risk |
| **Position Mode** | Fixed position | Recommended fixed, control risk |
| **Timeframe** | 5m | Mandatory, can't change |

### 10.2 Hardware Requirements (High Level)

This strategy uses multi EMA + Ichimoku Cloud, high computation:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------|---------|---------|------|
| 20-40 pairs | 2GB | 4GB | Can run |
| 40-80 pairs | 4GB | 8GB | Comfortable |

**Warning**: Don't try with below 2GB RAM VPS, this strategy really consumes resources 😅

### 10.3 Multi-Timeframe Advantages

- **Trend Confirmation**: 8 timeframes confirm, reduces false signals
- **Cloud Filtering**: Only trades above cloud
- **Auto Lies Flat**: Auto stops trading when trend down

**Roast**: This multi-timeframe is better than many paid strategies! 🤣

### 10.4 Backtest vs Live

Strategy logic is complex, backtest and live differences mainly from:
- Hyperopt overfitting
- Multi-timeframe data delays
- Ichimoku Cloud calculation delays

**Recommended Process**:
1. Backtest first to see historical performance
2. Use Hyperopt to optimize parameters
3. Paper trade (Dry-Run) for 2-4 weeks
4. Small capital live test for 1 month

**Don't go all-in immediately**, even good strategies need breaking in!

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Strategy name is ichiV1**: ichi (Ichimoku) + V1 (1st version)
   > "This name is telling you, this is an Ichimoku Cloud strategy, 1st version!"

2. **8 Timeframes**: From 5m to 8h
   > "This is real·octopus, watches 8 timeframes simultaneously!"

3. **Fan**: 1h/8h trend comparison
   > "This is real·trend strength measure, 1h stronger than 8h then buy!"

---

## 12. Last But Not Least

### One-Line Review
> **"8 Timeframe + Ichimoku Cloud, octopus advanced player"**

### Who Should Use It?
- ✅ People who like advanced strategies
- ✅ People who can accept high complexity
- ✅ People with quant basics
- ✅ Friends with VPS 4GB+ RAM

### Who Should NOT Use It?
- ❌ People who like simple strategies
- ❌ People wanting to make money in ranging markets
- ❌ People who don't want to optimize parameters
- ❌ Pure quant beginners

### Manual Trading Recommendations
Manual traders can reference this strategy's multi-timeframe approach:
- Observe multiple timeframe trends simultaneously
- Use cloud to filter trends
- Set loose stoploss (e.g., -25%)

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtest is Beautiful, Live Trading Needs Caution

ichiV1's historical backtest performance may be **very excellent** — but there's a trap:

> **Multi-timeframe + hyperopt optimization strategies easier to "fit" beautiful backtest curves, because many parameter combinations, may just "memorized" that historical period.**

Simply put: **Backtest data looks good, maybe because it just "remembered" how that period went.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Too few signals**: 8 timeframe confirmation may have no signals for long time
- **Overfitting risk**: Hyperopt results may overfit
- **Computation delays**: Multi EMA + Ichimoku Cloud may have delays

### My Recommendations (Real Talk)

```
1. Test with minimum capital first (e.g., 100U)
2. Run live for at least 2-4 weeks, observe signal frequency
3. Use Hyperopt to optimize parameters but verify
4. Consider adding BTC correlation filter yourself
```

**Remember**: The more complex the strategy, the more alert to overfitting risk. Surviving is most important!

---

**Final Reminder**: No matter how good the strategy, market won't say hi when teaching you a lesson. Light position test, surviving is most important! 🙏
