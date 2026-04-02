# NotAnotherSMAOffSetStrategy_V2: Strategy Explained

## 1. What Does This Strategy Do?

Imagine you're at a supermarket — smart shoppers know prices go up and down. Today expensive, tomorrow cheap. How do you buy at the cheapest time?

This strategy is a trading bot that teaches you to **"buy low, sell high."** It doesn't chase rising prices or fear falling prices. Instead, it specifically watches for "discount" opportunities — when prices drop to a certain level, it auto-buys; when prices bounce back, it sells for profit.

The strategy name "NotAnotherSMAOffSetStrategy_V2" translates to "not just another simple MA offset strategy." Why? Because there are too many MA strategies out there, and this one is innovative — not the old "price crosses MA up to buy, crosses down to sell" routine.

---

## 2. Core Logic: Buy When Cheap, Sell When Expensive

### Simply Put:

This strategy is like a smart shopper whose principles are:

**When buying**:
- Price must be a certain percentage below "fair price" (e.g., 2.5% cheaper)
- Can't just look at price; must also check "momentum" (RSI indicator) for oversold conditions
- Volume can't be too abnormal
- Several indicators must all say "buy"

**When selling**:
- Price has bounced back near or above the MA
- Momentum starts improving
- Got profit? Run!

---

## 3. Technical Indicators Explained in Plain English

### 3.1 Moving Average — Your "Fair Price" Reference Line

A moving average is simply the average price over a recent period, serving as the coin's "fair price level."

This strategy uses **offset MAs** — moving the MA down a bit. Like: normal MA at $100, but the strategy sets buy line at 97.5% of MA ($97.5). Only buys when price falls below $97.5, getting a better price!

The strategy has two buy offset values:
- **0.975** (normal buy): Buy when price drops to 97.5% of MA
- **0.95** (aggressive buy): Buy when price drops to 95% of MA, fishing for deeper bottoms

### 3.2 RSI — "Buying/Selling Pressure" Indicator

RSI is like aspring scale (spring scale), telling you if the market has "too much energy" or "not enough."

- **RSI > 70**: Market too excited, too many buyers, may pull back
- **RSI < 30**: Market too pessimistic, too many sellers, may rebound

The strategy uses three RSIs:
- **Main RSI (14-period)**: See the big picture
- **Fast RSI (4-period)**: Quick reaction, used to find entry timing
- **Slow RSI (20-period)**: Slow reaction, used to judge trend

### 3.3 EWO — "Wave Emotion" Indicator

EWO (Elliott Wave Oscillator) judges market "emotion."

- **Positive and large**: Market rising, optimistic sentiment
- **Negative and small**: Market falling, pessimistic sentiment

The strategy uses it to judge: Is the market overall rising or falling? Only in an UPTREND's pullback are opportunities good!

### 3.4 Volume — "Market Heat" Indicator

Volume is like supermarket foot traffic:
- High (active): Market is active, price changes are meaningful
- Low (quiet): Market is dull, may be just minor fluctuations

The strategy has a special volume indicator "vol_base" that converts volume into a -100 to 0 value:
- **Above -20**: Very active volume
- **-77 to -96**: Moderate-low volume (strategy's favorite)
- **Too low**: Don't trade

### 3.5 HMA — "Fast Trend Line"

Hull Moving Average (HMA) is a special MA known for fast reaction and low noise. Strategy uses 50-period HMA to judge whether to sell.

---

## 4. Buy Signal Details

The strategy has four buy signals, each with its own trigger conditions:

### 4.1 EWO1 Signal — Main Signal

Most commonly used buy signal, conditions:

```
✓ Volume moderate (not too hot, not too cold)
✓ Fast RSI below 35 (short-term oversold)
✓ Price below MA offset position (e.g., 97.5%)
✓ EWO shows market overall still rising (just a temporary pullback)
✓ Main RSI not at overbought (hasn't exceeded 69)
✓ Volume > 0 (exclude abnormal data)
✓ Price not yet at sell line
```

**Plain English**: Market was rising, suddenly dropped hard, people scared, but overall trend isn't broken. This is a "bargain hunting" opportunity!

### 4.2 EWO2 Signal — Aggressive Bottom-Fishing

More aggressive than EWO1, requires deeper price drop:

```
✓ Volume moderate
✓ Fast RSI below 35
✓ Price below 95.5% of MA (deeper than EWO1)
✓ EWO > -2.327
✓ Main RSI must be below 25 (VERY oversold)
✓ Other basic conditions
```

**Plain English**: Market panicked, price dropped terribly, RSI below 25. Buyers at this point are either brave or smart — extreme panic often brings big rebounds!

### 4.3 EWO3 Signal — Active Volume Version

Targets high-volume scenarios:

```
✓ Volume very active (vol_base > -20)
✓ Fast RSI below 35
✓ Price below MA offset
✓ EWO shows upward momentum
✓ Other basic conditions
```

**Plain English**: Market is bustling, everyone trading, price suddenly drops. This dip may just be short-term fluctuation, buyers will come soon to bottom-fish — we buy too!

### 4.4 EWOLow Signal — Extreme Oversold Bottom-Fishing

Targets "crash-style drops":

```
✓ Volume moderate
✓ Fast RSI below 35
✓ EWO very low (below -20.988)
✓ Price below MA offset
```

**Plain English**: Market crashed, everyone selling, EWO fell below -20. But as they say, "Be greedy when others are fearful." Extreme oversold often brings revenge rebounds. Obviously, this signal carries the most risk.

---

## 5. Sell Signal Details

The strategy's sell logic is relatively simple — two scenarios:

### 5.1 Condition A: Rebound Complete, Take Profit

```
✓ Price above 9-day MA
✓ Price at sell channel upper edge
✓ RSI restored above 50 (momentum normal)
✓ Fast RSI above slow RSI (short-term momentum strengthening)
✓ Volume present
```

**Plain English**: Price rebounded, momentum restored, time to take profit and run.

### 5.2 Condition B: Trend May Reverse, Get Out

```
✓ Price broke below 50-day HMA (trend may weaken)
✓ But price still above sell channel
✓ Fast RSI above slow RSI
✓ Volume present
```

**Plain English**: Though still at relatively high price, trend may be turning bad. With some profit left, run!

### 5.3 Sell Confirmation — Don't Sell Too Early

There's a smart mechanism: even if sell signal triggers, one more check:

```
If: Short-term MA still above long-term MA (trend still intact)
And: RSI not overheated
Then: Don't sell! Continue holding, let profits run more
```

**Plain English**: Sell signal came, but trend still healthy. Don't rush to sell; waiting may bring more gains.

---

## 6. Risk Control Mechanisms

### 6.1 Hard Stop-Loss: Max 35% Loss

```python
stoploss = -0.35
```

If judgment is wrong and price keeps falling, auto-sell after 35% loss. This stop-loss is relatively wide because mean reversion strategies need to tolerate some price fluctuation.

### 6.2 Trailing Stop — Profit Protection Tool

```
✓ After profit exceeds 2.5%, activate trailing stop
✓ Stop line follows highest price, maintaining 0.5% distance
✓ Price retraces over 0.5%, sell
```

**Example**:
- Bought at $100
- Rose to $102.50, profit 2.5%, trailing stop activates
- Rose to $110, stop line follows to $109.45 ($110 × 99.5%)
- Dropped to $109.45, triggers stop, you made 9.45%

The trailing stop's power — it "locks in" profits without "capping" them.

### 6.3 ROI Targets — Time is Money Too

The strategy sets tiered targets:

| Time | Target Return |
|------|-------------|
| Just bought | 21.5% (big goal) |
| After 40 min | 3.2% (lowered target) |
| After 87 min | 1.6% (lowered again) |
| After 201 min | 0% (accept any positive) |

**Plain English**: Bought in, expect a big rebound. Waited a while without big rise, lower expectations. Waited over 3 hours, sell if not losing — after all, time costs money too.

---

## 7. Parameter Details

### 7.1 Buy Parameters

| Parameter | Default | Adjustable Range | Purpose |
|---------|---------|-----------------|---------|
| base_nb_candles_buy | 14 | 5-80 | Buy MA period; smaller = faster reaction |
| low_offset | 0.975 | 0.9-0.99 | Buy discount; smaller = buy cheaper |
| low_offset_2 | 0.955 | 0.9-0.99 | Aggressive buy discount |
| ewo_high | 2.327 | 2.0-12.0 | EWO high threshold |
| ewo_low | -20.988 | -20.0 to -8.0 | EWO low threshold |
| rsi_buy | 69 | 30-70 | RSI buy threshold |

### 7.2 Sell Parameters

| Parameter | Default | Adjustable Range | Purpose |
|---------|---------|-----------------|---------|
| base_nb_candles_sell | 24 | 5-80 | Sell MA period |
| high_offset | 0.998 | 0.95-1.1 | Sell offset; larger = sell later |
| high_offset_2 | 1.0 | 0.99-1.5 | Aggressive sell offset |

---

## 8. Strategy Pros & Cons

### 8.1 Pros

**1. Precise entry**: Not buying the moment price drops; must drop below MA percentage before buying — gets better prices!

**2. Multi-verification**: Multiple "inspections" before buying: price position, momentum, volume, trend direction — all required. Fewer false signals.

**3. Smart exits**: Not selling at every rise; when trend is good, let profits run; when trend weakens, run.

**4. Trailing stop protects profits**: Whatever price rises, stop follows up — protects profits without limiting upside.

**5. Highly adjustable**: Lots of parameters to optimize — be aggressive or conservative, your choice!

### 8.2 Cons

**1. Long only**: Can only buy, can't short. In bear markets, just watch.

**2. Wide stop-loss**: 35% loss is painful when triggered.

**3. Too many parameters**: More parameters is good when tuned right, but a money-loser when tuned wrong.

**4. Needs ranging markets**: Doesn't perform well in strong trends (continuously rising or falling); prefers oscillating markets.

**5. Time cost**: Uses 5-minute candles, trading frequency may be high, fees add up.

---

## 9. How to Use This Strategy Well?

### 9.1 Market Selection

**Good markets**:
- Prices go up and down, oscillating
- Moderate volume, not too hot not too cold
- Not extreme one-sidedmarkets

**Bad markets**:
- Sustained falling bear market
- Low-liquidity small coins
- Extreme volatility (during major news)

### 9.2 Trading Pair Selection

**Good choices**:
- Major coins: BTC, ETH, etc.
- High volume
- Price fluctuations with patterns

**Bad choices**:
- Newly listed coins
- Coins with very low daily volume
- Coins with erratic price jumps

### 9.3 Risk Control Advice

1. **Don't go all-in**: Each trade no more than 5-10% of total capital
2. **Diversify across coins**: Run several trading pairs simultaneously, don't put all eggs in one basket
3. **Regular checks**: Review strategy performance when it's not doing well, consider parameter adjustments
4. **Stop-loss discipline**: Once stop is set, don't manually cancel
5. **Keep sufficient margin**: Don't get liquidated due to insufficient margin

---

## 10. FAQ

### Q1: Why is the stop-loss set so wide at 35%?

A: Mean reversion strategies need to tolerate some price fluctuation. Price might drop 20% first then bounce back; if you set 10% stop-loss, you'd get stopped out at the bottom. That said, 35% is wide for many people — adjust based on your risk tolerance.

### Q2: Which of the four buy signals should I use?

A: No need to choose manually — the strategy auto-judges which to use. EWO1 is the main signal, most frequent; EWO2 and EWOLow are bottom-fishing signals, higher risk but potentially higher returns; EWO3 targets active markets.

### Q3: How many trades per day?

A: Depends on market volatility. Heavily oscillating markets may see several trades per day; calm markets might go days without a signal.

### Q4: Do I need to watch it constantly?

A: No — that's the robot's advantage. Set parameters and let it run on its own; check results regularly.

---

## 11. Summary

NotAnotherSMAOffSetStrategy_V2 is a well-designed mean reversion strategy. It's not simply looking at one indicator to trade; it makes decisions by synthesizing multiple dimensions:

1. **Is the price cheap enough?** (MA offset)
2. **Is market sentiment right?** (RSI oversold)
3. **Is the overall trend good?** (EWO indicator)
4. **Is volume reasonable?** (Volume baseline)
5. **Is the sell timing right?** (Secondary confirmation mechanism)

Key to using this strategy well:
- Choose suitable markets and trading pairs
- Tune parameters and backtest thoroughly
- Execute risk control strictly

Remember, **no perfect strategy exists, only suitable strategies**. This strategy suits ranging markets, not extreme one-sidedmarkets. Understanding the strategy's principles and limitations is how you make money with it.

Final advice: **Trading has risk, invest cautiously**. No matter how good the strategy, trade within your means.

---

*Hope this plain-English version helps you understand this strategy. Feel free to discuss!*