# Strategy004: The Oversold Reversal Hunter

> **Nickname**: The Oversold Sniper  
> **Job**: Catcher of pullbacks during trend continuations  
> **Timeframe**: 5 minutes

---

## I. What's This Strategy About?

Simply put, **Strategy004** is:
- Looking for "oversold" opportunities
- But not blindly catching bottoms - must confirm there's a trend first
- Using two sets of Stochastic indicators for double verification
- Strong trend + oversold = entry

Like an experienced hunter who doesn't charge at prey on sight, but first confirms the wind direction (trend), then finds the best ambush point (oversold), and finally makes a steady move 🎯

---

## II. Core Configuration: In Plain English - "Quick In, Quick Out"

### Take-Profit Rules (ROI Table)

```
Holding 60+ minutes → Take 1% profit and run
Holding 30-60 minutes → Take 3% profit and run
Holding 20-30 minutes → Take 4% profit and run
Opens and jumps up immediately → Take 5% profit and run
```

**Translation**: This strategy is impatient - the faster you profit, the more eager it is to exit. If it jumps 5% right after opening, it leaves without hesitation. If it takes an hour to gain just 1%, it takes it and retreats.

### Stop Loss Rules

```
Fixed stop loss: -10%
Trailing stop: Activates after 2% profit, triggers on 1% pullback
```

**Translation**: Gives 10% room for error - not running at the first loss. But once you've made 2%, it starts watching closely - if it drops back 1%, it protects the remaining profit and exits.

---

## III. Buy Conditions: One Signal, Seven Gates

This strategy has only one buy signal, but hidden inside are seven gates - **all must be passed**:

### 🎯 Gate 1: Trend Strength Confirmation

```python
(dataframe['adx'] > 50) | (dataframe['slowadx'] > 26)
```

**Plain English**:
> "ADX above 50 (super strong trend), or slow ADX above 26 (at least there's a trend). Either one works. No trend? Not playing."

### 📉 Gate 2: CCI Oversold

```python
dataframe['cci'] < -100
```

**Plain English**:
> "CCI indicator below -100, definitely dropped hard enough."

### 🎲 Gates 3&4: Dual Stochastic Oversold

```python
# Fast Stochastic (5 candles)
fastk-previous < 20 AND fastd-previous < 20

# Slow Stochastic (50 candles)
slowfastk-previous < 30 AND slowfastd-previous < 30
```

**Plain English**:
> "Quick check - 5-candle Stochastic both below 20, that's short-term oversold.
> Slow check - 50-candle Stochastic both below 30, medium-term confirms oversold too.
> Both sides saying 'dropped enough' - then you pass!"

### 🔀 Gate 5: Stochastic Golden Cross

```python
fastk-previous < fastd-previous AND fastk > fastd
```

**Plain English**:
> "Previous candle: K line was below D line; this candle: K line jumped above D line - Golden cross! Reversal has started!"

### 💧 Gate 6: Volume Filter

```python
dataframe['mean-volume'] > 0.75
```

**Plain English**:
> "Average volume must be above 0.75, not touching dried-up coins."

### 💰 Gate 7: Price Filter

```python
dataframe['close'] > 0.00000100
```

**Plain English**:
> "Close price must exceed 0.00000100, not touching super cheap coins - liquidity might be problematic."

---

## IV. Sell Logic: Four Confirmations Before Exiting

### 4.1 Sell Condition Combination

```python
(slowadx < 25) &                    # Trend weakening
((fastk > 70) | (fastd > 70)) &      # Stochastic overbought
(fastk-previous < fastd-previous) &  # Previous candle K above D
(close > ema5)                       # Price still above moving average
```

**Plain English Translation**:

> "How to sell? All four conditions must be met:
> 1. Slow ADX drops below 25 - trend is indeed weakening
> 2. Fast K or D above 70 - Stochastic is overbought
> 3. Previous candle, K was still above D - confirming no death cross yet
> 4. Price still above EMA5 - sell while still above the average to lock profit"

**Comment**: This sell condition is a bit "greedy", wanting to exit near the peak. Problem is the market might not give you that chance 😅

### 4.2 ROI Take-Profit as Backup

If the sell signal doesn't come, ROI take-profit kicks in:
- Up 5% within 20 minutes of opening → Auto take-profit
- Up 3% after 30 minutes → Auto take-profit
- Up only 1% after an hour → Accept it and leave

---

## V. This Strategy's "Personality"

### ✅ Pros (Praise Time)

1. **Doesn't Catch Bottoms Without Trend**: ADX filter ensures entry only in trending markets, reducing "catching falling knife" risk
2. **Dual Stochastic Verification**: Both fast and slow periods confirm oversold, signals are more reliable
3. **Volume Filter**: Avoids low-liquidity coins, preventing slippage
4. **Trailing Stop Protection**: Protects profits once made, doesn't let them fly away

### ⚠️ Cons (Roast Time)

1. **Too Many Conditions, Too Strict**: All seven conditions must be met to enter, might miss many opportunities
2. **Fixed Parameters**: No optimization support, can only watch helplessly when market changes
3. **ADX Lag**: By the time ADX rises, trend might be halfway done
4. **Too "Ideal" Selling**: Wants to sell near the peak, might actually not be able to sell

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| 📈 Uptrend Pullback | ⭐⭐⭐⭐⭐ Strongly recommended | This is the strategy's home turf! |
| 🔄 Wide Range Consolidation | ⭐⭐☆☆☆ Be cautious | Few signals after ADX filtering, might still be false breakouts |
| 📉 Continuous Decline | ⭐⭐☆☆☆ Don't use | Many oversold signals, but high reversal failure rate |
| ⚡ Sharp Drops and Rallies | ⭐⭐⭐☆☆ Depends | Quick reaction but might get shaken out |

---

## VII. Summary: How's This Strategy Really?

### One-Line Review
> "A principled oversold hunter, only catches bottoms during trend continuations, but conditions are too strict and might miss opportunities."

### Who Should Use It?
- ✅ Traders who like pullback reversals
- ✅ Patient traders who can wait for signals
- ✅ Those who accept missing opportunities but don't want frequent trades

### Who Shouldn't Use It?
- ❌ Impatient traders wanting frequent trades
- ❌ Those seeking high win rates (this strategy has few signals)
- ❌ Those only trading altcoins (volume filter might be too loose)

### My Recommendations
1. **Use on major coins**: BTC/ETH etc. with good liquidity
2. **Check overall trend direction**: Look at the big picture trend yourself
3. **Adjust stop loss**: 10% might be too wide, can tighten appropriately
4. **Don't wait for sell signal**: ROI take-profit is important too, don't be too greedy

---

## VIII. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: Pullback Sniping During Trend Continuation

Strategy004 is a **bottom-catching strategy with principles**. Its profit philosophy:

> "I can catch bottoms, but only where there's a trend."

- **ADX Gatekeeper**: Ensures entry only when there's a trend
- **CCI + Dual Stochastic Confirmation**: Confirms truly oversold
- **Golden Cross Trigger**: Confirms reversal has started

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Bull Market Pullback | ⭐⭐⭐⭐⭐ | Perfect! Trend exists, oversold exists, reversal exists - perfect! |
| 🔄 Wide Range Consolidation | ⭐⭐☆☆☆ | Few signals, occasionally present, but might be false breakouts |
| 📉 Bear Market | ⭐⭐☆☆☆ | ADX will filter many, but caught bottoms might keep dropping |
| ⚡ Explosive Volatility | ⭐⭐⭐☆☆ | Quick reaction but easily shaken out |

**One-line Summary**: Use this strategy during bull market pullbacks for best results.

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Number of pairs | 5-20 | Too many signals to watch, too few missed opportunities |
| Coin selection | Major coins | Don't run volume filter on catching small coins |
| Timeframe | 5-minute default | Can try 15 minutes to reduce noise |

### 9.2 Key Config File Settings

```yaml
# config.json key configurations
"max_open_trades": 3,           # Max 3 simultaneous trades
"stake_currency": "USDT",       # Use USDT as base
"stake_amount": "unlimited",    # Each trade uses 1/N of total funds
"dry_run": true,                 # Run simulation first!
```

### 9.3 Hardware Requirements (Important!)

| Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|--------------|----------------|--------------------|------------|
| 1-10 pairs | 2GB | 4GB | Easy |
| 10-30 pairs | 4GB | 8GB | Okay |
| 30+ pairs | 8GB | 16GB | Starting to struggle |

**Warning**: This strategy doesn't have many indicators, but frequent Stochastic calculations might lag older computers 😅

### 9.4 Backtest vs Live Trading

**Backtests Look Great**: On historical data, oversold reversal logic looks perfect

**Live Trading Has Pitfalls**:
- Previous value judgment (`fastk-previous`) might have delays when candles just update
- Limit orders might have difficulty filling in fast markets
- Volume filter uses global average, might behave abnormally during market open/close

**Recommended Process**:
1. Backtest first, check historical performance
2. Run paper trading for at least two weeks
3. Small capital live test
4. Observe actual fill rates
5. Gradually increase capital

**Don't go all-in right away**, no matter how good the strategy, it needs tuning!

---

## X. Bonus: The Strategy Author's "Little Secrets"

Look carefully at the code, you'll find some interesting things:

1. **Dual ADX Judgment**: `adx > 50` or `slowadx > 26`
   > "I want both fast and slow - super strong trends I catch, normal trends I catch too."

2. **Previous Value Judgment**: Using `fastk-previous` not `fastk`
   > "I want to confirm it just crossed, not has been crossed. Reversal is king!"

3. **Price Filter**: `close > 0.00000100`
   > "Not touching cheap coins, might be trash."

4. **Volume Threshold 0.75**: Not a round number
   > "This was tuned through backtesting, might be the number that works best."

---

## XI. Final Words

### One-Line Review
> "A principled oversold hunter, but might be too picky."

### Who Should Use It?
- ✅ Trend traders
- ✅ Pullback bottom-catchers
- ✅ Patient traders
- ✅ Those who accept few signals

### Who Shouldn't Use It?
- ❌ Frequent trading enthusiasts
- ❌ Those chasing high win rates
- ❌ Small-cap only traders
- ❌ Get-rich-quick dreamers

### Manual Trader Recommendations

If you want to manually execute this strategy's logic:
1. Check ADX first - above 26? There's a trend, continue
2. Check Stochastic (5-period) - K and D both below 20? Oversold, continue
3. Check CCI - below -100? Confirms oversold
4. Wait for K line to cross above D line - Golden cross! Enter!
5. Set 10% stop loss, take-profit depends on situation

---

## XII. ⚠️ Risk Emphasis Again (Must Read)

### Backtests Look Great, Live Trading Needs Caution

Strategy004's historical backtest performance might **look good** - but there's a trap:

> **The biggest pitfall of oversold reversal strategies: Oversold can become more oversold.**

Simply put: **You think it's dropped enough, the market tells you "I can drop more."**

### Hidden Risks of Complex Strategies

In live trading, complex logic can lead to:
- **Few Signals**: All seven conditions hard to satisfy together, might go a day without signals
- **Missed Opportunities**: Conditions too strict, watching opportunities slip away
- **ADX Lag**: By the time ADX confirms trend, might have already rallied a bit
- **Limit Order Risk**: Might not fill during sharp drops and rallies

### My Recommendations (From the Heart)

```
1. Run paper trading for two weeks first, see actual signal frequency
2. If too few signals, consider relaxing conditions (modify code yourself)
3. Don't use on continuously dropping coins, catching bottoms mid-slope
4. Execute stop loss strictly, 10% is 10%
5. Use with other strategies together, don't rely solely on this one
```

**Remember**: No matter how good the strategy, when the market teaches you a lesson, it doesn't give advance notice. Light position testing, survival is most important! 🙏