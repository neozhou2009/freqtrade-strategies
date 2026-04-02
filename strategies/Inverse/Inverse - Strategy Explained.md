# Inverse: The Reversal Fisher Trend Follower

> **Nickname**: Reversal Hero  
> **Profession**: Quant world's "reversal player" — uses Fisher RSI inverse to capture trend reversals  
> **Timeframe**: 1 hour (medium-term player)

---

## 1. What's This Strategy?

Simply put, **Inverse** is:
- A strategy using **Fisher RSI inverse transformation**
- A strategy that watches **1h + 4h two timeframes**
- A **hyperopt optimized** strategy

Like a smart buyer waiting for reversals: "Did Fisher RSI reverse? Is 4h trend up? Both good? BUY! Fisher RSI reversed? SELL!" 🔄

---

## 2. Core Config: Basically "Reversal + Trend"

### Profit-Taking Rules (ROI Table)

```
Make 10% right after buying? → RUN!
Hold 30 minutes and make 5%? → RUN!
Hold 60 minutes and make 2%? → RUN!
```

**Translation**: This strategy is classic "trend following thinking", 10% ROI is relatively high, expecting to capture large trends!

### Stoploss Rules

```
Hard stoploss: Cut at 20% loss (loose)
Trailing stop: Activates after 17.4% profit, runs if 7.8% pullback
```

**Translation**: -20% stoploss is really loose, giving price ample room to fluctuate! 😅

---

## 3. Entry Conditions: Must Satisfy N Conditions

This strategy's entry conditions have 3 parts:

### 🎯 Condition 1: Fisher CCI Reversal

**Core Logic**:
1. Fisher CCI crosses above threshold 1 (-0.42)
OR
2. Fisher CCI crosses below threshold 2 (0.41) then bounces back

**In Plain English**:
> "Fisher CCI already reversed — if this isn't a buy, what is?"

### 🎯 Condition 2: 4h SSL Up

**Core Logic**:
1. 4h SSL upper > 4h SSL lower

**In Plain English**:
> "4h trend already up — if this isn't a buy, what is?"

### 🎯 Condition 3: EMA Bullish Alignment

**Core Logic**:
1. 1h 50EMA > 200EMA
2. 4h 50EMA > 100EMA
3. 4h 50EMA > 200EMA

**In Plain English**:
> "1h and 4h EMA all bullish aligned — if this isn't a buy, what is?"

**Roast**: This strategy is really "cautious", needs to satisfy so many conditions! 🤣

---

## 4. Protection: Trailing Stop + Confirm Exit

This strategy's protection is more luxurious than previous strategies:

| Protection Type | Function | Plain English |
|---------|------|---------------|
| **Hard Stoploss** | Cut at 20% loss | "If we're wrong, admit it. 20% is the line" |
| **Trailing Stop** | Automatically follows price after profit | "Activates after 17.4% profit, runs if 7.8% pullback" |
| **Confirm Exit** | Block premature exit based on ADX/DI | "Trend still good, let profits run more" |

**Roast**: This strategy's protection is really luxurious, confirm exit lets profits run! 🤣

---

## 5. Exit Logic: Run When Fisher CCI Reverses

### 5.1 Technical Exit: Fisher CCI Crosses Below

**Trigger**:
```python
(Fisher CCI crosses below threshold 1) OR (Fisher CCI crosses below threshold 2)
```

**In Plain English**:
> "Fisher CCI already crossed below threshold (trend reversal) — if you don't run now, what are you waiting for?"

### 5.2 Confirm Exit: Block Premature Exit Based on ADX/DI

**Trigger**:
```python
if DI up AND ADX rising:
    block_exit (let profits run)
```

**In Plain English**:
> "ADX still rising (trend still good), DI also up — don't run, let profits run more!"

**Roast**: This strategy is really "conflicted", one side wants stoploss, one side wants let profits run! 🤣

---

### 5.3 ROI Exit: 3-Level Profit Taking

```
Profit      Hold Time    Trigger Exit
─────────────────────────────────────
10%        Anytime      Run when reached (big profit)
5%         After 30min  Run when reached (medium profit)
2%         After 60min  Run when reached (small profit)
```

**In Plain English**:
- Make 10% right after buying? → Heaven-sent gift, run!
- Hold 1 hour and make 2%? → Still need to run, time cost!

---

## 6. This Strategy's "Personality"

### ✅ Pros
1. **Fisher RSI Inverse**: Captures trend reversal points
2. **Multi-Timeframe**: 1h + 4h confirms trend
3. **Confirm Exit**: Blocks premature exit based on ADX/DI
4. **Hyperopt Optimization**: Can auto-find best parameters
5. **Trailing Stop**: Automatically follows price after profit
6. **Loose Stoploss**: -20% stoploss, giving ample room

### ⚠️ Cons
1. **High Complexity**: Fisher RSI + multi-timeframe, headache to debug
2. **No BTC correlation**: Doesn't know when Bitcoin crashes
3. **Parameter sensitive**: Optimized parameters may overfit
4. **High Computation**: Multi-indicator + informative timeframe increases computation
5. **1h Timeframe**: Signal frequency lower than 5m

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| **Uptrend** | Highly recommended | Multi-timeframe + trailing stop, perfect match |
| **Ranging Market** | Recommended | Fisher RSI suitable for ranging markets |
| **Downtrend** | Auto pause | Multi-timeframe blocks most trades |
| **High Volatility** | Adjust parameters | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |
| **BTC Crash** | Auto pause | Multi-timeframe blocks entries |

---

## 8. Summary: How's This Strategy?

### One-Line Review
> **"A Fisher RSI inverse, watches 1h+4h trend reversal player"**

### Who Should Use It?
- ✅ People who like advanced strategies
- ✅ People who can accept some complexity
- ✅ People with quant basics
- ✅ Friends with VPS 2GB+ RAM

### Who Should NOT Use It?
- ❌ People who like simple strategies (this strategy has many conditions)
- ❌ People wanting to bottom-fish in downtrends (multi-timeframe blocks)
- ❌ People who don't want to optimize parameters
- ❌ Pure quant beginners (need to understand Fisher RSI)

### My Recommendations
1. **Paper trade first**: Run 2-4 weeks to see signal frequency
2. **Add filters**: Can add BTC correlation filter yourself
3. **Adjust parameters**: Can use Hyperopt to optimize parameters
4. **Watch BTC**: Although strategy has multi-timeframe, manually pause when Bitcoin crashes hard

---

## 9. What Markets Make Money?

### 9.1 Core Logic: Fisher RSI Faith

Inverse is a reversal player, code about 200 lines, what's that concept? Equivalent to a long article 📄

**Its money-making philosophy**:
> "Fisher RSI reversed then buy, multi-timeframe confirmation more reassuring, make big money and run isn't great?"

- **Fisher RSI Faith**: Inverse transformation captures trend reversal points
- **Multi-Timeframe Faith**: 1h + 4h confirms trend
- **Confirm Exit Faith**: ADX/DI still good then let profits run

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐⭐ | Multi-timeframe + trailing stop, perfect match |
| 🔄 Wide Ranging | ⭐⭐⭐⭐☆ | Fisher RSI suitable for ranging markets |
| 📉 Single-sided Crash | ⭐⭐⭐☆☆ | Multi-timeframe blocks most trades, auto lies flat |
| ⚡️ Extreme Sideways | ⭐⭐⭐☆☆ | Too little volatility, signals decrease but risk also low |

**One-Line Summary**: **Makes money in uptrends and ranging markets, auto lies flat in crash markets**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended Value | Roast |
|--------|--------|------|
| **Number of Pairs** | 20-40 | Moderate signal frequency |
| **Quote Currency** | USDT | Don't use BTC/ETH as quote currency |
| **Max Open Trades** | 3-6 orders | Control risk |
| **Position Mode** | Fixed position | Recommended fixed, control risk |
| **Timeframe** | 1h | Mandatory, can't change |

### 10.2 Hardware Requirements (Moderate Level)

This strategy uses multi-indicator + informative timeframe, moderate computation:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------|---------|---------|------|
| 20-40 pairs | 1GB | 2GB | Can run |
| 40-80 pairs | 2GB | 4GB | Comfortable |

**Warning**: Don't try with 512MB RAM VPS, this strategy consumes some resources 😅

### 10.3 Fisher RSI Inverse Advantages

- **Captures Reversal Points**: Fisher RSI inverse more sensitive
- **Reduces False Signals**: Multi-timeframe confirmation
- **Flexible Adjustment**: Can optimize thresholds via Hyperopt

**Roast**: This Fisher RSI is better than many paid strategies! 🤣

### 10.4 Backtest vs Live

Strategy logic is complex, backtest and live differences mainly from:
- Hyperopt overfitting
- Informative timeframe data delays
- Confirm exit behavior differences

**Recommended Process**:
1. Backtest first to see historical performance
2. Use Hyperopt to optimize parameters
3. Paper trade (Dry-Run) for 2-4 weeks
4. Small capital live test for 1 month

**Don't go all-in immediately**, even good strategies need breaking in!

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Strategy name is Inverse**: Inverse (reverse)
   > "This name is telling you, this is a reverse strategy!"

2. **Trailing stop activates at 17.4%**: Much higher than common strategies
   > "This is real·let profits run, 17.4% before activating trailing!"

3. **Confirm exit based on ADX/DI**: Don't let run if trend still good
   > "This is real·let profits run, ADX still rising don't run!"

---

## 12. Last But Not Least

### One-Line Review
> **"Fisher RSI Inverse + Multi-Timeframe, reversal player advanced player"**

### Who Should Use It?
- ✅ People who like advanced strategies
- ✅ People who can accept some complexity
- ✅ People with quant basics
- ✅ Friends with VPS 2GB+ RAM

### Who Should NOT Use It?
- ❌ People who like simple strategies
- ❌ People wanting to bottom-fish in downtrends
- ❌ People who don't want to optimize parameters
- ❌ Pure quant beginners

### Manual Trading Recommendations
Manual traders can reference this strategy's Fisher RSI approach:
- Use Fisher RSI inverse to capture reversal points
- Observe both 1h and 4h trends simultaneously
- Set loose stoploss (e.g., -20%)

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtest is Beautiful, Live Trading Needs Caution

Inverse's historical backtest performance may be **very excellent** — but there's a trap:

> **Multi-timeframe + hyperopt optimization strategies easier to "fit" beautiful backtest curves, because many parameter combinations, may just "memorized" that historical period.**

Simply put: **Backtest data looks good, maybe because it just "remembered" how that period went.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Too few signals**: Multi-condition confirmation may have no signals for long time
- **Overfitting risk**: Hyperopt results may overfit
- **Computation delays**: Multi-indicator + informative timeframe may have delays

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
