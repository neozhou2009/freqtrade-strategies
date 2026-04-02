# Renko Strategy: Reading Trends with "Tetris"

> **Nickname**: Tetris  
> **Profession**: Trend Observer (speaks in bricks)  
> **Timeframe**: 15 minutes

---

## 1. What Is This Strategy?

Simply put, **Renko** is a strategy that:
- Uses "brick charts" instead of candlestick charts
- Only looks at price changes, ignores the passage of time
- Enters when the trend changes, exits when the trend ends

Like **Tetris** 🧱 — stacking brick by brick, green bricks for uptrends, red bricks for downtrends, simple and intuitive!

---

## 2. Core Configuration: "Give the Trend Time, But Don't Get Greedy"

### Take-Profit Rules (ROI Table)

```
Just entered        → Take profit at 10%
Held for 30 min     → Take profit at 5%
Held for 60 min     → Take profit at 2%
```

**Translation**:
> "I'll give you time for the trend to develop, but the longer it takes, the more anxious I get. At the start I want 10%, after 30 minutes 5% is fine, after another half hour even 2% will do — let's cash out!"

### Stop-Loss Rules

```
Loss ≥ 10% → Cut losses and exit
```

**Translation**:
> "If I lose 10%, I admit defeat. No more nonsense."

---

## 3. Renko Brick Charts: Turning Candlesticks into "Building Blocks"

### 3.1 What Is a Renko Chart?

Regular candlestick chart: One candle per time period, regardless of whether price changed.

Renko chart: **Only draw a brick when price moves enough**.

```
Uptrend (Green Bricks):
┌─────┐
│ 🟢 │  Price increased by more than 1 brick
├─────┤
│ 🟢 │  
├─────┤
│ 🟢 │
└─────┘

Downtrend (Red Bricks):
┌─────┐
│ 🔴 │  Price decreased by more than 1 brick
├─────┤
│ 🔴 │
└─────┘
```

**In Plain English**:
> "Candlestick charts look at time — draw one candle every 15 minutes. Renko looks at price — only draw a brick when price moves enough. This filters out those annoying small fluctuations!"

### 3.2 How Is Brick Size Determined?

**Dynamic Calculation**: Use the mean of ATR (Average True Range)

```python
brick_size = Average ATR
```

**In Plain English**:
> "Brick size isn't fixed — it's determined by market volatility. High-volatility coins get bigger bricks, low-volatility coins get smaller bricks. Automatic adaptation!"

### 3.3 Trend Reversal Rules: Need 2 Bricks to Confirm

This is the smartest part of Renko:

| Current Trend | Reversal Condition | Description |
|--------------|-------------------|-------------|
| Upward (Green Bricks) | Decline of 2 bricks | Only then confirms downtrend |
| Downward (Red Bricks) | Increase of 2 bricks | Only then confirms uptrend |

**In Plain English**:
> "When the trend changes, one brick isn't enough — need 2 consecutive bricks in the opposite direction to confirm. This way you won't get fooled by false breakouts!"

---

## 4. Buy Conditions: 2 Situations to Enter

The strategy has 2 buy signals, which basically means:

### 🎯 Signal #1: Upward Trend Reversal

```
Previous brick was red (downtrend) → Current is green (uptrend)
```

**In Plain English**:
> "The trend was going down before, now it's turning up. Reversal confirmed, get in!"

### 🎯 Signal #2: Trend Continuation

```
Previous brick was green (uptrend) → Current is still green (uptrend)
```

**In Plain English**:
> "The trend is still going up, keep holding or add to your position!"

---

## 5. Sell Logic: Run When the Trend Ends

### 5.1 Trend Reversal Sell

```
Current trend turns red (downtrend) → Sell
```

**In Plain English**:
> "Green bricks turned to red bricks, trend reversed downward, run!"

### 5.2 Tiered Take-Profit: More Anxious as Time Passes

| Holding Time | Take-Profit Threshold | Mindset |
|-------------|----------------------|---------|
| Just entered | 10% | "Let the bullets fly for a while" |
| After 30 min | 5% | "About time, right?" |
| After 60 min | 2% | "Let's go already, don't dawdle" |

**In Plain English**:
> "When I first enter, my expectations are high — I want 10%. But the longer it takes, the more anxious I get. I'll give you 60 minutes, even 2% is fine, let's cash out!"

### 5.3 Profit Protection Mechanism

```python
sell_profit_only = True  # Only respond to sell signals when profitable
```

**In Plain English**:
> "Don't rush to sell when losing — wait until we break even first. Only start considering take-profit when we're in profit."

---

## 6. This Strategy's "Personality Traits"

### ✅ Strengths (Praise Session)

1. **Intuitive and Clear**: Brick colors show trend direction, even a dummy can understand
2. **Filters Noise**: Small fluctuations don't create bricks, much cleaner
3. **Strict Reversal Confirmation**: Needs 2 bricks to confirm, hard to fool
4. **Self-Adaptive**: Brick size automatically adjusts with market volatility

### ⚠️ Weaknesses (Complaint Session)

1. **Ignores Time**: May react slowly in fast-moving markets
2. **Sucks in Low Volatility**: Too many bricks in quiet markets, signals flying everywhere
3. **Complex Calculation**: Converting raw data to Renko data is brain-intensive
4. **Data Structure Changed**: Output isn't original candlesticks, watch out during backtesting

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Clear Trend | 🚀 Go heavy | Renko is excellent at capturing trends |
| Ranging/Sideways | 🛌 Lie flat and wait | Bricks change color frequently, many false signals |
| High Volatility Jumping | 🤔 Be cautious | Brick size may not keep up with changes |
| One-Way Big Rise/Fall | ✅ Perfect | Clear trend direction, Renko shines |

---

## 8. Summary: How Is This Strategy Really?

### One-Sentence Review
> "Using Tetris to read trends — simple and intuitive, but ranging markets will kill you."

### Who Should Use It?
- ✅ Those who like trend trading
- ✅ Those who hate candlestick chart noise
- ✅ Suitable for manual trading too
- ✅ Those who can accept tiered take-profit

### Who Should NOT Use It?
- ❌ Those wanting to make money in ranging markets
- ❌ Those pursuing extreme entry/exit precision
- ❌ Low-volatility coin lovers
- ❌ Those who don't want to learn new chart types

### My Recommendations
1. **Learn to read Renko charts first**: It's a unique chart type that needs adaptation
2. **Suitable for trending markets**: Use cautiously in ranging markets
3. **Can combine with candlestick charts**: Using both together works better
4. **Manual trading works too**: Unlike other strategies that are quant-only

---

## 9. In What Markets Can This Strategy Make Money?

### 9.1 Core Logic: Using Bricks to See Trends Clearly

Renko is a typical **trend-following strategy**. Its profit philosophy:

> "I don't care how long the rise or fall lasts — I only care if the trend changed. Green bricks = long, red bricks = run!"

- **Filter Noise**: Small fluctuations don't draw bricks, cleaner
- **Clear Trend**: Brick colors show direction at a glance
- **Strict Reversal Confirmation**: 2 bricks to confirm, hard to fool

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Clear Trend | ⭐⭐⭐⭐⭐ | Bricks stay the same color, just follow along |
| 🔄 Ranging/Sideways | ⭐⭐☆☆☆ | Bricks keep changing color, slaps both ways |
| 📉 Downtrend | ⭐⭐⭐⭐☆ | Red bricks appear and you run — don't get hurt |
| ⚡️ High Volatility | ⭐⭐⭐☆☆ | Brick size changes with it, can get messy |

**One-Sentence Summary**: Like a fish in water during clear trends, gets slapped around in ranging markets.

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Key Parameters

| Parameter | Default Value | Comment |
|-----------|--------------|---------|
| ATR Period | 5 | Used to calculate brick size, don't mess with it |
| Timeframe | 15m | Standard, can try 1h |
| Stop-Loss | 10% | Gives enough breathing room |

### 10.2 Key Settings in Config File

```yaml
# Take-Profit (Tiered)
minimal_roi:
  "0": 0.10    # Just entered: 10%
  "30": 0.05   # After 30 min: 5%
  "60": 0.02   # After 60 min: 2%

# Stop-Loss
stoploss: -0.10

# Timeframe
timeframe: 15m

# Sell Signal Settings
use_sell_signal: True
sell_profit_only: True
ignore_roi_if_buy_signal: True  # Keep holding if buy signal present
```

### 10.3 Hardware Requirements

| Number of Trading Pairs | Minimum RAM | Recommended RAM | Experience |
|------------------------|-------------|-----------------|------------|
| Below 10 | 2 GB | 4 GB | Smooth |
| 10-50 | 4 GB | 8 GB | Okay |
| Above 50 | 8 GB | 16 GB | Stable |

### 10.4 Backtesting vs Live Trading

**Backtesting Notes**:
- Strategy outputs Renko dataframe, not original candlesticks
- Be aware of data structure changes

**Live Trading Notes**:
- Renko bricks are calculated in real-time
- ATR changes, so brick size changes too

---

## 11. Easter Egg: Renko History and Fun Facts

### 11.1 Name Origin

"Renko" comes from Japanese "練行足" (renko-ashi), meaning "brick chart".

**In Plain English**:
> "The Japanese invented this thing, so they call it Renko. You can call it 'brick chart' if you want — nobody will stop you."

### 11.2 Why 2 Bricks for Reversal?

Because 1 brick might be a false breakout, 2 bricks confirm the reversal.

**In Plain English**:
> "Like when your girlfriend says 'break up' — the first time might be anger, the second time it's real."

---

## 12. Last But Not Least

### One-Sentence Review
> "Reading trends with brick charts — simple and intuitive, use cautiously in ranging markets."

### Who Should Use It?
- ✅ Those who like trend trading
- ✅ Those who hate candlestick noise
- ✅ Manual traders who want to use it
- ✅ Those who can accept tiered take-profit

### Who Should NOT Use It?
- ❌ Those wanting to make money in ranging markets
- ❌ Those pursuing extreme precision
- ❌ Low-volatility coins
- ❌ Those who don't want to learn new things

### Manual Trader Recommendations
**Highly recommend manual traders learn Renko charts**:
- Brick colors are crystal clear
- Entry/exit signals are explicit
- Can be used together with candlestick charts
- Filters noise, steadier mindset

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtesting Looks Great, Be Cautious in Live Trading

Renko strategy performs well in clear trends, but **ranging markets are its nightmare**:

> **Bricks change color frequently, slaps both ways, fees eat profits.**

### Hidden Risks of Complex Strategies

In live trading, watch out for:
- **Data transformation issues**: Outputs Renko data, not original data
- **Brick size changes**: ATR changes, brick size changes too
- **False signals in ranging markets**: Bricks keep changing during sideways movement

### My Recommendations (Honest Truth)

```
1. Test in ranging markets first — see if it can handle it
2. Only use on coins with clear trends
3. Manual trading works too — don't just think quant
4. Combine with candlestick charts — works better
```

**Remember**: Renko is a tool to see trends clearly, not a guarantee of profit. It's a godsend in clear trends, a pit in ranging markets!

---

**Final Reminder**: No matter how good the strategy, the market won't say hello before teaching you a lesson. Light positions for testing — staying alive is most important! 🙏

---
