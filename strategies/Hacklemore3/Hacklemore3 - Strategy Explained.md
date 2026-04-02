# Hacklemore3 Strategy: The 5-Minute Speedster

> **Nickname**: Short-Term Hunter  
> **Timeframe**: 5 Minutes

---

## 1. What's This Strategy About?

**Hacklemore3** is Hacklemore2's 5-minute short-term cousin. But it has a smarter twist: **when it's making money, it uses dynamic trailing stop to protect gains; when it's losing, it watches the trend to decide whether to bail**.

**Plain English Analogy**:
> Like driving:
> - Making money: buckle up (dynamic trailing stop)
> - Losing money: if the road looks bad, run (trend broken, you're out)

---

## 2. Core Settings

```
Take-profit: 15% (just bought) → 1.5% (5 min later)
Stop-loss: -10%
Trailing stop: 2% activation, 3% offset
```

---

## 3. Entry Conditions

Almost identical to Hacklemore2:
1. Uptrend
2. RMI > 55
3. SAR below price
4. Normal volume

---

## 4. Exit: Two Different Scenarios

### Scenario 1: Losing Money
```
dn_trend == True AND RMI < 50
```
→ "Trend broke, get out!"

### Scenario 2: Making Money
```
current_price > max_price * 0.8 AND consecutive decline
```
→ "Already made good money, price starting to fall — dynamic trailing stop kicks in!"

---

## 5. The Bottom Line

### One-Line Verdict
> "Knows when to protect profits, knows when to cut losses!"

---

## 6. Risk Reminder

**Remember**: Small position size test! 🙏
