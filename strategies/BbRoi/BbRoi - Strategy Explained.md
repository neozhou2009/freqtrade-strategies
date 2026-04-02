# BbRoi: I Only Buy When Trend Already Started! 📈

> **Nickname**: Trend Follower + Strong Zone Buyer + Confirmation King
> **Profession**: Don't catch bottoms — follow established trends
> **Timeframe**: 15 minutes

---

## 1. What's This Strategy?

Simply put — BbRoi is:
- Price in BB middle-to-upper zone (strong area!)
- EMAs all aligned bullishly (trend confirmed!)
- BUY!
- RSI overbought OR price falls below middle rail
- SELL!

Like a **momentum trader** 🏃:
> "I don't try to buy at bottom — that's too risky! I wait for trend to START — then jump on! Yes — I miss the absolute bottom — but I also avoid catching falling knives!"

This strategy's core philosophy is **trend following** — buy when trend already established — not when trying to catch bottoms.

---

## 2. Core Config: Aggressive Targets

### Take-Profit Rules

```python
minimal_roi = {
    "0": 0.176,    # 17.6% take-profit
    "53": 0.115,   # 11.5% after 53 candles (~13 hours)
    "226": 0.061,  # 6.1% after 226 candles (~2 days)
    "400": 0       # After ~4 days — trailing only
}
```

**In Plain English**:
> "17.6% take-profit — ambitious! Strategy expects to catch good trend moves. If can't make 17% quickly — willing to wait 13 hours for 11.5% — or 2 days for 6.1%. Patient trend following!"

### Stoploss Rules — HIGH!

```python
stoploss = -0.237    # 23.7% stoploss!
```

**In Plain English**:
> "23.7% stoploss! This is HIGH! Means you can lose almost 1/4 of position before cutting! Strategy gives trend lots of room to develop — but this is DANGEROUS for most traders!"

### Trailing Stop — Conservative

```python
trailing_stop = True
trailing_stop_positive = 0.01    # Lock 1% profit
trailing_stop_positive_offset = 0.018  # Activate after 1.8%
```

**In Plain English**:
> "Trailing activates after just 1.8% profit — locks 1%. Very conservative! This means strategy protects profits early — but may exit too soon in big trends!"

---

## 3. Entry Conditions: Trend Must Be Confirmed!

### Condition: Price in Strong Zone + EMAs Bullish

```python
# Price between BB middle and upper (strong zone!)
close > bb_middle AND close < bb_upper

# Price above EMAs
close > ema9 AND close > ema200

# EMA bullish arrangement
ema20 > ema200
```

**In Plain English**:
> "I don't buy when price is weak — I buy when price is STRONG!

Price must be in upper half of Bollinger Bands (strong zone!)
Price must be above all EMAs (momentum up!)
EMA20 must be above EMA200 (trend confirmed!)

Only when ALL conditions met — I buy!

This means I miss the absolute bottom — but I also avoid buying in downtrends!"

**Simple Translation**:
1. Price in BB upper zone (strong!)
2. Price above all EMAs (momentum!)
3. EMA20 > EMA200 (trend!)
4. All conditions met → BUY!

**Deep Interpretation**:
This is like waiting for train to start moving before jumping on:
- Train stopped = bottom fishing (risky!)
- Train starting to move = trend confirmation (safer!)
- Train at full speed = too late (don't chase!)

I wait for train to START moving — then jump on!

---

## 4. Exit Conditions: Overbought or Trend Broken!

### Condition: RSI > 75 OR Price Falls Below 97% of BB Middle

```python
# RSI overbought
rsi > 75

# OR trend broken
price < bb_middle * 0.97
```

**In Plain English**:
> "Two ways to exit:
1. RSI > 75 = overbought = time to take profits!
2. Price falls below middle rail = trend broken = cut and run!

Simple and clear!"

---

## 5. Strategy's "Personality Traits"

### ✅ Pros

1. **Trend confirmation**: Multiple confirmations = higher quality
2. **Strong zone entry**: Buys strength — not weakness
3. **Clear rules**: Entry and exit well defined
4. **Avoids counter-trend**: EMA filter prevents bad trades
5. **Defined risk**: Clear stoploss

### ⚠️ Cons

1. **23.7% stoploss**: HIGH — dangerous
2. **Misses bottoms**: Waits for confirmation — miss early moves
3. **Conservative trailing**: May exit too early
4. **Trend dependent**: Useless in ranging markets
5. **Complex conditions**: May miss opportunities

### 😇 Personality Portrait

> "This is a 'cautious trend follower' — won't jump in until trend confirmed! Like someone who waits for green light — then looks both ways — then crosses! Safe — but sometimes misses the bus!"

---

## 6. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Operation | Reason |
|-------------------|----------------------|--------|
| Strong Trend 🌟🌟🌟🌟🌟 | Perfect | Catches established trends |
| Ranging 🌟 | Don't use | No trends to follow |
| Breakout 🌟🌟🌟🌟 | Suitable | Catches breakout continuation |
| Reversal 🌟🌟 | Cautious | Waits for confirmation |

---

## 7. Bottom Line: How's This Strategy Really?

### One-Sentence Review
> "This is a 'cautious trend follower strategy' — I wait for trend confirmation before buying! Safe! But cost: 23.7% stoploss DANGEROUS — misses early moves — conservative trailing!"

### Who Should Use It?
- ✅ Trend followers (confirms before entering)
- ✅ Risk-averse on entry (won't catch bottoms)
- ✅ Can accept missing early moves
- ✅ Understand trend trading
- ✅ High risk tolerance (23.7% stoploss!)

### Who Should NOT Use It?
- ❌ Bottom fishers (waits for confirmation)
- ❌ Low risk tolerance (23.7% stoploss!)
- ❌ Want to catch early moves (misses them)
- ❌ Ranging markets (no trends)
- ❌ Impatient (requires confirmation)

---

## 8. ⚠️ Risk Reminder

### Key Risks

1. **23.7% stoploss**: Very high — can cause significant losses
2. **Misses early moves**: By time confirmed — price already moved
3. **Conservative trailing**: May give back too much profit
4. **Trend dependent**: Useless in ranging markets

### Critical Advice

> "MUST reduce stoploss before live trading! 23.7% is too high for most traders! Change to 10-15% maximum!

Also — understand this strategy misses early moves — that's by design! If you want to catch bottoms — look elsewhere!"

---

## Summary

BbRoi is a **trend-confirmed Bollinger Band** strategy. Core value:

1. **Trend confirmation**: Multiple EMA confirmations
2. **Strong zone entry**: Buys strength — not weakness
3. **Clear exits**: RSI or trend break

But CRITICAL: **23.7% stoploss is HIGH!** Must reduce before live trading! Also — accepts missing early moves for higher confirmation!

---

*This document is based on strategy code*
