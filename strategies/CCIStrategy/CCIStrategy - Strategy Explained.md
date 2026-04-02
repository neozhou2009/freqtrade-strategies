# CCIStrategy: CCI Mean Reversion + Trend Filter

> **Nickname**: Dual-CCI Hunter
> **Profession**: "Buy the dip, sell the top" expert specializing in catching extreme price swings
> **Timeframe**: 1 Minute

---

## 1. What's This Strategy All About?

Simply put, **CCIStrategy** is a strategy that:
- Uses CCI (Commodity Channel Index) to find oversold and overbought conditions
- Also checks capital flows (CMF, MFI) to make sure it's not a "fake move"
- Plus looks at moving average trends to avoid fighting the overall direction

Think of it like an **experienced hunter** — first uses the CCI telescope to spot prey (extreme prices), then uses the money flow detector to confirm the prey is real (capital direction), and finally uses the trend compass to decide whether to advance or retreat. 🔍

---

## 2. Core Settings: Basically "Take 10% and Run"

### Take-Profit Rule (ROI Table)

```
0 minutes → 10% profit → Run!
```

**Translation**:
> "As soon as you make 10%, don't hesitate, just leave. Lock in the gains!"

### Stop-Loss Rule

```
-2% stop-loss
```

**Translation**:
> "Cut losses at 2%, don't argue with the market."

---

## 3. Six Buy Conditions: I've Categorized Them for You

The strategy's buy conditions look complicated but are really just a "multiple confirmation" system. I've grouped them into 3 categories:

### 🎯 Category 1: Dual CCI Oversold Confirmation (2 Conditions)
**Core Logic**: Both long-term and short-term CCI must be oversold

**Plain English**:
> "I want to see the price drop a lot AND the short-term also drop a lot — dual confirmation is more reliable!"

**Key Conditions**:
- `cci_one < -100`: 170-period CCI below -100 → "Long-term oversold"
- `cci_two < -100`: 34-period CCI below -100 → "Short-term also oversold"

---

### 💰 Category 2: Capital Flow Confirmation (2 Conditions)
**Core Logic**: Capital is flowing out, price should rebound

**Plain English**:
> "Everyone's running away, the price must have dropped too much — buying here is probably right!"

**Key Conditions**:
- `cmf < -0.1`: Chaikin Money Flow negative → "Capital is fleeing"
- `mfi < 25`: Money Flow Index extremely low → "No money left in the market"

---

### 📈 Category 3: Trend Filter (2 Conditions)
**Core Logic**: Mid-term trend must be upward, long-term MA must be below price

**Plain English**:
> "Okay it's dropped a lot, but I need to confirm the long-term trend is still up — I don't want to catch a falling knife!"

**Key Conditions**:
- `resample_medium > resample_short`: 50-day MA > 25-day MA → "Mid-term trend is up"
- `resample_long < close`: 200-day MA below price → "Long-term also supports the rise"

---

## 4. Protection Mechanisms: Zero Layers of "Going Commando"

**Wait — this strategy has NO independent protection parameters!**

| Protection Type | Effect | Plain English |
|----------------|--------|---------------|
| None | All relying on 2% hard stop-loss and 10% ROI | "Whatever happens, happens" 😅 |

This strategy is like an **overconfident hunter** who only brings one gun (2% stop-loss) into the field. No armor, no backup plan.

---

## 5. Sell Logic: Stricter Than Buy

### 5.1 Sell Conditions: Dual CCI Overbought + Positive Capital Flow + Bearish MAs

```
cci_one > 100      # Long-term overbought
cci_two > 100      # Short-term overbought
cmf > 0.3          # Capital starting to flow back
resample_sma < resample_medium < resample_short  # Bearish MA alignment
```

**Plain English**:
> "Price rose too much (CCI overbought), money is starting to flow back in (positive CMF), but the MAs are all pointing down — Run!"

---

### 5.2 Take-Profit: Take 10% and Leave

```
0 minutes → 10% profit → Run!
```

**Plain English**:
> "Made 10%? What are you waiting for? There's an old trading saying: lock in your profits!"

---

## 6. Strategy "Personality"

### ✅ Strengths

1. **Multiple Confirmations**: Won't act until all 6 conditions are met; fewer false signals
2. **Smart Trend Filter**: Uses resampled MAs to avoid counter-trend trades
3. **Fast Response**: 1-minute timeframe, plenty of opportunities
4. **Clear Logic**: Buy and sell conditions symmetric; easy to understand

### ⚠️ Weaknesses

1. **Zero Protection**: No independent protection parameters; all relying on hard stop-loss
2. **Too Many Trades**: 1-minute timeframe; fees hurt
3. **Parameter Sensitive**: Minor changes to CCI thresholds ±100 may significantly alter results
4. **Average Trend Market Performance**: MA confirmation filters out some trend-following opportunities

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📊 Ranging Market | ✅ Focus on it | CCI oversold/overbought works best in ranging markets |
| 📈 Uptrend | ⚠️ Use carefully | MAs may filter out some opportunities |
| 📉 Downtrend | ⚠️ Use carefully | Buy signals get filtered by trend |
| 🎢 Extreme Volatility | ✅ Good to use | CCI sensitive to extreme moves |

---

## 8. Summary: What Do I Think?

### One-Line Verdict
> "A cautious strategy that uses CCI to find extremes and MAs to avoid getting burned — pursuing high-frequency small profits in ranging markets."

### Who's It For?
- ✅ People who like high-frequency trading
- ✅ People who can accept 2% stop-loss
- ✅ Users with low fees (< 0.1%)
- ✅ Ranging market environments

### Who's It NOT For?
- ❌ People who don't want frequent trading
- ❌ Platforms with high fees
- ❌ Clearly trending one-sided markets

### My Suggestions
1. **Test on paper trading first**: 1m high frequency; live may differ significantly
2. **Watch those fees**: 10% ROI can get eaten up by fees
3. **Pick high-liquidity coins**: 1m needs good depth
4. **Set alerts**: With so many conditions, signals may be sparse; don't miss them

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Use CCI to Find Extremes, MAs to Avoid Blame

**Its Money-Making Philosophy**:

1. **CCI Finds Extremes**: Price deviating too far from the mean will revert — its "sixth sense"
2. **Capital Flow Confirmation**: Not just looking at price, also seeing where money flows — more comprehensive
3. **MAs Prevent Blame**: Even if oversold, if trend is downward the strategy waits — cautious!

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English Explanation |
|:---|:---|:---|
| 🔄 Ranging Market | ⭐⭐⭐⭐⭐ | CCI oversold/overbought triggers repeatedly; mean reversion fully发挥作用 |
| 📈 Uptrend | ⭐⭐⭐☆☆ | Trend is up but CCI overbought triggers sell; may miss some gains |
| 📉 Downtrend | ⭐⭐⭐☆☆ | Buy signals filtered by MAs; sell signals effective |
| ⚡️ Extreme Volatility | ⭐⭐⭐⭐☆ | CCI sensitive to extreme price moves; capital flow confirmation improves accuracy |

**Bottom Line**: **Ranging markets are its home turf; use carefully in trending markets.**

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Suggested | Note |
|------------|-----------|------|
| Timeframe | 1m | Minimum config; ordinary people may not handle it |
| Number of pairs | 5-10 | Don't be greedy; 1m consumes lots of resources |
| Fees | < 0.1% | High-frequency strategies; fees are critical! |

### 10.2 Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| cci_one period | 170 | Long-term CCI |
| cci_two period | 34 | Short-term CCI |
| mfi threshold | 25 | Money flow oversold line |
| cmf threshold | -0.1 / 0.3 | Capital flow +/- thresholds |

### 10.3 Hardware Requirements (Important!)

1-minute timeframe has moderate computation but demands on trading frequency:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|----------------|-------------|
| 5-10 pairs | 1 GB | 2 GB | Smooth |
| 20-30 pairs | 2 GB | 4 GB | Okay |
| 50+ pairs | 4 GB+ | 8 GB+ | May lag |

**Warning**: 1m + resample calculation may need optimization in live trading. 😅

### 10.4 Backtesting vs Live Trading

- **Backtesting**: CCI signals clear, MA filter stable
- **Live**: Slippage may be significant, especially for low-liquidity coins

**Recommended Process**:
1. Backtest historical data with default parameters
2. Adjust ROI and stop-loss to find optimal
3. Run paper trading for a week to observe signal frequency
4. Small-capital live testing; confirm live matches paper
5. Gradually increase position

**Don't go all-in right away**, even good strategies need a磨合 period!

---

## 11. Easter Egg: Strategy Author's "Little Tricks"

Looking closely at the code, you'll find some interesting things:

1. **Dual CCI Design**
   > "Author uses 170-period and 34-period — 170 is near a Fibonacci number, so is 34. There may be some voodoo math involved, but dual confirmation is genuinely more reliable."

2. **chaikin_mf Function**
   > "Author implemented the Chaikin Money Flow formula themselves instead of using a library — this is a developer with ambition!"

3. **Resample 5x**
   > "1m data resampled 5x becomes 5m — they want to see the trend at a higher dimension without missing 1m opportunities."

---

## 12. The Final Word

### One-Line Verdict
> "A cautious strategy using CCI to find extremes and MAs to avoid blame — suitable for high-frequency small-profit ranging markets."

### Who's It For?
- ✅ Likes high-frequency trading
- ✅ Can accept 2% stop-loss
- ✅ Low fees (< 0.1%)
- ✅ Trades high-liquidity coins

### Who's It NOT For?
- ❌ Doesn't want frequent trading
- ❌ High fees
- ❌ Clearly trending one-sided markets
- ❌ Risk-averse

### Manual Trading Suggestions

If you want to follow this manually:
1. Open 1m chart
2. Wait for CCI (170) and CCI (34) both below -100 simultaneously
3. Confirm MFI < 25, CMF < -0.1
4. Check 5m MAs: 50-day > 25-day, AND 200-day < current price
5. All satisfied? Buy! Set 10% take-profit, -2% stop-loss

---

## 13. ⚠️ Risk Reminder (Must Read This Section)

### Backtesting Looks Good; Live Requires Caution

CCIStrategy's historical backtesting may look **decent** — but there are pitfalls:

> **1m backtesting vs live differences can be significant**, because:
> - Slippage impact: 1m sensitive to price changes; may have slippage on buy/sell
> - Fee erosion: High-frequency trading; fees may be key to profitability
> - Sparse signals: 6 conditions simultaneously satisfied is not easy; may go days without a signal

### Hidden Risks of Complex Strategies

Live, complex logic may cause:
- **Signal delay**: Resample and MA calculation adds delay
- **Missing opportunities**: Trend filter too strict; may filter good opportunities
- **Psychological pressure**: Frequent trading requires strong mental discipline

### My Suggestions (From the Heart)

```
1. Fees! Fees! Fees! Important things repeat three times
2. Run paper trading for a week first; check signal frequency and profitability
3. Small-capital live test; confirm live matches backtesting
4. Prepare for -20% loss tolerance; this strategy may stop out consecutively
5. Regularly check if parameters need adjustment
```

**Remember**: **High-frequency strategies make money from fee differentials, not from trends.**

---

**Final Reminder**: 1m looks exciting, but beginners can easily get burned by "frequent trading." Test with small positions; survival is what matters most! 🙏

---

**Appendix: CCI Explained**

CCI (Commodity Channel Index):
- **> +100**: Overbought; price may pull back
- **< -100**: Oversold; price may rebound
- **Oscillating around 0**: Consolidating

This strategy exploits CCI's characteristics, combined with capital flows and MAs, to do "mean reversion" business. 📊
