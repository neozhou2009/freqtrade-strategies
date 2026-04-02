# Obelisk_TradePro_Ichi_v1_1 Strategy Explained (Plain English)

## Intro: What Does This Strategy Do?

Simply put, this is a strategy that uses the "Ichimoku Cloud" invented by a Japanese gentleman to trade cryptocurrencies. It automatically helps you decide when to buy and when to sell. The core idea is: **Follow the trend - buy when the trend is up, sell when the trend is down.**

This strategy was published by someone named Obelisk in March 2021, with the core logic coming from a YouTube channel called Trade Pro's tutorial video. Although the video title was a bit exaggerated (claiming "100 trades verified"), this strategy definitely has substance.

Honestly, the coolest thing about this strategy is that it transformed an old-school financial market tool (Ichimoku) into a new weapon for cryptocurrency. It's like turning a classic car into a race car - the chassis is the same, but the engine has been upgraded.

---

## Chapter 1: What is the Ichimoku Cloud?

The Ichimoku Cloud sounds fancy, but it's basically a "weather map" drawn on a chart. It was invented by Japanese analyst Goichi Hosoda (pen name Ichimoku Sanjin) in the 1930s. The name literally means "one-glance equilibrium chart" - letting traders see market conditions at a glance.

It has five lines, each with its own name and purpose:

### Tenkan-sen (Conversion Line)
Like a thermometer, it tells you if short-term conditions are hot or not. Standard setting looks at the average of the highest high and lowest low over the past 9 periods. This line reacts fastest and is most sensitive to price changes.

### Kijun-sen (Base Line)
Like an average temperature line, it tells you which way the medium-term trend is heading. Standard setting is 26 periods. This line is more stable and an important reference for trend direction.

### Senkou Span A (Leading Span A)
This is the average of the Tenkan-sen and Kijun-sen, plotted 26 periods ahead. Think of it as a "future weather forecast" - telling you whether it'll be sunny or rainy later.

### Senkou Span B (Leading Span B)
This is the average of the highest high and lowest low over 52 periods, also plotted ahead. The area between the two lines is the "cloud." Green cloud means bullish, red cloud means bearish.

### Chikou Span (Lagging Span)
This one's special - it takes the current closing price and plots it 26 periods back. It's like looking at yesterday's weather to confirm if a trend is real.

When the Japanese invented this, they wanted traders to understand market conditions at a glance, without constantly staring at candlestick charts guessing. This was very advanced thinking in the pre-computer era.

---

## Chapter 2: What Makes This Strategy Different?

Most Ichimoku strategies on the market use "standard parameters" (9-26-52-26), designed by the Japanese decades ago for stock markets. But cryptocurrency markets are completely different from stocks:

**Cryptocurrency Characteristics:**
- 24/7 trading, no closing time
- Insane volatility - 20% daily swings are normal
- Crazy rallies and crashes
- Extreme market sentiment, prone to pump and dump

So this strategy changed all the parameters:
- Conversion line from 9 to **20** (more than doubled)
- Base line from 26 to **60** (more than doubled)
- Lagging span from 52 to **120** (more than doubled)
- Displacement from 26 to **30** (looking further ahead)

This is like changing a sprinter's training plan to a marathon runner's. The original parameters were too fast for crypto markets - you'd get slapped repeatedly. Slowing things down helps see the bigger trend without getting tricked by small fluctuations.

**Example**: With standard parameters, the conversion line is 9 periods. On a 1-hour chart, that's looking at the past 9 hours. That's way too short - crypto can swing back and forth several times in 9 hours. Change it to 20 hours, and you're looking at almost a full day's trend - much more stable.

---

## Chapter 3: How Does the Strategy Decide When to Buy?

This strategy has FIVE conditions that must ALL be met before it signals a buy. Like finding a partner who must have "a house, a car, savings, good looks, and good personality" - miss one and it's a no-go.

### Condition 1: Tenkan-sen Must Be Above Kijun-sen

This is called a "golden cross," the most basic buy signal. The Tenkan-sen reacts fast, the Kijun-sen reacts slow. When the fast one jumps above the slow one, it means short-term momentum has strengthened.

It's like a sprinter running ahead of a marathon runner - shows strong explosive power right now.

### Condition 2: Price Must Be Above the Cloud

The cloud is like the boundary between sky and ground. Price above the cloud is like a bird flying in the sky - good sign for uptrend. Price inside the cloud is like being in fog - can't see direction clearly. Price below the cloud is like crawling on the ground - definitely not good.

This condition ensures we only buy when the trend is clearly upward.

### Condition 3: Price Must Be Above the Cloud's Lower Edge

This is basically the same as condition 2, just ensuring price is completely outside the cloud, not just poking its head in. Why separate it? Because the cloud is dynamic - sometimes the upper and lower edges are far apart, and we need to confirm price has truly "broken through."

### Condition 4: The Future Cloud Must Be Green

This is cool - it can "see the future"! Of course not really time travel, but through calculation. Because the cloud is plotted 26 periods ahead, the "future cloud" at current position can actually be calculated.

If the future cloud is green, the uptrend should continue for a while. If the future cloud has already turned red, buying now means catching a falling knife.

### Condition 5: Lagging Span Must Be Above the Cloud

The lagging span is past closing prices. If closing prices from the past 26 periods (30 in this strategy) are also above the cloud, it means this trend has been stable for a while, not just a flash in the pan.

It's like making friends - you wouldn't trust someone you met yesterday, but someone you've known for a month is more reliable.

---

## Chapter 4: When Should You Sell?

Sell conditions are much simpler - either of two triggers means run:

### Condition 1: Tenkan-sen Falls Below Kijun-sen

This is called a "death cross," the most basic sell signal. The Tenkan-sen reacts fast, the Kijun-sen reacts slow. When the fast one falls below the slow one, short-term momentum has weakened.

Like a sprinter suddenly running out of gas and falling behind the marathon runner - that's a sign of exhaustion, time to exit.

### Condition 2: Price Falls Below the Base Line

The base line represents the medium-term trend. Price breaking below it is like a car driving out of its lane - dangerous! This usually means the trend might reverse, don't stick around.

### Safety Mechanism: Stop-Loss

Besides these signal exits, there's a hard stop-loss: **Lose 1.5% and you're out.**

No matter the reason, if you lose 1.5%, exit unconditionally. Sure you'll take a small loss, but you won't lose big. In a volatile market like crypto, setting a stop-loss is like wearing a seatbelt - usually unnecessary, but life-saving in critical moments.

---

## Chapter 5: Has This Strategy Made Money?

According to backtest data provided by the author (February 1 to March 24, 2021, about 52 days):

**Overall Results:**
- Total trades: 208
- Total profit: 131.9% (more than doubled in 52 days!)
- Win rate: Only 24% (roughly 1 win per 5 trades)

Wait, such a low win rate and still makes money? Exactly! This is the essence of trend-following strategies - **cut losses short, let profits run.**

**Detailed Analysis:**
- Stop-loss exits: 145 trades, average loss 1.54%, total loss about 223%
- Signal exits: 63 trades, average gain 14.01%, total gain about 883%
- Net profit: 883% - 223% = 660% (actual is 131.9% due to compounding, etc.)

**Risk-Reward Ratio**: 14.01% ÷ 1.54% ≈ 9x

This means: although you lose often, each loss is small; you win rarely, but each win is big. The final tally is profitable.

Let's say you play mahjong: out of 10 rounds, you lose 8, losing 10 dollars each round, total loss 80 dollars. But you win 2 rounds, winning 500 dollars each, total win 1000 dollars. You still net 920 dollars.

This is the core logic of trend-following: **Would rather take small losses many times to catch big opportunities.**

---

## Chapter 6: Which Coins Suit This Strategy?

Not all coins work with this strategy. From backtest data:

**Good Performers (Star Players):**
- BTMX/USD: +459.2% (Wow!)
- LINA/USD: +127.2%
- FTT/USD: +81.1%
- ETH/USD: +25.5%

**Poor Performers (Drag):**
- ADABULL/USD: -10.8%
- SRM/USD: -9.2%
- AAVE/USD: -9.7%
- LINK/USD: -8.8%

**Pattern Summary:**
- This strategy likes coins with **clear trends**
- Doesn't like coins that **range sideways**
- Leveraged tokens (names with BULL) perform poorly, possibly due to weird volatility
- Major coins (BTC, ETH) perform relatively stably

**Recommendation:** Don't use this strategy on all coins. Backtest first to see which coins perform well, and only trade those.

---

## Chapter 7: What Are the Risks?

Don't get carried away by the 131.9% return - the risks are real:

### Risk 1: 40% Maximum Drawdown

This is the scariest part. Drawdown is the decline from the highest point to the lowest point. Let's say you have $100, it goes to $150 (50% profit), then drops to $90 (40% drop from high), you now have $90.

**Key Point:** Although total profit is 131.9%, you might have experienced a 40% drawdown in between. If you entered at the peak, your account could shrink 40%.

This requires strong psychological endurance. Many people can't handle watching their account go from 100 to 60 and might panic-sell at the bottom, missing the subsequent recovery.

### Risk 2: Low Win Rate

Out of 5 trades, 4 are losers. Can you stay calm watching your account lose day after day?

It's like fishing - most of the time the bait gets eaten by small fish (small stop-losses), only occasionally catching a big fish (big wins). Requires patience and conviction.

### Risk 3: Gets Slapped Repeatedly in Ranging Markets

If the market swings back and forth without clear direction, this strategy will keep entering and getting stopped out, accumulating losses.

**Example:** Price oscillates between 100-105. The strategy might:
- Price rises to 103, triggers buy
- Price drops to 101.5, triggers stop-loss, lose 1.5%
- Price rises to 104, triggers buy
- Price drops to 102.5, triggers stop-loss, lose another 1.5%
- ...repeat multiple times

Before the real trend comes, you might have been slapped several times already.

### Risk 4: Parameters Might Be Overfitted

These parameters were optimized based on historical data and may not work as well in the future. Markets change, and strategies need to evolve with them.

---

## Chapter 8: How to Choose Timeframes?

Default is **1-hour chart**, a balanced choice:

**Timeframe Impact:**
- **Too short (like 5min, 15min):** Too many signals, too frequent trading, fees eat profits, lots of noise
- **Too long (like 4hr, daily):** Too few signals, not many opportunities, might go a month without trades
- **1 hour:** Just right, maybe a few trades per day, not too busy to handle

**Adjust Based on Your Situation:**
- **Professional traders:** Can use shorter timeframes (15min, 30min) to catch more opportunities
- **Office workers:** Can use longer timeframes (4hr, daily), don't need frequent operations
- **Beginners:** Recommend starting with 1 hour, adjust after getting familiar

**Note:** When changing timeframes, Ichimoku parameters need corresponding adjustment. Can't just copy 1-hour parameters to daily chart.

---

## Chapter 9: Is 1.5% Stop-Loss Too Small?

Good question! 1.5% is indeed tight - normal crypto volatility can hit that easily.

**Designer's thinking might be:**
1. Would rather small loss many times than big loss once - protect capital first
2. If entry is good, 1.5% pullback shouldn't trigger - good signals can handle it
3. Crypto is volatile, wider stop-loss might mean bigger losses - small stop-loss is safer

**But some think:**
1. Too easy to get "stopped out" - just stopped out, price continues in original direction
2. Too much market noise - 1.5% might just be normal fluctuation
3. Could widen to 2-3% - give price some breathing room

**My suggestion:**
- Run with default 1.5% for a while first, see how it works
- If frequently stopped out and price continues, consider widening
- If widening leads to bigger losses, change back
- Stop-loss size is personal choice, no standard answer

---

## Chapter 10: Can It Be Improved?

Of course! Here are some ideas:

### Improvement 1: Dynamic Stop-Loss

Don't fix at 1.5%, adjust based on market volatility:
- Wider stop-loss when volatility is high (like 2%)
- Tighter stop-loss when volatility is low (like 1%)

Use ATR (Average True Range) indicator to measure volatility.

### Improvement 2: Add Market Environment Filter

Don't trade during ranging markets, only trade when trend is clear:
- Add ADX indicator, don't trade when ADX below 25 (ranging market)
- Or add Bollinger Bands, don't trade when bands are narrowing
- Simply watch EMA slope too - too flat means don't trade

### Improvement 3: Position Sizing

Don't buy the same amount every time:
- Buy more when signal is very strong (all five conditions perfect)
- Buy less when signal is marginal (barely meeting conditions)
- Adjust position size based on account profit/loss, add when winning, reduce when losing

### Improvement 4: Only Trade Good Performers

From backtest data, some coins clearly don't suit this strategy:
- Kick those coins out, only trade suitable ones
- Regularly backtest, dynamically adjust coin pool
- Major coins (BTC, ETH) are generally stable, can prioritize

### Improvement 5: Scale Out Profits

Don't sell all at once, scale out:
- Sell half at 5% gain, secure profit
- Set trailing stop for the rest, let profits run
- This way you secure gains without missing big moves

---

## Chapter 11: How Should I Use This Strategy?

### Step 1: Select Coins

Pick a few liquid coins with trending history:
- **Safe choice:** Major coins like Bitcoin, Ethereum, good liquidity, relatively regular patterns
- **Aggressive choice:** Hot altcoins, potentially higher returns but higher risk too
- **Avoid:** Leveraged tokens (BULL/BEAR), stablecoins, very low volume coins

Recommend starting with 2-3 coins, don't be greedy.

### Step 2: Determine Capital

Don't put all your money in:
- Prepare money you can withstand 40% drawdown (e.g., if you have 100k, start with 20k)
- Single trade risk no more than 1-2% of total capital
- Maximum 5-10 concurrent positions

**Position Sizing Formula:**
```
Per trade amount = Total capital × Risk ratio ÷ Stop-loss ratio
                  = 10000 × 1% ÷ 1.5%
                  = 6666 dollars
```
In other words, if you have $10,000, with 1.5% stop-loss, you can lose up to $150 per trade. If you want each loss to be no more than 1% of total capital ($100), then each trade should be around $6,666.

### Step 3: Set Parameters

Run with default parameters first, then adjust based on actual performance:
- Stop-loss size: Observe if frequently getting stopped out
- ROI targets: Observe if profit targets are reasonable
- Ichimoku parameters: Unless you really understand, suggest not changing

### Step 4: Let It Run

Let the bot run on its own, you only need to:
- Check overall performance once a week
- Review trading records once a month
- Stop or adjust promptly if performance degrades

**Don't:**
- Don't stare at your account daily
- Don't panic after one or two losses
- Don't add leverage after one or two wins
- Don't frequently change parameters

---

## Chapter 12: The Core Wisdom of This Strategy

One sentence to summarize this strategy:

**"Would rather not earn than lose big; would rather small loss than big loss; catch one big trend and it's worth countless small stop-losses."**

This is the essence of trend-following. It's not about catching every opportunity, but being present when big opportunities come and accepting small losses gracefully.

**Comparison of Three Trading Philosophies:**

| Philosophy | Characteristics | Suitable For |
|------------|----------------|--------------|
| Trend Following | Low win rate, high risk-reward ratio | Patient people |
| Grid Trading | High win rate, small per-trade profit | People who like frequent trading |
| Arbitrage | Almost risk-free, small profit | People seeking stability |

**This strategy is the first type**, need to accept:
- Frequent losses are normal
- Most losses are small
- Occasional big win covers all losses
- Need patience to wait for big trends

Like fishing:
- Most times bait gets eaten by small fish (small stop-losses)
- Occasionally catch a big fish (big win)
- Overall, the big fish is worth more than the bait

Or like startups:
- 9 out of 10 projects fail (small stop-losses)
- 1 succeeds, valuation goes 100x (big win)
- Investors still profit overall

---

## Chapter 13: Final Words

This strategy isn't a "holy grail" and can't guarantee you'll make money. But it's a trading system with clear logic and controllable risk.

**Advantages:**
- Clear rules, no guessing, fully automated execution
- Parameters optimized for cryptocurrency
- Small stop-loss, big win, great risk-reward ratio (~9:1)
- Clear exit conditions, won't stubbornly hold

**Disadvantages:**
- Will lose repeatedly in ranging markets
- Drawdown can be big (40%)
- Low win rate (24%), psychological pressure
- Requires patience

**Suitable For:**
- People who believe in trend-following philosophy
- People who can accept low win rate with high risk-reward
- People with enough capital to handle drawdowns
- Patient, not impulsive people

**Not Suitable For:**
- Impatient people who want to change strategy after seeing losses
- People with too little capital, can't handle consecutive stop-losses
- People who like pursuing high win rates
- People without trading discipline

---

## Appendix: Key Parameters Quick Reference

| Parameter | Value | Meaning |
|-----------|-------|---------|
| Timeframe | 1 hour | How long each candle represents |
| Conversion Line Period | 20 | Short-term trend line, standard is 9 |
| Base Line Period | 60 | Medium-term trend line, standard is 26 |
| Lagging Span | 120 | Historical confirmation line, standard is 52 |
| Displacement | 30 | How far cloud projects forward, standard is 26 |
| Stop-Loss | -1.5% | Exit at this loss |
| First Target | 10% | 10% target right after entry |
| 30min Target | 5% | Take 5% after holding 30 minutes |
| 60min Target | 2% | Take 2% after holding 60 minutes |
| Max Positions | 5 | Maximum 5 concurrent positions |
| Startup Candles | 120 | Need 120 candles before trading starts |

---

## FAQ

**Q1: Why are parameters so much bigger than standard Ichimoku?**
A: Crypto is more volatile. Standard parameters are too sensitive, easy to get fake signals. Bigger parameters are more stable, filter out noise.

**Q2: Win rate only 24%, does the strategy suck?**
A: Can't just look at win rate, look at risk-reward ratio. This strategy has ~9:1 risk-reward. Math: 24% win rate × 14% profit - 76% loss rate × 1.5% loss = positive return.

**Q3: Can I widen the stop-loss?**
A: Can try, but need to backtest to verify. Wider stop-loss means bigger single loss, might affect overall risk-reward ratio.

**Q4: Can this strategy be used on other markets?**
A: Theoretically yes, but parameters need adjustment. Stocks and forex have different volatility characteristics, might need to re-optimize parameters.

**Q5: Need manual intervention?**
A: Generally no, fully automated. But suggest checking performance weekly, handle anomalies promptly.

---

*After reading this, you should have a basic understanding of this strategy. If you still have questions, suggest looking at the code or running a backtest to experience it.*

*Remember: Learning from paper is shallow, true knowledge comes from practice. Happy trading!*

---

*Document Version: v1.0*
*Generated Date: March 27, 2026*