# Kamaflage: The Multi-Indicator "Camouflage" Master

> **Nickname**: The Impostor, Indicator Stitcher  
> **Profession**: KAMA + MACD + RMI three musketeers, part-time order book detective  
> **Timeframe**: 5 minutes (5m)

---

## 1. What's This Strategy?

Simply put, **Kamaflage** is:
- A strategy that uses three momentum indicators to cross-verify — KAMA, MACD, RMI, all required
- A strategy that peeks at the order book, using real-time prices to check orders
- A strategy with aggressive trailing stop — starts locking profits after 4.67% gain

Like someone checking your credit report, social media, AND LinkedIn gossip before a blind date 🤣

The "Kama" in the name comes from **KAMA (Kaufman Adaptive Moving Average)**, and "flage" is probably from **camouflage** — maybe meaning it "camouflages" in the market, only acting when conditions are perfect.

---

## 2. Core Settings: Simply "Take Profits When You Can"

### Profit-Taking Rules (ROI Table)

```
Run immediately:    Exit at 15% profit
After 10 minutes:   Exit at 10% profit
After 20 minutes:   Exit at 5% profit
After 30 minutes:   Exit at 2.5% profit
After 60 minutes:   Exit at 1% profit
```

**Translation**: The longer you hold, the lower the threshold — like dating, high standards at first, then you get tired and settle 😅

### Stoploss Rules

```
Hard stoploss:    Force cut at 10% loss
Trailing stop:    Activates after 4.67% profit, run if pulls back 1.125%
```

**Translation**: Giving you a chance to make money, but don't be greedy — if you fall 1.125% from the peak, get out immediately.

---

## 3. Entry Conditions: All Three Indicators Must Agree

This strategy's entry conditions aren't complex, but require all three indicators to **simultaneously satisfy**:

### 🎯 Buy Signal (No Position)

Must all be satisfied:
1. **KAMA fast line > slow line** (3-period KAMA > 21-period KAMA)
2. **MACD golden cross and > 0** (MACD line > signal line, and MACD > 0)
3. **MACD histogram > 0** (momentum strengthening)
4. **RMI rising and > 50** (relative momentum index upward)
5. **Volume not abnormal** (Volume < average volume × 20)

**In Plain English**:
> "All three indicators say good, and no one's dumping crazily — buy!"

### 📈 Add Position Conditions (With Position)

Must simultaneously satisfy:
1. **Price > SAR** (Parabolic SAR, means trend is upward)
2. **RMI ≥ 75** (momentum super strong)

**In Plain English**:
> "Already bought? Then only add when momentum is exploding, don't be greedy."

---

## 4. Exit Logic: Run When RMI Says Oversold

### 4.1 Exit Conditions

When holding position, check these conditions:
1. **No more buy signal** (`buy == 0`)
2. **RMI < 30** (oversold)
3. **Profit > -3%** (only sell if loss not exceeding 3%)
4. **Volume > 0** (someone's trading)

**In Plain English**:
> "Buy signal disappeared, momentum indicator is oversold, and not losing much — let's bail."

**Why limit profit > -3%?**  
Because the strategy doesn't want you to cut flesh at huge losses — what if it bounces right after you sell? 😢

### 4.2 Order Timeout Check

The strategy also actively cancels "expired" orders:

**Buy order timeout**:
- If current price > order price × 1.01 (up over 1%)
- Cancel order, don't chase the high

**Sell order timeout**:
- If current price < order price × 0.99 (down over 1%)
- Cancel order, re-list

**In Plain English**:
> "Order listed for ages without filling? Price already ran, cancel and restart!"

---

## 5. This Strategy's "Personality Traits"

### ✅ Advantages (Praise Session)

1. **Multi-indicator confirmation, reliable signals**: KAMA + MACD + RMI triple verification, not single indicator guessing
2. **Order book optimization**: Real-time order book check, uses real prices to calculate profit, avoids slippage traps
3. **Aggressive trailing stop**: Locks profits when earned, doesn't let profits turn into losses
4. **Parameters optimized**: ROI and trailing parameters are hyperopt results

### ⚠️ Disadvantages (Roast Session)

1. **Many indicators, hard to debug**: Three indicators affect each other, changing one may affect everything
2. **No trend filter**: Doesn't look at broad market EMA/SMA, dares to charge in downtrends
3. **Doesn't care about BTC**: Still buying when Bitcoin crashes, a bit stubborn
4. **Order book API dependency**: Not all exchanges support it, backtesting also inaccurate

---

## 6. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Slow bull/ranging up | ✅ Recommended | Multi-indicator confirmation + trailing stop, performs well |
| Wide ranging | ✅ Recommended | Multi-indicator combination suitable for ranging |
| Single-sided crash | ❌ Don't use | No trend filter, will get buried badly |
| Extreme sideways | ⚠️ Cautious | Too little volatility, few signals, lose on fees |

---

## 7. Summary: How's This Strategy?

### One-Sentence Review
> "Three indicators watching together, plus peeking at order book — overly cautious, but not a bad thing."

### Who Should Use It?
- ✅ Quant players who like multi-indicator confirmation
- ✅ Advanced players wanting to learn order book checks
- ✅ Players with hyperopt experience
- ✅ 5-minute timeframe traders

### Who Should NOT Use It?
- ❌ Newbies just starting (too many indicators, hard to understand)
- ❌ Exchanges that don't support order book API
- ❌ Lazy people who just want simple strategies
- ❌ People unwilling to backtest and verify

### My Recommendations
1. **Backtest first**: Parameters are optimized, may overfit, must verify
2. **Watch the broad market**: Add BTC trend filter yourself, don't go against the trend
3. **Adjust stoploss**: -10% hard stoploss may be too wide, see what loss you can accept
4. **Monitor order book**: Order book data may have latency in live trading

---

## 8. What Markets Make Money with This Strategy?

### 8.1 Core Logic: Using Three Indicators to "Call Each Other Out"

Kamaflage is a **multi-indicator momentum strategy**. Its core philosophy is:

> "One indicator might be a liar, but if three indicators all say up at the same time, that should be credible, right?"

- **KAMA**: Adaptive moving average, automatically adjusts sensitivity based on volatility
- **MACD**: Classic momentum indicator, everyone knows golden/death crosses
- **RMI**: Relative momentum index, RSI variant, more sensitive

### 8.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Slow bull/ranging up | ⭐⭐⭐⭐☆ | Three-indicator confirmation, trailing stop locks profits |
| 🔄 Wide ranging | ⭐⭐⭐⭐☆ | Multi-indicator combination suitable for ranging, but fees may add up |
| 📉 Single-sided crash | ⭐⭐☆☆☆ | No trend filter, will get buried badly |
| ⚡️ Extreme sideways | ⭐⭐☆☆☆ | Too little volatility, few signals, just burning fees |

**One-sentence summary**: Performs well in uptrends, gets buried badly in crashes, just burns in sideways.

---

## 9. Want to Run This Strategy? Check These Configs First

### 9.1 Pair Configuration

| Configuration | Recommended Value | Roast |
|--------------|------------------|-------|
| Number of pairs | 20-40 | Too few = not enough signals, too many = can't compute |
| Max positions | 3-6 | Control risk, don't be greedy |
| Position mode | Fixed position | Percentage position may blow up |
| Timeframe | 5m | Mandatory, don't change |

### 9.2 Config File Key Settings

```yaml
# Strategy-specific configuration
timeframe: 5m

# Trailing stop (from hyperopt)
trailing_stop: true
trailing_stop_positive: 0.01125
trailing_stop_positive_offset: 0.04673
trailing_only_offset_is_reached: true

# ROI table
minimal_roi:
  0: 0.15
  10: 0.10
  20: 0.05
  30: 0.025
  60: 0.01
```

### 9.3 Hardware Requirements (Important!)

This strategy needs order book API, plus multi-indicator computation, has hardware requirements:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|-----------------|------------|
| 20-40 pairs | 1GB | 2GB | Normal |
| 40-80 pairs | 2GB | 4GB | Smooth |

**Warning**: Order book API may have latency, backtest data also not quite accurate — test before live trading!

### 9.4 Backtest vs Live Trading

**Backtest problems**:
- Order book data may be inaccurate
- Slippage simulation not realistic
- Parameters may overfit historical data

**Recommended process**:
1. Backtest with default parameters first, understand strategy behavior
2. Adjust parameters, see how backtest results change
3. Paper trade test at least 1 week
4. Small capital live test
5. Confirm stability before adding capital

**Don't go all-in immediately**, even optimized parameters are historical data!

---

## 10. Easter Egg: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Order book check**: Both buy and sell use `self.dp.orderbook()` to get real-time prices
   > "I don't trust K-line close prices, I want to see real-time order book bids!"

2. **Adding position is cautious**: With position, only add when RMI ≥ 75
   > "Already bought? Then wait for momentum explosion, don't add blindly."

3. **Sell checks profit**: Only sell if profit > -3%
   > "Lost too much? Just hold, don't cut flesh at the floor."

4. **Parameters all optimized**: ROI and trailing parameters have many decimal places
   > "Best solution from backtest, though it might be overfitting..."

---

## 11. Last But Not Least

### One-Sentence Review
> "KAMA + MACD + RMI, three indicators in agreement, trailing stop locks profits — suitable for quant players who like multiple confirmations."

### Who Should Use It?
- ✅ Multi-indicator confirmation believers
- ✅ Advanced players wanting to learn order book mechanics
- ✅ 5-minute timeframe traders
- ✅ People with hyperopt experience

### Who Should NOT Use It?
- ❌ Indicator phobia patients
- ❌ Lazy people who only use market orders
- ❌ People unwilling to backtest and verify
- ❌ Exchanges that don't support order book API

### Manual Trader Recommendations

You can reference Kamaflage's approach:
- Observe KAMA, MACD, RMI three indicators simultaneously
- Enter only when all three confirm upward
- Use trailing stop to protect profits when making money
- Set order timeout, don't chase highs or kill lows

But doing it manually is too tiring, let the robot handle it 🤖

---

## 12. Technical Details Supplement

### 12.1 Indicator Parameters

| Indicator | Parameters | Purpose |
|-----------|------------|---------|
| KAMA fast line | 3 periods | Short-term trend |
| KAMA slow line | 21 periods | Long-term trend |
| MACD | Default (12, 26, 9) | Momentum direction |
| RMI | Default | Relative momentum |
| SAR | Default | Trend stoploss |
| Volume MA | 24 periods | Volume average |

### 12.2 Hyperparameter Values

```python
# Buy parameters (optimized results)
buy_params = {
    "macd": 0,       # MACD threshold
    "macdhist": 0,   # MACD histogram threshold
    "rmi": 50,       # RMI threshold
}
```

### 12.3 Order Timeout Thresholds

| Order Type | Price Deviation | Action |
|------------|----------------|--------|
| Buy order | > 1% | Cancel |
| Sell order | < -1% | Cancel |

---

## 13. ⚠️ Risk Reminder Again (Must Read This Section)

### Backtest Is Beautiful, Live Trading Needs Caution

Kamaflage's historical backtest performance may look **very good** — but there's a trap:

> **Because parameters are hyperopt-optimized, it's easy to "memorize answers" — perfectly fits historical data, but may not work in the future.**

Simply put: **"Memorized all past exam questions, but next exam has different questions and you're lost."**

### Hidden Risks of Complex Strategies

In live trading, multi-indicator combinations may cause:
- **Signal conflicts**: Three indicators may disagree, making you hesitate to enter
- **Parameter sensitivity**: Change one parameter, entire strategy behavior changes
- **Order book latency**: Real-time prices and order book may have time difference
- **Computation timeout**: Many indicators, high computation, may miss entry timing

### The Pit of No Trend Filter

Kamaflage's biggest problem: **Doesn't care how the broad market moves, only looks at its own few indicators.**

When Bitcoin crashes, it may still be buying — this is called "counter-trend bottom-fishing", easy to get buried.

**Recommend adding a BTC trend filter yourself**:
- Don't buy when BTC is below EMA 50
- Or use other broad market indicators to judge

### My Recommendations (Real Talk)

```
1. Backtest with default parameters first, see strategy performance in different markets
2. Add a BTC trend filter yourself, don't go against the trend
3. Paper trade test at least 2 weeks, observe if order book check works normally
4. Small capital live test, don't exceed 10% of total capital
5. Regularly check strategy performance, stop timely if not working
```

**Remember**: No matter how smart the strategy, it can't fight black swans. Light position test, staying alive is most important! 🙏

---

**Final reminder**: Multi-indicator confirmation is a good habit, but over-relying on historical parameters is dangerous. The market always changes, no strategy makes money forever!
