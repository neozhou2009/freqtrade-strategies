# ClucHAnix_BB_RPB_MOD_CTT 策略深度解读

> **策略编号**: #99 (465 个策略中的第 99 个)  
> **策略类型**: 多条件趋势跟踪 + 布林带均值回归 + 自定义动态止盈止损 + CTT 时间窗口交易  
> **时间框架**: 1 分钟 (1m) + 1小时/1天信息层

---

## 一、策略概览

ClucHAnix_BB_RPB_MOD_CTT 是一个基于 Heikin Ashi（平均K线）和布林带均值回归原理的高级趋势跟踪策略。该策略是 ClucHAnix_BB_RPB_MOD 的增强版本，引入了 CTT（Custom Time Window Trading）自定义时间窗口交易机制，在特定时间段内启用或禁用交易信号，从而过滤不利的交易时段。策略名称中的"Cluc"源自"Cluc"系列，"BB"代表 Bollinger Bands（布林带），"RPB"代表自定义动态止盈模块，"MOD"表示经过修改的版本，"CTT"代表自定义时间窗口交易机制。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 8 个独立买入信号（7 个可独立启用/禁用），均需满足基础保护过滤 |
| **卖出条件** | 1 个基础卖出信号 + 多层动态止盈/止损系统（BB_RPB_TSL 风格） |
| **保护机制** | 2 组买入保护参数（BTC 趋势保护 + Pump 强度保护） + CTT 时间窗口过滤 |
| **时间框架** | 主时间框架 1m + 信息时间框架 1h 和 1d |
| **依赖库** | technical, pandas_ta, talib, numpy, pandas, qtpylib |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.10,      # 开仓后立即平仓可获得 10% 利润
    "60": 0.07,     # 1分钟后利润降至 7%
    "120": 0.05,    # 2分钟后利润降至 5%
    "240": 0.03,    # 4分钟后利润降至 3%
}

# 止损设置
stoploss = -0.10   # 基础止损线 -10%

# 追踪止损
trailing_stop = True
trailing_stop_positive = 0.001    # 盈利 0.1% 后启动追踪
trailing_stop_positive_offset = 0.012  # 追踪止损距离现价 1.2%
trailing_only_offset_is_reached = False
```

**设计思路**：
- **ROI 表设计**：采用前重后轻的梯度设计，初期期望获得较高利润（10%），随着时间推移逐步降低利润目标（4 分钟时仅需 3%）。这种设计在捕捉短期波动利润的同时，给趋势行情留出延续空间。
- **止损设计**：基础止损设置为 -10%，结合 custom_stoploss 实现的两级动态止盈止损机制，在不同盈利区间采用不同的风险管理策略。

### 2.2 订单类型配置

```python
order_types = {
    'buy': 'market',
    'sell': 'market',
    'emergencysell': 'market',
    'forcebuy': "market",
    'forcesell': 'market',
    'stoploss': 'market',
    'stoploss_on_exchange': False,
    'stoploss_on_exchange_interval': 60,
    'stoploss_on_exchange_limit_ratio': 0.99
}
```

**设计思路**：全部采用市价单（market order），确保订单立即成交，避免滑点风险

### 2.3 CTT 自定义时间窗口配置

```python
# CTT 时间窗口参数
enable_ctt = BooleanParameter(default=True)      # 启用 CTT 机制
ctt_start_hour = IntParameter(0, 23, default=9)  # 开始允许交易的小时
ctt_end_hour = IntParameter(0, 23, default=23)   # 结束允许交易的小时
ctt_days = CategoricalParameter(['all', 'weekdays', 'weekends'], default='all')  # 交易日期设置

# 特殊时段排除
exclude_market_open = BooleanParameter(default=True)  # 排除开盘时段
exclude_market_close = BooleanParameter(default=False) # 排除收盘时段
```

**设计思路**：
- CTT 机制允许交易者在特定时间段内进行交易，过滤掉流动性较低或波动异常的时段
- 可配置只允许在交易活跃时段（如 9:00-23:00）进行交易
- 可选择排除开盘/收盘等特殊时段，避免被套

### 2.4 自定义止损参数（BB_RPB_TSL 机制）

```python
# 硬性止损线
pHSL = DecimalParameter(-0.500, -0.040, default=-0.08)

# 盈利阈值区间 1
pPF_1 = DecimalParameter(0.008, 0.020, default=0.016)  # 触发点
pSL_1 = DecimalParameter(0.008, 0.020, default=0.011)  # 对应止损线

# 盈利阈值区间 2
pPF_2 = DecimalParameter(0.040, 0.100, default=0.080)  # 触发点
pSL_2 = DecimalParameter(0.020, 0.070, default=0.040)  # 对应止损线
```

**设计思路**：
- 当盈利 > 1.6% 时启用第一级保护，止损线上移至 1.1%
- 当盈利 > 8% 时启用第二级保护，止损线上移至 4%
- 当盈利 > 8% 时，止损线随盈利增长线性上移，实现"让利润奔跑"

---

## 三、买入条件详解

### 3.1 CTT 时间窗口过滤机制

CTT 机制在买入条件执行前进行时间窗口过滤，只有在允许的时间段内才会产生买入信号：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| enable_ctt | True | 是否启用 CTT 机制 |
| ctt_start_hour | 9 | 每日开始交易的小时（UTC 时间） |
| ctt_end_hour | 23 | 每日结束交易的小时（UTC 时间） |
| ctt_days | all | 交易日期：all/weekdays/weekends |

**实现逻辑**：
- 获取当前 UTC 时间的小时和星期几
- 判断当前时间是否在 CTT 允许的时间窗口内
- 如果启用排除开盘/收盘，则额外过滤这些特殊时段

### 3.2 基础保护机制（2 组）

每个买入条件都配有独立的保护参数组：

| 保护类型 | 参数说明 | 默认值示例 |
|---------|---------|-----------|
| BTC 趋势保护 | 1天收盘价相对 1分钟收盘价变化率需大于阈值 | > -0.311 |
| Pump 强度保护 | Pump 强度指标需低于阈值（防止追高） | < 0.133 |

**实现逻辑**：
- **BTC 保护**：通过对比 BTC/USDT 的 1 天周期和 1 分钟周期价格变化率，判断市场整体趋势。只有当 BTC 处于上升趋势或相对稳定时，才允许开多单。
- **Pump 保护**：通过 ZEMA 指标计算 Pump 强度，当市场出现快速上涨（Pump）时，降低买入优先级，避免追高被套。

### 3.3 买入条件详解

该策略有 8 个独立的买入条件，其中 7 个可通过布尔参数独立启用或禁用。

#### 条件 #1：Lambo1
```python
# 逻辑
- lambo1_enabled = True (默认禁用)
- close < ema_14 * 1.054 (价格低于 EMA14 的 105.4%)
- rsi_4 < 18 (4周期 RSI 处于超卖区间)
- rsi_14 < 26 (14周期 RSI 处于相对低位)
```

#### 条件 #2：Lambo2
```python
# 逻辑
- lambo2_enabled = True (默认启用)
- close < ema_14 * 0.981 (价格低于 EMA14 的 98.1%)
- rsi_4 < 44 (4周期 RSI 处于超卖区间)
- rsi_14 < 39 (14周期 RSI 处于相对低位)
```

#### 条件 #3：Local Uptrend
```python
# 逻辑
- local_trend_enabled = True (默认启用)
- ema_26 > ema_14 (短期均线高于中期均线，形成上升趋势)
- ema_26 - ema_14 > open * 0.125 (均线发散程度需达到一定阈值)
- close < bb_lowerband2 * 0.823 (价格触及或接近布林下轨)
- closedelta > close * 19.253 / 1000 (收盘价变化需显著)
```

#### 条件 #4：NFI32
```python
# 逻辑
- nfi32_enabled = True (默认启用)
- rsi_20 < rsi_20.shift(1) (RSI 处于下降趋势)
- rsi_4 < 49 (4周期 RSI 处于超卖区间)
- rsi_14 > 15 (14周期 RSI 处于相对高位)
- close < sma_15 * 0.93391 (价格低于 SMA15 的 93.4%)
- cti < -1.09639 (CTI 指标需低于阈值，表示价格走势疲软)
```

#### 条件 #5：EWO1（Elliot Wave Oscillator 高位）
```python
# 逻辑
- ewo_1_enabled = False (默认禁用)
- rsi_4 < 7 (4周期 RSI 极度超卖)
- close < ema(buy) * 1.04116 (价格低于买入均线)
- EWO > 5.249 (EWO 指标处于高位，表示强劲上升趋势)
- rsi_14 < 45 (14周期 RSI 处于相对低位)
- close < ema(sell) * 1.04116 (价格低于卖出均线)
```

#### 条件 #6：EWO Low（Elliot Wave Oscillator 低位）
```python
# 逻辑
- ewo_low_enabled = True (默认启用)
- rsi_4 < 35 (4周期 RSI 处于超卖区间)
- close < ema(buy) * 0.97463 (价格低于买入均线)
- EWO < -11.424 (EWO 指标处于低位，表示下跌趋势中的反弹机会)
- close < ema(sell) * 1.04116 (价格低于卖出均线)
```

#### 条件 #7：Cofi
```python
# 逻辑
- cofi_enabled = False (默认禁用)
- open < ema_8 * 0.639 (开盘价低于 EMA8 的 63.9%)
- fastk 上穿 fastd (随机指标金叉)
- fastk < 13 (快线处于低位)
- fastd < 40 (慢线处于相对低位)
- adx > 8 (ADX 指标显示趋势明确)
- EWO > 5.6 (EWO 指标处于高位)
```

#### 条件 #8：ClucHA
```python
# 逻辑
- clucha_enabled = False (默认禁用)
- rocr_1h > 0.41663 (1小时 ROC 指标显示上升趋势)
- 条件组 A：
  * bbdelta > ha_close * 0.04796 (布林带宽度达标)
  * ha_closedelta > ha_close * 0.00931 (HA 收盘价变化显著)
  * tail < bbdelta * 0.93112 (下影线相对较短)
  * ha_close < lower.shift() (HA 收盘价突破布林下轨)
  * ha_close <= ha_close.shift() (HA 收盘价呈下降趋势)
- 或条件组 B：
  * ha_close < ema_slow (价格低于长期均线)
  * ha_close < bb_lowerband * 0.01645 (价格触及布林下轨)
```

### 3.4 8 个买入条件分类

| 条件组 | 条件编号 | 核心逻辑 | 启用状态 |
|-------|---------|---------|---------|
| RSI 超卖类 | lambo1, lambo2 | 通过多周期 RSI 识别超卖反弹机会 | lambo1 禁用，lambo2 启用 |
| 趋势确认类 | local_uptrend | 均线多头 + 布林下轨支撑 | 启用 |
| 综合判断类 | nfi_32 | RSI 背离 + CTI 趋势疲软 | 启用 |
| 波动突破类 | ewo_1, ewo_low | EWO 极端值 + RSI 超卖 | ewo_1 禁用，ewo_low 启用 |
| 随机指标类 | cofi | 随机指标金叉 + 趋势确认 | 禁用 |
| 布林回归类 | clucHA | HA 蜡烛图 + 布林带均值回归 | 禁用 |

---

## 四、卖出逻辑详解

### 4.1 多层止盈系统（BB_RPB_TSL 机制）

策略采用分段动态止盈止损机制，根据当前盈利水平自动调整止损线：

```
利润率区间          止损策略
────────────────────────────────────────────
盈利 < 1.6%        使用硬性止损 pHSL = -8%
1.6% ≤ 盈利 < 8%   线性插值：从 -1.1% 到 -4%
盈利 ≥ 8%          止损线上移：让利润奔跑
```

**动态止损计算公式**：
```python
if current_profit > PF_2:  # 盈利 > 8%
    sl_profit = SL_2 + (current_profit - PF_2)
elif current_profit > PF_1:  # 1.6% ≤ 盈利 < 8%
    sl_profit = SL_1 + ((current_profit - PF_1) * (SL_2 - SL_1) / (PF_2 - PF_1))
else:  # 盈利 < 1.6%
    sl_profit = HSL
```

### 4.2 基础卖出信号（1 个）

```python
# 卖出信号：Fisher 指标反转
- fisher > 0.38414 (Fisher 指标高于阈值)
- ha_high ≤ ha_high.shift(1) (HA 最高价呈下降趋势)
- ha_high.shift(1) ≤ ha_high.shift(2) (连续两根 K 线最高价下降)
- ha_close ≤ ha_close.shift(1) (HA 收盘价呈下降趋势)
- ema_fast > ha_close (快速均线高于价格，趋势转弱)
- ha_close * 1.07634 > bb_middleband (价格触及布林中轨)
- volume > 0 (有成交量支撑)
```

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 用途 |
|---------|---------|------|
| 趋势指标 | EMA 8/14/26, SMA 15 | 判断价格趋势方向 |
| 动量指标 | RSI 4/14/20, ROCR, Fisher | 识别超买超卖和动量变化 |
| 波动指标 | Bollinger Bands (20, 40 周期), CTI | 判断价格波动性和支撑阻力 |
| 波浪指标 | EWO (Elliot Wave Oscillator) | 识别趋势强度和转折点 |
| 随机指标 | Stoch FastK/FastD | 判断短期超买超卖 |

### 5.2 信息时间框架指标（1h + 1d）

策略使用 1 小时和 1 天作为信息层，提供更高维度的趋势判断：

- **1小时信息层**：
  - Heikin Ashi 收盘价
  - ROCR (Rate of Change) 168 周期 - 反映长期动量

- **1天信息层**：
  - BTC/USDT 收盘价 - 用于 BTC 趋势保护

- **BTC 保护指标**：
  - BTC 1天 vs 1分钟价格变化率 - 判断市场整体趋势

### 5.3 自定义指标

| 指标名称 | 计算方式 | 用途 |
|---------|---------|------|
| Pump 强度 | (ZEMA_30 - ZEMA_200) / ZEMA_30 | 识别市场 Pump 强度 |
| HA 蜡烛图 | qtpylib.heikinashi() | 平滑价格波动，更清晰识别趋势 |
| CTT 时间窗口 | 时间过滤逻辑 | 过滤不利的交易时段 |

---

## 六、风险管理特色

### 6.1 CTT 时间窗口过滤

CTT 机制是本策略的核心特色之一，通过时间窗口过滤来避免在不利的时段交易：

| 时间段 | 交易状态 | 说明 |
|--------|---------|------|
| 允许时段内 | 正常交易 | 根据其他条件决定是否买入 |
| 允许时段外 | 禁止买入 | 即使满足买入条件也不交易 |
| 排除开盘/收盘 | 特殊时段过滤 | 避免流动性风险 |

### 6.2 多层动态止盈止损

BB_RPB_TSL 机制是本策略的核心风险管理特性：

| 盈利区间 | 止损策略 | 保护目标 |
|---------|---------|---------|
| 盈利 < 1.6% | 硬性止损 -8% | 限制最大亏损 |
| 1.6% ≤ 盈利 < 8% | 动态上移 1.1%→4% | 保护已有利润 |
| 盈利 ≥ 8% | 追踪止损 | 让利润奔跑 |

### 6.3 买入条件独立启用/禁用

策略提供 7 个布尔参数，可根据市场环境灵活调整：

```python
ewo_1_enabled = BooleanParameter(default=False)      # EWO 高位条件
ewo_low_enabled = BooleanParameter(default=True)     # EWO 低位条件
cofi_enabled = BooleanParameter(default=False)       # Cofi 条件
lambo1_enabled = BooleanParameter(default=False)     # Lambo1 条件
lambo2_enabled = BooleanParameter(default=True)      # Lambo2 条件
local_trend_enabled = BooleanParameter(default=True) # 局部趋势条件
nfi32_enabled = BooleanParameter(default=True)       # NFI32 条件
clucha_enabled = BooleanParameter(default=False)     # ClucHA 条件
```

### 6.4 市场环境保护

- **BTC 趋势保护**：当 BTC 处于下跌趋势时，减少买入信号
- **Pump 强度保护**：当市场快速上涨时，降低买入优先级

---

## 七、策略优势与局限

### ✅ 优势

1. **多条件并行**：8 个独立买入条件，可覆盖多种市场形态
2. **动态止盈止损**：BB_RPB_TSL 机制在保护利润的同时让利润奔跑
3. **CTT 时间过滤**：通过时间窗口过滤避免不利时段交易
4. **自适应市场**：通过 BTC 保护、Pump 保护和 CTT 机制，适应不同市场环境
5. **条件可配置**：每个买入条件可独立启用/禁用，灵活应对市场变化

### ⚠️ 局限

1. **参数众多**：超过 50 个参数，调优难度大
2. **1分钟框架**：高频交易对硬件和网络要求高
3. **过拟合风险**：多条件策略容易在历史数据上过拟合
4. **计算量大**：多指标计算可能导致交易延迟
5. **CTT 时段限制**：在不允许交易的时段可能错过一些机会

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| 波动市场 | 启用 lambo2, local_uptrend, nfi32, ewo_low | 捕捉超卖反弹和趋势延续 |
| 趋势行情 | 启用 clucHA + 延长 ROI 时间 | 让利润奔跑 |
| 震荡市场 | 关闭所有条件，仅保留基础保护 | 减少频繁交易 |
| BTC 上涨 | 启用 BTC 保护 | 顺势而为 |
| 低流动性时段 | 启用 CTT，限制交易时段 | 避免流动性风险 |

---

## 九、适用市场环境详解

ClucHAnix_BB_RPB_MOD_CTT 是 Cluc 系列策略的布林带均值回归 + 动态止盈止损 + CTT 时间窗口版本。基于其代码架构和参数设计，它最适合 **波动性适中且有一定趋势的市场**，而在极端行情或不活跃时段需谨慎使用。

### 9.1 策略核心逻辑

- **多条件趋势跟踪**：通过 8 个独立的买入条件，捕捉不同形态的买入机会
- **布林带均值回归**：价格触及布林下轨时寻找反弹机会
- **动态止盈止损**：BB_RPB_TSL 机制根据盈利水平自动调整保护策略
- **CTT 时间窗口**：通过时间过滤避免在不利的时段交易
- **市场环境过滤**：BTC 保护和 Pump 保护避免在不利环境下交易

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 趋势上涨 | ⭐⭐⭐⭐⭐ | 多条件可捕捉趋势启动点，动态止盈让利润奔跑 |
| 🔄 震荡整理 | ⭐⭐⭐⭐☆ | RSI 超卖条件可捕捉区间上下沿，ROI 表适合短期波动 |
| 📉 趋势下跌 | ⭐⭐☆☆☆ | BTC 保护可过滤部分下跌，但 1m 框架难以抵抗大趋势 |
| ⚡️ 极端波动 | ⭐⭐☆☆☆ | Pump 保护可减少追高，但参数众多需谨慎使用 |
| 🌙 低流动性时段 | ⭐⭐⭐⭐☆ | CTT 可过滤低流动性时段，减少虚假信号 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| max_open_trades | 3-5 | 根据资金量调整，避免同时持仓过多 |
| ROI 表 | 默认 | 已针对 1m 框架优化 |
| CTT 配置 | 9-23 UTC | 根据目标市场调整交易时段 |
| 自定义止损 | 默认 | 已针对中等波动市场优化 |

---

## 十、重要提醒：复杂性的代价

### 10.1 学习成本

该策略参数众多，需要深入理解每个指标的含义和相互作用。建议先从默认参数开始，逐步调整。

### 10.2 硬件要求

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 5-10 对 | 2 GB | 4 GB |
| 20-30 对 | 4 GB | 8 GB |
| 50+ 对 | 8 GB | 16 GB |

**注意**：1 分钟框架 + 多指标计算对 CPU 有一定要求，确保 VPS 性能足够。

### 10.3 回测与实盘的差异

- 1 分钟框架回测与实盘差异可能较大
- 多条件组合可能导致信号延迟
- CTT 时间窗口可能导致回测与实盘信号数量差异
- 建议先用小资金实盘测试验证

### 10.4 手动交易者建议

该策略不适合手动交易。8 个买入条件 + CTT 时间过滤 + 多层动态止盈止损，手动执行几乎不可能。

---

## 十一、总结

**ClucHAnix_BB_RPB_MOD_CTT** 是一个高度复杂的趋势跟踪策略，融合了多条件买入、动态止盈止损、市场环境过滤和 CTT 时间窗口交易等多种机制。它的核心价值在于：

1. **多条件覆盖**：8 个独立买入条件，覆盖超卖反弹、趋势延续、均值回归等多种形态
2. **智能止盈止损**：BB_RPB_TSL 机制根据盈利水平自动调整保护策略
3. **CTT 时间过滤**：通过时间窗口过滤，避免在不利的时段交易
4. **环境自适应**：BTC 保护、Pump 保护和 CTT 机制帮助避免不利市场环境

对于量化交易者而言，该策略适合有一定经验的交易者，需要投入时间理解每个参数的含义，并在实盘前进行充分回测和模拟交易。**不建议新手直接使用**。