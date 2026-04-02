# Schism6 Strategy Analysis

> **Strategy ID**: #381 (381st of 465 strategies)
> **Strategy Type**: Multi-Timeframe Trend Following + Dynamic Position Management
> **Timeframe**: 5 minutes (5m) + 1 hour (1h informative layer)

---

## I. Strategy Overview

Schism6 is a quantitative trading strategy that combines multi-timeframe analysis with dynamic position management. It filters entry opportunities through 1-hour level trend assessment, executes trades at the 5-minute level, and introduces a linear growth function to dynamically adjust parameters for adaptive risk control.

### Core Characteristics

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 modes (new entry + DCA/add-on), each with multiple condition combinations |
| **Sell Conditions** | Dynamic stop-loss logic + tiered ROI exits + trend reversal signals |
| **Protection Mechanisms** | Dynamic linear growth stop-loss, peak profit protection, slot management |
| **Timeframe** | 5m (main) + 1h (informative layer) |
| **Dependencies** | numpy, talib, qtpylib, arrow, pandas, cachetools, technical.indicators.RMI |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.025,    # 2.5% profit immediately
    "10": 0.015,   # Drop to 1.5% after 10 minutes
    "20": 0.01,    # Drop to 1% after 20 minutes
    "30": 0.005,   # Drop to 0.5% after 30 minutes
    "120": 0       # Break-even exit after 120 minutes
}

# Stop-loss setting
stoploss = -0.10  # 10% hard stop-loss

# Enable sell signals
use_sell_signal = True
sell_profit_only = True
ignore_roi_if_buy_signal = True  # Ignore ROI when buy signal is active
```

**Design Philosophy**:
- Uses declining ROI design to encourage quick short-term profits
- Break-even exit after 2 hours to avoid prolonged position risk
- 10% hard stop-loss as final defense, but dynamic stop-loss triggers earlier

### 2.2 Order Type Configuration

The strategy does not explicitly configure `order_types` and will use freqtrade defaults.

### 2.3 Buy Parameters

```python
buy_params = {
    'inf-pct-adr': 0.86884,  # ADR percentage threshold
    'inf-rsi': 65,           # 1-hour RSI threshold
    'mp': 53,                # MP indicator threshold
    'rmi-fast': 41,          # RMI fast line threshold
    'rmi-slow': 33           # RMI slow line threshold
}
```

---

## III. Buy Conditions Explained

### 3.1 Technical Indicator System

The strategy calculates the following core indicators:

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| RMI Series | RMI Slow (21,5), RMI Fast (8,4) | Trend judgment and overbought/oversold |
| ROC | ROC (period 6) | Rate of price change |
| MP | ROC's RSI (period 6) | Rate of change strength |
| RMI Trend | RMI uptrend/downtrend (3 periods) | Trend continuity judgment |

### 3.2 Informative Timeframe Indicators (1h)

The strategy uses 1 hour as the informative layer for higher-level trend assessment:

- **RSI (14)**: Determines larger timeframe overbought/oversold
- **1-Day High**: Highest price in 24 1h candles
- **3-Day Low**: Lowest price in 72 1h candles
- **ADR (Average Daily Range)**: 1-day high - 3-day low

### 3.3 Buy Condition Categories

#### Mode 1: New Entry (No Position)

```python
# Logic
- 1-hour RSI >= 65 (large timeframe strength)
- Close price <= 3-day low + 86.884% ADR (near support level)
- RMI downtrend == 1 (in pullback)
- RMI slow >= 33 (not extremely weak)
- RMI fast <= 41 (fast line not overbought)
- MP <= 53 (moderate price rate of change)
```

**Design Philosophy**: Enter during pullbacks under strong 1-hour level conditions, waiting for rebounds.

#### Mode 2: Add-on/DCA (Has Position)

```python
# Logic
- RMI uptrend == 1 (trend continuation)
- Current profit > peak profit * profit factor (profit protection)
- RMI slow >= linear growth value (dynamic threshold)
```

**Linear Growth Function**:
```python
def linear_growth(self, start: float, end: float, start_time: int, end_time: int, trade_time: int) -> float:
    time = max(0, trade_time - start_time)
    rate = (end - start) / (end_time - start_time)
    return min(end, start + (rate * time))
```

When adding positions, the RMI threshold grows linearly from 30 to 70, spanning 180 to 720 minutes (3 to 12 hours), achieving dynamic control where longer holding periods require higher add-on thresholds.

---

## IV. Sell Logic Explained

### 4.1 Dynamic Stop-Loss System

The strategy uses time-based dynamic stop-loss:

```python
# Linear growth stop-loss
loss_cutoff = linear_growth(-0.03, 0, 0, 300, trade_time)
```

- **0 minutes**: Stop-loss threshold at -3%
- **300 minutes**: Stop-loss threshold at 0% (break-even)
- **Intermediate times**: Linear interpolation

**Sell Condition Combination**:
```
Current profit < dynamic stop-loss threshold
AND current profit > hard stop-loss (-10%)
AND RMI downtrend == 1
AND volume > 0
```

### 4.2 Trend Reversal Signals

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| Has peak profit | RMI slow crosses below 50 | Trend weakening signal |
| No peak profit | RMI slow crosses below 10 | Extreme weakness signal |

### 4.3 Slot Management Mechanism

The strategy monitors profit/loss status of other trading pairs:

```python
if trade_data['other_trades']:
    if trade_data['free_slots'] > 0:
        # Has free slots, requires other pairs to be profitable
        hold_pct = (trade_data['free_slots'] / 100) * -1
        conditions.append(trade_data['avg_other_profit'] >= hold_pct)
    else:
        # No free slots, must be biggest loser to sell
        conditions.append(trade_data['biggest_loser'] == True)
```

**Design Philosophy**: Avoid missing rebounds after clearing losing positions while utilizing slot status to optimize capital efficiency.

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend | RMI Slow (21,5), RMI Fast (8,4) | Main trend and signal line |
| Momentum | ROC (6), MP (RSI of ROC) | Price rate of change and strength |
| Multi-timeframe | 1h RSI, ADR | Large timeframe trend filtering |
| Trend Determination | RMI uptrend/downtrend (3 periods) | Trend continuity |

### 5.2 RMI Indicator Explained

**RMI (Relative Momentum Index)** is a variant of RSI:

```python
from technical.indicators import RMI
dataframe['rmi-slow'] = RMI(dataframe, length=21, mom=5)
dataframe['rmi-fast'] = RMI(dataframe, length=8, mom=4)
```

- **RMI Slow (21,5)**: Used to determine main trend direction
- **RMI Fast (8,4)**: Used to identify short-term overbought/oversold

---

## VI. Risk Management Features

### 6.1 Dynamic Parameter System

The strategy introduces `linear_growth` function for time-based parameter adjustment:

| Application | Start Value | End Value | Start Time | End Time |
|-------------|-------------|-----------|------------|----------|
| Add-on RMI threshold | 30 | 70 | 180 min | 720 min |
| Stop-loss threshold | -3% | 0% | 0 min | 300 min |

### 6.2 Trade Status Tracking

```python
def populate_trades(self, pair: str) -> dict:
    # Returns dictionary containing:
    # - active_trade: whether has active trade
    # - current_profit: current profit rate
    # - peak_profit: peak profit rate
    # - open_minutes: holding minutes
    # - other_trades: whether other trades exist
    # - avg_other_profit: average profit of other trades
    # - biggest_loser: whether is biggest loser
    # - free_slots: number of free slots
```

### 6.3 Price Caching Mechanism

```python
custom_current_price_cache: TTLCache = TTLCache(maxsize=100, ttl=300)
```

Uses TTLCache to cache current price with 5-minute TTL, reducing API calls.

### 6.4 Order Timeout Protection

```python
def check_buy_timeout(self, pair: str, trade: Trade, order: dict, **kwargs) -> bool:
    # Buy order: cancel if current price > order price by 1%
    return current_price > order['price'] * 1.01

def check_sell_timeout(self, pair: str, trade: Trade, order: dict, **kwargs) -> bool:
    # Sell order: cancel if current price < order price by 1%
    return current_price < order['price'] * 0.99
```

### 6.5 Entry Confirmation Mechanism

```python
def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float, time_in_force: str, **kwargs) -> bool:
    # Reject entry if current price > limit price by 1%
    return current_price <= rate * 1.01
```

---

## VII. Strategy Advantages and Limitations

### Advantages

1. **Multi-Timeframe Confirmation**: Combines 1-hour trend with 5-minute entries for higher win rate
2. **Dynamic Parameter Adjustment**: Longer holding periods mean higher add-on thresholds, looser stop-loss
3. **Intelligent Slot Management**: Optimizes sell decisions based on global position status
4. **Peak Profit Protection**: Dynamically adjusts profit factor using peak profit rate
5. **Order Execution Protection**: Timeout cancellation and entry confirmation reduce slippage risk

### Limitations

1. **High Complexity**: Many parameters require deep understanding to optimize
2. **Depends on Live Data**: `populate_trades` relies on database queries, requires special attention in backtesting
3. **High Computational Cost**: Each calculation queries position status, has hardware requirements
4. **Parameter Sensitivity**: Buy parameters are optimized, may need re-tuning for different markets

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Slow Bull Trend | Default parameters | Strategy's intended design, enter on pullbacks |
| Oscillating Market | Raise stop-loss threshold | Reduce stop-loss frequency, wait for breakout |
| Rapid Decline | Disable | Multi-timeframe RSI may fail |
| High Volatility | Widen stop-loss range | Avoid being stopped by noise |

---

## IX. Applicable Market Environment Details

Schism6 is a **trend pullback strategy**. Based on its code architecture, it performs best in **slow bull or moderate uptrend markets**, and performs poorly in **sustained decline or extreme volatility**.

### 9.1 Core Strategy Logic

- **Multi-Timeframe Confirmation**: 1-hour RSI >= 65 ensures large timeframe strength
- **Pullback Entry**: Find rebound opportunities during RMI downtrend
- **Dynamic Risk Control**: Longer holding periods mean looser risk control (giving trends more time)

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|------------|--------|----------|
| Slow Bull Trend | Excellent | Pullback entry logic perfectly matches, multi-timeframe confirmation improves win rate |
| Moderate Oscillation | Average | May trigger stop-losses frequently, but add-on logic can lower cost |
| Sustained Decline | Poor | RSI strength condition fails, pullbacks may become continued decline |
| Extreme Volatility | Very Poor | Multiple indicators may conflict, high slippage risk |

### 9.3 Key Configuration Recommendations

| Configuration | Recommended Value | Description |
|--------------|-------------------|-------------|
| startup_candle_count | 72 | Need sufficient historical data for indicators |
| inf_timeframe | 1h | Can adjust to 4h based on market volatility |
| stoploss | -0.10 | Can adjust based on risk preference |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Curve

The strategy involves multiple custom indicators and dynamic parameter systems, requiring understanding of:
- RMI indicator calculation and meaning
- Linear growth function parameter tuning
- Slot management mechanism trigger conditions
- Multi-timeframe analysis comprehensive judgment

### 10.2 Hardware Requirements

| Trading Pairs | Minimum Memory | Recommended Memory |
|--------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 11-30 pairs | 4GB | 8GB |
| 30+ pairs | 8GB | 16GB |

**Note**: `populate_trades` queries database on every call, needs optimization with many trading pairs.

### 10.3 Backtesting vs Live Differences

The strategy executes complete trade status tracking logic in `live` and `dry_run` modes, but backtesting returns empty data from `populate_trades`, causing:
- Add-on logic not triggering
- Slot management logic not executing
- Dynamic stop-loss needs to rely on `custom_stoploss` (not currently implemented)

### 10.4 Manual Trader Recommendations

- Focus on whether 1-hour RSI >= 65
- Wait for pullback when RMI slow >= 33 and RMI fast <= 41
- Use ADR to determine support zone
- Note holding time's effect on risk control parameters

---

## XI. Summary

**Schism6** is an **elegantly designed trend pullback strategy**. Its core value lies in:

1. **Multi-Timeframe Confirmation**: Uses 1-hour trend to filter 5-minute entry signals
2. **Dynamic Parameter System**: Longer holding periods mean looser parameters
3. **Intelligent Capital Management**: Optimizes decisions based on global position status

For quantitative traders, this is a strategy that requires deep understanding to realize its potential, suitable for experienced developers for further optimization and live verification.

---