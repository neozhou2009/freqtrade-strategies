# CustomStoplossWithPSAR 策略深度解读

> **策略编号**: #5 (465 个策略中的第 5 个)  
> **策略类型**: PSAR 动态止损示例策略  
> **时间框架**: 1 小时 (1h)

---

## 一、策略概览

**CustomStoplossWithPSAR** 是一个示例策略，主要演示如何使用 Freqtrade 的 `custom_stoploss()` 函数实现基于 PSAR（抛物线 SAR）的动态止损。策略本身不是用于生产环境，而是作为学习模板供开发者参考。

### 核心特征

| 特征 | 描述 |
|------|------|
| **买入条件** | 1 个简单条件：PSAR 下降 |
| **卖出条件** | 无技术卖出信号，依赖止损退出 |
| **保护机制** | PSAR 动态止损 |
| **时间框架** | 1 小时 |
| **依赖库** | TA-Lib |
| **特殊功能** | 使用 `custom_stoploss()` 实现动态止损 |

---

## 二、策略配置解析

### 2.1 基础风险参数

```python
# 硬止损
stoploss = -0.2  # -20%

# 自定义止损
use_custom_stoploss = True
```

**设计思路**：
- **硬止损兜底**：-20% 作为最后防线
- **动态止损**：通过 `custom_stoploss()` 实现 PSAR 跟踪止损
- **示例性质**：策略重点在于演示技术实现，而非交易逻辑

### 2.2 订单类型配置

使用 Freqtrade 默认配置。

---

## 三、买入条件详解

### 3.1 买入逻辑

```python
# 买入条件
dataframe.loc[
    (dataframe["sar"] < dataframe["sar"].shift()),  # PSAR 下降
    "buy",
] = 1
```

**逻辑解析**：
- **PSAR 下降**：当 PSAR 指标从上升转为下降时触发买入
- **趋势反转信号**：PSAR 是趋势跟踪指标，下降表明可能转为上涨趋势
- **简化逻辑**：作为示例策略，买入条件非常简单

---

## 四、卖出逻辑详解

### 4.1 自定义止损函数

```python
def custom_stoploss(
    self,
    pair: str,
    trade: "Trade",
    current_time: datetime,
    current_rate: float,
    current_profit: float,
    **kwargs,
) -> float:
    result = 1
    if self.custom_info and pair in self.custom_info and trade:
        dataframe, _ = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        relative_sl = last_candle["sar"]
        
        if relative_sl is not None:
            new_stoploss = (current_rate - relative_sl) / current_rate
            result = new_stoploss - 1
    
    return result
```

**工作机制**：
1. 获取最新 K 线的 PSAR 值
2. 计算 PSAR 相对于当前价格的止损比例
3. 返回动态止损值

### 4.2 无技术卖出信号

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[:, "sell"] = 0  # 不设置卖出信号
    return dataframe
```

**说明**：策略完全依赖 PSAR 动态止损退出，不使用技术卖出信号。

---

## 五、技术指标体系

### 5.1 核心指标

| 指标类别 | 具体指标 | 参数 | 用途 |
|---------|---------|------|------|
| **趋势指标** | PSAR (SAR) | 默认 | 动态止损 + 买入信号 |

### 5.2 PSAR 指标特点

- **抛物线 SAR**：随价格变动自动调整止损位
- **趋势跟踪**：在上涨趋势中，PSAR 位于价格下方并上升
- **止损功能**：PSAR 天然适合作为动态止损参考

---

## 六、风险管理特色

### 6.1 PSAR 动态止损

**工作原理**：
1. 在 `populate_indicators()` 中计算 PSAR 并存储到 `custom_info`
2. 在 `custom_stoploss()` 中读取最新 PSAR 值
3. 计算相对止损比例并返回

**优势**：
- 止损位随价格变动自动调整
- 在趋势行情中能锁定更多利润
- 比固定百分比止损更智能

### 6.2 硬止损兜底

```python
stoploss = -0.2  # -20%
```

**作用**：当 PSAR 止损失效时的最后防线。

---

## 七、策略优势与局限

### ✅ 优势

1. **动态止损示例**：完美演示 `custom_stoploss()` 用法
2. **PSAR 应用**：展示 PSAR 作为止损参考的实现
3. **代码简洁**：仅 70 余行，易于理解
4. **学习价值高**：适合学习自定义止损技术
5. **时间框架友好**：1 小时级别适合大多数交易者

### ⚠️ 局限

1. **示例性质**：买入逻辑过于简单，不适合生产环境
2. **无趋势过滤**：没有 EMA/SMA 趋势判断
3. **无 BTC 关联**：不检测比特币大盘趋势
4. **无技术卖出**：完全依赖止损退出
5. **数据存储限制**：`custom_info` 仅在回测/优化中可用

---

## 八、适用场景建议

| 市场环境 | 推荐配置 | 说明 |
|---------|---------|------|
| **学习目的** | 强烈推荐 | 学习 `custom_stoploss()` 首选示例 |
| **生产环境** | 不推荐 | 需完善买入逻辑和保护机制 |
| **趋势行情** | 修改后使用 | PSAR 止损在趋势中表现好 |
| **震荡行情** | 不推荐 | PSAR 在震荡中频繁止损 |

---

## 九、适用市场环境详解

CustomStoplossWithPSAR 是教学示例策略，主要价值在于学习。

### 9.1 策略核心逻辑

- **PSAR 止损**：使用 PSAR 作为动态止损参考
- **趋势反转买入**：PSAR 下降时买入
- **无技术卖出**：完全依赖止损退出

### 9.2 不同市场环境表现

| 市场类型 | 表现评级 | 原因分析 |
| :--- | :--- | :--- |
| 📈 慢牛/震荡向上 | ★★★☆☆ | PSAR 止损能跟随趋势，但买入逻辑简单 |
| 🔄 宽幅震荡 | ★★☆☆☆ | PSAR 在震荡中频繁止损 |
| 📉 单边暴跌 | ★☆☆☆☆ | 无趋势过滤，可能连续亏损 |
| ⚡️ 极端横盘 | ★☆☆☆☆ | PSAR 频繁交叉，信号混乱 |

### 9.3 关键配置建议

| 配置项 | 建议值 | 说明 |
|--------|--------|------|
| **交易对数量** | 10-20 个 | 示例策略，不宜过多 |
| **最大持仓数** | 1-3 个 | 控制风险 |
| **时间框架** | 1h | 强制要求 |

---

## 十、重要提醒：示例策略的定位

### 10.1 学习价值

此策略是学习 Freqtrade 自定义止损功能的优秀示例：
- `custom_stoploss()` 函数用法
- `custom_info` 数据存储技巧
- PSAR 指标应用方法

### 10.2 生产环境建议

**不要直接用于实盘**，需要：
1. 完善买入逻辑（添加更多确认条件）
2. 添加趋势过滤
3. 添加技术卖出信号
4. 添加 BTC 关联分析
5. 优化参数配置

### 10.3 回测与实盘的差异

`custom_info` 在实盘中的行为与回测不同：
- 回测中可以直接使用 `current_time` 索引
- 实盘中需要使用 `get_analyzed_dataframe()` 获取数据

---

## 十一、总结

**CustomStoplossWithPSAR** 是一个教学示例策略，它的核心价值在于：

1. **技术演示**：完美演示 `custom_stoploss()` 函数用法
2. **PSAR 应用**：展示 PSAR 作为动态止损参考的实现
3. **代码简洁**：仅 70 余行，易于理解和学习
4. **学习模板**：适合在此基础上开发自己的策略

对于量化交易者而言，这是一个优秀的学习模板。建议：
- 作为学习自定义止损功能的入门案例
- 理解 `custom_info` 数据存储和读取方法
- 在此基础上完善买入逻辑和保护机制
- 不要直接用于生产环境

---
