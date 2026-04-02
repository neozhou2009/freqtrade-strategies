# Strategy001_custom_sell: EMA + RSI Profit-Taking Enhanced Edition

> **Nickname**: "The Moving Average School That Knows How to Sell Itself"  
> **Profession**: Trend Following + Active Profit Taking Expert  
> **Timeframe**: 5 minutes

---

## I. What Is This Strategy?

Simply put, **Strategy001_custom_sell** is:
- Strategy001 with RSI custom exit added
- EMA golden cross entry, RSI overbought profit taking
- Added a "smart selling" feature

Like a **driving school practice car with automatic braking** 🚗💨 — keeps the beginner-friendly features, plus a life-saving feature!

---

## II. What's the Difference from Strategy001?

| Feature | Strategy001 | Strategy001_custom_sell |
|---------|-------------|------------------------|
| Entry Logic | EMA golden cross + HA confirmation | **Same** |
| Exit Logic | EMA death cross signal | EMA death cross **+ RSI overbought exit** |
| Profit Taking Style | Passive wait for signal | **Active profit taking** |
| Capital Efficiency | Average | **Higher** |

**Plain English**: Strategy001 "dumbly waits for sell signals", this one "looks at the situation and actively runs"!

---

## III. Core Configuration: Identical to Strategy001

### Take Profit Rules (ROI Table)

```
Holding Time    Target Profit
────────────────────
Immediate       5%
20 minutes      4%
30 minutes      3%
60 minutes      1%
```

**Translation**: Made enough? Run. The longer you hold, the lower the target 💰

### Stop Loss Rules

```
Fixed Stop Loss: -10% (Lose 10% and surrender)
Trailing Stop: Activates at 2% profit, exits on 1% pullback
```

---

## IV. Entry Condition: Exactly Same as Strategy001

### 🎯 The Only Entry Condition: EMA Golden Cross + HA Confirmation

**Plain English**:
> "When EMA20 crosses above EMA50, check if the HA candle is green and price is above EMA20. If all three conditions are met, buy!"

**Code looks like this**:
```python
EMA20 crosses above EMA50      # Golden cross signal
HA close > EMA20               # Price above moving average
HA open < HA close             # Green candle
```

**Exactly same as Strategy001, won't expand here.**

---

## V. Exit Logic: Here's the New Stuff!

### 5.1 Base Exit Signal (Same as Strategy001)

**Plain English**:
> "EMA50 crosses above EMA100, price below EMA20, HA candle turned red? Then run!"

### 5.2 New! RSI Custom Exit 🎉

This is the core upgrade of this strategy!

**Plain English**:
> "RSI above 70? Still profitable? Then actively sell, don't wait for moving average death cross!"

**Code looks like this**:
```python
def custom_sell(...):
    if (RSI > 70) and (current profit > 0):
        return "rsi_profit_sell"  # Sell!
```

**What Does This Mean?**
- RSI > 70 = Recent gains too big, might pull back
- Profit > 0 = Only sell when making money
- Active sell = Don't wait for MA signal, lock in profits early

### 5.3 Three Exit Methods Comparison

| Exit Method | Trigger Condition | Plain English |
|-------------|-------------------|---------------|
| ROI Exit | Time + profit target met | "Made enough, run" |
| Trailing Stop | Pullback after profit | "Don't give back profits" |
| **RSI Exit** | **RSI > 70 and profitable** | **"Rose too fast, secure gains first"** |

---

## VI. This Strategy's "Personality"

### ✅ Pros (Compliment Time)

1. **Active Profit Taking**: When rising too fast, actively run, don't wait for trend reversal
2. **High Capital Efficiency**: Early profit taking releases capital, can do more trades
3. **Code Still Clean**: Only a few more lines than Strategy001

### ⚠️ Cons (Roast Time)

1. **Strong Trend FOMO**: In a big bull market, RSI might stay overbought for a long time, sell and can't buy back 😭
2. **Fixed RSI Threshold**: 70 might not suit all coins
3. **Oscillating Market Still Sucks**: RSI keeps hitting overbought and selling, fees eat profits

---

## VII. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| 📈 Clear Trend | Run with confidence | EMA golden cross + HA green bars work perfectly |
| 🔄 Volatile Market | **Recommended!** | RSI exit takes profits early on spike pullbacks |
| 📉 Downtrend | Don't touch | Long strategy going against trend is dangerous |
| ⚡ Strong Trend Bull Market | Raise RSI threshold | Avoid selling too early and missing gains |

---

## VIII. Summary: How Good Is This Strategy?

### One-Line Review
> "Smart version of Strategy001, knows when to actively run"

### Who Is It For?
- ✅ People already familiar with Strategy001
- ✅ People wanting to learn custom_sell function
- ✅ People wanting early profit taking in volatile markets
- ✅ People wanting to improve capital turnover rate

### Who Is It NOT For?
- ❌ People afraid of missing gains in strong trend bull markets
- ❌ People not wanting to learn new things
- ❌ Victims of oscillating markets
- ❌ Lazy people wanting to lie back and profit

### My Recommendation
1. **Run Strategy001 first**: Get familiar with basic logic
2. **Then try this version**: Experience the RSI profit taking effect
3. **Compare backtest results**: See which one fits your coins better
4. **Adjust RSI threshold**: Tune that 70 parameter based on market conditions

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Using RSI to Catch Spike and Pullback

Strategy001_custom_sell is an **enhanced trend following strategy**. Adding RSI profit taking on top of Strategy001 makes it **perform better in volatile markets**.

**Its Profit Philosophy**: Follow the trend when it comes, actively run when rising too fast.

- **Moving Average Cross**: Identify trend initiation
- **HA Candles**: Filter false breakouts
- **RSI Overbought**: Rising too hard? Take profits first

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|-------------|-------------------|--------------------------|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | Home turf! But RSI exit might make you earn less |
| 🔄 Volatile Market | ⭐⭐⭐⭐☆ | **This is its advantage!** Run on spikes |
| 📉 Downtrend | ⭐☆☆☆☆ | Long strategy against trend, forget about profits |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | RSI frequently overbought, might sell too early |

**One-Line Summary**: Catch spikes in volatile markets, might miss gains in strong trends!

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Comment |
|-------------------|-------------------|---------|
| Trading Pairs | Major coins | Good liquidity, low slippage |
| Timeframe | 5m (default) | Can try 15m to reduce noise |
| RSI Threshold | 70-80 | Bull market can raise to 80 |

### 10.2 Config File Key Settings

```yaml
# config.json key settings
"max_open_trades": 3,
"stake_currency": "USDT",
"stake_amount": "unlimited",
"dry_run": true,  # Paper trade first!
```

### 10.3 Hardware Requirements (Easy)

Same as Strategy001, this strategy has minimal computation:

| Number of Trading Pairs | Minimum Memory | Recommended Memory | Experience |
|------------------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-30 pairs | 4GB | 8GB | Fluid |

### 10.4 Backtest vs Live Trading

**Special Note**: RSI custom exit may perform differently in backtesting vs live trading:

- **In Backtesting**: RSI signal triggers precisely
- **In Live Trading**: Limit orders might not execute, missing best exit points
- **In Strong Trends**: RSI stays overbought for long time, sell and can't buy back

**Recommended Process**:
1. Paper trade compare both versions
2. Observe RSI exit frequency and effectiveness
3. Adjust RSI threshold per coin
4. Small position live trading validation

---

## XI. Bonus: "Little Tricks" in the Code

Look carefully at the custom_sell function, you'll find:

```python
if (current_candle['rsi'] > 70) and (current_profit > 0):
    return "rsi_profit_sell"
```

**Interesting Points**:

1. **Only Sell When Profitable**: `current_profit > 0` ensures no selling at loss
   > "Don't chase sells when losing money, let stop loss handle it"

2. **Returns Exit Reason**: `"rsi_profit_sell"` for easy analysis
   > "Know it was RSI-triggered exit, convenient for backtest optimization"

3. **Simple and Direct**: Only two lines of core logic
   > "If one line can do it, never write two"

---

## XII. Final Words

### One-Line Review
> "Smart version of Strategy001, but might make you earn less in strong trends"

### Who Is It For?
- ✅ People who've mastered Strategy001
- ✅ People wanting to learn custom_sell
- ✅ People wanting early profit taking in volatile markets
- ✅ People wanting to improve capital turnover rate

### Who Is It NOT For?
- ❌ People afraid of missing gains in strong trend bull markets
- ❌ Victims of frequent stop losses in oscillating markets
- ❌ People not wanting to learn new things
- ❌ Lazy people wanting to lie back and profit

### Manual Trader Recommendations

If using this logic manually:
1. Wait for EMA20 to cross above EMA50
2. Confirm Heikin Ashi green candle
3. Price holding above EMA20
4. Set trailing stop
5. **New**: Watch RSI, consider profit taking when above 70 and profitable
6. **Note**: In big bull markets, might want to wait for RSI to hit 80 before selling

---

## XIII. ⚠️ Risk Emphasis Again (Must Read This)

### RSI Profit Taking is a Double-Edged Sword

RSI custom exit may perform well in backtesting—but there's a trap:

> **In strong trends, RSI may stay overbought for extended periods. Early exit means missing big moves.**

Simply put: **Sell when it rises, it keeps rising after you sell, you'll kick yourself!** 🦵

### Hidden Risks of Enhanced Strategy

In live trading, RSI exit may encounter:
- **FOMO Risk**: Sell then it keeps rising, mentality breaks
- **Frequent Trading**: RSI keeps going overbought/oversold, fees eat profits
- **Limit Orders Not Executing**: Want to sell but price already dropped

### My Recommendation (Real Talk)

```
1. First compare backtest results of Strategy001 and this version
2. See if RSI exit actually helped you earn more or less
3. Adjust RSI threshold based on coin characteristics (70 isn't universal)
4. In strong trend markets, consider raising threshold to 75-80
5. In oscillating markets, consider lowering threshold or not using RSI exit at all
```

**Remember**: RSI overbought doesn't mean it will definitely drop, it might just be rising too hard. Strategies are dead, markets are alive!

---

**Final Reminder**: Enhanced version doesn't mean enhanced returns, adjust based on market conditions. Test with small positions, survival is most important! 🙏