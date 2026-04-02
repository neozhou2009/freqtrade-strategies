# Schism3 Strategy: The Bounce Prediction Master

> **Nickname**: Bounce Prediction Master, Three-Headed Six-Armed  
> **Job**: Rebound hunter with binoculars  
> **Timeframe**: 5 minutes (main battlefield) + 1 hour (big picture) / 1 hour + 4 hours (transformer version)

---

## 1. What Is This Strategy?

Simply put, **Schism3** is:
- First observes "might bounce", records the price
- Waits for price to actually recover before entering
- If you use BTC/ETH as stake currency, it also automatically checks big coin trends

Like an **old hunter who won't place an order until confirming the rebound** 🎯

**The coolest part**: It has three versions!
- Schism3: Base version (5 minutes + 1 hour)
- Schism3_BTC: BTC stake specific (1 hour + 4 hours)
- Schism3_ETH: ETH stake specific (1 hour + 4 hours)

---

## 2. Core Configuration: "Patiently Waiting for Rebound"

### Take-Profit Rules (ROI Table)

```
Just bought: Run at 5% profit
After 10 minutes: Run at 2.5% profit
After 20 minutes: Run at 1.5% profit
After 30 minutes: Run at 1% profit
After 12 hours: Run at 0.5% profit
After 24 hours: No profit required, watch for signals
```

**Translation**: This strategy can hold, won't panic even holding for a day.

### Stop-Loss Rule

```
Maximum loss: 30%
```

**Translation**: **30%!** That's right, this strategy gives plenty of room for volatility, kind of has a "I don't believe you won't go up" stubbornness 😅

---

## 3. Buy Conditions: The Strategy's Coolest "Bounce Prediction"

This strategy's buy conditions work in three steps, let me break it down:

### 🎯 Step 1: Bounce Pre-detection

The strategy asks these questions first:

```python
1h_rsi >= 37        # Large timeframe not too bad
rmi-dn-trend == 1   # Indeed falling
rmi-slow >= 35      # But not fallen too much
rmi-fast <= 28      # Fast indicator somewhat low
mp <= 60            # Momentum not high
```

**Plain English**:
> "Looks like it might bounce, let me remember this price"

### 📝 Step 2: Record Bounce Price

```python
bounce-price = if bounce signal exists, record current price
              otherwise take lowest price of last 8 candles
```

**Plain English**:
> "Write this price in my little notebook, let's see if it goes up later"

### ✅ Step 3: Confirm Entry

Actual buy requires these conditions:

```python
1h_rsi >= 59              # Big trend upward
Bounce signal within 8 periods  # Signal still valid
rmi-up-trend == 1         # RMI turned upward
close >= bounce-price     # Price actually recovered!
```

**Plain English**:
> "Signal's there, trend's right, price recovered too - place order!"

---

## 4. Multi-currency Support: For BTC/ETH Stake Users

If your stake currency is BTC or ETH, the strategy will **extra check**:

### Timeframe Conditions (5 minutes)

```python
(BTC's RSI < 60) OR (Fiat RSI > 15)
```

**Plain English**:
> "BTC shouldn't be too expensive, or USD oversold, then altcoins have a chance to rise"

### Information Frame Conditions (1 hour)

```python
BTC's 1h RMI < 70
```

**Plain English**:
> "Big coin shouldn't be pumping too crazy, otherwise altcoins get blood-sucked"

**Summary**: This strategy watches big coin's mood, doesn't want to buy altcoins when BTC is surging 🙈

---

## 5. Protection Mechanisms: 5 Layers of "Safety Fuses"

| Protection Type | Purpose | Plain English |
|----------------|---------|---------------|
| Fixed Stop-loss | Exit at 30% loss | "Plenty of room, but don't lose too much" |
| Dynamic Stop-loss | Higher requirements over time | "Held long enough without profit, leave" |
| Order Timeout | Cancel if price deviates 1% | "Price ran too fast, forget it" |
| Entry Confirmation | Reject if price deviates 1% | "Entry price wrong, won't play" |
| Bounce Invalidation | Don't enter if price doesn't recover | "Where's the bounce you promised?" |

This strategy's stop-loss is 30%, much looser than typical 10%, suitable for positions you can hold through 🔥

---

## 6. Sell Logic: Similar to Schism2MM

### 6.1 Dynamic Stop-loss

```
Held 0 minutes: Allow 3% loss
Held 150 minutes: Allow 1.5% loss
Held 300 minutes: Require profit
```

### 6.2 RMI Stop-loss

| Scenario | RMI Threshold | Plain English |
|----------|--------------|---------------|
| Was profitable | RMI < 50 | "Rose but now falling back, protect profit and leave" |
| Never profitable | RMI < 10 | "Never got up, just take the loss and go" |

### 6.3 Portfolio Profit Management

```python
if has free slots:
    Other position profit threshold = slot-related calculation
else:
    Only allow biggest loser to sell
```

**Plain English**: Be more lenient when there's room, let the worst performer go first when full.

---

## 7. This Strategy's "Personality Traits"

### ✅ Pros (Compliment Time)

1. **Bounce Prediction**: Record signal price first, confirm recovery before entry, don't buy halfway down
2. **Multi-currency Support**: Automatically adapts to BTC/ETH stake, watches big coin mood
3. **Three Versions**: Base, BTC, ETH versions - one code, three uses
4. **Parameter Override**: Customize parameters per coin group

### ⚠️ Cons (Complaint Time)

1. **30% Stop-loss**: A bit loose, may hold losses for a long time before stopping
2. **Multi-data Source**: Need extra BTC/USD, COIN/USD data
3. **High Complexity**: Bounce system + multi-currency conditions, headache
4. **Backtest Difficult**: Multi-currency conditions need extra configuration in backtest

---

## 8. Suitable Scenarios: When to Use It?

| Market Environment | Recommended Action | Reason |
|-------------------|-------------------|--------|
| BTC/ETH Stake | Use Schism3_BTC or Schism3_ETH | Automatically checks big coin trend |
| Stablecoin Stake | Use Schism3 base version | Default parameters work |
| Oscillating Uptrend | Default parameters | Strategy's design target |
| One-sided Downtrend | Don't use or lower stop-loss | 30% stop-loss may get blown through |

---

## 9. What Market Can This Strategy Make Money?

### 9.1 Core Logic: Bounce Prediction

Schism3 is a **smart rebound strategy**. About 350 lines of code (including sub-strategies) - what does that mean? Equivalent to **a complete academic paper** 📚

**Its profit philosophy**: Confirm rebound before entry, don't buy halfway down

- **Bounce Pending Signal**: First detect "might bounce" conditions
- **Price Recording**: Write down the price at signal time
- **Recovery Confirmation**: Wait for price to actually recover before buying

### 9.2 Performance in Different Markets (Plain English)

| Market Type | Performance Rating | Plain English Explanation |
|:-----------:|:-----------------:|---------------------------|
| 📈 Oscillating Uptrend | ⭐⭐⭐⭐⭐ | Bounce signals precise, confirmation mechanism works |
| 🔄 Sideways Oscillation | ⭐⭐⭐☆☆ | Bounce signals may trigger frequently |
| 📉 One-sided Downtrend | ⭐⭐☆☆☆ | 30% stop-loss may not hold up |
| ⚡ High Volatility | ⭐⭐⭐☆☆ | Price confirmation might get slapped |

**One-sentence Summary**: Makes money in oscillating uptrend markets, can't hold up in one-sided downtrend markets.

---

## 10. Want to Run This Strategy? Check These Configurations First

### 10.1 Choose the Right Version

| Stake Currency | Recommended Version | Timeframe |
|---------------|---------------------|-----------|
| USDT/USD | Schism3 | 5m + 1h |
| BTC | Schism3_BTC | 1h + 4h |
| ETH | Schism3_ETH | 1h + 4h |

### 10.2 Multi-currency Data Sources

If using BTC/ETH stake, need to configure:

```yaml
# config.json needs extra data pairs
"exchange": {
    "pair_whitelist": [
        "BTC/USDT",
        "ETH/USDT",
        ...your trading pairs
    ]
}
```

### 10.3 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|----------------|----------------|-------------------|------------|
| 1-10 pairs | 2GB | 4GB | Smooth |
| 10-30 pairs | 4GB | 8GB | Normal |
| 30+ pairs | 8GB | 16GB | Recommended |

### 10.4 Stop-loss Suggestions

**30% stop-loss is too loose!** Suggest adjusting based on risk tolerance:

- Conservative: `stoploss = -0.15`
- Moderate: `stoploss = -0.20`
- Aggressive: `stoploss = -0.25`

---

## 11. Easter Egg: The Strategy Author's "Little Thoughts"

Looking carefully at the code, you'll find some interesting things:

1. **Bounce Pending Three Steps**:
   > "First observe, then record, then confirm - these three steps are like dating: check photos first, remember the name, then meet before deciding"

2. **Multi-currency Auto-adaptation**:
   ```python
   if stake_currency in ('BTC', 'ETH'):
       # Extra check BTC/ETH trend
   ```
   > "Using BTC as stake? Then I need to check BTC's mood"

3. **Parameter Override System**:
   ```python
   if pair in ('ABC/XYZ', 'DEF/XYZ'):
       buy_params = self.buy_params_GROUP1
   ```
   > "Different coins can use different parameters, very flexible"

4. **Sub-strategy Inheritance**:
   > "One code, three versions, inheritance and reuse, elegant"

---

## 12. Final Words

### One-sentence Review
> "A smart strategy that waits for bounce confirmation before entering, but stop-loss is a bit loose."

### Who Should Use It?
- ✅ Players using BTC/ETH as stake currency
- ✅ Those who like rebound/pullback trading style
- ✅ Big hearts who can hold 30% floating loss
- ✅ Rational types pursuing scientific confirmation

### Who Shouldn't Use It?
- ❌ Conservative types who feel pain at 5% stop-loss
- ❌ Players only doing backtesting (multi-currency conditions hard to configure)
- ❌ Lazy people wanting simple strategies
- ❌ Warriors buying dips in one-sided downtrends

### Manual Trading Suggestions
If you want to follow manually without a bot:
1. Find coins with 1h RSI >= 37 but not too high
2. Wait for RMI trend to turn upward
3. Confirm price has recovered from recent lows
4. If using BTC stake, first check BTC isn't pumping too crazy

---

## 13. ⚠️ Risk Re-emphasis (Must Read)

### Backtest Looks Great, Live Trading Needs Caution

Schism3's 30% stop-loss seems very tolerant - but there's a trap:

> **30% stop-loss means you may bear significant floating losses!**

Simply put: **This strategy can hold, but can you?**

### Hidden Risks of Complex Strategies

In live trading, complex logic may cause:
- **Multi-currency Data**: Missing BTC/ETH data will cause strategy to fail
- **Bounce Confirmation Failure**: Price recovers then drops back down
- **Late Stop-loss Trigger**: 30% stop-loss may have you holding for a long time
- **Frequent Signals**: Oscillating markets may trigger many false signals

### My Advice (Sincere Words)

```
1. First adjust stop-loss to -0.15 to -0.20
2. Make sure multi-currency data source is configured correctly
3. Dry-run for at least two weeks observing signal quality
4. Small capital live test for bounce confirmation effect
```

**Remember**: No matter how smart the bounce prediction, when the market teaches you a lesson it won't call ahead. Light position testing, survival is most important! 🙏

---