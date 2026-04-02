# Ichimoku_v37: Strategy Explained — The "Chase-the-Trend" Bot

## Table of Contents

1. [What Does This Strategy Do?](#1-what-does-this-strategy-do)
2. [Why Is It Called Ichimoku?](#2-why-is-it-called-ichimoku)
3. [What Is the Cloud Anyway?](#3-what-is-the-cloud-anyway)
4. [What the Heck Is Heiken Ashi?](#4-what-the-heck-is-heiken-ashi)
5. [How Does the Strategy Work?](#5-how-does-the-strategy-work)
6. [When to Buy?](#6-when-to-buy)
7. [When to Sell?](#7-when-to-sell)
8. [What If It Goes Wrong?](#8-what-if-it-goes-wrong)
9. [When to Take Profits?](#9-when-to-take-profits)
10. [Why Use Two Timeframes?](#10-why-use-two-timeframes)
11. [What's Great About This Strategy?](#11-whats-great-about-this-strategy)
12. [What Are the Pitfalls?](#12-what-are-the-pitfalls)
13. [How Can Beginners Get Started?](#13-how-can-beginners-get-started)

---

## 1. What Does This Strategy Do?

Simply put, **Ichimoku_v37 is a "chase-the-trend" strategy**.

The core idea is straightforward: when the price breaks through something called the "cloud" upward, you buy; when the price falls back below the cloud, you sell and run.

It's like chasing a bus—when you see the bus moving, you jump on; when it's about to reach its final stop, you get off.

This strategy works best in **trending markets**. What does trending mean? When the price goes steadily up or down without turning back. For sideways choppy markets, this strategy doesn't work so well.

---

## 2. Why Is It Called Ichimoku?

**Ichimoku** is the English transliteration of the Japanese term for "Ichimoku Kinko Hyo."

This technical indicator was invented by a Japanese person named Goichi Hosoda, whose pen name was "Ichimoku Sanjin." It took him seven years of research to develop this system.

"Ichi" means "one glance," and "Kinko Hyo" means "equilibrium chart." Put together: **a chart you can understand with just one look**.

Japanese naming is quite vivid. This indicator can plot trend direction, support/resistance, and buy/sell timing all on one chart—no need to look at a messy pile of lines.

The "v37" is the version number. This strategy has been through many revisions, and version 37 is the latest iteration.

---

## 3. What Is the Cloud Anyway?

**The Cloud is the most important part of the Ichimoku system**—imagine a cloud floating above the candlestick chart.

This cloud has upper and lower boundary lines:
- **Upper boundary**: called "Leading Span A," we'll call it the "cloud top"
- **Lower boundary**: called "Leading Span B," we'll call it the "cloud bottom"

The cloud also has colors:
- **Green cloud**: Cloud top is above cloud bottom — bullish market
- **Red cloud**: Cloud bottom is above cloud top — bearish market

Imagine you're climbing a mountain:
- The cloud floats above your head — you're going uphill (green cloud)
- The cloud floats below your feet — you're going downhill (red cloud)

This strategy uses the cloud to judge the big picture: **look for buy opportunities when the cloud is green, be careful when it's red**.

The magic of the cloud is that it **adjusts automatically**. Unlike those fixed horizontal support/resistance lines drawn on charts, the cloud moves with price changes—kind of like a real cloud drifting with the wind.

---

## 4. What the Heck Is Heiken Ashi?

**Heiken Ashi is a special type of candlestick chart**, with the Japanese name meaning "average candle."

You've definitely seen regular candlesticks—those red and green candles, sometimes with long upper and lower wicks, looking messy and chaotic.

What Heiken Ashi does is **smooth these candles**:
- Takes an average of open, close, high, and low prices
- Recalculates new candlestick data

After this processing:
- Trends become much clearer
- Upper and lower wicks are reduced
- False breakouts decrease

Think of it this way: regular candlesticks are like a person walking—two steps forward, one step back, often veering sideways. Heiken Ashi is like smoothing out that walking path, so you can clearly see which direction they're actually going.

This strategy uses Heiken Ashi to determine **when price crosses the cloud**, rather than using regular prices. This avoids many false signals—the kind where it looks like a breakout but actually isn't.

---

## 5. How Does the Strategy Work?

This strategy's design can be summarized in four words: **"Read the sky, work the ground"**.

- **Read the sky**: Use the daily chart cloud to determine the major trend
- **Work the ground**: Use the 4-hour chart price to find buy and sell points

The specific process:

1. **Check the daily cloud first**: Is today's cloud green or red?
2. **Then look at 4-hour price**: Where is the price relative to the cloud?
3. **Price breaks through the cloud**: That's the buy signal
4. **Price falls back below the cloud**: That's the sell signal

The wisdom of this process: **use the large cycle to determine direction, use the small cycle to find entry timing**. Like hunting—you first confirm which direction the prey is (daily), then aim and fire (4-hour).

---

## 6. When to Buy?

There are two buy signal scenarios:

### Scenario 1: Green Cloud Breakout (Chase the Rise)

Buy when these conditions are met:
1. **Daily cloud is green** (major trend is up)
2. **4-hour price surges from below the cloud**
3. **It breaks through the cloud top** (Leading Span A)

In simple terms: **Major trend is up, price breaks through the cloud layer—chase it!**

Like mountain climbing—you know the mountain is going up (green cloud), you see someone has climbed to the summit (broke through the cloud top), so you follow along.

### Scenario 2: Red Cloud Breakout (Catch the Bottom)

Buy when these conditions are met:
1. **Daily cloud is red** (prior downtrend)
2. **4-hour price surges from below the cloud**
3. **It breaks through the cloud bottom** (Leading Span B)

In simple terms: **The major trend is falling, but price suddenly reverses upward—bottom fishing time!**

Like seeing a car going downhill suddenly start going uphill (breaks through red cloud)—things might be turning around, quickly get on board!

### Signal Comparison

| Signal Type | Cloud Color | Breakout Position | Meaning |
|------------|------------|-------------------|---------|
| Green cloud breakout | Green | Breaks cloud top A | Trend continuation, chase and add |
| Red cloud breakout | Red | Breaks cloud bottom B | Trend reversal, bottom fishing |

---

## 7. When to Sell?

The sell signal is super simple, just one sentence: **When price falls below the cloud, run!**

Specifically:
- **Falls below cloud top (Leading Span A)**: Sell!
- **Or falls below cloud bottom (Leading Span B)**: Also sell!

Look, buying requires checking cloud color and whether it's breaking the upper or lower boundary—pretty complicated. But selling doesn't care about any of that: **as soon as the price drops below the cloud, run**.

This design makes sense:
- **Be cautious when buying**: Multiple confirmations ensure reliable signals
- **Be decisive when selling**: One condition triggers exit, rather than risk being trapped

Like taking an elevator—boarding requires checking if the elevator is going up (confirming trend), but exiting only requires "we've arrived"—just get off!

### One Special Setting

The strategy has a setting called `sell_profit_only = True`, meaning:
- **Only respond to sell signals when making money**
- **When at a loss, even if price falls below the cloud, don't sell**

This prevents panic selling during a loss. BUT watch out! Stop loss is still effective—if the loss reaches 10%, forced stop-loss exits.

---

## 8. What If It Goes Wrong?

The strategy has a **hard stop loss: 10% loss triggers forced exit**.

```python
stoploss = -0.10
```

What does this mean? If you buy $100 worth of a coin and it drops to $90, the system automatically sells—no fantasies allowed.

How was the 10% stop loss determined? It's an empirical value:
- Too tight (e.g., 5%): Easily stopped out by normal fluctuations
- Too loose (e.g., 20%): Need huge gains to recover from one loss

10% is the sweet spot—it protects you from losing too much without getting washed out by normal market noise.

**Stop loss is your lifesaver**. Cryptocurrency can drop 30% in a single day. Without a stop loss, you're gambling with your life.

---

## 9. When to Take Profits?

This strategy has a clever **tiered take-profit design**:

```python
minimal_roi = {
    "0": 0.10,    # Immediately after buying: take profit at 10%
    "30": 0.05,   # After 30 minutes: take profit at 5%
    "60": 0.02    # After 60 minutes: take profit at 2%
}
```

What does this mean?

- **Right after buying**: If the price surges, take profit at 10% and lock in gains
- **Holding for a while without much rise**: Only need 5% to sell—don't get greedy
- **Still grinding along after a long hold**: Take profit at 2%—stop waiting

The wisdom of this design: **Give the trend time, but don't wait forever**.

Like fishing:
- Fish bites immediately after you cast (price surges 10%)—reel it in fast
- After waiting a while, fish finally bites (slow rise to 5%)—reel it in
- Only a nibble after half a day (rises to 2%)—anything is better than nothing

### One Important Exception

The strategy has a setting: `ignore_roi_if_buy_signal = True`

This means: **if the buy signal is still active (trend is still going), don't rush to take profit**.

For example, you've already made 10% profit. By rights you should sell. But if the cloud is still green and price is still above the cloud (buy signal valid), keep holding and let the profits run.

This is the famous "let profits run"—as long as the trend continues, don't jump off the train.

---

## 10. Why Use Two Timeframes?

This strategy uses **two timeframes**:
- **4-hour (primary timeframe)**: Used to determine buy/sell points
- **Daily (informative timeframe)**: Used to determine the major trend

Why so complicated?

### A Real-Life Analogy

Imagine driving to a city:

- **Daily chart** is like your **GPS navigation**: It tells you the general direction, "head north"
- **4-hour chart** is like **real-time traffic**: It tells you there's a red light ahead, now you can turn left

If you only look at the GPS (daily), the direction may be right but you might miss the best route.
If you only look at traffic (4-hour), you might discover halfway through that you're going the wrong direction.

So **look at both**:
- Use daily to confirm the big direction is correct
- Use 4-hour to find the precise entry point

### Technical Reasons

- **Daily cloud is more stable**: Updates only once a day, won't flip back and forth
- **4-hour signals are more timely**: Responds faster, won't miss opportunities

Using only daily would be too few signals; using only 4-hour would have too many false signals. **Together they're just right**.

---

## 11. What's Great About This Strategy?

### Advantage 1: Accurate Trend Identification

The cloud is really good at identifying trends. Green cloud means up, red cloud means down—at a glance, no guessing.

### Advantage 2: Fewer False Signals

Using Heiken Ashi to smooth prices plus daily filtering—double insurance. Those deceptive "breakouts that weren't really breakouts" are mostly filtered out.

### Advantage 3: Dynamic Adjustment

The cloud is alive and moves with price. Unlike rigid support/resistance lines drawn on charts that never change, the market changes and the cloud changes with it.

### Advantage 4: Solid Risk Control

Stop loss, take profit, signal exit—全套 (full set). Won't let you lose your shirt, won't let your hard-earned profits evaporate.

### Advantage 5: Great for Automated Trading

Logic is simple and clear—all rules the code can understand. Perfect for robot trading. No subjective "feeling like it's going up" or "might drop" nonsense.

---

## 12. What Are the Pitfalls?

### Pitfall 1: Gets Slapped Around in Ranging Markets

If the price wobbles around inside the cloud, this strategy will: buy → get slapped → sell → price goes up again → buy → get slapped again...

In this kind of market, the best move is to **not trade**. The problem is, how do you know it's a ranging market? That requires additional judgment.

### Pitfall 2: Slow to React

The cloud is fundamentally a lagging indicator—it needs historical data to calculate. By the time the cloud says "okay to buy," the price may have already risen quite a bit.

In fast-moving markets, this strategy may not keep up with the pace.

### Pitfall 3: Parameters May Not Suit All Coins

This strategy's parameters (20, 60, 120, 30) have been adjusted, but may not work for all cryptocurrencies. Bitcoin might do fine with these settings, but Dogecoin probably won't.

### Pitfall 4: Ignores Fundamentals

This strategy completely ignores news and fundamentals. If a big piece of news breaks, the strategy may not react in time. Whether Elon Musk tweets or a country announces policy—the strategy can't perceive any of it.

### Pitfall 5: Uses Only Technical Indicators

Only cloud and Heiken Ashi—no volume, no RSI, no MACD. Sometimes adding some auxiliary indicators would be better.

---

## 13. How Can Beginners Get Started?

### Step 1: Backtest! Backtest! Backtest!

Don't start with real money! First backtest with historical data to see how the strategy performed in past markets.

Freqtrade has great backtesting functionality—run it to find out:
- Does the strategy make money?
- What's the maximum drawdown?
- What's the win rate like?
- In what markets does it perform well?

### Step 2: Paper Trading

If backtesting looks good, run paper trading for a few days. Paper trading uses virtual money but real market data, so you can see how the strategy performs in real-time markets.

### Step 3: Small-Account Live Trading

Once paper trading is going smoothly, use a small amount of real money. Remember:
- **Only use money you can afford to lose**
- **Start with small positions**
- **Don't go all-in right away**

### Step 4: Monitor and Adjust

A strategy isn't something you set and forget. Regularly check:
- How far does actual performance deviate from backtesting expectations?
- Is the current market suitable for this strategy?
- Do parameters need adjusting?

### Step 5: Use in Combination

Don't put all your eggs in one basket. This strategy is just one tool in your toolbox:
- Can be combined with other strategies
- Can switch strategies based on different market states
- Can use it as an auxiliary judgment tool, with final decisions being your own

---

## Summary

Ichimoku_v37 is like a **cloud-watching, trend-chasing robot**:
- Use the daily cloud chart to judge the major trend
- Use the 4-hour price to find timing
- Buy above the cloud, sell below it
- Stop loss at 10% loss, take profit at 10% gain

It's suitable for:
- Trending markets with clear direction
- People who want automated trading
- Investors who can tolerate some drawdown

It's not suitable for:
- Wildly oscillating ranging markets
- People who want to get rich overnight
- People who want to set it and completely forget about it

Remember: **There is no perfect strategy, only suitable strategies**. Some people use this well, some don't. The key is knowing how to use it.

---

*This is the colloquial version. If you found it helpful, check out the formal version for more technical details and code explanations. Trade at your own risk!*
