# Freqtrade 策略修复日志

---

## 修复日期
2026-03-03

---

## 概述
修复 freqtrade 策略以适配最新版本的 API 接口。主要问题包括：
1. **qtpylib 导入路径变更**
2. **INTERFACE_VERSION 从 2 升级到 3**
3. **废弃参数重命名**
4. **代码兼容性问题**（如 numpy.NAN → nan）

---

## 通用修复清单

### 1. qtpylib 导入修复
```python
# 旧写法
import freqtrade.vendor.qtpylib.indicators as qtpylib

# 新写法
from technical import qtpylib
```

### 2. INTERFACE_VERSION 修复
```python
# 旧写法
INTERFACE_VERSION = 2

# 新写法
INTERFACE_VERSION = 3
```

### 3. 常用废弃参数修复

| 废弃参数/方法 | 新参数/方法 |
|--------------|-------------|
| `sell_profit_only = True` | `exit_profit_only = True` |
| `use_sell_signal = True` | `use_exit_signal = True` |
| `ignore_roi_if_buy_signal = False` | `ignore_roi_if_entry_signal = False` |
| `sell_profit_offset = 0.01` | `exit_profit_offset = 0.01` |
| `order_types["buy"]` | `order_types["entry"]` |
| `order_types["sell"]` | `order_types["exit"]` |
| `order_time_in_force["buy"]` | `order_time_in_force["entry"]` |
| `order_time_in_force["sell"]` | `order_time_in_force["exit"]` |
| `def check_buy_timeout()` | `def check_entry_timeout()` |
| `def check_sell_timeout()` | `def check_exit_timeout()` |
| `ticker_interval = "5m"` | `timeframe = "5m"` |
| `custom_sell()` | `custom_exit()` |

### 4. numpy 兼容性修复
```python
# 旧写法
np.NAN

# 新写法
np.nan
```

### 5. 其他修复
```python
# trailing_stop_positive_offset 必须大于 trailing_stop_positive
trailing_stop_positive = 0.02
trailing_stop_positive_offset = 0.01  # 错误
# 正确:
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
```

---

## 批次修复记录

### ✅ 第1批 (10个) - 2026-03-03 全部通过

| 序号 | 策略名称 | 状态 | 修复内容 |
|------|----------|------|----------|
| 1 | Nostalgia | ✅ | qtpylib + 全部废弃参数 + custom_sell→custom_exit |
| 2 | BBRSI21 | ✅ | qtpylib + INTERFACE_VERSION |
| 3 | BBRSIS | ✅ | +order_types + order_time_in_force + ticker_interval→timeframe |
| 4 | BbandRsi | ✅ | qtpylib + INTERFACE_VERSION |
| 5 | CustomStoplossWithPSAR | ✅ | qtpylib + INTERFACE_VERSION |
| 6 | FixedRiskRewardLoss | ✅ | qtpylib + INTERFACE_VERSION |
| 7 | Guacamole | ✅ | +sell_profit_only + use_sell_signal + check_buy_timeout等 |
| 8 | Ichimoku | ✅ | +sell_profit_only + use_sell_signal + ignore_roi_if_buy_signal |
| 9 | MACD_TRI_EMA | ✅ | qtpylib + INTERFACE_VERSION |
| 10 | Strategy005 | ✅ | +sell_profit_only + use_sell_signal + ignore_roi_if_buy_signal |

**通过率**: 10/10 (100%)

---

### ✅ 第2批 (10个) - 2026-03-03 9/10 通过

| 序号 | 策略名称 | 状态 | 修复内容 | 备注 |
|------|----------|------|----------|------|
| 11 | PRICEFOLLOWINGX | ✅ | qtpylib + 全部废弃参数 | |
| 12 | Kamaflage | ✅ | qtpylib + INTERFACE_VERSION | |
| 13 | ReinforcedQuickie | ✅ | qtpylib | |
| 14 | YOLO | ✅ | qtpylib | |
| 15 | CombinedBinHAndCluc2021Bull | ✅ | qtpylib | |
| 16 | Roth01 | ✅ | qtpylib | |
| 17 | ClucFiatROI | ✅ | +sell_profit_offset→exit_profit_offset | |
| 18 | ema | ✅ | qtpylib + trailing_stop_positive_offset修正 | |
| 19 | stratfib | ✅ | qtpylib + order_types修复 | |
| 20 | MultiMA_TSL | ❌ | qtpylib + INTERFACE_VERSION | pandas duplicate labels bug (非接口问题) |

**通过率**: 9/10 (90%)

---

### ⚠️ 第3批 (10个) - 2026-03-03 5/10 接口修复完成

| 序号 | 策略名称 | 状态 | 修复内容 | 问题说明 |
|------|----------|------|----------|----------|
| 21 | BBRSI4cust | ❌ | qtpylib | 代码bug - custom_exit float index error |
| 22 | CombinedBinHAndClucV7 | ✅ | qtpylib + INTERFACE_VERSION + np.NAN修复 | |
| 23 | NotAnotherSMAOffsetStrategy | ✅ | qtpylib + INTERFACE_VERSION + order_time_in_force | |
| 24 | Schism2 | ❌ | qtpylib | Python代码错误 (非接口问题) |
| 25 | BBRSI | ❌ | qtpylib | Python代码错误 (非接口问题) |
| 26 | strato | ❌ | qtpylib + INTERFACE_VERSION | 需要entry_pricing配置 |
| 27 | ichiV1 | ✅ | qtpylib + INTERFACE_VERSION | |
| 28 | Inverse | ✅ | qtpylib + INTERFACE_VERSION + order_types + order_time_in_force + np.NAN修复 | |
| 29 | EMAVolume | ✅ | qtpylib + ticker_interval→timeframe | |
| 30 | Ichimoku_v31 | ❌ | qtpylib | 需要entry_pricing配置 |

**通过率**: 5/10 (50%) - 5个接口问题，5个其他问题

---

### ✅ 第4批 (10个) - 2026-03-03 10/10 全部通过

| 序号 | 策略名称 | 状态 | 修复内容 | 备注 |
|------|----------|------|----------|------|
| 31 | XebTradeStrat | ✅ | qtpylib + INTERFACE_VERSION | |
| 32 | ONUR | ✅ | qtpylib + order_types修复 (emergencysell→emergency_exit等) | |
| 33 | BB_RPB_TSL_RNG_TBS_GOLD | ✅ | qtpylib + INTERFACE_VERSION | |
| 34 | Stavix2 | ✅ | qtpylib | |
| 35 | NostalgiaForInfinityNext_ChangeToTower_V6 | ✅ | qtpylib + INTERFACE_VERSION + order_types + trailing_stop_loss + custom_sell→custom_exit | |
| 36 | bbema | ✅ | qtpylib + INTERFACE_VERSION + order_types + order_time_in_force | 去除了重复的order_time_in_force定义 |
| 37 | ActionZone | ✅ | qtpylib + INTERFACE_VERSION + order_types + order_time_in_force + custom_sell→custom_exit | |
| 38 | NostalgiaForInfinityV4HO | ✅ | qtpylib + INTERFACE_VERSION + order_types + trailing_stop_loss + custom_sell→custom_exit | |
| 39 | BuyOnly | ✅ | qtpylib + INTERFACE_VERSION | |
| 40 | NFI46 | ✅ | qtpylib + INTERFACE_VERSION + order_types + trailing_stop_loss + custom_sell→custom_exit | |

**通过率**: 10/10 (100%)

> **注意**: 第4批发现并修复了新的废弃参数问题：
> - `emergencysell` → `emergency_exit`
> - `forcebuy` → `force_entry`
> - `forcesell` → `force_exit`
> - `trailing_stop_loss` (order_types中需要移除)

---

### ✅ 第5批 (10个) - 2026-03-03 10/10 全部通过

| 序号 | 策略名称 | 状态 | 修复内容 |
|------|----------|------|----------|
| 41 | BB_RPB_TSL_c7c477d_20211030 | ✅ | qtpylib + use_sell_signal→use_exit_signal |
| 42 | BB_RPB_TSLmeneguzzo | ✅ | qtpylib + use_sell_signal→use_exit_signal + custom_sell→custom_exit |
| 43 | BB_RSI | ✅ | qtpylib + 3废弃参数 + ticker_interval→timeframe + order_types |
| 44 | BB_Strategy04 | ✅ | qtpylib + INTERFACE_VERSION + 3废弃参数 + ticker_interval→timeframe + order_types + order_time_in_force |
| 45 | BBands | ✅ | qtpylib + INTERFACE_VERSION + 3废弃参数 + order_types + order_time_in_force |
| 46 | BBandsRSI | ✅ | qtpylib + INTERFACE_VERSION + 3废弃参数 + order_types + order_time_in_force |
| 47 | BBlower | ✅ | qtpylib + 3废弃参数 |
| 48 | Babico_SMA5xBBmid | ✅ | qtpylib + 2废弃参数 + order_types |
| 49 | Bandtastic | ✅ | qtpylib + INTERFACE_VERSION |
| 50 | BbRoi | ✅ | qtpylib + 2废弃参数 + ticker_interval→timeframe + order_types |

**通过率**: 10/10 (100%)

---

## 总体统计

| 指标 | 数值 |
|------|------|
| 已处理批次 | 5 |
| 已修复策略 | 50 |
| 接口修复通过 | 44 (88%) |
| 遇到的额外问题类型 | 5 |
| 剩余待修复文件 | ~370+ |
| 最近批次通过率 | 10/10 (100%) |

---

## 遇到的额外问题清单

### 1. pandas duplicate labels
- **策略**: MultiMA_TSL
- **错误**: `ValueError: cannot reindex on an axis with duplicate labels`
- **原因**: 代码逻辑错误
- **状态**: 需要深入调试

### 2. custom_exit float index error
- **策略**: BBRSI4cust
- **错误**: `AttributeError("'float' object has no attribute 'index'")`
- **原因**: custom_exit 方法有bug
- **状态**: 需要调试

### 3. Python代码错误
- **策略**: Schism2, BBRSI
- **错误**: `Impossible to load Strategy - class does not exist or contains Python code errors`
- **原因**: 代码本身有语法或逻辑错误
- **状态**: 需要逐个检查

### 4. entry_pricing 配置缺失
- **策略**: strato, Ichimoku_v31 (市场订单)
- **错误**: `Market entry orders require entry_pricing.price_side = "other"`
- **原因**: 使用market订单时需要额外配置 `entry_pricing`
- **状态**: 需要添加配置

### 5. numpy.NAN → nan
- **策略**: CombinedBinHAndClucV7, Inverse
- **错误**: `AttributeError: module 'numpy' has no attribute 'NAN'`
- **修复**: np.NAN → np.nan
- **状态**: ✅ 已修复

---

## 测试命令
```bash
cd test
./test-freqtrade.sh backtest -c config.json --strategy <StrategyName> --timerange=20250101-20250301
```

---

## 下一步计划
1. 继续第6批修复 (10个策略)
2. 对已修复但未通过的策略进行进一步调试
3. 批量修复剩余的 qtpylib 和 INTERFACE_VERSION 问题
4. 完成后进行全部策略的回归测试

---

## 修复工具使用
- `ast_grep_replace`: 用于批量替换代码模式
- `sed` 命令: 用于快速批量替换简单字符串
- `docker run freqtrade`: 用于测试策略

---
