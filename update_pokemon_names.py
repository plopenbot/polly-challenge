#!/usr/bin/env python3
"""
用真实的中文名称替换 #392-1025 的默认占位符
"""

import json
import re

def update_pokemon_names():
    # 读取全国图鉴数据
    print("📖 读取全国图鉴数据...")
    with open('national_pokedex.json', 'r', encoding='utf-8') as f:
        pokedex = json.load(f)
    
    # 构建编号到名称的映射
    pokemon_map = {}
    for pokemon in pokedex:
        pid = int(pokemon['id'])
        if 392 <= pid <= 1025:
            pokemon_map[pid] = {
                "name": pokemon['name'],
                "types": '/'.join(pokemon['types'])
            }
    
    print(f"✅ 从图鉴提取了 {len(pokemon_map)} 只宝可梦")
    
    # 读取现有的 pokemon-zh-data.js
    print("\n📖 读取现有的 pokemon-zh-data.js...")
    with open('pokemon-zh-data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 统计需要更新的数量
    update_count = 0
    
    # 替换所有 #392-1025 的默认名称
    for pid in range(392, 1026):
        if pid in pokemon_map:
            pokemon = pokemon_map[pid]
            
            # 查找并替换模式：
            # "392": {
            #     "name": "宝可梦 #392"
            # },
            old_pattern = rf'"{pid}":\s*{{\s*"name":\s*"宝可梦 #{pid}"\s*}}'
            
            # 新内容（带描述）
            new_entry = f'"{pid}": {{\n        "name": "{pokemon["name"]}",\n        "desc": "属性：{pokemon["types"]}"\n    }}'
            
            # 替换
            new_content = re.sub(old_pattern, new_entry, content)
            
            if new_content != content:
                update_count += 1
                content = new_content
    
    print(f"✅ 更新了 {update_count} 只宝可梦的名称")
    
    # 保存更新后的文件
    with open('pokemon-zh-data.js', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n💾 已保存到 pokemon-zh-data.js")
    
    # 验证更新
    print("\n🔍 验证更新结果（随机抽取10个）:")
    import random
    sample_ids = sorted(random.sample(range(392, 1026), min(10, len(pokemon_map))))
    
    for pid in sample_ids:
        match = re.search(rf'"{pid}":\s*{{[^}}]+}}', content)
        if match:
            print(f"  #{pid}: {match.group(0)[:100]}...")

if __name__ == '__main__':
    update_pokemon_names()
