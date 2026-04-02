# Saturn5 Strategy: The Three-Signal Catcher

> **Nickname**: Trend Pullback Hunter
> **Occupation**: Multi-Period EMA Analyst + VWMACD Confirmer
> **Timeframe**: 15 Minutes

---

## I. What is This Strategy?

Simply put, **Saturn5** is:
- A multi-condition strategy that uses three different "nets" to catch fish
- Five layers of protection mechanisms, more cautious than insurance companies
- 15-minute chart watching, 5% take profit, 20% stop loss

Like a veteran hunter with decision paralysis, prepared three different traps - any one triggered means it's time to work. 🤣

---

## II. Core Configuration: Basically "Run at 5% Profit"

### Take Profit Rule (ROI Table)

```
Profit ≥ 5% → Take profit immediately
```

**Translation**: See 5% profit and walk away, no greed. Like playing mahjong, win one round and leave, never overstay.

### Stop Loss Rule

```
Loss ≥ 20% → Admit defeat and exit
```

**Translation**: Stop loss only at 20%, this "safety belt" is pretty loose! Like driving, only braking at 200 km/h. 😅

---

## III. 3 Buy Conditions: I've Categorized Them for You

This strategy's buy conditions are divided into three independent signals, you can toggle any of them:

### 🎯 Type 1: Trend Pullback Hunter (signal_1)

**Core Logic**: Buy at pullback positions in a long-term uptrend

**Plain English**:
> "I just wait for price to pull back near the 240 moving average, then the 5 EMA crosses above 10 EMA, and volume MACD is also at the bottom ready to rise, that's when I enter!"

**Representative Condition**: buy_signal_1

**Classic Lines**:
- Condition 1: `vwmacd < signal` → "MACD waiting for golden cross below"
- Condition 2: `low < ema_240` → "Price pulled back below the long moving average"
- Condition 3: `close > ema_240` → "But close is back above, meaning support is valid"
- Condition 4: `ema_5 crosses above ema_10` → "Short-term trend starting to strengthen"
- Condition 5: `ema_3 < ema_50` → "But not too high, need to be below medium level"

---

### 📉 Type 2: Extreme Oversold Bounce (signal_2)

**Core Logic**: Dual confirmation of Fibonacci channel and Bollinger Bands oversold bounce

**Plain English**:
> "Price has fallen to grandma's house, Fibonacci lower band has even pierced through Bollinger lower band, at this point the probability of a bounce is high!"

**Representative Condition**: buy_signal_2

**Classic Lines**:
- Condition 1: `fib_lower crosses above bb_lower` → "Two lower bands crossed, oversold signal confirmed"
- Condition 2: `close < ema_50` → "Price below medium-long term moving average, has room to rise"

---

### 📊 Type 3: Bollinger Lower Band Scavenger (signal_3)

**Core Logic**: Look for volume-supported bounces at extreme Bollinger lower band positions

**Plain English**:
> "Price breaks below Bollinger lower band (3 standard deviations!), this is already an extreme position, if volume is okay at this time, I'll go in and gamble on a bounce."

**Representative Condition**: buy_signal_3

**Classic Lines**:
- Condition 1: `low < bb_lower(20, 3)` → "Price broke below Bollinger lower band, oversold"
- Condition 2: `high > volume_weighted_slow_ma` → "But high price can still break above volume-weighted moving average"
- Condition 3: `high < ema_50` → "High price can't be too high, need to be below 50 EMA"

---

## IV. Protection Mechanisms: 5-Layer "Anti-Pit System"

Each buy condition shares these 5 layers of protection, like wearing 5 bulletproof vests for trading:

| Protection Type | Function | Plain English |
|----------------|----------|---------------|
| **Cooldown Period** | Pause after selling... 0 minutes | "No cooldown, enter whenever you want" (basically none) |
| **Max Drawdown** | Pause 1 hour if loss >20% within 12 hours | "Lost too much today, take a break" |
| **Stop Loss Protection** | Pause 6 hours if 4 stop losses within 3 hours | "Getting chopped up recently, stop and reflect" |
| **Low Profit Lock #1** | Lock 15 min if 2 trades within 1.5 hours have <2% profit | "These two trades are trash, calm down" |
| **Low Profit Lock #2** | Lock 30 min if 4 trades within 6 hours have <1% profit | "Not in good shape today, rest a bit" |

Complaint: These protection mechanisms are pretty detailed, but cooldown set to 0? What's up with that? You can buy right after selling? 😅

---

## V. Sell Logic: Simple to the Point of Ridiculous

### 5.1 Pure ROI Take Profit

```
Profit reaches 5% → Sell!
```

**Plain English**:
- Just this one exit condition, no MACD death cross, no moving average break below, nothing
- Make 5% and run, everything else is whatever

---

### 5.2 Stop Loss Safety Net

```
Loss exceeds 20% → Give up!
```

**Plain English**: This stop loss is brutal enough, 20% before stopping. Need strong psychological fortitude. But combined with the protection mechanisms above, consecutive stop losses will get locked.

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Section)

1. **Signal Flexibility**: Three buy signals can be toggled independently, like three independent trading systems
2. **Complete Protection**: Five layers of protection mechanisms, consecutive losses get "persuaded to rest"
3. **Multi-Period Verification**: From 3 EMA to 240 EMA, layer by layer verification
4. **Volume-Weighted MACD**: More reliable than regular MACD, considers volume factors
5. **Simple Exit**: No need to struggle with conflicting sell signals

### ⚠️ Cons (Complaint Section)

1. **Stop Loss Too Wide**: 20% stop loss, capital volatility like a roller coaster 🎢
2. **No Trailing Stop**: Might miss out on a lot of profit in trending markets
3. **No Sell Signal**: Completely rely on ROI, can't take profit early
4. **Too Many Parameters**: Dozens of indicator parameters alone, optimizing is a headache
5. **Lots of Startup Data**: Needs 480 candles, about 5 days of data

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Slow Bull Uptrend | All on! | All three signals can work |
| 🔄 Wide Oscillation | Only signal_2 | Extreme oversold bounce opportunities are plentiful |
| 📉 One-sided Downtrend | Don't use | Long strategy in downtrend is just giving money away |
| ⚡ High Volatility | Reduce position | 20% stop loss easily triggered |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Review
> "A signal-heavy but logically clear trend strategy, suitable for patient hunters."

### Who Should Use It?
- ✅ Traders who like medium timeframes (15 minutes)
- ✅ People who can accept 20% stop loss width
- ✅ Technical traders willing to spend time on parameter optimization
- ✅ People who want flexible multi-signal combinations

### Who Shouldn't Use It?
- ❌ Intraday traders who want quick in-and-out
- ❌ Beginners who don't like complex indicator systems
- ❌ People with small capital who can't handle big volatility
- ❌ People seeking high win rate with tight stop losses

### My Recommendations
1. **Start with signal_1**: This signal has the most complete logic
2. **Stop loss can be lowered**: If you can't handle 20%, can change to 15%
3. **Backtest all three signals**: See which signal performs well on your pairs
4. **Small position testing**: Don't go all-in from the start, use small capital to break in first

---

## IX. What Market Can This Strategy Make Money In?

### 9.1 Core Logic: Building a "Trend Pullback Catcher" with Multiple Signals

Saturn5 is a trend strategy biased towards long positions. Its core is **buying at pullback positions in an uptrend**, not chasing highs.

**Its Money-Making Philosophy**: Go with the trend, enter on pullbacks

- **Multi-Period Confirmation**: From 3 EMA to 240 EMA, confirming trend layer by layer
- **Volume Verification**: VWMACD ensures it's not a "fake move"
- **Pullback Entry**: Don't chase highs, enter at pullback positions

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Slow Bull Trend | ⭐⭐⭐⭐⭐ | "This is home field, pullback entries work great" |
| 🔄 Wide Oscillation | ⭐⭐⭐☆☆ | "signal_2 can catch extreme oversold bounces" |
| 📉 One-sided Downtrend | ⭐⭐☆☆☆ | "Long strategy in downtrend is just giving money away" |
| ⚡ Violent Volatility | ⭐☆☆☆☆ | "20% stop loss may trigger frequently, protection mechanisms will frequently lock" |

**One-Sentence Summary**: **Eat meat in uptrends, drink northwest wind in downtrends.**

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Complaint |
|------------|-------------------|-----------|
| Timeframe | 15m | Don't change, this is the core of the strategy design |
| Stop Loss | -0.15 ~ -0.20 | Original is 20%, can tighten if too loose |
| ROI | 0.03 ~ 0.05 | 3-5% is fine, depends on how greedy you want to be |
| Simultaneous Positions | 10-30 | Don't be greedy, VPS will cry |

### 10.2 Key Configuration File Settings

```yaml
# Recommended Configuration
stake_amount: "3%-5% of total capital"
max_open_trades: 15
dry_run: true  # Run simulation first!
```

### 10.3 Hardware Requirements (Important!)

This strategy has many indicators, significant calculation load:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-30 pairs | 4GB | 8GB | Okay |
| 30+ pairs | 8GB | 16GB | Don't skimp |

**Warning**: Using low-spec VPS with too many pairs may cause calculation timeouts, missing signals! 😅

### 10.4 Backtesting vs Live Trading

In backtesting, all three signals might perform well, but in live trading note:

**Recommended Process**:
1. First backtest 1 year of data, see how each signal performs
2. Select the best-performing signal combination
3. Run dry_run for at least 1 month
4. Small position live testing
5. Only increase position after confirming stability

**Don't go all-in from the start**, no matter how good the strategy, it needs to be broken in!

---

## XI. Bonus: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **EMA Period Selection**: 3, 5, 10, 50, 240... 240 is 16 hours (approximately one trading day), this guy wants to use daily-level trends to guide 15-minute trading

   > "Big period for trend, small period for entry"

2. **Fibonacci 4.236**: This is an important Fibonacci extension position, the author wants to catch bounces after extreme oversold

   > "Fallen to this position, basically a golden pit"

3. **Protection Mechanism 0-Minute Cooldown**: Author didn't set a cooldown, probably thinking "if there's an opportunity after selling, should continue buying"

   > "Opportunities don't wait, just do it"

---

## XII. The Very Last

### One-Sentence Review
> "Saturn5 is an exquisitely designed trend strategy with three distinct signals and complete protection mechanisms. Suitable for traders who like medium timeframes and can accept relatively wide stop losses."

### Who Should Use It?
- ✅ People who like trend following strategies
- ✅ People who can accept 15-minute to several hours holding periods
- ✅ People willing to research different performance of three signals
- ✅ People who have time for backtesting and optimization

### Who Shouldn't Use It?
- ❌ People who like high-frequency short-term trading
- ❌ People who can't accept large stop losses
- ❌ People who don't want to study complex indicators
- ❌ People with too little capital (20% stop loss could cripple one trade)

### Manual Trader Recommendations
If you manually trade referencing this strategy, focus on:
1. **EMA 240 and EMA 50 relationship**: Determine major trend direction
2. **VWMACD golden cross**: Confirm momentum
3. **Bollinger lower band (3 standard deviations)**: Extreme oversold positions
4. **Volume**: Signals without volume support are just playing games

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Part)

### Backtesting is Beautiful, Live Trading Be Cautious

Saturn5's historical backtesting might look good, but note:

> **Each of the three signals has pros and cons, with numerous parameters, it's easy to "fit" the optimal solution for past market conditions, but this doesn't mean it will definitely profit in the future.**

Simply put: **Strategies with good historical performance don't necessarily mean good future performance.**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Signal Conflicts**: Three signals might simultaneously give different directional hints
- **Parameter Sensitivity**: Slightly change EMA period or Bollinger parameters, performance might be vastly different
- **Calculation Delay**: Too many indicators, large calculation load, might miss optimal entry timing
- **Overfitting Risk**: More parameters mean easier overfitting to historical data

### My Advice (Real Talk)

```
1. First backtest three signals separately, see which performs well
2. Only enable the well-performing signals, don't enable all
3. Stop loss can be appropriately tightened, like 15%
4. Must use simulation testing for at least 1 month first
5. Start with very small live positions, gradually increase
```

**Remember**: No matter how good the strategy, when the market teaches you a lesson, it won't give a heads up. Light position testing, staying alive is most important! 🙏

---