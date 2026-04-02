# Chandemtwo Strategy: The "Strict Version" of Trend-Chasing

> **Nickname**: Consecutive-Upside Hunter, Three-Consecutive-Strength Strategy, CMO Momentum Tracker
> **Profession**: Momentum-confirmation trend-chasing strategy
> **Timeframe**: 5 Minutes

---

## 1. What's This Strategy All About?

Simply put, **Chandemtwo** is a strategy that:
- Uses **CMO indicator** to judge whether price has sustained upward momentum
- Requires CMO to stay above zero for **3 consecutive periods** before buying
- Sells when price rises too much (breaks Bollinger upper band)
- Also sells when momentum can't sustain (CMO crosses below -35)

This is **Chandem strategy's upgraded version** — buy conditions stricter, sell conditions more flexible. Like dating: the regular version says "has a job is fine," the upgraded version says "must have job + house + car + good personality," much higher bar.

---

## 2. Core Settings: Basically "Greedy but Strict"

### Take-Profit Rule (ROI Table)

```
Immediately: 75.2% profit
After 827 minutes (~14 hours): 39% profit
After 2168 minutes (~36 hours): 34% profit
After 3527 minutes (~59 hours): break-even exit
```

**Translation**: This strategy is extremely greedy right from entry — won't leave until making 75%! If 14 hours pass and still haven't made 75%, then 39% is fine. Keep stalling and standards keep dropping. Like dating — initially must have 白富美, after a few years "差不多就行" 🤣

**Gripe**: 75% target is really too high! Most coins can barely reach it; may hold positions a long time.

### Stop-Loss Rule

```
Hard stop-loss: -33.6%
Trailing stop: activates at 1.523% profit, locks at 10.329%, exits on 1.5% pullback
```

**Translation**:
- Cut losses at 33.6% forced liquidation — this stop-loss line is loose, strategy allows large drawdowns
- Made 1.5%+ and trailing stop kicks in; made 10% and stop is locked; pull back 1.5% and you're out

---

## 3. Buy Conditions: Three Gates of Strict Screening

This strategy's buy conditions are like an obstacle course — must pass three gates consecutively:

### 🎯 Gate 1: CMO Crossed Above Zero 2 Periods Ago

**Core Logic**: `cmo.shift(2) > 0 and cmo.shift(3) <= 0`

**Plain English**:
> "2 periods ago, CMO turned from negative to positive. This means the downtrend ended; uptrend began."

**Classic line**:
- "I see upward momentum starting, but don't rush — confirm two more steps."

---

### 🎯 Gate 2: CMO Still Above Zero 1 Period Ago

**Core Logic**: `cmo.shift(1) >= 0`

**Plain English**:
> "Last period, CMO was still positive, means the uptrend is continuing, not quitting halfway."

**Classic line**:
- "Good, uptrend confirmed for the second day."

---

### 🎯 Gate 3: CMO Still Above Zero This Period

**Core Logic**: `cmo >= 0`

**Plain English**:
> "This period, CMO is still positive — 3 consecutive periods above zero. Like hitting 3 three-pointers in a row in basketball, hot hand confirmed!"

**Classic line**:
- "Three-upside confirmation! Upward momentum strong; can enter!"

---

### 📋 Gate Summary

| Gate | Condition | Plain English |
|------|-----------|---------------|
| 1 | CMO crossed above zero 2 periods ago | Downtrend ended, uptrend started |
| 2 | CMO >= 0 one period ago | Uptrend continuing |
| 3 | CMO >= 0 this period | Three-upside confirmed, momentum strong |

**One-liner**: This isn't "buy the moment I see rising" — it's "confirm 3 times before buying." Very strict; fewer signals but higher quality.

---

## 4. Protection Mechanisms: Three Layers of Safety Net

This strategy has three protection layers ensuring controllable losses:

| Protection Type | Effect | Plain English |
|-----------------|--------|---------------|
| Hard stop-loss | -33.6% forced exit | "Cut losses at one-third, admit defeat, no fantasies" |
| Trailing stop | 1.5% profit activates, 10% locks, 1.5% pullback exits | "Made profit, protect it, don't let it go" |
| Staged take-profit | 75%→39%→34%→break-even | "Be greedy but measured; longer you hold, lower your target" |

**Gripe**: Hard stop-loss of -33.6% is really loose! Shows the strategy can handle large drawdowns. But if you can't stomach 30%+ losses, this strategy isn't for you.

---

## 5. Sell Logic: Two Escape Routes

This strategy has **two escape routes**; triggering either one means sell:

### 📉 Escape Route A: Price Breaks Bollinger Upper Band

**Trigger**:
- Price > Bollinger upper band

**Plain English**:
> "Bollinger Band is like an elastic channel. Price breaks the upper band means risen too wildly; may pull back. Run now, don't be greedy."

**Gripe**: This is the "sold too high" logic; suitable for short-term pullbacks. But in a big bull market, may sell too early.

---

### 📉 Escape Route B: CMO Crosses Below -35

**Trigger**:
- CMO < -35
- CMO previous period >= -35

**Plain English**:
> "CMO dropped from high to below -35, means upward momentum exhausted. Like a marathon runner who can't go on — time to exit."

**Gripe**: This is the "can't sustain momentum so sell" logic; catches momentum exhaustion signals.

---

### 📊 Two Sell Signals Summary

| Sell Signal | Trigger | Plain English |
|------------|---------|---------------|
| Rose too much | Price > Bollinger upper band | "Risen too wild; may pull back" |
| Can't sustain | CMO crosses below -35 | "Momentum exhausted; time to go" |

**One-liner**: Either risen too much, or can't sustain — both mean sell.

---

## 6. Strategy "Personality"

### ✅ Strengths

1. **Strict entry**: 3 consecutive period confirmation; fewer false signals
2. **Trailing stop**: Locks profits; won't let winners turn into losers
3. **Ambitious targets**: 75% profit goal; bold ambitions
4. **Flexible exit**: Two sell conditions; either triggers = run
5. **Upgraded version**: Stricter than original Chandem; more reliable

---

### ⚠️ Weaknesses

1. **Target too high**: 75% profit hard to achieve; may hold positions long
2. **Stop-loss too loose**: -33.6% stop-loss; many can't handle it
3. **No BTC correlation**: Ignores overall market; Bitcoin crash means this crashes too
4. **Sparse signals**: 3 consecutive period confirmation; low signal frequency
5. **May miss strong moves**: In strong trends, waiting 3 periods may mean already risen significantly

---

## 7. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| **Strong uptrend** | ✅ Recommended | CMO consecutive confirmation catches upward momentum |
| **Big bull market** | ✅ Recommended | 75% target easier to achieve in bull markets |
| **Ranging market** | ❌ Not recommended | 75% target hard to achieve; may hold long |
| **One-sided crash** | ❌ Not recommended | No BTC correlation; crashes with the market |
| **High-volatility coins** | ✅ Recommended | Volatile coins easier to achieve 75% target |

---

## 8. Summary: What Do I Think?

### One-Line Verdict
> "Strict trend-chasing type; only enters after consecutive confirmation. Ambitious targets, loose stop-loss; for players with strong hearts."

### Who's It For?
- ✅ Traders who can handle 30%+ drawdowns
- ✅ People pursuing high returns (75% target)
- ✅ Traders who believe in momentum indicators
- ✅ 5-minute framework short-term traders
- ✅ People with patience to wait for signals (signals sparse)

### Who's It NOT For?
- ❌ People who can only handle < 10% losses
- ❌ People chasing high-frequency trading (signals sparse)
- ❌ Conservative strategy seekers (too aggressive)
- ❌ People who buy at the first sign of rising (not strict enough)

### My Suggestions
1. **Lower ROI target**: Suggest 30%-50%; 75% is too tough
2. **Tighten stop-loss**: Suggest -20% to -25%; -33.6% loses too much
3. **Add BTC correlation**: For live trading, suggest adding BTC trend filter
4. **Pick volatile coins**: BTC, ETH type volatile coins easier to hit 75% target

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Using Consecutive Confirmation to Raise Win Rate

Chandemtwo's core philosophy: **Rather miss than be wrong**.

- **3 consecutive periods confirmation**: Dramatically lowers false signals
- **Target 75%**: Need big trends to make real money
- **Trailing stop**: Locks profits; won't let winners become losers

---

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English |
|:---|:---|:---|
| 🌝 Big surge | ⭐⭐⭐⭐⭐ | Perfect match; 75% target achievable |
| 📈 Small rise | ⭐⭐⭐☆☆ | May achieve but needs time |
| 🎢 Ranging | ⭐⭐☆☆☆ | 75% target hard to achieve; may hold long |
| 📉 Dropping | ⭐☆☆☆☆ | May buy counter-trend; loses money |

**Bottom Line**: Best in big bull markets; be careful in ranging and dropping markets.

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Suggested | Note |
|------------|-----------|------|
| Number of pairs | 10-30 | Signals sparse; increase pair count |
| Max positions | 3-5 | Don't be greedy; control risk |
| Position mode | Fixed position | Simple and effective |

### 10.2 Key Config Settings

```yaml
# Timeframe forced 5 minutes
timeframe: 5m

# ROI table
minimal_roi:
  0: 0.752      # 75.2%
  827: 0.39     # 39%
  2168: 0.34    # 34%
  3527: 0       # Break-even exit

# Stop-loss
stoploss: -0.336

# Trailing stop
trailing_stop: true
trailing_stop_positive: 0.015
trailing_stop_positive_offset: 0.10329
trailing_only_offset_is_reached: true
```

### 10.3 Hardware Requirements

This strategy has light computation; just one CMO indicator:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|----------------|-------------|
| 10-30 pairs | 512MB | 1GB | Silky smooth |
| 30-60 pairs | 1GB | 2GB | Fine |
| 60+ pairs | 2GB | 4GB | No problem |

**Warning**: This strategy involves no complex calculations; hardware requirements are very low.

### 10.4 Backtesting vs Live Trading

**Backtesting trap**: This strategy targets 75%; backtesting may show many positions held long without selling. This is because the target is too high; many coins can't reach it.

**Recommended Process**:
1. Run backtesting with default parameters; check holding time distribution
2. Based on backtesting, adjust ROI target (suggest 30%-50%)
3. Small-capital live test
4. Continuously monitor; adjust parameters when necessary

**Don't go all-in right away**, even good strategies need a磨合 period!

---

## 11. Easter Egg: Chandem vs Chandemtwo

### Comparison Table

| Comparison | Chandem (Regular) | Chandemtwo (Upgraded) |
|------------|-------------------|----------------------|
| Entry strictness | ⭐⭐☆☆☆ | ⭐⭐⭐⭐☆ |
| Exit flexibility | ⭐⭐⭐☆☆ | ⭐⭐⭐⭐☆ |
| Greed level | 🤑 28% | 🤑🤑 75% |
| Risk tolerance | 🔥 -28% stop-loss | 🔥🔥 -33.6% stop-loss |
| Signal frequency | More | Fewer but more precise |

### What Was Upgraded?

1. **Stricter entry**: Regular needs 1 period confirmation; upgraded needs 3 consecutive periods
2. **Higher target**: Regular 28%, upgraded 75%
3. **Looser stop-loss**: Regular -28%, upgraded -33.6%
4. **Fewer signals**: Stricter = lower frequency, but higher quality

---

## 12. The Final Word

### One-Line Verdict
> "Chandemtwo = stricter Chandem = safer trend-chasing strategy. Ambitious targets, loose stop-loss; for players with strong hearts."

### Who's It For?
- ✅ Traders who can handle 30%+ drawdowns
- ✅ People pursuing high returns
- ✅ People who believe in momentum indicators
- ✅ People with patience to wait for signals
- ✅ 5-minute framework short-term traders

### Who's It NOT For?
- ❌ People who can only handle < 10% losses
- ❌ People chasing high-frequency trading
- ❌ Conservative strategy seekers
- ❌ People who don't want to hold long (75% target may require long holding)

### Manual Trading Suggestions

If you're a manual trader, can borrow this strategy's approach:
- Use CMO to judge upward momentum
- Enter only when CMO above zero for 3 consecutive periods
- Set trailing stop; protect profits
- Target 30%-50% is enough; don't be too greedy

---

## 13. ⚠️ Risk Reminder (Must Read This Section)

### Target Too High Is the Biggest Pitfall

This strategy's first ROI is **75.2%** — really high target!

**Reality**:
- Most coins can't rise 75% in short term
- May hold positions long; possibly weeks without hitting target
- May ultimately exit at break-even or hit stop-loss

**My suggestion**: Strongly suggest lowering first ROI to **30%-50%**. 75% target is too idealistic.

### Looser Stop-Loss Is the Second Pitfall

This strategy's hard stop-loss is **-33.6%**, meaning:
- Must be able to absorb one-third loss
- If you can't handle such drawdowns psychologically, pressure will be huge
- One loss may require two wins to recover

**My suggestion**:
- If you can handle -33.6%, use default
- If you can't, suggest changing to -20% to -25%

### No BTC Correlation Is the Third Pitfall

This strategy **ignores the overall market** and doesn't check BTC trend. This means:
- When BTC crashes, may counter-trend buy then crash together
- No trend filter; may frequently lose in bear markets

**My suggestion**: For live trading, suggest adding BTC trend filter:
- Only buy when BTC above SMA200
- Or only buy when BTC in uptrend

### Sparse Signals Is the Fourth Pitfall

Because entry conditions strict (3 consecutive periods confirmation), signal frequency is low:
- May have only a few signals per day
- If you pursue high-frequency trading, this strategy isn't for you
- Need more trading pairs to ensure sufficient signals

**My suggestion**:
- Configure 20-30 trading pairs
- Lower first ROI to increase sell frequency

### Live Trading Suggestions (From the Heart)

```
1. Lower first ROI to 30%-50%
2. Tighten stop-loss to -20% to -25% (if you can't handle large drawdowns)
3. Add BTC trend filter
4. Configure 20-30 trading pairs
5. Test with small positions; confirm effectiveness before increasing
6. Check regularly; adjust parameters when necessary
```

**Remember**: No matter how good a strategy is, the market doesn't care. Target 75% sounds attractive, but hard to achieve in reality. Test with small positions; survival matters most!

---

**Final Reminder**: This is Chandem's upgraded version; stricter but harder to achieve targets. Don't be misled by the 75% target; suggest lowering it in live trading. 🙏
