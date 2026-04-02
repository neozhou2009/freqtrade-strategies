# BB_RPB_TSL_2 Strategy In-Depth Analysis

> **Strategy ID**: #439 (439th of 465 strategies)  
> **Strategy Type**: Multi-Condition Bollinger Band Breakout + Tiered Trailing Stop Loss System  
> **Timeframes**: 3 minutes (3m) + Info frame 5m + 1h

---

## I. Strategy Overview

BB_RPB_TSL_2 is a multi-condition quantitative strategy based on Bollinger Band breakouts, incorporating Real Pull Back (RPB) pullback identification logic and a custom tiered trailing stop loss system. The strategy captures various market patterns through 28 independent buy signals, combined with dynamic take-profit and stop-loss mechanisms for risk control.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 28 independent buy signals (14 on 3m frame + 14 mirrored on 5m frame), can trigger independently |
| **Sell Conditions** | 20+ base sell signals + tiered dynamic take-profit logic |
| **Protection Mechanisms** | Custom tiered trailing stop loss + slippage confirmation + Dead Fish stop loss |
| **Timeframes** | Main frame 3m + Info frames 5m + 1h |
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
stoploss = -0.15  # 15% fixed stop loss (backup)

# Trailing Stop Loss
use_custom_stoploss = True  # Enable custom stop loss
```

**Design Rationale**:
- ROI set at 20.5%, providing ample profit room
- Fixed stop loss at -15% as a safety net, primarily controlling risk through custom stop loss
- Custom stop loss uses tiered trailing mechanism - the more profit, the tighter the protection

### 2.2 Order Type Configuration

The strategy uses standard order types by default, with slippage verification through the `confirm_trade_entry` function.

```python
# Slippage Control
max_slip = DecimalParameter(0.33, 0.80, default=0.33)
```

---

## III. Buy Conditions Detailed Analysis

### 3.1 Global Protection Mechanisms (2 Groups)

All buy signals must pass additional checks:

| Protection Type | Parameter Description | Default Value |
|-----------------|----------------------|---------------|
| **ROC_1h** | 1-hour rate of change limit | < 86 (hyperopt) |
| **BB_width_1h** | 1-hour Bollinger Band width limit | < 0.954 (hyperopt) |

```python
is_additional_check = (
    (dataframe['roc_1h'] < self.buy_roc_1h.value) &
    (dataframe['bb_width_1h'] < self.buy_bb_width_1h.value)
)
```

### 3.2 Buy Condition Categories

#### Condition Group 1: Bollinger Band Breakout (4 conditions)

**#1 BB_checked (Dip + Break Combination)**
```python
# Dip Conditions
(dataframe['rmi_length'] < 49) &
(dataframe['cci_length'] <= -116) &
(dataframe['srsi_fk'] < 32)

# Break Conditions
(dataframe['bb_delta'] > 0.025) &
(dataframe['bb_width'] > 0.095) &
(dataframe['closedelta'] > close * 17.922 / 1000) &
(dataframe['close'] < bb_lowerband3 * 0.999)
```

**Core Logic**: RMI oversold + CCI extreme + Stochastic RSI low, combined with lower Bollinger Band breakout and volatility expansion.

---

#### Condition Group 2: Trend Pullback (5 conditions)

**#2 Local Uptrend**
```python
(dataframe['ema_26'] > dataframe['ema_12']) &
(dataframe['ema_26'] - dataframe['ema_12'] > open * 0.026) &
(dataframe['close'] < bb_lowerband2 * 0.999) &
(dataframe['closedelta'] > close * 17.922 / 1000)
```

**Core Logic**: EMA26 > EMA12 (short-term downtrend), price touching 2 standard deviation lower Bollinger Band.

**#3 Local Dip**
```python
(dataframe['ema_26'] > dataframe['ema_12']) &
(dataframe['close'] < ema_20 * 1.014) &
(dataframe['rsi'] < 21) &
(dataframe['crsi'] > 10)
```

**Core Logic**: Local downtrend with deeply oversold RSI but CRSI not at extremes.

---

#### Condition Group 3: Elliott Wave (3 conditions)

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
(dataframe['rsi_fast'] < 45) &
(dataframe['EWO'] > 4.179) &
(dataframe['rsi'] < 35)
```

**Core Logic**: 1h EMA200 consecutively rising (strong trend) + high positive EWO + RSI oversold.

---

#### Condition Group 4: Inverse Dead Fish (1 condition)

**#6 R_Deadfish**
```python
(dataframe['ema_100'] < ema_200 * 1.054) &
(dataframe['bb_width'] > 0.299) &
(dataframe['close'] < bb_middleband2 * 1.014) &
(dataframe['volume_mean_12'] > volume_mean_24 * 1.59) &
(dataframe['cti'] < -0.115) &
(dataframe['r_14'] < -44.34)
```

**Core Logic**: Long-term moving averages in bearish alignment but Bollinger Band width expanding + volume increasing + CTI/Williams %R oversold.

---

#### Condition Group 5: ClucHA (1 condition)

**#7 ClucHA**
```python
(dataframe['rocr_1h'] > 0.526) &
# Sub-condition A: Bollinger Band 40-period breakout
(dataframe['bb_delta_cluc'] > ha_close * 0.049) &
(dataframe['tail'] < bb_delta_cluc * 1.146) &
(dataframe['ha_close'] < bb_lowerband2_40.shift())
# Sub-condition B: Slow EMA breakout
(dataframe['ha_close'] < ema_slow) &
(dataframe['ha_close'] < 0.018 * bb_lowerband2)
```

**Core Logic**: Heikin Ashi Bollinger Band breakout + 1h ROCR strength confirmation.

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

**Core Logic**: Stochastic Fast golden cross + ADX trend strength + extremely high EWO + multiple oversold confirmations.

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

---

### 3.3 Summary Table of 28 Buy Conditions

| Condition Group | Condition # | Core Logic | Backtest Win Rate |
|-----------------|-------------|------------|-------------------|
| BB Breakout | #1 BB_checked | Dip + Break combination | ~91.1% |
| Trend Pullback | #2 Local Uptrend | EMA downtrend pullback | ~92.4% |
| Trend Pullback | #3 Local Dip | Local decline RSI oversold | ~91.1% |
| EWO | #4 EWO | Elliott Wave positive | ~92.0% |
| EWO | #5 EWO_2 | 1h EMA200 rising + EWO | ~89.6% |
| Dead Fish | #6 R_Deadfish | Inverse dead fish pattern | ~86.9% |
| ClucHA | #7 ClucHA | HA Bollinger breakout | ~86.6% |
| COFI | #8 COFI | Stoch cross + ADX | ~94.4% |
| NFI | #9-14 | NFI/NFIX series | 83%-100% |
| **Mirrored 5m** | #15-28 | 5m frame versions of above 14 | Same as above |

---

## IV. Sell Logic Detailed Analysis

### 4.1 Tiered Trailing Take-Profit System

The strategy uses a 4-level dynamic trailing stop loss:

```
Profit Range      Protection Stop    Signal Name
─────────────────────────────────────────────────
> 20%            5%                 custom_stoploss_20
> 10%            3%                 custom_stoploss_10
> 6%             2%                 custom_stoploss_6
> 3%             1.5%               custom_stoploss_3
```

**Code Implementation**:
```python
def custom_stoploss(self, ...):
    if (current_profit > 0.2):
        sl_new = 0.05   # After 20% profit, only allow 5% pullback
    elif (current_profit > 0.1):
        sl_new = 0.03
    elif (current_profit > 0.06):
        sl_new = 0.02
    elif (current_profit > 0.03):
        sl_new = 0.015
    return sl_new
```

### 4.2 Profit Trailing Sell (12 signals)

| Profit Range | Trigger Condition | Signal Name |
|--------------|-------------------|-------------|
| 0-1.2% | max_profit > current + 4.5%, RSI < 46 | sell_profit_t_0_1 |
| 0-1.2% | max_profit > current + 2.5%, RSI < 32 | sell_profit_t_0_2 |
| 0-1.2% | max_profit > current + 5%, RSI < 48 | sell_profit_t_0_3 |
| 1.2-2% | max_profit > current + 1%, RSI < 39 | sell_profit_t_1_1 |
| 1.2-2% | CMF double-period negative confirmation | sell_profit_t_1_2 |
| 1.2-2% | CTI_1h > 0.8 + CMF negative | sell_profit_t_1_4 |
| ... | ... | ... |

### 4.3 Special Sell Scenarios

| Scenario | Trigger Condition | Signal Name |
|----------|-------------------|-------------|
| MOMDIV | momdiv_sell_1h = True, profit > 2% | signal_profit_q_momdiv_1h |
| Quick Take Profit | profit 2-6%, RSI > 80 | signal_profit_q_1 |
| Extreme CTI | profit 2-6%, CTI > 0.95 | signal_profit_q_2 |
| PMAX | PMAX indicator breaks threshold | signal_profit_q_pmax_bull/bear |
| Dead Fish Stop Loss | profit < -5%, BB width low, volume shrinking | sell_stoploss_deadfish |
| Emergency Stop Loss | profit < -5%, CMF/EMA combination | sell_stoploss_u_e_1 |

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

### 5.3 Info Timeframe Indicators (5m)

The strategy additionally uses 5m as an information layer, building mirrored buy conditions:

- All 14 conditions from the 3m frame are recalculated on the 5m frame
- Provides more granular entry opportunities
- Must pass the same additional check conditions

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

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Rich Signals**: 28 buy conditions cover various market patterns, reducing missed trade risk
2. **Flexible Stop Loss**: Tiered trailing stop loss balances profit protection with trend following
3. **Cross-Period Confirmation**: 5m + 1h information frames improve signal reliability
4. **Slippage Protection**: Entry confirmation mechanism prevents abnormal price execution
5. **Hyperopt Tunable**: Many parameters support hyperparameter optimization

### ⚠️ Limitations

1. **Computational Complexity**: Three-timeframe indicator calculations require significant hardware resources
2. **Many Parameters**: Large Hyperopt space, time-consuming optimization
3. **Overfitting Risk**: 28 conditions may lead to inflated historical backtest results
4. **Live Trading Differences**: Complex logic may produce unexpected behavior in live trading
5. **High Trading Frequency**: 3m frame may lead to high-frequency trading, transaction costs need attention

---

## VIII. Applicable Scenario Recommendations

| Market Environment | Recommended Configuration | Description |
|--------------------|---------------------------|--------------|
| Slow Bull Trend | Enable EWO_2, NFIX series | Trend pullback strategies perform well |
| Oscillating Market | Enable BB_checked, ClucHA | Bollinger Band breakout captures volatility |
| Fast Decline | Enable NFI_13, Local Dip | Deep oversold bottom-fishing conditions |
| High Volatility Coins | Lower max_slip, raise stop loss | Reduce abnormal execution risk |

---

## IX. Applicable Market Environment Details

BB_RPB_TSL_2 is one of the most complex strategies in the Freqtrade community. Based on its code architecture and community long-term live trading verification, it is best suited for **oscillating pullback markets**, while performing poorly during **rapid crashes**.

### 9.1 Strategy Core Logic

- **Multi-Condition Coverage**: 28 buy signals cover oversold, pullback, breakout, and other patterns
- **Tiered Stop Loss**: More profit leads to tighter stop loss, adapting to multiple entries in oscillating markets
- **Cross-Period Confirmation**: 1h trend filter + 5m mirrored conditions, improving signal quality

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|-------------|-------------------|-----------------|
| 📈 Slow Bull Trend | ⭐⭐⭐⭐⭐ | EWO_2, NFIX series capture trend pullbacks, tiered stop loss protects profits |
| 🔄 Oscillating Market | ⭐⭐⭐⭐☆ | BB_checked, ClucHA capture Bollinger Band breakouts, frequent entries |
| 📉 Slow Bear Decline | ⭐⭐⭐☆☆ | Local Dip, NFI_13 bottom-fishing has risk, stop loss may trigger too early |
| ⚡️ Rapid Crash | ⭐☆☆☆☆ | Dead Fish stop loss may fail when liquidity dries up |
| 📊 Sideways Consolidation | ⭐⭐☆☆☆ | Few condition triggers, low capital utilization |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|--------------------|-------------------|-------------|
| max_slip | 0.33%-0.50% | Balance execution rate with price protection |
| stoploss | -0.10 to -0.15 | Adjust based on coin volatility |
| Number of Trading Pairs | 10-30 | Diversify risk, avoid single-coin concentration |
| stake_amount | Dynamic or small fixed | High-frequency trading requires controlled single position size |

---

## X. Important Reminder: The Cost of Complexity

### 10.1 Learning Cost

BB_RPB_TSL_2 has over 800 lines of code, including:
- 28 buy condition combinations
- 20+ sell signals
- 3 timeframe indicator calculations
- Custom stop loss logic

Understanding each condition's purpose requires significant time investment.

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 10-20 | 4 GB | 8 GB |
| 30-50 | 8 GB | 16 GB |
| 50+ | 16 GB | 32 GB |

**Warning**: Three-timeframe indicator calculations will cause high CPU load. Multi-core VPS is recommended.

### 10.3 Backtest vs Live Trading Differences

Complex strategies' backtest performance is often **extremely excellent**, but live trading may show:
- Order execution delays causing missed signals
- Slippage exceeding expectations causing premature stop loss triggers
- Inability to exit at expected prices when liquidity is insufficient

### 10.4 Manual Trader Recommendations

Manual traders are not recommended to attempt replicating this strategy:
- Real-time judgment of 28 conditions is nearly impossible
- Tiered stop loss requires precise calculation of current profit rate
- Multi-timeframe switching judgment is difficult

---

## XI. Summary

**BB_RPB_TSL_2** is a typical "player" strategy—capturing various market opportunities through numerous buy conditions. Its core value lies in:

1. **Comprehensive Coverage**: 28 conditions cover oversold, pullback, breakout, trend, and other patterns
2. **Intelligent Stop Loss**: Tiered trailing stop loss balances profit protection with trend following
3. **Strict Verification**: Slippage confirmation + additional checks filter low-quality signals

For quantitative traders, this strategy is suitable for experienced users who need:
- Adequate hardware resources
- Deep understanding of parameter optimization
- Live testing to verify backtest result reliability