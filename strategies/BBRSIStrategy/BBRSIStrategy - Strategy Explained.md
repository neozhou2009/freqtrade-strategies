# BBRSIStrategy: The "Bounce Hunter" in Ranging Markets

> **Nickname**: Bollinger Band Bottom-Fisher King, Mean Reversion Expert  
> **Profession**: Bounce-catching specialist in high-volatility ranging markets  
> **Timeframe**: 15 minutes

---

## 1. What Is This Strategy?

Simply put, **BBRSIStrategy** is:
- **Hunts Extreme Prices**: Only buys when price breaks below Bollinger lower band
- **Simple and Direct**: Buy when RSI > 25, sell when RSI > 95
- **Complete Risk Control**: Tiered take-profit + trailing stop + ultra-wide stop loss

Like an **experienced driver who picks up bargains at cliff edges and sells at mountain peaks** 🤣

---

## 2. Core Configuration: Basically "Trading Time for Space"

### Take Profit Rules (ROI Table)

```
Holding Time    Target Profit
────────────────────
0-21 minutes    21.55%
21-48 minutes   5.49%
48-125 minutes  1.30%
125+ minutes    0% (rely on sell signal)
```

**Translation**: The longer you hold, the lower the profit requirement. First 21 minutes need 21%, then slowly lower the bar. After 125 minutes, rely on sell signals.

**Critique**: These ROI numbers look like they were **run through hyperparameter optimization**, precise to 8 decimal places, but actual effectiveness... who knows 😅

### Stop Loss Rule

```
Stop Loss Line: -36%
Trailing Stop: Enabled
```

**Translation**:
- Won't stop loss until 36% loss, super wide!
- Trailing stop enabled, follows profits

**Critique**: 36% stop loss is insanely wide! This is basically saying **"I'd rather die than stop loss"**. Though with trailing stop, might be okay.

---

## 3. One Buy Condition: Simple as It Gets

This strategy's buy condition is just two conditions combined, compared to BBRSIS earlier, it's a **minimalist**:

### 🎯 Buy Condition: Double Insurance

**Core Logic**: Price drops to Bollinger lower band, but RSI shouldn't be too low.

**Plain English**:
> "I want to buy, must satisfy two conditions:
> 1. RSI above 25 (not too extreme)
> 2. Price below 1-SD Bollinger lower band (cheap enough)"

**Classic Lines**:
- Condition #1: `rsi > 25` → "RSI shouldn't be too low, I don't want to catch a falling knife"
- Condition #2: `close < bb_lowerband_1sd` → "Price broke below Bollinger lower band, time to bounce"

**Compared to BBRSIS**:
- BBRSIS: 5 conditions (Triple MA + Multi-timeframe RSI + Bollinger)
- BBRSIStrategy: 2 conditions (RSI + Bollinger)

**Critique**: This strategy is **zen-like**, few conditions, many signals, but quality might not match BBRSIS. 🤔

---

## 4. Protection Mechanism: Three Layers

While there are no independent protection parameter groups, the strategy has three protection layers:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| Tiered Take-Profit | Lower requirements over time | "Wait for you to profit, I'll slowly lower the bar" |
| Trailing Stop | Follow profits | "Money you've earned, I'll help you keep it" |
| Ultra-Wide Stop Loss | -36% | "Don't call me until 36% loss" |

**Critique**: Of these three layers, **36% stop loss is too wide**, basically non-existent. What actually works is trailing stop and sell signals. 🤨

---

## 5. Sell Logic: Even Simpler Than Buy

### 5.1 Sell Condition: Run at Extreme Overbought

```
RSI > 95
AND
Price > Bollinger Upper Band
```

**Plain English**:
- RSI above 95 (extremely overbought)
- Price breaks above Bollinger upper band (over-extended)

**Critique**: **RSI > 95** is too extreme! Waiting for RSI to hit 95 means waiting until **insanely crazy** levels to exit. Most of the time this signal won't trigger, relying on ROI or stop loss instead. 😅

### 5.2 Actual Exit Methods

| Exit Method | Trigger Condition | Plain English |
|-------------|------------------|---------------|
| ROI Take-Profit | Holding time × Target profit | "Time's up, profit's enough, leaving" |
| Sell Signal | RSI > 95 + Price > Upper Band | "Too crazy, run now" |
| Trailing Stop | Profit pullback | "Earned money almost gone, retreat" |
| Fixed Stop Loss | -36% | "Really crashed, accept fate" |

**Critique**: In reality, **sell signal might be the last to trigger**. Most of the time rely on ROI and trailing stop. 😂

---

## 6. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Section)

1. **Simple Logic**: Under 100 lines of code, easy to understand
2. **High Signal Frequency**: Few conditions, many trigger opportunities
3. **Complete Risk Control**: Tiered take-profit + trailing stop
4. **Beginner-Friendly**: Concise code, easy to understand and modify

### ⚠️ Weaknesses (Roast Section)

1. **Stop Loss Too Wide**: 36% stop loss, one loss might eat multiple wins
2. **Sell Condition Too Extreme**: RSI > 95 too hard to trigger
3. **No Trend Filter**: No trend filtering, might catch falling knives in downtrends
4. **1-SD Band**: Bollinger Band too narrow, might have too many signals

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| High Volatility Range | ✅ Use it | This is its home turf |
| Normal Range | ⚠️ Cautious | Might have too many signals |
| Uptrend | ❌ Careful | Mean reversion may trade against trend |
| Downtrend | ❌ Don't use | Catching knives halfway down |

---

## 8. Summary: How's This Strategy Really?

### One-Liner Review
> **"Bounce hunter in ranging markets, simple and crude but not without risk."**

### Who Should Use It?
- ✅ Beginners learning (simple code)
- ✅ Ranging market traders (mean reversion)
- ✅ High volatility market traders (wide stop loss)
- ✅ Those who like simple strategies

### Who Shouldn't Use It?
- ❌ Conservatives (36% stop loss too wide)
- ❌ Trend traders (no trend filter)
- ❌ High-frequency traders (15-minute timeframe)
- ❌ Those who like complex strategies

### My Recommendations
1. **Adjust Stop Loss**: 36% is too wide, recommend 10%-15%
2. **Lower Sell Threshold**: RSI > 95 too extreme, consider 80-90
3. **Add Trend Filter**: Add moving average or trend indicator
4. **Backtest First**: Test in ranging markets, see results

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Mean Reversion + Extreme Value Capture

BBRSIStrategy is a **mean reversion strategy**. About 90 lines of code, simple logic.

**Its Money-Making Philosophy**: **Buy at extreme prices, wait for price to revert to normal**

- **Bollinger Lower Band Buy**: Price over-dropped, should bounce
- **Bollinger Upper Band Sell**: Price over-rose, should pull back
- **RSI Confirmation**: Not too extreme (buy) or really extreme (sell)

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Strong Uptrend | ⭐⭐☆☆☆ | Catching knives halfway up, mean reversion fails |
| 🔄 Ranging Market | ⭐⭐⭐⭐☆ | This is its home turf, eat swings back and forth |
| 📉 Strong Downtrend | ⭐⭐☆☆☆ | Similarly catching knives halfway |
| ⚡ High Volatility Range | ⭐⭐⭐⭐⭐ | Many signals, big swings, good for churning |

**One-Line Summary**: **Good buddy in ranging markets, sucker in trends.**

---

## 10. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Comment |
|-------------|------------------|---------|
| Timeframe | 15m (default) | Medium frequency |
| Minimum Pairs | 3-5 | Already enough signals |
| Stop Loss | -0.15 (adjusted) | Default 36% too wide |

### 10.2 Key Config File Settings

```yaml
# Recommended adjusted configuration
minimal_roi:
  "0": 0.15      # Lower short-term target
  "30": 0.08     # Medium-term target
  "60": 0.03     # Long-term target
  "120": 0       # Rely on sell signal

stoploss: -0.15  # Adjusted stop loss (original too wide)

trailing_stop: True
```

### 10.3 Hardware Requirements (Important!)

This strategy has minimal computation, low hardware requirements:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-50 pairs | 1 GB | 2 GB | Smooth |
| 50-200 pairs | 2 GB | 4 GB | Normal |
| 200+ pairs | 4 GB | 8 GB | Still smooth |

**Critique**: This strategy is **very resource-efficient**, any VPS can run it. 👍

### 10.4 Backtesting vs Live Trading

Mean reversion strategies need attention in backtesting:

**Potential Issues**:
- Slippage impact (Bollinger signals at extreme prices)
- Liquidity risk (might not buy/sell during fast moves)
- Extreme markets (stop loss might not execute)

**Recommended Process**:
1. Backtest with historical data first, check signal frequency
2. Set reasonable slippage parameters
3. Small-amount live testing
4. Observe differences between live and backtest

**Don't go all-in right away**, mean reversion strategies might have consecutive losses in trending markets!

---

## 11. Easter Egg: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **ROI Precise to 8 Decimal Places**: `0.21547444718127343`
   > "Clearly hyperparameter optimization output, possibly overfit historical data"

2. **Stop Loss Also Precise Number**: `-0.3603667187598833`
   > "Same as above, obvious hyperparameter optimization traces"

3. **Defined 4-SD Bollinger Band But Never Used**:
   ```python
   bollinger_4sd = qtpylib.bollinger_bands(..., stds=4)
   dataframe['bb_lowerband_4sd'] = bollinger_4sd['lower']
   ```
   > "Maybe left for future extension, or tested but found ineffective"

4. **RSI Uses Default 14-Period**:
   ```python
   dataframe['rsi'] = ta.RSI(dataframe)  # Default 14
   ```
   > "Standard configuration, no hyperparameter optimization"

---

## 12. Final Words

### One-Liner Review
> **"Simple and crude mean reversion strategy, great for ranging markets but deadly in trends."**

### Who Should Use It?
- ✅ Beginners learning Freqtrade strategy development
- ✅ Ranging market traders
- ✅ Those who like simple strategies
- ✅ High volatility coins

### Who Shouldn't Use It?
- ❌ Conservative traders (stop loss too wide)
- ❌ Trend traders
- ❌ Those who like complex logic
- ❌ Low volatility markets

### Manual Trader Tips
To manually execute this strategy, you need:
1. Set Bollinger Bands (20-period, 1-SD)
2. Set RSI (14-period)
3. Monitor price relationship with Bollinger Bands
4. Set tiered take-profit (or use trailing stop)

**Recommendation**: Manual trading might be more flexible than running a bot, can adjust strategy based on trend.

---

## 13. ⚠️ Risk Re-Emphasis (Read This Section!)

### Backtesting Is Beautiful, Live Trading Requires Caution

BBRSIStrategy's ROI and stop loss parameters are **precise to 8 decimal places**, this is clearly the result of **hyperparameter optimization**:

> **Risk of overfitting historical data is significant!**

Simply put: **Runs perfectly in historical data, might lose badly in live trading.**

### Risk of 36% Stop Loss

Stop loss at 36% means:
- **Single loss can be huge**
- **Multiple small wins might be eaten by one big loss**
- **Need very high win rate to be profitable**

### Risk of Mean Reversion Strategy

Mean reversion strategies in **trending markets** might:
- Consecutively catch knives halfway down
- Stop loss triggered repeatedly
- Small losses accumulate into big losses

### My Honest Recommendations

```
1. Adjust stop loss: From 36% to 10%-15%
2. Lower sell threshold: From RSI > 95 to 80-90
3. Add trend filter: Add a moving average or trend indicator
4. Control position size: Don't use too heavy positions
5. Backtest first: See performance in different markets
```

**Remember**: **Mean reversion strategies are deadly in trends, staying alive is most important!** 🙏