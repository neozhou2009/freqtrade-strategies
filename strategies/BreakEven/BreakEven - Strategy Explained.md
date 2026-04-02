# BreakEven Strategy: The "Get Me Out NOW!" Exit Tool

---

## 1. What's This Strategy All About?

**BreakEven**, or the "Quick Exit Strategy" — honestly, the name is a bit misleading.

It doesn't help you "break even" or make money. Instead, it's a **tool specifically designed to quickly liquidate positions**.

Imagine this: you're in a trade, suddenly you hear news the market might turn, or you just need to close all positions to do something else — that's when BreakEven comes in handy.

**One-line summary: This isn't a "make money" strategy — it's a "get out fast" tool.**

---

## 2. Core Settings

Three numbers:

```python
minimal_roi = {
    "0": 0.01,      # Made 1%? Sell immediately
    "10": 0         # Held 10 minutes? Sell regardless of profit/loss
}

stoploss = -0.05   # Lost 5%? Stop-loss
```

### Three Modes

| Mode | Config | Effect |
|------|--------|--------|
| Conservative | 1% take-profit + 10-min force | Made 1% = out, time's up = out |
| Aggressive | 0% take-profit | Sell as long as not losing money |
| Nuclear | -1% | Force sell everything regardless |

---

## 3. Buy Conditions

**There are NONE.**

```python
def populate_entry_trend(self, dataframe, metadata):
    # Empty! No buy conditions at all
    dataframe.loc[(), 'buy'] = 0
    return dataframe
```

The developer said:

> "Sometimes I just want to shut down the bot ASAP and not have positions floating around."

So this strategy is meant for one thing: **liquidation, not opening positions.**

---

## 4. Exit Logic

Fully automatic — three scenarios:

1. **Made over 1%** → Auto-sell
2. **Held 10 minutes** → Auto-sell
3. **Lost over 5%** → Stop-loss sell

---

## 5. The Strategy's "Personality"

| Trait | Description |
|-------|-------------|
| **Personality** | Cautious, conservative, impatient |
| **Catchphrase** | "Run!" "Lock in profits!" "Don't be greedy!" |
| **Strengths** | Strong execution, no hesitation, strong risk awareness |
| **Weaknesses** | Easy to miss big moves, no patience |
| **Good For** | Insurance agent, firefighter, cleaner |
| **Bad For** | Vanguard, general |

**In short: A "take-profits-and-run, never fight-the-market" personality.**

---

## 6. Summary: What's It For?

**BreakEven is a "liquidation-only tool."**

- Won't buy
- Only sells
- Made 1% = out
- 10 minutes = out
- Lost 5% = out

**It's not for making money — it's for controlling risk.**

---

## 7. ⚠️ Final Warning

| Risk | Description |
|------|-------------|
| ❌ Misses big moves | 10 minutes and out — big trends don't care |
| ❌ High trading frequency | May accumulate significant fees |
| ❌ Can't be main strategy | It can't even buy! |
| ❌ Not for long-term | 10 minutes = forced liquidation |

**Remember: BreakEven is the "run-away神器", not the "make-money神器".**

Use it to protect your assets, not to profit.
