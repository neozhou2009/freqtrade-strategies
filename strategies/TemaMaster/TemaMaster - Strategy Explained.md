# TemaMaster Strategy: The Art of Chasing Trends

> **Nickname**: The Trend Hunter  
> **Occupation**: Aggressive Trend Follower / Big Profit Catcher  
> **Timeframe**: 5 minutes

---

## 1. What is This Strategy?

Simply put, **TemaMaster** is:
- A strategy that chases big profits
- Uses three indicators combined to judge buy points
- Lets profits "run", doesn't sell easily

Like a "greedy hunter", squatting next to big profits, won't stop until goal achieved 🦁

---

## 2. Core Configuration: "Greedy Configuration"

### Take-profit Rules (ROI Table)

```
Just opened: Sell at 20.937% profit
After 4 hours: Sell at 6.449% profit
After 32 hours: Sell at 1.703% profit
After 58 hours: Any profit, just sell
```

**Translation**: When just opened "I want 20%!", then a bit later "fine, 6% works", finally "just don't lose money."

This is called the "gradually accepting fate" mode 😂

### Stop-loss Rule

```
Stop-loss: Run at 14.8% loss
```

**Translation**: Stop-loss is quite wide, giving price enough "wiggle room."

### Trailing Stop (The Main Event)

```
Trailing stop activation: Profit reaches 26.7%
Trailing stop distance: Sell when falling 17% from peak
```

**Translation**:
- After making 26.7%, start trailing
- Price rises to +30%, won't sell until dropping to +13%
- This is a "let profits run" configuration

---

## 3. The 1 Buy Condition: Combo Move

### 🎯 The Only Buy Condition: Three-Indicator Combo

**Core Logic**: TEMA crosses above Bollinger lower band + CMO not too bad

**Plain English**:
> "Buy when price drops to Bollinger lower band then starts bouncing, and momentum isn't too bad."

**What are the Three Indicators?**

| Indicator | Fancy Name | What It Does |
|-----------|-----------|--------------|
| TEMA | Triple Exponential Moving Average | Smooths price, faster response than EMA |
| Bollinger Bands | Bollinger Bands | Marks price's "normal range" |
| CMO | Chande Momentum Oscillator | Shows long/short power comparison |

**Buy Signal Breakdown**:

1. **TEMA crosses above BB lower band**
   - Bollinger lower band = price "floor"
   - TEMA coming up from below floor = might rebound
   
2. **CMO > -5**
   - CMO range is -100 to +100
   - Above -5 = momentum not too negative
   - Excludes "free fall" style drops

**Plain English Translation**:
> "Price got beaten to the floor, showing some bounce signs, and not in crazy crash mode, then buy."

---

## 4. Sell Logic: All Automatic

### Sell Signal? None!

This strategy has no active sell signal. Relies entirely on:

1. **ROI auto-sell** (hit target profit)
2. **Trailing stop** (fall back after rising a lot)
3. **Hard stop-loss** (lost too much)

**Plain English**:
> "After buying I don't care. Either make enough, lose enough, or rise then fall back down."

### Tiered Take-Profit (Human Version)

| Time | Target Profit | What It Means |
|------|--------------|----------------|
| Just opened | 20.9% | "I want to double!" |
| After 4 hours | 6.4% | "Fine, some profit works" |
| After 1 day | 1.7% | "Whatever, just take it" |
| After 2.5 days | 0% | "Any profit works, just don't lose" |

**Roast**: This config is too aggressive, 20% target is unrealistic 😅

---

## 5. Trailing Stop: The Soul of This Strategy

### How Does Trailing Stop Work?

Imagine you bought a coin, price starts rising:

```
Buy price: $100
Rises to $126.7 (+26.7%) → Trailing stop activates!
Continues to $150 → Trailing stop moves to $150 × 0.83 = $124.5
Continues to $200 → Trailing stop moves to $200 × 0.83 = $166
Then falls to $166 → Triggers sell! Made 66%!
```

**Plain English**:
> "After making 26.7%, I'll follow the price like a shadow. You rise, I rise. But if you drop more than 17%, I sell."

### Where is This Config Aggressive?

| Parameter | Value | Comment |
|-----------|-------|---------|
| Activation threshold | 26.7% | Too high! Most trades won't reach it |
| Trailing distance | 17% | Also very wide, may give back lots of profit |

**Roast**: 26.7% to start trailing, this isn't "catching big fish", it's "catching whales" 🐋

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **Good trailing take-profit design**: Can make a lot in big trends
2. **Multi-indicator combo**: TEMA + BB + CMO triple verification
3. **Tiered ROI**: Lower requirements over time, avoid stubborn holding
4. **Clean code**: Clear logic, easy to understand

### ⚠️ Cons (Roast Time)

1. **No active sell**: Relies entirely on ROI and stop-loss, may miss best exit points
2. **ROI too aggressive**: 20% target isn't common even in crypto
3. **Trailing stop activates too late**: 26.7% to start, medium gains unprotected
4. **Stop-loss too wide**: -14.8%, single trade may lose a lot

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Strong trend | ✅ Highly recommended | Trailing take-profit is killer |
| Ranging market | ❌ Don't use | Many false breakouts, frequent stop-losses |
| One-way downtrend | ❌ Don't use | Few buy signals |
| High volatility coins | 🤔 Can work | BB breakouts more effective |

---

## 8. Summary: How Good is This Strategy?

### One-sentence Review
> "Money machine in big trends, money loser in ranging markets."

### Who Should Use It?
- ✅ People who believe in trend trading
- ✅ People who can accept wide stop-losses
- ✅ People pursuing big single-trade returns
- ✅ People with patience waiting for big trends

### Who Should NOT Use It?
- ❌ People who don't like trailing stops
- ❌ People pursuing stable small returns
- ❌ People trading in ranging markets
- ❌ People with tight stop-losses

### My Suggestions

1. **Adjust trailing stop threshold**: Lower to 15-20%, protect profits faster
2. **Lower ROI target**: Initial target to 10-15% more realistic
3. **Tighten stop-loss**: -10% or tighter, control single trade risk
4. **Pick right coins**: Choose volatile coins with trends

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Catch Big Trends

TemaMaster's money-making philosophy is simple:

> "Find oversold reversal signals, then sit and wait for big rises, after 26% start trailing protection."

**Markets It Fits**:
- 📈 Strong trends: Trailing take-profit maximizes effect
- 🔄 Ranging: Many false breakouts, may repeatedly stop out

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Strong trend | ⭐⭐⭐⭐⭐ | Trailing take-profit lets you profit from start to finish |
| 🔄 Ranging | ⭐⭐☆☆☆ | BB lower band breakouts all false signals in ranging |
| 📉 Downtrend | ⭐☆☆☆☆ | Very few buy signals in downtrends |
| ⚡ High volatility | ⭐⭐⭐⭐☆ | Need volatility to reach trailing activation threshold |

**One-sentence Summary**: Wait for big trends, don't mess around in ranging markets.

---

## 10. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Comment |
|-------------------|-----------------|---------|
| Number of pairs | 5-15 | Too many to keep track of |
| Timeframe | 5 minutes | Default works |
| Coin selection | Volatile coins | How to rise to 26% without volatility? |

### 10.2 Key Config File Settings

```yaml
# Trailing stop (suggest adjusting)
trailing_stop: True
trailing_stop_positive: 0.15      # Lower a bit
trailing_stop_positive_offset: 0.18  # Lower a bit

# ROI (suggest adjusting)
minimal_roi:
  "0": 0.10      # 10% more realistic
  "120": 0.05    # 5% after 2 hours
  "360": 0.02    # 2% after 6 hours
  "720": 0       # Break-even after 12 hours

# Stop-loss (suggest adjusting)
stoploss: -0.10  # Tighten stop-loss
```

### 10.3 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|--------------------|------------|
| 1-10 pairs | 2GB | 4GB | Okay |
| 10-50 pairs | 4GB | 8GB | Smooth |

---

## 11. Easter Egg: Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **informative_pairs defined but not used**
   > "I prepared reference exchange rate, but... eh, never mind for now."

2. **Sell condition is empty**
   ```python
   # Sell condition: empty
   dataframe.loc[(), 'sell'] = 1
   ```
   > "After buying, just lie flat, let ROI and trailing stop handle it."

3. **Parameters precise to 5 decimal places**
   ```
   trailing_stop_positive = 0.17017
   trailing_stop_positive_offset = 0.26713
   ```
   > "These parameters came from hyperparameter optimization, don't ask why these numbers."

4. **sell_profit_only = True**
   > "Only sell when making money, just hold if losing."

---

## 12. The Very Last Word

### One-sentence Review
> "Big trend catcher, ranging market victim."

### Who Should Use It?
- ✅ Trend trading believers
- ✅ Pursuing big single-trade returns
- ✅ Can accept wide stop-losses
- ✅ Patient waiting for trends

### Who Should NOT Use It?
- ❌ Pursuing stable small returns
- ❌ Don't like trailing stops
- ❌ Ranging market lovers
- ❌ People with tight stop-losses

### Suggestions for Manual Traders

You can borrow this strategy's thinking:
- Use TEMA + BB to find oversold reversal points
- Use CMO to filter extreme downtrends
- Trailing take-profit protects big profits
- But adjust parameters to make it more practical

---

## 13. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting Looks Good, Live Trading Be Careful

TemaMaster's parameters (precise to 5 decimal places) are clearly from hyperparameter optimization:

> **This is a classic "curve fitting" feature—parameters adjusted to perfectly match historical data, but future may differ.**

Simply put: **Memorizing answers mode, the exam might be different.**

### Hidden Risks of Aggressive Parameters

In live trading, aggressive parameters may cause:
- **ROI target hard to achieve**: 20% target unrealistic most of the time
- **Trailing stop won't be used**: Most trades won't reach 26.7% activation threshold
- **Stop-loss too wide**: Single trade may lose 15%
- **No active sell**: Miss best exit points

### My Suggestion (Honest Words)

```
1. Lower trailing stop activation threshold to 15-18%
2. Lower initial ROI target to 10-15%
3. Tighten stop-loss to -10%
4. Pick volatile coins with trends
5. Small position testing, don't go all-in from the start
```

**Remember**: The more "precise" the strategy parameters, the more likely it's overfit. Light position testing, survival first! 🙏

---

*Strategy Number: #408*