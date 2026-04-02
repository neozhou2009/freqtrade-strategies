# ClucMay72018 Strategy: The Oversold Bargain Hunter

> **Nickname**: Oversold Bargain Hunter / Bollinger Band Assassin
> **Profession**: Counter-Trend Bottom-Fishing Pro
> **Timeframe**: 5 Minutes

---

## 1. What's This Strategy?

Simply put, **ClucMay72018** is:
- Price dropped below Bollinger Bands? Buy!
- Price bounced back to Bollinger middle band? Sell!
- What? Volume suddenly exploded? Never mind then, might be a trap 🕳️

It's like browsing a thrift market:
> "This thing originally cost 100, now it's 50% off and nobody wants it — definitely cheap, I'm buying! When it goes back to 70%, I'll sell it for a profit!"

This is a classic **mean reversion** approach — price deviating too far from its normal range will eventually come back.

The strategy was authored by **Gert Wohlgemuth**, whose design philosophy is: buy at oversold levels, sell when price returns to normal. Sounds like a "value investor"? But it's actually a **short-term trading strategy**, 5-minute level, specifically for capturing intraday swings.

---

## 2. Core Settings: Basically "Make 1% and Run"

### Take-Profit Rules (ROI Table)

```python
minimal_roi = {
    "0": 0.01  # Make 1% and bail
}
```

**Translation**: Whatever, make 1% and I'm out!

### Stop-Loss Rules

```python
stoploss = -0.05  # Cut losses at 5%
```

**Translation**: Maximum 5% loss, if it drops further I'm out — won't let myself get trapped!

### Timeframe

```python
timeframe = '5m'  # 5-minute level
```

**Plain English**: This is an **intraday strategy** — no overnight holds, buy and sell the same day.

---

## 3. 1 Buy Condition: Let Me Break It Down For You

This strategy appears to have only one buy condition, but it actually **has layers** — composed of 3 sub-conditions, and all three must be met simultaneously to buy:

### 🎯 Core Buy Formula

```
Buy = (Price < EMA100) AND (Price < Bollinger lower band × 0.985) AND (Volume < 20× average)
```

Here's it translated into plain English:

| Sub-Condition | Code | Plain English |
|--------------|------|---------------|
| Condition 1 | `close < ema100` | Price must be below the long-term moving average — can't chase in an uptrend |
| Condition 2 | `close < 0.985 × bb_lowerband` | Price must be 1.5% below the Bollinger lower band — must be super-super-oversold |
| Condition 3 | `volume < avg × 20` | Volume can't be too large — prevents buying "crashing like a mountain collapse" false rebounds |

**Personified Interpretation**:

> Strategy inner monologue: "Yo, this coin's price has dropped to the point where even its mother doesn't recognize it, and it's still falling on shrinking volume — not panic selling. I see it clearly, this dip is done for. I'm going in to pick up a bargain, and when it bounces back I'm out!"

---

## 4. Protection Mechanism: Volume Filtering

This strategy doesn't have a bunch of protection parameters like other strategies, but it has one **invisible protection**:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| Volume Filtering | Volume < 30-day avg × 20 | Must be "quietly" falling — can't be a volume-driven crash |

**Why is this so important?**

Think about it — if volume is exploding downward, that means the market is panicking, everyone's selling. If you jump in to buy at that point, aren't you catching a falling knife? The strategy is smart: it wants **shrinking volume**, which means the selling pressure has no more gas left, price is roughly at the bottom, and that's when the odds of winning are highest.

---

## 5. Exit Logic: Sell When It Returns to Normal

### 5.1 Sell Condition

```python
# Sell when price breaks above Bollinger middle band
close > bb_middleband
```

**Plain English**: Price has bounced back from oversold to "normal" fluctuation range — get out now!

### 5.2 Exit Logic Diagram

```
Upper Band ─────────────── ⚠️  Rallied too much, not chasing
Middle Band ─────────────── ✅  Sell here! Mean reversion complete
Lower Band ─────────────── 🔥  Oversold zone, can buy
```

**Personified Interpretation**:

> Strategy inner monologue: "Alright, price has climbed back from the valley to normal levels. I'm not being greedy — taking profits and selling selling selling!"

---

## 6. Strategy "Personality"

### ✅ Pros

1. **Simple and Brutal**: Just one buy condition, one sell condition — no need to memorize a bunch of complex rules
2. **Counter-Trend Bottom-Fishing**: Specifically buys oversold coins — sounds cool, right?
3. **Small Computational Load**: No complex models to run — works on any computer or even a phone
4. **Ranging Market Specialist**: Swimming freely in sideways consolidation markets
5. **Intraday Trading**: Settles the same day, no overnight risk worries

### ⚠️ Cons

1. **Exits Too Early**: Sells as soon as price breaks the middle band — the rest of the rally is none of your business
2. **Worthless in Trending Markets**: In sustained downtrends, may buy and lose repeatedly
3. **Fixed Parameters**: EMA100 and Bollinger parameters are hardcoded — may need adjustment for different coins
4. **Bull Markets Are None of Your Business**: Can't trigger buy conditions when price is rising — watching others make money

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📊 Ranging Market | Use aggressively | Price fluctuates within range, mean reversion logic perfectly aligned! |
| 📉 Downtrend | Use sparingly | May "catch falling knives" — be careful |
| 📈 Uptrend | Don't use | Buy conditions can't trigger — just watch |
| ⚡️ Sideways Consolidation | Suitable | No clear trend is when the strategy is most steady |

---

## 8. Summary: How Does This Strategy Really Stack Up?

### One-Line Verdict
> **"Zen bottom-fishing strategy — not greedy, makes 1% and runs each time"**

### Who's It For?
- ✅ People who like intraday trading
- ✅ People who like counter-trend bottom-fishing
- ✅ Risk-averse players (limited profit per trade, limited losses)
- ✅ People with low-end computers (minimal computation)

### Who's It NOT For?
- ❌ People who like chasing and cutting
- ❌ People who want to get rich in one shot
- ❌ People who like long-term holding
- ❌ People who don't have time to monitor the screen

### My Recommendations
1. **This is a beginner-level strategy**: Simple and understandable, great for newcomers learning quantitative trading logic
2. **Specialized for ranging markets**: Choosing the right market environment matters more than adjusting parameters
3. **Don't be greedy**: Strategy is already set to make 1% and run — don't try to make 10%
4. **Set stop-loss properly**: 5% stop-loss is a must — don't go naked

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Making Money from "Cheapness"

ClucMay72018's money-making philosophy is simple:

> **"When price drops too much it will bounce back — I buy at the absolute bottom and sell when it bounces!"**

- **Feature 1**: Only buys at oversold levels, never chases
- **Feature 2**: Sells when returning to normal, not greedy
- **Feature 3**: Volume must be low — prevents buying false rebounds

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Rating | Plain English Explanation |
|:-----------|:------:|:------------------------|
| Slow Bull | ⭐⭐☆☆☆ | Price always above the moving average, buy conditions can't trigger — anxiously watching |
| Ranging Market | ⭐⭐⭐⭐⭐ | Perfect! Price bouncing up and down, mean reversion logic eating and drinking happily |
| Downtrend | ⭐⭐⭐☆☆ | Buy conditions easily trigger but may buy "halfway down the mountain" — need to run fast |
| Extreme Volatility | ⭐⭐☆☆☆ | Volume sell-offs trigger protection — can't buy; post-surge pullback may have some opportunities |

**One-Line Summary**:
> **"Ranging markets are my home turf — other markets, I'll take my chances!"**

---

## 10. Want to Run This Strategy? Check These Settings First

### 10.1 Trading Pair Configuration

| Configuration Item | Suggested Value | Comment |
|-------------------|-----------------|---------|
| Trading Instruments | Mainstream coins (BTC, ETH) | Smaller coins have poor liquidity — may not get sufficient fills |
| Timeframe | 5 Minutes | Don't change! This is how the strategy was designed |
| Minimum ROI | 0.01 (1%) | Enough — don't raise it |
| Stop-Loss | -0.05 (5%) | Must set properly! |

### 10.2 Key Config File Settings

```yaml
# Strategy Configuration
minimal_roi:
  "0": 0.01

stoploss: -0.05

timeframe: 5m

# Trading Pair Selection
exchange:
  name: binance
  pair_whitelist:
    - BTC/USDT
    - ETH/USDT
```

### 10.3 Hardware Requirements (Important!)

This strategy **uses barely any computation** — minimal hardware requirements:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------------|-------------|-----------------|------------|
| 10-20 pairs | 512MB | 1GB | Smooth |
| 50-100 pairs | 1GB | 2GB | Smooth |
| 200+ pairs | 2GB | 4GB | May lag |

**Any VPS can run this!** Even a Raspberry Pi would be fine 😅

### 10.4 Backtest vs. Live Trading

**Notes**:

1. **Slippage**: Live buy prices are often higher than backtest prices — suggest setting 0.001 slippage
2. **Liquidity**: Smaller coins may not get sufficient fills
3. **Market Depth**: Extreme markets may cause market orders to fill at terrible prices

**Recommended Process**:
1. Run paper trading for one week first
2. Observe if strategy performance matches expectations
3. Test with small capital live
4. Increase position after confirming no issues

---

## 11. Bonus: Strategy Author's "Little Tricks"

### Bonus #1: Only Used 1 Buy Condition

> Other strategies have 5, 10 buy conditions — this one uses just 1! Lazy or confident? I think it's **simplicity is the ultimate sophistication**.

### Bonus #2: Calculated a Bunch of Useless Indicators

```python
# These indicators were all calculated but never used in buy/sell
dataframe['rsi'] = ta.RSI(...)
dataframe['macd'] = ta.MACD(...)
dataframe['adx'] = ta.ADX(...)
```

> Author inner monologue: "I calculated them all just in case they're useful later?" 😂

### Bonus #3: EMA100 Uses 50 Days

```python
dataframe['ema100'] = ta.EMA(dataframe, timeperiod=50)
```

> Wait, the variable is named `ema100` but the parameter is 50? What's with this clever naming? Maybe they wanted 100 5-minute candles ≈ ~8 hours of EMA? Whatever — it works.

---

## 12. The Bottom Line

### One-Line Verdict
> **"Simple and brutal counter-trend bottom-fishing strategy, suitable for ranging market profit enthusiasts"**

### Who's It For?
- ✅ Intraday traders
- ✅ Risk-averse players
- ✅ Quantitative trading beginners (for learning)
- ✅ People with low-end computers

### Who's It NOT For?
- ❌ People seeking overnight riches
- ❌ People who like chasing and cutting
- ❌ People who don't have time to monitor
- ❌ People who like long-term coin accumulation

### Manual Trading Recommendations

If you want to manually trade this strategy, remember these simplified rules:

1. **Open a 5-minute chart**
2. **Set EMA100 and Bollinger Bands** (20, 2)
3. **Observe buying when all three conditions are met**:
   - Price below EMA100
   - Price below Bollinger lower band
   - Volume hasn't suddenly exploded
4. **Sell when price breaks above Bollinger middle band**
5. **Set 5% stop-loss**

**Core Principle**: Don't be greedy, take profits when available! 🏃‍♂️

---

## ⚠️ Final Warning (Must Read!)

### Backtesting Looks Great — Be Careful in Live Trading

ClucMay72018's backtest performance looks **pretty good** — especially in ranging markets, mean reversion strategies often make steady profits. But there's a problem:

> **Past performance does not predict future results!** Market style changes, previously effective strategies may become ineffective.

### Hidden Risks of Counter-Trend Strategies

This strategy is **counter-trend bottom-fishing** — sounds cool but has a fatal flaw:

- **Buying more as it drops may catch "halfway down the mountain"**: You think it's done falling, but it may have just started.
- **Sustained losses when trends hit**: In consecutive downtrends, the strategy will buy and stop out repeatedly.
- **Exits too early and misses big rallies**: Sells as soon as price breaks the middle band — the big rally that follows is none of your business.

### My Recommendations (Sincere Advice)

```
1. Paper trade first — don't jump in with real money
2. Use in ranging markets, stop when trends hit
3. Must set stop-loss! 5% is the floor
4. Don't be greedy — strategy says make 1% and run, don't try to make 10%
5. Watch the market environment — 100× more important than adjusting parameters
```

**Remember**:
> **"Strategies are static, markets are dynamic. Survival is what matters!"** 🏥

---

**Final Reminder**: This strategy is suited for **ranging markets**. If your market is a unilateral move (like a bull run surge or a bear market crash), stand by for now. Paper trade with light positions, survival is the top priority! 🙏

---

*Strategy Author: Gert Wohlgemuth*
*Applicable Environment: Ranging markets, sideways consolidation*
*Risk Level: Medium-Low*
