# MACD_TRI_EMA: The "Classic Combo" Momentum Trader

> **Nickname**: The Momentum Whiz  
> **Profession**: Quant world's "minimalist" — if two indicators can solve it, never use three  
> **Timeframe**: 5 minutes (short-term player)

---

## 1. What Is This Thing?

Simply put, **MACD_TRI_EMA** is:
- A strategy with only **2 indicators** (MACD + TEMA)
- A **golden cross buy, death cross sell** classic strategy
- A **strict stoploss** strategy (-3% and run)

Like a decisive buyer who only looks at two indicators: "MACD golden cross? Price above TEMA? Both satisfied, buy!" ⚡

This strategy's logic is very simple:
1. Watch MACD golden cross (momentum turning strong)
2. Confirm price above TEMA (trend up)
3. Buy when both conditions met
4. Sell on MACD death cross

That's it, none of those fancy bells and whistles! 🤣

---

## 2. Core Config: Basically "Fast In Fast Out"

### Profit-Taking Rules (ROI Table)

```
Hold 10 min make 15%? → Run! (Big win)
Hold 15 min make 6%? → Run! (Medium win)
Hold 30 min make 4%? → Run! (Small win)
Hold 120 min? → Run at breakeven! (No loss)
```

**Translation**: This strategy is typical short-term thinking, 15% in 10 minutes most ideal, longer time lower requirements, breakeven after 2 hours!

**Roast**: This ROI table design is very "greedy" — high returns short-term, breakeven long-term. Typical "run fast after winning, don't linger after losing" thinking! 🤣

### Stoploss Rules

```
Hard stoploss: Cut at 3% loss (strict enough)
Trailing stop: None (exits via technical signals)
```

**Translation**: -3% stoploss is really strict, cut on slightest wrong move, typical "cut losses" thinking!

---

## 3. Entry Conditions: Just 2 Conditions

This strategy's entry conditions are simple and clear:

### 🎯 MACD Golden Cross + TEMA Trend Filter

**Core Logic**:
1. MACD golden cross (MACD line crosses above signal line)
2. Price above TEMA

**In Plain English**:
> "MACD already golden crossed (momentum turning strong), and price above TEMA (trend up) — not buying this?"

**Code Translation**:
```python
# Entry conditions
(MACD Golden Cross) AND (Previous candle price > TEMA)
```

**Roast**: This entry condition is really "classic" — MACD golden cross is one of oldest buy signals, used since 1970s!

---

## 4. Protection Mechanisms: Strict Stoploss

This strategy's protection mechanisms are simple but effective:

| Protection Type | Function | In Plain English |
|----------------|----------|------------------|
| **Hard Stoploss** | Cut at 3% loss | "3% loss means judgment wrong, run fast" |
| **TEMA Filter** | Ensures trend up | "Only buy when price above TEMA, don't play counter-trend" |

**Roast**: This strategy's protection is so simple it's heartbreaking, but -3% stoploss is really strict!

**Special Note**:
- No trailing stop
- No dynamic take-profit
- No entry protection parameters (other strategies easily have 30+ layers)
- Just one hard stoploss, simple to the extreme!

---

## 5. Exit Logic: Run on MACD Death Cross

### 5.1 Technical Exit: Just 1 Condition

**Trigger Condition**:
```python
MACD Death Cross (Signal line crosses above MACD line)
```

**In Plain English**:
> "MACD already death crossed (momentum turning weak), not running this waiting for what?"

**Roast**: Exit condition is just one MACD death cross, simple and brutal, no dragging!

---

### 5.2 ROI Exit: 4-Level Take-Profit

```
Profit      Hold Time    Trigger Exit
─────────────────────────────────────
15%        10 min       Run when reached (Big win)
6%         15 min       Run when reached (Medium win)
4%         30 min       Run when reached (Small win)
0%         120 min      Run at breakeven (No loss)
```

**In Plain English**:
- Hold 10 min make 15%? → Manna from heaven, run fast!
- Hold half hour make 4%? → Not bad, run!
- Hold 2 hours no profit? → Run at breakeven, not playing!

**Exit Priority**:
1. MACD death cross (technical signal)
2. ROI reached (profit target)
3. Hard stoploss (-3%)

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Simple to Tears**: Just 2 indicators, elementary students can understand
2. **Symmetric Signals**: Golden cross buy, death cross sell, logic clear
3. **TEMA Low Latency**: Faster reaction than traditional EMA
4. **Strict Stoploss**: -3% stoploss controls risk
5. **Low Computation**: Few indicators, low hardware requirements
6. **Short Code**: 40 lines of code, can finish in one glance

### ⚠️ Cons (Roast Section)

1. **No Long-Term Trend Filter**: No long-term trend judgment like EMA200
2. **No BTC Correlation**: Doesn't know when Bitcoin crashes
3. **Stoploss Too Strict**: -3% stoploss may trigger frequently in high volatility
4. **Fixed Parameters**: MACD and TEMA parameters not adjustable
5. **Example Nature**: Strategy is simple, suitable for learning not production

**Roast Summary**: This strategy is like a "minimalist" — if two indicators can solve it, never add a third! 🤣

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **Ranging Market** | Not Recommended | MACD has many false signals in ranging |
| **Uptrend** | Recommended | TEMA filter ensures trend-following trades |
| **Downtrend** | Pause | No trend filter, easy to lose consecutively |
| **High Volatility** | Adjust Stoploss | May need to widen stoploss to -5% |
| **Low Volatility** | Adjust ROI | Lower ROI thresholds for small volatility |
| **BTC Crash** | Pause | Big brother crashed, watch first |

---

## 8. Summary: How Is This Strategy Really?

### One-Line Review
> **"A concise momentum trader using classic MACD + TEMA combo"**

### Who Should Use It?
- ✅ Quant beginners (simple code, easy to understand)
- ✅ People who like simple strategies
- ✅ Low-spec VPS users (512MB RAM can run)
- ✅ Those wanting to learn MACD applications

### Who Should NOT Use It?
- ❌ People chasing high win rate (MACD has many false signals in ranging)
- ❌ Those wanting to bottom fish in downtrends (no trend filter)
- ❌ People wanting loose stoploss (-3% is really strict)
- ❌ Those expecting "overnight riches"

### My Recommendations
1. **Paper Trade First**: Run 2-4 weeks to check signal frequency
2. **Add Filters**: Can add EMA200 trend filter yourself
3. **Adjust Stoploss**: High volatility coins can widen to -5%
4. **Watch BTC**: Manually pause strategy when Bitcoin crashes hard

---

## 9. What Markets Make Money With This?

### 9.1 Core Logic: Faith in Momentum Continuation

MACD_TRI_EMA is a minimalist, code only 40 lines, what concept? Equivalent to length of a text message 📱

**Its Money-Making Philosophy**:
> "Buy when momentum turns strong, sell when momentum turns weak, only trade when trend up, strict stoploss to survive!"

- **MACD Faith**: Golden/death cross is classic momentum signal
- **TEMA Faith**: Triple exponential smoother more reliable than single
- **Fast In Fast Out**: Short-term high return expectations, lower requirements longer time

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|------------|-------------------|--------------------------|
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐☆ | Momentum strategy performs well in uptrends |
| 🔄 Wide Ranging | ⭐⭐☆☆☆ | MACD has many false signals in ranging |
| 📉 One-Way Crash | ⭐⭐☆☆☆ | No trend filter, easy to lose consecutively |
| ⚡ Extreme Sideways | ⭐⭐☆☆☆ | Too little volatility, signals reduce |

**One-Line Summary**: **Makes money in uptrends, many false signals in ranging, be careful in crashes**

---

## 10. Want to Run This? Check These Configs First

### 10.1 Pair Configuration

| Config | Recommended Value | Roast |
|--------|------------------|-------|
| **Number of Pairs** | 20-40 pairs | Moderate signal frequency |
| **Quote Currency** | USDT | Don't use BTC/ETH as quote |
| **Max Open Trades** | 3-6 orders | Control risk |
| **Position Mode** | Fixed Position | Recommend fixed, control risk |
| **Timeframe** | 5m | Mandatory, can't change |

### 10.2 Hardware Requirements (This Strategy Is Friendly!)

This strategy has minimal computation, very low VPS requirements:

| Pairs | Minimum RAM | Recommended RAM | Experience |
|-------|-------------|-----------------|------------|
| 20-40 | 512MB | 1GB | Runs easily |
| 40-80 | 1GB | 2GB | Very comfortable |

**Warning**: This is one of the few quant strategies that can run on a Raspberry Pi! 😅

### 10.3 Backtest vs Live Trading

MACD and TEMA are both lagging indicators, backtest and live trading differences are small.

**Recommended Process**:
1. Backtest first to see historical performance
2. Paper trade (Dry-Run) for 2-4 weeks
3. Observe if MACD cross signals meet expectations
4. Small capital live test for 1 month

**Don't go all-in immediately**, no matter how simple the strategy needsbreak-in period!

---

## 11. Easter Egg: The Author's "Little Tricks"

Look carefully at the code, you'll find interesting things:

1. **Strategy Name MACD_TRI_EMA**: TRI might be TEMA abbreviation
   > "Why not call it MACD_TEMA directly? Maybe sounds better!"

2. **ROI Has 4 Levels**: More than common strategies
   > "15% in 10min, 6% in 15min, 4% in 30min, breakeven in 120min — this is forcing you fast in fast out!"

3. **Stoploss Only -3%**: Stricter than common strategies
   > "This stoploss is really strict, cut on slightest wrong move, typical 'cut losses' thinking!"

4. **Entry Uses shift(1)**: Delayed confirmation
   > "Use previous candle confirmation, avoid future function issues — this is old driver's writing!"

---

## 12. Final Final Words

### One-Line Review
> **"Simple doesn't mean weak, sometimes the simplest strategies are most effective"**

### Who Should Use It?
- ✅ Quant beginners (top choice for entry)
- ✅ People who like simple strategies
- ✅ Low-spec VPS users
- ✅ Those wanting to learn MACD applications

### Who Should NOT Use It?
- ❌ People chasing high win rate
- ❌ Those wanting to bottom fish in downtrends
- ❌ People wanting loose stoploss
- ❌ Those expecting "overnight riches"

### Manual Trading Recommendations
Manual traders can reference this strategy's MACD + TEMA approach:
- Observe MACD golden/death cross signals
- Confirm price above TEMA
- Set strict stoploss (e.g., -3%)

---

## 13. ⚠️ Risk Reminder Again (MUST READ This Section)

### Backtests Are Beautiful, Live Trading Needs Caution

MACD_TRI_EMA's historical backtest performance may be **very excellent** — but here's a trap:

> **Momentum strategies often perform very well in backtests, because historical data always has some big trends, but this doesn't guarantee future trends.**

Simply put: **Backtest data looks good, maybe because itjust "met" that trend period.**

### Hidden Risks of Momentum Strategies

In live trading, momentum strategies may lead to:
- **Ranging Market Losses**: MACD has many false signals in ranging, may lose consecutively
- **Frequent Stoploss**: -3% stoploss may trigger frequently in high volatility
- **Trend Reversal**: When momentum suddenly reverses, death cross signals may lag

### Traps of Simple Strategies

Don't be fooled by "simple and effective":
- **No Long-Term Trend Filter**: May lose consecutively in downtrends
- **No BTC Correlation**: Still buying whenmarket crashes
- **Stoploss Too Strict**: May get stopped out frequently

### My Recommendations (Real Talk)

```
1. Test with minimum capital first (e.g., 100U)
2. Run live at least 2-4 weeks, observe signal frequency
3. Confirm performance in ranging markets (may lose consecutively)
4. Consider adding trend filter yourself (e.g., EMA200)
5. Manually pause strategy when Bitcoin crashes hard
```

**Remember**: Momentum strategies most afraid of ranging markets, survival is most important!

---

**Final Reminder**: No matter how good the strategy, the market won't say hello before teaching you a lesson. Light positions for testing, survival is most important! 🙏
