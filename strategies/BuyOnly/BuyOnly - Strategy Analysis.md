# BuyOnly Strategy Analysis

> **Strategy ID**: #79 (Batch 08, #79)  
> **Strategy Type**: Minimalist Trend Following + Buy Only, No Sell  
> **Timeframe**: 15 minutes (15m)

---

## I. Strategy Overview

BuyOnly is a "buy only, no sell" minimalist strategy. As the name suggests, the strategy only generates buy signals and has no active sell logic whatsoever. The core philosophy is to let profits run, completely relying on take-profit and stop-loss mechanisms to exit positions.

The strategy uses a classic technical indicator combination: RSI oversold + Bollinger Band lower band + TEMA trend confirmation, forming a simple but effective buy system.

### Core Characteristics

| Attribute | Description |
|-----------|-------------|
| **Buy Conditions** | 1 independent buy signal |
| **Sell Conditions** | 0 (completely relies on take-profit/stop-loss) |
| **Protection Mechanisms** | No explicit protection mechanisms |
| **Timeframe** | 15 minutes |
| **Dependencies** | talib, technical (qtpylib) |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# ROI Exit Table
minimal_roi = {
    "60": 0.01,    # After holding 60 minutes, exit at 1% profit
    "30": 0.02,    # After holding 30 minutes, exit at 2% profit
    "0": 0.04      # Exit immediately at 4% profit
}

# Stop-Loss
stoploss = -0.10  # 10% fixed stop-loss
```

**Design Philosophy**: BuyOnly's ROI settings show a **"reverse gradient"** — the shorter the holding time, the higher the take-profit target. This is because the strategy assumes early entries have better entry points and should pursue higher profits.

### 2.2 Trailing Stop Configuration

```python
trailing_stop = True
```

Strategy enables default trailing stop mechanism.

---

## III. Entry Conditions Details

### 3.1 Single Buy Condition

```python
(
    qtpylib.crossed_above(dataframe["rsi"], 30)) &  # RSI crosses above 30
    (dataframe["open"] <= dataframe["bb_lowerband"]) &  # Open price at Bollinger Band lower band
    (dataframe["tema"] > dataframe["tema"].shift(1)) &  # TEMA trending up
    (dataframe["volume"] > 0)  # Has volume
)
```

**Logic Breakdown**:
1. **RSI crossed_above(30)**: RSI rising from oversold zone
2. **open <= bb_lowerband**: Open price at or below Bollinger Band lower band
3. **tema > tema.shift(1)**: TEMA continuously rising
4. **volume > 0**: Has actual volume

---

## IV. Exit Logic Details

### 4.1 No Active Sell

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    """
    HODL
    """
    return dataframe
```

All exit decisions rely on:

| Exit Method | Trigger Condition |
|------------|------------------|
| Fixed Stop-Loss | Loss of 10% |
| Trailing Stop | Enabled with default settings |
| ROI Take-Profit | Holding time + profit rate |

---

## V. Risk Management Highlights

### 6.1 Fixed Stop-Loss

10% fixed stop-loss provides basic protection.

### 6.2 Aggressive Take-Profit

ROI settings reflect the strategy's pursuit of short-term gains, up to 4%.

### 6.3 No Protection Mechanisms

Strategy has no additional buy protection parameters, relying on RSI and Bollinger Bands as built-in filtering.

---

## VI. Strategy Pros & Cons

### Strengths

1. **Extremely Simple Code**: Easy to understand and modify
2. **Multi-Indicator Confirmation**: RSI + Bollinger Bands + TEMA triple verification
3. **Let Profits Run**: No active selling, relies on take-profit/stop-loss
4. **Learning-Friendly**: Suitable for beginners to understand strategy structure

### Weaknesses

1. **No Active Sell**: Completely passive exit
2. **Single Condition**: Only one buy condition
3. **No Trend Filtering**: Does not distinguish bull/bear markets
4. **Signals May Be Too Frequent**: 15-minute timeframe

---

## VII. Summary

BuyOnly is a **minimalist masterpiece**. It implements trend-following functionality with minimal code, and is one of the simplest strategies in the Freqtrade strategy library.

Its core value lies in:
1. **Simplicity**: Minimal code, easy to understand
2. **Let Profits Run**: No active intervention, lets the market decide exit timing
3. **Learning Value**: Suitable as a starting point for strategy development
4. **Extensibility**: Can add various protection mechanisms and complex exit logic on this basis

For quantitative traders, BuyOnly is an excellent "skeleton strategy" — you can build more conditions, protections, and complex exit logic on top of it.

---

*Document version: v1.0*  
*Strategy series: Minimalist Trend Following*
