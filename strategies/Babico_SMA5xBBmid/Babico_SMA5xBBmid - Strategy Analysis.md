# Babico_SMA5xBBmid Strategy Analysis

> **Strategy Number**: #48
> **Strategy Type**: EMA Breakthrough Bollinger Band Middle Rail
> **Timeframe**: 1 day (1d)

---

## I. Strategy Overview

Babico_SMA5xBBmid is an extremely simple trend following strategy — core logic based on crossover relationship between EMA (Exponential Moving Average) and Bollinger Band middle rail. Strategy design philosophy originates from classic technical analysis theory: when short-term moving average crosses above medium-term price benchmark — indicates market may enter uptrend; conversely may enter downtrend.

Strategy uses daily level (1d) timeframe — suitable for long-term investors or traders preferring low-frequency trading. Strategy's core philosophy is to capture medium-to-long term trend conversion points — achieves buy/sell decisions through simple moving average crossovers.

### Core Features

| Feature | Description |
|---------|-------------|
| **Entry Conditions** | EMA5 crosses above BB middle rail (golden cross) |
| **Exit Conditions** | BB middle rail crosses above EMA5 (death cross) |
| **Protection** | Fixed stoploss -10% — trailing stop enabled |
| **Timeframe** | 1d (daily) |
| **Dependencies** | technical, talib |

---

## II. Strategy Configuration Analysis

### 2.1 Base Risk Parameters

```python
minimal_roi = {
    "0": 0.10,    # Immediate take-profit 10%
    "30": 0.05,   # 5% after 30 candles
    "60": 0.02    # 2% after 60 candles
}

stoploss = -0.10   # Stoploss -10%

# Trailing stoploss configuration
trailing_stop = True
trailing_stop_positive = 0.01    # Positive trailing distance 1%
trailing_stop_positive_offset = 0.03  # Trigger offset 3%
```

**Configuration Logic Analysis**:

- **minimal_roi Design**: Strategy adopts decreasing ROI targets — initial 10% take-profit relatively high — then gradually decreases. This is because daily level trading frequency low — once holding exceeds 30 days (about one month) — take-profit target drops to 5% — after 60 days drops to 2%. This design allows strategy to continue holding in trend markets — while exiting timely in long-term trendless markets.

- **stoploss -10%**: 10% stoploss amplitude relatively conservative — acceptable for daily level strategy. This stoploss amplitude combined with 10% initial take-profit — profit/loss ratio target about 1:1 — considering high certainty of daily level trend following — this risk-reward ratio reasonable.

- **trailing_stop Enabled**: Trailing stoploss activates after profit exceeds 3% — stoploss line moves up to lock 1% profit. This provides additional protection mechanism — prevents profit giveback.

---

## III. Entry Conditions Details

### 3.1 Core Entry Condition: EMA5 Crosses Above BB Middle Rail

```python
qtpylib.crossed_above(dataframe['ema5'], dataframe['bb_mid'])
```

**Logic Deep Analysis**:

1. **EMA5 Function**: EMA5 (5-day Exponential Moving Average) is a sensitive short-term trend indicator. Compared to Simple Moving Average (SMA) — EMA more sensitive to price changes — can reflect market short-term changes faster.

2. **Bollinger Band Middle Rail Function**: Bollinger Band middle rail essentially 20-day Simple Moving Average (SMA20) — represents medium-term price benchmark. When price runs above Bollinger Band middle rail — usually considered in relatively strong state; conversely in relatively weak state.

3. **Crossover Signal Meaning**: When EMA5 crosses above Bollinger Band middle rail — means short-term price average exceeded medium-term price benchmark — this is short-term trend strengthening signal. In technical analysis theory — this phenomenon viewed as potential trend starting point.

4. **Trading Logic Explanation**: Strategy assumes if EMA5 can break through medium-term moving average pressure — market may already ready to enter uptrend. This is a forward-looking signal — aims to capture early stage of trend.

### 3.2 Limitations of Entry Conditions

- **No volume confirmation**: Strategy doesn't check whether volume cooperates — may produce false signals with volume-price divergence
- **No trend filter**: Doesn't judge medium-to-long term trend direction — may produce counter-trend buy signals in downtrend
- **No indicator confirmation**: Doesn't use other technical indicators (such as RSI — MACD) to confirm signals

---

## IV. Exit Conditions Details

### 4.1 Core Exit Condition: BB Middle Rail Crosses Above EMA5

```python
qtpylib.crossed_above(dataframe['bb_mid'], dataframe['ema5'])
```

**Logic Deep Analysis**:

1. **Death Cross Signal Meaning**: This is mirror logic of buy condition. When Bollinger Band middle rail crosses above EMA5 — means short-term price average fell below medium-term price benchmark — is short-term trend weakening signal.

2. **Sell Timing Selection**: Strategy chooses crossover point as sell timing — rather than fixed take-profit point. This means sell decision completely based on technical signals — rather than preset profit targets.

### 4.2 Take-Profit Strategy

Strategy adopts ROI (Return on Investment) step-style take-profit:

| Holding Time | Take-Profit Target | Design Intent |
|-------------|-------------------|---------------|
| 0 days | 10% | Capture initial trend move |
| About 30 days | 5% | Medium-term target |
| About 60 days | 2% | Prevent profit giveback |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator | Parameters | Usage |
|-----------|------------|-------|
| EMA | 5 | Short-term trend signal |
| Bollinger Bands | 20, 2 | Middle rail as benchmark |

### 5.2 Indicator Relationship

- EMA5 represents short-term consensus
- BB middle rail (SMA20) represents medium-term trend
- Crossover indicates trend change

---

## VI. Risk Management Features

### 6.1 Risk-Return Characteristics

| Dimension | Assessment |
|-----------|------------|
| Maximum Theoretical Loss | -10% (fixed stoploss) |
| Maximum Theoretical Profit | Unlimited (trailing stoploss) |
| Expected Profit/Loss Ratio | About 1:1 |
| Signal Frequency | Very Low (daily timeframe) |

---

## VII. Strategy Pros & Cons

### ✅ Pros

1. **Extremely simple**: Very small code volume — clear logic
2. **Daily timeframe**: Low frequency — less monitoring needed
3. **Clear signals**: Crossover signals unambiguous
4. **Classic approach**: Moving average crossover time-tested
5. **Conservative stoploss**: 10% reasonable for daily

### ⚠️ Cons

1. **Very few signals**: Daily timeframe means few trades
2. **No volume confirmation**: May have false breakouts
3. **No trend filter**: May trade against longer trend
4. **Lag inherent**: Moving averages lag price
5. **May miss early moves**: Waits for confirmation

---

## VIII. Summary

Babico_SMA5xBBmid is an **extremely simple daily trend following** strategy. Core value lies in **simplicity and clear signals**. Strategy suitable for long-term investors who can wait for high-certainty signals and don't need frequent trading.

---

*This document is based on strategy code*
