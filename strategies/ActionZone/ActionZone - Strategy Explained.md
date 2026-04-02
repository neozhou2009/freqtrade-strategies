# ActionZone Strategy: The Trend Catcher

> **Nickname**: Zone Hunter, Dynamic Stop Loss King  
> **Job**: Medium-term Trend Sniper  
> **Timeframe**: Daily (1d)

---

## 1. What is This Strategy?

Simply put, **ActionZone** is:
- A trend following strategy that uses two moving averages to define "zones"
- Fast line above slow line = "bullish zone", only go long
- Automatic stop loss at the lowest price, letting profits run

It's like a **"smart sniper following the main force"** 🎯—not too aggressive, not falling behind, only shooting when the big trend is confirmed, setting stop loss and waiting to count money.

---

## 2. Core Configuration: "Let Profits Run, Cut Losses Fast"

### Take Profit Rules (ROI Table)

```
Holding Time      Target ROI      Translation
─────────────────────────────────────────────
Immediately       10%             Wants 10% at the start
After 60 min      5%              Can't wait? Take 5% and go
After 120 min     2%              Waiting longer? Take 2%
After 180 min     1%              Really can't wait? 1% is fine
```

**Translation**: This strategy is a bit "impatient"—starts with high hopes of making 10%, gets less patient over time, eventually willing to take 1%. But don't worry, trailing stop helps lock in profits.

### Stop Loss Rules

```
Fixed Stop Loss: -10%        (Life-saving bottom line)
Trailing Stop: Activates at 2% profit  (Profit protector)
Dynamic Stop Loss: 14-day lowest price  (This is the key!)
```

**Translation**:
- **Fixed Stop Loss**: Maximum 10% loss, force close if exceeded
- **Trailing Stop**: After making over 2%, system starts "watching the door", sells on profit pullback
- **Dynamic Stop Loss**: This is the special move—uses the lowest price of past 14 days as stop level, as price rises, stop loss rises with it!

---

## 3. Buy Condition: Only One, But Reliable

### 🎯 The Only Buy Condition: Trend + Breakout

**Code Logic**:
```python
Condition 1: fastMA > slowMA     # Fast line above slow line = bullish trend
Condition 2: close > fastMA      # Price breaks above fast line = entry signal
Condition 3: volume > 0          # Has volume = not a fake signal
```

**Plain English**:
> "First check the big picture—fast line above slow line means bullish trend. Then wait for price to break above fast line, like price crossing a threshold, that's when to get on board. Make sure there's volume, don't get fooled by false breakouts."

**Analogy**:
Like waiting for a bus 🚌:
- Fast line above slow line = Bus is heading your way
- Price breaks above fast line = Bus has arrived
- Volume > 0 = There are people on board, not empty

---

## 4. Protection Mechanism: Three Layers of "Fuses"

Every buy condition comes with protection parameters, like three layers of insurance:

| Protection Type | Purpose | Plain English |
|----------------|---------|---------------|
| Fixed Stop Loss | Hard life-saving line | "Maximum 10% loss, have to run no matter what" |
| Trailing Stop | Profit locker | "Made money? Set a follower, sell on pullback" |
| Dynamic Stop Loss | Trend protection shield | "Use 14-day lowest price as bottom line, rising tide lifts all boats" |

**The Best Part is Dynamic Stop Loss** 🌟:
> Example: You bought at 100, lowest price in past 14 days is 90. If it rises to 120, the 14-day lowest might become 105, your stop level moves from 90 to 105! This is called "rising with the tide", letting profits run further.

### Position Management: Risk Budget

```python
max_loss_per_trade = 10  # Maximum $10 loss per trade
```

**Translation**:
> "No matter what I buy, I can lose at most $10 on this trade. If stop is far, buy less. If stop is close, buy more."

**Example**:
- Current price 100, stop price 90 → Stop distance 10 → Buy 1 unit
- Current price 100, stop price 95 → Stop distance 5 → Buy 2 units

This is called **"Risk Budget"**—fixed risk amount per trade, ensuring you won't get knocked out in one blow.

---

## 5. Sell Logic: More Important Than Buying

### 5.1 Three Ways to Sell

**Method 1: ROI Reached**
> Holding time reached target ROI, auto sell.

**Method 2: Trailing Stop Triggered**
> After 2% profit, price pulls back and sells.

**Method 3: Trend Reversal** (This is key)
```python
if fastMA < slowMA:  # Fast line crosses below slow line
    return True      # Trend turning bearish, run!
```

**Plain English**:
> "Trend is broken? Leave, don't linger. Fast line below slow line means bullish trend is over, retreat fast."

### 5.2 Base Sell Signal

**Code Logic**:
```python
Condition 1: fastMA < slowMA     # Fast line below slow line = bearish trend
Condition 2: close < fastMA      # Price breaks below fast line = confirmation signal
Condition 3: volume > 0          # Has volume = valid breakout
```

**Plain English**:
> "Fast line is below slow line, price also broke below fast line, bullish trend is over, retreat!"

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **Simple Logic**: Just two moving averages, easy to understand if you get trends
2. **Solid Risk Control**: Three layers of stop loss protection, hard to lose big
3. **Scientific Position Management**: Fixed risk per trade, won't get wiped out
4. **Good for Medium-term**: Daily timeframe, no need to stare at charts, good for office workers

### ⚠️ Cons (Roast Time)

1. **Slow Response**: Daily timeframe, takes a day to know trend changed
2. **Struggles in Ranging Markets**: Sideways oscillation means repeated stop losses, easy to get "ground down"
3. **Stop May Be Far**: 14-day lowest price might be far away in volatile times
4. **Long Only**: No short logic, can only sit out in bear markets

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Clear Uptrend | ⭐⭐⭐⭐⭐ Full steam ahead | This is its home turf! |
| Oscillating Uptrend | ⭐⭐⭐☆☆ Light position | Will get hit by false signals but overall follows |
| Sideways Consolidation | ⭐☆☆☆☆ Don't use | Frequent stop losses, fees will eat you |
| Downtrend | 🚫 Disable | Long only, going long in downtrend is giving money away |

---

## 8. Summary: How Good Is This Strategy?

### One-Line Review
> "Simple and effective trend following strategy, stop loss mechanism is the highlight, suitable for patient trend traders."

### Who Should Use It?
- ✅ Office workers (daily timeframe, no need to stare at charts)
- ✅ Trend trading enthusiasts
- ✅ People who like simple logic
- ✅ People who prioritize risk control

### Who Shouldn't?
- ❌ Day traders (daily is too slow)
- ❌ Bottom fishers (this is trend following)
- ❌ High-frequency traders in ranging markets
- ❌ Impatient people who can't wait for trends

### My Recommendations
1. **Test with small capital first**: Any strategy needs live verification
2. **Coin selection matters**: Choose coins with clear trends
3. **Combine with other strategies**: Use other strategies for ranging markets
4. **Adjust parameters**: Stop period and position risk can be adjusted to your needs

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Using "Zones" to Judge Trends

ActionZone is like **"someone following the bus"** 🚌:

- Fast line above slow line = Bus heading your way (bullish zone)
- Price breaks above fast line = Bus arrived, get on
- Dynamic stop loss = Get off when bus stops, don't chase too far

**Its Money-Making Philosophy**:
> "Don't predict tops and bottoms, just follow trends. Good trend? Ride the bus. Bad trend? Get off. Simple but effective."

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | Riding the trend express, profits can run far |
| 🔄 Oscillating Uptrend | ⭐⭐⭐☆☆ | Overall profitable, but will get stopped out a few times |
| 📉 Downtrend | ⭐☆☆☆☆ | Strategy is long only, downtrend is giving money away |
| ⚡️ High Volatility Sideways | ⭐☆☆☆☆ | Repeated stop losses, fees might exceed losses |

**One-Line Summary**:
> "Clear uptrends are its home turf, other situations are asking for trouble."

---

## 10. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| max_open_trades | 2-4 | Daily holding periods are long, don't open too many |
| max_loss_per_trade | $5-$20 | Depends on your wallet, don't lose too much per trade |
| min_price_period | 14 | Default, can adjust based on volatility |

### 10.2 Key Configuration Settings

```yaml
# Recommended configuration
max_open_trades: 3
stake_currency: USDT
stake_amount: unlimited  # Let strategy calculate position
```

### 10.3 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|-------------------|------------|
| 1-5 | 2GB | 4GB | Smooth |
| 6-15 | 4GB | 8GB | Comfortable |
| 16+ | 8GB | 16GB | Perfect |

**Note**: Daily strategy has low computation, old computers can run it.

### 10.4 Backtesting vs Live Trading

**Backtesting**: Looks great in historical data, clear trends, clear signals
**Live Trading**: Trend confirmation lags, actual returns might be discounted

**Recommended Process**:
1. Backtest first to see results
2. Small capital live test
3. Observe dynamic stop loss effectiveness
4. Adjust parameters for optimization
5. Go live

**Don't go all in right away**, even the best strategy needs breaking in!

---

## 11. Bonus: The Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Custom Stop Loss Function**: Author didn't lazy out with fixed stop, wrote `custom_stoploss` to track lowest price
   > "This stop rises as you make money, like your salary rising with performance"

2. **Position Management Algorithm**: `custom_stake_amount` calculates position based on stop distance
   > "Fixed loss amount per trade, buy less if stop is far, buy more if stop is close"

3. **Trend Sell Logic**: Besides ROI, there's `custom_sell` checking trend
   > "Trend broken? Run, don't hold on"

---

## 12. Final Words

### One-Line Review
> "Simple but not simplistic, a classic of trend following. Dynamic stop loss and position management are the finishing touches."

### Who Should Use It?
- ✅ People who like simple strategies
- ✅ People who prioritize risk control
- ✅ Medium-to-long term traders
- ✅ Office workers (no need to stare at charts)

### Who Shouldn't?
- ❌ Day trading enthusiasts
- ❌ Short-term traders in ranging markets
- ❌ Bottom fishers
- ❌ Impatient people who can't wait for trends

### Manual Trading Recommendations
If you want to manually execute this strategy:
1. Set up EMA(12) and EMA(26) in TradingView
2. Wait for price close to confirm breakout above fast line
3. Set stop loss at 14-day lowest price
4. Calculate your own position: Risk amount ÷ Stop distance

---

## 13. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting Looks Great, Live Trading Needs Caution

ActionZone's historical backtesting performance is often **quite good**—but there's a trap:

> **Daily timeframe trend strategies often perform well in historical data, but live trends might not be that clear.**

Simply put: **Trends in history look pretty, live trends might be twisty and turny.**

### Hidden Risks of Complex Strategies

In live trading, watch out for these risks:
- **Trend identification lag**: EMA is a lagging indicator, by the time it confirms, trend has already moved
- **Wide stop loss space**: 14-day lowest price might be far in volatile coins
- **Daily slippage**: Although daily slippage impact is small, it still exists
- **Overfitting**: Parameters might be optimized for specific coins

### My Recommendations (Real Talk)

```
1. Backtest first, but don't fully trust results
2. Small capital live test for at least 1 month
3. Choose coins with clear trends (majors over alts)
4. Adjust stop period for market volatility
5. Set reasonable max_loss_per_trade
```

**Remember**: No matter how good the strategy, the market will teach you lessons without warning. Test with light positions, survival comes first! 🙏

---