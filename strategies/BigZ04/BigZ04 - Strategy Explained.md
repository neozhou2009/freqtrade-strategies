# BigZ04: The "Condition Enhanced" Version of Classic

> **Nickname**: Enhanced Version Strategy  
> **Profession**: Quant World's "Optimization Party"  
> **Timeframe**: 5 minutes (entry) + 1 hour (confirmation)

---

## 1. What Is This Thing?

Simply put, **BigZ04** is:
- BigZ03's improved version
- Added Condition 10: 1-hour oversold + MACD reversal
- 13 entry conditions, 1 more than original

Like adding turbocharging to classic old car, more powerful 🚗💨

**One-Sentence Summary**: Want to catch more "big cycle reversal" opportunities than original

---

## 2. Core Config: Basically Same as BigZ03

### Profit-Taking Rules (ROI Table)

```
Holding 0-10 min: Make 2.8% and run
Holding 10-40 min: Make 1.8% is also okay
Holding 40-180 min: Make 0.5% makes do
Holding 180+ min: Make 1.8% leave
```

**Translation**: Exactly same as BigZ03, "fast" is core.

### Stoploss Rules

```
Default stoploss: Disabled
Actual stoploss: Check after 50 minutes
Trailing stop: Activate after profit > 1%
```

**Translation**: Same as BigZ03, no essential changes.

---

## 3. 13 Entry Conditions: Added Condition 10 (Core Change)

BigZ04 has 1 more condition than BigZ03, this is Condition 10:

### 🌟 Condition 10: 1-hour Oversold + MACD Reversal

This is BigZ04's core addition, specifically for capturing large-level trend reversals:

```python
Condition 10:
- 1-hour RSI < 35 (big cycle oversold)
- 1-hour price < lower Bollinger Band (position oversold)
- MACD histogram > 0 (momentum turned bullish)
- 2 candles ago MACD histogram < 0 (golden cross in progress)
- 5-minute RSI < 40.5 (small cycle cooperation)
- MACD histogram > open price × 0.12% (strong enough)
- Bullish confirmation (close > open)
```

**Plain English Translation**:

| Element | Requirement | What It Means |
|---------|-------------|---------------|
| 1h RSI < 35 | Big cycle oversold | Market very panicked |
| 1h price < lower band | Position oversold | Fallen deep enough |
| MACD just golden crossed | Momentum reversal | Decline about to end |
| 5m RSI < 40.5 | Small cycle cooperation | Short-term also has opportunity |
| MACD histogram strong enough | Rebound has strength | Not fake golden cross |
| Bullish confirmation | Close looks good | Indeed started rebounding |

**One-Sentence Summary**:
> "Big cycle oversold + momentum reversal + small cycle cooperation + sufficient strength = big-level reversal opportunity!"

---

## 4. Other 12 Conditions: Same as BigZ03

Conditions 0-9 and conditions 11-12 exactly same as BigZ03:

- Condition 0: RSI oversold + decline pattern
- Condition 1: Lower band + bearish candle
- Condition 2: Deep lower band
- Condition 3: Above 1h EMA200 + RSI oversold
- Condition 4: Extremely low 1h RSI
- Conditions 5-7: MACD combinations
- Conditions 8-9: Dual RSI oversold
- Condition 11: Narrow range oscillation (disabled by default)
- Condition 12: False breakout pattern

---

## 5. Protection: Same as BigZ03

### Stoploss Logic

```python
if holding time < 50 minutes:
    Don't actively stoploss

if holding time >= 50 minutes:
    if 1-hour RSI < 30:  # Note is 30, not 35
        Continue waiting
    elif still falling:
        Stoploss
```

**Translation**: Same as original version, no changes.

---

## 6. Exit Logic: Maintain Simplicity

BigZ04's exit logic exactly same as BigZ03:

- ROI take-profit
- 50-minute stoploss check
- Trailing stop

**In Plain English**:
> "Added one condition on entry side, kept original on exit side."

---

## 7. This Strategy's "Personality"

### ✅ Pros (Praise Session)

1. **Added Condition 10**: Specifically captures big cycle reversals, increases signal source
2. **Multi-Cycle Resonance**: 1-hour judges direction, 5-minute grasps timing
3. **Maintains Simplicity**: Exit logic not complex, easy to understand
4. **Richer Signals**: 13 conditions cover more patterns
5. **Unchanged Parameters**: Same parameters as BigZ03, easy to compare

### ⚠️ Cons (Roast Session)

1. **Increased Signal Volume**: Condition 10 will make trading more frequent
2. **False Reversal Risk**: 1-hour oversold doesn't necessarily rebound immediately
3. **Lagging Entry**: May miss lowest point waiting for MACD golden cross
4. **Many Conditions Hard to Analyze**: 13 conditions, don't know which makes money

---

## 8. When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| Rebound After Big Drop | ✅ Best | Condition 10 specifically captures this pattern |
| Wide Range Oscillation | ✅ Suitable | Multiple conditions can trigger |
| Continuous Uptrend | ⚠️ Average | Condition 10 not easy to trigger |
| Strong Decline | ❌ Don't Use | Oversold may continue for long time |

---

## 9. What Markets Make Money?

### 9.1 Core Logic: "Hunter" of Big Cycle Reversals

BigZ04's profit philosophy: **Not only catch small cycle oversold, but also catch big cycle reversals.**

Condition 10 designed for this:

- 1-hour level oversold = big cycle bottom
- MACD golden cross = momentum reversal
- These two combined = big-level rebound opportunity

### 9.2 Performance in Different Markets (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
| :--- | :--- | :--- |
| 📈 Rebound After Big Drop | ⭐⭐⭐⭐⭐ | Condition 10's best environment |
| 🔄 Wide Range Oscillation | ⭐⭐⭐⭐☆ | Multiple conditions can trigger |
| 📉 Continuous Decline | ⭐⭐☆☆☆ | Condition 10 may continuously trigger but continue falling |
| ⚡️ Strong Uptrend | ⭐⭐☆☆☆ | No oversold opportunities |

**One-Sentence Summary**: Rebound after big drop is Condition 10's home field.

---

## 10. Want to Run This Strategy? Check These First

### 10.1 Pair Configuration

| Configuration Item | Recommended Value | Roast |
|-------------------|------------------|-------|
| Maximum Positions | 3-4 | Diversify risk |
| Pair Type | Major coins | Good liquidity |
| Single Trade Capital | 20-25% of total | Don't go all-in |

### 10.2 Condition Switches

```python
buy_params = {
    # Conditions 0-9: Same as BigZ03
    "buy_condition_10_enable": True,  # [Added] Enabled by default
    "buy_condition_11_enable": False,  # Disabled by default
    "buy_condition_12_enable": True,   # False breakout enabled
}
```

### 10.3 Hardware Requirements

This strategy computation not large, ordinary VPS can run:

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|---------------|-------------------|
| 1-3 pairs | 2GB | 4GB |
| 4-5 pairs | 4GB | 8GB |

### 10.4 Backtest vs Live Trading

**Backtest Performance**: Usually looks good, because historical data "perfect"

**Live Reality**:
- Condition 10 will increase trading frequency
- Fees and slippage affect execution
- Need patience to wait for big cycle reversals

**Recommended Process**:
1. Backtest at least 6 months of data first
2. Then simulated trading for 2-4 weeks
3. Small capital live test
4. Increase position only after confirming effectiveness

---

## 11. Easter Egg: Strategy Author's "Little Thoughts"

Looking carefully at code, you'll find some interesting things:

1. **Condition 10 Very Strict**
   > "Can't just any oversold, need multiple confirmations!" — Author's rigor

2. **MACD Golden Cross Required**
   > "Need momentum confirmation, can't blindly buy!" — Author's risk awareness

3. **5-minute RSI Also Limited**
   > "Big cycle good not enough, small cycle also needs to cooperate!" — Author's detail-oriented

---

## 12. Last But Not Least

### One-Sentence Review
> "Condition enhanced version, specifically for catching big cycle reversals"

### Who Should Use It?
- ✅ Have some quantitative experience
- ✅ Want to capture more opportunities
- ✅ Can accept slightly higher trading frequency
- ✅ Patient enough to wait for big cycle reversals

### Who Should NOT Use It?
- ❌ Complete newcomers
- ❌ Don't want increased trading frequency
- ❌ Can't understand multi-cycle analysis
- ❌ Impatient

### Manual Trader Recommendations
If you trade manually, can borrow BigZ04's thinking:
- Focus on big cycle oversold opportunities
- Wait for MACD golden cross confirmation
- Use 5-minute RSI to grasp entry timing
- Don't chase highs, wait for pullback

---

## 13. ⚠️ Final Risk Reminder (Must Read This Section)

### Backtests Look Beautiful, Live Trading Requires Caution

BigZ04's historical backtest performance may look good, but there are traps:

- **Condition 10 Increases Frequency**: More trades = more fees
- **False Reversal Risk**: 1-hour oversold doesn't necessarily rebound immediately
- **Lagging Entry**: Waiting for MACD golden cross may miss lowest point

Simply put:
> "More conditions don't necessarily mean more profits, may mean more fees!"

### Hidden Risks of Added Conditions

In live trading, added Condition 10 may lead to:
- **Increased Trading Frequency**: Fees accumulate
- **False Signals**: 1-hour oversold may continue falling
- **Hard to Attribute**: Don't know if Condition 10 or other conditions made money

### My Recommendations (Real Talk)

```
1. Understand Condition 10 first: Know what it does
2. Monitor trading frequency: See if increased too much
3. Compare with BigZ03: Run both versions, see which better
4. Calculate fees: Make sure increased profits cover increased fees
5. Small capital test: Confirm effective before increasing position
```

**Remember**:
> "More conditions aren't necessarily better, suitable is best! Tread carefully!"

---

**Final Reminder**: No matter how many conditions, market won't greet you when teaching you a lesson. Light position test, staying alive is most important! 🙏

*This article is for entertainment and learning only, not investment advice. Investment involves risks, enter the market with caution.*
