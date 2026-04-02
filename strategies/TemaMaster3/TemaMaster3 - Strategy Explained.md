# TemaMaster3 Strategy: The "Rebound Hunter" at Bollinger Lower Band

> **Nickname**: Rebound Hunter  
> **Occupation**: Ultra-Short-Term Rebound Capture Specialist  
> **Timeframe**: 1 minute (High-frequency player's rhythm)

---

## I. What is This Strategy?

Simply put, **TemaMaster3** is:
- A "bargain hunter" watching the Bollinger lower band for opportunities
- Using Triple Exponential Moving Average to judge "has the rebound started?"
- Using CMO momentum indicator to confirm "this move has potential!"

Like waiting in the discount section, buying when the price drops below cost and starts bouncing back 🛒

---

## II. Core Configuration: "Disciplined Bargain Hunting"

### Take Profit Rules (ROI Table)

```
0 minutes: Make 25.57% and run
```

**Translation**: This strategy is "greedy", aiming for 25% right away, but trailing stop will intercept along the way.

### Stop Loss Rules

```
Hard stop loss: -8.85% (Cut losses here)
Trailing stop: Activates after 13% profit, allows pullback to around 18%
```

**Translation**: Like buying a stock, once it's up 13%, set a dynamic take-profit line so the cooked duck doesn't fly away.

---

## III. 1 Buy Condition: Looks Simple, But Has Depth

The strategy has only one buy condition, but it's a combination punch:

### 🎯 Buy Condition: TEMA Crosses Above Bollinger Lower Band + CMO Confirmation

**Technical Implementation**:
```python
# TEMA (Triple Exponential Moving Average) crosses from below to above Bollinger lower band
# AND CMO (Chande Momentum) greater than -3
```

**Plain English Translation**:
> "Price has fallen outside the Bollinger lower band, now TEMA is crossing back above the lower band, indicating a rebound has started! But check CMO too - if momentum is above -3, it's not a dead cat bounce, time to get on board!"

**Simple Understanding**:
- Bollinger lower band = price "floor"
- TEMA crossing lower band = price starting to go up
- CMO > -3 = momentum not extremely weak
- All three conditions met = high rebound probability

---

## IV. 2 Sell Signals: Running Based on Momentum "Mood"

Sell logic is entirely entrusted to the CMO momentum indicator, pick one of two signals:

### 5.1 Sell Signal Overview

| Signal | Trigger Condition | Plain English |
|--------|-------------------|----------------|
| **Signal #1** | CMO drops below -22 | "Momentum is dead, run!" |
| **Signal #2** | CMO drops below 25 from above | "Momentum dropping from high, take profits and go" |

### 5.2 Sell Logic Interpretation

**CMO Drops Below -22**:
> "Momentum indicator fell below -22, meaning market sentiment has turned bad, don't wait, sell quickly."

**CMO Drops Below 25 from Above**:
> "Momentum was high before (above 25), now starting to turn, might be topping out, lock in gains."

---

## V. Technical Indicators: How Does This Strategy "Read the Market"?

### Core Indicators

| Indicator | Parameter | Function |
|-----------|-----------|----------|
| **TEMA** | 60 period | Smoother trend line than EMA |
| **Bollinger Lower Band** | 60 period, standard deviation 1.4 | Dynamic "floor price" |
| **CMO** | 180 period | Momentum strength meter |

### An Interesting Thing

The code also calculates STDDEV, MA, COEFFV (coefficient of variation), but doesn't use them at all!

> It's like buying a bunch of groceries but only cooking two of them 🤣

Could be legacy code, or the author changed their mind later.

---

## VI. Strategy "Personality Traits"

### ✅ Pros (Praise Section)

1. **Cautious Entry**: Bollinger lower band + CMO dual confirmation, not easy to step on mines
2. **Flexible Exit**: One exit in weakness zone, one in strength zone, adapts to different situations
3. **Smart Stop Loss**: Trailing stop can lock in profits, won't "ride the elevator"
4. **Clear Logic**: Simple code, can understand what it's doing at a glance

### ⚠️ Cons (Criticism Section)

1. **Single Signal**: Only one set of buy/sell logic, stuck if market changes
2. **High-Frequency Trap**: 1-minute timeframe, fees and slippage can eat all profits
3. **Rigid Parameters**: No protection mechanism groups like other strategies, nowhere to adjust
4. **Redundant Code**: Calculated indicators not used, wasting CPU

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **Sideways Oscillation** | ✅ First choice | Bollinger lower band touched repeatedly, many rebound opportunities |
| **Slow Bull Market** | ✅ Can use | Capture pullback rebounds, but may exit too early |
| **Trending Down** | ❌ Use cautiously | High risk of catching falling knives, CMO filter may not be enough |
| **Extreme Volatility** | ❌ Don't use | Many false signals, stop loss may trigger frequently |

---

## VIII. Summary: How Is This Strategy Really?

### One-Sentence Review
> "A rebound hunter at Bollinger lower band, a small expert in oscillating markets, a bag holder in trending markets."

### Who Should Use It?
- ✅ Day traders who like high-frequency trading
- ✅ Technical analysts familiar with Bollinger and momentum indicators
- ✅ People with plenty of time to monitor the market
- ✅ Users on exchanges with low fee rates

### Who Shouldn't Use It?
- ❌ Office workers with no time to monitor
- ❌ Users on exchanges with high fee rates
- ❌ People who don't like frequent trading
- ❌ Investors seeking large trending moves

### My Advice
1. **Backtest First**: 1-minute timeframe must be backtested for verification
2. **Calculate Costs**: Factor in fees and slippage before deciding
3. **Adjust Parameters**: Try raising CMO threshold to 0
4. **Control Position**: Don't go all-in on short-term strategies, test with small positions

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Bollinger Lower Band Rebound Capture

TemaMaster3 is a **pure rebound strategy**. The logic is simple:

- **Wait**: Price falls outside Bollinger lower band (oversold territory)
- **Watch**: TEMA starts crossing above lower band (rebound initiated)
- **Confirm**: CMO momentum not extremely weak (not dead cat bounce)
- **Buy**: All three conditions met, enter position
- **Run**: Sell when momentum weakens or falls from high

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 **Slow Bull Trend** | ⭐⭐⭐☆☆ | Can catch pullbacks, but may sell too early in big trends |
| 🔄 **Sideways Oscillation** | ⭐⭐⭐⭐⭐ | Home territory! Upper and lower bands hit repeatedly, many rebound opportunities |
| 📉 **Trending Down** | ⭐⭐☆☆☆ | Catching falling knives, might catch a "dropping blade" |
| ⚡️ **High Volatility** | ⭐⭐⭐☆☆ | Many signals but also many false breakouts, need parameter optimization |

**One-Sentence Summary**: Makes money in oscillating markets, relies on luck in trending markets.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Timeframe | 1 minute | High-frequency player's rhythm |
| Number of Trading Pairs | 1-5 pairs | Can't calculate too many |
| Liquidity | High | Don't touch altcoins, slippage will eat you alive |

### 10.2 Key Configuration File Settings

```yaml
# Key configurations
timeframe: '1m'
stake_currency: 'USDT'  # or other quote currency

# Stop loss and take profit
stoploss: -0.08848
minimal_roi: { "0": 0.25574 }

# Trailing stop
trailing_stop: true
trailing_stop_positive: 0.12943
trailing_stop_positive_offset: 0.17942
```

### 10.3 Hardware Requirements (Important!)

This strategy uses 1-minute timeframe, high real-time requirements:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-5 pairs | 4GB | 8GB | Smooth |
| 5-10 pairs | 8GB | 16GB | Might be a bit laggy |
| 10+ pairs | 16GB | 32GB+ | Old computer will cry |

**Warning**: High-frequency strategies are sensitive to network and server latency! 😅

### 10.4 Backtest vs Live Trading

There will be gaps between backtesting and live trading:
- Backtests don't have slippage
- Backtest fees may be set low
- Backtests can't simulate extreme market conditions

**Recommended Process**:
1. Backtest first to verify strategy logic
2. Use paper trading to test actual execution
3. Small capital live trading verification
4. Gradually increase position

**Don't go all-in from the start**, high-frequency strategies have many pitfalls!

---

## XI. Bonus: The Strategy Author's "Little Tricks"

Looking carefully at the code, you'll find some interesting things:

1. **Informative Pair**: Code has `stake_currency/USDT` informative pair
   > "Author might have wanted to reference quote currency's trend against USDT, but actual code doesn't use it"

2. **Redundant Indicators**: STDDEV, MA, COEFFV calculated but not used
   > "Could be leftover from early versions, or author changed their mind later"

3. **Commented Out Conditions**: Sell logic has commented-out code
   > "Shows author debugged multiple times, finally chose this version"

---

## XII. Final Words

### One-Sentence Review
> "A rebound tool for oscillating markets, a bag-holding tool for trending markets. Use in the right scenario and it's a good strategy."

### Who Should Use It?
- ✅ High-frequency trading enthusiasts
- ✅ Oscillating market players
- ✅ Low fee exchange users
- ✅ People with time to monitor

### Who Shouldn't Use It?
- ❌ Trend traders
- ❌ Low-frequency trading style
- ❌ High fee exchange users
- ❌ People without time to monitor

### Manual Trader Advice

This strategy is **not suitable for manual execution**:
- 1-minute candles require constant monitoring
- Signal judgment requires real-time indicator calculation
- Manual operation easily misses best timing
- Emotional interference causes strategy deviation

If you really want to trade manually:
1. Increase timeframe to 5 or 15 minutes
2. Use TradingView to set alerts
3. Execute strictly according to signals, don't hesitate

---

## XIII. ⚠️ Risk Re-emphasis (Must Read)

### Backtests Are Beautiful, Live Trading Needs Caution

TemaMaster3's historical backtest may look good - but there's a trap:

> **High-frequency strategy backtest results are often overly optimistic because backtests can't simulate slippage, latency, and liquidity changes.**

Simply put: **Backtest thinks you can execute at signal price, live trading might slip 0.5%, cumulatively that's huge losses for high-frequency.**

### Hidden Risks of High-Frequency Strategies

In live trading, high-frequency strategies may cause:
- **Fees Eating Profits**: Trading dozens of times a day, fees accumulate significantly
- **Slippage Eating Returns**: 1-minute timeframe very sensitive to execution price
- **API Rate Limits**: Frequent calls may be limited by exchange
- **Emotional Interference**: Frequent signals easily cause fatigue and mistakes

### My Advice (Heartfelt)

```
1. Don't use this strategy on exchanges with fee rates above 0.1%
2. Don't touch trading pairs with slippage over 0.05%
3. Backtesting must include fees and slippage before evaluating
4. Live trade with small capital for at least a month first
```

**Remember**: No matter how good the strategy, when the market teaches you a lesson, it doesn't warn you. This is especially true for high-frequency strategies - fees and slippage are two "invisible killers" that can eat all profits!

---

**Final Reminder**: A rebound hunter in oscillating markets, a bag holder in trending markets. Choose the right scenario, test with small positions, staying alive is most important! 🙏