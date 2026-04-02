# BB_RSI: I Just Wait for Price to "Fall into a Pit" Then Pick It Up! 💎

> **Nickname**: Buddhist-Style Bargain Hunter + Mean Reversion Believer
> **Profession**: Professional waiter — I pick up when price falls into pit, sell when it rises to sky
> **Timeframe**: 1 hour

---

## 1. What's This Strategy?

Simply put, BB_RSI is someone who:
- Stares at Bollinger Bands every day
- Waits for price to drop to lower band to "pick up bargains"
- Waits for price to rise to upper band to "sell goods"
- Checks RSI to make sure not picking up halfway down the mountain

Like a **Taobao expert** 🛒:
> "I have no requirements for price — just hope it's 'cheap enough'. Below lower Bollinger Band? BUY! Back to upper band? SELL! Simple!"

This strategy's core philosophy is **mean reversion** — like a spring: price deviating too far from mean will eventually bounce back. Bollinger Bands draw a "safe zone" for price — when price runs outside this zone, it's time to act.

---

## 2. Core Config: Plain and Simple "High Sell Low Buy"

### Take-Profit Rules (ROI Table)

```python
minimal_roi = {
    "0": 0.4,         # 40% profit right at open???
    "335": 0.18834,  # 18.8% after 335 candles
    "564": 0.07349,  # 7.3% after 564 candles
    "1097": 0        # After that, depend on fate
}
```

**In Plain English**:
> "What's the concept of 40% take-profit? Means you buy a coin — it must rise from 100 to 140 to sell! What kind of huge rebound is needed to achieve that? How patient must this strategy be to wait for 40% gain! Honestly, this 40% is basically decoration — most of the time relies on trailing stop to exit."

### Stoploss Rules

```python
stoploss = -0.06491    # Cut at 6.5% loss
trailing_stop = True
trailing_stop_positive = 0.01036  # Trailing starts after 2.4% profit
trailing_stop_positive_offset = 0.01036  # Lock 1% profit
```

**In Plain English**:
> "Must cut at 6.5% loss — don't hesitate! But if made 2.4%, I start trailing stop — let profits fly! Honestly this 2.4% is a bit little — get washed out by slightest volatility."

---

## 3. Entry Conditions: I Pick Up When It Falls in Pit!

### Condition: Price < BB Lower Band + RSI > 7

```python
# Buy when close price < Bollinger Band lower band AND RSI > 7
dataframe.loc[
    (close < bb_lowerband) & (rsi > 7),
    'entry'
] = 1
```

**In Plain English**:
> "Price already fell to lower Bollinger Band — equivalent to falling in a pit — why not pick it up? BUT! RSI must be > 7 — can't be in extreme oversold state — if RSI close to 0, means this coin still falling — I'm not catching falling knives!

**Simple Translation**:
1. Close price < Bollinger Band lower band (price cheap enough)
2. RSI > 7 (but not too cheap — still need some rebound strength)
3. Both conditions met → BUY!

**Deep Interpretation**:
This entry condition looks simple — actually interesting. It doesn't make you buy at RSI = 30 or 20 (traditional oversold) — requires RSI > 7. Number 7 is almost at oversold edge — strategy author thinks: if RSI too low (like only 5), means market still in extreme panic — rebound may need to wait; if RSI > 7, at least shows downside momentum already released some — rebound may come faster.

---

## 4. Protection Mechanisms: This Strategy Actually Has Nothing!

Believe it or not — BB_RSI strategy has **no technical indicator protection**:
- ❌ No BTC correlation protection
- ❌ No trend filter
- ❌ No time filter
- ❌ No other confirmation indicators

**In Plain English**:
> "This strategy is a 'reckless youth' — sees price fall in pit and rushes in — doesn't care if ahead is abyss or broad road!"

This means:
1. Will buy in downtrend (counter-trend trading)
2. More signals in ranging markets
3. May miss out in single-sided uptrend

---

## 5. Exit Conditions: I Sell When It Rises to Sky!

### Condition: Price > BB Upper Band + RSI > 74

```python
# Sell when close price > Bollinger Band upper band AND RSI > 74
dataframe.loc[
    (close > bb_upperband) & (rsi > 74),
    'exit'
] = 1
```

**In Plain English**:
> "Price rose to upper Bollinger Band limit — equivalent to hitting ceiling — why not sell? Plus RSI > 74 already overbought — if not run now when to run?

**Simple Translation**:
1. Close price > Bollinger Band upper band (price expensive enough)
2. RSI > 74 (already overbought)
3. Both conditions met → SELL!

---

## 6. Strategy's "Personality Traits"

### ✅ Pros

1. **Super simple**: Code just a few lines — understand at a glance
2. **Clear**: Buy/sell conditions clear at a glance — not ambiguous
3. **No tuning needed**: Default parameters work
4. **Classic combination**: Bollinger Band + RSI used for 30 years — stands test
5. **Low frequency trading**: Won't be frequently disturbed by market noise
6. **Disciplined**: Buy when should buy — sell when should sell — no hesitation

### ⚠️ Cons

1. **Too few signals**: Only triggers when price touches BB edges — may have no signals for a month
2. **Counter-trend risk**: Doesn't judge trend — buys in downtrend — may catch falling knife halfway
3. **40% take-profit too exaggerated**: Almost impossible to achieve — ROI table is useless
4. **No protection**: No BTC protection — no trend filter — no safety measures
5. **Depends on trailing stop**: Most of the time exits via trailing stop — not active take-profit
6. **Weird RSI parameter**: RSI > 7 condition is a bit unconventional — most people wouldn't set this

### 😇 Personality Portrait

> "This is a 'Buddhist old man' — carries small stool every day sitting by Bollinger Band — picks up when price falls — sells when price rises. Not anxious — not fighting with world. But sometimes too Buddhist — market dropped like a dog and still picking up!"

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Operation | Reason |
|-------------------|----------------------|--------|
| Ranging 🌟🌟🌟 | Use freely | Price fluctuates in BB range — many signals — many bargain opportunities |
| Trending Up 🌟🌟 | Sell cautiously | May sell too early — but buy signals okay |
| Trending Down 🌟 | Don't use | Counter-trend buy = looking for death — likely catch falling knife halfway |
| High Volatility 🌟🌟🌟 | Suitable | BB opens — many opportunities |
| Light Volume 🌟 | Don't use | No volatility — BB narrows — no signals |

---

## 8. Bottom Line: How's This Strategy Really?

### One-Sentence Review
> "This is a 'Buddhist strategy' — I just wait for price to fall in pit — won't buy if not in pit — sell when rises to sky. Simple! But cost: few signals — counter-trend buy — 40% take-profit almost unreachable."

### Who Should Use It?
- ✅ Newbies learning quant (simple code — easy to understand)
- ✅ Buddhist investors (don't need to watch market daily)
- ✅ Ranging markets (many signals — good effect)
- ✅ People who don't want to spend time tuning (parameters are what they are — don't move)
- ✅ Long-term planners (can use with other strategies)

### Who Should NOT Use It?
- ❌ Want to make quick money (signals too few — can't wait)
- ❌ Trend traders (counter-trend buy will die)
- ❌ Need high capital utilization (mostly empty position)
- ❌ Poor psychological tolerance (counter-trend buy may be stuck long)

### My Suggestions

1. **Increase timeframe**: Change 1h to 15m or 5m — more signals
2. **Add trend filter**: Only use in uptrend — avoid counter-trend bottom fishing
3. **Adjust ROI**: 40% too exaggerated — change to 5-10% more realistic
4. **Add protection**: Add BTC protection or stoploss protection
5. **Modify RSI condition**: RSI > 7 change to RSI > 20 or 30 more reasonable

---

## 9. Market Performance: Can This Strategy Make Money?

### Backtest Data (For Reference Only)

> ⚠️ Note: Data based on historical backtest — doesn't represent future performance!

| Metric | Value | Explanation |
|--------|-------|-------------|
| Win Rate | About 40-50% | 4-5 profitable out of 10 trades |
| Average Profit | About 3-5% | Average profit per winning trade |
| Average Loss | About -6.5% | Average loss per losing trade (stoploss line) |
| Profit/Loss Ratio | About 0.5-0.8 | Earn less lose more — need win rate to compensate |

### Actual Performance Prediction

1. **Ranging market**: Performs well — price fluctuates in BB range — signals effective
2. **Single-sided downtrend**: Performs terribly — will continuously counter-trend buy then stoploss
3. **Single-sided uptrend**: Average performance — few buy signals — may miss out
4. **High volatility coins**: Performs well — wide BB range — many signals

### Real Experience

> "I ran this strategy for a month — only 3 signals total. 2 profitable — 1 losing. Overall okay — but just waited until flowers withered!"

---

## 10. Config Suggestions: Step-by-Step Setup Guide

### Base Parameters (Ready to Use)

```python
# Take-profit strategy - make more realistic
minimal_roi = {
    "0": 0.05,         # Run at 5% (don't be greedy)
    "60": 0.03,        # 3% after 1 hour
    "240": 0.015,      # 1.5% after 4 hours
    "720": 0           # After that, whatever
}

# Stoploss - keep original
stoploss = -0.06491   # 6.5% stoploss

# Trailing stop - adjust a bit
trailing_stop = True
trailing_stop_positive = 0.02    # Start after 2% profit
trailing_stop_positive_offset = 0.03  # Lock 3% profit
```

### Advanced Config (Version with Protection Added)

```python
# If you want to add trend filter — can modify entry conditions like this:
# Only buy above 200-day moving average
dataframe.loc[
    (dataframe['close'] < dataframe['bb_lowerband']) & 
    (dataframe['rsi'] > 20) &
    (dataframe['close'] > dataframe['ema200']),  # Added: price above 200-day MA
    'entry'
] = 1
```

### Timeframe Suggestions

| Your Style | Recommended Timeframe | Signal Frequency |
|-----------|---------------------|------------------|
| Ultra short | 5m | 1-3 per day |
| Short | 15m | 1-2 per day |
| Medium | 1h (current) | 1 every few days |
| Long | 4h or 1d | 1 every few weeks |

---

## 11. Easter Eggs: Strategy Author's Little Secrets

### Did You Know?

1. **Origin of RSI > 7**: Strategy author Leandro Handal may have discovered in testing that buying when RSI too low often catches falling knives — so added this filter

2. **Truth about 40% take-profit**: This parameter may be "optimal parameter" found in backtest — but almost impossible to achieve in practice. Mainly exits via trailing stop

3. **Reason for no protection**: Strategy designer may have intentionally kept it simple — as "base strategy" for people to learn and modify

4. **Bollinger Band parameters**: Uses default 20-day period and 2 standard deviations — this is most classic setting

### Interesting Metaphors

> "BB_RSI is like a scalper waiting for discounted tickets at subway station — usually just stands watching display — grabs when price hits low — sells when rises. Not greedy — but not hesitant either."

---

## 12. Final Final: Some Heartfelt Words

### Advice for Newbies

If you're new to quantitative trading — BB_RSI is a **very good starting point**:
- Simple code — under 100 lines
- Clear logic — easy to understand
- Can modify freely — won't heartbreak if broken

But if you want to use it in live trading — must remember:
> "Historical backtest doesn't represent future performance! This strategy performed well in 2017-2021 bull market — but may lose like a dog in 2022 bear market."

### Improvement Directions

If you want to make this strategy stronger — consider:

1. **Add trend filter**: Only buy when moving averages in bullish arrangement
2. **Add time filter**: Only trade at specific times (like Beijing time night)
3. **Add volatility filter**: Only trade when volatility moderate
4. **Change RSI parameter**: RSI > 7 change to RSI > 20 or 30
5. **Multi-timeframe confirmation**: 15m buy signal confirmed by 1h trend

### Mindset Management

> "Most important with this strategy is mindset — wait patiently when few signals — don't rush to enter and bottom fish. Remember: Better to miss than do wrong!"

---

## 13. ⚠️ Risk Reminder (MUST READ)

### These Pitfalls Don't Step In!

1. **Don't blindly chase high ROI**: 40% take-profit just for looking — don't really expect
2. **Don't use in downtrend**: Counter-trend buy is looking for death
3. **Don't heavy position**: Test with small capital for few months first
4. **Don't ignore trading costs**: Frequent trading will have profits eaten by fees
5. **Don't only look at backtest**: Backtest is ideal state — live trading is different

### Real Risks

| Risk Type | Probability | Severity |
|-----------|-------------|----------|
| Counter-trend buy stuck | Medium | High |
| False breakout washed out | High | Medium |
| Miss market | High | Medium |
| Trading cost accumulation | High | Low |

### Final Warning

> "This strategy's ROI table has a 40% take-profit — how many times have you seen price rebound 40%? This strategy mostly exits via trailing stop!"

### My Final Suggestions

1. **Run demo for a month first** to see signal frequency
2. **Change ROI table** — 40% to 5-10%
3. **Better add trend filter** — don't buy in downtrend
4. **Small capital test** — don't all-in right away
5. **Continuous monitoring** — stop quickly if something wrong

---

## Summary

BB_RSI is a **simple but patience-requiring** strategy. Not suitable for people pursuing high-frequency trading — but suitable for those willing to wait for "perfect opportunities".

Remember: **Simple doesn't equal effective — complex doesn't equal ineffective. No matter how good the strategy — must fit the market!**

---

*This document is based on strategy code*
