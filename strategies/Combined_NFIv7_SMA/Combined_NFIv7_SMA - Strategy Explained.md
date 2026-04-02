# Combined_NFIv7_SMA Strategy: 26-Path "Buy Master" + 8-Layer "Body Armor" (V7 Upgraded)

> **Nickname**: Nostalgia For Infinity SMA V7
> **Profession**: 5-Minute Trend Hunter + 1-Hour Telescope Scout
> **Timeframe**: 5 Minutes Main + 1 Hour Trend Confirmation

---

## 1. What's This Strategy?

**Combined_NFIv7_SMA** is the "NostalgiaForInfinity" (Hedge Infinity) Series' **7th Generation SMA-Enhanced Version**.

Simply put, this is an strategy **"armed to the teeth"** — and stronger than V6:

- **26 buy conditions** — like 26 weapons (2 more than V6!)
- **8 sell conditions** — like 8 escape routes
- **8 protection mechanisms** — like 8 layers of body armor
- **Dual timeframe** — enter on 5 minutes, see direction on 1 hour
- **New ZEMA indicator** — zero-lag EMA, more sensitive than regular EMA!

It feels like: you're driving and **the windshield shows 5 meters, the rearview mirror shows 500 meters** — and V7 upgraded you with night vision (ZEMA)!

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

**Translation**: This strategy has big appetite! But as time passes, expectations drop. After an hour, 2% satisfies it.

### Stop-Loss Rules

```python
stoploss = -0.10  # Cut at 10% loss
```

### Trailing Stop Rules

```python
trailing_stop = True
trailing_stop_positive = 0.005      # Starts observing at 0.5% profit
trailing_stop_positive_offset = 0.030  # Must rise to 3.0% before "providing protection"
```

Plain English: **Let the bullet fly, when it reaches 3% start protecting!** (Triggers earlier than V6's 3.5% — more active!)

---

## 3. 26 Buy Conditions: Let Me Sort Them Out

This strategy's buy conditions are ridiculously many. I've grouped them into 7 categories:

### 🎯 Category 1: RSI/MFI Oversold Rebound (Conditions 1, 2)

**Plain English**: "Price has fallen to the point even relatives don't recognize it — time to rebound!"

### 🎯 Category 2: Bollinger Band Rebound (Conditions 3, 4)

**Plain English**: "Bollinger Band has squeezed together — next it's fireworks!"

### 🎯 Category 3: EMA Golden Cross (Conditions 5, 6, 7)

**Plain English**: "MA golden cross! Plus price is cheap — this won't lose!"

### 🎯 Category 4: RSI Extreme Oversold (Conditions 8, 18, 19, 20, 21)

**Plain English**: "RSI low to the max + volume expanding + green close — whales are bottom-fishing!"

### 🎯 Category 5: MA Offset (Conditions 9, 10, 11, 14, 15, 16, 22)

**Plain English**: "Price deviated too far from the MA like a rubber band — time to snap back!"

### 🎯 Category 6: EWO Momentum Reversal (Conditions 12, 13, 16, 17, 22, 23)

**Plain English**: "EWO says there's momentum reversal, let me try!"

### 🆕 Category 7: ZEMA New Weapon (Conditions 24, 26) — V7 Exclusive!

**Core Logic**: ZEMA is zero-lag EMA, more sensitive than regular EMA!

**Plain English**:
> "ZEMA is more sensitive! This new weapon catches leads!"

---

## 4. 8 Protection Mechanisms: Hard to Lose Money

| Protection Type | Effect | Plain English |
|----------------|--------|--------------|
| **EMA Fast Protection** | Check fast EMA above 200 EMA | "Short-term trend up?" |
| **SMA200 Rising** | 200-day MA must be rising | "Long-term trend must be up" |
| **Safe Dips Protection** | Check if dropped too much | "Don't bottom-fish at mid-slope!" |
| **Safe Pump Protection** | Check if rose too much | "Don't chase at the top!" |

8 layers of protection — like "three-generation family history check" level caution 🤣

---

## 5. Exit Logic: Refined "Harvesting"

### Stepped Take-Profit: 12 Levels

The more you earn, the looser the conditions — **let profits run**!

| Level | Profit | RSI Threshold | Plain English |
|-------|--------|---------------|--------------|
| 0 | 1% | < 34 | Made 1%, RSI over 34? Run |
| 11 | 20% | < 34 | Made 20%! I'm calm |

---

## 6. The Strategy's "Personality Traits"

### ✅ Pros

1. **8-Layer Protection**: Hard to lose
2. **26 Buy Conditions** (2 more than V6): Always one for you
3. **12-Level Stepped Take-Profit**: Maximize profits
4. **Dual Timeframe**: See near and far
5. **🆕 ZEMA New Weapon**: Zero-lag EMA, more sensitive entry signals!

### ⚠️ Cons

1. **Absurdly Complex**: 26 conditions + 8 sell conditions
2. **Too Many Parameters**: Easy to overfit
3. **High Hardware Requirements**: Old computers might lag
4. **Poor in Consolidation**: Protection triggers frequently

---

## 7. When to Use It?

| Market Environment | Recommended Action |
|-------------------|---------------------|
| 📈 Bull Market | All conditions, 4-6 open trades |
| 🔄 Volatile Market | 2-3 trades, Safe Pump on |
| 📉 Bear Market | 1-2 trades, Safe Dips on |
| ⚡ Extreme Volatility | Pause trading |

---

## 8. V7 vs V6 Key Upgrades (Highlight!)

| Upgrade | V6 | V7 | Change |
|---------|-----|-----|--------|
| **New Conditions** | 24 | 26 | Added ZEMA-based #24 and #26 |
| **Trailing Stop Offset** | 3.5% | 3.0% | Earlier activation (more aggressive) |
| **New Protection Levels** | Fewer | 12 levels | More refined dip/pump detection |
| **900-Min Holding Protection** | No | Yes | Auto-exit after 15 hours |

> **💡 Summary**: V7 = V6 + 2 new weapons + more sensitive trailing stop + more refined protection

---

## 9. ⚠️ Risk Re-Emphasis (Must Read!)

### Backtesting Looks Great, Live Trading Is Different

Combined_NFIv7_SMA's backtesting often **looks extremely good** — but:

> **With many parameters, easily "fits" past markets, doesn't guarantee future profitability.**

### V7 New Risks

1. **ZEMA Parameter Sensitivity**: More sensitive but may generate more false signals
2. **Condition #26 Auto-Optimization**: May overfit historical data
3. **More Active Trailing Stop**: 3% activation (vs V6's 3.5%) may exit earlier

**Remember**: Strategies are rigid, markets are fluid. Test with small positions — survival is what matters! 🙏

---

**Final Reminder**: V7 is an upgrade, but more parameters = more complexity. **Suitable for experienced users; beginners should start with V6.**
