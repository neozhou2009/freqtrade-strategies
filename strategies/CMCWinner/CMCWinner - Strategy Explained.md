# CMCWinner Strategy: The Triple-Indicator Voting Rebound Catcher

> **Nickname**: The Three Brothers Voting Machine
> **Profession**: Mean Reversion Expert, specifically捡便宜 in panics
> **Timeframe**: 15 Minutes (medium-short term)

---

## 1. What's This Strategy All About?

Simply put, **CMCWinner** is a strategy that:
- Uses three indicators to "vote" on buy/sell decisions
- Specifically looks for deeply crashed coins to bottom-call
- Fast entry, fast exit, takes profit and runs

Think of it like an **old-school hunter** who doesn't rush to act — must wait until all three scouts report back "we can shoot" before firing — **rather miss than be wrong**.

The core philosophy is **mean reversion**:

> **"Extremes will reverse — when price deviates from the mean to an extreme degree, reversion is highly probable."**

Like a rubber band pulled too tight — it'll snap back. But CMCWinner doesn't trust its own judgment; requires all three indicators to agree:

- **CCI**: Measures price deviation
- **MFI**: Measures capital flow
- **CMO**: Measures downward momentum

All three must simultaneously say "buy" before the strategy acts. That's the "triple vote" mechanism — more reliable, but fewer opportunities.

---

## 2. Core Settings: Basically "Conservative Flash Sale"

### Take-Profit Rule (ROI Table)

```
Holding Time        Required Return
────────────────────────────────────
0-20 minutes        5%
20-30 minutes       3%
30-40 minutes       2%
After 40 minutes    0% (break-even and run)
```

**Translation**: Want 5% when just entering; if 20 minutes pass without it, lower expectations; after 40 minutes, just break even and leave — **make what you can, don't linger, never hold on desperately**.

### Stop-Loss Rule

```
Stop-loss = -5% (fixed)
```

**Translation**: Cut losses at 5%, don't argue with the market.

### Order Types

| Type | Method | Description |
|------|--------|-------------|
| Entry | Limit order | Guarantees execution price |
| Exit | Limit order | Stable exit |
| Stop-loss | Market order | Must execute in extreme conditions |

---

## 3. Buy Conditions: All Three Brothers Must Agree

This strategy's buy condition is extremely simple — **only one signal, but must pass three tests**.

### 🎯 The Three Buy Conditions

| Condition | Indicator | Threshold | Plain English |
|----------|-----------|-----------|---------------|
| Condition 1 | CCI | < -100 | Price dropped ridiculously far |
| Condition 2 | MFI | < 20 | Capital outflow crazy; nobody wants to buy |
| Condition 3 | CMO | < -50 | Downward momentum almost exhausted |

**Classic Dialogue**:
> CCI: Boss, price has dropped through the floor!
> MFI: Second brother, capital's all gone; can't push it down further!
> CMO: Third brother, running out of steam to go lower!
> All three in unison: **Fire!**

### 📉 What Do the Three Indicators Each Manage?

**CCI (Commodity Channel Index)**:
> CCI < -100 means price has **severely deviated** from the statistical mean, like someone pushed underwater — they'll eventually surface.

**MFI (Money Flow Index)**:
> MFI < 20 means market sentiment is **extremely pessimistic**, capital's all fleeing. But物极必反 — everyone's sold out, who's left to keep dumping?

**CMO (Chande Momentum Oscillator)**:
> CMO < -50 means downward momentum has **significantly decayed**, though price is still falling, the downward force is almost spent.

### ⚠️ Key Detail: Use Previous Day's Data!

```python
# Note: Using shift(1), i.e., previous day's data
dataframe['cci'].shift(1) < -100
dataframe['mfi'].shift(1) < 20
dataframe['cmo'].shift(1) < -50
```

**Why?**

When the current candle hasn't finished, indicator values **lie** — price moves, indicators follow. But using yesterday's confirmed data avoids this problem.

This is the design philosophy of an **old hand** — don't act rashly; wait until data stabilizes.

---

## 4. Protection Mechanisms: Two Lines of Defense

### First Line: Fixed 5% Stop-Loss

```
stoploss = -5%
```

**Plain English**: Cut losses at 5%, don't argue with the market.

5% is appropriate for 15-minute short-term trading — filters normal volatility while effectively controlling single-trade loss.

### Second Line: Staged Profit Targets

| Holding Time | Target | Design Philosophy |
|-------------|--------|-------------------|
| 0-20 minutes | 5% | Quick profit, no clinging |
| 20-30 minutes | 3% | Moderately lower expectations |
| 30-40 minutes | 2% | Further reduce requirements |
| After 40 minutes | 0% (break-even) | Longer you hold, lower the target |

**Core Philosophy**:

> The essence of short-term rebound strategies is "speed." If quick rebound doesn't happen, your judgment may be wrong; exit or lower expectations promptly.

---

## 5. Sell Logic: Perfectly Symmetric with Buy

### 5.1 Symmetric Sell Conditions

Sell and buy conditions are **perfect mirrors**:

| Condition | Indicator | Threshold | Plain English |
|----------|-----------|-----------|---------------|
| Condition 1 | CCI | > 100 | Price rose ridiculously high |
| Condition 2 | MFI | > 80 | Capital inflow crazy |
| Condition 3 | CMO | > 50 | Upward momentum too strong |

**Plain English**:
> **Price too high + capital inflow crazy + upward momentum too strong = Run!**

### 5.2 Complete Mean Reversion Loop

```
Buy: Extreme oversold → Potential rebound
Sell: Extreme overbought → Potential pullback
```

This embodies mean reversion's core philosophy — price won't deviate from value forever; eventually returns to equilibrium. The strategy enters on oversold, exits on overbought, fully capturing the mean reversion process.

### 5.3 Exit Priority

```
ROI take-profit > Indicator signal sell > Stop-loss
```

This means:
- If price rises quickly to ROI target → exit via ROI first
- If holding > 40 minutes without profit → hold as long as not hitting 5% stop-loss
- If overbought signal appears → exit proactively

---

## 6. Strategy "Personality"

### ✅ Strengths

1. **Clear Logic**: Buy/sell symmetric; understood at a glance
2. **Reliable Signals**: Triple-indicator verification; fewer false signals
3. **Controllable Risk**: Fixed stop-loss + staged ROI; crystal clear
4. **Simple Parameters**: No complex tuning; works out of the box
5. **Mature Philosophy**: Mean reversion is a classic; market-proven

### ⚠️ Weaknesses

1. **Sparse Signals**: Three indicators simultaneously meeting conditions is rare; may go days without signals
2. **Counter-Trend Trading**: Only does reversals; doesn't follow trends; poor in strong trending markets
3. **Fixed Stop-Loss**: Doesn't adjust stop-loss based on volatility; adaptability insufficient
4. **Entry Lag**: Uses previous day data; may miss best entry timing
5. **No Position Management**: Doesn't limit max positions; insufficient risk diversification

---

## 7. When to Use It?

| Market Environment | Recommendation | Action |
|-------------------|----------------|--------|
| Wide-range ranging | ⭐⭐⭐⭐⭐ | Best scenario; oversold/overbought repeatedly triggers |
| High-volatility coins | ⭐⭐⭐⭐☆ | Altcoins volatile; easy to trigger conditions |
| Monkey market (no direction) | ⭐⭐⭐⭐☆ | Price oscillates; mean reversion effective |
| Strong uptrend | ⭐⭐⭐☆☆ | May sell early, but won't lose |
| Strong downtrend | ⭐⭐☆☆☆ | Bottom-call risk high; may consecutively stop out |
| Low-volatility consolidation | ⭐⭐☆☆☆ | Hard to trigger signals; low capital utilization |

---

## 8. Summary: What Do I Think?

### One-Line Verdict
> **"A strategy with strong survival instincts — takes profit and runs, cuts losses, only acts with three votes."**

### Who's It For?
- ✅ People with patience to wait for signals
- ✅ People who can accept 5% stop-loss
- ✅ People who understand mean reversion principles
- ✅ People who want short-term but not high-frequency

### Who's It NOT For?
- ❌ People chasing high trading frequency
- ❌ People who can't watch charts and want to躺着赚
- ❌ People unwilling to cut losses
- ❌ People who only want to follow trends

### My Suggestions
1. **Patience is key**: Sparse signals are normal; quality over quantity
2. **Diversify coins**: Monitor 5-10 trading pairs simultaneously; more opportunities
3. **Test light**: Try with small capital first; don't go all-in
4. **Combine with trend strategies**: Works as supplement to trend strategies

---

## 9. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Mean Reversion

CMCWinner is a typical **mean reversion strategy**. Its money-making philosophy:

> **"Extremes don't last — overbought must fall, oversold must rise"**

Three core assumptions:
1. **Price has a mean**: Long-term, price oscillates around value
2. **Extremes don't last**: Overbought/oversold can't persist forever
3. **History repeats**: Previously effective reversal patterns stay effective

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Rating | Plain English |
|:---|:---|:---|
| 🔄 Wide-range ranging | ⭐⭐⭐⭐⭐ | Best scenario; oversold/overbought repeatedly triggers; steadiest earnings |
| 📈 Strong uptrend | ⭐⭐⭐☆☆ | Sell signals frequently trigger; may "sell too early," but won't lose |
| 📉 Strong downtrend | ⭐⭐☆☆☆ | Persistent oversold; may "bottom-call at mid-mountain," consecutive stops |
| ⚡ Low-volatility consolidation | ⭐⭐☆☆☆ | Signals scarce; almost no opportunities; low capital utilization |

**Bottom Line**: Ranging markets are its home turf; trending markets are its nightmare.

---

## 10. Want to Run This Strategy? Check These Configs First

### 10.1 Trading Pair Configuration

| Config Item | Suggested | Description |
|------------|-----------|-------------|
| Number of pairs | 5-10 | Diversify risk; more signal opportunities |
| Single position | 10-15% | Avoid single-trade losses too large |
| Max open positions | 3-5 | Don't hold too many simultaneously |
| Timeframe | 15m (default) | Adjust per coin characteristics |

### 10.2 Coin Selection

| Type | Recommendation | Reason |
|------|---------------|--------|
| Mainstream coins | ✅ Recommended | Good liquidity; moderate volatility |
| Altcoins | ⚠️ Use carefully | High volatility; more signals but higher risk |
| New coins | ❌ Not recommended | Poor liquidity; inaccurate data |

### 10.3 Hardware Requirements

This strategy's computation is light; VPS requirements are low:

| Number of Pairs | Minimum RAM | Recommended RAM | Experience |
|----------------|-------------|----------------|-------------|
| 1-5 pairs | 1GB | 2GB | Smooth |
| 5-10 pairs | 2GB | 4GB | Smooth |
| 10+ pairs | 4GB | 8GB | Stable |

### 10.4 Backtesting vs Live Trading

**Recommended Process**:
1. Backtest on historical data; see performance
2. Run paper trading for a week; observe actual signals
3. Small-capital live test; verify slippage and fee impact
4. Gradually increase position

**Don't go all-in right away** — mean reversion strategies consecutively stop out in strong trends!

---

## 11. Easter Egg: Strategy Name's "Little Secrets"

### 11.1 Where Does CMC Come From?

**CMCWinner**'s CMC represents three indicators:
- **C** = CCI (Commodity Channel Index)
- **M** = MFI (Money Flow Index)
- **C** = CMO (Chande Momentum Oscillator)

**Winner** expresses hope of winning the market with these three indicators — but actual results depend on backtesting and live trading 🤣

### 11.2 The Three Indicators' Synergy Effect

```
        ┌─────────┐
        │   CCI   │  ← Price dimension: measures price deviation
        └────┬────┘
             │
    ┌────────┴────────┐
    │                 │
┌───┴───┐         ┌───┴───┐
│  MFI  │         │  CMO  │
└───┬───┘         └───┬───┘
    │                 │
    │ Capital dimension│ Momentum dimension
    │ Measures flow   │ Measures conversion
    │                 │
    └────────┬────────┘
             │
        ┌────┴────┐
        │ Buy/Sell │
        │  Signal  │
        └─────────┘
```

Three dimensions confirm simultaneously — like three people voting — only executes when all three pass; dramatically lowers false signals.

### 11.3 Why Use Previous Day's Data?

This is design philosophy of an **old hand**:

> The current candle isn't finished yet; indicators bounce around with price. By the time you see a signal and enter, next second the indicator changes — all for nothing!

Using confirmed previous day data, though you may miss the best entry, signals are more reliable — **rather miss than be wrong**.

---

## 12. The Final Word

### One-Line Verdict
> **"Three brothers vote; signals few but reliable. For patient people, not for impatient types."**

### Who's It For?
- ✅ People with patience to wait for signals
- ✅ People who can accept 5% stop-loss
- ✅ People who understand mean reversion
- ✅ People who want short-term but not high-frequency
- ✅ People who can monitor multiple coins simultaneously

### Who's It NOT For?
- ❌ People chasing high trading frequency
- ❌ People who can't watch charts and want to躺着赚
- ❌ People unwilling to cut losses
- ❌ People who only want trend-following
- ❌ People who盯着一个coin操作

### Manual Trading Suggestions

If you want to follow manually:
1. Open 15-minute chart
2. Add CCI(20), MFI(14), CMO(14) indicators
3. Wait for previous candle to satisfy: CCI < -100, MFI < 20, CMO < -50
4. Open position; set 5% stop-loss
5. Wait for price rebound; sell when hitting target profit or overbought signal

### Combining with Other Strategies

| Strategy Type | Combination Method |
|--------------|-------------------|
| Trend-following strategies | Main strategy does trends; CMCWinner catches short-term rebounds |
| Grid strategies | Use grids in ranging markets; use CMCWinner in reversal markets |
| Momentum strategies | Momentum strategies catch breakouts; CMCWinner catches pullbacks |

---

## 13. ⚠️ Risk Reminder (Must Read This Section)

### The Cost of Sparse Signals

Triple-indicator joint confirmation improves reliability but brings **signal scarcity**:

- Daily trading signals may only be **1-3 times**
- Low-volatility markets may have **days without trades**
- Requires patience; not suitable for people chasing high frequency

**Countermeasures**:
- Monitor multiple trading pairs simultaneously; increase signal sources
- Consider relaxing some indicator thresholds (but lowers signal quality)
- Accept low frequency; pursue single-trade quality

### The Biggest Risk of Mean Reversion

The most dangerous scenario for mean reversion is **false reversal**:

```
Price drops → Oversold signal buy → Continues dropping → Triggers stop-loss
                          ↓
            Oversold again → Buy again → Continues dropping → Stop-loss again
```

This **"catching a falling knife"** risk is particularly pronounced in strong downtrends!

**Classic Case**:
> In Bitcoin's drop from 60K to 30K, every oversold bounce was brief; bottom-callers were repeatedly trapped.

### Live Trading Checklist

| Item | Description |
|------|-------------|
| Sufficient backtesting | Verify across different market cycles |
| Paper trading first | Verify performance before live |
| Select appropriate coins | Avoid extreme-condition coins; choose liquid mainstreams |
| Strict stop-loss | Don't cancel stop-loss due to floating loss; this protects capital |
| Control position size | Single trade shouldn't be too large; diversify |

### Risk Warning Checklist

```
1. ⚠️ Stop-loss! Stop-loss! Stop-loss! Important things repeat three times
2. ⚠️ May consecutively stop out in strong downtrends; be mentally prepared
3. ⚠️ Don't relax conditions just to trade; signals are sparse for a reason
4. ⚠️ "Bottom-calling" is always the most dangerous; strictly execute stop-loss
5. ⚠️ Mean reversion ≠ market must rebound; sometimes it keeps falling
```

### Final Advice

> **"When others are fearful, be greedy; when others are greedy, be fearful"** — sounds nice, but extremely hard to execute.

Bottom-calling at extreme oversold requires:
- **Iron discipline** (strictly execute stop-loss)
- **Heart of stone** (undisturbed by floating losses)
- **Water-like positions** (diversify risk; don't go all-in)

CMCWinner appears simple but actually requires deep market understanding. **Past performance doesn't guarantee future returns; decide based on your own risk tolerance.**

---

**Remember**: **Survival matters more than making money.** No strategy is a holy grail; stop-loss is the last line of defense!
