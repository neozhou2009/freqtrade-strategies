# Stinkfist 策略深度解读

> **策略编号**: #389 (465 个策略中的第 389 个)  
> **策略类型**: 自定义指标 + 动态加仓 + 价格保护机制  
> **时间框架**: 5 分钟 (5m) + 1 小时信息层 (1h)

---

## 一、策略概览

Stinkfist 是一个基于多种自定义技术指标的复杂趋势跟踪策略，支持动态加仓和精细的价格保护机制。策略名称源自 Tool 乐队的经典歌曲，体现了"深度挖掘"的设计理念——通过多层次的技术分析来寻找交易机会。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 2 套独立买入信号（新仓位 + 加仓），可独立触发 |
| **卖出条件** | 多条件组合卖出，包含动态止损和仓位管理 |
| **保护机制** | 3 组保护参数（价格保护、超时检查、订单确认） |
| **时间框架** | 5m 主时间框架 + 1h 信息时间框架 |
| **依赖库** | numpy, talib, technical.indicators, qtpylib, arrow, cachetools, pandas |
| **子策略** | BTC 专用版 (Stinkfist_BTC) 和 ETH 专用版 (Stinkfist_ETH) |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.05,      # 即刻：5% 利润目标
    "10": 0.025,    # 10 分钟后：2.5% 利润目标
    "20": 0.015,    # 20 分钟后：1.5% 利润目标
    "30": 0.01,     # 30 分钟后：1% 利润目标
    "720": 0.005,   # 12 小时后：0.5% 利润目标
    "1440": 0       # 24 小时后：平仓退出
}

# 止损设置
stoploss = -0.40    # 40% 硬止损
```

**设计思路**：
- 采用阶梯式 ROI 机制，持仓时间越长，利润目标越低
- 40% 的宽松止损给予策略足够的波动空间
- 24 小时后强制平仓，避免长期套牢

### 2.2 订单类型配置

```python
use_sell_signal = True         # 启用卖出信号
sell_profit_only = True        # 仅在盈利时使用卖出信号
ignore_roi_if_buy_signal = True  # 有买入信号时忽略 ROI
```

### 2.3 买入参数

```python
buy_params = {
    'inf-pct-adr': 0.80,  # 信息层 ADR 百分比阈值
    'mp': 30              # Momentum Pinball 阈值
}
```

---

## 三、买入条件详解

### 3.1 保护机制（3 组）

每个买入条件都配有独立的保护参数组：

| 保护类型 | 参数说明 | 默认值示例 |
|---------|---------|-----------|
| **价格保护** | 订单价格与当前价格偏差检查 | > 1% 拒绝 |
| **买入超时** | 订单未成交检查 | 价格偏离 > 1% 取消 |
| **卖出超时** | 订单未成交检查 | 价格偏离 < 1% 取消 |

### 3.2 买入条件分类

策略包含两套独立的买入逻辑：

#### 条件组 1：新仓位买入（4 个条件）

```python
# 逻辑
- 信息层条件：close <= 3d_low + (0.80 * adr)
- Momentum Pinball：mp < 30
- Streak ROC：streak-roc > pcc-lowerband
- MA Cross：mac == 1
```

**条件详解**：

| 条件编号 | 指标 | 条件 | 含义 |
|---------|------|------|------|
| 1 | 信息层 | `close <= 3d_low + (0.80 * adr)` | 价格接近 3 天低点 + 80% 日波动范围 |
| 2 | Momentum Pinball | `mp < 30` | 动量指标显示超卖状态 |
| 3 | Streak ROC | `streak-roc > pcc-lowerband` | 连续变化率高于下轨 |
| 4 | MA Cross | `mac == 1` | 快速均线上穿慢速均线 |

#### 条件组 2：加仓买入（动态增长逻辑）

```python
# 逻辑（仅在有活跃交易时触发）
- RMI 趋势向上：rmi-up-trend == 1
- 利润保护：current_profit > (peak_profit * profit_factor)
- RMI 增长阈值：rmi-slow >= linear_growth(30, 70, 180, 720)
```

**动态增长函数**：
```python
def linear_growth(self, start: float, end: float, 
                  start_time: int, end_time: int, trade_time: int) -> float:
    # 从 start（30）线性增长到 end（70）
    # 时间范围：180-720 分钟
    # 持仓越久，阈值越高
```

### 3.3 信息层指标详解

策略使用 1 小时时间框架作为信息层，提供更高维度的趋势判断：

```python
# 信息层指标
informative['1d_high'] = informative['close'].rolling(24).max()   # 24小时最高
informative['3d_low'] = informative['close'].rolling(72).min()     # 3天最低
informative['adr'] = informative['1d_high'] - informative['3d_low']  # 波动范围
```

---

## 四、卖出逻辑详解

### 4.1 动态止损系统

策略采用动态止损机制：

```python
# 动态止损阈值计算
loss_cutoff = linear_growth(-0.03, 0, 0, 300, open_minutes)
# 持仓时间越长，止损阈值越高（从 -3% 到 0%）
```

### 4.2 卖出信号组合

| 条件组 | 触发条件 | 说明 |
|--------|---------|------|
| 动态止损 | `current_profit < loss_cutoff` 且 `profit > stoploss` | 持仓越久止损越紧 |
| RMI 趋势反转 | `rmi-dn-trend == 1` | RMI 趋势向下 |
| 利润状态判断 | `peak_profit > 0` 时 `rmi-slow < 50`，否则 `rmi-slow < 10` | 区分盈利和亏损状态 |
| 仓位管理 | 有其他持仓时进行综合判断 | 考虑全局仓位 |

### 4.3 卖出信号逻辑

```python
# 卖出信号组合
conditions.append(
    (trade_data['current_profit'] < loss_cutoff) & 
    (trade_data['current_profit'] > self.stoploss) &  
    (dataframe['rmi-dn-trend'] == 1) &
    (dataframe['volume'].gt(0))
)
if trade_data['peak_profit'] > 0:
    conditions.append(dataframe['rmi-slow'] < 50)
else:
    conditions.append(dataframe['rmi-slow'] < 10)
```

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 用途 |
|---------|---------|------|
| **RMI** | RMI(21, 5) 慢速、RMI(8, 4) 快速 | 相对动量指标，趋势判断 |
| **MA Streak** | MA Streak(4) | 连续上涨/下跌计数 |
| **PCC** | Percent Change Channel(20, 2) | 百分比变化通道 |
| **MAC** | Moving Average Cross(20, 50) | 均线交叉判断 |
| **ROC/RSI** | ROC(1), RSI(ROC, 3) | 动量弹球指标 |

### 5.2 信息时间框架指标（1h）

策略使用 1 小时时间框架作为信息层：

- **24 小时最高价**：`1d_high = close.rolling(24).max()`
- **3 天最低价**：`3d_low = close.rolling(72).min()`
- **波动范围**：`adr = 1d_high - 3d_low`

### 5.3 自定义指标实现

#### MA Streak（连续计数）
```python
def ma_streak(self, dataframe: DataFrame, period: int = 4) -> Series:
    # 计算连续上涨/下跌的次数
    # 正数表示连续上涨，负数表示连续下跌
```

#### Percent Change Channel（百分比变化通道）
```python
def pcc(self, dataframe: DataFrame, period: int = 20, mult: int = 2):
    # 类似肯特纳通道，但使用百分比变化计算
    # 计算上轨、中轨、下轨
```

#### MA Cross（均线交叉）
```python
def mac(self, dataframe: DataFrame, fast: int = 20, slow: int = 50) -> Series:
    # 快速EMA（20）和慢速EMA（50）交叉判断
    # 返回 1（看涨）或 -1（看跌）
```

---

## 六、风险管理特色

### 6.1 价格保护机制

策略实现了三层价格保护：

```python
def confirm_trade_entry(self, pair: str, order_type: str, 
                        amount: float, rate: float, ...) -> bool:
    # 入场价格保护：当前价格 > 订单价格 * 1.01 时拒绝
    if current_price > rate * 1.01:
        return False
    return True

def check_buy_timeout(self, pair: str, trade: Trade, order: dict, ...) -> bool:
    # 买入超时：价格偏离 > 1% 时取消订单
    if current_price > order['price'] * 1.01:
        return True
    return False

def check_sell_timeout(self, pair: str, trade: Trade, order: dict, ...) -> bool:
    # 卖出超时：价格偏离 < 1% 时取消订单
    if current_price < order['price'] * 0.99:
        return True
    return False
```

### 6.2 全局仓位管理

策略跟踪所有开放交易进行综合判断：

| 数据项 | 说明 |
|--------|------|
| `active_trade` | 当前交易对是否有活跃交易 |
| `current_profit` | 当前利润比例 |
| `peak_profit` | 峰值利润 |
| `open_minutes` | 持仓时间（分钟） |
| `other_trades` | 是否有其他交易 |
| `avg_other_profit` | 其他交易平均利润 |
| `biggest_loser` | 当前是否为最大亏损交易 |
| `free_slots` | 剩余可用仓位 |

### 6.3 缓存机制

```python
custom_current_price_cache: TTLCache = TTLCache(maxsize=100, ttl=300)
# 5 分钟价格缓存，减少 API 调用
```

---

## 七、策略优势与局限

### ✅ 优势

1. **多层次保护机制**：价格保护、超时检查、订单确认三层防护
2. **动态加仓逻辑**：根据持仓时间和利润状态智能加仓
3. **信息层辅助决策**：1 小时时间框架提供更高维度的趋势判断
4. **子策略定制化**：BTC 和 ETH 版本有独立的优化参数
5. **全局仓位管理**：考虑所有持仓的综合利润和风险

### ⚠️ 局限

1. **复杂度高**：自定义指标多，理解和调试难度大
2. **止损宽松**：40% 的止损可能导致较大回撤
3. **依赖实时数据**：需要频繁获取当前价格和订单簿数据
4. **加仓逻辑风险**：在趋势逆转时加仓可能放大亏损

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| 波动市场 | 默认参数 | 利用波动范围指标捕捉机会 |
| 趋势市场 | ETH 版本 | 启用追踪止损锁定利润 |
| 震荡市场 | 调高 mp 阈值 | 减少假信号 |
| 高波动币种 | BTC 版本 | 关闭卖出信号，靠 ROI 退出 |

---

## 九、适用市场环境详解

Stinkfist 是一个**深度挖掘型策略**。基于其代码架构和多层保护机制，它最适合 **波动较大的市场环境**，而在单边暴跌时表现不佳。

### 9.1 策略核心逻辑

- **信息层辅助**：使用 1 小时框架的 3 天低点和波动范围判断入场时机
- **动态加仓**：根据持仓时间和利润状态智能调整加仓策略
- **全局视角**：考虑所有持仓的综合表现进行仓位管理
- **价格保护**：防止在价格剧烈波动时以不利价格成交

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 波动上涨 | ⭐⭐⭐⭐⭐ | 利用波动范围指标捕捉回调买入机会 |
| 🔄 震荡波动 | ⭐⭐⭐⭐☆ | 策略设计初衷，配合信息层判断 |
| 📉 单边下跌 | ⭐⭐☆☆☆ | 加仓逻辑可能放大亏损 |
| ⚡️ 低波动横盘 | ⭐⭐☆☆☆ | 缺乏明确的趋势信号 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| `inf-pct-adr` | 0.80-0.92 | 控制入场位置的激进程度 |
| `mp` | 30-66 | 动量阈值，越低越保守 |
| `stoploss` | -0.40 | 保持宽松以容纳波动 |
| 时间框架 | 5m + 1h | 不要轻易修改 |

---

## 十、重要提醒：复杂性的代价

### 10.1 学习成本

策略包含多个自定义指标（RMI、MA Streak、PCC、MAC），需要深入理解每个指标的含义和相互作用。建议先在回测环境中充分测试。

### 10.2 硬件要求

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 1-5 对 | 2 GB | 4 GB |
| 5-20 对 | 4 GB | 8 GB |
| 20+ 对 | 8 GB | 16 GB |

### 10.3 回测与实盘的差异

策略依赖实时价格数据和订单簿信息：
- 回测环境可能无法完全模拟价格保护逻辑
- 加仓逻辑在实盘中更加敏感
- 缓存机制在回测中效果可能不同

### 10.4 手动交易者建议

如果想在手动交易中借鉴此策略：
1. 关注 3 天低点 + 80% 日波动范围作为入场区域
2. 使用 RMI 和 MA Cross 确认趋势
3. 设置动态止损而非固定止损
4. 不要盲目加仓，等待趋势确认

---

## 十一、总结

**Stinkfist** 是一个**深度挖掘型的复杂策略**，通过多层次的技术分析和保护机制来寻找交易机会。它的核心价值在于：

1. **信息层辅助决策**：使用 1 小时框架提供更高维度的趋势判断
2. **动态风险管理**：根据持仓时间和利润状态调整策略参数
3. **全局仓位视角**：考虑所有持仓的综合表现，而非孤立判断

对于量化交易者而言，这是一个适合波动市场的策略，但需要充分理解其加仓逻辑和价格保护机制后再进行实盘部署。建议从单交易对开始测试，逐步扩展到多交易对场景。

---

## 十二、子策略变体

### Stinkfist_BTC（BTC 专用版）

```python
buy_params = {
    'inf-pct-adr': 0.91556,
    'mp': 66,
}
use_sell_signal = False  # 关闭卖出信号，依靠 ROI 退出
```

**特点**：更高的入场阈值，关闭卖出信号，更适合 BTC 的波动特性。

### Stinkfist_ETH（ETH 专用版）

```python
buy_params = {
    'inf-pct-adr': 0.81628,
    'mp': 40,
}
trailing_stop = True
trailing_stop_positive = 0.014
trailing_stop_positive_offset = 0.022
trailing_only_offset_is_reached = False
use_sell_signal = False
```

**特点**：启用追踪止损，参数经过 ETH 市场的优化。