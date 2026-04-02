# CustomStoplossWithPSAR Strategy: Plain English Edition

## Chapter 1: What Does This Strategy Do?

Hey folks! Today we're talking about a strategy called CustomStoplossWithPSAR. The name looks intimidating, but it's actually pretty simple when you break it down:

**CustomStoploss** = Custom Stoploss  
**PSAR** = Parabolic SAR (Parabolic Stop and Reverse)

Put together: a strategy that uses the PSAR indicator for dynamic stoploss.

You might ask: Isn't setting a stoploss at 5% or 10% good enough? Why build an entire strategy around it?

Great question! Traditional fixed stoploss has a big problem: set it too tight and normal price swings kick you out for no reason; set it too loose and you lose too much when it actually drops. This strategy solves this — the stoploss follows the price, rises when the price rises, keeping your profits safer.

## Chapter 2: What the Heck is PSAR?

To understand this strategy, you first need to know what PSAR is.

PSAR stands for Parabolic Stop and Reverse. It was invented by technical analysis legend J. Welles Wilder in 1978 — same guy who invented the RSI indicator. Old school!

### What Does PSAR Look Like?

Open your trading chart and add PSAR, and you'll see a bunch of little dots:

- **In an uptrend**: Dots appear below the candles, following price upward
- **In a downtrend**: Dots appear above the candles, following price downward

These dots form a curve that looks like a parabola — hence "parabolic."

### How Do You Use PSAR?

Simple:
- Dots are below = you're in a long position, and that dot is your stop level
- Price drops below that dot = stop out or reverse to short

The coolest thing about PSAR is that **it auto-adjusts**. When a trend just starts, the stop distance is far, giving price plenty of "breathing room." As the trend continues, the stop gets tighter and tighter, locking in more profits for you.

## Chapter 3: Core Philosophy of This Strategy

The core philosophy is one sentence: **Let PSAR decide your stoploss position.**

Traditional stoploss:
- Entry at $100
- Set stop at 10%
- Stop price = $90
- Whether price climbs to $150 or drops to $95, stop stays at $90

PSAR stoploss:
- Entry at $100, PSAR dot at $95
- Price climbs to $120, PSAR dot might move up to $110
- Price climbs to $150, PSAR dot might move up to $135
- Stop level follows price up, locking in profits!

This is called "moving stoploss" or "trailing stoploss" — let profits run while having protection.

## Chapter 4: Code Structure Overview

Alright, enough concepts. Let's look at the code. Don't worry — it's only about 80+ lines, and the core logic is even less.

```python
class CustomStoplossWithPSAR(IStrategy):
    timeframe = '1h'          # Use 1-hour candles
    stoploss = -0.2           # Floor stop at 20%
    custom_info = {}          # Storage for data
    use_custom_stoploss = True  # Enable custom stoploss
```

Just those few settings — simple, right?

The strategy has four main methods:
1. `populate_indicators` — Calculate PSAR indicator
2. `populate_entry_trend` — Decide when to buy
3. `populate_exit_trend` — Decide when to sell (disabled here)
4. `custom_stoploss` — The core stoploss logic

Let's go through them one by one.

## Chapter 5: Calculating the PSAR Indicator

The first method is `populate_indicators`. Its job is to calculate technical indicators.

```python
def populate_indicators(self, dataframe, metadata):
    dataframe['sar'] = ta.SAR(dataframe)
```

Just one line! Call TA-Lib's SAR function and store the result in the 'sar' column.

Then there's a backtest-only code snippet:

```python
if self.dp.runmode.value in ('backtest', 'hyperopt'):
    self.custom_info[metadata['pair']] = dataframe[['date', 'sar']].copy().set_index('date')
```

This stores PSAR data during backtesting because you can't fetch real-time data in backtest mode. In live trading, you don't need to pre-store anything — you can query in real-time.

## Chapter 6: Buy Signal

The buy logic is super simple — so simple that the strategy author himself calls it "nonsensical" and a placeholder:

```python
def populate_entry_trend(self, dataframe, metadata):
    dataframe.loc[
        (dataframe['sar'] < dataframe['sar'].shift()),
        'buy'] = 1
    return dataframe
```

Translated to plain English: **Buy when today's PSAR value is lower than yesterday's.**

This logic might not be super reliable in actual trading, so the author explicitly says this is a placeholder and you should replace it with your own buy strategy. This strategy's focus is stoploss, not buying.

## Chapter 7: Sell Signal

```python
def populate_exit_trend(self, dataframe, metadata):
    dataframe.loc[:, 'sell'] = 0
    return dataframe
```

This sets the 'sell' column to 0 for all rows, meaning: **Never sell via signal.**

Why? Because this strategy exits entirely through stoploss. Either you get stopped out, or you close manually — no selling based on signals. This keeps the stoploss logic pure.

## Chapter 8: Stoploss Logic — The Soul of the Strategy

Here's the main event! This method is the core of the entire strategy:

```python
def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    result = 1  # Default — 1 means no custom stoploss
    
    if self.custom_info and pair in self.custom_info and trade:
        relative_sl = None
        
        if self.dp:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
            last_candle = dataframe.iloc[-1].squeeze()
            relative_sl = last_candle['sar']
        
        if relative_sl is not None:
            new_stoploss = (current_rate - relative_sl) / current_rate
            result = new_stoploss - 1
    
    return result
```

Let me explain line by line:

**Step 1:** Set default `result = 1`. This is Freqtrade's convention — returning 1 means no stoploss is set.

**Step 2:** Check if data is available. Is this pair in `custom_info`? Is the `trade` object valid?

**Step 3:** Get the latest data via DataProvider, grab the last row, extract the PSAR value.

**Step 4:** Calculate the stoploss ratio.

Example:
- Current price = $100
- PSAR value = $95
- Stoploss distance = $100 - $95 = $5
- Stoploss ratio = $5 / $100 = 5%
- Return value = 5% - 1 = -0.95

Here, returning -0.95 tells Freqtrade: "Set the stop at 5% below the current price."

## Chapter 9: The Freqtrade Stoploss Return Value Gotcha

This is the most confusing part for beginners. Let me dedicate a whole chapter to it.

Freqtrade's `custom_stoploss()` return value has a specific meaning:

- **Return -0.05**: Stop is set 5% below current price
- **Return -0.1**: Stop is set 10% below current price
- **Return 0**: Disable custom stoploss, use default
- **Return 1**: Also disable stoploss (literally never stop out)

So our calculation:
```python
new_stoploss = (current_rate - relative_sl) / current_rate
result = new_stoploss - 1
```

If current_rate = 100, sar = 95:
- new_stoploss = 0.05
- result = -0.95

This -0.95 tells Freqtrade: "Trigger stoploss when price drops 5%."

Wait, you might ask: Why not just return -0.05 directly? This has to do with Freqtrade's internal calculation. The return value represents the "loss threshold ratio" — return -0.05 means "trigger stoploss when loss reaches 5%."

## Chapter 10: What's the Difference Between Backtest and Live?

This strategy behaves slightly differently in backtest vs. live, mainly in how it accesses data.

**Backtest Mode:**
1. All candle data loaded at once
2. `populate_indicators` called once, computes all historical data
3. Strategy stores PSAR data in `custom_info` dictionary
4. Stoploss calculation queries the corresponding SAR value from the dictionary

**Live Mode:**
1. Candle data updates in real-time
2. On each `custom_stoploss` call, fetches the latest PSAR value in real-time
3. No pre-storage of data needed

The code handling this difference:
```python
if self.dp.runmode.value in ('backtest', 'hyperopt'):
    self.custom_info[metadata['pair']] = dataframe[['date', 'sar']].copy().set_index('date')
```

Data is only stored during backtesting and hyperopt modes.

## Chapter 11: Strategy Pros and Cons

### Pros

**1. Follows Trends, Protects Profits**
PSAR stoploss tightens as trends continue, locking in profits. Very effective in trending markets.

**2. Clean Code, Easy to Understand**
The whole strategy is just ~80 lines with even fewer core lines. Perfect for learning Freqtrade's custom stoploss mechanism.

**3. Highly Extensible**
Stoploss logic and entry logic are separated — you can easily apply PSAR stoploss to any strategy.

### Cons

**1. Entry Logic is Too Simple**
"Buy when SAR drops" is too crude — produces many false signals in actual trading.

**2. Gets Whipsawed in Ranging Markets**
PSAR frequently crosses price in sideways markets, causing repeated stoploss triggers and accumulating significant trading costs.

**3. Parameters May Need Adjustment**
Default PSAR parameters (AF 0.02–0.20) may not suit all coins and timeframes — optimization may be needed.

## Chapter 12: How to Improve This Strategy

Since the entry logic is just a placeholder, let's think about improvements.

### Improve Buy Signal

```python
def populate_entry_trend(self, dataframe, metadata):
    dataframe['uptrend'] = dataframe['close'] > dataframe['sar']
    dataframe['sar_cross_under'] = (
        (dataframe['close'] > dataframe['sar']) & 
        (dataframe['close'].shift() < dataframe['sar'].shift())
    )
    dataframe.loc[(dataframe['sar_cross_under']), 'buy'] = 1
    return dataframe
```

Now instead of "buy whenever SAR drops," it's "buy only when price just crossed above SAR" — much more aligned with proper PSAR usage.

### Add Trend Filter

```python
dataframe['ema_200'] = ta.EMA(dataframe, timeperiod=200)
dataframe.loc[
    (dataframe['sar_cross_under']) & 
    (dataframe['close'] > dataframe['ema_200']),
    'buy'] = 1
```

Only go long when price is above the long-term moving average.

### Add Take-Profit Logic

Since there's a stoploss, you could add take-profit too:

```python
def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
    if current_profit > 0.20:
        return 'profit_target'
    return None
```

## Chapter 13: Practical Usage Recommendations

### 1. Use It as a Template, Not a Complete Strategy

The author says so himself — this strategy is for reference. Focus on learning how `custom_stoploss` is written, and write your own entry signals separately.

### 2. Backtest Before Going Live

Any strategy needs backtest verification first. Freqtrade's backtesting is powerful — test all your parameters and time ranges and see how the profit/loss ratio looks.

### 3. Test with Small Money First

Passed backtesting? Test with small money in live trading. Paper trading and live trading are different — live has slippage, emotions, and all sorts of surprises.

### 4. Watch the Market Environment

PSAR stoploss works well in trending markets, poorly in ranging markets. If the market keeps chopping sideways, consider pausing the strategy or switching to another approach.

### 5. Keep a Trading Journal

Record every stoploss trigger and track whether you got stopped out legitimately or unnecessarily. Over time, you'll learn whether the strategy fits the current market.

## Final Thoughts

CustomStoplossWithPSAR, though simple in code, demonstrates a crucial concept: **dynamic stoploss.**

In traditional trading, you set a fixed stoploss and forget about it — which is a shame in trending markets when you watch profits evaporate. Dynamic stoploss is like a "smart bodyguard" that moves with your profits, protecting capital while letting winners run.

Of course, no strategy is perfect. PSAR gets whipsawed in ranging markets too, but that's the cost of doing business. The key is finding what fits your risk tolerance.

Hope this plain English version helped you understand the strategy. If you have questions, read the code a few more times, tweak the parameters yourself, and test with backtest data — you'll get the hang of it.

---

**Final Reminder**: The entry logic in this strategy is a placeholder. Please replace it with your own signals!
