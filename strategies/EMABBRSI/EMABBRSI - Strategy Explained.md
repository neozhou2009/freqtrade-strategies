# EMABBRSI Strategy: The MA + Bollinger + RSI "Three-in-One"

> **Nickname**: Three-in-One Filter  
> **Occupation**: Uses 3 indicators to confirm trends — only buys "certain" signals  
> **Timeframe**: 1 Hour

---

## 1. What's This Strategy?

Put simply, **EMABBRSI** combines three common indicators:
- EMA crossover (judge trend direction)
- Bollinger Band breakout (find entry points)
- RSI confirmation (filter false signals)

Like a matchmaking event: **must have money (EMA), have a house (Bollinger), have a car (RSI)** — all three conditions met before saying yes! 😂

This is a **1-hour level** medium-to-long term strategy, suitable for capturing **trending markets**!

---

## 2. Core Settings: "Trend Following"

### Take-Profit Rules (ROI Table)

```
Immediate exit (0 minutes)     → Run when profit reaches 14.14%!
After 25 minutes              → Run when profit reaches 4.59%!
After 41 minutes              → Run when profit reaches 2.07%!
After 67 minutes              → Break-even exit
```

**Translation**: This strategy targets **medium-term trends** — 14% and run, not greedy!

### Stoploss Rules

```
Hard stoploss: -20%
```

**Translation**: -20% stoploss is reasonable, giving plenty of room!

---

## 3. 3 Buy Conditions: Here's the Breakdown

### 🎯 Type #1: Bollinger Lower Band Breakout + RSI Confirmation
**Core Logic**: Price bounced after dropping below Bollinger lower band + RSI confirms stabilization

**Plain English**:
> "Price dropped to the Bollinger lower band, and RSI recovered from oversold — it looks like it's done falling, time to bounce!"

**Trigger Conditions**:
- RSI > 33
- Close price crosses from below to above the Bollinger lower band

---

### 📈 Type #2: EMA200 Support Buy
**Core Logic**: Price pulls back to EMA200 and finds support

**Plain English**:
> "Price dropped to the 200-day MA — this is the long-term cost line, should have support!"

**Trigger Conditions**:
- Previous candle close > EMA200
- This candle low < EMA200 (wicked through)
- Close > EMA200 (closed back above)

---

### 🚀 Type #3: Golden Cross (EMA50 Crosses Above EMA200)
**Core Logic**: Short-term MA crosses from below to above long-term MA

**Plain English**:
> "The 50-day MA crossed above the 200-day MA — this is a classic bullish signal!"

**Trigger Conditions**:
- EMA50 crosses from below to above EMA200

---

## 4. Exit Logic: 2 Sell Conditions

### 4.1 Upper Bollinger Band + RSI Overbought

| Trigger Condition | Plain English |
|------------------|---------------|
| Close > Bollinger upper band | "Price hit the upper band, hitting resistance" |
| RSI > 91 | "Risen too much, should pull back" |

**Plain English**: > "Price hit resistance, and RSI is overbought too — it's gonna drop!"

### 4.2 Death Cross (EMA50 Crosses Below EMA200)

| Trigger Condition | Plain English |
|------------------|---------------|
| EMA50 crosses from above to below EMA200 | "Trend turned bearish, run!" |

---

## 5. Technical Indicators: What "Weapons" Does This Strategy Use?

| Indicator | Period | Purpose | Plain English |
|-----------|--------|---------|---------------|
| **EMA7** | 7 | Short-term trend | "Recent week's average cost" |
| **EMA25** | 25 | Short-term trend | "Recent month's average cost" |
| **EMA50** | 50 | Medium-term trend | "Recent two months' average cost" |
| **EMA200** | 200 | Long-term trend | "Recent year's average cost" |
| **RSI** | 14 | Overbought/oversold | "Check if it's risen too much" |
| **Bollinger Bands** | 20, 2/3 | Volatility boundaries | "Price channel" |

---

## 6. Risk Management: How Does This Strategy Protect Itself?

### 6.1 Protection Mechanism

This strategy **has no independent protection mechanism**, relying on:

1. **Generous stoploss**: -20%, plenty of room
2. **Time stoploss**: Break-even exit after 67 minutes
3. **Multi-condition filtering**: 3 buy conditions reduce false signals

### 6.2 Multi-Condition Combination Advantage

| Condition | Effect |
|-----------|--------|
| Bollinger breakout | Find oversold bounce points |
| EMA200 support | Find long-term MA support |
| Golden cross | Confirm trend turning bullish |

**Plain English**: Three cobblers equal aZhuge Liang!

---

## 7. The Strategy's "Personality Traits"

### ✅ Pros (The Praise Section)

1. **Multi-condition confirmation**: 3 types of indicators filter, reducing false signals
2. **Medium-to-long term strategy**: 1-hour level, no need to watch daily
3. **Clear logic**: Each condition has explicit logic
4. **Good for trending markets**: Good performance when trends are clear

### ⚠️ Cons (The Rant Section)

1. **Few signals**: Strict conditions, may not buy for a long time
2. **RSI > 91 too strict**: Rarely triggers in practice
3. **No protection mechanism**: May suffer consecutive losses in oscillating markets
4. **Long timeframe**: 1-hour level, long signal cycles

---

## 8. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 **Trending up** | Use freely | Golden cross + Bollinger breakout = double confirmation! |
| 📉 **Dip bounce** | Use condition 1 | Bollinger lower band bounce |
| 🔄 **Oscillating market** | Reduce trading pairs | Few signals, easy to get trapped |
| 😐 **Consolidation** | Don't use | Too many false signals |

---

## 9. Bottom Line: How's This Strategy Really?

### One-Line Verdict
> "MA + Bollinger + RSI — a three-in-one trend confirmation strategy"

### Who It's Good For:
- ✅ Medium-to-long term investors (no need to watch daily)
- ✅ Trend traders (profits big when trends come)
- ✅ People who like multi-condition confirmation
- ✅ Patient people (few signals)

### Who It's NOT For:
- ❌ Short-term traders (1-hour level too slow)
- ❌ Impatient people (can't wait)
- ❌ Oscillating traders

### My Suggestions

1. **Focus on golden cross**: This is the clearest signal
2. **Combine with Bollinger**: Use Bollinger to sell high/buy low in oscillating markets
3. **Set stoploss**: -20% is reasonable
4. **Don't watch constantly**: 1-hour level doesn't need daily monitoring

---

## 10. What Markets Does This Strategy Make Money In?

### 10.1 Core Logic: Confirming Trends with Multiple Indicators

**EMABBRSI's** money-making philosophy: **Not catching every opportunity, but catching high-certainty opportunities!**

- **Bollinger breakout**: Catch oversold bounce
- **EMA200 support**: Catch long-term MA support
- **Golden cross**: Confirm trend turning bullish

### 10.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:---|:---:|:---|
| 📈 Trending up | ⭐⭐⭐⭐⭐ | Golden cross confirms trend, multiple protections |
| 📉 Dip bounce | ⭐⭐⭐⭐☆ | Bollinger lower band bounce effective |
| 🔄 Oscillating market | ⭐⭐⭐☆☆ | Bollinger for selling high/buying low |
| 😐 Consolidation | ⭐⭐☆☆☆ | MA crosses whip-saw each other |

**One-liner**: Decent in trending markets,barely pass in oscillating markets 😎

---

## 11. Want to Run This Strategy? Check These Configs First

### 11.1 Trading Pair Configuration

| Config Item | Recommended Value | Comments |
|-------------|-------------------|----------|
| Number of pairs | 10-20 | Don't go too many |
| Mainstream coins only | BTC/ETH | Altcoins have many false signals |
| Timeframe | 1 hour | Don't change |

### 11.2 Key Config Settings

```yaml
# Recommended config
minimal_roi:
  "0": 0.1414
  "25": 0.0459
  "41": 0.0207
  "67": 0

stoploss: -0.20
```

### 11.3 Hardware Requirements

This strategy has extremely low computational load, no hardware demands:

| Number of Pairs | Min RAM | Recommended RAM |
|----------------|---------|-----------------|
| 10-20 pairs | 1 GB | 2 GB |
| 50+ pairs | 2 GB | 4 GB |

### 11.4 Backtesting vs. Live Trading

Backtesting looks great, live trading fails because:
1. **False breakout**: Bollinger breakout falls back quickly
2. **Signal delay**: Trend is already half over by the time signal arrives
3. **RSI condition too strict**: RSI > 91 almost never triggers

**Recommended Process**:
1. Backtest for 3 months
2. Dry-run for 2 weeks
3. Small capital live trading for 1 month
4. Scale up only if no issues

---

## 12. Bonus: The Strategy Author's "Little Tricks"

1. **RSI > 91**: The author must have been burned by "false breakouts" — that's why the sell condition is so strict!
2. **EMA200**: Using 200-day MA for long-term trend judgment is a classic approach!
3. **1-hour level**: The author must not be a short-term trader — they're a medium-to-long term trend investor!
4. **14.14% take-profit**: This number is close to √2 — there's some magic to it!

---

## ⚠️ Final Warning: Risk Re-emphasis (Must Read!)

### Backtesting Looks Great, Live Trading Requires Caution

**EMABBRSI's** historical backtesting performance often looks **very good** — but there's a trap:

> **RSI > 91 sell condition is too strict — rarely triggers in practice, the strategy mainly relies on ROI exit!**

Simply put: **Many buy conditions, few sell conditions — mainly depends on the take-profit table!**

### Simple Strategy Risks

In live trading, complex logic may cause:
- **Too few signals**: All 3 conditions met simultaneously is rare
- **Hard to sell**: RSI > 91 almost never triggers
- **False signals**: Golden cross quickly becomes death cross

### My Suggestions (Sincere Advice)

```
1. Focus on golden cross: This is the clearest buy signal
2. Don't rely on RSI for selling: Mainly use ROI table to take profit
3. Set stoploss: -20% is the bottom line
4. Diversify investments: Don't put all money on one strategy
```

**Remember**: More conditions = fewer signals ≠ higher win rate! 🙏

---

**Final Reminder**: No matter how good the strategy, the market won't hesitate to teach you a lesson. Test with small capital — survival is the top priority! 🙏
