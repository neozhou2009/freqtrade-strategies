# Combined_NFIv7_SMA_Rallipanos_20210707 Strategy: 26-Path "Buy Master" + 8-Path "Sell Master"

> **Nickname**: Nostalgia For Infinity Rallipanos Version (July 7, 2021 Version)
> **Profession**: 5-Minute Trend Trader + 1-Hour Trend Confirmation
> **Timeframe**: 5 Minutes Main + 1 Hour Scout

---

## 1. What's This Strategy?

**Combined_NFIv7_SMA_Rallipanos_20210707** is the "NostalgiaForInfinity" (Hedge Infinity) Series' **7th Generation Variant**, born on July 7, 2021.

Simply put, this is a strategy **"armed to the teeth"**. How ridiculous? Let me count:
- **26 buy conditions** — like 26 weapons!
- **8 sell conditions** — like 8 escape routes
- **8 protection mechanisms** — like 8 layers of body armor
- Also uses **ZEMA** (Zero-Lag EMA)!

It feels like: you're driving and **the windshield shows 5 meters, the rearview mirror shows 500 meters**, seeing both near opportunities and future trends.

---

## 2. Core Settings: "Let Profits Run"

```python
minimal_roi = {"0": 0.10, "30": 0.05, "60": 0.02}
stoploss = -0.10
trailing_stop = True
trailing_stop_positive = 0.005
trailing_stop_positive_offset = 0.030
```

**Translation**: This strategy has big appetite — wants 10% the moment it enters. But as time passes, expectations drop. This is **let profits run** for real!

---

## 3. 26 Buy Conditions: Going to Heaven?

26 conditions — like 26 different weapons, different situations use different ones:

### 🗡️ Weapons 1-6: Early Capture Type (Strict Protection)
- Specialized in catching trend starts
- Uses strictest "dip protection" (levels 10-40)
- Suitable for catching "first wave up"

### 🗡️ Weapons 7-14: Momentum Acceleration Type
- Adds **EWO** (Elliott Wave Oscillator)
- Specialized in catching trend acceleration
- Suitable for "main waves"

### 🗡️ Weapons 15-24: Trend Pullback Type
- Emphasizes "long-term trend confirmation"
- Each buy checks the 200-day MA's "expression"
- Suitable for "following major trend, counter minor trend"

### 🗡️ Weapon 26: ZEMA Ultimate
- Uses zero-lag EMA
- Parameters can be optimized, more flexible
- Specialized in catching "can't fall further" opportunities

---

## 4. 8 Protection Layers: "Iron Bell"

This strategy dares to set 10% take-profit because it has **8 layers of protection**:

| Layer | Name | What It Checks |
|-------|------|---------------|
| 1 | EMA MA Protection | Fast EMA above 200 MA |
| 2 | SMA200 Trend Protection | 200-day MA rising |
| 3 | 1-Hour EMA Protection | Check trend with telescope |
| 4-14 | 11 Levels of "Dip Protection" (Safe Dips) | "Fear of heights" detector |
| 15-26 | 12 Levels of "Pump Protection" (Safe Pump) | "Fear of rises" detector |

---

## 5. Exit Logic: 8 "Gates of Death"

### 🚪 Gates 1-2: Overbought Signals
- RSI too high + touching Bollinger upper band → Run!

### 🚪 Gates 3-4: Momentum Divergence
- Price makes new high but RSI didn't → Run!

### 🚪 Gates 5-8: Smart Take-Profit

This is the famous **"12-Stepped Take-Profit"**:

| Profit | RSI Threshold | Explanation |
|--------|---------------|------------|
| 1% | 34 | Just made 1%? Fine, run |
| 5% | 43 | Made enough, go |
| 10% | 54 | Made a bundle, must go |
| 20% | 34 | Made too much, might pull back |

**Plain English**: The more you earn, the looser the conditions — this is **"let profits run"**!

---

## 6. Strategy "Personality Traits"

This strategy is a **"Old Fox"**:

| Trait | Behavior |
|-------|---------|
| 🦊 Cautious | 26 conditions, won't act without certainty |
| 🦊 Patient | 10% take-profit target, waits for major trends |
| 🦊 Decisive | Once 10% stop-loss hit, cuts without hesitation |
| 🦊 Greedy | Trailing stop keeps letting profits run, unsatisfied until 20% |

---

## 7. When to Use It?

### ✅ Best Scenarios
1. **Early Bull Market**: Trend just started, 10% take-profit easily triggered
2. **Mainstream Coins**: BTC, ETH with moderate volatility and trends
3. **Portfolio**: Pairs with other strategies to form a "strategy fleet"

### ❌ Terrible Scenarios
1. **Sideways Volatility**: Gets slapped up and down repeatedly
2. **Small Coins**: Too volatile, 10% stop-loss not enough
3. **Bear Market**: Trend down, buy one get trapped one

---

## 8. Summary

**Combined_NFIv7_SMA_Rallipanos_20210707** is an **"Old Fox Type"** strategy:

- **26 weapons** — whichever fits the current market, use it
- **8 layers protection** — security guaranteed
- **12-Stepped Take-Profit** — let profits run to the max
- **Dual Timeframe** — more reliable signals

Suitable for **experienced traders willing to invest time managing**.

---

## 9. Market Performance

| Market Environment | Expected Performance | Notes |
|-------------------|---------------------|-------|
| Bull Market | ⭐⭐⭐⭐⭐ | Take-profit easily triggered |
| Bear Market | ⭐⭐☆☆☆ | Need strict risk control |
| Volatile | ⭐⭐⭐☆☆ | Pair with other strategies |

---

## 10. ⚠️ Risk Re-Emphasis

### ⚠️⚠️⚠️ Most Important Three Things:

1. **This strategy will lose money**
2. **10% stop-loss is no joke** — 10 consecutive stops shrinks account 65%!
3. **Complex strategies need more attention** — parameters easily overfit

**Remember**: Test with small positions — survival is what matters! 🙏

---

**Wishing everyone profitable trades and making money hand over fist!** 🚀
