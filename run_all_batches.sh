#!/bin/bash
# Run all batch tests from 28 to 41
# Batch 27 already tested

set -e

echo "🚀 开始批量测试批次 28-41"
echo "======================================"

for batch in {28..41}; do
    if [ -f "test/test_batch${batch}_strategies.sh" ]; then
        echo ""
        echo "📊 测试批次 ${batch}..."
        echo "--------------------------------------"
        ./test/test_batch${batch}_strategies.sh
        
        # 短暂暂停
        sleep 2
    else
        echo "⚠️  批次 ${batch} 脚本不存在"
    fi
done

echo ""
echo "✅ 所有批次测试完成!"
echo ""
echo "📋 结果汇总:"
echo "--------------------------------------"

for batch in {28..41}; do
    results_file="test/test_results_batch${batch}/results.csv"
    if [ -f "$results_file" ]; then
        echo "批次 ${batch}:"
        tail -n +2 "$results_file" | awk -F, '{print "  " $1 ": " $2}' | head -5
        if [ $(tail -n +2 "$results_file" | wc -l) -gt 5 ]; then
            echo "  ... (更多策略)"
        fi
        echo ""
    fi
done

echo "📊 统计汇总:"
echo "--------------------------------------"
total_load_errors=0
total_batches=0

for batch in {28..41}; do
    results_file="test/test_results_batch${batch}/results.csv"
    if [ -f "$results_file" ]; then
        batch_load_errors=$(tail -n +2 "$results_file" | grep -c "LOAD_ERROR")
        total_load_errors=$((total_load_errors + batch_load_errors))
        total_batches=$((total_batches + 1))
        
        echo "批次 ${batch}: ${batch_load_errors}/10 LOAD_ERROR"
    fi
done

echo ""
echo "📈 总计:"
echo "  测试批次: ${total_batches}"
echo "  总策略数: $((total_batches * 10))"
echo "  LOAD_ERROR 策略数: ${total_load_errors}"
echo "  通过率: $((100 - (total_load_errors * 100 / (total_batches * 10))))%"