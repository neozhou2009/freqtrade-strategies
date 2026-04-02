# Ichimoku: The Japanese Zen of Cloud Walking

> **Nickname**: The Cloud Walker  
> **Profession**: Old-school trend following samurai  
> **Timeframe**: 5 minutes

---

## 1. What Is This Thing?

Simply put, **Ichimoku** is:

- A trend strategy using the Japanese classic technical analysis "Ichimoku Kinko Hyo"
- Finds entry points via Tenkan/Kijun golden cross
- Only goes long above the cloud, doesn't short below cloud

Like an old-school Japanese samurai, believes in "going with the trend, fighting above the cloud" 🗾

Ichimoku Kinko Hyo translates to "one glance equilibrium chart", Japanese naming is this direct — one look and you know where the trend is, no guessing needed.

---

## 2. Core Config: Basically "Chase Trend, Let Profits Fly"

### Profit-Taking Rules (ROI Table)

```python
minimal_roi = {"0": 1}  # Exit at 100% profit
```

**Translation**: 100% profit to exit? Bro, this is basically "I don't care", let trailing stop do the work. Strategy author's meaning is clear: **I don't predict take-profit points, trend goes as far as I go.**

### Stoploss Rules

```python
stoploss = -0.1  # -10% hard stoploss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01           # 1% trailing
trailing_stop_positive_offset = 0.02    # 2% trigger
trailing_only_offset_is_reached = True  # Only trigger after 2% profit
```

**Translation**:
- Admit defeat at 10% loss (hard stoploss)
- After making 2% profit, start trailing stoploss
- Pullback 1% from highest point, cash out

**In Plain English**: This stoploss logic is "I'm not greedy, but not afraid either". Follow when trend comes, run when trend reverses, typical trend following approach.

---

## 3. One Entry Condition: Simple and Direct

This strategy has only **1** entry condition, very simple:

### 🎯 TK Golden Cross + Cloud Confirmation

**Core Logic**: Tenkan-sen crosses above Kijun-sen from below, simultaneously price above cloud.

```python
# Entry conditions
(
    (dataframe["tenkan"].shift(1) < dataframe["kijun"].shift(1))  # Yesterday: Tenkan < Kijun
    & (dataframe["tenkan"] > dataframe["kijun"])                  # Today: Tenkan > Kijun
    & (dataframe["cloud_red"] == True)                            # Price above cloud
)
```

**In Plain English**:
> "Tenkan crosses above Kijun = short-term trend turning strong; price above cloud = long-term trend up. Both conditions met simultaneously, I enter long."

That's it. No complex condition combos, no dozens of parameters, just two indicators say hello, cloud nods, done.

---

## 4. Ichimoku: Zen of Five Lines

Ichimoku looks complex, actually just five lines:

| Indicator | Period | Calculation | In Plain English |
|-----------|--------|-------------|------------------|
| **Tenkan-sen (Conversion Line)** | 9 | 9-period high/low midpoint | "Short-term trend line, reflects price range center of last 9 candles" |
| **Kijun-sen (Base Line)** | 26 | 26-period high/low midpoint | "Medium-term trend line, reflects price range center of last 26 candles" |
| **Senkou Span A (Leading Span A)** | 26 | (Tenkan + Kijun) / 2, shifted 26 forward | "Cloud's upper boundary (or lower, depends on price position)" |
| **Senkou Span B (Leading Span B)** | 26 | 52-period high/low midpoint, shifted 26 forward | "Cloud's lower boundary (or upper)" |
| **Chikou Span (Lagging Span)** | - | Current close, shifted 26 backward | "Strategy doesn't use this line, but it's key for signal confirmation" |

**Cloud (Kumo)**: Area between Senkou Span A and B.

- Cloud up (A > B) = Green cloud = Bullish
- Cloud down (A < B) = Red cloud = Bearish

This strategy uses `cloud_red`, meaning price above cloud (bullish state).

**Plain English Understanding**:

Imagine cloud as a "territory":

- Price above cloud = Bull market, longs dominate
- Price below cloud = Bear market, shorts dominate
- Price inside cloud = Melee, nobody convinces anybody

Tenkan and Kijun are like two scouts:

- Tenkan runs fast (9-period), reacts quickly
- Kijun walks steady (26-period), represents main force direction

When Tenkan crosses above Kijun from below = "Scout caught up with main force, charge up together!"

---

## 5. Exit Logic: I Don't Predict, Let Market Tell Me

### 5.1 No Technical Exit Signals

This strategy's weirdest part: **No technical exit signals.**

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[(), "sell"] = 1  # Always allow exit, but no conditions
    return dataframe
```

**In Plain English**:
> "When to sell? I don't guess. When market reverses, trailing stop tells me."

This is typical trend following thinking: **Don't predict tops and bottoms, let profits run, exit when reverses.**

### 5.2 Trailing Stop: The Real Exit Mechanism

Although no technical exits, trailing stop is the "invisible sell":

| Stage | Profit | Trailing Stop |
|-------|--------|---------------|
| Just Entered | 0% - 2% | Not triggered, hard stoploss -10% |
| Profit Trigger | > 2% | Trailing stop triggered |
| Trend Continues | Keeps rising | Stoploss line moves up |
| Trend Reverses | Pullback 1% | Trigger stoploss, exit |

**In Plain English**:
- Made 2%, I start protecting profits
- Price keeps rising, stoploss follows up
- Drop 1% from highest point, run quickly

**Classic Lines**:
> "Trend is my friend, but friends can turn. I slip away before they turn."

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Section)

1. **Classic Indicator**: Ichimoku is decades-old Japanese classic, validated by countless markets
2. **Simple Logic**: Just one entry condition, won't give you "choice paralysis"
3. **Trend Filter**: Cloud confirmation ensures trend-following trades, won't counter-trend bottom fish
4. **Trailing Stop**: Suitable for trend markets, can lock most profits
5. **Clean Code**: Around 60 lines, beginners can understand

### ⚠️ Cons (Roast Section)

1. **No Exit Signals**: Completely relies on trailing stop, may miss active take-profit opportunities
2. **No BTC Correlation**: Doesn't detect Bitcoinmarket, independent trading has high risk
3. **Fixed Parameters**: 9/26/52 are classic parameters, but may not be optimal
4. **Chikou Span Unused**: Ichimoku has 5 lines, strategy only uses 4
5. **Example Nature**: Strategy is simple, suitable for learning, not for direct live trading

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **Slow Bull/Ranging Up** | ⭐⭐⭐⭐⭐ Highly Recommended | Ideal environment for trend following, cloud golden cross signals accurate |
| **One-Way Surge** | ⭐⭐⭐⭐ Recommended | Can catch most of trend, trailing take-profit protects profits |
| **Wide Ranging** | ⭐⭐ Not Recommended | Trend strategy gets whipsawed, stoploss frequent |
| **Extreme Sideways** | ⭐ Not Recommended | Too little volatility, basically no signals |
| **One-Way Crash** | ⭐⭐⭐ Okay | Cloud filter blocks most trades, auto lies flat |

**One Line**: This strategy likes directional trends, hates directionless ranging.

---

## 8. Summary: How Is This Strategy Really?

### One-Line Review
> **"Classic Ichimoku teaching case, logic simple and clear, suitable for beginner learning."**

### Who Should Use It?
- ✅ Beginners who want to learn Ichimoku
- ✅ Traders who like trend following
- ✅ People who don't want to be confused by complex conditions
- ✅ Those who believe in "let profits run" philosophy

### Who Should NOT Use It?
- ❌ Quant geeks who want complex strategies
- ❌ Counter-trend traders who like bottom fishing/top picking
- ❌ Short-term players chasing high-frequency trading
- ❌ People who need precise take-profit points

### My Recommendations
1. **As Learning Material**: This is the best Ichimoku beginner case
2. **Can Improve**: Add Chikou span confirmation, BTC correlation, technical exit signals
3. **Test Before Using**: Backtest, paper trading, small position live, step by step
4. **Parameters Adjustable**: 9/26/52 are classic parameters, but can optimize for different coins

---

## 9. What Markets Make Money With This?

### 9.1 Core Logic: Prosperity for Trend Followers

Ichimoku is a **trend following strategy**. Its money-making philosophy is simple:

> "Get on when trend comes, get off when trend reverses. Don't predict, just follow."

- **Cloud Confirmation**: Ensures only long when long-term trend up
- **TK Golden Cross**: Short-term trend also turning strong, entry timing suitable
- **Trailing Stop**: Let profits run, exit when trend reverses

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|------------|-------------------|--------------------------|
| 📈 Slow Bull/Ranging Up | ⭐⭐⭐⭐⭐ | "Cloud golden cross signals accurate, can catch most of trend, trailing stop protects profits" |
| 🔄 Wide Ranging | ⭐⭐☆☆☆ | "Trend strategy gets whipsawed, golden cross today death cross tomorrow, fees kill you" |
| 📉 One-Way Crash | ⭐⭐⭐☆☆ | "Cloud filter blocks most trades, auto lies flat. Occasionally may enter wrongly, but stoploss protects" |
| ⚡ Extreme Sideways | ⭐⭐☆☆☆ | "Too little volatility, basically no signals. Even if signals, they're false" |

**One-Line Summary**: Makes money in bull market, loses in ranging, lies flat in bear market. Trend strategy's fate.

### 9.3 Key Configuration Recommendations

| Config | Recommended Value | Description |
|--------|------------------|-------------|
| **Number of Pairs** | 20-40 pairs | Moderate signal frequency, not too few not too many |
| **Max Open Trades** | 3-6 orders | Trend strategy doesn't need too many positions |
| **Position Mode** | Fixed Position | Simple and brutal, fixed amount every entry |
| **Timeframe** | 5m | Mandatory, don't change |

---

## 10. Want to Run This? Check These Configs First

### 10.1 Pair Configuration

Strategy has no special restrictions, but recommend:

- Choose coins with trendiness (not those dead fish coins)
- Avoid overly correlated coins (like selecting multiple Layer2 simultaneously)
- Liquid major coins best

### 10.2 Key Config File Settings

```yaml
# config.json key settings
"max_open_trades": 3,
"stake_currency": "USDT",
"stake_amount": "unlimited",
"dry_run": true,  # Paper trade first!
"timeframe": "5m"
```

### 10.3 Hardware Requirements (Very Low!)

This strategy has minimal computation, Ichimoku just a few indicators:

| Pairs | Minimum RAM | Recommended RAM | Experience |
|-------|-------------|-----------------|------------|
| 20-40 | 512MB | 1GB | Smooth |
| 40-80 | 1GB | 2GB | Smooth |

**Warning**: Basically no warnings, this strategy is very hardware-friendly 😅

### 10.4 Backtest vs Live Trading

Ichimoku is a **lagging indicator**, backtest and live trading differences are small.

But note:
- Backtest signals very clear on historical data
- In live trading, cloud and TK lines change in real-time
- Recommend using `sell_signal` for strict confirmation

**Recommended Process**:
1. Backtest at least 3 months data
2. See performance in bull, ranging, bear markets
3. Paper trade 1-2 weeks
4. Small position live test
5. Gradually increase position

**Don't go all-in immediately**, no matter how simple the strategy needsbreak-in period!

---

## 11. Easter Egg: Ichimoku History

### 11.1 Inventor's Story

Ichimoku was invented by Japanese journalist **Goichi Hosoda** in 1930s. He spent 30 years researching and perfecting this system, pen name "Ichimoku Sanjin".

**"Ichimoku"** means "one glance to understand", "Kinko" is equilibrium, "Hyo" is chart.

**In Plain English**: A Japanese journalist spent 30 years creating this, you know how reliable this thing is.

### 11.2 Why Parameters Are 9/26/52?

| Parameter | Source | In Plain English |
|-----------|--------|------------------|
| 9 | Japanese traditional workdays | "Japan used to work 6 days/week, ~9 days = 1.5 months" |
| 26 | Japanese traditional month | "Japan used to have ~26 workdays/month" |
| 52 | Japanese traditional year | "Year ≈ 52 weeks ≈ 2 months workdays" |

**Roast**: These parameters are based on 1930s Japanese calendar, now crypto trades 7×24, do these parameters still apply?

Answer: **Still apply**. Because these parameters essentially capture short, medium, long trend time scales, unrelated to specific market.

### 11.3 Why Chikou Span Unused?

This strategy doesn't use Chikou Span, this is a small pity.

Chikou Span's function: Plot current price 26 candles back, used to confirm trend.

- Current price > 26 candles ago price = Bullish confirmation
- Current price < 26 candles ago price = Bearish confirmation

**If want to improve strategy**, can add Chikou span confirmation:

```python
# Recommend adding
& (dataframe["close"] > dataframe["close"].shift(26))  # Chikou confirmation
```

---

## 12. Final Final Words

### One-Line Review
> **"Textbook Ichimoku implementation, clear logic, clean code, best beginner case for learning trend following."**

### Who Should Use It?
- ✅ Beginners who want to learn Ichimoku
- ✅ Traders who like trend following
- ✅ People who don't want to be confused by complex conditions
- ✅ Those who believe in "let profits run" philosophy

### Who Should NOT Use It?
- ❌ Quant geeks who want complex strategies
- ❌ Counter-trend traders who like bottom fishing/top picking
- ❌ Short-term players chasing high-frequency trading
- ❌ People who need precise take-profit points

### Manual Trading Recommendations

If you're a manual trader, can reference this strategy's usage:

1. **Observe Cloud Direction**: Only long when price above cloud, only short when below cloud
2. **Wait for TK Golden Cross**: Enter when Tenkan crosses above Kijun
3. **Use Trailing Stop**: Set 1% trailing stop after 2% profit
4. **Combine with Chikou**: Current price > 26 candles ago price, confirm trend

---

## 13. ⚠️ Risk Reminder Again (MUST READ This Section)

### Backtests Are Beautiful, Live Trading Needs Caution

Ichimoku's historical backtest performance is often good — but here's a trap:

> **Trend strategies perform excellently in trending markets, but get whipsawed repeatedly in ranging markets.**

Simply put: **It's a god in bull market, it's leeks in ranging market.**

### Strategy's Hidden Risks

Note in live trading:

1. **No Technical Exits**: Completely relies on trailing stop, may miss active take-profit opportunities
2. **Lagging Indicator**: Ichimoku is lagging indicator, signals may be delayed
3. **Fixed Parameters**: 9/26/52 are classic parameters, but crypto market volatility is high, may need adjustment
4. **No BTC Correlation**: Doesn't detect Bitcoinmarket, altcoin signals may fail when BTC crashes
5. **Ranging Market Killer**: In wide ranging, TK golden/death cross frequent, fees eat profits

### My Recommendations (Real Talk)

```
1. Backtest first: At least 3 months data, cover bull, ranging, bear
2. Then paper trade: Run 1-2 weeks, observe signal quality
3. Then small position: Small position live test, don't exceed 5% of total capital
4. Slowly increase: After confirming strategy performs normally, gradually increase position
5. Add improvements: Consider adding Chikou confirmation, BTC correlation, technical exit signals
```

**Remember**: Ichimoku is a good indicator, but good indicators also need good markets. When trend comes, it takes you flying; when ranging comes, it takes you losing.

**Final Reminder**: No matter how classic the strategy, the market won't say hello before teaching you a lesson. Light positions for testing, survival is most important! 🙏
