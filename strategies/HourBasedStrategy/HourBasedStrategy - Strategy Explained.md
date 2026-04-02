# HourBasedStrategy Strategy: Trading by the Clock

> **Nickname**: Time Manager  
> **Timeframe**: 1 Hour

---

## 1. What's This Strategy About?

**HourBasedStrategy** is a strategy that **only cares about the time**. It doesn't care about candles, indicators, or tea leaves — just what time it is: buy during the buy window, sell during the sell window!

**Plain English Analogy**:
> Like an office worker:
> - 9 AM to 5 PM: Work hours (buy window)
> - After 5 PM: Off hours (sell window)
> - Only looks at the clock, not the mood! 🕐

---

## 2. Core Settings

```
Take-profit: 52.8% (just bought) → 11.3% (3 hrs later)
             → 8.9% (9 hrs later) → 0% (1 day later)
Stop-loss: -10%
```

---

## 3. Buy and Sell Times

### Buy Time: 4 AM → Midnight
```
buy_hour: 4 - 24 (i.e., 4:00 AM - 11:59 PM)
```

### Sell Time: 9 PM → 10 PM
```
sell_hour: 21 - 22
```

---

## 4. Strategy Logic

**So simple it's almost sad**:
- What time is it?
- In the buy window? → BUY!
- In the sell window? → SELL!

---

## 5. The Bottom Line

### One-Line Verdict
> "Buy during work hours, sell at closing time!"

### Who's It For?
- ✅ Newcomers (easiest to understand)
- ✅ Traders wanting to try time-based effects

### Who's It NOT For?
- ❌ Complexity seekers

---

## 6. ⚠️ Risk Reminder

**Remember**: Small position size test! 🙏
