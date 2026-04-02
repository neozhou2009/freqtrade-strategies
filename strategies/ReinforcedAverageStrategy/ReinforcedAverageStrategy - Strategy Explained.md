# ReinforcedAverageStrategy: "Steady as an Old Dog" in Trends

> **Nickname**: Moving Average Watchman  
> **Job**: Veteran trend follower  
> **Timeframe**: 4 hours (4h)

---

## I. What is This Strategy?

Simply put, **ReinforcedAverageStrategy** is:
- Watch moving average crossover signals to buy and sell
- Use higher timeframe trend for secondary confirmation
- Trailing stop to protect profits

It's like an **old hunter waiting on a mountain** — won't shoot until the prey enters the best range and the wind direction is right 🎯

---

## II. Core Configuration: "Big Stop-Loss, Let Profits Run"

### Take-Profit Rules (ROI Table)

```
0% → 50% profit target
```

**Translation**: ROI is set at 50%, but this is just a reference, actually relies on trailing stop and sell signal to exit. Meaning "I'm not in a hurry, whatever I can make is fine."

### Stop-Loss Rules

```
Fixed stop-loss: -20%
Trailing stop: 2% activation threshold, 1% pullback triggers
```

**Translation**:
- Fixed stop-loss at 20%, giving the trend enough breathing room
- After rising 2%, trailing stop activates, if price pulls back 1% from the peak, exit immediately

This configuration says: **"I'm not afraid of fluctuations, but you gotta protect the money I've made!"**

---

## III. 1 Buy Condition: Simple and Direct

This strategy's buy condition is super simple, just one condition:

### 🎯 Buy Signal: MA Golden Cross + Trend Confirmation

**Core Logic**: 8-period EMA crosses above 21-period EMA, while price is above higher timeframe MA.

**Plain English**:
> "Short-term MA crosses above medium-term MA going up, major trend is also up, enter!"

**Code Explanation**:
```python
# Condition breakdown
qtpylib.crossed_above(dataframe['maShort'], dataframe['maMedium'])  # EMA(8) crosses above EMA(21)
(dataframe['close'] > dataframe['resample_sma'])  # Price above 48-hour SMA(50)
(dataframe['volume'] > 0)  # Has volume
```

**Translation**:
- 8-hour EMA crosses above 21-hour EMA going up = "Short-term momentum is picking up"
- Price above 48-hour SMA(50) = "Major trend is upward, not a fake breakout"
- Has volume = "Market has interest"

Like **dating**: Short-term impression is good (EMA crossover), family background is also verified (resampled trend confirmation), finally confirming the other person is alive (volume > 0), then decide to meet 💑

---

## IV. Protection Mechanism: Trailing Stop "Fuse"

The strategy configures trailing stop, like installing a "safety rope" for profits:

| Protection Type | Function | Plain English |
|----------------|----------|----------------|
| trailing_stop_positive_offset | 2% activation threshold | "I won't start watching until you're up 2%" |
| trailing_stop_positive | 1% stop distance | "If you drop 1% from the peak, I'm out" |

**Workflow**:
1. After buying, price rises 2% → Trailing stop activates
2. Price continues to 10% → Stop line also rises to 9%
3. Price drops from 10% to 9% → Triggers sell, locks in 9% profit

**Plain English**:
> "After making money, I'm like a clingy person, I follow wherever price goes, but if you dare run back 1%, I'm jumping off immediately!"

---

## V. Sell Logic: Reverse Cross and Run

### 5.1 Basic Sell Signal

**Trigger Condition**: EMA(21) crosses above EMA(8)

**Plain English**:
> "Short-term MA turns down and crosses below medium-term MA, trend reversal, retreat!"

```python
qtpylib.crossed_above(dataframe['maMedium'], dataframe['maShort'])
```

**Translation**: This is the MA death cross, trend turns from bullish to bearish.

### 5.2 Only Sell When Profitable

The strategy has a configuration `sell_profit_only = True`, meaning:

> "When losing, don't listen to sell signals, just hold on and wait for recovery or stop-loss."

This configuration is quite human — don't use MA signals when losing, avoiding emotional panic selling 😅

---

## VI. This Strategy's "Personality Traits"

### ✅ Advantages (Compliment Section)

1. **Simple and clear logic**: MA crossover is the most classic trading signal, no PhD needed to understand
2. **Good trend filtering**: Resampling technology ensures won't trade against the major trend
3. **Trailing stop protection**: Lets profits run without giving back what's earned
4. **Large timeframe stability**: 4-hour level reduces noise, won't frequently enter and exit

### ⚠️ Disadvantages (Roast Section)

1. **Signal lag**: MAs are lagging indicators, by the time they cross, the move is already underway
2. **Tortured in ranging markets**: During sideways movement MAs keep crossing back and forth, repeatedly getting slapped
3. **Fixed parameters**: Only one set of EMA(8,21), won't self-adapt to market conditions
4. **Stop-loss too wide**: 20% stop-loss is too exciting for timid people 💀

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Clear uptrend | ✅ Recommended | MA golden cross captures trends well |
| 📉 Clear downtrend | ✅ Watch or short | Strategy will stay in cash waiting, won't trade against trend |
| 🔄 Sideways oscillation | ⚠️ Use with caution | Will have frequent false breakouts, repeated stop-losses |
| ⚡ High volatility no direction | ❌ Not recommended | MA signals distorted, frequent stop-loss triggers |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Review
> "A classic among classics, simple but effective, suitable for old-school players in trending markets."

### Who Is It For?
- ✅ Quant beginners wanting to learn MA crossover
- ✅ Stable players who like trend following
- ✅ Brave souls who can accept 20% drawdown
- ✅ Patient traders willing to wait for signals

### Who Is It NOT For?
- ❌ Perfectionists pursuing high win rates
- ❌ Speculators only wanting to make money in ranging markets
- ❌ Impatient people who can't stand signal lag
- ❌ Small accounts that can't withstand 20% drawdown

### My Advice
1. **Enable when trend is clear**: See if major direction is up or down, use with the trend
2. **Turn off during oscillation**: Using this strategy in sideways markets is just sending fees to the exchange
3. **Combine with other indicators**: Can add ADX to judge trend strength
4. **Money management**: Don't go all in, this strategy's 20% stop-loss is no joke

---

## IX. In What Markets Can This Strategy Make Money?

### 9.1 Core Logic: Using MAs to Find Trend Start Points

ReinforcedAverageStrategy is a **typical trend-following strategy**. Not much code, but solid logic — use MA crossover to find entry points, use resampling to confirm trend, use trailing stop to protect profits.

**Its money-making philosophy**:
- **Don't predict**: Wait for the trend to show itself
- **Don't be greedy**: Trailing stop automatically exits
- **Don't go against**: Don't buy when major trend is down

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Sustained uptrend | ⭐⭐⭐⭐⭐ | MA golden cross perfectly captures, trailing stop captures most of the profit |
| 📉 Sustained downtrend | ⭐⭐⭐⭐☆ | Won't buy against trend, stays in cash and survives |
| 🔄 Sideways oscillation | ⭐⭐☆☆☆ | MAs keep crossing back and forth, repeatedly stopped out losing fees |
| ⚡ High volatility no direction | ⭐☆☆☆☆ | Signals completely fail, getting slapped back and forth |

**One-sentence summary**: When trends come it's a god, when oscillation comes it's a ghost.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Timeframe | 4h | Default, don't reduce, smaller = more noise |
| Resampling factor | 12 | Keep default, approximately 2-day cycle |
| Number of pairs | 5-20 | Too many to watch, too few not enough diversification |

### 10.2 Hardware Requirements (Important!)

This strategy has very low computational load, minimal hardware requirements:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|---------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | No problem |

**Warning**: Almost no need to worry about hardware, even a Raspberry Pi can run it 😂

### 10.3 Backtest vs. Live Trading

MA strategy backtest and live trading gap is relatively small, but note:
- **Slippage**: Price may have already moved when crossover signal confirms
- **Candle close**: Need to wait for 4-hour candle close to confirm signal

**Recommended Process**:
1. Backtest to see general performance
2. Paper trade for 1-2 weeks
3. Small position live test
4. Confirm no issues before increasing position

**Don't go all in right away**, no matter how good the strategy is, it needs to be broken in!

---

## XI. Bonus: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **ROI set at 50%**: Author has great patience, not in a rush
   > "I'm not in a hurry to sell, profits will run themselves"

2. **Bollinger Bands just for show**: Code calculates Bollinger Bands, but buy/sell logic doesn't use them at all
   > "I just drew them for looks, don't overthink it"

3. **Resampling technology is clever**: Uses 48-hour cycle to confirm trend, avoiding false breakouts
   > "Confirm the big direction before acting, steady!"

---

## XII. Final Words

### One-Sentence Review
> "Classic MA crossover + trend filter combination, suitable for players wanting to steadily make money in trending markets."

### Who Is It For?
- ✅ Quantitative learning beginners
- ✅ Trend following enthusiasts
- ✅ Patient investors who can accept drawdowns
- ✅ Minimalists who like simple strategies

### Who Is It NOT For?
- ❌ People pursuing high win rates
- ❌ People who only trade ranging markets
- ❌ Impatient traders
- ❌ People with too little capital

### Manual Trading Recommendations
This strategy's logic is simple, can be fully executed manually:
1. Open trading software, add EMA(8) and EMA(21)
2. Wait for golden cross confirmation
3. Switch to daily chart to see if major trend is up
4. Set trailing stop
5. Go do whatever you want

---

## XIII. ⚠️ Risk Emphasis (Must Read)

### Backtest Is Beautiful, Live Trading Needs Caution

ReinforcedAverageStrategy's historical backtest often performs **very impressively** in trending markets — but there's a trap:

> **MAs are lagging indicators, by the time they confirm a signal, the move may already be halfway or more complete.**

Simply put: **"By the time the MA tells you a trend has arrived, smart money has already entered."**

### Hidden Risks in Oscillating Markets

MA strategies are a nightmare in oscillating markets:
- **Repeated crossovers**: Cross up and down continuously, all signals are fake
- **Stop-loss accumulation**: Getting swept out 1-2% each time, adds up significantly
- **Confidence collapse**: After 10 consecutive losses you might question your life

### My Advice (Real Talk)

```
1. First determine if the market is trending, if not, don't use it
2. Use ADX or other trend strength indicators to filter signals
3. Just turn off the strategy during oscillation periods, preserve capital
4. Never go all in, enter in batches
```

**Remember**: MA strategies are the friend of trends, and the ATM of oscillation — the kind that sends money to the exchange.

**Final reminder**: No matter how good the strategy is, when the market teaches you a lesson, it won't give a heads up. Test with small positions, staying alive is most important! 🙏