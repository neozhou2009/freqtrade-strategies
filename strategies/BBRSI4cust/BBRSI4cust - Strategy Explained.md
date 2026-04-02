# BBRSI4cust: The Custom Exit Mean Reversion Player

> **Nickname**: Exit Master  
> **Profession**: Quant world's "flexible player" — simple entry, flexible exit  
> **Timeframe**: 15 minutes (not impatient)

---

## 1. What's This Strategy?

Simply put, **BBRSI4cust** is:
- A strategy with only **3 indicators** (PLUS_DI, RSI, Bollinger Bands)
- A **custom exit** strategy (doesn't use traditional sell signals)
- A **run at 0.3%** strategy (super fast turnover)

Like a smart buyer who waits for sales: "Is PLUS_DI going up? Did price break Bollinger Band? Both good? BUY! Break middle band? RUN!" 🛒

---

## 2. Core Config: Basically "Buy Low, Sell High"

### Profit-Taking Rules (ROI Table)

```
Make 0.3%? → RUN! (just this one level, super fast)
```

**Translation**: This strategy is classic "small profits quick turnover" thinking, 0.3% and run, not greedy!

### Stoploss Rules

```
Hard stoploss: Cut at 10% loss
Trailing stop: Yes, but no specific parameters configured
```

---

## 3. Entry Conditions: Just 2 Conditions

### 🎯 PLUS_DI + Bollinger Band Breakout

**Core Logic**:
1. PLUS_DI > threshold (default 20)
2. Price breaks below Bollinger Band lower band

**In Plain English**:
> "PLUS_DI is already going up (upward momentum), price broke below Bollinger Band lower band (oversold) — if this isn't a buying opportunity, what is?"

---

## 4. Protection: Dual Exit

This strategy's protection has a feature:

| Protection Type | Function | Plain English |
|---------|------|---------------|
| **Hard Stoploss** | Cut at 10% loss | "If we're wrong, admit it. 10% is the line" |
| **Trailing Stop** | Automatically follows price after profit | "Has trailing, but parameters not specified" |
| **Custom Exit** | Exit when price breaks middle band | "Break middle band and run, don't wait for signal" |

**Roast**: This strategy's exit mechanism is really flexible, technical signals + custom exit dual protection! 🤣

---

## 5. Exit Logic: More Flexible Than Entry

### 5.1 Technical Exit: Price Breaks Middle Band

**Trigger**:
```python
Price crosses above Bollinger Band middle band
```

**In Plain English**:
> "Price already broke through Bollinger Band middle band, mean reversion complete — if you don't run now, what are you waiting for?"

### 5.2 Custom Exit: Real-time Monitoring

**Trigger**:
```python
if current_price > Bollinger_Band_middle_band:
    return "bb_profit_sell"
```

**In Plain English**:
> "Real-time price monitoring, exit when breaks middle band, don't wait for candle close!"

**Roast**: This strategy is really "flexible", two ways to exit! 🤣

---

### 5.3 ROI Exit: Just One Level, 0.3%

```
Profit      Hold Time    Trigger Exit
─────────────────────────────────────
0.3%       Anytime      Run when reached
```

**In Plain English**:
- Make 0.3%? → Run run run, secure the bag!

---

## 6. This Strategy's "Personality"

### ✅ Pros
1. **Custom Exit**: Flexible control of sell timing
2. **Hyperopt Optimization**: Can auto-find best Bollinger Band std dev
3. **Dual Exit**: Technical signals + custom exit
4. **Low Computation**: Few indicators, 512MB RAM can run it
5. **Low ROI**: 0.3% ROI, quick turnover

### ⚠️ Cons
1. **No trend filter**: No long-term trend judgment like EMA200
2. **No BTC correlation**: Doesn't know when Bitcoin crashes
3. **Very Low ROI**: 0.3% ROI may exit large trends too early
4. **15m Timeframe**: Signal frequency lower than 5 minutes
5. **Parameter sensitive**: Bollinger Band std dev needs optimization

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| **Ranging Market** | Highly recommended | Mean reversion's paradise |
| **Uptrend** | Recommended | Low ROI enables quick turnover |
| **Downtrend** | Pause | No trend filter, easy to lose consecutively |
| **High Volatility** | Adjust parameters | May need to adjust Bollinger Band std dev |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |
| **BTC Crash** | Pause | Big brother crashed, wait and see |

---

## 8. Summary: How's This Strategy?

### One-Line Review
> **"A PLUS_DI + Bollinger Bands, custom exit mean reversion player"**

### Who Should Use It?
- ✅ Quant beginners (simple code, easy to understand)
- ✅ People who like simple strategies
- ✅ Low-config VPS users (512MB RAM can run it)
- ✅ People wanting to learn custom_exit

### Who Should NOT Use It?
- ❌ People chasing large trends (0.3% ROI too "conservative")
- ❌ People wanting to bottom-fish in downtrends
- ❌ People wanting complex strategies
- ❌ High-frequency traders (15m signals less than 5m)

### My Recommendations
1. **Paper trade first**: Run 2-4 weeks to see signal frequency
2. **Add filters**: Can add EMA200 trend filter yourself
3. **Adjust parameters**: Can use Hyperopt to optimize Bollinger Band std dev
4. **Watch BTC**: Manually pause when Bitcoin crashes hard

---

## 9. What Markets Make Money?

### 9.1 Core Logic: Mean Reversion Faith

BBRSI4cust is a flexible player, code about 100 lines, what's that concept? Equivalent to a long Weibo post 📱

**Its money-making philosophy**:
> "Price dropped too hard will always return, I just wait for that Bollinger Band break moment, make 0.3% and run isn't great?"

- **Bollinger Band Faith**: Price 95% of time within 2 standard deviations
- **Mean Reversion Faith**: Price returning from lower band to middle band is high probability
- **Small Profits Faith**: 0.3% quick turnover, accumulate small gains

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐☆ | Mean reversion + low ROI, performs well |
| 🔄 Wide Ranging | ⭐⭐⭐⭐⭐ | Born for ranging markets, harvests back and forth |
| 📉 Single-sided Crash | ⭐⭐☆☆☆ | No trend filter, easy to lose consecutively |
| ⚡️ Extreme Sideways | ⭐⭐⭐☆☆ | Too little volatility, signals decrease but risk also low |

**One-Line Summary**: **Makes money in ranging markets, uptrend also good, crash markets be careful**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended Value | Roast |
|--------|--------|------|
| **Number of Pairs** | 20-40 | Moderate signal frequency |
| **Quote Currency** | USDT | Don't use BTC/ETH as quote currency |
| **Max Open Trades** | 3-6 orders | Control risk |
| **Position Mode** | Fixed position | Recommended fixed, control risk |
| **Timeframe** | 15m | Mandatory, can't change |

### 10.2 Hardware Requirements (This Strategy is Friendly!)

This strategy has low computation, very low VPS requirements:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------|---------|---------|------|
| 20-40 pairs | 512MB | 1GB | Easy run |
| 40-80 pairs | 1GB | 2GB | Very comfortable |

**Warning**: 512MB RAM VPS can also run, this strategy is quite friendly! 😅

### 10.3 Custom Exit Advantages

- **Real-time Monitoring**: Not limited by candle close
- **Flexible Control**: Can add any exit conditions
- **Improved Timeliness**: Reduces signal delays

**Roast**: This exit mechanism is more flexible than many paid strategies! 🤣

### 10.4 Backtest vs Live

Strategy logic is simple, backtest and live differences are small.

**Recommended Process**:
1. Backtest first to see historical performance
2. Paper trade (Dry-Run) for 2-4 weeks
3. Observe if custom exit works properly
4. Small capital live test for 1 month

**Don't go all-in immediately**, even simple strategies need breaking in!

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Strategy name is BBRSI4cust**: BB (Bollinger Bands) + RSI + 4 (for) + cust (custom)
   > "This name is telling you, this is a Bollinger Bands + RSI strategy with custom exit!"

2. **ROI only 0.3%**: Much lower than common strategies
   > "This is real·small profits quick turnover, 0.3% and run isn't great?"

3. **Dual Bollinger Band System**: buy_bb and sell_bb can be set separately
   > "Entry and exit can use different Bollinger Bands, flexible!"

---

## 12. Last But Not Least

### One-Line Review
> **"Custom Exit + Dual Exit, flexible mean reversion player"**

### Who Should Use It?
- ✅ Quant beginners (simple code, easy to understand)
- ✅ People who like simple strategies
- ✅ Low-config VPS users
- ✅ People wanting to learn custom_exit

### Who Should NOT Use It?
- ❌ People chasing large trends
- ❌ People wanting to bottom-fish in downtrends
- ❌ People wanting complex strategies
- ❌ High-frequency traders

### Manual Trading Recommendations
Manual traders can reference this strategy's custom exit approach:
- Set price breakout above Bollinger Band middle band to exit
- Use PLUS_DI to confirm upward momentum
- Set strict stoploss (e.g., -10%)

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtest is Beautiful, Live Trading Needs Caution

BBRSI4cust's historical backtest performance may be **very excellent** — but there's a trap:

> **Mean reversion strategies often perform very well in backtests, because historical data always has ranging periods, but this doesn't mean future will definitely range.**

Simply put: **Backtest data looks good, maybe because it just "encountered" that ranging period.**

### Hidden Risks of Mean Reversion

In live trading, mean reversion strategies may cause:
- **Single-sided market losses**: May lose consecutively in single-sided markets
- **Exit too early**: 0.3% ROI may miss large trends
- **Parameter overfitting**: Bollinger Band std dev may overfit

### My Recommendations (Real Talk)

```
1. Test with minimum capital first (e.g., 100U)
2. Run live for at least 2-4 weeks, observe ranging market performance
3. Use Hyperopt to optimize parameters but verify
4. Consider adding trend filter yourself (e.g., EMA200)
```

**Remember**: Mean reversion strategies most fear single-sided markets, surviving is most important!

---

**Final Reminder**: No matter how good the strategy, market won't say hi when teaching you a lesson. Light position test, surviving is most important! 🙏
