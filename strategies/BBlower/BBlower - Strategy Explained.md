# BBlower: RSI Must Rise 5 Times Before I Buy! 📈

> **Nickname**: Momentum Waiter + 5-Candle Confirmer + Patient Hunter
> **Profession**: Won't buy until RSI proves it's serious
> **Timeframe**: 5 minutes

---

## 1. What's This Strategy?

Simply put — BBlower is someone who:
- Waits for price to fall to Bollinger Band lower band
- But doesn't buy immediately!
- Waits for RSI to rise 5 consecutive candles
- Only then says "OK — momentum confirmed — BUY!"

Like a **cautious investor** 🧐:
> "You say price is oversold? I don't believe you! You say momentum reversed? Show me proof! I need to see RSI rise 5 times in a row — THEN I'll consider buying!"

This strategy's core philosophy is **momentum confirmation** — doesn't buy at absolute bottom — waits for momentum to prove reversal already started.

---

## 2. Core Config: Aggressive Profit Targets

### Take-Profit Rules

```python
minimal_roi = {
    "0": 0.325,    # 32.5% take-profit — very aggressive!
    "220": 0.136,  # 13.6% after 220 candles (18 hours)
    "962": 0.107,  # 10.7% after 962 candles (3 days)
    "2115": 0      # After 7 days — rely on trailing
}
```

**In Plain English**:
> "32.5% take-profit! This is ambitious! Strategy expects to catch big trends — not small bounces. If can't make 32% — willing to wait 18 hours for 13.6% — or 3 days for 10.7%. Very patient!"

### Stoploss Rules

```python
stoploss = -0.139    # 13.9% stoploss
```

**In Plain English**:
> "13.9% stoploss — moderate. Not too tight — not too loose. Gives price room to breathe after buying."

### Trailing Stop — Very Aggressive!

```python
trailing_stop = True
trailing_stop_positive = 0.298     # Lock 29.8% profit
trailing_stop_positive_offset = 0.304  # Activate after 30.4% profit
```

**In Plain English**:
> "This trailing is CRAZY! Only activates after 30.4% profit — then locks 29.8%! This means strategy expects HUGE trends — won't protect profits until made 30%+! Either win big or don't play!"

---

## 3. Entry Conditions: RSI Must Prove Itself!

### Condition: TEMA Crosses BB Lower + RSI Rises 5 Times + RSI < 50

```python
# RSI must rise 5 consecutive candles
RSI > RSI.shift(1)  # Current > 1 ago
RSI.shift(1) > RSI.shift(2)  # 1 ago > 2 ago
RSI.shift(2) > RSI.shift(3)
RSI.shift(3) > RSI.shift(4)
# And RSI still below 50
RSI < 50
# And TEMA crosses above BB lower band
TEMA crossed above bb_lowerband
```

**In Plain English**:
> "Price fell to lower band? Good start! But I need MORE proof! Show me RSI rising! One candle? Not enough! Two candles? Still not convinced! I need FIVE consecutive candles of RSI rising! AND RSI must still be below 50 (not already rallied too much)! AND TEMA must cross above lower band!

Only when ALL conditions met — I buy!"

**Simple Translation**:
1. RSI rises 5 consecutive candles (momentum building)
2. RSI still below 50 (not overbought)
3. TEMA crosses above BB lower band (price action confirmation)
4. All conditions met → BUY!

**Deep Interpretation**:
This is like a boss interviewing a job candidate:
- Candidate says "I'm skilled!" (price at lower band)
- Boss says "Prove it!" (show me RSI rising)
- Candidate shows one certificate (1 candle rise)
- Boss says "More!"
- Candidate shows 5 certificates (5 candle rise)
- Boss says "OK — you're hired!" (BUY!)

---

## 4. Protection Mechanisms: Built-In Confirmation

BBlower has built-in protection:
- ✅ RSI 5-candle confirmation (filters false signals)
- ✅ RSI < 50 filter (won't chase highs)
- ✅ TEMA cross confirmation (price action)
- ✅ 13.9% stoploss
- ✅ Aggressive trailing stop

**In Plain English**:
> "This strategy is very cautious — won't buy until multiple confirmations. Like a detective who needs multiple pieces of evidence before making arrest!"

---

## 5. Exit Logic: Let Profits Run!

Strategy exits via:
- ROI table (take-profit targets)
- Trailing stoploss (protects profits)
- Fixed stoploss (limits losses)

**In Plain English**:
> "No explicit sell signals — just let profits run until hitting targets or trailing stops. Very hands-off approach!"

---

## 6. Strategy's "Personality Traits"

### ✅ Pros

1. **Momentum confirmation**: RSI 5-candle rise filters fakes
2. **Patient**: Won't chase — waits for proof
3. **High profit potential**: 32.5% target ambitious
4. **Clear rules**: Conditions well defined
5. **Lets profits run**: Aggressive trailing

### ⚠️ Cons

1. **May miss opportunities**: Too many conditions
2. **High stoploss**: 13.9% significant
3. **Few signals**: Many filters reduce frequency
4. **Very aggressive trailing**: 30% offset extreme

### 😇 Personality Portrait

> "This is a 'cautious detective' — needs multiple pieces of evidence before acting. Won't rush in — waits for all clues to align. Sometimes misses opportunities — but when acts — usually right!"

---

## 7. Bottom Line: How's This Strategy Really?

### One-Sentence Review
> "This is a 'cautious detective strategy' — I need RSI to prove itself 5 times before I buy. Patient! But cost: may miss opportunities — 13.9% stoploss — very aggressive trailing."

### Who Should Use It?
- ✅ Patient traders (can wait for confirmations)
- ✅ Trend chasers (32.5% target for big moves)
- ✅ Those who like momentum confirmation
- ✅ Traders who can accept fewer signals
- ✅ Those with high risk tolerance

### Who Should NOT Use It?
- ❌ Impatient traders (too many conditions)
- ❌ Want frequent trading (few signals)
- ❌ Low risk tolerance (13.9% stoploss)
- ❌ Can't accept missing opportunities
- ❌ Prefer simple strategies

---

## 8. ⚠️ Risk Reminder

### Key Risks

1. **May miss bottoms**: By time 5 candles rise — price already moved
2. **High stoploss**: 13.9% can hurt
3. **Extreme trailing**: 30% offset may give back too much
4. **Few signals**: May have long dry periods

### Final Advice

> "This strategy is for PATIENT traders! If you can wait for perfect setups — and want to catch big trends — this may work. But if you like frequent action — look elsewhere!"

---

## Summary

BBlower is a **patient — momentum-confirmed** oversold rebound strategy. Core value:

1. **RSI confirmation**: 5-candle rise filters false signals
2. **Multi-level confirmation**: Multiple conditions increase quality
3. **High profit targets**: Designed for big trends

But remember: **Patience required!** May miss some opportunities — but when signals fire — higher quality!

---

*This document is based on strategy code*
