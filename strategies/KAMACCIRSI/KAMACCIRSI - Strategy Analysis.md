# KAMACCIRSI Strategy Analysis

## Table of Contents

1. [Strategy Overview](#1-strategy-overview)
2. [Core Indicators Explained](#2-core-indicators-explained)
3. [Parameter Configuration System](#3-parameter-configuration-system)
4. [Buy Signal Logic](#4-buy-signal-logic)
5. [Sell Signal Logic](#5-sell-signal-logic)
6. [Risk Management Mechanisms](#6-risk-management-mechanisms)
7. [Hyperparameter Optimization](#7-hyperparameter-optimization)
8. [Strategy Applicable Scenarios](#8-strategy-applicable-scenarios)
9. [Backtesting and Optimization Recommendations](#9-backtesting-and-optimization-recommendations)
10. [Strategy Limitations Analysis](#10-strategy-limitations-analysis)
11. [Summary and Outlook](#11-summary-and-outlook)

---

## 1. Strategy Overview

### 1.1 Strategy Background and Positioning

KAMACCIRSI is a multi-indicator combination strategy developed by werkkrew. Its core design philosophy integrates three classic technical indicators—KAMA (Kaufman Adaptive Moving Average), CCI (Commodity Channel Index), and RSI (Relative Strength Index)—into a comprehensive trend-following and reversal-identification system.

The strategy is not pursuing groundbreaking technical breakthroughs but represents the author's practical results during the learning process of Freqtrade strategy development and hyperparameter optimization. As the author states: "This strategy has no groundbreaking innovations—it works and does what it does is nothing new." Yet this pragmatic design philosophy makes it an excellent model for understanding Freqtrade strategy development.

### 1.2 Design Philosophy

The strategy follows "modular + configurable" principles:

- **Modular**: Each indicator can be independently toggled, allowing flexible adjustment across different market environments
- **Configurable**: All parameters support Hyperopt optimization, avoiding subjective assumptions
- **Asymmetric buy/sell logic**: Buy and sell use independent parameter sets, implementing non-symmetric trading logic

### 1.3 Basic Configuration Overview

| Configuration | Value | Description |
|--------------|-------|-------------|
| Timeframe | 5 minutes | Suitable for short-term trading |
| Startup candles | 72 | Ensures indicator stability |
| Use sell signals | True | Enable strategy sells |
| Sell only profitable | True | Only respond to sell signals when profitable |
| Sell profit offset | 0.01 | Minimum profit threshold |

---

## 2. Core Indicators Explained

### 2.1 KAMA - Kaufman Adaptive Moving Average

KAMA is the strategy's core trend indicator, proposed by Perry Kaufman in 1995. Unlike traditional moving averages, KAMA has adaptive properties, dynamically adjusting smoothing based on market volatility.

#### 2.1.1 Calculation Principle

KAMA introduces the Efficiency Ratio (ER):

```
ER = |Price Change| / Sum of Price Volatility
```

ER values range from 0 to 1:
- ER close to 1: Market shows clear unilateral trend, price changes concentrated in one direction
- ER close to 0: Market oscillating, price fluctuates back and forth

KAMA dynamically adjusts smoothing coefficient based on ER:
```
Smoothing Coefficient = [ER × (Fast Smooth - Slow Smooth) + Slow Smooth]²
KAMA = Previous KAMA + Smoothing Coefficient × (Current Price - Previous KAMA)
```

#### 2.1.2 Dual KAMA Application

The strategy employs a dual KAMA system:

| KAMA Type | Buy Period | Sell Period | Function |
|-----------|-----------|-------------|----------|
| Short KAMA | 11 | 5 | Fast response to price changes |
| Long KAMA | 46 | 41 | Filter noise, identify main trend |

The period difference design embodies the strategy's core philosophy: buy requires more confirmation (longer period), sell responds quickly (shorter period).

#### 2.1.3 KAMA Trigger Mechanism

Two KAMA trigger modes:

1. **Cross trigger**: When short-period KAMA crosses above long-period KAMA, buy signal generates; crosses below, sell signal generates.
2. **Slope trigger**: By calculating long-period KAMA slope changes:
   ```
   Slope = Current KAMA / Previous Period KAMA
   ```
   Slope > 1 indicates uptrend; slope < 1 indicates downtrend.

### 2.2 CCI - Commodity Channel Index

CCI, developed by Donald Lambert, is a momentum indicator identifying deviation of prices from statistical averages.

#### 2.2.1 Calculation Formula

```
Typical Price (TP) = (High + Low + Close) / 3
SMA(TP) = n-period Simple Moving Average of TP
Mean Deviation = Mean Absolute Deviation of TP from SMA(TP)
CCI = (TP - SMA(TP)) / (0.015 × Mean Deviation)
```

#### 2.2.2 Standard Interpretation

| CCI Range | Market State | Strategy Application |
|-----------|-------------|---------------------|
| > +100 | Overbought | Buy confirmation (used by strategy) |
| < -100 | Oversold | Sell trigger (disabled by default) |
| -100 to +100 | Normal fluctuation | Neutral zone |

#### 2.2.3 CCI Configuration in Strategy

Buy parameters:
- Period: 18
- Threshold: 198 (extreme trend confirmation)
- Enabled: True

Sell parameters:
- Period: 18
- Threshold: -144 (deep oversold)
- Enabled: False (disabled by default)

CCI buy threshold set at 198 far exceeding traditional +100 overbought line—strategy seeks entry in high-momentum environments rather than bottom-fishing in oversold zones. This is "follow the trend" thinking.

### 2.3 RSI - Relative Strength Index

RSI, developed by J. Welles Wilder, is the most widely used momentum indicator.

#### 2.3.1 Calculation Method

```
RS = Average Gain / Average Loss
RSI = 100 - (100 / (1 + RS))
```

#### 2.3.2 Traditional Interpretation

| RSI Value | Market State | Trading Signal |
|-----------|-------------|----------------|
| > 70 | Overbought | Potential sell |
| < 30 | Oversold | Potential buy |

#### 2.3.3 RSI Configuration in Strategy

Buy parameters:
- Period: 5 (extremely short)
- Threshold: 72
- Enabled: False (disabled by default)

Sell parameters:
- Period: 12
- Threshold: 69
- Enabled: False (disabled by default)

RSI is disabled by default—likely an optimization result where KAMA and CCI combination already provides sufficient signal quality, and RSI addition would only create interference.

---

## 3. Parameter Configuration System

### 3.1 Buy Parameters

```python
buy_params = {
    'cci-enabled': True,        # CCI indicator toggle
    'cci-limit': 198,           # CCI buy threshold
    'cci-period': 18,          # CCI period
    'kama-long-period': 46,     # Long-period KAMA
    'kama-short-period': 11,    # Short-period KAMA
    'kama-trigger': 'cross',    # KAMA trigger mode
    'rsi-enabled': False,       # RSI toggle
    'rsi-limit': 72,            # RSI threshold
    'rsi-period': 5             # RSI period
}
```

### 3.2 Sell Parameters

```python
sell_params = {
    'sell-cci-enabled': False,     # CCI sell toggle
    'sell-cci-limit': -144,       # CCI sell threshold
    'sell-cci-period': 18,       # CCI period
    'sell-kama-long-period': 41,  # Long-period KAMA
    'sell-kama-short-period': 5,  # Short-period KAMA
    'sell-kama-trigger': 'cross',  # KAMA trigger mode
    'sell-rsi-enabled': False,    # RSI toggle
    'sell-rsi-limit': 69,        # RSI threshold
    'sell-rsi-period': 12         # RSI period
}
```

---

## 4. Buy Signal Logic

### 4.1 Signal Generation Process

```
Buy Signal = KAMA Trigger AND (CCI condition, if enabled) AND (RSI condition, if enabled) AND Volume > 0
```

### 4.2 Core Conditions

#### 4.2.1 KAMA Cross Condition (default enabled)

```python
if self.buy_params['kama-trigger'] == 'cross':
    conditions.append(dataframe['buy-kama-short'] > dataframe['buy-kama-long'])
```

Short-period KAMA (11) crosses above long-period KAMA (46)—indicates short-term momentum has surpassed the long-term trend.

#### 4.2.2 CCI Confirmation (default enabled)

```python
if self.buy_params['cci-enabled']:
    conditions.append(dataframe['buy-cci'] > self.buy_params['cci-limit'])
```

CCI > 198 ensures entry only when price strongly breaks out—a "chase the rally" strategy.

#### 4.2.3 RSI Condition (disabled by default)

---

## 5. Sell Signal Logic

### 5.1 Sell Signal Generation

```python
conditions.append(dataframe['sell-kama-short'] < dataframe['sell-kama-long'])
```

Short-period KAMA (5) crosses below long-period KAMA (41).

### 5.2 Sell Signal and Profit Requirements

Strategy configures `sell_profit_only = True` and `sell_profit_offset = 0.01`:
- Only when holding profit exceeds 1% does the strategy respond to sell signals
- Avoids exiting too early in minimal profit or loss states

---

## 6. Risk Management Mechanisms

### 6.1 Fixed Stop Loss

```python
stoploss = -0.32982
```

Approximately 33% fixed stop loss—relatively loose. For cryptocurrency markets, this level accommodates normal volatility while protecting capital in extreme conditions.

### 6.2 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.28596      # Trailing 28.6% after 28.6% profit
trailing_stop_positive_offset = 0.29771  # Trailing distance 29.8%
trailing_only_offset_is_reached = True   # Only activate after threshold
```

### 6.3 ROI Time Ladder

```python
minimal_roi = {
    "0": 0.11599,    # Immediately: 11.6%
    "18": 0.03112,   # After 18 hours: 3.1%
    "34": 0.01895,   # After 34 hours: 1.9%
    "131": 0          # After 131 hours: any profit
}
```

---

## 7. Hyperparameter Optimization

### 7.1 Hyperopt Support Range

All key parameters support Freqtrade Hyperopt:
- KAMA: short period, long period, trigger mode
- CCI: period, threshold, enabled state
- RSI: period, threshold, enabled state
- Risk control: stop loss, trailing parameters
- ROI: profit targets at time intervals

### 7.2 Optimization Recommendations

Author notes default parameters based on:
- Data: Kraken exchange, 60 days
- Trading pairs: 20 BTC pairs
- Loss function: SharpeHyperOptLoss

---

## 8. Strategy Applicable Scenarios

### 8.1 Best Application Environments

1. Markets with clear trends (KAMA cross strategies perform best in trending markets)
2. Cryptocurrency markets (default parameters optimized for crypto)
3. Short-to-medium-term trading (5-minute period suitable for intraday or short swings)
4. High-volatility instruments (CCI high threshold suitable for capturing strong momentum)

### 8.2 Not Applicable Scenarios

1. Sideways oscillating markets (KAMA crosses generate many false signals)
2. Low-liquidity markets (slippage erodes profits)
3. Extreme conditions (black swan events may penetrate stop loss)

---

## 9. Backtesting and Optimization Recommendations

### 9.1 Backtesting Configuration

```python
timeframe = '5m'
startup_candle_count: int = 72
```

### 9.2 Key Monitoring Indicators

1. Win rate: Trend strategies typically have 30-50% as normal
2. Profit/loss ratio: Trailing stop should produce favorable ratios
3. Maximum drawdown: Check if 33% stop loss is frequently triggered
4. Sharpe ratio: Risk-adjusted return assessment

---

## 10. Strategy Limitations Analysis

### 10.1 Design-Level Limitations

1. **Trend dependency**: Core relies on KAMA cross, limited performance in oscillating markets
2. **Lag**: All moving average strategies have inherent lag
3. **Single timeframe**: Only uses 5-minute data, lacks multi-timeframe confirmation
4. **Insufficient information utilization**: Author plans to add `informative_pairs` but hasn't implemented

### 10.2 Parameter Limitations

1. **Overfitting risk**: Default parameters optimized on specific dataset
2. **Fixed stop loss**: 33% too loose for low-volatility instruments
3. **Insufficient information utilization**: Buy/sell parameters independently calculated, not fully utilizing interrelationship

---

## 11. Summary and Outlook

### 11.1 Strategy Core Value

KAMACCIRSI, though the author modestly states "no groundbreaking innovation," provides value:

1. **Complete teaching case**: Demonstrates Freqtrade strategy development best practices
2. **Parameter optimization template**: Provides complete Hyperopt parameter definitions
3. **Modular design**: Indicators independently toggleable, easy to learn and modify
4. **Asymmetric buy/sell logic**: Demonstrates setting different parameters for buy vs. sell

### 11.2 Core Trading Logic Summary

```
Buy = KAMA Short crosses KAMA Long + CCI confirmation (optional) + RSI confirmation (optional) + Volume > 0
Sell = KAMA Short crosses below KAMA Long + CCI confirmation (optional) + RSI confirmation (optional) + Volume > 0
Risk Control = Fixed stop loss (-33%) + Trailing stop (29.77% activation) + ROI time ladder
```

### 11.3 Future Development

Author mentioned future plans:
- Add informative pairs (e.g., BTC/USD to inform */BTC pairs)

This valuable direction could better judge altcoin relative strength through BTC market trend as auxiliary information, improving signal quality.

---

*Strategy source: werkkrew | GitHub: https://github.com/werkkrew/freqtrade-strategies*
