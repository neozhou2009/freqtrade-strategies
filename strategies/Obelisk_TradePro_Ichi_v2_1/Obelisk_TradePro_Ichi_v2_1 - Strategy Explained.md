# Obelisk_TradePro_Ichi_v2_1 Strategy Explained (Plain English)

## Foreword: A Letter to Trading Beginners

You may have heard of "Ichimoku Cloud," or seen others use it to make money. But opening those professional books, full of Japanese terminology and complex formulas, makes your head spin. Don't worry, this document is prepared for you—using the simplest words to explain this strategy clearly.

This strategy is called Obelisk_TradePro_Ichi_v2_1, the name's a bit long, let's just call it "Ichimoku Strategy." It's an automated trading strategy that helps you decide when to buy and when to sell. Once configured, it runs on its own.

---

## Table of Contents

1. [What Does This Strategy Do?](#1-what-does-this-strategy-do)
2. [What is the Ichimoku Cloud?](#2-what-is-the-ichimoku-cloud)
3. [Five Lines to Understand the Market](#3-five-lines-to-understand-the-market)
4. [How to Use That "Cloud"?](#4-how-to-use-that-cloud)
5. [When to Buy?](#5-when-to-buy)
6. [When to Sell?](#6-when-to-sell)
7. [What If Losing? Stop-Loss Settings](#7-what-if-losing-stop-loss-settings)
8. [How to Protect Profits? Trailing Stop](#8-how-to-protect-profits-trailing-stop)
9. [What Do Parameters Mean?](#9-what-do-parameters-mean)
10. [What Market Conditions Suit This Strategy?](#10-what-market-conditions-suit-this-strategy)
11. [What Downsides to Watch For?](#11-what-downsides-to-watch-for)
12. [How Should Beginners Start?](#12-how-should-beginners-start)
13. [Final Words](#13-final-words)

---

## 1. What Does This Strategy Do?

### 1.1 One-Sentence Summary

Simply put, this is a "catch-the-trend" strategy. What does catching trend mean? When the market runs hard in one direction, you hop on, and get off when it stops running.

Like Bitcoin going from $30k to $60k, there might be ups and downs in between, but the big direction is up. This strategy helps you catch these big surge opportunities.

### 1.2 What's Different from Looking at Charts Yourself?

When you trade looking at charts yourself, maybe today you think it'll rise, tomorrow you think it'll fall, all based on feeling. But the strategy writes trading rules into code—what situations to buy, what situations to sell, all predetermined. No need to stare at charts daily, no need to struggle with decisions, code executes for you.

### 1.3 This Strategy's Characteristics

The biggest characteristic of this strategy is "careful and cautious." It needs 8 conditions all satisfied before buying. Sounds strict? Indeed, but that's also the advantage—better to miss than to make mistakes. Miss one opportunity, there's next one; make one mistake, might take a long time to recover.

---

## 2. What is the Ichimoku Cloud?

### 2.1 Don't Get Scared by the Name

"Ichimoku Cloud" sounds fancy, but actually "Ichimoku" means "one glance," and "Kinko Hyo" means "equilibrium chart." Combined, it's "one-glance equilibrium chart."

It was invented by a Japanese man named Goichi Hosoda. He developed this method in the 1930s, later became popular in Japanese stock markets. Now used worldwide, common in crypto circles too.

### 2.2 What Can It Tell You?

Ichimoku Cloud can simultaneously tell you three things:

First, which way is the big trend heading? Up, down, or sideways?

Second, where are support and resistance? Where might price bounce when falling, where might it get blocked when rising?

Third, how strong is the trend? Is it real rising or fake rising?

### 2.3 Why Suitable for Cryptocurrency?

Cryptocurrency markets have a characteristic—big volatility, sometimes 20% swings in a day. Traditional stock market parameters don't work well on crypto. This strategy adjusted all original parameters bigger, specially adapting to crypto's "crazy" markets.

---

## 3. Five Lines to Understand the Market

Ichimoku Cloud has five lines, let's explain one by one.

### 3.1 Tenkan-sen (Fast Line)

Tenkan-sen is like a short-term observer. It looks at the past 20 hours (strategy uses 1-hour chart), where price highest reached, where lowest reached, then takes the middle value.

If current price is above this line, means recent prices are relatively strong; if below, means relatively weak. This line reacts fast, changes immediately when price changes.

### 3.2 Kijun-sen (Slow Line)

Kijun-sen is similar to Tenkan-sen, but looks further—past 60 hours' high-low midpoint.

This line reacts slower, more stable. When price is above Kijun-sen, means medium-term trend is good; if below, medium-term trend not good.

### 3.3 How to Use These Two Lines?

The simplest usage is watching their crossover. When Tenkan-sen crosses from below to above Kijun-sen, like a sprinter catching up with a marathon runner, means short-term momentum got stronger, that's a buy signal.

Conversely, Tenkan-sen crossing from above to below Kijun-sen means short-term momentum weakened, weather might change.

### 3.4 Senkou Span A and Senkou Span B

These two lines need to be looked at together. They jointly draw a "cloud." Senkou Span A is the average of Tenkan-sen and Kijun-sen, moved 30 hours forward; Senkou Span B is the past 120 hours' high-low average, also moved 30 hours forward.

What does "moved forward" mean? It's drawing this line at future positions. So this cloud is "predicting" future 30 hours' support and resistance.

### 3.5 Chikou Span (Lagging Span)

Chikou Span is special—it takes current price and draws it 30 hours back.

This sounds weird, but actually verifies the trend. If Chikou Span is above the cloud, means current price is higher than 30 hours ago, trend really is rising. If Chikou Span is below the cloud, means current price is lower than 30 hours ago, trend really is falling.

---

## 4. How to Use That "Cloud"?

### 4.1 What Color is the Cloud?

Cloud has two colors. When Senkou Span A is higher than Senkou Span B, cloud is green; conversely, when Senkou Span A is lower than Senkou Span B, cloud is red.

Green cloud represents bullish market, high probability of price rising; red cloud represents bearish market, high probability of price falling.

### 4.2 Above Cloud, Below Cloud, Inside Cloud

Price relationship with cloud is important:

- Price above cloud: Bullish market, safe zone, can look bullish
- Price below cloud: Bearish market, danger zone, be careful
- Price inside cloud: Transition zone, unclear direction, wait and watch

### 4.3 Cloud Thickness Matters

Cloud thickness is the gap between Senkou Span A and Senkou Span B. Thick cloud means strong support or resistance; thin cloud means easier to break through.

Cloud going from thick to thin might be precursor to trend change; cloud going from thin to thick means trend is strengthening.

### 4.4 How Does This Strategy Use Cloud?

This strategy requires buying only when:

1. Current price is above cloud (means already in bullish zone)
2. Future cloud is green (means future expectation is still bullish)

Two conditions together mean from now to future all bullish pattern, then consider buying.

---

## 5. When to Buy?

### 5.1 Eight Buy Conditions

This strategy is strict about buying, needs 8 conditions all satisfied. Let's explain one by one in plain English:

**Condition 1: Tenkan-sen must be above Kijun-sen**

This is the most basic trend judgment. Fast line above slow line means short-term momentum stronger than medium-term.

**Conditions 2 and 3: Price must be above cloud's upper edge**

Price needs to be above cloud, and above both cloud edge lines. This ensures price has completely exited cloud area, not just poking its head out.

**Condition 4: Future cloud must be green**

Looking 30 hours ahead at the cloud, Senkou Span A needs to be higher than Senkou Span B. This represents future expectation is bullish.

**Condition 5: Chikou Span must be above cloud**

This verifies trend strength. Current price needs to be higher than 30 hours ago, and above cloud. Only then shows rising trend is real, not fake.

**Condition 6: SSL Channel must show bullish**

SSL is another technical indicator, simply speaking it's a channel drawn using volatility. Price needs to be in channel's upper half, meaning short-term momentum also supports rising.

**Condition 7: ROCR must be rising**

ROCR is rate of change, today's price divided by price 28 hours ago. This indicator needs to rise, meaning price rising speed is accelerating, not decelerating.

**Condition 8: RMI must be higher than before**

RMI is Relative Momentum Index, measuring buying and selling power. This value needs to be higher than 2 hours ago, meaning buyer power is increasing.

### 5.2 Why So Many Conditions?

You might think, so many conditions, isn't it too hard to satisfy? Indeed will miss some opportunities, but benefits are:

1. Low misjudgment rate—so many conditions simultaneously satisfied, means market really is rising
2. Avoid false breakouts—single indicator might be "fooled," multiple indicators together harder to fool
3. Buy with peace of mind—each extra condition is extra assurance

### 5.3 When Does Buying Trigger?

Not buying immediately when conditions satisfy, but at that first instant when all conditions become satisfied.

Like at 10 o'clock, 8 conditions only 7 satisfied, don't buy. At 11 o'clock see all 8 satisfied, then buy. Then if conditions continue satisfying, won't buy again, each trend only buys once.

---

## 6. When to Sell?

### 6.1 Sell Conditions

Sell conditions are looser than buy, mainly two judgments:

**Main judgment: SSL Channel no longer bullish**

SSL Channel changing from bullish to bearish, this is first signal.

**Secondary judgment: Tenkan-sen below Kijun-sen, or price below Kijun-sen**

Either one happening, plus SSL Channel bearish, then sell.

### 6.2 Why Sell Conditions More Loose?

Need to be cautious when buying, decisive when selling. Because:

1. Wrong buy loses money, wrong sell just earns less—risk not equal
2. Once trend turns, might drop fast, need to run timely
3. Better to sell a bit early than wait until nothing left to sell

### 6.3 Timing the Sell

Ideally sell near trend's highest point. But reality very hard to achieve. This strategy's approach is, wait until trend clearly turns then sell. This loses some profit but safer.

---

## 7. What If Losing? Stop-Loss Settings

### 7.1 What is Fixed Stop-Loss?

Stop-loss means "accept loss and exit." After you buy, if price drops, dropping to certain point automatically sell, no longer waiting for it to rise back.

This strategy's fixed stop-loss is -7.5%. Meaning, after buying if loss exceeds 7.5%, automatically sell.

### 7.2 Where Does 7.5% Come From?

This number is a balance result:

- Too small (like 3%): Normal crypto volatility might trigger, frequently stopped out
- Too large (like 15%): Won't trigger frequently, but when really losing hurts badly

7.5% for cryptocurrency, reasonable range that can handle normal volatility while controlling losses.

### 7.3 Stop-Loss Function

Stop-loss is like seatbelt, might not use normally, but life-saving at critical moments.

Many beginners lose big money because they don't stop-loss. After buying and price drops, thinking "wait, might rise back." Result drops more and more, finally can't bear the loss and cut, suffering heavily.

Stop-loss helps overcome this psychology—sell at the point, no fantasies.

---

## 8. How to Protect Profits? Trailing Stop

### 8.1 What is Trailing Stop?

Fixed stop-loss prevents losses, trailing stop protects profits.

Suppose after you buy, price rises 10%. At this point if no protection, price might drop back, profit becomes loss. Trailing stop rises following price rise, helping lock in profits.

### 8.2 This Strategy's Trailing Stop Settings

This strategy's trailing stop has three parameters:

1. **Activation threshold: 3%** — Trailing stop starts working only after profit exceeds 3%
2. **Trailing distance: 0.5%** — Trigger sell if pullback from highest point exceeds 0.5%
3. **Only effective after activation: Yes** — Before profit reaches 3%, no trailing stop

### 8.3 An Example

Suppose you buy at $100:

- Price rises to $103 (3% profit): Trailing stop activates, stop line around $102.5
- Price rises to $110: Stop line rises to about $109.5
- Price drops from $110 to $109: Still in safe range
- Price continues dropping below $109.5: Triggers sell, locks about 9.5% profit

### 8.4 Trailing Stop Benefits

Trailing stop lets you eat most of trend's profits, while not giving back profits when trend reverses.

It's like a moving "take-profit point," always following highest price. As long as trend still rising, it follows; once trend turns, it helps you sell.

---

## 9. What Do Parameters Mean?

### 9.1 Time Period

This strategy uses 1-hour chart. Each candle represents 1 hour's price change.

Why choose 1 hour? Too small (like 5 minutes) too much noise, many fake signals; too large (like daily) too few signals, miss opportunities. 1 hour is a compromise, both sufficient signals and filtering intraday volatility.

### 9.2 Ichimoku Parameters

Strategy uses "crypto customized" parameters:

- Tenkan-sen period: 20 (traditionally 9)
- Kijun-sen period: 60 (traditionally 26)
- Lagging span period: 120 (traditionally 52)
- Displacement period: 30 (traditionally 26)

Why all bigger? Because crypto volatility is big. Traditional parameters might work in stock markets, but in crypto markets frequently interfered by fake signals. Bigger parameters filter more noise.

### 9.3 SSL Channel Parameters

SSL Channel uses 10 periods. This is relatively sensitive, can quickly react to short-term momentum changes.

ATR period is 14, used to calculate channel width. ATR automatically adjusts based on market volatility—channel widens when volatility high, narrows when low.

### 9.4 Risk Control Parameters

- Fixed stop-loss: -7.5%
- Trailing stop activation: 3% profit
- Trailing stop distance: 0.5%
- Minimum return: 10% at opening, 5% after 30 minutes, 2% after 60 minutes

These parameters can be adjusted based on your risk preference. More conservative can tighten stop-loss, more aggressive can loosen.

---

## 10. What Market Conditions Suit This Strategy?

### 10.1 Best for Trend Markets

This strategy is most suitable for single-direction trend markets—price keeps rising or falling, with small pullbacks in between.

In this kind of market, strategy can eat most of the rise, from trend start to trend end, substantial profits.

### 10.2 Average Performance in Ranging Markets

Ranging markets are price oscillating in a range, no clear direction.

In ranging markets, strategy might keep stopping out. Buy then rises a bit then drops back, triggers stop-loss; then buy again, stop again. Repeated several times, accumulated losses not small.

### 10.3 Unsuitable Markets

Extremely volatile markets (like sudden big news) and extremely quiet markets (very low volume, price not moving) are not suitable.

In these markets, technical indicators easily fail, strategy judgment may be inaccurate.

### 10.4 How to Judge Suitability?

You can use two simple indicators:

1. Watch ATR—moderate volatility is best
2. Watch trend strength—ADX indicator above 25 means there's trend

If market has no trend, suggest pausing use or reducing position size.

---

## 11. What Downsides to Watch For?

### 11.1 Will Miss Some Opportunities

Because buy conditions are too strict (8 conditions all satisfied), some trend early stages will be missed. When you enter, already rose a segment.

But this is intentional—better to miss than to make mistakes. Missing just earns less, making mistakes loses money.

### 11.2 Will Lose Money in Ranging Markets

In sideways ranging markets, strategy will repeatedly buy and sell, each time losing a bit, accumulated amount not small.

Solution: Identify ranging markets, reduce trading or don't trade. Can add ADX indicator, pause strategy when ADX below 20.

### 11.3 Parameters Might Need Adjustment

This strategy's parameters are optimized based on historical data, but markets change. Parameters that worked in past may not work in future.

Suggest regular backtesting, see if parameters need tweaking. But also watch not to over-optimize—making parameters too perfectly adapted to historical data might actually perform poorly in live trading.

### 11.4 Only Long, No Short

This strategy only buys rising, doesn't sell falling. In bear markets, strategy keeps empty position, missing shorting opportunities.

If you want to earn in bear markets too, can consider other shorting strategies, or find platforms supporting shorting.

---

## 12. How Should Beginners Start?

### 12.1 Backtest First, Then Live Trading

Never start with real money! First use historical data to backtest, see how strategy performed in the past.

Backtesting helps you understand:
- What's the win rate
- How big is maximum drawdown
- What kind of markets suit it

After backtesting satisfied, then consider live trading.

### 12.2 Simulate First, Then Real Money

Many exchanges have simulation trading function. Run for a while in simulation environment, see strategy's actual performance.

Simulation trading has no psychological pressure, but helps you familiarize with operation flow and strategy characteristics.

### 12.3 Start with Small Money

When starting real money, first use small amount. After confirming strategy steadily profitable, then slowly increase position.

Experience says: First use money you can afford to lose. Assume this money completely lost won't hurt, use this amount to start.

### 12.4 Choose Suitable Trading Pairs

Not all coins suit this strategy. Suggest choosing:

1. Large volume mainstream coins (good liquidity)
2. Some volatility, but not extreme volatility
3. Listed long enough (at least dozens of days)

Bitcoin, Ethereum these mainstream coins are good choices.

### 12.5 Regular Checks

After strategy runs, regularly check:

1. Profit/loss situation
2. Whether drawdown exceeds expectation
3. Whether market environment changed

Find anomalies timely analyze causes, pause strategy if necessary.

---

## 13. Final Words

### 13.1 Strategy is Just a Tool

Even the best strategy is just a tool, key to making money is still the person using the tool.

You need to understand strategy logic, know when it works, when it might fail. Don't blindly believe backtest data, don't deny strategy because of short-term losses.

### 13.2 Risk Always Exists

Quantitative trading can't guarantee profit, any strategy has losing risk. What you can do:

1. Control position size, don't go heavy
2. Strict stop-loss, don't hold stubbornly
3. Keep patience, don't chase fast profits

### 13.3 Continuous Learning

Markets change, strategies need to change too. Keep learning, understand new technologies and methods, continuously optimize your strategy.

### 13.4 Good Luck

Hope this plain English explanation helps you understand this strategy. Trading journey is long, keep learning, keep cautious, hope you find your own profitable pattern in cryptocurrency markets.

---

*Last Updated: 2024*
*Strategy Version: Obelisk_TradePro_Ichi_v2_1*
*Time Period: 1 Hour*