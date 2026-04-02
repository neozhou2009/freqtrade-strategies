# DCBBBounce Strategy: Plain English Edition

## Chapter 1: What Does This Strategy Do?

Have you ever wondered if you could buy when a stock or cryptocurrency drops to a "floor price" and sell it after it bounces for profit? DCBBBounce does exactly this.

Its name sounds intimidating but it's actually simple when you break it down:
- DC = Donchian Channel (a way to see price highs and lows)
- BB = Bollinger Bands (another tool to see price volatility)
- Bounce = Price bouncing

Put together: using Donchian Channel and Bollinger Bands to find price bounce opportunities.

In short, this is a "bottom-fishing" strategy. Instead of chasing rising prices, it waits until price has fallen enough and starts bouncing, then buys. This approach is called "counter-trend trading" — the opposite of "chasing momentum."

---

## Chapter 2: What Are These Two Core Tools?

### Bollinger Bands — A "Breathing" Rubber Band

Imagine you have a rubber band. Price swings around in the middle of this band. When price bounces to the top of the rubber band, it's moved up too much. When it bounces to the bottom, it's dropped too much.

Bollinger Bands are this rubber band:
- **Middle line**: Average price line
- **Upper line**: Average plus two "volatility ranges"
- **Lower line**: Average minus two "volatility ranges"

The cool part: this rubber band "breathes" — it expands when price is volatile and contracts when things are calm. This strategy uses 20 periods (or 20 candles) for calculation.

### Donchian Channel — The Scoreboard for Highs and Lows

Imagine you're doing jump training and there's a scoreboard tracking your highest and lowest jumps over the past month. The Donchian Channel does exactly this:
- **Upper band**: Highest price over a period (e.g., 52 candles)
- **Lower band**: Lowest price over the same period

So the Donchian Channel tells you: in this period, price has moved between this high and this low.

### Putting the Two Tools Together

The essence of this strategy: look at Bollinger Bands AND Donchian Channel simultaneously!

When the Bollinger Band lower band (bottom of the rubber band) falls below the Donchian Channel lower band (historical low), price has really dropped — a potential bounce is coming. This is your bottom-fishing opportunity.

Conversely, when the Bollinger Band upper band rises above the Donchian Channel upper band (historical high), price has climbed too high — a pullback is likely. That's your sell signal.

---

## Chapter 3: How Does It Decide When to Buy?

Buying isn't as simple as "see a low and buy." You need to wait for the right moment. This strategy's buy conditions are as follows:

### Condition 1: Confirm Data is Valid

First, make sure Donchian Channel data is valid, not empty. Simple — no data, no judgment.

### Condition 2: Check the SAR Parabolic (Optional)

What is SAR? Think of it as a "shadow" that follows price:
- When price rises, the shadow supports it from below
- When price falls, the shadow presses down on it from above

The strategy says: if close price is below SAR, price is falling toward support — consider buying.

This condition is enabled by default but can be turned off.

### Condition 3: Check the Long-Term Trend Line (Optional)

The strategy also looks at SMA200, the average price of the last 200 candles. This represents the long-term trend.

If current price is above this line, the long-term trend is upward, so buying is safer — you're going with the flow.

This condition is disabled by default but can be enabled.

### Condition 4: Check the Medium-Term Trend Line (Optional)

There's also EMA50, a 50-period exponential moving average that weights recent prices more heavily.

Same idea: if price is above this line, the medium-term trend looks good.

This condition is also disabled by default.

### Condition 5: Check Trend Strength (ADX)

ADX measures trend strength on a 0-100 scale:
- Below 25: No clear trend, market is ranging
- 25-50: Some trend, moderate strength
- 50-75: Strong trend
- Above 75: Extremely strong trend

The strategy requires ADX > 25 (default) plus DM+ (positive momentum) >= DM- (negative momentum). Translation: trend must be strong enough AND going upward.

This is enabled by default.

### Condition 6: The Most Important — The Bottom-Fishing Signal!

This is the core condition:

1. Current candle must be bullish (close > open, meaning it went up)
2. Bollinger Band lower band crosses above Donchian Channel lower band

What does this mean? Price dropped so much it fell below both the Bollinger lower band AND the Donchian lower band. Now it's starting to bounce — the Bollinger lower band has moved back above the Donchian lower band. This is the "golden cross" of bottom-fishing — the signal to buy!

All these conditions must be met simultaneously. So as you can see, this strategy is cautious — it doesn't just bottom-fish randomly.

---

## Chapter 4: How Does It Decide When to Sell?

There are two ways to sell:主动卖 or let the machine handle it.

### Method 1: Let the Machine Handle It (Hold Mode)

If sell_hold = True (default), the strategy won't actively send sell signals. It relies on a few mechanisms to auto-sell:

**ROI Targets — Sell When Time Is Up**

Think of it as setting an alarm clock — time's up, you sell regardless of price movement. But this "alarm clock" is a bit smarter:

Set a 27.8% target immediately upon entry. If not sold after 39 minutes, target drops to 8.7%. Wait another 124 minutes, target drops to 3.8%. After 135 minutes, no more targets — just hold on.

Interesting design: right after entry you're ambitious, dreaming big. But time passes, ambition fades — small profit is fine too.

**Stoploss — Run When Losing Too Much**

Stoploss is set at -33.3%. If you lose more than 33.3%, the machine auto-sells. This stoploss is quite wide, giving price plenty of room to move.

**Trailing Stop — Move the Stoploss Up When Profitable**

This feature is particularly useful! Say you bought at $100 and price climbed to $120. The strategy moves the stoploss upward. For example, after a 17.2% profit, trailing stop activates, and if price retraces more than 21.2% from its peak, it sells.

This is "let profits run while locking in risk."

### Method 2: Proactively Find Sell Points (Active Sell Mode)

If sell_hold = False, the strategy actively sends sell signals.

Sell condition: Bollinger Band upper band crosses below Donchian Channel upper band.

Translation: price climbed so high it broke through both the Bollinger upper band AND the Donchian upper band. Now it's starting to pull back — the Bollinger upper band has dropped below the Donchian upper band. This is the "death cross" — time to run!

Each method has pros and cons. Hold mode is worry-free, suited for laid-back traders. Active sell mode is more engaged, suited for traders who want to capture every exit point.

---

## Chapter 5: Timeframe and Order Methods

### Using 5-Minute Candles

The strategy uses 5-minute candles. What does that mean? Every 5 minutes a candle is generated, and the strategy makes judgments based on that candle's open, close, high, and low prices.

What is 5 minutes? Slower than sub-second high-frequency trading, faster than daily/weekly charts. Medium-to-short term.

Why 5 minutes? Probably because: (1) enough signals without waiting forever, (2) not too many to cause excessive trading, (3) slippage and fees are still manageable.

### Using Limit Orders for Trading

The strategy defaults to limit orders for buys and sells. A limit order is one where you specify a price — only executes when that price is reached. Good: price is controlled. Bad: might not execute.

### Using Market Orders for Stoploss

Stoploss uses market orders (execute immediately at whatever price). Stoploss is life-or-death — speed matters more than price.

And the stoploss is placed at the exchange (stoploss_on_exchange = True), so even if your computer loses internet, the stoploss still fires. Important!

---

## Chapter 6: What Parameters Can You Adjust?

This strategy offers many adjustable parameters — like buying a car with various optional features.

### buy_period (Donchian Channel Period)

Default: 52
Range: 10 to 120

This is the number of candles used to calculate the Donchian Channel. 52 five-minute candles is roughly 4.3 hours.

Shorter period (10-30): Narrower channel, more signals, but potentially less accurate.
Longer period (70-120): Wider channel, fewer signals, but more reliable.

### buy_adx (ADX Trend Strength Threshold)

Default: 25
Range: 1 to 99

ADX must exceed this value to be considered "trending." 25 is the industry standard.

Lower (15-20): More buy opportunities, but might buy into false trends.
Higher (30-40): Fewer buy opportunities, but trends are more confirmed.

### buy_sma_enabled (Whether to Check 200 MA)

Default: False (disabled)

If enabled, only buy when price is above the 200 MA. Ensures you're trading in a long-term uptrend.

### buy_ema_enabled (Whether to Check 50 EMA)

Default: False (disabled)

If enabled, only buy when price is above the 50 EMA. Ensures you're trading in a medium-term uptrend.

### buy_adx_enabled (Whether to Check ADX)

Default: True (enabled)

If disabled, trend strength isn't checked. Signals increase but quality may drop.

### buy_sar_enabled (Whether to Check SAR)

Default: True (enabled)

If disabled, SAR isn't checked. Signals increase but buying may be less precise.

### sell_hold (Whether to Use Hold Mode)

Default: True (hold mode enabled)

If disabled, switches to active sell mode and sends sell signals based on channel crossover.

---

## Chapter 7: How to Run This Strategy on Freqtrade?

### Step 1: Prepare Files

Place DCBBBounce.py in your Freqtrade strategies folder, typically at: user_data/strategies/

### Step 2: Modify Config

Add to your config.json:

```json
{
  "strategy": "DCBBBounce",
  "timeframe": "5m"
}
```

To change parameters, add buy_params:

```json
{
  "strategy": "DCBBBounce",
  "buy_params": {
    "buy_period": 40,
    "buy_adx": 30
  }
}
```

### Step 3: Backtest Before Live Trading

Must backtest before going live!

```bash
freqtrade backtesting -s DCBBBounce --timerange 20230101-20231231 --timeframe 5m
```

This tests strategy performance on 2023 data. Check total return, max drawdown, win rate, etc.

### Step 4: Paper Trade

Passed backtesting? Try paper trading (dry-run):

```bash
freqtrade trade -s DCBBBounce --dry-run
```

Observe for a period to see actual performance.

### Step 5: Small Fund Live Trading

Paper trading is solid? Go live with small funds. Key rules:
- Don't go all-in from the start
- Set position size limits
- Be ready to stop out at any time

---

## Chapter 8: What Are the Strategy's Strengths?

### Strength 1: Two Tools Cross-Validate Each Other

Bollinger Bands and Donchian Channels are completely different indicators:
- Bollinger Bands use statistical standard deviation
- Donchian Channels use price extremes

Using both together makes signals more reliable. Like getting two people to confirm the same story.

### Strength 2: Multiple Filters Reduce False Signals

Before buying, several checkpoints must pass:
- Is the trend strong enough? (ADX)
- Where is support? (SAR)
- Is the big picture aligned? (SMA/EMA)

Signals that pass this screening are high quality.

### Strength 3: Complete Risk Control

Fixed stoploss as a floor, trailing stop locks in profits, ROI table controls time. Three layers of protection — won't blow up your account all at once.

### Strength 4: Flexible and Adjustable

Many parameters and switches — adjust to your risk tolerance and market conditions. Unlike "black box" strategies, you have full control.

### Strength 5: Clean Code

The code is clean and straightforward. If you know Python, you can add features or modify conditions yourself.

---

## Chapter 9: What Are the Strategy's Weaknesses?

### Weakness 1: Counter-Trend Trading Has Inherent Risk

Bottom-fishing is tricky. Price may keep falling after you buy. You think it's hit bottom, but there's a basement. And another below that. The strategy uses multiple filters to reduce risk, but the fundamental risk of counter-trend trading remains.

### Weakness 2: Indicators Have Lag

All moving average and channel-based indicators have lag. Price has already moved, indicators are still catching up. This is an inherent limitation of technical analysis.

### Weakness 3: Wide Stoploss

33% stoploss is too wide for many traders. Losing 33% requires a 50% gain to break even. If you don't like such a wide stop, you need to modify it yourself.

### Weakness 4: Signals May Be Scarce

Because conditions are many, signals may be insufficient. Especially in ranging markets or low-volatility coins. You might need to run multiple pairs simultaneously to get enough trading opportunities.

### Weakness 5: Market Environment Dependent

Strategy performs well in some markets, poorly in others. You need to learn to judge whether the current market suits this strategy.

---

## Chapter 10: What Markets Suit It?

### Suitable Markets

**Moderate volatility**: Price goes up and down but doesn't skyrocket or crash. Bollinger Bands and Donchian Channels work properly.

**Clear trends**: ADX can measure trend strength. The clearer the trend, the higher the bounce success rate.

**Liquid major coins**: BTC, ETH and other major coins have relatively predictable price behavior, technical analysis is more effective.

### Unsuitable Markets

**Skyrocketing/crashing markets**: Price soars or plummets, channel indicators break down. You think you're bottom-fishing, but there's an eighteenth floor below.

**Dead calm markets**: Price moves sideways with minimal volatility. Few signals, trading costs may exceed profits.

**New or manipulated coins**: Newly listed or hype-driven coins have no predictable price behavior. Technical analysis is basically useless.

---

## Chapter 11: Bottom Line

DCBBBounce is a strategy that finds bottom-fishing opportunities using Bollinger Bands and Donchian Channels.

**Core philosophy**: When price falls too deep (Bollinger lower band below Donchian lower band) and starts bouncing, that's your buy signal. When price climbs too high (Bollinger upper band above Donchian upper band) and starts falling, that's your sell signal.

**Safety measures**:
- ADX confirms trend strength
- SAR confirms support levels
- SMA/EMA confirm the big picture
- Bullish candle confirms bounce start
- Multiple filters reduce false signals

**Risk management**:
- 33% fixed stoploss as a floor
- Trailing stop locks in profits
- ROI table controls time
- Limit orders control price, market orders ensure execution

**Who it's for**:
- People who understand some technical analysis
- People who don't like chasing momentum, prefer bottom-fishing
- Patient people who can wait for signals
- People who can tolerate some volatility

**Who it's NOT for**:
- People who know nothing about technical analysis
- People looking to get rich quick
- People who can't handle losses
- People without time to learn and research

A strategy is just a tool — profitability depends on the person using it. Even the best strategy loses money in the wrong hands. Even a mediocre strategy makes money in the right hands. The key is understanding a strategy's logic, knowing when it works and when it doesn't.

Final reminder: Quantitative trading has risks, invest carefully. Test with small funds first, don't go all-in from the start. Learn, test, small-fund live trading, then scale up — this is the right approach.
