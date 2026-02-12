#!/bin/bash
# 宝可梦项目完整迁移脚本
# 作者：OpenClaw助手
# 用途：将项目从plopenbot迁移到你的GitHub仓库

echo "🎮 宝可梦项目完整迁移工具"
echo "=================================="
echo ""
echo "📋 功能:"
echo "1. 批量下载所有图片到本地"
echo "2. 创建新的数据文件（指向你的GitHub）"
echo "3. 生成GitHub推送指南"
echo ""
read -p "请输入你的GitHub用户名（例如pispeng）: " GITHUB_USER
read -p "请输入你的仓库名（建议: polly-challenge）: " GITHUB_REPO

echo ""
echo "📊 开始准备迁移..."
echo ""
echo "🌟 步骤1: 下载所有宝可梦图片..."

# 确保目录存在
mkdir -p images/complete_regular
mkdir -p images/complete_shiny

# 创建批量下载脚本
cat > download_all_images.js << 'EOF'
const fs = require('fs');
const https = require('https');

// 读取数据
const rawData = fs.readFileSync('pokemon-zh-data.js', 'utf8');
const dataMatch = rawData.match(/const pokemonZhData = \[(.*?)\];/s);

if (!dataMatch) {
  console.error('无法提取数据');
  process.exit(1);
}

// 解析数据
const evalStr = '[' + dataMatch[1].replace(/'/g, '"') + ']';
const pokemonData = JSON.parse(evalStr);

console.log(`找到 ${pokemonData.length} 条宝可梦数据`);

// 提取URL
const regularUrls = [];
const shinyUrls = [];

pokemonData.forEach((p, index) => {
  const id = index + 1;
  
  if (Array.isArray(p) && p.length >= 5) {
    const regularUrl = p[3];
    const shinyUrl = p.length > 4 ? p[4] : null;
    
    if (regularUrl && regularUrl !== 'N/A') {
      regularUrls.push({ id, url: regularUrl });
    }
    if (shinyUrl && shinyUrl !== 'N/A') {
      shinyUrls.push({ id, url: shinyUrl });
    }
  }
});

console.log(`需要下载: ${regularUrls.length} 普通图片, ${shinyUrls.length} 闪亮图片`);

// 简单的顺序下载（前50个）
let downloaded = 0;
const downloadNext = (type, list) => {
  if (list.length === 0) return;
  
  const item = list.shift();
  const filename = type === 'regular' 
    ? `images/complete_regular/${item.id.toString().padStart(4, '0')}.png`
    : `images/complete_shiny/${item.id.toString().padStart(4, '0')}.png`;
  
  if (fs.existsSync(filename)) {
    downloaded++;
    console.log(`[${downloaded}] ✅ ${item.id} 已存在`);
    setTimeout(() => downloadNext(type, list), 100);
    return;
  }
  
  const file = fs.createWriteStream(filename);
  https.get(item.url, (response) => {
    response.pipe(file);
    file.on('finish', () => {
      file.close();
      downloaded++;
      console.log(`[${downloaded}] ✅ 下载 ${item.id} (${type})`);
      setTimeout(() => downloadNext(type, list), 300);
    });
  }).on('error', (err) => {
    console.log(`[${downloaded}] ❌ 下载失败 ${item.id}: ${err.message}`);
    setTimeout(() => downloadNext(type, list), 100);
  });
};

// 先下载普通图片
console.log('开始下载普通图片...');
downloadNext('regular', regularUrls.slice(0, 50));

EOF

echo "📝 已创建下载脚本（先下载前50个）"
echo "执行下载..."
node download_all_images.js || echo "下载可能部分失败，继续下一步..."

echo ""
echo "🌟 步骤2: 创建替换后的数据文件..."
echo ""
echo "📦 正在生成 pokemon-zh-data-local.js ..."

# 创建Python脚本来生成本地版本
python3 << EOF
import json
import re

# 读取原始文件
with open('pokemon-zh-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换所有图片地址
new_content = re.sub(
    r'https://raw\.githubusercontent\.com/plopenbot/polly-challenge/main/',
    f'https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/',
    content
)

# 保存新文件
with open('pokemon-zh-data-local.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ 已生成: pokemon-zh-data-local.js")
print(f"🔗 所有图片地址已替换为: https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/")
EOF

echo ""
echo "🌟 步骤3: 创建GitHub推送指南..."
echo ""
cat > GITHUB_SETUP.md << EOF
# 🚀 GitHub部署指南

## 1. 创建新仓库
访问 https://github.com/new 创建新仓库：
- 仓库名: ${GITHUB_REPO}
- 描述: "Polly Challenge - 宝可梦答题游戏"
- 选择公开
- **不要**初始化README、.gitignore或许可证

## 2. 推送代码
\`\`\`bash
# 初始化git（如果还没做）
git init

# 添加所有文件
git add .

# 提交
git commit -m "迁移宝可梦项目到${GITHUB_USER}账户"

# 添加远程仓库（替换下面的命令）
git remote add origin https://github.com/${GITHUB_USER}/${GITHUB_REPO}

# 推送
git push -u origin main
\`\`\`

## 3. 更新游戏文件
**重要**: 你需要更新游戏文件以使用新的图片地址：

### 方法A（推荐）: 手动替换
\`\`\`bash
# 备份原文件
cp game.js game.js.original

# 使用sed替换
sed -i "s|https://raw\\.githubusercontent\\.com/plopenbot/polly-challenge/main/|https://raw\\.githubusercontent\\.com/${GITHUB_USER}/${GITHUB_REPO}/main/|g" game.js
\`\`\`

### 方法B: 替换数据文件
将 \`pokemon-zh-data.js\` 替换为 \`pokemon-zh-data-local.js\`：
\`\`\`bash
mv pokemon-zh-data-local.js pokemon-zh-data.js
\`\`\`

## 4. 测试游戏
重新部署游戏，现在所有宝可梦图片应该从你的GitHub加载：
\`\`\`bash
open index.html
# 或上传到GitHub Pages
\`\`\`

## 5. GitHub Pages部署（可选）
1. 进入仓库设置 → Pages
2. 选择分支: main
3. 选择文件夹: / (根目录)
4. 保存，等待几分钟后访问：https://${GITHUB_USER}.github.io/${GITHUB_REPO}/

## 文件结构说明
\`\`\`
${GITHUB_REPO}/
├── images/                    # 所有宝可梦图片
│   ├── complete_regular/      # 普通图片（0001.png, 0002.png...）
│   └── complete_shiny/        # 闪亮图片（0001.png, 0002.png...）
├── index.html                 # 主页面
├── game.js                    # 游戏逻辑
├── pokemon-zh-data.js        # 宝可梦数据
├── pokemon-zh-data-local.js  # 已替换地址的版本（备用）
└── questions.js              # 题目数据
\`\`\`

## 注意事项
1. 图片文件较多（1025×2 = 2050张），首次推送可能需要耐心
2. 中国大陆访问GitHub图片可能仍有延迟，但比原地址稳定
3. 如果游戏依然有图片显示问题，需要进一步修改图片加载逻辑
EOF

echo "✅ 已创建: GITHUB_SETUP.md"
echo ""
echo "🌟 步骤4: 创建一键推送脚本..."
cat > push_to_github.sh << EOF
#!/bin/bash
# 一键推送到GitHub
echo "🚀 推送宝可梦项目到你的GitHub..."

# 检查是否已初始化git
if [ ! -d ".git" ]; then
    echo "初始化Git仓库..."
    git init
    git add .
    git commit -m "迁移宝可梦项目到GitHub"
fi

# 添加远程仓库
REMOTE_URL="https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"
echo "添加远程仓库: \$REMOTE_URL"
git remote add origin \$REMOTE_URL 2>/dev/null || git remote set-url origin \$REMOTE_URL

# 推送
echo "推送代码..."
git push -u origin main 2>&1 || git push -u origin master 2>&1 || {
    echo "📋 推送失败，请手动执行以下命令:"
    echo "git push -u origin main"
    echo ""
    echo "📋 或查看GITHUB_SETUP.md获取详细指南"
}

echo ""
echo "🎉 完成！请查看GITHUB_SETUP.md获取后续步骤"
EOF

chmod +x push_to_github.sh
echo "✅ 已创建: push_to_github.sh"
echo ""
echo "📋 项目迁移完成！"
echo ""
echo "🚀 下一步操作:"
echo "1. 📖 查看 GITHUB_SETUP.md 获取详细部署指南"
echo "2. 📤 运行 ./push_to_github.sh 推送到GitHub"
echo "3. 🔧 更新游戏文件中的图片地址"
echo "4. 🎮 测试游戏是否正常显示图片"
echo ""
echo "💡 提示: 如果推送到GitHub遇到认证问题，可以使用GitHub Token:"
echo "git remote set-url origin https://<YOUR_TOKEN>@github.com/${GITHUB_USER}/${GITHUB_REPO}"
echo ""
echo "=================================="
echo "✅ 迁移工具已完成所有准备工作！"