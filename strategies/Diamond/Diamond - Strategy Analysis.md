# Diamond Strategy: In-Depth Analysis

## 1. Strategy Overview and Design Philosophy

### 1.1 Strategy Background

Diamond is a distinctive quantitative trading strategy named in tribute to the resilience of Afghan women — like diamonds buried in desert depths, shining even in darkness. This poetic design philosophy is reflected in the strategy's purity.

### 1.2 Core Design Philosophy: Minimalism

Unlike most strategies relying on complex technical indicators, Diamond takes a radically different path: **completely abandoning pre-calculated technical indicators, using only raw OHLCV data for trading decisions.**

This design choice reflects deep insight:

1. **Data Purity**: Raw market data is the most authentic price reflection; technical indicators are inherently secondary processing that may introduce distortion or lag
2. **Computational Efficiency**: Omitting indicator calculations makes strategy execution faster, enabling quicker response in fast-moving markets
3. **Extensibility**: Although the default does not use any indicators, the architecture allows users to freely add custom indicators incorporated into the hyperparameter optimization framework

### 1.3 Strategy Positioning

Diamond is positioned for:
- Traders who want to mine trading signals from basic data
- Quantitative researchers seeking market patterns through large-scale hyperparameter optimization
- Strategy development frameworks for building more complex systems

---

## 2. Architecture Analysis

### 2.1 Core Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Diamond Strategy                      │
├─────────────────────────────────────────────────────────┤
│  Parameter Definition Layer                             │
│  ├── buy_fast_key, buy_slow_key                        │
│  ├── buy_horizontal_push, buy_vertical_push            │
│  └── sell counterparts                                 │
├─────────────────────────────────────────────────────────┤
│  Entry Logic Layer (populate_entry_trend)               │
│  └── Buy signal based on crossover                      │
├─────────────────────────────────────────────────────────┤
│  Exit Logic Layer (populate_exit_trend)                 │
│  └── Sell signal based on crossover                     │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Timeframe

Default 5-minute timeframe (medium-frequency trading), capturing intraday opportunities without excessive transaction costs.

---

## 3. Parameter System

### 3.1 Buy Parameters

| Parameter | Optimization Value | Description |
|-----------|------------------|-------------|
| buy_fast_key | `high` | Use highest price as fast line |
| buy_slow_key | `volume` | Use volume as slow line |
| buy_horizontal_push | 7 | Time lag of 7 periods |
| buy_vertical_push | 0.942 | Volume scaled to 94.2% |

**Practical interpretation**: When highest price (lagged 7 periods) crosses above volume × 0.942, trigger buy signal.

### 3.2 Sell Parameters

| Parameter | Optimization Value | Description |
|-----------|------------------|-------------|
| sell_fast_key | `high` | Use highest price as fast line |
| sell_slow_key | `low` | Use lowest price as slow line |
| sell_horizontal_push | 10 | Time lag of 10 periods |
| sell_vertical_push | 1.184 | Low scaled to 118.4% |

**Practical interpretation**: When highest price (lagged 10 periods) crosses below lowest price × 1.184, trigger sell signal.

---

## 4. Entry Logic

```python
def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    conditions = []
    conditions.append(
        qtpylib.crossed_above(
            dataframe[self.buy_fast_key.value].shift(self.buy_horizontal_push.value),
            dataframe[self.buy_slow_key.value] * self.buy_vertical_push.value
        )
    )
    if conditions:
        dataframe.loc[
            reduce(lambda x, y: x & y, conditions),
            'buy'] = 1
    return dataframe
```

The essence: comparing current highest price with 7-period-lagged highest price against a volume-derived threshold. This cross-dimensional combination may discover patterns human intuition cannot detect.

---

## 5. Risk Management

### 5.1 Fixed Stoploss

```python
stoploss = -0.271  # 27.1%
```

Relatively wide stoploss suits the 5-minute timeframe trend-following style, giving trends sufficient development space.

### 5.2 ROI Table

```python
minimal_roi = {
    "0": 0.242,    # Immediate: 24.2%
    "13": 0.044,   # After 13 periods: 4.4%
    "51": 0.02,    # After 51 periods: 2%
    "170": 0       # After 170 periods: any profit
}
```

Time-decreasing design: initially high expectations (24.2%), progressively lowering as holding time extends.

### 5.3 Trailing Stop

```python
trailing_stop = True
trailing_stop_positive = 0.011  # 1.1%
trailing_stop_positive_offset = 0.054  # 5.4%
trailing_only_offset_is_reached = False
```

Activates after 5.4% profit, tracking 1.1% below peak price.

---

## 6. Strategy Pros & Cons

### Advantages

1. **Minimalist design**: Clean code, easy to understand and maintain
2. **Highly flexible**: All core parameters optimizable
3. **Computationally efficient**: No complex indicator calculations
4. **Strong extensibility**: Easy to add custom indicators
5. **Complete risk management**: Stoploss + ROI + trailing stop

### Limitations

1. **Over-reliance on optimization**: Strategy effectiveness highly dependent on hyperparameter quality
2. **Lack of traditional technical analysis**: No conventional indicators may miss certain signals
3. **Poor parameter interpretability**: Cross-dimensional combinations' economic meaning not intuitive
4. **Out-of-sample risk**: Optimized parameters may not adapt to future markets
