# NotAnotherSMAOffsetStrategyX1: Strategy Explained

## 1. What Does This Strategy Do?

### One-Line Summary

**"Buy low in uptrends, sell high when conditions change."** Like smart shopping — buy when discounted, sell when priced up. Only buys in confirmed uptrends.

### Name Meaning

"NotAnotherSMAOffsetStrategyX1" = "Not just another SMA Offset Strategy, version X1" — the developer wanted to distinguish it from basic MA crossover strategies.

---

## 2. Core Logic

### When to Buy? Two Main Signals

**Signal 1: ewo1 (Trend Pullback)**

Conditions:
1. RSI(4) < 35 — short-term oversold
2. Price < EMA(14) × 0.975 — 2.5% below average
3. EWO > 2.327 — strong uptrend
4. RSI(14) < 69 — not overheated
5. Volume > 0

**Plain English**: "Uptrend but pulled back, RSI shows oversold — buy!"

**Signal 2: ewolow (Reversal)**

Conditions:
1. RSI(4) < 35
2. Price < EMA(14) × 0.975
3. EWO < -19.988 — deeply bearish
4. Volume > 0

**Plain English**: "Market crashed, everyone panicking — buy the panic!"

---

## 3. When to Sell?

### Condition 1: Price Above HMA

- Price > SMA 9
- Price > EMA(24) × 0.997
- RSI > 50
- Fast RSI > Slow RSI

**Plain English**: "Rose to target, momentum still strong — take profit."

### Condition 2: Price Below HMA

- Price < HMA 50
- Price > EMA(24) × 0.991
- Fast RSI > Slow RSI

**Plain English**: "Trend weakening but still profitable — lock in gains."

### Exit Confirmation

If HMA 50 still clearly above EMA 100 BUT price dipped below EMA 100 — don't sell! Trend still intact.

---

## 4. Risk Control

### Stop-Loss
- **-35% hard stop** — maximum loss per trade

### Trailing Stop
- Activates at **3% profit**
- Follows price up at **0.5% below peak**

### Tiered Selling
- 12 profit tiers (~90 conditions per tier)
- Higher profit = looser exit conditions

### ROI Table
- Immediate: 21.5%
- 40 min: 3.2%
- 87 min: 1.6%
- 201 min: Break-even

---

## 5. Parameters

| Parameter | Default | Meaning |
|-----------|---------|---------|
| low_offset | 0.975 | Buy when 2.5% below MA |
| ewo_high | 2.327 | Must be in strong uptrend |
| ewo_low | -19.988 | Panic buy threshold |
| rsi_buy | 69 | RSI must be below this |
| high_offset | 0.991 | Sell when above MA |
| high_offset_2 | 0.997 | Sell when above MA |

---

## 6. Summary

**"Buy when price is cheap in an uptrend, sell when it recovers. Dynamic tiered selling locks in profits at every level."**

Best for: Medium-term traders who understand indicators and can monitor strategy performance. The -35% stop-loss is wide, so position sizing matters.

Key: Backtest → Paper trade → Small live → Monitor & adjust.

**Trade only what you can afford to lose.**
