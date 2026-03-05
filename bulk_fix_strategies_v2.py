#!/usr/bin/env python3
"""
批量修复 Freqtrade 策略脚本
修复以下问题:
1. 旧接口导入: from freqtrade.strategy.interface import IStrategy → from freqtrade.strategy import IStrategy
2. 添加接口版本: 在类定义前添加 INTERFACE_VERSION = 3
3. 修复 order_time_in_force 大小写问题: 'gtc' → 'GTC'
4. 修复 order_types 参数重命名问题:
   - 'emergencysell' → 'emergency_exit'
   - 'forcebuy' → 'force_entry'
   - 'forcesell' → 'force_exit'
   - 移除 'trailing_stop_loss' (如果存在)
"""

import os
import re
import glob
from pathlib import Path
from typing import List, Dict, Tuple
import argparse


class StrategyFixer:
    def __init__(self, strategies_dir: str = "strategies", verbose: bool = True):
        self.strategies_dir = Path(strategies_dir)
        self.verbose = verbose
        self.fixes_applied = 0
        self.files_processed = 0

    def find_strategy_files(self) -> List[Path]:
        pattern = str(self.strategies_dir / "**" / "*.py")
        files = glob.glob(pattern, recursive=True)
        return [Path(f) for f in files]

    def fix_import_statement(self, content: str) -> Tuple[str, bool]:
        old_pattern = r"from\s+freqtrade\.strategy\.interface\s+import\s+IStrategy"
        new_line = "from freqtrade.strategy import IStrategy"

        if re.search(old_pattern, content):
            fixed_content = re.sub(old_pattern, new_line, content)
            return fixed_content, True
        return content, False

    def add_interface_version(self, content: str) -> Tuple[str, bool]:
        if "INTERFACE_VERSION" in content:
            return content, False

        class_pattern = r"^class\s+\w+\(IStrategy\):"
        lines = content.split("\n")

        for i, line in enumerate(lines):
            if re.match(class_pattern, line.strip()):
                indent = len(line) - len(line.lstrip())
                spaces = " " * indent
                lines.insert(i, f"{spaces}INTERFACE_VERSION = 3")
                return "\n".join(lines), True

        return content, False

    def fix_order_time_in_force_case(self, content: str) -> Tuple[str, bool]:
        fixed = False

        if "order_time_in_force" in content:
            if "'gtc'" in content.lower():
                content = re.sub(r"'gtc'", "'GTC'", content, flags=re.IGNORECASE)
                fixed = True
            if '"gtc"' in content.lower():
                content = re.sub(r'"gtc"', '"GTC"', content, flags=re.IGNORECASE)
                fixed = True

        return content, fixed

    def fix_order_types_renaming(self, content: str) -> Tuple[str, bool]:
        fixed = False

        if "emergencysell" in content:
            content = content.replace("'emergencysell'", "'emergency_exit'")
            content = content.replace('"emergencysell"', '"emergency_exit"')
            fixed = True

        if "forcebuy" in content:
            content = content.replace("'forcebuy'", "'force_entry'")
            content = content.replace('"forcebuy"', '"force_entry"')
            fixed = True

        if "forcesell" in content:
            content = content.replace("'forcesell'", "'force_exit'")
            content = content.replace('"forcesell"', '"force_exit"')
            fixed = True

        if "trailing_stop_loss" in content:
            lines = content.split("\n")
            new_lines = []
            in_order_types = False

            for line in lines:
                if "order_types" in line and "{" in line:
                    in_order_types = True
                elif in_order_types and "}" in line:
                    in_order_types = False

                if in_order_types and "trailing_stop_loss" in line:
                    continue

                new_lines.append(line)

            content = "\n".join(new_lines)
            fixed = True

        return content, fixed

    def fix_qtpylib_import(self, content: str) -> Tuple[str, bool]:
        old_pattern = r"import\s+freqtrade\.vendor\.qtpylib\.indicators\s+as\s+qtpylib"
        new_line = "from technical import qtpylib"

        if re.search(old_pattern, content):
            fixed_content = re.sub(old_pattern, new_line, content)
            return fixed_content, True
        return content, False

    def fix_numpy_nan_case(self, content: str) -> Tuple[str, bool]:
        if "np.NAN" in content:
            content = content.replace("np.NAN", "np.nan")
            return content, True
        return content, False

    def analyze_strategy_file(self, filepath: Path) -> Dict[str, bool]:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            if self.verbose:
                print(f"❌ 无法读取文件 {filepath}: {e}")
            return {}

        problems = {
            "has_old_import": bool(
                re.search(
                    r"from\s+freqtrade\.strategy\.interface\s+import\s+IStrategy",
                    content,
                )
            ),
            "missing_interface_version": "INTERFACE_VERSION" not in content,
            "has_qtpylib_vendor_import": bool(
                re.search(
                    r"import\s+freqtrade\.vendor\.qtpylib\.indicators\s+as\s+qtpylib",
                    content,
                )
            ),
            "has_numpy_upper_nan": "np.NAN" in content,
            "has_lowercase_gtc": "'gtc'" in content.lower()
            or '"gtc"' in content.lower(),
            "has_emergencysell": "emergencysell" in content,
            "has_forcebuy": "forcebuy" in content,
            "has_forcesell": "forcesell" in content,
            "has_trailing_stop_loss": "trailing_stop_loss" in content,
        }

        return problems

    def fix_strategy_file(self, filepath: Path) -> Tuple[bool, Dict[str, bool]]:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            if self.verbose:
                print(f"❌ 无法读取文件 {filepath}: {e}")
            return False, {}

        original_content = content
        fixes_applied = {}

        content, fix1 = self.fix_import_statement(content)
        fixes_applied["fixed_import"] = fix1

        content, fix2 = self.add_interface_version(content)
        fixes_applied["added_interface_version"] = fix2

        content, fix3 = self.fix_qtpylib_import(content)
        fixes_applied["fixed_qtpylib"] = fix3

        content, fix4 = self.fix_numpy_nan_case(content)
        fixes_applied["fixed_numpy_nan"] = fix4

        content, fix5 = self.fix_order_time_in_force_case(content)
        fixes_applied["fixed_gtc_case"] = fix5

        content, fix6 = self.fix_order_types_renaming(content)
        fixes_applied["fixed_order_types"] = fix6

        if content == original_content:
            return False, fixes_applied

        backup_path = filepath.with_suffix(".py.bak")
        try:
            with open(backup_path, "w", encoding="utf-8") as f:
                f.write(original_content)
        except Exception as e:
            if self.verbose:
                print(f"⚠️ 无法创建备份 {backup_path}: {e}")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            self.fixes_applied += sum(fixes_applied.values())
            self.files_processed += 1

            return True, fixes_applied

        except Exception as e:
            if self.verbose:
                print(f"❌ 无法写入文件 {filepath}: {e}")

            if backup_path.exists():
                try:
                    with open(backup_path, "r", encoding="utf-8") as f:
                        backup_content = f.read()
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(backup_content)
                except Exception:
                    pass

            return False, fixes_applied

    def run_dry_run(self) -> Dict[str, int]:
        strategy_files = self.find_strategy_files()
        problem_stats = {
            "total_files": len(strategy_files),
            "old_import": 0,
            "missing_interface_version": 0,
            "qtpylib_vendor_import": 0,
            "numpy_upper_nan": 0,
            "lowercase_gtc": 0,
            "emergencysell": 0,
            "forcebuy": 0,
            "forcesell": 0,
            "trailing_stop_loss": 0,
        }

        if self.verbose:
            print(f"🔍 找到 {len(strategy_files)} 个策略文件")

        for filepath in strategy_files:
            problems = self.analyze_strategy_file(filepath)
            if problems:
                for key, value in problems.items():
                    if value:
                        if key in problem_stats:
                            problem_stats[key] += 1
                        else:
                            problem_stats[key] = 1

        return problem_stats

    def run_fixes(self) -> Dict[str, int]:
        strategy_files = self.find_strategy_files()
        results = {
            "total_files": len(strategy_files),
            "successfully_fixed": 0,
            "failed_fixes": 0,
            "skipped_files": 0,
            "fixes_by_type": {
                "fixed_import": 0,
                "added_interface_version": 0,
                "fixed_qtpylib": 0,
                "fixed_numpy_nan": 0,
                "fixed_gtc_case": 0,
                "fixed_order_types": 0,
            },
        }

        if self.verbose:
            print(f"🔧 开始修复 {len(strategy_files)} 个策略文件")

        for filepath in strategy_files:
            if self.verbose:
                print(f"处理: {filepath.name}")

            success, fixes_applied = self.fix_strategy_file(filepath)

            if success and any(fixes_applied.values()):
                results["successfully_fixed"] += 1
                for fix_type, applied in fixes_applied.items():
                    if applied:
                        results["fixes_by_type"][fix_type] += 1
            elif not any(fixes_applied.values()):
                results["skipped_files"] += 1
            else:
                results["failed_fixes"] += 1

        return results


def main():
    parser = argparse.ArgumentParser(description="批量修复 Freqtrade 策略脚本")
    parser.add_argument(
        "--dry-run", action="store_true", help="干测试模式，不实际修改文件"
    )
    parser.add_argument("--strategies-dir", default="strategies", help="策略目录路径")
    parser.add_argument("--verbose", action="store_true", help="显示详细输出")
    parser.add_argument("--fix-specific", type=str, help="修复特定策略文件")

    args = parser.parse_args()

    fixer = StrategyFixer(args.strategies_dir, args.verbose)

    if args.dry_run:
        print("🚀 运行干测试模式 (不修改文件)")
        print("=" * 60)

        stats = fixer.run_dry_run()

        print(f"\n📊 问题统计:")
        print(f"总策略文件数: {stats['total_files']}")
        print(
            f"使用旧接口导入的策略: {stats['old_import']} ({stats['old_import'] / stats['total_files'] * 100:.1f}%)"
        )
        print(
            f"缺少 INTERFACE_VERSION 的策略: {stats['missing_interface_version']} ({stats['missing_interface_version'] / stats['total_files'] * 100:.1f}%)"
        )
        print(f"使用旧 qtpylib 导入的策略: {stats['qtpylib_vendor_import']}")
        print(f"使用 np.NAN 大写形式的策略: {stats['numpy_upper_nan']}")
        print(f"使用小写 'gtc' 的策略: {stats['lowercase_gtc']}")
        print(f"使用 'emergencysell' 的策略: {stats['emergencysell']}")
        print(f"使用 'forcebuy' 的策略: {stats['forcebuy']}")
        print(f"使用 'forcesell' 的策略: {stats['forcesell']}")
        print(f"使用 'trailing_stop_loss' 的策略: {stats['trailing_stop_loss']}")

        print("\n💡 建议修复顺序:")
        print("1. 旧接口导入修复 (最高优先级)")
        print("2. 添加 INTERFACE_VERSION = 3")
        print("3. qtpylib 导入修复")
        print("4. order_time_in_force 大小写修复 ('gtc' → 'GTC')")
        print("5. order_types 参数重命名修复")
        print("6. numpy NaN 大小写修复")

    elif args.fix_specific:
        print(f"🔧 修复特定文件: {args.fix_specific}")
        filepath = Path(args.fix_specific)
        if filepath.exists():
            success, fixes_applied = fixer.fix_strategy_file(filepath)
            if success:
                print(f"✅ 成功修复 {filepath.name}")
                applied_fixes = [k for k, v in fixes_applied.items() if v]
                print(f"   应用的修复: {', '.join(applied_fixes)}")
            else:
                print(f"❌ 修复失败 {filepath.name}")
        else:
            print(f"❌ 文件不存在: {args.fix_specific}")

    else:
        print("🚀 开始批量修复策略文件")
        print("=" * 60)

        results = fixer.run_fixes()

        print(f"\n📊 修复结果:")
        print(f"总策略文件数: {results['total_files']}")
        print(f"成功修复的文件: {results['successfully_fixed']}")
        print(f"修复失败的文件: {results['failed_fixes']}")
        print(f"跳过的文件 (无需修复): {results['skipped_files']}")

        print(f"\n🔧 修复类型统计:")
        for fix_type, count in results["fixes_by_type"].items():
            if count > 0:
                print(f"  {fix_type}: {count}")

        print(f"\n✅ 总修复数: {fixer.fixes_applied}")
        print(f"📁 处理的文件数: {fixer.files_processed}")

        if results["failed_fixes"] > 0:
            print(f"\n⚠️  注意: {results['failed_fixes']} 个文件修复失败，请检查日志")

        print("\n💡 下一步:")
        print("1. 运行测试验证修复效果")
        print("2. 检查是否有遗漏的修复")
        print("3. 更新 ALL_STRATEGIES_FIX_PLAN.md 文档")


if __name__ == "__main__":
    main()
