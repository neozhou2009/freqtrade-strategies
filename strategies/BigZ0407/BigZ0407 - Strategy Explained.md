# BigZ0407: The "Survival First" Dip-Buyer

> **Nickname**: Low Drawdown King  
> **Profession**: Crypto market's cautious survivor — would rather miss out than lose big  
> **Timeframe**: 5 minutes (main) + 1 hour (big picture)

---

## 1. What's This Strategy?

BigZ0407 is a trading strategy created by a developer named ilya. This brother shared the strategy on GitHub, and basically it comes down to one sentence: **how to make losses smaller, and even smaller**.

Think about it, in the crypto world, making money is important, but what's more important is not losing big. This strategy is designed around that idea. Its core thinking is simple: wait until prices drop enough before buying, then sell as soon as there's a small profit, definitely don't get greedy. Why? Because you never know if prices will keep falling, cutting losses early is more important than waiting to break even.

This strategy also has a feature: it's not those rigid buy/sell rules, it has 11 different entry conditions, just like the 18 martial arts weapons in wuxia novels, each with different moves. Use this move when the market's bad, use that move when the market's good, there's always one that can catch opportunities.

The author says he improved it from another strategy called CombinedBinHAndClucV6, but added a lot of risk control stuff. He also says this strategy works best with 2 to 4 trading pairs open at the same time, don't open too many or you can't manage them.

## 2. Core Settings: Basically "Don't Lose Money"

Let's talk about basic settings first. Time-wise it uses 5-minute candles, but simultaneously looks at 1-hour data to judge the big direction. It's like when you're doing things, you can't just look at the present, you also have to think about whether you'll regret it later.

The stoploss setting is quite special, default is -99%, basically equals not using the stoploss function at all. Why? Because this strategy uses a set of self-developed "smart stoploss," much smarter than that simple percentage stoploss.

For take-profit, the strategy uses trailing stop, roughly starts watching when profit exceeds 1%, starts preparing to run when it rises 2.5%. This is like playing mahjong, win and run, don't think about winning more.

Order type uses limit orders, simply put I want to buy at this price, no rush to execute. Stoploss orders use market orders, so when something big really happens you can run faster.

## 3. 11 Entry Conditions

This strategy has up to 11 entry conditions, sounds a bit exaggerated right? But this is exactly where its power lies. Let me count them out for you:

**First type, RSI oversold rebound**. When 5-minute RSI drops below 30, simultaneously 1-hour RSI also below 71, and volume shrinks, buy at this time, wait for rebound.

**Second type, Bollinger Band lower rail type**. Price drops below the Bollinger Band, but still above 200-day moving average, 1-hour RSI also can't be too high, go in and pick up bargains at this time.

**Third type, MACD golden cross type**. MACD fast line rushes up from below, and price is still at Bollinger Band lower rail, this pattern shows bulls are starting to exert force.

**Fourth type, volume shrinkage type**. Volume suddenly expands earlier (might be spiking), then rapidly shrinks, price is at low levels at this time, often a good opportunity.

**Fifth to eleventh types**, basically are permutations and combinations of the conditions above, some need RSI especially low, some need to satisfy several conditions simultaneously. In short, one sentence: **have to wait for multiple indicators to point in the same direction before acting**.

## 4. Protection Mechanisms

This strategy's protection mechanisms, called comprehensive, is basically an "umbrella of protection."

**First layer protection: Custom stoploss**. The strategy watches position holding time, if opened over 50 minutes and still no improvement, starts preparing to run. Whether to actually run also depends on 1-hour RSI, if RSI is still very low, shows might fall more, then just cut the flesh; if RSI starts rising back, then wait a bit more.

**Second layer protection: Trailing take-profit**. As long as profit exceeds 1%, system remembers this price. Later whenever falls more than 2.5% from highest point, runs without saying a word. This trick works especially well when market reverses.

**Third layer protection: Pump protection**. Crypto circle often has those sudden spike up then crash down situations, strategy detects price volatility within 48 hours, 36 hours, 24 hours. Once something's not right, like rose too fiercely, immediately starts special protection mode, no matter how much earned, pocket it first.

**Fourth layer protection: Trend reversal detection**. If 200-day moving average starts walking down, and price already broke below 200-day moving average, strategy becomes especially careful, wants to run with just a bit of profit.

**Fifth layer protection: Recovery mechanism**. If accidentally bought high, lost quite a bit of money, as long as slightly break even a bit, strategy runs. This looks a bit conservative, but indeed can avoid bigger losses.

## 5. Exit Logic

After talking about protection mechanisms, let's talk about how the strategy specifically exits. The strategy's exit logic is the most complex I've ever seen, has dozens of different exit conditions.

**First type, fixed tiered take-profit**. Strategy decides when to sell based on how much you earned. Earned over 20%, run as long as RSI exceeds 34; earned 10% to 12%, run when RSI exceeds 42; and so on, the less earned the more can tolerate RSI being high.

**Second type, EMA200 below special handling**. If price already broke below 200-day moving average, no matter how much earned, as long as RSI reaches corresponding level, run, absolutely don't linger.

**Third type, trend reversal run**. If 200-day moving average starts declining, and price also fell below the moving average, no matter how much earned at this time, have to start preparing to run.

**Fourth type, long-term position handling**. If position held over 15 hours (900 minutes), and profit between 3% to 4%, also triggers exit. This is to prevent stubbornly holding on.

**Fifth type, recovery exit**. If unfortunately bought at the mountain top, lost over 6%, as long as slightly break even to 1% to 4%, and RSI below 46, strategy runs. Although lost, but at least won't lose more.

In summary, this strategy's exit logic is: **rather earn less, absolutely don't lose more**. These eight characters are the soul of the entire strategy.

## 6. Strategy's "Personality Traits"

If the strategy were compared to a person, BigZ0407 is a **particularly cowardly old fox**.

Where does its cowardice show? First, it never bottoms out during downtrends, must wait until trend stabilizes before starting to buy. Second, it wants to run after making money, absolutely not greedy. Third, it's constantly watching the market, prepares to run at the slightest wind or movement.

But where does its fox side show? First, it has 11 different entry methods, uses different moves based on different market conditions. Second, it's very good at timing, knows when to enter, when to retreat. Third, it won't be fooled by simple rebounds, must wait for multiple indicators to confirm before acting.

This strategy also has a characteristic: **especially懂得 how to assess the situation**. It performs best in oscillating markets, because this market condition most needs high sell low buy. In one-sided uptrend markets it might sell too early, missing some profits. But this exactly shows its cautious personality — **rather miss out, absolutely don't make mistakes**.

## 7. Suitable Scenarios

BigZ0407 strategy has several particularly suitable scenarios, listen to me count them out.

**First type, oscillating markets**. Price jumps up and down, but overall fluctuates within a range. At this time the strategy's oversold entry conditions can trigger frequently, can earn a bit each rebound. Although single earnings aren't much, but little by little adds up.

**Second type, rebounds after big drops**. Price fell from highs, already dropped quite a bit, go in and pick up bargains at this time, run after rebound. This kind of opportunity is especially common in crypto circle, because crypto circle is really fierce when it drops.

**Third type, high volatility markets**. Strategy has pump protection mechanism, specially handles those sudden spike up crash down situations. In this market condition, other strategies might not react in time, but BigZ0407 can quickly start protection mode.

**Fourth type, major coin trading**. BTC, ETH this kind of good liquidity coins, strategy's volume analysis can be accurate. Small market cap coins not recommended for this strategy, because volume too small, signals easily distorted.

Be cautious using in these scenarios: **one-sided uptrend bull markets**, strategy might sell too early; **long-term sideways**, too many signals but limited profits; **before/after major events**, market too crazy, strategy might not judge accurately.

## 8. Summary

BigZ0407 this strategy, simply put is a **risk control maniac**. All its design revolves around one objective: how to lose less money.

Advantages are very clear: risk control done well, many signals many opportunities, can also adapt to different market environments. For those scared of being cut in crypto circle, this strategy is simply a protective god.

But disadvantages also have to admit: too complex, 11 entry conditions, dozens of exit conditions, hundreds of parameters, ordinary people can't handle it at all. And because too conservative, might not earn as much as the bold in one-sided markets.

But I think, for most ordinary investors, **being conservative a bit is always fine**. Surviving in this market is more important than anything, keep the green hills and there'll be firewood to burn.

## 9. Market Performance

From theoretical analysis, this strategy should perform best in **oscillating markets**. Why? Because oscillating market characteristics are prices up and down, strategy's oversold entry conditions can trigger frequently, and each rebound can reach take-profit point.

In **rebound after decline** markets, strategy should also have good performance. Because this market condition is exactly the strategy's design original intention — buy at low points, run after rebound.

In **one-sided uptrend** markets, strategy's performance might be discounted. Because strategy's exit logic relatively conservative, might get shaken out after earning just a bit, watching the big market behind miss out.

In **one-sided decline** markets, strategy will struggle. Although entry conditions can find oversold opportunities, but market's continuous decline might make these buys all "catching falling knives," easy to buy halfway down the mountain. Suggest reducing positions or temporarily stopping trading at this time.

In summary, this strategy not suitable for that "all in one go" approach, more suitable for **slow and steady** playstyle. Accumulate little by little, over time you'll discover, compound interest's power scarier than any get-rich-quick myths.

## 10. Configuration Suggestions

If you decide to use this strategy, here are several suggestions for your reference.

**First, suggest opening 2 to 4 trading pairs simultaneously**. Open too few waste opportunities, open too many can't manage. And different coins' performance can compensate each other, this one loses that one earns, overall still acceptable.

**Second, don't greedily set too high expected returns**. Strategy's design philosophy is "small steps fast run," each time earning 1% to 5% is satisfied. Don't think about getting rich overnight, that's not this strategy's style.

**Third, regularly check strategy performance**. Although strategy runs automatically, but you have to occasionally look at whether it's working normally.if there's a bug，you can also discover timely.

**Fourth, do fund management well**. Suggest each trading pair use at most 10% to 20% funds, don't all in.万一遇到 continuous losses, also won't hurt the foundation.

**Fifth, consider adding positions when market panicking**. This strategy should be greedy when others are fearful, because panic often means oversold, opportunities come.

## 11. Easter Eggs

You know what's the most interesting thing about this strategy? Its stoploss setting is -99%, on the surface looks like no stoploss, actually it uses a set of smarter stoploss methods.

Author ilya mentioned in strategy description, this strategy's inspiration comes from another strategy called CombinedBinHAndClucV6. He says he borrowed a lot of iterativ's ideas, but himself did a lot of improvements in risk control.

Another interesting point, this strategy supports donations. Users can see author's BTC and ETH addresses in README. Although voluntary, but if you earned money using this strategy, donating a bit to author is also should, after allthey developed such a good useful strategy.

Oh right, this strategy also has a bunch of optimization parameters, but default all turned off. Author's meaning is, default parameters already good enough, if you're not especially confident, don't casually turn on optimization. Optimization this thing, accidentally easy to over-optimize, looks historical data perfect as hell, actually use it and it's trash.

## 12. Finally Finally

Using this strategy most importantly remember eight characters: **rather miss out, absolutely don't make mistakes**.

Market has plenty of opportunities, but not every opportunity should be grabbed. This strategy teaches us not how to make big money, but how to survive longer in this market. As long as alive, have opportunities; if dead, then nothing left.

Don't think about getting rich overnight, those are all fairy tale stories. Down to earth doing, accumulate little by little, after long time you'll discover, compound interest's power scarier than any get-rich-quick myths.

Last sentence, investment has risks, enter market需cautiously。No matter what strategy, can't guarantee 100% making money. Do risk control well, always first priority.

## 13. ⚠️ Risk Reminder Again

Important things say three times: **Risk control! Risk control! Risk control!**

This strategy although already very conservative, but doesn't mean no risks.

**First risk, parameter adjustment risk**. Strategy has hundreds of parameters, each one can affect performance. If you're not sure what you're doing, absolutely don't randomly change parameters. Default values are author optimized, usually safest choice.

**Second risk, overtrading risk**. Strategy has many entry conditions, might generate many trading signals. Trading too frequently not only increases fees, might also because fees erode profits lead to losses. Appropriate times can disable some entry conditions, reduce trading frequency.

**Third risk, market environment change risk**. This strategy designed for oscillating markets and rebound markets, if market enters continuous one-sided markets, strategy's performance might worsen. Regularly observe market environment, timely adjust strategy parameters or positions.

**Fourth risk, technical risk**. Strategy relies on real-time data analysis and auto execution, if encounter network problems, server crash, software bugs, etc., might lead to losses. Suggest regularly backup configs, check logs, if conditions permit do some paper trading tests.

**Fifth risk, psychological risk**. Most dangerous not strategy itself, but yourself. Can't help manually closing positions when seeing continuous losses, can't bear to sell when seeing big rises — these human weakness scarier than any strategy defects. Strictly execute strategy rules, don't be swayed by emotions.

**Sixth risk, liquidity risk**. If trading coins liquidity not good, might appear want to sell can't sell situations. Suggest only trade major coins, don't touch those can't trade several a day coins.

Remember, in crypto circle, **surviving more important than anything**. Rather earn less, don't big lose. This strategy's design philosophy is exactly this logic.
