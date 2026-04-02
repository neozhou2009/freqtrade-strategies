# Cluc5werk Strategy Explained

> **Read This and Get It Instantly** | Bollinger Bands + ROCR Trend Filter + Dual Confirmation 1-Minute Short-Term Hunter

---

## 1. What's This Strategy All About?

**Cluc5werk** is the **5th generation evolution** of the Cluc series; plays **1-minute ultra short-term**, but adds several power moves:

> "First check big picture (1-hour trend up), then find entry points (Bollinger Band signals), finally **confirm twice** before acting"

Plainly:

1. First confirm big trend — use **1-hour ROCR indicator** to judge if market is rising
2. Then find entries — use **Bollinger Bands** to find where price fell to the "floor"
3. **Confirm twice** — must have two consecutive candles satisfying conditions before buying
4. Fast entry/exit — sell when price touches BB middle band or three consecutive drops

This strategy is like an **extremely cautious short-term hunter**: only looks for opportunities when direction is right; requires two confirmations even when opportunities appear; acts only after careful confirmation. Its personality — **steady as an old dog; 90%+ win rate**.

---

## 2. Core Settings: Basically "High Win Rate + Wide Stop-Loss"

### 2.1 Take-Profit Rule (ROI Table)

| Holding Time | Target Profit | Plain English |
|-------------|---------------|---------------|
| Immediate | 2.13% | Want 2% the moment entering |
| 275 minutes | 1.75% | About 4.5 hours later, lower expectations |
| 559 minutes | 1.62% | About 9 hours later, more conservative |
| 621 minutes | 1.31% | 10 hours later, continue lowering |
| 791 minutes | 0.84% | 13 hours later, small profit就跑 |
| 1048 minutes | 0.44% | 17 hours later, just break even |
| 1074 minutes | 0% | 18 hours later, trailing stop takes over |

**Translation**:
> "Confident I can make 2% when first entering, but the longer I wait the more cowardly I become; in the end just don't lose money."

### 2.2 Stop-Loss Rule

| Type | Value | Plain English |
|------|-------|---------------|
| **Hard stop-loss** | -22.4% | Won't admit defeat until down 22%; extremely generous |
| **Trailing stop activation** | 18.6% profit | Start protecting when making 18% |
| **Trailing stop offset** | 23.1% profit | Final stop placed at making 23% |

**Translation**:
> "This strategy seems thick-skinned — won't give up until down 22%, but once it starts making money, clings to profits for dear life!"

### 2.3 Core Parameters

| Parameter | Value | Plain English |
|-----------|-------|---------------|
| **Timeframe** | 1 minute | Ultra short-term, fast entry/exit |
| **Informative timeframe** | 1 hour | Used for big picture |
| **Dependencies** | ta-lib, technical, qtpylib, numpy | Standard technical analysis libraries |
| **Entry modes** | 2 types | BB rebound + EMA volume-shrinking pullback |
| **Confirmation mechanism** | 2 consecutive candles | Both must satisfy before buying |

---

## 3. Entry Conditions: I've Categorized Them

This strategy has **2 entry modes**, but must satisfy a **mandatory prerequisite**:

### 3.1 Mandatory Prerequisite: 1-hour ROCR Filter

```
1-hour ROCR > 0.8973
```

**Plain English**:
> "First check big trend; past 7 days price rose at least 89.73% (how ROCR calculates); confirm it's an uptrend before considering buying."

This is the strategy's **first line of defense** — if big direction is wrong, never acts!

---

### 3.2 Mode 1: BB Rebound (Catches false breakout rebounds)

This mode specifically catches opportunities where **price briefly breaks BB lower band then quickly rebounds**.

**6 conditions must all be met**:

| Condition | Formula | Plain English |
|-----------|---------|---------------|
| 1 | BB lower valid | Data normal; not NaN |
| 2 | bbdelta > close × 1.85% | BB wide enough; room to maneuver |
| 3 | Price change > close × 0.17% | This candle volatile enough |
| 4 | Lower shadow < bbdelta × 78.8% | Lower shadow short |
| 5 | Close < previous BB lower | Price broke below lower band; "on sale" |
| 6 | Close ≤ previous close | Price didn't bounce back; still low |

**One-liner**:
> "Price suddenly broke through BB lower band, but lower shadow short — likely false breakout, may rebound immediately!"

---

### 3.3 Mode 2: EMA Volume-Shrinking Pullback (Catches panic bottom)

This mode specifically catches opportunities where **price crashed then volume shrunk**.

**3 conditions must all be met**:

| Condition | Formula | Plain English |
|-----------|---------|---------------|
| 1 | close < EMA50 | Below long-term MA (weak zone) |
| 2 | close < BB lower × 0.93% | Fell to extremely low level |
| 3 | Volume < 30-day avg × 35 | Volume shrunk (floor volume) |

**One-liner**:
> "Price fell to extremely low level, and volume dried up — nobody willing to sell, bottom likely!"

---

### 3.4 Dual Confirmation Mechanism (KEY!)

This is the biggest difference between Cluc5werk and other Cluc versions:

```python
# First mark the "fake buy" signal
fake_buy = (Mode 1 OR Mode 2)

# Actual buy: must have 2 consecutive candles satisfying fake_buy
buy = (fake_buy[previous] == 1) AND (fake_buy[current] == 1)
```

**Plain English translation**:
> "Even if a signal appears, the strategy doesn't rush to buy. It waits one candle period (1 minute) to see if the next candle also satisfies conditions. **Confirms twice before buying** — that's why win rate can reach 90%!"

---

## 4. Protection Mechanisms: Three "Life Preservers"

### 4.1 First Layer: ROCR Trend Filter

```
1-hour ROCR > 0.8973
```

Only trades with big trend up; avoids catching falling knives.

### 4.2 Second Layer: Dual Confirmation

Two consecutive candles must satisfy conditions before buying; filters false signals and noise.

### 4.3 Third Layer: Hard Stop-Loss + Trailing Stop

| Protection Type | Parameters | Function |
|----------------|-----------|----------|
| Hard stop-loss | -22.4% | Bottom-line protection; prevents extreme losses |
| Trailing activation | 18.6% profit | Starts tracking protection when making 18% |
| Trailing offset | 23.1% profit | Final stop locked at making 23% |

**Plain English**:
> "High loss tolerance (22%), but once it starts making money, clings to profits desperately — won't let earned money slip away."

---

## 5. Sell Logic: Not Greedy; Takes Profit and Runs

### 5.1 Main Sell Conditions

Sell must **simultaneously meet 4 conditions**:

| Condition | Formula | Plain English |
|-----------|---------|---------------|
| 1 | high ≤ previous high | High points declining or flat |
| 2 | previous high ≤ high 2 bars back | Three consecutive high points declining |
| 3 | close ≤ previous close | Close price weakening |
| 4 | close × 97% > BB middle | Price touching near BB middle |

**One-liner**:
> "Three consecutive candles' high points declining; can't rise anymore, and price near BB middle resistance — run!"

### 5.2 Sell Priority

```
ROI take-profit > Signal sell > Hard stop-loss
```

This means:
- Price quickly rises to ROI target → exit via ROI
- Sell signal appears → sell via signal
- Neither met and loss reaches 22.4% → trigger stop-loss

### 5.3 Only Sell When Profitable

```python
exit_profit_only = True
```

**Plain English**:
> "Only proactively sell when making money; wait for stop-loss or rebound if losing."

---

## 6. Strategy "Personality"

Describing Cluc5werk in human terms:

| Characteristic | Description |
|---------------|-------------|
| **Personality** | Extremely cautious; confirms twice before acting |
| **Trading style** | Short-term hunter; average holding 6 hours |
| **Risk preference** | High win rate; tolerates large drawdowns |
| **Decision speed** | Steady; not eager to enter |
| **Biggest advantage** | 90%+ win rate; dual confirmation reduces false signals |
| **Biggest disadvantage** | Many parameters; may overfit historical data |
| **Catchphrase** | "Wait, confirm again!" |

---

## 7. Applicable Scenarios

### 7.1 Good Scenarios

| Scenario | Recommendation | Description |
|----------|---------------|-------------|
| **Pullbacks in uptrends** | ⭐⭐⭐⭐⭐ | Best scenario; trend up + pullback buy |
| **High-volatility coins** | ⭐⭐⭐⭐⭐ | ALT, SHIB and meme coins; large moves |
| **Bull or strong-trend markets** | ⭐⭐⭐⭐☆ | ROCR filter effectively catches trending moves |
| **High-liquidity markets** | ⭐⭐⭐⭐☆ | Large volume; small slippage |

### 7.2 Bad Scenarios

| Scenario | Recommendation | Description |
|----------|---------------|-------------|
| **Downtrends** | ⭐⭐☆☆☆ | ROCR filter stops most trades |
| **Low-volatility consolidation** | ⭐⭐☆☆☆ | Too little movement; hard to trigger conditions |
| **Low-liquidity coins** | ⭐☆☆☆☆ | Large slippage; actual returns decrease |
| **Around major news** | ⭐☆☆☆☆ | Extreme moves may invalidate strategy |

---

## 8. Summary: What Do I Think?

### One-Line Verdict
> "Cluc series' pinnacle creation; dual confirmation traded for 90%+ win rate, but many parameters = overfitting risk. Use cautiously in live trading."

### Who's It For?
- ✅ Traders pursuing high win rate
- ✅ People who can accept wide stop-loss (22%)
- ✅ People trading high-liquidity coins
- ✅ People who understand trend + pullback logic
- ✅ People with time to monitor strategy operation

### Who's It NOT For?
- ❌ People who can't accept large drawdowns (22% very wide)
- ❌ People trading low-volatility coins
- ❌ People who don't want frequent monitoring
- ❌ People worried about parameter overfitting

### My Suggestions
1. **Prioritize high-liquidity coins**: Mainstream coins or hot meme coins
2. **Keep parameters unchanged**: These optimized through 1000 rounds of hyperopt; don't change arbitrarily
3. **Small-capital live test**: Run with small money first; verify live effects
4. **Monitor win rate changes**: If win rate drops below 80%, check market environment

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Dual Confirmation Trades for High Win Rate

Cluc5werk's money-making philosophy:

1. **ROCR filter**: Only trades when trend is up; avoids catching falling knives
2. **BB positioning**: Buy near lower band; sell near middle band
3. **Dual confirmation**: Two consecutive candles confirm; filters false signals

**Its personality**: Not as aggressive as other short-term strategies; **steady and methodical**.

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English |
|:---|:---|:---|
| 📈 Uptrend | ⭐⭐⭐⭐⭐ | Best scenario; ROCR filter makes you only trade with trend |
| 🔄 Wide-range oscillation | ⭐⭐⭐⭐☆ | BB signals frequent; dual confirmation reduces false signals |
| 📉 Downtrend | ⭐⭐☆☆☆ | ROCR filter keeps you in cash; miss bottom-call opportunities |
| ⚡ High volatility | ⭐⭐⭐⭐⭐ | Meme coins love this; large moves create opportunities |
| 💤 Low volatility | ⭐☆☆☆☆ | Hard to trigger buy conditions; low capital utilization |

**Bottom Line**:
> "This strategy **thrives in bull markets and high-volatility markets**, but basically lies flat in consolidation and downtrends."

### 9.3 Variant Versions

Strategy includes three versions optimized for different coins:

| Version | Suitable Coins | Characteristics |
|---------|--------------|----------------|
| **Cluc5werk** | General | Balanced parameters; suitable for most coins |
| **Cluc5werk_ETH** | ETH/Stable | More aggressive stop-loss (-33.7%); suitable for ETH volatility |
| **Cluc5werk_BTC** | BTC/Stable | Conservative stop-loss (-14.5%); suitable for BTC relative stability |
| **Cluc5werk_USD** | USD/Stable | Similar to ETH version |

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Suggested | Note |
|------------|-----------|------|
| **Number of pairs** | 10-20 | Diversify risk; increase signal opportunities |
| **Max positions** | 3-5 | Single stop-loss 22%; don't concentrate too much |
| **Single position** | 3-5% | 22% stop-loss = 0.66%-1.1% per trade risk |
| **Timeframe** | 1m (mandatory) | Strategy design requires |

### 10.2 Coin Selection

| Type | Recommendation | Reason |
|------|----------------|--------|
| Mainstream coins | ✅ Recommended | Good liquidity; reliable data |
| Meme coins | ✅ Recommended | High volatility; many triggers |
| New coins | ⚠️ Use carefully | Poor liquidity; large slippage |
| Stablecoin pairs | ❌ Not recommended | Too little movement; meaningless |

### 10.3 Hardware and Network Requirements

1-minute + dual confirmation needs **stable execution**:

| Requirement | Note |
|-------------|------|
| Memory | 2GB+ recommended |
| Network | Low latency (< 100ms) |
| API | Limit orders recommended; reduces slippage |

### 10.4 Backtesting vs Live Trading

Strategy optimized through 1000 rounds of hyperopt; backtest returns 509%, but:

> **Backtest performance ≠ Live performance**

Live may encounter:
- Slippage
- Fees
- Network latency
- Exchange rate limits

**Recommended Process**:
1. Backtest to verify logic
2. Paper trade at least one week
3. Small-capital live test
4. Observe win rate changes
5. Gradually add capital

**Don't go all-in right away**, strategy needs磨合!

---

## 11. Easter Egg: Strategy Author's "Little Tricks"

Looking closely at the code, you'll find interesting design choices:

### 11.1 Dual Confirmation's Secret

Why two consecutive candles?

> "One candle may be noise; two candles are a trend."

This is like crossing the street: looking once isn't enough; looking twice is safe.

### 11.2 "Weird Numbers" in Parameters

| Parameter | Value | Look random? |
|-----------|-------|-------------|
| bbdelta-close | 0.01853 | This came from hyperopt |
| rocr-1h | 0.8973 | Not 0.9; precise to 0.0001 |
| stoploss | -0.22405 | Why not -22%? |

**Truth**:
> These numbers are machines running 1000 rounds of optimization for the "optimal solution"; humans can't manually tune to this precision.

### 11.3 Three Variant Versions

Why ETH, BTC, and USD versions?

> Because different coins have different volatility characteristics:
> - ETH volatile → stop-loss widened to 33%
> - BTC relatively stable → stop-loss tightened to 14.5%
> - USD stablecoin pairs → reference ETH version

---

## 12. The Final Word

### One-Line Verdict
> "Dual confirmation traded for 90%+ win rate; the Cluc series' most steady version. But many parameters = high overfitting risk; use cautiously in live trading."

### Who's It For?
- ✅ Traders pursuing high win rate
- ✅ People who can accept wide stop-loss (22%)
- ✅ People trading high-liquidity, high-volatility coins
- ✅ People with time to monitor live operation
- ✅ People who understand trend + pullback + dual confirmation logic

### Who's It NOT For?
- ❌ People who can't accept single 22% loss
- ❌ People trading low-volatility coins
- ❌ People who don't want frequent strategy adjustments
- ❌ People with strong overfitting concerns
- ❌ People without time to monitor live operation

### Manual Trading Suggestions

If you want to follow manually but simplify:

1. Open 1-hour chart; confirm ROCR > 0.89 (or price clearly in uptrend)
2. Switch to 1-minute chart; add Bollinger Bands (20 periods, 2x std dev)
3. Wait for price touching near lower band
4. **Wait 1 minute**; see if next candle still at lows
5. Both candles confirmed → buy
6. Set 22% stop-loss
7. Sell when price touches middle band or three consecutive drops

---

## 13. ⚠️ Risk Reminder (Must Read This Section)

### Backtesting Looks Good; Live Requires Caution

Cluc5werk's historical backtesting performance is **extremely impressive** — 90% win rate, 509% returns. But there's a trap:

> **Because many parameters (6 buy parameters + 1 sell parameter), the strategy easily "fits" the optimal solution for past market conditions, but doesn't guarantee future profitability.**

Simply: **Like a student who memorized answers to score high; switch exam rooms (market environment changes) and it falls apart.**

### Hidden Risks of Complex Strategies

Live, complex logic may cause:

| Risk | Description |
|------|-------------|
| **Overfitting** | Parameters precisely match historical data; future may not work |
| **Look-ahead bias** | Some indicators may contain future info; backtest distorted |
| **Market changes** | Optimized parameters may fail when market structure changes |
| **Dual confirmation delay** | Waiting two candles may miss best entry |

### Wide Stop-Loss Hazards

22.4% stop-loss is very generous, meaning:

- Single loss may be significant
- 5 consecutive losses = 70%+ loss (arithmetic)
- Need larger profits to recover

**Psychological preparation**:
> You may profit on most trades, but one big loss may eat multiple profits.

### Live Trading Checklist

| Item | Description |
|------|-------------|
| Sufficient backtesting | Backtest across different market cycles |
| Paper trade first | Paper trade at least one week before live |
| Small-capital start | Test with small money first; verify live effects |
| Monitor win rate | Alert if win rate drops below 80% |
| Monitor avg profit | Check market environment if persistently below 1% |
| Don't change parameters | Parameters optimized; don't change arbitrarily |

### Risk Warning Checklist

```
1. ⚠️ 90% win rate is historical data; future may decline
2. ⚠️ 22% stop-loss is very wide; single loss may be significant
3. ⚠️ Many parameters = high overfitting risk
4. ⚠️ Dual confirmation may miss best entry
5. ⚠️ 1-minute framework sensitive to network latency
6. ⚠️ High-volatility coins have greater slippage risk
```

### The Final Word

> **Remember: High win rate doesn't guarantee steady profits; wide stop-loss may eat into many profits.**

Cluc5werk is a meticulously designed strategy; its success depends on:

1. **Market environment cooperation** — best in bull markets and high-volatility markets
2. **Parameter stability** — may fail when market changes
3. **Risk tolerance** — can accept 22% stop-loss wide drawdowns
4. **Live verification** — small-capital testing; gradually add capital

If you can do all four, Cluc5werk may become your **high win rate tool**. But remember:

**Past performance doesn't guarantee future returns; decide based on your own risk tolerance.**

**Survival matters more than making money. Stop-loss is the last line of defense!**
