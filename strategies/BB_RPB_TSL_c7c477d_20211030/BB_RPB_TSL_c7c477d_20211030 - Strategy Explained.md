# BB_RPB_TSL_c7c477d_20211030: The "Fishing" Master with a BTC Security Team 🎣

> **Nickname**: Bollinger Band "Fishing" Master + BTC Security Captain
> **Profession**: Multi-condition trend hunter, professional "bottom fishing" for 30 years
> **Timeframe**: 5-minute main attack + 1-hour observation

---

## 1. What's This Strategy?

Simply put, BB_RPB_TSL_c7c477d_20211030 is like someone "waiting for a rabbit by the tree" in the market:
- Specializes in waiting for prices to drop to the lower Bollinger Band to "pick up bargains"
- Has a BTC security captain on 24/7 guard duty to prevent getting buried during BTC crashes
- Runs away after making 10%, but allows profits to keep running 🎠

Like an old fisherman 🎣:
> "I just wait by the river, fish swim into my net on their own. Every now and then I check the weather forecast (BTC trend) — if a storm's coming, I won't go out fishing even if you pay me!"

---

## 2. Core Config: "Take Profits When You See Them, Let Profits Run"

### Take-Profit Rules (ROI Table)

```python
minimal_roi = {
    "0": 0.10,  # Made 10%? RUN!
}
```

**In Plain English**:
> "10% is the bottom line — make enough and run, never get greedy!"

### Stoploss Rules

```python
stoploss = -0.10      # Must cut at 10% loss
use_custom_stoploss = True  # But I'll dynamically adjust stoploss
```

**In Plain English**:
> "10% loss is my bottom line, but I'm smart — after making money, I secretly move the stoploss line up. That way, even if the market reverses, I can keep most of my profits!"

### How Does Trailing Stop Work?

Strategy has a "magical" trailing stop system with three gears:

| Profit Zone | Stoploss Position | Translation |
|-------------|------------------|-------------|
| < 1% | -17.8% | Haven't made 1% yet? Fine with losing |
| 1%-4.8% | Dynamic calculation | More profit = tighter stoploss |
| > 4.8% | Hardcore protection | Must protect 4.3%+ profit! |

**In Plain English**:
> "It's like fighting a Boss in a game: when HP is low (low profit) I play safe, when HP is thick (high profit) I get cocky, but either way I gotta stay alive!"

---

## 3. 7 Entry Conditions: I've Classified Them for You

This strategy's entry conditions are like choosing concubines — let me classify them:

### 🎯 Category 1: Wait for Pullbacks (2 conditions)
**Core Logic**: Price dropped too hard, time to rebound

**In Plain English**:
> "I'm greedy when others are fearful! Price already fell to three layers below the lower Bollinger Band — if it doesn't rebound, where's the justice?"

**Representative Conditions**:
- `BB_Dip`: `bb_delta > 0.025 & bb_width > 0.095 & rmi < 49`
  → "Bollinger Bands opened wide, CCI and RMI show oversold — BUY!"
- `Local Uptrend`: `ema_26 > ema_12 & close < bb_lowerband2 * 0.999`
  → "Short-term moving average still going up, but price dropped to lower BB — this is a fake drop!"

---

### 📈 Category 2: Trend Confirmation (2 conditions)
**Core Logic**: Trend is up, pullback is a buying opportunity

**In Plain English**:
> "The main wave is here! Pullback is your chance to get on board — miss this village, no more shops!"

**Representative Conditions**:
- `EWO`: `EWO > 2.055 & rsi_fast < 21`
  → "Wave indicator shows strong momentum, RSI hasn't risen yet — get on NOW!"
- `EWO2`: `EWO > 4.179 & rsi < 35` (more aggressive version)
  → "This EWO is even stronger! More aggressive than the last one — ALL IN!"

---

### 🔍 Category 3: Multiple Confirmations (3 conditions)
**Core Logic**: Only order when multiple indicators nod together

**In Plain English**:
> "I'm the type who won't release the eagle until I see the rabbit. All indicators must agree before I place an order!"

**Representative Conditions**:
- `Cofi`: `fastk crosses above fastd & adx > 20 & EWO > 2.055`
  → "Stochastic golden cross, trend is clear, momentum is there — this is solid!"
- `NFI 32`: `rsi_slow going down & rsi < 46 & cti < -0.86`
  → "RSI is weakening but not totally dead, CTI is also oversold — let's go!"
- `NFI 33`: `EWO > 8 & rsi < 32 & r_14 < -98`
  → "Momentum is exploding! RSI almost at zero, Williams also oversold — ALL IN!"

---

## 4. Protection Mechanisms: 3 Layers of "Bulletproof Vests" 🛡️

Each entry condition comes with a set of BTC protection parameters — like wearing three bulletproof vests:

| Protection Type | Function | In Plain English |
|-----------------|----------|------------------|
| BTC 5m Protection | Won't buy if BTC drops more than threshold in 5 minutes | "BTC crashed 5 minutes ago? No thanks, not buying!" |
| BTC 1d Protection | Won't buy if BTC dropped too much in 1 day | "BTC is down like a dog today — I'm not catching falling knives!" |
| Volume Protection | Volume must be > 0 | "Signals without volume are耍流氓!" |

**Roast**:
> "Is this strategy scared of BTC or what! Every time BTC drops, the strategy goes on vacation and doesn't trade. But hey, who says BTC isn't the big boss?"

---

## 5. Exit Logic: Even Fancier Than Entry

### 5.1 Dynamic Take-Profit: Let Profits Fly

This strategy's take-profit isn't fixed — it's dynamic. More profit = tighter stoploss!

```
Profit 0-1%   →  Stoploss: -17.8% (hard stop)
Profit 1-4.8% →  Stoploss: Dynamically moves up (linear interpolation)
Profit 4.8%+  →  Stoploss: Lock 4.3%+ (must protect at least 4.3%)
```

**In Plain English**:
> "When I first start making money, I'm timid — stoploss is far (-17.8%). After making more, I get bold and quietly move stoploss up — from needing 10% profit to being fine with 4.3%! This is called 'letting profits run'!"

### 5.2 Special Exit Scenarios

| Scenario | Trigger Condition | In Plain English |
|----------|------------------|------------------|
| BTC Crash | btc_diff < -389 | "Daddy BTC crashed, I'm out!" |
| EMA Breakdown | close < ema_200 * 0.988 | "200-day MA is broken — RUN!" |
| Capital Outflow | cmf < -0.046 | "Money's running, I'm running too!" |

### 5.3 Base Exit Signals

**Classic Lines**:

1. **BTC Protection Triggered**: `btc_diff < sell_btc_safe (-389)`
   > "BTC dropped too much in 5 minutes — not playing anymore, outta here!"

2. **EMA200 Combination Exit**: `close < ema_200 * 0.988 & cmf < -0.046 & rsi rising`
   > "Price broke below 200-day MA, money's fleeing, RSI still rising (about to rebound but I'm not waiting) — RUN!"

---

## 6. This Strategy's "Personality Traits"

### ✅ Pros (Praise Session)

1. **Very stable**: 7 entry conditions, there's always one for you
2. **Scared to die**: BTC protection mechanism avoids systemic risk
3. **Smart**: Dynamic trailing stop, profits run as far as they can
4. **Far-sighted**: 1-hour trend confirmation avoids counter-trend trading

### ⚠️ Cons (Roast Session)

1. **Choice paralysis**: Which of the 7 conditions to use? Newbies are confused
2. **Too many parameters**: Dozens of parameters to tune — headache
3. **Easy to overfit**: Backtest looks beautiful, live trading might slap your face
4. **Runs too slow**: Multi-timeframe + multi-indicators, VPS RAM isn't enough will go on strike

---

## 7. Applicable Scenarios: When to Use It?

| Market Environment | Recommended Operation | Reason |
|-------------------|----------------------|--------|
| Trending Up 🌟 | Focus on EWO/Cofi | Trend pullback buys, accurate hits |
| Ranging 🔄 | Focus on BB_Dip | High sell low buy in the range |
| BTC Crash 💥 | Stop all trading | Survival first, don't catch falling knives |
| Low Volatility 😴 | Reduce trading | Too few signals, wait empty-handed |

---

## 8. Bottom Line: How's This Strategy Really?

### One-Sentence Review
> "This is a 'seek stability while pursuing victory' strategy — uses complex condition filtering to ensure entry quality, uses BTC protection + dynamic stoploss to control risk."

### Who Should Use It?
- ✅ Traders with some quantitative foundation
- ✅ Investors pursuing steady growth
- ✅ OCD patients who can handle complex parameter tuning

### Who Should NOT Use It?
- ❌ Newbie beginners (too complex)
- ❌ Gamblers who like going all-in
- ❌ Lazy people who want simple settings
- ❌ Poor VPS users with only 1GB RAM

### My Suggestions

1. **Demo first**: Don't jump in with real money right away
2. **Watch signals**: Observe trigger frequency of each entry condition
3. **Tune parameters**: Adjust sensitivity based on your trading pairs
4. **Check logs**: Notice how often BTC protection triggers

---

## 9. What Markets Make This Strategy Money?

### 9.1 Core Logic: Building a "Bulletproof Net" with Complexity

BB_RPB_TSL_c7c477d_20211030 is a "multi-condition hunter" strategy based on Bollinger Bands. Code is over 600 lines — you know what that means? Equivalent to an undergraduate thesis 📚

**Its profit philosophy**:
> "I don't need to win every hand — I just need to win more when I win, lose less when I lose."

- **Bollinger Band pullback**: Price strayed too far from mean, will eventually return
- **Multi-indicator confirmation**: Multiple indicators nodding together = more reliable signals
- **Trend filtering**: Don't buy against the trend, reduce probability of getting stuck
- **Dynamic stoploss**: Let profits run, but don't get too greedy

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Trending Up | ⭐⭐⭐⭐⭐ | EWO conditions accurately capture pullbacks, 10% take-profit easily achieved |
| 🔄 Ranging | ⭐⭐⭐☆☆ | Multi-conditions trigger frequently, high friction costs |
| 📉 Trending Down | ⭐⭐☆☆☆ | Counter-trend buying = BTC protection trigger + frequent stoploss |
| ⚡️ High Volatility | ⭐⭐⭐⭐☆ | Bollinger Bands shine, can catch rebounds |

**One-Sentence Summary**:
> "Trending markets are for making money, ranging markets are for testing VPS performance, sideways markets are for vacationing!"

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Config

| Config Item | Suggested Value | Roast |
|-------------|-----------------|-------|
| Number of Pairs | 10-20 | Don't go too high, RAM will cry |
| Trading Varieties | Major coins | Altcoins too volatile, easy to get buried |
| Capital Amount | $1000+ | Too little can't handle volatility |

### 10.2 Key Config File Settings

```yaml
# At minimum set these
stoploss: -0.10
minimal_roi:
  "0": 0.10
timeframe: 5m
use_custom_stoploss: true
```

### 10.3 Hardware Requirements (IMPORTANT!)

This strategy has huge computation load — VPS RAM isn't enough will go on strike:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|-----------------|-------------|-----------------|------------|
| 10 pairs | 2GB | 4GB | Can run, but will lag |
| 20 pairs | 4GB | 8GB | Barely enough |
| 50 pairs | 8GB | 16GB | Silky smooth |

**WARNING**: Don't even try with VPS under 1GB RAM — you'll see `MemoryError`! 😅

### 10.4 Backtest vs Live Trading

| Aspect | Backtest | Live Trading |
|--------|----------|--------------|
| Signal Acquisition | 100% | May have delay |
| Slippage | None | Yes |
| Fill Rate | 100% | May miss |
| BTC Protection | Perfect execution | May lag in response |

**Suggested Process**:
1. Run on demo account for a week to observe
2. Small capital live test for signal execution rate
3. Adjust parameters based on live performance
4. Gradually add capital after confirming stability

**Don't go all-in right away** — even good strategies need磨合!

---

## 11. Easter Eggs: Strategy Author's "Little Thoughts"

Look carefully at the code, you'll find some interesting things:

1. **Dual Versions of EWO Indicator**:
   > "EWO actually has two versions — regular and premium! This is for investors with different risk appetites."

2. **Naming of NFI Conditions**:
   > "NFI 32 and NFI 33 are borrowed from some community strategy — mysterious naming, right?"

3. **Blog Links in Comments**:
   > "Author left blog links in comments — interested parties can check out the original!"

---

## 12. Final Final

### One-Sentence Review
> "This is a Bollinger Band strategy 'armed to the teeth' — uses 7 entry conditions to catch pullbacks, BTC protection to prevent black swans, dynamic stoploss to let profits run."

### Who Should Use It?
- ✅ Investors with quantitative experience
- ✅ Tech-savvy players who can handle complex configs
- ✅ Those pursuing steady growth, not getting rich quick

### Who Should NOT Use It?
- ❌ Newbies (start with simple strategies)
- ❌ Buddhist-style players who want simplicity
- ❌ Poor VPS users without enough RAM
- ❌ Gamblers wanting to get rich overnight

### Manual Trader Suggestions

If you want to manually reference this strategy:
1. Watch BTC trend daily — don't buy when BTC crashes hard
2. Consider buying when price drops near lower Bollinger Band
3. Combine with RSI < 30, CCI < -100 and other oversold signals
4. Consider selling in batches at 10% gain — don't be greedy

---

## 13. ⚠️ Risk Reminder (MUST READ)

### Backtest Looks Beautiful, Live Trading Needs Caution

BB_RPB_TSL_c7c477d_20211030's historical backtest performance often **looks very nice** — but there's a trap:

> **Strategy has 7 entry conditions, each with a dozen+ parameters — very easy to "fit" the optimal solution for past行情. This doesn't mean future profitability is guaranteed.**

Simply put:
> "A student who memorizes answers tests well — doesn't mean they'll do well on the real exam!"

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Signal delay**: Multi-indicator calculation takes time, market may have changed
- **RAM explosion**: VPS RAM insufficient will crash
- **Over-optimization**: Parameters tuned too finely,失效 in live trading
- **Execution difficulty**: Too many/complex signals, exchange may reject orders

### My Suggestions (Real Talk)

```
1. Run on demo account for a month first, observe signal trigger frequency
2. Small capital live test, see if orders can fill
3. Record trigger count and P&L for each entry condition
4. Adjust parameters based on data, remove conditions that often lose
5. Gradually add capital after confirming stability — don't All In!
```

**Remember**:
> "The market is always right — no strategy is mightier than the market. Light position testing, staying alive is most important!"

---

**Final Reminder**: Strategies are like weapons — used well they protect you, used poorly they kill you. Know your limits, don't bet your life savings on code! 🙏
