# Gumbo1 Strategy: The Rebound Hunter

> **Nickname**: Rebound Hunter  
> **Profession**: Counter-Trend Bottom-Picker  
> **Timeframe**: 5 Minutes + 1-Hour Info Layer

---

## 1. What's This Strategy About?

**Gumbo1** is basically a "wait until it's oversold, then pounce" strategy. It waits for EWO to hit extreme negative territory (meaning it's dropped way too much), then looks for buys near Bollinger Band support.

**Plain English Analogy**:
> Like catching a falling knife:
> - Everyone's panicking and selling
> - It waits until most people have stopped throwing
> - Then swoops in to grab the bargains 🏴‍☠️

---

## 2. Core Settings

```
Take-profit: 10% (just bought) → 5% (20 min later) → 3% (1 hr later)
Stop-loss: -25%
```

---

## 3. Entry Conditions

### Condition 1: EWO Extreme Negative
```
EWO < ewo_low (default 0, probably negative)
```
**Plain English**: "Dropped too much — time for a bounce!"

### Condition 2: 1-Hour Bollinger Band Confirmation
```
bb_middleband_1h >= T3_1h
```
**Plain English**: "The 1-hour Bollinger middle band is sitting up there — strong support!"

### Condition 3: T3 <= EMA
```
T3 <= EMA
```
**Plain English**: "Price is consolidating — about to make a move!"

---

## 4. Exit Conditions

### Condition 1: Stochastic Overbought
```
stoch > 80
```
**Plain English**: "Rallied too much — time for a pullback!"

### Condition 2: T3 Hits Bollinger Middle Band
```
T3 >= bb_middleband_40
```
**Plain English**: "Price hit the Bollinger middle band resistance!"

---

## 5. The Bottom Line

### Who's It For?
- ✅ People who can stomach a -25% stop-loss
- ✅ Patient folks waiting for extreme oversold setups
- ✅ Counter-trend traders

### Who's It NOT For?
- ❌ Conservative investors
- ❌ People chasing steady returns

### One-Line Verdict
> "Waits for the oversold bottom, bets on the bounce!"

---

## 6. What Markets Does This Make Money In?

| Market Type | Rating |
|:-----------|:------:|
| Trending | ⭐⭐⭐⭐⭐ |

---

## 7. Risk Reminder

**Remember**: Small position size test! 🙏
