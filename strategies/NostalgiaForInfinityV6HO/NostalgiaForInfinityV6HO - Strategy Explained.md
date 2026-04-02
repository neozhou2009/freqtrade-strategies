# NostalgiaForInfinityV6HO — Strategy Explained (Plain English)

## Chapter 1: What Is This Strategy?

### 1.1 One-Line Description

NostalgiaForInfinityV6HO is a crypto automated trading strategy that runs on Freqtrade. In simple terms: it lets your computer buy and sell crypto for you automatically.

### 1.2 Who Built It?

This strategy was built by a team called **iterativ**. They've released several versions, and V6HO is the sixth-generation optimized version — "HO" stands for **Hyper-Optimized**.

### 1.3 How to Use It?

The developers recommend:
- Watch 40–80 coins simultaneously
- Hold 4–6 positions at once
- Use USDT (or stable coins) for quoting — NOT BTC or ETH
- Avoid leveraged tokens: BULL, BEAR, UP, DOWN, etc.
- Timeframe must be **5 minutes**

### 1.4 How Much Can It Make?

No guarantees on that front. But the developers publicly share their BTC and ETH wallet addresses for donations. The code says "never will ask for donations, but as a symbol of appreciation will accept them." That says something about the developers' confidence in this strategy.

---

## Chapter 2: What's the Core Idea?

### 2.1 Main Logic

The core idea is: **When the trend is up, buy on pullbacks, then sell at the right price.**

Sounds simple, right? But the hard parts are: How do you know the trend is up? How do you know the pullback is done? How do you know when to sell?

This strategy uses very complex methods to solve these problems.

### 2.2 Two "Umbrellas"

The cleverest part: two "umbrellas" that prevent you from buying at the wrong time.

**Umbrella #1: Don't Chase High**
If you're looking at a coin that has risen too much recently, the strategy blocks your buy. Because it judges the price will likely pull back — buying now risks getting trapped.

It checks how much the coin rose in the past 24, 36, and 48 hours. Too much gain? Skip it, wait for a pullback.

**Umbrella #2: Don't Catch a Falling Knife**
If you see a coin that's dropped a lot and want to bottom-fish, the strategy also checks. It looks at how badly the coin has dropped recently. If it's dropped too much, it might drop more — so it won't let you buy.

### 2.3 Multi-Confirmation

The strategy doesn't let you buy on just one signal. It requires multiple conditions to be met simultaneously:

1. Big trend must be right (judged by 200-day MA)
2. Small trend must show a buy signal (judged by RSI, Bollinger Bands, etc.)
3. No risk of chasing high or catching a falling knife (umbrella checks)

Only when all three conditions are met does it trigger a buy.

---

## Chapter 3: What Indicators Does the Strategy Use?

### 3.1 Moving Averages

The strategy uses several types:

- **EMA (Exponential Moving Average)**: Gives more weight to recent prices, responds faster
- **SMA (Simple Moving Average)**: Treats all prices equally, smoother

Key periods: 12, 20, 26, 50, 100, 200. The 200-period is for judging the big trend.

### 3.2 RSI Indicator

RSI is the Relative Strength Index — tells you if something is overbought or oversold.

- RSI above 70: Too bought, might drop
- RSI below 30: Too sold, might rise

The strategy uses 14-period RSI and watches BOTH 5-minute AND 1-hour timeframes.

### 3.3 Bollinger Bands

Bollinger Bands use MAs +/- a multiple of standard deviation to form a channel.

- Price near the lower band: Relatively cheap, potential buy opportunity
- Price near the upper band: Relatively expensive, potential sell opportunity

### 3.4 MFI Indicator

MFI is the Money Flow Index — combines price and volume.

Simple understanding: Price down + volume up = funds flowing out; Price up + volume up = funds flowing in.

### 3.5 Other Indicators

- **EWO (Elliott Wave Oscillator)**: Judges wave positions in Elliot Wave theory
- **CMF (Chaikin Money Flow)**: Another fund flow indicator
- **Choppiness Index**: Tells whether the market is trending or choppy

---

## Chapter 4: What Are the Buy Conditions?

### 4.1 24 Buy Conditions in Total

The most complex part: the strategy defines 24 different buy conditions. Each condition is a complete set of logic — buy if ANY one of them triggers.

Why so many? Because markets change all the time. A single condition can't handle all situations. More conditions = more nets cast = more chances of catching opportunities.

### 4.2 Condition #1 (Most Comprehensive)

Condition 1 uses the most protection measures:

**Setup**:
- 200-day MA is rising (big trend is up)
- Close price above 200-day MA
- No recent wild swings

**Trigger Signals**:
- Past 36 candles' minimum has risen more than 2.2% (some upward momentum)
- 1h RSI between 30 and 84 (not too cold, not too hot)
- 5m RSI below 36 (short-term oversold)
- MFI below 36 (fund outflow has reached a certain level)

This condition is relatively conservative — maximum protection.

### 4.3 Condition #2 (Catch the Oversold)

Condition 2 specifically catches short-term oversold situations:

**Trigger Signals**:
- 5m RSI is 39+ points below 1h RSI (short-term dropped way more)
- Close price below 98.3% of Bollinger lower band
- MFI below 49

This condition uses fewer protections — suitable for aggressive buying when the trend is clear.

### 4.4 Condition #3 (Bollinger Band Breakout)

Condition 3 uses 40-period Bollinger Bands:

**Trigger Signals**:
- Bollinger Band width > 5.7% of close (volatility amplified)
- Close price change > 2.3% (momentum building)
- Lower wick not too long (avoiding false breakouts)
- Close breaks below previous candle's BB lower band
- But close doesn't exceed previous close (buying in the pullback)

### 4.5 Golden Cross Buy Conditions

Conditions 5, 6, 7, 14, 15 all use the EMA golden cross concept.

What is a golden cross? When the short MA crosses above the long MA — usually seen as a bullish signal.

Requirements:
- EMA26 is above EMA12 (bearish alignment)
- Gap between the two lines is big enough (not a false signal)
- Close price below BB lower band

This is a strategy to buy in trend pullbacks.

### 4.6 Wave Theory Buy Conditions

Conditions 12, 13, 16, 17 use the EWO indicator.

**Buy 12**: EWO > 1.8, RSI < 30 — indicates an upswing wave pullback stage.

**Buy 13**: EWO < -11.8 — indicates the downward wave is almost ending, might bounce.

### 4.7 Extreme RSI Buy Conditions

Conditions 20 and 21 specifically catch extreme situations:

**Condition 20**: 5m RSI < 27, 1h RSI < 20
**Condition 21**: 5m RSI < 23, 1h RSI < 24

These are oversold bounce opportunities, but risk is also higher.

---

## Chapter 5: What Are the Sell Conditions?

### 5.1 Two Sell Systems

The strategy has two paths to sell:

**Path 1: Technical Indicator Sell**
Traditional sell method based on technical indicators.

**Path 2: Profit Target Sell**
This is the essence of the strategy. It dynamically adjusts sell conditions based on how much you've made. More profit = more aggressive about selling; less profit = wait longer.

### 5.2 Technical Indicator Sells

**Sell 1**: RSI > 79.5, AND 6 consecutive candles are above the BB upper band.
"Clearly risen too much, time to sell."

**Sell 2**: RSI > 81, AND 3 consecutive candles above BB upper band.
"Earlier signal than Sell 1, suitable for quick profit-taking."

**Sell 3**: RSI > 82
"Simple and direct — overbought means sell."

**Sell 4**: 5m RSI > 73.4 AND 1h RSI > 79.6
"Both timeframes overbought — stronger confirmation signal."

**Sell 7**: 1h RSI > 81.7, AND EMA12 crosses below EMA26
"Overbought + death cross — classic trend reversal."

**Sell 8**: Close price exceeds 1h BB upper band by 1.1×
"Price massively broke through the volatility channel — take profit."

### 5.3 Profit Target Sell (The Core Part)

This is the most brilliant design in this strategy. The strategy defines multiple profit tiers:

**Normal conditions**:
- If profit > 20%, sell when RSI drops below 34
- If profit is 12%–20%, sell when RSI drops below 42
- If profit is 10%–12%, sell when RSI drops below 50
- If profit is 9%–10%, sell when RSI drops below 54
- And so on...

This design is smart: the more you've made, the lower the sell threshold. If you've already made 20%, even if RSI is only at 34 (still relatively low), sell and lock in profits. If you've only made 1%, wait until RSI crosses a certain value before selling.

**When price is below the 200-day MA**:
If the price is below the 200-day MA, the overall trend might not be great. The strategy uses a more aggressive set of sell parameters — if you're making money, take it and run.

**When a coin recently surged**:
If a coin has surged in the past 24, 36, or 48 hours, the strategy judges it's volatile and uses dedicated sell parameters. These are usually more aggressive, because surging coins often drop hard too.

### 5.4 Trailing Stop

The strategy implements trailing stop:

**Trailing Stop 1**: Profit is 16%–60%, RSI is between 20–50, AND the highest profit exceeds current profit by more than 3%.

Example: You peaked at 20% profit, now pulled back to 16% (dropped 4%). If 4% > 3% (the trailing threshold), it triggers a sell. This lets profits run but also secures them.

---

## Chapter 6: How Do the Protection Mechanisms Work?

### 6.1 Three Safe Pullback Checks

The strategy checks recent price action to see if it's dropped too badly:

**Normal mode**:
- Current candle's drop ≤ 2%
- Last 2 candles' max drop ≤ 14%
- Last 12 candles' max drop ≤ 32%
- Last 144 candles' (12 hours) max drop ≤ 50%

If all these are satisfied, the decline is controllable — consider buying.

**Strict mode**: Thresholds are tighter, suitable for volatile markets.

**Loose mode**: Thresholds are looser, suitable for aggressive buying when the trend is clear.

### 6.2 Three Safe Surge Checks

Similarly, the strategy checks if something has surged too much recently:

**Check logic**:
1. Has the rise in the past 24/36/48 hours been too big?
2. Is the price too close to its high point?

If the rise is too big AND the price is still near its high, the strategy judges the risk is too high and won't let you buy.

### 6.3 Trend Confirmation

Beyond the two umbrellas, the strategy also confirms trend direction:

**200-day MA check**: If the 200-day MA is rising, the big trend is up — buying is safer.

**Price position check**: If the close price is above the 200-day MA, the price is in an uptrend.

---

## Chapter 7: How to Optimize Parameters?

### 7.1 How Many Parameters Does This Strategy Have?

**Over 200!** Does that scare you?

These include:
- On/off switches for the 24 buy conditions
- Protection mechanism parameters for each buy condition
- Thresholds for various technical indicators
- Sell condition parameters
- Layered profit target parameters

### 7.2 Do You Need to Optimize All of Them?

**No.** The strategy already provides default values — these defaults were optimized by the developers.

You can:
1. Only optimize the parameters you think are important
2. Use Freqtrade's hyper-optimization feature to auto-optimize
3. Keep defaults and test first to see the results

### 7.3 What to Watch Out for When Optimizing?

**Don't over-optimize**: If you tune parameters to match past data too perfectly, it might not work in the future. This is called "overfitting."

**Use enough data**: Test with at least one year of historical data.

**Watch for stability**: Don't let optimized parameters deviate too much from defaults — extreme values are often a signal of overfitting.

---

## Chapter 8: Live Trading Tips

### 8.1 Config File Settings

Key settings in the Freqtrade config file:
```
"timeframe": "5m"                    # Must be 5 minutes
"use_sell_signal": true              # Must be on
"sell_profit_only": false            # Must be off
"ignore_roi_if_buy_signal": true    # Must be on
```

Wrong these settings, the strategy won't work properly.

### 8.2 How to Select Trading Pairs?

**Recommended**:
- Choose mainstream coins with good liquidity
- Use USDT-quoted trading pairs
- 40–80 trading pairs

**Not recommended**:
- Leveraged tokens (BULL, BEAR, etc.)
- Newly listed coins (less than 30 days)
- Low-liquidity coins

### 8.3 How to Allocate Capital?

Official recommendations:
- Maximum 4–6 positions at once
- Equal amount per position
- Or use dynamic position sizing

### 8.4 How to Set Stop Loss?

The strategy has a fixed -10% stop loss and also trailing stop.

The trailing stop activates after profit reaches 3%, with a 1% trailing distance.

---

## Chapter 9: Strategy Pros & Cons

### ✅ Pros

**Pro 1: Comprehensive Coverage**
24 buy conditions — no matter the market, at least one fits the current situation. It's not about buying or selling on just one signal.

**Pro 2: Solid Protections**
Chase protection, bottom-fish protection, trend confirmation — three layers of insurance prevent you from making big mistakes.

**Pro 3: Scientific Profit Management**
Layered profit targets are smart. The more you make, the more aggressively you take profits — won't let gains evaporate.

**Pro 4: Highly Adjustable**
Each condition can be independently switched on/off. Each parameter can be optimized. Customize based on your needs.

### ⚠️ Cons

**Con 1: Extremely Complex**
200+ parameters — beginners will find it confusing. Wrong parameter tweak could cause problems.

**Con 2: High Computation**
Calculates many indicators. If you're watching dozens of trading pairs simultaneously, your computer might struggle.

**Con 3: Not a Magic Wand**
May not perform well in sideways choppy markets — it's better suited for trending markets.

**Con 4: Overfitting Risk**
Too many parameters, easy to overfit to historical data. Great backtest results don't guarantee future profits.

---

## Chapter 10: Q&A

### Q: Why are my buy signals so infrequent?

Possible reasons:
1. Market is choppy with no clear trend
2. Protection mechanisms blocked many signals
3. Not enough trading pairs

Solution: Check the market conditions, or consider loosening some buy condition thresholds.

### Q: Why does stop loss trigger so often?

Possible reasons:
1. Entry timing wasn't right — immediately got trapped
2. Stop loss set too tight
3. Market volatility too high

Solution: Check if entry conditions were too aggressive, or consider widening the stop distance.

### Q: How to know if the strategy is working properly?

Monitor:
- Trigger frequency of each buy condition
- Distribution of each sell signal
- Win rate and profit factor
- Difference from backtest results

If significantly different from backtest, may need to check configuration or adjust parameters.

### Q: Can it guarantee profits?

**No.** No strategy can guarantee profits. This strategy has been tested and optimized by many people and has some reliability, but markets change — past performance doesn't predict future results.

---

## Chapter 11: Summary

### 11.1 Core Principles Review

**Core idea**: Buy on pullbacks in an uptrend, sell with scientific profit management.

**Core protection**: Chase protection and bottom-fish protection — prevent buying at the wrong time.

**Core feature**: Layered profit targets — the more you make, the more aggressively you sell.

**Core complexity**: 24 buy conditions, 200+ parameters — need serious study and adjustment.

### 11.2 Usage Recommendations

1. Start with paper trading to get familiar with strategy behavior
2. Don't modify parameters blindly
3. Continuously monitor strategy performance
4. Maintain respect for the market

### 11.3 Final Thoughts

This strategy is not a "holy grail" — it won't make you rich while you sleep. But it's a well-designed tool. Used correctly, it can improve trading efficiency and scientific rigor.

Remember: Tools are only as good as the person using them. Keep learning, keep improving, and you'll survive in the markets long-term.

---

*This document explains the core logic of NostalgiaForInfinityV6HO in plain language.*

*Disclaimer: This document is for learning and exchange only, not investment advice. Crypto trading carries high risks — please make careful decisions.*
