# NostalgiaForInfinityV3: A Strategy That Doesn't Want to Miss Opportunities

## Table of Contents

1. [What Is This Thing?](#1-what-is-this-thing)
2. [How Does It Make Money?](#2-how-does-it-make-money)
3. [When Does It Buy?](#3-when-does-it-buy)
4. [When Does It Sell?](#4-when-does-it-sell)
5. [How Does It Handle Stoploss?](#5-how-does-it-handle-stoploss)
6. [What Indicators Does It Use?](#6-what-indicators-does-it-use)
7. [How Does It Read Timeframes?](#7-how-does-it-read-timeframes)
8. [How Big Is the Risk?](#8-how-big-is-the-risk)
9. [Which Coins Does It Work On?](#9-which-coins-does-it-work-on)
10. [How to Tune Parameters?](#10-how-to-tune-parameters)
11. [Can Beginners Use It?](#11-can-beginners-use-it)
12. [What to Watch for in Live Trading?](#12-what-to-watch-for-in-live-trading)
13. [Summary: Pros and Cons](#13-summary-pros-and-cons)

---

## 1. What Is This Thing?

In simple terms, this is an automated cryptocurrency trading strategy that runs on the Freqtrade quantitative trading platform.

### Where Did It Come From?

Written by someone named iterativ. They gave it a very artistic name — "Nostalgia For Infinity." This is the third version (V3), which means the author keeps improving it.

### What Kind of Strategy Is It?

**Medium-frequency** — not dozens of trades per day like high-frequency, not one trade per week like low-frequency. It basically catches opportunities when the market moves.

### What's Its Style?

One sentence: **"In an uptrend, find pullback entries; sell when it's risen too much."**

Not a "chase the pump, panic on the dump" strategy. Not a counter-trend bottom-fishing strategy either. It's more like "follow the trend, wait patiently."

---

## 2. How Does It Make Money?

### The Core Logic

Imagine you see a stock that's been climbing steadily, but suddenly drops one day. You think:

- Long-term trend is still up
- The short-term drop might be a temporary adjustment
- This could be a good entry opportunity

This strategy is based on exactly this thinking.

### More Specifically

1. **Confirm the big uptrend**: Use the 1-hour chart — MAs must be aligned for an uptrend
2. **Wait for a short-term pullback**: Use the 5-minute chart — price drops to the Bollinger lower band, RSI is oversold
3. **Confirm nothing catastrophic happened**: Pullback isn't a crash
4. **Buy**: Volume should be low — no one's panic selling
5. **Wait for it to rise, then sell**: When it's risen enough and indicators show overbought, exit

Simple in concept! Though there are many detailed conditions in practice, the core idea is exactly this.

---

## 3. When Does It Buy?

The strategy has **10 buy conditions** — buy if any one is satisfied. Let me explain each:

### Buy Condition 1: Classic Pullback Buy

**Plain English**: Big trend is climbing nicely, suddenly drops a bit — time to buy.

**Requirements**:
- On the 1-hour chart, MAs are in golden cross
- On the 5-minute chart, RSI drops below 36 (oversold)
- Volume isn't too high (not panic selling)
- Recent drop isn't too severe (safety margin)

### Buy Condition 2: Bollinger Lower Band Buy

**Plain English**: Price breaks below the Bollinger lower band, like a spring compressed to its limit — might bounce.

**Requirements**:
- Big trend is still up
- Price drops below the Bollinger lower band
- 5-minute RSI is much lower than 1-hour RSI (short-term severely oversold)
- But close is still above the long-term MA (trend support intact)

### Buy Condition 3: BB40 Break Buy

**Plain English**: Find oversold opportunities using the longer-period Bollinger Band (40-period).

**Requirements**:
- Bollinger Band must be wide open (width sufficient)
- Price breaks below the lower band
- Lower shadow isn't too long (not an extreme move)

### Buy Condition 4: Perfect MA Alignment Buy

**Plain English**: MAs are neatly arranged, perfect bull pattern, price pulls back to below EMA50.

**Requirements**:
- All MAs aligned from short to long: EMA15 > EMA50 > EMA100 > EMA200
- On the 1-hour chart too, it's in bull alignment
- Price drops below EMA50, even breaking through the Bollinger lower band

### Buy Condition 5: EMA Death Cross Rebound Buy

**Plain English**: Short-term MA crosses below long-term MA — seems like it's falling, but too much drop might bounce.

**Requirements**:
- EMA26 is above EMA12 (death cross state)
- Death cross magnitude is sufficient
- Price is below the Bollinger lower band

### Buy Condition 6: Trend Pullback BB Buy

**Plain English**: Similar to Condition 5, but focuses more on the long-term trend.

**Requirements**:
- 1h SMA200 is trending up
- Volume is very low
- Other conditions similar to Condition 5

### Buy Condition 7: RSI Oversold Buy

**Plain English**: Under trend support, RSI drops to a very low level.

**Requirements**:
- Long-term MA support is valid
- RSI < 41
- Volume should be low

### Buy Condition 8: Alligator Buy

**Plain English**: Use the Alligator indicator to spot when a trend is just starting.

**Requirements**:
- Alligator mouth opens (lips > teeth > jaw)
- All three lines are moving upward
- Close is above the lips
- RSI < 46 (still has room to rise)

### Buy Condition 9: EMA Pullback Buy

**Plain English**: Price is above the long-term MA but below the short-term MA — a typical pullback spot.

**Requirements**:
- Close > EMA200
- Close < EMA50
- Breaks below the Bollinger lower band

### Buy Condition 10: Extreme Oversold Buy

**Plain English**: Even the 1h RSI is oversold — might bounce.

**Requirements**:
- 1h RSI < 30
- Long-term trend is up
- Price breaks below the Bollinger lower band

---

## 4. When Does It Sell?

The strategy has **8 sell conditions** plus custom sell logic. Selling is simpler than buying — the core idea is "sell when it's risen too much."

### Sell Condition 1: BB Upper Band Consecutive Break

**Plain English**: Price is above the Bollinger upper band for 6 consecutive candles — risen too much.

**Requirements**:
- Current and past 5 candles, close is above the upper band
- RSI > 79.5

### Sell Condition 2: BB Upper Band Short Break

**Plain English**: Price above the upper band for 3 consecutive candles, RSI even higher.

**Requirements**:
- 3 consecutive candles above the upper band
- RSI > 81

### Sell Condition 3: Pure RSI Overbought

**Plain English**: RSI exceeds 82, just sell.

The simplest sell condition.

### Sell Condition 4: Dual-Timeframe RSI Overbought

**Plain English**: Both 5-minute and 1-hour RSI are high.

**Requirements**:
- 5min RSI > 73.4
- 1h RSI > 79.6

### Sell Condition 5: Below-EMA Rebound Sell

**Plain English**: Price was below the long-term MA, suddenly rebounds, RSI surges.

**Requirements**:
- Close < EMA200
- But RSI is very high (4.38+ above 1h RSI)

### Sell Condition 6: Below-EMA Extreme RSI

**Plain English**: Below the long-term MA, RSI is ridiculously high.

**Requirements**:
- Close < EMA200
- Close > EMA50 (bounced)
- RSI > 87.7

### Sell Condition 7: 1h RSI High + EMA Death Cross

**Plain English**: Large timeframe is overbought, small timeframe starting to weaken.

**Requirements**:
- 1h RSI > 81.7
- EMA12 crosses below EMA26

### Sell Condition 8: 1h BB Upper Band Break

**Plain English**: From the big timeframe perspective, it's risen too much.

**Requirements**:
- Close > 1h BB upper band × 1.1

---

## 5. How Does It Handle Stoploss?

The stoploss setup is very distinctive — **it's almost like there's no hard stoploss**:

```python
stoploss = -0.99  # -99%, practically disabled
```

### Why This Way?

Because crypto is volatile. A 5% stoploss might get hit every day. The strategy chooses to control risk in other ways.

### So What Protects the Capital?

**1. Trailing Stoploss**

```
Activates after 15% profit
Trails price upward, keeping 5% distance
If price retraces 5%, sell
```

**2. Tiered Profit-Taking**

```
Made 1% with RSI < 38 → sell
Made 5% with RSI < 43 → sell
Made 25% with RSI < 52 → sell
Made 45% with RSI < 50 → sell
```

**3. Trend Reversal Profit-Taking**

```
Have profit, but price falls below EMA200 → sell
Have profit, and long-term MAs start falling → sell
```

**4. Retracement Profit-Taking**

```
Profit 16%-38%, pulled back 15% from high → sell
Profit 3%-10%, pulled back 4.5% from high → sell
```

So while there's no hard stoploss, many mechanisms protect your profits.

---

## 6. What Indicators Does It Use?

### Main Indicators at a Glance

| Indicator | Period | Purpose |
|-----------|--------|---------|
| EMA | 12, 26, 50, 100, 200 | Trend, support/resistance |
| SMA | 5, 50, 200 | Trend |
| RSI | 14 | Overbought/oversold |
| Bollinger Bands | 20, 40 | Volatility, overbought/oversold |
| MFI | 14 | Money flow |
| Alligator | 5, 8, 13 | Trend start detection |

---

## 7. How Does It Read Timeframes?

### Dual-Timeframe Design

**Main chart: 5 minutes**
- All buy/sell signals generated on the 5-minute chart
- Maintains sufficient trading frequency
- Captures short-term price movements

**Auxiliary chart: 1 hour**
- Confirms the big trend
- Filters fake signals
- Provides more reliable judgment

### Why This Design?

Think of watching a movie:
- The 5-minute chart is like individual frames — you can see the details
- The 1-hour chart is like the movie's main plot — you can see the big picture

---

## 8. How Big Is the Risk?

### Biggest Risk: No Hard Stoploss

**What the strategy does**:
1. Entry conditions are already strict, requires uptrend
2. Has pullback limits, won't buy during crashes
3. Uses trailing stoploss and tiered profit-taking for profitable positions

**But the problem**:
- If trend reverses after entry, losses can be significant
- Extreme moves happen in crypto markets
- Trailing stoploss needs to first be profitable to activate

### Another Risk: Too Many Parameters

**Benefits**: optimizable
**Drawbacks**: easy to overfit (looks great in backtests, poor in live trading)

### Overall Risk Rating: **Medium-High**

**Suitable for**:
- People with some quantitative trading experience
- Willing to spend time learning and optimizing
- Can handle moderate drawdowns

**Not suitable for**:
- Complete beginners
- Low risk tolerance
- People seeking steady returns

---

## 9. Which Coins Does It Work On?

### Author's Recommendations

**Suitable**:
- Stablecoin-quoted pairs (USDT, BUSD, etc.)
- Mainstream coins (BTC, ETH, BNB, etc.)
- High-liquidity coins

**Not suitable**:
- BTC or ETH-quoted pairs
- Leveraged tokens (*BULL, *BEAR, *UP, *DOWN)
- New coins, altcoins

### Why Stablecoin-Quoted?

Because BTC and ETH themselves fluctuate a lot.

### Recommended Pair Count: 20-80
### Recommended Concurrent Positions: 4-6

---

## 10. How to Tune Parameters?

### Parameters Overview

**Condition toggle parameters**:
- Enable/disable for 10 buy conditions
- Enable/disable for 8 sell conditions

**RSI threshold parameters**:
- Various overbought/oversold thresholds
- Different thresholds for different conditions

**Recommendation for beginners**: **Don't adjust first!**

Default parameters are tested by the author. Just use them as-is.

---

## 11. Can Beginners Use It?

### First Conclusion: Not Recommended for Direct Use

**Reasons**:
1. High complexity: 10 buy + 8 sell conditions, many custom logic rules
2. Risk exists: no hard stoploss
3. Needs tuning: different markets need different parameters
4. Needs monitoring: automation doesn't mean no management required

### What Beginners Should Do

1. **Learn the basics first**
2. **Paper trade first** (dry_run: true mode)
3. **Small capital live trading** (like 100U)
4. **Gradually add capital**

---

## 12. What to Watch for in Live Trading?

### Pre-Launch Checklist

1. **Sufficient data**: Need at least 400 candles of data
2. **Correct timeframe**: Set in config as "5m"
3. **Don't override strategy parameters**
4. **Trading pair settings**: whitelist stablecoins, blacklist leveraged tokens

### Post-Launch Monitoring

**Daily**: positions, P/L ratio, max drawdown
**Weekly**: trade record analysis, win rate changes
**Monthly**: strategy performance evaluation

---

## 13. Summary: Pros and Cons

### Pros

**Comprehensive signal system**:
- 10 buy conditions covering multiple market patterns
- 8 sell conditions judging exit timing from multiple angles

**Multi-timeframe confirmation**:
- 5-minute chart finds entry points
- 1-hour chart confirms big trend
- Reduces fake signals

**Flexible risk management**:
- Trailing stoploss protects profits
- Tiered profit-taking locks in gains
- Trend reversal exits timely

**Highly customizable**:
- Many adjustable parameters
- Each condition independently toggleable
- Supports hyperparameter optimization

### Cons

**High complexity**:
- Large codebase, hard to fully understand
- Too many parameters, difficult to optimize
- High maintenance cost

**No hard stoploss**:
- Can suffer large losses in extreme moves
- Trailing stoploss needs prior profit

**Trend-dependent**:
- All buys require uptrend
- May underperform in ranging and bear markets

**Fixed timeframe**:
- Only 5m + 1h
- Cannot adapt to all market cycles

**Overfitting risk**:
- Too many parameters = easy to over-optimize

### Final Verdict

NostalgiaForInfinityV3 is a well-designed strategy. Its core philosophy — "find pullbacks within trends" — is time-tested.

But its complexity and risk control approach require users to have sufficient experience and psychological resilience.

If you're a beginner, start with simpler strategies. If you have some experience, this strategy is worth studying deeply.

---

*Document Version: v1.0 Colloquial Version*
*Strategy Author: iterativ*
