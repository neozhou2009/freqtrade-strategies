# Chispei Strategy In-Depth Analysis

> **Strategy ID**: #86 (6th in Batch 9)
> **Strategy Type**: Trend-Following + Momentum Confirmation
> **Timeframe**: 4 Hours (4h)

---

## I. Strategy Overview

Chispei is a trend-following strategy combining **Moving Average Crossovers** with a **Momentum Indicator**. The strategy design is clean: uses 13-period SMA and 25-period SMA crossover to determine trend direction, while leveraging the 21-period Momentum indicator (MOM) to filter false signals and confirm entry timing.

Core Logic: Enter when short-term moving averages break above long-term moving averages (golden cross) in the relative bottom area of a downtrend (MOM<15); exit when momentum weakens (MOM<80) and moving averages form a death cross.

### Key Features

| Feature | Description |
|---------|-------------|
| **Buy Conditions** | 2 independent conditions (AND relationship) |
| **Sell Conditions** | 2 basic conditions (AND relationship) |
| **Protection** | No additional entry protection mechanism; pure technical signals |
| **Timeframe** | 4 Hours (4h) |
| **Dependencies** | talib, technical, numpy |

---

## II. Strategy Configuration Analysis

### 2.1 Core Risk Parameters

```python
# Staged Profit-Taking Table (ROI)
minimal_roi = {
    "5127": 0,      # ~3.56 days: force close
    "1836": 0.676,  # ~30.6 hours: 67.6% return
    "2599": 0.079,  # ~43.3 hours: 7.9% return
    "120": 0.10,    # 2 hours: 10%
    "60": 0.10,     # 1 hour: 10%
    "30": 0.05,     # 30 minutes: 5%
    "20": 0.05,     # 20 minutes: 5%
    "0": 0.04       # Immediate: 4%
}

# Stop-Loss Setting
stoploss = -0.32336  # -32.336% stop-loss
```

**Design Philosophy**:
- **Ultra-Long Stop-Loss (-32.336%)**: Indicates strategy is willing to endure significant drawdowns to capture trending moves; aligns with "let profits run" trend-following philosophy
- **Multi-Tier ROI Structure**: Sets higher profit targets (10%) in the first 120 minutes, then gradually lowers them; reflects pursuit of quick short-term profits
- **Force Close Mechanism**: After 5127 minutes (~3.56 days), force close regardless of profit/loss; prevents excessive holding

### 2.2 Timeframe Configuration

```python
timeframe = '4h'  # 4-hour candles
```

**Design Philosophy**: The 4-hour timeframe sits between intraday and interday; filters short-term noise while capturing medium-term trends; suitable for medium-short-term trading.

---

## III. Entry Conditions Details

### 3.1 Buy Conditions Logic

The strategy has **1 group** of buy conditions with **2 sub-conditions** (AND relationship):

#### Condition Group: Momentum Bottom + MA Bullish Alignment

```python
# Buy Signal: Momentum oversold + MA golden cross
(
    (dataframe['mom'] < 15) &          # Momentum indicator below 15 (oversold zone)
    (dataframe['fastMA'] > dataframe['slowMA'])  # 13-day MA > 25-day MA (bullish alignment)
)
```

| Sub-Condition | Indicator | Threshold | Meaning |
|--------------|-----------|-----------|---------|
| Condition #1 | MOM (21) | < 15 | Momentum at relatively low point; rebound opportunity possible |
| Condition #2 | SMA (13/25) | Fast > Slow | Short-term MA breaks above long-term MA; golden cross formed |

**Satisfaction**: Both conditions must be met simultaneously to trigger buy signal.

### 3.2 Buy Conditions Analysis

| Condition Group | Condition # | Core Logic | Signal Strength |
|----------------|-------------|------------|----------------|
| Trend Reversal | #1 | MOM<15 indicates market is in oversold state; rebound opportunity exists | Moderate |
| Trend Confirmation | #2 | MA golden cross confirms trend shift to bullish; improves signal reliability | Strong |

---

## IV. Exit Logic Details

### 4.1 Multi-Tier Profit-Taking System

The strategy uses a **staged ROI mechanism** that automatically triggers different profit levels based on holding time:

| Holding Time | Return | Notes |
|-------------|--------|-------|
| 0-20 minutes | 4% | Triggers lowest profit-taking immediately |
| 20-30 minutes | 5% | Short holding profit-taking |
| 30-60 minutes | 10% | 10% profit-taking within 1 hour |
| 60-120 minutes | 10% | Maintains 10% target within 2 hours |
| 120-2599 minutes | 7.9% | Medium holding reduces expectations |
| 2599-1836 minutes | 67.6% | Special time window high profit |
| 5127+ minutes | 0% | Force close |

**Design Feature**: There is an abnormally high 67.6% profit (1836-2599 minute window) that may be a backtesting optimization result; live trading requires careful verification.

### 4.2 Basic Sell Signal

```python
# Sell Signal: Momentum high pullback + MA death cross
(
    (dataframe['mom'] < 80) &           # Momentum below 80 (pullback from high)
    (dataframe['fastMA'] < dataframe['slowMA'])  # 13-day MA < 25-day MA (death cross)
)
```

| Sub-Condition | Indicator | Threshold | Meaning |
|--------------|-----------|-----------|---------|
| Condition #1 | MOM (21) | < 80 | Momentum pulling back from highs; market momentum weakening |
| Condition #2 | SMA (13/25) | Fast < Slow | Short-term MA falls below long-term MA; death cross formed |

---

## V. Technical Indicator System

### 5.1 Core Indicators

| Indicator Category | Specific Indicator | Parameter | Purpose |
|-------------------|-------------------|-----------|---------|
| Trend Indicator | SMA (Simple Moving Average) | 13 periods | Fast moving average; captures short-term trend |
| Trend Indicator | SMA (Simple Moving Average) | 25 periods | Slow moving average; confirms long-term trend |
| Momentum Indicator | MOM (Momentum) | 21 periods | Measures price change rate; identifies overbought/oversold |

### 5.2 Indicator Calculation Logic

```python
# Indicator Calculations
dataframe['fastMA'] = ta.SMA(dataframe, timeperiod=13)   # 13-day Simple Moving Average
dataframe['slowMA'] = ta.SMA(dataframe, timeperiod=25)   # 25-day Simple Moving Average
dataframe['mom'] = ta.MOM(dataframe, timeperiod=21)      # 21-day Momentum indicator
```

**Momentum Indicator (MOM) Explanation**:
- MOM = Current Price - N-Period-Ago Price
- MOM > 0: Price in uptrend
- MOM < 0: Price in downtrend
- MOM near 0: Price oscillating or at turning point

---

## VI. Risk Management Features

### 6.1 High Stop-Loss Strategy

| Risk Parameter | Value | Description |
|---------------|-------|-------------|
| stoploss | -0.32336 | Allows maximum 32.336% loss |

**Design Logic**:
- High stop-loss means strategy is willing to endure large drawdowns in exchange for trending move profits
- Suitable for markets with clear and sustained trends; but may cause frequent stop-loss triggers in ranging markets

### 6.2 Force Close Mechanism

| Parameter | Value | Purpose |
|----------|-------|---------|
| ROI["5127"] | 0 | Force close after ~3.56 days |

**Design Logic**: Prevents excessive holding leading to profit givebacks or unexpected risks.

### 6.3 Risk Assessment Summary

| Risk Type | Level | Description |
|-----------|-------|-------------|
| Drawdown Risk | High | -32% stop-loss; significant volatility |
| False Signal Risk | Medium | MOM<15 condition filters some false signals |
| Trend Reversal Risk | Medium | Relies on MA crossover; may lag |

---

## VII. Strategy Pros & Cons

### Advantages

1. **Simple and Efficient Indicators**: Uses only 3 technical indicators; clear logic; easy to understand and optimize
2. **Multi-Indicator Confirmation**: Combines momentum and moving average indicators; reduces false signal interference
3. **Strong Trend-Following Capability**: High stop-loss design allows strategy to fully capture trending moves
4. **Moderate Timeframe**: 4-hour framework balances trend judgment and trading frequency

### Limitations

1. **High Stop-Loss Risk**: -32% stop-loss may cause significant losses in ranging markets
2. **Parameter Sensitive**: MOM thresholds (15/80) and MA periods (13/25) may need per-market adjustment
3. **Trend Reversal Lag**: MA death cross typically occurs after trend reversal; sell may not be timely enough
4. **Lacks Protection Mechanism**: No additional entry protection (volume filtering, RSI confirmation, etc.)

---

## VIII. Applicable Scenarios

| Market Environment | Recommendation | Action |
|-------------------|----------------|--------|
| Clear uptrend in bull market | Suitable | MA golden cross signals effective; high returns expected |
| Clear downtrend in bear market | Suitable | Short selling also applicable via same logic; can capture downtrends |
| Ranging market | Not recommended | High stop-loss causes frequent losses |
| Consolidation | Not recommended | MA crossovers frequently produce false signals |

---

## IX. Applicable Market Environment Details

Chispei is a **trend-following strategy** trading based on technical indicator crossover signals. It is best suited for **markets with clear trends and moderate volatility**, and performs poorly in **low-volatility ranging markets**.

### 9.1 Core Strategy Logic

- **Momentum Filter**: Enter when MOM<15, indicating relatively bottom area of downtrend; exit when MOM<80, indicating upward momentum weakening
- **MA Confirmation**: Uses SMA golden/death cross to confirm trend direction; avoids being misled by short-term fluctuations
- **Let Profits Run**: High stop-loss design allows strategy to hold positions until trend ends

### 9.2 Performance in Different Market Environments

| Market Type | Rating | Analysis |
|:---|:---|:---|
| Uptrend | Five Stars | MA golden cross accurately captures uptrends; MOM rebounds from lows |
| Downtrend | Four Stars | Same logic applicable for shorting; can capture downtrends |
| Ranging Market | Two Stars | MA frequent crossovers produce false signals; high stop-loss causes losses |
| Fast Fluctuation | Three Stars | 4-hour framework may lag; high stop-loss protects capital |

### 9.3 Key Configuration Suggestions

| Configuration | Suggested Value | Notes |
|---------------|-----------------|-------|
| Trading Pairs | Mainstream coins (BTC/ETH) | Good liquidity; more stable trends |
| Timeframe | 4h | Strategy's native design; do not change |
| Initial Capital | Recommend 20%+ risk control | High stop-loss strategy needs sufficient capital buffer |

---

## X. Important Notes: The Cost of Complexity

### 10.1 Strategy Simplicity

Chispei is a **relatively simple** strategy with small code volume, containing only:
- 3 technical indicator calculations
- 1 buy condition group
- 1 sell condition group

This means:
- **Low learning curve**: Easy to understand strategy logic
- **Low overfitting risk**: Few parameters; not prone to over-optimization
- **Better live stability**: Simple logic; small difference between backtesting and live

### 10.2 Backtesting vs Live Trading Differences

| Difference | Impact | Suggestion |
|-----------|--------|------------|
| MOM indicator calculation | Possible platform differences | Use same data source |
| Slippage | Live execution price may be worse | Consider setting wider stop-loss |
| Liquidity | Large capital may not execute instantly | Build positions in batches |

### 10.3 Manual Trading Suggestions

Since strategy logic is clear, manual traders can easily implement:
1. Check 4-hour candles before daily close
2. Buy when MOM<15 AND 13-day MA > 25-day MA
3. Sell when MOM<80 AND 13-day MA < 25-day MA
4. Strictly adhere to 32% stop-loss line

---

## XI. Summary

Chispei is a **simple and efficient trend-following strategy**, with core value in:

1. **Simple and Reliable**: Uses only 3 indicators; clear logic; not prone to overfitting
2. **Strong Trend Capture**: High stop-loss design lets profits run fully
3. **Good Adaptability**: Works both long and short; applicable in bull and bear markets
4. **Medium-Low Frequency Trading**: 4-hour framework reduces trading frequency; lowers fees

For quantitative traders, Chispei is an **entry-level trend strategy** suitable as a learning starting point for quantitative trading or as a foundational module for combined strategies. However, pay attention to its high stop-loss characteristic; must control single-trade risk when using.

**Usage Recommendations**:
- Recommend testing with small capital on live trading for 1-2 months first
- Monitor MOM threshold performance in different market environments
- Consider adding additional filtering conditions (volume, RSI, etc.) to optimize signals
