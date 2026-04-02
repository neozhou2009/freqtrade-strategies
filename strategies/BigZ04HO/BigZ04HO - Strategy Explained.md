# BigZ04HO: A "Buy Low Sell Fast" Strategy

> **Nickname**: Bargain Hunter Expert  
> **Profession**: Quant world's "play safe" type — take profits and run, never linger  
> **Timeframe**: 5 minutes + 1 hour

---

## 1. What's This Thing?

BigZ04HO is a trading strategy developed by a guru named ilya, it's the 4th version of the BigZ series. HO means HyperOpt optimized, equivalent to "upgraded enhanced version."

Simply put, this strategy's gameplay is: **specializes in finds coins that dropped too much, waits for them to rebound a bit then runs**. It's not that chase-rise-sell-drop gameplay, but like a "bargain hunter expert", specializes in goes in when prices drop to cheap levels, then sells very quickly.

This strategy's core thinking comes down to eight characters: **surviving is more important than making money**. So it sets up layer after layer of protection measures, afraid you'll lose big.

---

## 2. Core Settings

**Timeframe:**
- Main battlefield: 5-minute candles (check every 5 minutes for opportunities)
- Auxiliary information: 1-hour candles (used to judge big direction)

**Stoploss Take-Profit:**
- Stoploss: -99% (basically disabled traditional stoploss, relies on custom one)
- Trailing stop: Enabled, after profit exceeds 1%, automatically runs if pullback 2.5% from highest point
- Fixed ROI: 4 levels, 2.8% within 10 minutes, 1.8% within 40 minutes, 0.5% within 3 hours, returns to 1.8% after 3 hours

**Other Settings:**
- Suggest playing 2-4 trading pairs simultaneously, don't bet all money on one coin
- Needs at least 200 historical candles to start working
- Order types all use market orders, ensuring quick execution

---

## 3. 14 Entry Conditions

This strategy has **14 different** entry methods, basically playing "oversold rebound" to the extreme.

### Condition 0: RSI Oversold Rebound
- Closing price above 200-day moving average (big direction is bull market)
- 5-minute RSI below 30 (short-term oversold)
- 1-hour RSI also relatively low
- Volume contracting (can't sell anymore, about to rebound)

### Condition 1: Bollinger Band Lower Rail Rebound
- Price above both 200-day and 1-hour moving averages
- Closing price near Bollinger Band lower rail
- 1-hour RSI below 69
- Volume shows contraction pattern

### Condition 2: Bollinger Band Lower Rail Safe Buy
- Similar to condition 1, but doesn't force 1-hour RSI requirement
- Just needs price near Bollinger Band lower rail + volume contraction to trigger
- Easier to trigger

### Condition 3: Double Oversold
- 1-hour trend upward, but 5-minute already dropped below Bollinger Band
- 5-minute RSI especially low
- This is "big direction is bull market, but short-term dropped too much" situation

### Condition 4: 1-Hour RSI Extremely Low
- 1-hour RSI below 20 (very oversold)
- 5-minute price dropped below Bollinger Band
- Volume contracting
- Simple and crude extreme oversold strategy

### Condition 5: MACD Golden Cross + Oversold
- MACD fast line above slow line (momentum turning strong)
- Closing price below Bollinger Band
- Volume contracting
- Plainly speaking "can't drop more, and people starting to buy"

### Condition 6: RSI+MACD Enhanced Version
- Similar to condition 5, but different parameters
- 1-hour RSI below 35.7
- Purpose is to catch opportunities in different market environments

### Condition 7: 1-Hour RSI+MACD Combo
- 1-hour RSI below 17.6 (more extreme oversold)
- MACD golden cross
- Volume contracting

### Condition 8: Dual RSI Oversold
- 1-hour RSI + 5-minute RSI both very low
- Volume contracting
- Both timeframes oversold, signals more reliable

### Condition 9: Dual RSI+Volume Contraction Plus
- 1-hour RSI below 36, 5-minute RSI below 10
- Volume conditions stricter
- Multiple insurance, improving signal quality

### Condition 10: 1-Hour Level Oversold Rebound
- 1-hour RSI very low
- 1-hour candles still below Bollinger Band
- MACD histogram starts turning positive
- 5-minute RSI also oversold
- Catching big level rebound opportunities

### Condition 11: Trend Confirmation Rebound
- MACD positive for 5 consecutive candles (continuous upward momentum)
- Bollinger Band narrowing (about to breakout)
- Closing price breaks above Bollinger Band middle rail
- RSI above 51 (bullish state)
- Belongs to relatively advanced consolidation breakout pattern

### Condition 12: False Breakout Reversal
- Price briefly drops below Bollinger Band lower rail then recovers
- Previous candle still above lower rail
- 1-hour RSI also can't be too high
- Volume contracting
- This catches "false breakout then reversal" opportunities

---

## 4. Protection Mechanisms

This strategy's protection mechanisms are basically "cowardly" to the extreme, total three layers of protection:

**First Layer: Fixed ROI**
- 0-10 minutes: Run at 2.8%
- 10-40 minutes: Run at 1.8%
- 40-180 minutes: Run at 0.5% (even tiny profits run)
- Over 3 hours: Returns to 1.8%
- Core thinking: **Don't be greedy, fast in fast out**

**Second Layer: Trailing Stop**
- Starts recording highest price after profit exceeds 1%
- Automatically runs if falls 2.5% from highest point
- This way can eat most of the gains, but won't ride the roller coaster

**Third Layer: Custom Stoploss**
- This is the core protection!
- If position still losing money after 50 minutes:
  - If 1-hour RSI still below 30, continue holding waiting for rebound
  - If price drops below opening price over 1.5%, directly stoploss 1%
- Simply put: **Don't stubbornly hold when losing, run when you should run**

---

## 5. Exit Logic

This strategy's exits mainly rely on three things:

**1. Fixed ROI**: Run when reaching the point, don't care if it rises more later

**2. Trailing Stop**: Run if pullback 2.5% from high point after profiting

**3. Exit Signal**: Sell when closing price exceeds 1.01 times Bollinger Band middle rail

Plainly speaking, this strategy's exit logic is: **Don't be greedy, run when reaching the point**. It's not like some strategies that wait to make big money before leaving, BigZ04HO's philosophy is accumulate little by little, accumulating returns through multiple small profits.

---

## 6. This Strategy's "Personality Traits"

If the strategy were compared to a person, BigZ04HO probably has this kind of personality:

**Trait 1: Scared of Death**
- Set up layers of protection, wants to run at the slightest wind or movement
- Starts panicking after losing money for over 50 minutes, wants to stoploss

**Trait 2: Not Greedy**
- Wants to run at 2.8% profit, absolutely doesn't linger
- Rather earn less to protect principal

**Trait 3: specializes in Picks Soft Persimmons**
- Only buys oversold coins
- Doesn't chase rises, doesn't do trend breakouts

**Trait 4: Flexible**
- 14 entry methods, there's always one suitable for current market
- Can play in bull markets, can also play in oscillating markets

**Trait 5: Impatient**
- Wants results within 10 minutes
- Must have conclusion within 3 hours

---

## 7. Suitable Scenarios

**Most Suitable:**
- Oscillating markets: Prices jump up and down,provides entry opportunities for strategy
- Bull market pullbacks: Rose too much then drops a bit, strategy goes in to catch, runs after rebound
- Sideways consolidation: Prices fluctuate within range, strategy repeatedly captures opportunities

**Not Very Suitable:**
- Strong downtrends: Keeps dropping keeps dropping, strategy may have continuous stoploss
- Strong uptrends: Rises right after buying, but strategy runs very quickly, misses big rises
- Too low volatility: No volatility means no opportunities, strategy can't find entry timing

---

## 8. Market Performance

**In Oscillating Markets:**
- Performs best, can repeatedly capture oversold rebound opportunities
- Each time earns 1%-3%, accumulate little by little
- Success rate relatively high

**In Bull Markets:**
- Performs well, can catch opportunities during pullbacks
- But may sell too early, miss some gains
- Overall still positive returns

**In Bear Markets:**
- Performs poorly, possibility of consecutive losses increases
- Needs to rely on custom stoploss to control losses
- Suggest reducing position quantity

---

## 9. Configuration Suggestions

**Basic Configuration:**
- Hold 2-4 trading pairs simultaneously
- Each investment accounts for 10%-20% of total funds
- Use USDT asquote currency

**Risk Control:**
- Set total position limit, like maximum 4 simultaneously
- Set daily loss limit, like pause if lose 5%
- Regularly check strategy performance

**Live Trading Suggestions:**
- Run paper trading for a while first
- Familiarize with strategy's operation logic
- Understand under what circumstances strategy will stoploss

---

## 10. Easter Eggs

**Secret 1: Author's Suggestions**
- Author says most suitable for 2-4 simultaneous positions
- Works best with unlimited stake mode
- Suggests using VolumePairlist to select trading pairs

**Secret 2: Truth About exit_profit_only**
- When set to True, only sells when profitable
- Higher risk this way, but potential returns also higher
- When set to False (default), drawdown lower, but returns also 10%-15% less

**Secret 3: Truth About stoploss**
- -99% doesn't really mean stoploss at 99% loss
- It actually disables default stoploss, enables custom stoploss
- Custom stoploss will stoploss around 1% based on market conditions

---

## 11. Final Key Points

Using this strategy, there are several points to keep in mind:

1. **It's not a get-rich-quick strategy**: Only earns 1%-3% each time, needs to accumulate little by little
2. **It will stoploss**: Don't feel bad when losing money, must stoploss when you should
3. **It needs patience**: Although trades frequently, needs to wait for suitable entry opportunities
4. **It fears extreme markets**: Be careful monitoring during continuous spike up crash down
5. **It needs 200 candles**: New coins or new pairs may not be usable

Remember this strategy's core thinking: **Surviving is more important than making money, rather earn less than lose big**.

---

## 12. One Sentence Summary

BigZ04HO is a **"fast in fast out, accumulate little by little"** strategy.

**Core Selling Point**: Lose little, live long  
**Disadvantages**: Doesn't earn enough in bull markets, complex parameters

**Suitable For**: Risk-averse investors, traders who like short-term trading

---

## 13. ⚠️ Risk Reminder Again

Say it again, although this strategy designed multi-layer protection, risks still exist:

**Biggest Risks:**
- May have consecutive losses in continuous downtrends
- May trigger larger losses in extreme situations
- Fixed stoploss disabled, completely relies on custom stoploss

**Other Risks:**
- Improper parameter settings may cause strategy failure
- Market environment changes may cause strategy performance decline
- Needs continuous monitoring and adjustment

**Suggestions:**
- Never invest more than you can afford to lose
- Fully test on paper trading first
- Be mentally prepared to accept strategy's normal losses
- Regularly review strategy performance

Crypto has risks, enter market需cautiously。BigZ04HO can help you control risks, but can't eliminate risks. Let's encourage each other!
