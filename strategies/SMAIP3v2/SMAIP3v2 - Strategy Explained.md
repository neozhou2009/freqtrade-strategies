# SMAIP3v2 Strategy: The "Dip-Buying Expert's" Smart Buying Guide

> **Nickname**: Dip-Buying Expert, Trend Sniper
> **Occupation**: Specializes in buying pullbacks, runs when it's up
> **Timeframe**: 5 minutes (suitable for day trading)

---

## I. What Is This Strategy?

Simply put, **SMAIP3v2** is a strategy that:
- Only works in uptrends
- Specifically waits for price pullbacks to buy
- Has a "brain" that refuses to sell when making money (thinking it can go higher)

Like a "dip-buying expert," but not blindly - it only acts when the major trend is up, the price pullback is in place, and there's no crash risk 🎯

---

## II. Core Configuration: Basically "Wait for Pullback in Uptrend"

### Take-Profit Rules (ROI Table)

```
Make 2.6% → Run immediately
```

**Translation**: This strategy is a bit "impatient" - makes 2.6% and calls it a day, not greedy. Of course, with trailing stop protection, sometimes it can make more.

### Stop Loss Rules

```
Lose 23% → Admit defeat and exit
Profit reaches 1.8% → Start trailing stop, pull back 0.3% and run
```

**Translation**:
- Stop loss is quite "generous," leaving plenty of room for volatility
- But once making money, immediately enables "life-saving mode," runs with just a small pullback

---

## III. 1 Buy Condition: Not Many Conditions, But Enough

This strategy has just 1 buy signal, but the logic is rigorous:

### 🎯 Core Buy: Trend Up + Price Pullback + No Crash

**Plain English**:
> "Major trend is up (EMA50 > EMA200), price is above long-term moving average, now pulled back below buy line, and no recent crash, then I buy!"

**Code Translation**:
```python
EMA50 > EMA200                    # Medium-term trend up
Price > EMA200                     # Long-term trend also up
pair_is_bad < 1                   # No recent crash
Price < buy threshold(MA × 0.968) # Pullback in place
Has volume                         # Not a dead coin
→ Buy!
```

---

## IV. Protection Mechanism: 2 Layers of "Crash Protection Net"

The strategy has a mechanism called `pair_is_bad` specifically for crash prevention:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| pair_is_bad_1 | 12 candles drop over 13% marked as bad | "Crashed 13% an hour ago, don't catch falling knife!" |
| pair_is_bad_2 | 6 candles drop over 7.5% marked as bad | "Crashed 7.5% half an hour ago, wait a bit!" |

This design is pretty smart - prevents you from catching falling knives before they land 🤣

---

## V. Sell Logic: More Interesting Than Buying

### 5.1 Basic Sell: Run When Above the Line

```
Price > sell threshold(EMA × 0.985) → Sell
```

**Plain English**: Price rebounds above sell line, made enough, time to run.

### 5.2 Smart Exit Rejection: This Strategy Can "Think"

The most interesting part is the `confirm_trade_exit` method:

**Code Logic**:
```python
If selling (ROI/signal/trailing stop):
    If current candle opens higher AND RSI>50 AND RSI still rising:
        Reject exit! Think it can go higher!
```

**Plain English**:
> "Sell signal came? Wait, let me check the market... hmm, opening price is higher, RSI still rising, momentum is strong, I choose not to sell, keep holding!"

This is like a trader with a mind of their own, not mechanically executing, but "thinking" about whether to really leave 😎

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Time)

1. **Rigorous Trend Confirmation**: Dual moving average filtering, won't blindly buy in downtrends
2. **Crash Protection in Place**: Bad pair detection prevents catching falling knives
3. **Complete Profit Protection**: Trailing stop + smart exit rejection, runs when should run, holds when should hold
4. **Optimizable Parameters**: Supports Hyperopt tuning, adaptable to different coins

### ⚠️ Cons (Roast Time)

1. **Stop Loss a Bit Wide**: 23% stop loss, people with weak hearts might not handle it
2. **Uncomfortable in Sideways**: Common problem with trend strategies, gets repeatedly slapped in sideways markets
3. **Single Timeframe**: Only looks at 5 minutes, no larger timeframe confirmation

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Clear Uptrend | 🔥 Use it! | Strategy's best home field, trend continuation after pullback buy |
| Oscillating Uptrend | ✅ Can use | Still can make money, but pullbacks may trigger stop loss |
| Downtrend | ❌ Don't use | Trend filter will block buys, capital sleeps |
| High Volatility Sideways | ⚠️ Use cautiously | Frequent entries/exits, fees can eat up profits |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Evaluation
> "A trend dip-buying strategy with a mind, will think about whether to keep holding when making money, not mechanically executing."

### Who Should Use It?
- ✅ Traders who like trend following
- ✅ People who can accept 23% stop loss space
- ✅ People willing to wait for pullbacks in uptrends
- ✅ Tech enthusiasts interested in parameter optimization

### Who Shouldn't Use It?
- ❌ High-frequency day scalpers
- ❌ Conservatives with strict stop losses (like 5%)
- ❌ Range traders specializing in sideways markets

### My Suggestions
1. **Pick Good Trading Pairs**: Major coins with good liquidity and obvious trends
2. **Backtest Before Live**: Run simulation for at least 1 month
3. **Watch Smart Exit Rejection**: See its rejection frequency, tune parameters
4. **Use More in Good Trends**: Appropriately reduce position in sideways periods

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Wait for Pullback, Buy at a Good Position

SMAIP3v2 is a typical "trend pullback buy" strategy. Not much code, but clear logic.

**Its Money-Making Philosophy**:
- **Only Work in Uptrends**: EMA50 > EMA200, price > EMA200
- **Wait for Pullback to Buy**: Only enter when price pulls back below dynamic buy line
- **Don't Buy Crashes**: Watch and wait for coins that recently crashed

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:-----------:|:-----------------:|---------------------------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | Home field! Buy on pullback then trend continues, making money while lying down |
| 🔄 Oscillating Uptrend | ⭐⭐⭐⭐☆ | Still can make money, but pullbacks may trigger stop loss, a bit painful |
| 📉 Downtrend | ⭐☆☆☆☆ | Almost no buy signals, capital takes a nap |
| ⚡ High Volatility Sideways | ⭐⭐☆☆☆ | Frequent small losses, fees can eat up profits |

**One-Sentence Summary**: It's a god when trends are good, it lies flat when sideways.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Commentary |
|-------------------|------------------|------------|
| Number of Pairs | 5-20 pairs | Too many can't watch, too few not enough diversification |
| Coin Selection | Major coins | Altcoins have high volatility, easily trigger bad pair detection |

### 10.2 Key Configuration File Settings

```yaml
# Recommended configuration
timeframe: 5m
stoploss: -0.23  # Or adjust based on risk preference
minimal_roi: {"0": 0.026}  # Can appropriately raise

# Trailing stop
trailing_stop: true
trailing_stop_positive: 0.003
trailing_stop_positive_offset: 0.018
```

### 10.3 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|---------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Normal |
| 50+ pairs | 8GB | 16GB | May need optimization |

### 10.4 Backtesting vs Live

Smart exit rejection performance in backtesting may differ from live trading, suggestions:

**Recommended Process**:
1. Backtest and optimize parameters first
2. Run simulation for at least 1 month
3. Observe actual trigger rate of smart exit rejection
4. Small capital live test
5. Gradually increase capital

**Don't go all-in right away**, no matter how good the strategy, it needs to be broken in!

---

## XI. Bonus: The Strategy Author's "Little Thoughts"

Looking carefully at the code, you'll find some interesting things:

1. **Smart Exit Rejection**: This feature is really "smart"
   > "I see the market is still okay, let's put the sell signal aside, hold a bit longer~"

2. **Bad Pair Detection**: Uses the gap between past opening price and current closing price
   > "This coin crashed too much recently, let me watch first"

3. **Buy with SMA, Sell with EMA**:
   > "Be more steady when buying (SMA reacts slow), be more sensitive when selling (EMA reacts fast)"

---

## XII. Final Words

### One-Sentence Evaluation
> "A thinking trend dip-buyer, doesn't execute mechanically, will refuse to sell when momentum is strong."

### Who Should Use It?
- ✅ Quantitative players who like trend trading
- ✅ Risk takers who can accept wider stop losses
- ✅ People willing to spend time tuning parameters
- ✅ Traders mainly doing major coins

### Who Shouldn't Use It?
- ❌ Short-termers pursuing high-frequency trading
- ❌ Conservatives with strict stop losses
- ❌ Altcoin kings specializing in small caps
- ❌ Lazy people who don't want to optimize parameters

### Manual Trader Suggestions
If you're trading manually, you can borrow the core ideas from this strategy:
- Use EMA50/EMA200 to judge trend
- Wait for price to pull back below a certain line before entering
- Set a rule "don't buy if recently crashed"
- Enable trailing stop when profitable, but can hold a bit longer when momentum is strong

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Backtesting Looks Beautiful, Live Trading Needs Caution

SMAIP3v2's historical backtesting performance might be **pretty good** - but be aware:

> **Smart exit rejection mechanism performance in live trading may differ from backtesting, especially in markets with insufficient liquidity or violent volatility.**

Simply put: **Backtesting looks at historical data, live trading faces unknown markets.**

### Hidden Risks of Complex Strategies

Be careful in live trading:
- **Slippage Risk**: 5-minute level trading, slippage can eat part of profits
- **Exchange Limitations**: Some exchange APIs may have delays
- **Black Swan Events**: Stop loss may fail during crashes

### My Suggestions (Real Talk)

```
1. Test in simulation for at least 1 month first
2. Watch actual effectiveness of smart exit rejection
3. Pick major coins with good liquidity
4. Reduce position or pause in sideways periods
5. Stop loss can be tightened (like -15%), depends on personal risk tolerance
```

**Remember**: No matter how good the strategy is, when the market teaches you a lesson, it won't give notice. Light position testing, staying alive is most important! 🙏