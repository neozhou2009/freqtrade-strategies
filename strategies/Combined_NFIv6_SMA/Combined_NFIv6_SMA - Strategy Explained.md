# Combined_NFIv6_SMA Strategy: 24-Path "Buy Master" + 8-Layer "Body Armor"

> **Nickname**: Nostalgia For Infinity SMA Version
> **Profession**: 5-Minute Trend Hunter + 1-Hour Telescope Scout
> **Timeframe**: 5 Minutes Main + 1 Hour Trend Confirmation

---

## 1. What's This Strategy?

**Combined_NFIv6_SMA** is the "NostalgiaForInfinity" (Hedge Infinity) Series' **6th Generation SMA-Enhanced Version**.

Simply put, this is an strategy **"armed to the teeth"**:

- **24 buy conditions** — like 24 weapons, one is always a hit
- **8 sell conditions** — like 8 escape routes
- **8 protection mechanisms** — like wearing 8 layers of body armor
- **Dual timeframe** — enter on 5 minutes, see direction on 1 hour

It feels like: you're driving and **the windshield shows 5 meters, the rearview mirror shows 500 meters** — you see both near opportunities and future trends.

---

## 2. Core Settings: "Let Profits Run"

### Take-Profit Rules (ROI Table)

```python
minimal_roi = {
    "0": 0.10,      # Make 10% immediately? Run!
    "30": 0.05,     # After 30 minutes, 5%? Run
    "60": 0.02,     # After 60 minutes, 2%? Run
}
```

**Translation**: This strategy has big appetite! Wants to make 10% the moment it enters — the "big fish big meat" type. But as time passes, its expectations drop — 5% is fine after 30 minutes, 2% satisfies after an hour.

### Stop-Loss Rules

```python
stoploss = -0.10  # Cut at 10% loss
```

**Translation**: You're allowed to lose 10%, but once you hit it, the trade is dead — run!

### Trailing Stop Rules

```python
trailing_stop = True
trailing_stop_positive = 0.005      # Starts observing at 0.5% profit
trailing_stop_positive_offset = 0.035  # Must rise to 3.5% before "providing protection"
trailing_only_offset_is_reached = True
```

**Translation**: At 0.5% profit, trailing stop just "looks." Only rises to 3.5% does it start working seriously. Then if it drops 0.5% from the high, immediately run.

Plain English: **Let the bullet fly, when it reaches 3.5% start providing protection!**

---

## 3. 24 Buy Conditions: Let Me Sort Them Out

This strategy's buy conditions are ridiculously many. I've grouped them into 6 categories:

### 🎯 Category 1: RSI/MFI Oversold Rebound (Conditions 1, 2)

**Core Logic**: RSI and MFI both oversold — clearly can't fall further!

**Plain English**:
> "Price has fallen to the point even relatives don't recognize it — time to rebound!"

---

### 🎯 Category 2: Bollinger Band Rebound (Conditions 3, 4)

**Core Logic**: Price touches Bollinger lower band, ready to bounce back

**Plain English**:
> "Bollinger Band has squeezed together — next it's fireworks!"

---

### 🎯 Category 3: EMA Golden Cross (Conditions 5, 6, 7)

**Core Logic**: EMA12 crosses above EMA26, short-term MA is taking over!

**Plain English**:
> "MA golden cross! Plus price is cheap — this won't lose!"

---

### 🎯 Category 4: RSI Extreme Oversold (Conditions 8, 18, 19, 20, 21)

**Core Logic**: RSI extremely low — clearly oversold!

**Plain English**:
> "Dropped this much and still someone buying? Must be a scheme! No wait, opportunity!"

---

### 🎯 Category 5: MA Offset (Conditions 9, 10, 11, 14, 15, 16, 22)

**Core Logic**: Price deviated too far from MA — time to revert!

**Plain English**:
> "Price deviated too far from the MA like a rubber band — time to snap back!"

---

### 🎯 Category 6: EWO Momentum Reversal (Conditions 12, 13, 16, 17, 22, 23)

**Core Logic**: EWO is a magical indicator, specialized in catching momentum reversals!

**Plain English**:
> "EWO says there's momentum reversal, let me try!"

---

## 4. 8 Protection Mechanisms: Hard to Lose Money

Each buy condition has a protection parameter set — like **8 layers of body armor**:

| Protection Type | Effect | Plain English |
|----------------|--------|--------------|
| **EMA Fast Protection** | Check if fast EMA is above 200 EMA | "Short-term trend up?" |
| **EMA Slow Protection** | Check if 1-hour EMA is healthy | "Use telescope to check for dangers ahead" |
| **SMA200 Rising** | 200-day MA must be rising | "Long-term trend must be up" |
| **SMA200 1h Rising** | 1-hour 200-day MA must be rising | "1-hour long-term must also be up" |
| **Safe Dips Protection** | Check if dropped too much | "Don't bottom-fish at mid-slope!" |
| **Safe Pump Protection** | Check if rose too much | "Don't chase at the top!" |

8 layers of protection — like "three-generation family history check" level caution 🤣

### Safe Dips (Safe Dips) Explained

| Type | What counts as "safe" dip? |
|------|--------------------------|
| **strict** | Dips of 1.5%/10%/24%/42% are safe to buy |
| **normal** | Dips of 2%/14%/32%/50% are safe to buy |
| **loose** | Dips of 2.6%/24%/42%/80% are safe to buy |

**Plain English**: If it dropped too much, the strategy says — "Bro, wait — don't buy until it's fully dropped!"

### Safe Pump (Safe Pump) Explained

| Type | How much rise in 24/36/48 hours counts as "unsafe"? |
|------|---------------------------------------------------|
| **strict** | Rise over 42% is unsafe to buy |
| **normal** | Rise over 60% is unsafe to buy |
| **loose** | Rise over 66% is unsafe to buy |

**Plain English**: "Rose too much, don't chase! Wait for a pullback!"

---

## 5. Exit Logic: Refined "Harvesting"

### 5.1 Stepped Take-Profit: How Much to Make and Run

This strategy has **12 stepped take-profit levels** — the more you earn, the looser the conditions:

| Level | Profit Required | RSI Threshold | Plain English |
|-------|----------------|---------------|--------------|
| 0 | 1% | < 33 | Made 1%, RSI over 33? Run |
| 1 | 2% | < 34 | Made 2%, RSI over 34? Run |
| 2 | 3% | < 38 | Made 3%, RSI over 38? Run |
| ... | ... | ... | ... |
| 10 | 12% | < 42 | Made 12%, allow RSI to 42 |
| 11 | 20% | < 34 | Made 20%! Allow RSI to 34 |

**Plain English**: The more you earn, **the calmer I get**. This is what "let profits run" really means!

---

## 6. The Strategy's "Personality Traits"

### ✅ Pros

1. **Good Protection**: 8 layers of protection, hard to lose money
2. **Many Opportunities**: 24 buy conditions, always one for you
3. **Refined Take-Profit**: 12-level stepped take-profit, maximize profits
4. **Trend Confirmation**: Dual timeframe, see near and far
5. **Flexible Config**: Each condition individually switchable

### ⚠️ Cons

1. **Absurdly Complex**: 24 buy conditions + 8 sell conditions, steep learning curve
2. **Too Many Parameters**: Easy to overfit historical data
3. **High Hardware**: Dual timeframe + many indicators, old computers might lag
4. **Trading Frequency**: Many trades in bull markets, fees eat into profits
5. **Poor in Consolidation**: Protection triggers frequently during sideways

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|---------------------|--------|
| 📈 Bull Market | max_open_trades: 4-6, all buy conditions on | Clear trend, maximize multi-signals |
| 🔄 Volatile Market | max_open_trades: 2-3, Safe Pump on | Reduce positions, avoid chasing tops |
| 📉 Bear Market | max_open_trades: 1-2, Safe Dips on | Careful bottom-fishing, control risk |
| ⚡ Extreme Volatility | Pause trading | Price limits may affect execution |

---

## 8. Summary

### One-Line Verdict
> "A trend hunter armed to the teeth, protection mechanisms outrageously many, but a money-maker in capable hands."

---

## 9. ⚠️ Risk Re-Emphasis (Must Read!)

### Backtesting Looks Great, Live Trading Is Different

Combined_NFIv6_SMA's historical backtesting often **looks extremely good** — but there's a trap:

> **With many parameters, the strategy easily "fits" the optimal solution for past markets, but doesn't guarantee future profitability.**

Simply put: **Like exam prep — all past exam answers memorized, but change the questions and you're lost.**

### My Suggestions

```
1. Paper trade at least 1-2 months, don't rush to live trade
2. Start with minimum position in live trading, verify performance before adding
3. Watch actual slippage and fees — backtesting won't tell you these
4. Don't blindly pursue high returns, stability matters more
5. Periodically review trading records, understand strategy failures
```

**Remember**: No matter how good a strategy, the market teaches lessons without warning. Test with small positions — survival is what matters! 🙏

---

**Final Reminder**: Quantitative trading is not a money printer — it's a tool. Good strategies need good execution; good execution needs good mindset. Stay humble, keep learning, and you can survive and thrive in the markets.
