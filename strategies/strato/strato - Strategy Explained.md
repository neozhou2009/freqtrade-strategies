# strato: The 1-Minute Ultra Short-Term Trader

> **Nickname**: One-Minute Hero  
> **Profession**: Quant world's "lightning player" — 1-minute timeframe, fast in fast out  
> **Timeframe**: 1 minute (ultra short-term player)

---

## 1. What's This Strategy?

Simply put, **strato** is:
- A strategy with only **2 indicators** (RSI + StochRSI)
- A **1-minute timeframe** strategy (ultra short-term)
- A **run at 1.2%** strategy (super fast turnover)

Like a lightning buyer who only looks at two indicators: "Is StochRSI oversold? Did K line golden cross? Both good? BUY! Overbought? SELL!" ⚡

---

## 2. Core Config: Basically "Fast In Fast Out"

### Profit-Taking Rules (ROI Table)

```
Make 1.2%? → RUN! (just this one level, super fast)
```

**Translation**: This strategy is classic "ultra short-term thinking", 1.2% and run, not greedy!

### Stoploss Rules

```
Hard stoploss: Cut at 10% loss
```

**Translation**: -10% stoploss is standard configuration, not wide not narrow!

---

## 3. Entry Conditions: Just 2 Conditions

### 🎯 StochRSI Oversold + K Line Confirmation

**Core Logic**:
1. StochRSI K < 18 (oversold)
2. K >= D (golden cross confirmation)

**In Plain English**:
> "StochRSI already at 18 below (oversold), K line also golden crossed D line — if this isn't a buy, what is?"

---

## 4. Protection: Standard Stoploss

This strategy's protection is simple:

| Protection Type | Function | Plain English |
|---------|------|---------------|
| **Hard Stoploss** | Cut at 10% loss | "If we're wrong, admit it. 10% is the line" |

**Roast**: This strategy's protection is so simple it's heartbreaking, but 1-minute trading needs speed! 🤣

---

## 5. Exit Logic: Sell When Overbought

### 5.1 Technical Exit: Just 2 Conditions

**Trigger**:
```python
(StochRSI K > 80) AND (D >= K)
```

**In Plain English**:
> "StochRSI already at 80 above (overbought), D line also death crossed K line — if you don't run now, what are you waiting for?"

---

### 5.2 ROI Exit: Just One Level, 1.2%

```
Profit      Hold Time    Trigger Exit
─────────────────────────────────────
1.2%       Anytime      Run when reached
```

**In Plain English**:
- Make 1.2%? → Run run run, secure the bag!

---

## 6. This Strategy's "Personality"

### ✅ Pros
1. **Simple to tears**: Just RSI + StochRSI, elementary school kids can understand
2. **Low Computation**: Few indicators, 512MB RAM can run it
3. **Low ROI**: 1.2% ROI, quick turnover
4. **Market Orders**: Ensures quick execution
5. **High Learning Value**: Suitable for learning StochRSI strategies

### ⚠️ Cons
1. **1-Minute Timeframe**: Signals extremely fast, needs low latency execution
2. **No trend filter**: No long-term trend judgment like EMA200
3. **No BTC correlation**: Doesn't know when Bitcoin crashes
4. **Fee Sensitive**: 1-minute trading is frequent, fees may exceed profits
5. **Many False Signals**: 1-minute level has many false signals

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| **Ranging Market** | Highly recommended | StochRSI's paradise |
| **Uptrend** | Recommended | Low ROI enables quick turnover |
| **Downtrend** | Pause | No trend filter, easy to lose consecutively |
| **High Volatility** | Adjust stoploss | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |
| **BTC Crash** | Pause | Big brother crashed, wait and see |

---

## 8. Summary: How's This Strategy?

### One-Line Review
> **"A StochRSI, 1-minute timeframe ultra short-term lightning player"**

### Who Should Use It?
- ✅ Quant veterans (1-minute trading needs experience)
- ✅ People who like ultra short-term
- ✅ Low-config VPS users (512MB RAM can run it)
- ✅ People wanting to learn StochRSI

### Who Should NOT Use It?
- ❌ Quant beginners (1-minute trading rhythm too fast)
- ❌ People chasing large trends (this is ultra short-term)
- ❌ Fee sensitive people (trading is frequent)
- ❌ High-frequency traders (this strategy not fast enough)

### My Recommendations
1. **Paper trade first**: Run 2-4 weeks to see fee impact
2. **Add filters**: Can add EMA200 trend filter yourself
3. **Adjust ROI**: Can adjust ROI based on market
4. **Watch BTC**: Manually pause when Bitcoin crashes hard

---

## 9. What Markets Make Money?

### 9.1 Core Logic: StochRSI Faith

strato is a lightning player, code about 40 lines, what's that concept? Equivalent to a SMS message 📱

**Its money-making philosophy**:
> "StochRSI oversold then buy, overbought then sell, 1.2% and run isn't great?"

- **StochRSI Faith**: RSI's stochastic indicator, more sensitive
- **K/D Cross Faith**: Golden cross buy death cross sell, classic and effective
- **Fast In Fast Out Faith**: 1.2% ROI and run, not greedy

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐☆☆ | 1-minute signals fast, but many false signals |
| 🔄 Wide Ranging | ⭐⭐⭐⭐☆ | Born for ranging markets, harvests back and forth |
| 📉 Single-sided Crash | ⭐⭐☆☆☆ | No trend filter, easy to lose consecutively |
| ⚡️ Extreme Sideways | ⭐⭐☆☆☆ | Too little volatility, signals decrease |

**One-Line Summary**: **Makes money in ranging markets, uptrend also okay, be careful in crash markets**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended Value | Roast |
|--------|--------|------|
| **Number of Pairs** | 10-20 | 1m signals extremely fast, don't use too many |
| **Quote Currency** | USDT | Don't use BTC/ETH as quote currency |
| **Max Open Trades** | 1-3 orders | Control risk |
| **Position Mode** | Fixed position | Recommended fixed, control risk |
| **Timeframe** | 1m | Mandatory, can't change |

### 10.2 Hardware Requirements (This Strategy is Friendly!)

This strategy has low computation, very low VPS requirements:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------|---------|---------|------|
| 10-20 pairs | 512MB | 1GB | Easy run |
| 20-40 pairs | 1GB | 2GB | Very comfortable |

**Warning**: 512MB RAM VPS can also run, this strategy is quite friendly! 😅

### 10.3 1-Minute Trading Risks

- **Fee Impact**: Trading is frequent, fees may exceed profits
- **Slippage Risk**: 1-minute price fluctuates fast, slippage may be large
- **Latency Sensitive**: Needs low latency execution, VPS location important

**Roast**: 1-minute trading is like "dancing on knife edge", exciting but dangerous! 🤣

### 10.4 Backtest vs Live

Strategy logic is simple, backtest and live differences are small, but note:
- Fee and slippage impact
- 1-minute data quality

**Recommended Process**:
1. Backtest first to see historical performance (consider fees)
2. Paper trade (Dry-Run) for 2-4 weeks
3. Calculate fee as percentage of profit
4. Small capital live test for 1 month

**Don't go all-in immediately**, 1-minute trading is risky!

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Strategy name is strato**: Maybe abbreviation of Strategy
   > "Simple and rough, just call it strato!"

2. **ROI only 1.2%**: Much lower than common strategies
   > "This is real·ultra short-term, 1.2% and run isn't great?"

3. **Market orders**: entry/exit/stoploss all market
   > "This is real·quick execution, don't wait for limit orders!"

---

## 12. Last But Not Least

### One-Line Review
> **"StochRSI + 1-Minute Timeframe, lightning ultra short-term player"**

### Who Should Use It?
- ✅ Quant veterans (1-minute trading needs experience)
- ✅ People who like ultra short-term
- ✅ Low-config VPS users
- ✅ People wanting to learn StochRSI

### Who Should NOT Use It?
- ❌ Quant beginners
- ❌ People chasing large trends
- ❌ Fee sensitive people
- ❌ High-frequency traders

### Manual Trading Recommendations
Manual traders can reference this strategy's StochRSI approach:
- K < 18 + K >= D → Consider buying
- K > 80 + D >= K → Consider selling
- Set strict stoploss (e.g., -5%)

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtest is Beautiful, Live Trading Needs Caution

strato's historical backtest performance may be **very excellent** — but there's a trap:

> **1-minute strategies often perform very well in backtests, because historical data always has suitable periods, but this doesn't mean future will.**

Simply put: **Backtest data looks good, maybe because it just "encountered" that period.**

### Hidden Risks of 1-Minute Trading

In live trading, 1-minute trading may cause:
- **Fees eat profits**: Trading is frequent, fees may exceed profits
- **Slippage risk**: 1-minute price fluctuates fast, slippage may be large
- **Many false signals**: 1-minute level has many false signals

### My Recommendations (Real Talk)

```
1. Test with minimum capital first (e.g., 100U)
2. Run live for at least 2-4 weeks, calculate fee as percentage of profit
3. Confirm performance in ranging markets
4. Consider adding trend filter yourself (e.g., EMA200)
```

**Remember**: 1-minute trading is like "dancing on knife edge", surviving is most important!

---

**Final Reminder**: No matter how good the strategy, market won't say hi when teaching you a lesson. Light position test, surviving is most important! 🙏
