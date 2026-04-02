# MultiMA_TSL: The "Multi Moving Average" Trend-Following Master

> **Nickname**: MA Master  
> **Profession**: Quant world's "collector" — collects EMA, ZEMA, TRIMA three moving averages  
> **Timeframe**: 5 minutes (short-term player)

---

## 1. What's This Strategy?

Simply put, **MultiMA_TSL** is:
- A strategy using **3 different MAs** (EMA, ZEMA, TRIMA)
- A strategy with **custom stoploss**
- A strategy with **protection mechanisms** (Cooldown + LowProfitPairs)

Like a cautious buyer who only buys on sale: "EMA on sale? ZEMA on sale? TRIMA on sale? All satisfied? Then buy!" 🛒

**Roast**: This strategy is really "indecisive", three MAs for you to choose! 🤣

---

## 2. Core Settings: Simply "Offset Trading + Dynamic Stoploss"

### Profit-Taking Rules (ROI Table)

```
Make 10% right after buying? → RUN!
Hold 30 minutes and make 5%? → RUN!
Hold 60 minutes and make 2%? → RUN!
```

**Translation**: This strategy is classic "trend-following thinking", 10% ROI is relatively high, expects to capture big trends!

**Roast**: 10% ROI? This strategy is ambitious, wants to catch big fish! 🎣

### Stoploss Rules

```
Hard stoploss: Cut at 15% loss
Trailing stop: Activates after 1.8% profit, run if pulls back 1%
```

**Translation**: -15% hard stoploss is looser than common strategies, gives trend fluctuation room — classic "let profits run" thinking 💰

---

## 3. Entry Conditions: Three MA Modes to Choose From

This strategy's entry conditions use "offset trading" approach:

### 🎯 Core Logic: Offset Trading

**Offset trading** = Only buy when price is below certain percentage of MA

```python
EMA offset: Price < EMA50 × 0.958 (95.8%)
ZEMA offset: Price < ZEMA30 × 0.963 (96.3%)
TRIMA offset: Price < TRIMA14 × 0.958 (95.8%)
```

**In Plain English**:
> "EMA says 100 bucks? I only buy at 95.8! Only buy on sale!"

### 🎯 EWO + RSI Confirmation

Not enough that price is low, also need EWO wave oscillator confirmation:

```python
(EWO < -20) OR ((EWO > 6) AND (RSI < 50))
```

**In Plain English**:
> "Either deep pullback (EWO < -20), or trend pullback (EWO > 6 but RSI not overbought) — then consider buying"

### 🎯 Three MA Mode Comparison

| Mode | MA Type | Period | Offset | Characteristics |
|------|---------|--------|--------|----------------|
| **EMA mode** | EMA | 50 | 0.958 | Standard, moderate response |
| **ZEMA mode** | ZEMA (zero-lag EMA) | 30 | 0.963 | Fast, almost no lag |
| **TRIMA mode** | TRIMA (triangular MA) | 14 | 0.958 | Smooth, filters noise |

**Roast**: Three MAs for you to choose, this is the legendary "three-choice dilemma"! 🤣

---

## 4. Protection: More Luxurious Than Previous Strategies

This strategy's protection is quite luxurious:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| **CooldownPeriod** | Pause 2 candles after entry | "Just bought, cool down 2 candles before next buy" |
| **LowProfitPairs** | Pause losing pairs | "This pair not making money, pause 20 candles" |
| **Trailing Stop** | Activates after 1.8% profit | "Follow price after making money, run if pulls back 1%" |
| **Custom Stoploss** | Quick exit when sell signal triggers | "Sell signal came? Set stoploss to 0.001, run fast!" |

**Roast**: Custom stoploss is a highlight of this strategy — almost immediate stoploss when sell signal triggers, doesn't let profits slip away! 🚀

---

## 5. Exit Logic: Simpler Than Entry

### 5.1 Technical Exit: Price Above Offset

**Trigger**:
```python
(Price > EMA32 × 1.002) OR (Price > TRIMA48 × 1.085)
```

**In Plain English**:
> "Price is above MA offset already (rose enough) — if you don't run now, what are you waiting for?"

**Roast**: EMA offset 0.2% to sell, TRIMA offset 8.5% to sell? That's a big gap! 🤔

### 5.2 Custom Stoploss: Quick Exit When Sell Signal Triggers

This is a big feature of this strategy:

```python
def custom_stoploss(...):
    if (sell_signal == 1) AND (buy_signal == 0):
        return 0.001  # Almost immediate stoploss
    return 1  # Default: don't trigger
```

**In Plain English**:
> "Sell signal came? No matter how much profit, run fast!"

**Note**: This feature **only effective in live/dry-run mode, not in backtest**!

### 5.3 ROI Exit: 3-Level Take-Profit

```
Profit      Hold Time    Trigger Exit
─────────────────────────────────────
10%         Anytime      Run when reached (big profit)
5%          After 30 min Run when reached (medium profit)
2%          After 60 min Run when reached (small profit)
```

**In Plain English**:
- Make 10% right after buying? → Pie from heaven, run!
- Hold 30 minutes and make 5%? → Not bad, run!
- Hold 60 minutes and make 2%? → Mosquito leg is still meat, run!

---

## 6. This Strategy's "Personality Traits"

### ✅ Advantages (Praise Session)

1. **Multiple MA types**: EMA, ZEMA, TRIMA three options, adapts to different market rhythms
2. **Offset trading**: Captures deep pullbacks, better entry prices
3. **Custom stoploss**: Quick exit when sell signal triggers, locks profits
4. **EWO filter**: Wave oscillator identifies trends and pullbacks
5. **Protection mechanisms**: Cooldown + LowProfitPairs dual protection
6. **Hyperparameter optimization**: Supports Hyperopt for key parameters

### ⚠️ Disadvantages (Roast Session)

1. **High complexity**: Multiple MA + custom stoploss, debugging is painful
2. **No BTC correlation**: Doesn't know when Bitcoin crashes
3. **Parameter sensitivity**: Offset amounts and MA periods need optimization for different pairs
4. **Backtest differences**: Custom stoploss not effective in backtest, may differ from live
5. **Medium computation**: Multiple MA types increase computational burden

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **Ranging market** | Highly recommended | Offset trading best for ranging pullbacks |
| **Uptrend** | Recommended | Custom stoploss can ride green candles |
| **Downtrend** | Pause or light position | No long-term trend filter, easy to lose consecutively |
| **High volatility** | Adjust parameters | May need to adjust offset amounts |
| **Low volatility** | Lower ROI | Lower ROI threshold for small moves |
| **BTC crash** | Pause | Big brother crashed, watch first |

---

## 8. Summary: How's This Strategy?

### One-Sentence Review
> **"A trend-following master using three MAs, with custom stoploss and protection mechanisms"**

### Who Should Use It?
- ✅ People who like multi-indicator combinations
- ✅ People who can accept some complexity
- ✅ People with quantitative foundation
- ✅ Friends with VPS RAM 2GB or more

### Who Should NOT Use It?
- ❌ People who like simple strategies (this strategy has many conditions)
- ❌ People wanting to bottom-fish in downtrends (no long-term trend filter)
- ❌ People who don't want to optimize parameters
- ❌ Pure quantitative newbies (need to understand multiple MAs)

### My Recommendations
1. **Backtest first**: Understand strategy behavior in different markets
2. **Add BTC filter**: Consider adding BTC trend filter for extra protection
3. **Dry-run test**: Test at least 1-2 weeks before live trading
4. **Start small**: Begin with small capital, increase after confirming stability

---

## 9. What Markets Make Money with This Strategy?

### 9.1 Core Logic: Riding Trends with Multiple MAs

MultiMA_TSL is a **trend-following strategy**. Its core philosophy is:

> "One MA might give false signals, but three MAs with offset confirmation should be more reliable, right?"

- **EMA faith**: Classic exponential moving average, widely used
- **ZEMA faith**: Zero-lag version, faster response
- **TRIMA faith**: Triangular smooth, filters noise

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Slow bull/ranging up | ⭐⭐⭐⭐☆ | Offset entry + custom stoploss works well |
| 🔄 Wide ranging | ⭐⭐⭐⭐☆ | Pullback entry suitable for ranging |
| 📉 Single-sided crash | ⭐⭐☆☆☆ | No trend filter, may buy and get stuck consecutively |
| ⚡️ Extreme sideways | ⭐⭐⭐☆☆ | Signals reduce, but offset filters false signals |

**One-sentence summary**: **Makes money in ranging and uptrends, be careful in crash markets**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Pair Configuration

| Configuration | Recommended Value | Roast |
|--------------|------------------|-------|
| Number of pairs | 15-30 | Moderate signal frequency |
| Max positions | 3-5 | Control risk, don't be greedy |
| Position mode | Fixed position | Recommended fixed, control risk |
| Timeframe | 5m | Mandatory, can't change |

### 10.2 Hardware Requirements (Moderate Level)

This strategy uses multiple MAs, moderate computation:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|-----------------|------------|
| 15-30 pairs | 1GB | 2GB | Normal |
| 30-60 pairs | 2GB | 4GB | Comfortable |

**Warning**: Custom stoploss only effective in live mode — backtest results may be optimistic!

### 10.3 Backtest vs Live Differences

**Backtest problems**:
- Custom stoploss not effective
- May miss some exit behaviors
- Results may be overly optimistic

**Recommended process**:
1. Backtest with default parameters first
2. Adjust parameters, see how results change
3. Dry-run test at least 1-2 weeks
4. Small capital live test
5. Confirm stability before adding capital

**Don't go all-in immediately**, backtest isn't everything!

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Three MA types**: EMA, ZEMA, TRIMA all available
   > "Can't decide which MA is best? Use all three!"

2. **Offset mechanism**: Buy below MA, sell above MA
   > "Buy low, sell high — the oldest trick in the book!"

3. **Custom stoploss**: Only works in live mode
   > "Backtest is fantasy, live trading is reality!"

4. **Protection mechanisms**: Cooldown + LowProfitPairs
   > "Don't trade too fast, don't lose too much!"

---

## 12. Last But Not Least

### One-Sentence Review
> **"Three MAs + offset trading + custom stoploss — suitable for trend followers who like multiple confirmations"**

### Who Should Use It?
- ✅ Multi-MA believers
- ✅ People wanting to learn offset trading
- ✅ 5-minute timeframe traders
- ✅ People with some quantitative experience

### Who Should NOT Use It?
- ❌ MA phobia patients
- ❌ People who want simple strategies
- ❌ People unwilling to backtest and verify
- ❌ Pure newbies

### Manual Trader Recommendations

You can reference MultiMA_TSL's approach:
- Observe multiple MA types simultaneously
- Buy when price below MA×offset
- Use trailing stop to protect profits
- Set cooldown between trades

But doing it manually is too tiring, let the robot handle it 🤖

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtest Is Beautiful, Live Trading Needs Caution

MultiMA_TSL's historical backtest performance may look **very good** — but there's a trap:

> **Custom stoploss only works in live mode, so backtest results may be overly optimistic.**

Simply put: **"Backtest is a dream, live trading is reality."**

### Hidden Risks of Complex Strategies

In live trading, multi-MA combinations may cause:
- **Signal conflicts**: Different MAs may give different signals
- **Parameter sensitivity**: Change one parameter, entire strategy behavior changes
- **Computation load**: Multiple MAs increase computation, may miss timing
- **Backtest/live gap**: Custom stoploss differences cause behavior gaps

### No Trend Filter Pit

MultiMA_TSL's biggest problem: **Doesn't care how the broad market moves.**

When Bitcoin crashes, it may still be buying — this is called "counter-trend bottom-fishing", easy to get buried.

**Recommend adding a BTC trend filter yourself**:
- Don't buy when BTC is below key MA
- Or use other broad market indicators to judge

### My Recommendations (Real Talk)

```
1. Backtest with default parameters first, see strategy behavior
2. Add a BTC trend filter yourself, don't go against the trend
3. Dry-run test at least 1-2 weeks, confirm custom stoploss works
4. Small capital live test, don't exceed 10% of total capital
5. Regularly check strategy performance, stop timely if not working
```

**Remember**: No matter how smart the strategy, it can't fight black swans. Light position test, staying alive is most important! 🙏

---

**Final reminder**: Multiple MA confirmations are good, but over-relying on historical parameters is dangerous. The market always changes, no strategy makes money forever!
