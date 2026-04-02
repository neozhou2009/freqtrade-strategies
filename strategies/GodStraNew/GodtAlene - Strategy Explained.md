# GodtAlene Strategy: The MA + RSI "Double Insurance"

> **Nickname**: Nordic Double Insurance  
> **Career**: Trend Momentum Follower  
> **Timeframe**: 1 Hour / 4 Hours

---

## 1. What's This Strategy?

**GodtAlene** is a **"double insurance"** strategy:
- MAs read the direction (trends)
- RSI reads the heat level (momentum)

Both agree → Buy!

---

## 2. Core Settings

### Take-Profit Rules

```
Holding > 0 minutes:  earn 10% and run
Holding > 2 hours:    earn 6% and run
Holding > 8 hours:    earn 3% and run
```

### Stop-Loss Rules

```
-6% stop-loss
```

---

## 3. Two "Brushes"

| Tool | Function |
|------|---------|
| **SMA100** | Read long-term trend |
| **RSI** | Read if it's overheated |

---

## 4. Buy Conditions

### Core Condition

```python
(Price > SMA100) & (RSI breaks above 40 from below)
```

**Plain English**:
> "Price above long-term MA + RSI starting to strengthen → Buy!"

**Translation**:
- Price > SMA100 = "Long-term trend is up"
- RSI breaks 40 = "Momentum starting to pick up"

---

## 5. Sell Conditions

### 5.1 Sell

```python
Price breaks below SMA100 OR RSI > 70
```

**Plain English**:
> "Breaks below MA or RSI too hot — run!"

### 5.2 Exit Methods

| Exit | Trigger |
|------|---------|
| MA break | Trend reversal |
| RSI > 70 | Overbought warning |
| Take-profit | Target reached |
| Stop-loss | Down 6% |

---

## 6. Characteristics

### Pros

1. **Double insurance**: MA + RSI both confirm
2. **Clear trends**: Only trades with the trend
3. **Not over-trading**: Signals not too frequent

### Cons

1. **May lag**: Needs time for MA confirmation
2. **Average in oscillation**: RSI may give false signals during consolidation
3. **Fixed parameters**: May need fine-tuning

---

## 7. Summary

**GodtAlene** is the **"dual swords combined"**:
- MA reads direction + RSI reads strength
- Needs patience to wait for signals

**One-liner**: Both indicators nod before you move! 🤝

---

*Document generated: 2026-03-23*

---

## 8. Technical Indicators

| Indicator | Purpose |
|-----------|---------|
| EMA | Trend |
| RSI | Momentum |

---

## 9. Risk Management

### Protection Layers

| Protection Layer | Function |
|-----------------|----------|
| Hard stop-loss | -5% |

---

## 10. Summary

### One-Line Rating
> "Simple and effective strategy!"

---

## 11. What Markets Does This Strategy Make Money In?

### Market Performance

| Market Type | Performance Rating |
|:-----------|:------------------|
| Trending | Excellent |
| Oscillating | Poor |

---

## 12. Want to Run This Strategy?

### Configuration

```yaml
minimal_roi:
  "0": 0.08
stoploss: -0.05
```

---

## 13. Final Warning ⚠️

### Risks

Simple ≠ Effective!

### My Suggestions

```
1. Test with small money
2. Use when the trend is clear
```

**Remember**: Simple strategies need testing too! 🙏

---

**Final Reminder**: Test with small positions! 🙏
