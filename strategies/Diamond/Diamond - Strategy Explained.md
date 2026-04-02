# Diamond Strategy: Plain English Edition

## 1. What Does This Strategy Do?

Diamond is a particularly "wilful" quantitative trading strategy. Other strategies pile on technical indicators — MA, MACD, RSI, Bollinger Bands... Diamond does the opposite: uses no indicators at all, just the rawest price data for trading decisions. How wilful is that?

Think of cooking: others dump in all the seasonings — soy sauce, vinegar, cooking wine, thirteen spices,恨不得 dump the whole pantry in. Diamond? Just salt and fire, and somehow still makes good food. That's "simplicity is the ultimate sophistication"!

The author gave this strategy a beautiful name — "Diamond" — paying tribute to Afghan women who remain strong in hardship. Like diamonds buried in desert depths, shining even in the darkest places. The strategy's naming gives cold code some warmth.

Diamond's core philosophy: **Raw data is the purest market information.** All technical indicators are essentially reprocessing of raw price and volume data. Reprocess too much, you might lose something or introduce lag. So why not just use raw data and let the optimization algorithm find patterns?

---

## 2. Core Logic: Watch Who Crosses Whom

Simply: **"Watch which line crosses which, and that decides buy or sell."**

This is just like the classic "golden cross" (MA cross) strategy you know — when fast line crosses above slow line, buy; when it crosses below, sell.

But here's the twist: Diamond doesn't restrict you to using MAs. You can use:
- Open price and close price crossing
- High price and low price crossing
- High price and volume crossing (yes, price vs. volume!)
- Any combination of data you can think of...

This is Diamond's "magic" — it liberates the MA cross concept. Any two data columns can be compared by crossover. Which combination works best? Let the optimization algorithm try it!

---

## 3. What Data Can This Strategy Use?

Five basic data types — the most raw market information:

| Data | English | Plain Meaning |
|------|---------|--------------|
| Opening price | open | Price when candle starts |
| Highest price | high | Highest price during candle |
| Lowest price | low | Lowest price during candle |
| Closing price | close | Price when candle ends |
| Volume | volume | How much traded in this candle |

Think that's not enough? Add your own indicators:

```python
dataframe['ma_fast'] = ta.SMA(dataframe, timeperiod=9)
dataframe['ma_slow'] = ta.SMA(dataframe, timeperiod=18)
```

After adding, you can select `ma_fast` and `ma_slow` in the parameters. It's like a DIY toolkit!

---

## 4. Horizontal Push: Looking Backwards

`horizontal_push` is essentially a "looking backwards" function.

Example: `horizontal_push = 7` means you take the current candle's highest price and compare it with the highest price from 7 candles ago.

On a 5-minute chart, 7 periods = 35 minutes. So you're comparing now with 35 minutes ago to see if there's a breakout.

---

## 5. Vertical Push: Scaling

`vertical_push` is simply multiplying data by a coefficient.

Why do this? Sometimes direct comparison isn't reasonable — need to adjust the "threshold."

Example: selling condition is highest price crossing below lowest price × 1.184. If lowest price is $100, the sell trigger is $118.4. The highest price must rise above $118.4, then drop below that point, to sell.

This parameter makes the crossover "threshold" adjustable — making the strategy much more flexible.

---

## 6. What Does the Optimized Signal Mean?

**Buy**: When highest price (lagged 7 periods) crosses above volume × 0.942, buy.

**Sell**: When highest price (lagged 10 periods) crosses below lowest price × 1.184, sell.

You might ask: comparing highest price with volume? They have different units! But for the optimization algorithm, it doesn't care about units — it only cares: when these two data cross, is the probability of making money higher?

This cross-dimensional comparison sometimes discovers things human intuition can't. That's why machine learning outperforms humans in many areas — it finds patterns we can't find!

---

## 7. Stoploss: 27.1%

If you buy at $100 and price drops to $72.9, it auto-stops. This is quite wide — over a quarter!

Why so wide? Because this is a 5-minute chart strategy, capturing relatively medium-term trends, needing to give trends some "breathing room." If stoploss is too tight (like 5%), normal fluctuations get you stopped out, and the big rally that follows has nothing to do with you.

---

## 8. ROI: Tiered Take-Profit

| Time | Target | Meaning |
|------|--------|---------|
| Immediately | 24.2% | Want big gains from the start |
| After 65 min | 4.4% | If can't make big gains, lower expectations |
| After 255 min | 2% | Lower expectations again |
| After 850 min | 0% | If still not profitable, take whatever you can get |

This is "time decay" take-profit. You're confident when you first enter, thinking you'll make big money. But the longer you wait, the more you accept you might not — take what's available and run.

---

## 9. Trailing Stop: Protecting Profits

Example: You buy at $100, price climbs to $120 (20% profit) — trailing stop activates!
- Price climbs to $150 — stop moves to $140
- Price retraces to $140 — triggered, you sell, locking in 40% profit!

Without trailing stop, price climbing to $150 then dropping to $90, you'd make nothing or even lose.

---

## 10. Summary

**Diamond's philosophy**: Sometimes the simplest solution contains the deepest market insight.

**Strengths**: Simple, flexible, efficient, extensible, complete risk management
**Weaknesses**: Over-relies on optimization, logic not intuitive, risk of overfitting

**Final reminder**: Historical performance doesn't guarantee future returns. No strategy is perfect — understand its logic, know when it works and when it doesn't, manage your risk, and don't bet your life savings!
