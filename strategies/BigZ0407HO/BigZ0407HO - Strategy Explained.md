# BigZ0407HO: The "Super Cautious Short-Term Player"

> **Nickname**: Optimized Bargain Hunter  
> **Profession**: Quant world's "play safe" type — surviving is more important than making money  
> **Timeframe**: 5 minutes + 1 hour

---

## 1. What's This Thing?

BigZ0407HO is the **optimized upgrade version** of BigZ0407, developed by a guru named ilya. Simply put, this is a trading strategyspecializes in for "buying low and selling high" in the cryptocurrency market, but it's not that chase-rise-sell-drop gameplay, instead it **specializes in finding oversold rebound opportunities**.

You can understand it as a "picking up bargains" expert: it doesn't panic and run when prices drop, but goes in to "catch the falling knife" when prices drop low enough, then runs after prices rebound just a bit. HO version means it's been HyperOpt optimized, parameters and such have been tuned more precisely.

This strategy's core thinking is: **surviving in crypto is more important than making money**. So it sets up all kinds of protection measures, afraid you'll lose too much. Of course, its money-making ability isn't bad either, especially in those up-and-down oscillating markets.

---

## 2. Core Settings: Basically "Survival First"

### Profit-Taking Rules (ROI Table)

```
Hold 0-10 min:    Consider selling if profit > 3.8%
Hold 10-40 min:   Consider selling if profit > 2.8%
Hold 40-180 min:  Consider selling if profit > 1.5%
Hold 180+ min:    Consider selling if profit > 1.8%
```

**Translation**: The longer you hold, the lower the requirements. But don't think about lying down and earning, maximum 3 hours for you.

### Stoploss Rules

```
Traditional stoploss: -99% (turned off)
Custom stoploss: Start judging after 50 minutes
Trailing stop: Starts after 1% profit, run if pullback 2.5%
```

**Translation**: Don't look at traditional stoploss being off,they have smarter stoploss methods — wait 50 minutes to see the situation first.

---

## 3. 12 Entry Conditions: I've Categorized Them for You

This strategy has 12 different entry methods, basically playing "oversold rebound" to the extreme, I've grouped them into 4 categories for you:

### 🎯 Category 1: RSI Oversold + Bollinger Bands (Conditions 0-2)
**Core Logic**: RSI low means oversold, Bollinger Band lower rail means cheap price

**In Plain English**:
> "Dropped to the right level, buy a bit to try"

**Classic Lines**:
- Condition #0: `RSI < 30 + Close above EMA200 + Volume shrinking` → "Big trend still there, short-term oversold, go!"
- Condition #1: `Close < Bollinger lower rail + RSI low + Volume shrinking` → "Price low enough, volume also shrunk, bet on rebound"

### 📉 Category 2: Double Oversold (Conditions 3-4)
**Core Logic**: 1-hour trend upward, but 5-minute already oversold

**In Plain English**:
> "Big direction is bull market, but short-term dropped too much"

**Classic Lines**:
- Condition #3: `1-hour EMA200 upward + 5-minute RSI extremely low` → "Big cycle upward, small cycle oversold, counter-trend bottom fishing"
- Condition #4: `1-hour RSI < 20 + Price at Bollinger lower rail` → "Big cycle already oversold, rebound probability higher"

### 🔧 Category 3: RSI + MACD Combo (Conditions 5-7)
**Core Logic**: Momentum turning strong + oversold position

**In Plain English**:
> "Can't drop more, and people starting to buy"

**Classic Lines**:
- Condition #5: `MACD golden cross + Close < Bollinger lower rail + RSI low` → "MACD just turned bullish, price still low, enter"
- Condition #7: `1-hour RSI < 17 + MACD golden cross` → "Big cycle extreme oversold + momentum turning strong, double insurance"

### 🌟 Category 4: Advanced Combo (Conditions 8-12)
**Core Logic**: Multi-indicator resonance, signals more reliable

**In Plain English**:
> "All conditions met, if you don't get on board now when will you"

**Classic Lines**:
- Condition #10: `1-hour Bollinger lower rail + MACD turned positive + 5-minute RSI low` → "Big cycle level rebound, go big"
- Condition #12: `Close < Bollinger lower rail + Previous candle still inside Bollinger Band + RSI low` → "False breakout then reversal, classic pattern"

These 12 conditions are like 12 keys, as long as one can unlock the door, the strategy enters! 🤣

---

## 4. Protection Mechanisms: 6 Layers of "Bulletproof Vest"

Each entry condition comes with a set of protection parameters, like wearing 6 layers of bulletproof vest:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| Custom Stoploss | Dynamic judgment after 50 minutes | "Give you 50 minutes to perform, if not then cut" |
| Trailing Take-Profit | Protect profits after earning | "Don't give back what you earned" |
| Tiered Take-Profit | Decide sell point based on profit | "The more you earn, the faster you run" |
| Pump Protection | Guard against spike up and crash down | "Rose too fiercely, run first" |
| Recovery Exit | Run after breaking even a bit when lost a lot | "Take small loss as profit" |
| Long-term Position Forced Exit | Forced liquidation after 15 hours | "Don't linger" |

This protection mechanism basically took "cowardly" to the extreme! 🤣

---

## 5. Exit Logic: Smarter Than Entry

### 5.1 Tiered Take-Profit: Run Based on How Much You Earned

```
Profit > 20%: Run when RSI > 34
Profit 1-2%: Also wait for RSI to threshold before selling
```

**In Plain English**:
- When earning a lot: Run at the slightest wind or movement
- When earning little: Wait a bit more to see if can earn more

### 5.2 Special Scenario Exits

| Scenario | Trigger Condition | Plain English |
|----------|------------------|---------------|
| Price below EMA200 | More alert, sell when RSI in position | "In downtrend protecting profits most important" |
| Abnormal volatility detected | Pump protection starts | "Coins with spike up crash down, run first" |
| Trend reversal | 200-day moving average declining | "Trend changed, retreat quickly" |

### 5.3 Basic Sell Signals (1 type)

**Classic Lines**:

1. **Signal #1**: `Close > Bollinger middle rail × 1.01`
   > "Rose to middle position, pocket the profits"

---

## 6. This Strategy's "Personality Traits"

### ✅ Advantages (Praise Session)

1. **Extremely conservative**: Rather earn less than lose big
2. **Shrewd and capable**: 12 entry methods, adapts to various markets
3. **Looks far ahead**: 5-minute + 1-hour dual timeframe, not impulsive
4. **Reacts fast**: Once something's wrong, runs faster than anyone

### ⚠️ Disadvantages (Roast Session)

1. **A bit neurotic**: Gets nervous with slight market fluctuations
2. **Doesn't earn enough in bull markets**: Always runs after earning a bit, misses big markets
3. **Hard to understand**: Hundreds of parameters, a dozen conditions

---

## 7. Suitable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Oscillating market | ✅ Strongly recommend | High sell low buy, strategy like fish in water |
| Bull market pullback | ✅ Recommended | Oversold rebound catches it perfectly |
| Strong trend upward | ⚠️ Caution | Sells too early, misses out |
| Continuous decline | ❌ Not recommended | May have continuous stoploss |

---

## 8. Summary: How's This Strategy Anyway?

### One Sentence Evaluation
> "Survival first, making money second. A super cautious short-term strategy."

### Who Should Use It?
- ✅ Risk-averse investors
- ✅ Traders who like short-term trading
- ✅ People who want "surviving" in crypto more important than "making big money"
- ✅ People who can accept "sold and still rising"

### Who Shouldn't Use It?
- ❌ Those wanting to catch 10x coins
- ❌ Those wanting long-term holding
- ❌ Those who go all in at once
- ❌ Those too lazy to learn strategy logic

### My Suggestions
1. **Run paper trading for 1 month first**: Familiarize with strategy behavior
2. **Start with small capital**: Don't bet big money at the beginning
3. **Run 2-4 coins simultaneously**: Diversify risk
4. **Set alerts**: Intervene timely on abnormal volatility

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Build "Defense Net" with Smart Stoploss

BigZ series is oscillating rebound type strategy. Core thinking is: **find oversold rebounds, earn a bit and run**.

**Its money-making philosophy**: Accumulate little by little, surviving is most important

- **Don't chase rises**: Only buy near Bollinger Band lower rail
- **Don't be greedy**: Wants to run at 2-3% profit
- **Smart stoploss**: Dynamic judgment after 50 minutes whether to cut

### 9.2 Different Market Performance (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Oscillating market | ⭐⭐⭐⭐⭐ | Best environment, repeatedly eat the spread |
| 🔄 Bull market pullback | ⭐⭐⭐⭐ | Oversold rebound catches it perfectly |
| 📉 Bear market | ⭐⭐ | Counter-trend buying has risks |
| ⚡️ Strong trend upward | ⭐⭐ | Serious missing out, sells too early |

**One sentence summary**: Oscillating market is home court, be careful with one-sided markets.

---

## 10. Want to Run This Strategy? First Look at These Configs

### 10.1 Trading Pair Configuration

| Config Item | Suggested Value | Roast |
|-------------|-----------------|-------|
| Simultaneous positions | 2-4 | Too few not enough opportunities, too many can't watch over |
| Trading pairs | Major coins (BTC/ETH) | Don't touch small coins, poor liquidity |
| Timeframe | 5 minutes + 1 hour | Don't change, already tuned |

### 10.2 Configuration File Key Settings

```yaml
max_open_trades: 3
stake_amount: "unlimited"
dry_run_wallet: 1000
```

### 10.3 Hardware Requirements (Important!)

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|-----------------|------------|
| 5-10 | 2GB | 4GB | Smooth |
| 10-20 | 4GB | 8GB | No problem |

**Warning**: Using 5-minute candles, CPU usage will be higher than long cycles, watch the heat dissipation! 😅

### 10.4 Backtest vs Live Trading

- Good backtest performance doesn't mean good live trading
- Market environment changed strategy might become invalid
- Suggest regularly checking strategy performance

**Suggested Process**:
1. Backtest 3 months data first
2. Run paper trading for 2 weeks
3. Small capital live trading
4. Gradually expand

**Don't go all in at the beginning**, no matter how good the strategy needs breaking in!

---

## 11. Easter Eggs: Strategy Author's "Little Schemes"

Look carefully at the code, you'll discover some interesting things:

1. **Meaning of HO**: HyperOpt optimized version, means parameters optimized through machine learning
   > "These parameters weren't blindly tuned by me, computer calculated them for me"

2. **Author donation address**: BTC and ETH addresses hidden in code
   > "If you made money using my strategy, remember to tip"

3. **Truth about -99% stoploss**: Not really losing 99%, using custom stoploss
   > "Don't be scared, I have smarter stoploss methods"

4. **exit_profit_only**: When set to True only sells when profitable
   > "Either profit, or lose to stoploss, don't actively lose"

---

## 12. Finally Finally

### One Sentence Evaluation
> "A 'scared of death' but runs fast strategy, suitable for people who want to survive in crypto."

### Who Should Use It?
- ✅ Risk-averse people
- ✅ Short-term trading enthusiasts
- ✅ People who want stable profits
- ✅ People who can accept complex strategies

### Who Shouldn't Use It?
- ❌ People who want to get rich quick
- ❌ Long-term investors
- ❌ People unwilling to learn
- ❌ People with bad mentality

### Manual Trader Suggestions
This strategy has too many conditions, not recommended for manual execution. Just use quant platforms honestly!

---

## 13. ⚠️ Risk Reminder Again (Must Read This Part)

### Backtest Beautiful, Live Trading Be Careful

BigZ0407HO's historical backtest performance is often good — but there's a trap:

> **Because it's an optimized version, parameters might be "fitted" to past market's optimal solution, but this doesn't represent future一定能盈利.**

Simply put: **Students who memorize answers might not know how when the questions change.**

### Hidden Risks of Complex Strategies

During live trading, complex logic may lead to:
- **Signal understanding difficulty**: Don't know why bought
- **Parameter overfitting**: Historical data good, future invalid
- **Overtrading**: Too many signals, fees eat profits
- **Extreme market risk**: Black swan events might break through protection

### My Suggestions (True Words)

```
1. Paper trade at least 1 month first
2. Start with small capital, don't exceed 20% of total funds
3. Set total loss alert, pause if over 10%
4. Regular review, optimize when needed
5. Don't bet all money on one strategy
```

**Remember**: No matter how good the strategy, the market won't say hello when teaching you lessons. Light position testing, surviving is most important! 🙏
