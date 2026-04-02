# NotAnotherSMAOffsetStrategy_uzi: Strategy Explained

## 1. What Does This Strategy Do?

### One-Line Summary

**"Buy when price dips in an uptrend, sell when it recovers."** Like buying groceries on sale — you only buy when the price is below what you consider fair value, and you only sell when it's back to normal or above.

### Name Meaning

The name "NotAnotherSMAOffsetStrategy_uzi" means this isn't just another basic MA strategy — it has the "offset" innovation built in, and "_uzi" is just a version identifier.

---

## 2. Core Logic in Plain English

### When to Buy?

The strategy has **two buy conditions** — satisfy either one and it buys:

**Condition 1: ewo1 (Trend Pullback)**

Think of it like this: "The market's going up, but it just took a breather. Buy now!"

Requirements:
1. RSI(4) < 35 — short-term price dropped quickly
2. Price < EMA(14) × 0.975 — 2.5% below the average
3. EWO > 2.327 — big trend is still UP
4. RSI(14) < 69 — not overheated
5. Volume > 0

**Condition 2: ewolow (Extreme Oversold)**

Think of it like this: "Everyone's panicking and selling. Be greedy when others are fearful."

Requirements:
1. RSI(4) < 35 — short-term price dropped fast
2. Price < EMA(14) × 0.975 — 2.5% below average
3. EWO < -20.988 — market is deeply depressed
4. Volume > 0

---

## 3. When to Sell?

**Two sell conditions** — satisfy either one and it sells:

**Condition 1: Made Good Profit, Trend Still Up**

Think: "Price recovered nicely, momentum still healthy — lock in the gains!"

Requirements:
1. Price > SMA 9
2. Price > EMA(24) × 0.997
3. RSI > 50
4. Fast RSI > Slow RSI
5. Volume > 0

**Condition 2: Momentum Running Out**

Think: "Price shot up fast but now stalling — take the money before it drops more!"

Requirements:
1. SMA 9 rose sharply (quick surge)
2. Price < HMA 50
3. Price still above EMA baseline
4. Fast RSI > Slow RSI

---

## 4. Risk Control

### Stop-Loss: 7% Maximum

Bought at $100 → drops to $93 → forced sell. 7% is the final safety net.

### Trailing Stop: Smart Profit Locker

- Kicks in after **3% profit**
- Follows price upward at **0.5% below peak**
- Example: Bought $100 → $103 activates → $110 peak → $109.45 stop → sells at $109.45, locking in 9.45% profit

### Take-Profit Table

| Holding Time | Target |
|-------------|--------|
| Immediate | 21.5% |
| 40 min | 3.2% |
| 87 min | 1.6% |
| 201 min | Break-even |

### Only Sell When Profitable

Won't execute sell signals unless you're **up 0.5%+**. This prevents panic selling when you're slightly down.

---

## 5. Parameters

| Parameter | Default | What It Does |
|-----------|---------|--------------|
| low_offset | 0.975 | Buy when price is 2.5% below MA |
| ewo_high | 2.327 | Must be in uptrend (EWO positive) |
| ewo_low | -20.988 | Only for panic buys (EWO deeply negative) |
| rsi_buy | 69 | RSI must be below this to buy |
| high_offset | 0.991 | Sell when price is slightly above MA |

---

## 6. Best Markets

| Market | How It Performs |
|--------|----------------|
| Uptrend with pullbacks | ★★★★★ Great |
| Deep crash | ★★★★ Good for ewolow |
| Ranging (no direction) | ★★★ Okay |
| One-sided crash | ★★ Tricky |
| Dead quiet | ★ Boring |

---

## 7. Summary

**"Buy when price is below average in a confirmed uptrend, sell when it recovers or momentum fades. 7% stop-loss and smart trailing protect your capital."**

This strategy works best for:
- Trend-following traders
- Short-to-medium term holds
- People who understand technical indicators
- Those who can accept moderate drawdowns

**Key rules**:
1. Backtest first
2. Start small
3. Monitor and adjust
4. Trade only what you can afford to lose

Good luck!
