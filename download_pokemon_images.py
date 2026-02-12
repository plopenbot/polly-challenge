#!/usr/bin/env python3
"""
批量下载宝可梦图片到本地
"""

import json
import requests
import os
import time
import concurrent.futures

def extract_urls_from_data():
    """从pokemon-zh-data.js中提取图片URL"""
    print("📊 读取宝可梦数据...")
    
    try:
        with open('pokemon-zh-data.js', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 查找数据数组
        start_idx = content.find('const pokemonZhData = [')
        end_idx = content.rfind('];') + 1
        
        if start_idx != -1 and end_idx != -1:
            data_str = content[start_idx + len('const pokemonZhData = ['):end_idx]
            # 转换为有效的JSON
            data_str = data_str.strip()
            
            # 替换单引号为双引号（JavaScript）
            import re
            data_str = re.sub(r",\s*\n\]", "\n]", data_str)
            
            try:
                pokemon_data = json.loads(data_str)
            except:
                # 尝试修复
                data_str = data_str.replace("'", '"')
                data_str = re.sub(r',\s+', ', ', data_str)
                pokemon_data = json.loads(data_str)
                
            print(f"✅ 从JS文件解析了 {len(pokemon_data)} 条数据")
        else:
            # 使用JSON文件
            with open('pokemon_verification.json', 'r', encoding='utf-8') as f:
                pokemon_data = json.load(f)
            print(f"✅ 从JSON文件读取了 {len(pokemon_data)} 条数据")
    except Exception as e:
        print(f"❌ 读取数据失败: {e}")
        return None
    
    # 提取URL
    image_urls = []
    shiny_urls = []
    
    for i, pokemon in enumerate(pokemon_data[:200]):  # 先处理200个
        img_url = None
        shiny_url = None
        
        if isinstance(pokemon, dict):
            img_url = pokemon.get('imageUrl') or pokemon.get('image')
            shiny_url = pokemon.get('shinyUrl') or pokemon.get('shiny')
        elif isinstance(pokemon, list) and len(pokemon) >= 5:
            img_url = pokemon[3] if pokemon[3] != 'N/A' else None
            shiny_url = pokemon[4] if len(pokemon) > 4 and pokemon[4] != 'N/A' else None
        
        if img_url and 'raw.githubusercontent.com' in img_url:
            image_urls.append((i+1, img_url))
        
        if shiny_url and 'raw.githubusercontent.com' in shiny_url:
            shiny_urls.append((i+1, shiny_url))
    
    return {
        'regular': image_urls,
        'shiny': shiny_urls,
        'total': len(pokemon_data)
    }

def download_image(id_num, url, folder):
    """下载单个图片"""
    file_name = f"{folder}/{id_num:04d}.png"
    
    # 如果文件已存在，跳过
    if os.path.exists(file_name):
        return True, file_name
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)
            return True, file_name
        else:
            print(f"❌ HTTP {response.status_code}: {url}")
            return False, url
    except Exception as e:
        print(f"❌ 下载失败 {id_num}: {e}")
        return False, url

def main():
    print("🚀 开始宝可梦图片下载任务")
    print("=" * 50)
    
    # 确保目录存在
    os.makedirs('images/regular', exist_ok=True)
    os.makedirs('images/shiny', exist_ok=True)
    
    # 提取URL
    urls_data = extract_urls_from_data()
    if not urls_data:
        return
    
    print(f"📷 发现图片: {len(urls_data['regular'])} 普通 + {len(urls_data['shiny'])} 闪亮")
    
    # 先测试下载10个
    test_count = 10
    print(f"🔧 先测试下载前 {test_count} 个图片...")
    
    # 下载普通图片
    success_count = 0
    for i, (id_num, url) in enumerate(urls_data['regular'][:test_count]):
        print(f"({i+1}/{test_count}) 下载 #{id_num} ...")
        success, result = download_image(id_num, url, 'images/regular')
        if success:
            success_count += 1
            print(f"   ✅ 已保存: {result}")
        time.sleep(0.5)  # 避免过快请求
    
    # 下载闪亮图片
    shiny_success = 0
    for i, (id_num, url) in enumerate(urls_data['shiny'][:min(5, len(urls_data['shiny']))]):
        print(f"({i+1}/5) 下载闪光 #{id_num} ...")
        success, result = download_image(id_num, url, 'images/shiny')
        if success:
            shiny_success += 1
            print(f"   ✨ 已保存闪亮: {result}")
        time.sleep(0.5)
    
    print("=" * 50)
    print(f"📊 下载结果:")
    print(f"   ✅ 普通图片: {success_count}/{test_count} 成功")
    print(f"   ✨ 闪亮图片: {shiny_success}/5 成功")
    
    if success_count > 0:
        # 创建替换脚本
        create_replacement_script()
    else:
        print("❌ 测试下载失败，请检查网络连接")

def create_replacement_script():
    """创建数据文件替换脚本"""
    script = """
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
"""
    
    with open('replace_image_urls.sh', 'w', encoding='utf-8') as f:
        f.write(script)
    
    os.chmod('replace_image_urls.sh', 0o755)
    print("📝 已创建替换脚本: replace_image_urls.sh")

if __name__ == '__main__':
    main()