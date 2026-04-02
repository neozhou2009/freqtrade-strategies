# Roth03 Strategy In-Depth Analysis

> **Strategy Number**: #352 (352nd of 465 strategies)  
> **Strategy Type**: Bollinger Band Mean Reversion + Fast Stochastic Confirmation  
> **Time Frame**: 5 minutes (5m)

---

## I. Strategy Overview

Roth03 is an oversold bounce strategy based on Bollinger Band lower band breakouts, belonging to the same Roth series as Roth01. This strategy introduces the Fast Stochastic (Stoch Fast) fastd as a confirmation condition in the buy signal, while the sell is triggered primarily by the SAR reversal signal. The stop-loss is set wider (-31.939%) and the initial ROI target is higher (24.553%), reflecting more aggressive profit expectations.

### Core Features

| Feature | Description |
|---------|-------------|
| **Buy Condition** | 1 buy signal, based on Bollinger Band lower band breakout + fastd confirmation + MFI oversold |
| **Sell Condition** | 1 sell signal, based on SAR reversal + RSI/MFI/fastd overbought combination |
| **Protection Mechanism** | Tiered ROI take-profit + Fixed stop-loss |
| **Time Frame** | 5 minutes |
| **Dependencies** | talib, qtpylib |

---

## II. Strategy Configuration Analysis

### 2.1 Basic Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "0": 0.24553,    # Immediate: 24.553%
    "33": 0.07203,   # After 33 minutes: 7.203%
    "90": 0.01452,   # After 90 minutes: 1.452%
    "111": 0         # After 111 minutes: No limit
}

# Stop-loss Setting
stoploss = -0.31939  # -31.939%
```

**Design Rationale**:
- Initial ROI target is as high as 24.553%, showing expectation for capturing significant rebounds
- Stop-loss is set quite loosely (-31.939%), more aggressive than Roth01
- ROI tiered timing differs from Roth01, using 33/90/111 minute segments

### 2.2 Order Type Configuration

The strategy uses default order type configuration, suitable for most exchanges.

---

## III. Buy Condition Analysis

### 3.1 Buy Condition Breakdown

Roth03 employs a single-path buy logic where three conditions must be satisfied simultaneously:

```python
# Single Buy Condition
dataframe.loc[
    (
        (dataframe['close'] < dataframe['bb_low']) &   # Price breaks below Bollinger lower band
        (dataframe['fastd'] > 37) &                     # fastd above 37, non-extreme oversold
        (dataframe['mfi'] < 20.0)                       # MFI below 20, extreme capital outflow
    ),
    'buy'] = 1
```

### 3.2 Buy Condition Interpretation

| Condition | Indicator | Threshold | Meaning |
|-----------|-----------|-----------|---------|
| Price Breakout | Close | < BB_Low | Price breaks below Bollinger lower band, deviation from mean |
| Momentum Confirmation | fastd | > 37 | Fast stochastic fastd above 37, non-extreme oversold |
| Capital Outflow | MFI | < 20 | Money flow extremely contracted, market panic |

**Logic Analysis**:
1. **Close < BB_Low**: Price breaking below the Bollinger lower band produces an oversold signal
2. **fastd > 37**: Fast stochastic's fastd value above 37 indicates that while oversold, it's not an extreme situation, with some rebound momentum
3. **MFI < 20**: Money Flow Index below 20 indicates significant capital outflow

**Differences from Roth01**:
- Roth01 uses CCI for oversold confirmation, Roth03 uses fastd
- Roth03's MFI threshold is stricter (20 vs 24)
- Roth03 introduces the fastd > 37 "non-extreme" condition, avoiding entries in extreme situations

---

## IV. Sell Logic Analysis

### 4.1 Multi-Tier Take-Profit System

The strategy employs a tiered ROI take-profit mechanism:

```
Time (minutes)    Target Profit    Description
─────────────────────────────────────────────
0                24.553%          Highest target set at position open
33               7.203%           Lower expectation after 33 minutes
90               1.452%           Conservative target after 90 minutes
111              0%               Any profit acceptable in under 2 hours
```

### 4.2 Sell Signal

```python
# Single Sell Condition
dataframe.loc[
    (
        (dataframe['sar'] > dataframe['close']) &  # SAR reverses downward
        (dataframe['rsi'] > 69) &                  # RSI overbought
        (dataframe['mfi'] > 86) &                  # MFI shows heavy capital inflow
        (dataframe['fastd'] > 79)                  # fastd high value confirmation
    ),
    'sell'] = 1
```

### 4.3 Sell Condition Interpretation

| Condition | Indicator | Threshold | Meaning |
|-----------|-----------|-----------|---------|
| Trend Reversal | SAR | > Close | Parabolic SAR reverses above price |
| Overbought State | RSI | > 69 | Relative Strength Index enters overbought zone |
| Capital Status | MFI | > 86 | Heavy capital inflow |
| Momentum Confirmation | fastd | > 79 | Fast stochastic confirms overbought |

**Design Features**:
- Sell conditions center on SAR reversal as the primary trigger
- RSI threshold is relatively moderate (69), not waiting for extreme overbought
- MFI > 86 indicates heavy capital inflow, market may be overheated
- fastd > 79 confirms overbought state

**Differences from Roth01**:
- Roth03 sell conditions do not include Bollinger upper band breakout
- Uses fastd instead of CCI as confirmation indicator
- Sell conditions are simpler (4 vs Roth01's 6)

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicators | Purpose |
|-------------------|---------------------|---------|
| Trend Indicators | MACD, SAR | Trend direction judgment |
| Volatility Indicators | Bollinger Bands (BB) | Price channel and overbought/oversold |
| Momentum Indicators | RSI, CCI, MFI | Overbought/oversold determination |
| Oscillator | Stoch Fast (fastd/fastk) | Momentum confirmation |
| Trend Strength | ADX | Trend strength (not actively used) |

### 5.2 Technical Indicator Calculations

```python
# MACD
macd = ta.MACD(dataframe)
dataframe['macd'] = macd['macd']
dataframe['macdsignal'] = macd['macdsignal']
dataframe['macdhist'] = macd['macdhist']

# Bollinger Bands
bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
dataframe['bb_low'] = bollinger['lower']
dataframe['bb_mid'] = bollinger['mid']
dataframe['bb_upper'] = bollinger['upper']
dataframe['bb_perc'] = (dataframe['close'] - dataframe['bb_low']) / (
            dataframe['bb_upper'] - dataframe['bb_low'])

# RSI, CCI, MFI, SAR, ADX, Stoch Fast
dataframe['rsi'] = ta.RSI(dataframe)
dataframe['cci'] = ta.CCI(dataframe)
dataframe['mfi'] = ta.MFI(dataframe)
dataframe['sar'] = ta.SAR(dataframe)
dataframe['adx'] = ta.ADX(dataframe)
stoch_fast = ta.STOCHF(dataframe)
dataframe['fastd'] = stoch_fast['fastd']
dataframe['fastk'] = stoch_fast['fastk']
```

---

## VI. Risk Management Features

### 6.1 Tiered Take-Profit Mechanism

The strategy uses time-decaying ROI targets with different take-profit points at various holding times:

| Holding Time | Target Profit | Risk Characteristics |
|--------------|---------------|----------------------|
| 0-33 minutes | 24.553% | High target, capturing significant rebounds |
| 33-90 minutes | 7.203% | Moderate target, reasonable profit |
| 90-111 minutes | 1.452% | Conservative target, securing small gains |
| >111 minutes | 0% | Any profit acceptable for exit |

### 6.2 Fixed Stop-Loss Protection

- **Stop-Loss Level**: -31.939%
- **Design Philosophy**: Very wide stop-loss allows ample room for price fluctuation, avoiding being shaken out by oscillations

### 6.3 Technical Signal Confirmation

Both buy and sell employ multi-indicator confirmation mechanisms:

- **Buy**: Bollinger Band + fastd + MFI triple confirmation
- **Sell**: SAR + RSI + MFI + fastd four-fold confirmation

---

## VII. Strategy Advantages and Limitations

### ✅ Advantages

1. **Reasonable Buy Conditions**: fastd > 37 avoids entries during extreme oversold, increasing rebound probability
2. **Simple Sell Conditions**: 4-condition sell logic is clearer than Roth01
3. **Wide Stop-Loss Space**: -31.939% stop-loss gives ample room for price fluctuation
4. **Aggressive ROI Target**: Initial target of 24.553% shows confidence in capturing significant rebounds

### ⚠️ Limitations

1. **Stop-Loss Too Wide**: -31.939% stop-loss means single-trade losses can be significant
2. **Dependence on Extreme Conditions**: Requires price to break below Bollinger lower band to trigger buys
3. **Missing Upper Band Confirmation**: Sell doesn't check Bollinger upper band, may exit too early
4. **Range-Bound Market Risk**: May result in frequent entries and exits

---

## VIII. Suitable Market Scenarios

| Market Environment | Recommended Configuration | Description |
|-------------------|--------------------------|-------------|
| Sharp Decline Rebound | Default configuration | Core design scenario |
| Oscillating Decline | Adjust stop-loss | Consider tightening stop-loss |
| Sustained Downtrend | Disable | Strategy is not adapted |
| Strong Uptrend | Disable | Cannot capture upward trends |

---

## IX. Applicable Market Environment Details

Roth03 and Roth01 belong to the same Roth series, both are mean reversion strategies suitable for capturing rebounds when the market experiences extreme oversold conditions. Based on its code architecture, it is best suited for **sharp decline rebound scenarios**, while performing poorly in **sustained downtrends** or **one-sided uptrends**.

### 9.1 Strategy Core Logic

- **Oversold Capture**: When MFI < 20 and price breaks below Bollinger lower band, the market is considered to be in extreme panic
- **Momentum Confirmation**: fastd > 37 ensures not extreme oversold, has rebound momentum
- **Reversal Exit**: SAR reversal as core signal, combined with RSI/MFI/fastd to confirm overbought

### 9.2 Performance in Different Market Environments

| Market Type | Performance Rating | Reason Analysis |
|:------------|:-------------------|:----------------|
| 📈 Sharp Decline Rebound | ⭐⭐⭐⭐⭐ | Core design scenario, capturing oversold reversals |
| 🔄 Range-Bound Market | ⭐⭐⭐☆☆ | May result in frequent entries/exits, fees eroding profits |
| 📉 Sustained Downtrend | ⭐⭐☆☆☆ | Frequent stop-loss triggers, accumulating losses |
| ⚡️ One-Sided Uptrend | ⭐☆☆☆☆ | Cannot trigger buy conditions |

### 9.3 Key Configuration Recommendations

| Configuration Item | Recommended Value | Description |
|-------------------|-------------------|-------------|
| Stop-Loss | -0.25 ~ -0.32 | Adjust based on risk tolerance, default is quite wide |
| Time Frame | 5m | Default setting, not recommended to modify |
| ROI Initial Target | 0.15 ~ 0.25 | Can be adjusted based on market volatility |

---

## X. Important Note: The Cost of Complexity

### 10.1 Learning Curve

Roth03's strategy logic is relatively simple, similar to but slightly different from Roth01. Requires understanding of technical indicators such as Bollinger Bands, MFI, fastd, RSI, and SAR.

### 10.2 Hardware Requirements

| Number of Trading Pairs | Minimum Memory | Recommended Memory |
|------------------------|----------------|-------------------|
| 1-10 pairs | 2GB | 4GB |
| 10-50 pairs | 4GB | 8GB |

Strategy computation is moderate, with modest hardware requirements.

### 10.3 Backtesting vs Live Trading Differences

Backtesting may show excellent performance, but in live trading be aware of:
- **Slippage in Extreme Conditions**: Liquidity may be insufficient during rapid declines
- **Stop-Loss Execution**: -31.939% stop-loss may face execution difficulties
- **False Signal Risk**: fastd confirmation may produce false signals

### 10.4 Manual Trader Recommendations

Manual traders can reference strategy signals:
1. Watch for assets with price below Bollinger lower band and MFI < 20
2. Wait for fastd > 37 to confirm non-extreme oversold
3. Set reasonable stop-loss to control per-trade risk

---

## XI. Summary

**Roth03** is an aggressive mean reversion strategy. Its core value lies in:

1. **Reasonable Entry Conditions**: fastd > 37 avoids extreme oversold, increasing rebound probability
2. **Simple Exit Logic**: SAR reversal as core, 4 conditions confirm exit
3. **Aggressive Profit Expectations**: ROI initial target of 24.553% shows confidence in capturing significant rebounds

For quantitative traders, Roth03 is the "aggressive version" of Roth01, suitable for traders with higher risk tolerance. Its stop-loss is wider and profit target higher, but also means single-trade losses can be larger. Recommended to use in combination with trend strategies for risk diversification.