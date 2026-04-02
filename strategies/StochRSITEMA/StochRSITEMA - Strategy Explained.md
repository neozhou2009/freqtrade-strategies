# StochRSITEMA Strategy: The "Cautious Type" with Triple Confirmation

> **Nickname**: Cautious Type, Triple Gatekeeper  
> **Specialty**: Ranging Market Rebound Catcher  
> **Timeframe**: 5 minutes

---

## I. What Is This Strategy?

Simply put, **StochRSITEMA** is:
- A "triple confirmation before entry" cautious player
- Super tight stop-loss (2.2%), runs if wrong
- Uses TEMA line to decide when to leave
- Simple clear logic, no fancy stuff

Like a **club with triple gatekeepers** 🚪🚪🚪 — want in? First pass the RSI gate, then the Stochastic gate, finally K-line golden cross confirmation. Only enter when all pass!

---

## II. Core Configuration: "Quick Stop-Loss + Lock Profits" in Plain Terms

### Take-Profit Rules (ROI Table)

```
Time         Profit Target
────────────────────
Immediate    19.5%
13 minutes   9.1%
36 minutes   2.9%
64 minutes   Close and leave
```

**Translation**: Just got in? Target is 19.5%. The longer you hold, the lower the target — like dating, passionate at first, then "good enough" over time.

### Stop-Loss Rules

```
Hard stop-loss: -2.2% (Very tight!)
Trailing stop: Activates when profit > 17.25%, trailing distance 25.16%
```

**Translation**: Stop-loss is only 2.2%, equivalent to buying $100 worth of stuff and running when it drops to $97.8! Very strict. But if you make over 17%, it starts "watching your back" — sells when price retraces 25% from high, locking in big profits.

---

## III. Buy Conditions: Quadruple "Gatekeeper" Check

This strategy's buy conditions can be summarized in one sentence:

> **RSI looks up first → Stochastic D line crosses up → Stochastic K line crosses up → K golden crosses D → Then enter**

### 🎯 Quadruple Check Detailed

| Checkpoint | Condition | Plain English Translation |
|------------|-----------|---------------------------|
| 1️⃣ RSI Gatekeeper | RSI(15) > 36 | "RSI has climbed out of oversold area" |
| 2️⃣ Stoch D Gatekeeper | slowd crosses above 48 | "Stochastic D line also rising from low" |
| 3️⃣ Stoch K Gatekeeper | slowk crosses above 48 | "K line also rising from low" |
| 4️⃣ Golden Cross Confirmation | K crosses above D | "K line golden crosses D line, trend reversal confirmed!" |

**Classic Dialogue**:
```
RSI: "I'm not oversold anymore!"
Stoch D: "I'm also up from low!"
Stoch K: "Me too!"
K/D Cross: "Golden cross confirmed, let them through!"
→ 🎫 Enter!
```

### Why So Strict?

These four checks all confirm one thing: **Price has rebounded from lows, trend is starting to reverse.**

- Avoid buying mid-downtrend ("catching falling knife halfway")
- Avoid false breakouts ("bounces then continues falling")
- Only enter when multiple indicators resonate

---

## IV. Sell Logic: Three Escape Routes

The strategy gives you three "escape routes":

### 4.1 Route One: TEMA Exit (Trend Reversal)

```
Close price < TEMA(5) → Sell
```

**Plain English**: TEMA is a smoothed trend line. When price breaks below this line, trend has reversed, run!

**TEMA Has Three Trigger Methods** (configurable):

| Method | Condition | Sensitivity |
|--------|-----------|-------------|
| `close` | Close price breaks below TEMA | Most sensitive |
| `both` | Both close and open break below TEMA | More conservative |
| `average` | (Close + Open)/2 breaks below TEMA | Medium |

### 4.2 Route Two: Stop-Loss (Admit Defeat)

```
Loss > 2.2% → Stop-loss sell
```

**Plain English**: Wrong? Admit it, run at 2.2% loss, no arguing.

### 4.3 Route Three: ROI (Target Reached)

```
Profit > 19.5% (or stepped targets) → Sell
```

**Plain English**: Made enough? Call it a day.

### 4.4 Route Four: Trailing Stop (Protect Profits)

```
Profit > 17.25% → Activate trailing stop, sell when 25.16% retracement
```

**Plain English**: If you made a lot, starts "watching your back". Sells when price retraces 25% from high, giving profits enough breathing room.

---

## V. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Section)

1. **Cautious Entry**: Four confirmations before entry, reduces false signals
2. **Strict Stop-Loss**: 2.2% stop-loss, runs if wrong, no dragging feet
3. **Clear Logic**: RSI + Stoch + TEMA, easy to understand
4. **Profit Protection**: Trailing stop helps lock in big profits
5. **Optimized Parameters**: Parameters after hyperparameter optimization

### ⚠️ Cons (Complaint Section)

1. **Stop-Loss Too Tight**: 2.2% may be shaken out by normal volatility
2. **Strict Entry Conditions**: Four confirmations may miss opportunities
3. **Parameters May Be Overfitted**: Optimized parameters may not suit live trading
4. **Single Timeframe**: No higher-dimensional trend judgment

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Ranging Uptrend | ⭐⭐⭐⭐⭐ Recommended | Good at catching rebounds |
| Sideways Range | ⭐⭐⭐⭐☆ Can use | Wait for confirmation signals to enter |
| One-sided Decline | ⭐⭐☆☆☆ Careful | Stop-loss frequently triggered, fees eat profits |
| One-sided Rally | ⭐⭐⭐☆☆ Okay | May miss fast rallies |

**One-sentence Summary**: Ranging market finding rebounds is its home turf, one-sided decline is its nightmare!

---

## VII. What Market Can This Strategy Make Money?

### 7.1 Core Logic: Triple Confirmation + Quick Stop-Loss

StochRSITEMA is a **ranging market rebound-catching strategy**. Its money-making philosophy:

- **Wait for confirmation before entry**: Four checks, no chasing
- **Run quickly if wrong**: 2.2% stop-loss, controllable single loss
- **Exit on trend reversal**: TEMA breakthrough as exit signal
- **Protect big profits**: Trailing stop locks gains

### 7.2 Performance in Different Markets (Human Version)

| Market Type | Rating | Plain English Explanation |
|-------------|--------|---------------------------|
| 📈 Ranging Uptrend | ⭐⭐⭐⭐⭐ | Home turf! Triple confirmation catches rebounds |
| 🔄 Sideways Range | ⭐⭐⭐⭐☆ | Finding support level rebounds, pretty good |
| 📉 One-sided Decline | ⭐⭐☆☆☆ | Stop-loss frequently triggered, fees eat all profits |
| ⚡ Fast Rally | ⭐⭐⭐☆☆ | Four confirmations too slow, might not catch up |

---

## VIII. Want to Run This Strategy? Check These Configurations First

### 8.1 Key Parameters

| Parameter | Default | Suggestion |
|-----------|---------|------------|
| `rsi-lower-band` | 36 | Lower = more aggressive, higher = more conservative |
| `stoch-lower-band` | 48 | Same as above |
| `tema-period` | 5 | Shorter period = more sensitive exit |
| `stoploss` | -0.022 | May need to loosen to -0.03 |

### 8.2 Hardware Requirements

This strategy is simple, low hardware requirements:

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|----------------|-------------------|
| 1-10 pairs | 1 GB | 2 GB |
| 10-30 pairs | 2 GB | 4 GB |
| 30+ pairs | 4 GB | 8 GB |

### 8.3 Backtest vs. Live Trading

Strategy parameters have been hyperparameter optimized, backtest results show:

```
47/50: 19 trades. 7/6/6 Wins/Draws/Losses. Avg profit -0.35%
```

**Warning**: This is backtest data! Live trading may differ:

- **Parameters may be overfitted**: Optimized parameters may only suit historical data
- **Stop-loss too tight**: Live volatility may be greater than backtest
- **Single timeframe**: No higher-dimensional trend judgment

**Recommended Flow**:
1. Backtest with default parameters first
2. Try loosening stop-loss to -0.03
3. Live test with small capital
4. Observe stop-loss trigger frequency
5. Adjust parameters based on actual situation

---

## IX. Parameter Optimization Note

Author wrote in code:

```python
# 47/50:     19 trades. 7/6/6 Wins/Draws/Losses. 
#            Avg profit  -0.35%. Median profit   0.00%. 
#            Total profit -0.00006706 BTC. Objective: 1.98291
```

**Plain English**: This is hyperparameter optimization result, but average profit is negative! This indicates:

1. This parameter combination didn't perform ideally in backtest
2. May need re-optimization
3. Don't blindly trust optimization results

---

## X. Manual Trading Recommendations

If you want to manually use this logic:

### Entry Checklist

```
□ RSI(15) > 36?
□ Stochastic D line crosses above 48?
□ Stochastic K line crosses above 48?
□ K line golden crosses D line?
□ Volume > 0?

All checked → Enter!
```

### Exit Strategy

```
1. Stop-loss: Run at 2-3% loss
2. Trend reversal: Run when price breaks below TEMA(5)
3. Target reached: Take profit when high enough
4. Trailing stop: Start watching when profit > 17%
```

---

## XI. Final Summary

### One-Sentence Review
> "Cautious type with triple confirmation, good at catching rebounds in ranging markets, but stop-loss too tight easily gets shaken out."

### Who Is It For?
- ✅ Ranging market traders
- ✅ Cautious types who like confirmation signals
- ✅ People who can accept 2-3% stop-loss
- ✅ People who like simple logic

### Who Is It NOT For?
- ❌ One-sided bull market chasers
- ❌ People who don't like frequent stop-losses
- ❌ People who like complex strategies
- ❌ Low-volatility market traders

---

## XII. ⚠️ Risk Emphasis Again (Must Read This Section)

### Stop-Loss Too Tight Risk

2.2% stop-loss on 5-minute timeframe is **very easily** triggered by normal volatility. You might encounter:

```
Enter → Get shaken out → Price goes up → "Damn! Got washed out!"
```

**Suggestion**: Loosen stop-loss to 3-5%, or use larger timeframe.

### Parameter Optimization Trap

Parameters in code are hyperparameter optimization results, but:

> **Optimization result average profit is negative (-0.35%)!**

What does this mean? The strategy may:
- Need re-optimization of parameters
- Not suit current trading pair
- Need to be combined with other strategies

### My Recommendations (Honest Words)

```
1. Don't use default parameters directly, re-optimize
2. Loosen stop-loss to -0.03 or -0.05
3. Use larger timeframe (15m or 1h)
4. Only use in clear ranging markets
5. Combine with higher timeframe for big trend judgment
```

**Remember**: Triple confirmation is safe, but will also make you miss opportunities. In fast-rising markets, by the time all four confirmations are met, price might have already flown. Balance "safety" and "opportunity", find your own sweet spot!

---

**Final Reminder**: No matter how good the strategy, stop-loss won't give notice when it fails. Ranging markets are opportunities, one-sided declines are nightmares. Light position testing, survival comes first! 🙏