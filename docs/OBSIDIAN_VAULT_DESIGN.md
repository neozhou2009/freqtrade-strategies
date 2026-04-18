# Freqtrade Strategies Vault 设计方案

## 目录结构

```
freqtrade-vault/
│
├── 📁 00_Index/                    # 入口导航
│   ├── Start Here.md              # 新用户入门指南
│   ├── MOC-Strategies.md          # 策略总览地图 (Map of Content)
│   ├── MOC-Indicators.md          # 指标知识地图
│   ├── MOC-Pipeline.md            # 评估管道地图
│   └── Quick-Reference.md         # 常用查询速查表
│
├── 📁 01_Strategies/              # 策略核心卡片
│   ├── 📁 Family-Nostalgia/       # 按家族分类
│   │   ├── NostalgiaForInfinityV5.md
│   │   ├── NostalgiaForInfinityV7.md
│   │   └── NFI-Family-Overview.md  # 家族总览
│   │
│   ├── 📁 Family-BinHV/
│   │   ├── BinHV45.md
│   │   ├── BinHV45HO.md
│   │   └── BinHV-Family-Overview.md
│   │
│   ├── 📁 Family-ClucHAnix/
│   ├── 📁 Family-Elliot/
│   ├── 📁 Family-CombinedBinH/
│   ├── 📁 Family-MACD/
│   ├── 📁 Family-BBRSI/
│   ├── 📁 Family-Ichimoku/
│   │
│   └── Strategy-Cards-by-Grade.md # 按等级索引：S/A/B/C/D
│
├── 📁 02_Indicators/              # 指标知识库
│   ├── RSI.md                     # 单指标详解
│   ├── MACD.md
│   ├── Bollinger-Bands.md
│   ├── ADX.md
│   ├── Ichimoku.md
│   ├── EMA.md
│   ├── VWAP.md
│   │
│   └── Indicator-Combinations.md  # 常见组合模式
│
├── 📁 03_Styles/                  # 交易风格
│   ├── Trend-Following.md
│   ├── Mean-Reversion.md
│   ├── Scalping.md
│   ├── Breakout.md
│   └── Style-Selection-Guide.md   # 市场环境匹配指南
│
├── 📁 04_Evaluation/              # VecScore评估体系
│   ├── VecScore-Overview.md       # 五维评分总览
│   ├── Dimension-P-Return.md      # P维度详解
│   ├── Dimension-R-Risk.md
│   ├── Dimension-S-Stability.md
│   ├── Dimension-T-Reliability.md
│   ├── Dimension-E-Efficiency.md
│   ├── Grade-Criteria.md          # S/A/B/C/D等级标准
│   └── Commercial-Eligibility.md  # 商用资格判定
│
├── 📁 05_Pipeline/                # 评估流程
│   ├── Phase0-Static-Filter.md    # 静态预筛规则
│   ├── Phase1-Quick-Backtest.md   # 快速回测标准
│   ├── Phase2-VecScore.md         # 评分计算
│   ├── Leaderboard-Generation.md
│   ├── Database-Sync.md           # MarketXpress集成
│   └── Pipeline-Cheat-Sheet.md    # 命令速查
│
├── 📁 06_Leaderboard/             # 排行榜快照
│   ├── Leaderboard-2025-Year.md
│   ├── Leaderboard-Last-30-Days.md
│   ├── Leaderboard-Last-1-Week.md
│   └── Leaderboard-History.md     # 排名变迁追踪
│
├── 📁 07_Operations/              # 操作指南
│   ├── Docker-Setup.md
│   ├── Data-Download.md
│   ├── Backtest-Commands.md
│   ├── K8s-Deployment.md
│   └── Troubleshooting.md
│
├── 📁 08_Decisions/               # 设计决策日志
│   ├── DEC-001-VecScore-v3.md     # 决策记录模板
│   ├── DEC-002-Grade-Thresholds.md
│   └── ADR-Template.md            # Architecture Decision Record模板
│
├── 📁 09_Archive/                 # 旧文档归档
│   ├── legacy-reports/            # 原docs/目录的完整报告
│   └── deprecated-strategies/
│
└── 📁 Templates/                  # Obsidian模板
    ├── Strategy-Card-Template.md
    ├── Indicator-Template.md
    ├── Decision-Template.md
    └── Pipeline-Run-Template.md
```

## 核心卡片模板

### Strategy-Card-Template.md

```markdown
---
tags: [strategy, <family>, <grade>, <timeframe>]
family: <家族名>
grade: <S|A|B|C|D>
vecscore: <数值>
timeframe: <5m|1h|...>
indicators: [<指标列表>]
style: [<风格列表>]
commercial: <true|false>
source: strategies/<StrategyName>/<StrategyName>.py
---

# <StrategyName>

## 📊 快速评分
| 维度 | 得分 | 满分 |
|------|------|------|
| P (收益) | <P_score> | 30 |
| R (风控) | <R_score> | 25 |
| S (稳定) | <S_score> | 20 |
| T (可靠) | <T_score> | 15 |
| E (效率) | <E_score> | 10 |
| **总分** | **<VecScore>** | 100 |

## 🎯 核心特征
- **风格**: <Trend | MeanReversion | Scalping>
- **市场环境**: <Trending | Sideways | Volatile>
- **交易方向**: <Long | Short | Both>
- **复杂度**: <1-10>

## 📈 30天回测表现
| 指标 | 数值 |
|------|------|
| ROI | <roi>% |
| Sharpe | <sharpe> |
| MaxDD | <max_dd>% |
| Win率 | <winrate>% |
| 交易数 | <trades> |

## 🔗 关联策略
- 同家族: [[<FamilyMember1>]], [[<FamilyMember2>]]
- 同风格: [[<StylePeer1>]], [[<StylePeer2>]]
- 进化版本: [[<NextVersion>]]
- 原始版本: [[<OriginalVersion>]]

## 📝 设计思想
<从策略评审报告提取的设计思想>

## ⚠️ 风险提示
<从评审报告提取的改进建议>

## 📋 使用建议
- **适用场景**: <场景描述>
- **参数调优**: <hyperopt建议>
- **组合推荐**: 与 [[<CompanionStrategy>]] 配合使用

---
*数据来源: VecScore报告 (2025-04-15)*
```

### MOC-Strategies.md (Map of Content)

```markdown
# 策略知识地图

> 本页是策略导航的入口，按不同维度组织策略卡片

## 🏆 按等级浏览

### S级 (旗舰策略)
- [[NostalgiaForInfinityV7]] ⭐ VecScore: 85
- ...

### A级 (商用推荐)
- [[BinHV45]] ⭐ VecScore: 78
- ...

### B级 (可用)
- [[ClucHAnix_5m]] ✅ VecScore: 65
- ...

## 🏠 按家族浏览

### Nostalgia 家族
> [[NFI-Family-Overview]] | 均值回归+动态止损失
- [[NostalgiaForInfinityV5]] → [[NostalgiaForInfinityV7]] → [[NostalgiaForInfinityV7_SMA]]

### BinHV 家族
> [[BinHV-Family-Overview]] | 布林带突破
- [[BinHV27]] → [[BinHV45]] → [[BinHV45HO]]

## 🎯 按风格浏览

### 趋势跟随 [[Trend-Following]]
- [[MACD_TRIPLE_MA]]
- [[ADX_15M_USDT]]

### 均值回归 [[Mean-Reversion]]
- [[BBRSI]]
- [[Cluc4]]

### 剥头皮 [[Scalping]]
- [[Scalp]]
- [[SmoothScalp]]

## ⏱ 按时间框架浏览

| Timeframe | 代表策略 |
|-----------|----------|
| 1m | [[BinHV45]], [[Combined_Indicators]] |
| 5m | [[NostalgiaForInfinityV7]], [[ClucHAnix_5m]] |
| 15m | [[ADX_15M_USDT]], [[BbandRsi]] |
| 1h | [[ADXMomentum]], [[MACD_TRIPLE_MA]] |

## 🔗 指标组合浏览

### RSI + 布林带 [[RSI]] [[Bollinger-Bands]]
- [[BBRSI]], [[BBRSI21]], [[Cluc4]]

### MACD + EMA [[MACD]] [[EMA]]
- [[MACD_TRIPLE_MA]], [[MACDRSI200]]

### Ichimoku 全套 [[Ichimoku]]
- [[Ichimoku_v30]], [[Ichimoku_v31]], [[Ichimoku_v32]]

---
> 💡 点击任意策略卡片，可查看完整评分、设计思想、关联策略
```

## 同步脚本思路

```python
# scripts/sync_to_obsidian.py
# 从 strategy_registry.json + vecscore_results.json → 生成策略卡片

def generate_strategy_card(name, registry, vecscore):
    template = load_template("Strategy-Card-Template.md")
    
    # 基本信息
    card = template.replace("<StrategyName>", name)
    card = card.replace("<family>", registry.get("family", "Unknown"))
    card = card.replace("<grade>", vecscore.get("grade", "D"))
    
    # 关联策略（同家族成员）
    family_members = find_family_members(registry["family"])
    card += f"\n## 🔗 同家族策略\n"
    for m in family_members:
        card += f"- [[{m}]]\n"
    
    # 同风格策略
    same_style = find_by_style(registry["style"])
    card += f"\n## 🔗 同风格策略\n"
    for s in same_style[:5]:
        card += f"- [[{s}]]\n"
    
    return card

def generate_moc_strategies(vecscore_results):
    """生成策略总览MOC"""
    by_grade = group_by_grade(vecscore_results)
    by_family = group_by_family(vecscore_results)
    # ... 拼接各个section
```

## Obsidian 配置建议

```json
// .obsidian/workspace.json (建议设置)
{
  "graph": {
    "collapseFilter": true,
    "groups": {
      "S级": { "query": "tag:#grade-S", "color": "#ff6b6b" },
      "A级": { "query": "tag:#grade-A", "color": "#ffd93d" },
      "B级": { "query": "tag:#grade-B", "color": "#6bcb77" },
      "策略": { "query": "tag:#strategy", "color": "#4d96ff" },
      "指标": { "query": "tag:#indicator", "color": "#845ec2" }
    }
  }
}
```

## 关键设计原则

1. **家族聚合**: 策略按家族组织，便于追踪进化路线
2. **多维度索引**: MOC页提供等级/风格/时间框架多入口
3. **双向链接**: 每个策略卡片链接到同家族、同风格策略
4. **指标知识库**: 指标独立成页，策略卡片链接到所用指标
5. **决策日志**: VecScore调整、等级阈值变化有决策记录
6. **时间快照**: 排行榜按时段归档，支持历史对比

## 下一步

1. 确认vault存放位置（新目录 vs 子目录）
2. 编写同步脚本从现有数据生成卡片
3. 补充指标知识页（从策略源码提取）
4. 配置Obsidian图谱颜色分组

---

**估算规模**:
- 策略卡片: ~300页
- 指标页: ~15页
- MOC页: ~5页
- 评估/流程: ~10页
- 总计: ~330页（可管理规模）