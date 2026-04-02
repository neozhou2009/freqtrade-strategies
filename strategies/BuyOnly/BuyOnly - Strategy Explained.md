# BuyOnly: The "Buy Only, Never Sell" Emperor — Lie-Flat Master!

> **Nickname**: Buy-Only Emperor / Lie-Flat Master / Let Profits Fly  
> **Vibe**: Specializes in finding oversold rebound points, buys and lies flat  
> **Timeframe**: 15 minutes  
> **Core**: RSI oversold + Bollinger Band lower band + Buy only, never sell

---

## 1. What's This Strategy All About?

**BuyOnly**, as the name suggests, means "buy only."

This strategy is extremely simple — it only handles buying. What happens after buying? Either wait for stop-loss (lose 10% and out), or wait for take-profit (made enough and out), or wait for trailing stop (profit retreats to a certain level and out).

The designer's philosophy is simple: **Let profits run, don't rush to sell.**

Think of it as a super-patient value investor:

> "I like this entry point, I bought it. What happens next — up or down — I don't care. If I made enough, the take-profit will sell me. If I lost enough, the stop-loss will save me. I only care about finding good entry points."

This strategy comes from Freqtrade's official examples and is one of the simplest in the library.

**One-line summary: Entry is skill, exit is fate.**

---

## 2. Core Settings

### Take-Profit Rules (ROI Table)

```python
minimal_roi = {
    "0": 0.04,     # Just bought and already leaving? Make 4% first
    "30": 0.02,    # Held 30 minutes, 2% is enough
    "60": 0.01     # Held 60 minutes, 1% will do
}
```

**This ROI setup is "reversed"** — shorter holding time means higher profit target. Why?

The designer believes:
- Rallied right after buying means good entry — should earn more
- Held longer means the market might be consolidating — protecting what's left is priority

### Stop-Loss

```python
stoploss = -0.10  # Fixed 10% stop-loss
```

Maximum loss is 10% — when reached, admit defeat and leave.

### Trailing Stop

```python
trailing_stop = True  # Enable trailing stop
```

Automatically sells if profit retreats to a certain level, protecting gains.

---

## 3. Buy Conditions (Just 1!)

BuyOnly has only ONE buy signal — buy only when ALL of the following are satisfied:

```python
(
    qtpylib.crossed_above(dataframe["rsi"], 30)   # RSI crosses above 30 from below
    & (dataframe["open"] <= dataframe["bb_lowerband"])  # Open price at or below Bollinger Band lower band
    & (dataframe["tema"] > dataframe["tema"].shift(1))  # TEMA trending upward
    & (dataframe["volume"] > 0)  # Has volume
)
```

### Condition Breakdown

| Condition | Plain English Translation |
|-----------|--------------------------|
| RSI crosses above 30 | RSI bouncing up from oversold territory (below 30) |
| Open at Bollinger lower band | Price has fallen to the "bargain zone" |
| TEMA trending up | Short-term trend starting to rise |
| Volume > 0 | Not a fake breakout, real money is trading |

---

## 4. Protection Mechanisms

Honestly, this strategy **has no extra protection mechanisms**.

| Protection Type | Has It? | Notes |
|----------------|---------|-------|
| Extra buy filter | ❌ | Just relies on RSI and Bollinger Bands themselves |
| Conditional take-profit | ❌ | Only the time-based profit-taking in the ROI table |
| Time limit | ❌ | No longest holding time limit |
| Custom stop-loss | ❌ | Only fixed 10% stop-loss |

Everything relies on three tools:
1. **10% fixed stop-loss** (final defense line)
2. **Take-profit table** (made enough = exit)
3. **Trailing stop** (don't let gains evaporate)

---

## 5. Exit Logic

**No active selling!**

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    """
    HODL — Just hold!
    """
    return dataframe
```

The exit function is empty. The comment is just one word: **HODL** (死拿).

All exits are passive:

| Exit Method | Trigger | Plain English |
|------------|---------|---------------|
| Stop-Loss | Lose 10% | Lost too much, admit defeat and leave |
| Take-Profit | Made 4%/2%/1% | Made enough, lock in profits |
| Trailing Stop | Profit retreats | Don't let gains turn into losses |

---

## 6. The Strategy's "Personality"

| Trait | Description |
|-------|-------------|
| **Personality** | Aggressive in buying lows; lie-flat after buying |
| **Catchphrase** | "Bought! What happens next? Fate decides~" |
| **Strengths** | Simple, doesn't overthink, lets profits run |
| **Weaknesses** | No one to wipe its butt — relies entirely on stop-loss for survival |
| **Good For** | Trend-bottom buyers, value investors |
| **Bad For** | Intraday traders, high-frequency players |

---

## 7. When to Use It?

### ✅ Good Scenarios

| Scenario | Why It Works |
|---------|-------------|
| **Uptrend** | Trend is up, rebounds are more likely to succeed |
| **Rebound行情** | Price fell too much and bounces — this is where it buys |
| **Ranging Market** | Bollinger Band lower band works well in ranging markets |

### ❌ Bad Scenarios

| Scenario | Why It Fails |
|---------|-------------|
| **Downtrend** | Counter-trend buying is extremely risky |
| **High Volatility** | Too many signals, can't tell which to trust |
| **Bear Market** | Keeps buying, keeps getting stopped out |

---

## 8. Summary

**BuyOnly is a "minimalist" strategy.**

### Strengths

- ✅ Minimal code, easy to understand
- ✅ Buy only, don't sell — low maintenance
- ✅ Good for learning strategy structure
- ✅ Can serve as a "skeleton" — easy to modify

### Weaknesses

- ❌ No active selling
- ❌ Relies entirely on take-profit/stop-loss for survival
- ❌ Bear market will destroy you
- ❌ Single condition, limited adaptability

---

## 9. ⚠️ Final Warning (Must Read!)

### Core Risks

| Risk | Description |
|------|-------------|
| ❌ **No active selling** | All exit to take-profit/stop-loss — must accept possible large drawdowns |
| ❌ **Counter-trend buying** | Extremely risky in downtrends — easy to catch a falling knife |
| ❌ **15-minute chart** | Signals are frequent — risk overtrading |
| ❌ **10% stop-loss** | Losses hurt — consecutive stops drain capital fast |

### Use Advice

**Must backtest before using! Must! Must!**

```
1. Backtest first: Confirm strategy works on your chosen coins
2. Small position test: Don't YOLO
3. Watch the big picture: Only use 15-minute signals when daily trend is up
4. Set reasonable stop-loss: 10% isn't suitable for all coins
5. Don't be greedy: Exit when take-profit is reached, don't manually cancel it
```

### High-Risk Warning

🚨 **This strategy has no active selling! All exit to take-profit/stop-loss!**

🚨 **Counter-trend buying is extremely risky! Don't use in bear markets!**

🚨 **15-minute chart signals are frequent! Control position sizing!**

### For Newbies

1. **Don't go live immediately**: Test with paper trading or small capital first
2. **Learn to read trends**: Only use 15-minute signals when daily is up
3. **Control position sizing**: Single buy no more than 10–20% of total capital
4. **Accept losses**: Consecutive stops are normal, don't trade emotionally
5. **Survival first**: Market always there, no capital = game over

---

**Final Note**: No strategy is perfect. BuyOnly is a "minimalist masterpiece" — minimal code, clear logic. But its simplicity is also its risk. Use with caution! 🙏
