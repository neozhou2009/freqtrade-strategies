# MACD Strategy: The MACD + CCI "Double Insurance" Combo

> **Nickname**: Trend Confirmer  
> **Timeframe**: 5 Minutes (medium-to-short-term)

---

## 1. What's This Strategy?

**MACD** is the **most classic** strategy in quantitative trading.

Simply put:
- Uses **MACD** to see which direction the trend is heading
- Uses **CCI** to see if it's overbought or oversold
- Both agree → then place an order

**Plain English**:
> Like pursuing your crush:
> - Did MACD agree? (Is the trend right?)
> - Did CCI agree? (Is the timing right?)
> - Both agree → make your move!

---

## 2. Core Settings

### Take-Profit (Multi-Level ROI)

| Holding Time | Profit Required |
|-------------|-----------------|
| Just bought | 5% |
| After 20 minutes | 4% |
| After 30 minutes | 3% |
| After 1 hour | 1% (get out) |

### Stop-Loss

```
Hard Stop: -30%
```

---

## 3. Entry Conditions: Both Must Be Met

### Condition 1: MACD Golden Cross

```
MACD > Signal (fast line above slow line)
```

**Plain English**:
> "Short-term moving average has crossed above long-term — the trend is starting to go up!"

---

### Condition 2: CCI Oversold

```
CCI <= -48 (optimized default)
```

**Plain English**:
> "CCI says it's oversold right now — price has fallen too much, a bounce is coming!"

---

### Condition 3: Has Volume

```
volume > 0
```

---

## 4. Exit Conditions: Reversed

### Condition 1: MACD Death Cross

```
MACD < Signal (fast line below)
```

### Condition 2: CCI Overbought

```
CCI >= 687 (optimized value)
```

---

## 5. How It Works

### 5.1 What Is MACD?

```
MACD = EMA12 - EMA26 (short-term minus long-term)
Signal = 9-period EMA of MACD
```

**Analogy**:
> Like comparing two runners' speeds:
> - You (short-term) run faster than your teacher (long-term) → MACD positive → trend up
> - You run slower than your teacher → MACD negative → trend down

---

### 5.2 What Is CCI?

```
CCI = Commodity Channel Index
```

**Purpose**: Detecting overbought/oversold
- CCI < -100: Oversold → potential bounce
- CCI > 100: Overbought → potential pullback

---

### 5.3 Why Use Both Together?

| Indicator | Role |
|-----------|------|
| MACD | Confirm trend direction |
| CCI | Confirm timing (overbought/oversold) |

**Analogy**:
> Like driving:
> - MACD: Check the direction (which way are you going?)
> - CCI: Check the speed (should you hit the brakes?)

---

## 6. Good Points

1. **Classic Combo**: Both MACD and CCI are classic indicators
2. **Double Insurance**: Trend + timing double confirmation
3. **Optimizable**: CCI parameters can auto-optimize
4. **Clear Logic**: Simple code, easy to understand

---

## 7. Bad Points

1. **Has Lag**: MACD itself is half a beat behind
2. **Useless in Ranging Markets**: Crosses back and forth, constant face-slapping
3. **Big Stop-Loss**: -30% really stings
4. **Parameter Sensitive**: CCI threshold has a big impact

---

## 8. When It Works — And When It Doesn't

| Market | Performance | Why |
|--------|-------------|-----|
| **Uptrend** | ⭐⭐⭐⭐⭐ | MACD golden cross + CCI oversold — perfect |
| **Downtrend** | ⭐⭐⭐⭐⭐ | Same logic in reverse, equally effective |
| **Ranging Upward** | ⭐⭐⭐ | Stair-step rallies can be caught |
| **Sideways Ranging** | ⭐⭐ | Too many false signals |

---

## 9. How to Use It

### 9.1 Default Parameters

| Parameter | Default | Optimized |
|-----------|---------|-----------|
| buy_cci | -50 | -48 |
| sell_cci | 100 | 687 |

### 9.2 Timeframe

Recommended 5 minutes or 15 minutes.

### 9.3 Optimization Tips

| Tweak | How |
|-------|-----|
| Make it stricter | Raise CCI threshold |
| Make it more lenient | Lower CCI threshold |

---

## 10. Risk Warnings

### ⚠️ Trap 1: Lag

**What Happens**:
> By the time MACD golden cross confirms, the move has already started

**Fix**:
- Use a shorter timeframe
- Combine with other leading indicators

### ⚠️ Trap 2: Ranging Face-Slapping

**What Happens**:
> Market chops back and forth, MACD crosses and recrosses

**Fix**:
- Only use when trend is clearly established
- Add moving average filtering

---

## 11. Bottom Line

**One-Line Summary**:
> MACD is a classic "trend + momentum" double-confirmation strategy — MACD for direction, CCI for timing. Best in clearly trending markets.

**Memory Aid**:
> "I watch for the MACD golden cross, I judge the CCI oversold zone — both agree, I buy; one disagrees, I stand by!"

---

*MACD — done! Last one: MACD_Cross!*

---

## 12. Want to Run This Strategy?

### Configuration

```yaml
minimal_roi:
  "0": 0.08
stoploss: -0.05
```

---

## ⚠️ Final Warning

### Risk

Simple ≠ Effective!

### My Advice

```
1. Test with small money
2. Use when trends are clear
3. Set your stop-loss
```

**Remember**: Strategies need testing! 🙏

---

**Final Reminder**: Start with light positions! 🙏
