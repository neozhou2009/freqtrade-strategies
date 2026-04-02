# NostalgiaForInfinityV1: Your 24/7 Crypto Trading Buddy

## Table of Contents

1. [What Is This Thing?](#1-what-is-this-thing)
2. [How Does It Make Money?](#2-how-does-it-make-money)
3. [When Does It Buy?](#3-when-does-it-buy)
4. [When Does It Sell?](#4-when-does-it-sell)
5. [How Is Stoploss Set?](#5-how-is-stoploss-set)
6. [How Is Take-Profit Set?](#6-how-is-take-profit-set)
7. [What Indicators Does It Use?](#7-what-indicators-does-it-use)
8. [How Does It Read Timeframes?](#8-how-does-it-read-timeframes)
9. [How Big Is the Risk?](#9-how-big-is-the-risk)
10. [What Do You Need to Prepare?](#10-what-do-you-need-to-prepare)
11. [How to Use It Safely?](#11-how-to-use-it-safely)
12. [Which Coins Should You NOT Use?](#12-which-coins-should-you-not-use)
13. [FAQ](#13-faq)

---

## 1. What Is This Thing?

### The Short Version

NostalgiaForInfinityV1 is an automated crypto trading strategy that runs on the Freqtrade quantitative trading platform.

### Its Core Approach

**Follow the trend: buy on dips, sell on rips.**

That's it!

It's not a "chase the rally, panic on the drop" strategy. Instead, it waits for price to pull back (meaning it rose too much and dropped a bit, or dropped too much and bounced) before making a move.

### Who Wrote It?

Someone named iterativ, contributed to the Freqtrade community.

### What's the Name Mean?

"Nostalgia For Infinity" translates to "Eternal Nostalgia." Maybe the author thinks that even though the crypto market changes super fast, some trading rules are timeless.

---

## 2. How Does It Make Money?

### The Core Logic

1. **Look at the big trend first**: Only trade coins that are in an uptrend
2. **Wait for a pullback**: Price has risen too much, now it's pulled back a bit — this is the time to buy
3. **Sell when it rises**: When price bounces back up to a certain level, sell for profit

### Think of It Like Shopping

- You know this item will appreciate in the long run (big trend is up)
- But right now the price is expensive, so you wait
- When the price pulls back to something cheaper, you buy
- After the price goes back up, you sell for the difference

### What It's NOT

- It's NOT a bottom-fishing strategy (doesn't bet on price bouncing back from the bottom)
- It's NOT a chase strategy (doesn't chase rallies)
- It's NOT high-frequency trading (5-minute level, not seconds)

---

## 3. When Does It Buy?

The strategy has **three buy conditions** — if any one is met, it buys. Let me explain each one:

### Buy Condition 1: Bollinger Band Lower Band Break

**Simple Version**: Price dips below the Bollinger Band lower band — might be a good opportunity.

**The Details**:
- Bollinger Bands draw a "normal price range" around the price
- The upper band is a resistance line, the lower band is a support line
- When price breaks below the lower band, it's dropped a bit "too much"
- If the big trend is still up, this "over-drop" will likely bounce back

**The strategy also checks**:
- The big trend must be up (EMA 50 above EMA 200)
- Price must be above the long-term MA (not actually crashing)
- Drop was fast but the lower shadow is short (a sharp drop, not slow bleeding)

### Buy Condition 2: Price Deviation

**Simple Version**: Price deviating too far from the Bollinger Band lower band — might mean reversion is coming.

**The Details**:
- Price is more than 0.8% away from the Bollinger Band lower band (dropped too fast)
- Volume is low (not panic selling)
- Big trend is up

This is like a rubber band that's been pulled too tight — it's gonna snap back.

### Buy Condition 3: RSI Oversold Divergence

**Simple Version**: Short-term is severely oversold, but long-term is still fine.

**The Details**:
- RSI is a 0-100 number; below 30 is oversold
- The strategy checks both 5-minute RSI and 1-hour RSI
- If the 5-minute RSI is more than 36 points below the 1-hour RSI
- It means short-term selling went overboard — might bounce

**Think of it like this**:
- Someone is running (long-term trend is up)
- Suddenly trips and falls (short-term RSI is very low)
- But didn't get seriously hurt, can get up and keep running
- This is when you buy — betting they'll get back up

---

## 4. When Does It Sell?

Same idea — three sell conditions, and if any one is met, it sells.

### Sell Condition 1: Three Green Candles in a Row

**Simple Version**: Price closed above the Bollinger upper band for 3 candles in a row — time to sell.

**The Details**:
- The upper band is a resistance level
- Price has closed above the upper band 3 times in a row
- It's risen too much, time for a rest
- Sell now to lock in profits

### Sell Condition 2: RSI Overbought

**Simple Version**: RSI exceeds 78, too expensive, sell!

**The Details**:
- RSI above 70 is considered overbought
- Above 78 means it's risen way too much
- Lots of people are buying — might be the last round of buying frenzy
- Time to sell, don't be greedy

### Sell Condition 3: Trend Broke

**Simple Version**: Price fell below the long-term MA, might drop further — get out now.

**The Details**:
- EMA 200 is the long-term trend line
- Price fell below EMA 200, trend might be reversing
- But RSI is still above 50 (not panic yet)
- Sell now before it drops further

---

## 5. How Is Stoploss Set?

### Fixed Stoploss: 36%

**You read that right — 36%!**

Here's why:

1. **Mainly a psychological defense line**: Prevents extreme moves from blowing up the account
2. **Rarely actually triggers**: Because of trailing stoploss, usually won't reach this point
3. **Gives the strategy enough room to breathe**: Crypto is volatile; too tight a stoploss gets stopped out by normal swings

### Trailing Stoploss: The Real MVP

**Settings**:
- Activates after profit reaches 30%
- Once active, the stoploss line follows the highest point
- Distance from the highest point: 2%

**Here's an example**:
1. You bought at price 100
2. Price climbed to 130, trailing stoploss activates
3. Price climbed to 150, stoploss line is at 147 (150 × 98%)
4. Price dropped to 147, sell triggered — you made 47%!

**This is called "letting profits run"**:
- As long as price keeps climbing, the stoploss line keeps moving up
- Price retraces more than 2%, you sell and lock in most of the profit
- Won't get shaken out by minor pullbacks, but still protects most of the gains

---

## 6. How Is Take-Profit Set?

### ROI Take-Profit: 25%

**Simple version**: Consider selling when profit reaches 25%.

**But there are two exceptions**:

**Exception 1**: There's still a buy signal
- If there's still a buy signal, the trend is still going — keep holding
- Don't rush to take profit

**Exception 2**: RSI is still above 50
- If RSI is above 50, momentum is still there
- Might still go up — don't rush to sell

### Real profit-taking relies more on trailing stoploss

The 25% ROI take-profit is more like a "floor." Real profits usually come from the trailing stoploss.

Since the trailing stoploss activates at 30%, if the market is good, you can easily make more than 30%.

---

## 7. What Indicators Does It Use?

### SSL Channels (Custom Indicator)

**What is it?**
- An indicator invented by the strategy author
- Like Bollinger Bands but with ATR (volatility) added in
- Width adjusts automatically based on market volatility

**How to use it**:
- Upper rail below = bearish
- Upper rail above = bullish

### Bollinger Bands

**What is it?**
- Classic technical indicator
- Middle line is the MA, with upper and lower lines above and below
- Upper band is resistance, lower band is support

**How to use it**:
- Price breaks below lower band = might be a buy opportunity
- Price breaks above upper band = might be time to sell

### EMA (Exponential Moving Average)

**What is it?**
- A smoothed price trend line
- More responsive than regular MAs

**How to use it**:
- EMA 50 > EMA 200 = uptrend
- Price above EMA 200 = strong trend support

### RSI (Relative Strength Index)

**What is it?**
- A number from 0 to 100
- Below 30 = oversold (dropped too much)
- Above 70 = overbought (risen too much)

**How to use it**:
- At buy time: look for oversold (RSI too low)
- At sell time: look for overbought (RSI too high)

### SMA (Simple Moving Average)

**What is it?**
- The most basic moving average
- The strategy uses 5-period and 9-period

**How to use it**:
- Price below SMA = short-term weakness
- At buy time, requiring price below SMA means waiting for a pullback

---

## 8. How Does It Read Timeframes?

### Two Timeframes

**Primary Chart**: 5 minutes
- Trading decisions are made at this level
- Buy/sell signals are generated at this level

**Auxiliary Chart**: 1 hour
- Provides big-picture direction
- Ensures you're not fighting the major trend

### Why Two?

**Think of it like driving**:
- You're driving (5-minute chart)
- But you check the GPS for the overall route (1-hour chart)
- GPS says there's a jam ahead and you need to detour (trend is down)
- You won't keep going straight

**How the strategy does it**:
1. First check the 1-hour: Is the trend up? Is price above EMA 200?
2. Then check the 5-minute: Is there a good entry point?
3. Only trade when both say yes

### How Is Data Merged?

Freqtrade has a feature that "merges" 1-hour data into the 5-minute data.

For example:
- The 1-hour EMA 200 value
- Gets copied to all 5-minute candles within that hour
- So the 5-minute level can use the 1-hour judgment

---

## 9. How Big Is the Risk?

### 36% Stoploss — Risk Is Real

If that 36% stoploss actually triggers, one trade loses a lot. But:

1. Trailing stoploss usually triggers earlier
2. Strategy requires 4-6 trading pairs simultaneously to diversify risk
3. Using stablecoin pairs, volatility is relatively lower

### The Biggest Risk: Chasing and Panic Selling

**Wrong approach**:
- Only picking a few high-volatility coins
- Position size too heavy
- Poor capital management

**Right approach**:
- Pick 20-60 trading pairs
- Don't overweight any single position
- Use "unlimited position" mode for automatic allocation

### Drawdown Control

The strategy doesn't have built-in drawdown control — recommended to add your own:

- If account drawdown exceeds 20%, pause trading
- Or if drawdown exceeds 10%, cut position size in half

---

## 10. What Do You Need to Prepare?

### Hardware Requirements

**What you need**:
- A computer or server that can run 24/7
- Stable internet connection
- Run 24/7 (or use a cloud server)

### Software Requirements

**Must-haves**:
- Freqtrade (quantitative trading framework)
- Python environment
- Exchange API (for reading market data + trading)

### Capital Requirements

**Recommendations**:
- Enough to open 4-6 positions
- Each position needs enough profit margin
- Don't put all your money in one strategy

### Trading Pair Requirements

**Recommended**:
- 20-60 stablecoin trading pairs (BTC/USDT, ETH/USDT)
- Good liquidity
- Not too small-cap coins

**Not recommended**:
- BTC or ETH trading pairs (like XRP/BTC, LTC/ETH)
- Leveraged tokens (like BULL, BEAR, UP, DOWN)

---

## 11. How to Use It Safely?

### Step 1: Backtesting

**What is backtesting?**
- Testing the strategy with historical data
- See how it performed in the past

**How to do it**:
- Download at least 6 months of historical data
- Include bull, bear, and ranging markets
- Add in trading fees and slippage

### Step 2: Paper Trading

**What is paper trading?**
- Real trading with fake money
- See how the strategy actually performs

**How long?**
- At least 1 month
- Observe if signals are reasonable
- Get familiar with the strategy's buy/sell logic

### Step 3: Small Capital Live Trading

**How to start**:
- Start with a small amount
- Like only 10% of your capital
- Closely monitor every single trade

### Step 4: Gradually Add Capital

**When to add**:
- Strategy has been running for 2-3 months
- Has stable profits
- Max drawdown is acceptable

**How to add**:
- Each time add 20-30% more capital
- Don't go all-in at once

---

## 12. Which Coins Should You NOT Use?

### Definitely Don't Use

**Leveraged tokens**:
- Those with BULL, BEAR (like BTCBULL, ETHBEAR)
- Those with UP, DOWN (like ETHUP, BTCDOWN)
- These tokens have special volatility mechanics — strategy doesn't handle them

### Not Recommended

**BTC or ETH trading pairs**:
- Like XRP/BTC, LTC/ETH
- Strategy is optimized for stablecoin pairs
- BTC or ETH quote volatility rules are different

### Avoid

**Tiny-cap coins**:
- Poor liquidity
- Easy to manipulate
- Wide bid-ask spreads

**Brand new coins**:
- Not enough historical data
- Volatility patterns uncertain

### Recommended

**Stablecoin mainstreets**:
- BTC/USDT
- ETH/USDT
- Other mainstream coins/USDT pairs

---

## 13. FAQ

### Q1: Too Few Signals?

**Possible causes**:
1. Too few trading pairs
2. Market is ranging, no trend
3. Wrong timeframe

**Solutions**:
- Increase trading pairs (to 40-60)
- Confirm the timeframe is 5 minutes
- Wait for the market to develop a trend

### Q2: Too Many Losses?

**Possible causes**:
1. Picked unsuitable coins
2. Market extreme conditions
3. Stoploss not working properly

**Solutions**:
- Check trading pair list
- Pause trading, wait for market to stabilize
- Check strategy configuration

### Q3: Profits Keep Retracing?

**Possible causes**:
- Trailing stoploss setting issue
- Market volatility too high

**Solutions**:
- Lower the trailing stoploss profit offset (from 30% to 20%)
- Tighten the trailing stoploss distance (from 2% to 3%)

### Q4: Can You Use It With Other Strategies?

**Yes, but be careful**:
- Don't let the same coin be traded by multiple strategies simultaneously
- Different strategies might give opposite directions
- Recommend splitting into different trading pair pools

### Q5: How Often Should You Check?

**Recommendations**:
- Look at it at least once a day
- Do a comprehensive check once a week
- Adjust promptly if something's off

### Q6: Should You Tune Parameters Yourself?

**Not recommended at the start**:
- Strategy parameters are pre-optimized
- Run with default parameters for a while first
- Only consider adjusting after you understand the strategy

**What you can adjust**:
- Trailing stoploss parameters
- ROI targets
- Trading pair selection

### Q7: Where to Get Backtest Data?

**Freqtrade supports**:
- Download from exchange
- Or use third-party data sources
- Recommend at least 6 months of data

### Q8: How Long Until You See Results?

**At least 3 months**:
- 1 month might be luck
- 2 months might be a ranging period
- 3 months shows real performance

### Q9: Does It Guarantee Profit?

**No**:
- Any strategy has risks
- Past performance doesn't predict future
- Crypto market changes fast

**But it improves odds**:
- Good strategy improves win rate
- Good risk control controls losses
- Good mindset helps you stick with it

### Q10: What's the Most Important Thing?

**Three sentences**:

1. **Trend is King**: Only trade upward trends
2. **Risk Control First**: Strict stoploss, diversify positions
3. **Don't Be Greedy**: Steady profits beat one-shot jackpots

---

## Summary

### Core Strategy Philosophy

**One-sentence summary**:
> In an uptrend, wait for a pullback to buy, sell when it rises, use trailing stoploss to protect profits.

### Who It's For

- People with some quantitative trading experience
- Can handle the fast pace of 5-minute level
- Patient enough to backtest and paper trade
- Can strictly follow risk control

### Who's It NOT For

- People looking to get rich quick
- People who can't handle drawdowns
- People who don't have time to monitor
- People who don't understand basic technical analysis

### Final Thoughts

NostalgiaForInfinityV1 is a battle-tested strategy with clear design logic and comprehensive risk control. But even the best strategy needs:

1. **Correct usage**
2. **Continuous monitoring**
3. **Appropriate adjustments**
4. **Good mindset**

Happy trading!

---

**Document Version**: v1.0 Colloquial Version
**Strategy Author**: iterativ
**Word Count**: ~7,200 words
