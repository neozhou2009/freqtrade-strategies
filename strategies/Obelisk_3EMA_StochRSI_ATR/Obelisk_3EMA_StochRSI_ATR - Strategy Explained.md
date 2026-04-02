# Obelisk_3EMA_StochRSI_ATR: Plain English Breakdown

## Written For You

This is for regular traders who don't need fancy math. We'll break it down piece by piece, guaranteed you'll understand after reading.

---

## 1. What Is This Strategy?

Three things combined into one complete system:

1. **Three lines (EMA)**: Tell you if the market is going up or down
2. **One indicator (StochRSI)**: Tell you when to jump in
3. **One ruler (ATR)**: Tell you how much to aim for and how much to risk

From an old YouTube video by "Trade Pro" claiming 76% win rate — but take that number with a BIG grain of salt.

**Important**: The author says "DON'T RUN THIS LIVE" — it's for learning and backtesting only.

---

## 2. What Are These Three EMAs?

Think of moving averages as roads of different lengths:

- **EMA8 (fast road)**: Average of last 8 candles — very responsive, reacts quickly
- **EMA14 (middle road)**: Average of last 14 candles — balanced
- **EMA50 (slow road)**: Average of last 50 candles — big picture

**How to read them:**

When they're stacked like stairs going up:
- EMA8 on top
- EMA14 in middle
- EMA50 on bottom

This = market is climbing → consider buying.

Reversed = market falling → don't buy.

**Why three instead of one?**

One road can lie to you — a tiny wiggle and it's confused. Three roads agreeing = more trustworthy.

---

## 3. What Is StochRSI?

First understand RSI: a thermometer for prices (0-100). Too high (>70) = overheated; too low (<30) = too cold.

StochRSI takes RSI and runs it through a "randomizer" again — like zooming in on the thermometer. Even more sensitive.

Has two lines:
- **K line**: Fast one
- **D line**: Slow one (average of K)

When K crosses above D = **golden cross** = momentum starting to strengthen = potential buy timing.

---

## 4. What Is ATR?

Average True Range — measures "how much does this market wiggle?"

Example:
- Bitcoin moves 5% a day → ATR is big
- A stable coin moves 0.1% a day → ATR is tiny

**How strategy uses it:**

- **Take-profit**: Entry price + 2 × ATR
- **Stop-loss**: Entry price - 3 × ATR

Example: You buy at $100, ATR is $2.
- Take-profit: $100 + 2×$2 = $104
- Stop-loss: $100 - 3×$2 = $94

**Why adapt to volatility?**

Big ATR (volatile market) → wider stops, you don't get shaken out by normal swings.
Small ATR (calm market) → tighter stops, you don't lose as much.

---

## 5. When Does It Buy?

All three conditions must be TRUE at the same time:

1. EMA8 > EMA14 > EMA50 (stairs going up)
2. K-line crosses above D-line (golden cross)
3. Both happen on the SAME candle

Like leaving home requiring: good weather AND parents said yes AND friends available AND good mood AND healthy AND destination open. One fail = stay home.

**Why both conditions?**

- EMA alone: tells you direction but not "is right now a good time?"
- StochRSI alone: might buy in a downtrend
- Both together: right direction + right timing = solid entry

---

## 6. When Does It Sell?

Two scenarios:

### Scenario 1: Made Enough
Price hits your take-profit level → auto-sell. Lock in gains.

### Scenario 2: Lost Too Much
Price hits your stop-loss level → auto-sell. Cut losses.

**No active selling**

This strategy doesn't say "I think it'll drop now" to sell. It only watches two lines: take-profit and stop-loss. Hit one = execute.

**Pros**: Won't get shaken out by short-term swings
**Cons**: May give back some profits if it spikes then pulls back

---

## 7. Stop-Loss and Take-Profit Details

### Take-Profit: +2× ATR
You buy at $100, ATR is $3.
TP = $100 + 2×$3 = $106.
Hit $106 → sell.

### Stop-Loss: -3× ATR
Same example: SL = $100 - 3×$3 = $91.
Drop to $91 → sell.

### The Math
Gain = $6, Loss = $9
Gain is LESS than loss. That seems bad...

But the strategy makes money through **WIN RATE**:
- 10 trades, 6 wins × $6 = $36
- 4 losses × $9 = $36
- Break even!

- 10 trades, 6.5 wins × $6 = $39
- 3.5 losses × $9 = $31.50
- Net profit = $7.50

**Needs about 60%+ win rate to make money.**

---

## 8. Timeframe Trick

**Backtest**: Use 5-minute chart
**Live**: Use 1-hour chart

**Why backtest small, trade big?**

Small timeframe = more precise simulation. Long timeframe = fewer fake "whipsaw" where one candle hits both your stop and target.

The strategy handles this conversion internally — you trade 1h but backtest on 5m.

---

## 9. Pros

1. **Logic is clear**: EMA says direction, StochRSI says timing, ATR says risk — each has a job
2. **Risk is set before entry**: You know max loss before you even buy
3. **Doesn't chase**: EMA arrangement confirms trend first, StochRSI finds good timing — not just "it's going up, BUY!"
4. **Adapts to volatility**: ATR-based stops grow and shrink with the market

---

## 10. Cons

1. **Long only**: Can't make money when market falls
2. **Unbalanced risk/reward**: Gain 2, lose 3 — need high win rate
3. **Gets hurt in ranging markets**: EMA flips back and forth, StochRSI keeps crossing — get stopped out repeatedly
4. **Author says don't use live**: The code literally says "DO NOT RUN LIVE"

---

## 11. How to Use This Strategy

### Step 1: Backtest
Run on historical data. Don't just look at returns — check:
- Max drawdown (biggest loss)
- Win rate
- Sharpe ratio
- Trades per day

### Step 2: Optimize Parameters
Defaults aren't perfect for every pair. Try:
- EMA periods (e.g., 7-21-55 instead of 8-14-50)
- StochRSI settings
- ATR multiples

### Step 3: Paper Trade
At least 1-2 months in paper mode.

### Step 4: Small Capital Live
Start with money you can afford to lose.

### Step 5: Keep Watching
Markets change. Strategy might need adjusting.

---

## 12. Quick Q&A

**Q: Can it make money?**
A: No guarantees. Backtest good ≠ live good. Market changes.

**Q: Do I need to know coding?**
A: To modify and run it, yes — some Python and Freqtrade knowledge needed.

**Q: Why is stop bigger than profit?**
A: Designed for high win rate. If win rate > 60%, still profitable.

**Q: Can I add shorting?**
A: Yes — flip the conditions: EMA8 < EMA14 < EMA50, K crosses below D.

**Q: Which timeframe?**
A: Author recommends backtest 5m or 1m, live trade 1h. Code handles the conversion.

---

## 13. Final Thoughts

This strategy is interesting. It combines three classic tools into one system:
- **Trend** (EMA): Which direction
- **Momentum** (StochRSI): When to go
- **Risk control** (ATR): When to stop

But it's not a holy grail. Author himself says don't use it live. Think of it as a teaching example.

**If you're new to quant trading**: Study this. When you understand it, you've taken the first step. Then look at more complex strategies and you'll notice many use similar building blocks.

**Remember**: Strategy is a tool, the market is alive. Even the best tool needs human supervision. Expecting to set it and forget it and print money? Wake up — that's not how this works.

---

## Quick Reference Card

| Item | Content |
|------|---------|
| Strategy Type | Trend following |
| Direction | Long only |
| Entry | EMA bullish + StochRSI golden cross |
| Exit | Hit take-profit or stop-loss |
| Take-Profit | Entry + 2× ATR |
| Stop-Loss | Entry - 3× ATR |
| Timeframe | Backtest 5m, Live 1h |
| Author Says | Don't use live |

---
