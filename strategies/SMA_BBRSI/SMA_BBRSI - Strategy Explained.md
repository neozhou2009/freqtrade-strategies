# SMA_BBRSI Strategy: The "Bottom-Sniping Specialist" with Analysis Paralysis

> **Nickname**: The "Bottom-Fishing Expert" with Analysis Paralysis  
> **Occupation**: Technical Indicator Collage Master  
> **Timeframe**: 5 minutes (main) + 1 hour (auxiliary)

---

## I. What is This Strategy?

Simply put, **SMA_BBRSI** is a strategy that:
- Uses moving averages to find "discounted" buying opportunities
- Uses a bunch of technical indicators to verify if this bottom-fishing is legit
- Uses dynamic stop loss to protect profits, run when needed

It's like when you see a product on sale at the mall, but you're not sure if it's a real discount or a trap. So you: check historical prices (EMA offset), look at review热度 (EWO), compare with similar products (RSI Bollinger Bands), check if it's a clearance sale (anti-pump mechanism)... only then do you decide whether to buy. 🤣

---

## II. Core Configuration: Basically "Quick In, Quick Out + Protect Capital"

### Take Profit Rules (ROI Table)

```
Just bought        →  Sell at 2.8% profit
After 10 candles   →  Sell at 1.8% profit
After 30 candles   →  Sell at 1.0% profit
After 40 candles   →  Sell at 0.5% profit
```

**Translation**: This strategy isn't here to be a shareholder - make some money and run, the motto is "fast, accurate, ruthless."

### Stop Loss Rules

```
Fixed stop loss: -10% (accept losing 10%)
Trailing stop: Activates after 1% profit, allows profits to run
Dynamic stop loss: Tiered smart stop loss
```

**Translation**: Losing money has a bottom line, making money has room.

---

## III. 3 Buy Conditions: I've Categorized Them for You

This strategy's buy conditions are divided into three major categories, each with its own "personality":

### 🎯 Type 1: Trend Pullback (Condition #1)

**Core Logic**: Find pullback opportunities in an uptrend

**Plain English**:
> "Price is rising, but just pulled back below the MA a bit, EWO shows there's still upward momentum, RSI isn't overheated yet... this is a buy!"

**Representative Conditions**:
- Condition #1: `close < EMA × 0.973` → "Price is 3% off!"
- Plus `EWO > 5.672` → "Momentum is okay"
- Plus `RSI < 59` → "Not overheated"

---

### 📉 Type 2: Deep Bottom-Fishing (Condition #2)

**Core Logic**: Buy after a big drop, hoping for a bounce

**Plain English**:
> "EWO dropped below -20, this drop is brutal, probably gonna bounce. Forget it, I'll... wait, just buy a little to test!"

**Representative Conditions**:
- Condition #2: `close < EMA × 0.973` → "Price is 3% off"
- Plus `EWO < -19.931` → "Dropped hard, should bounce right?"

---

### ⚡ Type 3: Oversold Confluence (Condition #3)

**Core Logic**: All indicators say "oversold!"

**Plain English**:
> "RSI broke below Bollinger lower band, short-term RSI under 25, CCI not overheated, long-term trend is up... boys, this is solid!"

**This condition is the most complex, need to satisfy a bunch of requirements**:
- RSI below Bollinger lower band
- EWO in reasonable range
- RSI(4) < 25
- CCI < 100
- moderi_96 trend upward

Translated to human: **"Stars are aligned, buy!"**

---

## IV. Protection Mechanisms: 3-Layer "Anti-Trap Shield"

Each buy condition comes with protection parameters, like wearing three layers of armor in a game:

| Protection Type | Function | Plain English |
|-----------------|----------|---------------|
| **Anti-pump** | Don't buy if pump_strength > 0.25 | "This coin is pumping too hard, don't chase!" |
| **LowProfitPairs** | Pause this pair after 5% loss | "This coin is toxic, let me take a break" |
| **MaxDrawdown** | Circuit breaker at 20% total loss | "Today's not good for trading, close shop!" |

There's also a hidden skill: **Dynamic Stop Loss**

```
Profit < 1%    → Stop loss -17.8% (just started, give some room)
Profit 1~4.8% → Stop loss dynamically adjusts (more profit, tighter stop)
Profit > 4.8% → Stop loss runs with profit (making big money, let it fly)
```

**Complaint**: This stop loss logic is written more complex than my college application... 😅

---

## V. Sell Logic: Even More Fancy Than Buying

### 5.1 Tiered Take Profit: How Much to Run With

```
Price > EMA × 1.01 → Sell! (1% above MA, run)
RSI > Bollinger upper band → Sell! (Overheated, run)
Price falls below ATR_high → Sell! (Dynamic stop loss triggered)
```

**Plain English**:
- Made enough? Run, don't be greedy
- RSI too hot? Run, wait for pullback
- ATR stop loss triggered? Run, protect capital

### 5.2 Anti-Pump Protection

This strategy also has built-in **anti-pump mechanism**: when abnormal price surge is detected (pump_strength > 0.25), buying is **forcefully prohibited**.

**Plain English**:
> "Bro, this coin is being pumped, chasing in means being a bag holder, hold steady!"

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **Reliable Signals**: Buy signals need to pass multiple checks, fewer false signals
2. **Strong Anti-pump Awareness**: Doesn't chase highs, won't be a bag holder
3. **Smart Stop Loss**: Dynamic adjustment, maximize profits
4. **Many Parameters**: Can HyperOpt optimize, good for tinkering

### ⚠️ Cons (Complaint Time)

1. **Too Many Parameters**: 20+ adjustable parameters, easy to "memorize answers" (overfit)
2. **Heavy Computation**: Multiple indicators calculated in real-time, old computers might lag
3. **5-minute Timeframe**: Sensitive to market noise, need to watch closely

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| 📈 Slow Bull Trend | ✅ Recommended | EMA pullback strategy's paradise |
| 🔄 Sideways Oscillation | ✅ Can use | RSI Bollinger Bands perform well |
| 📉 One-way Downtrend | ⚠️ Be careful | Stop loss may trigger frequently |
| ⚡️ Extreme Volatility | ❌ Not recommended | Anti-pump can't save this |

---

## VIII. Summary: How Is This Strategy Really?

### One-Sentence Review
> "Indicators so many they'll make you dizzy, but logic is clear, suitable for patient quantitative traders who like tuning parameters."

### Who Is It For?
- ✅ Traders with some quantitative foundation
- ✅ Those who like pullback buying style
- ✅ Those with time for HyperOpt optimization
- ✅ Those who can accept frequent trading

### Who Is It NOT For?
- ❌ Quantitative newbies (too many parameters will make you dizzy)
- ❌ Those who want passive income (need to tune, need to backtest)
- ❌ Those who hate stop losses (this strategy stops out quite diligently)

### My Advice
1. **Backtest First**: Don't rush to live trade, run through historical data
2. **Paper Trade**: Run with fake money for a few days, see how strategy performs
3. **Small Position**: Live trade with small capital first
4. **Keep Logs**: Record reasons for each trade, easy to review

---

## IX. What Market Can This Strategy Make Money In?

### 9.1 Core Logic: Building a "Defense Net" with Complexity

SMA_BBRSI is a variant of the NostalgiaForX10 series. Code is 300+ lines - what does that mean? Equivalent to writing a college entrance exam essay. 📚

**Its Money-Making Philosophy**: **Better to miss than to make mistakes**

- **EMA Offset**: Only buy at "discounts"
- **EWO Confirmation**: Only buy with momentum
- **RSI Bollinger Bands**: Only buy when oversold
- **Anti-pump Mechanism**: Don't chase pumps
- **Dynamic Stop Loss**: Run when making money, run faster when losing

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:---------------------------|
| 📈 Slow Bull Trend | ⭐⭐⭐⭐⭐ | "Buy on pullbacks, sell on small rises, perfect!" |
| 🔄 Sideways Oscillation | ⭐⭐⭐⭐☆ | "Can make money oscillating up and down, just lots of fees" |
| 📉 One-way Downtrend | ⭐⭐☆☆☆ | "Stop loss triggers frequently, mindset easily breaks" |
| ⚡️ Extreme Volatility | ⭐⭐☆☆☆ | "Anti-pump helps, but extreme volatility is still hard" |

**One-Sentence Summary**: **Makes money in trends, okay in oscillation, run in crashes.**

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Timeframe | 5m | Default, don't change |
| Number of pairs | 5-10 | Too many won't compute in time |
| Stop loss | -0.10 | Adjust based on your risk tolerance |

### 10.2 Key Configuration File Settings

```yaml
# config.json key settings
"timeframe": "5m",
"stake_currency": "USDT",
"dry_run": true,  # Paper trade first!
"stake_amount": "unlimited"
```

### 10.3 Hardware Requirements (Important!)

This strategy has significant computation, has requirements for VPS:

| Trading Pair Count | Minimum Memory | Recommended Memory | Experience |
|-------------------|----------------|-------------------|------------|
| 1-5 pairs | 2GB | 4GB | Smooth |
| 5-20 pairs | 4GB | 8GB | Occasional lag |
| 20+ pairs | 8GB | 16GB | "Bro, is your VPS okay?" |

**Warning**: Don't run this strategy on a free VPS, you'll cry when computation times out 😅

### 10.4 Backtesting vs Live Trading

HyperOpt optimized parameters might look beautiful in backtests, but live trading:

- Slippage will cause execution price deviation
- Market environment changes might make parameters fail
- Overfitting is "memorizing answers", fails when questions change

**Recommended Process**:
1. Historical backtest (at least 1 year data)
2. Out-of-sample test (test with unoptimized data)
3. Paper trade (run at least 2 weeks)
4. Small position live trade (test the waters first)
5. Gradually increase position

**Don't go all-in from the start**, no matter how good the strategy, it needs to磨合!

---

## XI. Bonus: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **RSI Bollinger Bands Dual Parameters**: Buy uses `for_ma_length`, sell uses `for_ma_length_sell`, the author was afraid of mixing up buy/sell signals, so optimized them separately.

2. **moderi_96**: This is a 96-period Volume Weighted EMA trend determination, using volume weighting, more "real" than regular EMA.

3. **pump_strength**: Uses ZEMA to calculate pump strength, this indicator is specifically for preventing chasing highs, can be called the "bag holder detector."

4. **Commented Code**: Code has some commented-out indicators (like ZLEMA, OTF), showing the author tried more indicators but simplified later. This strategy is already the "slimmed down version"!

---

## XII. The Very End

### One-Sentence Review
> "Technical indicator all-you-can-eat buffet, so many parameters you'll doubt life, but logic is rigorous, suitable for quantitative enthusiasts who like to tinker."

### Who Is It For?
- ✅ Traders with quantitative foundation
- ✅ Those who like studying technical indicators
- ✅ Those who can accept frequent trading
- ✅ Those with time for parameter optimization

### Who Is It NOT For?
- ❌ Quantitative newbies (learn basics first)
- ❌ Those who want to lie flat (this strategy needs tuning)
- ❌ Those who hate stop losses (stops out quite diligently)
- ❌ Those without time (HyperOpt runs forever)

### Manual Trader Advice

Don't manually execute this strategy! Signal determination requires real-time calculation of multiple indicators, manual execution is impossible. And dynamic stop loss needs programmatic execution, manual will exhaust you.

---

## XIII. ⚠️ Risk Reminder Again (Must Read)

### Backtests Are Beautiful, Live Trading Needs Caution

SMA_BBRSI's historical backtest performance is often **extremely excellent** - but there's a trap:

> **Because there are many parameters, the strategy easily "fits" the past market's optimal solution, but this doesn't mean it will definitely profit in the future.**

Simply put: **"Memorizing exam answers, fails when questions change."**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Computation Latency**: When candle closes, calculating multiple indicators might delay a few seconds
- **Overfitting**: Good historical performance ≠ good future performance
- **Parameter Sensitivity**: One small parameter change might affect overall performance

### My Advice (Real Talk)

```
1. Backtest with at least 1 year of data
2. Out-of-sample testing is a must
3. Paper trade at least 2 weeks
4. Live trade with minimum position first
5. Weekly review, record problems
```

**Remember**: No matter how good the strategy, when the market teaches you a lesson, it won't give notice. Light position testing, staying alive is most important! 🙏

---

**Final Reminder**: This strategy is 300+ lines of code, 10+ indicators, 20+ parameters... studying it is a journey. But because it's complex, it might be more adaptable - if you can master it!