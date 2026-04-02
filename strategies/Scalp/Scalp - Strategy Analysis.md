# Scalp Strategy In-Depth Analysis

> **Strategy ID**: #374 (374th of 465 strategies)
> **Strategy Type**: Ultra-Short-Term Quick In-Out Strategy
> **Timeframe**: 1 Minute (1m)

---

## I. Strategy Overview

Scalp is an ultra-short-term (Scalping) strategy focused on capturing small profits, with a design philosophy of "many small wins covering small losses." The strategy uses a 1-minute timeframe with a target take-profit of only 1% and stop-loss of 4%, accumulating returns through high-frequency trading. It is recommended to run at least 60 trading pairs simultaneously to diversify risk and improve overall profit probability.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 1 buy signal, oversold bounce logic |
| **Sell Conditions** | 2 types of sell signals (EMA take-profit + overbought exit) |
| **Protection Mechanisms** | No built-in protection mechanisms (relies on external configuration) |
| **Timeframe** | 1 minute (ultra-short-term) |
| **Dependencies** | talib, qtpylib, pandas |
| **Recommended Simultaneous Positions** | ≥ 60 trading pairs |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.01,  # Take profit at 1% profit
}

# Stop Loss Setting
stoploss = -0.04  # 4% hard stop loss
```

**Design Rationale**:
- **Micro take-profit target**: 1% ROI, pursuing high-frequency small profits
- **Relatively loose stop loss**: 4% stop loss is 4 times the take-profit, single trade risk is relatively high
- **Risk-Reward Ratio**: 1:4, requires high win rate to cover
- **Design Philosophy**: Diversify risk through many trades, use win rate advantage to accumulate returns

### 2.2 Timeframe Selection

```python
timeframe = '1m'  # 1-minute candle
```

**Design Philosophy**:
- Ultra-short-term operations, pursuing quick in and out
- Check for trading opportunities every minute
- High requirements for network latency and exchange response speed

### 2.3 Order Type Configuration

The strategy does not explicitly define `order_types` and will use Freqtrade's default configuration.

---

## III. Buy Conditions Explained

### 3.1 Single Buy Signal

The Scalp strategy uses a single buy signal with simple and clear logic:

```python
# Buy Condition
(
    (dataframe['open'] < dataframe['ema_low']) &      # Open price below EMA low
    (dataframe['adx'] > 30) &                          # ADX > 30 (trend strength)
    (
        (dataframe['fastk'] < 30) &                    # Fast K < 30 (oversold)
        (dataframe['fastd'] < 30) &                   # Fast D < 30 (oversold)
        (qtpylib.crossed_above(dataframe['fastk'], dataframe['fastd']))  # K line crosses above D line
    )
)
```

### 3.2 Buy Logic Breakdown

| Condition | Indicator | Threshold | Meaning |
|-----------|-----------|-----------|---------|
| **Condition 1** | Open price < EMA(5) low | - | Price opens below EMA low |
| **Condition 2** | ADX | > 30 | Sufficient trend strength, not directionless oscillation |
| **Condition 3** | Fast K | < 30 | Stochastic indicator in oversold zone |
| **Condition 4** | Fast D | < 30 | Stochastic indicator confirms oversold |
| **Condition 5** | Fast K crosses above Fast D | - | Stochastic golden cross, reversal signal |

### 3.3 Buy Signal Characteristics

**Signal Type**: Oversold bounce type

**Applicable Scenarios**:
- Short-term bounces in downtrend
- Oversold positions in sideways oscillation
- Pullback entries in trending markets

**Not Applicable Scenarios**:
- One-sided surge (no oversold opportunities)
- Trendless oscillation (ADX < 30)

---

## IV. Sell Logic Explained

### 4.1 ROI Take Profit

```
Profit Threshold    Take Profit Ratio
─────────────────────────────────────────
≥ 1%               Immediate take profit
```

**Design Philosophy**: Pursue small but stable profits, accumulate returns through high-frequency trading.

### 4.2 Sell Signals

The strategy uses two types of sell signals:

```python
# Sell Condition
(
    (dataframe['open'] >= dataframe['ema_high'])  # Condition 1: Open price >= EMA high
) |
(
    (qtpylib.crossed_above(dataframe['fastk'], 70)) |  # Condition 2: Fast K crosses above 70
    (qtpylib.crossed_above(dataframe['fastd'], 70))    # Condition 3: Fast D crosses above 70
)
```

**Sell Signal Classification**:

| Signal Type | Trigger Condition | Meaning |
|------------|-------------------|---------|
| **EMA Take Profit** | Open price >= EMA(5) high | Price bounces to above EMA |
| **Overbought Exit** | Fast K crosses above 70 | Stochastic enters overbought zone |
| **Overbought Exit** | Fast D crosses above 70 | Stochastic confirms overbought |

### 4.3 Sell Logic Characteristics

**Multi-dimensional Exit**:
- EMA direction: Exit when price bounces to EMA level
- Stochastic indicator: Exit when entering overbought, don't be greedy

**Exit Characteristics**:
- Quick in and out, don't hold for too long
- Exit at 1% profit or indicator overbought

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **EMA Series** | EMA(5) high/close/low | Price channel determination |
| **Trend Strength** | ADX | Confirm trend existence |
| **Stochastic** | Stochastic Fast (5,3,3) | Oversold/overbought determination |
| **Bollinger Bands** | 20 period, 2 standard deviations | Auxiliary reference (plotting only) |

### 5.2 EMA Three-Line System

```python
# EMA Calculation
dataframe['ema_high'] = ta.EMA(dataframe, timeperiod=5, price='high')
dataframe['ema_close'] = ta.EMA(dataframe, timeperiod=5, price='close')
dataframe['ema_low'] = ta.EMA(dataframe, timeperiod=5, price='low')
```

**Design Philosophy**:
- Use EMA instead of SMA for faster response
- Calculate EMA for high, close, and low prices separately
- Build dynamic price channel

### 5.3 Stochastic Fast Version

```python
# Stochastic Fast Parameters
stoch_fast = ta.STOCHF(dataframe, 5, 3, 0, 3, 0)
# Parameter explanation: K period 5, K smoothing 3, D smoothing 3
```

**Why Fast Instead of Slow**:
- Fast version responds more quickly, suitable for 1-minute ultra-short-term
- Captures reversal signals earlier
- Sacrifices some stability for speed

---

## VI. Risk Management Features

### 6.1 No Built-in Protection Mechanisms

The strategy code does not define a `protections` attribute, meaning:

- No cooldown period protection
- No maximum drawdown protection
- No stop loss frequency limit
- Completely relies on external configuration

**Recommended Configuration**: Manually add protection mechanisms in `config.json`:

```json
{
  "protections": [
    {
      "method": "CooldownPeriod",
      "stop_duration": 5
    },
    {
      "method": "MaxDrawdown",
      "trade_limit": 20,
      "stop_duration": 60,
      "max_allowed_drawdown": 0.15
    },
    {
      "method": "StoplossGuard",
      "lookback_period": 60,
      "trade_limit": 3,
      "stop_duration": 30
    }
  ]
}
```

### 6.2 Risk-Reward Ratio Analysis

| Item | Value | Analysis |
|------|-------|----------|
| Take Profit Target | 1% | Micro profit |
| Stop Loss Level | 4% | Stop loss is 4 times take profit |
| Risk-Reward Ratio | 1:4 | Requires approximately 80% win rate to break even |

**Risk Warning**:
- Single trade risk is relatively high (4% stop loss)
- Requires high win rate support
- Suitable for diversifying risk with many trades

### 6.3 Multi-Pair Strategy

The strategy author recommends running at least 60 trading pairs simultaneously:

> "we recommend to have at least 60 parallel trades at any time to cover non avoidable losses."

**Design Philosophy**:
- Diversify risk through many parallel trades
- Use win rate advantage to cover individual losses
- Law of large numbers comes into play

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Simple Logic**: Clear buy and sell conditions, easy to understand and maintain
2. **Fast Execution**: 1-minute cycle, quick entry and exit
3. **Streamlined Indicators**: Only uses EMA, ADX, Stochastic three core indicators
4. **Suitable for Quantification**: Clear rules, suitable for automated execution
5. **Clear Take Profit**: 1% target is clear, no greed

### ⚠️ Limitations

1. **Poor Risk-Reward Ratio**: 4% stop loss, 1% take profit, requires extremely high win rate
2. **No Protection Mechanisms**: Needs manual configuration, easily overlooked
3. **Strong Network Dependency**: 1-minute cycle is sensitive to latency
4. **High Trading Costs**: High-frequency trading fees accumulate significantly
5. **Requires Many Trading Pairs**: 60+ pairs have VPS performance requirements

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Explanation |
|-------------------|--------------------------|-------------|
| **Trending Market** | Enable ADX > 30 filter | Strategy depends on trend strength |
| **Oscillating Market** | Use with caution | Won't enter when ADX < 30 |
| **High Volatility** | Suitable | Many oversold bounce opportunities |
| **Low Volatility** | Not suitable | No oversold opportunities |

---

## IX. Applicable Market Environment Details

Scalp is an ultra-short-term strategy with the core of **capturing oversold bounce opportunities**. Based on its code architecture, it is best suited for **high-volatility trending markets**, while performing poorly in **low-volatility trendless markets**.

### 9.1 Strategy Core Logic

- **Oversold Identification**: Stochastic Fast K/D < 30
- **Trend Confirmation**: ADX > 30 ensures directionality
- **Reversal Signal**: K line crosses above D line
- **Quick Exit**: 1% take profit or overbought exit

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|-------------|-------------------|-----------------|
| 📈 Uptrend | ⭐⭐⭐⭐☆ | Many pullback oversold bounce opportunities, but might miss big rallies |
| 🔄 Oscillating Trend | ⭐⭐⭐☆☆ | Won't enter when ADX < 30, misses oscillation opportunities |
| 📉 Downtrend | ⭐⭐☆☆☆ | Bounces might be very weak, high stop loss risk |
| ⚡️ High Volatility | ⭐⭐⭐⭐⭐ | Rich oversold bounce opportunities, suitable for high-frequency trading |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Explanation |
|-------------------|-------------------|-------------|
| Simultaneous Positions | ≥ 60 | Diversify risk |
| Timeframe | 1m | Strategy core, not recommended to modify |
| Stop Loss | -0.03 ~ -0.04 | Can appropriately tighten |
| Trading Fee | 0.001 | Must consider fee impact |

---

## X. Important Reminder: The Cost of High-Frequency Trading

### 10.1 Fee Impact

Ultra-short-term strategies are extremely sensitive to fees:

```
Assuming 0.1% fee:
- Single trade cost: 0.2% (buy + sell)
- 1% take profit, fees take 20%!
- Actual net return: 1% - 0.2% = 0.8%
```

**Recommendations**:
- Use low-fee exchanges
- Consider fee rebates
- Must include fees in backtesting

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|----------------|----------------|-------------------|
| 60 pairs | 4GB | 8GB |
| 100 pairs | 8GB | 16GB |
| 150+ pairs | 16GB | 32GB |

### 10.3 Network Latency Impact

1-minute cycle is sensitive to latency:

- Ideal latency: < 100ms
- Acceptable latency: 100-500ms
- Dangerous latency: > 500ms

**Recommendations**:
- Choose VPS close to exchange
- Use stable network connection
- Avoid trading during peak hours

### 10.4 Backtesting vs Live Trading Differences

High-frequency strategies have significant differences between backtesting and live trading:

| Factor | Backtesting | Live Trading |
|--------|-------------|--------------|
| **Slippage** | Negligible | Significant |
| **Execution Speed** | Instantaneous | Affected by latency |
| **Fees** | May not be included | Must be included |
| **Market Impact** | None | Large orders have impact |

---

## XI. Summary

**Scalp** is a simply designed ultra-short-term strategy. Its core value lies in:

1. **Clear Logic**: Single buy signal, easy to understand and maintain
2. **Fast Execution**: 1-minute cycle, quick in and out
3. **Clear Target**: 1% take profit, no greed

For quantitative traders, this is a strategy suitable for high-frequency trading, but note:

- **Poor Risk-Reward Ratio**: Requires high win rate support
- **No Built-in Protection**: Needs manual configuration
- **Fee Erosion**: High-frequency trading fees accumulate significantly
- **Network Sensitivity**: 1-minute cycle has high latency requirements

It is recommended to fully backtest and configure protection mechanisms before testing with small positions in live trading, and only scale up after confirming effectiveness.

---