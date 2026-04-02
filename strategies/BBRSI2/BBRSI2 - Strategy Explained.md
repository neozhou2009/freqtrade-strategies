# BBRSI2 Strategy: The "Bottom-Fishing Specialist" on Bollinger Bands

> **Nickname**: The Bottom-Fishing Specialist  
> **Profession**: Oversold Bounce Expert  
> **Timeframe**: 1 minute (The Quick-Draw Artist)

---

## I. What is This Strategy?

Simply put, **BBRSI2** is a strategy that:
- Waits for price to break below the lower Bollinger Band ("dropped too much")
- Checks if RSI still has some support ("not completely dead yet")
- Decisively buys, waiting for the bounce

It's like **camping out in the supermarket clearance section**—waiting for good stuff to be marked down to rock-bottom prices, but making sure it's not about to expire, before jumping in 🛒

---

## II. Core Configuration: "Buy Hard, Run Fast"

### Take-Profit Rules (ROI Table)

```
0 minutes → Target 30% (Want big profits right at opening)
120 minutes → Target 20% (Waiting too long, lower expectations)
360 minutes → Target 15% (Even longer, even more conservative)
720 minutes → Target 0% (Whatever, just sell it, done fussing)
```

**Translation**: This strategy is like an impatient person—wants 30% right after buying, gets more anxious the longer it waits, and keeps lowering profit targets. After 6 hours, it's basically "whatever happens, happens."

### Stop-Loss Rules

```
Fixed stop-loss: -20%
Trailing stop: Enabled
```

**Translation**:
- Lose 20%? Cut immediately, no discussion
- Making money? Stop-loss line moves up to lock in profits

---

## III. One Buy Condition: That's It

### 🎯 The Only Buy Signal

**Core Logic**: Lower Bollinger Band + RSI Not Too Miserable

```python
(RSI > 35) AND (Close price < Lower Bollinger Band)
```

**In Plain English**:
> "Price broke below the lower Bollinger Band (oversold), but RSI is still above 35 (not completely crashed), opportunity knocks!"

**Example**:
- Bitcoin drops from 50000 to 48000, breaking below the lower Bollinger Band
- But RSI is 38, not that extreme crash-to-20 situation
- Strategy judges: "This is a 'false breakdown', high bounce probability, BUY!"

---

## IV. One Sell Condition: Take the Money and Run

### Sell Signal

```python
(RSI > 75) AND (Close price > Middle Bollinger Band)
```

**In Plain English**:
> "Price has bounced back to the middle Bollinger Band, RSI also shows overbought, good enough, lock in profits!"

**Human Translation**:
- Bounced from lower band to middle band = completed a nice mean reversion
- RSI > 75 = might be near a short-term top
- Sell now, take the profit and go

---

## V. Protection Mechanisms: Two "Fuses"

| Protection Type | Function | Plain English |
|-----------------|----------|---------------|
| Fixed stop-loss | Cut at 20% loss | "Knife at the neck, run!" |
| Trailing stop | Stop-loss line follows profits | "Lock in what you earn, don't let profits become losses" |

Plus exchange-side stop-loss—can run faster than others in extreme markets 🏃‍♂️

---

## VI. This Strategy's "Personality Traits"

### ✅ Strengths (The Compliments)

1. **Simple and Direct**: Just two indicators, one buy condition, don't even need to flip through pages of code
2. **Professional Bottom-Fisher**: Specializes in oversold bounces, thrives in ranging markets
3. **Bounded Risk**: Fixed stop-loss + trailing stop, no unlimited losses

### ⚠️ Weaknesses (The Complaints)

1. **Single Signal Risk**: Just one buy condition, no verification mechanism—"I say bottom-fish, I bottom-fish, who objects?"
2. **High-Frequency Money Burner**: 1-minute timeframe, fees and slippage might eat quite a bit of profit
3. **Cries in Single-Sided Trends**: When there's a sustained crash, RSI stays below 35, signals are pitifully rare

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|--------------------|--------|
| 🔄 Ranging Market | **Highly Recommended** | Up and down oscillation, lots of oversold opportunities |
| 📈 Slow Bull Pullback | Can use | Buy on pullback to lower band, trend continues |
| 📉 Single-Sided Downtrend | **Don't use** | Will catch falling knives halfway, catching until nothing's left |
| ⚡️ High Volatility | Use cautiously | Many false breakouts, may repeatedly hit stop-loss |

---

## VIII. Summary: How Is This Strategy Really?

### One-Sentence Review
> "Simple and crude bottom-fishing hero, pretty sweet in ranging markets, money-giver in single-sided trends."

### Who Should Use It?
- ✅ Quantitative players who like high-frequency trading
- ✅ Traders in ranging markets
- ✅ Beginners wanting to start with simple strategies

### Who Shouldn't Use It?
- ❌ Manual traders (1 minute is impossible to keep up with)
- ❌ People who don't want to trade frequently
- ❌ People who only do single-sided trends

### My Recommendations
1. **Fees Matter**: Find low-fee exchanges, accumulated fees from high frequency are scary
2. **Choose High-Liquidity Pairs**: 1-minute timeframe, slippage has big impact
3. **Test with Small Positions**: Run small capital first, see live performance before scaling up

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: The Art of Oversold Bounces

BBRSI2 is a **high-frequency reversal strategy**. Its profit philosophy is simple:

> **"Be greedy when others are fearful—but not too greedy, if RSI drops to 20 I won't touch it."**

- **Bottom-Fishing Mindset**: Break below lower Bollinger Band = oversold = bounce opportunity
- **Safety Margin**: RSI > 35 = avoid catching falling knives
- **Quick In, Quick Out**: Bounce to middle band then run, don't be greedy

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Slow Bull | ⭐⭐⭐⭐☆ | Bull market pullbacks are opportunities, buy and trend continues, stable profit |
| 🔄 Ranging | ⭐⭐⭐⭐⭐ | Price repeatedly hits lower Bollinger Band, lots of bottom-fishing opportunities, home turf! |
| 📉 Single-Sided Downtrend | ⭐☆☆☆☆ | Keeps dropping, RSI stays < 35, barely gives you any signals |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | Lower band getting pierced is common, but many false breakouts, frequent stop-losses |

**One-Sentence Summary**: Ranging markets are its home turf, single-sided downtrends are its nightmare.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Commentary |
|--------------------|-------------------|------------|
| Timeframe | 1m | High frequency, tiring |
| Trading Pair | High-liquidity major coins | Don't play small caps, slippage will school you |
| Fee Rate | Lower the better | High-frequency trading, fees are hidden costs |

### 10.2 Hardware Requirements

1-minute timeframe, not much computation, but high frequency:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-5 pairs | 2GB | 4GB | Smooth |
| 5-20 pairs | 4GB | 8GB | Comfortable |
| >20 pairs | 8GB | 16GB | Stable |

### 10.3 Backtest vs Live Trading

Backtests are beautiful, live trading has pitfalls:

| Difference | Backtest | Live |
|------------|----------|------|
| Slippage | Usually not considered | Real and potentially significant |
| Execution Speed | Assumed instant | Has network latency |
| Fees | Theoretical value | May actually be higher |

**Recommended Process**:
1. Backtest first, see theoretical performance
2. Small capital live test
3. Compare backtest and live differences
4. Adjust parameters before going big

**Don't go all-in right away**, high-frequency strategy pitfalls are more than you imagine!

---

## XI. Bonus: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll discover some interesting things:

1. **Bollinger Bands only use lower and middle bands**: Didn't even bother calculating the upper band
   > "For bottom-fishing I only care about lower and middle bands, upper band? Not my concern, that's someone else's joy"

2. **RSI threshold chosen at 35**: Not the classic oversold line of 30
   > "RSI dropping to 30 is too scary, 35 is my bottom-fishing bottom line"

3. **Timeframe chosen as 1 minute**: Not 5 minutes, not 15 minutes
   > "I just like it fast, fast entry, fast exit"

---

## XII. Final Words

### One-Sentence Review
> "Simple to the extreme bottom-fishing strategy, reaper in ranging markets, grinder in trending markets."

### Who Should Use It?
- ✅ Quantitative beginners wanting to learn Bollinger + RSI combination
- ✅ Ranging market enthusiasts
- ✅ High-frequency trading maniacs
- ✅ Automated trading executors

### Who Shouldn't Use It?
- ❌ Manual traders (1-minute timeframe, manual will exhaust you)
- ❌ People who only do single-sided trends (this strategy doesn't chase trends)
- ❌ People who don't like frequent stop-losses (quite a few stop-losses in ranging markets)
- ❌ People seeking big volatility windfalls (this strategy eats small swings)

### Manual Trader Advice

Don't manually trade this strategy! 1-minute timeframe, by the time you place your order the market has already moved. This wasn't designed for manual traders.

---

## XIII. ⚠️ Risk Emphasis (This Part Must Be Read)

### Backtests Are Beautiful, Live Trading Requires Caution

BBRSI2's backtest performance might be **decent**—but there's a trap:

> **High-frequency strategies in backtests often ignore slippage and latency, in live trading these costs can eat most of the profits.**

Simply put: **Backtesting is like simulation in an ideal world, live trading is the cruelty of the real battlefield.**

### Hidden Risks of High-Frequency Strategies

In live trading, 1-minute high frequency can lead to:
- **Fee Accumulation**: Dozens to hundreds of trades per day, fees might be higher than you imagine
- **Slippage Loss**: Large volatility within 1 minute, limit orders might execute at worse prices
- **Latency Impact**: Network latency might cause missing optimal entry points

### My Honest Advice

```
1. Run in simulation first, don't rush to live trade
2. Start with small capital in live trading, observe fee and slippage impact
3. Consider raising timeframe to 5 minutes, reduce trading frequency
4. Focus on ranging market performance, skip single-sided trends
```

**Remember**: No matter how good the strategy, when the market schools you, it doesn't give advance notice. Test with small positions, staying alive is most important! 🙏