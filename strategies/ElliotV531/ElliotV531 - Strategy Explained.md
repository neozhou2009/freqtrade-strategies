# ElliotV531: Plain and Simple

## 1. What's This Strategy?

ElliotV531 is an automated crypto trading strategy. Its core idea: "buy when the price pulls back, sell when it's risen."

The "Elliot" in the name comes from Elliott Wave Theory — proposed by Ralph Nelson Elliott in the 1930s. He noticed prices move in waves, like ocean tides — with impulse waves (main trends) and correction waves (pullbacks). This strategy uses math to identify these "waves" and find good entry and exit timing.

The strategy runs on 5-minute candlesticks, good for short-term and intraday traders. If you're the type who likes quick in-and-out trades, this might be your thing.

## 2. Three Key Indicators

The strategy uses three main indicators like three judges — all must agree before the strategy acts.

### The First: EMA (Moving Average)

EMA weights recent prices more heavily, reacting faster. The strategy uses:
- 11-period EMA to judge buy timing
- 17-period EMA to judge sell timing

When price is below EMA, it's relatively "cheap" — a potential buy. Think of it like spotting a discount at a store.

### The Second: EWO Oscillator (Most Important!)

EWO measures how much short-term trend differs from long-term trend:

```
EWO = (Short EMA - Long EMA) / Current Price × 100
```

- EWO positive: Short-term trend is stronger — possibly in an uptrend
- EWO negative: Short-term trend is weaker — possibly in a downtrend

Strategy sets two key thresholds:
- ewo_high = 2.337: When exceeded, short-term momentum is strong, trend continues
- ewo_low = -15.87: When below, short-term momentum is extremely weak (oversold), bounce likely

### The Third: RSI

RSI (0-100) tells if market is "too hot" or "too cold":
- Above 70: Overbought, might drop
- Below 30: Oversold, might bounce

Strategy requires RSI < 55 for buys — not trying to catch the absolute bottom, just wanting some upside room.

## 3. When to Buy? Two Scenarios

Two different buy situations, like having two fishing nets for different fishing spots.

### Scenario 1: Buy the Pullback (Higher Win Rate)

Conditions:
- Price < EMA × 0.979 (about 2% below average)
- EWO > 2.337 (short-term momentum still strong)
- RSI < 55 (not overheated)
- Volume > 0

Think of it: your favorite coin has been climbing from $50,000 to $55,000, great trend. Suddenly it pulls back to $53,900 (about 2% off). EWO is still positive (like 3.5), RSI around 50, not overbought. Strategy says: "Great pullback opportunity!" and buys.

This succeeds more often because you're riding the trend, like surfing — waiting for the wave, then riding it.

### Scenario 2: Bottom-Catch the Rebound (Higher Risk, Higher Potential)

Conditions:
- Price < EMA × 0.979
- EWO < -15.87 (seriously oversold!)
- Volume > 0

Think of it: your coin crashes from $50,000 to $42,000, everyone panicking. EWO drops to -18, extreme. Strategy might buy here, betting on a bounce.

No RSI check here because when EWO is this low, RSI is definitely already low too. Adding conditions would just filter out valid opportunities.

**Comparison:**

| | Scenario 1 (Pullback) | Scenario 2 (Bottom-Catch) |
|---|---------------------|------------------------|
| Market | Uptrend | Downtrend |
| Risk | Lower | Higher |
| Expected return | Trend continuation | Technical bounce |
| Holding time | Possibly shorter | Possibly longer |
| Win rate | Higher | Lower |
| Profit/loss ratio | Medium | Possibly higher |

## 4. When to Sell?

Exit conditions are simpler:
- Price > EMA × 0.997
- Volume > 0

There's also a "confirm exit" mechanism that checks if the trend is still strong — if HMA(50) is well above EMA(100) and price just dipped slightly below EMA(100), it might hold off on selling to let profits run.

**Slippage protection:**
```python
slippage_protection = {'retries': 3, 'max_slippage': -0.05}
```

If actual price differs from expected by more than 5%, the strategy skips and retries up to 3 times.

## 5. Four Layers of Stop-Loss Protection

Like an onion, layer after layer.

### Layer 1: Fixed Stop-Loss — 18.9%

```python
stoploss = -0.189
```

Basic protection. If price drops 18.9%, auto-sell. Why 18.9%? Looks random but was optimized. Crypto swings 10%+ in a day are normal, so this isn't too tight.

### Layer 2: Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.007     # 0.7%
trailing_stop_positive_offset = 0.0157  # 1.57%
```

When profit exceeds 1.57%, trailing stop activates. Then it follows price upward, staying 0.7% below peak. If price retraces, it locks in profits.

Example: Buy at $100, price climbs to $101.57 (1.57% profit) → activates. Climbs to $105, stop moves to $104.27. Price drops to $104 → sells, locks in ~4% profit.

### Layer 3: Custom Stop-Loss

```python
if current_profit > 0:
    return 0.99  # Almost immediate trigger
```

When profitable, the stop gets very tight (99% of current price). If you've made money and price even dips slightly, it sells and locks profits.

**For zombie positions:**
```python
if holding > 241 minutes AND price < entry × 0.985:
    return 0.01  # Tight stop, exit
```

Held too long (4+ hours) still losing? If price is 1.5% below entry, sell and move on. Don't keep holding forever.

### Layer 4: ROI Targets

```python
minimal_roi = {
    "0": 0.215,    # 21.5% ASAP
    "40": 0.132,   # 13.2% after 40 min
    "87": 0.086,   # 8.6% after 87 min
    "201": 0.03    # 3% after 201 min
}
```

In short: "Make big money early if possible. But the longer you wait, the lower your target. After 201 minutes, just don't lose money."

## 6. Timeframe

**Main: 5 minutes** — for buy/sell decisions, all indicators calculated here.

**Auxiliary: 30 minutes** — for judging the big trend direction.

Why both? 5 minutes alone gets fooled by noise (a big order can temporarily crush price but trend unchanged). 30 minutes alone is too slow (by the time it signals, price already moved a lot).

Use 30 minutes to see the big picture, 5 minutes to find the entry point — precise AND stable.

**startup_candle_count = 200**: Needs 200 candles (about 16-17 hours of 5-minute data) before indicators are ready.

## 7. Parameters

| Parameter | Default | Range | Role |
|-----------|---------|-------|------|
| base_nb_candles_buy | 11 | 5-80 | Buy EMA period |
| ewo_high | 2.337 | 2-12 | EWO high threshold |
| ewo_low | -15.87 | -20 to -8 | EWO low threshold |
| low_offset | 0.979 | 0.9-0.99 | Buy discount |
| rsi_buy | 55 | 30-70 | RSI buy limit |
| base_nb_candles_sell | 17 | 5-80 | Sell EMA period |
| high_offset | 0.997 | 0.99-1.1 | Sell premium |

**Conservative settings**: Raise ewo_high (4-5), lower ewo_low (-18 to -20), lower rsi_buy (40-45).

**Aggressive settings**: Lower ewo_high (2-3), raise ewo_low (-10 to -12), raise rsi_buy (60-65).

## 8. What Coins?

**Good:** BTC/USDT, ETH/USDT, SOL, BNB, AVAX — liquid, moderate volatility, predictable patterns.

**Bad:** Newly listed coins (abnormal volatility), tiny coins under $1M daily volume (slippage eats profits), extreme volatility (stop-loss gets triggered constantly).

## 9. Risks

**1. Stop-loss might get hit then reverse**
Sometimes price drops to trigger 18.9% stop, then bounces. You sold at the bottom, then watch it recover. Frustrating. But if you hadn't stopped, it might have dropped to 60. Stop-loss protects against worse.

**2. Bottom-catching might catch mid-fall**
Scenario 2 buys in a downtrend, betting on a bounce. If the downtrend continues, you buy, then it drops more.

**3. High-frequency fees add up**
5-minute framework can produce lots of trades. At 5 trades/day × 0.2% fees (buy+sell) × 365 days = 365% annual fees! Use low-fee exchanges.

**4. Slippage risk**
In thin markets, fill prices differ from expected. The strategy has protection, but can't eliminate it entirely.

**5. Parameter overfitting**
Parameters tuned to historical data might only work on past markets, not future ones.

## 10. How to Use

1. **Backtest first!** Use historical data: `freqtrade backtesting --strategy ElliotV531 --timerange 20230101-20231231`
2. **Simulated trading** (dry-run) for 1-2 weeks
3. **Small-capital live** (10-20% of funds) for a month
4. **Gradual scale-up** if performing well
5. **Weekly/monthly check-ins** — watch performance, adjust if needed

## 11. Summary

ElliotV531 is a mature short-term trading strategy:

**Strengths:**
- High-quality signals (price + momentum + volume triple confirmation)
- Great risk control (4 layers of stop-loss protection)
- Flexible parameters (tunable for different markets)
- Dual timeframes (5-min decisions + 30-min trend confirmation)

**Good for:**
- Experienced traders who understand technical indicators
- Those who can handle moderate risk
- People with time to monitor or automate with programs

**Not for:**
- Complete beginners unfamiliar with technical analysis
- Those seeking steady returns without any volatility
- People without time to monitor markets
- Those unwilling to use programmatic trading

**Key rule:** Risk control comes first, always. This strategy's risk design is solid, but ultimately, how well it works depends on how YOU use it.

---

*Disclaimer: For learning reference only, not investment advice. Crypto trading is high-risk — invest cautiously!*
