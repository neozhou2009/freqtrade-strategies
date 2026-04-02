# Cluc4 策略深度解读

> **策略编号**: #87 (第 9 批次第 7 个策略)  
> **策略类型**: 布林带 + ROCR 趋势过滤  
> **时间框架**: 1 分钟 (1m)

---

## 一、策略概览

**Cluc4** 是一个基于布林带和 ROCR（变化率）指标的短周期交易策略。策略核心特点是使用 1 小时周期的 ROCR 指标进行趋势过滤，同时结合双重布林带系统（40 周期和 20 周期）来捕捉短期交易机会。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 2 种模式（BinHV 变体 + Cluc 变体） |
| **卖出条件** | 价格突破布林带中轨 |
| **保护机制** | ROCR 趋势过滤 + 硬止损 |
| **时间框架** | 1 分钟（主）+ 1 小时（信息周期） |
| **依赖库** | TA-Lib, technical, qtpylib, numpy |
| **特殊功能** | 多时间框架分析、双重布林带系统 |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# ROI 退出表
minimal_roi = {
    "0": 0.015,    # 立即退出：1.5% 利润
    "20": 0.005,   # 20 分钟后：0.5% 利润
    "30": 0.001,   # 30 分钟后：0.1% 利润
}

# 止损设置
stoploss = -0.01  # -1% 硬止损

# 追踪止损配置
trailing_stop = False  # 未启用

# 退出信号配置
use_exit_signal = True
exit_profit_only = True
ignore_roi_if_entry_signal = True
```

**设计思路**：
- **多级 ROI**：3 级递减 ROI，持仓时间越长退出门槛越低
- **紧凑止损**：-1% 硬止损，相对紧凑
- **仅退出信号**：exit_profit_only = True，只在盈利时退出

### 2.2 时间框架配置

```python
timeframe = '1m'  # 主时间框架：1 分钟

# 信息时间框架
def informative_pairs(self):
    pairs = self.dp.current_whitelist()
    informative_pairs = [(pair, '1h') for pair in pairs]
    return informative_pairs
```

**说明**：
- 主时间框架：1 分钟（短期交易）
- 信息时间框架：1 小时（趋势过滤）

---

## 三、买入条件详解

### 3.1 ROCR 趋势过滤

```python
# 1 小时周期的 ROCR 过滤
dataframe['rocr_1h'].gt(0.65)
```

**含义**：1 小时周期的 ROCR（168 周期）大于 0.65，表示 1 小时级别处于上升趋势中。

### 3.2 买入条件 - 模式 1（BinHV 变体）

```python
(
    dataframe['lower'].shift().gt(0) &
    dataframe['bbdelta'].gt(dataframe['close'] * 0.006) &
    dataframe['closedelta'].gt(dataframe['close'] * 0.013) &
    dataframe['tail'].lt(dataframe['bbdelta'] * 0.968) &
    dataframe['close'].lt(dataframe['lower'].shift()) &
    dataframe['close'].le(dataframe['close'].shift())
)
```

**逻辑解析**：
- `lower.shift() > 0`：布林带下轨有效（非 NaN）
- `bbdelta > close * 0.006`：布林带带宽 > 0.6%
- `closedelta > close * 0.013`：价格变化 > 1.3%
- `tail < bbdelta * 0.968`：下影线 < 带宽的 96.8%
- `close < lower.shift()`：价格 < 前一根布林带下轨
- `close <= close.shift()`：价格不高于前一根收盘价

### 3.3 买入条件 - 模式 2（Cluc 变体）

```python
(
    (dataframe['close'] < dataframe['ema_slow']) &
    (dataframe['close'] < 0.013 * dataframe['bb_lowerband']) &
    (dataframe['volume'] < (dataframe['volume_mean_slow'].shift(1) * 28))
)
```

**逻辑解析**：
- `close < ema_slow`：价格 < EMA50（趋势偏弱）
- `close < 0.013 * bb_lowerband`：价格 < 布林带下轨 × 0.013（极低价格）
- `volume < volume_mean_slow.shift(1) * 28`：成交量 < 30 日均量 × 28（地量）

### 3.4 综合买入逻辑

```python
dataframe.loc[
    (
        dataframe['rocr_1h'].gt(0.65)  # 1小时趋势过滤
    ) &
    (
        # 模式1 或 模式2
        (模式1条件) | (模式2条件)
    ),
    'buy'
] = 1
```

**关键要点**：
- 必须满足 1 小时 ROCR > 0.65（趋势过滤）
- 满足两种买入模式之一即可入场

---

## 四、卖出逻辑详解

### 4.1 卖出条件

```python
(
    (qtpylib.crossed_above(dataframe['close'], dataframe['bb_middleband'])) &
    (dataframe['volume'] > 0)
)
```

**逻辑解析**：
- `crossed_above(close, bb_middleband)`：价格上穿布林带中轨
- `volume > 0`：有成交量确认

**综合含义**：价格突破布林带中轨且有成交量确认时卖出。

### 4.2 ROI 退出机制

策略使用三级 ROI 退出：

| 时间 | 最小利润 |
|------|---------|
| 0 分钟 | 1.5% |
| 20 分钟 | 0.5% |
| 30 分钟 | 0.1% |

### 4.3 退出信号配置

```python
use_exit_signal = True       # 启用退出信号
exit_profit_only = True      # 仅在盈利时退出
ignore_roi_if_entry_signal = True  # 忽略 ROI 如果有新的入场信号
```

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 参数 | 用途 |
|---------|---------|------|------|
| **波动指标** | Bollinger Bands | 40 周期，2 倍标准差 | BinHV 变体 |
| **波动指标** | Bollinger Bands | 20 周期，2 倍标准差 | Cluc 变体 |
| **趋势指标** | EMA | 50 周期 | 价格趋势判断 |
| **动量指标** | ROCR | 28 周期（1m）/ 168 周期（1h） | 趋势过滤 |
| **成交量** | Volume MA | 30 周期 | 成交量过滤 |

### 5.2 自定义布林带函数

```python
def bollinger_bands(stock_price, window_size, num_of_std):
    rolling_mean = stock_price.rolling(window=window_size).mean()
    rolling_std = stock_price.rolling(window=window_size).std()
    lower_band = rolling_mean - (rolling_std * num_of_std)
    return np.nan_to_num(rolling_mean), np.nan_to_num(lower_band)
```

**说明**：自定义 40 周期布林带计算，用于 BinHV 变体。

### 5.3 多时间框架分析

策略使用 1 小时周期的 ROCR 指标进行趋势过滤：

```python
# 1 分钟周期的 ROCR
dataframe['rocr'] = ta.ROCR(dataframe, timeperiod=28)

# 1 小时周期的 ROCR
inf_tf = '1h'
informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=inf_tf)
informative['rocr'] = ta.ROCR(informative, timeperiod=168)
dataframe = merge_informative_pair(dataframe, informative, self.timeframe, inf_tf, ffill=True)
```

---

## 六、风险管理特色

### 6.1 紧凑止损

```python
stoploss = -0.01  # -1%
```

**说明**：-1% 紧凑止损，适合短期交易。

### 6.2 ROCR 趋势过滤

```python
dataframe['rocr_1h'].gt(0.65)
```

**作用**：
- 仅在 1 小时上升趋势中买入
- 避免逆势交易
- 减少假信号

### 6.3 ROI 退出机制

| 时间 | 最小利润 |
|------|---------|
| 0 分钟 | 1.5% |
| 20 分钟 | 0.5% |
| 30 分钟 | 0.1% |

**策略**：快速积累小利润，适合高频交易。

---

## 七、策略优势与局限

### ✅ 优势

1. **ROCR 趋势过滤**：使用 1 小时 ROCR 过滤，避免逆势交易
2. **双重布林带**：40 周期 + 20 周期，覆盖不同时间维度
3. **紧凑止损**：-1% 止损，控制单笔亏损
4. **快速退出**：1.5% 起步 ROI，快速积累利润
5. **多时间框架**：结合 1 分钟和 1 小时分析

### ⚠️ 局限

1. **复杂度中等**：双重布林带 + 多时间框架，调试需要经验
2. **参数敏感**：ROCR 阈值 0.65 可能需要根据市场调整
3. **交易频率高**：1 分钟时间框架可能导致过度交易
4. **趋势依赖**：ROCR 过滤可能错过趋势启动机会
5. **信息时间框架延迟**：1 小时 ROCR 可能滞后

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **震荡市** | 调整 ROCR 阈值 | 降低 ROCR 阈值增加信号 |
| **上涨趋势** | 默认配置 | ROCR 过滤效果好 |
| **下跌趋势** | 暂停交易 | ROCR 过滤可能失效 |
| **高波动** | 调整止损 | 1% 止损可能过紧 |
| **低波动** | 调整 ROI | 可能需要降低 ROI 门槛 |

---

## 九、适用市场环境详解

Cluc4 是基于"布林带 + ROCR 趋势过滤"核心哲学的策略。

### 9.1 策略核心逻辑

- **ROCR 趋势过滤**：1 小时 ROCR > 0.65，确保趋势向上
- **双重布林带**：40 周期 + 20 周期，覆盖不同时间维度
- **价格突破**：价格突破布林带中轨时卖出

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 上涨趋势 | ★★★★☆ | ROCR 过滤有效，顺势交易 |
| 🔄 宽幅震荡 | ★★★☆☆ | 布林带信号频繁，可能过度交易 |
| 📉 下跌趋势 | ★★☆☆☆ | ROCR 过滤可能失效 |
| ⚡️ 快速波动 | ★★★★☆ | 1 分钟框架反应灵敏 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| **交易对数量** | 10-20 个 | 信号频率较高 |
| **最大持仓数** | 2-4 个 | 控制风险 |
| **仓位模式** | 固定仓位 | 建议固定仓位 |
| **时间框架** | 1m | 强制要求 |

---

## 十、重要提醒：复杂性的代价

### 10.1 学习成本中等

策略代码约 80 行，需要理解：
- 布林带计算
- ROCR 指标原理
- 多时间框架分析

### 10.2 硬件要求较低

单时间框架计算量较小：

| 交易对数量 | 最低内存 | 推荐内存 |
|-----------|---------|---------|
| 10-20 对 | 512MB | 1GB |
| 20-40 对 | 1GB | 2GB |

### 10.3 多时间框架注意事项

策略使用 1 小时信息时间框架：
- 需要获取历史 1 小时数据
- 数据延迟可能影响信号准确性
- 实盘时需要稳定的数据源

### 10.4 手动交易者建议

手动交易者可参考此策略的思路：
- 同时观察 1 分钟和 1 小时图表
- 使用 ROCR 确认趋势方向
- 设置 1.5% 止盈和 1% 止损

---

## 十一、总结

**Cluc4** 是一个设计精巧的布林带 + ROCR 趋势过滤策略，它的核心价值在于：

1. **ROCR 趋势过滤**：1 小时 ROCR > 0.65，确保顺势交易
2. **双重布林带**：40 周期 + 20 周期，覆盖不同时间维度
3. **紧凑止损**：-1% 止损，控制单笔亏损
4. **快速退出**：1.5% 起步 ROI，适合高频交易
5. **多时间框架**：结合 1 分钟和 1 小时分析

对于量化交易者而言，这是一个优秀的布林带 + 趋势过滤策略模板。建议：
- 作为学习多时间框架分析的入门案例
- 理解 ROCR 指标的应用方法
- 注意交易频率可能较高，需要合理配置
- 实盘前需充分测试，关注滑点和手续费

---