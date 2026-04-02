# PRICEFOLLOWING Strategy: The "Bottom Fishing Master" of Moving Averages

> **Nickname**: The Bottom Fisher  
> **Occupation**: Contrarian operator who buys on dips and sells on rallies  
> **Timeframe**: 5 minutes

---

## I. What Is This Strategy?

Simply put, **PRICEFOLLOWING** is:

- Sees moving average cross downward → buys (likes to catch bottoms)
- Sees moving average cross upward → sells (takes profits)
- Opposite mindset from most people—"buy more as it falls more"

Like that friend of yours who always likes to step in when stocks have dropped to their underwear 🤣

---

## II. Core Configuration: "Cautious Bottom Fishing, Quick Escapes"

### Take Profit Rules (ROI Table)

```
Buy and immediately rise 4% → Run!
Hold 30 minutes and rise 3% → Run!
Hold 60 minutes and rise 2.5% → Still run!
```

**Translation**: This strategy focuses on short-term quick in-and-out, taking any profit and running, no greed.

### Stop Loss Rules

```
Fixed stop loss: Lose 10% and accept defeat
Trailing stop: After making 3%, activates, runs if retraces 2%
```

**Translation**: Sets two lines of defense for you—

- First line: If loss exceeds 10%, unconditional stop loss (life-saving line)
- Second line: When profitable, system automatically locks in profits (profit-protecting line)

For example, if you're up 5% after buying, the trailing stop line rises to 3%. If price retraces to 3%, auto-sell ensures you keep at least 3% profit.

---

## III. Buy Conditions: Two Ways to Play

### 🎯 Mode 1: RSI Filter Mode (Disabled by Default)

**Core Logic**: RSI shows oversold + moving average crosses downward = buy

**Plain English**:
> "RSI below 30 means it's dropped too much. At this point, EMA7 crossing down through TEMA looks like continued decline, but the strategy thinks 'it's dropped so much, should bounce soon' and buys."

**Conditions**:
1. RSI < 30 (default, adjustable)
2. EMA7 crosses downward through TEMA from above

**Critique**: This logic is indeed counterintuitive—moving average crossing downward is typically bearish, but the strategy chooses to buy. Classic "buy when others are fearful" style.

---

### 📉 Mode 2: Pure Moving Average Mode (Enabled by Default)

**Core Logic**: EMA7 crosses below TEMA + TEMA is declining = buy

**Plain English**:
> "EMA7 crossing below TEMA indicates short-term trend weakness, plus TEMA itself is heading down—looks bleak. The strategy says: 'Great opportunity!' and buys."

**Conditions**:
1. EMA7 crosses downward through TEMA from above
2. TEMA current value lower than previous candle (currently declining)

**Critique**: This is a pure "buy on dips" strategy, completely opposite to chasing highs. If the market truly enters a bear market, this bottom-fishing strategy might catch falling knives halfway down.

---

## IV. Protection Mechanism: Two "Safety Belts"

Every buy action comes with protection parameters:

| Protection Type | Purpose | Plain English |
|----------------|---------|---------------|
| Fixed Stop Loss 10% | Accept defeat if loss too big | "If I lose 10%, I give up, no more gambling" |
| Trailing Stop 2%/3% | Lock in floating profits | "After making 3%, if it drops 2% I'm running with profits" |

**Critique**: 10% fixed stop loss is a bit wide for a 5-minute strategy. BTC fluctuating 5% in a day is normal, 10% stop loss might only trigger when the market really crashes 🤣

---

## V. Sell Logic: Run When It Rises

### 5.1 Sell Conditions

**Mode 1: RSI Filter On (Default)**

```
RSI < 70 + EMA7 crosses above TEMA = sell
```

**Plain English**:
> "RSI hasn't reached overbought territory (below 70), then EMA7 crosses above TEMA, indicating short-term trend strengthening. Strategy says: 'Good enough, run!'"

**Critique**: RSI < 70 is way too loose—normal market conditions have RSI below 70 most of the time, so this basically equals no filter.

---

**Mode 2: RSI Filter Off**

```
EMA7 crosses above TEMA = sell
```

**Plain English**:
> "EMA7 crosses above TEMA, that's the only condition, sell!"

**Classic Line**:
> "Rose? Run if it rose! Don't wait for it to drop back and regret!"

---

### 5.2 ROI Forced Exit

Strategy also has "sell when time's up" mechanism:

| Holding Time | Profit Required |
|--------------|-----------------|
| Just bought | Sell if up 4% |
| 30 minutes | Sell if up 3% |
| 60 minutes | Sell if up 2.5% |

**Plain English**:
> "If it goes up 4% right after buying, sell immediately! If it takes 30 minutes to go up 3%, still sell! If it takes an hour to go up 2.5%, still sell! In short, don't be greedy!"

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Section)

1. **Simple Logic**: Just one moving average crossover, understandable with middle school math
2. **Adjustable Parameters**: RSI threshold, moving average parameters all optimizable
3. **Dual Stop Loss**: Fixed stop + trailing stop, won't lose your principal
4. **Low Computing Needs**: Low hardware requirements, even a Raspberry Pi can run it
5. **Good for Learning**: About 200 lines of code, beginners won't get dizzy

### ⚠️ Cons (Critique Section)

1. **Counterintuitive Logic**: Buying when moving average crosses down feels like "catching falling knives"
2. **Wasted Calculations**: Code calculates ADX, MACD, SAR, Hilbert but doesn't use any
3. **Idle Parameter**: `ema_pct` defined but nowhere used, probably legacy
4. **Wasted Information Layer**: Gets ETH, BTC, RVN 15-minute data but completely unused in trading logic
5. **Ineffective RSI Filter**: RSI < 70 for selling basically doesn't work

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Oscillating Sideways | ✅ Recommended | High sell low buy, oscillating markets are mean reversion's home turf |
| Slow Decline | ⚠️ Use Cautiously | Bottom fishing may succeed, but don't catch halfway down |
| One-way Uptrend | ❌ Don't Use | Strategy sells during rise, then can't buy back |
| Violent Volatility | ❌ Don't Use | Stop loss gets triggered frequently, fees eat profits |

---

## VIII. Summary: How Is This Strategy?

### One-Line Review
> "A simple-logic but contrarian-thinking bottom fishing strategy—while others chase highs, you catch bottoms."

### Who Should Use It?
- ✅ Beginners wanting to learn moving average crossover systems
- ✅ Traders who like contrarian operations and dare to catch bottoms
- ✅ Running on oscillating market pairs
- ✅ Users with low hardware requirements wanting simple strategies

### Who Shouldn't Use It?
- ❌ Trend traders who like chasing highs and selling lows
- ❌ Running in one-way bullish markets
- ❌ Users needing complex multi-factor strategies
- ❌ People who can't accept "catching falling knives" risk

### My Recommendations
1. **Turn On RSI Filter**: RSI filter is off by default, recommend enabling, buying at oversold is safer
2. **Adjust Stop Loss**: 10% stop loss is too wide for 5-minute strategy, recommend 3%-5%
3. **Use Larger Timeframe**: Check 1-hour or 4-hour trend, avoid repeatedly bottom fishing during major downtrends
4. **Choose Right Pairs**: Choose pairs with moderate, regular volatility, don't use this on meme coins

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Mean Reversion

PRICEFOLLOWING is a classic **mean reversion strategy**. Its money-making philosophy:

> "What drops a lot will rise, what rises a lot will drop—buy when dropping, sell when rising."

**Characteristics**:
- **Contrarian Thinking**: Buy when others are fearful, sell when others are greedy
- **Short-term Operation**: 5-minute timeframe, quick in and out
- **Technical Driven**: Completely relies on moving average crossover signals

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 One-way Uptrend | ⭐⭐☆☆☆ | Strategy sells early in uptrend, then watches helplessly as it keeps rising, can't buy back |
| 🔄 Oscillating Sideways | ⭐⭐⭐⭐⭐ | This is the home turf! Up and down oscillation repeatedly takes profits |
| 📉 Slow Decline | ⭐⭐⭐☆☆ | Bottom fishing might succeed, but if real bear market comes, 10% stop loss won't hold |
| ⚡ Violent Volatility | ⭐⭐☆☆☆ | Trailing stop gets swept back and forth, fees will kill you |

**One-sentence Summary**: This is a strategy for oscillating markets, don't use it in trending markets.

---

## X. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Notes |
|------------|-------------------|-------|
| Number of pairs | 3-10 | Too many can't monitor, too few not diversified |
| Pair selection | Mainstream + moderate volatility | Don't pick meme coins, will get swept repeatedly |
| Timeframe | 5m (default) | Can also try 15m, signals more stable |

### 10.2 Key Config File Settings

```yaml
# Recommended configuration
"rsi_enabled": true,          # Turn on RSI filter
"rsi_value": 25,              # Lower RSI threshold, buy at oversold
"sell_rsi_enabled": false,    # Don't use RSI for selling, just watch moving averages
"trailing_stop_positive_offset": 0.04,  # Start trailing after 4% profit
"trailing_stop_positive": 0.025,        # Trail at 2.5%
"stoploss": -0.05             # Adjust stop loss to 5%
```

### 10.3 Hardware Requirements (Important!)

This strategy has minimal calculation needs, almost no hardware requirements:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-5 pairs | 512MB | 1GB | Raspberry Pi can run |
| 5-20 pairs | 1GB | 2GB | Smooth |
| 20+ pairs | 2GB | 4GB | No pressure |

**Warning**: Don't run too many pairs just because the strategy is simple, position management is most important!

### 10.4 Backtest vs Live

**Backtest Recommendations**:
1. At least 3 months of historical data
2. Include both oscillating and trending market phases
3. Pay attention to slippage and fee settings

**Live Recommendations**:
1. Test with small capital for 1-2 weeks first
2. Observe difference between actual fill prices and backtest
3. Monitor stop loss trigger frequency

**Don't go all-in right away**, mean reversion strategies lose badly in trending markets!

---

## XI. Easter Egg: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **Defined but Unused Parameters**
   ```python
   ema_pct = DecimalParameter(0.0001, 0.1, ...)
   ```
   > "I defined this parameter but won't tell you where I use it (actually nowhere)" 🤣

2. **Calculated but Unused Indicators**
   ```python
   dataframe['adx'] = ta.ADX(dataframe)
   dataframe['sar'] = ta.SAR(dataframe)
   # MACD, Hilbert also not used in trading logic
   ```
   > "I calculated a bunch of indicators to show off, actual buy/sell only looks at EMA crossover~"

3. **Fetched but Unused Information Layer**
   ```python
   def informative_pairs(self):
       return [("ETH/USDT", "15m"), ("BTC/USDT", "15m"), ("RVN/USDT", "15m")]
   ```
   > "I monitor ETH, BTC, RVN 15-minute data, but guess if I use it? Nope!"

---

## XII. The Final End

### One-Line Review
> "Clean code, clear logic, but contrarian thinking—suitable for oscillating markets, avoid trending markets."

### Who Should Use It?
- ✅ Quantitative beginners wanting to learn moving average systems
- ✅ Pairs in oscillating markets
- ✅ Traders who like contrarian thinking
- ✅ Users with low hardware specs

### Who Shouldn't Use It?
- ❌ Chase high sell low types
- ❌ One-way bullish markets
- ❌ People pursuing complex multi-factor strategies
- ❌ People who can't handle "catching falling knives"

### Manual Trader Recommendations

If you trade manually, you can reference this strategy's thinking:

1. **EMA Crossover as Reference**: EMA7 and TEMA crossover does reflect trend changes
2. **Watch RSI Oversold Zone**: RSI < 30 does have higher bounce probability
3. **Set Good Stop Loss**: 10% is too wide, recommend 3%-5%
4. **Look at Larger Timeframes**: 1-hour or 4-hour to confirm major trend direction, avoid contrarian bottom fishing

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Part)

### Backtest Looks Beautiful, Live Trading Be Careful

PRICEFOLLOWING's historical backtest might perform well in oscillating markets—but there's a trap:

> **Mean reversion strategies are naturally suited for oscillating markets, but no one knows when oscillation ends and trend begins.**

Simply put: **You think you're catching the bottom, but you're catching halfway down the knife.**

### Hidden Risks of Complex Strategies

Although this strategy has simple logic, risks aren't small:

- **Catching Falling Knives Risk**: Buying on decline might catch ever-lower knives
- **Stop Loss Too Wide**: 10% stop loss too wide for short-term strategy, one loss offsets ten wins
- **Trend Reversal**: Oscillating market suddenly becomes trending, strategy keeps losing
- **Over-optimization**: Hyperopt parameters easily overfit historical data

### My Recommendations (Honest Words)

```
1. Only use on clearly oscillating pairs
2. Adjust stop loss from 10% to 3%-5%
3. Enable RSI filter, buy only when RSI < 25
4. Use 15-minute timeframe, reduce noise
5. Maximum position no more than 20% of total capital
```

**Remember**: Bottom fishing strategies fear most when "the bottom is still below." The market cures all不服 (disbelief), test with small positions, staying alive is most important! 🙏

---