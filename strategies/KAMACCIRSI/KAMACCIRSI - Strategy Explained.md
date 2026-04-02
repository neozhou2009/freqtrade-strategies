# KAMACCIRSI Strategy Explained — The "Three-Indicator Combo" Trend Chaser

## 1. What Does This Strategy Do?

Simply put, **KAMACCIRSI is a momentum-chasing strategy.**

Its name strings together three indicators:
- **KAMA** = Kaufman Adaptive Moving Average
- **CCI** = Commodity Channel Index
- **RSI** = Relative Strength Index

Author werkkrew is very direct: "This strategy has nothing groundbreaking—it's just what I wrote while learning the Freqtrade framework." But exactly because of this, it's great for beginners—clean code, clear logic, all parameters adjustable.

**Core idea**: wait for trend to be clearly established, confirm it's genuinely going to rise, then buy. Not bottom-fishing—chasing momentum. Take profit when enough, cut losses when deep.

---

## 2. How Do the Three Indicators Work Together?

Imagine driving:

- **KAMA** is like your **GPS navigation** — tells you the big direction
- **CCI** is like your **gas gauge** — tells you if there's momentum
- **RSI** is like your **speedometer** — tells you if you're going too fast

Strategy uses KAMA and CCI by default, RSI is turned off. Why? Because after extensive backtesting, RSI actually interfered with signals in this combination.

Buy and sell each have their own parameters:
- Buy has buy settings
- Sell has sell settings

This is called "asymmetric design" — enter cautiously, exit decisively.

---

## 3. What Is KAMA?

KAMA stands for "Kaufman Adaptive Moving Average." Sounds complex but the principle is simple.

### Problem with Regular Moving Averages

Moving averages have a dilemma:
- **Short period**: Fast response but lots of noise, gives many false signals
- **Long period**: Less noise but slow to respond, by the time it signals the opportunity is gone

### KAMA's Smart Feature

KAMA judges market conditions:
- **Market trending up or down**: KAMA becomes sensitive, follows price closely
- **Market oscillating**: KAMA becomes sluggish, filters noise

Like a "smart operator" moving average—trends come it follows closely, oscillation comes it ignores.

### How Strategy Uses KAMA

Strategy uses two KAMAs:
- **Short KAMA (period 11)**: Fast, follows price closely
- **Long KAMA (period 46)**: Steady, represents the big trend

When short KAMA crosses above long KAMA → price going up!
When short KAMA crosses below long KAMA → price going down!

Like you and a friend running: you (short KAMA) pass your friend (long KAMA) → you're in good shape; you get passed → you're losing steam.

---

## 4. What Is CCI?

CCI stands for "Commodity Channel Index"—measures how much price deviates from its average.

### Simple Explanation

Say something normally costs $100:
- Suddenly rises to $120, CCI might be +150 → risen too much
- Drops to $80, CCI might be -150 → fallen too much
- Oscillates between $95-105, CCI near 0 → normal

### How Strategy Uses CCI

Strategy's usage is **very special**:

- **Buy condition**: CCI > 198

Traditional thinking: CCI > 100 is "overbought" (risen too much), should sell. But this strategy requires CCI > 198 to buy!

What's the logic?

**This is a momentum-chasing strategy!** Author believes: when CCI has risen to 198, market momentum is extremely strong — if this strong, there's probably more room to go, let's chase!

Like going to a concert — the entrance is packed (CCI very high), you actually want to go in even more because it shows the show is great.

---

## 5. RSI Everyone Knows

RSI = "Relative Strength Index" — old traders know this well:

- **RSI > 70**: Overbought, might drop
- **RSI < 30**: Oversold, might bounce

### How Strategy Uses RSI

Strategy's RSI is **turned off by default**!

Author found through extensive testing that RSI actually hurt results in this strategy combination, so it was disabled.

Parameters are ready if you want to enable:
- Buy: RSI > 72 confirms
- Sell: RSI < 69 confirms

This is the opposite of traditional usage — traditional is RSI > 70 sell, this is RSI > 72 buy. Momentum chasing again.

---

## 6. When to Buy?

Combine the above:

### Default Buy Conditions

1. **Short KAMA crosses above long KAMA** (this is the main signal)
2. **CCI > 198** (this is the confirmation signal, must have)
3. **Volume > 0** (can't be empty volume)

RSI condition is off by default, ignore it.

### Example

Watching ETH 5-minute chart:

| Time | Short KAMA | Long KAMA | CCI | Result |
|------|-----------|-----------|-----|--------|
| 9:00 | 2000 | 2010 | 120 | No signal (KAMA not crossed) |
| 9:05 | 2015 | 2010 | 150 | No signal (crossed but CCI insufficient) |
| 9:10 | 2025 | 2010 | 210 | **BUY!** |

See 9:10: short KAMA (2025) has crossed above long KAMA (2010), AND CCI reached 210, exceeding the 198 threshold. All three conditions met — open position!

### Why So Strict?

Three indicators together就是为了 (are for the purpose of) **fewer mistakes**.

- KAMA crossed but CCI insufficient? Probably false breakout, don't enter.
- CCI high but KAMA not crossed? Probably just a spike, don't enter.
- All met then enter —宁可错过，不可做错 (rather miss it than do it wrong).

---

## 7. When to Sell?

Sell logic mirrors buy but with different parameters.

### Default Sell Conditions

1. **Short KAMA crosses below long KAMA** (note: uses another set of parameters)
2. **CCI < -144** (this is off by default, so actually not checked)
3. **Volume > 0**
4. **Must have >1% profit** to respond to sell signals

Notice: **buy and sell use SEPARATE parameters!**

### Buy vs. Sell Parameter Comparison

| Parameter | Buy Uses | Sell Uses | Difference |
|-----------|----------|-----------|------------|
| Short KAMA period | 11 | 5 | Sell more sensitive |
| Long KAMA period | 46 | 41 | Sell more sensitive |
| CCI enabled | On | Off | Only for buy confirmation |
| CCI threshold | 198 | -144 | One positive one negative |
| RSI enabled | Off | Off | Neither uses |

Notice it?
**Buy cautious, sell decisive.**

- Buy uses 11-period KAMA, slower response, wait for confirmation before entering
- Sell uses 5-period KAMA, faster response, when things look bad, run fast

---

## 8. What If You Lose? Stop Loss Settings

Strategy sets three layers of protection:

### Layer 1: Fixed Stop Loss

```
Stop loss = -33%
```

Meaning: force close when loss reaches 33%.

33% sounds like a lot? In crypto this is not unusual. Crypto swings 10-20% in a day are normal. Stop too tight and you'd get washed out by normal movements.

### Layer 2: ROI Time Stop

A "schedule":

| Holding Time | Minimum Profit Target |
|-------------|---------------------|
| Just bought | 11.6% |
| After 18 hours | 3.1% |
| After 34 hours | 1.9% |
| After 131 hours | any profit |

What does this mean?

Just bought, goal is 11.6%+. If price rose 8% and hasn't been held 18 hours yet, don't sell, keep waiting.

But if held 131 hours (~5 days), even just a tiny profit is okay to take. Time换空间 (exchanges time for space) — give it time to make big profits, but if it's been too long, take whatever you can get.

This prevents **long-term holding getting trapped** — if it's not going up, get out and find the next opportunity.

### Layer 3: Must Be Profitable to Sell

Setting `sell_profit_only = True`

With `sell_profit_offset = 0.01`, meaning:

Only when profit exceeds 1% will the strategy respond to KAMA's sell signal.

If you just bought and it's going down, KAMA gives sell signal, strategy says "don't sell, still not profitable." This prevents getting washed out.

---

## 9. How to Protect Profits? Trailing Stop

This is the cleverest part — **trailing stop**.

### What Is Trailing Stop?

Regular stop loss is fixed: lose 10% and run.

Trailing stop moves: price goes up, stop line follows up; price goes down, stop line doesn't move down.

### Strategy Settings

```
Trailing stop activation threshold: 29.77% profit
Trailing stop distance: 28.6% from peak
```

### Example

You buy at $100:
1. Price rises to $120 (+20%) — trailing not activated yet, keep holding
2. Price rises to $130 (+30%) — activated! Stop line set at 130 × (1 - 28.6%) ≈ $93
3. Price continues to $150 — stop line follows to 150 × 0.714 ≈ $107
4. Price pulls back to $107 — triggers stop, locked in ~7% profit
5. If price continues to $200 — stop line at $143, locked in 43% profit

**Core idea**: let profits充分奔跑 (run fully), but once they retrace too far from the peak, quickly lock in what you have.

---

## 10. How Long to Hold? ROI Table

Besides the above stop mechanisms, there's also the ROI table controlling sell timing.

Looking at the ROI table:

| Holding Duration | Target Return |
|----------------|--------------|
| 0 hours | 11.6% |
| 18 hours | 3.1% |
| 34 hours | 1.9% |
| 131 hours | 0% |

Operation:
- **Just bought**: want 11.6%+ profit, don't hit target yet, keep holding
- **18 hours held**: target drops to 3.1%, if it's there, sell
- **34 hours held**: target drops to 1.9%
- **131 hours held**: if even 0.1% profit, take it, don't wait

This is time换空间: give it time to make big money fast, but if time passes without results, lower expectations and get out to find the next trade.

---

## 11. Who Is This Strategy For?

### Good For

1. **Beginners learning**: Code structure is clear, parameters all commented, great for learning Freqtrade strategy development
2. **Trend traders**: Like chasing, not bottom-fishing
3. **Crypto players**: Default parameters optimized for crypto
4. **Short-term traders**: 5-minute period, suitable for intraday or short swings

### Not For

1. **Bottom fishers**: This strategy chases momentum, bottom-fishing is not its style
2. **Ranging market traders**: Moving average crosses get slapped around in sideways markets
3. **Long-term investors**: 5 minutes is way too short

### Good Coins

Recommended:
- BTC, ETH and other mainstream coins — liquidity good, trends relatively clear
- High-cap altcoins — won't be easily manipulated by a few big players

Not recommended:
- New coins — insufficient history
- Small caps — poor liquidity, big slippage
- Stablecoin pairs — no volatility, nothing to trade

---

## 12. What Pitfalls to Watch?

### Pitfall 1: Ranging Markets

This is the death of all moving average strategies.

When price oscillates, short KAMA and long KAMA cross repeatedly — buy, sell, buy, sell, getting slapped over and over, paying fees on each.

**Solution**: Add a trend filter, like checking if the larger timeframe's moving average is also pointing up.

### Pitfall 2: Black Swan

33% stop loss is wide. In extreme situations it might get penetrated.

**Solution**: Don't go all-in. Control position size per trade.

### Pitfall 3: Parameter Overfitting

Author says default parameters optimized using Kraken 60 days + 20 BTC pairs.

Switch to a different exchange, different time period, parameters might not work.

**Solution**: Use Hyperopt to re-optimize with your own data.

### Pitfall 4: Only One Timeframe

Strategy only looks at 5-minute chart, no higher timeframe confirmation.

**Solution**: Add your own filter — like requiring the 1-hour KAMA also pointing up.

---

## 13. How to Make Money With It?

### Step 1: Understand the Logic

First understand this strategy's core: **chase momentum, don't bottom-fish, follow the trend**.

If you're a value investor who likes buying dips, this strategy isn't for you.

### Step 2: Choose the Right Pairs

Not every coin suits every strategy.

Backtest and find coins it works well on. Generally:
- Strong trending coins work well
- Wild oscillating coins don't

### Step 3: Optimize Parameters

Default parameters might not suit your market.

Run Hyperopt:

```bash
freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss \
    --strategy KAMACCIRSI \
    --epochs 500 \
    --spaces buy sell roi stoploss trailing
```

### Step 4: Small Account Test

Don't go all-in from the start.

Start with small money, run a few days, see:
- Any slippage issues in actual fills?
- Signal frequency normal?
- Profit/loss ratio as expected?

### Step 5: Continuous Monitoring

Strategies need regular check-ins.

Periodically check:
- Is drawdown too large?
- Has market environment changed?
- Do parameters need adjustment?

### Key Points Summary

1. **Momentum-chasing strategy**, not bottom-fishing
2. **Three indicators** combined, but defaults only use KAMA and CCI
3. **Buy and sell use separate parameters** — buy cautious, sell decisive
4. **Triple protection**: fixed stop, trailing stop, ROI time table
5. **5-minute period**, suitable for short-term
6. **Needs parameter optimization** — default may not suit your market

---

## Final Words

This strategy's value isn't in how much money it makes, but in being a **complete, clear, learnable template**.

If you're a Freqtrade beginner, this strategy can teach you:
- How to organize parameters
- How to write buy/sell conditions
- How to configure stop loss and trailing stop
- How to make parameters support Hyperopt optimization

Master this and you'll have a framework for writing your own strategies!

**Strategy source**: werkkrew
**GitHub**: https://github.com/werkkrew/freqtrade-strategies

---

*This document is for learning and exchange only. Quantitative trading has risks; trade carefully.*
