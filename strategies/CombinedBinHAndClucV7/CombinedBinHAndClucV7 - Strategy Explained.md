# CombinedBinHAndClucV7: The Four-in-One V7 Warrior

> **Nickname**: Four-in-One Warrior  
> **Profession**: Quant world's "collector" — collected 4 entry strategies  
> **Timeframe**: 5 minutes (short-term player)

---

## 1. What's This Strategy?

Simply put, **CombinedBinHAndClucV7** is:
- A strategy with **4 entry modes** (BinHV45 + Cluc + RSI + MFI)
- A strategy that watches **1h big trend**
- A **V7 version** strategy (optimized through 7 iterations)

Like a cautious buyer who asks 4 friends before buying: "BinHV45 says buy? Cluc says buy? RSI says buy? MFI says buy? If one says buy, then BUY!" 🤔

---

## 2. Core Config: Basically "Multi-Strategy Combination"

### Profit-Taking Rules (ROI Table)

```
Make 1.81%? → RUN! (just this one level)
```

**Translation**: This strategy is classic "quick turnover" thinking, 1.81% and run, not greedy!

### Stoploss Rules

```
Hard stoploss: Cut at 99% loss (basically none)
Custom stoploss: Loss over 280 minutes stoploss at 1%
Trailing stop: Activates after 3% profit, runs if 1% pullback
```

**Translation**: This strategy's hard stoploss is nominal, mainly relies on custom stoploss and trailing stop! 😅

---

## 3. Entry Conditions: Buy If Any of 4 Modes Trigger

This strategy has 4 entry modes:

### 🎯 Mode 1: BinHV45 Variant

**Core Logic**:
1. Price > EMA200 (1h)
2. EMA50 > EMA200
3. EMA50 (1h) > EMA200 (1h)
4. Bollinger Band bandwidth sufficient
5. Price breaks below previous lower band

**In Plain English**:
> "1h trend is up, EMA golden cross, price broke Bollinger Band — if this isn't a buy, what is?"

### 🎯 Mode 2: ClucMay72018 Variant

**Core Logic**:
1. Price > EMA200
2. Price > EMA200 (1h)
3. Price < EMA50
4. Price < Bollinger Band lower × 0.992
5. Volume < Average volume × 29

**In Plain English**:
> "Trend is up, price pulled back below EMA, broke Bollinger Band, volume also normal — if this isn't a buy, what is?"

### 🎯 Mode 3: RSI Difference

**Core Logic**:
1. Price < SMA5
2. SSL (1h) going up
3. EMA50 > EMA200
4. EMA50 (1h) > EMA200 (1h)
5. RSI < RSI (1h) - 50.48

**In Plain English**:
> "Price pulled back, 1h trend is up, RSI much lower than 1h RSI — if this isn't a buy, what is?"

### 🎯 Mode 4: RSI + MFI

**Core Logic**:
1. SMA200 rising
2. SMA200 (1h) rising
3. RSI (1h) > 67
4. RSI < 38.5
5. MFI < 36

**In Plain English**:
> "Long-term trend is up, 1h RSI high, 5m RSI low, MFI also low — if this isn't a buy, what is?"

**Roast**: This strategy is really "clever rabbit with four burrows", one of 4 modes will always trigger! 🤣

---

## 4. Protection: Custom Stoploss + Confirm Exit

This strategy's protection is much more luxurious than previous strategies:

| Protection Type | Function | Plain English |
|---------|------|---------------|
| **Custom Stoploss** | Stoploss 1% after 280 minutes loss | "Lost for almost 5 hours, run, don't occupy the spot" |
| **Confirm Exit** | Block premature exit based on RSI | "RSI still high, let profits run more" |
| **Trailing Stop** | Automatically follows price after profit | "Activates after 3% profit, runs if 1% pullback" |

**Roast**: This strategy's protection is really luxurious, custom stoploss + confirm exit + trailing stop! 🤣

---

## 5. Exit Logic: More Complex Than Entry

### 5.1 Technical Exit: Two Modes

**Mode 1: Bollinger Band Upper**
```python
(Price > Bollinger Band upper)
AND (Previous price > Previous upper)
AND (Two candles ago price > Two candles ago upper)
```

**In Plain English**:
> "Price already broke above Bollinger Band upper, and 3 consecutive candles above upper — if you don't run now, what are you waiting for?"

**Mode 2: RSI Overbought**
```python
RSI > 77
```

**In Plain English**:
> "RSI already at 77 (overbought) — if you don't run now, what are you waiting for?"

### 5.2 Custom Stoploss: Loss Over 280 Minutes

**Trigger**:
```python
if (loss < 0) AND (holding time > 280 minutes):
    stoploss 1%
```

**In Plain English**:
> "Lost for almost 5 hours, don't wait, run, give spot to better trades!"

### 5.3 Confirm Exit: Block Premature Exit Based on RSI

**Trigger**:
```python
if exit_reason == "roi":
    if profit > 10% AND RSI > 34:
        block_exit (let profits run)
    elif profit > 3% AND RSI > 38:
        block_exit
    elif profit > 0% AND RSI > 50:
        block_exit
```

**In Plain English**:
> "Making good profit, RSI still high, don't run, let profits run more!"

**Roast**: This strategy is really "conflicted", one side wants stoploss, one side wants let profits run! 🤣

---

## 6. This Strategy's "Personality"

### ✅ Pros
1. **Multi-Strategy Combination**: 4 entry modes, covering different scenarios
2. **Informative Timeframe**: 1h confirms trend, reduces false signals
3. **Custom Stoploss**: Manages losing trades, frees up space
4. **Confirm Exit**: Blocks premature exit based on RSI
5. **Hyperopt Optimization**: Can auto-find best parameters
6. **Trailing Stop**: Automatically follows price after profit

### ⚠️ Cons
1. **High Complexity**: Multi-strategy + multi-indicator, headache to debug
2. **No BTC correlation**: Doesn't know when Bitcoin crashes
3. **Parameter sensitive**: Optimized parameters may overfit
4. **High Computation**: Multi-indicator + informative timeframe increases computation
5. **Almost no hard stoploss**: -99% stoploss is nominal

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| **Ranging Market** | Highly recommended | Multi-strategy combination most suitable for ranging markets |
| **Uptrend** | Highly recommended | Informative timeframe + trailing stop performs well |
| **Downtrend** | Auto pause | Informative timeframe blocks most trades |
| **High Volatility** | Adjust parameters | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |
| **BTC Crash** | Auto pause | Informative timeframe blocks entries |

---

## 8. Summary: How's This Strategy?

### One-Line Review
> **"A 4 entry modes, watches 1h trend, custom stoploss V7 version player"**

### Who Should Use It?
- ✅ People who like multi-strategy combination
- ✅ People who can accept some complexity
- ✅ People with quant basics
- ✅ Friends with VPS 2GB+ RAM

### Who Should NOT Use It?
- ❌ People who like simple strategies (this strategy has many conditions)
- ❌ People wanting to bottom-fish in downtrends (informative timeframe blocks)
- ❌ People who don't want to optimize parameters
- ❌ Pure quant beginners (need to understand multi-strategy combination)

### My Recommendations
1. **Paper trade first**: Run 2-4 weeks to see signal frequency
2. **Add filters**: Can add BTC correlation filter yourself
3. **Adjust parameters**: Can use Hyperopt to optimize parameters
4. **Watch BTC**: Although strategy has informative timeframe, manually pause when Bitcoin crashes hard

---

## 9. What Markets Make Money?

### 9.1 Core Logic: Multi-Strategy Combination Faith

CombinedBinHAndClucV7 is a collector, code about 300 lines, what's that concept? Equivalent to a long article 📄

**Its money-making philosophy**:
> "One strategy may lie, four strategies together won't all lie! Only trade when 1h trend is up, lie flat in downtrend!"

- **Multi-Strategy Faith**: 4 entry modes, one always fits current market
- **Informative Timeframe Faith**: 1h more reliable than 5m
- **Custom Stoploss Faith**: Run after 280 minutes loss
- **Confirm Exit Faith**: Let profits run if RSI still high

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐⭐ | Multi-strategy + informative timeframe + trailing stop, perfect match |
| 🔄 Wide Ranging | ⭐⭐⭐⭐☆ | Born for ranging markets, harvests back and forth |
| 📉 Single-sided Crash | ⭐⭐⭐☆☆ | Informative timeframe blocks most trades, auto lies flat |
| ⚡️ Extreme Sideways | ⭐⭐⭐☆☆ | Too little volatility, signals decrease but risk also low |

**One-Line Summary**: **Makes money in ranging and uptrend, auto lies flat in crash markets**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended Value | Roast |
|--------|--------|------|
| **Number of Pairs** | 20-60 | Recommended 20-60 pairs |
| **Quote Currency** | USDT | Don't use BTC/ETH as quote currency |
| **Max Open Trades** | 4-6 orders | Recommended 4-6 open trades |
| **Position Mode** | Unlimited stake | Recommended unlimited stake |
| **Timeframe** | 5m | Mandatory, can't change |

### 10.2 Hardware Requirements (Moderate Level)

This strategy uses multi-indicator + informative timeframe, moderate computation:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------|---------|---------|------|
| 20-40 pairs | 1GB | 2GB | Can run |
| 40-80 pairs | 2GB | 4GB | Comfortable |

**Warning**: Don't try with 512MB RAM VPS, this strategy consumes some resources 😅

### 10.3 Informative Timeframe Advantages

- **Trend Confirmation**: 1h trend way more reliable than 5m
- **Reduces False Signals**: Only trades when 1h trend is up
- **Auto Lies Flat**: Auto stops trading when 1h trend is down

**Roast**: This informative timeframe is better than many paid strategies! 🤣

### 10.4 Backtest vs Live

Strategy logic is complex, backtest and live differences mainly from:
- Hyperopt overfitting
- Informative timeframe data delays
- Custom stoploss behavior differences

**Recommended Process**:
1. Backtest first to see historical performance
2. Use Hyperopt to optimize parameters
3. Paper trade (Dry-Run) for 2-4 weeks
4. Small capital live test for 1 month

**Don't go all-in immediately**, even good strategies need breaking in!

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Strategy name is CombinedBinHAndClucV7**: Combined + BinH (BinHV45) + Cluc (ClucMay72018) + V7 (7th version)
   > "This name is telling you, this is a combination strategy, already 7th version!"

2. **Hard stoploss -99%**: Basically no hard stoploss
   > "This is real·relies on custom stoploss, hard stoploss is nominal!"

3. **Custom stoploss 280 minutes**: About 4.7 hours
   > "Lost for almost 5 hours and still don't run? Run, give spot to better trades!"

4. **Confirm exit based on RSI**: Don't let run if profit high and RSI high
   > "This is real·let profits run, RSI still high don't run!"

---

## 12. Last But Not Least

### One-Line Review
> **"Multi-strategy combination + informative timeframe, V7 version collector player"**

### Who Should Use It?
- ✅ People who like multi-strategy combination
- ✅ People who can accept some complexity
- ✅ People with quant basics
- ✅ Friends with VPS 2GB+ RAM

### Who Should NOT Use It?
- ❌ People who like simple strategies
- ❌ People wanting to bottom-fish in downtrends
- ❌ People who don't want to optimize parameters
- ❌ Pure quant beginners

### Manual Trading Recommendations
Manual traders can reference this strategy's multi-strategy approach:
- Observe both 5m and 1h trends simultaneously
- Use multi-strategy combination to cover different scenarios
- Set custom stoploss to manage losing trades

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtest is Beautiful, Live Trading Needs Caution

CombinedBinHAndClucV7's historical backtest performance may be **very excellent** — but there's a trap:

> **Multi-strategy + hyperopt optimization strategies easier to "fit" beautiful backtest curves, because many parameter combinations, may just "memorized" that historical period.**

Simply put: **Backtest data looks good, maybe because it just "remembered" how that period went.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Too few signals**: 4 modes may have no signals for long time
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
