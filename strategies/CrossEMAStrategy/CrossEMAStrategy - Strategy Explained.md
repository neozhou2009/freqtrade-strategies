# CrossEMAStrategy: The "Ultra-Minimalist" of Dual Moving Average Crossovers

> **Nickname**: The Elementary Schooler of Quantitative Trading / Simplest Trend Follower  
> **Specialty**: Making it in the trading world with just two EMA lines + one Stochastic RSI  
> **Timeframe**: 1 hour

---

## 1. What's This Strategy?

Simply put, **CrossEMAStrategy** is:
- A strategy with only **2 indicators** (EMA28 + EMA48 + Stochastic RSI)
- A strategy with only **1 buy condition**
- A strategy with only **1 sell condition**
- A strategy with **less than 100 lines** of code

It's like someone who decides whether to buy based purely on "reading the vibe" — simple and brutal, but sometimes surprisingly accurate! 😅

---

## 2. Core Configuration: Fast In, Fast Out

### Take-Profit Rules (ROI Table)

```
0-30 minutes: Exit at 10% profit!
30-60 minutes: Exit at 5% profit!
After 60 minutes: Exit at 2% profit!
```

**Translation**: This strategy is greedy — wants 10% right out of the gate! But it also knows when to fold — as time passes, the target gets lower and lower. Classic "take profits when you got 'em" 😅

### Stop-Loss Rules

```
Hard stop-loss: -99% (basically not set)
Trailing stop: Yes! Starts tracking from the moment you're profitable
```

**Translation**: The official rule says "cut losses at 99% down," but by the time you're down 99%, the trailing stop would've already bailed you out long ago. Basically: "Don't let me lose too much, or I'm out of here!" 🏃‍♂️

---

## 3. Buy Condition: Just 1, Simple to the Point of Crying

### Core Logic (Triple Filter)

```python
# Must satisfy all 3 conditions simultaneously:
1. EMA28 > EMA48  # Short-term MA above long-term MA (golden cross)
2. Stochastic RSI < 0.8  # Price in oversold zone, don't chase
3. Volume > 0    # Confirms real trading, not fake signals
```

**Plain English translation**:

1. **"Trend is up"**: Short-term MA crossed above long-term MA, the rally is starting
2. **"Price isn't too expensive"**: Stochastic RSI below 0.8, price hasn't run up too much
3. **"Trade is real"**: Volume supports it, not a fake breakout by market makers

**Classic line**:
> "Short-term MA beat long-term MA, and price hasn't rallied too much yet — load up!" 👍

---

## 4. Sell Condition: Also Just 1, Symmetrically Designed

### Core Logic

```python
# Must satisfy all 3 conditions simultaneously:
1. EMA28 < EMA48  # Short-term MA below long-term MA (death cross)
2. Stochastic RSI > 0.2  # Price in overbought zone, don't be greedy
3. Volume > 0    # Confirms real trade
```

**Plain English translation**:

1. **"Trend is down"**: Short-term MA fell below long-term MA, the rally is ending
2. **"Price is already expensive"**: Stochastic RSI above 0.2, price has rallied quite a bit
3. **"Trade is real"**: Volume confirms, not a fake breakout

**Classic line**:
> "Moving averages dead crossed, and price has rallied enough — take the money and run!" 💰

---

## 5. Technical Indicators: Just 3, You Can Count Them on One Hand

### Indicator List

| Indicator | Purpose | Plain English |
|-----------|---------|---------------|
| **EMA28** | 28-period Exponential Moving Average | Short-term MA, responsive |
| **EMA48** | 48-period Exponential Moving Average | Long-term MA, filters noise |
| **Stochastic RSI** | Momentum indicator | Tells if price is "overbought" or "oversold" |

### How EMA Crossover Works

```
Golden cross (Buy signal): EMA28 crosses from below to above EMA48
  → Short-term uptrend forming → BUY!

Death cross (Sell signal): EMA28 crosses from above to below EMA48
  → Short-term downtrend forming → SELL!
```

**Analogy**: Like watching marathon runners:
- **EMA28** is the **current leader's position** (short-term performance)
- **EMA48** is the **main group's position** (long-term trend)
- When the leader overtakes the main group → the rally is accelerating!
- When the leader gets caught by the main group → the rally is slowing down!

### What is Stochastic RSI?

```
Stochastic RSI = Apply "randomization" to RSI values one more time
- Value < 0.2: Oversold zone, may rebound
- Value > 0.8: Overbought zone, may correct
- Value in the middle: Wait and see
```

**Plain English**: Just think of Stochastic RSI as putting RSI through "beauty mode" — making overbought/oversold signals more sensitive!

---

## 6. The Strategy's "Personality"

### ✅ Pros

1. **Ultra-minimal code**: Under 100 lines, beginners can understand it
2. **Few parameters**: Only 2 parameters (buy/sell thresholds), easy to optimize
3. **Fast computation**: 3 indicators, computer barely breaks a sweat
4. **Double insurance**: Trend confirmation + momentum filtering reduces false signals
5. **History-backed**: Author provided backtest data from 2017-2021

### ⚠️ Cons

1. **No protection mechanism**: No independent risk control parameters
2. **Hard stop-loss is nominal**: -99% basically doesn't exist
3. **Single timeframe**: Only uses 1 hour, no multi-period confirmation
4. **May miss moves**: Stochastic RSI threshold too high may miss opportunities

---

## 7. When to Use It?

| Market Environment | Recommended Move | Reason |
|-------------------|------------------|--------|
| 📈 Strong uptrend | Keep default | EMA golden cross catches big waves |
| 📉 Strong downtrend | Keep default | Death cross exits timely |
| 🔄 Ranging market | Tighten parameters | Reduce false signals |
| ⚡️ Fast volatility | 10% target | Good for fast in/fast out |
| 😴 Dead consolidation | Reduce trading pairs | MA crossovers frequent, may over-trade |

---

## 8. Parameter Tuning: Just 2 Parameters, Ridiculously Simple

### Adjustable Parameters

| Parameter | Default | Range | Adjustment Suggestion |
|-----------|---------|-------|----------------------|
| **buy_stoch_rsi** | 0.8 | 0.5-1.0 | Lower = more conservative, requires deeper oversold to buy |
| **sell_stoch_rsi** | 0.2 | 0-0.5 | Higher = more conservative, requires higher overbought to sell |

### Parameter Adjustment Examples

**Conservative version** (reduce false signals):
```python
buy_stoch_rsi = 0.6   # Require deeper drop before buying
sell_stoch_rsi = 0.4  # Require higher rally before selling
```
> "I'll wait for a bigger dip before buying, and a bigger rally before selling!"

**Aggressive version** (catch more moves):
```python
buy_stoch_rsi = 0.9   # Buy even if price hasn't dropped much
sell_stoch_rsi = 0.1  # Sell even if price hasn't rallied much
> "Just signal and we go!"

---

## 9. What Markets Does This Make Money In?

### 9.1 Core Logic: Simple and Brutal Trend Following

CrossEMAStrategy is the **simplest-coded** strategy in the Freqtrade ecosystem, period. Under 100 lines of code — think of it as a single tweet's length! 📱

**Its money-making philosophy**: "Jump on when you see a trend, get off when the trend ends"

- **EMA crossover**: The most classic trend judgment indicator
- **Stochastic RSI**: Filters out "fake breakouts," avoids chasing
- **No protection**: Trust the trend, let the market decide

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English Explanation |
|:-----------|:------:|--------------------------|
| 📈 Strong uptrend | ⭐⭐⭐⭐⭐ | Golden cross signals are accurate, catches big waves |
| 📉 Strong downtrend | ⭐⭐⭐⭐ | Death cross exits timely, avoids big drops |
| 🔄 Wide-range oscillation | ⭐⭐⭐ | MA crossovers frequent, may get slapped around |
| ⚡️ Fast volatility | ⭐⭐⭐⭐ | 30-minute 10% target great for fast moves |
| 📊 Consolidation | ⭐⭐ | Too many crossover signals, may over-trade |

**One-liner**: This strategy performs best in **clearly trending** markets and gets "slapped from both sides" in **sideways oscillation**! 🤕

---

## 10. Before Running This Strategy: Check These Configs

### 10.1 Key Parameter Configuration

| Config Item | Default | Suggestion | Notes|
|------------|--------|------------|---|
| buy_stoch_rsi | 0.8 | 0.7-0.9 | Default 0.8 is pretty reasonable |
| sell_stoch_rsi | 0.2 | 0.1-0.3 | Default 0.2 is a bit conservative |
| minimal_roi."0" | 0.10 | 0.08-0.15 | Want 10%? Depends on the market |
| timeframe | 1h | Keep it | Strategy designed specifically for 1h |

### 10.2 Configuration File Example

```python
# Strategy Configuration
crossemasstrategy:
  buy_stoch_rsi: 0.8
  sell_stoch_rsi: 0.2

# Risk Configuration
minimal_roi:
  "0": 0.10
  "30": 0.05
  "60": 0.02

stoploss: -0.99
trailing_stop: true
```

### 10.3 Hardware Requirements

This strategy has minimal computational demands:

| # of Trading Pairs | Min RAM | Recommended RAM | Experience |
|-------------------|---------|-----------------|-----------|
| 10-50 pairs | 512MB | 1GB | Light and breezy |
| 50-100 pairs | 1GB | 2GB | No problem at all |
| 100+ pairs | 2GB | 4GB | More than enough |

**Rest assured**: This strategy runs lighter than texting on WeChat! 😄

### 10.4 Backtest vs Live Trading

**Common issues**:
- Backtest: Simple parameters, hard to overfit
- Live: Stochastic RSI may fail in extreme market conditions
- Slippage: 1-hour timeframe, limited slippage impact

**Suggested process**:
1. Backtest with default params (at least 6 months of data)
2. Observe strategy performance across different market environments
3. Adjust stoch_rsi thresholds based on trading pair characteristics
4. Small-capital live validation (at least 2 weeks)

---

## 11. Risk Reminders: Hidden Pitfalls of Simple Strategies

### 11.1 No Independent Protection Mechanism

This strategy lacks:
- ❌ Capital protection parameter
- ❌ Volatility protection
- ❌ Independent maximum holding time

**Risk**: Extreme moves may cause significant losses!

### 11.2 Hard Stop-Loss Is Nominal

```python
stoploss = -0.99  # Cut losses at 99% down
```

This is essentially meaningless! All actual risk control depends on the trailing stop.

**Suggestion**: If you're worried about extreme moves, manually set a stricter stop-loss, e.g., -15%

### 11.3 Limitations of Single Timeframe

Only using 1-hour period may:
- Miss trends on larger timeframes
- Be interfered with by short-term noise

**Suggestion**: If possible, use a longer timeframe as reference

---

## 12. The Bottom Line

### One-Line Rating
> "The 'Elementary Schooler' of quantitative trading — simplest and most brutal trend-following strategy"

### Who Should Use It?
- ✅ Beginners (code is simple, easy to pick up)
- ✅ Lazy folks (few parameters, no fussing needed)
- ✅ Speed chasers (fast computation, minimal resource usage)
- ✅ Experienced quants (as a benchmark strategy, for quick screening)

### Who Shouldn't?
- ❌ People seeking complex risk control (strategy is too simple)
- ❌ People who like multi-period analysis (only 1h)
- ❌ People worried about extreme moves (no hard protection)

### Manual Trading Recommendations

If you don't want to use automation, watch for these signals:
1. **EMA28 crosses above EMA48** → Trend turning up, prepare to buy
2. **Stochastic RSI < 0.8** → Price hasn't rallied too much yet
3. **EMA28 crosses below EMA48** → Trend turning down, prepare to sell
4. **Stochastic RSI > 0.2** → Price has rallied enough already

**Remember**: Follow the trend, don't fight it! 🚢

---

## ⚠️ Risk Reiteration (Must Read)

### Backtests Look Great, Live Trading Is Another Story

CrossEMAStrategy's historical backtest data comes from 2017-2021, which was crypto's **big bull market**. In bear or ranging markets, strategy performance may be significantly worse!

> **The simple strategy trap**: Don't think that just because it's simple, it can't lose money in the wrong market environment!"

### Simple Strategy Risks

1. **No protection mechanism**: No "safety belt" in extreme moves
2. **Fixed parameters**: Default parameters may not suit all trading pairs
3. **Trend-dependent**: Makes money in one-sided moves, loses in ranging markets

### My Recommendations (Sincere Advice)

```
1. Run with default params first, observe for at least 1 month
2. Test with small money — big gap between backtest and live is possible
3. Watch market environment — only use when trends are clear
4. Suggest setting external risk control, e.g., -15% hard stop
5. Don't be greedy — simple strategies especially need to take profits when available
```

**Remember**: The simpler the strategy, the more you must respect the market! Test with small capital — survival is what matters! 🙏

---

**Final reminder**: Dual moving average crossover is the **most classic** trend strategy, but that doesn't make it **the most perfect**. Learn to read trends, but also learn when to rest! 👋
