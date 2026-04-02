# BcmbigzV1: The "Sea King" Player in Bollinger Band World

> **Nickname**: Sea King Strategy  
> **Profession**: Quant World's "Net-Casting Fisherman"  
> **Timeframe**: 5 minutes (entry) + 1 hour (confirmation)

---

## 1. What Is This Thing?

Simply put, **BcmbigzV1** is:
- Wants to buy when seeing "oversold" — aggressive type
- Frantically probes near lower Bollinger Band
- 14 entry conditions take turns on duty, whichever is satisfied enters

Like a veteran squatting at a vegetable market, can't help but buy dips when seeing price fall to bottom of bag 🛒

**One-Sentence Summary**: "Dip-buying enthusiast" whose hands itch when seeing lower Bollinger Band

---

## 2. Core Config: Simply "Fast In Fast Out"

### Profit-Taking Rules (ROI Table)

```
Holding 0-10 min: Make 3.8% and run
Holding 10-40 min: Make 2.8% is also okay
Holding 40-180 min: Make 1.5% makes do
Holding 180+ min: Make 1.8% let's leave
```

**Translation**: This strategy's core philosophy is "fast"! The faster you make money, the better. The longer the time, the more anxious to sell.

### Stoploss Rules

```
Hard stoploss: Disable default stoploss (-99%, basically equals none)
Actual stoploss: Custom stoploss logic
Trailing stop: Activate after profit exceeds 1%, stoploss line moves up 2.5%
```

**Translation**: Strategy doesn't set fixed stoploss, but has a 50-minute "observation period". Still losing after observation period? Then decide whether to stoploss based on situation.

---

## 3. 14 Entry Conditions: Sea King's "Concubine Selection" Standards

This strategy's entry conditions can be called "quant world's sea king", enter if any of 14 conditions is satisfied, I've categorized them for you:

### 🎯 Category 1: RSI Oversold Type (Conditions 0, 3, 4, 8, 9)

**Core Logic**: RSI below certain value means "cheap", buy!

**In Plain English**:
> "RSI fell below 30? Buy when it breaks! Fell below 14? Close eyes and go all-in!"

**Representative Conditions**:
- **Condition 0**: 5-minute RSI < 30 + Price above EMA200 + Still falling recently → "Trend up but short-term plummet, buy the dip!"
- **Condition 4**: 1-hour RSI < 16.5 + Price at lower Bollinger Band → "Big cycle extremely oversold, high rebound probability!"

---

### 📉 Category 2: Lower Bollinger Band Type (Conditions 1, 2, 12)

**Core Logic**: Buy when price approaches lower Bollinger Band

**In Plain English**:
> "Price fell to lower Bollinger Band? Buy! Fell more? Even more certain!"

**Representative Conditions**:
- **Condition 1**: Price < Lower Band × 0.989 + Bearish close → "Touched band and still bearish, high probability of rebound tomorrow"
- **Condition 2**: Price < Lower Band × 0.982 → "Deeply broke below band, buy more aggressively!"

---

### 🔄 Category 3: MACD Momentum Type (Conditions 5, 6, 7, 10)

**Core Logic**: MACD golden cross + low price = entry

**In Plain English**:
> "MACD golden cross? Price still at bottom? This is the legendary 'golden pit'!"

**Representative Conditions**:
- **Condition 5**: MACD fast line > slow line + difference big enough + price at lower band → "Momentum turned positive + low price, double insurance!"
- **Condition 10**: 1-hour RSI < 35 + 1-hour price at lower band + MACD just golden crossed → "Big cycle oversold + momentum reversal, this is bottom signal!"

---

### 💰 Category 4: Capital Flow Type (Condition 11)

**Core Logic**: CMF (capital flow) significantly outflowing + RSI oversold

**In Plain English**:
> "Capital significantly outflowing? RSI still very low? This may be prelude to main force accumulation followed by rally!"

---

### 🎪 Category 5: Special Pattern Type (Condition 12)

**Core Logic**: False breakout pattern

**In Plain English**:
> "Price broke below lower band then recovered? This is false breakout! Buy during rebound!"

---

## 4. Protection: 14-Layer "Safety Net"

Each entry condition has independent protection parameters, like giving each "concubine" an exclusive bodyguard:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| Volume Pump Detection | Prevent buying at pumpdump top | "Volume exploded 2.5x in 48 hours? Don't buy, may be cutting leeks" |
| Volume Contraction Detection | Confirm bottom | "Volume contracted to 1/3.8 of before? Shows selling exhausted" |
| 1-hour RSI Confirmation | Avoid buying at ceiling | "Can only buy if 1-hour RSI below 69, prevent buying at top" |

**Roast**: 14 conditions with so many parameters, optimization will give you plenty to drink 😅

---

## 5. Exit Logic: 50-Minute Life-or-Death Line

### 5.1 Custom Stoploss (Core)

```python
if holding time < 50 minutes:
    Don't actively stoploss, give market time to reverse

if holding time >= 50 minutes:
    if 1-hour RSI < 40:
        Continue holding, wait for rebound
    elif price above EMA200 and fell more than 2.5%:
        Stoploss 1%, admit judgment mistake
    elif fell more than 1.5%:
        Stoploss 1%, admit defeat
```

**In Plain English**:
- **First 50 minutes**: Don't rush, give market time to catch breath
- **After 50 minutes**:
  - RSI still very low? Then wait, don't stoploss at lowest point
  - Still falling? Then stoploss, admit this judgment was wrong

### 5.2 Trailing Stop

```
Activate trailing stop after profit > 1%
Stoploss line follows price increase, keep 2.5% pullback room
```

**In Plain English**: After making money, strategy follows price up, if falls 2.5% automatically sell, protect profits.

---

## 6. This Strategy's "Personality"

### ✅ Pros (Praise Session)

1. **Rich Signals**: 14 conditions, opportunity to enter no matter how market changes
2. **Dual Confirmation**: 5-minute entry + 1-hour confirmation, reduce false signals
3. **Smart Time Stoploss**: Not simple fixed stoploss, judges based on RSI
4. **Volume Filtering**: pumpdump detection reduces probability of being deceived

### ⚠️ Cons (Roast Session)

1. **Too Many Conditions**: 14 conditions × multiple parameters, extremely high optimization difficulty
2. **High Trading Frequency**: Many signals means may trade frequently, fees hurt
3. **Fixed Parameters**: No adaptive capability, different markets may need manual adjustment
4. **Only Suitable for Bull Market**: All conditions require price above EMA200, basically useless in bear market

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Bull Market Pullback | ✅ Key Use | Pullback is entry opportunity |
| Range Upward | ✅ Suitable | Buy when falling to lower band |
| Sideways Range | ⚠️ Caution | May frequently be stopped out |
| One-Sided Decline | ❌ Don't Use | EMA200 condition not satisfied, basically no signals |

---

## 8. Bottom Line: How Is This Strategy?

### One-Sentence Review
> "Many signals, mixed conditions, suitable for quantitative players with patience to tune parameters"

### Who Should Use It?
- ✅ Players with quantitative experience
- ✅ Willing to spend time optimizing parameters
- ✅ Can accept certain trading frequency
- ✅ Prefer short-term trading

### Who Should NOT Use It?
- ❌ Newcomers pursuing simple strategies
- ❌ People who don't want frequent operations
- ❌ "Lazy people" hoping for one-time setup

### My Recommendations
1. **Run with default parameters for 2 weeks first**: Don't rush to optimize, see performance first
2. **Monitor each condition's performance**: Some conditions may be more reliable than others
3. **Set maximum position count**: Suggest maximum 3, avoid over-diversification

---

## 9. What Markets Make Money?

### 9.1 Core Logic: 14 "Fishing Nets"

BcmbigzV1's profit philosophy: **Cast many nets, surely can catch some fish**.

14 entry conditions, each is a net. Some nets specialize in catching "RSI oversold", some specialize in "lower Bollinger Band", some specialize in "MACD golden cross".

**No one can predict what opportunities market will give. But with many nets, one will always catch something.**

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Bull Market Pullback | ⭐⭐⭐⭐⭐ | Best environment, pullback is entry opportunity |
| 🔄 Wide Range Oscillation | ⭐⭐⭐⭐☆ | Frequently triggers lower band conditions, can make money |
| 📉 Continuous Decline | ⭐⭐☆☆☆ | Occasionally catches rebounds, but easily stopped out |
| ⚡️ Surge-Plunge | ⭐☆☆☆☆ | pumpdump protection may fail, high risk |

**One-Sentence Summary**: Most satisfying to use in bull market, can make do in range market, don't think about bear market and extreme situations.

---

## 10. Want to Run This Strategy? Check These First

### 10.1 Pair Configuration

| Configuration Item | Recommended Value | Roast |
|-------------------|------------------|-------|
| Maximum Positions | 3 | Can't manage too many |
| Pair Type | Major coins | Altcoins too volatile |
| Capital Allocation | 20-30% per trade | Don't go all-in right away |

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|---------------|-------------------|------------|
| 1-2 pairs | 2GB | 4GB | Smooth |
| 3-4 pairs | 4GB | 8GB | Relatively stable |
| 5+ pairs | 8GB | 16GB | May lag |

**Warning**: 14 conditions calculating simultaneously, CPU pressure not small, old computers may overheat 😅

### 10.3 Backtest vs Live Trading

**Backtest Performance**: Usually looks very good, because historical data "perfectly fits"

**Live Reality**: May be quite different, because:
- Slippage: Actual execution price 0.1%-0.5% worse than backtest
- Liquidity: Small coins may not be able to buy
- Emotions: Strategy won't panic, but you will

**Recommended Process**:
1. Run simulated trading for 2 weeks first
2. Watch trade records daily, understand strategy behavior
3. Adjust parameters to comfortable range
4. Small capital live test

**Don't go all-in right away**, even good strategies need breaking in!

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Looking carefully at code, you'll find some interesting things:

1. **Condition 2 Particularly Aggressive**: Allows price to fall 1.8% below lower band
   > "The harder it falls, the harder it rebounds" — author's gambling mentality

2. **RSI Threshold Distribution Very Wide**: From 10 to 35 all present
   > "Different degrees of oversold, different entry timing" — author wants to cover all oversold scenarios

3. **50-Minute Stoploss Observation Period**
   > "Don't stoploss too early, may stoploss exactly at lowest point" — author deeply understands leek psychology

---

## 12. Last But Not Least

### One-Sentence Review
> "Many conditions, many signals, intermediate strategy requiring patience to debug"

### Who Should Use It?
- ✅ Traders with some quantitative experience
- ✅ Willing to spend time understanding and optimizing
- ✅ Can accept more trade counts
- ✅ Mainly do short-term trading

### Who Should NOT Use It?
- ❌ Complete newcomers
- ❌ Pursuing simple stability
- ❌ Don't want frequent operations
- ❌ Long-term investors

### Manual Trader Recommendations
If you trade manually, can borrow this strategy's thinking:
- Focus on oversold opportunities near lower Bollinger Band
- Use 1-hour RSI to confirm big trend
- Set an "observation period", don't stoploss too fast
- But manual trading hard to execute 14 conditions, suggest simplifying

---

## 13. ⚠️ Final Risk Reminder (Must Read This Section)

### Backtests Look Beautiful, Live Trading Requires Caution

BcmbigzV1's historical backtest performance often **looks very beautiful** — but there's a trap:

> **14 conditions × multiple parameters, easily "fits" historical market conditions's optimal solution, but this doesn't mean future will definitely profit.**

Simply put: **Got full marks on historical exam, doesn't mean will do well on college entrance exam.**

### Hidden Risks of Complex Strategies

In live trading, 14 entry conditions may lead to:
- **Overtrading**: Too many signals, fees accumulate into mountain
- **Parameter Sensitivity**: Slight threshold adjustment, results worlds apart
- **Hard to Attribute**: Don't know which condition made money when winning, don't know why when losing

### Signal Quality Varied

Not all 14 conditions are good:
- Some conditions may not trigger long-term
- Some conditions have very low win rate after triggering
- You need time to observe which conditions are reliable

### My Recommendations (Real Talk)

```
1. Run at least 2 weeks simulated trading, observe each condition's performance
2. Can consider disabling some conditions, keep most effective 5-7
3. Set reasonable maximum position count, don't exceed 3
4. Check trade records weekly, adjust timely when finding problems
```

**Remember**: No matter how good the strategy, market won't greet you when teaching you a lesson. Light position test, staying alive is most important! 🙏

*This article is for entertainment and learning only, not investment advice. Investment involves risks, enter the market with caution.*
