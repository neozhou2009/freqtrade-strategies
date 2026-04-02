# NostalgiaForInfinityNext_ChangeToTower_V6: Your Swiss Army Knife of Crypto Trading

## 1. What Is This Thing?

In plain terms, this is a program that automatically buys and sells cryptocurrencies, specifically hunting for profit opportunities within 5-minute price movements.

The name sounds fancy, but it's actually a customized version of something called "NostalgiaForInfinity." The original author is an overseas quantitative trading team, and this strategy is pretty well-known in the circle — lots of people use it for automated crypto trading.

**The core idea is dead simple**: Buy at the right time, sell at the right time, and don't blow up your account in the process.

---

## 2. How Does This Strategy Make Money?

### The Money-Making Principle

The strategy watches a whole bunch of indicators — like a seasoned trader staring at a dozen screens. It only places an order when most of these indicators say "looks good to buy." Same thing for selling — it needs multiple indicators to confirm before exiting.

Think of it like this:
- You want to buy some apples, but first you check if they're fresh, if the price is reasonable, if there's a sale today, if the store next door is cheaper...
- This strategy works the same way: it checks whether the trend is right, whether the price is low, whether the market is stable, whether there are risks...

### When Should You Use It?

- Good for buying coins with USDT (stablecoin quote, less affected by BTC swings)
- Uses 5-minute candlestick charts
- Manages 4-6 coins simultaneously
- Monitors 40-80 trading pairs total

**Whatever you do, stay away from leveraged tokens like BULL, BEAR, UP, and DOWN** — their volatility is off the charts, and this strategy can't handle them.

---

## 3. What Indicators Does the Strategy Watch?

### 3.1 Moving Average Indicators

A moving average takes prices from a period of time and averages them into a line.

**EMA (Exponential Moving Average)**:
- Smaller numbers are more sensitive — EMA12 changes faster than EMA200
- The strategy uses over a dozen EMAs, from EMA12 all the way to EMA200
- Mainly used to judge trends: price above EMA = uptrend, price below EMA = downtrend

**SMA (Simple Moving Average)**:
- Smoother than EMA, changes more slowly
- Mainly looks at SMA200 to judge the big-picture trend

### 3.2 Oscillator Indicators

**RSI (Relative Strength Index)**:
- A number from 0 to 100
- Too high (like above 70) means too many buyers, price might drop
- Too low (like below 30) means too many sellers, price might bounce
- The strategy also checks RSI on the 1-hour chart — double confirmation!

**MFI (Money Flow Index)**:
- Tracks how much money is flowing in and out
- When it's low, money is flowing out — might be a dip-buying opportunity

**CTI (Trend Strength Indicator)**:
- A number from -1 to 1
- Very negative means price has dropped too far — a bounce might be coming

**Williams %R**:
- Another overbought/oversold indicator
- The strategy uses an extremely long period version to spot extreme price deviations

### 3.3 Bollinger Bands

Bollinger Bands have three lines: upper band, middle band, and lower band.

- Price touching the upper band: might have risen too much
- Price touching the lower band: might have dropped too much
- The strategy mainly looks for opportunities where price dips below the lower band

### 3.4 Some Advanced Indicators

**Ichimoku Cloud**:
- A Japanese system — very complex but very comprehensive
- Has clouds, lines, and all sorts of elements
- Mainly used to determine trend direction

**MODERI (Modified Elder Ray Index)**:
- Looks at trends combined with volume
- Uses three periods: 32, 64, and 96
- Only dares to buy when several of them confirm bullish

**SSL Channels**:
- Another trend-spotting tool
- Price breaking above the upper rail = bullish; breaking below = bearish

---

## 4. When Does It Buy?

The strategy has 40 different buy scenarios, each with its own conditions. Let me highlight a few typical ones:

### Every Buy Has to Pass "Security Check" First

No matter which buy signal it is, it has to pass a "security check" first — professionally called a "protection mechanism":

1. **Trend protection**: EMA has to be in a reasonable position — can't buy during a crash
2. **Price position protection**: Price can't be too far below the EMA
3. **MA slope protection**: SMA200 has to be rising, can't be in a downtrend
4. **Dip protection**: Can't buy during a freefall
5. **Pump protection**: Can't chase — if it's already surged, wait for a pullback before buying
6. **BTC environment check**: If Bitcoin is crashing, hold off on buying

### Typical Buy Signals

**Signal 1: Basic Dip-Buying**
- Big trend is still up (SMA200 is rising)
- Price has pulled back a bit
- RSI not high, MFI not high, CTI very negative
- Conclusion: Pullback in an uptrend — can buy

**Signal 2: RSI Divergence**
- Current RSI is much lower than 1h RSI
- Price has dropped near the Bollinger lower band
- Conclusion: Might be reversing — buy some

**Signal 8: Multi-Confirmation**
- 96-period MODERI says bullish
- CTI very negative
- Price near Bollinger lower band
- Close price above EMA200
- Conclusion: Trend is up, short-term oversold — buy

**Signal 27: Extreme Oversold**
- Williams %R at extreme lows
- 1h-period Williams %R also very low
- RSI sum not high, CTI very negative
- BTC is not in a downtrend
- Conclusion: Way too oversold — it's bounce time, buy

**Signal 39: Ichimoku Confirmation**
- All Ichimoku elements pointing to bullish
- But price has pulled back to the SSL channel lower rail
- Conclusion: Trend confirmed — buy the pullback

**Signal 40: Fast Reversal**
- ZLEMA golden cross
- Multiple indicators showing oversold
- TD Sequential conditions met
- Conclusion: Fast reversal signal — buy

---

## 5. When Does It Sell?

Selling is even more important than buying, because how well you sell directly determines how much you profit.

### 5.1 How to Sell When You're Winning?

The strategy sets different sell conditions based on how much you've made:

**Making 1%-2%**:
- RSI can't be too high (like below 34)
- This ensures you're not selling during a pump

**Making 3%-5%**:
- RSI can't be too high
- CMF (money flow) must be negative
- Money is flowing out — time to go

**Making 10%-20%**:
- RSI needs to be relatively low
- Confirms it's genuine profit protection, not getting trapped chasing

**Making 20%+**:
- RSI needs to be very low (price is already pulling back)
- Lock in the big profits

Note: If you're below EMA200 (bear market), conditions are stricter — you need even lower RSI to sell.

### 5.2 How to Sell Pumped-Up Coins?

If a coin has surged incredibly in 48 hours (like over 90%), it's a "pumped coin":

- Made 1%? Can sell (RSI below 34)
- Made 2%? Can sell (RSI below 40)
- And so on...

Pumped coins are high-risk, so take profits early.

### 5.3 What's a Trailing Stop?

This is a dynamic way to sell:

Say you bought at $100 and it climbed to $110 — you're up 10%.
The strategy will set a rule: if price pulls back more than 5% from its high, sell.

The benefit:
- If price keeps climbing, you keep holding
- If price starts dropping, you auto-sell to lock in profits

### 5.4 How to Stop Losses When You're Losing?

**ATR Stoploss**:
- ATR measures volatility
- Subtract a multiple of ATR from the highest price to get the stop level
- If price drops below this level, stop out

**Loss-Range Stoploss**:
- Down 8%-12%: use 5.4x ATR as stop
- Down 12%-16%: use 5.2x ATR as stop
- Down 16%-20%: use 5.0x ATR as stop
- Down more than 20%: use 2.0x ATR as stop

**Recovery Stoploss**:
- If you've taken a big loss (like 12%) and price bounces back
- Say it climbs to 6% profit — the strategy will auto-sell
- This prevents profits from evaporating again

### 5.5 Signal-Based Sells

Some sells are triggered purely by signals:

**Signal 1**: RSI above 79.5, 5 consecutive candles above Bollinger upper band → Sell (it's going crazy!)

**Signal 4**: Both RSI and 1h RSI are very high → Sell (double overbought confirmed!)

**Signal 7**: 1h RSI above 81.7, EMA12 crosses below EMA26 → Sell (trend reversal!)

---

## 6. How Does Risk Control Work?

### 6.1 Multi-Timeframe Confirmation

The strategy doesn't just look at the 5-minute chart — it also checks the 1-hour chart.

Why? Because 5-minute wiggles might just be noise; the 1-hour chart shows the big picture.

For example: A buy signal pops up on the 5-minute chart, but the 1-hour chart shows the big trend is actually down — the strategy won't buy.

### 6.2 BTC Market Filtering

Bitcoin is the boss of crypto — when it drops, most coins drop too.

So the strategy watches BTC's trajectory:
- If BTC is in a downtrend, many buy signals get suppressed
- It waits for BTC to stabilize before opening buys

### 6.3 The Hold Feature (Force-Hold)

If you really like a certain coin, you can force the strategy to hold it until it's profitable.

Create a file called `hold-trades.json`:
```json
{"trade_ids": [1, 3, 7], "profit_ratio": 0.005}
```

This means: Trades with IDs 1, 3, and 7 must be up at least 0.5% before they can be sold.

### 6.4 Other Protections

**Backtest Age Filtering**: Only trade coins that have been listed for a certain number of days — brand new coins have unreliable data.

**Outage Protection**: If data suddenly cuts out (like an API failure), the strategy pauses trading.

---

## 7. Key Strategy Parameters

### Stoploss Settings
- Fixed stoploss: -10% (lose no more than 10%)
- Trailing stop: Activates after 3% profit, pulls back 1% to sell

### ROI Settings (Profit Targets)
- Immediately: 10%
- After 30 minutes: 5%
- After 60 minutes: 2%

### Timeframes
- Primary period: 5 minutes
- Auxiliary period: 1 hour
- Warmup period: Needs 480 candles (~40 hours)

---

## 8. What Are Safe Dips and Safe Pumps?

### 8.1 Safe Dips (Safe Dips)

You can't buy just any dip — you have to look at how severe the dip is.

The strategy divides dips into 13 levels (10 to 130):

- Level 10: Strictest — only tolerates the tiniest drops
- Level 130: Most permissive — tolerates pretty big drops

Each level checks 4 time periods:
- How much the current candle dropped
- How much the last 2 candles dropped
- How much the last 12 candles dropped
- How much the last 144 candles dropped

For example, Level 50:
- Current candle: drop no more than 2%
- 2 candles: drop no more than 14%
- 12 candles: drop no more than 32%
- 144 candles: drop no more than 50%

All 4 conditions must be met before the dip is considered "safe."

### 8.2 Safe Pumps (Safe Pump)

Can't chase — if it's already pumped too much, wait for a pullback.

The strategy checks gains over 24h, 36h, and 48h windows.

For example: A 48h gain of 80% counts as a pump.
But if there's been enough pullback (like 20% from the high), the strategy might still allow buying.

---

## 9. What's Quick Trade Mode?

Buy signals 32 through 38 and #40 fall into "quick mode."

After these buy signals trigger, the strategy uses a dedicated set of exit rules:

- Made 2%-6% and RSI is very high → Sell immediately
- ATR threshold broken → Sell immediately
- PMAX indicator triggered → Sell immediately
- ZLEMA crossover → Sell immediately

Quick mode is all about: fast in, fast out, take small profits and move on — no attachment.

---

## 10. What's Ichimoku Trading Mode?

Buy signal #39 uses Ichimoku-specific logic.

Sell conditions:
- Holding over 1440 minutes (24 hours) and RSI above 75 → Sell
- Recovered from max loss by a certain amount → Sell
- Down more than 10% → Stoploss
- ZLEMA crossover confirmed → Sell

Ichimoku mode is more steady — good for trending markets.

---

## 11. How Do You Use This Strategy?

### Step 1: Install Freqtrade

Freqtrade is an open-source quantitative trading framework. Get it installed first.

### Step 2: Download the Strategy File

Put the strategy file in your Freqtrade strategies directory.

### Step 3: Configure config.json

Key configs:
```json
{
  "timeframe": "5m",
  "use_sell_signal": true,
  "sell_profit_only": false,
  "ignore_roi_if_buy_signal": true
}
```

### Step 4: Backtest

```bash
freqtrade backtesting --strategy NostalgiaForInfinityNext_ChangeToTower_V6
```

See how it performed historically.

### Step 5: Paper Trade

```bash
freqtrade trade --strategy NostalgiaForInfinityNext_ChangeToTower_V6 --dry-run
```

Test it with fake money, observe how it behaves.

### Step 6: Live Trading

Once you're confident, use real money.

---

## 12. Strategy Pros and Cons

### Pros

1. **Many signals**: 40 buy signals covering all kinds of situations — won't miss opportunities
2. **Many protections**: Layer upon layer of gatekeeping — won't buy carelessly
3. **Great exits**: Multiple sell mechanisms to protect profits
4. **Sees the big picture**: Factors in BTC's trajectory — won't fight the trend
5. **Customizable**: Each buy signal can be toggled on/off individually

### Cons

1. **Too complex**: Way too many parameters — beginners get lost easily
2. **Needs computing power**: Heavy calculations — need a good computer
3. **Needs data**: Requires lots of historical data to run
4. **Might go stale**: Markets change — the strategy might need updates

---

## 13. Final Summary

### Core Takeaways

1. This is an automated trading strategy that helps you decide when to buy and sell
2. Uses many technical indicators — only acts when multiple confirm
3. Prioritizes risk control — has stoploss, trailing stop, market filtering, and more
4. Best suited for traders with some experience

### Usage Tips

1. **Test with fake money first**: Don't jump in with real cash right away
2. **Understand it first**: Know what the strategy is doing before you run it
3. **Start small**: Test the waters before going big
4. **Review regularly**: Look at your trade history, learn from it
5. **Adjust to the market**: Markets change — parameters need to change too

### Remember

Even the best strategy isn't a money tree. The market has risks — invest carefully.

The strategy is just a tool. The final decision is always yours.

---

*Note: This document explains the strategy's core content in plain language. For more detailed technical explanations, please refer to the Strategy Analysis version.*

*Document Version: V1.0*
*Generated: March 26, 2026*
