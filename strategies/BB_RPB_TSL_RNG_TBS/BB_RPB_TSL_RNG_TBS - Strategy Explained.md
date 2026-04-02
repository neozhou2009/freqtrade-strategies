# BB_RPB_TSL_RNG_TBS Strategy: Dual Trailing Master

> **Nickname**: Dual Trailing Master  
> **Profession**: Track Price Before Buying + Track Stop Loss After Buying  
> **Timeframe**: 5 minutes

---

## I. What Is This Strategy?

Simply put, **BB_RPB_TSL_RNG_TBS** is the "Plus Version" of BB_RPB_TSL_RNG_2:
- Has all the features of the base version
- Added a "trailing buy" function—doesn't rush to buy when signal appears, waits for price to drop a bit more before buying

It's like seeing a product on sale at the supermarket, but you think "it could get even cheaper," so you wait. When the price rebounds a bit, you strike!

**TBS = Trailing Buy Strategy**

---

## II. What's the Difference from the Base Version?

| Feature | Base Version (RNG_2) | TBS Version (RNG_TBS) |
|------|-------------|---------------|
| Trailing Buy | ❌ No | ✅ Yes |
| Backtesting Support | ✅ Yes | ❌ No |
| Hyperopt Optimization | ✅ Yes | ❌ No |
| BTC Info Pair | Fixed BTC/USDT | Auto-adapts to quote currency |
| Sell Trigger | Slower | Faster (offset <1) |

**One-Sentence Summary**:
> TBS version is the "deluxe edition" for live trading, base version is the "standard edition" for R&D

---

## III. Trailing Buy: The Soul Function of This Strategy

### 3.1 What Does Trailing Buy Mean?

Normal Buy: Signal appears → Buy immediately

Trailing Buy: Signal appears → Wait for price to drop a bit more → Buy when price rebounds

```
Example:

Signal Price: $100
After Trailing: Buy at $99

Saved: 1%
```

**Plain English**:
> "You say it's buyable, I'll wait a bit, see if I can get it cheaper"

### 3.2 How Does Trailing Buy Work?

Like fishing:

1. **Spot the Fish**: Buy signal appears, price at 100
2. **Cast Net and Wait**: Start tracking, set upper limit = 100.5 (buy on 0.5% rebound)
3. **Fish Dives Deeper**: Price drops to 99, upper limit adjusts down to 99.5
4. **Fish Jumps Up**: Price rebounds to 99.5, trigger buy!

### 3.3 Trailing Buy Parameters

| Parameter | Default Value | Plain English Explanation |
|------|--------|-----------|
| trailing_buy_max_stop | 2% | If price rises more than 2% above starting price, stop chasing |
| trailing_buy_max_buy | 0% | Buy when price is below starting price |
| trailing_expire_seconds | 1800 seconds | Give up if waiting more than 30 minutes |

**Translation**:
- Wait for price to drop, max wait 30 minutes
- If price rises more than 2%, forget it, not chasing
- Buy when price rebounds, snag a bargain!

### 3.4 Tiered Rebound Thresholds

| Price Drop | Buy on Rebound Of |
|---------|-------------|
| Drop 6% or more | Rebound 2% |
| Drop 3%-6% | Rebound 1% |
| Drop 0-3% | Rebound 0.5% |

**Plain English**:
> "The more it drops, the wider the rebound threshold—because the bargain is bigger, no need to rush"

---

## IV. Protection Mechanism: Dual Trailing

### Before Buying (Trailing Buy)

| Scenario | Action | Plain English |
|------|------|--------|
| Signal Appears | Start tracking | "Okay, let's see how much more you can drop" |
| Price Falls | Update upper limit | "Keep dropping, limit goes down with it" |
| Price Rebounds | Trigger buy | "Enough, enough, strike!" |
| Price Rises Too Much | Stop tracking | "Rose too much, forget it, not buying" |
| 30 Minute Timeout | Stop tracking | "Waited too long, forget it" |

### After Buying (Trailing Stop)

| Profit Level | Stop Loss Protection | Plain English |
|---------|---------|--------|
| Just Entered | -17.8% | "Give enough room first" |
| Above 1.9% Profit | Start breaking even | "Made money, start tightening" |
| Above 6.5% Profit | Follow the profit | "Made big money, follow it" |

**Summary**:
> Wait for bargains before buying, protect earned money after buying—tracking throughout, covering both ends!

---

## V. Buy Conditions: Same as Base Version

7 buy conditions, exactly the same as BB_RPB_TSL_RNG_2:

| Condition Group | Core Logic | Plain English |
|-------|---------|--------|
| BB_checked | Bollinger Bands oversold + breakout | "Fallen to the floor, time for rebound right" |
| local_uptrend | Uptrend pullback | "Trend upward but temporarily pulled back" |
| ewo | Elliott Wave pullback | "Wave theory says time to buy" |
| ewo_2 | EWO momentum upward | "Momentum is going up" |
| cofi | Stochastic golden cross confirmation | "Golden cross, there's a trend" |
| nfi_32 | Deep pullback | "Dropped deep enough" |
| nfi_33 | Extreme oversold | "Extreme oversold, someone will bottom-fish" |

**Difference**: These 7 conditions just "spot the fish," the actual "net casting" relies on trailing buy.

---

## VI. Sell Logic: More Conservative Than Base Version

TBS version sell offset parameters are smaller (<1), meaning faster sell triggers:

| Parameter | Base Version | TBS Version | Description |
|------|-------|-------|------|
| high_offset | 1.051 | 0.991 | TBS sells faster |
| high_offset_2 | 1.02 | 0.997 | TBS sells faster |

**Plain English**:
> "TBS version sells faster—maybe because entry price is lower, so not being greedy"

---

## VII. This Strategy's "Personality Traits"

### ✅ Strengths

1. **Better Entry Price**: Trailing buy may snag cheaper prices
2. **Full-Process Tracking**: Track price before buying, track stop loss after buying
3. **Auto-Adaptation**: Works regardless of exchange quote currency
4. **Complete Inheritance**: Keeps all the good stuff from base version
5. **Saves Computing Resources**: Only calculates on new candles

### ⚠️ Weaknesses

1. **Cannot Backtest**: Trailing buy can't be simulated in backtesting
2. **Cannot Optimize**: Can't use Hyperopt, must use base version first to tune parameters
3. **Waiting Too Long May Miss Opportunities**: 30-minute timeout, good opportunities may slip away
4. **API Latency Impact**: Real-time tracking depends on API speed
5. **More Complex Parameters**: Added a bunch of trailing buy parameters

---

## VIII. Applicable Scenarios: When to Use It?

| Scenario | Recommended Version | Reason |
|------|---------|------|
| Backtesting Research | Base Version (RNG_2) | TBS doesn't support backtesting |
| Parameter Optimization | Base Version (RNG_2) | TBS doesn't support Hyperopt |
| Live Trading Deployment | TBS Version | Trailing buy advantage |
| Volatile Market | TBS Version | Better entry price |
| Fast Trend | Base Version | Waiting for trailing may miss opportunities |

---

## IX. Live Trading Usage Recommendations

### 9.1 Configuration Process

```
Step 1: Use base version for backtesting and parameter tuning
Step 2: Copy parameters to TBS version
Step 3: Run TBS version in dry-run mode
Step 4: Deploy live after confirming stability
```

### 9.2 Key Parameter Settings

```yaml
# config.json Key Settings
"dry_run": true,  # Run simulation first!
"max_open_trades": 3,  # Max 3 trades simultaneously

# TBS Version Special Settings
trailing_buy_order_enabled: true  # Enable trailing buy
trailing_expire_seconds: 1800  # 30-minute timeout
```

### 9.3 Hardware Requirements

Same as base version:
- ≤10 trading pairs: 8GB memory is enough
- >10 trading pairs: Recommend 16GB

---

## X. Easter Eggs: Hidden Logic of Trailing Buy

Look at the code and you'll find:

1. **Force Buy Function**:
   > Timeout + price below starting price + buy signal still active → Force buy
   > "Waited too long but opportunity still there, just buy it"

2. **Upward Trend Quick Buy**:
   > trailing_buy_uptrend_enabled = False (disabled by default)
   > If enabled: Quick buy if price rises more than 2% within 90 seconds
   > "Upward trend is here, not waiting, buying directly"

3. **Before/After Buy Dual Trailing**:
   > Wait for cheap before buying, protect profits after buying
   > This strategy is "chasing" from start to finish

---

## XI. Summary

### One-Sentence Evaluation
> "An enhanced version specifically for live trading, chase bargains before buying, chase profits after buying, but still need base version for R&D phase"

### Usage Strategy Recommendations

| Phase | What Version to Use |
|------|----------|
| Parameter Research/Backtesting | BB_RPB_TSL_RNG_2 |
| Live Trading Deployment | BB_RPB_TSL_RNG_TBS |

### Final Recommendations

```
1. Use base version for parameter optimization first
2. Migrate parameters to TBS version
3. Run TBS in dry-run for at least two weeks
4. Compare both versions with small capital live trading
5. Fully deploy only after confirming TBS performs well
```

---

## XII. ⚠️ Important Warnings

### Traps of Trailing Buy

**Cannot Backtest ≠ Definitely Good in Live Trading**

Trailing buy effectiveness in live trading depends on:
- API Latency: Too much latency may miss best entry points
- Liquidity: May not be able to buy during extreme conditions
- Slippage: Entry price during rebound may not be ideal

### Correct Usage Process

```
Backtest → Base Version Parameter Tuning → Migrate Parameters to TBS → Dry-Run → Live Trading
```

**Do NOT** use TBS version for live trading directly without tuning parameters first!

### Risk Reminder Again

- Trailing buy waiting 30 minutes may miss good opportunities
- Unstable API may cause tracking failure
- No backtesting support means unknown effectiveness

**Remember**: Research first then live trading, staying alive is most important! 🙏
