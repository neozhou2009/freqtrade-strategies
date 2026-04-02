# NostalgiaForInfinityV5: The "More Ways to Catch a Dip" Strategy

## 1. What Is This Thing?

This is an automated crypto trading strategy for the Freqtrade platform, the 5th version of the NostalgiaForInfinity series. The core idea: **"Catch dips in uptrends, sell when it's risen too much."**

In other words, it watches the market, waits for price to pull back in a healthy uptrend, buys the dip, then sells when it's made enough profit.

---

## 2. How Does It Make Money?

### The Money-Making Logic

**Buy when**: Price has pulled back to a "reasonably low" spot in an overall uptrend.

**Sell when**: You've made enough profit, or the trend looks like it's changing.

### The Protection Layers (What It Won't Do)

This strategy's biggest strength isn't what it buys — it's what it **won't** buy:

**Won't catch a falling knife**: Checks multiple time windows (current candle, last 2, 12, and 144 candles) to ensure the drop isn't too severe before buying.

**Won't chase a pump**: Checks 24h/36h/48h windows — if a coin has surged too much, it waits for a pullback before buying.

**Needs trend confirmation**: Only buys when the long-term trend is clearly up.

---

## 3. What Tools Does It Use?

### Moving Averages (the backbone)

Different period MAs for different purposes:
- **Short-term**: EMA 12, 20, 26 — catch recent momentum
- **Medium-term**: EMA 50, 100 — judge the mid-term trend
- **Long-term**: EMA 200 — the big boss, the bull/bear divider

**Rule of thumb**: Price above EMA200 = potentially bullish; EMA50 above EMA200 = confirmed bullish.

### RSI (how tired is the price?)

A 0-100 number:
- **RSI < 30**: Price has been beaten up — might bounce
- **RSI > 70**: Price is exhausted — might pull back

The strategy uses **dual-timeframe RSI** (5-minute and 1-hour) for better confirmation.

### Bollinger Bands (the rubber band)

Three lines around price — upper band, middle band (MA), lower band:
- **Touch lower band**: Price may be oversold, potential buy
- **Touch upper band**: Price may be overbought, potential sell

The strategy uses **two BB configs**: BB20 (standard) and BB40 (longer, more stable).

### MFI (smart money flow)

Like RSI but considers volume too. If RSI is low but MFI isn't, it might be a false drop.

### EWO (Elliott Wave Oscillator)

Measures momentum: positive EWO = strong uptrend momentum; negative EWO = potential oversold bounce.

### Choppiness Index

Measures if the market is trending or ranging:
- **Low values (< 38.2)**: Strong trend — good for this strategy
- **High values (> 61.8)**: Ranging — strategy might underperform

---

## 4. The 21 Buy Conditions (What Kinds of Dips Does It Catch?)

The strategy has **21 different buy conditions**, but they're all variations of a few core themes:

### Type 1: Trend Pullback (Conditions 1, 8, 11, 14)

Big trend is up, price has pulled back, RSI shows oversold — buy.

**Example** (Condition 1):
- 1h EMA50 > EMA200 (uptrend confirmed)
- SMA200 rising
- Not too much of a drop (dip protection ✓)
- Not too much of a recent pump (pump protection ✓)
- RSI < 23.4 (deeply oversold)
- MFI < 21.7 (money flow also oversold)

### Type 2: Bollinger Band Dip (Conditions 2, 4, 9, 10, 12, 16, 17)

Price touched or broke below the Bollinger Band lower band — classic mean reversion entry.

**Example** (Condition 2):
- 1h SMA200 trending up
- Not a recent pump
- Volume < 2.6x average (low volume pullback)
- 5m RSI much lower than 1h RSI (oversold relative to timeframe)
- MFI < 49
- Price < BB lower band × 0.983

### Type 3: Extreme Oversold (Conditions 20, 21)

Both 5m and 1h RSI need to be very low. This is rare but reliable.

**Condition 20**: 5m RSI < 26, 1h RSI < 20
**Condition 21**: 5m RSI < 23, 1h RSI < 24

### Each condition can be toggled on/off independently!

---

## 5. The 8 Sell Conditions

All essentially mean: **"It's risen too much, time to take profits."**

### Basic Sell Conditions

1. **RSI > 79.5 + 6 consecutive candles above BB upper band** — way overbought, exit
2. **RSI > 81 + 3 consecutive candles above BB upper band** — still overbought
3. **RSI > 82** — simple and direct
4. **5m RSI > 73.4 AND 1h RSI > 79.6** — dual-timeframe confirmation
5. **Price below EMA200 + RSI above 1h RSI + 4.4** — below major MA but rallying, exit
6. **Price between EMA50-200 + RSI > 79** — mid-range rally
7. **1h RSI > 81.7 + EMA death cross** — trend reversal signal
8. **Price > 1h BB upper band × 1.1** — extreme overbought

---

## 6. The Smart Sell: Custom Profit Management

This is the best part — the strategy doesn't just set a take-profit point and forget it.

### Tiered Profit-Taking

The more you've made, the more lenient it gets about selling:

| Profit Made | RSI Must Be Below | Why |
|------------|------------------|-----|
| > 1% | 33 | You haven't made much, wait |
| > 3% | 38 | Got a little, still wait |
| > 5% | 43 | Getting decent, starting to take profits |
| > 8% | 48 | Made good money, take more profits |
| > 25% | 50 | Made great money, take it whenever RSI is high |

### Trailing Retracement

The strategy remembers your peak profit. If you've made a lot but it starts giving back:
- Made 15-46% and pulled back 18% from peak → sell
- Made 1-12% and pulled back 14% from peak → sell

This is how it "lets profits run while protecting them."

---

## 7. The Dual Timeframe Trick

### Why Two Timeframes?

The 1-hour chart is like your GPS — shows the overall direction.
The 5-minute chart is like your eyes — shows you when to act.

**The strategy's logic**:
1. Check 1-hour: Is the trend clearly up?
2. Check 5-minute: Has price pulled back enough to buy?
3. If both say yes → buy!

### The RSI Trick

If 5-minute RSI is low but 1-hour RSI is normal → good buy (short-term oversold, mid-term still fine).

If both are low → might be a bigger problem, proceed with caution.

---

## 8. Risk Control: Four Safety Nets

### Layer 1: Fixed Stoploss
-10%. If you're down 10%, the strategy cuts the trade. Last resort.

### Layer 2: Trailing Stoploss
- Activates at 3% profit
- Trails 1% behind the peak
- Lets winners run, cuts losers fast

### Layer 3: Smart Sell Signals
As described above — tiered profit-taking, trend reversal exits.

### Layer 4: Pre-Entry Protection
Dip protection + pump protection + trend confirmation = only enters reasonably.

---

## 9. Practical Setup

### Config Must-Haves
```json
{
  "timeframe": "5m",
  "use_sell_signal": true,
  "sell_profit_only": false,
  "ignore_roi_if_buy_signal": true
}
```

### Recommended Settings
- **Pairs**: 40-80 stablecoin pairs (USDT, BUSD)
- **Concurrent trades**: 4-6
- **Avoid**: Leveraged tokens (*BULL, *BEAR, *UP, *DOWN)
- **Use**: Unlimited stake mode for automatic capital allocation

---

## 10. Who Is This For?

### Good For
- ✅ People with some trading knowledge
- ✅ People willing to backtest and optimize
- ✅ People who can handle moderate drawdowns
- ✅ People who want a systematic approach

### Not For
- ❌ Complete beginners (too complex)
- ❌ People needing zero losses (all trading has risk)
- ❌ People who want set-and-forget (needs monitoring)
- ❌ People chasing jackpots (this is steady, not explosive)

---

## 11. Tips for Success

1. **Backtest first**: Use at least 6 months of data, including bull, bear, and ranging markets
2. **Start small**: Test with a fraction of planned capital
3. **Review regularly**: Markets change, parameters may need adjusting
4. **Don't over-optimize**: Parameters that are "perfect" on historical data may fail going forward
5. **Keep it running**: Give the strategy time to work — don't judge it after a week

---

## Summary

**NostalgiaForInfinityV5** is a comprehensive strategy with 21 buy conditions and a sophisticated profit management system. Its core philosophy — "buy dips in uptrends, sell when it's overbought" — is time-tested and sound.

The real value is in its protection mechanisms: it won't catch a falling knife, won't chase a pump, and has multiple layers of profit protection. This makes it a solid choice for traders who want systematic exposure to crypto with built-in risk management.

But it requires patience, testing, and ongoing attention. It's a tool, not a money printer.

**Risk warning**: Past backtest results do not guarantee future performance. Trade responsibly.

---

*Document Version: V1.0 Colloquial*
*Strategy Version: NostalgiaForInfinityV5*
