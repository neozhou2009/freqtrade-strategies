# NotAnotherSMAOffsetStrategyLite: Strategy Explained

## 1. What Does This Strategy Do?

### One-Line Summary

**"Buy falling prices in uptrends, sell when recovered."**

Simply: Wait for price to be below average, buy. When price recovers, sell. Only buy when the big trend is up.

Named "NotAnotherSMAOffsetStrategyLite" = simplified version of the MA offset strategy, keeping core logic while reducing complexity.

---

## 2. Core Logic

### When to Buy?

The strategy has THREE conditions — ALL must be met:

1. **Price cheap**: Price must be 2.5% below the average price (EMA × 0.975)
2. **Big trend up**: EWO > 0 (market's "fast line" above "slow line")
3. **Active trading**: Volume > 0 (not a dead market)

**Example**:
- BTC price $49,000
- EMA (14 candles) = $50,000
- Discount price = $50,000 × 0.975 = $48,750
- Current price $48,000 < $48,750 ✓
- EWO > 0 ✓
- Volume active ✓
- **BUY signal!**

### When to Sell?

EVEN simpler — only TWO conditions:

1. Price above EMA × 0.991
2. Volume > 0

**Example** (continuing):
- After buying at $48,000, price rose to $49,500
- Sell line = $50,000 × 0.991 = $49,550
- Current $49,500 < $49,550 → not yet
- Price rose to $49,600 > $49,550 ✓
- **SELL signal!**
- Profit: ($49,600 - $48,000) / $48,000 ≈ 3.3%

---

## 3. Indicators Explained

### EMA — "Average Price"

EMA (Exponential Moving Average) weights recent prices more heavily. Strategy uses:
- **Buy EMA**: 14 candles — faster, catches entry timing
- **Sell EMA**: 24 candles — slower, avoids early exits

### EWO — "Big Trend Direction"

EWO compares fast and slow EMAs. Positive = uptrend, Negative = downtrend.

Only buy when EWO > 0. Don't catch "falling knives."

### RSI — "Temperature"

Three RSIs for different purposes:
- **RSI 4**: Super fast — catches short-term oversold for entry
- **RSI 14**: Standard — overall state
- **RSI 20**: Slow — confirms long-term trend

---

## 4. Stop-Loss — The Safety Valve

### 4.1 Fixed Stop: 10% Max Loss

```python
stoploss = -0.1
```

Bought at $100 → drops to $90 → forced sell. 10% is relatively wide for 5-min trading, giving price room to fluctuate.

### 4.2 Dynamic Stop: Time-Based Tightening

```python
if holding > 12 hours AND loss > 5%:
    tighten stop to -1%
```

**Why?**: If still losing 5%+ after 12 hours, your judgment was likely wrong. Tighten the stop to cut losses faster.

---

## 5. Take-Profit

### 5.1 Fixed: 2.5% Minimum

```python
minimal_roi = {'0': 0.025}
```

Price rises 2.5%+ → eligible to sell.

### 5.2 Sell Only When Profitable

```python
sell_profit_only = True
sell_profit_offset = 0.01
```

Won't sell unless you're up 1%+. Prevents selling the moment you're slightly profitable.

---

## 6. Parameters

### Buy Parameters

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| base_nb_candles_buy | 14 | 5-80 | MA period; smaller = faster |
| low_offset | 0.975 | 0.9-0.99 | Discount required; smaller = bigger discount needed |

### Sell Parameters

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| base_nb_candles_sell | 24 | 5-80 | MA period; larger = more stable |
| high_offset | 0.991 | 0.95-1.1 | Price above MA to sell; smaller = sell earlier |

---

## 7. Pros & Cons

### Pros

1. **Simple logic**: Three conditions to buy, two to sell
2. **Follows trend**: Only buys in uptrends (EWO > 0)
3. **Buys at discount**: Waits for price below average
4. **Risk controlled**: Stop-loss + dynamic stop + take-profit
5. **Adjustable**: Four parameters can be tuned

### Cons

1. **Long only**: Can't profit from falling markets
2. **Ranging market struggles**: Back-and-forth = losses
3. **Parameter sensitive**: Different coins need different settings
4. **Misses big moves**: May sell early in powerful trends
5. **Needs tuning**: Not "set and forget"

---

## 8. Best Markets

| Market | Performance |
|--------|-------------|
| Bull with pullbacks | ★★★★★ |
| Ranging up/down | ★★★ |
| One-sided crash | ★ |
| Dead quiet | ★★ |

---

## 9. Summary

This strategy is **"buy the dip in an uptrend, sell when recovered, with stop-loss protection."** Simple but effective. Best suited for short-term traders in trending markets who want clear logic and are willing to tune parameters.

**Key rules**:
1. Backtest before going live
2. Start small
3. Check and adjust regularly
4. Control risk
5. Keep learning

**Most important**: No strategy is perfect. Trade only what you can afford to lose!
