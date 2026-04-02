# SlowPotato Strategy: The "Potato" Trader That Takes Its Sweet Time

> **Nickname**: Range High-Sell Low-Buy King  
> **Job**: Sideways Market Harvester  
> **Timeframe**: 5 minutes

---

## I. What Is This Strategy?

Simply put, **SlowPotato** is:
- Look at the average high and low prices over the past 5 days
- Buy when it drops to the average low
- Sell when it rises to the average high
- That's it!

The "Slow" in the name suggests this is a slow strategy, and "Potato" might mean it's plain and unpretentious? Anyway, this is just a buy-low-sell-high-in-a-range strategy, like shopping at a farmers market.

---

## II. Core Configuration: Basically "Sell High, Buy Low"

### Take-Profit Rule (ROI Table)

```python
"0":  0.10,   # Run immediately at 10% profit
"30": 0.05,   # After 30 minutes, run at 5% profit
"60": 0.02    # After 60 minutes, run at 2% profit
```

**Translation**:
- Just bought, ambitious, want to make 10%
- Held a while, compromised, 5% is fine too
- Drag on longer, getting zen, 2% and get out quick

**Plain English**: This strategy is a bit "impatient," wants to make money and run right after buying, getting less ambitious the longer it holds.

### Stop-Loss Rule

```python
stoploss = -0.10  # Admit defeat at 10% loss

trailing_stop = True
trailing_stop_positive = 0.02      # Start trailing after 2% profit
trailing_stop_positive_offset = 0.03  # Trail distance 3%
```

**Translation**:
- Maximum 10% loss
- If profit exceeds 2%, start trailing stop
- Stop line follows 3% below highest price

**Plain English**: Admit defeat at 10% loss. But if you're up more than 2%, raise the stop-loss line, follow the price, prevent winning from becoming losing.

---

## III. Buy Condition: Buy When Dropping to 5-Day Average Low

### 🎯 Buy Logic

```python
(dataframe['low'] <= dataframe['low'].rolling(1440).mean()) &  # Drops to 5-day average low
(dataframe['volume'] > 0)                                        # Has volume
```

**Plain English Translation**:

| Condition | Human Language |
|-----------|----------------|
| low <= 5-day average low | "Price dropped to the average of the lowest prices over 5 days, time to buy the dip!" |
| volume > 0 | "People are trading, not a dead market" |

**Classic Line**:
> "What's the average of the lowest prices over 5 days? OK, I'll buy when it drops to that level!"

### Why 1440?

- One 5-minute candle
- One day: 24 hours × 60 minutes ÷ 5 minutes = 288 candles
- 5 days = 288 × 5 = 1440 candles

So rolling(1440) is the past 5 days of data.

---

## IV. Sell Condition: Sell When Rising to 5-Day Average High

### 📈 Sell Logic

```python
(dataframe['high'] >= dataframe['high'].rolling(1440).mean()) &  # Rises to 5-day average high
(dataframe['volume'] > 0)                                         # Has volume
```

**Plain English Translation**:

| Condition | Human Language |
|-----------|----------------|
| high >= 5-day average high | "Price rose to the average of the highest prices over 5 days, time to sell!" |
| volume > 0 | "People are trading, not a dead market" |

**Classic Line**:
> "What's the average of the highest prices over 5 days? OK, I'll sell when it rises to that level!"

### Complete Trading Cycle

1. Wait for price to drop to 5-day average low → Buy
2. Wait for price to rise to 5-day average high → Sell
3. Repeat cycle, like harvesting back and forth in the range

---

## V. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Super simple logic**: Buy low, sell high, elementary schoolers can understand
2. **No fancy indicators**: No MACD, RSI, just looks at price
3. **Has trailing stop**: Locks in profits, prevents giveback
4. **Tiered take-profit**: Gets more zen the longer you hold, avoids greed

### ⚠️ Cons (Roast Section)

1. **Only for ranging markets**: Good in sideways, dumb in trends
2. **Assumes price reverts**: In one-sided uptrend, never get buy signal
3. **Fixed window**: 5-day window doesn't adjust to market
4. **No trend filter**: Doesn't know bull from bear, only knows range

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|--------------------|--------|
| Sideways ranging | ✅ Perfect match | Price oscillates in range, buy low sell high perfect |
| One-sided uptrend | ❌ Don't use | Price keeps rising, buy signal never triggers |
| One-sided downtrend | ❌ Don't use | Price keeps dropping, buy and get trapped |
| High volatility | ⚠️ Use cautiously | Range frequently broken, signals may fail |

**One sentence**: This strategy is a "sideways market harvester," forget about trending markets.

---

## VII. Summary: How Is This Strategy Really?

### One-Sentence Review
> "Sideways ranging market's best friend, trending market's nightmare."

### Who Should Use It?
- ✅ Sideways market lovers: Like selling high, buying low
- ✅ Simple logic seekers: Hate complex indicators
- ✅ Patient investors: Willing to wait for price reversion

### Who Shouldn't Use It?
- ❌ Trend followers: Want to catch big moves, don't use
- ❌ Momentum chasers: Not your style
- ❌ High-frequency traders: Strategy is "Slow" by name

### My Recommendations

1. **Judge the market first**: Confirm it's sideways ranging before using
2. **Set good stop-loss**: 10% is fine, don't set too wide
3. **Pair with trend indicators**: Avoid forcing it in trending markets
4. **Keep trailing stop on**: Locking profits is important

---

## VIII. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: Mean Reversion

SlowPotato's profit philosophy is:
- **Believe in mean reversion**: What goes up must come down, what goes down must come up
- **Range arbitrage**: Eat the spread back and forth in a 5-day range
- **No chasing rallies or killing declines**: Just wait for price at range edges

### 8.2 Performance in Different Markets (Plain Speak Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 One-sided bull | ⭐☆☆☆☆ | Price keeps rising, buy signal never triggers, miss out |
| 🔄 Sideways ranging | ⭐⭐⭐⭐⭐ | Perfect match! Price goes back and forth in range, steady profits |
| 📉 One-sided bear | ⭐☆☆☆☆ | Price keeps dropping, buy signal triggers then get trapped |
| ⚡️ High volatility | ⭐⭐☆☆☆ | Range keeps breaking, signals may fail |

**One-sentence summary**: Only use in sideways ranging markets! Don't bother with trending markets.

---

## IX. Want to Run This Strategy? Check These Configs First

### 9.1 Trading Pair Configuration

| Config Item | Recommended Value | Comment |
|-------------|-------------------|---------|
| Pair type | Ranging coins | Don't pick those that love to moon or crash |
| Timeframe | 5 minutes | Keep default |
| Number of pairs | 10-30 | Too few miss volatility, too many can't monitor |

### 9.2 Hardware Requirements

This strategy has minimal computation, just one average:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|--------------------| -----------|
| 1-10 pairs | 1GB | 2GB | Smooth |
| 10-50 pairs | 2GB | 4GB | Fluid |
| 50+ pairs | 4GB | 8GB | Sufficient |

**Good news**: Old computers can run it too!

### 9.3 Backtest vs Live

**Note a few things**:
- Backtest may overestimate "touching average price" precision
- Live slippage may shrink profits
- When liquidity is poor, execution near average prices may not be good

---

## X. Bonus: The Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **Author contact**: Discord jadex#0557, feedback welcome
   > "Find me if you have issues, help improve welcome!"

2. **Donation addresses**: Has both BTC and ETH
   > "If you find it useful, tips are welcome..."

3. **TODO list**:
   - "Hyperopt currently not profitable" (parameter optimization not tuned yet)
   - "Sort trading pairs by profit difference"
   - "Faster method to calculate 5-day average price"
   
   > "This strategy is still in development, good ideas welcome!"

4. **Author note**:
   > "If still not sold after one day, recalculate 5-day average high"
   
   This shows the author is also thinking about dynamic adjustment.

---

## XI. Final Words

### One-Sentence Review
> "Sideways ranging market's magic weapon, trending market's nightmare. Use in the right market, steady profits guaranteed."

### Who Should Use It?
- ✅ Sideways ranging market traders
- ✅ People who like simple logic
- ✅ People who can judge market conditions
- ✅ Patient investors

### Who Shouldn't Use It?
- ❌ Trend followers
- ❌ Momentum chasers
- ❌ High-frequency traders
- ❌ People who don't judge market environment

### Manual Trader Recommendations

Manual trading can borrow this thinking:
1. Observe 5-day price range
2. Place buy orders at range lower bound
3. Place sell orders at range upper bound
4. Set good stop-loss and take-profit

But remember: **Only use in sideways ranging markets!**

---

## XII. ⚠️ Risk Emphasis (Must Read)

### The Mean Reversion Trap

SlowPotato's core assumption is: **Price will revert to the range.** But there's a big trap:

> **In trending markets, price will never revert, just keep going further.**

Simply put: **Price drops to 5-day average low, you buy, then it keeps dropping... drops through historical records.**

### Risks of Mean Reversion Strategies

In live trading, mean reversion strategies may cause:
- **Trapped in one-sided moves**: Buy then price keeps dropping
- **Range breakout failure**: Historical range broken, strategy fails
- **Frequent stop-losses**: Easy to get washed out when volatile

### My Recommendations (Real Talk)

```
1. First determine if current market is ranging
2. Only enable this strategy in ranging markets
3. Shut it off as soon as trend forms
4. Set stop-loss well, don't hold losers
5. Don't use on highly volatile coins
```

**Remember**: Mean reversion isn't everything. Once market enters a trend, "reversion" is a fantasy. Know your market, choose your strategy, survival is most important! 🙏

---