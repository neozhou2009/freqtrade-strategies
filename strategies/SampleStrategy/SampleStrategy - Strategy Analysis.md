# SampleStrategy Strategy Analysis

> **Strategy Number**: #371 (371st of 465 strategies)  
> **Strategy Type**: Multi-condition Trend Following + Multi-layer Protection Mechanism  
> **Timeframe**: 5 minutes (5m) + 1 hour (1h) informative layer

---

## I. Strategy Overview

**SampleStrategy** is a highly complex trend-following strategy based on the NostalgiaForInfinityV7 architecture. This strategy builds a comprehensive signal capture system with up to 26 independent buy conditions and 8 sell conditions, equipped with multiple layers of dynamic protection mechanisms to ensure entry safety.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 26 independent buy signals, can be enabled/disabled independently |
| **Sell Conditions** | 8 base sell signals + custom_sell dynamic take-profit logic |
| **Protection Mechanisms** | 26 groups of buy protection parameters (EMA filtering, safe Dip, safe Pump, etc.) |
| **Timeframe** | Main timeframe 5m + informative timeframe 1h |
| **Dependencies** | talib, qtpylib, technical (zema) |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "0": 0.10,    # Exit at 10% profit immediately
    "30": 0.05,   # Exit at 5% profit after 30 minutes
    "60": 0.02,   # Exit at 2% profit after 60 minutes
}

# Stop loss setting
stoploss = -0.10   # Fixed stop loss at 10%

# Trailing stop
trailing_stop = True
trailing_only_offset_is_reached = True
trailing_stop_positive = 0.01     # Start trailing at 1% profit
trailing_stop_positive_offset = 0.03  # Begin trailing at 3% profit
```

**Design Rationale**:
- ROI table adopts a progressive design: longer holding time means lower profit target
- 10% fixed stop loss as bottom-line protection
- Trailing stop used to lock in profits, activated after reaching 3% profit

### 2.2 Order Type Configuration

```python
order_types = {
    'buy': 'limit',
    'sell': 'limit',
    'trailing_stop_loss': 'limit',
    'stoploss': 'limit',
    'stoploss_on_exchange': False
}
```

All orders use limit orders to ensure precise price execution.

---

## III. Buy Conditions Detailed Analysis

### 3.1 Protection Mechanisms (26 Groups)

Each buy condition is paired with independent protection parameter groups, including:

| Protection Type | Parameter Description | Default Example |
|-----------------|----------------------|-----------------|
| **EMA Fast Filter** | Check if fast line is above slow line | ema_fast_len: 26/50/100/200 |
| **EMA Slow Filter** | Check slow line trend direction | ema_slow_len: 26/50/100/200 |
| **Close Above EMA** | Verify price position | close_above_ema_fast_len: 12-200 |
| **SMA200 Rising** | Confirm long-term trend upward | sma200_rising_val: 20-50 |
| **1h SMA200 Rising** | Multi-timeframe trend confirmation | sma200_1h_rising_val: 20-50 |
| **Safe Dip Protection** | Prevent entry during crashes | safe_dips_type: 10-100 level |
| **Safe Pump Protection** | Prevent entry after surges | safe_pump_type: 10-120 level |

### 3.2 Typical Buy Condition Examples

#### Condition #1: Basic Trend Buy
```python
# Logic
- EMA fast line > EMA 200 (trend confirmation)
- SMA200 rising (long-term trend upward)
- Safe Dip protection (prevent crash entry)
- Safe Pump protection (prevent post-surge entry)
```

#### Condition #2: EMA Slope Buy
```python
# Logic  
- EMA slow line trend confirmation
- Safe Dip level 50
- Close above EMA verification
```

### 3.3 Classification of 26 Buy Conditions

The strategy's buy conditions can be categorized into the following types:

| Condition Group | Condition Numbers | Core Logic |
|-----------------|-------------------|------------|
| **Trend Type** | 1, 2, 3, 4, 5 | EMA/SMA trend confirmation + protection filtering |
| **RSI+MFI Type** | 6, 7, 8 | RSI indicator combined with money flow |
| **Bollinger Band Type** | 9, 10, 11, 12 | BB lower band breakout + RSI verification |
| **EWO Type** | 13, 16, 17 | Elliott Wave Oscillator signals |
| **Composite Type** | 14, 15, 18, 19, 20, 21, 22, 23, 24, 26 | Multi-indicator combination verification |
| **Special Type** | 25 | Special signal conditions |

---

## IV. Sell Logic Detailed Analysis

### 4.1 Multi-layer Take-Profit System

The strategy adopts a tiered take-profit mechanism, combined with custom_sell:

```
Profit Range        RSI Threshold    Signal Name
─────────────────────────────────────────────────
> 20%              < 34              signal_profit_11
12-20%             < 42              signal_profit_10
10-12%             < 54              signal_profit_9
8-10%              < 54              signal_profit_8
7-8%               < 48              signal_profit_7
6-7%               < 45              signal_profit_6
5-6%               < 43              signal_profit_5
4-5%               < 42              signal_profit_4
3-4%               < 37              signal_profit_3
2-3%               < 35              signal_profit_2
1-2%               < 34              signal_profit_1
0-1%               < 34              signal_profit_0
```

### 4.2 Special Sell Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| **Below EMA200 Take-Profit** | Price below EMA200 + RSI condition | signal_profit_u_* |
| **Post-Pump Take-Profit** | 48h/36h/24h pump identification | signal_profit_p_* |
| **SMA Declining Take-Profit** | SMA200 downtrend + profit range | signal_profit_d_* |
| **Trailing Take-Profit** | Pullback from high + RSI range | signal_profit_t_* |

### 4.3 Base Sell Signals (8 Total)

```python
# Sell Signal 1: RSI + BB combination
- RSI > sell_rsi_bb_1 (79.5)
- Price near BB upper band

# Sell Signal 2: High RSI warning
- RSI > sell_rsi_bb_2 (81)
- Overbought signal confirmation

# Sell Signal 3: Main RSI threshold
- RSI > sell_rsi_main_3 (82)
- Strong overbought confirmation

# Sell Signal 4: Dual RSI confirmation
- 5m RSI > 73.4
- 1h RSI > 79.6

# Sell Signal 5: EMA relative position
- Price deviation from EMA
- RSI difference verification

# Sell Signal 6: RSI below threshold
- RSI > sell_rsi_under_6 (79)
- Overbought pullback confirmation

# Sell Signal 7: 1h RSI trigger
- 1h RSI > sell_rsi_1h_7 (81.7)
- Large timeframe overbought

# Sell Signal 8: BB relative position
- Price exceeds BB middle band by 110%
- Bollinger band deviation sell
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|--------------------|---------------------|---------|
| **Trend Type** | EMA(12,15,20,26,35,50,100,200) | Trend direction confirmation |
| **Trend Type** | SMA(5,30,200) | Long-term trend verification |
| **Momentum Type** | RSI(14) | Overbought/oversold judgment |
| **Momentum Type** | MFI | Money flow verification |
| **Volatility Type** | BB(20,40) - STD2 | Price volatility boundary |
| **Volatility Type** | EWO(50,200) | Elliott Wave Oscillator |
| **Special Type** | ZEMA(61) | Zero-Lag EMA |
| **Special Type** | Choppiness(14) | Market oscillation indicator |

### 5.2 Informative Timeframe Indicators (1h)

The strategy uses 1h as the informative layer, providing higher-dimension trend judgment:

- EMA(12,15,20,26,35,50,100,200) - Large cycle trend
- SMA200 decline detection - 20-period slope judgment
- RSI(14) - Large cycle momentum
- BB(20) - Large cycle volatility range
- CMF(20) - Chaikin Money Flow
- Pump protection calculation - 24/36/48h gain monitoring

---

## VI. Risk Management Features

### 6.1 Dip Protection System

The strategy includes 12 levels of Dip protection parameters, from strict to loose:

| Level | Name | Application Scenario |
|-------|------|---------------------|
| 10 | Strict Dip | Prevent deep drop entry |
| 20-40 | Moderate Dip | Balance drop entry |
| 50-80 | Normal Dip | General drop protection |
| 90-110 | Loose Dip | Higher drop tolerance |

### 6.2 Pump Protection System

Prevent chasing highs after surges:

```
Time Window    Gain Threshold    Pullback Threshold
─────────────────────────────────────────────────────
24h            0.42-0.78         1.5-2.2
36h            0.58-0.78         1.5-2.0
48h            0.8-2.0           1.3-2.0
```

### 6.3 Long-term Position Take-Profit

For positions held over 900-1200 minutes:

```python
sell_custom_long_duration_min_1 = 900  # 15 hours
sell_custom_long_profit_min_1 = 0.03   # 3% profit
sell_custom_long_profit_max_1 = 0.04   # 4% profit
```

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Multi-layer Protection System**: 26 independent protection parameter groups effectively filter false signals
2. **Flexible Buy Combination**: Any buy condition can be independently enabled/disabled for easy optimization
3. **Dynamic Take-Profit Mechanism**: custom_sell provides profit locking and pullback protection
4. **Multi-timeframe Verification**: 1h informative layer provides large-cycle trend confirmation

### ⚠️ Limitations

1. **High Complexity**: Over 300 parameters, difficult to tune
2. **Computational Resource Requirements**: startup_candle_count = 400, requires longer historical data
3. **Overfitting Risk**: Numerous parameters may lead to excellent historical performance but large real trading differences

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|--------------------|---------------------------|-------------|
| **Slow Bull Trend** | Enable all buy conditions | Follow trend, catch pullbacks |
| **Oscillating Market** | Enable BB + RSI conditions | Utilize volatility boundary signals |
| **Downtrend** | Enable strict Dip protection levels | Wait for deep drops before rebound |
| **Surge Market** | Enable strict Pump protection levels | Avoid chasing highs |

---

## IX. Applicable Market Environment Details

**SampleStrategy** is a typical **complex trend-following strategy**. Based on its code architecture, it is most suitable for **mild trend markets**, while performance may be unstable in extreme market conditions.

### 9.1 Strategy Core Logic

- **Multi-layer Protection Philosophy**: Build a defense network through 26 protection parameter groups
- **Tiered Take-Profit Design**: Dynamically adjust sell thresholds based on profit ranges
- **Multi-timeframe Verification**: 1h trend confirmation + 5m entry execution

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 Mild Uptrend | ⭐⭐⭐⭐⭐ | Multi-layer protection effectively filters, trend following is smooth |
| 🔄 Oscillating Sideways | ⭐⭐⭐☆☆ | BB+RSI conditions can catch oscillation, but signals may be too many |
| 📉 Slow Decline | ⭐⭐☆☆☆ | Dip protection prevents crash entry, but frequent stop losses |
| ⚡ Fast Surge | ⭐☆☆☆☆ | Pump protection may prevent entry, missing opportunities |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|--------------------|-------------------|-------------|
| Number of Trading Pairs | 40-80 pairs | Official recommended range |
| Parallel Trades | 4-6 | Balance risk diversification |
| Timeframe | 5m (fixed) | Cannot be changed |
| Trading Pair Type | USDT stable pairs | Avoid BTC/ETH pairs |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Curve

The strategy has over 300 parameters. Understanding all logic requires:
- Familiarity with Freqtrade strategy framework
- Understanding of various technical indicator principles
- Mastery of relationships between protection parameters

### 10.2 Hardware Requirements

| Number of Pairs | Minimum Memory | Recommended Memory |
|-----------------|----------------|-------------------|
| 20-40 | 4GB | 8GB |
| 40-80 | 8GB | 16GB |

### 10.3 Backtest vs Real Trading Differences

Complex strategies often perform better in backtests:
- Backtests cannot simulate slippage and delays
- Many parameters easily fit historical optimum
- Recommend dry-run verification first

### 10.4 Manual Trader Advice

Not recommended for manual traders to use this strategy directly:
- Condition judgment is overly complex
- Requires real-time monitoring of multiple timeframes
- Manual execution difficult to achieve strategy effectiveness

---

## XI. Conclusion

**SampleStrategy** is a **highly complex multi-condition trend-following strategy**. Its core value lies in:

1. **Defensive Design**: 26 protection parameter groups build multiple safety nets
2. **Flexible Combination**: Buy conditions can be independently controlled for targeted optimization
3. **Dynamic Take-Profit**: custom_sell provides profit protection mechanism

For quantitative traders, this strategy is suitable for **experienced users for secondary development**. It is not recommended for beginners to use directly in live trading. Recommend dry-run testing first, and adjust the buy condition enablement combination based on specific markets.

---