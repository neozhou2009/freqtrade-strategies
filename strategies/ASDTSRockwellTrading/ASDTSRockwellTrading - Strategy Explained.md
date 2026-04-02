# ASDTSRockwellTrading Strategy: The MACD Classic from a YouTube Tutorial

> **Nickname**: The MACD Model Student  
> **Occupation**: Trend Follower, Only Trusts MACD  
> **Timeframe**: 5 Minutes

---

## I. What Exactly Is This Strategy?

Simply put, **ASDTSRockwellTrading** is:
- Uses only one indicator (MACD)
- Logic so simple even a grade schooler can understand
- A "model student" strategy from a YouTube tutorial
- Classic trend following that can't get more classic

Like a **student who only memorizes key notes for exams**—might not get perfect scores, but definitely won't fail 📚

---

## II. Core Configuration: Basically "Whatever MACD Says Goes"

### Take-Profit Rules (ROI Table)

```
Just bought and it's up 5%? Run!
Waited 20 minutes (4 candles) and still 4%? Run!
Waited 30 minutes (6 candles) and still 3%? Run!
Waited 60 minutes (12 candles) and still 1%? Run!
```

**Translation**: This strategy is realistic—happy with 5% profit, will even take 1% if needed. Main philosophy is "lock in profits."

### Stop-Loss Rules

```
When down to -30%... stop-loss triggers!
```

**Translation**: Stop-loss is set pretty wide, giving plenty of room for the trend to develop. Basically saying "don't panic, let it fly for a while."

---

## III. Buy Condition: Classic That Can't Be More Classic

### 🎯 MACD Bullish Confirmation

**Core Logic**: MACD above zero line + MACD higher than signal line → Buy

```python
# The actual code is this simple
(dataframe['macd'] > 0) &          # MACD above zero line
(dataframe['macd'] > dataframe['macdsignal'])  # MACD higher than signal line
```

**Plain English Translation**:
> "MACD is positive (bullish market) + MACD line above signal line (momentum strengthening) → Buy!"

**What Does This Signal Mean?**
- MACD > 0: Short-term moving average is higher than long-term average, meaning recent price is rising faster than before
- MACD > Signal: Momentum is accelerating, not just rising but rising faster

**Simple Analogy**:
Like driving uphill—
- MACD > 0: Car is already going uphill (not downhill)
- MACD > Signal: Still stepping on the gas and accelerating (not releasing)

---

## IV. Sell Condition: Run as Soon as Momentum Weakens

### 📉 MACD Crosses Below Signal Line

**Core Logic**: MACD lower than signal line → Sell

```python
# Sell condition is even simpler
(dataframe['macd'] < dataframe['macdsignal'])
```

**Plain English Translation**:
> "MACD dropped below signal line? Get out!"

**Note**: This only requires MACD to cross below signal line, regardless of whether MACD is positive or negative.

**This Means**:
- Even if MACD is still above zero line (still bullish market)
- As long as MACD crosses below signal line (momentum starts weakening)
- Sell immediately!

**Simple Analogy**:
Still driving uphill—
- Previously had gas pedal floored (MACD > Signal)
- Now released the gas (MACD < Signal)
- Although car is still moving up (MACD > 0), but no power, get off quick!

---

## V. This Strategy's "Personality"

### ✅ Pros (Compliment Time)

1. **Classic Logic**: MACD is a "founding father" level technical indicator
2. **Clear Signals**: No "maybe" or "probably," either it fits or it doesn't
3. **Simple Code**: 60 lines, even beginners can understand
4. **Follow the Trend**: Only enters after trend is confirmed
5. **Quick Response**: Runs as soon as momentum weakens, doesn't wait for trend reversal

### ⚠️ Cons (Complaint Time)

1. **Gets Harvested in Oscillating Markets**: During sideways movement, MACD keeps crossing, signals trigger repeatedly
2. **Stop-Loss Too Wide**: -30% stop-loss means you might lose a third before running
3. **Single Indicator**: Only looks at MACD, no other confirmation
4. **No Trend Filter**: Doesn't care if it's trending or oscillating, just charges in on any signal

---

## VI. Applicable Scenarios: When Should You Use It?

| Market Environment | Recommended Action | Reason |
|--------------------|-------------------|--------|
| Clear Uptrend | 👍 Recommended | Follow the trend, performs well |
| Sideways Oscillation | 👎 Not Recommended | Many false signals, frequent stop-losses |
| Downtrend | 🤷 Auto-Stays Out | MACD < 0, won't buy |
| High Volatility | ⚠️ Cautious | Need to add filter conditions |

---

## VII. Summary: How's This Strategy Really?

### One-Sentence Review
> "MACD beginner must-learn, trend following simplified to the extreme"

### Who Should Use It?
- ✅ Beginners wanting to learn MACD strategies
- ✅ People who like simple logic
- ✅ Traders who only trade trending markets

### Who Shouldn't Use It?
- ❌ People wanting to make money in oscillating markets
- ❌ People wanting complex filter conditions
- ❌ People who don't want to optimize strategies themselves

### My Recommendations
1. **Add ADX Filter**: Only enter when ADX > 25, avoid false signals in oscillating markets
2. **Tighten Stop-Loss**: -30% is too wide, suggest -10% to -15%
3. **Can Add Volume Filter**: More reliable when volume increases

---

## VIII. What Market Can This Strategy Make Money In?

### 8.1 Core Logic: Follow MACD

This strategy has about 60 lines of code, core is one sentence: **MACD says buy, I buy; MACD says sell, I sell**.

**Its Money-Making Philosophy**:
> "When trend comes, get on board; when momentum goes, get off"

- **Trend Confirmation**: MACD > 0 means bullish market
- **Momentum Confirmation**: MACD > Signal means still accelerating
- **Quick Exit**: MACD < Signal means out of gas

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | MACD bullish confirmation, following all the way up |
| 🔄 Sideways Oscillation | ⭐☆☆☆☆ | Repeated buying and selling, fees will bankrupt you |
| 📉 Downtrend | ⭐⭐☆☆☆ | MACD < 0, won't buy, stays in cash |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | Many false signals, need filters |

**One-Sentence Summary**: This is a trend strategy; don't use it in oscillating markets, you'll get slapped repeatedly.

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Comment |
|--------------------|-----------------|---------|
| Timeframe | 5m | Default setting, can also try 15m |
| Trading Pair Selection | Trending Coins | Choose coins with clear trends |
| How Many Pairs at Once | 5-20 pairs | Not too many, MACD doesn't use much resources |

### 9.2 Key Configuration File Settings

```yaml
# Suggested configurations to keep
timeframe: 5m

# Suggested configurations to modify
stoploss: -0.15  # Originally -0.30, too wide

# Can add this configuration
# Add ADX judgment in populate_indicators
```

### 9.3 Hardware Requirements (Very Resource-Friendly)

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|:-----------------------:|:--------------:|:-----------------:|:----------:|
| 1-10 pairs | 512MB | 1GB | Smooth |
| 10-50 pairs | 1GB | 2GB | Smooth |
| 50+ pairs | 2GB | 4GB | Still smooth |

**Good News**: This strategy also doesn't need a powerful computer, any VPS can run it.

### 9.4 Backtesting vs Live Trading

**Backtesting Notes**:
- Choose time periods with clear trends
- Avoid oscillating periods, otherwise returns look ugly

**Suggested Process**:
1. Backtest trending periods, see performance
2. Paper trading with small capital
3. Live trading with small positions
4. Increase position size after confirming stability

---

## X. Bonus: Strategy Source

This strategy comes from a YouTube tutorial video:
https://www.youtube.com/watch?v=mmAWVmKN4J0

Author: Gert Wohlgemuth

**Core Concepts from Video**:

| Concept | Definition |
|---------|------------|
| Uptrend | MACD > 0 and MACD > Signal |
| Downtrend | MACD < 0 and MACD < Signal |
| Sell Signal | MACD < Signal |

**Translation**:
> "The author just translated the video's concepts into code"

---

## XI. How to Use This for Manual Trading?

If you want to manually execute this strategy:

1. **Open TradingView**, add MACD indicator (default parameters: 12, 26, 9)
2. **Switch to 5-minute chart**
3. **Wait for Signal**:
   - MACD line (fast line) above zero line
   - MACD line above signal line (slow line)
   - → **Buy**
4. **Sell**:
   - MACD line drops below signal line
   - → **Sell**

That simple! Don't need to look at any other indicators.

---

## XII. ⚠️ Risk Re-emphasis (This Section Is Must-Read)

### Backtesting Looks Great, Live Trading Needs Caution

ASDTSRockwellTrading backtesting usually performs well if you choose trending periods—but:

> **Oscillating markets are MACD's natural enemy. During sideways movement, it will repeatedly buy and sell, and fees can eat you alive.**

### Hidden Risks of Simple Strategies

In live trading, overly simple logic can lead to:
- **Oscillating Market False Signals**: MACD repeatedly crosses during sideways movement
- **Slow Stop-Loss Triggers**: -30% stop-loss too wide, may incur big losses
- **Lack of Trend Confirmation**: Doesn't know if market is trending or oscillating

### My Advice (Honest Truth)

```
1. Add ADX filter: Only enter when ADX > 25
2. Tighten stop-loss: Change to -15% or -10%
3. Choose good pairs: Only trade coins with trends
4. Avoid oscillation periods: Pause when market is sideways
5. Control position size: Don't go all-in, leave some room
```

**Remember**: MACD is a good indicator, but it really can't be trusted in oscillating markets. When trend comes, this strategy is sweet; when oscillation comes, get out quick! 🙏

---

## XIII. Final Words

### One-Sentence Review
> "Textbook-level MACD trend strategy, simple but needs oscillation filtering"

### Who Should Use It?
- ✅ People wanting to learn MACD strategies
- ✅ People who like simple logic
- ✅ People who can judge trend vs oscillation themselves

### Who Shouldn't Use It?
- ❌ People wanting fully automated hands-off profits
- ❌ People who frequently don't watch the charts
- ❌ People trading in oscillating markets

### If You Must Use It As-Is...

At least remember:
1. **Only use in trending markets**
2. **Tighten stop-loss to -15%**
3. **Test with small positions**

MACD is a good tool, but the tool is only as good as the person using it. Don't blame it in oscillating markets, the market just isn't cooperating!

---