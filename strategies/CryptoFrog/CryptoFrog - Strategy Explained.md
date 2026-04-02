# CryptoFrog Strategy: Sitting and Waiting Like a Frog

> **Nickname**: Sit-and-Wait Strategy / Volatility Hunter  
> **Specialty**: Waiting for volatility to explode, then jumping in — like a frog!  
> **Timeframe**: 5 minutes + 1-hour informational layer

---

## 1. What's This Strategy?

Simply put, **CryptoFrog** is:
- A strategy using **Smoothed Heiken Ashi** to filter noise
- A strategy that waits for **Bollinger Band Expansion** (volatility about to explode) before entering
- A strategy using **linear-decay stop-loss** (gradually loosens over time)
- A strategy with **dynamic ROI** (doesn't take profits during trends)

Think of it like a frog sitting on a lily pad, waiting for mosquitoes before striking — normally still and silent, precise strike when opportunity arises! 🐸✨

---

## 2. Core Configuration: Waiting for the Wind to Blow

### Take-Profit Rules (ROI Table)

```
0-39 minutes: Exit at 21.3% profit!
39-96 minutes: Exit at 10.3% profit!
96-166 minutes: Exit at 3.7% profit!
After 166 minutes: Exit whenever
```

**Translation**: This strategy is very greedy — wants 21.3% right out of the gate! But as time passes, the target gets lower and lower — classic "shoot for the moon, then chicken out" 😅

### Stop-Loss Rules

```
Hard stop-loss: -8.5% (managed by custom linear decay)
Linear decay: From -8.5% gradually to -2% (within 166 minutes)
Trailing stop: Yes! Starts tracking from 0.5% profit, exits on 1.5% drawdown from high
```

**Translation**: The official stop-loss looks reasonable (-8.5%), but the strategy actually has a whole "gradually loosening" stop-loss — as time passes after entry, the stop-loss line moves toward 0, giving you more time to wait for a rebound!

---

## 3. Entry Logic: The Frog's Three Bug-Catching Techniques

This strategy has **3 independent buy methods**; satisfy any one and you buy:

### 🐸 Technique 1: BB Expansion + Momentum Confirmation

```python
# Bollinger Bands suddenly expand (volatility about to explode) + squeeze ended
(bbw_expansion == 1) & (sqzmi == False)
& (
    mfi < 20  # Money flow extremely low, rebound incoming!
    |
    dmi_minus > 30  # Selling pressure strong, reversal coming!
)
```

**Plain English**: "Volatility about to explode! And the market's been quiet for a long time — this is the calm before the storm!"

### 🐸 Technique 2: SAR + Stochastic RSI Oversold

```python
# Price below SAR (trend may reverse)
close < sar
& srsi_d >= srsi_k & srsi_d < 30  # Stochastic RSI just dead crossed, still in oversold
& fastd > fastk & fastd < 23       # Stochastic indicator also in oversold
& mfi < 30  # Money flowing out
```

**Plain English**: "Price fell below SAR, indicators also show oversold — isn't this a sure-fire rebound opportunity?"

### 🐸 Technique 3: DMI Crossover + Bollinger Band Bottom

```python
# Method A: DMI- crosses above DMI+
(dmi_minus > 30) & (dmi_minus crosses above dmi_plus)
& close < bb_lowerband

# Method B: Quick rebound after squeeze ends
sqzmi == True  # Bollinger Band squeeze
& fastd > fastk & fastd < 20  # Stochastic indicator just golden crossed
```

**Plain English**: "DMI crossed! And price is still at the Bollinger Band bottom — money sitting right there!"

### 🔒 Final Defense: Volume Confirmation

```python
vfi < 0  # Money flowing out (buyers sitting on sidelines)
& volume > 0  # Real volume confirmation
```

**Plain English**: Price signals alone aren't enough — actual money has to come in!

---

## 4. Exit Logic: More Complex Than the Entry

### 4.1 Core Exit Conditions

```python
# Close price above Heiken Ashi high
close > Smooth_HA_H
& # 1-hour Hansen HA confirms trend up
emac_1h > emao_1h
& # BB expansion + MFI/DMI overbought
bbw_expansion == 1
& (
    mfi > 80  # Money flow extremely high
    |
    dmi_plus > 30  # Buying pressure topped out
)
& # Volume confirmation
vfi > 0 & volume > 0
```

**Plain English**: "Price hit HA high, big timeframe confirms uptrend, volatility expanding, money flowing in — why aren't you running yet?"

### 4.2 Dynamic ROI: Don't Take Profits During Trends

This strategy has a "smart" dynamic ROI system:

```
If in a trend (RMI rising / SSL up / Candles rising)
→ Ignore ROI table, keep holding until trend ends!

If price starts pulling back
→ When profit retraces from high to a certain level, sell half!
```

**Plain English**: "Trend still there? Keep holding, let profits run! As soon as it pulls back, sell half!"

### 4.3 Linear-Decay Stop-Loss: Loosens Over Time

```
Time in position → Stop-loss line
0 minutes → -8.5%
30 minutes → -7.0%
60 minutes → -5.5%
90 minutes → -4.0%
120 minutes → -2.5%
166 minutes → -2.0% (stops changing after this)
```

**Plain English**: "If you're down 8.5% in the first half hour, cut and run! But the longer you hold, the looser the stop-loss — more time to wait for a rebound!"

---

## 5. The Strategy's "Personality"

### ✅ Pros

1. **Volatility hunter**: BB expansion detection enters before moves explode
2. **Smart stop-loss**: Linear decay gives you more time, won't get shaken out by noise
3. **Let profits run**: Dynamic ROI doesn't take profits during trends
4. **Multi-mode coverage**: 3 buy methods, always one for current conditions
5. **Highly customizable**: 20+ parameters, tune however you want

### ⚠️ Cons

1. **Too complex**: 400+ lines of code, many parameters, debugging is a nightmare 😅
2. **Too greedy**: 21.3% first target, may never be reached in low-volatility markets
3. **Heavy computation**: Multi-indicator + dual timeframe, VPS takes a beating
4. **High barrier**: Custom stop-loss and dynamic ROI require deep understanding to use

---

## 6. When to Use It?

| Market Environment | Recommended Move | Reason |
|-------------------|------------------|--------|
| 🚀 Strong uptrend | Enable dynamic ROI | 21.3% target + trend confirmation, big gains |
| 📉 Dip-buying | Lower ROI target | Adjust to 10-15%, more realistic |
| 🔄 Ranging market | Enable BB expansion mode | Volatility turning points precisely captured |
| ⚡️ High-volatility pairs | Keep default | This strategy was built for high volatility! |
| 😴 Low-volatility pairs | Add more pairs | Find more volatile coins |

---

## 7. What Markets Does This Make Money In?

### 7.1 Core Logic: Hunting with "Frog Wisdom"

CryptoFrog's core philosophy is **"sit and wait"**:

> "I don't chase moves — I wait. Wait for volatility to explode, wait for trend confirmation, wait for the perfect moment!"

- **HA filtering**: Use smoothed Heiken Ashi to remove noise, see only the "essence"
- **BB expansion**: Wait until Bollinger Bands open (volatility explosion) before acting
- **Trend confirmation**: 1-hour big timeframe confirms direction, don't fight the trend
- **Linear stop-loss**: Gives you time, won't get shaken out by small moves

### 7.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English Explanation |
|:-----------|:------:|--------------------------|
| 📈 Strong uptrend | ⭐⭐⭐⭐⭐ | Dynamic ROI + multi-mode entry catches big waves |
| 📉 Downtrend | ⭐⭐⭐ | Buy conditions may catch falling knives |
| 🔄 Wide-range oscillation | ⭐⭐⭐⭐ | BB expansion mode shines in ranging markets |
| ⚡️ Fast volatility | ⭐⭐⭐⭐⭐ | 21.3% target + volatility detection, perfect! |
| 📊 Consolidation | ⭐⭐ | Conditions too strict, may have long signal gaps |

**One-liner**: This strategy performs best in **high-volatility, clearly trending** markets; in **low-volatility, sideways oscillation**, the frog just squats and can't find signals 😴

---

## 8. Before Running This Strategy: Check These Configs

### 8.1 Key Parameter Configuration

| Config Item | Default | Suggestion | Notes|
|------------|--------|------------|---|
| minimal_roi."0" | 0.213 | 0.10-0.20 | Want 21%? Depends on the market |
| decay-time | 166 | 120-240 | Adjust stop-loss loosening speed |
| decay-end | -0.02 | -0.03~-0.01 | Final stop-loss line |
| trailing_stop_positive_offset | 0.047 | Keep | Starts tracking from 4.7% profit |
| droi_trend_type | any | rmi | Stricter trend judgment |

### 8.2 Recommended Configuration Combos

**Conservative version**:
```python
# Lower first target, more realistic
minimal_roi = {"0": 0.12, "45": 0.06, "120": 0.02}

# More conservative stop-loss
custom_stop['decay-end'] = -0.03
```

**Aggressive version**:
```python
# Keep high targets
minimal_roi = {"0": 0.25, "40": 0.12, "100": 0.04}

# More aggressive trailing
trailing_stop_positive_offset = 0.035
```

### 8.3 Hardware Requirements (Important!)

This strategy is computationally heavy:

| # of Trading Pairs | Min RAM | Recommended RAM | Experience |
|-------------------|---------|-----------------|-----------|
| 10-20 pairs | 2GB | 4GB | Runs, but may be slow |
| 20-50 pairs | 4GB | 8GB | Recommended config |
| 50+ pairs | 8GB | 16GB | Go crazy if you want |

**Warning**: Below-minimum RAM may cause **calculation timeouts**, missing buy/sell signals! 😅

---

## 9. The Strategy's "Hidden Skills"

### 🐸 Secret of Linear-Decay Stop-Loss

```python
'decay-time': 166  # Exactly matches the last ROI time!
```

> "Intentional! Stop-loss loosening time exactly matches the final ROI time — held over 166 minutes without profit? Then you only have -2% stop-loss left!"

### 🐸 Three Modes of Dynamic ROI

```python
droi_trend_type = ['rmi', 'ssl', 'candle', 'any']
```

> "Can use RMI, SSL channel, or candle trend to judge the trend — 'any' uses all three!"

### 🐸 VFI Volume Filtering

```python
# Buy: VFI < 0 (money flowing out, buyers watching)
# Sell: VFI > 0 (money flowing in, buyers active)
```

> "Clever design — when buying, money is flowing out (pessimistic); when selling, money is flowing in (optimistic)!"

---

## 10. The Bottom Line

### One-Line Rating
> "The 'Sit-and-Wait' practitioner of quantitative trading — wait for the wind, wait for volatility, then strike precisely!"

### Who Should Use It?
- ✅ Experienced quantitative traders
- ✅ Volatility-trading trend followers
- ✅ Technical folks who enjoy tweaking parameters
- ✅ Patient long-term optimizers

### Who Shouldn't?
- ❌ Beginners (complexity is a turn-off)
- ❌ Lazy folks (can't maintain it)
- ❌ Low-volatility trading pairs (target unreachable)
- ❌ People who want simplicity

### Manual Trading Recommendations

If you don't want automation, focus on these core signals:
1. **BB expansion + MFI < 20**: Volatility about to explode, money watching
2. **Price < SAR + Stochastic RSI < 23**: Technical oversold
3. **Close > HA high + 1h EMA up**: Trend confirmed up

Remember: **Wait for the wind, don't chase it**! 🍃

---

## ⚠️ Final Warning

### Backtests Look Great, Live Trading Is Another Story

CryptoFrog's backtest often **looks beautiful** — multi-condition combinations, always finds "perfect parameters." But there's a trap:

> **Because there are so many conditions, the strategy easily "fits" the optimal solution for past market behavior — but that doesn't guarantee future profitability.**

Simply put: **Getting a perfect score on memorized tests doesn't guarantee you'll pass the final** 📝

### Hidden Risks of Complex Strategies

In live trading, complex logic can cause:
- **Signal delay**: Heavy computation, may miss optimal buy/sell points
- **Over-trading**: More conditions, but not necessarily more trades
- **Parameter drift**: Market changes, params need retuning
- **Equity curve volatility**: Multi-condition strategies may have big wins and losses

### My Recommendations (Sincere Advice)

```
1. Run with default params first, observe for at least 1 month
2. Don't change multiple params at once — change one at a time
3. Test with small money — big gap between backtest and live is possible
4. Review regularly — see how strategy performs across markets
5. Don't be greedy — 21.3% isn't achievable every time
```

**Remember**: No matter how good a strategy is, the market doesn't play favorites. Test with small capital — survival is what matters! 🙏

---

**Final reminder**: The 21.3% first target is attractive, but **what suits you is what matters most**! 🐸✨
