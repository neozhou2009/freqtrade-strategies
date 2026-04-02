# Combined_NFIv6_SMA Strategy Analysis

> **Strategy Number**: #127 (127th of 465 strategies)
> **Strategy Type**: Multi-Condition Trend Following + Bollinger Band Rebound + Dynamic Take-Profit
> **Timeframe**: 5 Minutes (5m) + 1 Hour (1h) Dual Timeframe

---

## I. Strategy Overview

**Combined_NFIv6_SMA** is a variant of the NostalgiaForInfinityV6 series created by Freqtrade community developer **iterativ**, fusing the core design philosophy of the NFI (Nostalgia For Infinity) series with SMA (Simple Moving Average) trend filtering. The strategy constructs a complex but efficient buy/sell signal system through multi-layer technical indicator protection mechanisms and multi-timeframe analysis.

From the strategy architecture, Combined_NFIv6_SMA adopts a "protection layer + core signal" dual-layer filtering mechanism. Each buy condition group is equipped with EMA protection, SMA200 trend protection, and special protection mechanisms for "dips" and "pumps." This design significantly reduces the probability of triggering false signals under extreme market conditions.

The strategy's timeframe design embodies "combining long and short": 5 minutes captures short-term trading opportunities, while 1 hour confirms long-term trend direction. This cross-timeframe analysis enables the strategy to maintain good adaptability across different market environments.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 24 independent buy signals, independently enableable/disableable |
| **Sell Conditions** | 8 basic sell signals + multi-layer dynamic take-profit logic + trailing stop |
| **Protection Mechanisms** | 8 groups of buy protection parameters (EMA, SMA200, Dip, Pump, etc.) |
| **Timeframe** | 5-minute primary + 1-hour informational |
| **Dependencies** | TA-Lib, technical (qtpylib), numpy, pandas |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table (time: minimum profit rate)
minimal_roi = {
    "0": 0.10,      # Immediate: 10% profit
    "30": 0.05,     # After 30 minutes: 5% profit
    "60": 0.02,     # After 60 minutes: 2% profit
}

# Stop Loss Settings
stoploss = -0.10   # 10% hard stop-loss

# Trailing Stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.005
trailing_stop_positive_offset = 0.035
```

### 2.2 Order Type Configuration

```python
order_types = {
    'entry': 'limit',           # Limit order entry
    'exit': 'limit',            # Limit order exit
    'stoploss': 'limit',        # Limit order stop-loss
    'stoploss_on_exchange': False
}
```

### 2.3 Exit Signal Configuration

```python
use_exit_signal = True
exit_profit_only = True
ignore_roi_if_entry_signal = True
```

---

## III. Entry Conditions Details

The strategy contains 24 independent buy conditions, each with independent enable/disable switches and protection mechanism configurations.

### 3.1 Protection Mechanisms (8 Groups)

Each buy condition supports independent configuration of the following protection mechanisms:

| Protection Type | Parameter Description | Default Example |
|-----------------|----------------------|-----------------|
| **EMA Fast Protection** | `buy_xx_protection__ema_fast` | True (fast EMA above 200 EMA) |
| **EMA Slow Protection** | `buy_xx_protection__ema_slow` | True (1h EMA above 1h 200 EMA) |
| **Close Above EMA Fast** | `buy_xx_protection__close_above_ema_fast` | Specified EMA period |
| **SMA200 Rising** | `buy_xx_protection__sma200_rising` | True (200-day MA rising) |
| **SMA200 1h Rising** | `buy_xx_protection__sma200_1h_rising` | True (1h 200-day MA rising) |
| **Safe Dips Protection** | `buy_xx_protection__safe_dips` | Enable safe dip detection |
| **Safe Pump Protection** | `buy_xx_protection__safe_pump` | Enable safe pump detection |

### 3.2 Typical Buy Condition Examples

| Condition Group | Condition # | Core Logic |
|----------------|-------------|------------|
| **RSI/MFI Oversold Rebound** | 1, 2 | RSI and MFI simultaneously oversold, with EMA protection |
| **Bollinger Band Rebound** | 3, 4 | BB40/BB20 lower band breakout + volume confirmation |
| **EMA Golden/Death Cross** | 5, 6, 7 | EMA12 crosses above EMA26 + various filtering conditions |
| **RSI Extreme Oversold** | 8, 18, 19, 20, 21 | RSI extremely low (<20) + volume expansion |
| **MA Offset** | 9, 10, 11, 14, 15, 16, 22 | Price below MA by certain percentage + other indicator confirmation |
| **EWO Oscillator** | 12, 13, 16, 17, 22, 23 | Elliot Wave Oscillator captures momentum reversal |

---

## IV. Exit Conditions Details

### 4.1 Multi-Level Take-Profit System

The strategy implements a refined stepped take-profit mechanism:

```
Profit Rate Zone    RSI Threshold    Signal Name
─────────────────────────────────────────────
1%                 < 33            sell_custom_profit_0
2%                 < 34            sell_custom_profit_1
3%                 < 38            sell_custom_profit_2
4%                 < 42            sell_custom_profit_3
5%                 < 43            sell_custom_profit_4
6%                 < 44            sell_custom_profit_5
7%                 < 49            sell_custom_profit_6
8%                 < 54            sell_custom_profit_7
9%                 < 54            sell_custom_profit_8
10%                < 50            sell_custom_profit_9
12%                < 42            sell_custom_profit_10
20%                < 34            sell_custom_profit_11
```

**Design Philosophy**: The more you earn, the more relaxed the exit conditions. As profit increases, the strategy allows RSI to reach higher levels before triggering sells, giving the trend sufficient room to continue.

### 4.2 Special Exit Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| **Sell Below EMA200** | Close below EMA200 with sufficient profit | Specific take-profit trigger |
| **Trailing Stop Mode 1** | Profit 16-60%, RSI 20-50, 3% drawdown from high | trailing_sell_1 |
| **Trailing Stop Mode 2** | Profit 10-40%, RSI 20-50, 3% drawdown | trailing_sell_2 |
| **Trailing Stop Mode 3** | Profit 6-20%, 1h SMA200 declining, 5% drawdown | trailing_sell_3 |
| **Pump Scenario Sell** | After 24/36/48h sharp rise, profit threshold reached | pump_sell |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| **Moving Averages** | EMA (12, 15, 20, 26, 35, 50, 100, 200), SMA (5, 30, 200) | Trend judgment, support/resistance |
| **Momentum Indicators** | RSI (4, 14), MFI | Overbought/oversold judgment |
| **Volatility Indicators** | Bollinger Bands (20, 40 periods) | Price channels, breakout signals |
| **Money Flow Indicators** | CMF (Chaikin Money Flow) | Fund inflow/outflow |
| **Trend Indicators** | HMA (Hull Moving Average) | Smoothed trend judgment |
| **Oscillator** | EWO (Elliot Wave Oscillator) | Momentum reversal signals |

---

## VI. Risk Management Features

### 6.1 Safe Dips (Safe Dips) Protection

Prevents "catching a falling knife":

| Type | Detection Logic (Dip Thresholds) |
|------|----------------------------------|
| **strict** | 1.5%/10%/24%/42% |
| **normal** | 2%/14%/32%/50% |
| **loose** | 2.6%/24%/42%/80% |

### 6.2 Safe Pump (Safe Pump) Protection

Prevents "chasing at the top":

| Type | Period | Rise Threshold | Drawdown Threshold |
|------|--------|---------------|-------------------|
| **strict** | 24h | 0.42 | 2.2 |
| **strict** | 36h | 0.58 | 2.0 |
| **strict** | 48h | 0.80 | 2.0 |
| **normal** | 24h | 0.60 | 1.75 |
| **normal** | 36h | 0.64 | 1.75 |
| **normal** | 48h | 0.85 | 1.75 |
| **loose** | 24h | 0.66 | 1.7 |
| **loose** | 36h | 0.70 | 1.7 |
| **loose** | 48h | 1.60 | 1.4 |

---

## VII. Strategy Pros & Cons

### Advantages

1. **Multi-Layer Protection**: 8 different protection mechanisms significantly reduce false signal probability
2. **Dual-Timeframe Analysis**: Combines 5m and 1h timeframes, balancing short-term opportunities and long-term trends
3. **Refined Take-Profit**: 12-level dynamic take-profit maximizes profits, dynamically adjusting exit conditions
4. **Highly Configurable**: 24 buy conditions and 8 sell conditions can all be independently configured
5. **Strong Trend-Following**: Multiple EMA and SMA confirmations effectively capture trending markets

### Limitations

1. **High Complexity**: Large number of parameters require reasonable configuration; steep learning curve for newcomers
2. **Trading Frequency**: May generate many trades during bull markets; attention needed for fees and slippage
3. **Overfitting Risk**: Large number of parameters may overfit historical data
4. **Computational Requirements**: Dual-timeframe + multi-indicator calculation has hardware requirements

---

## VIII. Applicable Scenarios

| Market Environment | Recommended Configuration | Notes |
|-------------------|--------------------------|-------|
| **Bull Market** | max_open_trades: 4-6, enable all buy conditions | Fully utilize multi-signal opportunities |
| **Wide-Range Volatility** | max_open_trades: 2-3, enable Safe Pump protection | Reduce positions, prevent chasing tops |
| **Bear Market** | max_open_trades: 1-2, enable Safe Dips protection | Cautious bottom-fishing, control risk exposure |
| **Extreme Volatility** | Pause trading or reduce positions | Price limit moves may affect execution |

---

## IX. Live Trading Notes

**Combined_NFIv6_SMA** is the 6th-generation variant of the NostalgiaForInfinity series, inheriting the core design philosophy of the "Hedge Infinity" strategy. Based on its code architecture and community live-trading validated experience, it is best suited for **markets with clear medium-to-long-term trends** and should be used with caution during **high-volatility extreme markets**.

### 9.1 Core Strategy Logic

- **Multi-Condition Resonance**: 24 buy conditions provide diverse entry signals; any single condition triggering enables entry
- **Trend Filtering**: Confirms trends through SMA200 and EMA, avoiding counter-trend trades
- **Reverse Protection**: Safe Dips and Safe Pump prevent bottom-fishing at mid-slope and chasing at peaks
- **Dynamic Take-Profit**: Dynamically adjusts exit conditions based on profit levels

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Analysis |
|:------------|:------------------|:---------|
| Bull Market | ⭐⭐⭐⭐⭐ | Clear trends; multi-condition resonance most effective; trailing stop maximizes trends |
| Volatile Market | ⭐⭐⭐☆☆ | Protection triggers frequently; may miss some opportunities; fee consumption increases |
| Bear Market | ⭐⭐☆☆☆ | Safe Dips active; trading frequency reduced; bottom-fishing signals still require caution |
| Extreme Volatility | ⭐⭐☆☆☆ | Price limit moves may affect execution; slippage increases |

---

## X. Summary

**Combined_NFIv6_SMA** is a meticulously designed, fully-featured trading strategy. It inherits the core philosophy of the NostalgiaForInfinity series, achieving effective control of market risks through multi-layer technical indicator protection mechanisms and refined take-profit/stop-loss design.

Its core value lies in:
1. **Multi-Layer Protection**: 8 protection mechanisms significantly reduce false signal probability
2. **Refined Take-Profit**: 12-level dynamic take-profit maximizes profits
3. **Flexible Configuration**: 24 buy conditions independently enableable/disableable
4. **Dual Timeframe**: Balances short-term opportunities and long-term trends

For quantitative traders, this strategy provides sufficient customization space. Test thoroughly in paper trading before production use, and fine-tune parameters based on actual market conditions. Remember: **no matter how good a strategy is, the market can always teach a lesson. Test with small positions; survival is paramount.**
