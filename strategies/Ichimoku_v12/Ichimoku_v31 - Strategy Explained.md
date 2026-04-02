# Ichimoku_v31: The Japanese Samurai V31

> **Nickname**: Japanese Samurai V31  
> **Profession**: Quant world's "Japanese exchange student" — using 70-year-old Japanese technical indicators, already version 31  
> **Timeframe**: 1 hour (medium-term player)

---

## 1. What's This Strategy?

Simply put, **Ichimoku_v31** is:
- A strategy using **Ichimoku Cloud**
- A strategy using **Heikin Ashi candles**
- A strategy that watches **4h big trend**

Like a cautious buyer using Japanese indicators: "Did Heikin Ashi cross above cloud? Is 4h cloud green? Both good? BUY! Break below cloud? SELL!" 🇯🇵

---

## 2. Core Config: Basically "Follow the Trend"

### Profit-Taking Rules (ROI Table)

```
Make 10% right after buying? → RUN!
Hold 30 minutes and make 5%? → RUN!
Hold 60 minutes and make 2%? → RUN!
```

**Translation**: This strategy is classic "trend following thinking", 10% ROI is relatively high, expecting to capture large trends!

### Stoploss Rules

```
Hard stoploss: Cut at 10% loss
Trailing stop: Activates after 2% profit, runs if 1% pullback
```

**Translation**: Standard configuration, not wide not narrow!

---

## 3. Entry Conditions: Just 2 Conditions

### 🎯 Heikin Ashi + Cloud Breakout

**Core Logic**:
1. 4h Heikin Ashi close crosses above cloud (senkou_a or senkou_b)
2. Previous candle below cloud
3. 4h cloud is green

**In Plain English**:
> "4h Heikin Ashi already crossed above cloud (breakout), and cloud is green (uptrend) — if this isn't a buy, what is?"

---

## 4. Protection: Cloud Filtering + Trailing Stop

This strategy's protection is simple but effective:

| Protection Type | Function | Plain English |
|---------|------|---------------|
| **Hard Stoploss** | Cut at 10% loss | "If we're wrong, admit it. 10% is the line" |
| **Trailing Stop** | Automatically follows price after profit | "Activates after 2% profit, runs if 1% pullback" |
| **Cloud Filtering** | Only buy when 4h cloud is green | "Don't buy if cloud not green, auto filters downtrends" |

**Roast**: This strategy's cloud filtering is really useful, auto filters downtrends! 🤣

---

## 5. Exit Logic: Run When Break Below Cloud

### 5.1 Technical Exit: Just 1 Condition

**Trigger**:
```python
(4h Heikin Ashi close < senkou_a) OR (4h Heikin Ashi close < senkou_b)
```

**In Plain English**:
> "4h Heikin Ashi already broke below cloud (trend weakening) — if you don't run now, what are you waiting for?"

---

### 5.2 ROI Exit: 3-Level Profit Taking

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
1. **Ichimoku Cloud**: Cloud filters trends, classic and effective
2. **Heikin Ashi**: Smooth candles reduce noise
3. **Multi-Timeframe**: 4h confirms trend, reduces false signals
4. **Market Orders**: Ensures quick execution
5. **Low Computation**: Few indicators, 512MB RAM can run it
6. **Trailing Stop**: Automatically follows price after profit

### ⚠️ Cons
1. **No BTC correlation**: Doesn't know when Bitcoin crashes
2. **1h Timeframe**: Signal frequency lower than 5m
3. **Fixed parameters**: Ichimoku Cloud parameters fixed
4. **Market order slippage**: Market orders may have slippage
5. **Cloud lag**: Cloud calculation has lag

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| **Uptrend** | Highly recommended | Cloud filtering + multi-timeframe, perfect match |
| **Ranging Market** | Not recommended | Trend strategy has many false signals in ranging |
| **Downtrend** | Auto pause | Cloud filtering blocks most trades |
| **High Volatility** | Adjust parameters | May need to adjust stoploss threshold |
| **Low Volatility** | Adjust ROI | Lower ROI threshold for small moves |
| **BTC Crash** | Auto pause | Cloud filtering blocks entries |

---

## 8. Summary: How's This Strategy?

### One-Line Review
> **"An Ichimoku Cloud, Heikin Ashi, watches 4h trend Japanese Samurai V31"**

### Who Should Use It?
- ✅ Quant beginners (simple code, easy to understand)
- ✅ People who like simple strategies
- ✅ Low-config VPS users (512MB RAM can run it)
- ✅ People wanting to learn Ichimoku Cloud

### Who Should NOT Use It?
- ❌ People wanting to make money in ranging markets (trend strategy has many false signals)
- ❌ People wanting to bottom-fish in downtrends (cloud filtering blocks)
- ❌ People wanting complex strategies
- ❌ High-frequency traders (1h signals less than 5m)

### My Recommendations
1. **Paper trade first**: Run 2-4 weeks to see signal frequency
2. **Add filters**: Can add BTC correlation filter yourself
3. **Watch BTC**: Although strategy has cloud filtering, manually pause when Bitcoin crashes hard

---

## 9. What Markets Make Money?

### 9.1 Core Logic: Ichimoku Cloud Faith

Ichimoku_v31 is a Japanese Samurai, code about 80 lines, what's that concept? Equivalent to a long Weibo post 📱

**Its money-making philosophy**:
> "Heikin Ashi crosses above cloud then buy, breaks below cloud then sell, 4h cloud green more reassuring, make big money and run isn't great?"

- **Ichimoku Cloud Faith**: Cloud filters trends, classic and effective
- **Heikin Ashi Faith**: Smooth candles reduce noise
- **Multi-Timeframe Faith**: 4h more reliable than 1h

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐⭐ | Cloud filtering + multi-timeframe, perfect match |
| 🔄 Wide Ranging | ⭐⭐☆☆☆ | Trend strategy has many false signals in ranging |
| 📉 Single-sided Crash | ⭐⭐⭐☆☆ | Cloud filtering blocks most trades, auto lies flat |
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
| **Timeframe** | 1h | Mandatory, can't change |

### 10.2 Hardware Requirements (This Strategy is Friendly!)

This strategy has low computation, very low VPS requirements:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------|---------|---------|------|
| 20-40 pairs | 512MB | 1GB | Easy run |
| 40-80 pairs | 1GB | 2GB | Very comfortable |

**Warning**: 512MB RAM VPS can also run, this strategy is quite friendly! 😅

### 10.3 Cloud Filtering Advantages

- **Trend Confirmation**: 4h cloud more reliable than 1h
- **Reduces False Signals**: Only trades when cloud is green
- **Auto Lies Flat**: Auto stops trading when cloud is red

**Roast**: This cloud filtering is better than many paid strategies! 🤣

### 10.4 Backtest vs Live

Strategy logic is simple, backtest and live differences are small, but note:
- Cloud lag
- Market order slippage

**Recommended Process**:
1. Backtest first to see historical performance
2. Paper trade (Dry-Run) for 2-4 weeks
3. Observe if cloud filtering works properly
4. Small capital live test for 1 month

**Don't go all-in immediately**, even simple strategies need breaking in!

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Strategy name is Ichimoku_v31**: Ichimoku + v31 (31st version)
   > "This name is telling you, this is an Ichimoku Cloud strategy, already 31st version!"

2. **Heikin Ashi candles**: Smooth price noise
   > "This is real·reduce noise, regular candles too messy!"

3. **Market orders**: entry/exit/stoploss all market
   > "This is real·quick execution, don't wait for limit orders!"

---

## 12. Last But Not Least

### One-Line Review
> **"Ichimoku Cloud + Heikin Ashi, Japanese Samurai V31 intermediate player"**

### Who Should Use It?
- ✅ Quant beginners (simple code, easy to understand)
- ✅ People who like simple strategies
- ✅ Low-config VPS users
- ✅ People wanting to learn Ichimoku Cloud

### Who Should NOT Use It?
- ❌ People wanting to make money in ranging markets
- ❌ People wanting to bottom-fish in downtrends
- ❌ People wanting complex strategies
- ❌ High-frequency traders

### Manual Trading Recommendations
Manual traders can reference this strategy's Ichimoku Cloud approach:
- Use Heikin Ashi to smooth price
- Observe both 1h and 4h cloud simultaneously
- Set standard stoploss (e.g., -10%)

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtest is Beautiful, Live Trading Needs Caution

Ichimoku_v31's historical backtest performance may be **very excellent** — but there's a trap:

> **Trend strategies often perform very well in backtests, because historical data always has trending periods, but this doesn't mean future will definitely trend.**

Simply put: **Backtest data looks good, maybe because it just "encountered" that trending period.**

### Hidden Risks of Trend Strategies

In live trading, trend strategies may cause:
- **Ranging market losses**: Trend strategy has many false signals in ranging markets
- **Cloud lag**: Cloud calculation has lag
- **Market order slippage**: Market orders may have slippage

### My Recommendations (Real Talk)

```
1. Test with minimum capital first (e.g., 100U)
2. Run live for at least 2-4 weeks, observe ranging market performance
3. Consider adding BTC correlation filter yourself
4. Note cloud lag
```

**Remember**: Trend strategies most fear ranging markets, surviving is most important!

---

**Final Reminder**: No matter how good the strategy, market won't say hi when teaching you a lesson. Light position test, surviving is most important! 🙏
