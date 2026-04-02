# BBRSIS Strategy: The "Bottom-Fishing Artist" in Trends

> **Nickname**: Trend Bottom-Fisher King, Triple Confirmation OCD Patient  
> **Profession**: Oversold bounce specialist in bull markets  
> **Timeframe**: 5 minutes

---

## 1. What Is This Strategy?

Simply put, **BBRSIS** is a strategy that:
- **Only trades longs**: Won't touch anything that's not an uptrend
- **Hunts for bargains**: Only considers buying when price breaks below Bollinger lower band
- **OCD-level confirmation**: Triple moving averages + Three-layer RSI all must confirm before entry

Like an **experienced driver who checks three generations of family history before a blind date AND requires the partner to be lying at rock bottom** 🤣

---

## 2. Core Configuration: Basically "Waiting for Oversold Opportunities in Big Trends"

### Take Profit Rules (ROI Table)

```
Profit    Time
─────────────
30%       Immediately
```

**Translation**: Run when you make 30%, don't be greedy. This target is set high, meaning the strategy catches big swings.

### Stop Loss Rule

```
Stop Loss Line: -10%
```

**Translation**: Accept a 10% loss and move on. Stop loss is set relatively wide, giving the strategy room to breathe.

---

## 3. One Buy Condition: Looks Simple, Actually Insanely Strict

This strategy has only one buy signal, but the conditions stack like **Russian nesting dolls**:

### 🎯 Buy Condition: Five-Fold Verification

**Core Logic**: Price must be extremely oversold, AND trend must be upward.

**In Plain English**:
> "I want to buy, but must satisfy five conditions:
> 1. Price broke below Bollinger lower band (dirt cheap)
> 2. Short-term MA is above medium-term MA (short-term trend up)
> 3. Medium-term MA is above long-term MA (medium-term trend up)
> 4. Current RSI is at least 5 points lower than the next timeframe's RSI (truly oversold)
> 5. Volume isn't zero (this candle is valid)"

**Classic Lines**:
- Condition #1: `close < bb_lowerband` → "Price must break below Bollinger lower band, cheap as dirt"
- Condition #2: `sma5 >= sma75` → "5-period MA must be above 75-period MA"
- Condition #3: `sma75 >= sma200` → "75-period MA must be above 200-period MA"
- Condition #4: `rsi < resample_15m_rsi - 5` → "Current RSI must be 5 points lower than 15-min RSI"

**Critique**: This condition combo is basically "I want to find an extremely oversold point in an uptrend, AND confirm larger timeframes agree with this oversold condition." **By the time you confirm everything, the opportunity is long gone** 😅

---

## 4. Protection Mechanism: Two Layers of Insurance

While each buy condition doesn't have independent protection parameters, the strategy has two protection layers:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| Stop Loss -10% | Loss cap | "Run at 10% loss, I'm out" |
| Take Profit 30% | Profit target | "Run at 30% profit, take the money" |

**Critique**: Protection is simple, but the 30% take profit target is aggressive, might be hard to trigger. Strategy relies more on sell signals than ROI. 🤔

---

## 5. Sell Logic: Even Stricter Than Buying

### 5.1 Sell Condition: Five-Fold Confirmation

```
Price returns to Bollinger middle band
AND Current RSI > 15-min RSI + 5
AND Current RSI > 30-min RSI
AND Current RSI > 50-min RSI
AND Volume > 0
```

**Plain English**:
- Price climbed from below middle band to above: **Starting to bounce**
- Current RSI is higher than all three larger timeframe RSIs: **Momentum confirms reversal**
- Only then consider selling

**Critique**: **Selling is even harder than buying**. Price is already above middle band, RSI must also be higher than all three larger timeframes to sell - this basically means **selling at local tops**. Pro operation, stable!

### 5.2 Basic Sell Signal (1)

**Classic Line**:

1. **Signal #1**: `close > bb_middleband AND rsi_conditions`
   > "Price is above middle band, RSI also higher than three larger timeframes, time to run."

---

## 6. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Section)

1. **High Signal Quality**: Five-fold confirmation, every signal is premium
2. **Trend-Friendly**: Only trades longs, following the trend
3. **Extreme Value Capture**: 3-SD Bollinger Bands, hunts genuine oversold
4. **Multi-Timeframe Verification**: Larger timeframes verify smaller ones, fewer false signals

### ⚠️ Weaknesses (Roast Section)

1. **Too Few Signals**: Five-fold confirmation stacked, might not get a signal all day
2. **Misses Early Trend**: Waiting for 200-MA confirmation, trend is halfway done
3. **Useless in Ranging Markets**: MAs are a mess, no signals ever
4. **Take Profit Too High**: 30% ROI basically never triggers, relies on sell signals

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Clear Uptrend | ✅ Use it | This is its home turf |
| Sideways Range | ❌ Don't use | Triple MA never aligns properly |
| Downtrend | ❌ Don't use | Strategy won't buy anyway |
| High Volatility | ⚠️ Cautious | Too many false breakouts possible |

---

## 8. Summary: How's This Strategy Really?

### One-Liner Review
> **"Oversold bounce specialist in trending markets, few signals but high quality."**

### Who Should Use It?
- ✅ Patient traders (few signals)
- ✅ Long-only traders (trend-following mindset)
- ✅ Extreme-value bottom-fishers (Bollinger lower band)
- ✅ Those who want high-quality signals (multiple confirmations)

### Who Shouldn't Use It?
- ❌ High-frequency trading enthusiasts
- ❌ Those who want to trade in ranging markets
- ❌ Left-side traders
- ❌ Impatient people

### My Recommendations
1. **Trend First**: Use other tools to judge the big trend, confirm it's a bull market
2. **Multi-Pair Monitoring**: Since signals are rare, monitor multiple trading pairs simultaneously
3. **Be Patient**: This strategy is built for quality, don't expect quantity
4. **Accept Empty Positions**: Ranging markets might have no signals for days, get used to it

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Building a "High Win-Rate Net" with Multiple Confirmations

BBRSIS is a **trend-following strategy**. About 80 lines of code, clear logic, but strict conditions.

**Its Money-Making Philosophy**: **Better to miss than to make mistakes**

- **Trend is King**: Triple MA alignment is entry prerequisite, ensuring you're in an uptrend
- **Extreme Value Entry**: Bollinger 3-SD lower band, only enter on genuine oversold
- **Multi-Timeframe Verification**: Use larger timeframe RSI to confirm, avoid small timeframe false signals
- **Mean Reversion Exit**: Consider retreating when price returns to middle band

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | This is its home turf, wait for pullback entries |
| 🔄 Sideways Range | ⭐☆☆☆☆ | MAs are a mess, zero signals |
| 📉 Downtrend | ☆☆☆☆☆ | Won't buy at all, just watch |
| ⚡ High Volatility | ⭐⭐☆☆☆ | Might get tricked by false breakouts |

**One-Line Summary**: **Only works in bull markets, lies flat in ranging and downtrending markets.**

---

## 10. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Comment |
|-------------|------------------|---------|
| Minimum Pairs | 5-10 | Signals are rare, monitor more |
| Timeframe | 5m (default) | Can adjust based on coin |
| Volume Requirement | >0 | Default is fine |

### 10.2 Key Config File Settings

```yaml
# Recommended to use default configuration
minimal_roi: { "0": 0.30 }
stoploss: -0.10
timeframe: 5m
```

### 10.3 Hardware Requirements (Important!)

This strategy uses multi-timeframe resampling, has extra memory consumption:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-10 pairs | 2 GB | 4 GB | Smooth |
| 10-50 pairs | 4 GB | 8 GB | Normal |
| 50+ pairs | 8 GB | 16 GB | Needs monitoring |

**Warning**: Multi-timeframe calculations increase memory pressure, don't use an ancient VPS. 😅

### 10.4 Backtesting vs Live Trading

Multi-timeframe strategies may encounter **data alignment issues** in backtesting:

**Recommended Process**:
1. Backtest with historical data first, check signal frequency
2. Confirm if backtest results are reasonable
3. Small-amount live testing
4. Observe differences between live and backtest

**Don't go all-in right away**, no matter how good the strategy seems!

---

## 11. Easter Egg: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **Triple Timeframe Design**: 5m × 3 = 15m, 5m × 6 = 30m, 5m × 10 = 50m
   > "Using non-standard timeframes might be intentional to avoid competing with other strategies"

2. **Bollinger Bands Use 3 SD**: Standard is 2 SD
   > "I want genuine oversold, not just regular oversold"

3. **RSI Period Uses 20**: Standard is 14
   > "Smoother RSI, less noise"

---

## 12. Final Words

### One-Liner Review
> **"Conservative bottom-fisher in trending markets, few signals but steady."**

### Who Should Use It?
- ✅ Patient quantitative traders
- ✅ Long-only trend traders
- ✅ Extreme-value entry enthusiasts
- ✅ Quality over quantity seekers

### Who Shouldn't Use It?
- ❌ High-frequency trading lovers
- ❌ Those who want to trade ranging markets
- ❌ Left-side traders
- ❌ Impatient people

### Manual Trader Tips
To manually execute this strategy, you need to:
1. Watch 5-minute, 15-minute, 30-minute, 50-minute timeframes simultaneously
2. Calculate 5, 75, 200 three moving averages
3. Calculate 20-period RSI
4. Draw Bollinger Bands (20 period, 3 SD)
5. Compare RSIs across four timeframes in real-time

**Recommendation**: Let the bot run it, manual execution is too exhausting. 😅

---

## 13. ⚠️ Risk Re-Emphasis (Read This Section!)

### Backtesting Is Beautiful, Live Trading Requires Caution

BBRSIS's historical backtest might look good — but there's a trap:

> **Multi-timeframe strategies are easily affected by data alignment issues, backtest results may be overly optimistic.**

Simply put: **Historical data aligns perfectly, live data might not.**

### Hidden Risks of Complex Strategies

In live trading, multi-timeframe logic may cause:
- **Resampling Delay**: Larger timeframe data updates slowly, signals may lag
- **Data Inconsistency**: Different timeframes might have small data source differences
- **Memory Consumption**: Multi-timeframe calculations increase system burden

### My Honest Recommendations

```
1. Backtest with default config first, check signal frequency
2. Confirm if backtest results are reasonable (risk/reward ratio)
3. Small-amount live testing (recommend 5%-10% position)
4. Observe live signal quality vs backtest differences
5. Gradually increase position (if results are good)
```

**Remember**: **No matter how good the strategy, test first. Staying alive is most important!** 🙏