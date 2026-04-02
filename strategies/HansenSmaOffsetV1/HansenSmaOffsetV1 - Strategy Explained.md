# HansenSmaOffsetV1 Strategy: Simple and Brutal

> **Nickname**: Band Breakout Brawler  
> **Timeframe**: 15 Minutes

---

## 1. What's This Strategy About?

**HansenSmaOffsetV1** is a "brute force" strategy:
- Dropped too much? Buy! (breakout of lower band)
- Rallied too much? Sell! (breakout of upper band)

**Plain English Analogy**:
> Like a bouncy ball:
> - Ball hits the floor (lower band) → bounces up (buy)
> - Ball hits the ceiling (upper band) → drops down (sell)

---

## 2. Core Settings

### Take-Profit Rule (ROI Table)

```
Immediate exit (0 min)     → Take 10% and run!
After 30 minutes           → Take 5% and run!
After 60 minutes           → Take 2% and run!
```

### Stop-Loss Rule

```
Hard stop-loss: -10%
```

---

## 3. Entry Conditions

### 🎯 Core Conditions

1. **Price breaks lower band**: `high < smad1`
2. **Green candle close**: `hopen < hclose`

**Plain English**:
> "Price dropped below the lower band, and it's closing green — rebound incoming, BUY!"

---

## 4. Exit Logic

### 4.1 Exit Conditions

1. **Price breaks upper band**: `low > smau1`
2. **Red candle close**: `hopen > hclose`

**Plain English**:
> "Price jumped above the upper band, and it's closing red — pullback incoming, SELL!"

---

## 5. Technical Indicators

### SMA Offset Band

| Indicator | Calculation | Purpose |
|---------|------------|---------|
| Upper band | SMA(20) × 1.05 | Resistance |
| Lower band | SMA(20) × 0.95 | Support |

---

## 6. The Strategy's "Personality"

### Pros

1. **Dead Simple**: One look and you get it
2. **Clear Signals**: No hemming and hawing
3. **Beginner-Friendly**: Great starting point

### Cons

1. **Ranging Market Mediocre Performance**: Upper and lower bands trigger constantly
2. **No Filters**: Prone to fake signals

---

## 7. When to Use It?

| Market | What to Do |
|--------|-----------|
| Ranging/Sideways | ✅ Use it |
| Trending | ⚠️ Tweak it |

---

## 8. The Bottom Line

### One-Line Verdict
> "Simple and brutal — buy the dip, sell the rip!"

### Who's It For?
- ✅ Newcomers (easy to understand)
- ✅ Simple-strategy lovers

### Who's It NOT For?
- ❌ Complexity seekers
- ❌ People who want fake signal filters

---

## 9. What Markets Does This Make Money In?

### Market Performance

| Market Type | Rating |
|:-----------|:------:|
| Ranging/Sideways | ⭐⭐⭐⭐⭐ |
| Trending | ⭐⭐⭐☆☆ |

---

## 10. Want to Run This?

### Config

```yaml
minimal_roi:
  "0": 0.10
  "30": 0.05
  "60": 0.02

stoploss: -0.10
```

---

## 11. Bonus Bits

1. **SMA Offset**: Uses ±5% as the channel
2. **Pure Brutality**: No fancy tricks here

---

## 12. ⚠️ Risk Reminder

### Risk

Ranging markets = frequent stop-losses!

### My Advice

```
1. Use it when market is ranging
2. Small money test
3. Set your stop-loss
```

**Remember**: Simple ≠ Effective! 🙏

---

**Final Reminder**: Small position test, survival first! 🙏
