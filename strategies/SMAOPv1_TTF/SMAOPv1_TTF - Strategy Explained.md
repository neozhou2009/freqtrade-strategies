# SMAOPv1_TTF Strategy: The "Thermometer" MA Dip-Buying King

> **Nickname**: TTF Trend Hunter  
> **Job**: MA Offset Hunter + TTF Thermometer Combo  
> **Timeframe**: 5 minutes (main) + 1 hour (helper)

---

## I. What is This Strategy?

Simply put, **SMAOPv1_TTF** is a strategy that:
- Uses moving averages as "discount lines" - buy when price drops to a certain percentage below MA
- Uses EWO to judge "which way the wind is blowing" - avoid trading against the trend
- Uses TTF as a "thermometer" - run when it gets too hot

Like buying vegetables at the supermarket 🥬: You see vegetables that normally cost $10 now at a 2% discount (MA offset), confirm it's a normal discount not expired goods (EWO), buy! Then when the thermometer shows "too hot" (TTF), sell quickly!

---

## II. Core Configuration: Simply Put, "Three Safety Fuses"

### Take Profit Rules (ROI Table)

```
Immediately    10% profit
30 minutes     5% profit  
60 minutes     2% profit
```

**Translation**: Target 10% right after buying, get more anxious as time passes, settle for 2% after 60 minutes.

### Stop Loss Rules

```
Fixed stop loss: -10%
Trailing stop: Activates after profit > 1%, locks in 99.9% profit
```

**Translation**: Accept 10% loss. But after making 1%, switch to "life-saving mode" - follow price up, exit if it drops just 0.1%.

---

## III. 2 Buy Conditions: I've Categorized Them For You

Not many buy conditions in this strategy, just 2, but cleverly designed:

### 🎯 Type 1: Trend Pullback Buy (Condition #1)

**Core Logic**: Pullback opportunity in an uptrend

**Plain English**:
> "The wind is still blowing east (EWO high), price pulled back a bit (MA offset), and it's not too hot (RSI not high) - perfect time to hop on!"

**Representative Condition**: Condition #1

**Detailed Script**:
- Price is 2.2% below MA (offset 0.978)
- EWO > 5.638 (strong trend)
- RSI < 61 (not overheated)
- Has volume

---

### 📉 Type 2: Oversold Bounce Buy (Condition #2)

**Core Logic**: When it drops too much, it'll bounce eventually

**Plain English**:
> "It's crashed! EWO is nearly -20, this price is dirt cheap - let's pick some up and see!"

**Representative Condition**: Condition #2

**Detailed Script**:
- Price is 2.2% below MA (offset 0.978)
- EWO < -19.993 (extremely oversold)
- Has volume

---

## IV. Protection Mechanism: 3 Layers of "Anti-Pit Net"

Each buy condition has triple protection, like three airbags:

| Protection Type | Function | Plain English |
|-----------------|----------|---------------|
| EWO Filter | Judges trend direction | "Don't run against the wind!" |
| RSI Filter | Judges overbought/oversold | "Don't chase highs!" |
| Trailing Stop | Locks in profits | "Run when you profit, don't be greedy!" |

---

## V. Sell Logic: More Sophisticated Than Buying

### 5.1 ROI Take Profit: More Anxious Over Time

```
Just bought   → Target 10%
30 minutes    → Target drops to 5%
60 minutes    → Target drops to 2%
```

**Plain English**:
- Just bought: I want 10%!
- 30 minutes: Fine, 5% is okay...
- 60 minutes: Please, I'll take 2% too!

### 5.2 Trailing Stop: Follows Price Up

```
Profit reaches 1% → Activate trailing stop
Stop line follows up → Exit if it drops just 0.1%
```

**Plain English**: Once profitable, don't let it escape - stop line climbs with the price!

---

### 5.3 Two Sell Signals

**Classic Script**:

1. **Signal #1: MA Breakout Sell**
   > "Price is 0.6% above the MA (offset 1.006), too expensive - sell!"

2. **Signal #2: TTF Overheat Sell**
   > "TTF crossed above 100, buying power is too intense - time to pull back, take profits!"

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Dual Entry Opportunities**: Can chase trend pullbacks AND buy oversold bounces - never miss an opportunity
2. **Solid Protection**: EWO + RSI + trailing stop - three layers of defense
3. **Flexible Exit**: TTF indicator provides independent exit signal, not stuck on ROI
4. **Adjustable Parameters**: 11 optimizable parameters, fits various market conditions

### ⚠️ Cons (Complaint Section)

1. **Too Many Parameters**: 11 parameters, headache to tune, easy to overfit 🤣
2. **TTF is Uncommon**: Not many people use this indicator, limited community verification
3. **Loses in Ranging Markets**: In sideways markets, offset strategy gets slapped repeatedly
4. **1h Informative Layer Barely Used**: Defined but not really applied in code, kind of wasteful

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|--------------------|---------------|--------|
| Uptrend | ✅ Go for it | MA offset catches pullbacks, TTF exits timely |
| Ranging Market | ⚠️ Light position | Easy to get slapped back and forth, reduce size |
| Downtrend | ❌ Don't use | Bottom-catching can get you buried |
| High Volatility Coins | ✅ Works | Trailing stop protects profits |

---

## VIII. Summary: How Good Is This Strategy?

### One-Line Verdict
> "Buy at MA discount, sell when TTF overheats, check wind direction with EWO - solid trend-following strategy"

### Who Should Use It?
- ✅ Veterans familiar with MA strategies
- ✅ Cautious types who like multi-indicator confirmation
- ✅ Quant enthusiasts willing to spend time tuning parameters
- ✅ Traders dealing with trending coins

### Who Shouldn't Use It?
- ❌ Newbies (too many parameters, easy to get confused)
- ❌ Lazy people who just want to copy-paste (needs coin-specific tuning)
- ❌ Traders mainly in ranging markets
- ❌ People who don't like trailing stops

### My Suggestions
1. **Backtest First**: Verify parameter effectiveness with historical data
2. **Small Position Live Trading**: Run 1-2 coins first, observe performance
3. **Tuning Advice**: Set base_nb_candles_buy to 20-30 for more stability
4. **Watch TTF**: This indicator is the selling point - understand it to better time exits

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Three-Piece Combo

SMAOPv1_TTF is a "MA offset + trend filter + thermometer exit" combination strategy.

**Its Money-Making Philosophy**: "Buy good stuff at discount, sell when temperature rises"

- **MA Offset**: Wait for price to drop below MA by a certain percentage before buying - like getting a "discount"
- **EWO Filter**: Make sure the wind direction is right, don't go against the trend
- **TTF Thermometer**: Take profits timely when buying power gets too intense, don't be greedy

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | Pullback buy + TTF exit, perfect coordination |
| 🔄 Ranging Market | ⭐⭐☆☆☆ | MA lines cross frequently, high chance of getting slapped |
| 📉 Downtrend | ⭐⭐☆☆☆ | Bottom-catching can get buried, use with caution |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | Trailing stop helps, but might get shaken out |

**One-Line Summary**: Best in uptrends, be careful in ranging markets!

---

## X. Want to Run This Strategy? Check These First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Commentary |
|--------------------|-------------------|------------|
| Number of pairs | 5-20 | Too many to keep track of |
| Coin selection | Trending coins mainly | Don't pick ranging coins |
| Timeframe | 5m | Default is fine |

### 10.2 Key Config File Settings

```yaml
# Buy parameters (defaults)
base_nb_candles_buy: 16      # MA period
low_offset: 0.978            # Offset ratio (2.2% discount)
ewo_high: 5.638             # EWO high threshold
ewo_low: -19.993            # EWO low threshold
rsi_buy: 61                 # RSI upper limit

# Sell parameters
base_nb_candles_sell: 49
high_offset: 1.006          # Offset ratio (0.6% premium)
ttf_upperTrigger: 100       # TTF trigger line
```

### 10.3 Hardware Requirements (Important!)

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|---------------|---------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Decent |

**Warning**: This strategy has moderate computation, older computers can run it, just don't open too many pairs 😅

### 10.4 Backtest vs Live Trading

Backtest and live trading may differ, main reasons:
- Slippage: In extreme markets, buy price may differ from expected
- TTF extremes: May trigger earlier or later in live trading than backtest

**Recommended Flow**:
1. Backtest to find optimal parameters
2. Paper trade for 1-2 weeks
3. Small position live test
4. Gradually increase position

**Don't go all-in right away** - no matter how good the strategy, it needs to be broken in!

---

## XI. Bonus: The Strategy Author's "Little Secrets"

Looking closely at the code, you'll find some interesting things:

1. **Very Conservative Trailing Stop**: Only locks in 0.1% profit
   > "A little profit is still profit, don't let the duck in hand fly away"

2. **Two Buy Conditions with Clear Logic**: One chases pullbacks, one catches oversolds
   > "Won't miss either direction, but both have protection"

3. **TTF is Custom Function**: Not a standard indicator, needs self-calculation
   > "My own formula, more peace of mind using it"

---

## XII. Final Words

### One-Line Verdict
> "Buy at MA discount, sell on TTF temperature, check wind with EWO - a steady and progressive strategy"

### Who Should Use It?
- ✅ Trend-following traders
- ✅ Quant players who accept parameter tuning
- ✅ Learners willing to research new indicators
- ✅ Investors with risk awareness

### Who Shouldn't Use It?
- ❌ Conservatives seeking stable returns
- ❌ People who don't like trailing stops
- ❌ Traders mainly in ranging markets
- ❌ Lazy people who don't want to tune parameters

### Manual Trader Suggestions
If you're a manual trader, you can borrow this strategy's concepts:
1. Find a moving average, wait for price to drop 2-3% below it before considering buying
2. Use EWO to judge trend direction, go with the big trend
3. Watch if buying power is overheated - consider selling when it is
4. Set trailing stops to protect profits

---

## XIII. ⚠️ Risk Emphasis Again (Must Read This Section)

### Backtests Are Beautiful, Live Trading Needs Caution

SMAOPv1_TTF's historical backtest may look nice - but note:

> **11 adjustable parameters make it easy to "fit" past market optimal solutions, but this doesn't guarantee future performance.**

Simply put: **Past optimal ≠ Future optimal**

### Hidden Risks of Complex Strategies

In live trading, complex logic may lead to:
- **Parameter Overfitting**: 100% win rate in backtest, under 50% in live trading
- **TTF Misjudgment**: TTF may fail in extreme markets
- **Ranging Losses**: Frequent buy/sell triggers in sideways markets, fees eat profits

### My Advice (Honest Words)

```
1. Run backtest with default parameters first, don't hyperopt right away
2. Paper trade for at least 2 weeks, observe TTF behavior
3. Small position live trading, no more than 5% of total capital per trade
4. Regularly review parameter performance, adjust when needed
```

**Remember**: Strategies are just tools, the market is boss. Light positions for testing, survival comes first! 🙏

---

**Final Reminder**: No matter how good the strategy, the market will humble you without warning. Respect the market, control risk!