# ElliotV7: Plain and Simple

## 1. What Is This?

ElliotV7 is an automated crypto trading strategy built by @Rallipanos. The name says it all: the 7th major version of the Elliott Wave-based strategy. "Elliot" = uses Elliott Wave theory, "V7" = seventh iteration, thoroughly tested and refined.

Core philosophy: **only buy in confirmed uptrends, and only when price has pulled back a bit. Never chase, always wait for a better entry.**

## 2. How It Decides to Buy

The strategy ONLY buys in uptrends, confirmed by looking at the bigger picture (1-hour chart) before making decisions on the 5-minute chart.

Think of it like this: you're driving and checking the GPS (1-hour) for direction, then watching the road (5-minute) for when to accelerate or brake. If the GPS says you're going south, you're not gonna make a U-turn just because the road ahead looks clear.

### Buy Channel 1: The Trend Pullback (Main Way)

7 conditions ALL must be met:
1. 1-hour trend is UP (EMA20 > EMA25)
2. Fast RSI below 35 (short-term oversold)
3. Price is ~2.5% below the buy MA
4. EWO > 2.327 (trend momentum is strong)
5. Regular RSI < 69 (not overheated)
6. Volume is happening
7. Price is still below the sell MA

This is extremely strict. It means: "Market's going up, it pulled back a bit, short-term is oversold, but still healthy — good time to buy."

### Buy Channel 2: The Crash Bounce

Same 1-hour trend check, but EWO < -19.988 (extreme oversold, way worse than Channel 1).

This is for when the market has crashed so hard that even though the 1-hour trend might still be technically up, everyone's panicking. EWO at -20 is almost unheard of — that's full panic mode. The strategy bets that when things get this bad, a bounce is coming.

## 3. How It Decides to Sell

Two different sell channels, adapting to market strength:

### Sell Channel 1: Strong Momentum Exit

When market is running strong:
- 9-period SMA above 50-period HMA (short-term riding high)
- Price above sell MA
- RSI > 50 (still healthy)
- Fast RSI crossing above slow RSI

This means: "The trend is strong and accelerating, but we're taking profits anyway." More conservative exits in strong markets.

### Sell Channel 2: Normal Exit

When momentum is weaker:
- 9-period SMA below HMA
- Price above sell MA
- Fast RSI crossing slow RSI

More lenient — even if the trend isn't super strong, if we've made a little profit and the bounce is losing steam, take it and move on.

## 4. Three Layers of Protection

### Layer 1: Fixed Stop-Loss — 32%

If you're down 32%, admit defeat and exit. Seems huge, but:
- The entry conditions are SO strict (7 things must line up), this is the backup
- Crypto can gap 20%+ overnight
- The entry is at a pullback, so your cost basis is already reasonable

### Layer 2: Trailing Stop (Smart Lock)

After making 3% profit, it starts tracking:
- Climbs to $110 → stop at $109.45
- Pulls back to $109.45 → SELLS, locks in ~9.45%

### Layer 3: Time Stop (The "12-Hour Rule")

If you've been holding for 12+ hours AND you're down more than 10%, the stop tightens to just -1%. This means: "We gave this trade 12 hours. It's still deeply underwater. Something's wrong. Get out now."

## 5. What About Profits?

ROI targets (time-based):
- Right away: 5.1%
- After 10 min: 3.1%
- After 22 min: 1.8%
- After 66 min: ANY profit will do

The longer you wait, the less profit you demand. Your capital has opportunity cost.

**Exception:** If buy signals are still firing, it ignores time and keeps holding. "The trend is still your friend."

## 6. Key Indicators

### Multi-Timeframe Trend Check

1-hour EMA(20) > EMA(25) = uptrend. This is the MOST IMPORTANT condition — if the 1-hour trend isn't up, NOTHING triggers a buy.

### EWO

Short EMA (50) minus Long EMA (200). 
- EWO > 2.327: Strong upward momentum, pullback buy territory
- EWO < -19.988: Extreme panic, crash bounce territory

### RSI Family

- RSI(4): Lightning-fast, catches oversold quickly
- RSI(14): Standard, for confirmation
- RSI(20): Slower, for trend direction
- RSI(100): Ultra-long, for the big picture on the 1h chart

### HMA(50)

Hull Moving Average — faster than regular MA but smoother than EMA. Used to judge if the short-term trend is healthy.

## 7. Pros and Cons

### Pros
- **Bulletproof entry**: 7 conditions = almost no bad entries
- **Smart exits**: Different strategies for strong vs. weak markets
- **Time horizon respected**: Won't hold forever
- **Clear philosophy**: Only in uptrends, only on pullbacks

### Cons
- **Few signals**: 7 conditions = very selective
- **-32% stop is wide**: Largest stop among Elliot variants
- **Needs trending markets**: No trades in choppy/bear markets
- **Parameter sensitivity**: Each of the 7 conditions has tunable parameters

## 8. Who Is This For?

**Good for:**
- Patient traders who can wait for perfect setups
- Those who want minimum false signals
- Capital that can withstand -32% worst-case
- People who understand multi-timeframe analysis

**Not for:**
- Traders who want frequent action
- Capital that can't handle -32% swings
- Choppy/ranging market traders
- Beginners without Elliott Wave knowledge

## 9. Summary

ElliotV7 is the "quality over quantity" choice in the Elliot family:
- Only enters confirmed uptrends with 7 strict conditions
- Two different sell approaches based on market strength
- Three protection layers including a 12-hour time stop
- Designed for quality signals, not frequency

**Best use:** Use it when you want maximum confidence in each trade, can tolerate wider stops, and have patience for fewer but higher-quality setups.

**Before live:** Backtest extensively, validate with out-of-sample data, start small.

---

*For learning reference only, not investment advice.*
