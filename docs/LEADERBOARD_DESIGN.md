# Design System: Freqtrade Strategy Leaderboard (Stitch Optimized)
**Project ID:** `projects/freqtrade-backtest-v1`

## 1. Visual Theme & Atmosphere
本数据大盘采用 **"Obsidian Financial" (黑曜石金融)** 视觉风格。整体氛围呈现出：
- **高端 (Premium)**: 深色背景配合极高对比度，模拟彭博终端（Bloomberg Terminal）的专业感。
- **高密度 (High Density)**: 专为专业交易员设计，单页面承载多层级数据流，减少滚动疲劳。
- **动感 (Dynamic)**: 通过霓虹发光边框（Neon Glow）和微缩历史曲线（Sparkline）营造实时跳动的市场感。

## 2. Color Palette & Roles
本套系统的色彩定义基于功能语义（Semantic Colors）：
- **Carbon Base (#121212)**: 核心背景色。用于底层画布，确立深沉稳重的基调。
- **Obsidian Elevate (#1A1C23)**: 容器背景色。用于 Hero 卡片和表格主体，通过细微色差建立视觉层级（Z-index）。
- **Neon Success Green (#00E676)**: 收益/正面色彩。用于盈利数据、上涨 Sparkline 及 "Highest Profit" 核心卡片。
- **Cyber Blue (#2979FF)**: 交互/胜率色彩。用于 "Best Win Rate" 冠军卡片、表头排序状态及链接。
- **Nuclear Risk Red (#FF5252)**: 回撤/风险色彩。用于 "Lowest Drawdown"（负向指标显红）及警告状态。
- **Chiclet Gray (#2C2E33)**: 标签底色。用于 Filter Bar 的未选中状态。

## 3. Typography Rules
- **Header (Inter-Bold)**: 所有卡片标题和表头使用加粗无衬线体，字母间距（Letter-spacing）设为 `-0.02em` 以增强力量感。
- **Data (Roboto Mono)**: 凡涉及具体金额、百分比、回撤率的数字，均采用等宽字体（Monospaced），确保在大表格垂直排列时位数精确对齐。
- **Labels (Inter-Regular)**: 用于次要描述信息，颜色通常设为 70% 灰度以降低干扰。

## 4. Component Stylings
- **Hero Cards**: 
  - **形状**: 采用 `Gently Curved (#12px)` 圆角。
  - **边框**: 顶部设有 2px 的颜色霓虹灯装饰条（根据指标类型变色）。
  - **阴影**: 高度扩散的柔和背光（Glow Effect），而非传统的重投影。
- **Filter Tags**: 
  - **形状**: 采用 Pill-shaped (全圆角) 的胶囊造型。
  - **状态**: 激活态带有 1px 的外边框发光和色彩填充，未激活态仅保留深灰色底。
- **Leaderboard Table**: 
  - **斑马纹**: 取消边框线，通过隔行变色实现视觉导流。
  - **排序图标**: 现代化的空心三角形（🔼🔽），激活态由灰色转为 Cyber Blue。

## 5. Layout Principles
- **Whitespace Strategy**: 坚持 **"Breathing Data" (留白呼吸)** 原则，即使在多维榜单中，行高也设定为 `64px`，确保每个策略条目都有足够的垂直呼吸空间。
- **Grid Alignment**: 严格遵循 12 栅格系统。顶层 3 个 Hero 卡片平分空间（Offset-0），中部过滤器与底层跑马灯保持对齐。
- **Navigation Flow**: 用户视线流向呈 "Z" 字型：从左上角总收益冠军开始 -> 扫视右侧风控 -> 向下通过过滤器进行思维聚焦 -> 最终沉淀到海量数据总表进行深度钻研。
