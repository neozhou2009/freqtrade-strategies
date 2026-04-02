# BigZ06 Strategy Analysis

## I. Strategy Overview

**BigZ06** is a quantitative trading strategy created by developer ilya, inspired by iterativ's CombinedBinHAndClucV6. The strategy's core design philosophy is: **minimize drawdown as much as possible, buy at lows, sell quickly for profits**.

### Core Features

| Feature | Description |
|------|------|
| **Entry Conditions** | 14 independent conditions |
| **Exit Conditions** | ROI + Custom Stoploss + Trailing Stop |
| **Protection Mechanisms** | Custom intelligent stoploss |
| **Timeframe** | 5-minute main cycle + 1-hour auxiliary |
| **Recommended Positions** | 3-5 pairs |

### Design Philosophy

The strategy author's four core objectives:

1. **Minimize drawdown as much as possible** (Make drawdown as low as possible)
2. **Buy during dips** (Buy at dip)
3. **Sell quickly to release capital** (Sell quick as fast as you can)
4. **Soft detection of market rise, hard detection of market decline**

---

## II. Strategy Configuration Analysis

### 2.1 Time Cycle Configuration

```python
timeframe = '5m'      # Main trading cycle
inf_1h = '1h'         # Information cycle (for auxiliary judgment)
```

### 2.2 Order Type Configuration

```python
order_types = {
    'entry': 'market',
    'exit': 'market',
    'stoploss': 'market',
    'stoploss_on_exchange': False
}
```

### 2.3 Take-Profit Configuration (ROI)

```python
minimal_roi = {
    "0": 0.028,      # Immediate take-profit 2.8%
    "10": 0.018,     # Take-profit 1.8% after 10 minutes
    "40": 0.005,     # Take-profit 0.5% after 40 minutes
    "180": 0.018,    # Take-profit 1.8% after 180 minutes
}
```

### 2.4 Stoploss Configuration

```python
stoploss = -0.99  # Actually disabled default stoploss
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.025
```

---

## III. Entry Conditions Details

BigZ06 contains 14 independent entry conditions (buy_condition_0 to buy_condition_13), each with independent switch parameters adjustable.

### Condition 0: RSI Oversold + Trend Confirmation

- Closing price above 200-day EMA (uptrend)
- 5-minute RSI below 30 (oversold)
- Past 3 candles showing declining trend
- 1-hour RSI below 71 (medium-term not overheated)

### Condition 1: Bollinger Band Lower Rail Rebound + Volume Contraction

- Price touches near Bollinger Band lower rail
- Volume contracts to 1/3.8 of previous candle
- Closing is bearish candle (rebound after decline)

### Condition 2: Bollinger Band Lower Rail Buy

- Closing price within Bollinger Band lower rail (2% safety margin)
- Volume contracts

### Condition 3: RSI Deep Oversold

- 5-minute RSI extremely low (14.2)
- Volume significantly contracts

### Condition 4: 1-Hour RSI Oversold

- 1-hour RSI extremely oversold (16.5)
- Price at Bollinger Band lower rail

### Conditions 5-7: MACD Golden Cross + Bollinger Band

- EMA26 > EMA12 (short-term MA above)
- MACD histogram positive
- Price at Bollinger Band lower rail

### Conditions 8-9: Dual RSI Oversold

- 1-hour RSI < 20
- 5-minute RSI < 28

### Condition 10: 1-Hour Bollinger Band Lower Rail + MACD Reversal

- 1-hour candles at Bollinger Band lower rail
- MACD histogram turns from negative to positive
- 5-minute RSI < 40.5

### Condition 11: Bollinger Band Narrowing + MACD Continuous Rise

- Bollinger Band width narrows within 10%
- MACD positive for consecutive 5 candles
- RSI > 51 (strong)

### Condition 12: Volume Contraction Bearish Candle + Bollinger Band

- Price briefly pierces Bollinger Band lower rail
- Closing price closes inside lower rail
- Bearish candle (selling pressure released)

### Condition 13: CMF Capital Outflow + RSI Oversold

- Chaikin Money Flow extremely negative (-0.435)
- RSI < 22
- Long-term trend upward

---

## IV. Exit Logic Details

### 4.1 Active Exit (Exit Signal)

When closing price breaks above 101% of Bollinger Band middle rail, triggers exit signal. Strategy author comments "Don't be greedy, sell fast."

### 4.2 ROI Take-Profit

Strategy uses 4-level ROI ladder:
- 0-10 minutes: 2.8%
- 10-40 minutes: 1.8%
- 40-180 minutes: 0.5%
- After 180 minutes: 1.8%

### 4.3 Custom Stoploss

Strategy implements custom stoploss logic after 50 minutes of holding:
- If 1-hour RSI below 40, continue holding waiting for reversal
- If price drops more than 3.5% below opening, stoploss at 1%
- If price drops more than 2.5% below opening, stoploss at 1%

### 4.4 Trailing Stop

- Trailing stop activates after 2.5% profit
- Trailing amplitude is 1%

---

## V. Technical Indicator System

### Trend Indicators

| Indicator | Period | Usage |
|------|------|------|
| EMA200 | 200 | Long-term trend |
| EMA200_1h | 200 (1h) | 1-hour trend |

### Momentum Indicators

| Indicator | Parameters | Usage |
|------|------|------|
| RSI | 14 | Overbought/oversold |
| RSI_1h | 14 (1h) | 1-hour momentum |
| MACD | 12,26,9 | Trend momentum |

### Volatility Indicators

| Indicator | Parameters | Usage |
|------|------|------|
| Bollinger Bands | 20,2 | Support/resistance |

### Volume Indicators

| Indicator | Period | Usage |
|------|------|------|
| Volume | - | Confirmation |
| CMF | 21 | Capital flow |

---

## VI. Strategy Pros & Cons

### 6.1 Advantages

1. **Excellent Drawdown Control**: Multiple protection mechanisms effectively limit losses
2. **Rich Entry Signals**: 14 conditions provide diverse entry opportunities
3. **Fast Turnover**: Quick selling releases capital for next opportunities
4. **Multi-Timeframe Analysis**: Combines 5-minute and 1-hour for better judgment

### 6.2 Limitations

1. **Conservative Exits**: May exit too early in strong trends
2. **Complex Logic**: Multiple conditions increase understanding difficulty
3. **Parameter Sensitivity**: Default parameters may not suit all markets

---

## VII. Applicable Scenarios

### 7.1 Recommended Scenarios

- **Oscillating Markets**: Strategy excels in range-bound conditions
- **High Volatility**: Well-suited for volatile crypto markets
- **Dip Buying**: Excellent at capturing rebound opportunities

### 7.2 Not Recommended Scenarios

- **Strong Bull Markets**: May exit too early
- **Low Volatility**: Entry conditions hard to trigger
- **Continuous Downtrends**: May face consecutive losses

---

## VIII. Summary

BigZ06 is a mean reversion strategy emphasizing low drawdown and fast turnover. Through 14 entry conditions, custom stoploss, and trailing mechanisms, it builds a system focused on "buy low, sell fast, control losses."

**Key Features:**
- 14 independent entry conditions
- Custom stoploss after 50 minutes
- ROI ladder for quick profits
- Suitable for oscillating markets

**Risk Warning:**
The strategy's fast-exit design means limited profits per trade. Ensure full understanding before use and conduct proper risk management.
