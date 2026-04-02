# Mark_Strat Strategy: The Bollinger Bands "Bottom Fisher"

> **Nickname**: Bottom Fisher, Bollinger Bands Rebel  
> **Profession**: Tough guy who dares to buy when price breaks below lower band  
> **Timeframe**: 1 minute (ultra-short-term scalping)

---

## I. What Is This Strategy?

Simply put, **Mark_Strat** is a strategy that:
- Buys when price breaks below Bollinger Bands lower band
- Runs when RSI shoots above 90
- Must wrap up work within 29 minutes

It's like **discount shopping**: Wait for the product to drop to rock-bottom price, buy; wait for it to return to original price, sell! 🛒

---

## II. Core Configuration: "Quick In, Quick Out, Let Profits Run"

### Take-Profit Rules (ROI Table)

```
Just bought: Target 3.65%
7 minutes later: Target drops to 1.22%
16 minutes later: Target drops to 0.76%
29 minutes later: No matter what, get out!
```

**Translation**: This strategy is a scalper, must finish the fight within 29 minutes. After buying, hope it rises fast; if it rises slowly, lower expectations.

### Stop Loss Rules

```
Initial Stop Loss: -23.94% (wait, did I read that right?)
```

**Translation**: Yes, you read that right, initial stop loss is -23.94%! Super loose! Meaning "even if it drops 20% after buying, I'm not panicking, because I have trailing stop."

### Trailing Stop (This Is the Key Point)

```
Profit reaches 17.49% → Activate trailing stop
Profit retraces to 13.60% → Trigger stop loss, protect profits
```

**Translation**: Initial stop loss is ridiculously wide, but once you've made big money (above 17%), it starts protecting your profits. As long as profit retraces to 13.6%, it locks in your gains.

---

## III. 1 Buy Condition: Buy When Breaking Below Lower Band

### 🎯 Buy Condition

**Plain English**:
> "Close price breaks below Bollinger Bands lower band? Has volume? Do it!"

**Classic Lines**:
```python
# Buy Conditions
(
    ((dataframe['close'] < dataframe['bb_lowerband'])) &  # Break below Bollinger Bands lower band
    (dataframe['volume'] > 0)                               # Someone is trading
)
```

> "Bollinger Bands lower band? That's support! Breaking below it is giving away money!"

**Breakdown**:
- **Bollinger Bands Lower Band**: 20 periods, 2 standard deviations, price breaking below this position is "oversold"
- **Volume > 0**: Confirms someone is trading at this position

---

## IV. Multi-Layer Exit Mechanism: This Strategy Is "Fickle"

### 4.1 Three Exit Methods

| Exit Method | Trigger Condition | Description |
|---------|---------|------|
| ROI Take-Profit | Time-based decreasing | Forced exit within 29 minutes |
| Sell Signal | RSI > 90 + Return to middle band | Active exit |
| Trailing Stop | Profit retraces to 13.6% | Protect profits |

### 4.2 Sell Signal Detailed Explanation

**Plain English**:
> "RSI shot above 90, price also returned to Bollinger Bands middle band, run!"

**Classic Lines**:
```python
# Sell Conditions
(
    (dataframe['rsi'] > 90) &                              # RSI super high
    ((dataframe['close'] > dataframe['bb_middleband'])) &  # Returned to middle band
    (dataframe['volume'] > 0)                               # Someone is trading
)
```

> "RSI is already 90, price returned to middle band, rebound is over, hurry and cash out!"

### 4.3 Trailing Stop Diagram

```
Profit Development          Stop Loss Behavior
────────────────────────────────────────
0% ~ 17%                  Initial stop loss -24% active
Reach 17.49%              Trailing stop activates!
Profit retraces to 13.60%  Trigger exit, lock in ~4% profit buffer
```

**Plain English**: Once you've earned enough, it starts protecting you, not letting profits slip away.

---

## V. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Section)

1. **Simple Logic**: Buy at Bollinger Bands lower band, sell at middle band, crystal clear
2. **Trailing Stop Is Powerful**: Protects you once you've earned enough, lets profits run
3. **Clear Time Constraint**: Must leave within 29 minutes, no dithering
4. **Only Sell When Profitable**: sell_profit_only = True, won't come out at a loss

### ⚠️ Weaknesses (Complaint Section)

1. **Initial Stop Loss Too Wide**: -24%! Won't stop loss even if it drops 20% after buying, too "Buddhist"
2. **1-Minute Level**: Miss the market if internet is slow
3. **Indicator Redundancy**: Calculated MACD, SAR, StochRSI but didn't use any of them
4. **Scalping Costs**: Frequent trading fees will eat profits

---

## VI. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|---------|---------|------|
| 📊 Sideways Volatile | ✅ Strongly Recommended | This is home court! Buy low, sell high |
| 📈 Moderate Uptrend | ✅ Can use | Has pullback opportunities |
| 📉 Downtrend | ⚠️ Careful | Easy to catch falling knives halfway down |
| 🚀 Strong Single-Sided | ❌ Don't use | Counter-trend operation, certain death |

---

## VII. Summary: How Is This Strategy Really?

### One-Sentence Evaluation
> "A scalper that buys at Bollinger Bands lower band, runs at middle band, must wrap up within 29 minutes."

### Who Should Use It?
- ✅ Sideways market traders
- ✅ People who like mean reversion strategies
- ✅ Those who can accept large stop loss space
- ✅ 1-minute level scalping enthusiasts

### Who Should NOT Use It?
- ❌ People who don't like wide stop losses
- ❌ Single-sided trend markets
- ❌ Environments with high network latency
- ❌ People who don't want to trade frequently

### My Recommendations
1. **Tighten initial stop loss**: -24% is too wide, suggest changing to -15%
2. **Only trade sideways currency pairs**: Find currencies with regular volatility
3. **Watch transaction costs**: Scalping fees eat profits
4. **Need good internet**: 1-minute level, latency is money

---

## VIII. What Markets Can This Strategy Make Money In?

### 8.1 Core Logic: Mean Reversion

Mark_Strat is a **mean reversion strategy**. Its profit philosophy:

> **"Price breaks below Bollinger Bands lower band, that's oversold; wait for it to return to middle band, that's profit."**

- **Buy at Bollinger Bands Lower Band**: Price has fallen too far
- **Sell at Bollinger Bands Middle Band**: Price has returned to normal
- **RSI > 90 Confirmation**: Rebound is strong enough, time to go

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📊 Sideways Volatile | ⭐⭐⭐⭐⭐ | This is home court! Up and down, buy low sell high |
| 📈 Moderate Uptrend | ⭐⭐⭐⭐☆ | Has pullback opportunities, can capture rebounds |
| 📉 Downtrend | ⭐⭐☆☆☆ | Will fall more after breaking below lower band, catch falling knives halfway |
| 🚀 Strong Single-Sided | ⭐☆☆☆☆ | Counter-trend operation, you short when it rises单边, you bottom fish when it falls单边, die very fast |

**One-Sentence Summary**: **Sideways market is home court, single-sided market is graveyard.**

---

## IX. Want to Run This Strategy? Check These Configurations First

### 9.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|--------|--------|------|
| Trading Pairs | Currencies with regular volatility | Don't find those explosive crazy coins |
| Timeframe | 1m (default) | Can try 3m or 5m |
| Initial Stop Loss | Change to -15% | Original -24% is too wide |

### 9.2 Hardware Requirements (Some Requirements)

This strategy uses 1-minute level, has requirements for response speed:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------|---------|---------|------|
| 1-5 pairs | 2GB | 4GB | Smooth |
| 5-20 pairs | 4GB | 8GB | Okay |
| 20+ pairs | 8GB | 16GB | May struggle |

**Comment**: 1-minute level, both network and machine need to keep up, don't run on a potato!

### 9.3 Backtesting vs Live Trading

Scalping strategies have large differences between backtesting and live trading:

- **Slippage**: 1-minute level, slippage may eat half your profits
- **Latency**: Exchange latency may miss best entry
- **Transaction Fees**: Frequent trading, fees account for high percentage
- **Liquidity**: Large orders may produce larger slippage

**Recommended Process**:
1. Backtest to validate logic
2. Demo test execution
3. Small capital live trading
4. Calculate actual costs (slippage + fees) for each trade

**Don't be fooled by backtesting**; scalping strategy live performance is often much worse!

---

## X. Easter Egg: The Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Initial stop loss -23.936%, precise to decimal point**
   > "This number was definitely optimized, but -24% is too wide..."

2. **Trailing stop only activates at 17.49%**
   > "Earn less than 17%? Then I don't care about you, handle it yourself."

3. **Calculated MACD, SAR, StochRSI but didn't use them**
   > "Probably found they weren't useful in backtesting, but too lazy to delete code..."

4. **sell_profit_only = True**
   > "Don't let sell signals trigger when losing money, let stop loss or ROI handle it."

5. **29-minute forced exit**
   > "Must finish the fight within half an hour, ultra-short-term means fast!"

---

## XI. Last But Not Least

### One-Sentence Evaluation
> "A scalper that buys at Bollinger Bands lower band and runs at middle band, initial stop loss is ridiculously wide, but trailing stop is quite powerful."

### Who Should Use It?
- ✅ Sideways market enthusiasts
- ✅ Mean reversion strategy fans
- ✅ Those who can accept large stop loss space
- ✅ 1-minute level scalping experts

### Who Should NOT Use It?
- ❌ People who don't like wide stop losses
- ❌ Single-sided trend markets
- ❌ Environments with poor internet
- ❌ People who don't want to trade frequently

### Manual Trader Recommendations
Can manually apply this logic:
1. Set up Bollinger Bands (20 periods, 2 standard deviations)
2. Wait for price to break below lower band
3. Set stop loss -15% (tighter than original strategy)
4. Run when price returns to middle band + RSI > 90

---

## XII. ⚠️ Risk Re-emphasis (Must Read This Section)

### Backtesting Is Beautiful, Live Trading Requires Caution

Mark_Strat's historical backtesting performance may **look good**—but there are several traps:

> **The biggest enemies of scalping strategies are transaction costs and slippage.**

### Hidden Risks of 1-Minute Level

In live trading, 1-minute level may lead to:
- **Slippage**: Price changes within seconds, entry price may differ a lot
- **Latency**: Network latency may miss best timing
- **Transaction Fees**: Frequent trading, fees may eat half your profits
- **Liquidity**: Small currencies may not be able to buy or sell

### Wide Stop Loss Risks

- **Maximum loss 24%**: One trade may lose a quarter
- **High trailing stop activation threshold**: Need to earn 17.5% to activate protection
- **Many trades won't wait for trailing stop**: Come out at a loss

### My Recommendations (Honest Truth)

```
1. Tighten initial stop loss to -15%
2. Lower trailing stop activation threshold to 10%
3. Only use in sideways markets
4. Small capital test, don't go all-in
5. Calculate actual costs (slippage + fees) for each trade
```

**Remember**: Scalping strategies look simple, but live execution is hardest. Network latency, exchange latency, slippage, fees—each one is eating your profits!

---

**Final Reminder**: Bollinger Bands lower band is not a support level; it's just a statistically calculated "abnormal value." May fall more after breaking below lower band, don't迷信 bottom fishing! 🙏
