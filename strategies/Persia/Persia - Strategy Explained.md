# Persia Strategy Explained

## 1. What Does This Strategy Do?

Persia sounds like a fancy name, but it's actually a super "flexible" strategy—so flexible that even what to buy and when to buy isn't fixed. It lets you find the optimal solution through hyperparameter optimization.

Think of it this way: regular strategies are like a fixed recipe—first add onions, then ginger, finally salt. Persia is like a "seasoning box" with all kinds of seasonings (indicators) that you can freely combine. Which combination tastes best? You have to try it yourself.

The core idea of this strategy: **let the machine find the optimal strategy for you**. You provide a bunch of parameter options, and Freqtrade's Hyperopt function will automatically search for which combination makes the most money.

## 2. What Tools Does This Strategy Use?

### Four Moving Averages

The strategy just uses four moving averages, all basic ones:

**SMA (Simple Moving Average)**
- Just adding up past N candlestick prices divided by N
- Like SMA-5, the average of past 5 candlestick prices
- Characteristic: stable, but slow to react

**EMA (Exponential Moving Average)**
- Gives recent prices higher weight
- Today's price matters most, yesterday's less, and so on backward
- Characteristic: fast response, but also easily affected by noise

**TEMA (Triple Exponential Moving Average)**
- Moving average smoothed three times
- Characteristic: extremely fast response, almost no lag
- Downside: too sensitive, easy to have false signals

**DEMA (Double Exponential Moving Average)**
- Moving average smoothed twice
- Characteristic: between EMA and TEMA

### Eight Time Periods

The strategy supports 8 time periods: 3, 7, 9, 21, 27, 63, 81, 189

What do these numbers mean? How many candlesticks to use when calculating the moving average.

- **3 candlesticks**: Super short, almost follows price
- **7 candlesticks**: Short-term baseline, commonly used for intraday
- **21 candlesticks**: About one month of trading days
- **189 candlesticks**: About one year of trading days, super long-term

### Ten Formulas

This is the strategy's core. Formulas describe the relationship between two indicators:

| Formula | Plain English Explanation |
|---------|--------------------------|
| A>B | Indicator A greater than indicator B |
| A<B | Indicator A less than indicator B |
| A*R==B | A times some coefficient equals B |
| A==R | A equals some specific value |
| A!=R | A not equal to some specific value |
| A/B>R | A divided by B greater than some value |
| B/A>R | B divided by A greater than some value |
| 0<=A<=1 | A between 0 and 1 |
| 0<=B<=1 | B between 0 and 1 |

### Real Number Parameter R

Each formula has an R, which is an adjustable number ranging from -2.0 to 2.0.

For example, formula "A>R", if R is set to 0.5, it means "A greater than 0.5".

## 3. What's the Core Thinking Behind This Strategy?

### No Fixed Logic

Most strategies have fixed buy/sell logic, like "buy when RSI below 30". Persia doesn't do that—it says: tell me what indicators, what formulas to use, and I'll combine them for judgment.

### Condition Combination

The strategy lets you set multiple conditions, all must be satisfied to trigger a trade.

For example, setting 3 conditions:
1. TEMA-9 not equal to 0.5
2. DEMA-3 between 0 and 1
3. DEMA-63 divided by DEMA-27 greater than -1.4

All three conditions must be met together to buy. Sounds weird, right? This is the "optimal combination" found by Hyperopt—why it's this way, maybe the machine discovered this combination performed best in historical data.

### Automatically Find Optimal

You don't need to think about which combination is best, let Hyperopt run it. It will try various combinations and finally tell you which makes the most money.

## 4. How Does This Strategy Decide When to Buy?

### Current Configuration's Buy Conditions

Let's look at the three buy conditions in current default configuration:

**Condition 1**:
- What indicator: TEMA-9 (9-period triple EMA)
- Formula: A!=R (not equal to some value)
- R value: 0.5

Translation: When TEMA-9's value is not 0.5, condition is satisfied. This condition is almost always satisfied since prices rarely exactly equal 0.5.

**Condition 2**:
- What indicator: DEMA-3 as A, EMA-27 as B
- Formula: 0<=B<=1
- Meaning EMA-27 between 0 and 1

**Condition 3**:
- What indicator: DEMA-27 as A, DEMA-63 as B
- Formula: B/A>R
- R value: -1.4
- Meaning DEMA-63 divided by DEMA-27 greater than -1.4

### Are These Conditions Reasonable?

Honestly, these conditions look weird. TEMA not equal to 0.5? EMA between 0 and 1? These values are too specific—they might just be "best fit" found by Hyperopt in historical data.

This is the problem with this strategy: optimized parameters might just happen to perform well in historical data, but may not work in the future.

### How Are Signals Generated?

The code logic works like this:

```python
# For each condition
A = indicator A's value (like TEMA-9)
B = indicator B's value (like EMA-27)
R = real number parameter

# Use pandas eval to calculate formula
condition_satisfied = eval(formula)

# AND all conditions together
If all conditions are satisfied:
    buy_signal = 1
```

## 5. When to Sell?

### Current Configuration's Sell Conditions

Sell conditions are also three:

**Condition 1**:
- EMA-21 equals 1.5 (A==R)
- Meaning EMA-21's value exactly equals 1.5

**Condition 2**:
- DEMA-21 divided by TEMA-27 greater than 1.4
- Meaning short-term MA/long-term MA ratio is large

**Condition 3**:
- TEMA-3 not equal to 1.6

### ROI Forced Exit

Besides sell conditions, there's ROI setting:

| Time | Minimum Profit Requirement |
|------|---------------------------|
| Immediately | 27.3% |
| After 26 minutes | 8.4% |
| After 79 minutes | 3.3% |
| After 187 minutes | 0% (forced sell) |

This ROI setting is aggressive, requiring 27% profit. But actually after 187 minutes it forces a sell, regardless of whether profit was made.

### Stop Loss

Stop loss is set at -19%, very wide. Gives strategy enough room for fluctuation, but also means a single trade could lose a lot.

## 6. What Safety Mechanisms Does This Strategy Have?

### No Built-in Protections!

This is the biggest problem with this strategy: **no built-in protection mechanisms at all**.

- No MaxDrawdown protection
- No StoplossGuard
- No LowProfitPairs protection
- No trailing stop

Just one fixed stop loss at -19%, nothing else.

### You Need to Add Them Yourself

If using this strategy, recommend adding protection mechanisms yourself:

1. **Add MaxDrawdown**: Pause trading after consecutive losses
2. **Add StoplossGuard**: Pause after stop loss
3. **Add fund management**: Limit single position size
4. **Consider trailing stop**: Lock in profits after gaining

## 7. How to Use This Strategy?

### Core Usage: Hyperopt Optimization

The correct way to use this strategy is:

```bash
freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --strategy Persia
```

Let the machine find optimal parameters for you.

### What If Parameter Space Is Too Large?

Here's the problem: this strategy's parameter space is huge.

Each condition has:
- 10 formula choices
- 4 indicator choices
- 8 time period choices
- 40 real number values

A single condition has about 400,000 combinations! Three conditions is astronomical.

### Optimization Suggestions

**Reduce condition count**:
```python
CONDITIONS = 1  # Start with just one condition
```

**Limit parameter range**:
- Time periods only select a few common ones
- Narrow real number range

**Step-by-step optimization**:
1. First optimize buy
2. Then optimize sell
3. Finally joint fine-tuning

## 8. What Are the Risks?

### Overfitting Risk (Biggest Risk)

This is the biggest problem. Parameter space is so large that Hyperopt will find a "perfect in historical data" combination, but future markets are completely different.

For example: Hyperopt might discover "TEMA-7 not equal to 0.3 and DEMA-21 between 0.8 and 1.2" made tons of money in historical data. But that's just coincidence—future won't work this way every time.

### Black Box Risk

After optimization you just get a pile of parameters, like "formula0=A!=R, indicator0=TEMA, timeframe0=9, real0=0.5".

What trading logic does this represent? Can't explain. You don't know why this combination makes money, only that it made money in historical data.

### No Protection Risk

As mentioned earlier, no built-in protection mechanisms. In extreme markets, might get wiped out.

### Stop Loss Too Wide Risk

19% stop loss is too wide. If triggered, single trade loses nearly 20%. A few of those and your capital is gone.

## 9. How Does This Compare to Other Strategies?

### Compared to Fixed Logic Strategies

**Regular Strategies** (like NostalgiaForInfinity):
- Have clear trading logic
- "RSI low, price pullback, trend up" → buy
- Easy to understand, easy to tune

**Persia**:
- No fixed logic
- Parameter combination determined by machine
- Optimization results hard to interpret

### Advantages

1. **Extremely high flexibility**: Can simulate various moving average strategies
2. **Automatic discovery**: Machine might discover combinations humans wouldn't think of
3. **Learning value**: Helps understand effects of different parameters

### Disadvantages

1. **Extremely high overfitting risk**: Historical perfection doesn't equal future effectiveness
2. **Hard to interpret**: Optimization results are black box
3. **No protection**: Risk control completely depends on yourself

## 10. Practical Suggestions

### Use Only for Research

Recommend treating Persia as a research tool, not for direct live trading.

### If You Must Go Live

1. **Strictly control parameter space**
   - Use only 1-2 conditions
   - Limit time period range
   - Narrow real number range

2. **Add protection mechanisms**
   - MaxDrawdown protection
   - StoplossGuard protection
   - Fund management

3. **Strict validation**
   - Walk-Forward validation
   - Out-of-sample testing
   - Multi-market validation

### Validation Methods

**Walk-Forward Validation**:
- Use first 6 months of data for optimization
- Validate on next 3 months of data
- See if optimization results still work

**Check parameter boundaries**:
- If optimal parameter is exactly at boundary (like real=2.0)
- Might mean better values exist outside boundary
- Such results are unstable

## 11. Who Is This Strategy For?

**Suitable for**:
- Quantitative trading researchers
- People exploring strategy possibilities
- People with time for strict validation
- People with clear understanding of overfitting risks

**Not suitable for**:
- Beginners (can't see where risks are)
- People wanting to make money directly (optimization results might be invalid)
- People pursuing stable returns (this strategy is too unstable)

## 12. Final Summary

Persia is a unique strategy framework, designed with "let machine find strategy" philosophy.

**Core Mechanism**:
- Four moving averages (SMA, EMA, TEMA, DEMA)
- Eight time periods
- Ten mathematical formulas
- Combinable buy and sell conditions

**Greatest Advantage**: Extremely high flexibility, theoretically can simulate any moving average strategy

**Greatest Risk**: Overfitting, perfect historical performance doesn't equal future effectiveness

**Correct Usage**:
1. Use as research tool
2. Strictly limit parameter space
3. Conduct sufficient out-of-sample validation
4. Add risk management mechanisms
5. Don't directly use optimization results

This strategy's value lies in demonstrating possibilities of "automatic strategy discovery", while reminding us of overfitting dangers. Machines can find patterns in historical data, but these patterns might not continue working in the future.

## 13. ⚠️ Risk Reminder

1. **Overfitting is the deadliest risk**: Parameter space is so large, easy to find a "historically perfect" combination. But this combination might just be coincidence, completely ineffective in future. You might see 100% win rate in historical data, but live trading loses everything.

2. **Optimization results are unexplainable**: You get a pile of parameters, like "TEMA-9 not equal to 0.5". What does this mean? Don't know. Machine found it, humans can't understand. This makes it impossible to judge whether the logic is reasonable.

3. **No protection mechanisms**: Strategy has no built-in protections whatsoever. During consecutive losses, it keeps trading; during black swans, stop loss might have slippage. You must add risk management yourself.

4. **Stop loss too wide**: 19% stop loss means single trade can lose nearly one-fifth. A few consecutive stop losses and your capital is halved.

5. **Don't trust backtest data**: This strategy's backtest data usually looks beautiful (because it's optimized from it). But beautiful backtest doesn't equal live profit. Walk-Forward validation is mandatory, not optional.

6. **Primary use is research**: Recommend treating Persia as a learning tool, understanding effects of different indicators and time periods. If using optimization results for live trading, must add protection mechanisms and conduct strict validation.

Remember: Quantitative trading is not a "find optimal parameters" game, but finding "stable and effective" strategies. Persia helps you find optimal parameters but doesn't guarantee stability or effectiveness. Before using,务必 understand this difference.