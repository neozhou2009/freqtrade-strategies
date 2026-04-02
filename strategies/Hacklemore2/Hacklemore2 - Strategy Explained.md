# Hacklemore2 Strategy: Board the Trend, Then Get Off

> **Nickname**: Trend Catcher  
> **Timeframe**: 15 Minutes

---

## 1. What's This Strategy About?

**Hacklemore2** is a "wait for the trend to be obvious, then jump in" strategy. It waits for price to hit a 60-day high, RMI to strengthen — only then will it buy.

**Plain English Analogy**:
> Like surfing:
> - Spot the wave coming (uptrend)
> - Surfboard's ready (RMI strong)
> - Jump on! 🏄‍♂️

---

## 2. Core Settings

```
Take-profit: 14.5% (just bought) → 7.7% (10 min later)
Stop-loss: -10%
Trailing stop: 2% activation, 3% offset
```

---

## 3. Entry Conditions

All must be met simultaneously:

1. **Uptrend**: `up_trend == True` (60-day high)
2. **RMI Strong**: `RMI > 55` AND `RMI >= RMI.rolling(3).mean()`
3. **Price Rising**: `close > close.shift() > close.shift(2)` (three green candles in a row)
4. **SAR Confirmation**: `sar < close` (price above SAR)
5. **Volume Filter**: `volume < volume_ma * 30`

---

## 4. Exit Conditions

1. **Buy signal disappears**: `buy == 0`
2. **Downtrend**: `dn_trend == True`
3. **RMI Weak**: `RMI < 30`
4. **Profit protection**: `profit > -3%`

---

## 5. The Bottom Line

### One-Line Verdict
> "No trend, no entry — trend leaves, you leave!"

---

## 6. Risk Reminder

**Remember**: Small position size test! 🙏
