# Divergences Strategy: Plain English Edition

## 1. What Does This Strategy Do?

Today we're talking about Divergences — a trading strategy with an intimidating name but a surprisingly simple principle: **catching moments when "price deceives you."**

What does "price deceives you" mean? Example: a coin keeps rising, rising, rising... but its "momentum" is actually shrinking. Like someone still running forward but obviously running out of steam — they'll stop soon. That's when we prepare to go short.

Conversely: price keeps falling but downward momentum is getting weaker — a bounce is coming. That's when we prepare to bottom-fish.

This strategy uses computer programs to automatically spot these "momentum changed" moments and catch reversal opportunities for us!

---

## 2. What the Heck IS Divergence?

Picture someone climbing stairs:
- **Normal**: Climb one floor, get tired; climb another, get more tired. Effort and height are "in sync."
- **Divergence**: Still climbing but getting easier, or getting more tired but still climbing. Effort and performance are "not in sync."

In crypto terms:
- **Normal uptrend**: Price rises + RSI rises = momentum sufficient, will keep rising
- **Diverging uptrend**: Price still rising + RSI no longer rising = momentum weakening, might fall

When price makes a new low but RSI doesn't make a new low, sellers' momentum is exhausted. Buyers might counterattack. That's our entry signal!

---

## 3. How Does the Strategy Work?

### Step 1: Watch Price Patterns

The strategy uses 5 candles to identify where the "bottom" is.

**Bullish Pattern (finding bottom)**:
```
      - 
  - -   - -
  4 3 2 1 0
```
Candle position 2 is the lowest point — lower than both sides, and the earlier candle (4) is higher than this bottom. Price fell and bounced.

### Step 2: Check RSI

RSI is like a fitness meter (0-100):
- Above 70: too overheated, might drop
- Below 30: too oversold, might bounce

Strategy uses threshold of 40 (slightly more relaxed than 30) to catch more opportunities.

**Buy**: RSI ≤ 40 AND bullish pattern = open long!

### Step 3: When to Sell?

Sell condition is simple: see bearish pattern, sell.

But with protection: only sell when profitable! If still losing money, even seeing bearish pattern won't sell. Why? Because it's heartbreaking to sell at a loss!

---

## 4. Stoploss: Three Lines of Defense

### First Line: Fixed Stoploss at 10%

Loss reaches 10% → auto-sell and admit defeat. This is relatively generous in crypto, giving price room to fluctuate.

### Second Line: Trailing Stop

This is the strategy's essence! The stop level follows profits upward but never downward.

Example:
- Buy at $100
- Price rises to $120 (20% profit) → trailing stop activates!
- Price climbs to $150 → stop moves to $142.5
- Price climbs to $200 → stop moves to $190
- Price drops to $190 → triggered, sell, locks in 90% profit!

Without trailing stop, price climbs to $200 then drops to $90, you'd make nothing.

### Third Line: Profit Protection

`sell_profit_only = True` — only sell when profitable. Prevents getting shaken out by small fluctuations at a loss.

---

## 5. What Markets Suit This?

**Best for: Ranging markets**
Price bouncing up and down without a clear trend. Divergence strategy is most effective here — buy at bottoms, sell at tops, eat the swings.

**Not good for: One-directional暴涨暴跌 (extreme spikes/crashes)**
Like a coin jumping 50% in one day — momentum too strong, divergence signals fail.

**Best scenarios**:
- Major coins (BTC, ETH)
- 1-hour timeframe
- Moderate volatility, not extreme markets

---

## 6. What Indicators Does It Use?

**Core**: RSI (most important!), MACD (auxiliary)
**Auxiliary**: Bollinger Bands, EMA (7 of them!), CCI, SAR

The strategy's buy/sell signals mainly rely on RSI and price patterns — everything else is "for reference only."

---

## 7. Summary

Divergences is a simple but effective trend reversal strategy. It uses the most classic divergence principle — when price action and momentum indicator are inconsistent, a reversal often follows — to catch trading opportunities.

**Core logic in three sentences**:
1. Price makes new low but RSI doesn't = buy
2. Price makes new high but RSI doesn't = sell
3. Use trailing stop to protect profits

**Best for**: People with some technical analysis foundation, who want to profit from ranging markets and trend turning points, who don't want to chase momentum or catch falling knives.

**Caution**: Don't use in one-directional extreme markets. Backtesting and paper trading required. Start with small positions, scale up gradually. Keep learning and improving.

This strategy's greatest value: it implements decades-old classic theory in code, so you don't need to watch charts all day — the computer finds opportunities for you automatically!

---

*Plain English disclaimer: This document explains the Divergences strategy in simple terms. For learning reference only, not investment advice. Trading involves risk — invest carefully!*
