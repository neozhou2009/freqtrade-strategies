# NostalgiaForInfinityX2 — Strategy Explained (Plain English)

> **Nickname**: The "Patient Hunter" / Trend Watcher / Super Conservative  
> **Timeframe**: 5 minutes (main) + 15m/1h/4h/1d (auxiliary observation)

---

## 1. What Is This Strategy?

In simple terms, **NostalgiaForInfinityX2** is a:
- 🎯 **Wait for trend confirmation → then wait for oversold** — look first, then shoot
- 🔬 **Multi-timeframe cross-verification** — 5m AND 1h trends must agree, double insurance
- 💰 **26-level dynamic profit-taking** — higher profit = more aggressive exit, never let gains evaporate
- 🛡️ **Four-layer safety net** — hard stop + trailing + dynamic exit + slippage protection

Like a **veteran hunter** — won't shoot at just any movement. First confirms wind direction (trend), then waits for prey to get close enough (oversold), then steadily takes the shot. 🦌

---

## 2. Core Configuration

### Profit-Taking (ROI)

```
Immediate:  10% → sell!
After 30m:  5% → sell!
After 60m:  2% → sell!
```

**Translation**: **Fast in, fast out, lock in profits.** Made 10% right away? Take it! Held for 30 minutes, 5% is fine! Past an hour, 2% is acceptable!

### Stop Loss

```
Hard stop:     -10% (final defense, admit defeat)
Trailing:      Activates at 3% profit, exits on 1% drawdown
Emergency:     -5% (middle warning, retreat first)
```

**Translation**:
- **Down 5%**: Situation not looking good, retreat partially
- **Down 10%**: Complete surrender, this trade is done
- **Up 3%**: "Profit protection mode" activates — if price pulls back 1%, lock in and run

**Example**: Bought, rose to +5%, pulled back to +4% → trailing triggers (dropped 1% from +5%), exit at +4%.

---

## 3. The ONE Buy Condition

Yes, this strategy has **just 1 buy condition**! But it's carefully designed:

### The Only Entry: Multi-Timeframe Golden Cross + RSI Oversold

```python
SMA_50 > SMA_200 on 5 minutes  # 5m trend is up
SMA_50 > SMA_200 on 1 hour     # 1h trend is up
RSI_14 < 30.0                   # RSI oversold
volume > 0                       # Data is valid
```

**Plain English Translation**:
> "I'm a cautious person, very cautious. I won't even look at a coin unless SMA50 is above SMA200 on BOTH the 5-minute AND 1-hour charts. And I won't buy yet even then! I wait until RSI drops below 30. Only then do I enter. Steady and stable, never chase!"

**Why this design?**

| Design Element | Reason |
|---------------|--------|
| Dual-timeframe verification | Prevents false signals from 5m alone |
| RSI < 30 | Oversold means better entry price |
| SMA golden cross | Only trade in confirmed uptrends |

---

## 4. Slippage Protection: >3.8% Slip = No Trade

Every order is checked before execution:

| Slippage | Action |
|----------|--------|
| < 3.8% | Allow trade |
| ≥ 3.8% | Cancel trade + warning |

**Plain English**:
> "Wait, the actual price is 4% higher than expected? Something's fishy — low liquidity or someone manipulating? No buy, retreat!"

**Why 3.8%?** Normal situations should be < 1%. This threshold catches real problems like small coin pumps or exchange lag.

---

## 5. Sell Logic: The Real Innovation

If the buy condition is "conservative," the sell logic is **flashy and meticulously designed**!

### 26-Level Dynamic Profit-Taking

**In a Strong Market (Price above SMA200_1h)**:

```
Profit 0.1%–1%:   RSI < 26 → sell!  (Tiny profit = very conservative)
Profit 1%–2%:     RSI < 30 → sell!
Profit 2%–3%:     RSI < 32 → sell!
Profit 3%–4%:     RSI < 34 → sell!
...
Profit 10%–12%:  RSI < 48 → sell!
Profit 12%–20%:  RSI < 46 → sell!  (High profit = more sensitive)
Profit >20%:      RSI < 44 → sell!  (Made enough = lock it fast)
```

**In a Weak Market (Price below SMA200_1h)**: Thresholds slightly higher (more conservative).

**The Smart Part**:
- Profit 0%–12%: RSI threshold gradually rises (26→48) = more patient with profits
- Profit 12%+: RSI threshold actually drops (48→44) = **faster exit when making big money**

This counterintuitive design means: **Made big money? Exit faster — don't let it evaporate!**

---

## 6. Base Sell Signals (8): Extreme Situations = Run

1. **#1**: RSI > 78 + 5 consecutive candles above BB upper → "Way too overbought, RSI ~78, this is crazy — RUN!"
2. **#3**: RSI > 81 → "RSI over 81! Whatever, just run!"
3. **#4**: 5m AND 1h RSI both > 77 → "Both timeframes overbought — resonance signal, more reliable, exit!"
4. **#7**: 1h RSI > 79 + EMA12 crosses below EMA26 → "Hourly overbought + death cross — classic reversal!"

---

## 7. Strategy Pros & Cons

### ✅ Pros

1. **Rigorously trend-confirmed**: Dual SMA cross = no counter-trend trades
2. **Smart profit-taking design**: 26 levels + RSI = profits don't evaporate
3. **Complete risk control**: 4 layers of defense
4. **High entry quality**: Waits for perfect conditions
5. **Clean code**: Timeframe modules clearly organized

### ⚠️ Cons

1. **Only 1 buy condition**: Not many opportunities — might watch others profit while you wait
2. **Data overkill**: BTC data and multiple timeframes computed but barely used
3. **Choppy market struggles**: SMA filter blocks most entries
4. **Hardware demands**: Multi-timeframe data needs decent VPS RAM
5. **New coins can't use it**: Needs 480 candles of history

---

## 8. ⚠️ Risk Reminder

**Backtests beautiful — live trading needs extreme caution!**

> The buy condition depends on SMA golden cross + RSI < 30. This easily "fits" the best historical entries, but live markets don't cooperate as neatly.

```
1. Run backtests first — at least 3–6 months of data
2. Test with paper trading 1–2 weeks before going live
3. Pair with other strategies — this one alone has few signals
4. Watch BTC direction — while BTC data isn't used in the code, it's smart to follow
5. Accept low trading frequency — this is a trend strategy, not a scalper
```

**Remember**: This strategy is a tool. The market is always the boss. Small position testing, survival first! 🙏
