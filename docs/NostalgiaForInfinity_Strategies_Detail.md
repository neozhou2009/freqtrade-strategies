# NostalgiaForInfinity 系列策略详细说明

本文档详细列出了所有 47 个 NostalgiaForInfinity (NFI) 系列策略的用途及详细信息。

---

## 概览

NostalgiaForInfinity 是由 iterativ 开发的 Freqtrade 策略系列，专注于加密货币量化交易。所有策略均基于 5 分钟时间周期（部分 Next 系列为 15 分钟），采用多技术指标组合进行进出场判断。

---

## 一、主版本系列 (V1-V7) - 14个

基础版本系列，逐步迭代优化核心逻辑。

| 策略名 | 基础版本 | 时间周期 | 止损 | ROI | 特点说明 |
|--------|----------|----------|------|-----|----------|
| **NostalgiaForInfinityV1** | V1 | 5m | -0.36 | 25% | 初代版本，建立基础策略框架，使用 SSL Channels 指标 |
| **NostalgiaForInfinityV2** | V2 | 5m | -0.10 | 10%/5%/2% | 增加 Hyper 参数优化功能，阶梯式 ROI |
| **NostalgiaForInfinityV3** | V3 | 5m | -0.99 | 10%/5%/2% | 几乎禁用止损，依赖信号出场，增强 Trailing Stop |
| **NostalgiaForInfinityV4** | V4 | 5m | -0.10 | 10%/5%/2% | 增加更多买入条件，扩展支持 40-80 交易对 |
| **NostalgiaForInfinityV4HO** | V4 HO | 5m | -0.10 | 10%/5%/2% | V4 的 Hyper-Optimized 超优化版本 |
| **NostalgiaForInfinityV5** | V5 | 5m | -0.10 | 10%/5%/2% | 增强卖出逻辑，优化 Trailing 参数配置 |
| **NostalgiaForInfinityV5MultiOffsetAndHO** | V5+MOHO | 5m | - | 10%/5%/2% | V5 + MultiOffsetLambo + 超优化参数，17 个买入条件可配置 |
| **NostalgiaForInfinityV5MultiOffsetAndHO2** | V5+MOHO2 | 5m | - | 10%/5%/2% | MOHO 的第二个变体版本，参数微调 |
| **NostalgiaForInfinityV6** | V6 | 5m | -0.10 | 10%/5%/2% | 增加更多技术指标组合，优化进出场逻辑 |
| **NostalgiaForInfinityV6HO** | V6 HO | 5m | -0.10 | 10%/5%/2% | V6 的 Hyper-Optimized 超优化版本 |
| **NostalgiaForInfinityV7** | V7 | 5m | -0.10 | 10%/5%/2% | 增加 zema 指标，增强进出场信号判断 |
| **NostalgiaForInfinityV7_7_2** | V8 衍生 | 5m | -0.10 | 10%/5%/2% | 增加 pandas_ta 支持，增强 Hold 持仓功能 |
| **NostalgiaForInfinityV7_SMA** | V7 SMA | 5m | -0.10 | 10%/5%/2% | V7 + SMA 均线过滤，增强趋势判断 |
| **NostalgiaForInfinityV7_SMAv2** | V7 SMAv2 | 5m | -0.10 | 10%/5%/2% | SMA 版本的优化迭代，参数微调 |
| **NostalgiaForInfinityV7_SMAv2_1** | V7 SMAv2_1 | 5m | -0.10 | 10%/5%/2% | SMA 第二版本的进一步微调版本 |

---

## 二、X 系列 - 3个

旗舰版本系列，支持多时间框架分析。

| 策略名 | 时间周期 | BTC 信息框架 | 特点说明 |
|--------|----------|--------------|----------|
| **NostalgiaForInfinityX** | 5m | 5m/15m/1h/4h/1d | 旗舰版本，支持多时间框架 BTC 信息分析，增加 RMI/ichimoku 指标，增强 Hold 支持 |
| **NostalgiaForInfinityX2** | 5m | 5m/15m/1h/4h/1d | X 的精简版本，同样支持多时间框架和 BTC 信息，增加交易所推荐链接 |
| **NostalgiaForInfinityXw** | 5m | - | X 的扩展版本，增加 PMAX 指标支持，多种 MA 类型可选 (EMA/DEMA/T3/SMA/VIDYA/TEMA/WMA/VWMA/zema) |

---

## 三、Next 系列 - 7个

下一代版本系列，采用更新的架构设计。

| 策略名 | 基础版本 | 时间周期 | 特点说明 |
|--------|----------|----------|----------|
| **NostalgiaForInfinityNext** | V7.3.1 BUSD | 5m | Next 基础版本，增加 pandas_ta 和 ichimoku 支持，BUSD 专用优化 |
| **NostalgiaForInfinityNextGen** | V9 | 15m | 下一代版本，采用 15 分钟周期，增强 Hold 支持功能 |
| **NostalgiaForInfinityNextGen_TSL** | V9 | 15m | NextGen + Trailing Stop Loss 增强版，优化止损追踪逻辑 |
| **NostalgiaForInfinityNextV7155** | V8 | 5m | Next 系列 V8 版本，特定优化参数配置 |
| **NostalgiaForInfinityNext_ChangeToTower_V5_2** | V8 | 5m | Tower 策略变体版本 5.2，修改核心逻辑 |
| **NostalgiaForInfinityNext_ChangeToTower_V5_3** | V8 | 5m | Tower 策略变体版本 5.3，进一步优化 |
| **NostalgiaForInfinityNext_ChangeToTower_V6** | V8 | 5m | Tower 策略变体版本 6，增加 buy_tag 追踪功能 |
| **NostalgiaForInfinityNext_maximizer** | V8 | 5m | 利润最大化版本，增加 JSON 输出功能，优化利润提取逻辑 |

---

## 四、NFI 缩写变体系列 - 21个

基于各主版本的缩写命名变体，包含多种优化方向。

### 4.1 基于V4的NFI46系列

| 策略名 | 时间周期 | ROI | 止损 | 特点说明 |
|--------|----------|-----|------|----------|
| **NFI46** | 5m | 10%/5%/2% | -0.10 | V4 基础变体，优化 Trailing Stop 参数 |
| **NFI46Frog** | 5m | 10%/5%/2% | -0.10 | 增加 finta 库支持，增强 TTLCache 缓存机制 |
| **NFI46FrogZ** | 5m | 2.8%/1.8%/0.5% | -0.10 | Frog 的激进版本，采用更低的 ROI 目标追求快速出场 |
| **NFI46Offset** | 5m | 1.3% | -0.10 | MultiOffset 版本，多种均线偏移参数可优化 (SMA/EMA/TRIMA/T3/KAMA) |
| **NFI46OffsetHOA1** | 5m | 1.3% | -0.10 | Offset 的 Hyper 优化版本 A1，参数超优化 |
| **NFI46Z** | 5m | 2.8%/1.8%/0.5% | -0.10 | 自定义止损功能，激进 ROI 目标，启用 use_custom_stoploss |
| **NFI47V2** | 5m | 10%/5%/2% | -0.10 | V4 的 V2 迭代版本，增加 zema 指标支持 |

### 4.2 基于V4的其他变体

| 策略名 | 时间周期 | ROI | 止损 | 特点说明 |
|--------|----------|-----|------|----------|
| **NFI4Frog** | 5m | 10%/5%/2% | -0.10 | 基于V4，增加 finta 库和 TTLCache 缓存支持 |

### 4.3 基于V5的MOHO系列

| 策略名 | 时间周期 | 特点说明 |
|--------|----------|----------|
| **NFI5MOHO** | 5m | V5 + MultiOffset + Hyper 优化，17 个买入条件全部可配置，exit 使用 market 订单 |
| **NFI5MOHO2** | 5m | MOHO 第二版本，参数微调优化 |
| **NFI5MOHO_WIP** | 5m | Work In Progress 开发版本，实验性功能 |
| **NFI5MOHO_WIP_1** | 5m | WIP 迭代版本 1 |
| **NFI5MOHO_WIP_2** | 5m | WIP 迭代版本 2 |

### 4.4 Next的MOHO系列

| 策略名 | 时间周期 | 特点说明 |
|--------|----------|----------|
| **NFINextMOHO** | 5m | Next + MultiOffset + Hyper 优化组合 |
| **NFINextMOHO2** | 5m | NextMOHO 第二版本 |
| **NFINextMultiOffsetAndHO** | 5m | Next + MultiOffset 完整版 |
| **NFINextMultiOffsetAndHO2** | 5m | MultiOffset 第二版本 |

### 4.5 其他MOHO变体

| 策略名 | 时间周期 | 特点说明 |
|--------|----------|----------|
| **NFI7MOHO** | 5m | V7 + MultiOffset + Hyper 优化组合 |

### 4.6 特殊变体

| 策略名 | 时间周期 | 特点说明 |
|--------|----------|----------|
| **NFI731_BUSD** | 5m | BUSD 专用版本，特定参数优化配置 |
| **NFIX_BB_RPB** | 5m | X 系列 + Bollinger Band + RPB (Relative Price Band) 指标组合 |
| **NFIX_BB_RPB_c7c477d_20211030** | 5m | BB_RPB 的特定 commit 版本 (c7c477d)，2021年10月30日版本 |

---

## 五、其他相关策略

社区衍生和组合版本。

| 策略名 | 时间周期 | 特点说明 |
|--------|----------|----------|
| **Nostalgia** | 5m | 基础 Nostalgia 策略，可能为早期版本或简化版本 |
| **NfiNextModded** | 5m | Next 的 Modded 修改版本，社区自定义调整 |
| **Combined_NFIv6_SMA** | 5m | V6 + SMA 均线组合策略 |
| **Combined_NFIv7_SMA** | 5m | V7 + SMA 均线组合策略 |
| **Combined_NFIv7_SMA_bAdBoY_20211204** | 5m | 用户 bAdBoY 于 2021年12月4日提交的特定版本 |
| **Combined_NFIv7_SMA_Rallipanos_20210707** | 5m | 用户 Rallipanos 于 2021年7月7日提交的特定版本 |
| **BigZ07Next** | 5m | BigZ07 + Next 组合策略 |
| **BigZ07Next2** | 5m | BigZ07Next 第二版本 |

---

## 六、共通特性总结

所有 NFI 系列策略的通用配置建议：

### 运行配置

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| **推荐交易对数** | 40-80 对 | Volume pairlist 效果最佳 |
| **推荐同时持仓** | 4-6 个 | 无限 stake 模式 |
| **推荐币种** | 稳定币对 (USDT/BUSDT/USDC) | 避免 BTC/ETH 对，减少波动影响 |
| **必须排除** | 杠杆代币 (*BULL, *BEAR, *UP, *DOWN) | 高风险波动品种 |

### 风控参数

| 参数 | 范围 | 说明 |
|--------|------|------|
| **止损范围** | -0.10 到 -0.36 | V3 版本接近禁用 (-0.99) |
| **Trailing Stop** | 0.01-0.05 | 触发后追踪止损比例 |
| **Trailing Offset** | 0.025-0.30 | Trailing 触发阈值 |
| **启动K线数** | 400 根 | 策略启动所需最小历史数据 |

### 技术指标依赖

| 指标类型 | 具体指标 |
|----------|----------|
| **趋势指标** | EMA, SMA, DEMA, T3, TEMA, VIDYA, WMA, VWMA, zema, KAMA |
| **波动指标** | ATR, Bollinger Band |
| **动量指标** | RMI, RSI |
| **通道指标** | SSL Channels |
| **组合指标** | Ichimoku, PMAX |
| **辅助指标** | EWO (Elliott Wave Oscillator), VWAP |

### 外部库依赖

| 库名 | 用途 | 使用策略 |
|------|------|----------|
| **pandas_ta** | 技术分析扩展 | V7_7_2, X系列, Next系列 |
| **technical** | Freqtrade 技术库 | 所有策略 |
| **finta** | 金融技术分析 | Frog系列 |
| **cachetools** | 缓存机制 | Frog系列 |
| **skopt** | 参数优化 | Frog系列 |

---

## 七、推荐使用顺序

根据用户水平推荐策略选择：

### 新手入门路径
```
V4 → V5 → V7
```
基础版本，逻辑清晰，参数较少，适合学习策略框架。

### 进阶用户路径
```
V7_SMA → X → X2
```
增加均线过滤和多时间框架分析，提升策略稳定性。

### 高级用户路径
```
NextGen → NFI5MOHO → NFI46Offset
```
采用 MOHO 多偏移优化，支持大量参数调优，需要深入理解策略逻辑。

### 实验性版本
```
NFI5MOHO_WIP系列 / ChangeToTower系列 / maximizer
```
实验性功能，需要充分回测验证，不建议直接实盘使用。

---

## 八、版本演进关系图

```
V1 (基础框架)
  │
  ├── V2 (增加Hyper参数)
  │     │
  │     └── V3 (增强Trailing)
  │
  ├── V4 (扩展买入条件)
  │     │
  │     ├── V4HO (超优化版)
  │     ├── NFI46系列 (缩写变体)
  │     │     ├── NFI46Frog (+finta)
  │     │     ├── NFI46Offset (+MultiOffset)
  │     │     └── NFI46Z (+自定义止损)
  │     └── NFI4Frog
  │
  ├── V5 (增强卖出逻辑)
  │     │
  │     ├── V5MOHO系列 (+MultiOffset+HO)
  │     ├── NFI5MOHO系列
  │
  ├── V6 (增加技术指标)
  │     │
  │     ├── V6HO (超优化版)
  │     └── Combined_NFIv6_SMA
  │
  ├── V7 (增加zema)
  │     │
  │     ├── V7HO
  │     ├── V7_7_2 (+pandas_ta)
  │     ├── V7_SMA系列 (+SMA过滤)
  │     ├── NFI7MOHO
  │     └── Combined_NFIv7_SMA系列
  │
  ├── X系列 (旗舰版，多时间框架)
  │     ├── X (+BTC信息)
  │     ├── X2 (精简版)
  │     ├── Xw (+PMAX)
  │     └── NFIX_BB_RPB系列
  │
  └── Next系列 (下一代)
        ├── Next (V7.3.1 BUSD)
        ├── NextGen (V9, 15m)
        ├── NextV7155 (V8)
        ├── Next_ChangeToTower系列
        ├── Next_maximizer
        └── NFINextMOHO系列
```

---

## 九、注意事项

1. **必须使用正确的配置文件参数**：
   - `use_exit_signal: true`
   - `exit_profit_only: false`
   - `ignore_roi_if_entry_signal: true`

2. **时间周期不可覆盖**：
   - 大多数策略必须使用 5m 时间周期
   - NextGen 系列必须使用 15m 时间周期

3. **Hold 支持功能**：
   - 通过 `hold-trades.json` 或 `nfi-hold-trades.json` 配置特定交易持有
   - 可设置特定交易对的最低盈利出场比例

4. **回测建议**：
   - 建议至少 400 根 K 纨启动数据
   - MOHO 系列需要大量参数调优，建议 Hyperopt 优化后再使用

---

## 十、参考链接

- **官方策略仓库**: https://github.com/iterativv/NostalgiaForInfinity
- **Freqtrade 官方文档**: https://github.com/freqtrade/freqtrade
- **技术分析库**: https://github.com/twopirllc/pandas-ta

---

*文档生成日期: 2026-04-15*