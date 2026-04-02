# NotAnotherSMAOffsetStrategyModHO: Strategy Explained

## 1. What Does This Strategy Do?

### One-Line Summary

**"Buy cheap when trend is up, sell when trend weakens."** Think of it like supermarket shopping — only buy when the price is below the average, and only sell when the price rises above average.

### Name Meaning

**NotAnotherSMAOffsetStrategyModHO** broken down:
- "NotAnother": Not just another ordinary strategy
- "SMA": Moving average (but uses EMA)
- "Offset": Price must deviate from MA by a percentage
- "ModHO": Modified + Hull Optimization

---

## 2. Core Logic in Plain English

### The Strategy's Approach

Imagine you're at a supermarket. The strategy:

1. **Finds the "fair price"** — using EMA
2. **Waits for discounts** — price must be at least 1.6% below fair price (offset 0.984)
3. **Checks the "trend direction"** — using EWO
4. **Buys** when conditions are met
5. **Sells** when price is above fair price and trend weakens

---

## 3. When to Buy? Two Signals

### Signal 1: "Buy the Dip" (ewo1)

**When**: Uptrend still intact, but price pulled back.

**Conditions**:
1. Fast RSI < 35: Short-term oversold
2. Price < EMA × 0.984: 1.6% below average
3. EWO > 3.206: Strong upward momentum
4. RSI(14) < 63: Not overheated
5. Volume > 0
6. Price not too high vs sell line

**Example**: BTC climbing steadily from $50k to $55k, suddenly drops to $54k. Strategy buys the dip.

### Signal 2: "Bottom-Fish" (ewo2)

**When**: Price crashed hard, EWO deeply negative.

**Conditions**:
1. Fast RSI < 35
2. Price < EMA × 0.984: 1.6% below average
3. EWO < -10.69: Very bearish
4. Volume > 0
5. Price below sell line

**Example**: BTC crashed from $55k to $45k. Strategy catches the bottom.

---

## 4. When to Sell? Two Conditions

### Condition 1: Profit Target Hit

**When**: Price rose and momentum still strong.

**Conditions**:
1. Price > SMA 9
2. Price > sell EMA × 1.0: Above baseline
3. RSI > 50: Still bullish
4. Fast RSI > Slow RSI
5. Volume > 0

**Plain English**: Made money, trend still healthy, time to take profit.

### Condition 2: Trend Weakening

**When**: Price dropped but still above baseline.

**Conditions**:
1. Price < HMA 50: Broke below mid-term trend
2. Price > sell EMA × 1.002: Still above baseline
3. Fast RSI > Slow RSI

**Plain English**: Trend may change, still profitable — take the money.

---

## 5. Risk Control — Three Layers

### Layer 1: Stop-Loss (32% Max)

Bought at $100 → drops to $68 → forced sell.

### Layer 2: Trailing Stop

Activates at 3% profit. Stops follow price up at 0.75% below peak.

### Layer 3: Take-Profit Target (21.4%)

Goal is 21.4% profit. If buy signal still active, may hold longer.

---

## 6. Parameters Summary

| Parameter | Default | Meaning |
|-----------|---------|---------|
| low_offset | 0.984 | Buy when 1.6% below MA |
| ewo_high | 3.206 | Must be in uptrend to buy |
| ewo_low | -10.69 | Bottom-fish threshold |
| high_offset | 1.002 | Sell when slightly above MA |

---

## 7. Pros & Cons

**Pros**: Clear logic, risk controlled, multiple signals
**Cons**: Wide 32% stop-loss, needs parameter tuning, no shorting

---

## 8. Summary

**"Buy when price is cheap in an uptrend, sell when price recovers or trend weakens. Three layers of risk protection."**

Best for: Trend-following traders who understand indicators and accept moderate risk.
