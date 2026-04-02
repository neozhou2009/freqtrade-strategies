# BigZ03: The "Classic Old Cannon" in Quant World

> **Nickname**: Classic Old Cannon  
> **Profession**: "Founding Father" of BigZ Series  
> **Timeframe**: 5 minutes (entry) + 1 hour (confirmation)

---

## 1. What Is This Thing?

Simply put, **BigZ03** is:
- The "original authentic" BigZ series
- Core philosophy: Low drawdown, quick sell, high capital efficiency
- 12 entry conditions, cover various oversold patterns

Like an experienced old hunter, doesn't greed for big prey, steady and sure 🎯

**One-Sentence Summary**: "Conservative party's first choice" pursuing stability and disliking drawdown

---

## 2. Core Config: Simply "Make Some and Run"

### Profit-Taking Rules (ROI Table)

```
Holding 0-10 min: Make 2.8% and run
Holding 10-40 min: Make 1.8% is also okay
Holding 40-180 min: Make 0.5% makes do
Holding 180+ min: Make 1.8% leave
```

**Translation**: Core philosophy is "fast"! 2.8% isn't much, but make it fast, high capital turnover efficiency.

### Stoploss Rules

```
Default stoploss: Disabled (-99%)
Actual stoploss: Check after 50 minutes, dynamically decide whether to stoploss
Trailing stop: Activate after profit > 1%, stoploss line moves up 2.5%
```

**Translation**: Don't actively stoploss in first 50 minutes, give market time to rebound. After 50 minutes decide based on situation.

---

## 3. 12 Entry Conditions: Classic "Combination Punch"

BigZ03 has 12 entry conditions, divided into 5 major categories:

### 🎯 Category 1: RSI Oversold Type (Condition 0)

**Core Logic**: Buy when RSI below 30

**In Plain English**:
> "Price above 200-day moving average, but RSI fell below 30? This is healthy pullback, buy!"

```python
Condition 0:
- Close > EMA200 (trend up)
- RSI < 30 (short-term oversold)
- 3 candles ago was big bullish (means recently falling)
- 1-hour RSI < 71 (big cycle not overheated)
```

---

### 📉 Category 2: Lower Bollinger Band Type (Conditions 1, 2, 12)

**Core Logic**: Buy when price touches lower Bollinger Band

**In Plain English**:
> "Fell to lower Bollinger Band? Buy! Broke below more? Even more certain!"

**Representative Conditions**:
- **Condition 1**: Price < Lower Band × 0.989 + Bearish close + Volume contraction
  > "Touched band and still bearish, high probability of rebound tomorrow"
- **Condition 2**: Price < Lower Band × 0.982
  > "Deeply broke below band, buy more aggressively"
- **Condition 12**: False breakout pattern
  > "Broke below band then recovered? Fake! Buy during rebound"

---

### 🔄 Category 3: MACD Momentum Type (Conditions 5, 6, 7)

**Core Logic**: MACD golden cross + low price = entry

**In Plain English**:
> "MACD golden cross means momentum turned positive, price still at bottom, double confirmation!"

**Representative Conditions**:
- **Condition 5**: MACD fast line > slow line + difference big enough + price at lower band
- **Conditions 6-7**: Different RSI threshold combinations

---

### 🌊 Category 4: Multi-Cycle Resonance Type (Conditions 3, 4, 8, 9)

**Core Logic**: 5-minute + 1-hour dual-cycle confirmation

**In Plain English**:
> "Big cycle up, small cycle oversold, this is real opportunity!"

**Representative Conditions**:
- **Condition 3**: Above 1-hour EMA200 + 5-minute touches lower band + RSI < 14.2
- **Condition 4**: 1-hour RSI < 16.5 + 5-minute touches lower band
  > "1-hour RSI as low as 16.5, this is extremely oversold, rebound probability extremely high!"

---

### 🎪 Category 5: Special Pattern Type (Conditions 10, 11)

**In Plain English**: These two conditions disabled by default, author thinks not mature enough

---

## 4. Protection: 50-Minute Observation Period

### Core Stoploss Logic

```python
if holding time < 50 minutes:
    Don't actively stoploss, give market breathing time

if holding time >= 50 minutes:
    if 1-hour RSI < 35:
        # Market extremely oversold, continue waiting
        Don't stoploss
    elif price above EMA200 and fell more than 2.5%:
        # Trend may reverse
        Stoploss 1%
    elif fell more than 1.5%:
        # Judgment mistake
        Stoploss 1%
```

**Plain English Explanation**:

| Situation | Handling | Reason |
|-----------|----------|--------|
| Holding < 50 min | Don't stoploss | Give enough time for market to reverse |
| RSI extremely low | Continue waiting | Don't stoploss at lowest point |
| Still falling | Admit defeat stoploss | Admit judgment was wrong |

### Trailing Stop

```
Activate after profit > 1%
Stoploss line follows price increase, keep 2.5% pullback room
```

---

## 5. Exit Logic: No Active Exit Signals

BigZ03's design philosophy: **No exit signals, either ROI take-profit or stoploss close.**

**In Plain English**:
> "12 conditions for entry, exit just depends on ROI and stoploss. Simple crude, but effective."

---

## 6. This Strategy's "Personality"

### ✅ Pros (Praise Session)

1. **Low Drawdown**: First target only 2.8%, not easily trapped
2. **High Capital Efficiency**: Quick take-profit, capital can frequently turnover
3. **Multi-Condition Coverage**: 12 conditions cover various oversold patterns
4. **Smart Stoploss**: 50-minute observation period + RSI exception, avoid stoplossing at lowest point
5. **Concise Code**: Compared to subsequent versions, logic clear easy to understand

### ⚠️ Cons (Roast Session)

1. **Frequent Trading**: 2.8% target means frequent buying selling, fees accumulate
2. **Sell Too Early**: When big moves come, may only eat 2.8%
3. **Fixed Parameters**: No adaptation, needs manual adjustment
4. **Not Suitable for Strong Trends**: Normal pullbacks in trends may be misjudged as "oversold"

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Wide Range Oscillation | ✅ Best | Frequent oversold-rebound cycle |
| Range Upward | ✅ Suitable | Pullback is entry opportunity |
| Strong Trend | ⚠️ Caution | Normal pullbacks may be misjudged |
| Continuous Decline | ❌ Don't Use | Each oversold may continue falling |

---

## 8. Bottom Line: How Is This Strategy?

### One-Sentence Review
> "Stability prevails over everything,not seeking quick riches but seek steady earnings classic strategy"

### Who Should Use It?
- ✅ Risk-averse traders
- ✅ Pursuing stable returns
- ✅ Can accept frequent trading
- ✅ Have time to monitor

### Who Should NOT Use It?
- ❌ Pursuing high returns
- ❌ Don't want frequent operations
- ❌ Hope for "set and forget"
- ❌ Long-term investors

### My Recommendations
1. **First understand logic**: This is strategy's foundation, must understand before using
2. **Suitable for range markets**: Need enough oscillation to trigger signals
3. **Set good position management**: Don't exceed 25% of total capital per trade
4. **Have psychological expectations**: 2.8% isn't much, but accumulates

---

## 9. What Markets Make Money?

### 9.1 Core Logic: Using Classic Indicators to "Buy Dips"

BigZ03's profit philosophy: **Don't greed for big moves, seek stable small profits.**

12 entry conditions, each is a net. Some nets specialize in catching "RSI oversold", some specialize in "lower Bollinger Band", some specialize in "MACD golden cross".

**No one can predict what opportunities market will give. But with many nets, one will always catch something.**

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Wide Range Oscillation | ⭐⭐⭐⭐⭐ | Best environment, frequently triggers oversold-rebound |
| 🔄 Range Upward | ⭐⭐⭐⭐☆ | Pullback is entry opportunity |
| 📉 Continuous Decline | ⭐⭐☆☆☆ | Each oversold may continue falling |
| ⚡️ Strong Trend | ⭐⭐☆☆☆ | Normal pullbacks may be misjudged |

**One-Sentence Summary**: Range market is home field, other markets need caution.

---

## 10. Want to Run This Strategy? Check These First

### 10.1 Pair Configuration

| Configuration Item | Recommended Value | Roast |
|-------------------|------------------|-------|
| Maximum Positions | 3-4 | Diversify risk |
| Pair Type | Major coins | Good liquidity |
| Single Trade Capital | 20-25% of total | Don't go all-in |

### 10.2 Condition Switches

```python
buy_params = {
    # Conditions 0-9: Same as original
    "buy_condition_10_enable": False,  # Disabled by default
    "buy_condition_11_enable": False,  # Disabled by default
    "buy_condition_12_enable": True,   # False breakout enabled
}
```

### 10.3 Hardware Requirements

This strategy computation not large, ordinary VPS can run:

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|---------------|-------------------|
| 1-3 pairs | 2GB | 4GB |
| 4-5 pairs | 4GB | 8GB |

### 10.4 Backtest vs Live Trading

**Backtest Performance**: Usually looks good, because historical data "perfect"

**Live Reality**:
- 2.8% take-profit may be easily reached in backtests
- Fees and slippage in live trading may affect execution
- Need patience for frequent trading

**Recommended Process**:
1. Backtest at least 6 months of data first
2. Then simulated trading for 2-4 weeks
3. Small capital live test
4. Increase position only after confirming effectiveness

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Looking carefully at code, you'll find some interesting things:

1. **2.8% First Target Very Conservative**
   > "Make a bit and run, don't be greedy" — author's risk preference

2. **50-Minute Observation Period**
   > "Don't stoploss too early, may stoploss exactly at lowest point" — author deeply understands leek psychology

3. **12 Conditions Cover Various Patterns**
   > "More nets, more likely to catch fish" — author's probability thinking

---

## 12. Last But Not Least

### One-Sentence Review
> "Stability prevails over everything, classic strategy for conservative traders"

### Who Should Use It?
- ✅ Risk-averse traders
- ✅ Pursuing stable returns
- ✅ Can accept frequent trading
- ✅ Have time to monitor

### Who Should NOT Use It?
- ❌ Pursuing high returns
- ❌ Don't want frequent operations
- ❌ Hope for "set and forget"
- ❌ Long-term investors

### Manual Trader Recommendations
If you trade manually, can borrow BigZ03's thinking:
- Focus on oversold opportunities in uptrend
- Use 1-hour RSI to confirm big trend
- Set an "observation period", don't stoploss too fast
- Take profits quickly, don't be greedy

---

## 13. ⚠️ Final Risk Reminder (Must Read This Section)

### Backtests Look Beautiful, Live Trading Requires Caution

BigZ03's historical backtest performance may look good, but there are traps:

- **2.8% Target Too Small**: May be eaten up by fees and slippage
- **Frequent Trading**: Fees accumulate into mountain
- **May Sell Too Early**: Big moves come, only eat 2.8%

Simply put:
> "Making 2.8% ten times may not cover one 10% loss!"

### Hidden Risks of Frequent Trading

This strategy looks stable, but live trading may lead to:
- **High Fee Cost**: Frequent trading fees accumulate
- **Slippage Impact**: Each trade has slippage, accumulates
- **Mentality Exhaustion**: Frequent operations easily tired

### My Recommendations (Real Talk)

```
1. Calculate fees first: Make sure 2.8% covers fees
2. Run simulated trading first: Observe 2-4 weeks before live
3. Small capital! Small capital! Small capital! Can't stress enough
4. Mental preparation: May have consecutive small losses
5. If fees too high, consider increasing take-profit target
```

**Remember**:
> "In crypto, staying alive is more important than making money! Light position test, don't go all-in!"

---

**Final Reminder**: Strategy may be classic, but market always changing. Tread carefully 🙏

*This article is for entertainment and learning only, not investment advice. Investment involves risks, enter the market with caution.*
