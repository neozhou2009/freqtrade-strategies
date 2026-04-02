# HyperStra_GSN_SMAOnly Strategy: Moving Average Mathematician

> **Nickname**: MA Math Whiz  
> **Timeframe**: 5 Minutes

---

## 1. What's This Strategy About?

**HyperStra_GSN_SMAOnly** is a **hyper-parameterized** moving average strategy. It doesn't just use one MA — it uses 7 SMAs of different periods (5, 6, 15, 50, 55, 100, 110), then runs all kinds of mathematical operations on them to find the optimal signal combo.

**Plain English Analogy**:
> Like taking a math exam:
> - 7 MAs = 7 math problems
> - Gotta calculate the optimal answer
> - And find the best problem-solving method! 📐

---

## 2. Core Settings

### Take-Profit Rule (ROI Table)

```
Immediate exit (0 min)     → Take 28.8% and run!
After 90 minutes            → Take 10.1% and run!
After 180 minutes           → Take 4.9% and run!
After 480 minutes           → Break even and get out
```

### Stop-Loss Rule

```
Hard stop-loss: -5%
Trailing stop: activation 0.5%, offset 1.6%
```

---

## 3. Entry Conditions (3 Groups of Parameters)

### 🎯 Group 1

- SMA(5) / SMA(110) normalized ratio < 0.3

### Group 2

- SMA(5) / SMA(6) normalized ratio < 0.5

### Group 3

- SMA(55) / SMA(100) normalized ratio < 0.9

**Plain English**:
> "All three math conditions must be satisfied!"

---

## 4. Exit Logic (3 Groups of Parameters)

### 4.1 Exit Conditions

| Group | Condition |
|-------|----------|
| Group 1 | SMA(50) normalized value == 0.9 |
| Group 2 | SMA(50) crosses above SMA(110) |
| Group 3 | SMA(110) crosses below SMA(5) |

**Plain English**:
> "All three conditions must be met before selling!"

---

## 5. Technical Indicators

| Indicator | Periods | Purpose |
|---------|--------|---------|
| SMA | 5, 6, 15, 50, 55, 100, 110 | Multi-period MAs |

---

## 6. The Strategy's "Personality"

### Pros

1. **Hyper-Parameterized**: Big optimization space
2. **Mathematically Rigorous**: Clear logic

### Cons

1. **Too Many Parameters**: Intimidating for beginners
2. **Needs Hyperopt**: Bad results without parameter tuning

---

## 7. When to Use It?

| Market | What to Do |
|--------|-----------|
| Needs optimization | ✅ Use it |
| Newcomers | ❌ Not for you |

---

## 8. The Bottom Line

### One-Line Verdict
> "Trading through a math exam!"

### Who's It For?
- ✅ People who can use Hyperopt
- ✅ Quant optimization enthusiasts

### Who's It NOT For?
- ❌ Newcomers (too many parameters)
- ❌ People who don't want to tune parameters

---

## 9. What Markets Does This Make Money In?

### Market Performance

| Market Type | Rating |
|:-----------|:------:|
| Trending | ⭐⭐⭐⭐☆ |
| Ranging | ⭐⭐⭐☆☆ |

---

## 10. Want to Run This?

### Config

```yaml
minimal_roi:
  "0": 0.288
  "90": 0.101
  "180": 0.049
  "480": 0

stoploss: -0.05
trailing_stop_positive: 0.005
trailing_stop_positive_offset: 0.016
```

---

## 11. Bonus Bits

1. **7 SMAs**: Mathematician's delight
2. **GSN**: Short for Gradient Stochastic Normalization

---

## 12. ⚠️ Risk Reminder

### Risk

Too many parameters = overfitting risk!

### My Advice

```
1. Only use if you know Hyperopt
2. Small money test
3. Don't over-optimize
```

**Remember**: More parameters ≠ Better results! 🙏

---

**Final Reminder**: Small position test, survival first! 🙏
