# Roth03 Strategy: The Aggressive Bottom Picker

> **Nickname**: The Daredevil Bottom Hunter  
> **Specialty**: Aggressive Oversold Bounce Hunter  
> **Time Frame**: 5 minutes

---

## I. What Is This Strategy?

Simply put, **Roth03** is a strategy that:
- A more aggressive bottom-picking strategy than Roth01
- Wider stop-loss, higher profit targets
- Uses fastd instead of CCI for confirmation

Like Roth01's "turbo version" — bigger guts, bigger ambitions 🤣

---

## II. Core Configuration: "Big Guts + Quick Exit"

### Take-Profit Rules (ROI Table)

```
Right after buying: Run with 24.6% profit
After 33 minutes: Run with 7.2% profit
After 90 minutes: Run with 1.5% profit
After 111 minutes: Any profit will do
```

**Translation**: Wants 24.6% right off the bat — pretty ambitious! But will compromise over time.

### Stop-Loss Rule

```
Cut losses at -31.9%
```

**Translation**: Even wider than Roth01! The strategy is saying "I trust I can pick the bottom, give me room to wiggle!"

---

## III. 1 Buy Condition: Smart Bottom-Picking

This strategy also has a single buy signal, but it's a bit different from Roth01:

### 🎯 Buy Trio

**Plain English**:
> "Price breaks below Bollinger lower band + fastd above 37 (not extreme oversold) + MFI below 20 (money has fled). Time to pick bottoms — there's rebound momentum!"

**Detailed Breakdown**:

| Condition | Code | Plain English |
|-----------|------|----------------|
| Below lower band | Close < BB_Low | Price breaks below Bollinger lower band |
| Momentum confirmation | fastd > 37 | Fast stochastic above 37, has rebound potential |
| Money fled | MFI < 20 | Money flow extremely contracted |

**Difference from Roth01**:
- Roth01 uses CCI to confirm oversold, Roth03 uses fastd
- Roth03's MFI threshold is stricter (20 vs 24)
- The fastd > 37 condition is clever — not extreme oversold, but "somewhat oversold with rebound momentum"

---

## IV. Sell Logic: Four-Piece Exit

This strategy's sell conditions are simpler than Roth01:

### 4.1 Sell Quartet

| Condition | Code | Plain English |
|-----------|------|----------------|
| SAR reversal | SAR > Close | Parabolic SAR says trend is reversing |
| RSI overbought | RSI > 69 | Relative Strength Index is overbought |
| Money rushed in | MFI > 86 | Heavy capital inflow |
| fastd confirmation | fastd > 79 | Fast stochastic confirms overbought |

**Plain English**:
> "SAR reversed, RSI overbought, money rushed in, fastd also says run — alright, let's go!"

### 4.2 Sell Comparison with Roth01

| Comparison | Roth01 | Roth03 |
|------------|--------|--------|
| Number of conditions | 6 | 4 |
| Bollinger upper band | Must break above | Not checked |
| CCI confirmation | Yes | No |
| fastd confirmation | No | Yes |
| Sell logic | More conservative | Simpler |

---

### 4.3 Tiered ROI Take-Profit

| Holding Time | Target Profit | Mindset |
|--------------|---------------|---------|
| 0-33 minutes | 24.6% | I want big money! |
| 33-90 minutes | 7.2% | Still okay |
| 90-111 minutes | 1.5% | At least something |
| >111 minutes | 0% | Just break even... |

---

## V. Technical Indicators: Pretty Similar to Roth01

### 5.1 Core Indicators

| Indicator | Purpose |
|-----------|---------|
| MACD | Trend judgment (calculated but not used) |
| Bollinger Bands | Overbought/oversold determination |
| RSI | Relative strength |
| CCI | Commodity Channel (calculated but not used) |
| MFI | Money flow |
| SAR | Trend reversal signal |
| ADX | Trend strength (calculated but not used) |
| Stoch Fast | Momentum confirmation (actually used) |

### 5.2 Actually Used

- **Buy**: Bollinger Band + fastd + MFI
- **Sell**: SAR + RSI + MFI + fastd

---

## VI. Strategy "Personality Traits"

### ✅ Pros (Compliments Section)

1. **Smarter Entry**: fastd > 37 avoids entering during extreme oversold
2. **Simpler Exit**: 4 conditions is clearer than Roth01's 6
3. **Bigger Ambitions**: 24.6% initial ROI target, wants more
4. **Plenty of Room**: -31.9% stop-loss, not afraid of small fluctuations

### ⚠️ Cons (Criticism Section)

1. **Stop-loss is WIDE**: Cut at -31.9% loss... that's brutal...
2. **Doesn't Check Bollinger Upper Band on Sell**: Might exit too early
3. **Still Dangerous in Extreme Markets**: What if you pick bottoms on the mountainside?
4. **Range-Bound Slapping**: Back and forth stop-losses, paying lots of fees

---

## VII. Suitable Scenarios: When to Use It?

| Market Environment | Recommendation | Reason |
|-------------------|----------------|--------|
| Sharp Decline Rebound | ⭐⭐⭐⭐⭐ | Exactly its home turf |
| Range-Bound Market | ⭐⭐⭐☆☆ | Watch out for frequent stop-losses |
| Sustained Downtrend | ⭐⭐☆☆☆ | Picking bottoms on the mountainside |
| One-Sided Uptrend | ⭐☆☆☆☆ | Can't even buy in |

---

## VIII. Summary: How Is This Strategy Really?

### One-Line Review
> "Roth01's aggressive sibling, wider stop-loss, higher targets, bigger guts."

### Who Should Use It?
- ✅ High risk tolerance players
- ✅ Mean reversion believers
- ✅ Those who can handle large drawdowns
- ✅ People who like simple strategies

### Who Should NOT Use It?
- ❌ Conservative investors
- ❌ Tight stop-loss users
- ❌ Trend followers wanting big money in bull markets
- ❌ Newbie beginners

### My Suggestions
1. **Adjust stop-loss**: -31.9% is too wide, suggest adjusting to around -20%
2. **Pair with trend strategy**: Don't use it alone, pair with a trend-following strategy for hedging
3. **Watch the big picture**: When the market is crashing, don't try to pick bottoms

---

## IX. What Markets Can This Strategy Make Money In?

### 9.1 Core Logic: Aggressive Bottom-Picking

Roth03 is Roth01's "aggressive version." Both are mean reversion strategies, but Roth03 is more willing to take risks.

**Its Money-Making Philosophy**:

- **Don't Pick Extreme Bottoms**: fastd > 37, don't enter at the most extreme
- **Give Room to Wiggle**: -31.9% stop-loss, not afraid of small oscillations
- **Go Big or Go Home**: 24.6% initial target, pretty ambitious

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:--------------------------|
| 📈 Sharp Decline Rebound | ⭐⭐⭐⭐⭐ | This is its home turf! |
| 🔄 Range-Bound Market | ⭐⭐⭐☆☆ | Watch out for fees eating profits |
| 📉 Sustained Downtrend | ⭐⭐☆☆☆ | Picking bottoms on the mountainside |
| ⚡️ One-Sided Uptrend | ⭐☆☆☆☆ | Can't even buy in |

**One-Line Summary**: It laughs in sharp drops, cries in slow drops, gets dizzy in sideways, and watches in surges.

---

## X. Want to Run This Strategy? Check These Configurations First

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Notes |
|-------------------|-------------------|-------|
| Number of Pairs | 5-20 | Too many to manage |
| Time Frame | 5 minutes | Don't change, it's designed this way |

### 10.2 Hardware Requirements (Important!)

This strategy doesn't need heavy computation, no need for high-end machines:

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-50 pairs | 4GB | 8GB | Good |

**Warning**: Don't use those cheap VPSs, they'll freeze up 😅

### 10.3 Backtesting vs Live Trading

Backtesting looks beautiful, live trading may be different:

**Recommended Process**:
1. Backtest first to see historical performance
2. Run on paper trading for a while
3. Small capital live test
4. Confirm it works before increasing capital

**Don't go all-in right away**, no matter how good the strategy is, it needs to be calibrated!

---

## XI. Roth01 vs Roth03: Which to Choose?

| Comparison | Roth01 | Roth03 |
|------------|--------|--------|
| Stop-Loss | -29.6% | -31.9% (wider) |
| Initial ROI | 14.7% | 24.6% (higher) |
| Buy Confirmation | CCI <= -57 | fastd > 37 |
| Sell Confirmation | 6 conditions | 4 conditions |
| Style | Conservative bottom-picking | Aggressive bottom-picking |

**How to Choose?**
- Conservative? Choose Roth01
- Aggressive? Choose Roth03
- Run both? Also fine, diversify risk

---

## XII. Final Words

### One-Line Review
> "Roth01's aggressive sibling, bigger guts, bigger ambitions."

### Who Should Use It?
- ✅ High risk tolerance players
- ✅ Those who can handle -30% stop-loss
- ✅ Minimalists who like simple strategies
- ✅ Patient people waiting for extreme conditions

### Who Should NOT Use It?
- ❌ Conservative investors
- ❌ Tight stop-loss users
- ❌ Newbie beginners
- ❌ Impatient people who can't wait

### Manual Trader Tips
If you trade manually, you can reference this approach:
1. Watch for assets with MFI < 20 and price below Bollinger lower band
2. Wait for fastd > 37 to confirm rebound momentum
3. Set your stop-loss, don't be greedy

---

## XIII. ⚠️ Risk Re-emphasis (Must Read!)

### Backtesting Is Beautiful, Live Trading Requires Caution

Roth03's historical backtest may look good — but there's a trap:

> **The cost of aggressive bottom-picking: When you fail, losses are bigger.**

Simply put: **Big guts are a double-edged sword, win more, lose more**

### Hidden Risks of Complex Strategies

In live trading, watch out for:
- **Slippage in Extreme Conditions**: Liquidity may be poor during rapid declines
- **Stop-Loss Execution Issues**: With -31.9% stop-loss, you might have lost even more by the time it triggers
- **False Rebound Risk**: fastd confirmation can also be wrong

### My Advice (From the Heart)

```
1. Adjust stop-loss to around -20%, don't use the default -31.9%
2. Don't go all-in on this strategy, pair with a trend strategy for hedging
3. Don't use it when the market is crashing, you won't catch the bottom
4. Paper trade first, then go live
5. If you're afraid of losing too much, use Roth01 instead
```

**Remember**: No matter how good the strategy is, the market will teach you a lesson without warning. Test with small positions, staying alive is what matters! 🙏