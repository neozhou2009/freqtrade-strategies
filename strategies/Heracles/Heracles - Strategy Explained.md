# Heracles Strategy: The Ultra-Long-Haul Player

> **Nickname**: Heracles (Greek Hero)  
> **Profession**: Ultra-Long-Term Trend Hunter  
> **Timeframe**: 12 Hours (Ultra-long-term!)

---

## 1. What's This Strategy About?

**Heracles** is an **ultra-long-term** strategy — 12-hour timeframe, holding periods can last a WEEK! Its core is finding volatility extremes: volatility's gotten ridiculously small? That means it's about to EXPLODE!

**Plain English Analogy**:
> Like waiting for an earthquake:
> - Everything's been quiet (low volatility)
> - Suddenly... volatility starts increasing
> - Earthquake coming! → Get in!

---

## 2. Core Settings

### Take-Profit Rule (ROI Table)

```
Immediate exit (0 min)     → Take 32.8% and run!
After 27 hours              → Take 17.9% and run!
After 4 days                → Take 5.4% and run!
After 7.5 days              → Break even and get out
```

### Stop-Loss Rule

```
Hard stop-loss: -4.66%
Trailing stop: activation point 2.4%
```

**Heads up**: This is an ultra-long-term strategy — holding period can exceed 7 days!

---

## 3. Entry Conditions

### 🎯 Core Condition

```
Donchian Channel Percentile < Keltner Channel Width
```

**Plain English**:
> "Volatility's way too low — price's about to break out! BUY!"

---

## 4. Exit Logic

### 4.1 Exit Condition

```
MACD Signal crosses below EMA(12)
```

**Plain English**:
> "Trend's starting to weaken — time to get out!"

---

## 5. Technical Indicators

| Indicator | Purpose |
|---------|---------|
| Keltner Channel | Volatility |
| Donchian Channel | Price position |
| MACD | Trend |
| EMA(12) | Fast trend |

---

## 6. The Strategy's "Personality"

### Pros

1. **Ultra-Long-Term**: No need to watch the screen all day
2. **Volatility Capture**: Finds setups about to break out
3. **For Patient People**: Built for those who can wait

### Cons

1. **Long Holding Period**: Could be holding for a week
2. **Not for Impatient Folks**: Patience is non-negotiable

---

## 7. When to Use It?

| Market | What to Do |
|--------|-----------|
| Post-Low-Volatility Breakout | ✅ Use it |
| Ranging | ❌ Don't use it |

---

## 8. The Bottom Line

### One-Line Verdict
> "Ultra-long-haul player — holds for a week at a time!"

### Who's It For?
- ✅ Patient folks
- ✅ Big-trend seekers

### Who's It NOT For?
- ❌ Impatient traders
- ❌ Short-term traders

---

## 9. What Markets Does This Make Money In?

### Market Performance

| Market Type | Rating |
|:-----------|:------:|
| Post-Low-Volatility Breakout | ⭐⭐⭐⭐⭐ |
| Ranging | ⭐⭐☆☆☆ |

---

## 10. Want to Run This?

### Config

```yaml
minimal_roi:
  "0": 0.328
  "27h": 0.179
  "4d": 0.054
  "7.5d": 0

stoploss: -0.0466
trailing_stop_positive: 0.024
```

---

## 11. Bonus Bits

1. **Heracles Name**: Greek mythology hero — symbol of strength
2. **12-Hour Timeframe**: Ultra-long-term player

---

## 12. ⚠️ Risk Reminder

### Risk

Long holding = more variables!

### My Advice

```
1. Only use if you're patient
2. Small money test
3. Set your stop-loss
```

**Remember**: Ultra-long-term ≠ Safer! 🙏

---

**Final Reminder**: Small position test, survival first! 🙏
