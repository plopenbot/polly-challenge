#!/usr/bin/env python3
"""
从神奇宝贝百科抓取 #392-1025 的宝可梦中文名称
"""

import json
import re
import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser

class PokemonTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pokemon_data = {}
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_tag = None
        self.current_id = None
        self.current_name = None
        self.cell_count = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            # 查找包含宝可梦列表的表格
            for attr, value in attrs:
                if attr == 'class' and 'roundy' in value:
                    self.in_table = True
                    
        elif tag == 'tr' and self.in_table:
            self.in_row = True
            self.cell_count = 0
            
        elif tag in ['td', 'th'] and self.in_row:
            self.in_cell = True
            self.cell_count += 1
            
        elif tag == 'a' and self.in_cell:
            # 提取链接中的宝可梦名称
            for attr, value in attrs:
                if attr == 'title':
                    self.current_name = value
                    
    def handle_data(self, data):
        if self.in_cell and self.cell_count == 1:
            # 第一列是编号
            data = data.strip()
            if data.startswith('#') and data[1:].isdigit():
                self.current_id = int(data[1:])
                
    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
            
        elif tag == 'tr':
            # 行结束，保存数据
            if self.current_id and self.current_name and 392 <= self.current_id <= 1025:
                # 只保留宝可梦名称，去除括号内容（如地区形态）
                clean_name = re.sub(r'（.*?）', '', self.current_name)
                clean_name = re.sub(r'\(.*?\)', '', clean_name)
                self.pokemon_data[self.current_id] = clean_name.strip()
            
            self.in_row = False
            self.current_id = None
            self.current_name = None
            
        elif tag in ['td', 'th']:
            self.in_cell = False

def fetch_pokemon_data():
    """从神奇宝贝百科获取宝可梦数据"""
    # URL编码中文部分
    base_url = 'https://wiki.52poke.com/wiki/'
    page_name = urllib.parse.quote('宝可梦列表（按全国图鉴编号）')
    url = base_url + page_name
    
    try:
        print(f"正在获取数据...")
        
        # 设置请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8')
            
        # 解析 HTML
        parser = PokemonTableParser()
        parser.feed(html)
        
        return parser.pokemon_data
        
    except urllib.error.URLError as e:
        print(f"网络错误: {e}")
        return {}
    except Exception as e:
        print(f"解析错误: {e}")
        import traceback
        traceback.print_exc()
        return {}

def main():
    print("开始抓取宝可梦数据...")
    pokemon_data = fetch_pokemon_data()
    
    if not pokemon_data:
        print("❌ 未能获取数据")
        return
    
    print(f"\n✅ 成功获取 {len(pokemon_data)} 只宝可梦数据")
    print(f"范围: #{min(pokemon_data.keys())} - #{max(pokemon_data.keys())}")
    
    # 保存为 JSON
    output_file = '/root/.openclaw/workspace/math-challenge-grade4/pokemon_392_1025.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 已保存到: {output_file}")
    
    # 显示前10个示例
    print("\n📋 数据示例:")
    for i, (pid, name) in enumerate(sorted(pokemon_data.items())[:10]):
        print(f"  #{pid}: {name}")
    
    print("\n...")
    
    # 显示最后10个
    for i, (pid, name) in enumerate(sorted(pokemon_data.items())[-10:]):
        print(f"  #{pid}: {name}")

if __name__ == '__main__':
    main()
