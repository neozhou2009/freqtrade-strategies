# PRICEFOLLOWINGX Strategy Explained

## 1. What Does This Strategy Do?

PRICEFOLLOWINGX—the name sounds fancy, but it's basically a "follow the price" strategy. What does that mean? When prices form a clear uptrend, it follows along and buys in; when the trend looks bad, it sells quickly and runs.

The core feature of this strategy: **it uses an improved RSI indicator**. You probably know regular RSI—it tells you if the market is overbought or oversold. But regular RSI has a problem: when it reaches extreme values, it kind of gets stuck there and doesn't move much. The Fisher Transform RSI used in this strategy is like adding lubricant to RSI—it's more responsive in extreme zones.

The timeframe is 15 minutes, so it's medium frequency. Not the super-fast kind that trades every few seconds, and not the kind that holds for days. Good for people who want to profit from intraday swings.

## 2. What Tools Does This Strategy Use?

### Fisher Transform RSI (frsi)

This is the biggest highlight of this strategy. Regular RSI goes from 0 to 100—below 30 is oversold, above 70 is overbought. But here's the thing: when the market goes crazy, RSI can stay overbought for a long time and just won't come down.

Fisher Transform RSI does a mathematical transformation on RSI, making the range -1 to 1. It's like "stretching" RSI so extreme values become more obvious. This way, when the market truly hits extreme states, the signal is clearer.

**Buy threshold**: Default -0.40 (equivalent to regular RSI around 35)
**Sell threshold**: Default 0.20 (equivalent to regular RSI around 60)

### TEMA (Triple Exponential Moving Average)

TEMA is "triple" EMA—through three rounds of smoothing to reduce lag. Regular moving averages have delay—price goes up for a while before the average catches on. TEMA solves this problem with faster response.

This strategy uses 7-period TEMA, which is very short, so it reacts quickly. But it's also sensitive and can be noisy.

### Bollinger Bands

Bollinger Bands are three lines: upper band, middle band, lower band. When price drops near the lower band, it usually bounces; when it rises near the upper band, it usually pulls back.

The strategy uses 19-period, 2.2x standard deviation Bollinger Bands—slightly tighter than the standard 20-period, 2x standard deviation.

### Heikin Ashi Smoothed Candles

This is a special way of drawing candlesticks—averaging prices to make them look smoother. Green candles mean up, red candles mean down, easy to read.

### EMA Moving Averages

The strategy uses two key moving averages:
- **emalow**: 12-period EMA, calculated using low prices
- **emahigh**: 14-period EMA, calculated using high prices
- **ema7**: Actually a 14-period SMA, used to judge main trend

### Other Indicators

There's also ADX (judges trend strength), MACD (judges trend direction), but these two are more for auxiliary reference in the strategy.

## 3. What's the Core Thinking Behind This Strategy?

The strategy's logic can be summarized as: **find opportunities to buy in oversold zones, sell when the trend weakens**.

### Buy Logic

The strategy has two buy modes you can switch between:

**Mode One (RSI Enabled)**:
1. Fisher RSI crosses below -0.40 from above, meaning it's entered oversold territory
2. TEMA drops below the Bollinger Band lower band, price is really low
3. TEMA crossed below the emalow moving average, short-term pullback is in place

All three conditions must be met together. It doesn't buy on just a small dip—it waits for a real drop.

**Mode Two (RSI Disabled)**:
1. TEMA rises above the Bollinger Band middle band, price is starting to strengthen
2. TEMA crosses above ema7 moving average, trend confirmed upward

This mode catches trend initiation, not bottom fishing.

### Sell Logic

There are two corresponding sell modes:

**Mode One (RSI Enabled)**:
1. Fisher RSI crosses below 0.20 from above, momentum starting to fade
2. TEMA drops below the Bollinger Band middle band
3. TEMA crosses below ema7 moving average

Note: Selling uses Fisher RSI crossing down, not up. This means when it starts dropping from highs, get alert—even if it's not truly oversold yet.

**Mode Two (RSI Disabled)**:
1. TEMA below the Bollinger Band middle band
2. TEMA crosses below ema7 moving average

Simple and direct.

### Trailing Stop

The strategy has a very practical feature: **trailing stop**.

Here's the setup:
- After profit reaches 3%, trailing stop activates
- The stop line follows the price, keeping a 2% distance
- If price retraces more than 2% from the highest point, it automatically sells

The benefit of this mechanism: when going up, it follows; when dropping, it locks in your profit. For example, if you buy and it goes up 10%, without trailing stop it might drop back down and you'd gain nothing. With trailing stop, if it goes up 10% and drops 2%, it sells—you still keep 8% profit.

## 4. How Does This Strategy Decide When to Buy?

### RSI Enabled Mode Buy Conditions

Let's break down this combination:

**Condition 1: Fisher RSI Crosses Below Threshold**

Fisher RSI normally oscillates between -0.4 and 0.4. When it drops below -0.4, it means the market is panicking, price has dropped too much. This is a bottom-fishing signal, but this one condition alone isn't enough.

**Condition 2: TEMA Below Bollinger Band Lower Band**

The Bollinger Band lower band is like the floor. TEMA dropping below the floor means price is truly oversold, not just normal fluctuation. This second condition confirms the strength of the oversold condition.

**Condition 3: TEMA Crosses Below emalow**

emalow is a moving average calculated from low prices—basically a support line. TEMA breaking below this support means the pullback is truly in place, not just starting to drop.

**Connecting the three conditions**:
Market is panicking (Fisher RSI low) → Price broke below the floor (TEMA < BB lower band) → Support also broke (TEMA < emalow)

Buying at this point is like buying against the crowd when everyone is panicking. Of course, the premise is that the major trend isn't broken—it's just a short-term pullback.

### RSI Disabled Mode Buy Conditions

This mode is simpler:

**Condition 1: TEMA Above Bollinger Band Middle Band**

The Bollinger Band middle band is just a moving average. Price standing above the average means short-term trend is starting to go up.

**Condition 2: TEMA Crosses Above ema7**

ema7 is the main trend line. TEMA crossing above confirms trend reversal upward.

**Connecting the two conditions**:
Price stands above the average → Trend line also broke through

This is a right-side trading approach: wait for the trend to emerge before chasing. The benefit is not catching falling knives and not getting trapped in downtrends; the downside is potentially buying near the high.

## 5. When to Sell?

### RSI Enabled Mode Sell Conditions

**Condition 1: Fisher RSI Crosses Below 0.20**

Note it's crossing down, not up. Why? Because Fisher RSI dropping from highs means upward momentum is weakening. No need to wait until truly overbought (like 0.8) to sell—that might be too late.

**Condition 2: TEMA Below Bollinger Band Middle Band**

Price dropping below the average from above, trend starting to weaken.

**Condition 3: TEMA Crosses Below ema7**

Short-term trend line crossing below main trend line confirms trend reversal.

**Connecting the three conditions**:
Momentum fading (Fisher RSI crossing down) → Price dropped below average → Trend line also broke

Selling at this point is exiting when the trend just starts to go bad, preserving profit.

### RSI Disabled Mode Sell Conditions

Pretty similar to enabled mode, just without the Fisher RSI condition:

1. TEMA below Bollinger Band middle band
2. TEMA crosses below ema7

Simple and direct.

### Trailing Stop Auto-Sell

If price keeps going up and triggers trailing stop, then drops 2%, it will also auto-sell. This is the final safety net.

## 6. What Safety Mechanisms Does This Strategy Have?

### Fixed Stop Loss

Stop loss is set at -10%, meaning if price drops 10% after buying, it auto-sells. This stop loss is fairly wide, suitable for trend trading. If the stop loss is too tight, normal fluctuations will shake you out.

### Triple Protection Mechanism

The strategy has three layers of insurance:

**1. MaxDrawdown Protection**
- Within the past 12 hours, if 5 trades produced drawdown over 75%, pause trading
- Prevents continuing to trade during consecutive losses

**2. StoplossGuard Protection**
- Within the past 6 hours, if a coin triggers stop loss 3 times, pause that coin's trading
- Prevents getting repeatedly slapped by the same coin

**3. LowProfitPairs Protection**
- Within the past 7.5 hours, if 2 trades of a coin both make less than 0.5% profit, pause it
- Filters out those coins that "just don't make money no matter what"

### Trailing Stop

As mentioned earlier, activates after 3% profit, sells on 2% pullback. This is dynamic, more flexible than fixed take-profit.

## 7. How to Use This Strategy?

### Basic Configuration

Timeframe: 15 minutes (must use 15 minutes, don't change to 5 minutes or 1 hour, parameters won't match)

Stop loss: -10%
Trailing stop: Enabled

### How to Choose Between the Two Modes?

**RSI Enabled Mode**:
- Good for ranging-to-upward markets
- Looking for pullback buying opportunities
- Fewer signals but more precise

**RSI Disabled Mode**:
- Good for clear trending markets
- Chasing momentum, not bottom fishing
- More signals but might buy near highs

### How to Adjust Parameters?

You can tune through Hyperopt (hyperparameter optimization):

- **buy_frsi**: Fisher RSI threshold when buying, default -0.40
  - Lower it (like -0.60): more aggressive, buy earlier, but might catch falling knife
  - Raise it (like -0.20): more conservative, wait for real drop, but might miss opportunities

- **sell_frsi**: Fisher RSI threshold when selling, default 0.20
  - Lower it: sell earlier, preserve profit but might miss gains
  - Raise it: let profits run more, but bigger pullback risk

### Recommended Coins and Times

- Focus on major coins: BTC, ETH with good liquidity
- Avoid small coins: easily manipulated, stop loss might not even help
- Run 24/7: crypto trades 24 hours, strategy should run 24 hours too

## 8. What Are the Risks?

### Trending Market Risk

This is a trend strategy, most afraid of sideways chop. Price bouncing around inside Bollinger Bands, TEMA going up and down—might get repeatedly chopped and stopped out.

### Stop Loss Risk

10% stop loss is pretty wide. If there's a flash crash, it might drop past stop loss before it can trigger. Especially with low-liquidity small coins.

### Parameter Overfitting Risk

The strategy has several tunable parameters. If tuned too precisely, backtesting data might look great but live trading could be completely different. This is called "overfitting"—treating historical noise as patterns.

### Slippage Risk

Using limit orders can reduce slippage, but if market is volatile, limit orders might not fill. Using market orders might have big slippage.

### Mode Switching Risk

The two buy modes (RSI enabled/disabled) suit different markets. If the market changes but you're still using the wrong mode, results will be poor.

## 9. How Does This Compare to Other Strategies?

### Advantages

1. **Fisher RSI improvement is clear**: Really more responsive than regular RSI, especially near extreme values
2. **Complete protection mechanisms**: Triple protection plus trailing stop, risk control is solid
3. **Adjustable parameters**: Can tune based on market, not a rigid strategy
4. **Clear logic**: Buy and sell conditions are clear, not a black box

### Disadvantages

1. **Few buy conditions**: Only one set of buy logic, covers limited scenarios
2. **No volume confirmation**: Doesn't check volume, signal reliability is discounted
3. **No multi-timeframe verification**: Only looks at 15 minutes, doesn't use larger timeframes to confirm trend
4. **Choppy market vulnerability**: Might get repeatedly stopped out during sideways

### Who Is It For?

- Some experience, can judge if market is trending or ranging
- Can accept medium-frequency trading (possibly a few trades per day)
- Willing to spend time tuning parameters, checking results

Not for complete beginners, because you need to judge when to use which mode, and periodically tune parameters.

## 10. Practical Suggestions

### Backtest Before Live Trading

Don't jump in with real money. Backtest with at least 3 months of historical data to see how the strategy performs. If backtesting loses money, live trading will definitely be worse.

### Start with Small Positions

Initially use 10%-20% of total capital, confirm the strategy works before adding more. Don't go all-in from the start.

### Watch the Big Trend

Although the strategy only looks at 15 minutes, you should check daily charts to judge the big trend. Strategy works better when big trend is up; when big trend is down, better to stay in cash.

### Periodically Check Performance

Check strategy performance weekly, look at both winning and losing trades. If losing consecutively, maybe market conditions changed—need to adjust parameters or pause the strategy.

### Set Alerts

Set a few key alerts:
- Daily loss over 5%
- Single trade loss over 8%
- Position held over 4 hours without selling

These anomalies need human intervention to check.

## 11. Who Is This Strategy For?

**Suitable for**:
- Some trading experience, understand technical analysis basics
- Can accept medium-frequency trading
- Have time to monitor strategy performance
- Medium risk tolerance

**Not suitable for**:
- Complete beginners (learn basics first)
- Wanting to make passive income (strategy needs monitoring and parameter tuning)
- Can't handle any losses (no strategy is guaranteed profit)
- Only doing long-term investing (this strategy holds for hours to days)

## 12. Final Summary

PRICEFOLLOWINGX is a trend-following strategy with Fisher Transform RSI at its core.

**Core Features**:
- Fisher RSI improves traditional RSI, more sensitive in extreme zones
- TEMA fast response, reduces lag
- Multiple protection mechanisms control risk
- Trailing stop lets profits run

**Main Logic**:
- Buy: Find opportunities in oversold zones (Fisher RSI low, TEMA below Bollinger Band lower band)
- Sell: Exit when trend weakens (Fisher RSI crossing down, TEMA below moving average)

**Usage Suggestions**:
1. Backtest first to verify effectiveness
2. Small position live testing
3. Adjust parameters based on market
4. Regularly check and optimize

This strategy's tool design is good, but buy conditions are relatively limited. Recommend combining with volume indicators and larger timeframe trend judgment for better results.

## 13. ⚠️ Risk Reminder

1. **Trend strategies hate chop**: If the market is going sideways, this strategy will struggle, possibly getting repeatedly chopped. Better to pause or switch strategies in ranging markets.

2. **10% stop loss is not small**: If you unfortunately hit stop loss, a single trade loses 10%. Lose a few in a row and your capital shrinks significantly. Recommend controlling position size, don't go heavy on one coin.

3. **Parameter tuning has traps**: Don't go too aggressive with Hyperopt. Perfect historical performance doesn't equal future profits. Recommend using Walk-Forward validation.

4. **No universal strategy**: Even the best strategy fails sometimes. When market conditions change, strategy might stop working. Keep observing, stop when needed.

5. **Black swan events**: In extreme markets, no technical indicators work. Stop loss might have slippage, exchange might go down. Never go all-in, always have a backup plan.

Quantitative trading is not a money printer—it's a tool. Used well, it helps you execute discipline and avoid emotional trading; used poorly, it might be worse than manual trading. Continuous learning, ongoing optimization, and risk control are the keys to long-term stable profits.