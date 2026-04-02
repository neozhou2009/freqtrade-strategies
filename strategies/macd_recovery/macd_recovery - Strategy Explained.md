# MACD_Recovery Strategy: The Trend Pullback "Bargain Hunter"

> **Nickname**: Bargain Hunter, Pullback Harvester  
> **Profession**: Sniper who only "buys the dip" in uptrends  
> **Timeframe**: 5 minutes

---

## I. What Is This Strategy?

Simply put, **MACD_Recovery** is a strategy that:
- Only works in uptrends
- Waits for price pullbacks to buy cheap
- Uses MACD golden cross to confirm entry timing

It's like **waiting for the subway**: You don't chase after it; you stand on the platform and board when it stops 🚇

---

## II. Core Configuration: "Quick In, Quick Out"

### Take-Profit Rules (ROI Table)

```
Just bought: Target around 3%
5 hours later: Target drops to 2.9%
10 hours later: Target drops to 2.5%
...
35 hours later: No matter what, get out!
```

**Translation**: The strategy wants to make money fast. If you buy and it doesn't rise, it'll bail after about a day and a half.

### Stop Loss Rules

```
Loss reaches 4%, unconditional retreat
```

**Translation**: Stop loss is set quite tight, allowing maximum 4% loss. This means you can easily get "shaken off," but it also ensures you won't lose big.

---

## III. 1 Buy Condition: Three Conditions Combined

This strategy's buy condition looks like one, but actually contains three conditions that must be satisfied **simultaneously**:

### 🎯 Three-in-One Buy Condition

**Plain English**:
> "I'm waiting for three things to happen together: 1) RSI minimum in the last 8 candles dropped below 41 (oversold); 2) Price is above EMA200 (uptrend); 3) MACD golden cross (momentum reversal)."

**Classic Lines**:
```python
# Buy Conditions
(
    (dataframe['rsi'].rolling(8).min() < 41) &      # RSI is a bit low
    (dataframe['close'] > dataframe['ema200']) &    # Trend is upward
    (qtpylib.crossed_above(dataframe['macd'], 
                           dataframe['macdsignal'])) # MACD golden crossed!
)
```

> "RSI oversold + Uptrend + MACD golden cross = Perfect entry point!"

**Breakdown**:
- **RSI < 41**: Price has pulled back enough, selling pressure is almost exhausted
- **Price > EMA200**: Big trend is upward, not catching a falling knife
- **MACD Golden Cross**: Momentum is starting to reverse, confirming upward movement

---

## IV. 1 Sell Condition: Take Profits and Run

### 4.1 Sell Signal

**Plain English**:
> "I'm waiting for three things to happen together: 1) RSI maximum in the last 8 candles shot above 93 (overbought); 2) MACD is still positive (still in bullish zone); 3) MACD death cross (momentum weakening). Run!"

**Classic Lines**:
```python
# Sell Conditions
(
    (dataframe['rsi'].rolling(8).max() > 93) &      # RSI is too high!
    (dataframe['macd'] > 0) &                       # MACD still bullish
    (qtpylib.crossed_below(dataframe['macd'], 
                           dataframe['macdsignal'])) # But already death crossed
)
```

> "RSI hit 93, MACD still above zero but starting to death cross—if you don't run now, when will you?"

### 4.2 11-Level Take-Profit Table

Besides the sell signal, there's a super detailed take-profit table:

```
Time           Target Return
─────────────────────────
0 minutes      3.024%
~5 hours       2.924%
~10 hours      2.545%
~14 hours      2.444%
~16 hours      2.096%
~21 hours      1.709%
~23.5 hours    1.598%
~28 hours      1.22%
~31.5 hours    0.732%
~34 hours      0.493%
~35 hours      0% (forced exit)
```

**Plain English**: After buying, hope it rises fast. If it rises slowly, I'll lower expectations. More than 35 hours (about a day and a half) and still not profitable? Bye bye!

---

## V. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Section)

1. **Simple Logic**: Three conditions combined, crystal clear, not too much, not too little
2. **Trend Filtering**: EMA200 ensures only trading in uptrends, not against the trend
3. **Time Constraint**: 35-hour forced exit, capital won't be occupied indefinitely

### ⚠️ Weaknesses (Complaint Section)

1. **Fewer Signals**: Only one combined buy condition, may miss other opportunities
2. **Stop Loss Too Tight**: 4% stop loss can easily get "shaken" out by the market
3. **No Trailing Stop**: Can't run with the trend when it rises; can only wait for sell signal

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| 📈 Moderate Uptrend | ✅ Recommended | Best scenario, many pullback entry opportunities |
| 🔄 Oscillating Uptrend | ✅ Can use | EMA200 filtering can avoid false breakouts |
| 📉 Downtrend | ❌ Don't use | EMA200 filtering will result in very few signals |
| ⚡ High Volatility | ⚠️ Caution | 4% stop loss can be frequently triggered |

---

## VII. Summary: How Is This Strategy Really?

### One-Sentence Evaluation
> "A 'bargain hunter' that waits for pullbacks in uptrends, simple logic, suitable for beginners to learn."

### Who Should Use It?
- ✅ Beginners learning trend strategies
- ✅ Traders who prefer simple logic
- ✅ 5-minute level short-term traders
- ✅ People wanting to understand EMA/RSI/MACD combination usage

### Who Should NOT Use It?
- ❌ People pursuing complex strategies
- ❌ Those needing more entry signals
- ❌ People who don't like tight stop losses
- ❌ Those wanting to go long in downtrends

### My Recommendations
1. **Backtest first**: Test effects on different currencies and timeframes
2. **Adjust stop loss**: Can appropriately relax to 5% based on volatility
3. **Add filtering**: If signals are too few, can lower RSI threshold to 35
4. **Small capital test**: Verify with small capital in live trading

---

## VIII. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: Trend Pullback Trading

MACD_Recovery is a **trend pullback strategy**. Its profit philosophy:

> **"Don't chase the rise, wait for pullback; trend exists, then I come."**

- **EMA200 Filtering**: Only trade in bull markets
- **RSI Oversold**: Wait for price to pull back into place
- **MACD Golden Cross**: Confirm reversal before entering

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Moderate Uptrend | ⭐⭐⭐⭐⭐ | Many pullback opportunities, stable trend, simply home court |
| 🔄 Oscillating Uptrend | ⭐⭐⭐⭐☆ | Has trend, has pullbacks, can capture swings |
| 📉 Downtrend | ⭐☆☆☆☆ | EMA200 filtering leaves you with almost no signals |
| ⚡️ High Volatility | ⭐⭐☆☆☆ | 4% stop loss easily gets penetrated, frequent small losses |

**One-Sentence Summary**: **Only suitable for uptrends, rest during downtrends, don't force it.**

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|--------|--------|------|
| Trading Pairs | Major currency pairs | Don't use currencies with poor liquidity |
| Timeframe | 5m (default) | Can try 15m |

### 9.2 Hardware Requirements (Easy)

This strategy has extremely low computational requirements:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------|---------|---------|------|
| 1-10 pairs | 1GB | 2GB | Smooth |
| 10-50 pairs | 2GB | 4GB | No pressure |

**Comment**: Can run on a Raspberry Pi, don't worry about hardware!

### 9.3 Backtesting vs Live Trading

Due to simple logic, differences between backtesting and live trading are not large. Main points to note:
- **Slippage**: 5-minute level, slippage may eat away some profits
- **Latency**: Exchange latency may miss best entry price
- **Stop Loss Hit**: 4% stop loss is relatively tight, may trigger more easily in live trading than backtesting

**Recommended Process**:
1. First validate with historical data backtesting
2. Test with demo trading for 1-2 weeks
3. Small capital live trading test
4. Adjust parameters based on results

**Don't go all-in immediately**; even the best strategy needs磨合!

---

## X. Easter Egg: The Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **RSI threshold set to 41 instead of 30**
   > "I don't want to wait too long, start preparing when RSI hits 41."

2. **35-hour forced exit**
   > "If it's not profitable after a day and a half, this trade is a failure, hurry to the next one."

3. **Stop loss 4.032%, precise to decimal point**
   > "This number was definitely optimized, not just randomly set by me."

---

## XI. Last But Not Least

### One-Sentence Evaluation
> "Simple trend pullback strategy, suitable for beginner learning and moderate uptrend markets."

### Who Should Use It?
- ✅ Beginners learning strategy logic
- ✅ People who like simple and clear things
- ✅ 5-minute short-term traders
- ✅ People wanting to understand EMA/RSI/MACD combination

### Who Should NOT Use It?
- ❌ People pursuing complex strategies
- ❌ Those wanting more signals
- ❌ People wanting to trade in downtrend markets
- ❌ Those who don't like tight stop losses

### Manual Trader Recommendations
Can manually apply this logic:
1. Draw EMA200 on the chart
2. Wait for price pullback, RSI below 41
3. Observe MACD golden cross signal
4. Set 4% stop loss, target 3%

---

## XII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Backtesting Is Beautiful, Live Trading Requires Caution

MACD_Recovery's historical backtesting performance may be **pretty good**—but there's a trap:

> **Simple strategies are often parameter-sensitive; optimized numbers (4.032% stop loss, 41 RSI threshold) may just "happen" to fit historical data.**

Simply put: **"Working well in the past doesn't mean it will work well in the future."**

### Hidden Risks of Tight Stop Loss

In live trading, tight 4% stop loss may lead to:
- **Frequently shaken out**: Normal volatility triggers stop loss
- **Slippage amplifies losses**: Actual execution price may be worse
- **Missing subsequent rebound**: Price rises again after stop loss

### My Recommendations (Honest Truth)

```
1. Test with demo trading for at least two weeks first
2. Consider relaxing stop loss to 5%
3. Only use in clear uptrends
4. Pause strategy or switch to other strategies during downtrends
```

**Remember**: Trend strategies make money in trending markets, lose money in sideways markets. Recognizing market environment is more important than choosing strategies!

---

**Final Reminder**: No matter how good the strategy, the market won't say hello when it teaches you a lesson. Light position testing, staying alive is most important! 🙏
