# ElliotV5HO: Plain and Simple

## 1. What Is This?

ElliotV5HO is an auto crypto trading bot. "Elliot" means it uses Elliott Wave theory — the idea that prices move in predictable wave patterns. "V5HO" = Version 5, Highly Optimized.

Core idea: **Buy when price is on sale, sell when it's risen.** Sounds simple, but there are clever mechanics inside.

## 2. How It Decides to Buy

Two ways, either triggers a buy:

### Way 1: Buy the Discount (Trending Pullback)

Conditions:
- Price ~2% below the moving average
- EWO shows trend is still strong (EWO > 2.337)
- RSI below 55 (not overheated)

Like seeing your favorite thing go on a small sale while the overall trend is still upward.

### Way 2: Catch the Extreme Dip (Oversold Bounce)

Conditions:
- Price ~2% below moving average
- EWO is deeply negative (EWO < -15.87) — market is panicking
- No RSI check (when EWO is this low, RSI is already rock-bottom)

Like seeing everything on fire-sale during a panic. High risk, high reward.

## 3. How It Decides to Sell

Sell when price gets close to or slightly above the moving average.

But here's the clever part: if the price is way above what you paid, the moving average is climbing too. When price starts lagging the climbing average, it's time to take profits.

Only sells when profitable (at least 1%).

## 4. Three Layers of Protection

### Layer 1: Fixed Stop-Loss — 30.2%

If you're down 30.2%, the strategy admits defeat and exits. Seems wide, but crypto can swing 20% in a day. Too tight a stop gets shaken out by normal swings, then you watch it bounce back without you.

### Layer 2: Trailing Stop

- Activates after you make 3% profit
- Then stays 0.5% below the highest price you've reached
- If price climbs to $110, trailing stop sits at $109.45
- If price drops to $109.45 → you sell and lock in ~9.45% profit

This is "let profits run, lock them in when they retreat."

### Layer 3: Smart Stop (The "Big Fish" Strategy)

This is the clever part:

| If you've made | Stop gets |
|----------------|-----------|
| 10-20% | Locks in at least 5% |
| 20-30% | Locks in at least 10% |
| More than 30% | Loosens to -15% |

Why loosen when you're winning big? Because big trends have big swings. If your stop is too tight, a normal pullback during a monster rally kicks you out right before it surges again. Loosening the stop at 30% profit lets you "fish for the big one" — stay in the trade for the full trend.

## 5. How Long to Hold? (ROI)

| Time held | Target |
|-----------|--------|
| Right away | 5.1% |
| After 20 min | 3.2% |
| After 45 min | 1.6% |
| After 70 min | Any profit! |

Logic: the longer you wait, the lower your expectations. Your capital is tied up! Better to free it up and find a new opportunity.

**Exception:** If buy signals are still firing (market still climbing), it ignores the time limit and keeps holding.

## 6. What Indicators Does It Use?

### EWO (Elliott Wave Oscillator)

- Short EMA (50) minus Long EMA (200), divided by price
- Like your speedometer: current speed vs. average speed
- High positive = accelerating; High negative = braking hard

### EMA

Gives recent prices more weight, responds faster than simple average. Strategy uses:
- 11-period for buy signals
- 17-period for sell signals

### RSI

Classic 0-100 gauge. Below 55 for buying — don't chase when everyone's hyped up.

## 7. Pros and Cons

### Pros

1. **Sound theory**: Elliott Wave isn't made up, it's decades-old
2. **Two ways to catch opportunities**: Both trending pullbacks and crash rebounds
3. **Smart protection**: Three layers, especially the "big fish" loosening
4. **Not greedy**: ROI design shows "good enough is good enough"
5. **Tunable**: Many parameters to fit different coins/markets

### Cons

1. **Choppy markets hurt**: When price wobbles sideways, you get whipsawed
2. **Few signals**: Entry conditions are strict, might wait long between trades
3. **Parameter sensitive**: Defaults work OK but need tuning per coin
4. **Only 5-minute**: Can't easily switch timeframes

## 8. Practical Tips

**Which coins?** BTC, ETH, SOL, AVAX — big, liquid, predictable. Avoid tiny low-volume coins or newly listed ones with wild swings.

**When to use?** Trending markets with clear direction, no major news events.

**When to pause?** Choppy ranges, big news events (Fed meetings etc.), extreme volatility.

**How to tune parameters?** Use Freqtrade's hyperopt, but:
- Use 6-12 months of data
- Reserve some data for validation (don't overfit)
- Small real-money test before going big

**Position sizing:** 1-5% per trade. Don't go all-in on one trade.

## 9. The Strategy's Hidden Wisdom

**Wisdom 1: Follow the trend**
Buy Condition 1 is all about "buy the dip in an uptrend." Don't fight the tape.

**Wisdom 2: What goes down too far, goes back up**
Buy Condition 2 bets on mean reversion — extreme panic creates buying opportunities.

**Wisdom 3: Let winners run, cut losers fast**
Trailing stops and the "big fish" strategy lock in profits while giving trends room.

**Wisdom 4: Good enough is good enough**
ROI design says: don't be greedy. Take profits when you have them.

**Wisdom 5: Give opportunities time, but not forever**
The declining ROI targets: if it hasn't worked in a while, lower your expectations and move on.

## 10. Summary

ElliotV5HO is a thoughtfully designed strategy. It takes Elliott Wave — something that can feel "fuzzy" — and turns it into concrete rules with multiple layers of protection.

**No strategy is perfect.** All have losing periods. The key:
1. Long-term profitability
2. Maximum drawdown you can stomach
3. Whether you can stick to the system

**Before live trading:**
- Backtest thoroughly
- Simulated trading test
- Small real money first
- Regular check-ins
- Adjust as markets change

Remember: quantitative trading is a tool, not a money tree. It helps you follow rules and avoid emotional decisions, but it can't predict the future. Keep expectations realistic, keep learning, and don't invest what you can't afford to lose.

---

*For learning reference only, not investment advice.*
