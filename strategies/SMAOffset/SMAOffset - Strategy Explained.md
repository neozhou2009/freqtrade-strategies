# SMAOffset Strategy: Buy at Average Discount, Sell at Premium

> **Nickname**: MA Offset King  
> **Job**: Mean Reversion Specialist  
> **Timeframe**: 5 minutes

---

## I. What is This Strategy?

Simply put, **SMAOffset** is a strategy that:
- Waits for price to drop below the moving average by a certain percentage, then buys
- Waits for price to rise above the moving average by a certain percentage, then sells
- Simple enough to be simple!

Like buying vegetables at the market 🥕: Vegetables normally $5/lb, today discounted to $4.8 (below average), buy! Tomorrow price rises to $5.1 (above average), sell!

---

## II. Core Configuration: Simply Put, "One MA Line, Two Trigger Lines"

### Take Profit Rules (ROI Table)

```
100% profit to exit
```

**Translation**: ROI is basically decorative, the strategy exits via sell signals and trailing stop.

### Stop Loss Rules

```
Fixed stop loss: -10%
Trailing stop: Activates immediately, locks in 99.99% profit
```

**Translation**: Accept 10% loss. But make just a tiny profit, and the stop line starts climbing with price, locking in almost all profit. This is extremely conservative design!

---

## III. 1 Buy Condition: Simple Enough to Doubt Life

This strategy has just one buy condition, really just one:

### 🎯 Only Buy: MA Discount Buy

**Core Logic**: Price is 4.2% below MA, buy!

**Plain English**:
> "Normally this thing hovers around the MA, now it's dropped 4.2% below the average - it's cheap! Buy some and wait for it to bounce back!"

**Detailed Script**:
```
Price < MA × 0.958  →  Buy!
Has volume           →  Confirm
```

**Adjustable Parameters**:
| Parameter | Default | Function |
|------------|---------|----------|
| base_nb_candles_buy | 30 | MA period (30 candles) |
| low_offset | 0.958 | Discount ratio (4.2% discount) |
| buy_trigger | SMA | MA type (can choose EMA) |

**Example**:
- MA price $100
- Discount line = 100 × 0.958 = $95.8
- Current price drops to $95.5 → Trigger buy!

---

## IV. 1 Sell Condition: Simple Enough to Doubt Life x2

Sell also has just one condition:

### 🎯 Only Sell: MA Premium Sell

**Core Logic**: Price is 1.2% above MA, sell!

**Plain English**:
> "Normally this thing hovers around the MA, now it's risen 1.2% above the average - it's expensive! Sell and wait for it to drop back!"

**Detailed Script**:
```
Price > MA × 1.012  →  Sell!
Has volume          →  Confirm
In profit state     →  Only then sell
```

**Adjustable Parameters**:
| Parameter | Default | Function |
|------------|---------|----------|
| base_nb_candles_sell | 30 | MA period (30 candles) |
| high_offset | 1.012 | Premium ratio (1.2% markup) |
| sell_trigger | EMA | MA type (default more sensitive than buy) |

**Example**:
- MA price $100
- Premium line = 100 × 1.012 = $101.2
- Current price rises to $101.5 → Trigger sell!

---

## V. Protection Mechanism: Two Life-Savers

This strategy may be simple, but its protection mechanism is solid:

| Protection Type | Function | Plain English |
|-----------------|----------|---------------|
| Fixed Stop Loss | -10% | "Accept the loss if it's too much" |
| Trailing Stop | Locks in 99.99% profit | "Lock profit as soon as you have it, leave nothing behind" |
| Profit-Only Sell | Only sell when profitable | "Don't sell at a loss, wait for bounce" |

**Commentary**: Trailing stop locking in 99.99% profit - this is the ultimate "run at first profit" version! 😅

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Simple Logic**: Just one MA with two offsets, elementary schoolers can understand
2. **Fast Calculation**: Only calculates MA, even old computers can run it
3. **Flexible Parameters**: Buy/sell parameters independent, can tune separately
4. **Solid Protection**: Aggressive trailing stop, won't lose profits easily

### ⚠️ Cons (Complaint Section)

1. **Too Simple**: No trend judgment, may trade against the trend 🤣
2. **Only Works in Ranging Markets**: Trend markets will slap you
3. **Too Aggressive Trailing Stop**: Locks profit right away, might miss out on gains
4. **No Volume or Momentum Filter**: Only price judgment

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|--------------------|---------------|--------|
| Ranging Market | ✅ Go for it! | Price oscillates around MA, perfect match |
| Uptrend | ⚠️ Be careful | May keep waiting for pullback that never comes |
| Downtrend | ❌ Don't use | May catch falling knives halfway down |
| High Volatility Coins | ✅ Works | Use EMA for faster response |

---

## VIII. Summary: How Good Is This Strategy?

### One-Line Verdict
> "The ultimate simple mean reversion strategy: buy at discount, sell at premium, shear sheep in ranging markets"

### Who Should Use It?
- ✅ Newbies starting out (simple logic, easy to understand)
- ✅ Ranging market players (price oscillates back and forth, perfect)
- ✅ People who like simple strategies
- ✅ Those wanting to learn MA offset concepts

### Who Shouldn't Use It?
- ❌ Trend traders (this strategy doesn't chase trends)
- ❌ High-frequency traders (5-minute timeframe too slow)
- ❌ Those seeking complex strategies
- ❌ People who only make money in bull markets

### My Suggestions
1. **Ranging Coins First**: Choose coins with regular price oscillations
2. **Tuning Advice**: low_offset can be set to 0.93-0.96, wait for bigger discounts
3. **Add Trend Filter**: Can add RSI or MACD for filtering
4. **Watch Fees**: Frequent trading in ranging markets, fees can eat profits

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Mean Reversion

SMAOffset is a classic "mean reversion" strategy.

**Its Money-Making Philosophy**: "Price will eventually return to the average, buy cheap, sell expensive"

- **Underlying Assumption**: Price oscillates around MA
- **Buy Timing**: Price below MA by certain percentage
- **Sell Timing**: Price above MA by certain percentage

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Uptrend | ⭐⭐☆☆☆ | Price keeps rising, can't catch the pullback or it's too shallow |
| 🔄 Ranging Market | ⭐⭐⭐⭐⭐ | Price oscillates back and forth, MA strategy plays perfectly |
| 📉 Downtrend | ⭐⭐☆☆☆ | Price keeps falling, catching falling knives halfway |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | Trailing stop helps, but may exit too early |

**One-Line Summary**: Ranging markets are its home turf, trend markets are its nemesis!

---

## X. Want to Run This Strategy? Check These First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Commentary |
|--------------------|-------------------|------------|
| Pair selection | Ranging coins | Don't pick coins that only go up |
| Timeframe | 5m | Default is fine |
| Buy offset | 0.93-0.97 | Depends how big a discount you want to wait for |

### 10.2 Key Config File Settings

```yaml
# Buy parameters (defaults)
base_nb_candles_buy: 30    # MA period
low_offset: 0.958          # Discount ratio (4.2% discount)
buy_trigger: SMA           # Use simple MA

# Sell parameters (defaults)
base_nb_candles_sell: 30   # MA period
high_offset: 1.012         # Premium ratio (1.2% markup)
sell_trigger: EMA          # Use exponential MA, more sensitive
```

### 10.3 Hardware Requirements (Really Low!)

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|---------------|-------------------|------------|
| 1-50 pairs | 1GB | 2GB | Smooth |
| 50-200 pairs | 2GB | 4GB | Decent |

**Commentary**: This strategy has minimal computation, a Raspberry Pi can run it! 😄

### 10.4 Backtest vs Live Trading

This strategy's backtest and live trading differences mainly in:
- **Fees**: Frequent trading in ranging markets, fees are real money
- **Slippage**: Actual execution price may differ from expected
- **Extreme Markets**: MA becomes ineffective during rapid surges or crashes

**Recommended Flow**:
1. Add fee settings in backtest
2. Paper trade at least 1 week
3. Choose ranging coins for live trading
4. Monitor fee ratio

**Don't go all-in right away**, test the waters first!

---

## XI. Bonus: The Strategy Author's "Little Secrets"

Looking closely at the code, you'll find some interesting things:

1. **Buy and Sell MA Can Be Different**:
   > "Buy uses SMA, sell uses EMA - buy more stable, sell more sensitive"

2. **Trailing Stop Locks 99.99%**:
   > "How afraid of losing profit is this? Lock it as soon as you have it!"

3. **ROI Set to 100%**:
   > "Basically giving up on ROI, relying entirely on sell signals"

4. **Independent Parameter Design**:
   > "Buy/sell parameters separate, tune however you want"

---

## XII. Final Words

### One-Line Verdict
> "Buy at MA discount, sell at premium - the ranging market sheep-shearing tool"

### Who Should Use It?
- ✅ Newbies starting out (simple logic)
- ✅ Ranging market players (core users)
- ✅ People who like simple strategies
- ✅ Those wanting to learn MA offsets

### Who Shouldn't Use It?
- ❌ Trend traders
- ❌ Those seeking complex strategies
- ❌ People who only make money in bull markets
- ❌ High-frequency traders

### Manual Trader Suggestions
If you're a manual trader, this strategy's core concept is very practical:
1. Find a moving average (like 30-period)
2. Wait for price to drop 3-5% below the MA before buying
3. Wait for price to rise 1-3% above the MA before selling
4. Works best in ranging markets, be careful in trend markets

---

## XIII. ⚠️ Risk Emphasis Again (Must Read This Section)

### Backtests Are Beautiful, Live Trading Needs Caution

SMAOffset may perform well in backtests for ranging markets - but note:

> **Mean reversion assumes price will revert, but in strong trends this assumption doesn't exist!**

Simply put: **If price keeps going up or down, this strategy is useless**

### Strategy's Fatal Weakness

In live trading, pay special attention to:
- **Trend Risk**: In uptrends can't catch the pullback, in downtrends catching falling knives
- **Fee Risk**: Frequent trading in ranging markets, fees may eat most profits
- **Premature Exit**: Trailing stop too aggressive, may run at first profit

### My Advice (Honest Words)

```
1. Only use this strategy in ranging markets
2. Identify trend: If price stays above or below MA, pause strategy
3. Set minimum profit threshold to avoid overtrading
4. Watch fees, calculate if it's worth it
```

**Remember**: The simpler the strategy, the narrower its application. Shearing sheep in ranging markets works, but don't use it in trend markets!

---

**Final Reminder**: MA strategies look simple, but to make money you need to pick the right market environment. Ranging coins + ranging market = steady returns; trend coins + trend market = accept your fate! 🙏