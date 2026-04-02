# Seb Strategy: The "Minimalist" of EMA Crossovers

> **Nickname**: The EMA Prince
> **Role**: Trend Follower
> **Timeframe**: 5 minutes

---

## I. What is This Strategy?

Simply put, **Seb** is:
- Code so simple you'll question your life choices
- Just one buy condition, one sell condition
- Uses EMA crossover + Heikin Ashi candles to confirm trends

Like a **craftsman who does one thing but does it well** - not fancy, but effective.

---

## II. Core Configuration: "Lock Profits, Don't Be Greedy"

### Take Profit Rules (ROI Table)

```
Immediately  → 5% profit? Take it
20 minutes   → 4% is fine too
30 minutes   → 3% is acceptable
60 minutes   → 1% is whatever
```

**Translation**: This strategy is the "take what you get" type - profit targets decrease over time, doesn't fall in love with positions.

### Stop-Loss Rules

```
Hard stop-loss: -10% (final line)
Trailing stop: Activates at 2% profit, exits on 1% pullback
```

**Translation**: Accept -10% as a loss, but once you're profitable, set protection - don't let gains become losses.

**Example**:
- Entry price $100
- Rises to $102 (2% profit), trailing stop activates
- Stop set at $101 (1% pullback)
- Continues to $105, stop rises to $103.95
- Pulls back to $103.95, auto-sell, locks in ~4% profit

---

## III. Buy Conditions: Just One, Simple and Direct

### The Only Buy Signal

**Condition Breakdown**:

| Condition | Plain English |
|-----------|---------------|
| EMA20 crosses above EMA50 | Short-term MA golden cross above medium-term MA |
| HA close > EMA20 | Price above MA |
| HA green candle | Heikin Ashi is green (bullish) |

**Plain English**:
> "Short-term MA crosses above medium-term MA, price above MA, and it's a bullish candle - BUY!"

**Translation**:
- **EMA Crossover**: Like seeing a green light, you can go
- **Price Above MA**: Like having tailwind, less resistance
- **Green Candle**: Like clear road ahead, no worries

---

## IV. Sell Logic: Also Just One, Symmetrical Design

### The Only Sell Signal

**Condition Breakdown**:

| Condition | Plain English |
|-----------|---------------|
| EMA50 crosses above EMA100 | Medium-term MA golden cross above long-term MA |
| HA close < EMA20 | Price below MA |
| HA red candle | Heikin Ashi is red (bearish) |

**Plain English**:
> "Medium-term MA crosses above long-term MA, price breaks below short-term MA, and it's a bearish candle - SELL!"

Wait, isn't this a "golden cross"? Why sell?

**Key Point**: The logic uses **different periods for buy and sell**:
- Buy: EMA20/50
- Sell: EMA50/100

**Plain English**:
> "Buy looks at 'small trend starting', sell looks at 'big trend reversing'."

---

## V. This Strategy's "Personality"

### Pros (The Good Stuff)

1. **Simple and Understandable**: Code is clean, even beginners can understand
2. **Trend Confirmation**: Dual verification (MA + candle), not guessing
3. **Trailing Stop**: Auto-protection after profit, not greedy
4. **Official Example**: Produced by freqtrade, standard code
5. **High Extensibility**: Pre-calculated many indicators, easy to optimize

### Cons (The Not-So-Good Stuff)

1. **Few Signals**: Only one buy condition, low trading frequency
2. **Oscillating Markets Kill**: May get repeatedly stopped out in sideways
3. **Wasted Indicators**: Calculated a bunch but doesn't use them
4. **Unoptimized Parameters**: Buy/sell params are decoration, you have to tune

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Clear Trend | ✅ Default parameters | MA crossover strategy's home field |
| Sideways Oscillation | ⚠️ Widen stop-loss | May get frequent false breakouts |
| Rapid Decline | ❌ Don't use | Very few buy signals, no short protection |
| Low Volatility | ⚠️ Extend timeframe | Can try 15m or 1h |

---

## VII. What Market Can This Strategy Make Money In?

### 7.1 Core Logic: Trend Following, No Dips, No Tops

Seb is a **classic trend following strategy**. Its profit philosophy:

> **"Get on when trend comes, get off when trend goes, do nothing in between."**

- **Trend Identification**: EMA crossover tells you trend direction
- **Trend Confirmation**: Heikin Ashi filters false signals
- **Trend Protection**: Trailing stop locks in profits

### 7.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English |
|-------------|--------|---------------|
| Uptrend | ⭐⭐⭐⭐⭐ | MA crossover perfectly captures trend, money maker |
| Oscillating Market | ⭐⭐☆☆☆ | Repeated slaps in the face, stop-losses galore |
| Downtrend | ⭐☆☆☆☆ | Almost no buy signals, just watching |
| Fast Volatility | ⭐⭐⭐☆☆ | Trailing stop can protect some profits |

**One Line Summary**: Use when there's trend, hide when sideways.

---

## VIII. Want to Run This Strategy? Check These Configs

### 8.1 Trading Pair Configuration

| Configuration | Recommended | Comment |
|--------------|-------------|---------|
| timeframe | 5m | Default, can try 3m or 15m |
| trailing_stop_positive | 0.01 | Trail distance 1%, can adjust to 1.5% |
| trailing_stop_positive_offset | 0.02 | Activation threshold 2%, can adjust to 2.5% |

### 8.2 Hardware Requirements (So Minimal!)

This strategy has simple calculations, very low machine requirements:

| Trading Pairs | Min Memory | Recommended | Experience |
|--------------|-----------|-------------|------------|
| 1-50 pairs | 1GB | 2GB | Runs easily |
| 50-100 pairs | 2GB | 4GB | No pressure |
| 100+ pairs | 4GB | 8GB | Piece of cake |

**Tip**: This strategy is truly resource-friendly, old computers can run it.

### 8.3 Optimization Suggestions

Code calculates a bunch of indicators but doesn't use:

```
Used: EMA20, EMA50, EMA100, Heikin Ashi
Unused: RSI, MACD, Bollinger, Stochastic, ADX, CCI, SAR, Fisher RSI, Hammer
```

**You can add filters to entry conditions**:

```python
# Example: Add RSI filter
(dataframe['rsi'] < 70)  # Don't buy when overbought
```

**Or use Hyperopt to optimize parameters**:

```python
buy_rsi = IntParameter(low=1, high=100, default=30, space='buy', optimize=True)
sell_rsi = IntParameter(low=1, high=100, default=70, space='sell', optimize=True)
```

---

## IX. Easter Egg: The Strategy Author's "Little Details"

Look carefully at the code, you'll find some interesting things:

1. **Calculated tons of indicators, but only uses EMA and HA**
   > "Calculated just in case, for future optimization"

2. **Buy/sell params are all Hyperopt parameters**
   > "Default values are examples, you Hyperopt for optimal"

3. **Candlestick patterns not used either (Hammer)**
   > "Reserved reversal signals, waiting for your creativity"

4. **Code comments are detailed**
   > "This is a teaching strategy, not a money-making strategy"

---

## X. Summary: How Good Is This Strategy?

### One-Line Verdict
> "Simple to the extreme, just a classic EMA crossover strategy, suitable for learning and optimization."

### Who Should Use It?
- ✅ Beginner newbies (clean code, easy to understand)
- ✅ People learning quant (official example)
- ✅ People wanting to optimize themselves (reserved many indicators)
- ✅ Resource-limited machines (low computation)

### Who Shouldn't Use It?
- ❌ Those wanting to make money directly (too few signals)
- ❌ Those trading in oscillating markets (false breakouts galore)
- ❌ High-frequency traders (5-minute level)
- ❌ Those not wanting to tune parameters (default params are average)

### My Recommendation
1. **Learn First**: Understand EMA crossover and Heikin Ashi principles
2. **Then Backtest**: Verify strategy performance with historical data
3. **Then Optimize**: Use Hyperopt to find optimal parameters
4. **Finally Live**: Start with small capital, see actual results

---

## XI. ⚠️ Risk Re-emphasis (Must Read)

### Backtesting Looks Great, Live Needs Caution

Seb as an official example strategy was designed for **teaching** —

> **It shows how to write a complete strategy, but doesn't guarantee profits.**

Simply put: **The code is textbook quality, not money-printing machine quality.**

### Hidden Strategy Risks

In live trading, you may encounter:
- **Too Few Signals**: Wait forever for a buy
- **False Breakouts**: EMA crossover then immediately reverses
- **Trailing Stop Sweeps**: High volatility easily swept out
- **Lagging Trend Judgment**: MAs always lag behind price

### My Suggestion (Honest Truth)

```
1. Treat it as a learning template, not a money-making machine
2. Use Hyperopt to optimize parameters, don't use defaults
3. Add some filter conditions to improve signal quality
4. Backtest at least a year to verify strategy effectiveness
5. Start with small capital, don't go all-in from the start
```

**Remember**: Simple strategies are easy to understand but also easy for the market to "play with". Add more filter conditions, improving win rate is the way!

---

## XII. Final Note

### Strategy Positioning

Seb is a **teaching strategy**:
- Standard code structure
- Complete indicator calculations
- Detailed comments
- Easy to extend

**Its value isn't in making money directly, but in teaching you how to write strategies.**

### Beginner Roadmap

```
Step 1: Read and understand the code
   ↓
Step 2: Understand EMA crossover and Heikin Ashi
   ↓
Step 3: Run backtests to see results
   ↓
Step 4: Use Hyperopt to optimize parameters
   ↓
Step 5: Add filter conditions to improve win rate
   ↓
Step 6: Small capital live verification
```

### Advanced Optimization Directions

1. **Add RSI Filter**: Don't trade at overbought/oversold
2. **Add Volume Filter**: Confirm trend strength
3. **Add MACD Confirmation**: Dual trend verification
4. **Dynamic Parameters**: Adjust stop distance based on market volatility
5. **Multi-Timeframe**: Look at big timeframe trend, small timeframe entry

---

**Final Reminder**: Simple is an advantage but also a disadvantage. The market is complex, simple strategies need you to put thought into optimization! Good luck!

---