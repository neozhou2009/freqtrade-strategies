#!/bin/bash
# 批量修复第42-47批次策略脚本
# 使用方法: ./batch_fix_42_47.sh

set -e  # 遇到错误退出

echo "=== 开始修复第42-47批次策略 ==="
echo "总策略数: 55个"
echo "批次数: 6批 (第42-47批)"
echo

# 第42批策略列表 (10个)
BATCH42=("ADXMomentum" "ADX_15M_USDT" "ADX_15M_USDT2" "ASDTSRockwellTrading" "ActionZone" "AdxSmas" "AlligatorStrat" "AlligatorStrategy" "AlwaysBuy" "Apollo11")

# 第43批策略列表 (10个)
BATCH43=("AverageStrategy" "AwesomeMacd" "BBMod1" "BBRSI" "BBRSI2" "BBRSI21" "BBRSI3366" "BBRSI4cust" "BBRSINaiveStrategy" "BBRSIOptim2020Strategy")

# 第44批策略列表 (10个)
BATCH44=("BBRSIOptimStrategy" "BBRSIOptimizedStrategy" "BBRSIS" "BBRSIStrategy" "BBRSITV" "BBRSIoriginal" "BBRSIv2" "BB_RPB_TSL" "BB_RPB_TSL_2" "BB_RPB_TSL_BI")

# 第45批策略列表 (10个)
BATCH45=("BB_RPB_TSL_BIV1" "BB_RPB_TSL_RNG" "BB_RPB_TSL_RNG_2" "BB_RPB_TSL_RNG_TBS" "BB_RPB_TSL_RNG_TBS_GOLD" "BB_RPB_TSL_RNG_VWAP" "BB_RPB_TSL_SMA_Tranz" "BB_RPB_TSL_SMA_Tranz_TB_1_1_1" "BB_RPB_TSL_SMA_Tranz_TB_MOD" "BB_RPB_TSL_Tranz")

# 第46批策略列表 (10个)
BATCH46=("BB_RPB_TSL_c7c477d_20211030" "BB_RPB_TSLmeneguzzo" "BB_RSI" "BB_Strategy04" "BBands" "BBandsRSI" "BBlower" "Babico_SMA5xBBmid" "Bandtastic" "BbRoi")

# 第47批策略列表 (5个)
BATCH47=("macd_recovery" "mark_strat" "mark_strat_opt" "quantumfirst" "redditMA")

# 通用修复函数
fix_strategy() {
    local strategy=$1
    local file="strategies/${strategy}/${strategy}.py"
    
    if [ ! -f "$file" ]; then
        echo "❌ 策略文件不存在: $file"
        return 1
    fi
    
    echo "🔧 修复策略: $strategy"
    
    # 备份原文件
    cp "$file" "${file}.backup"
    
    # 1. 修复qtpylib导入
    sed -i 's/import freqtrade\.vendor\.qtpylib\.indicators as qtpylib/from technical import qtpylib/g' "$file"
    sed -i 's/from freqtrade\.vendor import qtpylib/from technical import qtpylib/g' "$file"
    
    # 2. 修复INTERFACE_VERSION
    sed -i 's/INTERFACE_VERSION = 2/INTERFACE_VERSION = 3/g' "$file"
    
    # 3. 修复废弃参数 buy -> entry, sell -> exit
    sed -i 's/sell_profit_only =/exit_profit_only =/g' "$file"
    sed -i 's/use_sell_signal =/use_exit_signal =/g' "$file"
    sed -i 's/ignore_roi_if_buy_signal =/ignore_roi_if_entry_signal =/g' "$file"
    sed -i "s/'buy'/'entry'/g" "$file"
    sed -i "s/'sell'/'exit'/g" "$file"
    
    # 4. 修复custom_sell -> custom_exit
    sed -i 's/def custom_sell/def custom_exit/g' "$file"
    
    # 5. 修复numpy.NAN -> np.nan
    sed -i 's/np\.NAN/np.nan/g' "$file"
    
    # 6. 修复旧版导入
    sed -i 's/from freqtrade\.strategy\.interface import IStrategy/from freqtrade.strategy import IStrategy/g' "$file"
    
    echo "✅ 修复完成: $strategy"
}

# 修复第42批
echo "=== 修复第42批 (10个策略) ==="
for strategy in "${BATCH42[@]}"; do
    fix_strategy "$strategy"
done

# 修复第43批
echo "=== 修复第43批 (10个策略) ==="
for strategy in "${BATCH43[@]}"; do
    fix_strategy "$strategy"
done

# 修复第44批
echo "=== 修复第44批 (10个策略) ==="
for strategy in "${BATCH44[@]}"; do
    fix_strategy "$strategy"
done

# 修复第45批
echo "=== 修复第45批 (10个策略) ==="
for strategy in "${BATCH45[@]}"; do
    fix_strategy "$strategy"
done

# 修复第46批
echo "=== 修复第46批 (10个策略) ==="
for strategy in "${BATCH46[@]}"; do
    fix_strategy "$strategy"
done

# 修复第47批
echo "=== 修复第47批 (5个策略) ==="
for strategy in "${BATCH47[@]}"; do
    fix_strategy "$strategy"
done

echo
echo "=== 修复完成 ==="
echo "已修复策略总数: $(( ${#BATCH42[@]} + ${#BATCH43[@]} + ${#BATCH44[@]} + ${#BATCH45[@]} + ${#BATCH46[@]} + ${#BATCH47[@]} ))"
echo "建议接下来运行测试验证修复效果"