# NostalgiaForInfinityV4 (NFI4): The "Let Your Robot Do the Work" Strategy

## 1. What Is This Thing?

NostalgiaForInfinityV4 (let's just call it NFI4) is an automated crypto trading bot that runs on Freqtrade. Think of it as a 24/7 robot trader that watches candlestick charts, and when conditions are met, it automatically buys or sells.

The core philosophy: **follow the big trend, buy when price pulls back, sell when it's risen too much.**

---

## 2. What Timeframe Does It Use?

NFI4 watches two timeframes simultaneously:

**Primary View: 5-Minute Chart**
Every 5 minutes, a new candle forms. This is the main basis for decisions. The 5-minute chart is flexible — captures intraday swings without being so sensitive that it trades on noise.

**Secondary View: 1-Hour Chart**
Used to confirm the big picture direction. When the 1-hour chart shows uptrend and the 5-minute chart shows a price pullback, that's when you consider buying. This prevents "bottom-fishing in a downtrend" — the classic money-losing move.

Think of it like this: the 5-minute chart is a magnifying glass (catches details), the 1-hour chart is a telescope (shows the big picture). Using both together gives you a clearer view.

---

## 3. What Indicators Does It Watch?

### 3.1 Moving Averages (MA)

Moving averages smooth out price data into a line. Two types:

**EMA (Exponential MA)**: Cares more about recent prices, faster reaction. The strategy uses EMA12, EMA20, EMA26, EMA50, EMA100, EMA200.

**SMA (Simple MA)**: Treats all prices equally, smoother. The strategy uses SMA5, SMA30, SMA200.

How they're used:
- Price above EMA200 = long-term uptrend
- EMA50 above EMA200 = medium-term uptrend
- Most buy conditions require "trend is up" — confirmed by these MAs

### 3.2 RSI (Relative Strength Index)

A number from 0 to 100:
- Below 30: oversold (might bounce) — **good time to look for buys**
- Above 70: overbought (might pull back) — **good time to look for sells**

The strategy heavily uses RSI. Buy when RSI is low, sell when RSI is high.

### 3.3 MFI (Money Flow Index)

Like RSI but incorporates volume too. If RSI is low but MFI isn't low, it might be a false dip. If both are low, it's a genuine oversold.

### 3.4 Bollinger Bands

Three lines around price:
- Upper band: overbought zone
- Lower band: oversold zone

The strategy uses two sets: BB20 (standard) and BB40 (longer period, more stable).

### 3.5 EWO (Elliott Wave Oscillator)

Calculates the difference between two EMAs:
- Positive EWO = uptrend momentum is strong
- Negative EWO = might be deeply oversold

---

## 4. How Does It Avoid Bad Entries?

This strategy's biggest strength isn't what it buys — it's what it **won't** buy.

### Won't Chase Pumps (Pump Protection)

If a coin surged 46%+ in 24 hours, the strategy won't chase it:
- Big surges usually pull back
- Chasing gets you trapped at the top

The strategy checks 24h, 36h, and 48h windows. If a coin has pumped too much, it waits for a pullback first.

### Won't Catch Falling Knives (Dip Protection)

If a coin is still crashing:
- Strategy waits for the crash to slow
- Waits for stabilization signals
- Won't blindly bottom-fish

The protection checks 4 time windows: current candle, last 2 candles, last 12 candles, and last 144 candles.

Three protection levels: **strict** (only buys on tiny dips), **normal**, and **loose** (accepts bigger dips).

### Won't Buy When BTC Is Falling (BTC Protection)

Bitcoin is the market leader. When BTC drops, most alts drop too. The strategy checks BTC's trend and suppresses buy signals when BTC is in a downtrend.

---

## 5. When Does It Buy? (17 Ways!)

The strategy has **17 different buy conditions**. Satisfy any one and it buys. Here are the main types:

### Buy 1: Classic Pullback Buy

Big trend is still up, but price pulled back and RSI shows oversold.

**Requirements**:
- 1h EMA50 > EMA200 (medium-term uptrend)
- SMA200 rising
- Not too much of a recent pump
- RSI < 23.4 (deeply oversold)
- MFI < 21.7 (money flow also oversold)

**Plain English**: The big trend is healthy, but RSI says price got beaten up — time to buy.

### Buy 2: Bollinger Lower Band Buy

Price broke below the Bollinger lower band, and RSI is much lower on the 5m chart than on the 1h chart.

**Requirements**:
- 1h SMA200 rising
- Not a recent pump
- Volume < 8.3x average (low volume)
- RSI much lower than 1h RSI (5m very oversold vs. 1h)
- Price < BB lower band × 0.977

**Plain English**: Price at the floor with volume drying up — someone quietly bought in, and now you can too.

### Buy 4: Low Volume, Low Price

Price is below EMA50 and the Bollinger lower band, with extremely low volume.

**Requirements**:
- Big trend is up
- Price below EMA50
- Price below BB lower band × 0.933
- Volume < 32x the 30-period average

**Plain English**: Quiet market, nobody's selling — price is cheap and nobody's pushing it down. A good entry spot.

### Buy 8: Alligator Opens

The Alligator indicator (three smoothed MAs) is fully aligned upward — lips > teeth > jaw, all trending up.

**Requirements**:
- Price above 1h EMA200 × 98.8%
- 1h EMA50 > EMA100
- 1h SMA200 rising
- Alligator is fully open upward
- RSI < 41.3

**Plain English**: The Alligator indicator shows a strong trend is just starting. Trend confirmed, RSI still has room to climb — buy!

### Buy 17: Extreme Oversold

When EWO drops below -17.9 (extremely negative), price has likely oversold severely.

**Requirements**:
- Price below EMA20 × 0.97
- EWO < -17.9 (extreme oversold)
- Dip protection satisfied

**Plain English**: Market panic selling — when fear is at its peak, a bounce is likely. This is contrarian buying at its finest.

---

## 6. When Does It Sell? (8 Ways!)

### Sell 1: Bollinger Upper Band Streak

Price is above the Bollinger upper band for 6 consecutive candles, and RSI > 65.4.

**Plain English**: Price keeps punching through the roof — it's overheated, take profits!

### Sell 3: RSI Overbought

RSI > 81.1 — simple and direct.

**Plain English**: RSI is way too high — even if you haven't made much, sell!

### Sell 5: Below EMA200 + RSI Divergence

Price fell below EMA200, but RSI is higher than the 1h RSI by more than 4.4 points.

**Plain English**: Price is below the safety line but somehow RSI is still strong — this is a fake rally, get out!

### Sell 8: Broke Through 1h Bollinger Upper

Price exceeds 129.3% of the 1h Bollinger upper band.

**Plain English**: Blew right through the ceiling — this can't last, sell!

---

## 7. The Smart Sell: Dynamic Profit-Taking

### Tiered Profit-Taking

Based on how much you've made, it decides when to sell:

| Made This Much | RSI Must Be Below | Why |
|--------------|-------------------|-----|
| > 58.7% | 54.5 | Made big money, take it whenever |
| > 6.7% | 47.92 | Getting good, take profits |
| > 8.3% | 45.91 | Made decent, take more |
| > 1.2% | 48.33 | Made something, be more careful |

**The logic**: The more you've made, the more lenient the sell conditions — don't be greedy!

### Trend Breakdown = Exit

- Made > 1.2% but price fell below EMA200: out
- Made > 8.8% but SMA200 is falling: out
- Made > 12.1% but price fell below EMA100: out

**Logic**: You have profits, but the trend is breaking down — lock them in.

### Trailing Retracement

If you've made a lot but it starts pulling back:
- Made 19.3-50% and pulled back 15.4% from peak: sell
- Made 4.6-13% and pulled back 8.9% from peak: sell

**Logic**: Don't let hard-earned profits evaporate.

---

## 8. What Is Trailing Stoploss?

Here's how it works:
1. You buy at $100
2. Price rises to $105 (5% profit, exceeds 3% threshold)
3. Trailing stop activates at $104 ($105 - 1%)
4. Price keeps climbing to $110, trailing stop moves to $108.9
5. Price drops to $108.9, triggers sell — you locked in 8.9% profit!

**Plain English**: Like climbing a mountain — each time you climb higher, you move your safety line up. If you slip, you only fall to the last safety point, not all the way down.

---

## 9. What to Watch Out For?

### Timeframe Must Be Right

Strategy is designed for 5-minute charts. Don't change it.

### Pair Selection

- Use stablecoin pairs (USDT, BUSD), not BTC pairs
- Pick 40-80 pairs
- Blacklist leveraged tokens (BULL, BEAR, UP, DOWN)

### Config Settings

```json
{
  "timeframe": "5m",
  "use_sell_signal": true,
  "sell_profit_only": false,
  "ignore_roi_if_buy_signal": true
}
```

### Position Count

**4-6 concurrent positions** is the sweet spot — not too many, not too few.

---

## 10. Can You Tune Parameters?

Yes! Each of the 17 buy conditions has its own on/off switch.

**Default enabled**: 1, 2, 3, 4, 7, 9, 11, 12, 13, 14, 16, 17
**Default disabled**: 5, 6, 8, 10, 15

Each sell condition is also toggleable:
**Default enabled**: 3, 5, 8
**Default disabled**: 1, 2, 4, 6, 7

### Tuning Tips

**Conservative** (fewer but higher quality signals): Enable fewer conditions, make thresholds stricter.

**Aggressive** (more signals but more risk): Enable more conditions, loosen thresholds.

**Recommendation**: Start with defaults, then fine-tune based on your backtest results.

---

## 11. Pros and Cons

### Pros

1. **Comprehensive protection**: Pump protection, dip protection, and BTC filtering keep you out of bad trades
2. **Many entry opportunities**: 17 buy conditions, something triggers in most market conditions
3. **Smart exits**: Tiered profit-taking, trailing stoploss, and trend-break exits
4. **Highly customizable**: Every condition individually toggleable
5. **Multi-timeframe confirmation**: 5m + 1h cross-validation improves signal quality

### Cons

1. **Too many parameters**: Over 100 optimizable parameters — easy to overfit
2. **Wide stoploss**: -10% stoploss might be too loose for some traders
3. **High trading frequency**: 5-minute charts mean more trades per day
4. **Extreme market risk**: Protection mechanisms may fail during flash crashes

---

## 12. Practical Tips

### 1. Backtest First

Don't use real money immediately! Use at least 6 months of historical data, including bull, bear, and ranging markets.

### 2. Roll Out in Batches

Don't go all-in:
- Start with 10-20% of planned capital
- Observe performance
- Gradually increase

### 3. Review Regularly

Markets change — review and adjust monthly:
- Which conditions are working?
- Which conditions are losing?
- Do parameters need updating?

### 4. Don't Be Greedy

Set your stoploss and respect it:
- One big loss wipes out ten small wins
- Don't override the strategy because "it'll bounce back"

---

## 13. Summary

**NostalgiaForInfinityV4** is a comprehensive automated trading strategy. Its core philosophy — "buy dips in uptrends, sell when overbought" — is a time-tested approach.

**Best suited for**:
- Traders with some experience
- People who can accept moderate risk
- People willing to backtest and optimize

**Not suited for**:
- Complete beginners
- Low risk tolerance individuals
- Get-rich-quick seekers

**Core reminder**: No strategy is perfect. Backtest results don't guarantee future performance. Start small, test thoroughly, and scale up gradually.

**Risk warning**: Cryptocurrency trading is risky. Invest only what you can afford to lose.

---

*Document Version: V1.0*
*Strategy: NostalgiaForInfinityV4*
