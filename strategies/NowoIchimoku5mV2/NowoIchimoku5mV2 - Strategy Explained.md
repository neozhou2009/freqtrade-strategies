# NowoIchimoku5mV2: What's This Strategy Doing?

## 1. What Is This Strategy?

NowoIchimoku5mV2 is a cryptocurrency trading strategy. Its core idea is simple: **follow the trend, buy above the cloud, exit when the trend dies.**

It mainly uses the Ichimoku Cloud, combined with Bollinger Bands and StochRSI to decide when to enter and when to leave. It's for trend traders — the kind who "see it rising, ride along a bit, then sell when it stops rising."

⚠️ **Warning**: The strategy file header says "This version of the strategy is broken!" — don't use it for live trading yet! But it's great for learning.

---

## 2. The Ichimoku Cloud in Plain English

The Ichimoku Cloud looks complex but is just several lines on a chart that help you read the trend.

**The Cloud (most important part)**:
- Has upper and lower boundaries
- Has colors: green = uptrend, red = downtrend
- Price above the cloud = bulls winning
- Price below the cloud = bears winning
- Price inside the cloud = sideways, direction unclear

**Two main lines**:
- Conversion Line (fast): responsive, like a short-term MA
- Base Line (slow): less responsive, like a medium-term MA
- Fast above slow = short-term winning
- Fast below slow = short-term losing

**Bottom line**: This strategy waits for price to stand above the cloud AND the cloud is green before considering a buy.

---

## 3. What Tools Does It Use?

### 3.1 Ichimoku Cloud
Judges the big picture direction. Looks at cloud color and price-to-cloud position.

### 3.2 Bollinger Bands
Like a rubber band around price — when price reaches the upper band, it's risen too far and may pull back. This strategy only uses the upper band to judge if it's gotten too overextended.

### 3.3 StochRSI
Helps identify "way too many buyers" (overbought) or "way too many sellers" (oversold).
- Value > 80 = overbought
- Value < 20 = oversold

Used to decide when to take profits.

---

## 4. Timeframe Setup

This strategy watches two time levels:
- **5-minute chart (main battlefield)**: Where actual trades happen
- **1-hour chart (big picture)**: Where trend direction is judged, then applied to the 5-minute chart

Why both? Like zooming in and out: far away you see the big picture, close up you see details. Together they let you catch the big direction AND find good entry points.

---

## 5. When Does It Buy?

Seven conditions must ALL be met:

**Condition 1**: Current candle is bullish (close > open)
**Condition 2**: Price breaks above the displaced cloud upper (× 0.603)
**Condition 3**: Price is above displaced cloud lower
**Condition 4**: Cloud is green (Leading A > Leading B)
**Condition 5**: Conversion Line > Base Line
**Condition 6**: Price > displaced Conversion Line
**Condition 7**: Price > double-displaced cloud upper

All seven must pass = BUY. Like leaving home requires: good weather, free schedule, friends available, good mood, healthy body, destination open. One fail = stay home.

### Cooldown Mechanism
After buying, next buy requires cloud to go red then green again. Prevents repeatedly opening positions in the same trend.

---

## 6. When Does It Sell?

No active selling — exits are handled by "stops." These aren't just for losses, they also trigger when profitable!

### 6.1 StochRSI Overbought Exit
When StochRSI K > 80 AND you've made at least 3.6%, sell.

**Plain English**: Risen too fast, take the money and run.

### 6.2 Bollinger Breakout Exit
When price crosses from below to above the Bollinger upper AND you've made at least 1.1%, sell.

**Plain English**: Price ran too far outside normal range, time to go.

### 6.3 Target Price Exit
Target = Entry Price + (Entry Price - Entry Cloud Lower) × 1.918

When price hits this, sell.

**Plain English**: Made enough, take profits.

### 6.4 Cloud Support Failure Exit
If price drops below 97.1% of entry cloud lower, sell.

**Plain English**: Support broke, trend may reverse, run!

---

## 7. Stop-Loss Setup

### 7.1 Hard Stop
**-29.3%**. If it drops that much, it's gone.

⚠️ This is very wide! Means buying $100 might lose up to $70. Aggressive — needs a trader who can handle big swings.

### 7.2 Trailing Stop
When you're in profit, the stop line moves up with price. If it retraces and hits the line, it sells.

### 7.3 Time-Decaying Profit Targets
- Right when buying: want 10%
- After 30 minutes: only need 5%
- After 60 minutes: just 2%

**Plain English**: The longer it takes, the lower your expectations — don't be greedy.

---

## 8. Tunable Parameters

### Buy Parameter
**close_above_shifted_upper_cloud** (default 0.603, range 0.5-2.0): How strictly price must break the cloud. Higher = stricter.

### Sell Parameters
**srsi_k_min_profit** (default 3.6%): StochRSI overbought profit threshold. Higher = wait longer for bigger gains.
**above_upper_min_profit** (default 1.1%): Bollinger breakout profit threshold. Lower = easier to trigger.
**limit_factor** (default 1.918): Target multiplier. Higher = higher target = longer hold.
**lower_cloud_factor** (default 0.971): Cloud stop discount. Lower = tighter stop.

---

## 9. Pros

### 9.1 Rigorous Trend Confirmation
Seven conditions = not random buying, only when trend is truly established.

### 9.2 Dual Timeframe
1-hour for direction, 5-minute for entry — not just staring at theshort term.

### 9.3 Dynamic Exit Mechanism
Not stubbornly holding to a stop — exits when overbought, overextended, or target reached.

### 9.4 Adjustable Parameters
Five parameters can be tuned to your style — more aggressive or more conservative.

### 9.5 Clean Code Structure
Python code with clear logic separation — easy to learn from.

---

## 10. Cons

### 10.1 Stop-Loss Too Wide
-29.3% stop is massive. Many can't stomach it. Several losses in a row will hurt your capital badly.

### 10.2 Entry Conditions Too Strict
All 7 conditions must be met. Few signals. May miss good opportunities even in strong trends.

### 10.3 No Explicit Profit Target
Only exit conditions, no hard "make X% and leave" rule. May give back profits in pullbacks.

### 10.4 Gets Hurt in Ranging Markets
Trend strategies get beaten up in sideways markets. Price bounces around, you get stopped out repeatedly.

### 10.5 Strategy Version Has Problems
File says "broken" — don't use directly!

---

## 11. Backtesting Prep

### 11.1 Data
Need at least 500 5-minute candles. Ichimoku needs lots of history to "warm up."

### 11.2 Duration
At least several months, ideally a year, to cover different market conditions.

### 11.3 Fees and Slippage
Set fees (exchange usually 0.1%) and slippage in backtesting — or results will look toooptimistic.

### 11.4 Split Validation
Split data into segments: one for finding parameters, another for validation. Don't optimize on all one dataset — that's overfitting.

---

## 12. Live Trading Tips

### 12.1 Position Sizing
Because stop is -29.3%, risk each trade at 1-3% of total capital.

For a $10,000 account:
- Max loss per trade: $100-300
- Stop 29.3%
- Per-trade position = $100/0.293 ≈ $340 (conservative) or $300/0.293 ≈ $1,020 (aggressive)

### 12.2 Pick the Right Coins
High-liquidity mainstream coins like BTC, ETH. Small coins have bigger slippage, strategy underperforms.

### 12.3 Keep an Eye On It
Though automated, check periodically:
- Too many or too few signals?
- Stop-losses triggered?
- Drawdown manageable?

### 12.4 Set Alerts
- Daily loss exceeds X%
- Y consecutive losses
- Market volatility spikes

---

## 13. Summary

### One-Line Summary
A **trend-following cloud strategy** with strict entries, wide stops, for trend traders who can handle big swings.

### What It Teaches Us
1. **Multi-condition confirmation**: Don't act on one signal — verify with several.
2. **Multi-timeframe**: Big picture direction + small entry timing — great approach.
3. **Dynamic exits**: Adjusting to market vs. waiting for a fixed stop — smarter.
4. **Cloud usage**: Ichimoku is a great tool — worth deep study.

### How to Improve This Strategy
1. **Tighten the stop**: -29.3% is too wild, -10% to -15% more comfortable.
2. **Add volatility filter**: Don't trade when ADX is low (no trend).
3. **Partial profit-taking**: Take half at 5%, half at 10%.
4. **Relax entry slightly**: Try 5-out-of-7 conditions rather than all-7.

### Who Is This For?

**Good**:
- Can handle big drawdowns
- Trend traders
- Patient for signals
- Want to learn strategy thinking

**Not good**:
- Risk-averse
- High-frequency traders
- Short-term only
- Want a plug-and-play strategy (this version has problems!)

---

**Final thought**: Strategy is a tool. Good strategy plus good mindset and position management = surviving and profiting in markets.

NowoIchimoku5mV2 has "has problems" written on it, but its thinking and logic are worth studying. Especially how it combines multiple conditions and designs dynamic exits — can borrow these ideas for other strategies.

**Remember**: Never trade with money you can't afford to lose. Always backtest first, then live. Always keep learning.

---

*This document is for learning purposes only and does not constitute investment advice.*
