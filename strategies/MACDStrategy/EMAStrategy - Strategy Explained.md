# EMAStrategy: The Art of EMA "Lining Up"

> **Nickname**: The EMA Queue Master  
> **Career**: Trend Follower  
> **Timeframe**: 5 Minutes / 15 Minutes / 1 Hour

---

## 1. What's This Strategy?

**EMAStrategy** is a strategy that watches EMAs "line up in order":
- Short MA > Medium MA > Long MA → Buy! (Bullish queue)
- Short MA < Medium MA → Sell! (Queue disbanded)

Think of it like lining up for bubble tea — **whoever's in front calls the shots** 🧋

---

## 2. Core Settings: "Grab Profits and Run"

### Take-Profit Rules (ROI Table)

```
Immediate exit (0 minutes)     → Earn 5% and run!
After 30 minutes               → Earn 3% and run!
After 60 minutes               → Earn 2% and run!
After 120 minutes              → Earn 1.5% and run!
```

**Translation**: The longer you hold, the lower your goal. Don't get greedy! 😏

### Stop-Loss Rules

```
Hard stop-loss: -5%
Trailing stop: activation at 3%, pullback 5%
```

---

## 3. Buy Conditions: EMA Bullish Queue

### Core Condition: Queue Up!

```python
(ema_short > ema_medium) & (ema_medium > ema_long) & (close > ema_short)
```

**Plain English**:
> "Short MA > Medium MA > Long MA + price above short MA → Buy!"

**Translation**:
- EMA9 > EMA21 > EMA50 = "Short, medium, and long all look good — trend is up!"
- Price > EMA9 = "Current price is strong, above the short MA"

---

## 4. How to Pick EMA Periods?

| MA Type | Typical Values | Analogy |
|---------|---------------|---------|
| **Short-term** | 9 / 10 | Impatient type (reacts fast) |
| **Medium-term** | 21 / 26 | Steady type |
| **Long-term** | 50 / 200 | Old sage (looks far ahead) |

---

## 5. Sell Logic: Queue Disbanded

### 5.1 Sell Conditions

```python
ema_short < ema_medium  # Death cross
```

**Plain English**:
> "Short MA dropped from above to below the medium MA — trend might change → Sell!"

### 5.2 Exit Methods

| Exit Method | Trigger Condition |
|-------------|------------------|
| Death cross sell | Short MA < Medium MA |
| Price sell | Closing price breaks below medium MA |
| Take-profit exit | Target profit reached |
| Stop-loss exit | Loss of 5% |

---

## 6. Technical Indicators

| Indicator | Period | Purpose |
|-----------|--------|---------|
| EMA | Adjustable | Core trend line |
| Volume | - | Signal confirmation |

---

## 7. Risk Management

### Protection Layers

| Protection Layer | Function |
|-----------------|----------|
| Hard stop-loss | -5% |
| Trailing stop | Protect profits |
| ROI take-profit | Phased exit |

---

## 8. Strategy "Personality"

### Pros

1. **Simple and easy**: Just watch the EMA queue
2. **Clear signals**: No hesitation about whether to buy
3. **Crushes trending markets**: Trade with the trend
4. **Adjustable parameters**: Works in different markets

### Cons

1. **Dies in choppy markets**: MAs line up randomly during consolidation
2. **Has lag**: By the time the signal appears, it might be too late
3. **Many false signals**: Frequent crossovers get you slapped in the face

---

## 9. Applicable Scenarios

| Market Environment | Recommended Action |
|-------------------|-------------------|
| Trending up | Works great |
| Trending down | Use in reverse |
| Oscillating | Not suitable |
| Consolidating | Not suitable |

---

## 10. Summary

### One-Line Rating
> "A brutally simple MA strategy — works great in trending markets!"

### Who Is It For?
- Beginners (simple and clear)
- Trend traders
- People who don't want to overthink

### Who Is It NOT For?
- Oscillation traders
- Impatient folks

---

## 11. What Markets Does This Strategy Make Money In?

### 11.1 Core Logic

EMA bullish alignment = trend is up = Buy!

### 11.2 Market Performance

| Market Type | Performance Rating |
|:-----------|:------------------|
| Trending up | Excellent |
| Trending down | Excellent |
| Oscillating | Poor |
| Consolidating | Very Poor |

---

## 12. Want to Run This Strategy?

### Configuration

```yaml
minimal_roi:
  "0": 0.05
  "30": 0.03
  "60": 0.02
  "120": 0.015

stoploss: -0.05
trailing_stop: true
```

### Suggestions

1. Add RSI filtering
2. Add volume confirmation
3. Check the direction of larger timeframes

---

## 13. Final Warning ⚠️

### Risks

EMA lag = The signal might be late!

### My Suggestions

```
1. Only use when the trend is obvious
2. Set stop-losses
3. Diversify investments
```

**Remember**: Simple ≠ Effective! 🙏

---

**Final Reminder**: Test with small positions! 🙏
