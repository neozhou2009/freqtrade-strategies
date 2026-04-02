# BBRSITV Strategy: RSI Meets Bollinger Bands, EWO Keeps Watch

> **Nickname**: RSI Through Bollinger Bands  
> **Job**: The "Rebel" of the Momentum School — Doesn't Play by the Rules  
> **Timeframe**: 5 minutes

---

## I. What is This Strategy?

Simply put, **BBRSITV** is:
- RSI stuffed inside Bollinger Bands to measure "dispersion"
- EWO (Elliott Wave Oscillator) acting as the "bouncer"
- A "trend pullback player" that only buys dips in uptrends

Like a smart bottom-fisher: **Doesn't blindly catch bottoms — first confirms the trend is up, then waits for price to pull back before striking** 🎯

This strategy was ported from a popular TradingView indicator called "RSI + BB (EMA) + Dispersion (2.0)". The original author applied Bollinger Bands to RSI, creating a new way to judge overbought/oversold conditions.

---

## II. Core Configuration: Simply Put, "Make 10% and Run, Lose 25% and Admit Defeat"

### Take Profit Rules (ROI Table)

```
Profit reaches 10% → Auto sell
```

**Translation**: This is a medium-term strategy, not looking for long-term holds. 10% target is neither too ambitious nor too modest, giving enough room for volatility.

### Stop Loss Rules

```
Hard stop loss: -25% (lose a quarter and admit defeat)
Trailing stop: Activates after 2.5% profit, tracks with 0.5% distance
```

**Translation**:
- 25% stop loss is pretty wide — giving plenty of room to "ride the roller coaster"
- Trailing stop is a bit "stingy" — won't activate until you've made 2.5%, then only leaves 0.5% room for pullback
- Meaning: **Protect my profits, but first prove you can make money**

### Protection Mechanism (Prevents "Tilting After Losing")

| Protection Type | Trigger Condition | Penalty |
|----------------|-------------------|---------|
| LowProfitPairs | A pair loses 5% | Pause that pair for 1 hour |
| MaxDrawdown | Total drawdown exceeds 20% | Pause everything for 1 hour |

**Translation**:
- One coin getting crushed? Cool off for an hour
- Overall losing big? Full stop, take a breather

---

## III. Buy Conditions: RSI Through Bollinger Bands

The strategy's buy logic has one core concept: **RSI breaks below Bollinger Band lower band + EWO confirms trend is up**.

### 🎯 Core Logic Breakdown

**Step 1: Put Bollinger Bands on RSI**

Normal Bollinger Bands are drawn on price — this strategy draws them on RSI instead!

```
RSI's EMA (middle band) = Average of last 22 RSI candles
RSI's Standard Deviation = How much RSI has been fluctuating over last 22 candles
Lower Dispersion Threshold = Middle band - Standard Deviation × 1.74
```

**Plain English**:
> "RSI, where have you been hanging out lately? Let me draw a warning line — if you fall below this line, you're 'too low'."

**Step 2: Let EWO Be the "Bouncer"**

```python
EWO = (5-period EMA - 200-period EMA) / Current Price × 100
```

**Plain English**:
> "EWO > 4.86 means short-term average is above long-term average, trend is up. When RSI breaks below the lower band in this case, it's a 'good opportunity' — otherwise it's 'don't catch that falling knife'!"

### Buy Signal Summary

| Condition | Formula | Plain English |
|-----------|---------|---------------|
| #1 | RSI < Middle band - StdDev × 1.74 | "RSI broke through the Bollinger Band lower band, it's too low!" |
| #2 | EWO > 4.86 | "Trend is up, safe to bottom-fish now" |
| #3 | volume > 0 | "Someone needs to be trading" |

---

## IV. Sell Logic: Run When RSI Gets Too High

Selling is much simpler than buying — just two conditions, meet one and run:

### Signal #1: RSI Absolute Value Too High

```
RSI > 72 → Sell
```

**Plain English**:
> "RSI is over 72, better run before getting trapped!"

### Signal #2: RSI Breaks Above Bollinger Band Upper Band

```
RSI > Middle band + StdDev × 1.895 → Sell
```

**Plain English**:
> "RSI is floating above the Bollinger Band upper band, momentum is too strong, time to rest."

### Note

The strategy has `sell_profit_only = True`, meaning:
- **Only responds to sell signals when making money**
- Need at least 1% profit to trigger sell

**Complaint**:
> This setting is a bit "conservative" — even if RSI hits the sell signal while underwater, it won't sell, just waits for stop loss. Want to change that? Edit the config yourself!

---

## V. This Strategy's "Personality Traits"

### ✅ Pros (Praise Time)

1. **Innovative Concept**: Putting Bollinger Bands on RSI — that's a clever move. Traditional Bollinger Bands look at price, this one looks at RSI — like going one level deeper into "relative position."

2. **Rigorous Trend Confirmation**: Won't buy just because RSI is low — needs EWO to say "trend is up" first. This is called "don't release the hawk until you see the rabbit."

3. **Flexible Parameters**: Buy parameters and sell parameters are separate, can be adjusted independently. Also provides 5 variant versions — there's one for you.

4. **Solid Protection Mechanism**: Single coin loss pause + total drawdown pause — won't let you "tilt harder after losing."

5. **Refined Trailing Stop**: Won't start trailing until 2.5% profit — not right after opening a position. Very reasonable design.

### ⚠️ Cons (Complaint Time)

1. **Stop Loss Too Wide**: 25% stop loss — for conservative types, that's "way too much heart." Losing 25% in a day is no joke.

2. **5-Minute Timeframe Too Tiring**: Needs constant watching, not suitable for part-time traders. Want to use this strategy? Better quit your job (just kidding).

3. **Parameter Sensitive**: Adjusting the for_sigma parameter a tiny bit can lead to very different trading results. Newbies can easily get burned by parameter optimization.

4. **Doesn't Handle Ranging Markets Well**: EWO filter is too strict, almost no trades in ranging markets, low capital utilization.

5. **No Volume Analysis**: Just volume > 0, which is basically no volume analysis at all. Completely ignores big players moving in and out — feels like "trading blindfolded."

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Clear Uptrend | Full position (with position management) | EWO filter effective, precisely captures pullback entries |
| 🔄 Mild Range | Small position to test waters | Can make money but profit limited |
| 📉 Sustained Downtrend | Turn off the strategy | EWO will block most buys, basically running for nothing |
| ⚡ High Volatility No Direction | Don't use | Lots of false signals, fees eat all profits |

---

## VII. Summary: How Is This Strategy Really?

### One-Sentence Review
> **"A smart bottom-fisher's tool — check the trend first, wait for pullback, let RSI through Bollinger Bands give you the signal."**

### Who Is It For?
- ✅ Quant traders with programming skills (parameter optimization required)
- ✅ Day traders pursuing medium-term trades
- ✅ "Technical types" who understand RSI and Bollinger Bands
- ✅ People willing to spend time backtesting and optimizing

### Who Is It NOT For?
- ❌ Complete beginners (concepts too twisted, easy to get confused)
- ❌ Conservative investors (25% stop loss unacceptable)
- ❌ Long-term investors (5-minute timeframe too tiring)
- ❌ Manual traders (calculations complex, monitoring exhausting)

### My Recommendations

1. **Choose the Right Market First**: Prioritize coins in clear uptrends, skip downtrending ones.

2. **Must Backtest Parameters**: Don't use default parameters directly — at least backtest 3 months of data to see performance.

3. **Try the Variants**: BBRSITV4 and BBRSITV5 might fit current markets better than the default version — don't get stuck on one.

4. **Position Control**: Don't go all-in — this strategy's signal frequency isn't that high, enter in batches for stability.

---

## VIII. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: "Contrarian Thinking" in the Momentum School

BBRSITV belongs to the **"Trend Pullback School"** — when the major trend is up, wait for a pullback to buy. The code isn't huge, but the logic is elegant.

**Its Money-Making Philosophy**:

- **Go With the Trend**: EWO ensures trend is up before acting
- **Contrarian Entry**: RSI drops to Bollinger Band lower band — "contrary to small fluctuations"
- **Trend-Following Exit**: RSI shoots to Bollinger Band upper band — exit with the momentum

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Clear Uptrend | ⭐⭐⭐⭐⭐ | Designed for this scenario, EWO keeps giving green lights, every RSI pullback is a buy |
| 🔄 Mild Range | ⭐⭐⭐☆☆ | Can make money, but few signals, limited profit space |
| 📉 Sustained Downtrend | ⭐⭐☆☆☆ | EWO directly blocks most buys, basically "spectator mode" |
| ⚡ High Volatility No Trend | ⭐☆☆☆☆ | All kinds of false signals, buy and get slapped in the face |

**One-Sentence Summary**:
> **Find the right trend, this strategy is a "money-picking machine"; find the wrong trend, it's in "silent power-saving mode."**

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Note |
|-------------------|-------------------|-------|
| Number of Pairs | 3-5 pairs | Too few = not enough signals; too many = protection triggers frequently |
| Pair Types | Major coins + Popular alts | Need enough liquidity, avoid those "trading a few thousand dollars a day" coins |
| Timeframe | 5m (default) | Can try 15m to reduce trade frequency |

### 9.2 Hardware Requirements (Decent)

This strategy doesn't need much computation, a regular VPS can run it:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-3 pairs | 1GB | 2GB | Smooth |
| 4-8 pairs | 2GB | 4GB | Normal |
| 9+ pairs | 4GB | 8GB | No problem |

### 9.3 Backtest vs Live Trading

**Backtest Recommendations**:
- At least 3 months of historical data
- Include uptrend, ranging, and downtrend phases
- Test all 5 variants separately

**Live Trading Notes**:
- 5-minute timeframe is sensitive to network latency
- Ensure exchange API is stable
- Recommend paper trading for 1-2 weeks first

---

## X. Bonus: The Strategy Author's "Little Secrets"

Look carefully at the code, and you'll find some interesting things:

1. **Buy and Sell Parameters Are Different**:
   > Buy uses 22-period EMA, sell uses 65-period EMA
   > 
   > "I want to buy fast, but sell slow — let profits run"

2. **5 Variant Versions**:
   > BBRSITV1-5 are all parameter-optimized for different scenarios
   > 
   > "Don't know which to use? Backtest and pick the best"

3. **TradingView Original Code Hidden in Comments**:
   > A big chunk of Pine Script comments in the populate_indicators function
   > 
   > "Original flavor, check it yourself if you want to see the raw logic"

4. **EWO Fast/Slow Line Parameters**:
   > fast_ewo=50, slow_ewo=200
   > 
   > "Not the standard 5/200, changed to 50/200 — interesting adjustment"

---

## XI. Final Thoughts

### One-Sentence Review
> **"Advanced RSI play — put Bollinger Bands on RSI to see dispersion, add EWO to guard the trend. For players with some experience."**

### Who Is It For?
- ✅ Those who understand RSI and Bollinger Band principles
- ✅ Those pursuing medium-term trading
- ✅ Those with time for parameter optimization
- ✅ Those who can handle 25% drawdown

### Who Is It NOT For?
- ❌ Complete beginners
- ❌ Extreme risk-averse types
- ❌ Those wanting passive income
- ❌ Manual traders

### Manual Trader Recommendations

Honestly, this strategy isn't suitable for manual trading:
- 5-minute timeframe, watching is exhausting
- Calculating RSI's Bollinger Bands, brain not enough
- EWO needs real-time updates, manual impossible

**Want to play manually? Search TradingView for "RSI + BB (EMA) + Dispersion" — someone's written the indicator, just watch for signals.**

---

## XII. ⚠️ Risk Warning Again (Must Read)

### Backtesting Looks Great, Live Trading Be Careful

BBRSITV's historical backtest performance is often **good** — but note:

> **Many parameters can easily "fit" the optimal solution for past prices, doesn't guarantee future performance.**

Simply put: **Great at memorizing answers, not necessarily great at taking the test.**

### Hidden Risks of Complex Strategies

In live trading, this strategy might lead to:
- **Sparse Signals**: EWO filter too strict, ranging markets might only have a few signals a day
- **Slippage Impact**: 5-minute timeframe demands fast execution, slow and you miss the best price
- **Wide Stop Loss**: 25% stop loss, hit a "black swan" event and you could lose months of profits in a day

### My Advice (From the Heart)

```
1. Backtest at least 6 months, covering different market environments
2. Test all 5 variants separately, pick the most stable
3. Run live for 1-2 weeks first, observe signal quality and execution efficiency
4. Initial position no more than 20% of total capital
5. Regularly review, stop immediately if anything seems wrong
```

**Remember**: No matter how good the strategy, when the market teaches you a lesson, it won't give advance notice. Light position testing, survival is most important! 🙏

---

**Strategy Source**: TradingView - "RSI + BB (EMA) + Dispersion (2.0)"  
**Strategy Author**: Freqtrade Community Port  
**Nickname**: RSI Through Bollinger Bands