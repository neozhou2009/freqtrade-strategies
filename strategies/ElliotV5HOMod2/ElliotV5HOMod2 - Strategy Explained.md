# ElliotV5HOMod2: Plain and Simple

## 1. What's This Strategy?

ElliotV5HOMod2 automatically buys and sells crypto. Core idea: **wait for a discount in an uptrend, sell when it's risen enough.**

Uses Elliott Wave theory — prices move in waves, like tides. The strategy catches the small "ripple" waves (pullbacks) to hop on the big wave direction.

## 2. How It Buys

### Buy Way 1: Ride the Trend Down a Little

Market is going up (bullish). Price suddenly dips a bit. Conditions:
- Price drops to ~2% below the buy moving average
- EWO > 3.34: Trend is still strong
- RSI < 60: Hasn't overheated
- Volume is happening

This is "buying the dip in an uptrend" — following the trend.

### Buy Way 2: Catch the Panic Crash

Market is crashing, everyone panicking. Conditions:
- Price drops to ~2% below moving average
- EWO < -17.457: WAY oversold, extreme
- No RSI check (EWO this low already means RSI is terrible too)

This is reverse thinking — betting the panic went too far and a bounce is coming.

## 3. How It Sells

When price rises to about 1.1% above the sell moving average (39-period, longer than the 17-period buy MA), it sells.

Why is the sell MA longer (39 vs 17)? Because:
- Buy: React fast, find opportunities quickly
- Sell: Stay calm, don't panic-sell

## 4. Four Layers of Protection

### Layer 1: Fixed Stop-Loss — 10%

Down 10% and you're out. Not as wide as some other Elliot strategies — tighter control.

### Layer 2: Trailing Stop

After making 3% profit, starts tracking the peak. If it climbs and then drops 0.5% from peak → sell and lock in most profits.

### Layer 3: Time Stop — "Zombie Position" Killer

Held more than 2 hours and still barely profitable or losing? Tighter stop activates. The thinking: a good trade should show gains relatively quickly. Holding 2+ hours with no profit means something's probably wrong, exit and move on.

### Layer 4: Declining ROI

| Held for | Target profit |
|----------|--------------|
| Just bought | 5% |
| 40 minutes | 4% |
| 3+ hours | 3% |

The longer you hold, the less profit you demand. Don't let capital sit forever waiting for the perfect exit.

## 5. Key Indicators

### EWO

Fast EMA (50) minus Slow EMA (200), divided by price. Strategy:
- EWO > 3.34: Climbing hard, look for pullback buys
- EWO < -17.457: Dropped way too hard, consider bottom-catch

Notice: positive threshold 3.34 vs negative threshold -17.457. The magnitude differs because crypto goes up slowly but crashes fast. So "climbing hard" is a lower bar than "dropped way too hard."

### EMA

- Buy EMA (17-period): Short-term average, reactive
- Sell EMA (39-period): Longer average, stable

### RSI

Standard 14-period. Buy requires RSI < 60 — not buying when overheated.

## 6. Pros and Cons

### Pros
- **Clear theory**: Elliott Wave isn't made up
- **Two approaches**: Handles both trending and crashed markets
- **Good risk control**: Four layers including zombie-position killer
- **Tunable**: Many parameters to adjust
- **Fast execution**: 5-minute timeframe

### Cons
- **Choppy markets = losses**: Trend strategies suffer when market wobbles
- **Parameters need care**: Can overfit to history
- **Slippage adds up**: 5-minute trades, watch fees
- **1-hour data unused**: Informative timeframe defined but not utilized

## 7. Which Coins?

**Good:** BTC/USDT, ETH/USDT, SOL, AVAX — liquid, trending behavior.

**Bad:** New small coins (no history), extreme volatility (stop-loss gets hunted), low-volume coins (can't get in/out at good prices).

## 8. How to Use

1. **Backtest**: `freqtrade backtesting --strategy ElliotV5HOMod2`
2. **Optimize**: `freqtrade hyperopt --strategy ElliotV5HOMod2 --epochs 500 --spaces buy sell`
3. **Dry run**: Simulated trading for 1-2 weeks
4. **Small live**: Start with 10-20% of capital
5. **Monitor**: Check weekly, adjust as needed

## 9. Summary

ElliotV5HOMod2 is a well-designed quantitative strategy:
- Based on real theory (Elliott Wave)
- Dual-entry for different market conditions
- Four-layer protection including zombie-position killer
- Reasonable 10% stop-loss

**Remember:** No strategy guarantees profits. Backtest well, start small, monitor regularly, and always — risk management first.

---

*For learning reference only, not investment advice.*
