# InformativeSample Strategy Explained — Peek at What "Big Brother" Bitcoin Is Doing

## Chapter 1: What Does This Strategy Do?

Have you ever thought: when trading, could you also check what "Big Brother" is doing?

In the crypto world, Bitcoin is that "Big Brother." It goes up, other coins follow; it goes down, other coins fall too. So, when trading a certain coin, if you could also see what Bitcoin is doing, wouldn't that be more reliable?

InformativeSample does exactly this—it analyzes the coin you want to buy while watching Bitcoin's trend. Only when both check out does it let you buy or sell.

The strategy was written by xmatthias, a Freqtrade core developer, primarily to teach people how to use Freqtrade's "informative pairs" feature. Although the strategy itself isn't great at making money (the author admits this), by learning it you can master a very practical skill: cross-coin analysis.

---

## Chapter 2: What Are "Informative Pairs"?

The "informative pairs" concept might be a bit confusing. Let me use an analogy.

Suppose you're a stock investor holding Tencent shares. Every day you look at Tencent's candlestick chart, analyzing its movements. One day you suddenly think: what if I could also check the broader market (like the S&P 500 or CSI 300)?

Because when the broad market goes up, Tencent will probably go up too; when the market crashes, even a great company like Tencent can't escape unscathed.

That's the role of informative pairs—they let you reference another trading pair's data while analyzing one trading pair. In Freqtrade, you define it like this:

```python
def informative_pairs(self):
    return [("BTC/USDT", '15m')]
```

This tells the bot: "Keep an eye on BTC/USDT on the 15-minute timeframe—I need it as a reference."

The bot obediently downloads BTC's data, stores it, and waits for you to use it.

---

## Chapter 3: What Indicators Does This Strategy Use?

This strategy uses just two types of indicators:

### 3.1 Main Coin Indicators

Whichever coin you're trading, the strategy calculates three moving averages for it:

- **EMA 20**: 20-period exponential moving average, short-term trend
- **EMA 50**: 50-period exponential moving average, medium-term trend
- **EMA 100**: 100-period exponential moving average, long-term trend

The usage is simple: if EMA 20 is above EMA 50, the short-term trend is better than the medium-term—it's a buy signal; reverse is a sell signal.

### 3.2 Reference Coin Indicators

The strategy calculates one indicator for BTC/USDT:

- **SMA 20**: 20-period simple moving average

Just one! Simple, right? When BTC's price is above this line, Bitcoin's short-term trend is good; below means it's weakening.

---

## Chapter 4: When to Buy?

The buy conditions are just two, and BOTH must be met:

### Condition 1: EMA 20 Must Be Above EMA 50

This is a form of "golden cross." When the short-term moving average is above the long-term moving average, it means prices are rising and momentum is good.

Imagine you're driving uphill—if your speed (short-term) is faster than the average speed (medium-term), you're accelerating. Same with stocks: when EMA 20 is above EMA 50, it's accelerating upward.

### Condition 2: BTC Price Must Be Above Its SMA 20

This means: Bitcoin's current trend is good, sitting above its short-term moving average.

Why check this? Because Bitcoin is the "lead dog." When Big Brother is in a good mood, the little guys (other coins) dare to go up with confidence. If Big Brother himself is falling, how can you expect the little guys to go far?

When both conditions are met, the strategy says: "OK, you can buy!"

---

## Chapter 5: When to Sell?

The sell conditions are the exact opposite of the buy conditions, also two:

### Condition 1: EMA 20 Drops Below EMA 50

This means the short-term trend has deteriorated and prices are falling—be careful.

### Condition 2: BTC Price Falls Below Its SMA 20

This means Bitcoin is also struggling. If Big Brother starts falling, the little guys won't be far behind.

When both conditions are met, the strategy says: "Run! Time to sell!"

See how symmetrical this logic is: when buying, both need to be good; when selling, both need to be bad. Simple and clear—it won't trip itself up.

---

## Chapter 6: When to Take Profits? (ROI Settings)

This strategy has a set of staged take-profit rules:

| How Long Held | Take Profit At |
|--------------|---------------|
| Immediately after buying (0 minutes) | 5% |
| Held 20 minutes | 4% |
| Held 30 minutes | 3% |
| Held 60 minutes | 1% |

What does this mean? Simply: the longer you wait, the lower the requirement.

Right after buying, the strategy thinks: "I'm satisfied with 5% profit." If the price quickly hits 5%, great, sell immediately and lock in gains.

But if you've been holding for 60 minutes and haven't sold yet (maybe the price has been going up and down, never quite reaching 5%), the strategy thinks: "Alright, I'll take 1%, don't want to wait any longer—too much can go wrong overnight."

The rationale: the longer you hold, the greater the uncertainty, so better to exit earlier.

---

## Chapter 7: When to Cut Losses? (Stop Loss Settings)

The strategy has two lines of defense:

### 7.1 Fixed Stop Loss: -10%

If you buy and the price steadily falls, hitting a 10% loss, the strategy forces a sell. This is the absolute bottom line, preventing you from holding on and digging yourself deeper into a hole.

Some say 10% is too big? But in crypto, 10% fluctuation is just "normal daily movement." If set too tight, the price might sell and then rebound—you'd lose money AND miss the subsequent rise.

### 7.2 Trailing Stop: Protecting Profits

This is more interesting. The rules are:

- When your profit reaches 4%, the trailing stop activates
- From that point, if the price retraces more than 2% from its high, auto-sell triggers

Example:

You buy at $100. Price rises to $104 (4% profit), trailing stop activates. Stop line is set at $104 × 0.98 = $101.92.

Price continues rising to $120! Amazing! Stop line follows up to $120 × 0.98 = $117.60.

Suddenly the price starts falling, down, down, down... hits $117.60 and triggers a sell! You made 17.6% profit. Happy!

But if the price plunges through $117.60 from $120, you still managed to protect most of your gains. That's the benefit of trailing stop—it locks in profits while leaving room for the price to keep climbing.

---

## Chapter 8: Buy and Sell Timeframes

This strategy uses two timeframes:

- **Primary timeframe: 5 minutes** — Analyze the coin you're trading, decide to buy/sell
- **Reference timeframe: 15 minutes** — Look at BTC's trend as a reference

Why not use the same timeframe? There's a reason:

The 5-minute period is fast, capturing trading opportunities quickly. But BTC as a "reference object" doesn't need to be checked that frequently—15 minutes is often enough. Checking too often might introduce noise.

It's like driving: you need to watch the road conditions closely (5 minutes), but you don't need to check the weather forecast that often (15 minutes is fine—occasionally is enough).

---

## Chapter 9: How Is the Code Written?

### 9.1 Fetching BTC Data

```python
def informative_pairs(self):
    return [("BTC/USDT", '15m')]
```

This line tells Freqtrade: "I need BTC/USDT data on the 15-minute timeframe—please prepare it for me."

### 9.2 Calculating Indicators

```python
def populate_indicators(self, dataframe, metadata):
    # Calculate EMA for the main coin
    dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
    dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
    dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)
    
    # Calculate SMA for BTC
    informative = self.dp.get_pair_dataframe(pair="BTC/USDT", timeframe='15m')
    informative['sma20'] = informative['close'].rolling(20).mean()
    
    # Merge the two dataframes
    dataframe = merge_informative_pair(dataframe, informative, '5m', '15m', ffill=True)
    
    return dataframe
```

This code does three things:
1. Calculate EMA indicators for the coin you're trading
2. Calculate SMA indicator for BTC
3. Merge the two dataframes into one, so they can be used together

### 9.3 Buy Signal

```python
def populate_entry_trend(self, dataframe, metadata):
    dataframe.loc[
        (dataframe['ema20'] > dataframe['ema50']) &
        (dataframe['close_15m'] > dataframe['sma20_15m']),
        'buy'] = 1
    return dataframe
```

Meaning: when EMA 20 > EMA 50 (main coin trend is good) AND BTC price > BTC SMA 20 (Big Brother's trend is good), buy.

### 9.4 Sell Signal

```python
def populate_exit_trend(self, dataframe, metadata):
    dataframe.loc[
        (dataframe['ema20'] < dataframe['ema50']) &
        (dataframe['close_15m'] < dataframe['sma20_15m']),
        'sell'] = 1
    return dataframe
```

Opposite of buying: when EMA 20 < EMA 50 AND BTC price < BTC SMA 20, sell.

---

## Chapter 10: What Are the Benefits?

### 10.1 Simple and Easy to Understand

The code isn't long, the logic is clear, no complicated indicators. Even beginners can understand what's going on.

### 10.2 Checks the Big Picture

Not working in isolation—checks what "Big Brother" Bitcoin is doing. This is a great approach: considering external environment when making decisions, not just focusing on your own little corner.

### 10.3 Good Risk Control

Fixed stop loss + trailing stop + staged take profit. Three lines of defense protecting your principal and profits.

### 10.4 Teaches Real Skills

From this strategy, you can learn how to use the informative pairs feature. This is a very practical skill in Freqtrade that will come in handy when developing more complex strategies.

---

## Chapter 11: What Are the Drawbacks?

### 11.1 The Author Says It Doesn't Make Much Money

The code comments explicitly state "Not performing very well"—so don't expect to use it directly to make money. It's a teaching example.

### 11.2 Indicators Are Too Simple

Just a few moving averages, no commonly used indicators like volume, RSI, or MACD. May miss many signals or generate many false ones.

### 11.3 Only One BTC Reference

Only looks at Bitcoin, not ETH, overall market sentiment, etc. Sometimes Bitcoin falls but other coins rise—this strategy might miss those opportunities.

### 11.4 Gets Worn Out in Ranging Markets

Moving average strategies work well in trending markets but struggle in sideways markets (going up and down with no direction). In ranging conditions, you might buy and sell frequently, with trading fees eating up all the profits.

---

## Chapter 12: How to Improve This Strategy?

### 12.1 Add Other Indicators

For example, add RSI:

```python
dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
```

Then the buy condition can include: RSI can't be too high (e.g., below 70), to avoid chasing highs.

### 12.2 Check Volume

```python
dataframe['volume_sma'] = dataframe['volume'].rolling(20).mean()
```

If volume expands when buying, it means capital is flowing in—more reliable.

### 12.3 Reference Multiple Coins

```python
def informative_pairs(self):
    return [
        ("BTC/USDT", '15m'),
        ("ETH/USDT", '15m')
    ]
```

Watching both BTC and ETH gives more comprehensive information.

### 12.4 Use Hyperopt to Optimize Parameters

Use Freqtrade's Hyperopt feature to automatically find optimal parameters:
- What's the best EMA period?
- What's the best trailing stop setting?
- How should ROI be configured for maximum profit?

---

## Chapter 13: Summary

InformativeSample teaches us three things:

### First: Cross-Coin Analysis Is Very Useful

Don't just focus on the coin you're buying—sometimes checking what "Big Brother" Bitcoin is doing can be a lifesaver. When Bitcoin rises, altcoins dare to rise confidently; when Bitcoin falls, even great altcoins have to follow.

### Second: The Informative Pairs Feature Is Great

Freqtrade's `informative_pairs` and `merge_informative_pair` make cross-coin analysis simple. Once you've mastered this, you can develop more complex strategies.

### Third: Even Simple Strategies Need Complete Risk Control

Although the strategy logic is simple, it has fixed stop loss, trailing stop, and staged take profit—none of the risk control measures are skimped on. This tells us: strategies can be simple, but risk control cannot be omitted.

---

## Final Thoughts

If you're new to Freqtrade, my recommendations:

1. Read through this strategy's code completely and understand what every line does
2. Run backtesting yourself and see how it performs on different coins and time periods
3. Try modifying parameters and see how results change
4. Add some new indicators and see if you can improve returns

Once you've learned this strategy, you'll have mastered the "ultimate technique" of informative pairs—and that will help you develop strategies that can actually make money!

Remember: this strategy is for learning, not for making money. But the methods it teaches can help you develop strategies that truly make money. Good luck!

---

*This document is the colloquial version of InformativeSample Strategy.*
