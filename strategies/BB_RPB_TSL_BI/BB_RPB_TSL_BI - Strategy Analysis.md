# BB_RPB_TSL_BI Strategy In-Depth Analysis

> **Strategy ID**: #440 (440th of 465 strategies)  
> **Strategy Type**: Multi-Condition Bollinger Band Breakout + Tiered Trailing Stop Loss System  
> **Timeframes**: 5 minutes (5m) + Info frame 1h

---

## I. Strategy Overview

BB_RPB_TSL_BI is a multi-condition quantitative strategy based on Bollinger Band breakouts, belonging to the same strategy family as BB_RPB_TSL_2, but with simplified timeframe configuration. The strategy captures various market patterns through 15 independent buy signals, combined with dynamic take-profit and stop-loss mechanisms for risk control.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 15 independent buy signals, can trigger independently |
| **Sell Conditions** | 20+ base sell signals + tiered dynamic take-profit logic |
| **Protection Mechanisms** | Custom tiered trailing stop loss + slippage confirmation + Dead Fish stop loss |
| **Timeframes** | Main frame 5m + Info frame 1h |
| **Dependencies** | talib, pandas_ta, qtpylib, technical.indicators |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.205,  # 20.5% target profit
}

# Stop Loss Setting
stoploss = -0.10  # 10% fixed stop loss (backup)

# Trailing Stop Loss
use_custom_stoploss = True  # Enable custom stop loss
```

**Design Rationale**:
- ROI set at 20.5%, providing ample profit room
- Fixed stop loss at -10% as a safety net, more aggressive than BB_RPB_TSL_2
- Custom stop loss uses tiered trailing mechanism - the more profit, the tighter the protection

### 2.2 Parameter Differences (Comparison with BB_RPB_TSL_2)

| Parameter | BB_RPB_TSL_2 | BB_RPB_TSL_BI |
|-----------|--------------|---------------|
| Main Timeframe | 3m | 5m |
| Info Frames | 5m + 1h | 1h |
| Fixed Stop Loss | -0.15 | -0.10 |
| Buy Conditions Count | 28 | 15 |

---

## III. Buy Conditions Detailed Analysis

### 3.1 Global Protection Mechanisms (2 Groups)

All buy signals must pass additional checks:

| Protection Type | Parameter Description | Default Value |
|-----------------|----------------------|---------------|
| **ROC_1h** | 1-hour rate of change limit | < 4 (hyperopt) |
| **BB_width_1h** | 1-hour Bollinger Band width limit | < 1.074 (hyperopt) |

```python
is_additional_check = (
    (dataframe['roc_1h'] < self.buy_roc_1h.value) &
    (dataframe['bb_width_1h'] < self.buy_bb_width_1h.value)
)
```

### 3.2 Buy Condition Categories

#### Condition Group 1: Bollinger Band Breakout (2 conditions)

**#1 BB_checked (Dip + Break Combination)**
```python
# Dip Conditions
(dataframe['rmi_length'] < 49) &
(dataframe['cci_length'] <= -116) &
(dataframe['srsi_fk'] < 32)

# Break Conditions
(dataframe['bb_delta'] > 0.025) &
(dataframe['bb_width'] > 0.095) &
(dataframe['closedelta'] > close * 13.494 / 1000) &
(dataframe['close'] < bb_lowerband3 * 0.999)
```

**Core Logic**: RMI oversold + CCI extreme + Stochastic RSI low, combined with lower Bollinger Band breakout and volatility expansion.

---

#### Condition Group 2: Trend Pullback (4 conditions)

**#2 Local Uptrend**
```python
(dataframe['ema_26'] > dataframe['ema_12']) &
(dataframe['ema_26'] - dataframe['ema_12'] > open * 0.024) &
(dataframe['close'] < bb_lowerband2 * 0.999) &
(dataframe['closedelta'] > close * 13.494 / 1000)
```

**Core Logic**: EMA26 > EMA12 (short-term downtrend), price touching 2 standard deviation lower Bollinger Band.

**#3 Local Dip**
```python
(dataframe['ema_26'] > dataframe['ema_12']) &
(dataframe['close'] < ema_20 * 1.084) &
(dataframe['rsi'] < 20) &
(dataframe['crsi'] > 10)
```

**Core Logic**: Local downtrend with deeply oversold RSI (RSI < 20), more extreme bottom-fishing condition.

---

#### Condition Group 3: Elliott Wave (2 conditions)

**#4 EWO (Elliott Wave Oscillator)**
```python
(dataframe['rsi_fast'] < 44) &
(dataframe['close'] < ema_8 * 0.935) &
(dataframe['EWO'] > -5.001) &
(dataframe['close'] < ema_16 * 0.968) &
(dataframe['rsi'] < 23)
```

**Core Logic**: Fast RSI oversold + positive EWO (trend reversal signal) + price below multiple EMAs.

**#5 EWO_2**
```python
(dataframe['ema_200_1h'] > dataframe['ema_200_1h'].shift(12)) &
(dataframe['ema_200_1h'].shift(12) > dataframe['ema_200_1h'].shift(24)) &
(dataframe['rsi_fast'] < 48) &
(dataframe['EWO'] > 4.072) &
(dataframe['rsi'] < 42) &
(dataframe['close'] < ema_8 * 1.164) &
(dataframe['close'] < ema_16 * 1.092)
```

**Core Logic**: 1h EMA200 consecutively rising (strong trend) + high positive EWO + RSI oversold. Note EMA parameters differ from BB_RPB_TSL_2.

---

#### Condition Group 4: Inverse Dead Fish (1 condition)

**#6 R_Deadfish**
```python
(dataframe['ema_100'] < ema_200 * 0.972) &
(dataframe['bb_width'] > 0.091) &
(dataframe['close'] < bb_middleband2 * 0.911) &
(dataframe['volume_mean_12'] > volume_mean_24 * 1.008) &
(dataframe['cti'] < -0.115) &
(dataframe['r_14'] < -44.34)
```

**Core Logic**: More extreme long-term moving averages bearish alignment (EMA100 < EMA200 * 0.972) + moderate Bollinger Band width + volume confirmation.

---

#### Condition Group 5: ClucHA (1 condition)

**#7 ClucHA**
```python
(dataframe['rocr_1h'] > 0.416) &
# Sub-condition A: Bollinger Band 40-period breakout
(dataframe['bb_delta_cluc'] > ha_close * 0.04) &
(dataframe['tail'] < bb_delta_cluc * 0.913) &
(dataframe['ha_close'] < bb_lowerband2_40.shift())
# Sub-condition B: Slow EMA breakout
(dataframe['ha_close'] < ema_slow) &
(dataframe['ha_close'] < 0.04 * bb_lowerband2)
```

**Core Logic**: Heikin Ashi Bollinger Band breakout + 1h ROCR confirmation (threshold lower at 0.416).

---

#### Condition Group 6: COFI (1 condition)

**#8 COFI**
```python
(dataframe['open'] < ema_8 * 1.147) &
(qtpylib.crossed_above(fastk, fastd)) &
(dataframe['fastk'] < 39) &
(dataframe['fastd'] < 28) &
(dataframe['adx'] > 13) &
(dataframe['EWO'] > 8.594) &
(dataframe['cti'] < -0.892) &
(dataframe['r_14'] < -85.016)
```

**Core Logic**: Same as BB_RPB_TSL_2, Stochastic Fast golden cross + ADX trend strength + extremely high EWO + multiple oversold confirmations.

---

#### Condition Group 7: NFI/NFIX (6 conditions)

**#9 NFI_13**
```python
(dataframe['ema_50_1h'] > ema_100_1h) &
(dataframe['close'] < sma_30 * 0.99) &
(dataframe['cti'] < -0.92) &
(dataframe['EWO'] < -5.585) &
(dataframe['cti_1h'] < -0.88) &
(dataframe['crsi_1h'] > 10.0)
```

**#10 NFI_32**
```python
(dataframe['rsi_slow'] < rsi_slow.shift(1)) &
(dataframe['rsi_fast'] < 46) &
(dataframe['rsi'] > 25.0) &
(dataframe['close'] < sma_15 * 0.93) &
(dataframe['cti'] < -0.9)
```

**#11 NFI_33**
```python
(dataframe['close'] < ema_13 * 0.978) &
(dataframe['EWO'] > 8) &
(dataframe['cti'] < -0.88) &
(dataframe['rsi'] < 32) &
(dataframe['r_14'] < -98.0)
```

**#12 NFI_38**
```python
(dataframe['pm'] > pmax_thresh) &
(dataframe['close'] < sma_75 * 0.98) &
(dataframe['EWO'] < -4.4) &
(dataframe['cti'] < -0.95) &
(dataframe['r_14'] < -97)
```

**#13 NFIX_5**
```python
(dataframe['ema_200_1h'] > ema_200_1h.shift(12)) &
(dataframe['ema_200_1h'].shift(12) > ema_200_1h.shift(24)) &
(dataframe['close'] < sma_75 * 0.932) &
(dataframe['EWO'] > 3.6) &
(dataframe['cti'] < -0.9) &
(dataframe['r_14'] < -97.0)
```

**#14 NFIX_49**
```python
# 3-period delayed condition combination
(dataframe['ema_26'].shift(3) > ema_12.shift(3)) &
(dataframe['close'].shift(3) < ema_20.shift(3) * 0.916) &
(dataframe['rsi'].shift(3) < 32.5) &
(dataframe['cti'] < -0.105) &
(dataframe['r_14'] < -81.827)
```

**#15 NFIX_51** (New Condition)
```python
(dataframe['close'].shift(3) < ema_16.shift(3) * 0.944) &
(dataframe['EWO'].shift(3) < -1.0) &
(dataframe['rsi'].shift(3) > 28.0) &
(dataframe['cti'].shift(3) < -0.84) &
(dataframe['r_14'].shift(3) < -94.0) &
(dataframe['rsi'] > 30.0) &
(dataframe['crsi_1h'] > 1.0)
```

---

### 3.3 Summary Table of 15 Buy Conditions

| Condition Group | Condition # | Core Logic | Backtest Win Rate |
|-----------------|-------------|------------|-------------------|
| BB Breakout | #1 BB_checked | Dip + Break combination | ~90.9% |
| Trend Pullback | #2 Local Uptrend | EMA downtrend pullback | ~92.3% |
| Trend Pullback | #3 Local Dip | Local decline RSI oversold | ~97.8% |
| EWO | #4 EWO | Elliott Wave positive | ~86.4% |
| EWO | #5 EWO_2 | 1h EMA200 rising + EWO | ~87.0% |
| Dead Fish | #6 R_Deadfish | Inverse dead fish pattern | ~93.9% |
| ClucHA | #7 ClucHA | HA Bollinger breakout | ~93.4% |
| COFI | #8 COFI | Stoch cross + ADX | ~89.1% |
| NFI | #9-12 | NFI series | 83%-100% |
| NFIX | #13-15 | NFIX series | 97%-100% |

---

## IV. Sell Logic Detailed Analysis

### 4.1 Tiered Trailing Take-Profit System

The strategy uses a 4-level dynamic trailing stop loss (same as BB_RPB_TSL_2):

```
Profit Range      Protection Stop    Signal Name
─────────────────────────────────────────────────
> 20%            5%                 custom_stoploss_20
> 10%            3%                 custom_stoploss_10
> 6%             2%                 custom_stoploss_6
> 3%             1.5%               custom_stoploss_3
```

### 4.2 Profit Trailing Sell (12 signals)

| Profit Range | Trigger Condition | Signal Name |
|--------------|-------------------|-------------|
| 0-1.2% | max_profit > current + 4.5%, RSI < 46 | sell_profit_t_0_1 |
| 0-1.2% | max_profit > current + 2.5%, RSI < 32 | sell_profit_t_0_2 |
| 1.2-2% | max_profit > current + 1%, RSI < 39 | sell_profit_t_1_1 |
| 1.2-2% | CMF double-period negative confirmation | sell_profit_t_1_2 |
| ... | ... | ... |

### 4.3 Special Sell Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| MOMDIV | momdiv_sell_1h = True, profit > 2% | signal_profit_q_momdiv_1h |
| Quick Take Profit | profit 2-6%, RSI > 80 | signal_profit_q_1 |
| Extreme CTI | profit 2-6%, CTI > 0.95 | signal_profit_q_2 |
| PMAX | PMAX indicator breaks threshold | signal_profit_q_pmax_bull/bear |
| Dead Fish Stop Loss | profit < -5%, BB width low, volume shrinking | sell_stoploss_deadfish |
| Emergency Stop Loss | profit < -5%, CMF/EMA/RSI combination | sell_stoploss_u_e_1 |

### 4.4 Sell Differences from BB_RPB_TSL_2

BB_RPB_TSL_BI's emergency stop loss adds the `sell_rsi_delta` parameter:

```python
# BB_RPB_TSL_BI Emergency Stop Loss
(current_profit < -0.05) &
(close < ema_200 * sell_ema.value) &
(cmf < sell_cmf.value) &
(((ema_200 - close) / close) < sell_ema_close_delta.value) &
(rsi > previous_rsi) &
(rsi > (rsi_1h + sell_rsi_delta.value))  # New RSI cross-period confirmation
```

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Usage |
|--------------------|---------------------|-------|
| **Bollinger Bands** | BB(20,2), BB(20,3), BB(40,2) | Oversold breakout identification |
| **Moving Averages** | EMA 8/12/13/16/20/26/50/100/200, SMA 9/15/21/30/75 | Trend determination |
| **Momentum** | RSI(4/14/20), RMI, CCI, StochRSI, StochFast | Oversold/overbought determination |
| **Volatility** | CTI, Williams %R(14/32/64/96/480), CRSI | Extreme value identification |
| **Volume** | CMF, Volume_mean, MFI | Liquidity determination |
| **Special** | EWO, PMAX, MOMDIV, ROCR | Advanced signals |

### 5.2 Info Timeframe Indicators (1h)

The strategy uses 1h as the information layer, providing higher-dimensional trend judgment:

- EMA 50/100/200 for long-term trend direction
- CTI_1h, CRSI_1h, RSI_1h for cross-period momentum confirmation
- BB_width_1h, ROC_1h for volatility filtering
- MOMDIV_1h for momentum divergence signals
- Williams %R(480) for long-period extremes

---

## VI. Risk Management Features

### 6.1 Tiered Trailing Stop Loss

Automatically tightens stop loss after profit, achieving "more profit, tighter protection":

```python
# After 20% profit, only allow 5% pullback
# After 10% profit, only allow 3% pullback
# After 6% profit, only allow 2% pullback
# After 3% profit, only allow 1.5% pullback
```

### 6.2 Slippage Confirmation Mechanism

Verifies actual entry price through `confirm_trade_entry` function:

```python
slippage = (rate / dataframe['close'] - 1) * 100
if slippage < max_slip:  # Default 0.33%
    return True
```

### 6.3 Dead Fish Stop Loss

Special stop loss scenario for liquidity exhaustion:

```python
(current_profit < -0.05) &
(close < ema_200) &
(bb_width < 0.043) &
(close > bb_middleband2 * 0.954) &
(volume_mean_12 < volume_mean_24 * 2.37)
```

---

## VII. Strategy Advantages and Limitation

### ✅ Advantages

1. **Moderate Computation**: Only dual timeframe, CPU consumption lower than BB_RPB_TSL_2
2. **Rich Signals**: 15 buy conditions cover main market patterns
3. **Flexible Stop Loss**: Tiered trailing stop loss balances profit protection with trend following
4. **Cross-Period Confirmation**: 1h information frame improves signal reliability
5. **Hyperopt Tunable**: Many parameters support hyperparameter optimization

### ⚠️ Limitations

1. **Many Parameters**: Large Hyperopt space, time-consuming optimization
2. **Overfitting Risk**: 15 conditions may lead to inflated historical backtest results
3. **Live Trading Differences**: Complex logic may produce unexpected behavior in live trading
4. **Aggressive Stop Loss**: -10% fixed stop loss more aggressive than BB_RPB_TSL_2
5. **High Trading Frequency**: 5m frame may lead to high-frequency trading

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|--------------------|---------------------------|-------------|
| Slow Bull Trend | Enable EWO_2, NFIX series | Trend pullback strategies perform well |
| Oscillating Market | Enable BB_checked, ClucHA | Bollinger Band breakout captures volatility |
| Fast Decline | Enable NFI_13, Local Dip | Deep oversold bottom-fishing conditions |
| High Volatility Coins | Lower max_slip, raise stop loss | Reduce abnormal execution risk |

---

## IX. Applicable Market Environment Details

BB_RPB_TSL_BI is a simplified version of BB_RPB_TSL_2, suitable for users with limited hardware resources who still want to use multi-condition strategies. Based on its code architecture and community long-term live trading verification, it is best suited for **oscillating pullback markets**.

### 9.1 Strategy Core Logic

- **Multi-Condition Coverage**: 15 buy signals cover oversold, pullback, breakout, and other main patterns
- **Tiered Stop Loss**: More profit leads to tighter stop loss, adapting to multiple entries in oscillating markets
- **Cross-Period Confirmation**: 1h trend filter, improving signal quality

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|-------------|-------------------|-----------------|
| 📈 Slow Bull Trend | ⭐⭐⭐⭐⭐ | EWO_2, NFIX series capture trend pullbacks |
| 🔄 Oscillating Market | ⭐⭐⭐⭐☆ | BB_checked, ClucHA capture Bollinger Band breakouts |
| 📉 Slow Bear Decline | ⭐⭐⭐☆☆ | Local Dip, NFI_13 bottom-fishing has risk |
| ⚡️ Rapid Crash | ⭐⭐☆☆☆ | Liquidity exhaustion risk |
| 📊 Sideways Consolidation | ⭐⭐☆☆☆ | Few condition triggers, low capital utilization |

### 9.3 Comparison with BB_RPB_TSL_2

| Feature | BB_RPB_TSL_2 | BB_RPB_TSL_BI |
|---------|--------------|---------------|
| Computation Complexity | High (three timeframes) | Medium (dual timeframes) |
| Buy Conditions Count | 28 | 15 |
| Fixed Stop Loss | -15% | -10% |
| Hardware Requirements | High | Medium |
| Target Users | Advanced users | Intermediate users |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

BB_RPB_TSL_BI has about 600 lines of code, including:
- 15 buy condition combinations
- 20+ sell signals
- 2 timeframe indicator calculations
- Custom stop loss logic

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 10-20 | 2 GB | 4 GB |
| 30-50 | 4 GB | 8 GB |
| 50+ | 8 GB | 16 GB |

Lower hardware requirements than BB_RPB_TSL_2, suitable for regular VPS.

### 10.3 Backtest vs Live Trading Differences

Complex strategies' backtest performance is often **extremely excellent**, but live trading may show:
- Order execution delays causing missed signals
- Slippage exceeding expectations causing premature stop loss triggers
- Inability to exit at expected prices when liquidity is insufficient

---

## XI. Summary

**BB_RPB_TSL_BI** is a simplified version of BB_RPB_TSL_2, retaining the core logic of multi-condition buying but reducing computational complexity. Its core value lies in:

1. **Moderate Coverage**: 15 conditions cover main oversold, pullback, breakout patterns
2. **Efficient Computation**: Dual timeframe, moderate CPU consumption
3. **Intelligent Stop Loss**: Tiered trailing stop loss balances profit protection with trend following

For quantitative traders, this strategy is suitable for intermediate users who need:
- Moderate hardware resources
- Basic understanding of parameter optimization
- Live testing to verify backtest result reliability