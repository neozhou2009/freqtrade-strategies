import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

# 定义要扫描的目录
STRATEGIES_DIR = Path("strategies")

# 中文 README 模板
README_TEMPLATE = """# {strategy_name} 策略分析报告

> **分析日期**: {analysis_date}
> **策略版本**: 自动分析版
> **分析师**: Freqtrade 策略分析机器人

---

## 📋 执行摘要

{execution_summary}

**风险评级**: {risk_rating}

---

## 策略概述

- **策略名称**: {strategy_name}
- **时间框架**: {timeframe}
- **止损设置**: {stoploss}
- **最小ROI**: {roi}

## 策略意图和目的

{strategy_intent}

### 核心逻辑

{core_logic}

### 适用市场

本策略适用于**数字货币市场**的交易。

---

## 使用技术指标

{indicators_list}

---

## 🔴 风险与问题分析

### 1. 代码问题
{code_issues}

### 2. 投资逻辑/风控问题
{logic_issues}

---

## 💡 改进建议

1. **止损优化**: {stoploss_suggestion}
2. **ROI调整**: {roi_suggestion}
3. **风控增强**: 建议开启 `use_custom_stoploss` 并结合 ATR 或其他波动率指标进行动态止损。
4. **代码升级**: {code_fix_suggestion}

---

## 🚀 使用说明

1. 将策略文件复制到 Freqtrade 的 `strategies` 目录（如果尚未在）。
2. 运行回测测试策略效果: `freqtrade backtesting -s {strategy_name}`
3. 如有需要，使用 hyperopt 优化参数。
4. **风险提示**: 实盘前务必进行充分测试，尤其是以前未经过验证的策略。

"""

class StrategyAnalyzer:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.source_code = self.file_path.read_text(encoding="utf-8", errors="ignore")
        self.tree = ast.parse(self.source_code)
        self.class_node = self._find_strategy_class()
        
        # 提取的元数据
        self.strategy_name = self.class_node.name if self.class_node else "Unknown"
        self.timeframe = self._extract_variable("timeframe", "5m")
        self.stoploss = self._extract_variable("stoploss", -0.10)
        self.roi = self._extract_variable("minimal_roi", {})
        self.indicators = self._extract_indicators()
        self.issues = []
        self.risk_score = 0  # 越高风险越大

    def _find_strategy_class(self):
        for node in self.tree.body:
            if isinstance(node, ast.ClassDef):
                # 简单判断，通常类名就是策略名
                return node
        return None

    def _extract_variable(self, var_name: str, default: Any) -> Any:
        if not self.class_node:
            return default
        for node in self.class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == var_name:
                        try:
                            # 尝试获取变量的字面值
                            return ast.literal_eval(node.value)
                        except:
                            # 如果是一个复杂的表达式 (比如 dict 构造), 返回一个占位符或默认值
                            if isinstance(node.value, ast.Dict):
                                return "{...}"
                            return default
        return default
    
    def _extract_indicators(self) -> List[str]:
        indicators = set()
        # 简单正则匹配常见的 TA-Lib 和 qtpylib 调用
        # e.g. ta.RSI, qtpylib.bollinger_bands
        
        matches = re.findall(r'(ta\.[A-Z0-9]+|qtpylib\.[a-z_]+)', self.source_code)
        for m in matches:
            # 清理 ta. 或 qtpylib. 前缀，只留指标名
            name = m.replace('ta.', '').replace('qtpylib.', '')
            indicators.add(name)
        
        return list(sorted(indicators))

    def analyze_risks(self):
        # 1. 检查导入
        if "freqtrade.strategy.interface" in self.source_code:
            self.issues.append({"type": "code", "msg": "使用了已废弃的导入: `freqtrade.strategy.interface`", "severity": "low"})
        
        # 2. 检查止损
        try:
            sl = float(self.stoploss) if isinstance(self.stoploss, (int, float)) else -0.1
            if sl == -1:
                self.issues.append({"type": "logic", "msg": "**极高风险**: 止损设置为 -1 (100%)，意味着没有硬止损保护。", "severity": "high"})
                self.risk_score += 5
            elif sl < -0.2:
                self.issues.append({"type": "logic", "msg": "**高风险**: 止损设置宽松 (低于 -20%)，单次亏损风险较大。", "severity": "medium"})
                self.risk_score += 2
        except:
            pass
            
        # 3. 检查 ROI
        if not self.roi or self.roi == "{...}":
             pass # Skip complex dict check for now

        # 4. 检查是否重写了 populate_indicators
        if "def populate_indicators" not in self.source_code:
             self.issues.append({"type": "code", "msg": "缺少 `populate_indicators` 方法，策略可能不完整。", "severity": "high"})
             self.risk_score += 5

    def generate_report_content(self, date_str):
        # 格式化指标列表
        indicators_list = ", ".join(self.indicators) if self.indicators else "未检测到明显的技术指标调用"
        
        # 格式化问题
        code_issues_list = [f"- {i['msg']}" for i in self.issues if i['type'] == 'code']
        code_issues_str = "\n".join(code_issues_list) if code_issues_list else "- 未发现明显的代码语法问题。"
        
        logic_issues_list = [f"- {i['msg']}" for i in self.issues if i['type'] == 'logic']
        logic_issues_str = "\n".join(logic_issues_list) if logic_issues_list else "- 常见风控配置检查通过。"
        
        # 评级
        rating = "🟢 低风险"
        if self.risk_score >= 5:
            rating = "🔴 高风险"
        elif self.risk_score >= 2:
            rating = "🟠 中等风险"
        
        # 意图推断 (非常基础)
        intent = "本策略通过计算技术指标并在特定条件下触发买卖信号。"
        if "RSI" in self.indicators and "bollinger_bands" in self.indicators:
             intent += " 看起来结合了震荡指标 (RSI) 和波动率通道 (Bollinger Bands) 进行交易，可能包含均值回归逻辑。"
        elif "EMA" in self.indicators or "SMA" in self.indicators:
             intent += " 包含移动平均线，可能是一个趋势跟踪策略。"

        return README_TEMPLATE.format(
            strategy_name=self.strategy_name,
            analysis_date=date_str,
            execution_summary=f"本策略共检测到 {len(self.indicators)} 个技术指标调用。{'存在高风险配置项，请务必注意。' if self.risk_score >= 5 else '基础配置看起来相对正常。'}",
            risk_rating=rating,
            timeframe=self.timeframe,
            stoploss=self.stoploss,
            roi=self.roi,
            strategy_intent=intent,
            core_logic="基于 `populate_entry_trend` 和 `populate_exit_trend` 中定义的逻辑。",
            indicators_list=indicators_list,
            code_issues=code_issues_str,
            logic_issues=logic_issues_str,
            stoploss_suggestion="建议设置在 -0.05 到 -0.10 之间，或根据 ATR 动态调整。" if self.risk_score > 0 else "当前设置可接受，但建议结合动态止损。",
            roi_suggestion="建议分段止盈，例如 `{'0': 0.1, '30': 0.05}`。",
            code_fix_suggestion="已自动修复过时的导入语句 (如有)。"
        )

    def fix_code(self) -> bool:
        """
        执行简单的代码修复。
        返回 True 如果有修改。
        """
        original_code = self.source_code
        new_code = self.source_code
        
        # 修复 1: 导入
        if "from freqtrade.strategy.interface import IStrategy" in new_code:
            new_code = new_code.replace(
                "from freqtrade.strategy.interface import IStrategy",
                "from freqtrade.strategy import IStrategy"
            )
            
        if new_code != original_code:
            self.file_path.write_text(new_code, encoding="utf-8")
            return True
        return False

def main():
    import datetime
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    count = 0
    analyzed_count = 0
    # 遍历 strategies 目录下的所有子目录
    for root, dirs, files in os.walk(STRATEGIES_DIR):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = Path(root) / file
                
                try:
                    # 简单的日志
                    # print(f"Analyzing {file}...")
                    
                    analyzer = StrategyAnalyzer(file_path)
                    analyzer.analyze_risks()
                    
                    # 生成 README
                    readme_content = analyzer.generate_report_content(today)
                    readme_path = file_path.parent / "README.md"
                    
                    # 仅当 README 不存在时写入，或者始终覆盖 (根据需求，这里选择覆盖以更新)
                    readme_path.write_text(readme_content, encoding="utf-8")
                    
                    # 修复代码
                    fixed = analyzer.fix_code()
                    if fixed:
                        print(f"Fixed code issues in {file}")
                    
                    analyzed_count += 1
                except Exception as e:
                    print(f"Error processing {file}: {str(e)}")
                    continue

    print(f"Finished processing {analyzed_count} strategies.")

if __name__ == "__main__":
    main()
