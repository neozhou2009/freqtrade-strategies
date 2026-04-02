# NotAnotherSMAOffsetStrategyModHO_LamineDz_20210901: Strategy Explained

## 1. What Does This Strategy Do?

### One-Line Summary

**"Buy when price dips below average in an uptrend, sell when price recovers or trend weakens."**

Think of it as smart shopping — buy when prices are on sale, sell when they're marked up. The twist: only buy when the store (market) is generally heading up.

### Name Meaning

This is an MA Offset strategy developed by LamineDz in September 2021. The "NotAnother" part is the author's way of saying "I'm not just doing the same old thing" — this strategy really is different from basic MA crossover strategies.

---

## 2. Core Logic in Plain English

### The Idea

1. **Find the "fair price"** — using EMA
2. **Wait for a discount** — price must be at least 1.6% below fair price (offset 0.984)
3. **Check the "vibe"** — using EWO to confirm market direction
4. **Buy when conditions align**
5. **Sell when trend weakens**

---

## 3. When to Buy? Two Scenarios

### Scenario 1: Uptrend Pullback (EWO High Channel)

**When**: Market was going up, but took a breather.

**Conditions**:
1. Fast RSI < 35
2. Price < EMA × 0.984 (1.6% discount)
3. EWO > 3.206 (still bullish)
4. RSI(14) < 63
5. Volume > 0
6. Price below sell line

**Plain English**: "Market's going up but took a dip — buy!"

### Scenario 2: Deep Oversold (EWO Low Channel)

**When**: Market crashed and everyone's panicking.

**Conditions**:
1. Fast RSI < 35
2. Price < EMA × 0.984
3. EWO < -10.69 (deeply bearish)
4. Volume > 0
5. Price below sell line

**Plain English**: "Market's crashed hard — time to catch the falling knife!"

---

## 4. When to Sell? Two Conditions

### Condition 1: Made Money, Trend Still Up

**When**: Price recovered and momentum is still strong.

**Conditions**:
1. Price > SMA 9
2. Price > sell EMA × 1.0
3. RSI > 50
4. Fast RSI > Slow RSI
5. Volume > 0

**Plain English**: "Made money, trend still healthy — take profit!"

### Condition 2: Trend Showing Weakness

**When**: Price broke below HMA but still above baseline.

**Conditions**:
1. Price < HMA 50
2. Price > sell EMA × 1.002
3. Fast RSI > Slow RSI

**Plain English**: "Trend weakening but still profitable — protect gains!"

---

## 5. Risk Control

### Stop-Loss
- **10% fixed** — if it drops 10% from entry, sell automatically

### Trailing Stop
- Activates at **3% profit**
- Follows price up at **0.75% below peak**

### Slippage Protection
- If execution price is **2%+ worse** → reject and retry (up to 3 times)

### Profit Only Sell
- Won't sell unless you're **up 1%+**
- Prevents panic selling at small losses

---

## 6. Parameters

| Parameter | Default | Meaning |
|-----------|---------|---------|
| low_offset | 0.984 | Buy when 1.6% below MA |
| ewo_high | 3.206 | Must be in uptrend |
| ewo_low | -10.69 | Deep oversold threshold |
| rsi_buy | 63 | RSI must be below this |

---

## 7. Summary

**"Buy the dip when the trend is up, sell when it recovers or weakens. Five layers of protection keep you safe."**

Best for: Trend-following traders who understand technical analysis and accept moderate risk.

Remember: Backtesting ≠ future performance. Trade only what you can afford to lose.
