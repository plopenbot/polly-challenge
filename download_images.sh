#!/bin/bash
cd "$(dirname "$0")"
img_dir="pokemon_images"

# 下载100个示例图片（测试）
echo "开始下载宝可梦图片..."
total=1025
concurrent=50  # 并发下载数量

for i in $(seq 1 $total); do
    (
        # 普通形态
        url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${i}.png"
        wget -q -nc -O "${img_dir}/${i}.png" "$url" 2>/dev/null
        # 闪光形态  
        url="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/${i}.png"
        wget -q -nc -O "${img_dir}/${i}_shiny.png" "$url" 2>/dev/null
    ) &
    
    # 控制并发数
    if (( i % concurrent == 0 )); then
        wait
        echo "已下载: $i/$total"
    fi
done

wait
echo "🎉 所有图片下载完成"

# 检查缺失情况
missing=0
for i in $(seq 1 $total); do
    if [[ ! -f "${img_dir}/${i}.png" ]]; then
        missing=$((missing + 1))
        echo "❌ 图片缺失: #${i}"
    fi
done

echo "📊 结果统计："
echo "   总数：$total"
echo "   已下载：$((total - missing))"
echo "   缺失：$missing"
