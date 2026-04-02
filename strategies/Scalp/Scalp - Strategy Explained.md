# Scalp Strategy: The 1-Minute 1% Little Bee

> **Nickname**: Mosquito Meat Harvester
> **Occupation**: Ultra-Short-Term Sniper
> **Timeframe**: 1 Minute (Fast enough, right?)

---

## I. What is This Strategy?

Simply put, **Scalp** is:
- 1-minute chart watching, run at 1% profit
- Use many small trades to cover occasional big losses
- Author recommends running 60+ pairs simultaneously

Like a hardworking little bee, only collecting a little nectar each time, but visiting many flowers means lots of honey. 🐝

---

## II. Core Configuration: Basically "Mosquito Meat is Still Meat"

### Take Profit Rule (ROI Table)

```
Profit ≥ 1% → Take profit immediately
```

**Translation**: See 1% profit and run, won't wait another second. Like picking up coins, grab and go.

### Stop Loss Rule

```
Loss ≥ 4% → Admit defeat!
```

**Translation**: Stop loss is 4 times the take profit! Like betting $1 to win $4, but losing costs $16. Need super high win rate to make money. 😅

---

## III. 1 Buy Condition: Simple and Brutal

This strategy has just one buy condition, super simple:

### 🎯 The Only Buy Signal

**Core Logic**: Oversold + Trend + Reversal Confirmation

**Plain English**:
> "Price opens below EMA, and ADX shows there's a trend (not random oscillation), Stochastic is already oversold, then K line crosses above D line, that's when I rush in!"

**Classic Lines**:

| Condition | Code | Plain English Translation |
|-----------|------|--------------------------|
| Condition 1 | `open < ema_low` | "Open price below EMA, meaning it's dropping" |
| Condition 2 | `adx > 30` | "ADX above 30, there's a trend, not random oscillation" |
| Condition 3 | `fastk < 30` | "K value below 30, oversold" |
| Condition 4 | `fastd < 30` | "D value also below 30, confirming oversold" |
| Condition 5 | `fastk crosses above fastd` | "K line crosses above D line, reversal signal!" |

**Simply Put**: **Dropped enough + Has trend + Starting to bounce = Buy!**

---

## IV. Sell Logic: Two Ways to Escape

### 4.1 Target Take Profit

```
Profit reaches 1% → Run!
```

**Plain English**: Make 1% and leave, no greed.

### 4.2 Active Sell Signals

There are two situations that trigger active selling:

| Signal | Condition | Plain English |
|--------|-----------|----------------|
| **EMA Take Profit** | `open >= ema_high` | "Price ran above EMA, time to go" |
| **Overbought Exit** | `fastk crosses above 70` | "K value above 70, overbought, run fast" |
| **Overbought Exit** | `fastd crosses above 70` | "D value also above 70, confirming overbought, run" |

**Plain English**:
- Price bounces to above EMA → Made enough, withdraw!
- Stochastic overbought → At the top, withdraw!

---

## V. Indicator System: Pitifully Simple

### 5.1 EMA Three Brothers

```
ema_high = EMA(5) of high price
ema_close = EMA(5) of close price
ema_low = EMA(5) of low price
```

**Plain English**: Use 5-period EMA to track high, close, and low prices separately, forming a "channel."

### 5.2 ADX Trend Strength

```
ADX > 30 → Has trend
ADX < 20 → No trend (oscillation)
```

**Plain English**: ADX is used to judge if there's a trend. Below 30, the strategy won't buy at all.

### 5.3 Stochastic Fast (Quick Stochastic)

```
K Period: 5
K Smoothing: 3
D Smoothing: 3
```

**Plain English**: Use the fast version of Stochastic, responds faster, suitable for 1-minute ultra-short-term.

### 5.4 Bollinger Bands (For Plotting Only)

```python
# This is for plotting, strategy logic doesn't use it!
bollinger = qtpylib.bollinger_bands(dataframe['close'], window=20, stds=2)
```

**Complaint**: The code calculates this, but buy and sell logic doesn't use it at all. Maybe the author forgot to delete it? 😅

---

## VI. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Section)

1. **Simple and Easy to Understand**: Just one buy condition, elementary school students can understand
2. **Fast Execution**: 1-minute cycle, quick in and out
3. **Clear Target**: 1% take profit, no hesitation
4. **Streamlined Indicators**: Just 3 core indicators, not flashy
5. **Suitable for Automation**: Clear rules, programs execute without pressure

### ⚠️ Cons (Complaint Section)

1. **Terrible Risk-Reward Ratio**: 4% stop loss, 1% take profit, need to win 4 times to cover 1 loss
2. **No Protection Mechanisms**: Nothing in the code, have to configure yourself
3. **Fees Eat You Alive**: High-frequency trading fees accumulate to scary amounts
4. **Needs Tons of Trading Pairs**: Author recommends 60+, high VPS cost
5. **Network Latency Sensitive**: 1-minute cycle, delay a bit and signal is wasted

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Uptrend | Suitable | Many pullback oversold bounce opportunities |
| 🔄 Oscillating Market | Not suitable | ADX < 30, strategy won't enter |
| 📉 Downtrend | Use with caution | Bounces might be weak, easy to stop out |
| ⚡ High Volatility | Super suitable | Oversold bounce opportunities galore |

---

## VIII. Summary: How's This Strategy Really?

### One-Sentence Review
> "A simple and brutal ultra-short-term strategy, clear logic but terrible risk-reward ratio, needs high win rate and large trading volume to support."

### Who Should Use It?
- ✅ People with low-fee channels (VIP, rebates, etc.)
- ✅ People who can run 60+ trading pairs (need good VPS)
- ✅ People with low network latency (close to exchange)
- ✅ People who accept high-frequency trading fees

### Who Shouldn't Use It?
- ❌ People with small capital (can't diversify risk)
- ❌ People with low-spec VPS (can't run 60+ pairs)
- ❌ People with high network latency (signals will fail)
- ❌ People who don't like high-frequency trading

### My Recommendations
1. **Must configure protection mechanisms**: This strategy has zero protection in the code!
2. **Fees must be low**: With 0.1% fees, 1% profit gets eaten by 20%
3. **Win rate must be high**: Stop loss is 4x take profit, below 80% win rate will lose money
4. **Test with simulation first**: Don't go live immediately, run dry_run first

---

## IX. What Market Can This Strategy Make Money In?

### 9.1 Core Logic: Use High Win Rate to Cover Terrible Odds

Scalp's core is **oversold bounce**. Its money-making philosophy:

> "Find oversold pits, wait for bounces, make 1% and run, lose 4% and accept it. Win by volume!"

- **Oversold Identification**: Stochastic Fast K/D < 30
- **Trend Filter**: ADX > 30 ensures there's direction
- **Quick Exit**: 1% take profit, no greed

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|---------------------------|
| 📈 Uptrend | ⭐⭐⭐⭐☆ | "Lots of pullback oversold opportunities, bounces easy to succeed" |
| 🔄 Oscillating Market | ⭐⭐⭐☆☆ | "ADX under 30 won't buy, misses oscillation opportunities" |
| 📉 Downtrend | ⭐⭐☆☆☆ | "Bounces very weak, easy to get stopped out" |
| ⚡ High Volatility | ⭐⭐⭐⭐⭐ | "Oversold bounce opportunities everywhere, home field!" |

**One-Sentence Summary**: **Eat meat in volatile trending markets, drink water in low-volatility oscillating markets.**

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Config Item | Recommended Value | Complaint |
|------------|-------------------|-----------|
| Timeframe | 1m | Don't change, this is the core |
| Simultaneous Positions | ≥ 60 | Less can't diversify risk |
| Stop Loss | -0.03 ~ -0.04 | Original is 4%, can tighten appropriately |
| Trading Fee | The lower the better | High fees will eat profits |

### 10.2 Must-Configure Protection Mechanisms

**This strategy has ZERO protection in the code!** You must add it yourself in config.json:

```json
{
  "protections": [
    {
      "method": "CooldownPeriod",
      "stop_duration": 5
    },
    {
      "method": "MaxDrawdown",
      "trade_limit": 20,
      "stop_duration": 60,
      "max_allowed_drawdown": 0.15
    },
    {
      "method": "StoplossGuard",
      "lookback_period": 60,
      "trade_limit": 3,
      "stop_duration": 30
    }
  ]
}
```

### 10.3 Hardware Requirements (Important!)

This strategy needs 60+ pairs, high VPS requirements:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 60 pairs | 4GB | 8GB | Barely enough |
| 100 pairs | 8GB | 16GB | Smooth |
| 150+ pairs | 16GB | 32GB | Don't skimp |

**Warning**: Using low-spec VPS with many pairs may cause calculation timeouts, missed signals! 😅

### 10.4 Fee Impact (Super Important!)

Ultra-short-term strategies are SUPER sensitive to fees:

```
Assuming 0.1% fee (buy + sell = 0.2%):
- Take profit 1%, fees eat 0.2%, actual profit 0.8%
- Fees are 20% of profit!

If fee is 0.2% (buy + sell = 0.4%):
- Take profit 1%, fees eat 0.4%, actual profit 0.6%
- Fees are 40% of profit!
```

**Recommendations**:
- Find low-fee exchanges (VIP, rebates)
- Must add fees in backtesting
- If fees are too high, this strategy might work for nothing

---

## XI. Bonus: The Strategy Author's "Little Secrets"

Looking carefully at the code, you'll find some interesting things:

1. **Bollinger Bands Calculated but Not Used**:
   ```python
   # Code calculates Bollinger Bands, but buy/sell doesn't use it at all
   bollinger = qtpylib.bollinger_bands(...)
   ```
   > "Maybe copy-pasted and forgot to delete? Or left for future expansion?"

2. **Recommends 60+ Trading Pairs**:
   > "we recommend to have at least 60 parallel trades at any time"
   
   The author directly tells you: This strategy has high risk running alone, needs the law of large numbers!

3. **Stop Loss is 4x Take Profit**:
   > "should not be below 3% loss"
   
   The author knows the stop loss is big, but that's ultra-short-term for you, small take profit, big stop loss.

---

## XII. The Very Last

### One-Sentence Review
> "Scalp is a simple and brutal ultra-short-term strategy, logic so clear even elementary students can understand, but terrible risk-reward ratio, needs high win rate and large trading volume to compensate."

### Who Should Use It?
- ✅ People with low-fee channels
- ✅ People who can run many trading pairs
- ✅ People with low network latency
- ✅ People who accept high-frequency trading fees
- ✅ People whose backtesting win rate reaches 70%+

### Who Shouldn't Use It?
- ❌ People with small capital
- ❌ People with low-spec VPS
- ❌ People with high network latency
- ❌ People with high fees
- ❌ People who don't like high-frequency trading

### Manual Trader Recommendations
If you manually trade referencing this strategy, focus on:
1. **Stochastic Fast < 30**: Oversold zone
2. **ADX > 30**: Has trend, not random oscillation
3. **K crosses above D**: Reversal signal
4. **1% Take Profit**: Don't be greedy, leave when reached

---

## XIII. ⚠️ Risk Re-emphasis (Must Read This Part)

### Backtesting is Beautiful, Live Trading Be Cautious

Scalp strategy backtesting might look great: make 1% each time, accumulating nicely. But note:

> **High-frequency trading fees and slippage are hidden killers. Backtest 1% take profit, live might only make 0.6%.**

Simply put: **Theory is beautiful, reality is harsh.**

### Risk-Reward Ratio is a Big Pit

This strategy's risk-reward ratio is 1:4:
- Need to win 4 times to offset 1 loss
- Need at least 80% win rate to break even
- After considering fees, need even higher win rate

### Hidden Risks of High-Frequency Trading

In live trading, high-frequency trading may cause:
- **Slippage Accumulation**: Each trade has slippage, accumulates to scary amounts at high frequency
- **Network Latency**: 1-minute cycle, signals are fleeting
- **Exchange Rate Limiting**: Too frequent may be restricted by exchange
- **Fee Erosion**: High-frequency trading fees are the biggest enemy

### My Advice (Real Talk)

```
1. Must add protection mechanisms (not in original code!)
2. Must find low-fee channels
3. Must add fees in backtesting
4. Test with simulation for at least 1 month first
5. Confirm win rate can reach 70%+ before live trading
6. Start with very small live positions
```

**Remember**: Stop loss is 4x take profit, need to win 4 times to cover 1 loss. If win rate isn't high enough, this strategy is a money-losing machine! 🙏

---