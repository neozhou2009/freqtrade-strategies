# Strategy005 Strategy Analysis

> **Strategy Number**: #10 (10th of 465 strategies)  
> **Strategy Type**: Multi-Indicator Hyperopt Strategy  
> **Timeframe**: 5 minutes (5m)

---

## 1. Strategy Overview

**Strategy005** is one of the classic strategies in the Freqtrade official strategy library, developed by Gerald Lonlas. The strategy combines RSI, STOCHF, MACD, SAR, and other technical indicators, and incorporates hyperparameter optimization (Hyperopt) functionality, allowing users to find optimal parameter combinations through optimization.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | Multi-condition combination (RSI + STOCHF + MACD + SAR + Volume) |
| **Exit Conditions** | 2 modes available (RSI-MACD or SAR-FisherRsi) |
| **Protection** | Trailing stop |
| **Timeframe** | 5 minutes |
| **Dependencies** | TA-Lib, technical, numpy |
| **Special Features** | Hyperopt support |

---

## 2. Configuration Analysis

### 2.1 Base Risk Parameters

```python
# ROI exit table
minimal_roi = {
    "1440": 0.01,   # After 1440 minutes: 1% profit
    "80": 0.02,     # After 80 minutes: 2% profit
    "40": 0.03,     # After 40 minutes: 3% profit
    "20": 0.04,     # After 20 minutes: 4% profit
    "0": 0.05,      # Immediate exit: 5% profit
}

# Stoploss setting
stoploss = -0.10  # -10% hard stoploss

# Trailing stop
trailing_stop = True
trailing_stop_positive = 0.01      # 1% trailing activation
trailing_stop_positive_offset = 0.02  # 2% offset trigger
```

**Design Logic**:
- **Time-decreasing ROI**: Longer hold time means lower exit threshold
- **Low Return Expectation**: Maximum only 5% ROI,追求 stable returns
- **Trailing Stop**: 2% profit triggers 1% trailing

### 2.2 Order Type Configuration

```python
order_types = {
    "entry": "limit",       # Limit order entry
    "exit": "limit",        # Limit order exit
    "stoploss": "market",   # Market stoploss order
    "stoploss_on_exchange": False,
}
```

---

## 3. Entry Conditions Explained

### 3.1 Entry Logic

```python
# Entry conditions
dataframe.loc[
    (
        (dataframe["close"] > 0.00000200)                      # Price > minimum (prevent dead coins)
        & (dataframe["volume"] > dataframe["volume"].rolling(self.buy_volumeAVG.value).mean() * 4)  # Volume > avg × 4
        & (dataframe["close"] < dataframe["sma"])              # Price < SMA40 (buy on pullback)
        & (dataframe["fastd"] > dataframe["fastk"])            # STOCHF golden cross
        & (dataframe["rsi"] > self.buy_rsi.value)              # RSI > threshold
        & (dataframe["fastd"] > self.buy_fastd.value)          # STOCHF fastd > threshold
        & (dataframe["fisher_rsi_norma"] < self.buy_fishRsiNorma.value)  # Fisher RSI < threshold
    ),
    "buy",
] = 1
```

**Logic Analysis**:
- **Price Filter**: Excludes extremely low price dead coins
- **Volume Confirmation**: Volume greater than 4x average, confirms activity
- **SMA Pullback**: Price below SMA40, pullback buying logic
- **STOCHF Golden Cross**: Stochastic golden cross, short-term momentum turning strong
- **RSI Confirmation**: RSI above threshold, avoids deep oversold
- **Fisher RSI**: Normalized Fisher RSI below threshold, confirms oversold

### 3.2 Hyperparameters

```python
# Buy hyperparameters
buy_volumeAVG = IntParameter(low=50, high=300, default=70, space="buy", optimize=True)
buy_rsi = IntParameter(low=1, high=100, default=30, space="buy", optimize=True)
buy_fastd = IntParameter(low=1, high=100, default=30, space="buy", optimize=True)
buy_fishRsiNorma = IntParameter(low=1, high=100, default=30, space="buy", optimize=True)
```

**Optimization Ranges**:
- Volume average period: 50-300 candles
- RSI threshold: 1-100
- STOCHF fastd threshold: 1-100
- Fisher RSI threshold: 1-100

---

## 4. Exit Logic Explained

### 4.1 Exit Mode 1: RSI-MACD

```python
# Exit conditions - Mode 1
dataframe.loc[
    (
        (dataframe["rsi"] > self.sell_rsi.value)              # RSI > threshold
        & (dataframe["macd"] < dataframe["macdsignal"])       # MACD < signal
    ),
    "sell",
] = 1
```

**Logic**: RSI overbought + MACD weakening triggers exit.

### 4.2 Exit Mode 2: SAR-FisherRsi

```python
# Exit conditions - Mode 2
dataframe.loc[
    (
        (dataframe["sar"] > dataframe["close"])               # SAR > price
        & (dataframe["fisher_rsi_norma"] > self.sell_fishRsiNorma.value)  # Fisher RSI > threshold
    ),
    "sell",
] = 1
```

**Logic**: SAR reversal + Fisher RSI overbought triggers exit.

### 4.3 Exit Mode Selection

Strategy allows selecting exit mode via hyperopt:
- Mode 1: RSI-MACD combination
- Mode 2: SAR-FisherRsi combination

---

## 5. Technical Indicator System

### 5.1 Core Indicators

| Indicator | Parameters | Usage |
|-----------|------------|-------|
| **RSI** | 14 periods | Overbought/oversold |
| **STOCHF** | 5, 3, 3 | Stochastic fast |
| **MACD** | Standard | Momentum |
| **SAR** | Default | Parabolic SAR |
| **Fisher RSI** | Custom | Normalized RSI |
| **SMA** | 40 periods | Trend reference |

### 5.2 Indicator Characteristics

- **RSI**: Standard relative strength index
- **STOCHF**: Fast stochastic oscillator
- **MACD**: Moving Average Convergence Divergence
- **SAR**: Parabolic Stop and Reverse
- **Fisher RSI**: Normalized Fisher transform of RSI

---

## 6. Risk Management Features

### 6.1 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.01      # 1%
trailing_stop_positive_offset = 0.02  # 2%
```

**Mechanism**:
- Trailing activates after 2% profit
- Trails at 1% distance
- Locks in gains during trends

### 6.2 Multi-level ROI

Time-based profit taking:
- 5% immediate profit
- Gradually降低 to 1% after 1440 minutes
- Ensures capital turnover

### 6.3 Hard Stoploss

```python
stoploss = -0.10  # -10%
```

**Purpose**: Final backup protection.

---

## 7. Strategy Strengths and Limitations

### ✅ Strengths

1. **Multi-Indicator Confirmation**: Multiple indicators reduce false signals
2. **Hyperopt Support**: Parameters can be optimized for current conditions
3. **Flexible Exit**: Two exit modes available
4. **Volume Filter**: Confirms activity before entry
5. **Trailing Stop**: Locks in profits on trending moves

### ⚠️ Limitations

1. **Complex Logic**: Many conditions increase complexity
2. **Hyperopt Dependent**: Performance relies on optimized parameters
3. **No BTC Correlation**: Doesn't account for Bitcoin direction
4. **Many Parameters**: Requires careful monitoring
5. **Mode Selection**: Must choose correct exit mode for market

---

## 8. Hyperopt Guide

### 8.1 Running Hyperopt

```bash
freqtrade hyperopt --strategy Strategy005 --hyperopt-loss SharpeHyperOptLossDaily --epochs 100
```

### 8.2 Parameter Spaces

- **Buy space**: buy_rsi, buy_fastd, buy_fishRsiNorma, buy_volumeAVG
- **Sell space**: sell_rsi, sell_fishRsiNorma
- **ROI space**: ROI table optimization
- **Stoploss space**: Stoploss optimization

### 8.3 Recommended Epochs

- Minimum: 100 epochs
- Recommended: 500-1000 epochs
- Thorough: 2000+ epochs

---

## 9. Summary

**Strategy005** is a comprehensive multi-indicator strategy with hyperopt support. Its core value lies in:

1. **Indicator Diversity**: RSI, STOCHF, MACD, SAR, Fisher RSI combination
2. **Hyperopt Ready**: Built-in parameter optimization
3. **Flexible Design**: Two exit modes for different conditions
4. **Volume Confirmation**: Ensures liquidity before entry
5. **Trailing Protection**: Locks in profits on trends

For quantitative traders, this demonstrates:
- Multi-indicator combination techniques
- Hyperopt parameter optimization
- Flexible exit strategy design
- Comprehensive risk management

**Recommendations**:
- Run hyperopt for current market conditions
- Test both exit modes to find optimal
- Monitor parameter stability over time
- Consider adding BTC correlation filter

---
