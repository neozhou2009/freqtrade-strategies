# Combined_Indicators Strategy: Two Old Masters "Team Up"

> **Nickname**: Twin Swords Combined, Short-Term Harvester
> **Profession**: 1-Minute High-Frequency Trader
> **Timeframe**: 1 Minute (so fast your eyes can't keep up)

---

## 1. What's This Strategy?

Simply put, **Combined_Indicators** is a "two old masters team up to make money" strategy.

It forcibly combines two classic strategies:
- **BinHV45**: The old hand at Bollinger Band 40-period rebounds
- **ClucMay72018**: The low-volume breakout player at Bollinger Band 20-period + volume

Both strategies can compete on their own. Together, it's "twin swords combined" to improve success rate.

Like forming a **CP in a game** — one handles damage, one handles support, cooperate to defeat monsters 🎮

---

## 2. Core Settings: "Take the Money and Run"

### Take-Profit Rules (ROI Table)

```python
minimal_roi = {
    "0": 0.015  # Made 1.5%? Out immediately!
}
```

**Translation**: As long as you're up 1.5%, without a word, close and leave. This is classic "fast in, fast out" — don't be greedy, make a little and run, accumulate over time.

### Stop-Loss Rules

```python
stoploss = -0.0658  # Cut at 6.58% loss
```

**Translation**: You can lose 6.58%, but if this triggers, the trade is already dead.

### Trailing Stop Rules

```python
trailing_stop = True
trailing_stop_positive = 0.0198        # Starts tracking at 1.98% profit
trailing_stop_positive_offset = 0.03082  # Activates officially at 3.082%
trailing_only_offset_is_reached = True   # Must reach 3.082% first
```

**Translation**:
- At 1.98% profit, trailing stop just "watches"
- Only continues to 3.082% does it start working for real
- Then if it drops 1.98% from the high, immediately run

Plain English: **Let the bullet fly first, when it reaches 3%, start providing protection**

---

## 3. Two Buy Conditions: Let Me Sort Them Out

This strategy has just two buy conditions, simple and brutal:

### 🎯 Category 1: BinHV45 Rebound Signal (1 Condition)

**Core Logic**: Price shows "braking" near the Bollinger lower band, ready to rebound

**Plain English**:
> "Price has dropped to the Bollinger lower band, and the last candle had a very short lower wick — means there's capital buying the dip! This is the rebound signal I want!"

**Specific Conditions**:

```python
dataframe['lower'].shift().gt(0)  # BB lower band exists
dataframe['bbdelta'].gt(dataframe['close'] * 0.00703)  # BB width needs to be sufficient
dataframe['closedelta'].gt(dataframe['close'] * 0.01476)  # Price fluctuation needs to be big
dataframe['tail'].lt(dataframe['bbdelta'] * 0.03632)  # Lower wick needs to be short
dataframe['close'].lt(dataframe['lower'].shift())  # Close below lower band
dataframe['close'].le(dataframe['close'].shift())  # No new highs
```

**Classic Line**:
> "Price dropped to the Bollinger lower band, and the lower wick is so short — this has potential! Buy!"

---

### 🎯 Category 2: ClucMay72018 Low-Volume Breakout Signal (1 Condition)

**Core Logic**: Volume shrank to the extreme — if price is still dropping, it's the "last fall"!

**Plain English**:
> "Volume has shrunk to the point where even mom doesn't recognize it (only 1/34th of normal), and price is still making new lows? This must be 'can't fall further' — rebound incoming!"

**Specific Conditions**:

```python
dataframe['close'] < dataframe['ema_slow']  # Price below 50-period MA
dataframe['close'] < 0.98863 * dataframe['bb_lowerband']  # Price below BB lower band
dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 34)  # Volume extremely contracted
```

**Classic Line**:
> "Low volume low price! Volume so low someone is still selling? Clearly can't sell anymore — prepare to bottom-fish!"

---

## 4. The Difference Between Two Buy Conditions

| Comparison | BinHV45 Rebound | ClucMay72018 Low Volume |
|-----------|-----------------|------------------------|
| **Focus** | Candle pattern | Volume |
| **BB Period** | 40 periods | 20 periods |
| **Easier to Trigger** | When volatility is high | When volatility is very low |
| **Style** | Aggressive | Conservative |

**My Assessment**: These two conditions are like "red face" and "white face" in Chinese opera — one sings bullish, one sings bearish, but the goal is the same — make money for your position.

---

## 5. Exit Logic: Simpler Than Entry

### 5.1 Take-Profit: 1.5% and Out

```python
minimal_roi = {"0": 0.015}
```

**Plain English**: Make 1.5% and leave, never be greedy!

### 5.2 Trailing Stop: Let Profits Run

Only when price rises to 3.082% does the "protection mechanism" activate — if it drops 1.98% from the high, run.

### 5.3 Sell Signal: Break Above Bollinger Middle Band

```python
dataframe['close'] > dataframe['bb_middleband']
```

**Plain English**: Price breaks the 20-period Bollinger middle line (20-period MA) — short-term might turn from down to up, time to run.

---

## 6. The Strategy's "Personality Traits"

### ✅ Pros

1. **Double Insurance**: Two strategies — if either is satisfied, can enter; higher success rate
2. **Fast Mover**: 1-minute framework, short holding time, high capital utilization
3. **Volume Filtering**: That 34x volume requirement in ClucMay72018 is really strict — filters most false signals
4. **Multi-Layer Protection**: ROI + trailing stop + hard stop — layered protection

### ⚠️ Cons

1. **Fee Eater**: 1-minute framework trades dozens of times — fees cut into your flesh! 💸
2. **Slippage Master**: You want to limit buy? Might not fill at all
3. **Too Many Magic Numbers**: Those 0.00703, 0.01476, 0.03632, 34, 0.98863... who knows how they were tuned
4. **Will Fail in Trending Markets**: This is a mean-reversion strategy — gets killed in continuous up or down trends

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|---------------------|--------|
| 📊 Consolidation | Go all in | Strategy's home turf |
| 📈 Uptrend | Reduce positions | Logic may conflict with trend |
| 📉 Downtrend | Be careful | Might be a pause in downtrend |
| ⚡ Wild Fluctuation | Don't use | Too much noise, signals unreliable |

---

## 8. Summary: How Good Is This Strategy Really?

### One-Line Verdict
> "Two old masters team up, high-frequency wool harvesting, but flips in trending markets"

### Who Should Use It?
- ✅ People who like high-frequency trading, short holding periods
- ✅ "Whales" with low fee channels
- ✅ People who accept "accumulating small gains" not "all in one go"
- ✅ People confident in consolidation markets

### Who Should NOT?
- ❌ "Suckers" with high fees (profits eaten)
- ❌ Trend followers, long-term holders
- ❌ Impatient people who don't want high-frequency monitoring
- ❌ People with small capital (fees too high a percentage)

---

## 9. What Markets Does This Strategy Make Money In?

### 9.1 Core Logic: Building a "Defense Net" with "Rebound" and "Low Volume"

Combined_Indicators' core idea is simple:
- Price falls too much → rebounds (mean reversion)
- Volume shrinks too much → reverses (low volume low price)

These two logics are both strong on their own. Combined together means **improving signal reliability**.

**Its Money Philosophy**:
- **Don't chase highs**: Only do oversold rebounds, don't chase
- **Wait for volume shrinkage**: No volume contraction, ignore the rebound
- **Run fast**: Make 1.5% and out, never attached

### 9.2 Performance by Market (Plain English)

| Market Type | Rating | Plain English |
|:------------|:-------|:--------------|
| 📈 Uptrend | ⭐⭐☆☆☆ | You're doing rebounds, market is rising — this wave you won't outrun |
| 📉 Downtrend | ⭐⭐⭐☆☆ | Short-term rebounds possible, but getting slapped in continuous drops |
| 🔄 Consolidation | ⭐⭐⭐⭐⭐ | Strategy's home turf! Up and down, you harvest repeatedly |
| ⚡ Wild Fluctuation | ⭐⭐⭐☆☆ | Too many signals, lots are fake, needs stricter filtering |

**Bottom Line**: Built for consolidation markets, gets wiped out in trending markets.

---

## 10. ⚠️ Risk Re-Emphasis (Must Read!)

### Backtesting Looks Great, Live Trading Is Different

Combined_Indicators' historical backtesting looks "okay" — but that's because:

1. **1-minute framework has too many signals** — any fitting produces good results
2. **Too many magic numbers** — easily "coincidentally" fit certain market periods
3. **Fees not counted** — many backtest at 0% fees, live loses big

Simply put: **Backtesting profit doesn't mean live trading profit, historical performance doesn't predict future results**

### Hidden Risks of High-Frequency Strategies

1. **Fees eat profits**: Trade 50 times at 0.1% fee each = 5% gone
2. **Slippage eats profits**: 1-minute framework slippage can start at 0.5%
3. **API Rate Limiting**: High-frequency calls may get your IP banned by exchange
4. **Psychological Pressure**: Fifty trades a day, wrong calls blow up your mind

### My Suggestions

```
1. Paper trade for a month first, observe real fees and slippage
2. Set reasonable fee assumptions (at least 0.1% per trade)
3. Start with small money, don't start with your life savings
4. Watch market conditions, use during consolidation, stop when trends start
5. Be ready to stop out — this strategy will lose continuously in extreme markets
```

**Remember**: High-frequency strategy's core is **stability**, not **big profits**. Surviving is more important than making fast money!

---

**Final Reminder**: 1-minute strategy looks cool, but reality is cruel. Fees, slippage, API limits will teach you lessons personally. Test with small positions, survival matters! 🙏

---

*This document is for entertainment and learning reference only, not investment advice.*
