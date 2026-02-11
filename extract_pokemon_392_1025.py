#!/usr/bin/env python3
"""
从全国图鉴数据中提取 #392-1025 的宝可梦中文名称
"""

import json

def extract_pokemon_names():
    # 读取全国图鉴数据
    with open('national_pokedex.json', 'r', encoding='utf-8') as f:
        pokedex = json.load(f)
    
    # 提取 #392-1025 的宝可梦
    pokemon_392_1025 = {}
    
    for pokemon in pokedex:
        pid = int(pokemon['id'])
        if 392 <= pid <= 1025:
            pokemon_392_1025[str(pid)] = {
                "name": pokemon['name'],
                "desc": f"属性：{'/'.join(pokemon['types'])}"
            }
    
    print(f"✅ 提取了 {len(pokemon_392_1025)} 只宝可梦")
    print(f"范围: #{min(map(int, pokemon_392_1025.keys()))} - #{max(map(int, pokemon_392_1025.keys()))}")
    
    # 读取现有的 pokemon-zh-data.js
    with open('pokemon-zh-data.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找现有数据的结尾（最后一个 "xxx": { } 之后）
    # 我们需要在最后的 } 之前插入新数据
    
    # 找到最后一个数据项
    import re
    
    # 提取现有的所有编号
    existing_pattern = r'"(\d+)":\s*{[^}]+}'
    existing_ids = [int(m.group(1)) for m in re.finditer(existing_pattern, content)]
    
    if existing_ids:
        last_id = max(existing_ids)
        print(f"现有数据最后编号: #{last_id}")
    else:
        print("⚠️ 未找到现有数据")
        last_id = 0
    
    # 生成新数据的 JavaScript 对象字符串
    new_entries = []
    for pid in sorted(pokemon_392_1025.keys(), key=int):
        if int(pid) > last_id:
            pokemon = pokemon_392_1025[pid]
            entry = f'    "{pid}": {{\n        "name": "{pokemon["name"]}",\n        "desc": "{pokemon["desc"]}"\n    }}'
            new_entries.append(entry)
    
    if not new_entries:
        print("⚠️ 没有需要添加的新数据")
        return
    
    print(f"需要添加 {len(new_entries)} 条新数据")
    
    # 在文件最后的 }; 之前插入新数据
    # 找到最后一个完整的数据项
    last_item_pattern = r'("' + str(last_id) + r'":\s*{[^}]+})'
    match = re.search(last_item_pattern, content)
    
    if match:
        # 在匹配项之后插入逗号和新数据
        insert_pos = match.end()
        
        new_data_str = ',\n' + ',\n'.join(new_entries)
        
        new_content = content[:insert_pos] + new_data_str + content[insert_pos:]
        
        # 保存更新后的文件
        with open('pokemon-zh-data.js', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"\n✅ 已更新 pokemon-zh-data.js")
        print(f"添加了 #{last_id+1} 到 #{max(map(int, pokemon_392_1025.keys()))} 的数据")
        
        # 显示前5个和后5个示例
        print("\n📋 新增数据示例（前5个）:")
        for entry in new_entries[:5]:
            pid = entry.split('"')[1]
            name = pokemon_392_1025[pid]['name']
            print(f"  #{pid}: {name}")
        
        print("\n📋 新增数据示例（后5个）:")
        for entry in new_entries[-5:]:
            pid = entry.split('"')[1]
            name = pokemon_392_1025[pid]['name']
            print(f"  #{pid}: {name}")
    else:
        print("⚠️ 无法找到插入位置")

if __name__ == '__main__':
    extract_pokemon_names()
