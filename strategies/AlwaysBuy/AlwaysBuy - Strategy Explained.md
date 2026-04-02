# AlwaysBuy Strategy: The "Blind Box Player" of Quant Trading

> **Nickname**: Mindless Buying Machine, Test Tool Specialist  
> **Job**: Framework Tester / Benchmark Control Group  
> **Timeframe**: 5 minutes (5m)

---

## 1. What Is This Strategy?

Simply put, **AlwaysBuy** is:
- A "strategy" with absolutely no technical analysis
- A "blind box player" that buys at every candlestick it sees
- A tool specifically designed to test frameworks

Like throwing money into the stock market with your eyes closed, wherever it lands, it lands 🎲

**One-sentence summary**: This is not a trading strategy, this is a testing tool!

---

## 2. Core Configuration: Simply Put, "Buy and Wait"

### Take Profit Rules (ROI Table)

```
After 0 minutes: Sell only if profit ≥ 100%
After 100 minutes: Sell only if profit ≥ 200%
After 200 minutes: Sell only if profit ≥ 300%
After 300 minutes: Stop selling, wait for stop loss
```

**Translation**: These take-profit levels are ridiculously high, basically meaning "no active take-profit." Who expects to double their money before selling? This is a test configuration 🤣

### Stop Loss Rules

```
Fixed stop loss: Admit defeat at 20% loss
Trailing stop: After reaching 3% profit, run if it pulls back 0.5%
```

**Translation**:
- Fixed stop loss at 20%, that's wide enough to drive a truck through
- Trailing stop is reasonable, but the question is—why would you use a trailing stop to protect a "blind buy" strategy?

---

## 3. 1 Entry Condition: Let Me Translate to "Human Language"

This strategy's entry condition is so simple it makes you doubt life:

### 🎯 Category 1: Unconditional Buy (1 condition)

**Code Logic**:
```python
dataframe.loc[:, ["enter_long", "enter_tag"]] = (1, "entry_reason")
```

**Plain English**:
> "Whether it's up or down, oscillating or trending, just buy!"

**Actual Effect**:
- Every candlestick is a buy signal
- Keeps buying as long as funds are available
- Only stops when limited by `max_open_trades`

**Roast**: The core philosophy of this strategy is—"I don't look at the market, I just buy." The quantitative version of the "blindfolded investing method" 😂

---

## 4. Protection Mechanisms: 0 Layers of "Naked Exposure"

This strategy has **absolutely no protection mechanisms**:

| Protection Type | Available? | Comment |
|-----------------|------------|---------|
| Cooldown Period | ❌ No | Lose it all? Keep going |
| Max Drawdown Protection | ❌ No | Keep losing |
| Consecutive Stop Loss Protection | ❌ No | Still losing |
| Low Profit Protection | ❌ No | Always losing |

**Translation**: This strategy is "naked" trading. Lost? Continue! Lost again? Continue!

**But to be fair**: As a testing tool, it doesn't need protection mechanisms. You're here to test the framework, not to make money.

---

## 5. Exit Logic: Complete Lying Flat

### 5.1 No Active Exit

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    return dataframe  # Nothing here
```

**Plain English**:
> "Exit? Non-existent. Let the stop loss decide."

### 5.2 Passive Exit Methods

| Exit Method | Trigger Condition | Plain English |
|-------------|-------------------|---------------|
| Fixed Stop Loss | 20% loss | "Hold until you can't hold anymore" |
| Trailing Stop | Profit pullback | "Finally made some money, time to run" |
| ROI | Double your money | "Dream on, only sell when doubled" |

---

## 6. This Strategy's "Personality Traits"

### ✅ Advantages (Actually Not Really Advantages)

1. **Super Simple Code**: Less than 50 lines total, understand it in one read
2. **Framework Testing Magic Tool**: Use to verify if Freqtrade installation is correct
3. **Benchmark Reference Value**: Compare the difference between "mindless buying" and "strategic buying"
4. **Extremely Low Resource Usage**: No indicator calculations, CPU fan won't even spin

### ⚠️ Disadvantages (This Is the Real Point)

1. **Not a Trading Strategy**: It has no strategy 🤣
2. **Mindless Buying**: Doesn't look at market state at all
3. **Fee Killer**: Frequent trading fees will bankrupt you
4. **Stop Loss Too Wide**: 20% stop loss line is like betting half your life

---

## 7. Applicable Scenarios: When to Use It?

| Scenario | Recommended Action | Reason |
|----------|-------------------|--------|
| Testing Freqtrade Installation | ✅ Use it | Quickly verify if framework is normal |
| Testing Exchange API | ✅ Use it | Verify if orders can execute properly |
| Comparing Strategy Effectiveness | ✅ Use it | See how much better your strategy is than "blind buying" |
| Learning Strategy Structure | ✅ Use it | Understand the minimal strategy template |
| Live Trading for Profit | ❌ Don't use | Find a real strategy instead |
| Simulation Trading for Profit | ❌ Don't use | Losing fees, meaningless |

---

## 8. Summary: How Is This Strategy Really?

### One-Sentence Review
> "It's not a strategy, it's a testing tool. Don't expect it to make money."

### Who Should Use It?
- ✅ Freqtrade beginners—verify installation
- ✅ Developers—test framework functionality
- ✅ Strategy researchers—need a benchmark reference
- ✅ Learners—study the minimal strategy structure

### Who Shouldn't Use It?
- ❌ People who want to make money—find a real strategy
- ❌ Live traders—this strategy will make you lose money
- ❌ Fee-sensitive traders—frequent trading fees are high
- ❌ Risk-averse traders—completely unprotected

### My Advice
1. **Only use it to test the framework**: After installing Freqtrade, run this strategy to see if you can place orders
2. **As a strategy template**: Start here to write your own strategy
3. **As a control group**: See how much better your strategy is than "blind buying"
4. **Never use it for live trading**: Seriously, don't. It's not designed to make money.

---

## 9. What "Market" Can This Strategy Make Money In?

### 9.1 Core Logic: Doesn't Look at the Market at All

AlwaysBuy is a **testing tool**, it doesn't analyze any market:

- **No indicators**: Doesn't calculate moving averages, MACD, RSI, nothing
- **No logic**: Entry condition is always true
- **No protection**: No cooldown period, no drawdown protection

**Its Philosophy**: Whatever market you're in, I'm buying anyway!

### 9.2 Performance in Different "Markets" (Plain English Version)

| Market Type | Performance Rating | Plain English Explanation |
|:------------|:-------------------|:---------------------------|
| 📈 Big Bull Market | ⭐⭐⭐☆☆ | Blind buying might profit, but don't know when to sell |
| 🔄 Oscillating Market | ⭐☆☆☆☆ | Buy at the top, stop out, buy again, lose again, fees explode |
| 📉 Big Bear Market | ⭐☆☆☆☆ | Buy and get trapped, wait for 20% stop loss |
| ⚡️ High Volatility | ⭐⭐☆☆☆ | Trailing stop might trigger frequently, double hit from fees and slippage |

**One-sentence summary**: Don't expect this strategy to make money, it wasn't designed to make money.

---

## 10. Want to Run This Strategy? Configuration Recommendations

### 10.1 Trading Pair Configuration

| Configuration Item | Recommended Value | Reason |
|--------------------|-------------------|--------|
| max_open_trades | 1-3 | Limit positions, reduce risk |
| stake_amount | Minimum amount | Don't test with real money |
| dry_run | True | Strongly recommend simulation only |

### 10.2 Key Config File Settings

```yaml
# config.json key configuration
{
    "max_open_trades": 1,
    "stake_amount": "unlimited",  # Or set minimum amount
    "dry_run": true,  # Simulation mode!
    "stoploss": -0.2
}
```

### 10.3 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory | Experience |
|-----------------|----------------|-------------------|------------|
| 1-5 pairs | 512MB | 1GB | Smooth |
| 5-20 pairs | 1GB | 2GB | Smooth |
| 20+ pairs | 2GB | 4GB | Smooth |

**Analysis**: This strategy **calculates no indicators**, so hardware requirements are extremely low. Even a Raspberry Pi can run it.

---

## 11. Easter Egg: The Strategy Author's "Little Thoughts"

Looking carefully at the code, you'll find some interesting things:

1. **ROI Table Design**: Double to take profit? This is clearly not a live trading configuration, but a test configuration
   > "I just want to test if the ROI feature works, who cares about actual returns"

2. **enter_tag called "entry_reason"**: Marking all buy reasons as the same
   > "Since it's all blind buying anyway, just write whatever tag"

3. **INTERFACE_VERSION = 3**: Using the latest interface version
   > "I may be simple, but I keep up with trends"

---

## 12. Final Words

### One-Sentence Review
> "Testing magic tool, making money useless. Use it to verify frameworks, don't use it for live trading."

### Who Should Use It?
- ✅ Beginners configuring Freqtrade
- ✅ Developers wanting to verify exchange connections
- ✅ Strategy researchers needing benchmark comparison
- ✅ Learners wanting to understand minimal strategy structure

### Who Shouldn't Use It?
- ❌ People who want to make money with strategies
- ❌ People who need risk management
- ❌ People sensitive to fees
- ❌ Anyone who wants to use it in live trading

### Advice for Manual Traders

This strategy has no reference value for manual traders. Its buy logic is "unconditional buy," which in manual trading is equivalent to "buy a random stock and pray."

If you must learn something:
- **Trailing stop** configuration can be referenced
- **Strategy structure** can be used as a development template
- **Don't learn its trading logic**—this is the most important lesson 🙏

---

## 13. ⚠️ Risk Re-emphasis (This Part Is a Must-Read)

### Backtesting Looks Great, Live Trading Requires Caution

AlwaysBuy might look "okay" in backtesting (if you chose a trading pair with good upward momentum), but this is pure luck:
> **It has no trading logic, buying anything is based on luck. Choose the wrong pair in backtesting, and you'll see losses.**

### Hidden Risks of Mindless Buying

In live trading, this strategy will cause:
- **Fee Consumption**: Frequent buying and selling, fees accumulate amazingly
- **Slippage Loss**: Market order slippage will further erode returns
- **No Risk Management**: No protection mechanism when losing consecutively

### My Advice (Honest Words)

```
1. Only use dry_run mode for testing
2. Do not invest any real funds
3. After using it to verify the framework, switch to a real strategy
4. If you don't know what a "real strategy" is, learn the basics first
```

**Remember**: This strategy's purpose is to test frameworks, not make money. Use it to learn, use it to test, but don't use it to lose money!

---

**Final Reminder**: No matter how simple the strategy, the market won't be gentle. Testing tools should only be used for testing! 🙏