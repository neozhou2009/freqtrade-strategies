# Divergences Strategy: In-Depth Analysis

## 1. Strategy Overview

Divergences is a technical analysis trading strategy based on the price divergence principle — when price action and momentum indicators diverge, it often signals an impending trend reversal. The strategy cleverly combines price pattern recognition with RSI, capturing trading opportunities when markets show potential reversal signals.

Divergence trading is one of the most forward-looking analytical methods in technical analysis. Unlike trend-following strategies that chase momentum, divergence strategies attempt to enter at critical turning points just as trends are about to end, characterized by "early positioning, controllable risk."

The strategy is designed for high-volatility markets like cryptocurrency, operating on a 1-hour timeframe that avoids short-term noise while capturing signals within a reasonably responsive timeframe.

---

## 2. Core Theory

### 2.1 Divergence Principle

Divergence (Divergence) is a core concept in technical analysis where price action and indicator action show inconsistent directions. Based on the physics principle of momentum conservation, when price continuously rises but upward momentum is declining, or price continuously falls but downward momentum is weakening, a trend reversal is often imminent.

**Bullish Divergence Pattern** (5-candle formation):
```
      - 
  - -   - -
  4 3 2 1 0  (candle position number)
```
Candle position 2 forms a local low — its close is below both adjacent candles (1 and 3), and candle 4's close is above candle 2. This pattern signals a local bottom may form and upward reversal is possible.

**Bearish Divergence Pattern**:
```
  - -   - -
      - 
  4 3 2 1 0
```
Candle position 2 forms a local high — its close is above both adjacent candles, and candle 4's close is below candle 2. Signals a local top may form and downward reversal is possible.

### 2.2 RSI Oversold Filtering

RSI below 30 is traditionally oversold. Divergences uses the more conservative RSI threshold of ≤ 40, allowing more potential reversal entry points while remaining in relatively low RSI territory preserving bounce space.

---

## 3. Entry Logic

### 3.1 Entry Signal Combination

```
Buy Condition = (RSI <= 40) AND (Bullish Divergence Pattern Confirmed)
```

**RSI <= 40**: Ensures market is in relatively oversold state, providing momentum foundation for price bounce

**Bullish Divergence**:
```python
dataframe['bullish_div'] = (
    (dataframe['close'].shift(4) > dataframe['close'].shift(2)) &
    (dataframe['close'].shift(3) > dataframe['close'].shift(2)) &
    (dataframe['close'].shift(2) < dataframe['close'].shift(1)) &
    (dataframe['close'].shift(2) < dataframe['close'])
)
```

Candle position 2 (2 candles back from current) forms the local lowest point.

---

## 4. Exit Logic

### 4.1 Sell Signal

```
Sell Condition = Bearish Divergence Pattern Confirmed
```

```python
dataframe['bearish_div'] = (
    (dataframe['close'].shift(4) < dataframe['close'].shift(2)) &
    (dataframe['close'].shift(3) < dataframe['close'].shift(2)) &
    (dataframe['close'].shift(2) > dataframe['close'].shift(1)) &
    (dataframe['close'].shift(2) > dataframe['close'])
)
```

### 4.2 Profit Protection

`sell_profit_only = True` ensures sell signals only execute when the position is profitable — avoiding exits during drawdowns.

---

## 5. Risk Management

### 5.1 Fixed Stoploss

```python
stoploss = -0.10  # 10%
```

Moderately wide stoploss for crypto markets, giving price sufficient volatility room.

### 5.2 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.05    # 5% retracement
trailing_stop_positive_offset = 0.20  # Activates after 20% profit
trailing_only_offset_is_reached = True
```

**Mechanism**: After profit reaches 20%, trailing stop activates. Stop level tracks 5% below the peak price.

**Example**: Buy at $100 → price reaches $130 (30% profit) → trailing activates at $123.5 → price retraces to $123.5 → sells, locking in 23.5% actual profit.

### 5.3 ROI Strategy

```python
minimal_roi = {"0": 1}  # 100% profit target
```

The strategy does not actively close positions at fixed profit targets but relies on trailing stop for profit-taking — embodying "let profits run."

---

## 6. Supporting Indicator System

**Core Trading Indicators**: RSI (14-period), MACD, CCI (170 and 34 periods)
**Trend Indicators**: EMA 3/5/10/21/50/100/200, TEMA 9, SAR
**Volatility Indicators**: Bollinger Bands (20-period, 2 std dev)
**Other**: ADX, MFI, Fast Stochastic, HT Sine

---

## 7. Strategy Pros & Cons

### Advantages

1. **Solid theoretical foundation**: Divergence principle is a classic, market-validated theory
2. **Clear logic**: Entry conditions clear (RSI oversold + bullish divergence), exit conditions explicit (bearish divergence)
3. **Complete risk management**: 10% fixed stoploss, trailing stop locks profits, profit-only sell protection
4. **Wide applicability**: Not dependent on specific trading pairs

### Limitations

1. **Ranging market risk**: Frequent false signals in sideways markets causing consecutive small losses
2. **Trending market risk**: Counter-directional trades in strong trends may face sustained losses
3. **Sell signal frequency**: Sell signals may be overly frequent without trend filtering
4. **Parameter sensitivity**: Fixed RSI threshold may not suit all markets

---

## 8. Summary

Divergences provides a clear divergence trading framework, suitable both as a technical analysis learning case and as a foundation for live trading strategies. Through continuous optimization, it has potential to demonstrate stable profitability across various market environments.
