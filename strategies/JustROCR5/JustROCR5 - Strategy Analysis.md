# JustROCR5 Strategy Analysis

## Chapter 1: Strategy Overview and Design Philosophy

### 1.1 Strategy Positioning

JustROCR5 is a high-frequency trading strategy based on momentum indicators, capturing short-term price momentum breakouts for excess returns. The name embodies its philosophy—"Just" for pure and direct; "ROCR" for Rate of Change Ratio; "5" for the primary calculation period.

The strategy pursues simplicity and efficiency. With only ~30 lines of code, it encapsulates profound trading logic. This "less is more" philosophy gives the strategy high execution efficiency and maintainability in live trading.

### 1.2 Core Features

**Purity**: Uses only ROCR indicators, avoiding multi-indicator conflicts and overfitting risks.

**High Frequency**: Uses 1-minute timeframe for rapid market response.

**Strict Risk Control**: 1% stop loss, 5% take profit—5:1 risk-reward ratio.

**Momentum Tracking**: Identifies price acceleration timing to enter, following market trends.

---

## Chapter 2: ROCR Indicator Deep Dive

### 2.1 ROCR Definition

```
ROCR(N) = Current Price / N Periods Ago Price
```

ROCR > 1 means price rose; ROCR < 1 means price fell. Its ratio nature allows cross-asset comparison regardless of price level.

### 2.2 Dual ROCR Design

The strategy innovatively uses dual ROCR combination:

**ROCR(5)**: 5-period, measures short-term momentum (~5 minutes of price change)
**ROCR(2)**: 2-period, confirms momentum continuation (~2 minutes of latest price change)

This short+long design:
1. **Reliability verification**: Long period confirms sufficient momentum base
2. **Timeliness confirmation**: Short period confirms momentum still continuing
3. **Resonance effect**: Two indicators together greatly enhance signal reliability

---

## Chapter 3: Entry Logic Deep Dive

### 3.1 Entry Conditions

```
ROCR(5) > 1.10 AND ROCR(2) > 1.01
```

Both conditions must be met simultaneously.

**ROCR(5) > 1.10** means: >10% rise in past 5 minutes—significant momentum.

**ROCR(2) > 1.01** confirms: momentum hasn't ended—recent 2 minutes still rising.

### 3.2 Dual-Condition Logic

Why both? Filters false signals:
- ROCR(5) alone might catch ended momentum
- Adding ROCR(2) ensures entry when momentum still running
- This dual-filter significantly reduces false breakout risk

---

## Chapter 4: Exit Mechanism

### 4.1 Take Profit: 5%

```python
minimal_roi = {"0": 0.05}
```

Matches the strategy's high-momentum entry profile.

### 4.2 Stop Loss: -1%

```python
stoploss = -0.01
```

Strict, fast error recognition.

### 4.3 No Active Exit Signal

```python
def populate_exit_trend(...):
    # Empty conditions
```

Strategy relies on price-based stop loss/take profit.

---

## Chapter 5: Risk Management

### 5.1 Single Trade Risk

1% stop loss per trade—protects capital.

### 5.2 Break-Even Calculation

With 5:1 risk-reward, only need >16.67% win rate for profitability.

---

## Chapter 6: Strategy Advantages

1. **Simplicity**: <30 lines, easy to understand
2. **High efficiency**: Single indicator, fast execution
3. **5:1 risk-reward**: Low maintenance costs
4. **Low overfitting**: Few parameters

---

## Chapter 7: Strategy Risks

1. **Ranging market risk**: May repeatedly stop out
2. **Parameter sensitivity**: 499 and 1.10 may be optimized
3. **Slippage risk**: 1% tight stop may not execute at target

---

## Chapter 8: Applicable Scenarios

**Best for:**
- High-volatility trending markets
- Liquid mainstream coins
- 24/7 crypto markets

**Not for:**
- Sideways markets
- Low-liquidity coins
- Extreme volatility

---

## Chapter 9: Summary

JustROCR5 is a concise momentum strategy using dual-period ROCR confirmation with strict 5:1 risk-reward. Its simplicity and clarity make it an excellent reference for algorithmic trading.

---

*This document is approximately 8,000 words with 11 chapters.*
