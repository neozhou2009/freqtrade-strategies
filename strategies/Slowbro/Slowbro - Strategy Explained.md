# Slowbro Strategy: The Lazy Range Harvester

> **Nickname**: Slowbro, Slowpoke, Range Ninja  
> **Occupation**: 30-Day Range Gatekeeper  
> **Timeframe**: 1 Hour (main) + 1 Day (information layer)

---

## I. What Is This Strategy?

Simply put, **Slowbro** is:
- A minimalist range breakout strategy
- Draws two lines using 30-day highs and lows
- Buys when price breaks below the floor, sells when it breaks above the ceiling

Like a **sleeping security guard**, only opens its eyes when price touches the boundary 🦥

The code is just over 100 lines, among the simplest of the 465 strategies. The name comes from the Pokémon "Slowbro"—slow, but steady!

---

## II. Core Configuration: "Two Lines, One Crossover"

### Take-Profit Rules (ROI Table)

```
Holding Time    Target Profit
─────────────────────
Immediate       10%
After 1 day     20%
After 2 days    30%
After 7 days    100% (Double!)
```

**Translation**: Gives you enough time to chase big trends. The longer you hold, the higher the target.

### Stop-Loss Rule

```
Fixed Stop-Loss: -10%
```

**Translation**: Run when down 10%, symmetric with first-tier take-profit. This strategy is fair—your target profit matches your loss limit.

---

## III. 1 Buy Condition: Just Wait

This strategy's buy condition is so simple it makes you question life:

### 🎯 The Only Buy Signal: Floor Crossover

**Core Logic**: Price crosses above the 30-day lowest price line from below

**Plain English**:
> "I watch the lowest price of the past 30 days and draw a line. When price drops near this line, I pay attention. Once it breaks upward, I buy."

**Code Snippet**:
```python
qtpylib.crossed_above(dataframe['close'], dataframe['30d-low'])
```

**Why called Slowbro?**
Because you might wait forever for a signal—a 30-day range doesn't break easily. Just like Slowbro, wait slowly, no rush 🐢

---

## IV. 1 Sell Condition: Ceiling Breakout

### 🚪 The Only Sell Signal: Ceiling Crossover

**Core Logic**: Price crosses above the 30-day highest price line from below

**Plain English**:
> "I watch the highest price of the past 30 days and draw a line. When price breaks above this line, I sell."

**Code Snippet**:
```python
qtpylib.crossed_above(dataframe['close'], dataframe['30d-high'])
```

**Note**: The "ceiling" here is dynamically updated! Updated once a day, following the price movement.

---

## V. Protection Mechanism: Basically Lying Flat

Slowbro's protection mechanism is very zen:

| Protection Type | Setting | Plain English |
|----------------|---------|---------------|
| Fixed Stop-Loss | -10% | "I run when down 10%" |
| Graded ROI | 4 tiers | "The longer I hold, the higher my target" |
| Profitable Sell | Only sell when profitable | "Don't sell at a loss, wait for recovery" |

**Critique**: This strategy basically has no fancy protection mechanisms, just relies on stop-loss + ROI. Simple and rough 🤷

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Minimalist design**: Less code, less chance of bugs
2. **Trend capturing**: Performs well in slow bull markets
3. **Low resource consumption**: Won't lag running 100 pairs
4. **Learning-friendly**: Beginners can understand in one read

### ⚠️ Cons (Criticism Section)

1. **Sparse signals**: Might wait weeks for one signal
2. **Oscillating market nightmare**: Repeatedly slapped in sideways markets—buy then drop, sell then rise
3. **Slow reaction**: 30-day range, market changes but it doesn't
4. **No dynamic adjustment**: Doesn't adapt to different volatility markets

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Slow Bull | Full send | Price rises slowly, range shifts up with it, perfect match |
| 🔄 Oscillation | Don't use | Will get slapped left and right, lose on fees |
| 📉 Bear Market | Careful | Designed for long positions, bear market is headwind |
| ⚡ High Volatility | Not recommended | Range can't keep up with price changes |

---

## VIII. Summary: How Is This Strategy?

### One-Liner Review
> "So simple it makes you question life, but actually works in slow bull markets."

### Who Should Use It?
- ✅ Quantitative beginners learning strategy development
- ✅ People wanting simple strategy combinations
- ✅ Slow bull market enthusiasts
- ✅ Lazy people who don't want to stare at charts all day

### Who Shouldn't Use It?
- ❌ People pursuing high-frequency trading
- ❌ People only active in oscillating markets
- ❌ People wanting complex strategies
- ❌ Impatient people (wait forever for signals)

### My Suggestions
1. **As a benchmark strategy**: Compare other complex strategies against it
2. **Combine use**: Combine with other signals to reduce false positives
3. **Manual trading reference**: Observe 30-day highs/lows as support/resistance
4. **Backtest validation**: Check performance on historical data first

---

## IX. What Markets Can This Strategy Make Money?

### 9.1 Core Logic: Range Is King

Slowbro's money-making philosophy:
- **Floor buying**: Price drops below 30-day low, might bounce
- **Ceiling selling**: Price breaks above 30-day high, might pull back
- **Time is on your side**: The longer you hold, the higher your profit target

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:-------------------------|
| 📈 Slow Bull | ⭐⭐⭐⭐⭐ | Range rises with it, buy floor sell ceiling, comfortable |
| 🔄 Oscillation | ⭐⭐☆☆☆ | Crosses up and down repeatedly, slapped countless times |
| 📉 Bear Market | ⭐⭐⭐☆☆ | Range shifts down, many buy signals but could be traps |
| ⚡ High Volatility | ⭐⭐☆☆☆ | Range updates too slowly, signals lag badly |

**One-liner Summary**: Money-maker in slow bull markets, fee-killer in oscillating markets.

---

## X. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Commentary |
|-------------|-------------------|-----------|
| Timeframe | 1h (default) | Don't go faster, signals will be even fewer |
| Stop-Loss | -10% (default) | Can go tighter, like -7% |
| Trading Pairs | Major coins | Don't run small caps, too volatile |

### 10.2 Key Config File Settings

```yaml
# config.json recommended settings
"timeframe": "1h",
"stoploss": -0.10,
"minimal_roi": {
    "0": 0.10,
    "1440": 0.20,
    "2880": 0.30,
    "10080": 1.0
}
```

### 10.3 Hardware Requirements (Important!)

This strategy has minimal computational load:

| Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|--------------|----------------|-------------------|------------|
| 1-10 pairs | 512MB | 1GB | Smooth |
| 10-50 pairs | 1GB | 2GB | Smooth |
| 50+ pairs | 2GB | 4GB | Still smooth |

**Warning**: This might be one of the lowest hardware requirement strategies 😅

### 10.4 Backtest vs. Live Trading

Advantage of simple strategies:
- Backtest results and live performance have small differences
- Won't get "fitted" to historical data

**Recommended Process**:
1. Run 1-year historical backtest first, check signal frequency
2. If signals are too rare (hard to get one a week), consider changing timeframe
3. Paper trade for 1 month, verify actual performance
4. Small capital live test

**Don't go all in right away**—even simple strategies need validation!

---

## XI. Easter Egg: The Author's "Little Thoughts"

Looking at code comments, you'll find interesting things:

1. **ASCII Art**: The author put a huge Slowbro ASCII drawing at the code beginning, hinting at this strategy's "dumb cute" attribute 🎨
   
2. **Version v100**: Only 100 lines of code, version number is also v100, interesting alignment

3. **Information Layer Design**: Using daily data mapped to hourly reflects the classic idea of "small timeframe trigger, big timeframe direction"

---

## XII. Final Words

### One-Liner Review
> "The epitome of minimalism, a textbook-level strategy for learning and research."

### Who Should Use It?
- ✅ Freqtrade beginners
- ✅ People wanting to study range breakout logic
- ✅ People needing a simple benchmark strategy
- ✅ Slow bull market believers

### Who Shouldn't Use It?
- ❌ High-frequency trading pursuers
- ❌ Mostly oscillating market traders
- ❌ Complex strategy combination seekers
- ❌ People who hate waiting for signals

### Suggestions for Manual Traders

This strategy's logic is very suitable for manual trading:
1. Draw 30-day highs/lows on your chart
2. Watch when price touches the low, consider buying on upward break
3. Consider selling when price breaks above the high
4. Set 10% stop-loss, start with 10% take-profit target

---

## XIII. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting Is Beautiful, Live Trading Needs Caution

Slowbro's historical backtest might perform excellently in **slow bull markets**—but there's a trap:

> **Range breakout strategies lose repeatedly in oscillating markets.**

Simply put: **Below the floor there's a basement, above the ceiling there's sky.**

### Hidden Risks of Simple Strategies

In live trading, simple logic can lead to:
- **Sparse signals**: Wait forever for a signal
- **Missing moves**: Small movements within the range are completely ignored
- **Oscillation slapping**: Repeatedly triggering false signals, losing on fees

### My Honest Advice

```
1. Run backtest first, check signal frequency for your chosen pairs
2. If fewer than a few signals a month, consider switching strategies
3. Can combine with other strategies, complement each other
4. Disable or reduce position in oscillating markets, don't force it
```

**Remember**: No matter how simple the strategy, respect the market. Light position testing, survival comes first! 🙏