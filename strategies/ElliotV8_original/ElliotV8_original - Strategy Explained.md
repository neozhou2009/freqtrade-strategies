# ElliotV8_original: Plain and Simple

## 1. What Is This?

ElliotV8_original is the original/reference version of the V8 Elliot Wave strategy for Freqtrade. Built by @Rallipanos. Think of it as the "director's cut" — all the features, all the knobs to turn, everything in one place.

Core idea: **follow Elliott Wave theory to catch waves — buy when price dips in an uptrend, sell when the wave peaks.**

## 2. How It Decides to Buy

Two ways to enter, both strict:

### Way 1: Trend Pullback

6 conditions must be met:
1. Fast RSI < 35 (short-term is oversold)
2. Price is about 2.5% below buy MA
3. EWO > 2.327 (uptrend momentum is there)
4. Regular RSI < 69 (not overheated)
5. Volume is happening
6. Price also below sell MA level

This is for when the market is climbing but took a small breath — a healthy pullback in an uptrend.

### Way 2: Extreme Crash Bounce

5 conditions:
1. Fast RSI < 35
2. Price is about 2.5% below buy MA
3. EWO < -19.988 (EXTREME oversold — this is panic territory)
4. Volume is happening
5. Price also below sell MA level

No RSI check because when EWO is at -20, RSI is already terrible.

## 3. How It Decides to Sell

### Sell Way 1: Strong Momentum

- Price above HMA(50) (still in uptrend)
- Price above sell MA × 0.997
- RSI > 50 (market is healthy)
- Fast RSI crossing above slow RSI

This is the "let winners run" exit — market is strong and accelerating, but you're taking profits at a good level.

### Sell Way 2: Weak Momentum

- Price below HMA(50) (trend is uncertain)
- Price just above sell MA × 0.991
- Fast RSI crossing above slow RSI

This is the "don't push your luck" exit — the bounce is losing steam, even if you only made a little, take it and move on.

## 4. Four Layers of Protection

### Layer 1: Fixed Stop-Loss — 32%

If you're down 32%, exit. Seems huge, but:
- Entry conditions are strict, so when you enter you're already in a good spot
- Crypto can swing wildly, especially on 5-minute charts
- This gives trades room to breathe

### Layer 2: Trailing Stop

- Activates at 2% profit
- Stays 0.1% below peak (very tight!)
- If price even dips 0.1% from its high → sells

Example: Buy at $100, climbs to $102 (2%) → activates. Climbs to $110 → stop at $109.89. Pulls back to $109.89 → sells, locks in ~9.89%.

Why so tight (0.1%)? Because V8 series is designed to lock in profits aggressively and move on.

### Layer 3: Time-Based ROI (Profit Targets)

| Held for | Target |
|----------|--------|
| Just bought | 8% |
| 40 minutes | 3.2% |
| 87 minutes | 1.6% |
| 3+ hours | Any profit! |

Longer hold = lower expectations. Your capital has better uses.

### Layer 4: Sell Signal Protection

Only sells via signals when you're profitable (at least 1%). Won't panic-sell at a loss based on technical signals.

## 5. Key Indicators

### EWO

Short EMA (50) minus Long EMA (200). The V8_original uses:
- ewo_high = 2.327: Moderate threshold (V8HO uses 5.417, much stricter)
- ewo_low = -19.988: Extreme panic threshold (same as V8HO)

This means V8_original is more permissive on the upside (lower bar) than V8HO, potentially generating more buy signals.

### RSI Family

Three speeds working together:
- RSI(4): Lightning-fast, catches oversold fast
- RSI(14): Standard confirmation
- RSI(20): Slower, for trend direction

### Moving Averages

- Buy EMA: 14-period (relatively short)
- Sell EMA: 24-period (longer)
- HMA(50): Low-lag, for trend health checks

## 6. Pros and Cons

### Pros
- **Full feature set**: Everything the V8 series offers, all in one place
- **More buy signals**: Lower EWO threshold than V8HO
- **4-layer protection**: Comprehensive risk management
- **Well-documented code**: Great for learning Elliott Wave systems
- **Highly tunable**: 8 parameters to optimize

### Cons
- **32% stop is huge**: Largest potential loss in the V8 family
- **Needs lots of data**: Requires 400 candles to start
- **More signals = more noise**: More trades but some may be lower quality
- **Requires tuning**: All those parameters need optimization

## 7. Who Is This For?

**Good for:**
- Learners who want to study the full system
- Traders who want more frequent opportunities
- People willing to spend time optimizing parameters
- Those who understand Elliott Wave theory basics

**Not ideal for:**
- Beginners who want plug-and-play
- Capital that can't handle -32% worst-case scenarios
- People who want minimal parameter tweaking
- Ultra-conservative traders

## 8. How to Use

1. **Download**: Put ElliotV8_original.py in your Freqtrade strategies folder
2. **Get data**: `freqtrade download-data --timeframe 5m --timerange 20220101-`
3. **Backtest**: `freqtrade backtesting --strategy ElliotV8_original --timeframe 5m`
4. **Optimize**: `freqtrade hyperopt --strategy ElliotV8_original --epochs 500 --spaces buy sell`
5. **Validate**: Use different time periods to confirm parameters aren't overfitted
6. **Dry run**: Simulated trading for 1-2 weeks
7. **Small live**: Start with 10-20% of capital

## 9. Common Questions

**Q: Can I use this for stocks?**
A: In theory, but parameters would need significant adjustment. Stocks don't have the same volatility patterns as crypto, and there are trading hour restrictions.

**Q: How much capital do I need?**
A: Recommend at least 10-20x your minimum trade size to allow for proper position sizing and drawdown management. Maybe $500-1000 minimum to make it worth the effort.

**Q: Can I just use default parameters?**
A: Defaults were optimized on historical data but market conditions change. Periodic re-optimization is recommended.

## 10. Summary

ElliotV8_original is the complete V8 Elliot Wave strategy — the full framework, all features included, with maximum tunability. It's the version to study if you want to understand the whole system, and the version to customize if you want to build on the approach.

**Key decision factors:**
- Choose this if you want the full toolkit and are willing to tune it
- Choose V8HO if you want stricter entry quality out of the box
- Choose V5 variants if you want tighter stop-losses

**Universal truth:** Backtest thoroughly, validate carefully, start small, monitor always, and remember — strategy is a tool, not a guarantee.

---

*For learning reference only, not investment advice.*
