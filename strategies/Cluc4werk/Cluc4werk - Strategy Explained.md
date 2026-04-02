# Cluc4werk Strategy Explained

> **Read This and Get It Instantly** | Bollinger Bands + ROCR Trend Filter 1-Minute Sprint Runner

---

## 1. What's This Strategy All About?

**Cluc4werk** is a 1-minute ultra short-term trading strategy; core logic is simple:

> "First check big picture (1-hour trend), then find small opportunities (1-minute Bollinger Band signals)"

In plain terms: confirms the 1-hour timeframe shows an uptrend via ROCR indicator, then looks for Bollinger Band signals on the 1-minute chart to buy. Sell is equally direct — sell when price breaks through BB middle band.

This strategy is like a **short-term hunter**; specializes in catching pullbacks or breakouts within trends; holding time is short, generally minutes to tens of minutes before potentially exiting.

---

## 2. Core Settings

### 2.1 Key Parameters

| Parameter | Value | Meaning |
|-----------|-------|---------|
| **Timeframe** | 1 minute | Ultra short-term |
| **Informative timeframe** | 1 hour | Used for big picture |
| **Stop-loss** | -1% | Cut losses at 1% |
| **ROI 1** | 1.5% | Hold 0-20 minutes |
| **ROI 2** | 0.5% | Hold 20-30 minutes |
| **ROI 3** | 0.1% | Hold 30+ minutes |

### 2.2 Indicator Dependencies

- **Bollinger Bands**: 40 periods + 20 periods
- **ROCR**: 28 periods (1m) + 168 periods (1h)
- **EMA**: 50 periods
- **Volume MA**: 30 periods

Requires: `talib`, `technical`, `qtpylib`, `numpy`

---

## 3. Entry Conditions (2 Modes)

### 3.1 Prerequisite: ROCR Trend Filter

```
1-hour ROCR > 0.65
```

This is **mandatory**! Only considers buying when 1-hour timeframe is in an uptrend.

> Think of it like checking both ways for cars before crossing — confirm safety first.

### 3.2 Mode 1: BinHV Variant

All **6 conditions** must be met simultaneously:

1. ✅ BB lower band valid (not NaN)
2. ✅ BB bandwidth > close × 0.6%
3. ✅ Price change > close × 1.3%
4. ✅ Lower shadow < bandwidth × 96.8%
5. ✅ Current price < previous BB lower band
6. ✅ Current price ≤ previous close

**Plain English**: Price suddenly crashed then closed near lower band; short lower shadow; can't fall further.

### 3.3 Mode 2: Cluc Variant

All **3 conditions** must be met simultaneously:

1. ✅ Price < EMA50
2. ✅ Price < BB lower band × 0.013
3. ✅ Volume < 30-day avg × 28

**Plain English**: Price fell to very low level, and volume shrunk to extremes (floor volume).

### 3.4 Summary

```
Buy = (1-hour uptrend) AND (Mode 1 OR Mode 2)
```

---

## 4. Protection Mechanisms

Cluc4werk has several protection layers:

### 4.1 ROCR Trend Filter (First Defense)

```
1-hour ROCR > 0.65
```

This is the **core protection** — only trades when big trend is up; avoids counter-trend moves.

### 4.2 Tight Stop-Loss (Second Defense)

```
stoploss = -1%
```

Cut losses at 1%; never linger.

### 4.3 Multi-Timeframe Confirmation (Third Defense)

Views both 1-minute and 1-hour data simultaneously; **dual confirmation is safer**.

---

## 5. Sell Logic

### 5.1 Main Sell Condition

```
Price crosses above BB middle band AND has volume
```

**Plain English**: Price rose to BB's middle position; likely hit resistance; exit and lock in profits.

### 5.2 ROI Auto-Exit

| Holding Time | Auto-Exit Condition |
|-------------|-------------------|
| 0-20 minutes | Profit ≥ 1.5% |
| 20-30 minutes | Profit ≥ 0.5% |
| 30+ minutes | Profit ≥ 0.1% |

### 5.3 Take-Profit Logic

```
exit_profit_only = True
```

Only sell when making money; wait for stop-loss if losing.

---

## 6. Strategy "Personality"

Describing Cluc4werk in human terms:

| Characteristic | Description |
|---------------|-------------|
| **Personality** | Extremely cautious; only acts with confirmation |
| **Trading style** | Ultra short-term sprinter; short holding |
| **Risk preference** | Low-risk lover; runs at 1% |
| **Decision speed** | Fast and decisive; no hesitation |
| **Biggest advantage** | Has trend protection; doesn't fight trends |
| **Biggest disadvantage** | May miss trend starts |
| **Catchphrase** | "Wait, confirm again!" |

---

## 7. Applicable Scenarios

### ✅ Good Scenarios

- **Pullbacks in uptrends**: Trend up; price pulls back to BB lower band
- **Oscillating markets**: Price oscillates between upper and lower bands
- **High volatility markets**: 1-minute volatility large; many signals
- **Daytime trading sessions**: Volatile and active

### ❌ Bad Scenarios

- **Downtrends**: ROCR filter fails; easy to lose
- **Low-volatility consolidation**: Movement too small; signals unclear
- **Late night/holidays**: Low volatility; sparse signals
- **Low-volatility coins**: Movement too small; 1% stop-loss may be too sensitive

---

## 8. Summary (Minimalist Version)

**Cluc4werk = 1-hour trend confirmation + 1-minute Bollinger Band signals**

- 🏃 Holding time: Minutes to tens of minutes
- 🛡️ Max loss: 1%
- 🎯 Target profit: Starting at 1.5%
- ⏰ Trading frequency: High
- 📊 Good markets: Uptrends, oscillating markets

---

## 9. Market Performance

### 9.1 Ideal Conditions

| Market Type | Expected Performance |
|------------|-------------------|
| 📈 Uptrend | ⭐⭐⭐⭐☆ Accurate signals; steady profits |
| 🔄 Wide-range oscillation | ⭐⭐⭐☆☆ Frequent signals; good profits |
| 📉 Downtrend | ⭐⭐☆☆☆ Fewer signals; may stay in cash |
| ⚡ High volatility | ⭐⭐⭐⭐☆ Many opportunities; good returns |

### 9.2 Risk Alerts

- 1-minute timeframe easily affected by **false breakouts**
- ROCR threshold 0.65 may need per-market adjustment
- High-frequency trading may lead to **fee erosion of profits**

---

## 10. Configuration Suggestions

### 10.1 Suggested Configuration

| Config Item | Suggested Value |
|------------|-----------------|
| **Number of pairs** | 10-20 |
| **Max positions** | 2-4 |
| **Single coin position** | 2-5% |
| **Timeframe** | 1m (mandatory) |

### 10.2 Parameter Tuning Suggestions

| Parameter | Adjustment Suggestion |
|----------|---------------------|
| **ROCR threshold** | Raise to 0.7-0.8 in high volatility |
| **Stop-loss** | Can widen to -1.5% in high-volatility markets |
| **ROI** | Can adjust based on fees |

### 10.3 Notes

1. ⚠️ 1-minute framework needs **fast execution**
2. ⚠️ Needs stable data source; low network latency
3. ⚠️ Suggest using **market orders** for fills

---

## 11. Easter Egg

### 11.1 Strategy Inspiration Source

Cluc4werk originates from classic **Cluc series**, combining **BinHV**'s Bollinger Band approach. ROCR trend filter is a classic multi-timeframe analysis application.

### 11.2 Fun Fact

- ROCR (Rate of Change) measures price change percentage over a period
- 168-period ROCR on 1-hour chart equals **one week** of price changes
- Threshold of 0.65 means price rose 65%+ over the past week

### 11.3 Advanced Play

Manual traders can simplify usage:
1. Open 1-hour chart; confirm ROCR > 0.65
2. Switch to 1-minute chart; wait for price near BB lower band
3. Buy; set 1% stop-loss
4. Sell when price breaks through BB middle band

---

## 12. The Final Word

Cluc4werk is a **meticulously designed** short-cycle strategy; core advantages:

1. ✅ **Trend protection**: Uses 1-hour ROCR to avoid counter-trend trades
2. ✅ **Dual confirmation**: 1-minute + 1-hour; safer
3. ✅ **Fast stop-loss**: 1% stop-loss; controls risk
4. ✅ **Multi-tier ROI**: Auto take-profit; no monitoring needed

But it's **not a universal strategy**:
- ❌ Not for lazy people (high trading frequency)
- ❌ Not for long-term holds
- ❌ Needs good execution environment and low fees

---

## 13. ⚠️ Risk Reminder

**Important things repeat three times:**

1. ⚠️ **1-minute strategies have high trading frequency**; fees significant portion; ensure fees < 0.2%
2. ⚠️ **ROCR filter may fail** in extreme markets; may need manual intervention
3. ⚠️ **False breakouts are frequent**; reasonable stop-loss is protection
4. ⚠️ **High-volatility markets** may consecutively trigger stop-loss; control total position

---

**Summary**: Cluc4werk is a **short-term hunter** strategy; suitable for people who have time and energy to manage, pursuing high-frequency trading. If you want **steady, safe returns**, consider long-term strategies; if you want **fast entry/exit**, Cluc4werk is a good tool.

> 🎯 Remember: **Discipline matters more than strategy**; even the best strategy can't save people who don't set stop-losses.
