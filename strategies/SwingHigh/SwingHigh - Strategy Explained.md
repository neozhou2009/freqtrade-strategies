# SwingHigh Strategy: The "Bottom-Fisher" in Trends

> **Nickname**: Bottom-Fisher, Pullback Hunter  
> **Job**: An experienced driver who specializes in picking up bargains during trend pullbacks  
> **Timeframe**: 30 Minutes

---

## I. What is This Strategy?

Simply put, **SwingHigh** is:
- Using MACD to determine the overall direction
- Using CCI to find extreme oversold points
- Boldly entering during trend pullbacks

It's like watching a stock go up, noticing it pulled back a bit too hard, and then diving in to "buy the dip" 🤣

---

## II. Core Configuration: "Bold Bottom-Fishing, Careful Exiting"

### Profit Taking Rules (ROI Table)

```
Hold 0-23 minutes: Take 16% and run
Hold 23-54 minutes: Take 3.2% and run
Hold 54-173 minutes: Take 1.2% and run
After 173 minutes: Run even without profit
```

**Translation**: This strategy likes short-term trades. The shorter the time, the higher the expectation. If it's still dilly-dallying after 3 hours, it's not worth waiting anymore.

### Stop Loss Rules

```
Hard Stop Loss: -22.27% (Cut at this loss)
Trailing Stop: Activates after 10% profit, follows the rise, exits on 8% pullback
```

**Translation**: It gives you a 22% "error margin," and once you're making money, it automatically helps you lock in most of the profits. Pretty thoughtful!

---

## III. 1 Buy Condition: The One Trick

### 🎯 The Only Buy Condition: MACD Golden Cross + CCI Crashed to the Floor

**Core Logic**:
- MACD line needs to golden cross (trend upward)
- CCI needs to drop below -188 (extremely oversold)
- Has volume (not fake data)

**Plain English**:
> "The stock is going up, suddenly takes a hit, and when it hits hard enough, I jump in to buy the dip!"

**The Code Looks Like This**:
```python
(dataframe["macd"] > dataframe["macdsignal"]) &   # MACD golden cross
(dataframe["cci-buy"] <= -188.0) &                  # CCI crashed hard
(dataframe["volume"] > 0)                           # Has volume
```

**Comment**: CCI needs to drop to -188 to buy, that threshold is extreme! Normal oversold is -100, this strategy waits for a "bloodbath" before acting 😅

---

## IV. 1 Sell Condition: Wait Until It Goes Crazy

### 📉 The Only Sell Condition: MACD Death Cross + CCI Shoots to the Sky

**Core Logic**:
- MACD line needs to death cross (trend downward)
- CCI needs to rise above 231 (extremely overbought)
- Has volume

**Plain English**:
> "The trend starts heading down, and CCI hits 231 - it's gone crazy, time to run!"

**The Code Looks Like This**:
```python
(dataframe["macd"] < dataframe["macdsignal"]) &   # MACD death cross
(dataframe["cci-sell"] >= 231.0) &                  # CCI went crazy
(dataframe["volume"] > 0)                           # Has volume
```

**Note**: The CCI period for selling is 76, much larger than the 13 for buying. Meaning: **Fast entry, slow exit**.

---

## V. Trailing Stop: The "Bodyguard" After Making Money

This strategy has a great design - trailing stop:

| Parameter | Value | Plain English |
|-----------|-------|---------------|
| trailing_stop | True | Turn on trailing |
| trailing_stop_positive | 0.08 | Stop line follows the rise, keeps 8% distance |
| trailing_stop_positive_offset | 0.10 | Activates after 10% profit |
| trailing_only_offset_is_reached | True | Don't trail until 10% is made |

**Plain English**:
> "When you're making money, I'll let you run first. Once you've made 10%, I'll assign you a bodyguard. The bodyguard follows the price up, keeping an 8% distance. If price pulls back more than 8%, the bodyguard drags you out immediately."

This design is clever - it lets you eat enough gains while not letting you give back too much profit.

---

## VI. The "Personality" of This Strategy

### ✅ Advantages (Praise Section)

1. **Simple Logic**: Just two indicators, easy to understand
2. **Fast In, Slow Out**: Buy with fast CCI(13), sell with slow CCI(76), aligns with trend trading philosophy
3. **Good Protection**: Trailing stop locks profits, 22% large stop loss gives room
4. **Not Flashy**: Simple parameters, not easy to overfit

### ⚠️ Disadvantages (Criticism Section)

1. **Few Signals**: CCI needs to drop to -188 to buy, those opportunities are rare
2. **Long Only**: Can't short, useless in downtrends
3. **Beating in Ranging Markets**: Trend strategy meets sideways movement = repeated beatings

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Clear Uptrend | 🟢 Use it! | Good dip-buying when trend is clear |
| 📉 Clear Downtrend | 🔴 Don't use | Strategy only goes long |
| 🔄 Wide Range | 🟡 Be careful | May get stopped repeatedly, but large stop loss can take it |
| ⚡️ Narrow Sideways | 🔴 Don't use | CCI extremes won't trigger at all |

---

## VIII. Summary: How's This Strategy Really?

### One-Liner Review
> "A concise trend pullback strategy, good for trending markets, be careful in ranging markets."

### Who Should Use It?
- ✅ Beginners learning (simple logic, easy to understand)
- ✅ Trend traders (buy dips in trends)
- ✅ People who like large stop loss space (-22% can take it)

### Who Shouldn't Use It?
- ❌ People seeking high-frequency trading (few signals)
- ❌ Ranging market traders
- ❌ People who want to short

### My Suggestions
1. **Combine with other strategies**: Can be used alongside ranging strategies
2. **Adjust CCI threshold**: If signals are too few, change -188 to -150
3. **Keep trailing stop on**: This is the highlight of this strategy, don't turn it off

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Fast In Slow Out Bottom-Fishing Philosophy

SwingHigh's money-making philosophy is simple:

> "Stocks going up will always pull back. I buy the dip at the deepest pullback, then patiently wait for it to go crazy."

- **MACD Golden Cross**: Confirms overall direction is up
- **CCI Extreme Value**: Finds the deepest pullback point
- **Fast In, Slow Out**: Quick entry response (CCI 13), patient exit (CCI 76)

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:-----------|:------------------|:--------------------------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | "Trend is here, pullbacks are free money! Dip-buying like crazy!" |
| 📉 Clear Downtrend | ⭐⭐☆☆☆ | "This strategy only goes long, downtrend means just watching." |
| 🔄 Wide Range | ⭐⭐⭐☆☆ | "Still playable, large stop loss helps you take it, but fees hurt a bit." |
| ⚡️ Narrow Sideways | ⭐☆☆☆☆ | "CCI won't hit -188/231 at all, strategy goes dormant." |

**One-Liner Summary**: It's a god when trends come, it's useless when ranging.

---

## X. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Suggested Value | Comment |
|------------|----------------|---------|
| Timeframe | 30m | Don't change, it's designed this way |
| Trading Pairs | 5-20 pairs | Too many and signals become even fewer |

### 10.2 Config File Key Settings

```yaml
# config.json key settings
"trailing_stop": true,
"trailing_stop_positive": 0.08,
"trailing_stop_positive_offset": 0.10,
"trailing_only_offset_is_reached": true,
"stoploss": -0.22274
```

### 10.3 Hardware Requirements

This strategy has minimal computation, doesn't need a high-end machine:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Fluid |
| 50+ pairs | 8GB | 16GB | No problem at all |

### 10.4 Backtesting vs Live Trading

**Backtesting Notes**:
- CCI extremes may trigger more frequently in historical data
- Trailing stop execution may differ between backtesting and live
- Recommend running demo for at least 1 month before live

**Recommended Flow**:
1. First backtest with default parameters
2. Then run demo for 1 month
3. Observe actual signal frequency
4. Adjust CCI thresholds if needed
5. Only go live after confirming stability

**Don't go all-in from the start**, no matter how good the strategy is, it needs to be calibrated!

---

## XI. Bonus: The Author's "Little Tricks"

Look carefully at the code, you'll find some interesting things:

1. **Different CCI periods for buy/sell**: Buy uses 13 period, sell uses 76 period
   > "The author designed this intentionally: buy fast, sell slow. This is the wisdom of an experienced driver."

2. **Large Stop Loss Space**: -22.27% with 5 decimal places precision
   > "Probably optimized by Hyperopt. The author gave plenty of error margin."

3. **Clean Comments**: Almost no comments in the code, very concise
   > "A strategy this clean was written by either a master or a lazy person (probably the former)."

---

## XII. The Very End

### One-Liner Review
> "Simple, effective, well-protected. A godsend in trending markets, trash in ranging markets."

### Who Should Use It?
- ✅ Beginners learning strategy logic
- ✅ Trend traders
- ✅ People who like large stop loss space
- ✅ People who want simple strategies

### Who Shouldn't Use It?
- ❌ Ranging market traders
- ❌ People seeking high-frequency signals
- ❌ People who need to short
- ❌ People who want complex strategies

### Manual Trader Recommendations
If you want to manually use this strategy:
1. Open a 30-minute candlestick chart
2. Add MACD indicator
3. Add CCI indicator (periods 13 and 76)
4. Wait for MACD golden cross + CCI(13) drops below -188
5. Enter, set trailing stop
6. Patiently wait for CCI(76) to rise above 231 before exiting

---

## XIII. ⚠️ Risk Emphasis Again (Must Read)

### Backtesting is Beautiful, Live Trading Needs Caution

SwingHigh's historical backtesting performance might look good - but note:

> **CCI thresholds -188/231 are quite extreme, signals may be infrequent in historical data. If you adjust thresholds, you might overfit.**

Simply put: **"Past 'golden parameters' aren't necessarily future 'money-making parameters'."**

### Hidden Risks of Trend Strategies

In live trading, trend strategies can lead to:
- **Repeated stop losses in ranging markets**: Trend strategies fear sideways most, may get nickle-and-dimed
- **Few signals**: CCI extremes don't happen often, patience is key
- **Trailing stop slippage**: Fast pullbacks may have larger slippage

### My Suggestion (From the Heart)

```
1. Run demo for at least 1 month first
2. Observe CCI signal frequency, if too few can loosen thresholds
3. Don't put all funds on this one strategy
4. Combine with other strategies to diversify risk
```

**Remember**: Trend strategies eat one wave at a time, no trend means no action. Staying alive is most important! 🙏

---

**Final Reminder**: No matter how good the strategy is, the market will humble you without warning. Test lightly, stay alive! 🙏