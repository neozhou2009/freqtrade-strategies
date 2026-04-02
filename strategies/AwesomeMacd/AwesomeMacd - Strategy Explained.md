# AwesomeMacd Strategy: The Dual-Blade Momentum Hunter

> **Nickname**: MACD's Best Friend, The Momentum Duet  
> **Profession**: Momentum Reversal Catcher  
> **Timeframe**: 1 Hour

---

## I. What is This Strategy?

Simply put, **AwesomeMacd** is:
- MACD + Awesome Oscillator dual confirmation
- Only enters on momentum reversal
- No games — signals must have double verification

It's like having two guards who both need to nod before you can enter — one says "looks like trend is going up", the other says "momentum is indeed strengthening", only when both nod do you get in! 🚪

This strategy was ported from the Mynt quantitative framework, originally written in C#, and moved to Freqtrade by the author.

---

## II. Core Configuration: Plain English Version

### Take Profit Rules (ROI Table)

```python
minimal_roi = {"0": 0.1}  # Run at 10%
```

**Translation**: Sell automatically at 10% profit. This target is pretty practical — for a 1-hour level strategy, 10% is good enough.

### Stop Loss Rules

```python
stoploss = -0.25  # Cut at 25% loss
```

**Translation**: Only stop loss at 25% down — that's a lot of room. 1-hour level has big swings, tight stops get shaken out easily.

---

## III. Entry Conditions: Three Guardians Must All Nod

This strategy's entry requires three conditions to be met simultaneously, none can be missing:

### 🎯 Triple Confirmation Entry

**Plain English Translation**:
> "MACD is above zero (trend up), AO is also above zero (momentum up), AND the previous candle's AO was below zero (just turned positive) — NOW we buy!"

**Breakdown**:

| Condition | Indicator State | Plain English |
|-----------|-----------------|---------------|
| Condition 1 | MACD > 0 | "Trend is already up, short-term MA above long-term MA" |
| Condition 2 | AO > 0 | "Momentum is positive right now" |
| Condition 3 | AO previous < 0 | "Last candle momentum was negative, just turned positive!" |

**Core Logic**:
- MACD confirms trend direction — "Is the big direction right?"
- AO confirms momentum reversal — "Is this the trigger point?"
- AO must just turn from negative to positive — "Catch that exact moment of momentum reversal!"

**It's like**: Waiting for the traffic light to turn green, AND confirming it just turned green that second, before stepping on the gas! 🚦

---

## IV. Exit Logic: Mirror Symmetry

Exit conditions are completely symmetrical to entry, just reversed:

| Condition | Indicator State | Plain English |
|-----------|-----------------|---------------|
| Condition 1 | MACD < 0 | "Trend has turned down" |
| Condition 2 | AO < 0 | "Momentum is negative now" |
| Condition 3 | AO previous > 0 | "Last candle momentum was positive, just turned negative!" |

**Plain English**:
> "MACD dropped below zero, AO also dropped, and AO just turned from positive to negative — this is a momentum reversal to the downside, run!"

**Perfect logical symmetry**: Buy the same way you sell, clean and efficient.

---

## V. This Strategy's "Personality"

### ✅ Pros (The Good Stuff)

1. **Dual confirmation reduces false signals**: Both MACD and AO need to nod, way fewer fake breakouts
2. **Precise momentum reversal capture**: AO negative-to-positive/positive-to-negative is a classic momentum inflection signal
3. **Symmetrical logic**: Buy and sell conditions mirror each other, consistent and easy to understand
4. **1-hour level**: Good for intraday swings, don't have to wait too long

### ⚠️ Cons (The Bad Stuff)

1. **Stop loss is a bit wide**: 25% stop loss, small accounts might not survive
2. **No trailing stop**: Profits might be given back
3. **ADX calculated but unused**: Code calculates ADX but doesn't use it — wasting compute or leaving it for users?
4. **Ranging markets are deadly**: MACD and AO will repeatedly cross zero, getting slapped constantly

---

## VI. Suitable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|--------------------|--------|
| Momentum Market | Default configuration | Strategy specializes in catching momentum reversals |
| Single-direction Trend | Consider raising ROI | Hold longer when trending |
| Sideways Range | Don't use | Zero line crossings will kill you |
| High Volatility | Increase stop loss | Avoid getting stopped by noise |

**Bottom line**: Use it in momentum markets, stay away when there's no momentum.

---

## VII. Summary: How's This Strategy Really?

### One-liner
> "Twin blades combined, a precise momentum reversal hunter. But gets destroyed in ranging markets."

### Who should use it?
- ✅ Momentum strategy enthusiasts
- ✅ Those who can tolerate wider stop losses
- ✅ Those wanting to learn multi-indicator combinations
- ✅ Intraday swing traders

### Who shouldn't use it?
- ❌ Those trading ranging markets
- ❌ Those seeking tight stop losses
- ❌ Those wanting trailing stop protection
- ❌ Those who get headaches from multiple indicators

### My Advice

```
1. During backtesting, see if ADX is useful, can add ADX > 25 filter
2. Consider adding trailing stop, make profits more secure
3. Turn it off in ranging markets, or use a different strategy
```

---

## VIII. What Market Can This Strategy Make Money In?

### 8.1 Core Logic: Momentum Reversal Capture

AwesomeMacd is a **classic example of a momentum confirmation strategy**.

**Its money-making philosophy**:
- **Trend confirmation**: MACD tells you if the big direction is right
- **Timing capture**: AO tells you if this is the trigger point
- **Double insurance**: Both must nod before acting, reducing false signals

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English |
|:------------|:-------------------|:--------------|
| 📈 Momentum Uptrend | ⭐⭐⭐⭐⭐ | This is its home turf! Precisely catches momentum initiation |
| 📉 Momentum Downtrend | ⭐⭐⭐☆☆ | Exit signal is accurate, but no shorting mechanism |
| 🔄 Sideways Range | ⭐⭐☆☆☆ | Zero crossings repeatedly, getting slapped |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | Noise may cause false signals |

**One sentence summary**: Momentum markets are its home, ranging markets are its nemesis.

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration | Recommended Value | Commentary |
|---------------|-------------------|------------|
| Trading Pairs | BTC/USDT, ETH/USDT | Major coins have obvious momentum |
| Timeframe | 1h (default) | Can try 4h, less noise |

### 9.2 Key Configuration Settings

```yaml
timeframe: 1h
stoploss: -0.25
minimal_roi: {"0": 0.1}
```

### 9.3 Hardware Requirements (Easy)

This strategy has moderate computational needs:
- RAM: 1-2GB is enough
- CPU: Standard VPS works fine
- Pairs: Can run multiple

---

## X. Easter Egg: "Little Quirks" in the Strategy Code

Looking carefully at the code, you'll find some interesting things:

1. **ADX calculated but not used**:
   ```python
   dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
   ```
   Calculates ADX, but doesn't use it in entry/exit conditions at all!
   
   **Possible reasons**:
   - Left for users to develop
   - Original C# code used it, not cleaned up during port
   - Used for backtesting analysis or visualization

2. **MACD calculates three values**:
   ```python
   dataframe['macd'] = macd['macd']
   dataframe['macdsignal'] = macd['macdsignal']  # Not used
   dataframe['macdhist'] = macd['macdhist']       # Not used either
   ```
   MACD calculates three lines, but only uses one MACD line!
   
   **Commentary**: Signal line and histogram calculated but unused, isn't that a bit wasteful?

3. **AO uses shift() for reversal detection**:
   ```python
   (dataframe['ao'] > 0) & (dataframe['ao'].shift() < 0)
   ```
   Compares previous candle value with current to determine momentum reversal.
   
   **Kudos**: This is a classic momentum reversal detection method, simple and effective!

---

## XI. Final Words

### One-liner Review
> "Dual confirmation is great, but ranging markets are its nemesis."

### Who should use it?
- ✅ Momentum trading enthusiasts
- ✅ Those wanting to learn multi-indicator combinations
- ✅ Intraday swing players
- ✅ Those who can handle wider stop losses

### Who shouldn't use it?
- ❌ Those wanting to profit in ranging markets
- ❌ Those seeking precise stop losses
- ❌ Those wanting trailing stop protection

### Advice for Users

```
1. Add ADX > 25 filter during backtesting, way fewer false signals in ranging markets
2. Consider adding trailing stop to protect profits
3. Turn off this strategy in ranging conditions, use something else
4. Try 4h timeframe, less noise
```

**Remember**: The soul of this strategy is "dual confirmation" — both indicators must nod before entry. Quality over quantity, fewer but better.

---

## XII. ⚠️ Risk Re-emphasis (Must Read)

### Dual Confirmation ≠ 100% Correct

Even with two indicators confirming, it doesn't mean you won't lose money:

> **Momentum strategies fear ranging markets most — both indicators will repeatedly slap you in ranging conditions.**

### This Strategy's "Pitfalls"

| Risk Point | Description |
|------------|-------------|
| Repeated zero crossings | In ranging markets, MACD and AO will repeatedly cross zero |
| Wide stop loss | 25% stop loss, small accounts can't handle |
| No trailing stop | Profits may be given back |

### My Honest Advice

```
1. Run backtesting first, see when your trading pair makes money
2. Turn off during ranging periods, turn on during momentum periods
3. Consider adding ADX to filter trend strength
4. Don't go all-in right away, test with small positions first
```

**Remember**: Strategies are tools, the market is the boss. No matter how good the tool, if the market doesn't cooperate, it won't work.

---

## XIII. Indicator Education: What are MACD and AO?

### MACD (Moving Average Convergence Divergence)

- **Calculation**: Short-term EMA - Long-term EMA
- **MACD > 0**: Short-term MA above long-term MA, bullish bias
- **MACD < 0**: Short-term MA below long-term MA, bearish bias
- **Purpose**: Determine trend direction

### Awesome Oscillator (AO)

- **Calculation**: 5-period SMA - 34-period SMA (using median price)
- **AO > 0**: Bullish momentum
- **AO < 0**: Bearish momentum
- **AO negative to positive**: Momentum reversing upward, possible buy signal
- **AO positive to negative**: Momentum reversing downward, possible sell signal
- **Purpose**: Determine momentum direction and reversal timing

### Why Use Both Together?

- MACD tells you "is the direction right"
- AO tells you "is the timing right"
- Both must be right before acting, higher quality!

---

**Final Reminder**: The soul of momentum strategies is "trend + timing", MACD handles trend, AO handles timing. But this strategy fears ranging markets most — stay away from ranging markets! 🙏