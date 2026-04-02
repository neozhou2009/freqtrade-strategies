# BinHV27: Waiting for That One Big Double — Violent Rebound Seeker!

> **Nickname**: Double-or-Nothing Freak / 100% Target Aficionado / Oversold Catcher  
> **Vibe**: Ultra-patient hunter who only hunts extreme oversold setups  
> **Timeframe**: 5 minutes  
> **Core**: Dual MA crossover + ADX momentum confirmation + RSI oversold + 100% take-profit target

---

## 1. What's This Strategy All About?

Simply put, **BinHV27** is a strategy that:
- Only considers buying when RSI drops below 20 (extreme oversold)
- Aims for **100% returns (doubling)** — not 20%, 100%!
- Enters at the precise moment a trend is about to reverse, then waits it out

Think of it as a super-patient hunter:

> "No rush. The worse it falls, the better the rebound. Either I don't make a move, or when I do, I'm going for the double. No compromise!"

This strategy comes from the Slack community's guru **BinH**, representing the HV (High Volatility) series. HV series' shared traits:
- High targets (go big or go home)
- Strict conditions (nothing less than extreme oversold)
- Infinite patience (won't leave without 100%)

---

## 2. Core Settings: Either Double or Lose 10%

### Take-Profit (ROI Table)

```python
minimal_roi = {"0": 1}  # Hold for any duration → Sell at 100% profit!
```

**Translation**: This strategy is greedy beyond belief! Goes for the double right from the start. No matter how long it holds, must make 100% to leave. Can't reach it? Keep holding 😏

> "20%? 30%? Not interested! We want 100%!"

### Stop-Loss

```python
stoploss = -0.10  # Fixed 10% stop-loss
```

**Translation**: Maximum loss is 10%. If it drops 10% after buying, admit defeat and exit without hesitation.

### Timeframe

```python
timeframe = '5m'  # 5-minute candles
```

Suited for intraday trading and quickly validating strategy effectiveness.

---

## 3. The 4 Buy Conditions: Base + Categorized

### 3.1 Base Conditions (5 must ALL be satisfied)

Before buying, must pass these 5 gates:

| # | Condition | Plain English |
|---|-----------|---------------|
| 1 | slowsma > 0 | 240-period SMA above zero (long-term trend up) |
| 2 | close < highsma | Price below 120-period EMA (relatively low) |
| 3 | close < lowsma | Price below 60-period EMA (further confirming low) |
| 4 | minusdi > minusdiema | DI- crosses above its 25-period EMA (downward momentum weakening) |
| 5 | rsi >= rsi.shift() | RSI rising (oversold condition improving) |

**Plain English Summary**:
> "Long-term trend is still rising, but price has dropped below the short-term MAs, and downward pressure is easing, and RSI is starting to recover — interesting!"

### 3.2 Categorized Conditions (ANY ONE of these 4 scenarios works)

After passing the base conditions, must satisfy ONE of these:

---

#### 🎯 Scenario A: Rebound in Downtrend (ADX > 25)

```
Base conditions + ALL of the following:
- No trend reversal signal (preparechangetrend = False)
- Short-term MAs haven't confirmed rise (continueup = False)
- ADX > 25 (some trend strength)
- Bearish alignment (fastsma < slowsma)
- EMA(RSI) <= 20 (extreme oversold)
```

**Plain English**:
> "Still falling, but can't fall anymore, RSI is at 20, ADX shows a trend — gotta bounce, right?"

---

#### 🎯 Scenario B: Already Mini-Rebounded in Downtrend (ADX > 30)

```
Base conditions + ALL:
- No trend reversal signal
- Short-term MAs have risen (just rebounded)
- ADX > 30 (stronger trend)
- Bearish alignment
- EMA(RSI) <= 20
```

**Plain English**:
> "Still technically down, but there's a mini-rebound happening, ADX is stronger (>30) — we're good!"

---

#### 🎯 Scenario C: Pullback in Uptrend (ADX > 35)

```
Base conditions + ALL:
- Short-term MAs not continuously rising (just pulled back)
- ADX > 35 (strong trend confirmed)
- Bullish alignment (fastsma > slowsma)
- EMA(RSI) <= 20
```

**Plain English**:
> "Pulling back after a rally is normal — RSI is at 20 now, ADX is still strong (>35) — opportunity!"

---

#### 🎯 Scenario D: Minor Pullback in Uptrend (ADX > 30)

```
Base conditions + ALL:
- Short-term MAs continuously rising
- ADX > 30
- Bullish alignment
- EMA(RSI) <= 25 (slightly relaxed)
```

**Plain English**:
> "In an uptrend, a bit less extreme RSI (<25) is acceptable — trend is still there, ADX is strong enough!"

---

## 4. Protection Mechanisms: Triple Insurance

This strategy has extremely high requirements for oversold conditions, with triple protection:

| Protection Layer | Condition | Meaning |
|----------------|-----------|---------|
| **RSI Oversold Protection** | EMA(RSI) <= 20 or 25 | Must be extremely oversold to enter |
| **ADX Trend Protection** | > 25/30/35 | Must have trend strength, can't be a ranging market |
| **RSI Trend Protection** | RSI >= last candle | RSI must be improving, not getting worse |

**Plain English**:
> "Want to buy? Not so fast! RSI must drop below 20, ADX must show trend strength, AND RSI must be rising — three conditions, missing one means no buy!"

---

## 5. Exit Logic: 5 Scenarios Trigger Exit

### 🚪 Exit 1: Price Rebounded, But Trend Still Bearish

```
- Trend reversal not confirmed
- Short-term MAs haven't risen
- Price bounced above MAs
- But still bearish alignment
```

**Plain English**:
> "Price did bounce, but the long-term MAs are still below — bearish hasn't changed, get out!"

---

### 🚪 Exit 2: Broke the High, But Looking Shaky

```
- Trend reversal not confirmed
- Short-term MAs haven't risen
- Price broke above 120-day EMA
- RSI >= 75 OR just broke 240-day SMA
- Still bearish alignment
```

**Plain English**:
> "Price went up, but RSI has surged to 75 — this is a top signal! And the long-term MAs are still bearish... seems fake."

---

### 🚪 Exit 3: RSI Exploded in Bullish Trend

```
- Trend reversal not confirmed
- Price broke above 120-day EMA
- ADX > 30
- RSI >= 80 (extremely overbought!)
- Bullish alignment
```

**Plain English**:
> "Was going up great, but RSI hit 80 — that's crazy! ADX is strong too, might pull back!"

---

### 🚪 Exit 4: Momentum Exhausted After Trend Reversal

```
- Trend reversal confirmed
- Short-term MAs stopped rising
- Upward momentum slowing
- RSI >= 75
```

**Plain English**:
> "Trend reversal was confirmed, but upward momentum is clearly running out of steam, RSI is overbought — time to go!"

---

### 🚪 Exit 5: DI Death Cross Confirmed

```
- Trend reversal confirmed
- DI- crosses below DI+ (death cross)
- Price above 60-day EMA
```

**Plain English**:
> "DI formed a death cross — it's going down! Get out!"

---

## 6. The Strategy's "Personality"

### 🧠 Personality Profile

| Trait | Description |
|-------|-------------|
| **Patience** | Extremely patient, can wait for 100% returns |
| **Conservative** | Only enters at extreme oversold |
| **Trend Follower** | Relies on trend reversal signals, not random bottom fishing |
| **Greedy** | Aims for the double, not small gains |
| **Cautious** | ADX filters ranging markets, won't trade frequently |

### 🗣️ The Strategy's Inner Monologue

> "Fall? Keep falling! RSI is at 10 and still no bounce? Fine, I wait!
>
> What? RSI is starting to recover? ADX is up too? Trend is about to reverse?
>
> ALL IN! Target: double! Won't leave without 100%!
>
> What? RSI hit 80? ADX starting to weaken?
>
> Running! Next one!"

---

## 7. When to Use It?

| Market Environment | Suitability | Notes |
|-------------------|-------------|-------|
| 📉 **Post-Crash Rebound** | ★★★★★ | Perfect! RSI oversold + trend reversal |
| 🔄 **Trend Reversal Point** | ★★★★☆ | preparechangetrend catches it precisely |
| 📈 **Pullback in Uptrend** | ★★★★☆ | Scenarios C/D suitable |
| 📊 **Ranging Market** | ★☆☆☆☆ | 100% target unattainable, ADX won't pass |
| ⚡️ **Low Volatility** | ★☆☆☆☆ | Insufficient volatility to reach 100% |
| 🌙 **Trending Down** | ★☆☆☆☆ | Don't use — will get stopped out repeatedly |

---

## 8. Summary: What's the Verdict?

### One-Line Rating

> **BinHV27 = Extreme Oversold + Trend Reversal + Target: Double**

### Who's It For?
- ✅ Traders with high risk tolerance
- ✅ Investors who can hold positions for a long time waiting for big reversals
- ✅ Quantitative traders seeking high returns and willing to accept high volatility
- ✅ Veterans who understand dual MAs and ADX

### Who's It NOT For?
- ❌ Newbies (too aggressive, easy心态崩溃)
- ❌ Impatient people (can't wait for the double)
- ❌ Conservative investors (target is outrageous)
- ❌ Low-volatility market players (never reach the target)

### Strengths

1. Strict conditions, won't buy randomly
2. Precise trend reversal capture
3. Concise code, easy to understand
4. ADX filters ranging markets, high signal quality

### Weaknesses

1. 100% target unattainable in most situations
2. May hold positions for a very long time
3. Easy to miss small-to-medium rebound opportunities
4. Fixed stop-loss with no flexibility

---

## 9. ⚠️ Final Warning (Must Read!)

### 100% Target Is Hard to Reach

> **In most market environments, 100% returns are extremely rare. You may hold for a long time, and in the end get stopped out.**

This isn't alarmist:
- 30–50% rebounds after a crash are common
- 100% rebound? That's a true violent reversal
- Most of the time, you'll exit on sell signals or stop-loss

### May Hold Positions for a Long Time

If the market doesn't rebound:
- You'll keep holding
- Could be weeks or even months
- This demands a lot from capital management and mental endurance

### Fixed Stop-Loss Has No Flexibility

No custom stop-loss logic — losses are losses:
- In extreme conditions, losses may exceed 10% (slippage)
- No trailing stop to protect profits

### For High Risk Takers Only

This is a "either会所嫩模 or下海干活" strategy:
- Don't try it without the skills
- Test with small capital first
- Try lowering the ROI first

### My Advice

```
1. Lower the ROI first: 100% → 20–30%, ensure you can make money first
2. Set max loss: Don't actually let it lose 10%
3. Pick the right market: Only use it after crashes
4. Test with small capital: Scale up only after confirming effectiveness
5. Be prepared for long holds: Might wait a long time
6. Never invest more than you can afford to lose
```

---

**Final Note**: No matter how good a strategy is, the market won't warn you before teaching you a lesson. Extreme oversold doesn't equal a bottom, 100% target doesn't equal reality. Test with small positions — survival is what matters! 🙏
