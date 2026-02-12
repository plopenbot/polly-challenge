
#!/bin/bash
# 自动替换宝可梦图片地址为本地GitHub地址
# 用法: ./replace_image_urls.sh [你的GitHub用户名]

GITHUB_USER=${1:-pispeng}  # 默认为pispeng
GITHUB_REPO="polly-challenge"  # 你的仓库名

echo "🔄 替换宝可梦图片地址到 https://raw.githubusercontent.com/$GITHUB_USER/$GITHUB_REPO/main/images/"

# 备份原文件
cp pokemon-zh-data.js pokemon-zh-data.js.backup
echo "📦 已备份: pokemon-zh-data.js.backup"

# 创建替换版本
python3 -c "
import json
import re

# 读取数据
with open('pokemon-zh-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到数据部分
start = content.find('const pokemonZhData = [')
end = content.rfind('];') + 1

if start != -1 and end != -1:
    data_str = content[start+len('const pokemonZhData = ['):end-1]
    
    # 替换地址
    new_data = re.sub(
        r'https://raw\.githubusercontent\.com/plopenbot/polly-challenge/main/',
        'https://raw.githubusercontent.com/$GITHUB_USER/$GITHUB_REPO/main/',
        data_str
    )
    
    # 重新组装
    new_content = content[:start+len('const pokemonZhData = [')] + new_data + content[end-1:]
    
    with open('pokemon-zh-data-local.js', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print('✅ 已生成: pokemon-zh-data-local.js')
    print('🔗 所有图片地址已替换为你的GitHub仓库')
else:
    print('❌ 找不到数据数组')
"

echo ""
echo "📋 下一步操作:"
echo "1. 将 images/ 目录推送到你的GitHub仓库"
echo "2. 使用 pokemon-zh-data-local.js 替换原文件"
echo "3. 测试游戏确保图片正常加载"
