# PrawnstarOBV Strategy: The Volume Detective

> **Nickname**: The Volume-Price Detective  
> **Job**: Sniffing out capital inflows at market bottoms  
> **Timeframe**: 1 Hour

---

## I. What is This Strategy?

Simply put, **PrawnstarOBV** is:

- A "snoop" that keeps staring at trading volume
- A "bottom-fishing master" that only acts when the market is weak
- A "capital tracker" using OBV (On-Balance Volume) to find money flowing in

It's like a scalper lurking at the market entrance, knowing exactly who's buying big and who's secretly selling 🕵️

---

## II. Core Configuration: Basically "Steady Bottom-Fishing"

### Take-Profit Rules (ROI Table)

```
Right after buying: Goal is 29.6% profit (pretty ambitious)
After 3 hours: Down to 13.7% is fine
After 13.5 hours: 2.5% is okay too
After 17 hours: Break-even and leave, game over
```

**Translation**: This strategy is like "new official, three fires" - super ambitious right after buying, then gets zen over time, eventually accepting break-even. Just like chasing someone - at first you're like "I won't marry anyone else," three months later you think "being friends is fine too" 🤣

### Stop-Loss Rules

```
Hard stop-loss: Run at 15% loss
Trailing stop: After making 4%, run if it pulls back 0.1%
```

**Translation**: After making 4%, it gets super chicken - runs at the tiniest pullback from the peak. This is called "wallet-clutching mode" - not giving back a penny of profit.

---

## III. 3 Buy Conditions: I've Sorted Them For You

This strategy's buy conditions fall into three categories, neatly organized:

### 🎯 Category 1: Golden Cross Bottom-Fishing (Condition #1)

**Core Logic**: OBV crosses above MA + RSI weak confirmation

**Plain English**:
> "Volume momentum suddenly strengthened, and the market is still in a weak zone - this could be a bottom reversal signal!"

**Code snippet**:
```python
OBV crosses above OBV MA
AND RSI < 50
```

**Interpretation**:
- OBV (On-Balance Volume) is a cumulative volume indicator
- When OBV crosses above its 7-day MA, it means money is starting to flow in
- RSI < 50 ensures we're bottom-fishing in a weak zone
- It's like saying: "Money is coming in, but the market is still cheap - opportunity!"

---

### 📉 Category 2: Deviation Bottom-Fishing (Condition #2)

**Core Logic**: Volume-price deviation exceeds 10%

**Plain English**:
> "The volume MA is way off from price - something fishy is going on, time to buy the dip!"

**Code snippet**:
```python
(OBV MA - Close Price) / OBV MA > 0.1
```

**Interpretation**:
- This condition judges the divergence between volume momentum and price
- When deviation exceeds 10%, something unusual is happening with volume-price relationship
- Could be a bottom signal - like goods on sale, but suddenly more people are buying

---

### 🔍 Category 3: Trend Confirmation (Condition #3)

**Core Logic**: OBV rising + OBV MA trend up + RSI weak

**Plain English**:
> "Volume is up, volume MA is trending up, but RSI is still weak - solid bottom signal!"

**Code snippet**:
```python
OBV > Previous OBV
AND OBV MA > OBV MA from 5 candles ago
AND RSI < 50
```

**Interpretation**:
- OBV higher than previous: momentum increasing
- OBV MA higher than 5 candles ago: trend pointing up
- RSI < 50: still in weak zone
- Triple confirmation, more reliable

---

## IV. Protection Mechanism: 3 Layers of "Security Doors"

This strategy has no active sell, relying entirely on protection mechanisms:

| Protection Layer | Function | Plain English |
|-----------------|----------|---------------|
| Fixed Stop Loss | Run at 15% loss | "Lost too much, I'm out!" |
| ROI Take-Profit | Lower targets over time | "Waiting too long is boring, break-even is fine" |
| Trailing Stop | After 4% profit, run on 0.1% pullback | "Not losing a penny of profit!" |

The design is like: wanting to make big money when entering, then getting zen over time, then clutching the wallet tight when profitable 🤐

---

## V. Sell Logic: There Isn't Any!

### Yep, You Read That Right

This strategy's sell function is **empty**:

```python
def populate_exit_trend(self, dataframe, metadata):
    dataframe.loc[( ), 'sell'] = 1
    return dataframe
```

**Plain English**:
> "Sell? I don't know how! Let me rely on ROI and trailing stop to escape!"

This design is like a driver who doesn't know how to brake - relying entirely on walls (stop loss) and destinations (ROI) to stop 🚗

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Time)

1. **Volume-Price Combo**: Not just looking at price, also watching volume - more information
2. **Triple Confirmation**: Three different angles confirming the bottom, more reliable signals
3. **Solid Protection**: Trailing stop + ROI take-profit + fixed stop loss - triple insurance
4. **Focused on Bottom-Fishing**: RSI < 50 restriction ensures only entering in weak zones

### ⚠️ Cons (Complaint Time)

1. **No Active Sell**: No sell signals, relies entirely on stops and take-profits, might miss better exits
2. **Oscillating Market Weapon, Trending Market Useless**: RSI < 50 restriction is completely useless in trending up markets
3. **May Catch Falling Knives**: Buying in weak zones, there might be more downside below
4. **1-Hour Timeframe is Slow**: Slow reaction to fast markets

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Oscillating Market | ✅ Use heavily | Core scenario, catching bottom reversals |
| Bottom Consolidation | ✅ Recommended | OBV momentum changes most effective |
| Trending Up | ❌ Don't use | RSI < 50 restriction, missed opportunities |
| Trending Down | ⚠️ Careful | May catch falling knives |

---

## VIII. Summary: How's This Strategy?

### One-Sentence Review
> "A good guy who only knows how to bottom-fish but doesn't know how to sell - enters on triple confirmation, exits on luck and stops."

### Who's It For?
- ✅ People good at bottom-fishing in oscillating markets
- ✅ People who believe "volume precedes price" theory
- ✅ Long-term thinkers willing to trade time for space
- ✅ People who don't chase frequent trades

### Who's It NOT For?
- ❌ People who want to follow trends (RSI<50 restriction is too limiting)
- ❌ People who want high-frequency trading (1-hour timeframe is too slow)
- ❌ People who don't like trailing stops
- ❌ People who want to make money in bull markets (this is for bottom-fishing)

### My Recommendations
1. **Use mainly in oscillating markets**: This strategy is designed for bottom-fishing, don't use in trending markets
2. **Combine with other indicators**: Consider adding a trend filter
3. **Adjust stop loss**: 15% stop loss might be too wide, adjust based on coin volatility

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Finding Bottoms with Volume

PrawnstarOBV is a **bottom-fishing strategy**. Its core philosophy is:

> "Price can lie, volume doesn't."

**Its Money-Making Philosophy**:
- **Volume Before Price**: When OBV rises, money is flowing in, price might not have reacted yet
- **Enter When Weak**: RSI < 50 ensures not chasing highs
- **Multiple Confirmation**: Three conditions verify bottoms from different angles

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English Explanation |
|:-----------|:-------|:--------------------------|
| 📈 Trending Up | ⭐⭐☆☆☆ | RSI stays above 50, can't buy in at all, misses the move |
| 🔄 Oscillating Market | ⭐⭐⭐⭐⭐ | This is the main battlefield! Repeatedly confirming bottoms, eating profits |
| 📉 Trending Down | ⭐⭐☆☆☆ | Might catch falling knives, buying higher than the real bottom |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | Signals might be frequent, but trailing stop protects profits |

**One-Sentence Summary**: Oscillating market bottoms are its home turf, go around during other times.

---

## X. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Recommended | Notes |
|------------|-------------|-------|
| Timeframe | 1 Hour | Default is fine, don't mess with it |
| Number of Pairs | 5-10 | Too many to watch |
| Coin Selection | Major coins | Good liquidity, OBV more reliable |

### 10.2 Key Config File Settings

```yaml
# Stop loss setting
stoploss: -0.15

# Trailing stop (optional optimization)
trailing_stop: true
trailing_stop_positive: 0.001
trailing_stop_positive_offset: 0.04
trailing_only_offset_is_reached: true
```

### 10.3 Hardware Requirements (Important!)

This strategy isn't computationally heavy, doesn't need much VPS:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|---------------|-------------------|------------|
| 1-5 pairs | 2GB | 4GB | Smooth |
| 5-20 pairs | 4GB | 8GB | Comfortable |
| 20+ pairs | 8GB | 16GB | No pressure |

### 10.4 Backtest vs Live

1. Note OBV signals may differ in backtesting vs live
2. 1-hour timeframe parameters might overfit historical data
3. Recommend testing on paper trading first

**Recommended Flow**:
1. Backtest 3 months of data
2. Paper trade for 2 weeks
3. Small position live test
4. Gradually increase position

**Don't go all-in right away**, no matter how good the strategy, it needs breaking in!

---

## XI. Bonus: The Author's "Little Tricks"

Look carefully at the code, you'll find some interesting things:

1. **ROI Design is "Quirky"**
   > 29.6%, 13.7%, 2.5%, 0% - these numbers are clearly backtest-optimized, not integer-friendly for OCD

2. **Super Tight Trailing Stop**
   > After profiting, runs on 0.1% pullback - the author is really afraid of giving back profits

3. **Buy Conditions Written a Bit Messy**
   > Three conditions connected by OR, but bracket placement is headache-inducing - Python precedence issues to watch out for

---

## XII. Final Words

### One-Sentence Review
> "A strategy that only knows how to bottom-fish and doesn't actively sell - enters on triple confirmation, exits entirely on stops and take-profits."

### Who's It For?
- ✅ Oscillating market lovers
- ✅ Bottom-fishing enthusiasts
- ✅ People who believe in volume analysis
- ✅ Patient long-term thinkers

### Who's It NOT For?
- ❌ Trend followers
- ❌ High-frequency traders
- ❌ People who like active take-profits
- ❌ Bull market chasers

### Manual Trader Recommendations

The OBV + RSI combo in this strategy can be used independently:
- Watch when OBV crosses above MA
- Enter when RSI < 50
- Set your own take-profit and stop-loss

The core idea is: **volume precedes price changes** - this concept is valuable for any trader.

---

## XIII. ⚠️ Risk Reminder Again (Must Read)

### Backtesting Looks Great, But Be Careful in Live Trading

PrawnstarOBV's backtesting might look good - but there's a trap:

> **Because RSI and OBV are common indicators, parameters can easily be "fitted" to historical optimum, but that doesn't mean they'll work in the future.**

Simply put: **Good report card in history doesn't mean you'll ace the next exam.**

### Hidden Risks of Complex Strategies

In live trading, this strategy might cause:
- **Missing Bull Markets**: RSI < 50 restriction is useless during bulls
- **Catching Falling Knives**: Buying in weak zones, there might be lower below
- **Getting Trailing Stop Swept**: 0.1% trailing distance is too tight, normal volatility might sweep it

### My Honest Recommendations

```
1. Use in oscillating markets, avoid trending markets
2. Stop loss can be relaxed to -0.10
3. Trailing stop distance can be adjusted to 0.5%-1%
4. Use with trend filters
```

**Remember**: No matter how good the strategy, the market will humble you without warning. Light position testing, staying alive is most important! 🙏

---

**Final Reminder**: Volume indicators are good stuff, but bottom-fishing is an art, not a science. The strategy gives you signals, decisions are still up to you.