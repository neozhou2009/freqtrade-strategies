# ElliotV8HO: Plain and Simple

## 1. What Is This?

ElliotV8HO = Elliott Wave + Version 8 + Hyperopt Optimized. It's an auto crypto trading bot using Elliott Wave theory with computer-optimized parameters.

Core idea: **only buy when momentum is REALLY strong (or REALLY weak), and take profits with discipline.**

## 2. How It Decides to Buy

### Way 1: Strong Trend Pullback

Conditions:
- Fast RSI < 35 (short-term oversold)
- Price below buy MA × 0.983 (~1.7% discount)
- EWO > 5.417 (VERY strong momentum — this is a high bar!)
- RSI < 61 (not overheated)
- Volume happening
- Price also below sell MA × 1.011 (not already at exit)

### Way 2: Extreme Crash Bounce

Conditions:
- Fast RSI < 35
- Price below buy MA × 0.983
- EWO < -17.251 (panic mode, crashed hard)
- Volume happening
- Price below sell MA × 1.011

Notice Way 1's EWO threshold is 5.417 — much higher than most other Elliot strategies (typically 2-3). This means: "Only buy if momentum is SUPREMELY strong." Fewer false signals, but fewer opportunities.

## 3. How It Decides to Sell

### Sell Way 1: When Things Are Hot

- Price above HMA(50) (still in an uptrend)
- Price above sell MA × 1.011 (~1.1% above)
- RSI > 50 (market still bullish)
- Fast RSI crossing above slow RSI (momentum accelerating)

This means: "The trend is strong and getting stronger. Take profits at a good level."

### Sell Way 2: When Momentum Is Weak

- Price below HMA(50) (trend uncertain)
- But price above sell MA × 0.997 (~at the MA level)
- Fast RSI crossing slow RSI (some bounce)

This means: "The trend is weak, but there's a small bounce. Get out with what you have."

## 4. Three Layers of Protection

### Layer 1: Fixed Stop-Loss — 18.9%

Down 18.9% and you're out. Moderate width for crypto volatility.

### Layer 2: Phased ROI (Take-Profit Ladder)

| Held for | Target |
|----------|--------|
| Just bought | 8% |
| 40 minutes | 3.2% |
| 87 minutes | 1.6% |

The longer you wait, the less profit you demand. Your capital could be doing something else.

### Layer 3: Trailing Stop (The Lock)

- After making 2% profit, trailing stop activates
- Tracks the peak, stays 0.5% below it
- If price pulls back 0.5% from peak → SELLS

Example: Buy at $100, climbs to $102 (2% profit) → activates. Climbs to $110 → stop at $109.45. Pulls back to $109.45 → sells, locks in ~9.45%.

## 5. Key Indicators

### EWO

Short EMA (50) minus Long EMA (200). The key difference in this variant: ewo_high = 5.417 is much higher than other Elliot strategies (typically 2-3).

Why so high? Because when EWO exceeds 5, it means the short-term EMA has run WAY above the long-term EMA — a super strong momentum. The strategy only buys pullbacks in THIS kind of environment. Fewer signals, but each one is high-conviction.

### RSI

Three versions:
- RSI(4): Fast, catches oversold quickly
- RSI(14): Standard confirmation
- RSI(20): Slower, for trend checks

Buy requires fast RSI < 35, standard RSI < 61.

### HMA(50)

Hull Moving Average — faster than regular MA, smoother than EMA. Used as the trend health check. Price above HMA = healthy trend.

## 6. Pros and Cons

### Pros
- **High-conviction entries**: EWO > 5.417 = very selective
- **Phased profit targets**: Not greedy, adapts to time
- **HMA exit confirmation**: Catches momentum shifts well
- **Hyperopt optimized**: Parameters well-tuned
- **Two sell modes**: Strong and weak market strategies

### Cons
- **Fewer signals**: High EWO bar = less frequent trades
- **May miss opportunities**: EWO might not hit 5.4 in moderate trends
- **18.9% stop**: Moderate width
- **1h timeframe unused**: Defined but not integrated

## 7. Who Is This For?

**Good for:**
- Patient traders who wait for perfect setups
- Quality-over-quantity traders
- Those who want fewer but stronger signals
- People comfortable with 8% profit targets

**Not ideal for:**
- Traders who want frequent action
- Low-capital accounts (can't wait long between trades)
- Those who want to capture every small move

## 8. How to Use

1. **Backtest**: `freqtrade backtesting --strategy ElliotV8HO`
2. **Optimize**: `freqtrade hyperopt --strategy ElliotV8HO --epochs 100`
3. **Dry run**: Simulated trading for 1-2 weeks
4. **Small live**: Start with 10-20% of capital
5. **Monitor**: Check weekly

## 9. Summary

ElliotV8HO is the "quality and patience" variant in the Elliot family. Its standout feature: requiring EWO > 5.417 for entries — much stricter than siblings. This means fewer trades, but each trade has stronger momentum behind it.

**Best choice if:** You prioritize quality over frequency, can be patient, and want high-conviction setups.

**Choose a different variant if:** You want more frequent trading, have small capital needing turnover, or prefer catching all moves.

**Key rule:** No strategy guarantees profits. Backtest first, start small, monitor always, and remember — risk control beats chasing returns.

---

*For learning reference only, not investment advice.*
