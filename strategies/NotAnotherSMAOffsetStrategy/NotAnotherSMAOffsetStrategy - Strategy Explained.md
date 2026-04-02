# NotAnotherSMAOffsetStrategy: Strategy Explained

## Chapter 1: What Does This Strategy Do?

Imagine you're shopping at a supermarket. Product prices fluctuate around a "fair price." Sometimes discounts are deep, sometimes markups are high. This strategy helps you buy when prices are "discounted" and sell when they're "marked up."

Specifically, NotAnotherSMAOffsetStrategy:

1. Monitors price deviation from "average price"
2. When price is significantly below average, considers buying
3. When price returns to or exceeds average, considers selling
4. Uses multiple indicators to confirm whether it's truly worth trading

The "NotAnother" means "this is not another ordinary MA strategy" — it's much more refined than simple "price crosses MA up to buy, crosses down to sell" routines.

---

## Chapter 2: Core Indicators in Plain English

### 2.1 Moving Average (MA) — Your Price Ruler

A moving average is like a ruler measuring price's "fair position."

Example: If a stock's recent 14-day prices average around $100.4, that's your reference "fair price."

The strategy uses EMA (Exponential Moving Average), weighting recent prices more heavily, making it more sensitive.

### 2.2 Offset Coefficient — Discount Judgment

**Buy offset (low_offset)**: Default 0.975
- Means: Only consider buying when price falls below 97.5% of average price
- Example: Average $100 → buy only below $97.50
- Philosophy: "Wait for discounts"

**Sell offset (high_offset)**: Default 0.991
- Means: Consider selling when price exceeds 99.1% of average
- Example: Average $100 → sell above $99.10

### 2.3 EWO — Market Thermometer

EWO compares short-term and long-term average price differences. Bigger difference = stronger momentum.

- **EWO positive and large**: Market rising vigorously, optimistic
- **EWO negative and small**: Market falling, pessimistic

The strategy uses three thresholds:
- ewo_high = 2.327: High momentum threshold
- ewo_high_2 = -2.327: Medium momentum threshold
- ewo_low = -20.988: Extreme panic threshold

### 2.4 RSI — Overbought/Oversold Alarm

- **RSI > 70**: Overbought, price rose too much, may drop
- **RSI < 30**: Oversold, price dropped too much, may rebound

The strategy uses three RSIs:
- RSI-14: Standard, sees the big picture
- RSI-4: Fast, catches short-term changes
- RSI-20: Slow, sees long-term trends

---

## Chapter 3: Three Buy Signals Explained

### 3.1 Buy Signal 1: ewo1 — "Strong Trend Pullback"

**When it triggers**: Price was in an uptrend, suddenly pulled back. We buy on the dip.

**Conditions**:
1. Short RSI < 35: Price dropped recently
2. Price >2.5% below average: Discount big enough
3. EWO > 2.327: Market still in upward trend (just a temporary pullback)
4. Standard RSI < 69: Not at extreme overbought
5. Volume > 0: Not a dead market
6. Price also below sell MA: Confirms it's a pullback not a reversal

**Example**: Bitcoin rose from $30,000 to $35,000, suddenly pulled back to $34,000. If conditions are met, strategy buys.

### 3.2 Buy Signal 2: ewo2 — "Deep Oversold Rebound"

**When it triggers**: Price dropped extremely, RSI near bottom. A rebound may come.

**Conditions**:
1. Short RSI < 35
2. Price >4.5% below average: Bigger discount
3. EWO > -2.327: Momentum not extremely pessimistic
4. Standard RSI < 25: Deeply oversold
5. Volume > 0
6. Price also below sell MA

**Example**: A coin got hit by bad news, dropped 20% in a day, RSI below 20. Strategy tries to buy for a rebound.

### 3.3 Buy Signal 3: ewolow — "Extreme Panic Bottom-Fishing"

**When it triggers**: Market is extremely panicked. EWO deeply negative.

**Conditions**:
1. Short RSI < 35
2. Price >2.5% below average
3. EWO < -20.988: Extremely negative, market very panicked
4. Volume > 0
5. Price also below sell MA

**Note**: This signal carries the most risk but highest potential return.

---

## Chapter 4: Exit Signals Explained

Two exit conditions; satisfying either one triggers exit.

### 4.1 Exit Type 1: Normal Profit-Taking

**Conditions**:
1. Price above 9-day MA: Short-term trend up
2. Price > sell MA × 0.3%: Already profitable
3. RSI > 50: Bullish forces dominant
4. Fast RSI > Slow RSI: Momentum still upward

**Plain English**: Price bounced back, momentum good, decent profit earned, time to take it and run.

### 4.2 Exit Type 2: Trend May Reverse

**Conditions**:
1. Price below 50-day HMA: Short-term trend may weaken
2. Price > sell MA: Still profitable
3. Fast RSI > Slow RSI: Short-term momentum okay

**Plain English**: While still profitable, short-term trend may be turning. Better to take the money and run.

### 4.3 Exit Signal Protection Mechanism

Before selling, one final check:

If both conditions are met, refuse to sell:
- HMA-50 significantly above EMA-100 (long-term trend still up)
- Price slightly below EMA-100

**Why**: This means despite the exit signal, long-term trend may still be up. Don't sell; wait for a better price.

---

## Chapter 5: Stop-Loss and Take-Profit Protection

### 5.1 Tiered Take-Profit

| Time | Profit Target |
|------|-------------|
| Immediate | 21.5% |
| After 40 min | 3.2% |
| After 87 min | 1.6% |
| After 201 min | 0% (force sell) |

**Philosophy**: Big expectations when just bought; reduce expectations over time; after 3+ hours, sell regardless.

### 5.2 Fixed Stop-Loss: Max 35% Loss

```python
stoploss = -0.35
```

If price drops 35% from entry, auto-sell. This stop-loss is wide because crypto is volatile; too tight gets stopped out by normal fluctuations.

### 5.3 Trailing Stop — The Smartest Part

**Config**:
- Activates after 3% profit
- Stop follows highest price at 0.5% below
- Price retraces to stop → auto-sell

**Example**:
- Bought at $100
- Rose to $103 (3% profit), trailing stop activates
- Stop price: $103 × (1-0.5%) = $102.45
- Rose to $110, stop follows to $109.45
- Dropped to $109, triggers stop, you made 9%

---

## Chapter 6: Parameter Tuning Advice

### 6.1 Buy Parameters

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| base_nb_candles_buy | 14 | 5-80 | MA period; smaller = more sensitive |
| low_offset | 0.975 | 0.9-0.99 | Discount required; smaller = need bigger discount |
| low_offset_2 | 0.955 | 0.9-0.99 | Second buy discount |
| ewo_high | 2.327 | 2-12 | Momentum threshold |
| ewo_low | -20.988 | -20 to -8 | Extreme momentum threshold |
| rsi_buy | 69 | 30-70 | RSI buy upper limit |

**How to tune**:
- Want fewer but higher-quality signals: Raise ewo_high, lower low_offset
- Want more signals but higher risk: Lower ewo_high, raise low_offset

### 6.2 Different Market Environments

**Bull market**:
- Raise ewo_high (e.g., 5-8), catch strong pullbacks
- Lower low_offset (e.g., 0.95-0.96), wait for bigger discounts

**Bear market**:
- Lower ewo_high (e.g., 2-3), don't require strong momentum
- Raise low_offset (e.g., 0.98-0.99), catch smaller pullbacks

**Ranging market**:
- Lower ewo_high and ewo_low
- Narrow buy/sell offset range

---

## Chapter 7: Time Frame and Data

### 7.1 Default Time Frame: 5 Minutes

**Why 5 minutes**:
- Less noisy than 1 minute
- More responsive than 1 hour
- Suited for crypto's high volatility

### 7.2 Data Requirements

Needs at least **200 candles** of historical data.

**Why**:
- EMA-100 needs 100 candles to stabilize
- EWO's EMA-200 needs 200 candles

---

## Chapter 8: Who Is This Strategy For?

### 8.1 Suitable For

- People with quantitative trading basics
- Trend-following traders
- People with moderate risk tolerance (35% stop-loss isn't small)
- People with time to monitor (5-minute cycle needs some attention)

### 8.2 Not Suitable For

- Complete beginners (may misuse without understanding)
- Risk-averse people (35% stop-loss keeps you up at night)
- People wanting passive income (any strategy needs maintenance)
- Ultra-short-term traders (5-min cycle not for second-level trades)

### 8.3 Suitable Trading Pairs

**Recommended**:
- BTC/USDT
- ETH/USDT
- Other major coin/USDT pairs

**Not recommended**:
- Low-liquidity small coins
- Extremely volatile altcoins
- Heavily manipulated coins

---

## Chapter 9: Strategy Pros & Cons

### 9.1 Pros

**1. High signal quality**
Three buy signals each correspond to different market states; won't open positions recklessly.

**2. Complete risk control**
Tiered take-profit, fixed stop-loss, trailing stop — three layers of protection.

**3. Highly customizable**
12 adjustable parameters, adaptable to risk preferences.

**4. Clear logic**
Every condition has a clear meaning; not a black box.

### 9.2 Cons

**1. Poor ranging market performance**
Easily gets whipped in oscillating markets with no trend.

**2. Parameter sensitivity**
12 parameters; over-optimizing historical data may cause poor live performance.

**3. Not suited for one-sided crashes**
Bottom-fishing signals may trigger too early in sustained declines.

**4. Needs continuous monitoring**
5-minute cycle not suited for complete hands-off operation.

---

## Chapter 10: Practical Usage Guide

### 10.1 Pre-Launch Preparation

1. **Backtest**: Test on at least 6 months of historical data
2. **Paper trade**: Run in simulation environment for at least 1 month
3. **Small live trade**: Verify with money you can afford to lose
4. **Record trades**: Track every trade for analysis

### 10.2 Position Management

**Per trade**: 2-5% of total capital
**Simultaneous positions**: 3-5 pairs recommended
**Correlation**: Choose low-correlation pairs

### 10.3 Routine Maintenance

**Daily**: Check if strategy running normally, review trade records
**Weekly**: Analyze weekly P&L, check if parameters need adjustment
**Monthly**: Backtest and optimize

### 10.4 Common Problem Solutions

**Problem: Too many signals**
Solution: Raise ewo_high, lower low_offset, make conditions stricter

**Problem: Too few signals**
Solution: Lower ewo_high, raise low_offset, relax conditions

**Problem: Stopped out too frequently**
Solution: Check if market is ranging; consider pausing strategy or changing pairs

**Problem: Missed sell points**
Solution: Lower high_offset, make exit conditions looser

---

## Chapter 11: Comparison with Other Strategies

### 11.1 vs Simple MA Crossover

| Aspect | This Strategy | Simple MA |
|--------|--------------|-----------|
| Entry | MA offset vs crossing | MA crossing |
| Reaction speed | Faster | Slow (waits for crossing) |
| Signal frequency | Medium | Low |
| False signals | Fewer (multi-verification) | Many |

### 11.2 vs Pure RSI Strategy

| Aspect | This Strategy | RSI Strategy |
|--------|--------------|--------------|
| Indicator count | Multiple | Single |
| Entry precision | High | Low |

### 11.3 vs Trend-Following Strategy

| Aspect | This Strategy | Trend-Following |
|--------|--------------|----------------|
| Philosophy | Buy pullbacks (mean reversion) | Chase trends |
| Advantage | Works in ranging markets | Catches big trends |
| Disadvantage | May miss big trends | Losses in ranging markets |

---

## Chapter 12: Advanced Tips

### 12.1 Multi-Timeframe Confirmation

While the strategy is primarily 5-minute, use 1-hour to confirm major direction:

1. 1-hour chart judges big trend (simple trend line or MA)
2. Only trade in the big trend's direction
3. 5-minute chart finds entry points

**Benefit**: Filters counter-trend trades, improves win rate.

### 12.2 Trading Session Selection

Crypto markets vary by time:

**High volatility (Asian trading hours)**:
- 9 PM - 1 AM (US market open)
- Use looser parameters

**Low volatility**:
- Asian daytime
- May have fewer signals, or use more aggressive parameters

### 12.3 Position Sizing with Kelly Formula

**Simple fixed ratio**:
Per trade risk = Total capital × Risk ratio (e.g., 1%)
Position size = Risk amount / Stop-loss ratio

**Example**:
- Total: $10,000
- Per trade risk 1% = $100
- Stop-loss 35%
- Position = $100 / 0.35 = $285

---

## Chapter 13: Final Summary

### 13.1 Core Takeaways

1. **Strategy essence**: Buy when price deviates from MA, sell when it recovers
2. **Three buy signals**: Normal pullback, deep oversold, extreme panic
3. **Two exit conditions**: Normal profit-taking, trend reversal
4. **Triple protection**: Tiered take-profit, trailing stop, fixed stop-loss
5. **Highly adjustable**: 12 parameters adaptable to risk preferences

### 13.2 Three Principles

**Principle 1: Backtest before live trading**
Don't trust any strategy's default parameters; always verify with historical data.

**Principle 2: Start small**
Even with great backtest results, verify with small capital first.

**Principle 3: Continuous monitoring and optimization**
Markets change; strategies need adjustment. No set-it-and-forget-it.

### 13.3 Final Thoughts

The best strategy is just a tool. Real success depends on:

1. **Discipline**: Execute strategy rules strictly; don't change rules due to emotions
2. **Patience**: Wait for right opportunities; don't trade just to trade
3. **Learning**: Understand strategy principles to better use and improve it

Crypto markets carry extreme risk. Any strategy can lose money. Please control risk and only trade with funds you can afford to lose.

Good luck trading!

---

*Disclaimer: This document is for learning and research reference only, not investment advice. Crypto trading involves high risk; historical returns don't guarantee future performance. Please trade prudently and bear your own risk.*
