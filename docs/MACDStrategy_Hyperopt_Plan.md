# MACDStrategy Hyperopt 优化方案

> 制定时间: 2026-04-20
> 策略类型: 趋势跟踪
> 数据范围: 2022-12-15 至 2026-04-18 (约3.5年)

---

## 一、策略分析

### 1.1 策略逻辑

| 条件 | 入场信号 | 出场信号 |
|------|---------|---------|
| MACD | MACD > MACD Signal | MACD < MACD Signal |
| CCI | CCI <= buy_cci | CCI >= sell_cci |
| Volume | > 0 | > 0 |

**核心思想**: MACD判断趋势方向，CCI判断超买超卖程度

### 1.2 可优化参数

| 参数 | 范围 | 默认值 | 当前值 | 说明 |
|------|------|--------|--------|------|
| `buy_cci` | -700 ~ 0 | -50 | -48 | 入场时CCI阈值（越负越激进） |
| `sell_cci` | 0 ~ 700 | 100 | 687 | 出场时CCI阈值（越大越保守） |

### 1.3 固定参数

| 参数 | 值 | 说明 |
|------|-----|------|
| `stoploss` | -0.3 | 固定止损30% |
| `timeframe` | 5m | 5分钟周期 |
| `minimal_roi` | {"0":0.05, "20":0.04, "30":0.03, "60":0.01} | ROI阶梯 |

---

## 二、数据与市场环境

### 2.1 数据覆盖

| 年份 | 交易日 | 牛市天数 | 熊市天数 | 年度涨跌 |
|------|--------|---------|---------|---------|
| 2023 | 365 | 154 (42%) | 211 (58%) | +154.7% |
| 2024 | 366 | 327 (89%) | 39 (11%) | +111.5% |
| 2025 | 365 | 265 (73%) | 100 (27%) | -7.4% |
| 2026 | 108 | 0 (0%) | 108 (100%) | -14.8% |

### 2.2 市场周期划分

| 周期 | 类型 | 时间范围 | 天数 |
|------|------|---------|------|
| 周期1 | 熊市 | 2022-12-15 ~ 2023-07-02 | 199天 |
| 周期2 | 牛市 | 2023-07-02 ~ 2024-07-04 | ~280天 |
| 周期3 | 牛市 | 2024-07-13 ~ 2025-02-26 | 162天 |
| 周期4 | 牛市 | 2025-04-19 ~ 2025-10-17 | 181天 |
| 周期5 | 熊市 | 2025-11-03 ~ 至今 | 166天+ |

---

## 三、优化方案设计

### 3.1 方案选择：分市场环境优化

**推荐方案**: 分别优化牛市参数和熊市参数

**原因**:
- 趋势跟踪策略在不同市场表现差异大
- 2023-2024牛市数据充足（约600天）
- 2025年底-2026熊市数据充足（约200天）
- 单一参数难以适应两种市场

### 3.2 数据集划分

| 数据集 | 时间范围 | 市场类型 | 用途 |
|--------|---------|---------|------|
| **训练集A** | 2023-07-01 ~ 2024-06-30 | 牛市 | 优化牛市参数 |
| **训练集B** | 2025-11-01 ~ 2026-03-31 | 熊市 | 优化熊市参数 |
| **测试集A** | 2024-07-01 ~ 2024-12-31 | 牛市延续 | 验证牛市参数 |
| **测试集B** | 2026-04-01 ~ 2026-04-18 | 熊市延续 | 验证熊市参数 |

### 3.3 优化参数配置

#### 牛市参数优化

```bash
# 训练
freqtrade hyperopt --strategy MACDStrategy \
    --hyperopt-loss SharpeHyperOptLoss \
    --spaces buy sell \
    --timerange 20230701-20240630 \
    --epochs 100 \
    --jobs 4

# 验证
freqtrade backtesting --strategy MACDStrategy \
    --timerange 20240701-20241231
```

#### 熊市参数优化

```bash
# 训练
freqtrade hyperopt --strategy MACDStrategy \
    --hyperopt-loss SharpeHyperOptLoss \
    --spaces buy sell \
    --timerange 20251101-20260331 \
    --epochs 100 \
    --jobs 4

# 验证
freqtrade backtesting --strategy MACDStrategy \
    --timerange 20260401-20260418
```

### 3.4 损失函数选择

| 损失函数 | 适用场景 | 权重建议 |
|---------|---------|---------|
| `SharpeHyperOptLoss` | 通用，平衡收益和风险 | 默认 |
| `WinRatioLoss` | 提高胜率 | 牛市优先 |
| `ProfitDrawDownHyperOptLoss` | 控制回撤 | 熊市优先 |
| `CalmarHyperOptLoss` | 收益/回撤比 | 长期稳定 |

**建议**:
- 牛市: `SharpeHyperOptLoss` + `WinRatioLoss` 组合
- 熊市: `ProfitDrawDownHyperOptLoss` 或 `CalmarHyperOptLoss`

---

## 四、参数稳定性验证

### 4.1 多周期交叉验证

| 验证方法 | 说明 |
|---------|------|
| **Walk-forward** | 滚动训练验证，每3个月训练，下月验证 |
| **参数稳定性** | 多次hyperopt，检查最佳参数是否一致 |
| **过拟合检测** | 训练集表现 vs 测试集表现差异 |

### 4.2 过拟合判断标准

| 指标 | 过拟合阈值 | 健康阈值 |
|------|----------|---------|
| 训练ROI vs 测试ROI | >50%差距 | <20%差距 |
| 训练Sharpe vs 测试Sharpe | >1.0差距 | <0.3差距 |
| Win Rate变化 | >15%下降 | <5%变化 |

---

## 五、预期结果与固化策略

### 5.1 牛市参数预期

| 参数 | 预期范围 | 逻辑 |
|------|---------|------|
| `buy_cci` | -100 ~ -300 | 牛市CCI波动大，阈值可放宽 |
| `sell_cci` | 200 ~ 400 | 及时止盈，避免回调损失 |

### 5.2 熊市参数预期

| 参数 | 预期范围 | 逻辑 |
|------|---------|------|
| `buy_cci` | -50 ~ -100 | 熊市入场需更谨慎 |
| `sell_cci` | 500 ~ 700 | 等待更明确的出场信号 |

### 5.3 策略固化方案

优化完成后，采用**市场环境自适应**方案：

```python
class MACDStrategy(IStrategy):
    # 牛市参数
    bull_params = {
        "buy_cci": -200,  # 待优化确定
        "sell_cci": 300,
    }
    
    # 熊市参数  
    bear_params = {
        "buy_cci": -50,
        "sell_cci": 600,
    }
    
    def populate_entry_trend(self, dataframe, metadata):
        # 根据市场环境选择参数
        market_state = self.detect_market(dataframe)
        if market_state == "bull":
            cci_threshold = self.bull_params["buy_cci"]
        else:
            cci_threshold = self.bear_params["buy_cci"]
        ...
```

---

## 六、执行计划

| 步骤 | 任务 | 预估时间 |
|------|------|---------|
| 1 | 牛市参数hyperopt (100 epochs) | ~30分钟 |
| 2 | 牛市参数验证backtest | ~5分钟 |
| 3 | 熊市参数hyperopt (100 epochs) | ~20分钟 |
| 4 | 熊市参数验证backtest | ~3分钟 |
| 5 | 参数稳定性交叉验证 | ~15分钟 |
| 6 | 固化策略代码修改 | ~10分钟 |
| 7 | 最终全周期验证 | ~10分钟 |

**总预估时间**: 约1.5小时

---

## 七、风险评估

| 风险 | 说明 | 缓解措施 |
|------|------|---------|
| 过拟合 | 参数只对训练集有效 | 多周期验证 |
| 市场变化 | 未来市场不同于历史 | 持续监控，定期重优化 |
| 参数极端 | hyperopt可能找到极端值 | 人工审核参数合理性 |
| 策略本身局限 | MACD+CCI组合简单 | 考虑添加其他指标 |

---

## 八、附录：完整执行命令

```bash
# ===== 牛市优化 =====
# Step 1: 训练
docker run --rm -v "$(pwd)/user_data:/freqtrade/user_data" \
    neozhou2009/freqtrade-full:latest hyperopt \
    --strategy MACDStrategy \
    --hyperopt-loss SharpeHyperOptLoss \
    --spaces buy sell \
    --timerange 20230701-20240630 \
    --epochs 100 --jobs 4

# Step 2: 验证
docker run --rm -v "$(pwd)/user_data:/freqtrade/user_data" \
    neozhou2009/freqtrade-full:latest backtesting \
    --strategy MACDStrategy \
    --timerange 20240701-20241231

# ===== 熊市优化 =====
# Step 3: 训练
docker run --rm -v "$(pwd)/user_data:/freqtrade/user_data" \
    neozhou2009/freqtrade-full:latest hyperopt \
    --strategy MACDStrategy \
    --hyperopt-loss ProfitDrawDownHyperOptLoss \
    --spaces buy sell \
    --timerange 20251101-20260331 \
    --epochs 100 --jobs 4

# Step 4: 验证
docker run --rm -v "$(pwd)/user_data:/freqtrade/user_data" \
    neozhou2009/freqtrade-full:latest backtesting \
    --strategy MACDStrategy \
    --timerange 20260401-20260418

# ===== 全周期最终验证 =====
docker run --rm -v "$(pwd)/user_data:/freqtrade/user_data" \
    neozhou2009/freqtrade-full:latest backtesting \
    --strategy MACDStrategy \
    --timerange 20230101-20260418
```

---

*方案制定完成，待执行*